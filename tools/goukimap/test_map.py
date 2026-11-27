#!/workspace/pwenv/bin/python3
"""v6566-goukimap (Erik t535u): the nurse desk map shows the red Xs and the SE circle, never an orange Gouki pin.
usage: test_map.py <worktree> [port] [--shots DIR] [--live]"""
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
root = Path(args[0]); PORT = int(args[1]) if len(args) > 1 else 52691
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

CLR = "(function(){ W.scGen=(W.scGen|0)+1; try{sLock(0,'x')}catch(e){} try{close()}catch(e){} W.cut=false; W.dlg=false; W.scr=false; W.busy=false; W.qBusy=0; document.body.classList.remove('fff-dlg-on'); var q=document.getElementById('qmap'); if(q) q.remove(); })()"
MARKS = "(function(){ var o=document.getElementById('qmap'); if(!o) return null; return [...o.querySelectorAll('.qmk')].map(function(e){ var cs=getComputedStyle(e); return [e.dataset.id, e.className, cs.backgroundImage.indexOf('196, 90, 16')>=0 || cs.backgroundImage.indexOf('c45a10')>=0]; }); })()"
async def main():
    h = serve(root, PORT)
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p)
        await ev(pg, CLR)
        # 1) the script itself
        steps = await ev(pg, "QTALK.q_mb_cafe.filter(function(l){return l[0]==='@map'}).map(function(l){return l[1]})")
        print('map steps:', steps)
        if not live:
            ok('q_mb_cafe has no gouki map step', 'gouki' not in steps, steps)
            ok('q_mb_cafe keeps on / 3 Xs / se / off', steps == ['on', 'x:mb_lib', 'x:mb_art', 'x:mb_cafe', 'se', 'off'], steps)
        # 2) play the real desk-map conversation (map + dialog rows only; no quest side effects)
        await ev(pg, "(function(){ root.__evlog=[]; var o=root.ev; root.FFF_CIN_K=0.5; W.__mapscene=0; var L=QTALK.q_mb_cafe.filter(function(l){return l[0]!=='@done'&&l[0]!=='@quest'}); scene('t_goukimap', L, function(){ W.__mapscene=1; }); return L.length; })()")
        seen = {}; shot = False; t = 0
        while t < 90:
            m = await ev(pg, MARKS)
            if m:
                for e in m: seen[e[0]] = e
                ids = [e[0] for e in m]
                if 'mb_field' in ids and not shot:
                    await pg.wait_for_timeout(500)
                    if shots:
                        nm = ('before_live' if live else 'after_branch') + '_desk_map.png'
                        await pg.screenshot(path=str(Path(shots) / nm)); print('shot', nm)
                        try:
                            from PIL import Image
                            bx = await ev(pg, "(function(){ var r=document.querySelector('#qmap .qmin').getBoundingClientRect(); return [r.left,r.top,r.right,r.bottom]; })()")
                            im = Image.open(str(Path(shots) / nm)); im.crop(tuple(int(v) for v in [max(0,bx[0]-8), max(0,bx[1]-8), min(390,bx[2]+8), min(844,bx[3]+8)])).resize((int((bx[2]-bx[0]+16)*2), int((bx[3]-bx[1]+16)*2))).save(str(Path(shots) / nm.replace('.png', '_zoom.png')))
                        except Exception as eZ: print('zoom failed', eZ)
                    shot = True
            if await ev(pg, "W.__mapscene"): break
            await pg.evaluate("(()=>{var d=document.getElementById('wdlg'); if(d&&d.offsetParent) d.click();})()")
            await pg.wait_for_timeout(450); t += 1
        print('marks seen:', list(seen.values()))
        done = await ev(pg, "W.__mapscene"); gone = await ev(pg, "!document.getElementById('qmap')")
        if not live:
            ok('scene finished', done == 1)
            ok('3 red Xs placed', all(k in seen and 'qx' in seen[k][1] for k in ['mb_lib', 'mb_art', 'mb_cafe']), seen)
            ok('SE storehouse circle placed', 'mb_field' in seen and 'qc' in seen['mb_field'][1], seen)
            ok('no Gouki pin ever placed', 'gouki' not in seen and not any('qg' in v[1] or v[2] for v in seen.values()), seen)
            ok('map closed at end', gone)
            # 3) old / mid-flight callers of the 'gouki' step: no pin, callback still fires
            await ev(pg, CLR)
            r = await ev(pg, "(function(){ root.__gk=0; qMap('on', function(){}); qMap('gouki', function(){ root.__gk=1; }); return 1; })()")
            await pg.wait_for_timeout(400)
            ok("legacy qMap('gouki') continues the scene", await ev(pg, "root.__gk") == 1)
            ok("legacy qMap('gouki') draws no pin", await ev(pg, "document.querySelectorAll('#qmap .qmk').length") == 0)
            ok('qg pin CSS gone', await ev(pg, "(function(){ for (var s of document.styleSheets) { try { for (var r of s.cssRules) if (r.selectorText && r.selectorText.indexOf('.qmk.qg')>=0) return false; } catch(e){} } return true; })()"))
            await ev(pg, "qMap('off')")
        else:
            print('LIVE gouki pin present:', 'gouki' in seen)
        ok('no page errors', not errs, errs)
        await b.close()
    h.shutdown()
    bad = [n for c, n in RES if not c]
    print(f"{len(RES)-len(bad)}/{len(RES)} PASS"); sys.exit(1 if bad else 0)
asyncio.run(main())
