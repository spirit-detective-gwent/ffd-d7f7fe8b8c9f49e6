#!/usr/bin/env python3
"""Two-person carry sheet for c2_goda Fierce carry-off.
Old Sato (left, slightly back) and Tome-baa (right, nearer) walk Gōda between them.
His arms are over their shoulders, his feet drag. Cel parts come from their walk/idle/lie
sheets; holding arms are painted in the same ink/fill language.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math

ROOT = Path(__file__).resolve().parents[2]
SATO_W = Image.open(ROOT / 'world/npc3_net_walk.webp').convert('RGBA')
TOME_W = Image.open(ROOT / 'ck/npc_clerk_walk.webp').convert('RGBA')
GODA_I = Image.open(ROOT / 'world/mb2_sentoY_idle.webp').convert('RGBA')
GODA_L = Image.open(ROOT / 'world/mb2_sentoY_lie.webp').convert('RGBA')
CW, CH = 208, 272
INK = (20, 17, 23, 255)
SKIN_G, SKIN_GD = (233, 185, 140, 255), (214, 150, 112, 255)
SKIN_S, SKIN_T = (228, 186, 150, 255), (230, 188, 152, 255)
SATO_SH, SATO_SHD = (168, 80, 46, 255), (140, 62, 34, 255)
TOME_SL, TOME_SLD = (228, 221, 196, 255), (208, 196, 168, 255)
CELL_W, CELL_H, FOOT, SRC_FOOT = 520, 300, 288, 260
FRAMES, WALK_IDX = 4, [0, 2, 4, 6]
OUT_PREV = Path('/workspace/v6560-review/fix_t293/goda_carry_sheet.png')
OUT_SHEET = ROOT / 'world/mb2_sentoY_carry.webp'
OUT_DIR = Path('/tmp/carrybuild'); OUT_DIR.mkdir(exist_ok=True)

def cell(im, r, c):
    return im.crop((c * CW, r * CH, c * CW + CW, r * CH + CH)).copy()

def scale(im, k):
    if abs(k - 1) < 1e-3:
        return im
    w, h = im.size
    return im.resize((max(1, round(w * k)), max(1, round(h * k))), Image.Resampling.LANCZOS)

def rot(im, deg):
    return im.rotate(deg, resample=Image.Resampling.BICUBIC, expand=True, fillcolor=(0, 0, 0, 0))

def bbox(im):
    return im.split()[-1].getbbox()

def blit(dst, src, x, y):
    dst.alpha_composite(src, (int(round(x)), int(round(y))))

def erase_rect(im, box, feather=0):
    x0, y0, x1, y1 = [int(v) for v in box]
    mask = Image.new('L', im.size, 0)
    ImageDraw.Draw(mask).rectangle((x0, y0, x1, y1), fill=255)
    if feather:
        mask = mask.filter(ImageFilter.GaussianBlur(feather))
    r, g, b, a = im.split()
    im.paste(Image.merge('RGBA', (r, g, b, ImageChops.subtract(a, mask))))
    return im

def close_goda_eye(im):
    """Cover the open eye on a right-facing Gōda cell (eye ~ 130, 58)."""
    out = im.copy(); px = out.load(); w, h = out.size
    # only meaningful on a full 208-wide cell; if cropped, search
    targets = [(130, 58), (128, 56), (132, 60)]
    b = bbox(im)
    if b and im.size != (208, 272):
        x0, y0, x1, y1 = b
        targets = [(int(x0 + (x1 - x0) * 0.78), int(y0 + (y1 - y0) * 0.48))]
    for ex, ey in targets:
        for dy in range(-5, 6):
            for dx in range(-8, 9):
                x, y = ex + dx, ey + dy
                if not (0 <= x < w and 0 <= y < h):
                    continue
                r, g, b, a = px[x, y]
                if a < 80:
                    continue
                t = max(0.0, 1.0 - (dx * dx) / 55 - (dy * dy) / 20)
                if t > 0 and r + g + b > 90:
                    px[x, y] = (int(r * (1 - t) + SKIN_G[0] * t),
                                int(g * (1 - t) + SKIN_G[1] * t),
                                int(b * (1 - t) + SKIN_G[2] * t), a)
        ImageDraw.Draw(out).arc((ex - 7, ey - 2, ex + 7, ey + 5), 200, 345, fill=INK, width=2)
    return out

def capsule(im, p1, p2, radius, fill, ink=INK, ink_w=2):
    """Antialiased limb: ink capsule behind, fill capsule, optional inner shade."""
    d = ImageDraw.Draw(im, 'RGBA')
    x1, y1 = p1; x2, y2 = p2
    # draw via a thick line + end circles (ImageDraw.line has rounded ends if we use a wide line)
    if ink and ink_w:
        d.line((x1, y1, x2, y2), fill=ink, width=int(radius * 2 + ink_w * 2))
        r = radius + ink_w
        d.ellipse((x1 - r, y1 - r, x1 + r, y1 + r), fill=ink)
        d.ellipse((x2 - r, y2 - r, x2 + r, y2 + r), fill=ink)
    d.line((x1, y1, x2, y2), fill=fill, width=int(radius * 2))
    d.ellipse((x1 - radius, y1 - radius, x1 + radius, y1 + radius), fill=fill)
    d.ellipse((x2 - radius, y2 - radius, x2 + radius, y2 + radius), fill=fill)

def polyline_limb(im, pts, radius, fill, ink=INK, ink_w=2):
    for a, b in zip(pts, pts[1:]):
        capsule(im, a, b, radius, fill, ink, ink_w)

def hand(im, cx, cy, fill, ink=INK, s=1.0):
    r = 7 * s
    d = ImageDraw.Draw(im, 'RGBA')
    d.ellipse((cx - r - 1, cy - r - 1, cx + r + 1, cy + r + 1), fill=ink)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)

def lie_legs():
    """Tight trousers + zori from the lie sheet (feet on the left)."""
    fr = GODA_L.crop((0, 0, 336, 128))
    # feet 48–70, trousers to ~160, vertical 55–128
    legs = fr.crop((44, 50, 168, 128)).copy()
    return legs

TROU = (58, 52, 48, 255)  # Gōda's trouser fill, sampled from the lie sheet

def goda_carried(bob=0, leg_tilt=0):
    """Assemble a slumped, semi-upright Gōda: happi torso, trailing legs.
    Returns (image, shoulder_L, shoulder_R, hip) in local coordinates.
    Legs and the thigh seam go down first; the happi body is composited on top
    so the jacket hem tucks over the thigh (no hole at the peak).
    """
    src = cell(GODA_I, 2, 0)  # side profile already reads as a quiet, half-lidded face
    body = src.copy()
    erase_rect(body, (0, 155, 208, 272), feather=3)
    body = rot(body, -8)
    legs = rot(lie_legs(), 28 + leg_tilt)

    W, H = 420, 340
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    bx, by = 150, 10
    # hip end tucks under the happi hem; feet hang lower so they still drag after we raise him
    lx, ly = 88, 160 + bob
    blit(out, legs, lx, ly)
    # the lie-legs peak left a wedge gap at the thigh; fill it in trouser colour
    seam = Image.new('RGBA', out.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(seam, 'RGBA')
    hx, hy = 248, 178 + bob
    thigh = [
        (hx - 60, hy - 4),
        (hx - 52, hy - 18),
        (hx - 36, hy - 18),
        (hx - 16, hy - 12),
        (hx + 22, hy - 8),
        (hx + 18, hy + 26),
        (hx - 44, hy + 20),
        (hx - 58, hy + 12),
    ]
    d.line([(hx - 54, hy - 14), (hx - 52, hy - 18), (hx - 36, hy - 18), (hx - 22, hy - 14)], fill=INK, width=3)
    d.polygon(thigh, fill=TROU)
    out.alpha_composite(seam)
    blit(out, body, bx, by)
    shL = (bx + 70, by + 108)
    shR = (bx + 175, by + 112)
    hip = (bx + 120, by + 165)
    return out, shL, shR, hip

def compose(fi):
    wi = WALK_IDX[fi]
    k = 2
    W, H = CELL_W * k, CELL_H * k
    foot = FOOT * k
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    bob = (0, 2, 0, -2)[fi] * k
    step_s = (0, 4, 0, -3)[fi] * k
    step_t = (0, -3, 0, 4)[fi] * k
    leg_tilt = (0, 3, 0, -3)[fi]

    sato = scale(cell(SATO_W, 2, wi), 1.06 * k)
    tome = scale(cell(TOME_W, 2, wi), k)
    goda, shL, shR, hip = goda_carried(bob=0, leg_tilt=leg_tilt)
    goda = scale(goda, k)

    sato_x = 95 * k + step_s
    sato_y = foot - int(SRC_FOOT * 1.06 * k) + bob
    tome_x = 250 * k + step_t
    tome_y = foot - SRC_FOOT * k + bob
    # raise Gōda so his shoulders sit on theirs (arms over shoulders), feet still drag
    sato_sh_y = sato_y + sato.size[1] * 0.32
    goda_x = 18 * k
    goda_y = sato_sh_y - shL[1] * k + 10 * k + bob

    blit(canvas, sato, sato_x, sato_y)
    blit(canvas, goda, goda_x, goda_y)
    blit(canvas, tome, tome_x, tome_y)

    s_sh = (sato_x + sato.size[0] * 0.58, sato_y + sato.size[1] * 0.30)
    t_sh = (tome_x + tome.size[0] * 0.38, tome_y + tome.size[1] * 0.27)
    g_shL = (goda_x + shL[0] * k, goda_y + shL[1] * k)
    g_shR = (goda_x + shR[0] * k, goda_y + shR[1] * k)
    g_waist = (goda_x + hip[0] * k + 8 * k, goda_y + hip[1] * k + 4 * k)

    arms = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    iw = max(2, int(1.2 * k))
    polyline_limb(arms, [g_shL, (s_sh[0] + 6 * k, s_sh[1] - 10 * k), (s_sh[0] + 2 * k, s_sh[1] + 22 * k)],
                  radius=5 * k, fill=SKIN_G, ink=INK, ink_w=iw)
    hand(arms, s_sh[0] + 2 * k, s_sh[1] + 28 * k, SKIN_G, INK, s=k)
    polyline_limb(arms, [g_shL, (s_sh[0] + 6 * k, s_sh[1] - 8 * k)],
                  radius=2.5 * k, fill=SKIN_GD, ink=None, ink_w=0)

    polyline_limb(arms, [g_shR, (t_sh[0] - 2 * k, t_sh[1] - 10 * k), (t_sh[0] + 4 * k, t_sh[1] + 24 * k)],
                  radius=5 * k, fill=SKIN_G, ink=INK, ink_w=iw)
    hand(arms, t_sh[0] + 4 * k, t_sh[1] + 30 * k, SKIN_G, INK, s=k)
    polyline_limb(arms, [g_shR, (t_sh[0] - 2 * k, t_sh[1] - 8 * k)],
                  radius=2.5 * k, fill=SKIN_GD, ink=None, ink_w=0)

    polyline_limb(arms, [s_sh, ((s_sh[0] + g_waist[0]) / 2 + 6 * k, (s_sh[1] + g_waist[1]) / 2 + 10 * k), g_waist],
                  radius=4.5 * k, fill=SATO_SH, ink=INK, ink_w=iw)
    hand(arms, g_waist[0] + 2 * k, g_waist[1] + 4 * k, SKIN_S, INK, s=k * 0.95)

    polyline_limb(arms, [t_sh, ((t_sh[0] + g_waist[0]) / 2 - 6 * k, (t_sh[1] + g_waist[1]) / 2 + 12 * k),
                         (g_waist[0] + 10 * k, g_waist[1] + 8 * k)],
                  radius=4 * k, fill=TOME_SL, ink=INK, ink_w=iw)
    hand(arms, g_waist[0] + 12 * k, g_waist[1] + 12 * k, SKIN_T, INK, s=k * 0.9)

    canvas.alpha_composite(arms)
    return canvas.resize((CELL_W, CELL_H), Image.Resampling.LANCZOS)


def main():
    rights = []
    for i in range(FRAMES):
        fr = compose(i)
        fr.save(OUT_DIR / f'right_{i}.png')
        rights.append(fr)
        fr.transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(OUT_DIR / f'left_{i}.png')
    lefts = [r.transpose(Image.Transpose.FLIP_LEFT_RIGHT) for r in rights]
    G = 8
    cw, ch = CELL_W + G * 2, CELL_H + G * 2
    sheet = Image.new('RGBA', (cw * FRAMES, ch * 2), (0, 0, 0, 0))
    for i, fr in enumerate(rights):
        sheet.paste(fr, (i * cw + G, G), fr)
    for i, fr in enumerate(lefts):
        sheet.paste(fr, (i * cw + G, ch + G), fr)
    sheet.save(OUT_SHEET, 'WEBP', quality=90, method=6)
    print('wrote', OUT_SHEET, sheet.size, OUT_SHEET.stat().st_size)

    from PIL import ImageFont
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
        font2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    except Exception:
        font = font2 = None
    bg = (36, 32, 44, 255)
    prev = Image.new('RGBA', (cw * FRAMES + 40, ch * 2 + 80 + CELL_H * 2), bg)
    d = ImageDraw.Draw(prev)
    d.text((20, 10), "Gōda carry  —  row 0 walk right (4 frames)   row 1 walk left   —  arms over shoulders, feet drag", fill=(240, 230, 210, 255), font=font)
    prev.paste(sheet, (20, 40), sheet)
    zy = ch * 2 + 58
    d.text((20, zy - 20), "Frame 0 and 1  ×2 nearest", fill=(240, 230, 210, 255), font=font2)
    prev.paste(rights[0].resize((CELL_W * 2, CELL_H * 2), Image.Resampling.NEAREST), (20, zy))
    prev.paste(rights[1].resize((CELL_W * 2, CELL_H * 2), Image.Resampling.NEAREST), (40 + CELL_W * 2, zy))
    prev.convert('RGB').save(OUT_PREV, 'PNG')
    print('wrote', OUT_PREV, prev.size)

if __name__ == '__main__':
    main()
