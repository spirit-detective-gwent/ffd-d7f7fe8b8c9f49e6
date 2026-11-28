#!/usr/bin/env python3
"""v6566-handheld (GGD-93): hand-drawn art for the handheld side quest, in the same flat outlined style as the
classrooms (world/int_c1a.webp) and the nurse's hallway (world/int_hall.webp).
  world/int_staff.webp      Staff Room interior, 960x640 (1x, like the classrooms)
  world/int_hall_sdoor.webp hallway patch (2x): a Staff Room door where the first three lockers by the nurse stood
  world/hh_boy.webp         the Kitsune BOY handheld lying on the confiscation box (2x, 56x40 world px)
  portraits/glitch_neutral.webp  Glitch Kono, hood up, face lit by his own handheld (360x480, like the other portraits)
Run from the repo root: python3 tools/hh/paint_staff.py"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random
ROOT = __import__('pathlib').Path(__file__).resolve().parent.parent.parent
INK = (34, 32, 42); WALL = (239, 230, 210); FRAME = (44, 39, 52); WAIN = (155, 150, 138)
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FJ = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
S = 3  # supersample

def font(px, jp=False): return ImageFont.truetype(FJ if jp else FB, int(px * S))
class P:
    def __init__(s, w, h, bg=(0, 0, 0, 0)):
        s.w, s.h = w, h; s.im = Image.new('RGBA', (w * S, h * S), bg); s.d = ImageDraw.Draw(s.im)
    def k(s, v): return [int(round(a * S)) for a in v]
    def rect(s, x0, y0, x1, y1, fill, lw=3, ol=INK, r=0):
        b = s.k([x0, y0, x1, y1])
        if r: s.d.rounded_rectangle(b, radius=int(r * S), fill=fill, outline=ol if lw else None, width=int(lw * S) if lw else 0)
        else: s.d.rectangle(b, fill=fill, outline=ol if lw else None, width=int(lw * S) if lw else 0)
    def line(s, pts, col=INK, lw=3): s.d.line(s.k(pts), fill=col, width=int(lw * S), joint='curve')
    def ell(s, x0, y0, x1, y1, fill, lw=3, ol=INK): s.d.ellipse(s.k([x0, y0, x1, y1]), fill=fill, outline=ol if lw else None, width=int(lw * S) if lw else 0)
    def poly(s, pts, fill, lw=3, ol=INK):
        s.d.polygon(s.k(pts), fill=fill)
        if lw: s.d.line(s.k(pts + pts[:2]), fill=ol, width=int(lw * S), joint='curve')
    def text(s, x, y, t, px, col=INK, anchor='mm', jp=False): s.d.text((x * S, y * S), t, font=font(px, jp), fill=col, anchor=anchor)
    def out(s): return s.im.resize((s.w, s.h), Image.LANCZOS)

def desk(p, x, y, w=92, h=58, top=(176, 132, 92), papers=True, rnd=None):
    """one teacher's desk seen from the front-top, like the classroom desks but bigger, with drawers"""
    p.rect(x + 6, y + h - 2, x + w + 6, y + h + 8, (120, 104, 88, 120), 0)  # shadow
    p.rect(x, y, x + w, y + h * 0.55, top)            # top
    p.rect(x, y + h * 0.55, x + w, y + h, (130, 96, 64))  # front
    p.rect(x + w - 30, y + h * 0.6, x + w - 6, y + h * 0.95, (150, 112, 76), 2)
    p.line([x + w - 22, y + h * 0.78, x + w - 14, y + h * 0.78], INK, 2)
    if papers and rnd:
        for i in range(rnd.randint(1, 3)):
            px0 = x + 8 + rnd.randint(0, int(w * 0.45)); py0 = y + 4 + rnd.randint(0, 6)
            p.rect(px0, py0, px0 + 22, py0 + 16, (248, 246, 238), 2)
            p.line([px0 + 4, py0 + 6, px0 + 18, py0 + 6], (150, 150, 160), 1.5); p.line([px0 + 4, py0 + 10, px0 + 15, py0 + 10], (150, 150, 160), 1.5)

def chair(p, x, y, col=(70, 84, 104)):
    p.rect(x, y, x + 34, y + 12, col, 2.5, r=4); p.rect(x + 4, y + 12, x + 30, y + 26, (56, 66, 82), 2.5, r=3)

def staff_room():
    rnd = random.Random(93)
    p = P(960, 640, FRAME + (255,))
    # side walls (like the classroom frame)
    p.rect(12, 0, 948, 640, (160, 156, 144), 3)
    p.rect(60, 18, 900, 580, WALL, 3)
    # floor: blue-gray linoleum tiles (the classrooms are wood; teachers get the tiled room)
    p.rect(70, 168, 890, 575, (196, 204, 200), 0)
    for gx in range(70, 890, 48): p.line([gx, 168, gx, 575], (178, 188, 184), 1.5)
    for gy in range(168, 575, 48): p.line([70, gy, 890, gy], (178, 188, 184), 1.5)
    for i in range(26):
        tx = 70 + 48 * rnd.randint(0, 16); ty = 168 + 48 * rnd.randint(0, 8)
        p.rect(tx + 1, ty + 1, min(tx + 47, 889), min(ty + 47, 574), (186, 196, 192), 0)
    # sun patches from the windows, soft
    for x0 in (120, 690):
        p.poly([x0, 168, x0 + 150, 168, x0 + 210, 560, x0 + 60, 560], (230, 236, 226, 70), 0)
    # wall band + skirting
    p.rect(60, 152, 900, 170, (62, 104, 92), 0); p.line([60, 152, 900, 152], INK, 3); p.line([60, 170, 900, 170], INK, 3)
    # sign plate over the board, like "1-A"
    p.text(440, 30, '\u8077\u54e1\u5ba4', 15, (84, 78, 90), jp=True); p.text(518, 30, 'STAFF ROOM', 13, (84, 78, 90))
    # windows
    for x0 in (90, 700):
        p.rect(x0, 46, x0 + 170, 132, (246, 240, 228), 3)
        p.rect(x0 + 8, 52, x0 + 162, 126, (206, 228, 200), 3)
        p.rect(x0 + 8, 90, x0 + 162, 126, (178, 212, 200), 0); p.rect(x0 + 8, 52, x0 + 162, 126, None, 3)
        p.line([x0 + 60, 52, x0 + 60, 126], (246, 240, 228), 4); p.line([x0 + 110, 52, x0 + 110, 126], (246, 240, 228), 4)
        p.line([x0 + 8, 90, x0 + 162, 90], (246, 240, 228), 4)
        p.rect(x0 - 4, 132, x0 + 174, 140, (246, 240, 228), 2.5)
    # duty roster whiteboard (the "chalk" spot)
    p.rect(320, 40, 640, 146, (122, 98, 74), 3)
    p.rect(330, 48, 630, 138, (246, 248, 244), 3)
    for i, w in enumerate((170, 120, 200, 90)):
        p.line([346, 66 + i * 18, 346 + w, 66 + i * 18], (70, 110, 170), 2.5)
    for c in range(5): p.line([470 + c * 30, 60, 470 + c * 30, 128], (200, 200, 206), 1.5)
    p.rect(560, 58, 598, 82, (255, 230, 120), 2); p.rect(600, 92, 624, 112, (255, 190, 200), 2)
    p.rect(340, 138, 380, 144, (220, 80, 80), 1.5); p.rect(386, 138, 420, 144, (60, 110, 200), 1.5)
    # clock
    p.ell(282, 56, 314, 88, (250, 250, 246), 3); p.line([298, 72, 298, 61], INK, 2.5); p.line([298, 72, 306, 76], INK, 2.5)
    # filing cabinets (left), "cab"
    for i in range(2):
        x0 = 96 + i * 56
        p.rect(x0 + 4, 248, x0 + 54, 256, (120, 120, 120, 90), 0)
        p.rect(x0, 176, x0 + 50, 250, (186, 192, 198), 3)
        for j in range(3):
            p.rect(x0 + 5, 182 + j * 22, x0 + 45, 200 + j * 22, (204, 210, 214), 2)
            p.line([x0 + 18, 191 + j * 22, x0 + 32, 191 + j * 22], INK, 2.5)
    # tea counter with kettle and mugs (right), "kettle"
    p.rect(740, 182, 878, 252, (150, 112, 76), 3); p.rect(736, 174, 882, 190, (196, 158, 116), 3)
    p.rect(752, 196, 800, 244, (130, 96, 64), 2); p.rect(810, 196, 866, 244, (130, 96, 64), 2)
    p.ell(752, 140, 794, 178, (226, 228, 232), 3); p.rect(764, 132, 782, 144, (60, 60, 70), 2.5)  # kettle
    p.line([792, 152, 806, 146], INK, 3)
    for i, c in enumerate(((230, 90, 80), (90, 140, 210), (240, 220, 120))):
        x0 = 816 + i * 20; p.rect(x0, 158, x0 + 14, 176, c, 2.5)
    # two desk islands (four desks each, pushed together)
    for ix in (210, 520):
        for r in range(2):
            for c in range(2):
                x0 = ix + c * 104; y0 = 286 + r * 70
                if r == 0: chair(p, x0 + 30, y0 - 22)
                desk(p, x0, y0, 100, 56, rnd=rnd)
                if r == 1: chair(p, x0 + 30, y0 + 58)
        # monitor + mug on the islands
        p.rect(ix + 54, 268, ix + 92, 296, (60, 66, 80), 2.5); p.rect(ix + 58, 272, ix + 88, 292, (140, 190, 210), 0); p.rect(ix + 68, 296, ix + 78, 302, (60, 66, 80), 2)
        p.rect(ix + 150, 350, ix + 164, 366, (240, 240, 236), 2.5)
    # the confiscation box on the front-right desk of the right island (the handheld lies on it: world/hh_boy.webp)
    bx, by = 646, 350
    p.rect(bx, by, bx + 52, by + 24, (206, 170, 118), 2.5); p.poly([bx, by, bx + 10, by - 8, bx + 62, by - 8, bx + 52, by], (226, 194, 140), 2.5)
    p.line([bx + 52, by, bx + 62, by - 8], INK, 2.5); p.rect(bx + 52, by, bx + 62, by + 16, (186, 150, 100), 0); p.line([bx + 62, by - 8, bx + 62, by + 16, bx + 52, by + 24], INK, 2.5)
    p.rect(bx + 6, by + 8, bx + 46, by + 18, (248, 244, 232), 1.5); p.text(bx + 26, by + 13, '\u6ca1\u53ce', 8, (180, 40, 40), jp=True)
    # sofa + low table (bottom-left, where teachers nap)
    p.rect(104, 470, 290, 498, (88, 112, 150), 3, r=8); p.rect(96, 492, 298, 534, (100, 126, 166), 3, r=8)
    p.rect(96, 482, 116, 538, (82, 104, 140), 3, r=6); p.rect(278, 482, 298, 538, (82, 104, 140), 3, r=6)
    p.rect(130, 548, 262, 566, (150, 112, 76), 2.5, r=4)
    p.rect(150, 544, 176, 552, (240, 240, 236), 2)
    # copier (bottom-right)
    p.rect(752, 464, 852, 548, (222, 222, 226), 3, r=4); p.rect(758, 452, 846, 470, (196, 198, 204), 3, r=3)
    p.rect(800, 478, 840, 492, (90, 150, 110), 2); p.rect(764, 500, 846, 540, (206, 208, 212), 2)
    # plant
    p.rect(862, 540, 890, 566, (196, 92, 60), 2.5)
    for (cx, cy) in ((868, 520), (884, 526), (876, 508), (862, 532), (888, 538)): p.ell(cx - 14, cy - 10, cx + 14, cy + 10, (96, 168, 96), 2.5)
    # bottom wall with the doorway (same as the classrooms)
    p.rect(12, 575, 948, 640, (168, 164, 150), 3)
    p.rect(12, 575, 948, 590, (226, 220, 204), 3)
    p.rect(432, 568, 528, 640, (222, 216, 200), 0)
    p.rect(420, 568, 436, 640, (190, 186, 176), 3); p.rect(524, 568, 540, 640, (190, 186, 176), 3)
    return p.out()

def hall_patch():
    """2x patch for world/int_hall.webp at x 3188..3540, y 96..472: the Training door's twin, re-lettered STAFF ROOM, then two lockers"""
    H = Image.open(ROOT / 'world/int_hall.webp').convert('RGBA')
    X0, Y0, X1, Y1 = 3188, 96, 3540, 472
    patch = H.crop((X0, Y0, X1, Y1)).copy()
    # 1. wall + baseboard background across the old first three lockers (sampled from bare wall at x=3190)
    col = H.crop((3190, Y0, 3191, Y1)).copy()
    wall = H.getpixel((3190, 90))
    for y in range(0, 252 - Y0): col.putpixel((0, y), wall)  # the bulletin board ends here; above it is bare wall
    for x in range(0, 3398 - X0): patch.paste(col, (x, 0))
    # 2. the door (frame included) from the Training room door
    door = H.crop((2796, 145, 2999, 466)); patch.paste(door, (3192 - X0, 145 - Y0))
    # 3. the name plate, re-lettered
    plate = H.crop((2784, 102, 3012, 146)); patch.paste(plate, (3182 - X0 + 6, 102 - Y0))
    d = ImageDraw.Draw(patch)
    px0, py0 = 3182 - X0 + 6, 102 - Y0
    d.rectangle([px0 + 8, py0 + 7, px0 + 228 - 9, py0 + 44 - 8], fill=(243, 241, 237))
    d.text((px0 + 114, py0 + 23), 'Staff Room', font=ImageFont.truetype(FB, 25), fill=(28, 26, 34), anchor='mm')
    # 4. the locker bank now starts at the old divider: copy its left frame there
    edge = H.crop((3204, 140, 3216, 456)); patch.paste(edge, (3394 - X0, 140 - Y0))
    cap = H.crop((3204, 140, 3300, 172)); patch.paste(cap.crop((0, 0, 12, 32)), (3394 - X0, 140 - Y0))
    return patch

def hh_item():
    """the Kitsune BOY lying on the box: cream body, green screen, red A / B (2x)"""
    p = P(56, 40)
    p.poly([6, 30, 14, 6, 44, 4, 50, 28], (0, 0, 0, 60), 0)
    p.poly([4, 26, 12, 2, 42, 0, 48, 24], (234, 228, 212), 2.5)
    p.poly([12, 8, 16, 2.5, 34, 1.5, 32, 10], (74, 82, 98), 1.5)
    p.poly([14.5, 7.5, 17.5, 3.5, 32, 2.8, 30.5, 9], (155, 188, 15), 0)
    p.ell(30, 12, 36, 17, (163, 50, 74), 1.5); p.ell(37, 14, 43, 19, (163, 50, 74), 1.5)
    p.line([14, 14, 22, 15], (27, 42, 60), 2.5); p.line([18, 11, 18, 18], (27, 42, 60), 2.5)
    big = P(56, 40); big.im = p.im
    im = p.out().resize((112, 80), Image.LANCZOS)
    return im

def glitch_portrait():
    """Glitch Kono: repainted from the painted student portrait (portraits/student_neutral.webp, same framing and brushwork):
    hair dyed black, a charcoal hoodie with the hood up over the spikes and the bare chest, round lenses glowing with his
    handheld, green under-light, and the purple aura turned Black Comet green. 360x480, like every portrait."""
    import numpy as np
    src = Image.open(ROOT / 'portraits/student_neutral.webp').convert('RGB')
    a = np.asarray(src).astype(np.float32) / 255.0
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(-1); mn = a.min(-1); sat = (mx - mn) / (mx + 1e-4); lum = 0.3 * r + 0.59 * g + 0.11 * b
    H0, W0 = a.shape[:2]; yy, xx = np.mgrid[0:H0, 0:W0]
    # 1. blond -> black hair (yellow, saturated, upper half)
    hair = (r > 0.35) & (g > 0.28) & (b < g * 0.72) & (sat > 0.32) & (yy < 300) & ~((yy > 150) & (yy < 260) & (xx > 120) & (xx < 280) & (r > g * 1.18))
    k = lum[hair]; a[hair] = np.stack([0.06 + k * 0.16, 0.07 + k * 0.2, 0.08 + k * 0.17], -1)
    # 2. purple aura -> green
    pur = (b > g * 1.15) & (r > g * 1.02) & (sat > 0.25)
    k = lum[pur] * 1.15; a[pur] = np.stack([k * 0.42, np.minimum(1, k * 1.05), k * 0.38], -1)
    img = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert('RGBA')
    big = img.resize((W0 * S, H0 * S), Image.LANCZOS)
    # 3. hoodie + hood (outer shape minus the face opening), painted fabric with soft edges
    m = Image.new('L', big.size, 0); md = ImageDraw.Draw(m)
    md.ellipse([50 * S, -34 * S, 340 * S, 330 * S], fill=255)
    md.polygon([v * S for v in [0, 480, 0, 280, 40, 262, 120, 262, 270, 262, 350, 262, 360, 280, 360, 480]], fill=255)
    md.ellipse([116 * S, 98 * S, 280 * S, 296 * S], fill=0)
    md.polygon([v * S for v in [168, 272, 226, 272, 214, 318, 197, 336, 180, 318]], fill=0)  # neck
    m = m.filter(ImageFilter.GaussianBlur(2.0 * S))
    fab = Image.new('RGBA', big.size, (0, 0, 0, 255)); fd = ImageDraw.Draw(fab)
    for rr0 in range(0, 420, 4):  # light from the upper left, like the other portraits
        t = rr0 / 420.0; c = (int(70 - 48 * t), int(72 - 48 * t), int(82 - 54 * t), 255)
        fd.ellipse([(110 - rr0) * S, (40 - rr0) * S, (110 + rr0) * S, (40 + rr0) * S], outline=c, width=5 * S)
    for pts in ([70, 250, 96, 150, 150, 70], [318, 250, 300, 150, 246, 70], [36, 470, 70, 380, 130, 320], [326, 470, 300, 380, 262, 320], [150, 480, 172, 392], [248, 480, 226, 392]):
        fd.line([v * S for v in pts], fill=(18, 19, 24, 255), width=8 * S, joint='curve')
        fd.line([(v + 5) * S for v in pts], fill=(78, 80, 92, 255), width=2 * S, joint='curve')
    fab = fab.filter(ImageFilter.GaussianBlur(2.2 * S))
    big.paste(fab, (0, 0), m)
    # the inside of the hood: a dark lining band around the opening
    ln = Image.new('RGBA', big.size, (0, 0, 0, 0)); ldd = ImageDraw.Draw(ln)
    ldd.ellipse([112 * S, 94 * S, 284 * S, 300 * S], outline=(10, 10, 14, 230), width=12 * S)
    big.alpha_composite(ln.filter(ImageFilter.GaussianBlur(4 * S)))
    d = ImageDraw.Draw(big)
    # rim light on the hood opening + the green seam and drawstrings
    d.arc([114 * S, 96 * S, 282 * S, 298 * S], 200, 340, fill=(120, 220, 90, 110), width=2 * S)
    d.line([(194 * S, -4 * S), (197 * S, 96 * S)], fill=(110, 220, 76, 255), width=5 * S)
    for x0, x1 in ((178, 168), (216, 226)):
        d.line([(x0 * S, 300 * S), (x1 * S, 420 * S)], fill=(120, 230, 80, 255), width=4 * S)
        d.ellipse([(x1 - 6) * S, 416 * S, (x1 + 6) * S, 428 * S], fill=(160, 245, 120, 255))
    # 4. shadow of the hood across the brow, lenses lit by the screen, under-light on the chin
    sh = Image.new('RGBA', big.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.ellipse([96 * S, 70 * S, 294 * S, 176 * S], fill=(8, 8, 12, 170))
    big.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14 * S)))
    gl = Image.new('RGBA', big.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
    gd.ellipse([126 * S, 152 * S, 200 * S, 192 * S], fill=(130, 240, 80, 150)); gd.ellipse([214 * S, 160 * S, 270 * S, 198 * S], fill=(130, 240, 80, 150))
    big.alpha_composite(gl.filter(ImageFilter.GaussianBlur(3 * S)))
    gd2 = ImageDraw.Draw(big)
    for (x, y) in ((142, 162), (226, 170)): gd2.rectangle([x * S, y * S, (x + 9) * S, (y + 5) * S], fill=(225, 255, 210, 230))
    ul = Image.new('RGBA', big.size, (0, 0, 0, 0)); ud = ImageDraw.Draw(ul)
    ud.ellipse([130 * S, 220 * S, 262 * S, 330 * S], fill=(120, 230, 80, 70))
    big.alpha_composite(ul.filter(ImageFilter.GaussianBlur(18 * S)))
    return big.resize((W0, H0), Image.LANCZOS).convert('RGB')

if __name__ == '__main__':
    staff_room().convert('RGB').save(ROOT / 'world/int_staff.webp', quality=90, method=6)
    hp = hall_patch().convert('RGBA'); px = hp.load()
    for x in range(3384 - 3188, 3394 - 3188):  # the cork-board edge copied with the Training door: the frame's grey runs all the way up
        ref = px[x, 300 - 96]
        for y in range(120 - 96, 300 - 96):
            if px[x, y][0] > px[x, y][2] + 30: px[x, y] = ref
    hp.save(ROOT / 'world/int_hall_sdoor.webp', quality=92, method=6)
    hh_item().save(ROOT / 'world/hh_boy.webp', quality=95, method=6)
    glitch_portrait().save(ROOT / 'portraits/glitch_neutral.webp', quality=88, method=6)
    print('painted')
