#!/workspace/pwenv/bin/python3
"""v6566-healcircle (Erik t549u): the beat-wrap heal ring and its perfect hit test must agree.
Freezes the ring at sizes just inside / just outside both edges of the drawn gold band, measures the DRAWN geometry
from the DOM (ring line radius = scaled box radius, band = gold border annulus), taps on the ring at 8 angles, and
checks PERFECT iff the drawn ring line is inside the drawn band. Repeats at DPR 1/2/3 and two viewports, plus a
live-timing run. usage: test_healcircle.py <worktree>"""
import asyncio, sys, json, math, functools, http.server, socketserver, threading
from pathlib import Path
from playwright.async_api import async_playwright
root = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test(e.textContent.trim())&&e.offsetParent);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
HUSH = """()=>{try{if(typeof c2AbortTalk==='function')c2AbortTalk()}catch(e){}try{if(typeof scKill==='function')scKill()}catch(e2){}var A=window.WORLD_API,W=A&&A.W;if(W){W.scGen=(W.scGen|0)+1;W.dlg=false;W.cut=false;W.busy=false;}var d=document.getElementById('wdlg');if(d)d.className='';var t=document.getElementById('c2trans');if(t)t.remove();return 1}"""
async def skipall(pg):
    for i in range(6):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(700); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(700)
R = []
def ok(name, cond, detail=''):
    R.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + ('' if cond else '  ' + json.dumps(detail)[:500]), flush=True)
def serve():
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    s = socketserver.ThreadingTCPServer(('127.0.0.1', 0), functools.partial(Q, directory=str(root))); s.daemon_threads = True
    threading.Thread(target=s.serve_forever, daemon=True).start(); return s
OPEN = """(f)=>{window.FFF_HS_BEAT_FREEZE=f;window.__hsr=null;var o=document.getElementById('hsbw');if(o)o.remove();var W=WORLD_API.W;if(W)W.busy=false;
FFF_HS.beat('dress',function(p){window.__hsr=p});o=document.getElementById('hsbw');var g=o.querySelector('.rg').getBoundingClientRect(),
b=o.querySelector('.pz>i'),br=b.getBoundingClientRect(),bw=parseFloat(getComputedStyle(b).borderTopWidth),tg=o.querySelector('.tg').getBoundingClientRect();
return {cx:g.x+g.width/2,cy:g.y+g.height/2,rr:g.width/2,ro:br.width/2,ri:br.width/2-bw,bcx:br.x+br.width/2,bcy:br.y+br.height/2,tcx:tg.x+tg.width/2,tcy:tg.y+tg.height/2,hs:o.__hs?{tol:o.__hs.tol,s:o.__hs.scale()}:null}}"""
async def case(pg, f):
    g = await pg.evaluate(OPEN, f); return g
async def run(b, url, vw, vh, dpr, tag):
    ctx = await b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=dpr, is_mobile=True, has_touch=True); pg = await ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    await pg.goto(url); await pg.wait_for_timeout(3000)
    await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(1500); await skipall(pg); await pg.evaluate(HUSH)
    await pg.evaluate("(()=>{var c=document.getElementById('wcrawl');if(c)c.remove()})()")
    T = 1600
    g0 = await case(pg, 0)
    tol = g0['hs']['tol'] if g0['hs'] else None
    ok(f'[{tag}] shared tol exposed and = 110ms/1.6s window (0.11)', tol is not None and abs(tol - 0.11) < 1e-9, g0)
    if tol is None: await ctx.close(); return
    ok(f'[{tag}] band centred on ring centre', abs(g0['bcx'] - g0['cx']) < 0.6 and abs(g0['bcy'] - g0['cy']) < 0.6 and abs(g0['tcx'] - g0['cx']) < 0.6, g0)
    rr1 = g0['rr'] / g0['hs']['s']  # ring line radius at scale 1, in CSS px as drawn
    ok(f'[{tag}] drawn band edges = R*(1-tol), R*(1+tol)', abs(g0['ro'] - rr1 * (1 + tol)) < 0.3 and abs(g0['ri'] - rr1 * (1 - tol)) < 0.3, [g0, rr1])
    eps = 0.6  # px either side of each drawn edge
    targets = []
    for edge in ('ro', 'ri'):
        for d, want in ((-eps, None), (eps, None)):
            targets.append((edge, d))
    angles = [i * 45 for i in range(8)]
    bad = []; n = 0
    for edge, d in targets:
        rpx = g0[edge] + d
        s = rpx / rr1; f = T * (1 - (s - 1) / 1.6)
        for a in angles:
            g = await case(pg, f)
            inside = g['ri'] <= g['rr'] <= g['ro']
            x = g['cx'] + g['rr'] * math.cos(math.radians(a)); y = g['cy'] + g['rr'] * math.sin(math.radians(a))
            await pg.touchscreen.tap(x, y); await pg.wait_for_timeout(450)
            res = await pg.evaluate("window.__hsr")
            n += 1
            if bool(res) != inside: bad.append(dict(edge=edge, d=d, a=a, rr=g['rr'], ri=g['ri'], ro=g['ro'], got=res))
    ok(f'[{tag}] {n} taps at both edges +/-{eps}px x 8 angles: PERFECT iff ring line inside drawn band', not bad, bad[:4])
    # ring passes through the target (no resting on it): after T+200 it is well inside the band's inner edge and counts Good
    g = await case(pg, T + 200); await pg.touchscreen.tap(g['cx'], g['cy'] - g['rr']); await pg.wait_for_timeout(450)
    ok(f'[{tag}] T+200ms ring is past the band and is Good (not resting on target)', g['rr'] < g['ri'] and (await pg.evaluate("window.__hsr")) is False, g)
    # live timing: real rAF, tap at t~T; result must equal the drawn state at the tap
    await pg.evaluate("window.FFF_HS_BEAT_FREEZE=null")
    mism = []
    for dt in (-300, -60, 0, 60, 300):
        st = await pg.evaluate("""(dt)=>new Promise(r=>{window.__hsr=null;var W=WORLD_API.W;if(W)W.busy=false;FFF_HS.beat('dress',function(p){window.__hsr=p});var o=document.getElementById('hsbw'),t0=performance.now();
          (function w(){if(performance.now()-t0<1600+dt){requestAnimationFrame(w);return}var h=o.__hs,s=h.scale();o.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));r({s:s,tol:h.tol})})()})""", dt)
        await pg.wait_for_timeout(450); res = await pg.evaluate("window.__hsr")
        if bool(res) != (abs(st['s'] - 1) <= st['tol']): mism.append([dt, st, res])
    ok(f'[{tag}] live rAF taps: result matches the ring on screen', not mism, mism)
    ok(f'[{tag}] no page errors', not errs, errs)
    await ctx.close()
async def main():
    s = serve(); url = f'http://127.0.0.1:{s.server_address[1]}/index.html'
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
        for vw, vh, dpr in ((390, 844, 3), (390, 844, 1), (360, 740, 2), (430, 932, 3)):
            await run(b, url, vw, vh, dpr, f'{vw}x{vh}@{dpr}')
        await b.close()
    print(f'{sum(R)}/{len(R)} passed'); sys.exit(0 if all(R) else 1)
asyncio.run(main())
