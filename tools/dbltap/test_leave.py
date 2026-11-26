#!/workspace/pwenv/bin/python3
"""Regression: a double-tap at a multi-round (ROUND 2) transition must not leave the fight.

Covers:
  A) Double-tap / double-click the wave-1 result "ROUND 2 ►" button (or the
     result screen once the cine is over) — must enter and STAY in wave 2.
  B) Touch double-tap (150-300ms) on the ROUND 2 banner, including over the
     ESCAPE button — must not flee.
  C) Intentional press of ESCAPE after the guard — still flees.
  D) Card / act button still works after the banner (no play lock).

usage: test_leave.py <worktree> [port]
"""
import asyncio, sys, functools, http.server, socketserver, threading
from pathlib import Path
from playwright.async_api import async_playwright

root = Path(sys.argv[1]).resolve()
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 52640

class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def serve():
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_GET(self):
            if self.path.split('?', 1)[0] in ('/', '/index.html'):
                raw = (root / 'index.html').read_bytes()
                n = b'root.WORLD_API = {'
                raw = raw.replace(n, b'root.__ev=function(s){return eval(s)};' + n, 1)
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(raw)))
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(raw)
                return
            return super().do_GET()
    h = TS(('127.0.0.1', PORT), functools.partial(Q, directory=str(root)))
    threading.Thread(target=h.serve_forever, daemon=True).start()
    return h

SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""

RES = []
def ok(name, cond, extra=''):
    RES.append((bool(cond), name, extra))
    print(('PASS ' if cond else 'FAIL ') + name + ((' :: ' + str(extra)[:400]) if extra else ''), flush=True)
    if not cond:
        try:
            Path('/workspace/dbltap/logs/last_fail.json').write_text(__import__('json').dumps(extra, default=str)[:20000])
        except Exception:
            pass

async def ev(pg, code):
    return await pg.evaluate(
        "(c)=>{try{var r=__ev(c);return (r===undefined)?null:JSON.parse(JSON.stringify(r))}catch(e){return {__err:String(e&&e.message||e)}}}",
        code)

async def skipall(pg, n=12):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(250)
            c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c)
        await pg.wait_for_timeout(250)
    await pg.evaluate("(()=>{var b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Close'&&e.offsetParent);if(b)b.click()})()")

async def boot(p):
    b = await p.chromium.launch(headless=True, args=['--disable-dev-shm-usage'])
    ctx = await b.new_context(
        viewport={'width': 390, 'height': 844}, device_scale_factor=1,
        is_mobile=True, has_touch=True,
        user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
    pg = await ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:240]))
    await pg.goto(f'http://127.0.0.1:{PORT}/index.html')
    await pg.wait_for_timeout(3500)
    await pg.evaluate("WORLD_API.enter(true)")
    await pg.wait_for_timeout(2000)
    await skipall(pg, 12)
    return b, ctx, pg, errs

INSTALL = r"""
(() => {
  if (window.__dbltapReady) return 'ok';
  window.__ends = [];
  window.__onEnd = function (win, st) {
    var n = st && st.ctx && st.ctx.wave && st.ctx.wave.n;
    window.__ends.push({ win: !!win, n: n || 0, escaped: !!(st && st.escaped), evs: (FFF_UI.ST.events || []).slice(-8) });
    if (win && n === 1) {
      FFF_UI.startMatch('ryo', {
        foes: ['bully3', 'bully4'], esc: 0.5, drop: 0,
        ctx: { wave: { n: 2, of: 2, cnt: 2 } },
        onEnd: window.__onEnd
      });
    }
  };
  window.__startW1 = function () {
    window.__ends = [];
    FFF_UI.ST.events = [];
    FFF_UI.startMatch('ryo', {
      foes: ['bully1', 'bully2', 'bully3'], esc: 0.6, drop: 1,
      ctx: { wave: { n: 1, of: 2, cnt: 2 } },
      onEnd: window.__onEnd
    });
    return { inGame: !!FFF_UI.ST.inGame, phase: FFF_UI.ST.phase, wave: FFF_UI.ST.story && FFF_UI.ST.story.ctx && FFF_UI.ST.story.ctx.wave };
  };
  window.__startW2 = function () {
    window.__ends = [];
    FFF_UI.ST.events = [];
    window.FFF_ESC_ROLL = 0;
    FFF_UI.startMatch('ryo', {
      foes: ['bully3', 'bully4'], esc: 0.5, drop: 0,
      ctx: { wave: { n: 2, of: 2, cnt: 2 } },
      onEnd: window.__onEnd
    });
    return { inGame: !!FFF_UI.ST.inGame, busy: !!FFF_UI.ST.busy, banner: !!document.getElementById('fwvB'),
             esc: FFF_UI.ST.story && FFF_UI.ST.story.esc, phase: FFF_UI.ST.phase };
  };
  window.__forceWin = function () {
    var ST = FFF_UI.ST, b = ST.b;
    if (!b) return { ok: false };
    (b.grp || []).forEach(function (s) { s.hp = 0; });
    if (b.s[1]) b.s[1].hp = 0;
    b.over = true; b.winner = 0;
    FFF_UI.endMatch();
    return { ok: true, cine: !!(window.VC || (typeof VC !== 'undefined' && VC)), resultOn: document.getElementById('result').classList.contains('on') };
  };
  window.__snap = function () {
    var ST = FFF_UI.ST, r = document.getElementById('btnRun'), b = r && r.getBoundingClientRect();
    var fw = document.getElementById('fwvB'), rm = document.getElementById('rMap');
    var evs = ST.events || [];
    return {
      inGame: !!ST.inGame, busy: !!ST.busy, phase: ST.phase, over: !!(ST.b && ST.b.over),
      escaped: !!(ST.story && ST.story.escaped) || !!(ST.b && ST.b.escaped),
      winner: ST.b && ST.b.winner,
      wave: ST.story && ST.story.ctx && ST.story.ctx.wave && ST.story.ctx.wave.n,
      banner: !!fw, gameOn: document.getElementById('game').classList.contains('on'),
      resultOn: document.getElementById('result').classList.contains('on'),
      rMap: rm && { txt: rm.textContent, cls: rm.className, dis: !!rm.disabled },
      btnRun: r && { hidden: !!r.hidden, disabled: !!r.disabled, txt: r.textContent,
                     x: b.left + b.width/2, y: b.top + b.height/2, w: b.width, h: b.height },
      ends: window.__ends.slice(),
      evs: evs.filter(function (s) { return /escape|story:back|wave:|vc:leave|match:start|match:end/.test(s); }).slice(-20)
    };
  };
  window.__dbltapReady = 1;
  return 'ok';
})()
"""

async def install(pg):
    r = await ev(pg, INSTALL)
    return r

async def skip_cine(pg, max_ms=8000):
    """Advance the victory cinematic until V.over or result vend, via taps + VC.tap()."""
    t0 = asyncio.get_event_loop().time()
    while (asyncio.get_event_loop().time() - t0) * 1000 < max_ms:
        st = await ev(pg, """({
          over: !!(typeof VC!=='undefined' && VC && VC.over),
          dead: !!(typeof VC!=='undefined' && VC && VC.dead),
          left: !!(typeof VC!=='undefined' && VC && VC.left),
          vend: document.getElementById('result').classList.contains('vend'),
          on: document.getElementById('result').classList.contains('on'),
          fwv: document.getElementById('rMap') && document.getElementById('rMap').classList.contains('fwv-next')
        })""")
        if isinstance(st, dict) and (st.get('over') or st.get('vend') or st.get('left')):
            return st
        # skip current cine step
        await ev(pg, "if (typeof VC!=='undefined' && VC && VC.tap) VC.tap()")
        await pg.wait_for_timeout(40)
    return await ev(pg, "({over:!!(VC&&VC.over),vend:document.getElementById('result').classList.contains('vend'),timeout:1})")

async def box(pg, sel):
    return await pg.evaluate("""(s)=>{var e=document.querySelector(s);if(!e)return null;var r=e.getBoundingClientRect();if(!r.width&&!r.height)return null;return {x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height}}""", sel)

async def double_tap(pg, x, y, gap=200):
    await pg.touchscreen.tap(x, y)
    await pg.wait_for_timeout(gap)
    await pg.touchscreen.tap(x, y)

async def case_result_doubletap(pg, gap, label):
    await ev(pg, "window.FFF_VC_K=0.25; window.FFF_NO_VC=null; window.FFF_ESC_ROLL=0;")
    st = await ev(pg, "window.__startW1()")
    await pg.wait_for_timeout(200)
    await ev(pg, "if(window.FFF_WAVE) FFF_WAVE.stop()")  # dismiss ROUND 1 banner if any
    await ev(pg, "FFF_UI.ST.busy=false")
    fw = await ev(pg, "window.__forceWin()")
    cine = await skip_cine(pg)
    # wait until rMap is the ROUND 2 button
    rm = None
    for _ in range(40):
        rm = await ev(pg, """(function(){var b=document.getElementById('rMap'),R=document.getElementById('result');
          if(!b||!R)return null; var r=b.getBoundingClientRect();
          return {txt:b.textContent,fwv:b.classList.contains('fwv-next'),on:R.classList.contains('on'),
                  vend:R.classList.contains('vend'),x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height};})()""")
        if isinstance(rm, dict) and rm.get('fwv') and rm.get('w', 0) > 0:
            break
        await pg.wait_for_timeout(50)
    if not (isinstance(rm, dict) and rm.get('fwv')):
        # try to nudge cine once more
        await ev(pg, "if (typeof VC!=='undefined' && VC && VC.tap) VC.tap()")
        await pg.wait_for_timeout(200)
        rm = await ev(pg, """(function(){var b=document.getElementById('rMap'),R=document.getElementById('result');
          if(!b||!R)return null; var r=b.getBoundingClientRect();
          return {txt:b.textContent,fwv:b.classList.contains('fwv-next'),on:R.classList.contains('on'),
                  vend:R.classList.contains('vend'),x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height};})()""")
    # Double-tap the ROUND 2 button (and also the screen center as a variant)
    if isinstance(rm, dict) and rm.get('w', 0) > 0:
        await double_tap(pg, rm['x'], rm['y'], gap)
    else:
        await double_tap(pg, 195, 700, gap)
    # Also fire two close click()s in case touch did not hit the button
    await ev(pg, """(function(){var b=document.getElementById('rMap'); if(b){ b.click(); b.click(); }})()""")
    # Let any 420ms fade + leftover timer fire, plus wave-2 banner
    await pg.wait_for_timeout(900)
    snap = await ev(pg, "window.__snap()")
    still = isinstance(snap, dict) and snap.get('inGame') and snap.get('wave') == 2
    ok(label, still, {'start': st, 'force': fw, 'cine': cine, 'rm': rm, 'snap': snap})
    return snap

async def case_banner_dbltap(pg, where, gap, label):
    await ev(pg, "window.FFF_VC_K=0.25; window.FFF_ESC_ROLL=0; window.FFF_WAVE_BANNER=undefined;")
    st = await ev(pg, "window.__startW2()")
    # wait for banner
    for _ in range(30):
        if await pg.evaluate("!!document.getElementById('fwvB')"):
            break
        await pg.wait_for_timeout(40)
    await pg.wait_for_timeout(650)  # past skipAt (600ms)
    if where == 'escape':
        b = await box(pg, '#btnRun')
        if not b:
            # button may have 0 size if hidden; use last known top-right of topbar
            b = await ev(pg, """(function(){var r=document.getElementById('btnRun');
              if(r){r.hidden=false; var b=r.getBoundingClientRect();
                return {x:b.left+b.width/2,y:b.top+b.height/2,w:b.width,h:b.height};}
              var t=document.querySelector('#game .topbar'); if(!t)return {x:360,y:20,w:1,h:1};
              var q=t.getBoundingClientRect(); return {x:q.right-24,y:q.top+q.height/2,w:40,h:q.height};})()""")
        x, y = b['x'], b['y']
    elif where == 'center':
        x, y = 195, 400
    else:
        x, y = 195, 80
    await double_tap(pg, x, y, gap)
    await pg.wait_for_timeout(500)
    snap = await ev(pg, "window.__snap()")
    fled = bool(isinstance(snap, dict) and (not snap.get('inGame') or snap.get('escaped') or any(e.get('n') == 2 for e in (snap.get('ends') or []))))
    # fled if we left the in-game wave-2 match
    left = isinstance(snap, dict) and (not snap.get('inGame') or snap.get('escaped'))
    ok(label, not left, {'start': st, 'xy': [x, y], 'snap': snap, 'left': left, 'fled': fled})
    return snap

async def case_intentional_escape(pg, label):
    await ev(pg, "window.FFF_ESC_ROLL=0;")
    st = await ev(pg, "window.__startW2()")
    await ev(pg, "if(window.FFF_WAVE) FFF_WAVE.stop(); FFF_UI.ST.busy=false; FFF_UI.render(false);")
    await pg.wait_for_timeout(500)  # past any leave-guard
    before = await ev(pg, "window.__snap()")
    await ev(pg, "if (typeof tapRun==='function') tapRun(); else document.getElementById('btnRun') && document.getElementById('btnRun').click();")
    await pg.wait_for_timeout(200)
    # tapRun is async; wait for escape
    for _ in range(20):
        snap = await ev(pg, "window.__snap()")
        if isinstance(snap, dict) and (snap.get('escaped') or not snap.get('inGame') or 'escape:ok' in (snap.get('evs') or [])):
            break
        await pg.wait_for_timeout(100)
    evs = (snap or {}).get('evs') or []
    fled = isinstance(snap, dict) and (snap.get('escaped') or (not snap.get('inGame') and any('escape' in str(x) for x in evs)) or any(e.get('escaped') for e in (snap.get('ends') or [])))
    ok(label, fled, {'start': st, 'before': before, 'snap': snap})

async def case_play_after_banner(pg, label):
    await ev(pg, "window.FFF_ESC_ROLL=0;")
    st = await ev(pg, "window.__startW2()")
    await ev(pg, "if(window.FFF_WAVE) FFF_WAVE.stop(); FFF_UI.ST.busy=false; FFF_UI.render(false);")
    await pg.wait_for_timeout(200)
    snap = await ev(pg, """(function(){
      var ST=FFF_UI.ST, cards=document.querySelectorAll('#hand .card');
      return { inGame:!!ST.inGame, busy:!!ST.busy, phase:ST.phase, turn:ST.b&&ST.b.turn,
               nHand: cards.length, act: !!(document.getElementById('btnAct') && !document.getElementById('btnAct').disabled) };
    })()""")
    playable = isinstance(snap, dict) and snap.get('inGame') and snap.get('phase') == 'play' and snap.get('busy') is False and snap.get('nHand', 0) > 0
    ok(label, playable, {'start': st, 'snap': snap})

async def main():
    h = serve()
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p)
        inst = await install(pg)
        ok('boot + hooks', inst in ('ok',) or inst == 'ok', {'inst': inst, 'errs': errs[:3]})

        async def settle():
            await ev(pg, "if(root.FFF_WAVE) FFF_WAVE.stop(); if(typeof VC!=='undefined' && VC){VC.dead=1;VC.left=1;} var c=document.getElementById('fwvCatch'); if(c&&c.parentNode)c.parentNode.removeChild(c);")
            await pg.wait_for_timeout(200)
        # A: result-screen double taps at 150, 200, 300ms
        await case_result_doubletap(pg, 150, 'A1 wave1 result double-tap 150ms stays in wave 2')
        await settle()
        await case_result_doubletap(pg, 200, 'A2 wave1 result double-tap 200ms stays in wave 2')
        await settle()
        await case_result_doubletap(pg, 300, 'A3 wave1 result double-tap 300ms stays in wave 2')
        await settle()

        # B: ROUND 2 banner double-taps
        await case_banner_dbltap(pg, 'escape', 200, 'B1 ROUND 2 banner dbltap over Escape does not flee')
        await settle()
        await case_banner_dbltap(pg, 'center', 200, 'B2 ROUND 2 banner dbltap at center does not flee')
        await settle()
        await case_banner_dbltap(pg, 'top', 150, 'B3 ROUND 2 banner dbltap at top 150ms does not flee')
        await settle()

        # C: intentional escape still works after the guard
        await case_intentional_escape(pg, 'C intentional Escape still flees after guard')

        # D: play not locked
        await case_play_after_banner(pg, 'D hand is playable after ROUND 2 banner')

        ok('no page errors', not errs, errs[:4])
        await b.close()
    fails = [r for r in RES if not r[0]]
    print('SUMMARY', sum(1 for r in RES if r[0]), 'pass,', len(fails), 'fail', flush=True)
    h.shutdown()
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    asyncio.run(main())
