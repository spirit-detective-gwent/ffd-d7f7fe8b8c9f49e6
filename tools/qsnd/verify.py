#!/workspace/pwenv/bin/python3
"""Take Four Corners, exit the gym, walk onto the next street. Fail if quest_ready/roundwin plays."""
import asyncio, json, http.server, socketserver, threading, functools, sys
from pathlib import Path
from playwright.async_api import async_playwright

FFD = '/workspace/ffd-qsnd'
PORT = 8972
OUT = Path('/tmp/qsnd')
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def serve(port, directory=FFD):
    s = TS(('127.0.0.1', port), functools.partial(Q, directory=directory))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s

def body():
    t = Path(FFD + '/index.html').read_text(encoding='utf-8')
    needle = 'var W = { guards: [], paused: false'
    assert needle in t
    t = t.replace(needle, 'root.__ev=function(s){return eval(s)};' + needle, 1)
    return t

async def ev(pg, code):
    return await pg.evaluate(
        """(c)=>{var r=window.__ev(c);try{return (r&&typeof r.then==='function')?'THEN':(typeof r==='string'?r:JSON.parse(JSON.stringify(r===undefined?null:r)))}catch(e){return String(r)}}""",
        code,
    )

HOOK = r"""
if (window.__sfxhook) 'already';
else (function(){
  window.__sfxhook = 1; window.__sfxlog = [];
  function rec(src, name, extra) {
    var e = {}, S = null;
    try { S = c2S(); e = (S && S.e) || {}; } catch (err) {}
    window.__sfxlog.push({
      t: Math.round(performance.now()), src: src, name: String(name), extra: extra || null,
      x: (W.ryo && Math.round(W.ryo.x)) || 0, y: (W.ryo && Math.round(W.ryo.y)) || 0,
      room: (typeof c2Room === 'function' && c2Room()) || '',
      hear: !!e.fc51Hear, out: !!e.fc13sOut, qa: (S && S.qa) || SAVE.qa || '',
      locks: S && S.q && S.q.cq2_locks
    });
  }
  if (AU && AU.play) { var p0 = AU.play; AU.play = function (n, o) { rec('AU.play', n, { gain: o && o.gain }); return p0.apply(this, arguments); }; }
  if (typeof qBanner === 'function') { var qb = qBanner; qBanner = function (k, t, s) { rec('qBanner', k, { title: t, sub: s }); return qb.apply(this, arguments); }; }
  if (typeof ev === 'function') { var ev0 = ev; ev = function (k) { var s = String(k || ''); if (/quest|banner|beacon|qdone|13t:outside|fc13s/i.test(s)) rec('ev', s); return ev0.apply(this, arguments); }; }
  'hooked';
})()
"""

SEED = r"""
(function(){
  window.FFF_SKIP_C2_CINE = 1; W._c2SkipCine = 1;
  var S = c2S(); S.e = S.e || {}; S.q = S.q || {};
  ['arrive','gymIn','genji','herbBrief','sumire','informant','infPunk','c2sRep','roam','called','c2lMap'].forEach(function (k) { S.e[k] = 1; });
  delete S.e.fc51Hear; delete S.e.fc13sOut; delete S.e.fc13sTrk; delete S.e.ask44Beat; delete S.e.fc51Brawls; delete S.e.fc51Seen;
  S.q.cq2_arrive = 9; S.q.cq2_hq = 9; S.q.cq2_scout = 9; S.q.cq2_word = 0; S.q.cq2_locks = 0; S.qa = 'cq2_locks';
  SAVE.chapter = 2; SAVE.qa = 'cq2_locks'; SAVE.qs = SAVE.qs || {};
  SAVE.qs.cq2_arrive = 9; SAVE.qs.cq2_hq = 9; SAVE.qs.cq2_scout = 9; SAVE.qs.cq2_word = 0; SAVE.qs.cq2_locks = 0;
  save(); if (typeof c2QSync === 'function') c2QSync();
  1;
})()
"""

HUSH = r"""(function(){try{if(typeof phClose==='function')phClose()}catch(e){}W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];W.fading=0;var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML='';}1;})()"""

async def skipall(pg, n=10):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(200)
            c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c)
        await pg.wait_for_timeout(250)

async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    serve(PORT)
    html = body()
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:240]))
        async def rt(route):
            await route.fulfill(body=html, content_type='text/html')
        await pg.route('**/index.html', rt)
        await pg.goto(f'http://127.0.0.1:{PORT}/index.html')
        await pg.wait_for_function("()=>!!(window.WORLD_API && window.__ev)", timeout=90000)
        await pg.wait_for_timeout(600)
        await pg.touchscreen.tap(195, 420)
        await pg.evaluate("WORLD_API.enter(true)")
        await pg.wait_for_timeout(1200)
        await skipall(pg)
        await ev(pg, "window.FFF_SKIP_C2_CINE=1;W._c2SkipCine=1;1")
        await pg.evaluate("WORLD_API.c2Begin(true)")
        await pg.wait_for_timeout(2500)
        await skipall(pg, 14)
        await ev(pg, HUSH)
        await ev(pg, SEED)
        await ev(pg, "c2Go('gym');1")
        await pg.wait_for_timeout(800)
        await skipall(pg, 6)
        await ev(pg, HUSH)
        hook = await ev(pg, HOOK)
        print('HOOK', hook)
        await ev(pg, "window.__sfxlog=[];1")
        await ev(pg, "c2Out('gym');1")
        await pg.wait_for_timeout(1200)
        # advance hear dialogue
        for i in range(22):
            st = await ev(pg, "({dlg:!!W.dlg,hear:!!(c2S().e&&c2S().e.fc51Hear),txt:(document.getElementById('wdlg')&&document.getElementById('wdlg').innerText||'').slice(0,80)})")
            if st and st.get('dlg'):
                await pg.touchscreen.tap(195, 700)
            await pg.wait_for_timeout(350)
            if st and st.get('hear') and not st.get('dlg') and i > 5:
                break
        # walk east along Gym Lane past the X1/X3 midpoint (~1861) and a bit north
        for x, y in ((1200, 2670), (1600, 2670), (2000, 2670), (2300, 2670), (2000, 2500)):
            await ev(pg, f"W.dlg=false;W.busy=false;W.cut=false;if(WORLD_API.walkToX)WORLD_API.walkToX({x},{y});else if(typeof walkTo==='function')walkTo({x},{y},true,true);1")
            await pg.wait_for_timeout(2200)
        log = await ev(pg, "window.__sfxlog||[]") or []
        Path(OUT / 'verify.json').write_text(json.dumps(log, indent=2, default=str))
        bad = [x for x in log if x.get('src') == 'AU.play' and x.get('name') in ('quest_ready', 'roundwin')]
        banners = [x for x in log if x.get('src') == 'qBanner']
        beacons = [x for x in log if x.get('src') == 'ev' and 'fc13s:beacon' in str(x.get('name'))]
        end = await ev(pg, "({hear:!!c2S().e.fc51Hear,locks:c2S().q.cq2_locks,qa:c2S().qa,xy:W.ryo&&[Math.round(W.ryo.x),Math.round(W.ryo.y)],room:c2Room()})")
        print('END', json.dumps(end))
        print('BANNERS', json.dumps(banners, default=str)[:800])
        print('BEACONS', json.dumps(beacons, default=str)[:800])
        print('BAD', json.dumps(bad, default=str))
        names = {}
        for x in log:
            if x.get('src') == 'AU.play':
                names[x['name']] = names.get(x['name'], 0) + 1
        print('AU', json.dumps(names, indent=2))
        print('ERRS', errs)
        ok = not bad and end and end.get('hear') and end.get('locks') != 9 and end.get('qa') == 'cq2_locks'
        print('RESULT', 'PASS' if ok else 'FAIL')
        await b.close()
        if not ok:
            sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
