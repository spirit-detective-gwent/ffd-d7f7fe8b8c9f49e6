#!/usr/bin/env python3
"""Render Phase 5 preview canvases to /workspace/v6560-review/seal2/phase5/v2/"""
import asyncio, base64, functools, io, os, threading
from http.server import ThreadingHTTPServer as TS, SimpleHTTPRequestHandler as Q
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = Path('/workspace/v6560-review/seal2/phase5')
V1 = OUT / 'v2'
PORT = int(os.environ.get('PORT', '8906'))

def font(size):
    for p in ('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
              '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

ROOM_IDS = [
    'depYard','depClock','depBay','depCrates','depCold','depCage','depBikes',
    'depLoft','depBreak','depTunnel','depManifest','depAntero','depShutter'
]
LABELS = {
    'depYard': 'Yard gate', 'depClock': 'Time clock', 'depBay': 'Loading bay',
    'depCrates': 'Crate stacks', 'depCold': 'Cold store', 'depCage': 'Parts cage',
    'depBikes': 'Bike bay', 'depLoft': 'Dispatch loft', 'depBreak': 'Break room',
    'depTunnel': 'Tunnel spur', 'depManifest': 'Manifest office',
    'depAntero': 'Lift anteroom', 'depShutter': 'Lift shutter',
    'depShutterLeave': 'Leave him', 'depShutterNotes': 'The notes',
    'depShutterHelp': 'Help him up', 'battleShutter': 'Battle · shutter',
    'sheet_masa': 'Masa sheet', 'manifestItem': 'Manifest item',
}

def room_sheet():
    V1.mkdir(parents=True, exist_ok=True)
    W, H = 320, 250
    cells = []
    for cid in ROOM_IDS:
        p = V1 / f'{cid}.png'
        if not p.exists():
            continue
        im = Image.open(p).convert('RGB')
        im.thumbnail((W - 8, H - 36), Image.Resampling.LANCZOS)
        cell = Image.new('RGB', (W, H), (22, 18, 26))
        d = ImageDraw.Draw(cell)
        d.text((8, 6), LABELS.get(cid, cid), fill=(232, 216, 176), font=font(14))
        cell.paste(im, (8, 28))
        cells.append(cell)
    if not cells:
        return
    cols = 4
    rows = (len(cells) + cols - 1) // cols
    sh = Image.new('RGB', (cols * W + 24, rows * H + 48), (16, 12, 20))
    d = ImageDraw.Draw(sh)
    d.text((12, 10), "Seal 2 Phase 5  ·  Masa's Seal  ·  13 depot rooms  ·  v2", fill=(244, 234, 210), font=font(18))
    for i, c in enumerate(cells):
        r, col = divmod(i, cols)
        sh.paste(c, (12 + col * W, 36 + r * H))
    sh.save(V1 / 'phase5_rooms_v2.png')
    sh.save(OUT / 'phase5_rooms_v2.png')
    print('room sheet', sh.size, 'cells', len(cells))

async def main():
    V1.mkdir(parents=True, exist_ok=True)
    s = TS(('127.0.0.1', PORT), functools.partial(Q, directory=str(HERE)))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = await b.new_context(viewport={'width': 2000, 'height': 8000}, device_scale_factor=1)
        pg = await ctx.new_page()
        pg.on('pageerror', lambda e: print('PAGEERR', e))
        await pg.goto(f'http://127.0.0.1:{PORT}/preview_p5.html')
        await pg.wait_for_function("() => document.title.indexOf('ready') >= 0", timeout=40000)
        await pg.wait_for_timeout(400)
        ids = await pg.evaluate("()=>[...document.querySelectorAll('canvas')].map(c=>c.id)")
        print('canvases', ids)
        for cid in ids:
            data = await pg.evaluate("""(id)=>{
              var c=document.getElementById(id); return c ? c.toDataURL('image/png') : null;
            }""", cid)
            if not data:
                continue
            im = Image.open(io.BytesIO(base64.b64decode(data.split(',', 1)[1]))).convert('RGB')
            im.save(V1 / f'{cid}.png')
            print(cid, im.size)
        await b.close()
    room_sheet()
    print('done', V1)

if __name__ == '__main__':
    asyncio.run(main())
