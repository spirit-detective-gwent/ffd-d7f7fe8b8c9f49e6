#!/workspace/pwenv/bin/python3
"""Capture in-game Off Schedule stills to phase4/wired/."""
import asyncio, functools, http.server, socketserver, threading, os, sys
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
INDEX = HERE.parent.parent / 'index.html'
OUT = Path('/workspace/v6560-review/seal2/phase4/wired')
OUT.mkdir(parents=True, exist_ok=True)
PORT = int(os.environ.get('PORT', '8898'))

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
      SAVE.chapter=2; SAVE.ch1=1; SAVE.ch2=1; SAVE.bond=SAVE.bond||{}; SAVE.bond.path='fierce'; SAVE.bond.lock=1;
      try { STORY.ensure(SAVE); } catch(e){}
      var st=c2S(); st.e=st.e||{}; st.e.run_fac='arc'; st.e.seal_sento=1; st.e.sealKnown=1; st.e.c2sRep=1; st.e.c2lMap=1;
      st.e.n13='done'; st.e.arrive=1; st.e.gymIn=1; st.e.genji=1; st.e.nq=st.e.nq||{};
      st.q=st.q||{}; st.q.cq2_nq_west=9; st.q.cq2_nq_cold=9; st.q.cq2_nq_paint=9; st.q.cq2_nq_door=9; st.q.cq2_nq_seal=9;
      st.q.cq2_locks=0; st.qa='cq2_locks';
      st.q.cq2_s2_waga=9; if (root.FFF_S2&&root.FFF_S2.setStg) root.FFF_S2.setStg('done');
      st.q.cq2_s2_runs=9; if (root.FFF_S2P2&&root.FFF_S2P2.setStg) root.FFF_S2P2.setStg('done');
      st.q.cq2_s2_boat=9; if (root.FFF_S2P3&&root.FFF_S2P3.setStg) root.FFF_S2P3.setStg('done');
      try { c2QSync(); save(); } catch(e){}
      try { if (root.FFF_S2P3&&root.FFF_S2P3.chainRepair) root.FFF_S2P3.chainRepair(); } catch(e3){}
      try { if (root.FFF_S2P4&&root.FFF_S2P4.chainRepair) root.FFF_S2P4.chainRepair(); } catch(e4){}
      return { p4:!!root.FFF_S2P4, q:st.q.cq2_s2_gar, stg:root.FFF_S2P4&&root.FFF_S2P4.stg&&root.FFF_S2P4.stg() };
    })()""")

async def go_town(pg, x, y):
    await ev(pg, f"""(function(){{
      try {{ c2Go('town', [{x}, {y}, 0]); }} catch(e){{}}
      try {{ if (W.ryo) {{ W.ryo.x={x}; W.ryo.y={y}; place(W.ryo,0); }} if (W.aoi) {{ W.aoi.x={x}-60; W.aoi.y={y}+40; place(W.aoi,0); }} camera(true); }} catch(e3){{}}
      try {{ if (root.FFF_S2P4 && root.FFF_S2P4.placeDoor) root.FFF_S2P4.placeDoor(); }} catch(e){{}}
      return typeof c2Room==='function'?c2Room():null;
    }})()""")
    await ev(pg, HUSH)
    await pg.wait_for_timeout(500)

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
        # façade on the south quay, west of the depot door
        await go_town(pg, 4040, 3900)
        fac = await ev(pg, """(function(){
          var el=document.getElementById('s2GarSouth');
          return {room:typeof c2Room==='function'?c2Room():null, fac:!!el, wrain:(function(){var e=document.getElementById('wrain'); if(!e)return 'none'; return getComputedStyle(e).display;})()};
        })()""")
        print('facade', fac, flush=True)
        await shot(pg, '01_garage_facade')
        # interior, Sada at the desk
        inside = await ev(pg, """(function(){
          try{c2Go('gar',[640,700,0]);}catch(e){}
          try{ if(W.ryo){ W.ryo.x=640; W.ryo.y=700; place(W.ryo,0);} if(W.aoi){ W.aoi.x=560; W.aoi.y=740; place(W.aoi,0);} camera(true);}catch(e2){}
          try{ if(root.FFF_S2P4&&root.FFF_S2P4.paintRoom) root.FFF_S2P4.paintRoom(); }catch(e3){}
          var k=W.c2n&&W.c2n.s2sada;
          var rain=(function(){var e=document.getElementById('c2amb'); if(!e)return 'none'; return e.style.display||getComputedStyle(e).display;})();
          return {room:typeof c2Room==='function'?c2Room():null, sada:k?[Math.round(k.x),Math.round(k.y)]:null, amb:rain, canvas:!!document.getElementById('s2P4Room_gar')};
        })()""")
        print('interior', inside, flush=True)
        await pg.wait_for_timeout(700)
        await ev(pg, HUSH)
        await shot(pg, '02_garage_interior')
        # cleared interior
        cleared = await ev(pg, """(function(){
          var P4=root.FFF_S2P4, st=c2S();
          P4.setStg('done'); st.q.cq2_s2_gar=9;
          try{c2Pop();}catch(e){}
          try{ if(W.ryo){ W.ryo.x=640; W.ryo.y=700; place(W.ryo,0);} camera(true);}catch(e2){}
          try{ if(P4.paintRoom) P4.paintRoom(); }catch(e3){}
          return {room:typeof c2Room==='function'?c2Room():null, cleared:P4.cleared&&P4.cleared(), sada:!!(W.c2n&&W.c2n.s2sada)};
        })()""")
        print('cleared', cleared, flush=True)
        await pg.wait_for_timeout(600)
        await ev(pg, HUSH)
        await shot(pg, '03_garage_cleared')
        # depot approach, door still shut (re-open the quest without flags)
        await ev(pg, """(function(){
          var P4=root.FFF_S2P4, st=c2S();
          st.e.baseOpen_dep=0; st.e.guardGone_depot=0;
          st.q.cq2_s2_gar=0; P4.setStg('open');
          try{ c2Go('town',[4220,3880,0]); }catch(e){}
          try{ if(W.ryo){ W.ryo.x=4220; W.ryo.y=3880; place(W.ryo,0);} if(W.aoi){ W.aoi.x=4160; W.aoi.y=3900; place(W.aoi,0);} camera(true);}catch(e2){}
          try{ if(P4.placeDoor) P4.placeDoor(); }catch(e3){}
          return { open: typeof c2LmOpen==='function'?!!c2LmOpen('depot'):null, fac:!!document.getElementById('s2GarSouth') };
        })()""")
        await pg.wait_for_timeout(500)
        await ev(pg, HUSH)
        await shot(pg, '04_depot_approach')
        # after the win, door is open, pin at the depot
        await ev(pg, """(function(){
          var P4=root.FFF_S2P4, st=c2S();
          st.q.cq2_s2_gar=8; P4.openDepot(); P4.qClose();
          try{ c2Go('town',[4300,3720,0]); }catch(e){}
          try{ if(W.ryo){ W.ryo.x=4300; W.ryo.y=3880; place(W.ryo,0);} camera(true);}catch(e2){}
          var t=typeof c2LocksT==='function'?c2LocksT():null;
          return { open: typeof c2LmOpen==='function'?!!c2LmOpen('depot'):null, pin:t&&{lab:t.lab,loc:t.loc,x:t.x,y:t.y}, dep:!!st.e.baseOpen_dep };
        })()""")
        await pg.wait_for_timeout(400)
        await ev(pg, HUSH)
        await shot(pg, '05_depot_door_open')
        print('ERRS', errs[:8], flush=True)
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
