#!/usr/bin/env python3
"""GGD-50 garden previews: clinic nook, pot states, pick/plant strips, rare-find toast.

Handmade cel art over the existing c2_clinic.webp so the rest of the room stays pixel-identical.
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

from paint_plant_frames import (
    POT_FOOT,
    POT_SCALE,
    plant_frames,
    potpick_frames,
    write_world_sheets,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CLINIC = ROOT / "world" / "c2_clinic.webp"
GPICK = {
    "ryo": HERE / "sprites" / "ryo_gpick.png",
    "aoi": HERE / "sprites" / "aoi_gpick.png",
}
OUT = Path("/workspace/v6560-review/garden")

INK = (26, 18, 16, 255)
INK_S = (26, 18, 16)
CREAM = (232, 217, 183)
BEAM = (90, 62, 42)
BEAM_DK = (58, 40, 28)
FLOOR_A = (184, 141, 97)
FLOOR_B = (169, 121, 78)
FLOOR_LINE = (90, 58, 38)
SUN_A = (210, 170, 118)
SUN_B = (196, 152, 100)
WOOD = (107, 68, 25)
WOOD_LT = (138, 90, 50)
POT = (176, 96, 58)
POT_LT = (198, 118, 74)
POT_DK = (128, 68, 40)
SOIL = (74, 52, 34)
SOIL_LT = (96, 68, 44)
LEAF = (95, 140, 78)
LEAF_LT = (132, 168, 104)
LEAF_DK = (62, 100, 54)
FRAME = (75, 52, 37)
FRAME_OUT = (44, 39, 52)

# Cabinet we are opening (from the live room art)
CAB = (129, 39, 470, 300)
# Garden nook on the floor (walkable 3x3)
NOOK = (132, 148, 464, 428)
# Window in the opened wall
WIN = (156, 28, 438, 142)

# 3x3 pot foot positions (world px). Spacing leaves ~56–70 px aisles.
def pot_feet():
    x0, y0, x1, y1 = NOOK
    # inset so rim/leaves stay inside the nook frame
    cols = [x0 + 62, (x0 + x1) // 2, x1 - 62]
    rows = [y0 + 70, (y0 + y1) // 2 + 8, y1 - 48]
    feet = []
    for r, y in enumerate(rows):
        for c, x in enumerate(cols):
            feet.append((c, r, x, y))
    return feet


def font(size, bold=True):
    cands = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in cands:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def slice_gpick(who):
    im = Image.open(GPICK[who]).convert("RGBA")
    gw, cw, ch = 8, 200, 256
    frames = []
    for i in range(6):
        x = gw + i * (cw + gw)
        y = gw
        frames.append(im.crop((x, y, x + cw, y + ch)))
    return frames


def restore_wall_and_floor(base: Image.Image) -> Image.Image:
    """Erase the cabinet. Continue the cream wall from the right, and the SAME
    vertical floor planks from below the cabinet so the nook sits on the room's floor."""
    im = base.copy()
    px = im.load()
    w, h = im.size
    x0, y0, x1, y1 = CAB  # 129,39,470,300

    # 1) Cream wall + rails: copy from the clear wall just to the right of the cabinet.
    for x in range(x0 - 1, x1 + 2):
        sx = 488 + ((x - x0) % 40)  # 488-528 is cream wall, before hanging herbs
        for y in range(10, 88):
            px[x, y] = px[min(sx, w - 1), y]

    # 2) Floor inside the old cabinet footprint: copy the existing planks from below
    #    (same x, so the boards run straight into the nook).
    for x in range(max(100, x0 - 2), min(x1 + 3, w)):
        for y in range(88, 301):
            src_y = 320 + (y - 88) % 140  # 320-459 is original floor
            px[x, y] = px[x, src_y]

    # 3) Reassert the left inner wall so we never smear floor onto it.
    for x in range(86, 100):
        for y in range(20, 320):
            px[x, y] = px[x, 500]

    return im


def _line(d, a, b, fill=INK_S, w=3):
    d.line([a, b], fill=fill, width=w)


def _rr(d, box, fill=None, outline=INK_S, w=3):
    d.rounded_rectangle(box, radius=4, fill=fill, outline=outline, width=w)


def draw_window(d: ImageDraw.ImageDraw, glow_layer: Image.Image):
    x0, y0, x1, y1 = WIN
    # lintel / posts, flush with the room's top rail
    d.rectangle((x0 - 10, y0 - 6, x1 + 10, y0 + 8), fill=BEAM_DK, outline=INK_S, width=3)
    d.rectangle((x0 - 8, y0, x0 + 6, y1 + 6), fill=BEAM, outline=INK_S, width=3)
    d.rectangle((x1 - 6, y0, x1 + 8, y1 + 6), fill=BEAM, outline=INK_S, width=3)
    d.rectangle((x0 - 10, y1, x1 + 10, y1 + 10), fill=BEAM_DK, outline=INK_S, width=3)
    # paper / warm alley light
    d.rectangle((x0 + 6, y0 + 8, x1 - 6, y1 - 2), fill=(248, 234, 196), outline=INK_S, width=3)
    g = ImageDraw.Draw(glow_layer)
    for i, a in enumerate((55, 28)):
        pad = 10 + i * 22
        g.ellipse((x0 - pad, y0, x1 + pad, y1 + 80 + i * 24), fill=(255, 214, 140, a))
    # faint distant foliage, one or two ink-outline clumps, not random dots
    d.ellipse((x0 + 36, y0 + 28, x0 + 88, y0 + 70), fill=(210, 214, 170), outline=None)
    d.ellipse((x1 - 100, y0 + 36, x1 - 40, y0 + 80), fill=(204, 210, 164), outline=None)
    # 2x2 panes
    inner = (x0 + 10, y0 + 14, x1 - 10, y1 - 6)
    mx = (inner[0] + inner[2]) // 2
    my = (inner[1] + inner[3]) // 2
    # paper highlight on left of each pane
    for px0, py0, px1, py1 in (
        (inner[0], inner[1], mx, my),
        (mx, inner[1], inner[2], my),
        (inner[0], my, mx, inner[3]),
        (mx, my, inner[2], inner[3]),
    ):
        d.rectangle((px0 + 3, py0 + 3, px0 + 9, py1 - 3), fill=(255, 250, 230))
    d.rectangle((mx - 3, inner[1], mx + 3, inner[3]), fill=BEAM_DK, outline=INK_S, width=2)
    d.rectangle((inner[0], my - 3, inner[2], my + 3), fill=BEAM_DK, outline=INK_S, width=2)


def draw_nook_floor(d, im):
    """Sill, posts and a light wash only — the boards themselves are the room's own planks."""
    x0, y0, x1, y1 = NOOK
    # sill under the window, sitting on the floor
    d.rectangle((x0 - 4, y0 - 8, x1 + 4, y0 + 14), fill=BEAM, outline=INK_S, width=3)
    d.rectangle((x0, y0 - 2, x1, y0 + 10), fill=WOOD_LT, outline=INK_S, width=2)
    # posts of the wall opening (from the beam down to a short stop, not a full boxed rug)
    d.rectangle((x0 - 10, 86, x0 + 3, y0 + 18), fill=BEAM, outline=INK_S, width=3)
    d.rectangle((x1 - 3, 86, x1 + 10, y0 + 18), fill=BEAM, outline=INK_S, width=3)
    # no boxed threshold — the nook is just the opened wall and the same floor


def draw_mini_cabinet(d):
    """A short drawer stack to the right of the nook, so the room still reads as an apothecary."""
    x0, y0 = 476, 40
    cols, rows = 2, 4
    cw, ch = 42, 38
    pad = 6
    W = pad * 2 + cols * cw
    H = pad * 2 + rows * ch
    d.rectangle((x0, y0, x0 + W, y0 + H), fill=(58, 40, 28), outline=INK_S, width=3)
    for r in range(rows):
        for c in range(cols):
            dx = x0 + pad + c * cw
            dy = y0 + pad + r * ch
            d.rectangle((dx, dy, dx + cw - 3, dy + ch - 3), fill=WOOD, outline=INK_S, width=2)
            # label
            d.rectangle((dx + 8, dy + 8, dx + cw - 11, dy + 22), fill=(246, 237, 221), outline=INK_S, width=1)
            # knob
            d.ellipse((dx + cw // 2 - 5, dy + 25, dx + cw // 2 + 4, dy + 34), fill=(212, 176, 74), outline=INK_S, width=1)


def pot_poly(cx, cy, r=16, h=22, s=1.0):
    """Trapezoid pot, foot at (cx, cy). Returns rim y."""
    rim_y = cy - h
    inset = max(2, int(round(4 * s)))
    lip = max(2, int(round(4 * s)))
    top_l, top_r = cx - r, cx + r
    bot_l, bot_r = cx - r + inset, cx + r - inset
    body = [(top_l, rim_y + lip), (top_r, rim_y + lip), (bot_r, cy), (bot_l, cy)]
    return body, rim_y, top_l, top_r


def draw_pot(d, cx, cy, state="empty", variant=0, sparkle=False, scale=1.0):
    """state: empty | planted | bloomed. cy is the foot. scale=1 is room pixels."""
    s = float(scale)
    r = int(round((15 + (variant % 3)) * s))
    h = int(round((22 + (variant % 3)) * s))
    body, rim_y, top_l, top_r = pot_poly(cx, cy, r=r, h=h, s=s)
    bot_l, bot_r = cx - r + int(4 * s), cx + r - int(4 * s)
    # shadow on the boards
    d.ellipse((cx - r + int(2 * s), cy - int(4 * s), cx + r - int(2 * s), cy + int(5 * s)), fill=(90, 62, 40))
    # body
    d.polygon(body, fill=POT, outline=INK_S)
    # slightly thicker ink
    d.line(body + [body[0]], fill=INK_S, width=3)
    # left highlight
    lw = max(2, int(round(3 * min(s, 1.6))))
    d.line((top_l + int(3 * s), rim_y + int(6 * s), bot_l + int(3 * s), cy - int(3 * s)), fill=POT_LT, width=lw)
    # rim lip
    d.ellipse((top_l - 1, rim_y - int(5 * s), top_r + 1, rim_y + int(9 * s)), fill=POT_DK, outline=INK_S, width=lw)
    d.ellipse((top_l + int(2 * s), rim_y - int(2 * s), top_r - int(2 * s), rim_y + int(6 * s)), fill=SOIL if state != "empty" else SOIL_LT, outline=INK_S, width=max(2, lw - 1))
    if state == "empty":
        d.ellipse((cx - int(6 * s), rim_y - int(1 * s), cx + int(6 * s), rim_y + int(4 * s)), fill=SOIL)
    elif state == "planted":
        d.ellipse((cx - int(7 * s), rim_y - int(3 * s), cx + int(7 * s), rim_y + int(5 * s)), fill=SOIL)
        d.ellipse((cx - int(5 * s), rim_y - int(4 * s), cx + int(5 * s), rim_y + int(2 * s)), fill=SOIL_LT)
        d.ellipse((cx - int(2 * s), rim_y - int(5 * s), cx + int(2 * s), rim_y - int(1 * s)), fill=(214, 196, 140), outline=INK_S, width=max(1, lw - 1))
    else:
        d.ellipse((cx - int(7 * s), rim_y - int(3 * s), cx + int(7 * s), rim_y + int(4 * s)), fill=SOIL)
        draw_mugwort(d, cx, rim_y, variant, scale=s)
    if sparkle:
        draw_sparkle(d, cx + r - 2, rim_y - int(16 * s))
    return rim_y


def draw_mugwort(d, cx, rim_y, variant=0, scale=1.0):
    """Cel mugwort: a small palmate herb, silvery green, ink outline. Not a tree."""
    s = float(scale)
    lw = max(2, int(round(2 * min(s, 1.8))))
    d.line((cx, rim_y, cx, rim_y - int(8 * s)), fill=LEAF_DK, width=lw)
    node = (cx, rim_y - int(10 * s))
    arms = [
        (0, -16, 5, 9),
        (-10, -12, 5, 8),
        (10, -12, 5, 8),
        (-13, -4, 5, 7),
        (13, -4, 5, 7),
        (0, -6, 4, 6),
    ]
    jitter = int(round((-1, 0, 1, 0, -1, 1)[variant % 6] * s))
    for dx, dy, rx, ry in arms:
        x, y = node[0] + int(dx * s) + jitter, node[1] + int(dy * s)
        rx, ry = max(2, int(rx * s)), max(2, int(ry * s))
        d.ellipse((x - rx, y - ry, x + rx, y + ry), fill=LEAF, outline=INK_S, width=lw)
        d.ellipse((x - rx + int(2 * s), y - ry + int(1 * s), x, y + int(1 * s)), fill=LEAF_LT)
        d.line((node[0], node[1], x, y - 2), fill=LEAF_DK, width=max(1, lw - 1))


def draw_sparkle(d, x, y):
    # 8-point sparkle, gold
    col = (255, 220, 110)
    d.line((x, y - 9, x, y + 9), fill=col, width=2)
    d.line((x - 9, y, x + 9, y), fill=col, width=2)
    d.line((x - 6, y - 6, x + 6, y + 6), fill=col, width=2)
    d.line((x - 6, y + 6, x + 6, y - 6), fill=col, width=2)
    d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(255, 248, 200), outline=INK_S, width=1)



def apply_feathered_wash(im: Image.Image) -> Image.Image:
    """Warm window light on the nook floor, edges blurred so it is not a visible box."""
    wx0, wy0, wx1, wy1 = NOOK[0] + 8, NOOK[1] + 10, NOOK[2] - 8, NOOK[3] - 6
    wash = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(wash).ellipse((wx0 - 10, wy0 - 5, wx1 + 10, wy1 - 5), fill=(255, 214, 140, 48))
    wash = wash.filter(ImageFilter.GaussianBlur(radius=36))
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rectangle((NOOK[0] - 4, NOOK[1] + 16, NOOK[2] + 4, NOOK[3] + 20), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=10))
    r, g, b, a = wash.split()
    wash = Image.merge("RGBA", (r, g, b, ImageChops.multiply(a, mask)))
    return Image.alpha_composite(im, wash)


def paint_room(state="bloomed", sparkle_i=None) -> Image.Image:
    base = Image.open(CLINIC).convert("RGBA")
    im = restore_wall_and_floor(base)
    glow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    # floor / posts first
    d = ImageDraw.Draw(im)
    draw_nook_floor(d, im)
    draw_window(d, glow)
    draw_mini_cabinet(d)
    # sunlit wash on the nook boards: feathered so there is no visible box
    im = apply_feathered_wash(im)
    # composite window glow under the pots but over the floor
    im = Image.alpha_composite(im, glow)
    d = ImageDraw.Draw(im)
    # pots, back row first so front overlap is correct
    feet = pot_feet()
    feet.sort(key=lambda t: t[3])
    for i, (c, r, x, y) in enumerate(feet):
        sparkle = sparkle_i is not None and (c + r * 3) == sparkle_i
        draw_pot(d, x, y, state=state, variant=(c * 3 + r), sparkle=sparkle)
    return im.convert("RGB")


# --------------- sprite work ---------------

def plant_bbox(fr):
    """Tight bbox of green / ginger-tan pixels in a gpick frame."""
    px = fr.load()
    w, h = fr.size
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 80:
                continue
            if g > r + 16 and g > 58 and g > b - 5:
                xs.append(x); ys.append(y)
    if not xs:
        return None
    return (max(0, min(xs) - 2), max(0, min(ys) - 2), min(w, max(xs) + 3), min(h, max(ys) + 3))


def cut_held_plant(fr):
    """Clear only the held sprig, in a tight bbox, leaving the uniform alone."""
    im = fr.copy()
    box = plant_bbox(fr)
    if not box:
        return im
    px = im.load()
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = px[x, y]
            if a < 16:
                continue
            green = g > r + 12 and g > 52
            # ginger dirt / stem, not skin (skin is r-g ~50 and lighter)
            dirt = (r > 90 and r < 200 and 40 < g < 160 and b < 90
                    and (r - g) < 80 and (r + g) < 330 and y < 210)
            if green or dirt:
                px[x, y] = (0, 0, 0, 0)
    return im


def recolor_held_mugwort(fr):
    """Keep the held-plant pose, shift ginger greens toward mugwort."""
    im = fr.copy()
    box = plant_bbox(fr)
    if not box:
        return im
    px = im.load()
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = px[x, y]
            if a < 80:
                continue
            if g > r + 10 and g > 50:
                # toward the silvery clinic mugwort
                px[x, y] = (min(255, int(r * 0.9 + 20)), min(255, int(g * 0.85 + 30)), min(255, int(b * 0.8 + 20)), a)
    return im


def paint_hands_on_rim(fr, mode="press"):
    """Cel hands over a kneel pose, at pot-rim height (mid-torso of the kneel)."""
    im = cut_held_plant(fr)
    d = ImageDraw.Draw(im)
    # kneel torso center ~ (100, 170)
    if mode == "press":
        # two small fists together, pressing a seed
        for dx in (-7, 6):
            d.ellipse((96 + dx - 7, 166, 96 + dx + 6, 180), fill=(201, 150, 110), outline=INK_S, width=2)
        d.ellipse((96, 170, 108, 178), fill=(214, 196, 140), outline=INK_S, width=1)
    else:
        # open pat: one flat hand
        d.ellipse((90, 164, 118, 180), fill=(201, 150, 110), outline=INK_S, width=2)
        d.ellipse((94, 166, 110, 174), fill=(214, 176, 140))
    return im


def make_strips():
    """6-frame pot-pick and planting strips.

    The pot sits to the LEFT of the body at ~2.9x (room pot vs SPH 86, mapped
    onto the 256-tall official cell) so a kneel puts official/new hands on the
    rim. The pot is drawn behind the body; only the lower lip sits in front of
    the shoes, so the near leg still reads as kneeling *beside* the pot.
    """
    out = {}
    cw, ch = 200, 280
    # Character is pasted at (0, 8) so official feet (y=252) land on cy=260.
    pot_x, pot_y = POT_FOOT[0], POT_FOOT[1] + 8
    sc = POT_SCALE
    # Lip in front of the shoes only (below mid-shin), not over the kneeling leg.
    LIP_Y = 214

    def compose(frames, states):
        strip = Image.new("RGBA", (6 * cw + 5 * 8, ch), (16, 12, 18, 255))
        for i, f in enumerate(frames):
            c = Image.new("RGBA", (cw, ch), (16, 12, 18, 255))
            d = ImageDraw.Draw(c)
            if states[i]:
                draw_pot(d, pot_x, pot_y, state=states[i], variant=1, scale=sc)
            c.alpha_composite(f, (0, 8))
            if states[i]:
                lip = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
                ld = ImageDraw.Draw(lip)
                draw_pot(ld, pot_x, pot_y, state=states[i], variant=1, scale=sc)
                pxd = lip.load()
                for y in range(0, LIP_Y):
                    for x in range(cw):
                        pxd[x, y] = (0, 0, 0, 0)
                c.alpha_composite(lip)
            strip.paste(c, (i * (cw + 8), 0))
        return strip

    def sheet(frames):
        im = Image.new("RGBA", (1248, 272), (0, 0, 0, 0))
        for i, f in enumerate(frames):
            im.paste(f, (8 + i * (200 + 8), 8), f)
        return im

    for who in ("ryo", "aoi"):
        pick_fr = potpick_frames(who)
        # bloomed in the pot until the lift (f2 holds the sprig at the rim), then empty
        pick_pot = ["bloomed", "bloomed", "bloomed", "empty", "empty", "empty"]
        plant_fr = plant_frames(who)
        plant_pot = ["empty", "empty", "empty", "planted", "planted", "planted"]
        out[f"{who}_potpick"] = compose(pick_fr, pick_pot)
        out[f"{who}_plant"] = compose(plant_fr, plant_pot)
        out[f"{who}_potpick_sheet"] = sheet(pick_fr)
        out[f"{who}_plant_sheet"] = sheet(plant_fr)
    return out


def make_inroom_sheet(who, kind, frames_key):
    """Character composited in the nook at game scale (SPH 86 / cell 256)."""
    return None  # filled in main() after strips exist


def make_toast_preview(room: Image.Image) -> Image.Image:
    """390x844 phone frame, nook close-up, rare-find toast + glint."""
    W, H = 390, 844
    phone = Image.new("RGB", (W, H), (10, 8, 16))
    # crop the nook, scale to fill the 'world' area
    crop = room.crop((80, 0, 560, 560)).resize((W, 520), Image.Resampling.LANCZOS)
    phone.paste(crop, (0, 80))
    # letterbox bars like the in-game HUD
    d = ImageDraw.Draw(phone)
    d.rectangle((0, 0, W, 80), fill=(12, 10, 22))
    d.rectangle((0, 700, W, H), fill=(12, 10, 22))
    # HP / yen stub
    d.text((12, 18), "HP  40/55", fill=(240, 220, 180), font=font(15))
    d.text((W - 86, 18), "¥  12", fill=(240, 220, 180), font=font(15))
    # toast
    msg = "A length of tape in the mud."
    fnt = font(14)
    # measure
    tw = d.textlength(msg, font=fnt)
    pad_x, pad_y = 16, 10
    tw, th = int(tw), 18
    box_w = tw + pad_x * 2
    bx0 = (W - box_w) // 2
    by0 = 60 + 8
    d.rounded_rectangle((bx0, by0, bx0 + box_w, by0 + th + pad_y * 2), radius=12, fill=(10, 10, 24, 230))
    # inset hairline
    d.rounded_rectangle((bx0, by0, bx0 + box_w, by0 + th + pad_y * 2), radius=12, outline=(255, 255, 255, 40), width=1)
    d.text((W // 2, by0 + pad_y + th // 2), msg, fill=(236, 230, 210), font=fnt, anchor="mm")
    # glint over a front pot (approx after resize)
    draw_sparkle(d, 196, 430)
    d.text((12, 760), "Rare find  ·  0.5%", fill=(180, 170, 150), font=font(12, bold=False))
    return phone


def caption(im: Image.Image, title: str) -> Image.Image:
    bar = 40
    out = Image.new("RGB", (im.width, im.height + bar), (16, 12, 20))
    if im.mode != "RGB":
        im = im.convert("RGB")
    out.paste(im, (0, bar))
    d = ImageDraw.Draw(out)
    d.text((12, 10), title, fill=(244, 230, 200), font=font(18))
    return out


def contact_sheet(paths_titles, path, cols=3, tw=380):
    ims = []
    for p, t in paths_titles:
        im = Image.open(p).convert("RGB")
        im.thumbnail((tw, tw), Image.Resampling.LANCZOS)
        cell_h = im.height + 36
        cell = Image.new("RGB", (tw, cell_h), (16, 12, 20))
        d = ImageDraw.Draw(cell)
        d.text((8, 8), t, fill=(232, 216, 176), font=font(14))
        cell.paste(im, ((tw - im.width) // 2, 32))
        ims.append(cell)
    if not ims:
        return
    rows = (len(ims) + cols - 1) // cols
    h = max(c.height for c in ims)
    sheet = Image.new("RGB", (cols * tw + 24, rows * h + 48), (12, 10, 16))
    d = ImageDraw.Draw(sheet)
    d.text((12, 10), "GGD-50  ·  Tsukikage mugwort garden  ·  previews", fill=(244, 234, 210), font=font(18))
    for i, c in enumerate(ims):
        r, col = divmod(i, cols)
        sheet.paste(c, (12 + col * tw, 36 + r * h))
    sheet.save(path)
    print("sheet", path, sheet.size)



def make_inroom_strips(strips_frames):
    """Honest game-scale composites: character at SPH=86, pots at room size,
    standing just north of the front-center pot, facing the camera."""
    out = {}
    SPH = 86
    scale = SPH / 256.0
    fw, fh = int(round(200 * scale)), int(round(256 * scale))
    # front-center pot is col 1, row 2
    feet = pot_feet()
    _, _, pot_x, pot_y = [f for f in feet if f[0] == 1 and f[1] == 2][0]
    # East of the pot, close enough that the left-hand at sprite x=72 meets
    # the right rim, and feet sit on the pot's ground line so y=190 hands
    # meet the 22px rim when the 256-tall sheet is drawn at SPH=86.
    stand_x, stand_y = pot_x + 24, pot_y + 1

    def compose(who, kind, frames, states):
        # base room matches the first pot state (empty for plant, bloomed for pick)
        base_state = "bloomed" if kind == "potpick" else "empty"
        room = paint_room(base_state, sparkle_i=None)
        cells = []
        for i, fr in enumerate(frames):
            # rebuild room with that one pot's state: paint all, then stamp this pot
            st = states[i]
            im = paint_room(base_state, sparkle_i=None)
            # overdraw the front-center pot in the current frame state
            d = ImageDraw.Draw(im)
            # erase a small floor patch under the pot by cloning nearby floor, then redraw
            # (the pot is already drawn in base_state; redrawing covers it)
            draw_pot(d, pot_x, pot_y, state=st, variant=1)
            frs = fr.convert("RGBA").resize((fw, fh), Image.Resampling.LANCZOS)
            px = int(round(stand_x - 96 * scale))
            py = int(round(stand_y - 252 * scale))
            if im.mode != "RGBA":
                im = im.convert("RGBA")
            im.alpha_composite(frs, (px, py))
            crop = im.crop((pot_x - 80, pot_y - 140, pot_x + 130, pot_y + 50))
            cells.append(crop)
        # strip
        cw, ch = cells[0].size
        strip = Image.new("RGBA", (6 * cw + 5 * 6, ch), (16, 12, 18, 255))
        for i, c in enumerate(cells):
            strip.paste(c, (i * (cw + 6), 0))
        return strip

    for who in ("ryo", "aoi"):
        pick_fr = potpick_frames(who)
        pick_pot = ["bloomed", "bloomed", "bloomed", "empty", "empty", "empty"]
        plant_fr = plant_frames(who)
        plant_pot = ["empty", "empty", "empty", "planted", "planted", "planted"]
        out[f"{who}_potpick_inroom"] = compose(who, "potpick", pick_fr, pick_pot)
        out[f"{who}_plant_inroom"] = compose(who, "plant", plant_fr, plant_pot)
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    write_world_sheets(ROOT)
    shots = []
    for state in ("empty", "planted", "bloomed"):
        sparkle = 0 if state == "empty" else None  # first-visit sparkle on pot 0
        im = paint_room(state, sparkle_i=sparkle)
        p = OUT / f"clinic_{state}.png"
        im.save(p)
        # also a nook close-up
        close = im.crop((90, 0, 520, 500))
        cp = OUT / f"nook_{state}.png"
        close.save(cp)
        shots.append((p, f"Room  ·  {state}"))
        shots.append((cp, f"Nook  ·  {state}"))
        print("wrote", p, im.size)

    # animation strips (preview composites; raw character sheets go to sheets/)
    strips = make_strips()
    sheet_dir = OUT / "sheets"
    sheet_dir.mkdir(exist_ok=True)
    for k, im in strips.items():
        if k.endswith("_sheet"):
            p = sheet_dir / f"{k}.png"
            im.save(p)
            print("wrote", p, im.size)
            continue
        p = OUT / f"{k}_strip.png"
        im.convert("RGB").save(p)
        shots.append((p, k.replace("_", " ")))
        print("wrote", p, im.size)

    inroom = make_inroom_strips(strips)
    for k, im in inroom.items():
        p = OUT / f"{k}_strip.png"
        im.convert("RGB").save(p)
        shots.append((p, k.replace("_", " ")))
        print("wrote", p, im.size)

    # planting gif (in-room, both characters, ryo first)
    frames = []
    for who in ("ryo", "aoi"):
        strip = inroom[f"{who}_plant_inroom"]
        cw = strip.width // 6
        # account for 5 gutters: total = 6*cw + 5*6 if cw is cell width
        cell_w = (strip.width - 5 * 6) // 6
        for i in range(6):
            x0 = i * (cell_w + 6)
            frames.append(strip.crop((x0, 0, x0 + cell_w, strip.height)).convert("RGB"))
    # hold last
    gif_frames = frames + [frames[-1]] * 2
    gif_path = OUT / "planting.gif"
    gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:], duration=420, loop=0)
    print("wrote", gif_path)

    # pot-pick gif
    frames = []
    for who in ("ryo",):
        strip = inroom[f"{who}_potpick_inroom"]
        cell_w = (strip.width - 5 * 6) // 6
        for i in range(6):
            x0 = i * (cell_w + 6)
            frames.append(strip.crop((x0, 0, x0 + cell_w, strip.height)).convert("RGB"))
    gif_frames = frames + [frames[-1]] * 2
    gif_path = OUT / "potpick.gif"
    gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:], duration=380, loop=0)
    print("wrote", gif_path)

    room = paint_room("bloomed", sparkle_i=7)
    toast = make_toast_preview(room)
    tp = OUT / "rare_find_toast.png"
    toast.save(tp)
    shots.append((tp, "Rare-find toast"))
    print("wrote", tp)

    contact_sheet(shots, OUT / "garden_sheet.png", cols=3, tw=400)
    print("done", OUT)


if __name__ == "__main__":
    main()
