#!/workspace/pwenv/bin/python3
"""NG+ Gouki harness (Playwright). Serves the given index.html with assets from the worktree root (ASSETS env overrides)."""
import asyncio, functools, http.server, socketserver, threading, os, json, socket
from pathlib import Path
from playwright.async_api import async_playwright
ASSET_DIR = os.environ.get('ASSETS', str(Path(__file__).resolve().parent.parent.parent))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True; daemon_threads = True
HUSH = """(function(){try{if(typeof phClose==='function')phClose()}catch(e){}W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};return 1})()"""
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^(Skip)/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
NX = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^(Next|Skip|Continue|OK|Nice)/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
# hooks: every AU.play name, every ev(), every fight() ctx
HOOK = """(function(){ if(window.__hk) return 1; window.__hk=1; window.__snd=[]; window.__evs=[]; window.__ctxs=[];
  var p0=AU.play; AU.play=function(n,o){ try{ window.__snd.push(Math.round(performance.now())+' '+n) }catch(e){} return p0.apply(this,arguments) };
  var e0=ev; ev=function(k){ try{ window.__evs.push(Math.round(performance.now())+' '+k) }catch(e){} return e0.apply(this,arguments) };
  var f0=fight; fight=function(grp,boss,ctx){ try{ window.__ctxs.push({grp:grp,boss:boss,ctx:ctx}) }catch(e){} return f0.apply(this,arguments) };
  return 1})()"""
class Game:
    def __init__(self, index, out=os.environ.get('SHOTS', '/workspace/ngpgouki/shots')):
        self.index = Path(index); self.out = Path(out); self.out.mkdir(parents=True, exist_ok=True); self.errs = []; self.dpr = 1
        k = socket.socket(); k.bind(('127.0.0.1', 0)); self.port = k.getsockname()[1]; k.close()
    async def __aenter__(self):
        self.srv = TS(('127.0.0.1', self.port), functools.partial(Q, directory=ASSET_DIR))
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.p = await async_playwright().start()
        self.b = await self.p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required'])
        self.ctx = await self.b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=self.dpr)
        self.pg = await self.ctx.new_page(); self.pg.on('pageerror', lambda e: self.errs.append(str(e)))
        html = self.index.read_text(encoding='utf-8'); assert 'root.FFF_13U = { CONTEST' in html
        html = html.replace('root.FFF_13U = { CONTEST', 'root.__ev=function(s){return eval(s)};root.FFF_13U = { CONTEST', 1)
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
        for i in range(n):
            c = await self.pg.evaluate(SK)
            if not c:
                await self.wait(200); c = await self.pg.evaluate(SK)
                if not c: break
            await self.pg.touchscreen.tap(*c); await self.wait(200)
    async def adv(self, n=40):
        idle = 0
        for i in range(n):
            c = await self.pg.evaluate(NX)
            if not c:
                idle += 1
                if idle > 4: return i
                await self.wait(300); continue
            idle = 0; await self.pg.touchscreen.tap(*c); await self.wait(350)
        return n
    async def hush(self): await self.ev(HUSH)
    async def boot(self):
        await self.pg.touchscreen.tap(195, 420)
        await self.pg.evaluate("WORLD_API.enter(true)"); await self.wait(1500); await self.skipall()
        await self.ev("root.FFF_NO_TUT=1"); await self.hush(); await self.ev(HOOK)
    async def shot(self, name):
        p = self.out / f'{name}.png'; await self.pg.screenshot(path=str(p), type='png'); print('shot', p, flush=True); return p
