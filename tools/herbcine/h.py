#!/workspace/pwenv/bin/python3
"""Shared headless harness for v6564-jin. import h; async with h.Game() as g: ..."""
import asyncio, functools, http.server, socketserver, threading, os, sys, json
from pathlib import Path
from playwright.async_api import async_playwright
INDEX = Path(os.environ.get('FFD_INDEX', '/workspace/herbcine/wt/index.html'))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True; daemon_threads = True
HUSH = """(function(){try{if(typeof phClose==='function')phClose()}catch(e){}
W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];
var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};
var q=document.getElementById('wquest'); if(q) q.style.display='none';
return 1})()"""
SETUP = """(function(){
  SAVE.chapter=2; SAVE.ch1=1; SAVE.ch2=1; SAVE.bond=SAVE.bond||{}; SAVE.bond.path='%(path)s'; SAVE.bond.lock=1;
  try { STORY.ensure(SAVE); } catch(e){}
  var st=c2S(); st.e=st.e||{}; st.e.run_fac='arc'; st.e.seal_sento=1; st.e.sealKnown=1; st.e.c2sRep=1; st.e.c2lMap=1;
  st.e.n13='done'; st.e.arrive=1; st.e.gymIn=1; st.e.genji=1; st.e.nq=st.e.nq||{};
  st.q.cq2_arrive=9; st.q.cq2_hq=9; st.q.cq2_scout=9;
  st.q.cq2_nq_west=9; st.q.cq2_nq_cold=9; st.q.cq2_nq_paint=9; st.q.cq2_nq_door=9; st.q.cq2_nq_seal=9;
  st.q.cq2_locks=0; st.qa='cq2_locks';
  st.q.cq2_s2_waga=9; if (root.FFF_S2&&root.FFF_S2.setStg) root.FFF_S2.setStg('done');
  st.q.cq2_s2_runs=9; if (root.FFF_S2P2&&root.FFF_S2P2.setStg) root.FFF_S2P2.setStg('done');
  st.q.cq2_s2_boat=9; if (root.FFF_S2P3&&root.FFF_S2P3.setStg) root.FFF_S2P3.setStg('done');
  st.q.cq2_s2_gar=9; if (root.FFF_S2P4&&root.FFF_S2P4.setStg) root.FFF_S2P4.setStg('done');
  st.e.baseOpen_dep=1; st.e.guardGone_depot=1;
  %(seal2)s
  st.e.nq.udon=1; SAVE.items=Math.max(SAVE.items|0, 300);
  try { c2QSync(); save(); } catch(e){}
  try { if (root.FFF_S2P5&&root.FFF_S2P5.chainRepair) root.FFF_S2P5.chainRepair(); } catch(e5){}
  try { if (root.FFF_S2P6&&root.FFF_S2P6.chainRepair) root.FFF_S2P6.chainRepair(); } catch(e6){}
  return { p5:!!root.FFF_S2P5, p6:!!root.FFF_S2P6, q5:st.q.cq2_s2_depot, q6:st.q.cq2_s2_jin };
})()"""
SEAL2 = "st.e.seal_depot=1; st.e.down_dep=1; st.q.cq2_s2_depot=9; if (root.FFF_S2P5&&root.FFF_S2P5.setStg) root.FFF_S2P5.setStg('done'); st.e.masaFate='help';"
class Game:
    def __init__(self, port=None, out='/workspace/herbcine/shots', path='fierce', seal2=True, throttle=None):
        self.throttle = throttle
        import socket as _s; _k=_s.socket(); _k.bind(('127.0.0.1',0)); _fp=_k.getsockname()[1]; _k.close()
        self.port = port or int(os.environ.get('PORT', _fp)); self.out = Path(out); self.out.mkdir(parents=True, exist_ok=True)
        self.path = path; self.seal2 = seal2; self.errs = []
    async def __aenter__(self):
        self.srv = TS(('127.0.0.1', self.port), functools.partial(Q, directory=str(INDEX.parent)))
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.p = await async_playwright().start()
        self.b = await self.p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required'])
        self.ctx = await self.b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=float(os.environ.get('DSF','1')), **({'record_video_dir': os.environ['VID'], 'record_video_size': {'width': 390, 'height': 844}} if os.environ.get('VID') else {}))
        self.pg = await self.ctx.new_page(); self.pg.on('pageerror', lambda e: self.errs.append(str(e)))
        if self.throttle:
            self.cdp = await self.ctx.new_cdp_session(self.pg); await self.cdp.send('Emulation.setCPUThrottlingRate', {'rate': self.throttle})
        self.pg.on('console', lambda m: (m.type == 'error') and self.errs.append('console:' + m.text[:300]))
        html = INDEX.read_text(encoding='utf-8').replace('root.FFF_13U = { CONTEST', 'root.__ev=function(s){return eval(s)};root.FFF_13U = { CONTEST', 1)
        async def rt(route): await route.fulfill(body=html, content_type='text/html')
        await self.pg.route('**/index.html', rt)
        await self.pg.goto(f'http://127.0.0.1:{self.port}/index.html', timeout=120000); await self.pg.wait_for_timeout(2200)
        return self
    async def __aexit__(self, *a):
        try: await self.b.close(); await self.p.stop()
        finally: self.srv.shutdown(); self.srv.server_close()
    async def ev(self, code):
        return await self.pg.evaluate("(c)=>{var r=window.__ev(c);try{return (typeof r==='string')?r:JSON.parse(JSON.stringify(r===undefined?null:r))}catch(e){return String(r)}}", code)
    async def wait(self, ms): await self.pg.wait_for_timeout(ms)
    async def skipall(self, n=8):
        SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
        for i in range(n):
            c = await self.pg.evaluate(SK)
            if not c:
                await self.wait(200); c = await self.pg.evaluate(SK)
                if not c: break
            await self.pg.touchscreen.tap(*c); await self.wait(200)
    async def hush(self): await self.ev(HUSH)
    async def boot(self):
        pg = self.pg
        await pg.touchscreen.tap(195, 420)
        await pg.evaluate("WORLD_API.enter(true)"); await self.wait(1500); await self.skipall()
        await self.ev("root.FFF_NO_TUT=1")
        await pg.evaluate("WORLD_API.c2Begin(true)"); await self.wait(2500); await self.skipall(); await self.hush()
        return await self.ev(SETUP % {'path': self.path, 'seal2': SEAL2 if self.seal2 else ''})
    async def go(self, k, x=640, y=720, face=0):
        r = await self.ev(f"""(function(){{
          try {{ c2Go('{k}', [{x}, {y}, {face}]); }} catch(e){{ return 'goerr '+e.message }}
          try {{ if (typeof c2Pop==='function') c2Pop(); }} catch(e2){{}}
          try {{ if (W.ryo) {{ W.ryo.x={x}; W.ryo.y={y}; place(W.ryo,0); }} if (W.aoi) {{ W.aoi.x={x}-70; W.aoi.y={y}+30; place(W.aoi,0); }} camera(true); }} catch(e3){{}}
          return typeof c2Room==='function'?c2Room():null; }})()""")
        await self.wait(700); await self.hush(); await self.wait(200)
        return r
    async def shot(self, name, hush=True):
        if hush: await self.hush(); await self.wait(150)
        p = self.out / f'{name}.png'; await self.pg.screenshot(path=str(p), type='png'); print('shot', p, flush=True); return p
    async def tap(self, x, y): await self.pg.touchscreen.tap(x, y)
NX = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^(Next|Skip|Continue|OK)/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
async def adv(self, n=40, stop=None):
    """press Next/Skip until no dialog button for ~1s, or stop() js truthy"""
    idle = 0
    for i in range(n):
        if stop and await self.ev(stop): return i
        c = await self.pg.evaluate(NX)
        if not c:
            idle += 1
            if idle > 4: return i
            await self.wait(300); continue
        idle = 0
        await self.pg.touchscreen.tap(*c); await self.wait(350)
    return n
Game.adv = adv

async def enter(self, k, x=None, y=None, face=0):
    """natural room entry (c2Enter): one set of NPC sprites, same as play. Optionally then stand Ryo at x,y."""
    await self.ev(f"c2Enter('{k}')"); await self.wait(1500); await self.hush()
    if x is not None:
        await self.ev(f"(function(){{ W.ryo.x={x}; W.ryo.y={y}; place(W.ryo,0); if (W.aoi) {{ W.aoi.x={x}-70; W.aoi.y={y}+30; place(W.aoi,0); }} camera(true); return 1 }})()")
        await self.wait(400)
    await self.hush(); return await self.ev("c2Room()")
Game.enter = enter
