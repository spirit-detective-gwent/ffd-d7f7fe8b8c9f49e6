#!/workspace/pwenv/bin/python3
"""Render v2 preview stills, town-door composite, side-by-sides, and phase1_sheet_v2.png."""
import asyncio, http.server, socketserver, threading, functools, base64, io, shutil
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = Path('/workspace/v6560-review/seal2/phase1')
V2 = OUT / 'v2'
PORT = 8872
OUT.mkdir(parents=True, exist_ok=True)
V2.mkdir(parents=True, exist_ok=True)

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def font(sz=18):
    try:
        return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', sz)
    except Exception:
        return ImageFont.load_default()

def compose_exterior(door_im):
    town = Image.open('/workspace/v6560-review/c2_town_full.png').convert('RGBA')
    # street north of Wagashi + the north facade + a little roof
    box = (2620, 2480, 3540, 3020)
    before = town.crop(box)
    after = before.copy()
    # facade 400x160; top-left in world (3080-200, 2760-160) = (2880, 2600)
    lx, ly = 2880 - box[0], 2600 - box[1]
    door = door_im.convert('RGBA')
    if door.size != (400, 160):
        door = door.resize((400, 160), Image.Resampling.LANCZOS)
    after.paste(door, (lx, ly), door)
    before.convert('RGB').save(V2 / 'exterior_before.png')
    after.convert('RGB').save(V2 / 'exterior_after.png')
    # side by side
    w, h = after.size
    pair = Image.new('RGB', (w * 2 + 36, h + 40), (26, 18, 32))
    pair.paste(before.convert('RGB'), (12, 32))
    pair.paste(after.convert('RGB'), (w + 24, 32))
    d = ImageDraw.Draw(pair)
    f = font(16)
    d.text((12, 8), 'Existing Wagashi north facade (cream placeholder door)', fill=(244, 234, 210), font=f)
    d.text((w + 24, 8), 'Same block, door overlay added (preview only, not wired)', fill=(244, 234, 210), font=f)
    pair.save(V2 / 'exterior_before_after.png')
    after.convert('RGB').save(OUT / 'exterior_v2.png')
    pair.save(OUT / 'exterior_v2_compare.png')
    print('exterior composite', after.size, 'door at', lx, ly)
    return after

async def main():
    s = TS(('127.0.0.1', PORT), functools.partial(Q, directory=str(HERE)))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = await b.new_context(viewport={'width': 1600, 'height': 2800}, device_scale_factor=1)
        pg = await ctx.new_page()
        pg.on('pageerror', lambda e: print('PAGEERR', e))
        await pg.goto(f'http://127.0.0.1:{PORT}/preview.html')
        await pg.wait_for_function("() => document.getElementById('battle') && document.getElementById('chiyoFacings')", timeout=20000)
        await pg.wait_for_timeout(200)
        ids = await pg.evaluate("()=>[...document.querySelectorAll('canvas')].map(c=>c.id)")
        print('canvases', ids)
        saved = {}
        for cid in ids:
            data = await pg.evaluate("""(id)=>{
              var c=document.getElementById(id); return c ? c.toDataURL('image/png') : null;
            }""", cid)
            if not data: continue
            im = Image.open(io.BytesIO(base64.b64decode(data.split(',',1)[1]))).convert('RGB')
            im.save(V2 / f'{cid}.png')
            # also v2-named copies in phase1 for the requested stills
            if cid in ('interior', 'battle', 'chiyoIdle', 'chiyoWalk', 'chiyoFacings', 'chiyoTalk',
                       'sweetRoll', 'dango', 'rollSplit', 'facadeDoor', 'menu'):
                im.save(OUT / f'{cid}_v2.png')
            saved[cid] = im
            print('saved', cid, im.size)
        await b.close()
    s.server_close()

    door = saved.get('facadeDoor')
    if door:
        compose_exterior(door)

    # copy sprite lineup already made
    # side-by-sides vs existing game art
    def load(p):
        p = Path(p)
        return Image.open(p).convert('RGB') if p.exists() else None

    def row_of(ims, labels, h=400, bg=(26,18,32), title=''):
        ims2, labs2 = [], []
        for im, lab in zip(ims, labels):
            if im is None: continue
            r = min(1, (h-40)/im.height, 640/im.width)
            ims2.append(im.resize((int(im.width*r), int(im.height*r)), Image.Resampling.LANCZOS))
            labs2.append(lab)
        if not ims2: return None
        W = 24 + sum(im.width + 24 for im in ims2)
        out = Image.new('RGB', (max(W, 800), h + (36 if title else 8)), bg)
        d = ImageDraw.Draw(out)
        f = font(16)
        y0 = 28 if title else 4
        if title:
            d.text((16, 6), title, fill=(244,234,210), font=f)
        x = 16
        for im, lab in zip(ims2, labs2):
            out.paste(im, (x, y0 + (h-40-im.height)//2))
            d.text((x, y0 + h-36), lab, fill=(244,234,210), font=f)
            x += im.width + 24
        return out

    comps = []
    street = load('/workspace/v6560-review/bg_battle_street.png')
    battle = saved.get('battle')
    if street and battle:
        comps.append(row_of([street, battle], ['C2BT: Ch2 street (shipped)', 'v2: X3 Wagashi row (preview)'], h=520,
                            title='Battle backdrops — same helpers and detail level'))
    udon = load('/workspace/v6560-review/q_udon_interior.png')
    interior = saved.get('interior')
    if interior:
        comps.append(row_of([udon, interior] if udon else [interior],
                            (['Kitsune Udon (shipped)', 'Chiyo Wagashi interior v2'] if udon else ['Chiyo Wagashi interior v2']),
                            h=420, title='Cel interiors — density and props'))
    staff = load('/workspace/v6560-review/gangs/club_staff_sprites.png')
    lineup = load(V2/'chiyo_lineup.png')
    if staff and lineup:
        comps.append(row_of([staff, lineup], ['Club staff (hostess / dealer / cashier)', 'Chiyo v2 on the same yk / Hina rig'],
                            h=360, title='Sprite proportions vs club staff'))
    extp = load(V2/'exterior_before_after.png')
    if extp:
        comps.append(row_of([extp], ['Town Wagashi facade, door added'], h=extp.height+50,
                            title='Exterior — door on the existing block, not a new building'))

    for i, c in enumerate(comps):
        if c:
            c.save(V2 / f'compare_{i}.png')
            print('compare', i, c.size)

    # contact sheet v2
    W, pad = 1400, 24
    chunks = []
    def captioned(im, cap, maxw=1350):
        if im is None: return None
        r = min(1, maxw / im.width)
        im = im.resize((int(im.width*r), int(im.height*r)), Image.Resampling.LANCZOS)
        c = Image.new('RGB', (W, im.height + 36), (26, 18, 32))
        c.paste(im, ((W-im.width)//2, 30))
        ImageDraw.Draw(c).text((24, 8), cap, fill=(244,234,210), font=font(18))
        return c

    port = load(OUT/'chiyo_neutral.png')
    idle = saved.get('chiyoIdle'); walk = saved.get('chiyoWalk'); fac = saved.get('chiyoFacings'); talk = saved.get('chiyoTalk')
    if port and fac:
        row = Image.new('RGB', (W, 560), (26,18,32))
        p = port.resize((300, 400), Image.Resampling.LANCZOS)
        row.paste(p, (24, 40))
        f2 = fac.resize((min(1040, fac.width), int(fac.height*min(1040,fac.width)/fac.width)), Image.Resampling.LANCZOS)
        row.paste(f2, (340, 40))
        ImageDraw.Draw(row).text((24, 8), 'Ms. Chiyo — portrait + yk cel sheet (4 facings, Hina / club-staff proportions)', fill=(244,234,210), font=font(18))
        chunks.append(row)
    if walk and idle:
        chunks.append(captioned(row_of([idle, walk, talk], ['Idle (breathing sheet)', 'Walk front x4', 'Talk / map'], h=260),
                                'Walk, idle breathing, talk/overworld'))
    for im, cap in [
        (saved.get('interior'), 'Interior v2 — lanterns clear of noren; display case, steamer, register, tea, wall menu'),
        (saved.get('battle'), 'X3 battle backdrop v2 — Wagashi row at night (C2BT helpers: noren, lanterns, shutters, vending, wet asphalt)'),
        (load(V2/'exterior_before_after.png'), 'Existing Wagashi north facade, with the new door overlaid (preview only)'),
        (row_of([saved.get('sweetRoll'), saved.get('dango'), saved.get('rollSplit')],
                ['Sweet roll', 'Dango', 'Pull-apart'], h=200), 'Sweets used in the eat game'),
        (saved.get('menu'), 'Proposed counter prices (still open)'),
    ]:
        c = captioned(im, cap)
        if c: chunks.append(c)
    for i, c in enumerate(comps):
        cap = ['Battle BG vs shipped C2BT street', 'Interior vs Kitsune Udon', 'Sprite vs club staff', 'Exterior on the town block'][i] if i < 4 else f'Compare {i}'
        cc = captioned(c, cap, maxw=1350)
        if cc: chunks.append(cc)
    # path cards reused from v1 if present
    cards = []
    for pid in ('fierce','strategic','balanced'):
        for kind in ('brief','win'):
            im = load(OUT/f'card_{pid}_{kind}.png')
            if im: cards.append(im)
    if cards:
        cw, ch = cards[0].size
        grid = Image.new('RGB', (W, ch*3 + 50), (26,18,32))
        d = ImageDraw.Draw(grid)
        d.text((24, 8), 'Path-line cards (unchanged from v1) — Flip briefing and the win, all three paths', fill=(244,234,210), font=font(18))
        for i, im in enumerate(cards):
            r, col = divmod(i, 2)
            grid.paste(im, (20 + col * (cw + 16), 40 + r * ch))
        chunks.append(grid)

    H = pad + sum(c.height + pad for c in chunks)
    sheet = Image.new('RGB', (W, H), (16, 12, 22))
    y = pad
    for c in chunks:
        sheet.paste(c, (0, y)); y += c.height + pad
    sheet.save(OUT / 'phase1_sheet_v2.png')
    print('sheet', sheet.size, OUT/'phase1_sheet_v2.png')

if __name__ == '__main__':
    asyncio.run(main())
