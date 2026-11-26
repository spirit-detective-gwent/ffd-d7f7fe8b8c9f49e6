"""Shared harness for the Ch2 bond-moment tests/clips (serves a worktree; review-only, no publish)."""
import asyncio, os, sys, time, json, http.server, socketserver, threading, functools, subprocess, shutil, base64
from pathlib import Path
from playwright.async_api import async_playwright
FFD = os.environ.get('FFD', '/workspace/ffd-bond')
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
HUSH = """(function(){try{if(typeof phClose==='function')phClose()}catch(e){}try{close()}catch(e2){}W.scGen=(W.scGen|0)+1;W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];try{while((W.scr|0)>0)sLock(0)}catch(e5){}var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''}try{if(typeof commentHide==='function')commentHide()}catch(e3){}try{FFF_SCAM.clear()}catch(e7){}return 1})()"""
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True; daemon_threads = True
def serve(port, root=None):
    s = TS(('127.0.0.1', port), functools.partial(Q, directory=root or FFD))
    threading.Thread(target=s.serve_forever, daemon=True).start(); return s
def inject(path=None):
    t = Path(path or (FFD + '/index.html')).read_text(encoding='utf-8')
    n = 'root.FFF_13U = { CONTEST'; assert n in t
    return t.replace(n, 'root.__ev=function(s){return eval(s)};' + n, 1)
async def ev(pg, code):
    return await pg.evaluate("""(c)=>{try{var r=__ev(c);return (r&&typeof r.then==='function')?'THEN':(typeof r==='string'?r:JSON.parse(JSON.stringify(r===undefined?null:r)))}catch(e){return 'ERR:'+e.message}}""", code)
async def skipall(pg, n=10):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(200); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(280)
async def boot(pg, port, body):
    async def rt(route): await route.fulfill(body=body, content_type='text/html')
    await pg.route('**/index.html', rt)
    await pg.goto(f'http://127.0.0.1:{port}/index.html', wait_until='domcontentloaded', timeout=90000)
    await pg.wait_for_timeout(2500)
    await pg.touchscreen.tap(195, 420); await pg.wait_for_timeout(300)
    await ev(pg, "(function(){try{root.FFF_CRAWL_MS=1;ST.set.cam='on';ST.set.txt='fast';ST.set.tips=false}catch(e){}return 1})()")
    await pg.evaluate('WORLD_API.enter(true)'); await pg.wait_for_timeout(2000)
    await ev(pg, HUSH)
    await ev(pg, "(function(){SAVE.intro=1;SAVE.sc=SAVE.sc||{};SAVE.sc.nurse=1;root.FFF_NURSE_SKIP=1;SAVE.icard={ryo:1,aoi:1,nurse:1};SAVE.bent={};SAVE.splVs={};return 1})()")
async def ch2(pg):
    await pg.evaluate('WORLD_API.c2Begin(true)'); await pg.wait_for_timeout(2500); await skipall(pg, 4); await ev(pg, HUSH)

# ---- virtual-time recorder (60 fps, deterministic; WAAPI is stepped from rAF because it runs on the compositor clock) ----
SHIM = r"""(function(){var L=[],o=Element.prototype.animate;Element.prototype.animate=function(k,op){var a=o.call(this,k,op);try{a.pause();var d=typeof op==='number'?op:((op&&op.delay)||0)+((op&&op.duration)||0);L.push({a:a,t0:performance.now(),d:d})}catch(e){}return a};
(function f(){var n=performance.now();L=L.filter(function(x){try{if(x.a.playState==='idle')return false;var t=n-x.t0;if(t>=x.d){x.a.finish();return false}x.a.currentTime=t}catch(e){return false}return true});requestAnimationFrame(f)})()})();"""
class VT:
    def __init__(s, pg, ctx, outdir):
        s.pg, s.ctx, s.out, s.n = pg, ctx, outdir, 0
        shutil.rmtree(outdir, ignore_errors=True); os.makedirs(outdir, exist_ok=True)
    async def start(s):
        s.cdp = await s.ctx.new_cdp_session(s.pg); s.ev = asyncio.Event()
        s.cdp.on('Emulation.virtualTimeBudgetExpired', lambda e: s.ev.set())
        await s.cdp.send('Emulation.setVirtualTimePolicy', {'policy': 'pause'})
    async def step(s, shot=True):
        s.ev.clear()
        await s.cdp.send('Emulation.setVirtualTimePolicy', {'policy': 'pauseIfNetworkFetchesPending', 'budget': 1000 / 60.0})
        await asyncio.wait_for(s.ev.wait(), 30)
        if shot:
            r = await s.cdp.send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 80})
            open(f'{s.out}/f{s.n:05d}.jpg', 'wb').write(base64.b64decode(r['data'])); s.n += 1
    async def run(s, secs, shot=True):
        for i in range(int(round(secs * 60))): await s.step(shot)
def encode(d, out, fps=60):
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', f'{d}/f%05d.jpg', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', str(out)])
