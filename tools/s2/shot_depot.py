#!/workspace/pwenv/bin/python3
"""After-seal depot counter stills and a short onigiri order clip."""
import asyncio, functools, http.server, socketserver, threading, os, time, subprocess, shutil
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
INDEX = HERE.parent.parent / 'index.html'
OUT = Path('/workspace/v6560-review/shopmenus/depot')
OUT.mkdir(parents=True, exist_ok=True)
PORT = int(os.environ.get('PORT', '8866'))

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
      SAVE.items=40; SAVE.hp=28; SAVE.sp=20;
      try { STORY.ensure(SAVE); } catch(e){}
      var st=c2S(); st.e=st.e||{}; st.e.run_fac='arc'; st.e.seal_sento=1; st.e.sealKnown=1; st.e.c2sRep=1; st.e.c2lMap=1;
      st.e.n13='done'; st.e.arrive=1; st.e.gymIn=1; st.e.genji=1; st.e.nq=st.e.nq||{};
      st.q=st.q||{}; st.q.cq2_nq_west=9; st.q.cq2_nq_cold=9; st.q.cq2_nq_paint=9; st.q.cq2_nq_door=9; st.q.cq2_nq_seal=9;
      st.q.cq2_s2_gar=9; st.q.cq2_s2_waga=9; st.q.cq2_locks=0; st.qa='cq2_locks';
      st.e.seal_depot=1; st.e.down_dep=1; st.e.eastSeal=1; st.e.nq.dep='done'; st.q.cq2_s2_depot=9;
      try { if (root.FFF_S2P5 && FFF_S2P5.setStg) FFF_S2P5.setStg('done'); } catch(eS){}
      try { c2QSync(); save(); hud(); } catch(e){}
      root.FFF_EATG_BOT='win';
      return { p5:!!root.FFF_S2P5, menus:!!root.FFF_S2MENUS, after:!!(root.FFF_S2P5&&FFF_S2P5.afterSeal&&FFF_S2P5.afterSeal()), yen:SAVE.items };
    })()""")

async def go_clock(pg):
    return await ev(pg, """(function(){
      try { c2Go('dclock', [550, 780, 3]); } catch(e){}
      try {
        if (W.ryo) { W.ryo.x=550; W.ryo.y=780; W.ryo.v=0; W.path=[]; if (typeof c2Face==='function') c2Face(W.ryo, 550, 500); place(W.ryo,0); }
        if (W.aoi) { W.aoi.x=480; W.aoi.y=810; place(W.aoi,0); }
      } catch(e3){}
      try { if (typeof c2Pop==='function') c2Pop(); } catch(eP){}
      try { if (root.FFF_S2P5 && FFF_S2P5.popClerk) FFF_S2P5.popClerk(); } catch(eC){}
      try { if (root.FFF_S2P5 && FFF_S2P5.paintRoom) FFF_S2P5.paintRoom(); } catch(e5){}
      try { camera(true); } catch(eCa){}
      var clk=W.c2n&&W.c2n.s2depclk;
      return { room:typeof c2Room==='function'?c2Room():null, clk:!!clk, cx:clk&&clk.x, cy:clk&&clk.y, x:W.ryo&&W.ryo.x, y:W.ryo&&W.ryo.y };
    })()""")

async def shot(pg, name):
    path = OUT / f'{name}.png'
    await pg.screenshot(path=str(path), type='png')
    print('shot', path, flush=True)
    return path

async def open_menu(pg):
    return await ev(pg, """(function(){
      var M=root.FFF_S2MENUS;
      SAVE.items=40; SAVE.hp=28; SAVE.sp=12; try{hud();}catch(e){}
      M.open('s2_depot');
      var el=document.getElementById('wshop');
      var html=el?el.innerHTML:'';
      return { on:!!(el&&el.classList.contains('on')), cls:el&&el.className, pt:html.indexOf('endo_neutral')>=0, nails:/<s>/.test(html), x:W.ryo&&W.ryo.x, y:W.ryo&&W.ryo.y };
    })()""")

async def buy_item(pg, iid):
    loc = await ev(pg, f"""(function(){{
      var id={iid!r};
      var b=document.querySelector('.s2m-it[data-i="'+id+'"] button');
      if(!b){{
        var nodes=document.querySelectorAll('.s2m-it');
        for(var i=0;i<nodes.length;i++){{ if(nodes[i].getAttribute('data-i')===id) b=nodes[i].querySelector('button'); }}
      }}
      if(!b||b.disabled) return null;
      var r=b.getBoundingClientRect();
      return [r.x+r.width/2, r.y+r.height/2, b.innerText];
    }})()""")
    if not loc:
        return {'err': 'no button', 'id': iid}
    await pg.touchscreen.tap(loc[0], loc[1])
    return {'tapped': loc, 'id': iid}

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
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        pg = await ctx.new_page()
        html = body()
        async def rt(route): await route.fulfill(body=html, content_type='text/html')
        await pg.route('**/index.html', rt)
        await pg.goto(f'http://127.0.0.1:{PORT}/index.html')
        await pg.wait_for_timeout(2200)
        boot_r = await boot(pg)
        print('boot', boot_r, flush=True)
        await ev(pg, HUSH)
        clock = await go_clock(pg)
        print('clock', clock, flush=True)
        await pg.wait_for_timeout(500)
        await shot(pg, 'counter')
        menu = await open_menu(pg)
        print('menu', menu, flush=True)
        await pg.wait_for_timeout(300)
        await shot(pg, 'menu_nails')
        # order clip: close and reopen with mid HP, then buy onigiri
        await ev(pg, HUSH)
        await go_clock(pg)
        await open_menu(pg)
        await pg.wait_for_timeout(200)
        tmp = Path('/tmp/s2m-depot-clip'); shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
        buy = await buy_item(pg, 'onigiri')
        print('buy', buy, flush=True)
        async def until():
            # stop a beat after EATG finishes and the menu is back, or after handoff if eatg never starts
            st = await ev(pg, """(function(){
              var eat=false; try{ eat=!!(root.EATG&&root.EATG.busy&&root.EATG.busy()); }catch(e){}
              var menu=!!(document.getElementById('wshop')&&document.getElementById('wshop').classList.contains('on'));
              var hand=!!document.querySelector('.s2m-hand');
              return {eat:eat, menu:menu, hand:hand};
            })()""")
            until._seen_eat = getattr(until, '_seen_eat', False) or (st and st.get('eat'))
            until._seen_hand = getattr(until, '_seen_hand', False) or (st and st.get('hand'))
            if until._seen_eat and st and not st.get('eat') and st.get('menu'):
                return True
            return False
        n = await grab_frames(pg, tmp, fps=12, seconds=9, until=until)
        print('frames', n, flush=True)
        encode_clip(tmp, OUT / 'order_onigiri.mp4', fps=12)
        await b.close()
    s.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
