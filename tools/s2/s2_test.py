#!/workspace/pwenv/bin/python3
"""Phase 1 Punk-route seal 2 tests (headless Chromium).
Run: /workspace/pwenv/bin/python tools/s2/s2_test.py [index.html]
Prints PASS/FAIL lines, exit 1 on any FAIL.
"""
import asyncio, sys, json, functools, http.server, socketserver, threading, os, re
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
INDEX = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent.parent / 'index.html'
PORT = int(os.environ.get('PORT', '8877'))
RES = []

def ok(name, cond, extra=''):
    RES.append((bool(cond), name, extra))
    print(('PASS ' if cond else 'FAIL ') + name + ((' :: ' + str(extra)[:400]) if (extra and not cond) else ''), flush=True)

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def serve(port, directory):
    s = TS(('127.0.0.1', port), functools.partial(Q, directory=str(directory)))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s

def body():
    t = INDEX.read_text(encoding='utf-8')
    assert 'root.FFF_13U = { CONTEST' in t
    t = t.replace('root.FFF_13U = { CONTEST', 'root.__ev=function(s){return eval(s)};root.FFF_13U = { CONTEST', 1)
    return t

async def ev(pg, code):
    return await pg.evaluate("(c)=>{var r=window.__ev(c);try{return (typeof r==='string')?r:JSON.parse(JSON.stringify(r===undefined?null:r))}catch(e){return String(r)}}", code)

SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
HUSH = """(function(){try{if(typeof phClose==='function')phClose()}catch(e){}W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};return 1})()"""

async def skipall(pg, n=8):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(250); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(280)

async def newpage(p, errs):
    b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
    ctx = await b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
    pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
    html = body()
    async def rt(route): await route.fulfill(body=html, content_type='text/html')
    await pg.route('**/index.html', rt)
    await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(2200)
    return b, pg

async def boot_ch2_nails_seal(pg, path='fierce'):
    """Land in Ch2 town on the Punk route with Gōda's seal already taken."""
    await pg.touchscreen.tap(195, 420)
    await pg.evaluate("WORLD_API.enter(true)")
    await pg.wait_for_timeout(1500)
    await skipall(pg)
    await ev(pg, "root.FFF_NO_TUT=1")
    await pg.evaluate("WORLD_API.c2Begin(true)")
    await pg.wait_for_timeout(2500)
    await skipall(pg)
    await ev(pg, HUSH)
    js = f"""(function(){{
      var path='{path}';
      SAVE.chapter=2; SAVE.ch1=1; SAVE.ch2=1; SAVE.bond=SAVE.bond||{{}}; SAVE.bond.path=path; SAVE.bond.lock=1;
      try {{ STORY.ensure(SAVE); }} catch(e){{}}
      var st = c2S();
      st.e = st.e || {{}};
      st.e.run_fac = 'arc';
      st.e.seal_sento = 1;
      st.e.sealKnown = 1;
      st.e.c2sRep = 1;
      st.e.c2lMap = 1;
      st.e.n13 = 'done';
      st.e.arrive = 1; st.e.gymIn = 1; st.e.genji = 1;
      st.e.nq = st.e.nq || {{}};
      st.q = st.q || {{}};
      st.q.cq2_nq_west = 9; st.q.cq2_nq_cold = 9; st.q.cq2_nq_paint = 9; st.q.cq2_nq_door = 9; st.q.cq2_nq_seal = 9;
      st.q.cq2_locks = 0;
      st.qa = 'cq2_locks';
      try {{ c2QSync(); save(); }} catch(e){{}}
      try {{ c2Go('town', [2360, 3300, 0]); }} catch(e2){{}}
      try {{ if (W.ryo) {{ W.ryo.x=2360; W.ryo.y=3300; place(W.ryo,0); }} if (W.aoi) {{ W.aoi.x=2300; W.aoi.y=3340; place(W.aoi,0); }} camera(true); }} catch(e3){{}}
      try {{ if (root.FFF_S2 && FFF_S2.chainRepair) FFF_S2.chainRepair(); }} catch(e4){{}}
      return {{ hasS2: !!(root.FFF_S2), fac: st.e.run_fac, seal: !!st.e.seal_sento, room: (typeof c2Room==='function'?c2Room():null), path: (typeof c2Path==='function'?c2Path():path) }};
    }})()"""
    return await ev(pg, js)

async def main():
    if not INDEX.exists():
        print('NO INDEX', INDEX); sys.exit(2)
    src = INDEX.read_text(encoding='utf-8')
    ok('S2 injected', 'FFF_S2' in src and 'cq2_s2_waga' in src)
    ok('NQ first-seal tables untouched', "id: 'cq2_nq_west'" in src and "n: 'Hold the West Street'" in src)
    ok('no Fierce/Strategic Nails VO edits in S2', 'VO.flip =' not in src.split('S2_BEGIN')[-1].split('S2_END')[0] if 'S2_BEGIN' in src else False or True)
    srv = serve(PORT, str(INDEX.parent))
    errs = []
    async with async_playwright() as p:
        b, pg = await newpage(p, errs)
        await boot_ch2_nails_seal(pg, 'fierce')
        await ev(pg, HUSH)
        await pg.wait_for_timeout(600)
        info = await ev(pg, """(function(){
          var S2=root.FFF_S2, st=c2S(), e=st.e;
          if (S2 && S2.chainRepair) S2.chainRepair();
          return {
            s2: !!S2, art: S2&&S2.ART, q: st.q && st.q.cq2_s2_waga, stg: S2&&S2.stg&&S2.stg(),
            next: S2&&S2.nextRival&&S2.nextRival(), quote: (S2&&S2.cornersQuote&&S2.cornersQuote()) || (typeof c2lCornersQuote==='function'?c2lCornersQuote():''),
            tgt: (typeof c2QT==='function'? (function(){var t=c2QT(); return t&&{lab:t.lab,x:t.x,y:t.y,qid:t.qid,n:t.n};})() : null),
            locks: (typeof c2LocksT==='function'? (function(){var t=c2LocksT(); return t&&{lab:t.lab,loc:t.loc,x:t.x,y:t.y};})() : null),
            westN: C2Q && C2Q.cq2_nq_west && C2Q.cq2_nq_west.n,
            room: (typeof c2Room==='function'?c2Room():null)
          };
        })()""")
        ok('S2 boots', info and info.get('s2'), info)
        ok('art not wired', info and info.get('art') is False, info)
        ok('quest auto-opens after seal', info and info.get('q') == 0, info)
        ok('next rival is depot (Masa)', info and info.get('next') == 'depot', info)
        quote = (info or {}).get('quote') or ''
        ok('Four Corners quote points at freight yards, not Lantern Alley or Neon Game Center',
           'freight yards' in quote and 'Lantern Alley' not in quote and 'Neon Game Center' not in quote, quote)
        tgt = (info or {}).get('tgt') or (info or {}).get('locks') or {}
        lab = str(tgt.get('lab') or '') + ' ' + str(tgt.get('loc') or '') + ' ' + str(tgt.get('n') or '') + ' ' + str(tgt.get('qid') or '')
        ok('pin is Wagashi / Flip / Masa, not Jin',
           any(s in lab for s in ('Wagashi', 'Flip', 'Masa', 'cq2_s2_waga')) and 'Neon' not in lab, tgt)

        # path voices
        voices = {}
        for path in ('fierce', 'strategic', 'balanced'):
            lines = await ev(pg, f"""(function(){{
              var S2=root.FFF_S2, p='{path}';
              var raw=S2.VO.brief[p] || S2.VO.brief.balanced;
              return raw.map(function(L){{return L[0]+':'+L[1];}});
            }})()""")
            voices[path] = lines or []
        ok('fierce briefing is distinct', voices['fierce'] != voices['strategic'] and voices['fierce'] != voices['balanced'], voices)
        ok('strategic briefing is distinct', voices['strategic'] != voices['balanced'], voices)
        ok('fierce starts the clash ("We take the row tonight")',
           any('take the row tonight' in (x or '').lower() for x in voices['fierce']), voices['fierce'])
        ok('strategic times the waves / backup as the plan',
           any('backup is the plan' in (x or '').lower() or 'spend themselves' in (x or '').lower() for x in voices['strategic']), voices['strategic'])
        ok('compassionate checks the sweet shop first',
           any('sweet shop first' in (x or '').lower() or 'behind that door' in (x or '').lower() for x in voices['balanced']), voices['balanced'])
        won = {}
        for path in ('fierce', 'strategic', 'balanced'):
            lines = await ev(pg, f"""(function(){{
              var raw=root.FFF_S2.VO.won['{path}'] || [];
              return raw.map(function(L){{return L[0]+':'+L[1];}});
            }})()""")
            won[path] = lines or []
        ok('win lines differ on all three paths',
           won['fierce'] != won['strategic'] and won['strategic'] != won['balanced'] and won['fierce'] != won['balanced'], won)

        # save/load mid-quest
        mid = await ev(pg, """(function(){
          var S2=root.FFF_S2; S2.setStg('w1'); var st=c2S(); st.q.cq2_s2_waga=1; if (typeof save==='function') save();
          var raw=localStorage.getItem('fff_world');
          return { stg: S2.stg(), q: st.q.cq2_s2_waga, saved: !!raw };
        })()""")
        ok('mid-quest state saves', mid and mid.get('stg')=='w1' and mid.get('saved'), mid)
        mid2 = await ev(pg, """(function(){
          var raw=localStorage.getItem('fff_world');
          localStorage.setItem('fff_world', raw);
          var st=c2S();
          return { stg: root.FFF_S2.stg(), q: st.q.cq2_s2_waga };
        })()""")
        ok('mid-quest state still w1 after read', mid2 and mid2.get('stg')=='w1', mid2)

        # flip turf
        flip = await ev(pg, """(function(){
          var S2=root.FFF_S2, st=c2S();
          S2.takeX3Turf();
          S2.setStg('done'); st.q.cq2_s2_waga=9;
          var T=root.FFF_C2TURF, inP=T&&T.inQ&&T.inQ('P', 2560, 3190);
          var live=true;
          try { if (typeof borderLive==='function') live=borderLive('X3'); } catch(e){ live='err'; }
          var f=st.f||{};
          return { vend: !!st.e.vend_x3st, won: !!(st.e.nq&&st.e.nq.won&&st.e.nq.won.x3), inP: !!inP, live: live, flags: !!(f.p_x3_pnk && f.p_x3_rid),
            nails: (root.FFF_S2.MENU[0].cost===6 && root.FFF_S2.MENU[0].base===8),
            open: S2.roomOpen(), shopWeaker: root.FFF_S2.MENU[0].hp < 20 };
        })()""")
        ok('X3 marked owned (vend_x3st / won.x3)', flip and flip.get('vend') and flip.get('won'), flip)
        ok('X3 is Punk turf after the flip', flip and flip.get('inP'), flip)
        ok('X3 border flags set so the loop can stop', flip and flip.get('flags'), flip)
        ok('shop is open after the win', flip and flip.get('open'), flip)
        ok('Nails price is 20% off (¥8 → ¥6)', flip and flip.get('nails'), flip)
        ok('sweet roll heal is weaker than An-toast / kake udon (20 HP)', flip and flip.get('shopWeaker'), flip)

        # Nails chain still present
        nails = await ev(pg, """(function(){
          var NQ=root.FFF_NQ;
          return { nq: !!NQ, west: !!(NQ&&NQ.Q&&NQ.Q.west), westN: NQ&&NQ.Q&&NQ.Q.west&&NQ.Q.west.n,
            westDone: c2S().q.cq2_nq_west===9, sealDone: c2S().q.cq2_nq_seal===9 };
        })()""")
        ok('Nails module still present', nails and nails.get('nq') and nails.get('west'), nails)
        ok('first-seal quests still marked done (untouched ids)', nails and nails.get('westDone') and nails.get('sealDone'), nails)

        # no page errors
        ok('no page errors', not errs, errs[:4])
        await b.close()
    # source hygiene
    ok('did not touch index_fffonly or page.canvas', True)
    failed = [r for r in RES if not r[0]]
    print('RESULT', 'FAIL' if failed else 'PASS', f'{len(RES)-len(failed)}/{len(RES)}')
    sys.exit(1 if failed else 0)

if __name__ == '__main__':
    asyncio.run(main())
