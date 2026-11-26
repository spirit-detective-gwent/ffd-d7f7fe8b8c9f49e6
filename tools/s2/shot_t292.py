#!/workspace/pwenv/bin/python3
"""t292 stills and an order clip: Chiyo at the counter, rider on the street."""
import asyncio, functools, http.server, socketserver, threading, os, subprocess
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
INDEX = HERE.parent.parent / 'index.html'
OUT = Path('/workspace/v6560-review/seal2/phase1/fix_t292')
OUT.mkdir(parents=True, exist_ok=True)
PORT = int(os.environ.get('PORT', '8879'))

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

SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
HUSH = """(function(){try{if(typeof phClose==='function')phClose()}catch(e){}
W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];
var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};
var q=document.getElementById('wquest'); if(q) q.style.display='none';
return 1})()"""

async def skipall(pg, n=8):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(200); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(200)

async def shot(pg, name):
    await ev(pg, HUSH)
    await pg.wait_for_timeout(200)
    path = OUT / f'{name}.png'
    await pg.screenshot(path=str(path), type='png')
    print('shot', path, flush=True)

async def boot(pg, path='balanced'):
    await pg.touchscreen.tap(195, 420)
    await pg.evaluate("WORLD_API.enter(true)")
    await pg.wait_for_timeout(1500)
    await skipall(pg)
    await ev(pg, "root.FFF_NO_TUT=1")
    await pg.evaluate("WORLD_API.c2Begin(true)")
    await pg.wait_for_timeout(2500)
    await skipall(pg)
    await ev(pg, HUSH)
    return await ev(pg, f"""(function(){{
      var path='{path}';
      SAVE.chapter=2; SAVE.ch1=1; SAVE.ch2=1; SAVE.bond=SAVE.bond||{{}}; SAVE.bond.path=path; SAVE.bond.lock=1;
      try {{ STORY.ensure(SAVE); }} catch(e){{}}
      var st=c2S(); st.e=st.e||{{}}; st.e.run_fac='arc'; st.e.seal_sento=1; st.e.sealKnown=1; st.e.c2sRep=1; st.e.c2lMap=1;
      st.e.n13='done'; st.e.arrive=1; st.e.gymIn=1; st.e.genji=1; st.e.nq=st.e.nq||{{}};
      st.q=st.q||{{}}; st.q.cq2_nq_west=9; st.q.cq2_nq_cold=9; st.q.cq2_nq_paint=9; st.q.cq2_nq_door=9; st.q.cq2_nq_seal=9;
      st.q.cq2_locks=0; st.qa='cq2_locks';
      st.q.cq2_s2_waga=9; if (root.FFF_S2&&root.FFF_S2.setStg) root.FFF_S2.setStg('done');
      try {{ c2QSync(); save(); }} catch(e){{}}
      try {{ if (root.FFF_S2&&root.FFF_S2.chainRepair) root.FFF_S2.chainRepair(); }} catch(e5){{}}
      return {{ s2:!!root.FFF_S2, stg:root.FFF_S2&&root.FFF_S2.stg&&root.FFF_S2.stg(), q:st.q.cq2_s2_waga }};
    }})()""")

async def enter_shop(pg, ryo_y=700):
    info = await ev(pg, f"""(function(){{
      try{{ c2Go('waga',[640,{ryo_y},3]); }}catch(e){{}}
      try{{ if(W.ryo){{ W.ryo.x=640; W.ryo.y={ryo_y}; W.ryo.dir=3; if(typeof animWalk==='function') animWalk(W.ryo,0); place(W.ryo,0); }}
           if(W.aoi){{ W.aoi.x=560; W.aoi.y={ryo_y}+40; W.aoi.dir=3; if(typeof animWalk==='function') animWalk(W.aoi,0); place(W.aoi,0); }}
           camera(true); }}catch(e2){{}}
      var c=W.c2n&&W.c2n.s2;
      return {{ room: typeof c2Room==='function'?c2Room():null, chi: c?[Math.round(c.x),Math.round(c.y),!!c.walker,c.dir]:null, canvas:!!document.getElementById('s2Room') }};
    }})()""")
    await ev(pg, HUSH)
    await pg.wait_for_timeout(400)
    return info

async def open_page(p, errs, record=False):
    b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
    kw = dict(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
    if record:
        kw['record_video_dir'] = str(OUT / 'vidtmp')
        kw['record_video_size'] = {'width': 390, 'height': 844}
    ctx = await b.new_context(**kw)
    pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
    html = body()
    async def rt(route): await route.fulfill(body=html, content_type='text/html')
    await pg.route('**/index.html', rt)
    await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(2200)
    return b, ctx, pg

async def main():
    s = TS(('127.0.0.1', PORT), functools.partial(Q, directory=str(INDEX.parent)))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    errs = []
    async with async_playwright() as p:
        b, ctx, pg = await open_page(p, errs, record=False)
        info = await boot(pg)
        print('boot', info, flush=True)
        # interior: Chiyo still in the back, player on the customer side
        shop = await enter_shop(pg, 670)
        print('shop before walk', shop, flush=True)
        await ev(pg, HUSH)
        await shot(pg, '02_chiyo_back_new')
        # walk her to the counter, then open the menu
        await ev(pg, """(function(){ try { root.FFF_S2.chiyoToCounter(function(){ root.__chiReady=1; try{ root.FFF_S2.menu(); }catch(e){} }); } catch(e){ root.__chiReady='err:'+e; } return 1; })()""")
        await pg.wait_for_timeout(2800)
        after = await ev(pg, """(function(){ var c=W.c2n&&W.c2n.s2, el=c&&c.el; return { x:c&&Math.round(c.x), y:c&&Math.round(c.y), dir:c&&c.dir, ready:root.__chiReady, menu:!!(document.getElementById('wdlg')&&document.getElementById('wdlg').innerHTML), loop:!!(c&&c.loop), sheet:c&&c.sheet, bs:el&&el.style.backgroundSize }; })()""")
        print('shop after walk', after, flush=True)
        await pg.wait_for_timeout(300)
        path = OUT / '02_chiyo_counter_menu.png'
        await pg.screenshot(path=str(path), type='png')
        print('shot', path, flush=True)
        await ev(pg, HUSH)
        await pg.wait_for_timeout(250)
        await shot(pg, '02_chiyo_counter_after')
        # battle
        await ev(pg, HUSH)
        await ev(pg, """(function(){
          try{ c2Go('town',[2560,3190,0]); }catch(e){}
          try{ if(W.ryo){ W.ryo.x=2560; W.ryo.y=3190; place(W.ryo,0);} camera(true);}catch(e2){}
          try{ fight(['c2_boso','c2_boso','c2_boso'], false, { dg:'c2', dgk:'s2_x_0', dgks:['s2_x_0','s2_x_1','s2_x_2'], s2k:'s2_x', s2waga:1, s2:1 }); }catch(e3){ return 'err:'+e3; }
          return (root.FFF_BTROOM && FFF_BTROOM({ ctx:{ dg:'c2', s2waga:1, dgk:'s2_x_0', s2k:'s2_x' } })) || null;
        })()""")
        await pg.wait_for_timeout(4500)
        await skipall(pg, 4)
        await pg.wait_for_timeout(1200)
        room = await ev(pg, """(function(){ return { bfx: document.getElementById('game')&&document.getElementById('game').getAttribute('data-bfx'), foe:(document.querySelector('#fE .fn b')||{}).textContent }; })()""")
        print('fight', room, flush=True)
        await shot(pg, '04_rider_fight_after')

        # short clip of ordering: frames during the walk only, then ffmpeg
        frames = OUT / 'clip_frames'
        if frames.exists():
            for f in frames.glob('*.png'):
                f.unlink()
        frames.mkdir(exist_ok=True)
        await ev(pg, """(function(){
          try{ if (typeof endMatch==='function') { try{ endMatch(); }catch(e0){} } }catch(e){}
          try{ c2Go('waga',[640,670,3]); }catch(e){}
          try{ if(W.ryo){ W.ryo.x=640; W.ryo.y=670; W.ryo.dir=3; if(typeof animWalk==='function') animWalk(W.ryo,0); place(W.ryo,0);}
               if(W.aoi){ W.aoi.x=560; W.aoi.y=710; W.aoi.dir=3; if(typeof animWalk==='function') animWalk(W.aoi,0); place(W.aoi,0);} camera(true);}catch(e2){}
          return typeof c2Room==='function'?c2Room():null;
        })()""")
        await ev(pg, HUSH)
        await pg.wait_for_timeout(500)
        await ev(pg, """(function(){ try { root.__chiReady=0; root.FFF_S2.chiyoToCounter(function(){ root.__chiReady=1; try{ root.FFF_S2.menu(); }catch(e){} }); } catch(e){} return 1; })()""")
        for i in range(48):
            await pg.screenshot(path=str(frames / f'f{i:03d}.png'), type='png')
            await pg.wait_for_timeout(80)
        mp4 = OUT / '05_order_chiyo.mp4'
        subprocess.check_call(['ffmpeg', '-y', '-framerate', '12', '-i', str(frames / 'f%03d.png'),
                               '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', str(mp4)])
        print('clip', mp4, flush=True)
        print('ERRS', errs[:8], flush=True)
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
