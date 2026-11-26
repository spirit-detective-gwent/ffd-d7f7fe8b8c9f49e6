#!/usr/bin/env python3
"""Plant and pot-pick frames for Ryu and Aoi.

Official gpick stand/squat frames are used as-is. The official deep-kneel
(frame 2) is cleaned of the held sprig with a tight leaf-bbox mask, then
official-style cel hands are painted at the pot rim: press a seed, pat the soil.
The rise frame is official squat (no cut). Pot-pick keeps the official held
sprig, only recolored toward mugwort — no cuts.
"""
from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
SPR = HERE / "sprites"
OUT_DEBUG = Path("/tmp/garden-src/plant_v2")

INK = (20, 18, 28, 255)
SKIN = {
    "ryo": ((245, 201, 163, 255), (214, 160, 118, 255)),
    "aoi": ((245, 205, 171, 255), (216, 168, 128, 255)),
}
SLEEVE = {
    "ryo": (32, 33, 44, 255),
    "aoi": (44, 52, 75, 255),
}
SLEEVE_LT = {
    "ryo": (48, 48, 62, 255),
    "aoi": (58, 66, 92, 255),
}
# Flat cel fills for the sprig hole — official jackets/skirts are flat color.
HOLE_FILL = {
    "ryo": ((38, 38, 50, 255), (28, 29, 38, 255)),
    "aoi": ((44, 52, 75, 255), (32, 38, 56, 255)),
}
GOLD = (196, 169, 98, 255)
CUFF_AOI = (222, 224, 239, 255)
SEED = (214, 196, 140, 255)
SEED_SH = (180, 150, 100, 255)

gw, cw, ch = 8, 200, 256

# Close-up / sheet pot: room pot is ~22px beside an 86px sprite; on a 256-tall
# cell that is ~2.9x. Placed to the LEFT of the body so official pick sprigs
# and new plant hands meet the rim. Foot stays on the same ground line.
POT_SCALE = 2.9
POT_FOOT = (52, 252)  # in the 200x256 cell (cy = sprite feet)


def slice_sheet(path: Path, row: int = 0, n: int = 6):
    im = Image.open(path).convert("RGBA")
    frames = []
    for i in range(n):
        x = gw + i * (cw + gw)
        y = gw + row * (ch + gw)
        frames.append(im.crop((x, y, x + cw, y + ch)))
    return frames


def slice_gpick(who: str):
    return slice_sheet(SPR / f"{who}_gpick.png", 0)


def is_leaf(r, g, b, a):
    # Official ginger leaf is clearly green (g well above r and b), never navy/collar.
    return a > 80 and g > r + 20 and g > b + 8 and g > 70


def is_root(r, g, b, a):
    # Official root/dirt tan, not skin shadow (skin has higher b and lower g-b).
    if a < 80 or r >= 235:
        return False
    return r > 140 and 90 < g < 200 and 40 < b < 130 and (r - g) < 70 and (g - b) > 30


def is_dirt_ink(r, g, b, a):
    # Warm brown ink on the root only — not hair or uniform outlines (those are cooler).
    return a > 80 and r > g + 8 and r > b + 8 and 30 < r < 90 and g < 55 and b < 45


def is_low_glint(r, g, b, a):
    """Semi-transparent yellow crescent beside Aoi's official sprig."""
    return 0 < a < 160 and r > 180 and g > 150 and (r + g) > b + 60


def is_near_white(r, g, b, a):
    return a > 80 and r > 200 and g > 200 and b > 200


def sprig_mask(fr: Image.Image) -> Image.Image:
    px = fr.load()
    w, h = fr.size
    leaves = [(x, y) for y in range(h) for x in range(w) if is_leaf(*px[x, y])]
    m = Image.new("L", (w, h), 0)
    if not leaves:
        return m
    xs = [p[0] for p in leaves]
    ys = [p[1] for p in leaves]
    # Tight around the leaves; extra pad left for the low-alpha yellow crescent.
    x0, y0 = max(0, min(xs) - 22), max(0, min(ys) - 4)
    x1, y1 = min(w, max(xs) + 16), min(h, max(ys) + 22)
    # never climb into the face / collar
    face_cut = max(0, min(ys) - 10)
    y0 = max(y0, face_cut)

    seeds = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = px[x, y]
            if is_leaf(r, g, b, a) or is_root(r, g, b, a) or is_dirt_ink(r, g, b, a) or is_low_glint(r, g, b, a):
                seeds.append((x, y))

    # near-white tag only if it sits against a leaf or root (not the sailor collar)
    plant = set(seeds)
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = px[x, y]
            if not is_near_white(r, g, b, a):
                continue
            if any((x + dx, y + dy) in plant for dx in range(-6, 7) for dy in range(-6, 7)):
                seeds.append((x, y))

    seen = set(seeds)
    q = deque(seeds)
    while q:
        x, y = q.popleft()
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)):
            xx, yy = x + dx, y + dy
            if not (x0 <= xx < x1 and y0 <= yy < y1) or (xx, yy) in seen:
                continue
            r, g, b, a = px[xx, yy]
            # do not flood through near-white — collar and shoe highlights would leak
            if is_leaf(r, g, b, a) or is_root(r, g, b, a) or is_dirt_ink(r, g, b, a) or is_low_glint(r, g, b, a):
                seen.add((xx, yy))
                q.append((xx, yy))
            elif is_near_white(r, g, b, a) and any((x + dx2, y + dy2) in plant for dx2 in range(-4, 5) for dy2 in range(-4, 5)):
                seen.add((xx, yy))
                q.append((xx, yy))
    mp = m.load()
    for x, y in seen:
        mp[x, y] = 255
    m = m.filter(ImageFilter.MaxFilter(3))
    mp = m.load()
    for y in range(0, face_cut):
        for x in range(w):
            mp[x, y] = 0
    return m


def _is_plant_color(c):
    r, g, b, a = c
    return is_leaf(r, g, b, a) or is_root(r, g, b, a) or is_low_glint(r, g, b, a)


def _left_silhouette(fr: Image.Image, mask: Image.Image, y0: int, y1: int) -> dict:
    """Left body edge per row, interpolated across the hole so we do not bite the hip."""
    px, m = fr.load(), mask.load()
    w, h = fr.size
    edge = {}
    for y in range(max(0, y0 - 20), min(h, y1 + 20)):
        for x in range(w):
            if m[x, y] < 128 and px[x, y][3] > 80:
                edge[y] = x
                break
    # Rows whose first unmasked pixel is the *right* of the hole jump inward — ignore those.
    # Use a running edge from rows outside the hole.
    known = sorted((y, x) for y, x in edge.items() if y < y0 or y >= y1)
    if not known:
        known = sorted(edge.items())
    out = {}
    for y in range(y0, y1):
        above = [p for p in known if p[0] <= y]
        below = [p for p in known if p[0] >= y]
        if above and below:
            y0k, x0k = above[-1]
            y1k, x1k = below[0]
            if y1k == y0k:
                out[y] = x0k
            else:
                t = (y - y0k) / (y1k - y0k)
                out[y] = int(round(x0k + t * (x1k - x0k)))
        elif above:
            out[y] = above[-1][1]
        elif below:
            out[y] = below[0][1]
    return out


def fill_hole(fr: Image.Image, mask: Image.Image, who: str) -> Image.Image:
    """Paint the sprig hole with a flat official jacket/skirt cel, darker on the left."""
    out = fr.copy()
    op, m, src = out.load(), mask.load(), fr.load()
    w, h = out.size
    holes = [(x, y) for y in range(h) for x in range(w) if m[x, y] >= 128]
    if not holes:
        return out
    ys = [p[1] for p in holes]
    y0, y1 = min(ys), max(ys) + 1
    mid_x = sum(p[0] for p in holes) / len(holes)
    sil = _left_silhouette(fr, mask, y0, y1)
    fill, shadow = HOLE_FILL[who]
    ink = INK
    for x, y in holes:
        edge = sil.get(y, int(mid_x) - 20)
        if x < edge - 1:
            op[x, y] = (0, 0, 0, 0)
        elif x <= edge + 1:
            op[x, y] = ink  # restore the hip outline the sprig hid
        elif x <= mid_x - 4:
            op[x, y] = shadow
        else:
            op[x, y] = fill
    return out


def clean_kneel(fr: Image.Image, who: str) -> Image.Image:
    m = sprig_mask(fr)
    out = fill_hole(fr, m, who)
    # Second pass only inside the original mask bbox (dilated), never the face or shins.
    bbox = m.getbbox()
    if not bbox:
        return out
    x0, y0, x1, y1 = bbox
    x0, y0 = max(0, x0 - 4), max(0, y0 - 4)
    x1, y1 = min(out.width, x1 + 4), min(out.height, y1 + 4)
    leftover = Image.new("L", out.size, 0)
    lp, px = leftover.load(), out.load()
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = px[x, y]
            if is_leaf(r, g, b, a) or is_root(r, g, b, a) or is_low_glint(r, g, b, a):
                lp[x, y] = 255
                n += 1
    if n:
        leftover = leftover.filter(ImageFilter.MaxFilter(3))
        out = fill_hole(out, leftover, who)
    # Paint leftover pale tag/cuff stubs on the midriff (never the face or shoes).
    if bbox:
        x0, y0, x1, y1 = bbox
        x0, y0 = max(0, x0 - 8), max(0, y0 - 2)
        x1, y1 = min(out.width, x1 + 8), min(out.height, min(y1 + 2, 188))
        pale = Image.new("L", out.size, 0)
        pp, px = pale.load(), out.load()
        pn = 0
        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b, a = px[x, y]
                if a < 80:
                    continue
                lum = (r + g + b) // 3
                # Grey/white stubs only (equal channels). Skin is r>>g>>b; gold is r>g>>b.
                if lum >= 140 and abs(r - g) < 18 and abs(g - b) < 18:
                    pp[x, y] = 255
                    pn += 1
        if pn:
            out = fill_hole(out, pale.filter(ImageFilter.MaxFilter(3)), who)
    return out


def _ellipse(d, box, fill, outline=INK, width=2):
    d.ellipse(box, fill=fill, outline=outline, width=width)


def draw_cuff(d, who, wx, wy):
    """A short official cuff overlapping the existing left jacket hem — no new arm."""
    sleeve, slt = SLEEVE[who], SLEEVE_LT[who]
    _ellipse(d, (wx - 9, wy - 7, wx + 9, wy + 7), sleeve, INK, 2)
    d.ellipse((wx - 6, wy - 5, wx + 6, wy + 4), fill=slt)
    if who == "aoi":
        d.arc((wx - 8, wy - 6, wx + 8, wy + 6), 200, 340, fill=CUFF_AOI, width=2)
    else:
        d.line([(wx - 6, wy - 1), (wx + 6, wy - 1)], fill=GOLD, width=2)


def draw_press_hand(im: Image.Image, who: str, palm):
    """Compact official-style hand on the LEFT, pressing a seed into the rim."""
    d = ImageDraw.Draw(im)
    skin, sh = SKIN[who]
    px, py = palm
    # cuff sits on the existing jacket hem, just above the wrist
    draw_cuff(d, who, px + 4, py - 10)
    # back of the hand
    _ellipse(d, (px - 9, py - 9, px + 10, py + 5), skin, INK, 2)
    d.ellipse((px - 7, py - 8, px + 3, py + 1), fill=sh)
    # thumb toward the body (right of the palm)
    _ellipse(d, (px + 5, py - 4, px + 14, py + 6), skin, INK, 2)
    # three curled fingers, short official capsules
    for dx, dy in ((-6, 4), (0, 6), (6, 4)):
        _ellipse(d, (px + dx - 4, py + dy - 2, px + dx + 4, py + dy + 5), skin, INK, 2)
    d.ellipse((px - 3, py + 3, px + 2, py + 7), fill=sh)
    # seed, half-buried at the fingertips
    _ellipse(d, (px - 4, py + 3, px + 4, py + 11), SEED, INK, 1)
    d.ellipse((px - 2, py + 4, px + 1, py + 7), fill=SEED_SH)
    return im


def draw_pat_hand(im: Image.Image, who: str, palm):
    """Open palmar pat: short rounded pads, not drippy fingers."""
    d = ImageDraw.Draw(im)
    skin, sh = SKIN[who]
    px, py = palm
    draw_cuff(d, who, px + 4, py - 9)
    _ellipse(d, (px - 11, py - 8, px + 12, py + 5), skin, INK, 2)
    d.ellipse((px - 8, py - 2, px + 8, py + 5), fill=sh)
    for dx in (-9, -3, 3, 9):
        _ellipse(d, (px + dx - 4, py + 2, px + dx + 4, py + 8), skin, INK, 2)
    _ellipse(d, (px + 8, py - 5, px + 16, py + 5), skin, INK, 2)
    return im


def recolor_held_mugwort(fr: Image.Image) -> Image.Image:
    """Keep the official hold-a-sprig pose; shift ginger greens toward mugwort."""
    im = fr.copy()
    px = im.load()
    w, h = im.size
    leaves = [(x, y) for y in range(h) for x in range(w) if is_leaf(*px[x, y])]
    if not leaves:
        return im
    xs, ys = [p[0] for p in leaves], [p[1] for p in leaves]
    x0, y0 = max(0, min(xs) - 4), max(0, min(ys) - 4)
    x1, y1 = min(w, max(xs) + 5), min(h, max(ys) + 5)
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = px[x, y]
            if a < 80:
                continue
            if g > r + 10 and g > 50:
                px[x, y] = (min(255, int(r * 0.9 + 20)), min(255, int(g * 0.85 + 30)), min(255, int(b * 0.8 + 20)), a)
    return im


def plant_frames(who: str):
    """6 RGBA 200x256 frames, no pot baked in: stand, squat, press, pat, rise, stand."""
    fr = slice_gpick(who)
    kneel = clean_kneel(fr[2], who)
    press = kneel.copy()
    pat = kneel.copy()
    # Palm at the left-side pot rim (scale 2.9, foot y=252, h≈64, rim≈188).
    palm = (72, 190)
    draw_press_hand(press, who, palm)
    draw_pat_hand(pat, who, (74, 191))
    return [fr[0], fr[1], press, pat, fr[1], fr[5]]


def potpick_frames(who: str):
    """Official pick sequence, mugwort recolor on the hold frames, no cuts."""
    fr = slice_gpick(who)
    return [
        fr[0],
        fr[1],
        recolor_held_mugwort(fr[2]),
        recolor_held_mugwort(fr[3]),
        recolor_held_mugwort(fr[4]),
        fr[5],
    ]


def make_sheet(frames):
    im = Image.new("RGBA", (1248, 272), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        im.paste(f, (8 + i * (200 + 8), 8), f)
    return im


def write_world_sheets(root: Path):
    world = root / "world"
    for who in ("ryo", "aoi"):
        make_sheet(plant_frames(who)).save(world / f"{who}_gplant.webp", "WEBP", lossless=True, quality=100, method=6)
        make_sheet(potpick_frames(who)).save(world / f"{who}_ppick.webp", "WEBP", lossless=True, quality=100, method=6)
        print("wrote", world / f"{who}_gplant.webp", world / f"{who}_ppick.webp")


def debug_zooms():
    OUT_DEBUG.mkdir(parents=True, exist_ok=True)
    for who in ("ryo", "aoi"):
        fr0 = slice_gpick(who)
        cl = clean_kneel(fr0[2], who)
        m = sprig_mask(fr0[2])
        ov = fr0[2].copy()
        op, mp = ov.load(), m.load()
        w, h = ov.size
        xs, ys = [], []
        for y in range(h):
            for x in range(w):
                if mp[x, y] >= 128:
                    op[x, y] = (255, 40, 40, 180)
                    xs.append(x); ys.append(y)
        print(who, "mask", len(xs), "bbox", (min(xs), min(ys), max(xs), max(ys)) if xs else None)
        ov.resize((400, 512), Image.Resampling.NEAREST).save(OUT_DEBUG / f"{who}_mask.png")
        cl.resize((400, 512), Image.Resampling.NEAREST).save(OUT_DEBUG / f"{who}_clean_kneel.png")
        cl.crop((50, 110, 150, 230)).resize((400, 480), Image.Resampling.NEAREST).save(OUT_DEBUG / f"{who}_clean_mid.png")
        frames = plant_frames(who)
        names = ("stand", "squat", "press", "pat", "rise", "stand2")
        for i, (fr, n) in enumerate(zip(frames, names)):
            fr.resize((400, 512), Image.Resampling.NEAREST).save(OUT_DEBUG / f"{who}_{i}_{n}.png")
            fr.crop((40, 80, 160, 240)).resize((480, 640), Image.Resampling.NEAREST).save(
                OUT_DEBUG / f"{who}_{i}_{n}_torso.png"
            )
        print("wrote", who)
    print("debug", OUT_DEBUG)


if __name__ == "__main__":
    debug_zooms()
