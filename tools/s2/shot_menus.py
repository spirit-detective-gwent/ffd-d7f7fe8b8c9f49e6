#!/workspace/pwenv/bin/python3
"""Wired stills and order-to-eat clips for the seal 2 shop menus."""
import asyncio, functools, http.server, socketserver, threading, os, time, subprocess, shutil
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
INDEX = HERE.parent.parent / 'index.html'
OUT = Path('/workspace/v6560-review/shopmenus')
OUT.mkdir(parents=True, exist_ok=True)
CLIP = OUT / 'clips'
CLIP.mkdir(parents=True, exist_ok=True)
PORT = int(os.environ.get('PORT', '8874'))

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
try{ if(root.FFF_S2MENUS) FFF_S2MENUS.close(); }catch(e){}
return 1})()"""

SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""

async def skipall(pg, n=8):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(200); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(200)

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
      SAVE.items=40; SAVE.hp=40; SAVE.sp=20;
      try { STORY.ensure(SAVE); } catch(e){}
      var st=c2S(); st.e=st.e||{}; st.e.run_fac='arc'; st.e.seal_sento=1; st.e.sealKnown=1; st.e.c2sRep=1; st.e.c2lMap=1;
      st.e.n13='done'; st.e.arrive=1; st.e.gymIn=1; st.e.genji=1; st.e.nq=st.e.nq||{};
      st.q=st.q||{}; st.q.cq2_nq_west=9; st.q.cq2_nq_cold=9; st.q.cq2_nq_paint=9; st.q.cq2_nq_door=9; st.q.cq2_nq_seal=9;
      st.q.cq2_locks=0; st.qa='cq2_locks';
      st.q.cq2_s2_waga=9; if (root.FFF_S2&&root.FFF_S2.setStg) root.FFF_S2.setStg('done');
      try { c2QSync(); save(); hud(); } catch(e){}
      try { if (root.FFF_S2&&root.FFF_S2.chainRepair) root.FFF_S2.chainRepair(); } catch(e4){}
      root.FFF_EATG_BOT='win';
      return { s2:!!root.FFF_S2, menus:!!root.FFF_S2MENUS, yen:SAVE.items };
    })()""")

async def go_room(pg, room, x, y):
    await ev(pg, f"""(function(){{
      try {{ c2Go('{room}', [{x}, {y}, 0]); }} catch(e){{}}
      try {{ if (W.ryo) {{ W.ryo.x={x}; W.ryo.y={y}; W.ryo.v=0; W.path=[]; place(W.ryo,0); }}
            if (W.aoi) {{ W.aoi.x={x}-70; W.aoi.y={y}+30; place(W.aoi,0); }} camera(true); }} catch(e3){{}}
      return typeof c2Room==='function'?c2Room():null;
    }})()""")
    await ev(pg, HUSH)
    await pg.wait_for_timeout(350)

async def shot(pg, name):
    path = OUT / f'{name}.png'
    await pg.screenshot(path=str(path), type='png')
    print('shot', path, flush=True)

async def open_menu(pg, sid, nails=None):
    return await ev(pg, f"""(function(){{
      var M=root.FFF_S2MENUS, id={sid!r};
      if (!M) return {{err:'no menus'}};
      if (id==='s2_depot') M.SHOPS.s2_depot.wired=true;
      if ({'null' if nails is None else 'true'}) {{
        var want={str(bool(nails)).lower()};
        M.SHOPS[id]._nails0=M.SHOPS[id].nails;
        M.SHOPS[id].nails=function(){{return want;}};
      }}
      SAVE.items=40; SAVE.hp=40; SAVE.sp=20; try{{hud();}}catch(e){{}}
      M.open(id);
      var el=document.getElementById('wshop');
      return {{ on:!!(el&&el.classList.contains('on')), cls:el&&el.className, room:typeof c2Room==='function'?c2Room():null, x:W.ryo&&W.ryo.x, y:W.ryo&&W.ryo.y }};
    }})()""")

async def close_menu(pg):
    await ev(pg, """(function(){
      var M=root.FFF_S2MENUS;
      try{ if(M){ M.close(); if(M.SHOPS.s2_depot) M.SHOPS.s2_depot.wired=false;
        ['s2_chiyo','s2_hase','s2_depot'].forEach(function(id){ var s=M.SHOPS[id]; if(s&&s._nails0){ s.nails=s._nails0; delete s._nails0; } });
      } }catch(e){}
      return 1;
    })()""")

async def buy_item(pg, iid):
    # click the buy button for this item
    loc = await ev(pg, f"""(function(){{
      var b=document.querySelector('.s2m-it[data-i={iid!r}] button');
      if(!b||b.disabled) return null;
      var r=b.getBoundingClientRect();
      return [r.x+r.width/2, r.y+r.height/2, b.innerText];
    }})()""")
    if not loc:
        return {'err': 'no button', 'id': iid}
    await pg.touchscreen.tap(loc[0], loc[1])
    return {'tapped': loc, 'id': iid}

async def wait_menu(pg, timeout=12000):
    t0 = time.time()
    while (time.time() - t0) * 1000 < timeout:
        on = await ev(pg, "(function(){ var e=document.getElementById('wshop'); return !!(e&&e.classList.contains('on')&&e.querySelector('.s2m-it')); })()")
        if on: return True
        await pg.wait_for_timeout(200)
    return False

async def wait_eatg_done(pg, timeout=14000):
    t0 = time.time()
    started = False
    while (time.time() - t0) * 1000 < timeout:
        busy = await ev(pg, "(function(){ try{ return !!(root.EATG&&root.EATG.busy&&root.EATG.busy()); }catch(e){ return false; } })()")
        if busy: started = True
        if started and not busy: return True
        await pg.wait_for_timeout(150)
    return started

async def grab_frames(pg, folder, fps=12, seconds=10, until=None):
    folder = Path(folder); folder.mkdir(parents=True, exist_ok=True)
    n, t0 = 0, time.time()
    while time.time() - t0 < seconds:
        if until and await until(): break
        await pg.screenshot(path=str(folder / f'f{n:04d}.png'), type='png')
        n += 1
        await pg.wait_for_timeout(int(1000 / fps))
    return n

def encode_clip(folder, dest, fps=12):
    folder = Path(folder)
    dest = Path(dest)
    cmd = ['ffmpeg', '-y', '-framerate', str(fps), '-i', str(folder / 'f%04d.png'),
           '-vf', 'scale=390:844', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '22', str(dest)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print('ffmpeg', dest, r.returncode, (r.stderr or '')[-400:], flush=True)
    return r.returncode == 0

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

        # Chiyo: stand on the customer side of the counter
        await go_room(pg, 'waga', 640, 720)
        # full price board (staged — the counter stays closed until the row is taken)
        print('chiyo full', await open_menu(pg, 's2_chiyo', nails=False), flush=True)
        await pg.wait_for_timeout(250)
        await shot(pg, 'chiyo_menu_fullprice')
        await close_menu(pg)
        print('chiyo nails', await open_menu(pg, 's2_chiyo', nails=True), flush=True)
        await pg.wait_for_timeout(250)
        await shot(pg, 'chiyo_menu_nails')
        await close_menu(pg)

        # Hase: customer side of the counter (south of Hase at 780,520)
        await go_room(pg, 'mshop', 760, 660)
        print('hase full', await open_menu(pg, 's2_hase', nails=False), flush=True)
        await pg.wait_for_timeout(250)
        await shot(pg, 'hase_menu_fullprice')
        await close_menu(pg)
        print('hase nails', await open_menu(pg, 's2_hase', nails=True), flush=True)
        await pg.wait_for_timeout(250)
        await shot(pg, 'hase_menu_nails')
        await close_menu(pg)

        # Depot UI staged only (not wired into phase 5)
        print('depot full', await open_menu(pg, 's2_depot', nails=False), flush=True)
        await pg.wait_for_timeout(250)
        await shot(pg, 'depot_menu_fullprice')
        await close_menu(pg)
        print('depot nails', await open_menu(pg, 's2_depot', nails=True), flush=True)
        await pg.wait_for_timeout(250)
        await shot(pg, 'depot_menu_nails')
        await close_menu(pg)

        # ----- order clips -----
        foods = [
            ('s2_chiyo', 'roll', 'waga', 640, 720, 'order_sweetroll.mp4', 12),
            ('s2_chiyo', 'dango', 'waga', 640, 720, 'order_dango.mp4', 12),
            ('s2_chiyo', 'hojicha', 'waga', 640, 720, 'order_hojicha.mp4', 8),
            ('s2_hase', 'cancoffee', 'mshop', 760, 660, 'order_cancoffee.mp4', 8),
        ]
        for sid, iid, room, x, y, fname, secs in foods:
            await go_room(pg, room, x, y)
            await ev(pg, "SAVE.items=40; SAVE.hp=30; SAVE.sp=10; try{hud();}catch(e){} root.FFF_EATG_BOT='win';")
            print('open for', iid, await open_menu(pg, sid, nails=True), flush=True)
            await pg.wait_for_timeout(300)
            tmp = Path('/tmp/s2m-clip') / iid
            if tmp.exists(): shutil.rmtree(tmp)
            tmp.mkdir(parents=True)
            async def act():
                r = await buy_item(pg, iid)
                print('buy', iid, r, flush=True)
                if iid in ('roll', 'dango'):
                    await wait_eatg_done(pg, 14000)
                    await wait_menu(pg, 8000)
                else:
                    await pg.wait_for_timeout(2000)
                    await wait_menu(pg, 4000)
            # grab frames concurrently with the buy
            grab = asyncio.create_task(grab_frames(pg, tmp, fps=12, seconds=secs + 4))
            await act()
            await pg.wait_for_timeout(600)
            grab.cancel()
            try:
                await grab
            except asyncio.CancelledError:
                pass
            # if too few frames, grab a couple more
            if len(list(tmp.glob('f*.png'))) < 8:
                await grab_frames(pg, tmp, fps=8, seconds=1)
            encode_clip(tmp, CLIP / fname, fps=12)
            await close_menu(pg)

        print('errs', errs[:4], flush=True)
        await b.close()
    s.server_close()

if __name__ == '__main__':
    asyncio.run(main())
