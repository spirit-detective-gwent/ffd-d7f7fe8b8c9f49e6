#!/workspace/pwenv/bin/python3
"""Ch1 + Ch2 boot smoke. Boots each chapter, skips intros, visits a few spots, asserts no page errors
and that Ch2 new-art characters never resolve to a removed old sheet.
usage: ch_smoke.py <worktree> [port]  -> PASS/FAIL, exit 1 on fail."""
import asyncio, sys, functools, http.server, socketserver, threading, re
from pathlib import Path
from playwright.async_api import async_playwright
root = Path(sys.argv[1]); PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 52601
class TS(socketserver.ThreadingTCPServer): allow_reuse_address = True; daemon_threads = True
def serve():
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_GET(self):
            if self.path.split('?', 1)[0] in ('/', '/index.html'):
                raw = (root / 'index.html').read_bytes(); n = b'root.WORLD_API = {'
                raw = raw.replace(n, b'root.__ev=function(s){return eval(s)};' + n, 1)
                self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(raw))); self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(raw); return
            return super().do_GET()
    h = TS(('127.0.0.1', PORT), functools.partial(Q, directory=str(root))); threading.Thread(target=h.serve_forever, daemon=True).start(); return h
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
    RES.append((bool(cond), name, extra)); print(('PASS ' if cond else 'FAIL ') + name + ((' :: ' + str(extra)[:240]) if extra and not cond else ''), flush=True)
OLD = re.compile(r'c2x_act_(punk|hustler)(?!Y)|world/(c2_punk|c2_hustler|mb2_sento|goda)_')
async def scan_old(pg, tag):
    r = await pg.evaluate("""()=>[...document.querySelectorAll('#world .wsp')].map(e=>{var bi=e.style.backgroundImage||'';var m=bi.match(/world\\/([^?")]+)/);return {who:e.dataset.who||'',loop:e.dataset.loop||'',bg:m?m[1]:(bi.indexOf('data:')>=0?'DATA':(bi.indexOf('blob:')>=0?'BLOB':'')),cls:e.className}})""")
    bad = [q for q in r if OLD.search((q.get('loop') or '') + ' ' + (q.get('bg') or '')) or (q.get('loop') in ('c2x_act_punk', 'c2x_act_hustler'))]
    ok(tag + ': no old sheets on screen', not bad, bad[:6])
    return r
async def boot_page(p):
    b = await p.chromium.launch(headless=True, args=['--disable-dev-shm-usage'])
    ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True,
      user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
    pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(3500)
    return b, ctx, pg, errs
async def main():
    h = serve()
    async with async_playwright() as p:
        # ---- Ch1 ----
        b, ctx, pg, errs = await boot_page(p)
        await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(2500); await skipall(pg, 12)
        ryo = await ev(pg, "W.ryo && {x:Math.round(W.ryo.x),y:Math.round(W.ryo.y)}")
        ok('Ch1 boots, Ryo is on the map', isinstance(ryo, dict) and 'x' in ryo, ryo)
        await ev(pg, "(function(){if(W.ryo){W.ryo.x=640;W.ryo.y=900;WORLD_API.camera(true)}})()")
        await pg.wait_for_timeout(1500)
        ok('Ch1 no page errors after boot+walk', not errs, errs[:3])
        await b.close()
        # ---- Ch2 ----
        b, ctx, pg, errs = await boot_page(p)
        await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(2500); await skipall(pg, 12)
        await pg.evaluate("WORLD_API.c2Begin(true)"); await pg.wait_for_timeout(3000); await skipall(pg, 12); await pg.wait_for_timeout(1200)
        st = await ev(pg, "(function(){var S=c2S();S.e.genji=1;S.e.roam=1;S.e.arrive=1;S.e.gymIn=1;return {ch:typeof chN==='function'?chN():null,room:typeof c2Room==='function'?c2Room():null}})()")
        ok('Ch2 boots into town', isinstance(st, dict) and st.get('ch') == 2, st)
        # remaps: logical keys point at Y files, no missing world/ URLs
        maps = await ev(pg, r"""(function(){var o={}, miss=[]; ['c2_punk_walk','c2_punk_fig','c2_hustler_walk','c2_hustler_fig','c2_hustler_idle','mb2_sento_walk','mb2_sento_fig','mb2_sento_idle','n13hus_walk','n13hus_idle','c2_doorman_walk','c2_gray_idle','c2_boss_idle','c2_punkY1_idle','c2x_act_punkY1','c2x_act_hustlerY'].forEach(function(k){var v=IMG[k]||'';o[k]=String(v).slice(0,80);if(/^world\//.test(v)&&!v)miss.push(k)}); return {o:o,miss:miss,ykoff:!!(root.FFF_YK&&root.FFF_YK.off),base:!!(root.FFF_YK&&root.FFF_YK.base)}})()""")
        ok('no ?ykoff / FFF_YK.base', isinstance(maps, dict) and not maps.get('ykoff') and not maps.get('base'), maps)
        if isinstance(maps, dict):
            badk = []
            for k, v in (maps.get('o') or {}).items():
                if not v: badk.append((k, 'missing'))
                if re.search(r'(c2_punk_(walk|fig)|c2_hustler_(walk|fig)|mb2_sento_(walk|fig)|goda_)(?!Y)', v) and 'Y' not in v and 'hustlerY' not in v and 'sentoY' not in v and 'punkY' not in v:
                    # file URLs should be the Y files
                    if v.startswith('world/') and 'Y' not in v: badk.append((k, v))
            ok('logical keys remap to Y file URLs', not badk, (badk, maps.get('o')))
        for name, (x, y) in {'crosswalk X1': (1900, 1950), 'Wagashi gate X3': (2560, 3340), 'Yu door': (330, 1050), 'arcade apron': (2180, 3460)}.items():
            await ev(pg, "(a)=>{var A=WORLD_API,W=A.W;W.ryo.x=a[0];W.ryo.y=a[1];W.aoi.x=a[0];W.aoi.y=a[1]+60;A.camera(true)}",)
            await pg.evaluate("(a)=>{var A=WORLD_API,W=A.W;W.ryo.x=a[0];W.ryo.y=a[1];W.aoi.x=a[0];W.aoi.y=a[1]+60;A.camera(true)}", [x, y])
            await pg.wait_for_timeout(2800)
            await scan_old(pg, 'spot ' + name)
        # force the crosswalk clash and a hustler street event
        await ev(pg, "g38tStart('X1','test')")
        await pg.wait_for_timeout(4000)
        await scan_old(pg, 'crosswalk clash X1')
        await ev(pg, "FFF_C2EV && FFF_C2EV.clear && FFF_C2EV.clear()")
        await pg.evaluate("(a)=>{var A=WORLD_API,W=A.W;W.ryo.x=a[0];W.ryo.y=a[1];W.aoi.x=a[0];W.aoi.y=a[1]+60;A.camera(true)}", [380, 2100])
        await ev(pg, "FFF_C2EV.force('H1W2')")
        await pg.wait_for_timeout(4000)
        await scan_old(pg, 'hustler smoke event H1W2')
        ok('Ch2 no page errors', not errs, errs[:3])
        await b.close()
    h.shutdown()
    failed = [n for c, n, e in RES if not c]
    print(('FAIL: ' + ', '.join(failed)) if failed else 'PASS: Ch1/Ch2 smoke')
    sys.exit(1 if failed else 0)
asyncio.run(main())
