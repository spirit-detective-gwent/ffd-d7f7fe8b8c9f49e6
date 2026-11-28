#!/workspace/pwenv/bin/python3
import asyncio, sys, io, functools, http.server, socketserver, threading
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
exec(open('/workspace/healcircle/wt/tools/healcircle/test_healcircle.py').read().split('R = []')[0].split('root = Path')[0])
SKH = open('/workspace/healcircle/wt/tools/healcircle/test_healcircle.py').read()
exec(SKH[SKH.index('SK = '):SKH.index('R = []')])
DPR = 2; T = 1600
def srv(d):
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    s = socketserver.ThreadingTCPServer(('127.0.0.1', 0), functools.partial(Q, directory=d)); s.daemon_threads = True
    threading.Thread(target=s.serve_forever, daemon=True).start(); return s
async def grab(b, d, times):
    s = srv(d); url = f'http://127.0.0.1:{s.server_address[1]}/index.html'
    ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=DPR, is_mobile=True, has_touch=True); pg = await ctx.new_page()
    await pg.goto(url); await pg.wait_for_timeout(3000); await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(1500); await skipall(pg); await pg.evaluate(HUSH)
    await pg.evaluate("(()=>{var c=document.getElementById('wcrawl');if(c)c.remove()})()")
    out = []
    for t in times:
        g = await pg.evaluate("""(f)=>{window.FFF_HS_BEAT_FREEZE=f;var o=document.getElementById('hsbw');if(o)o.remove();WORLD_API.W.busy=false;FFF_HS.beat('dress',function(){});o=document.getElementById('hsbw');
          var r=o.querySelector('.rg').getBoundingClientRect(),tg=o.querySelector('.tg').getBoundingClientRect();return {cx:r.x+r.width/2,cy:r.y+r.height/2,rr:r.width/2,tr:tg.width/2,hs:o.__hs?{ri:o.__hs.ri,ro:o.__hs.ro}:null}}""", t)
        await pg.wait_for_timeout(150)
        png = await pg.screenshot(clip={'x': g['cx'] - 140, 'y': g['cy'] - 110, 'width': 280, 'height': 200})
        out.append((t, g, Image.open(io.BytesIO(png)).convert('RGBA')))
    await ctx.close(); return out
def overlay(im, g, ri, ro, ok):
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    cx, cy = 140 * DPR, 110 * DPR
    # hit area = the ring-line radii that the game scores PERFECT (cyan, hatched annulus)
    for r in (ro, ri): d.ellipse([cx - r * DPR, cy - r * DPR, cx + r * DPR, cy + r * DPR], outline=(0, 240, 255, 255), width=3)
    d.ellipse([cx - ro * DPR, cy - ro * DPR, cx + ro * DPR, cy + ro * DPR], fill=None); d.ellipse([cx - ri * DPR, cy - ri * DPR, cx + ri * DPR, cy + ri * DPR], fill=(0, 0, 0, 0))
    m = Image.new('L', im.size, 0); md = ImageDraw.Draw(m); md.ellipse([cx - ro * DPR, cy - ro * DPR, cx + ro * DPR, cy + ro * DPR], fill=255); md.ellipse([cx - ri * DPR, cy - ri * DPR, cx + ri * DPR, cy + ri * DPR], fill=0)
    fillc = Image.new('RGBA', im.size, (0, 230, 255, 0)); ov2 = Image.composite(fillc, Image.new('RGBA', im.size, (0, 0, 0, 0)), m)
    return Image.alpha_composite(Image.alpha_composite(im, ov2), ov)
async def main():
    times = [T - 110, T, T + 250]
    async with async_playwright() as p:
        b = await p.chromium.launch()
        live = await grab(b, '/workspace/healcircle/live', times); new = await grab(b, '/workspace/healcircle/wt', times); await b.close()
    F = lambda n: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', n)
    W_, H_ = 280 * DPR, 200 * DPR; pad = 16
    canvas = Image.new('RGBA', (pad + 3 * (W_ + pad), 70 + 2 * (H_ + 80) + 130), (18, 22, 30, 255)); d = ImageDraw.Draw(canvas)
    d.text((pad, 14), 'First aid heal ring. Cyan lines = the zone where the white ring scores PERFECT', font=F(26), fill=(255, 255, 255))
    rows = [('BEFORE (live v6.5.64)', live, lambda t, g: (60.0, 60 * (1 + 1.6 * 110 / T)) if t <= T + 110 else (60.0, 60.0),
             {T - 110: 'PERFECT  (ring outside the circle)', T: 'PERFECT', T + 250: 'GOOD  (ring sitting on the circle)'}),
            ('AFTER (fix)', new, lambda t, g: (g['hs']['ri'], g['hs']['ro']),
             {T - 110: 'PERFECT  (ring at the band edge)', T: 'PERFECT', T + 250: 'GOOD  (ring has passed the band)'})]
    y = 60
    for name, shots, hit, lab in rows:
        d.text((pad, y), name, font=F(24), fill=(255, 210, 90)); y += 36
        for i, (t, g, im) in enumerate(shots):
            ri, ro = hit(t, g)
            if name.startswith('BEFORE'): ri, ro = 60.0, 60 * (1 + 1.6 * 110 / T)  # live: perfect while |t-T|<=110 -> ring line radius 60..66.6 (it rests at 60 after T)
            im2 = overlay(im, g, ri, ro, True); x = pad + i * (W_ + pad); canvas.paste(im2, (x, y))
            dt = t - T; d.text((x, y + H_ + 6), f't = T{dt:+d} ms' if dt else 't = T', font=F(20), fill=(220, 230, 240))
            col = (255, 210, 90) if lab[t].startswith('PERFECT') else (255, 140, 120)
            if name.startswith('BEFORE') and t == T + 250: col = (255, 90, 90)
            if name.startswith('BEFORE') and t == T - 110: col = (255, 90, 90)
            d.text((x, y + H_ + 30), lab[t], font=F(17), fill=col)
        y += H_ + 80
    d.text((pad, y), 'Before: hit test used the clock (+/-110 ms) and the ring stopped on the circle, so the two disagreed.', font=F(17), fill=(200, 210, 220))
    d.text((pad, y + 24), 'After: hit test reads the ring size on screen; the gold band IS the cyan hit area. Same 110 ms window.', font=F(17), fill=(200, 210, 220))
    Path('/workspace/healcircle/shots').mkdir(exist_ok=True); canvas.convert('RGB').save('/workspace/healcircle/shots/healcircle_before_after.png'); print('saved')
asyncio.run(main())
