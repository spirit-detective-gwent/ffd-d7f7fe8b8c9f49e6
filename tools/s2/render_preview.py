#!/workspace/pwenv/bin/python3
"""Render tools/s2/preview.html canvases into /workspace/v6560-review/seal2/phase1/."""
import asyncio, http.server, socketserver, threading, functools
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = Path('/workspace/v6560-review/seal2/phase1')
PORT = 8871
OUT.mkdir(parents=True, exist_ok=True)

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

async def main():
    s = TS(('127.0.0.1', PORT), functools.partial(Q, directory=str(HERE)))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = await b.new_context(viewport={'width': 1600, 'height': 2400}, device_scale_factor=1)
        pg = await ctx.new_page()
        await pg.goto(f'http://127.0.0.1:{PORT}/preview.html')
        await pg.wait_for_timeout(800)
        ids = await pg.evaluate("()=>[...document.querySelectorAll('canvas')].map(c=>c.id)")
        print('canvases', ids)
        for cid in ids:
            data = await pg.evaluate("""(id)=>{
              var c=document.getElementById(id); return c.toDataURL('image/png');
            }""", cid)
            raw = data.split(',',1)[1]
            import base64, io
            im = Image.open(io.BytesIO(base64.b64decode(raw))).convert('RGB')
            im.save(OUT / f'{cid}.png')
            print('saved', cid, im.size)
        await b.close()
    s.server_close()

    # contact sheet
    parts = [
        ('exterior.png', 'Exterior + door'),
        ('interior.png', 'Interior (cel)'),
        ('chiyo_portrait', 'Portrait + sprite'),
        ('battle.png', 'X3 battle backdrop'),
        ('sweets', 'Sweet roll, dango, pull-apart'),
        ('eatboard.png', 'Eat-game beats'),
        ('menu.png', 'Counter menu (proposed)'),
        ('cards', 'Path-line cards'),
    ]
    # assemble a tall sheet
    W, pad = 1400, 24
    chunks = []
    def load(name):
        pth = OUT / name
        return Image.open(pth).convert('RGB') if pth.exists() else None
    def captioned(im, cap, maxw=1350):
        if im is None: return None
        r = min(1, maxw / im.width)
        im = im.resize((int(im.width*r), int(im.height*r)), Image.Resampling.LANCZOS)
        h = im.height + 36
        c = Image.new('RGB', (W, h), (26, 18, 32))
        c.paste(im, ((W-im.width)//2, 30))
        d = ImageDraw.Draw(c)
        try:
            f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
        except Exception:
            f = ImageFont.load_default()
        d.text((24, 8), cap, fill=(244, 234, 210), font=f)
        return c
    # portrait + sprite row
    port = Image.open(OUT/'chiyo_neutral.png').convert('RGB') if (OUT/'chiyo_neutral.png').exists() else None
    idle = load('chiyoIdle.png'); walk = load('chiyoWalk.png')
    if port and idle:
        row = Image.new('RGB', (W, 520), (26, 18, 32))
        p = port.resize((360, 480), Image.Resampling.LANCZOS)
        row.paste(p, (40, 28))
        i2 = idle.resize((200, 250), Image.Resampling.LANCZOS)
        row.paste(i2, (430, 140))
        if walk:
            wim = walk.resize((700, 250), Image.Resampling.LANCZOS)
            row.paste(wim, (650, 140))
        d = ImageDraw.Draw(row)
        try:
            f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
        except Exception:
            f = ImageFont.load_default()
        d.text((40, 6), 'Ms. Chiyo — portrait (360x480 webp q78) + matching cel sprite', fill=(244,234,210), font=f)
        chunks.append(row)
    # sweets row
    rolls = [load('sweetRoll.png'), load('dango.png'), load('rollSplit.png')]
    if all(rolls):
        row = Image.new('RGB', (W, 260), (26, 18, 32))
        x = 80
        for im in rolls:
            row.paste(im, (x, 50))
            x += im.width + 60
        d = ImageDraw.Draw(row)
        try:
            f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
        except Exception:
            f = ImageFont.load_default()
        d.text((24, 8), 'Sweet roll, cheaper dango, tap-to-pull-apart beat', fill=(244,234,210), font=f)
        chunks.append(row)
    # main stills
    for name, cap in [('exterior.png','Shop exterior with new door under the noren'),
                      ('interior.png','Shop interior — counter, noren, trays'),
                      ('battle.png','X3 Wagashi clash battle backdrop (720x1280)'),
                      ('eatboard.png','Eat-game storyboard (onigiri poses, roll swapped in)'),
                      ('menu.png','Proposed counter prices (still open)')]:
        c = captioned(load(name), cap)
        if c: chunks.append(c)
    # path cards in a grid
    cards = []
    for pid in ('fierce','strategic','balanced'):
        for kind in ('brief','win'):
            im = load(f'card_{pid}_{kind}.png')
            if im: cards.append(im)
    if cards:
        cw, ch = cards[0].size
        grid = Image.new('RGB', (W, ch*3 + 50), (26, 18, 32))
        d = ImageDraw.Draw(grid)
        try:
            f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
        except Exception:
            f = ImageFont.load_default()
        d.text((24, 8), 'Path-line cards — Flip briefing and the win, all three paths', fill=(244,234,210), font=f)
        for i, im in enumerate(cards):
            r, col = divmod(i, 2)
            x = 20 + col * (cw + 16)
            y = 40 + r * ch
            grid.paste(im, (x, y))
        chunks.append(grid)
    H = pad + sum(c.height + pad for c in chunks)
    sheet = Image.new('RGB', (W, H), (16, 12, 22))
    y = pad
    for c in chunks:
        sheet.paste(c, (0, y)); y += c.height + pad
    sheet.save(OUT / 'phase1_sheet.png')
    print('sheet', sheet.size, OUT/'phase1_sheet.png')

if __name__ == '__main__':
    asyncio.run(main())
