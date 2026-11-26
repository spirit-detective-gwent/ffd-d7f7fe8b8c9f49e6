#!/usr/bin/env python3
"""Build nq_depclk sheets: dock-hand body, tenugui removed, short hair crown."""
from pathlib import Path
from PIL import Image, ImageDraw

SRC = Path('/workspace/ffd/world')
OUT_DIR = Path('/tmp/depclk')
OUT_DIR.mkdir(parents=True, exist_ok=True)

CW, CH = 208, 272
INK = (20, 19, 24, 255)
HAIR_DK = (16, 16, 20, 255)
HAIR_MD = (28, 26, 32, 255)
HAIR_HI = (38, 37, 44, 255)

def is_skin(p):
    r, g, b, a = p
    return a > 200 and r > 200 and g > 140 and b > 100 and r > g

def is_orange(p):
    r, g, b, a = p
    return a > 200 and r > 180 and 50 < g < 160 and b < 90 and r > g + 50

def is_dark(p, lim=42):
    r, g, b, a = p
    return a > 80 and max(r, g, b) < lim

def is_stripe(p):
    r, g, b, a = p
    if a < 200:
        return False
    if abs(r - g) > 16 or abs(g - b) > 16:
        return False
    return 85 <= r <= 125

def head_top(cell):
    px = cell.load()
    w, h = cell.size
    for y in range(h):
        if any(px[x, y][3] > 20 for x in range(w)):
            return y
    return 0

def head_cx(cell, top, band=20):
    px = cell.load()
    w, h = cell.size
    xs = []
    for y in range(top, min(top + band, h)):
        for x in range(w):
            if px[x, y][3] > 20:
                xs.append(x)
    return (sum(xs) // len(xs)) if xs else w // 2

def find_stripe_y(cell, top):
    px = cell.load()
    w, h = cell.size
    best_y, best_n = None, 0
    for y in range(top + 8, min(top + 40, h)):
        n = sum(1 for x in range(w) if is_stripe(px[x, y]))
        if n > best_n:
            best_n, best_y = n, y
    if best_n >= 12:
        return best_y
    return None

def cap_x_range(cell, top, stripe_y):
    px = cell.load()
    w = cell.size[0]
    xs = []
    y1 = stripe_y if stripe_y is not None else top + 22
    for y in range(top, y1 + 1):
        for x in range(w):
            p = px[x, y]
            if is_dark(p) or is_stripe(p):
                xs.append(x)
    if not xs:
        return 0, w - 1
    # drop the extreme 6% on each side (flap / knot outliers) for the MAIN cap
    xs.sort()
    lo = xs[int(len(xs) * 0.06)]
    hi = xs[int(len(xs) * 0.94)]
    return lo, hi

def erase_tenugui(cell, facing):
    """Remove the cap, reflective stripe, and trailing flap. Keep under-cap hair, face, ears."""
    out = cell.copy()
    px = out.load()
    src = cell.load()
    w, h = cell.size
    top = head_top(cell)
    stripe = find_stripe_y(cell, top)
    y_cut = (stripe + 3) if stripe is not None else top + 24
    lo, hi = cap_x_range(cell, top, stripe if stripe is not None else y_cut)
    cx = (lo + hi) // 2
    # include a little margin and the flap on the trailing side
    pad = 28
    x0, x1 = max(0, lo - pad), min(w - 1, hi + pad)

    def is_cap_pixel(p):
        if is_skin(p) or is_orange(p):
            return False
        return is_dark(p, 46) or is_stripe(p)

    # 1) erase cap band (crown through stripe + a couple of rim pixels)
    for y in range(top, min(y_cut + 1, h)):
        for x in range(x0, x1 + 1):
            if is_cap_pixel(src[x, y]):
                px[x, y] = (0, 0, 0, 0)

    # 2) erase trailing flap / knot: dark pixels stuck to the cap's sides, not ears (skin)
    # Left-facing (1): flap is to the RIGHT of the head. Right-facing (2): LEFT.
    # Back (3): flap often on the right. Front (0): small knot either side.
    flap_xs = list(range(hi + 1, min(w, hi + 36))) + list(range(max(0, lo - 36), lo))
    if facing == 1:
        flap_xs = list(range(hi + 1, min(w, hi + 40)))
    elif facing == 2:
        flap_xs = list(range(max(0, lo - 40), lo))
    y_flap1 = min(h - 1, y_cut + 28)
    # flood from remaining dark pixels in the flap zone
    seeds = []
    for y in range(max(0, y_cut - 8), y_flap1 + 1):
        for x in flap_xs:
            if is_cap_pixel(px[x, y]):
                seeds.append((x, y))
    seen = set()
    stack = list(seeds)
    while stack:
        x, y = stack.pop()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h):
            continue
        if y > y_flap1 or y < top - 2:
            continue
        p = px[x, y]
        if not is_cap_pixel(p):
            continue
        seen.add((x, y))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)):
            stack.append((x + dx, y + dy))
    for x, y in seen:
        px[x, y] = (0, 0, 0, 0)

    # 3) wipe AA fringes, leftover stripe, and isolated ghost pixels in the cap/flap zone
    y_clean = min(h - 1, y_cut + 30)
    def near_stripe_or_dark(p):
        if p[3] == 0:
            return False
        if is_skin(p) or is_orange(p):
            return False
        if p[3] < 255 and (is_dark(p, 80) or is_stripe(p)):
            return True
        if is_stripe(p):
            return True
        return False
    for y in range(max(0, top - 4), y_clean + 1):
        for x in range(x0, x1 + 1):
            if near_stripe_or_dark(px[x, y]):
                px[x, y] = (0, 0, 0, 0)
    # isolated dark specks (old outline ghosts) around the head
    doomed = []
    for y in range(max(0, top - 6), min(h, y_cut + 36)):
        for x in range(max(0, lo - 40), min(w, hi + 40)):
            p = px[x, y]
            if p[3] == 0 or is_skin(p) or is_orange(p):
                continue
            if not (is_dark(p, 60) or p[3] < 255):
                continue
            n = 0
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < w and 0 <= yy < h and px[xx, yy][3] > 80:
                    n += 1
            if n <= 2:
                doomed.append((x, y))
    for x, y in doomed:
        px[x, y] = (0, 0, 0, 0)

    return out, cx, top, y_cut, lo, hi, stripe

def _crisp(layer):
    """Snap semi-transparent AA edges to 0 or 255 so the sheet stays cel-crisp."""
    px = layer.load()
    w, h = layer.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 128:
                px[x, y] = (0, 0, 0, 0)
            elif a < 255:
                px[x, y] = (r, g, b, 255)
    return layer

def paint_crown(size, cx, top, y_cut, lo, hi, facing):
    """Short hair cap that fills the removed tenugui and meets the existing hair."""
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # main skull width: the cap without flap
    cap_w = hi - lo
    # slightly tighter than the tenugui (no extra knot width)
    rad_x = max(18, cap_w // 2 - 1)
    # shallow dome: crown just above old top, bottom just below the stripe so it seams into existing hair
    y0 = top - 1
    y1 = y_cut + 4  # overlap existing under-hair, keep the dome shallow
    if facing == 3:
        y1 = y_cut + 6
    # ink outline (2px larger)
    d.ellipse((cx - rad_x - 2, y0 - 2, cx + rad_x + 2, y1 + 2), fill=INK)
    d.ellipse((cx - rad_x, y0, cx + rad_x, y1), fill=HAIR_DK)
    # mid volume, slightly upper
    d.ellipse((cx - rad_x + 4, y0 + 3, cx + rad_x - 4, y0 + (y1 - y0) * 0.7), fill=HAIR_MD)
    # a couple of messy tufts on the crown (asymmetric)
    d.ellipse((cx - 8, y0 - 3, cx + 2, y0 + 8), fill=HAIR_DK)
    d.ellipse((cx + 4, y0 - 1, cx + 14, y0 + 7), fill=HAIR_MD)
    # subtle highlight
    d.ellipse((cx - 5, y0 + 5, cx + 2, y0 + 10), fill=HAIR_HI)
    # a single short crown highlight, not tenugui streaks
    # front: short bangs only in the center, dipping a little past y_cut
    if facing == 0:
        bang_y = y_cut + 10
        for bx, bw, dip in ((-10, 8, 0), (-2, 9, 2), (8, 8, 0)):
            d.ellipse((cx + bx, y_cut, cx + bx + bw, bang_y + dip), fill=HAIR_DK)
    # sides: a little hair along the skull toward the nape, not a flap
    if facing in (1, 2):
        # trailing side is +x when facing left (1)
        s = 1 if facing == 1 else -1
        xa, xb = cx + s * (rad_x - 6), cx + s * (rad_x + 4)
        d.ellipse((min(xa, xb), y_cut - 4, max(xa, xb), y_cut + 10), fill=HAIR_DK)
        # short nape
        d.ellipse((cx - 6, y_cut + 2, cx + 8, y_cut + 16), fill=HAIR_DK)
    if facing == 3:
        # short rounded nape, no hanging tail
        d.ellipse((cx - 10, y_cut + 2, cx + 10, y_cut + 16), fill=HAIR_DK)
    return _crisp(layer)

def punch_protected(hair, original):
    """Never paint over skin, eyes-next-to-skin, or the orange jacket."""
    hp = hair.load()
    op = original.load()
    w, h = original.size
    for y in range(h):
        for x in range(w):
            if hp[x, y][3] < 10:
                continue
            p = op[x, y]
            if is_skin(p) or is_orange(p):
                hp[x, y] = (0, 0, 0, 0)
                continue
            # eyes / iris: dark pixels with a skin neighbor
            if is_dark(p, 55):
                for dx, dy in ((-2, 0), (2, 0), (0, 2), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < w and 0 <= yy < h and is_skin(op[xx, yy]):
                        hp[x, y] = (0, 0, 0, 0)
                        break
    return hair

def fill_crown_gaps(img, cx, top, y_cut, lo, hi):
    """Fill stripe gaps and pale leftover tape in the hair cap."""
    out = img.copy()
    px = out.load()
    w, h = out.size
    y0, y1 = max(0, top - 2), min(h - 1, y_cut + 8)
    x0, x1 = max(0, lo - 6), min(w - 1, hi + 6)
    # recolor pale leftover tape
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            r, g, b, a = px[x, y]
            if a > 200 and min(r, g, b) > 80 and max(r, g, b) < 230 and abs(r - g) < 30:
                px[x, y] = HAIR_DK
    # fill transparent holes with 3+ opaque hair neighbors
    for _ in range(3):
        fills = []
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if px[x, y][3] > 80:
                    continue
                n = 0
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < w and 0 <= yy < h and px[xx, yy][3] > 200 and is_dark(px[xx, yy], 70):
                        n += 1
                if n >= 3:
                    fills.append((x, y))
        for x, y in fills:
            px[x, y] = HAIR_DK
    return out

def process_cell(cell, facing):
    cleared, cx, top, y_cut, lo, hi, stripe = erase_tenugui(cell, facing)
    hair = paint_crown(cell.size, cx, top, y_cut, lo, hi, facing)
    hair = punch_protected(hair, cell)  # use ORIGINAL so we still know where the face was
    out = Image.alpha_composite(cleared, hair)
    return fill_crown_gaps(out, cx, top, y_cut, lo, hi)

def process_sheet(src_path, cell_w, cell_h, out_name):
    im = Image.open(src_path).convert('RGBA')
    w, h = im.size
    cols, rows = w // cell_w, h // cell_h
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for r in range(rows):
        for c in range(cols):
            cell = im.crop((c * cell_w, r * cell_h, (c + 1) * cell_w, (r + 1) * cell_h))
            out.paste(process_cell(cell, r), (c * cell_w, r * cell_h))
    dest = OUT_DIR / out_name
    out.save(dest, 'WEBP', lossless=True, quality=100, method=6)
    print('wrote', dest, dest.stat().st_size, 'cells', cols, 'x', rows)
    return out

def process_single(src_path, out_name, facing=0):
    im = Image.open(src_path).convert('RGBA')
    out = process_cell(im, facing)
    dest = OUT_DIR / out_name
    out.save(dest, 'WEBP', lossless=True, quality=100, method=6)
    print('wrote', dest, dest.stat().st_size, out.size)
    return out

def previews(idle, walk, fig, mp):
    sheet = Image.new('RGBA', (CW * 4, 110), (0, 0, 0, 255))
    for r in range(4):
        sheet.paste(idle.crop((0, r * CH, CW, r * CH + 110)), (r * CW, 0))
    sheet.resize((CW * 4 * 2, 220), Image.NEAREST).save(OUT_DIR / 'preview_idle_heads.png')
    row = Image.new('RGBA', (CW * 8, 110), (0, 0, 0, 255))
    for c in range(8):
        row.paste(walk.crop((c * CW, 0, c * CW + CW, 110)), (c * CW, 0))
    row.resize((CW * 8, 220), Image.NEAREST).save(OUT_DIR / 'preview_walk_front.png')
    col = Image.new('RGBA', (CW * 4, 110), (0, 0, 0, 255))
    for r in range(4):
        col.paste(walk.crop((0, r * CH, CW, r * CH + 110)), (r * CW, 0))
    col.resize((CW * 4 * 2, 220), Image.NEAREST).save(OUT_DIR / 'preview_walk_r0_heads.png')
    # all walk rows, frame 0 and 4
    grid = Image.new('RGBA', (CW * 2 * 2, 110 * 4 * 2), (0, 0, 0, 255))
    for r in range(4):
        for i, c in enumerate((0, 4)):
            hd = walk.crop((c * CW, r * CH, c * CW + CW, r * CH + 110))
            grid.paste(hd.resize((CW * 2, 220), Image.NEAREST), (i * CW * 2, r * 220))
    grid.save(OUT_DIR / 'preview_walk_grid.png')
    fig.resize((fig.width * 3, fig.height * 3), Image.NEAREST).save(OUT_DIR / 'preview_fig.png')
    mp.resize((mp.width * 3, mp.height * 3), Image.NEAREST).save(OUT_DIR / 'preview_map.png')
    print('previews ok')

def main():
    idle = process_sheet(SRC / 'c2_bosoK2_idle.webp', CW, CH, 'nq_depclk_idle.webp')
    walk = process_sheet(SRC / 'c2_bosoK2_walk.webp', CW, CH, 'nq_depclk_walk.webp')
    fig = process_single(SRC / 'c2_bosoK2_fig.webp', 'nq_depclk_fig.webp', facing=0)
    mp = process_single(SRC / 'c2_bosoK2_map.webp', 'nq_depclk_map.webp', facing=0)
    previews(idle, walk, fig, mp)

if __name__ == '__main__':
    main()
