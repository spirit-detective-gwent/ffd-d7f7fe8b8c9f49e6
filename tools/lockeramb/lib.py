#!/workspace/pwenv/bin/python3
"""v6565-nursecab: Ch1 nurse white cabinet restocks once per Ch1 MAIN quest (1 gauze + 1 tape, no timer, no stacking).
usage: test_cab.py <worktree> [port] [--shots DIR] [--live]   (--live: only the 'before' shot, on a tree without cabQuestDone)
Real game functions in a headless 390x844 page."""
import asyncio, sys, functools, http.server, socketserver, threading, json
from pathlib import Path
from playwright.async_api import async_playwright
args = sys.argv[1:]
def opt(name, flag=False):
    if name in args:
        i = args.index(name)
        if flag: del args[i]; return True
        v = args[i + 1]; del args[i:i + 2]; return v
shots = opt('--shots'); live = opt('--live', True)
root = Path(args[0]); PORT = int(args[1]) if len(args) > 1 else 52671
class TS(socketserver.ThreadingTCPServer): allow_reuse_address = True; daemon_threads = True
def serve(rt, port):
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_GET(self):
            if self.path.split('?', 1)[0] in ('/', '/index.html'):
                raw = (rt / 'index.html').read_bytes(); n = b'root.WORLD_API = {'
                raw = raw.replace(n, b'root.__ev=function(s){return eval(s)};' + n, 1)
                self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(raw))); self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(raw); return
            return super().do_GET()
    h = TS(('127.0.0.1', port), functools.partial(Q, directory=str(rt))); threading.Thread(target=h.serve_forever, daemon=True).start(); return h
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
async def ev(pg, code):
    return await pg.evaluate("(c)=>{try{var r=__ev(c);return (r===undefined)?null:JSON.parse(JSON.stringify(r))}catch(e){return {__err:String(e&&e.message||e)}}}", code)
async def skipall(pg, n=12):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(300); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(280)
    await pg.evaluate("(()=>{var b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Close'&&e.offsetParent);if(b)b.click()})()")
RES = []
def ok(name, cond, extra=''):
    RES.append((bool(cond), name)); print(('PASS ' if cond else 'FAIL ') + name + ((' :: ' + str(extra)[:300]) if extra else ''), flush=True)
async def boot(p, init=None):
    b = await p.chromium.launch(headless=True, args=['--disable-dev-shm-usage'])
    ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True,
      user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mobile/15E148 Safari/604.1')
    if init: await ctx.add_init_script(init)
    pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(3500)
    await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(2500); await skipall(pg, 12)
    return b, ctx, pg, errs
CLR = "(function(){ W.scGen=(W.scGen|0)+1; try{sLock(0,'x')}catch(e){} try{close()}catch(e){} W.cut=false; W.dlg=false; W.scr=false; W.busy=false; W.qBusy=0; document.body.classList.remove('fff-dlg-on'); var o=document.getElementById('wquest'); if(o) o.remove(); })()"
DLG = "(function(){ var d=document.getElementById('wdlg'); return d&&d.offsetParent!==null? d.innerText : ''; })()"
CLOSE = "(()=>{var b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Close'&&e.offsetParent);if(b)b.click()})()"
