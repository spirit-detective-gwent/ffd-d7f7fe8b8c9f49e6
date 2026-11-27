#!/workspace/pwenv/bin/python3
"""Battle fps/heat: live vs this worktree. usage: battle_perf.py NEW_DIR OLD_DIR [port_new] [port_old]"""
import asyncio, sys, functools, http.server, socketserver, threading, json
from pathlib import Path
from playwright.async_api import async_playwright

NEW = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path('.')
OLD = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path('.')
PN = int(sys.argv[3]) if len(sys.argv) > 3 else 52652
PO = int(sys.argv[4]) if len(sys.argv) > 4 else 52653

class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def serve(root, port):
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

SAMPLER = """()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);}"""
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""

def stats(ft):
    ft = [x for x in ft[2:] if x and x < 1000]
    if not ft:
        return {}
    tot = sum(ft)
    return dict(fps=round(1000*len(ft)/tot, 1), frames=len(ft), worst=round(max(ft), 1), over20=sum(1 for x in ft if x>20))

async def skipall(pg, n=10):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(250); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(220)
    await pg.evaluate("(()=>{var b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Close'&&e.offsetParent);if(b)b.click()})()")

async def metrics(cdp):
    m = await cdp.send('Performance.getMetrics')
    return {x['name']: x['value'] for x in m['metrics']}

async def window(pg, cdp, secs):
    await pg.evaluate(SAMPLER)
    m0 = await metrics(cdp)
    await pg.wait_for_timeout(int(secs*1000))
    m1 = await metrics(cdp)
    await pg.evaluate("window.__run=false")
    ft = await pg.evaluate("window.__ft")
    wall = m1['Timestamp'] - m0['Timestamp']
    r = stats(ft)
    r['heat'] = round(100*(m1['TaskDuration']-m0['TaskDuration'])/wall, 1)
    r['heap_mb'] = round(m1['JSHeapUsedSize']/1e6, 1)
    return r

async def bench(p, url, thr, secs=6):
    b = await p.chromium.launch(headless=True, args=['--disable-dev-shm-usage'])
    ctx = await b.new_context(viewport={'width':390,'height':844}, device_scale_factor=1, is_mobile=True, has_touch=True,
        user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
    pg = await ctx.new_page()
    cdp = await ctx.new_cdp_session(pg)
    await cdp.send('Performance.enable')
    if thr > 1:
        await cdp.send('Emulation.setCPUThrottlingRate', {'rate': thr})
    await pg.goto(url)
    await pg.wait_for_timeout(3500)
    await pg.evaluate("WORLD_API.enter(true)")
    await pg.wait_for_timeout(1800)
    await skipall(pg, 10)
    # a 2-foe wave-2 style battle (the ROUND 2 board)
    await pg.evaluate("""()=>{if(window.FFF_WAVE) FFF_WAVE.stop();
      FFF_UI.startMatch('ryo',{foes:['bully1','bully2'],esc:0.5,drop:0,ctx:{wave:{n:2,of:2,cnt:2}}});
    }""")
    await pg.wait_for_timeout(2500)
    await pg.evaluate("if(window.FFF_WAVE) FFF_WAVE.stop(); FFF_UI.ST.busy=false; FFF_UI.render(false);")
    await pg.wait_for_timeout(400)
    r = await window(pg, cdp, secs)
    # second window to confirm heap is flat
    r2 = await window(pg, cdp, 3)
    r['heap2_mb'] = r2['heap_mb']
    r['fps2'] = r2.get('fps')
    r['inGame'] = await pg.evaluate("!!(FFF_UI.ST && FFF_UI.ST.inGame && FFF_UI.ST.b && !FFF_UI.ST.b.over)")
    await b.close()
    return r

async def main():
    hn, ho = serve(NEW, PN), serve(OLD, PO)
    out = {}
    async with async_playwright() as p:
        for name, port in (('new', PN), ('live', PO)):
            url = f'http://127.0.0.1:{port}/index.html'
            print('bench', name, '1x', flush=True)
            a = await bench(p, url, 1, 6)
            print('bench', name, '4x', flush=True)
            b4 = await bench(p, url, 4, 6)
            out[name] = {'1x': a, '4x': b4}
            print(name, json.dumps({'1x': a, '4x': b4}), flush=True)
    Path('/workspace/dbltap/logs/battle_perf.json').write_text(json.dumps(out, indent=2))
    n, o = out['new'], out['live']
    fps_ok = n['1x']['fps'] >= 55
    heat_d = round(n['4x']['heat'] - o['4x']['heat'], 1)
    heat_ok = heat_d <= 5
    mem_flat = abs(n['1x']['heap2_mb'] - n['1x']['heap_mb']) <= 8
    print('COMPARE', json.dumps({
        'new_fps_1x': n['1x']['fps'], 'live_fps_1x': o['1x']['fps'],
        'new_heat_4x': n['4x']['heat'], 'live_heat_4x': o['4x']['heat'], 'heat_delta': heat_d,
        'new_heap': n['1x']['heap_mb'], 'new_heap2': n['1x']['heap2_mb'],
        'fps_ok': fps_ok, 'heat_ok': heat_ok, 'mem_flat': mem_flat,
        'inGame_new': n['1x'].get('inGame')
    }), flush=True)
    hn.shutdown(); ho.shutdown()
    sys.exit(0 if fps_ok and heat_ok and mem_flat else 1)

if __name__ == '__main__':
    asyncio.run(main())
