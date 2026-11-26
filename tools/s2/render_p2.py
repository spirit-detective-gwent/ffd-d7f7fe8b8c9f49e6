#!/workspace/pwenv/bin/python3
"""Render Phase 2 preview stills, town composites, and a review sheet."""
import asyncio, http.server, socketserver, threading, functools, base64, io
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = Path('/workspace/v6560-review/seal2/phase2')
V1 = OUT / 'v1'
PORT = 8873
OUT.mkdir(parents=True, exist_ok=True)
V1.mkdir(parents=True, exist_ok=True)

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def font(sz=18):
    for p in (
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
        '/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    ):
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            continue
    return ImageFont.load_default()

def compose_facades():
    town = Image.open('/workspace/v6560-review/c2_town_full.png').convert('RGBA')
    # south face + boardwalk
    box_s = (3700, 3180, 4960, 3680)
    before_s = town.crop(box_s)
    after_s = before_s.copy()
    south = Image.open(V1 / 'minaSouth.png').convert('RGBA')
    if south.size != (1140, 220):
        south = south.resize((1140, 220), Image.Resampling.LANCZOS)
    # overlay at world (3760, 3300) covering windows/shutters in the street band
    # try y=3280 so it sits on the window row (~3320)
    lx, ly = 3760 - box_s[0], 3280 - box_s[1]
    after_s.paste(south, (lx, ly), south)
    pair_s = Image.new('RGB', (before_s.width * 2 + 36, before_s.height + 40), (22, 16, 28))
    pair_s.paste(before_s.convert('RGB'), (12, 32))
    pair_s.paste(after_s.convert('RGB'), (before_s.width + 24, 32))
    d = ImageDraw.Draw(pair_s)
    f = font(16)
    d.text((12, 8), 'Existing eastS south face (windows + shutters)', fill=(244, 234, 210), font=f)
    d.text((before_s.width + 24, 8), 'Minato-sō south overlay (workshop bay, sign, mixed windows)', fill=(244, 234, 210), font=f)
    before_s.convert('RGB').save(V1 / 'south_before.png')
    after_s.convert('RGB').save(V1 / 'south_after.png')
    pair_s.save(V1 / 'south_before_after.png')
    pair_s.save(OUT / 'south_v1_compare.png')

    # north street edge
    box_n = (3700, 2480, 4960, 3000)
    before_n = town.crop(box_n)
    after_n = before_n.copy()
    north = Image.open(V1 / 'minaNorth.png').convert('RGBA')
    if north.size != (1140, 168):
        north = north.resize((1140, 168), Image.Resampling.LANCZOS)
    # overlay at (3760, 2760-168) = (3760, 2592), like Wagashi
    lx, ly = 3760 - box_n[0], 2592 - box_n[1]
    after_n.paste(north, (lx, ly), north)
    pair_n = Image.new('RGB', (before_n.width * 2 + 36, before_n.height + 40), (22, 16, 28))
    pair_n.paste(before_n.convert('RGB'), (12, 32))
    pair_n.paste(after_n.convert('RGB'), (before_n.width + 24, 32))
    d = ImageDraw.Draw(pair_n)
    d.text((12, 8), 'Existing eastS north edge (roof / street)', fill=(244, 234, 210), font=f)
    d.text((before_n.width + 24, 8), 'Minato-sō north overlay (lobby door, lit/dark windows)', fill=(244, 234, 210), font=f)
    before_n.convert('RGB').save(V1 / 'north_before.png')
    after_n.convert('RGB').save(V1 / 'north_after.png')
    pair_n.save(V1 / 'north_before_after.png')
    pair_n.save(OUT / 'north_v1_compare.png')
    print('composites', 'south@', 3760, 3280, 'north@', 3760, 2592)

def sheet():
    # contact sheet of key stills
    keys = [
        ('minaNorth.png', 'North façade'),
        ('minaSouth.png', 'South façade'),
        ('minaLobby.png', 'Lobby'),
        ('minaShop.png', 'Workshop'),
        ('battleBridge.png', 'Bridge battle'),
        ('battleSE.png', 'SE street battle'),
        ('battleWaga.png', 'Wagashi battle (ref)'),
        ('sheet_hase.png', 'Hase sheet'),
        ('sheet_mori.png', 'Mori sheet'),
        ('sheet_nao.png', 'Nao sheet'),
        ('sheet_haru.png', 'Haru sheet'),
        ('north_before_after.png', 'North before/after'),
        ('south_before_after.png', 'South before/after'),
        ('line_mori_held.png', 'Mori held'),
        ('line_mori_taken.png', 'Mori taken'),
        ('line_nao_held.png', 'Nao held'),
        ('line_nao_taken.png', 'Nao taken'),
        ('line_haru_held.png', 'Haru held'),
        ('line_haru_taken.png', 'Haru taken'),
    ]
    cells = []
    for fn, lab in keys:
        p = V1 / fn
        if not p.exists():
            continue
        im = Image.open(p).convert('RGB')
        # fit into 480x300 box
        tw, th = 480, 300
        im.thumbnail((tw, th - 24), Image.Resampling.LANCZOS)
        cell = Image.new('RGB', (tw, th), (22, 16, 28))
        cell.paste(im, ((tw - im.width) // 2, 24 + (th - 24 - im.height) // 2))
        d = ImageDraw.Draw(cell)
        d.text((8, 6), lab, fill=(244, 234, 210), font=font(14))
        cells.append(cell)
    if not cells:
        return
    cols = 3
    rows = (len(cells) + cols - 1) // cols
    W, H = 480, 300
    sheet = Image.new('RGB', (cols * W + 24, rows * H + 48), (16, 12, 20))
    d = ImageDraw.Draw(sheet)
    d.text((12, 10), 'Seal 2 Phase 2  ·  Night Runs  ·  v1 preview sheet', fill=(244, 234, 210), font=font(18))
    for i, c in enumerate(cells):
        r, col = divmod(i, cols)
        sheet.paste(c, (12 + col * W, 36 + r * H))
    sheet.save(V1 / 'phase2_sheet_v1.png')
    sheet.save(OUT / 'phase2_sheet_v1.png')
    print('sheet', sheet.size, 'cells', len(cells))

async def main():
    s = TS(('127.0.0.1', PORT), functools.partial(Q, directory=str(HERE)))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = await b.new_context(viewport={'width': 1800, 'height': 3200}, device_scale_factor=1)
        pg = await ctx.new_page()
        pg.on('pageerror', lambda e: print('PAGEERR', e))
        await pg.goto(f'http://127.0.0.1:{PORT}/preview_p2.html')
        await pg.wait_for_function("() => document.title.indexOf('ready') >= 0", timeout=30000)
        await pg.wait_for_timeout(200)
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
            im.save(OUT / f'{cid}_v1.png')
        await b.close()
    compose_facades()
    sheet()
    print('done', V1)

if __name__ == '__main__':
    asyncio.run(main())
