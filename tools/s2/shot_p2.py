#!/workspace/pwenv/bin/python3
"""Capture in-game Night Runs stills to phase2/wired/."""
import asyncio, functools, http.server, socketserver, threading, os, sys
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
INDEX = HERE.parent.parent / 'index.html'
OUT = Path('/workspace/v6560-review/seal2/phase2/wired')
OUT.mkdir(parents=True, exist_ok=True)
PORT = int(os.environ.get('PORT', '8867'))

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def body():
    t = INDEX.read_text(encoding='utf-8')
    t = t.replace('root.FFF_13U = { CONTEST', 'root.__ev=function(s){return eval(s)};root.FFF_13U = { CONTEST', 1)
    return t

async def ev(pg, code):
    return await pg.evaluate("(c)=>{var r=window.__ev(c);try{return (typeof r==='string')?r:JSON.parse(JSON.stringify(r===undefined?null:r))}catch(e){return String(r)}}", code)

HUSH = """(function(){try{if(typeof phClose==='function')phClose()}catch(e){}
W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];
var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};
var q=document.getElementById('wquest'); if(q) q.style.display='none';
return 1})()"""

async def skipall(pg, n=8):
    SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(200); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(200)

async def shot(pg, name):
    await ev(pg, HUSH)
    await pg.wait_for_timeout(250)
    path = OUT / f'{name}.png'
    await pg.screenshot(path=str(path), type='png')
    print('shot', path, flush=True)

async def boot(pg):
    await pg.touchscreen.tap(195, 420)
    await pg.evaluate("WORLD_API.enter(true)")
    await pg.wait_for_timeout(1500)
    await skipall(pg)
    await ev(pg, "root.FFF_NO_TUT=1")
    await pg.evaluate("WORLD_API.c2Begin(true)")
    await pg.wait_for_timeout(2500)
    await skipall(pg)
    await ev(pg, HUSH)
    return await ev(pg, """(function(){
      SAVE.chapter=2; SAVE.ch1=1; SAVE.ch2=1; SAVE.bond=SAVE.bond||{}; SAVE.bond.path='balanced'; SAVE.bond.lock=1;
      try { STORY.ensure(SAVE); } catch(e){}
      var st=c2S(); st.e=st.e||{}; st.e.run_fac='arc'; st.e.seal_sento=1; st.e.sealKnown=1; st.e.c2sRep=1; st.e.c2lMap=1;
      st.e.n13='done'; st.e.arrive=1; st.e.gymIn=1; st.e.genji=1; st.e.nq=st.e.nq||{};
      st.q=st.q||{}; st.q.cq2_nq_west=9; st.q.cq2_nq_cold=9; st.q.cq2_nq_paint=9; st.q.cq2_nq_door=9; st.q.cq2_nq_seal=9;
      st.q.cq2_locks=0; st.qa='cq2_locks';
      st.q.cq2_s2_waga=9; if (root.FFF_S2&&root.FFF_S2.setStg) root.FFF_S2.setStg('done');
      try { c2QSync(); save(); } catch(e){}
      try { if (root.FFF_S2P2&&root.FFF_S2P2.chainRepair) root.FFF_S2P2.chainRepair(); } catch(e4){}
      try { if (root.FFF_S2&&root.FFF_S2.chainRepair) root.FFF_S2.chainRepair(); } catch(e5){}
      try { if (root.FFF_S2P2&&root.FFF_S2P2.chainRepair) root.FFF_S2P2.chainRepair(); } catch(e6){}
      return { p2:!!root.FFF_S2P2, q:st.q.cq2_s2_runs, stg:root.FFF_S2P2&&root.FFF_S2P2.stg&&root.FFF_S2P2.stg() };
    })()""")

async def go_town(pg, x, y):
    await ev(pg, f"""(function(){{
      try {{ c2Go('town', [{x}, {y}, 0]); }} catch(e){{}}
      try {{ if (W.ryo) {{ W.ryo.x={x}; W.ryo.y={y}; place(W.ryo,0); }} if (W.aoi) {{ W.aoi.x={x}-60; W.aoi.y={y}+40; place(W.aoi,0); }} camera(true); }} catch(e3){{}}
      try {{ if (root.FFF_S2P2) {{ if (root.FFF_S2P2) {{}} }} }} catch(e){{}}
      return typeof c2Room==='function'?c2Room():null;
    }})()""")
    await ev(pg, HUSH)
    await pg.wait_for_timeout(400)

async def main():
    s = TS(('127.0.0.1', PORT), functools.partial(Q, directory=str(INDEX.parent)))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    errs = []
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        html = body()
        async def rt(route): await route.fulfill(body=html, content_type='text/html')
        await pg.route('**/index.html', rt)
        await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(2200)
        info = await boot(pg)
        print('boot', info, flush=True)
        # SE street façade
        await go_town(pg, 4300, 3520)
        await ev(pg, "try{if(root.FFF_S2P2){var el=document.getElementById('s2MinaSouth');}}catch(e){}")
        await pg.wait_for_timeout(400)
        await shot(pg, '01_south_facade')
        # bridge
        await go_town(pg, 3610, 3480)
        await shot(pg, '02_bridge_foot')
        # lobby
        await ev(pg, """(function(){ try{c2Go('mina',[640,700,0]);}catch(e){} return typeof c2Room==='function'?c2Room():null; })()""")
        await pg.wait_for_timeout(600)
        await ev(pg, HUSH)
        await shot(pg, '03_lobby')
        # stair approach
        await ev(pg, """(function(){ try{ if(W.ryo){ W.ryo.x=860; W.ryo.y=600; place(W.ryo,0);} camera(true);}catch(e){} return 1; })()""")
        await pg.wait_for_timeout(300)
        await shot(pg, '04_lobby_stair')
        # workshop
        await ev(pg, """(function(){ try{c2Go('mshop',[640,700,0]);}catch(e){} return typeof c2Room==='function'?c2Room():null; })()""")
        await pg.wait_for_timeout(600)
        await ev(pg, HUSH)
        await shot(pg, '05_workshop')
        # after flip, still in workshop (Hase stays)
        await ev(pg, """(function(){ var P2=root.FFF_S2P2; P2.takeEastTurf(); P2.setStg('done'); var st=c2S(); st.q.cq2_s2_runs=9; try{c2Pop();}catch(e){} return {won:!!(st.e.nq&&st.e.nq.won&&st.e.nq.won.east)}; })()""")
        await pg.wait_for_timeout(400)
        await ev(pg, HUSH)
        await shot(pg, '06_workshop_after')
        # lobby after
        await ev(pg, """(function(){ try{c2Go('mina',[640,700,0]);}catch(e){} return 1; })()""")
        await pg.wait_for_timeout(600)
        await ev(pg, HUSH)
        await shot(pg, '07_lobby_after')
        print('ERRS', errs[:6], flush=True)
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
