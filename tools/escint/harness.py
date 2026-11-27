"""Shared Playwright harness for the escint tests (static server with __ev hook, 390x844 touch phone)."""
import asyncio, functools, http.server, socketserver, threading, json
from pathlib import Path
from playwright.async_api import async_playwright

class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def serve(root, port):
    root = Path(root).resolve()
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_GET(self):
            if self.path.split('?', 1)[0] in ('/', '/index.html'):
                raw = (root / 'index.html').read_bytes()
                n = b'root.WORLD_API = {'
                raw = raw.replace(n, b'root.__ev=function(s){return eval(s)};' + n, 1)
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(raw)))
                self.send_header('Cache-Control', 'no-store')
                self.end_headers(); self.wfile.write(raw); return
            return super().do_GET()
    h = TS(('127.0.0.1', port), functools.partial(Q, directory=str(root)))
    threading.Thread(target=h.serve_forever, daemon=True).start()
    return h

SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""

async def ev(pg, code):
    return await pg.evaluate(
        "(c)=>{try{var r=__ev(c);return (r===undefined)?null:JSON.parse(JSON.stringify(r))}catch(e){return {__err:String(e&&e.message||e)}}}", code)

async def skipall(pg, n=12):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(250)
            c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c)
        await pg.wait_for_timeout(250)
    await pg.evaluate("(()=>{var b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Close'&&e.offsetParent);if(b)b.click()})()")

async def boot(p, port, enter=True):
    b = await p.chromium.launch(headless=True, args=['--disable-dev-shm-usage'])
    ctx = await b.new_context(
        viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True,
        user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
    pg = await ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:240]))
    await pg.goto(f'http://127.0.0.1:{port}/index.html')
    await pg.wait_for_timeout(3500)
    if enter:
        await pg.evaluate("WORLD_API.enter(true)")
        await pg.wait_for_timeout(2000)
        await skipall(pg, 12)
    return b, ctx, pg, errs

READY = """(function(){try{unstage&&unstage()}catch(e){};W.scGen=(W.scGen|0)+1;SAVE.intro=1;SAVE.sc=SAVE.sc||{};SAVE.sc.nurse=1;SAVE.sc.after=1;SAVE.sc.why=1;W.dlg=false;W.busy=false;W.scr=0;W.cut=false;W.path=[];var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};W.ryo.x=X;W.ryo.y=Y;W.aoi.x=X;W.aoi.y=Y+60;resetTrail(X,Y,3);camera(true);return 1})()"""

async def ch1_ready(pg, x=1800, y=2900):
    r = await ev(pg, READY.replace('X', str(x)).replace('Y', str(y)))
    await pg.wait_for_timeout(600)
    return r
