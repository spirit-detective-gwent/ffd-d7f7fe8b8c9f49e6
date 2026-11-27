#!/usr/bin/env python3
"""v6566-baseexp (Erik t546/t548): paint the 8 new Cafeteria / Storehouse rooms and add the new doors to the existing rooms.
Handmade, code-drawn in the same flat cel style as the v4.40 / v4.47 rooms (dark outline, flat fills, 3/4 front faces, soft
drop shadows). Walls / baseboards / bottom wall come from the existing room art of the same base (cleaned of props); floors,
furniture, doors and plaques are drawn here. Output: world/cf_*.webp, world/sf_*.webp (+ patched wkitbg PNGs for the
existing rooms with a baked wall kit, which build_embed.py writes back into index.html).
usage: paint_rooms.py <worktree> [--only name] [--overlay DIR]   (overlay: draw block rects + guard cones for review)"""
import sys, json, math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
WT = Path(sys.argv[1]); args = sys.argv[2:]
ONLY = args[args.index('--only') + 1] if '--only' in args else None
OVL = args[args.index('--overlay') + 1] if '--overlay' in args else None
WORLD = WT / 'world'; WORK = Path('/workspace/baseexp/work')
SPEC = json.loads((WT / 'tools/baseexp/rooms.json').read_text())
OUT = (30, 24, 36, 255)
K = 2  # supersample
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def load(n):
    p = WORLD / (n + '.webp')
    return Image.open(p).convert('RGB')

# ---------------- template cleaning ----------------
def clean_col(im, y0, y1, xs):
    """pick the column whose top band matches its neighbours best (no props)"""
    best = None
    for x in xs:
        d = 0
        for y in range(y0, y1, 2):
            a = im.getpixel((x, y)); b = im.getpixel((x + 18, y)); c = im.getpixel((x - 18, y))
            d += sum(abs(p - q) for p, q in zip(a, b)) + sum(abs(p - q) for p, q in zip(a, c))
        if best is None or d < best[1]: best = (x, d)
    return best[0]

def template(spec):
    t = spec['tpl']; im = load(t)
    W, H = im.size; out = im.copy(); px = out.load(); src = im.load()
    top = spec.get('wall_h', 152)
    cx = clean_col(im, 0, top, range(130, W - 130, 6))
    for y in range(0, top + 6):
        c = src[cx, y]
        for x in range(96, W - 96): px[x, y] = c
    ry = spec.get('side_row', 770)
    for y in range(top + 6, 786):
        for x in range(0, 100): px[x, y] = src[x, ry]
        for x in range(W - 100, W): px[x, y] = src[x, ry]
    if spec.get('bottom'):
        b = load(spec['bottom']).load()
        for y in range(780, H):
            for x in range(0, W): px[x, y] = b[x, y]
    # side columns of the top band (corner frames) keep the template's clean row too
    for y in range(0, top + 6):
        for x in list(range(0, 96)) + list(range(W - 96, W)): px[x, y] = src[x, min(H - 1, max(0, y))]
    return out

# ---------------- floors ----------------
def floor_tile(out, box, base, line, period=40, seed=1, dark=None):
    rnd = random.Random(seed); px = out.load(); x0, y0, x1, y1 = box
    darks = set()
    for i in range(40): darks.add((rnd.randrange(0, 40), rnd.randrange(0, 30)))
    dk = dark or tuple(max(0, c - 5) for c in base)
    for y in range(y0, y1):
        for x in range(x0, x1):
            gx, gy = (x - 4) % period, (y - 4) % period
            if gx == 0 or gy == 0: px[x, y] = line
            elif ((x - 4) // period, (y - 4) // period) in darks: px[x, y] = dk
            else: px[x, y] = base

def floor_wood(out, box, cols, joint, seed=2, plank=34):
    rnd = random.Random(seed); px = out.load(); x0, y0, x1, y1 = box
    x = x0 - rnd.randrange(0, plank)
    while x < x1:
        y = y0 - rnd.randrange(0, 200)
        while y < y1:
            L = rnd.randrange(150, 420); col = rnd.choice(cols)
            for yy in range(max(y0, y), min(y1, y + L)):
                for xx in range(max(x0, x), min(x1, x + plank)):
                    px[xx, yy] = joint if (xx == x or yy == y) else col
            y += L
        x += plank

def floor_concrete(out, box, base, line, seed=3):
    rnd = random.Random(seed); px = out.load(); x0, y0, x1, y1 = box
    for y in range(y0, y1):
        for x in range(x0, x1):
            px[x, y] = line if ((x - 10) % 160 == 0 or (y - 10) % 160 == 0) else base
    d = ImageDraw.Draw(out)
    for i in range(70):
        cx, cy = rnd.randrange(x0, x1), rnd.randrange(y0, y1); r = rnd.randrange(1, 3)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=tuple(max(0, c - 10) for c in base))

# ---------------- 2x overlay drawing ----------------
class Ov:
    def __init__(self, size):
        self.im = Image.new('RGBA', (size[0] * K, size[1] * K), (0, 0, 0, 0)); self.d = ImageDraw.Draw(self.im)
    def S(self, v): return [c * K for c in v]
    def rr(self, r, fill, rad=4, ow=2.5, outline=OUT):
        self.d.rounded_rectangle(self.S(r), radius=rad * K, fill=fill, outline=outline if ow else None, width=int(ow * K) if ow else 0)
    def shadow(self, r, dx=7, dy=8, a=40, rad=6):
        self.d.rounded_rectangle(self.S([r[0] + dx, r[1] + dy, r[2] + dx, r[3] + dy]), radius=rad * K, fill=(20, 16, 30, a))
    def box(self, r, top, front, fh=18, rad=4, shadow=True):
        x1, y1, x2, y2 = r
        if shadow: self.shadow(r)
        self.rr([x1, y1, x2, y2], front, rad)
        self.rr([x1, y1, x2, y2 - fh], top, rad)
    def circ(self, c, rad, fill, ow=2, outline=OUT):
        self.d.ellipse(self.S([c[0] - rad, c[1] - rad, c[0] + rad, c[1] + rad]), fill=fill, outline=outline if ow else None, width=int(ow * K) if ow else 0)
    def ell(self, r, fill, ow=0, outline=OUT):
        self.d.ellipse(self.S(r), fill=fill, outline=outline if ow else None, width=int(ow * K) if ow else 0)
    def line(self, pts, col, w=2):
        self.d.line([(p[0] * K, p[1] * K) for p in pts], fill=col, width=int(w * K))
    def poly(self, pts, fill, ow=2.5, outline=OUT):
        self.d.polygon([(p[0] * K, p[1] * K) for p in pts], fill=fill, outline=None)
        if ow: self.d.line([(p[0] * K, p[1] * K) for p in pts + [pts[0]]], fill=outline, width=int(ow * K), joint='curve')
    def text(self, xy, s, size, col=OUT, anchor='mm'):
        f = ImageFont.truetype(FONT, int(size * K)); self.d.text((xy[0] * K, xy[1] * K), s, font=f, fill=col, anchor=anchor)
    def put(self, out):
        sm = self.im.resize((out.size[0], out.size[1]), Image.LANCZOS)
        base = out.convert('RGBA'); base.alpha_composite(sm); return base.convert('RGB')

# ---------------- doors (measured from cf_line / sf_lockers) ----------------
BROWN = (155, 108, 72, 255); BROWN_HI = (166, 125, 86, 255); FRAME = (118, 113, 106, 255); WIN = (229, 222, 200, 255); KNOB = (214, 208, 186, 255)
def door_west(o, flip=False, W=1152):
    def X(x): return (W - x) if flip else x
    def P(pts): return [(X(x), y) for x, y in pts]
    o.shadow([X(116) if not flip else X(118), 336, X(124) if not flip else X(110), 560], dx=0, dy=0, a=0)
    fr = [81, 323, 90, 560]
    o.rr([min(X(fr[0]), X(fr[2])), fr[1], max(X(fr[0]), X(fr[2])), fr[3]], FRAME, 1, 2)
    o.poly(P([(88, 330), (116, 338), (116, 555), (88, 558)]), BROWN, 2.2)
    xs = sorted([X(96), X(111)]); o.rr([xs[0], 352, xs[1], 420], WIN, 1, 2)
    o.circ((X(108), 451), 3.4, KNOB, 1.6)

def door_north(o, label=None, x0=499, x1=646):
    o.rr([x0, 25, x1, 152], FRAME, 1, 2.2)
    o.rr([x0 + 7, 36, x1 - 7, 150], BROWN, 1, 2.2)
    o.rr([x0 + 11, 40, x0 + 18, 146], BROWN_HI, 0, 0)
    cx = (x0 + x1) / 2
    o.rr([cx - 31, 47, cx + 31, 79], (210, 228, 247, 255), 1, 2)
    o.circ((x1 - 21, 101), 3.6, KNOB, 1.6)
    if label:
        f = ImageFont.truetype(FONT, int(13 * K)); w = f.getlength(label) / K
        o.rr([cx - w / 2 - 9, 3, cx + w / 2 + 9, 24], (246, 244, 236, 255), 2, 2)
        o.text((cx, 14), label, 13)

def gap_south(out):
    """paste the gS threshold + posts from sf_lockers (only the pixels that differ from its floor)"""
    L = load('sf_lockers'); lp = L.load(); px = out.load()
    for y in range(780, 864):
        for x in range(425, 726):
            c = lp[x, y]
            if y < 789 and (abs(c[0] - 185) + abs(c[1] - 191) + abs(c[2] - 198) < 24 or abs(c[0] - 178) + abs(c[1] - 184) + abs(c[2] - 190) < 14): continue
            px[x, y] = c

def kit_patch(out, x):
    """the closed wall first-aid kit, as baked in wkitbg_cf_kitchen (kit centre x=125), moved to centre x"""
    a = Image.open(WORK / 'wkitbg_cf_kitchen.png').convert('RGB'); b = load('cf_kitchen')
    ap, bp, px = a.load(), b.load(), out.load()
    for yy in range(78, 150):
        for xx in range(80, 175):
            ca, cb = ap[xx, yy], bp[xx, yy]
            if sum(abs(p - q) for p, q in zip(ca, cb)) > 18:
                tx = xx - 125 + x
                if 0 <= tx < out.size[0]: px[tx, yy] = ca

# ---------------- props ----------------
def P_rack(o, r, boxes=True, seed=0, top=(198, 205, 213, 255), front=(146, 155, 166, 255)):
    o.box(r, top, front, fh=16)
    rnd = random.Random(seed); x = r[0] + 10
    if boxes:
        while x < r[2] - 40:
            w = rnd.randrange(34, 62); h = (r[3] - r[1]) - 30
            col = rnd.choice([(201, 160, 104, 255), (190, 148, 94, 255), (220, 230, 236, 255), (180, 205, 160, 255)])
            o.rr([x, r[1] + 6, min(x + w, r[2] - 10), r[1] + 6 + max(12, h)], col, 2, 1.8)
            x += w + rnd.randrange(6, 14)
    for yy in [r[3] - 16 + 5, r[3] - 16 + 11]: o.line([(r[0] + 6, yy), (r[2] - 6, yy)], (110, 118, 130, 255), 1.4)

def P_crates(o, r, col=(184, 134, 84, 255), front=(150, 106, 64, 255)):
    o.box(r, col, front, fh=14)
    x = r[0] + 8
    while x < r[2] - 8:
        o.line([(x, r[1] + 6), (x, r[3] - 20)], (140, 98, 58, 255), 1.4); x += 16

def P_van(o, r):
    x1, y1, x2, y2 = r; o.shadow(r, 9, 10, 46, 14)
    o.rr([x1, y1, x2, y2], (232, 234, 238, 255), 14)
    o.rr([x1 + 10, y2 - 30, x2 - 10, y2 - 4], (196, 200, 208, 255), 8, 2)
    o.rr([x1 + 6, (y1 + y2) / 2 - 14, x2 - 6, (y1 + y2) / 2 + 2], (150, 92, 196, 255), 3, 2)
    o.rr([x2 - 70, y1 + 12, x2 - 14, y2 - 44], (150, 196, 226, 255), 6, 2)
    for wx in [x1 + 40, x2 - 54]:
        o.rr([wx, y2 - 8, wx + 34, y2 + 6], (40, 36, 46, 255), 5, 2)
    o.circ((x1 + 60, y1 + 30), 14, (232, 195, 90, 255), 2); o.text((x1 + 60, y1 + 31), 'M', 14)

def P_pallet(o, r, seed=0):
    o.box(r, (173, 128, 82, 255), (140, 100, 60, 255), fh=12)
    rnd = random.Random(seed); x = r[0] + 6
    while x < r[2] - 20:
        w = rnd.randrange(26, 44); col = rnd.choice([(201, 160, 104, 255), (190, 148, 94, 255), (210, 172, 118, 255)])
        o.rr([x, r[1] + 4, min(r[2] - 6, x + w), r[3] - 18], col, 2, 1.8)
        o.line([(x + 4, r[1] + 14), (min(r[2] - 6, x + w) - 4, r[1] + 14)], (150, 112, 66, 255), 1.2); x += w + 4

def P_counter(o, r, top=(205, 210, 216, 255), front=(150, 158, 168, 255), items=None):
    o.box(r, top, front, fh=16)
    for it in (items or []):
        kind, cx, cy = it
        if kind == 'bread': o.ell([cx - 9, cy - 6, cx + 9, cy + 6], (232, 195, 90, 255), 1.6)
        if kind == 'pbread': o.ell([cx - 9, cy - 6, cx + 9, cy + 6], (186, 132, 214, 255), 1.6)
        if kind == 'tray': o.rr([cx - 16, cy - 9, cx + 16, cy + 9], (96, 160, 200, 255), 2, 1.6)
        if kind == 'bowl': o.circ((cx, cy), 8, (240, 240, 236, 255), 1.6)
        if kind == 'tape': o.circ((cx, cy), 7, (236, 236, 228, 255), 1.6); o.circ((cx, cy), 3, (180, 180, 172, 255), 1)

def P_trays(o, r, col=(96, 160, 200, 255)):
    o.shadow(r); n = max(2, int((r[3] - r[1]) / 10))
    for i in range(n):
        y = r[3] - 12 - i * 8
        o.rr([r[0], y - 10, r[2], y + 6], col if i % 2 == 0 else (86, 176, 128, 255), 3, 1.8)

def P_trayrack(o, r):
    o.box(r, (190, 197, 206, 255), (140, 148, 160, 255), fh=12)
    y = r[1] + 8
    while y < r[3] - 20:
        o.line([(r[0] + 5, y), (r[2] - 5, y)], (110, 118, 130, 255), 1.4)
        o.ell([r[0] + 8, y + 1, r[0] + 26, y + 9], (232, 195, 90, 255), 1.2); y += 14

def P_oven(o, r):
    o.box(r, (176, 182, 190, 255), (120, 126, 136, 255), fh=20)
    w = r[2] - r[0]; n = max(1, int(w / 90))
    for i in range(n):
        x1 = r[0] + 10 + i * (w - 20) / n; x2 = x1 + (w - 20) / n - 10
        o.rr([x1, r[1] + 10, x2, r[3] - 30], (46, 40, 52, 255), 3, 2)
        o.rr([x1 + 6, r[3] - 48, x2 - 6, r[3] - 36], (238, 150, 70, 255), 2, 0)
        o.circ((x1 + 8, r[3] - 24), 3, (220, 70, 70, 255), 1); o.circ((x1 + 20, r[3] - 24), 3, (220, 70, 70, 255), 1)

def P_sink(o, r):
    o.box(r, (205, 210, 216, 255), (150, 158, 168, 255), fh=16)
    o.rr([r[0] + 12, r[1] + 8, r[2] - 12, r[3] - 26], (150, 190, 214, 255), 4, 2)
    o.circ(((r[0] + r[2]) / 2, r[1] + 6), 4, (120, 126, 136, 255), 1.4)

def P_conveyor(o, r):
    o.box(r, (178, 184, 192, 255), (128, 134, 144, 255), fh=14)
    x = r[0] + 8
    while x < r[2] - 6:
        o.line([(x, r[1] + 4), (x, r[3] - 18)], (130, 136, 146, 255), 1.6); x += 12
    for cx in range(int(r[0] + 30), int(r[2] - 20), 70): o.rr([cx - 16, r[1] + 6, cx + 16, r[3] - 20], (96, 160, 200, 255), 2, 1.6)

def P_bench(o, r, col=(68, 120, 98, 255)):
    o.box(r, col, tuple(max(0, c - 30) for c in col[:3]) + (255,), fh=10)

def P_locker(o, r, n=6):
    o.box(r, (176, 182, 192, 255), (150, 156, 166, 255), fh=8)
    w = (r[2] - r[0]) / n
    for i in range(n):
        x1 = r[0] + i * w; o.rr([x1 + 3, r[1] + 4, x1 + w - 3, r[3] - 12], (214, 218, 226, 255), 1, 1.6)
        o.line([(x1 + w / 2, r[1] + 14), (x1 + w / 2, r[1] + 24)], (120, 126, 136, 255), 1.4)

def P_cage(o, r):
    x1, y1, x2, y2 = r; o.shadow(r, 5, 6, 30)
    o.rr(r, (150, 158, 168, 70), 2, 2.2)
    step = 14
    for k in range(int(x1) - int(y2 - y1), int(x2), step):
        o.line([(max(x1, k), y1 + max(0, x1 - k)), (min(x2, k + (y2 - y1)), min(y2, y1 + (x2 - k)))], (120, 128, 140, 200), 1.2)
        o.line([(max(x1, k), y2 - max(0, x1 - k)), (min(x2, k + (y2 - y1)), max(y1, y2 - (x2 - k)))], (120, 128, 140, 200), 1.2)
    o.rr(r, None, 2, 2.4)

def P_balls(o, r, seed=0):
    o.box(r, (170, 176, 186, 255), (130, 136, 146, 255), fh=12)
    rnd = random.Random(seed); x = r[0] + 14
    while x < r[2] - 12:
        col = rnd.choice([(232, 120, 60, 255), (240, 240, 236, 255), (220, 70, 70, 255), (232, 195, 90, 255)])
        o.circ((x, (r[1] + r[3] - 12) / 2), 10, col, 1.8); x += 24

def P_hurdles(o, r):
    o.shadow(r)
    for i, y in enumerate(range(int(r[1]), int(r[3]) - 8, 10)):
        o.rr([r[0], y, r[2], y + 7], (216, 50, 58, 255) if i % 2 == 0 else (240, 240, 236, 255), 2, 1.4)
    o.rr([r[0] + 4, r[1], r[0] + 10, r[3]], (232, 195, 90, 255), 1, 1.4); o.rr([r[2] - 10, r[1], r[2] - 4, r[3]], (232, 195, 90, 255), 1, 1.4)

def P_cart(o, r):
    o.box(r, (98, 110, 130, 255), (70, 80, 98, 255), fh=10)
    for cx in range(int(r[0] + 16), int(r[2] - 8), 22): o.circ((cx, r[1] + 16), 9, (232, 120, 60, 255), 1.6)

def P_stall(o, r):
    o.rr(r, (214, 228, 236, 255), 2, 2)
    o.rr([r[0] + 6, r[1] + 6, r[2] - 6, r[3] - 6], (190, 214, 228, 255), 2, 1.6)
    o.circ(((r[0] + r[2]) / 2, r[1] + 16), 6, (160, 170, 182, 255), 1.6)
    o.circ(((r[0] + r[2]) / 2, r[3] - 22), 4, (110, 120, 132, 255), 1.2)

def P_divider(o, r):
    o.rr(r, (160, 176, 190, 255), 1, 2)

def P_puddle(o, r):
    o.ell(r, (168, 205, 230, 150), 0)

def P_footprints(o, c, rx, ry, n=14):
    for i in range(n):
        a = i / n * math.pi * 2; x = c[0] + math.cos(a) * rx; y = c[1] + math.sin(a) * ry
        o.ell([x - 4, y - 6, x + 4, y + 6], (150, 120, 190, 110), 0)

def P_tub(o, r):
    o.shadow(r, 6, 7, 40, 18)
    o.rr(r, (184, 192, 202, 255), 18, 2.4)
    o.rr([r[0] + 12, r[1] + 12, r[2] - 12, r[3] - 14], (168, 214, 236, 255), 12, 2)
    for i in range(4): o.rr([r[0] + 24 + i * 22, r[1] + 22 + (i % 2) * 14, r[0] + 36 + i * 22, r[1] + 32 + (i % 2) * 14], (240, 248, 252, 255), 2, 1.2)

def P_table(o, r, top=(120, 72, 80, 255), front=(92, 52, 60, 255)):
    o.box(r, top, front, fh=14)

def P_desk(o, r):
    o.box(r, (98, 106, 122, 255), (70, 76, 90, 255), fh=18)
    for i, x in enumerate(range(int(r[0] + 20), int(r[2] - 14), 26)):
        o.circ((x, r[1] + 18), 5, [(220, 70, 70, 255), (90, 200, 120, 255), (232, 195, 90, 255)][i % 3], 1.4)
    o.rr([r[0] + 18, r[1] + 30, r[2] - 18, r[3] - 26], (36, 40, 52, 255), 2, 1.6)

def P_lapclock(o, r, txt='00:41.7'):
    o.rr(r, (30, 28, 38, 255), 3, 2.2)
    o.text(((r[0] + r[2]) / 2, (r[1] + r[3]) / 2 + 1), txt, (r[3] - r[1]) * 0.55, (230, 70, 70, 255))

def P_window(o, r):
    o.rr(r, (170, 205, 225, 255), 2, 2.4)
    o.rr([r[0] + 6, r[1] + (r[3] - r[1]) * 0.55, r[2] - 6, r[3] - 6], (110, 170, 90, 255), 1, 0)
    o.line([((r[0] + r[2]) / 2, r[1]), ((r[0] + r[2]) / 2, r[3])], OUT, 2)

def P_lever(o, x, y):
    o.rr([x - 18, y - 30, x + 18, y + 22], (98, 106, 122, 255), 3, 2.2)
    o.line([(x, y + 4), (x + 16, y - 34)], (60, 60, 70, 255), 4)
    o.circ((x + 16, y - 36), 8, (220, 60, 60, 255), 2)

def P_board(o, r, col=(46, 70, 60, 255), txt=None, tc=(230, 236, 220, 255), size=11):
    o.rr(r, col, 2, 2.2)
    if txt: o.text(((r[0] + r[2]) / 2, (r[1] + r[3]) / 2), txt, size, tc)

def P_rollup(o, r):
    o.rr(r, (178, 182, 190, 255), 2, 2.4)
    y = r[1] + 8
    while y < r[3] - 4: o.line([(r[0] + 4, y), (r[2] - 4, y)], (140, 146, 156, 255), 1.6); y += 9
    o.rr([r[0] - 6, r[3] - 6, r[2] + 6, r[3] + 2], (232, 195, 90, 255), 1, 1.6)

def P_stripes(o, r):
    x = r[0]
    while x < r[2]:
        o.poly([(x, r[3]), (x + 14, r[1]), (x + 28, r[1]), (x + 14, r[3])], (232, 195, 90, 255), 0); x += 28
    o.rr(r, None, 0, 2)

def P_sacks(o, r):
    o.shadow(r)
    for i, x in enumerate(range(int(r[0]), int(r[2]) - 30, 34)):
        o.rr([x, r[1] + (i % 2) * 6, x + 38, r[3] - (1 - i % 2) * 6], (236, 226, 204, 255), 10, 2)
        o.text((x + 19, (r[1] + r[3]) / 2), 'F', 11, (150, 120, 80, 255))

def P_plant(o, x, y):
    o.rr([x - 12, y - 6, x + 12, y + 14], (190, 100, 70, 255), 3, 2)
    for dx, dy in [(-10, -12), (8, -14), (0, -22), (-14, -2), (12, -2)]: o.circ((x + dx, y + dy), 10, (100, 170, 90, 255), 1.8)

PROPS = {'rack': P_rack, 'crates': P_crates, 'van': P_van, 'pallet': P_pallet, 'counter': P_counter, 'trays': P_trays, 'trayrack': P_trayrack,
         'oven': P_oven, 'sink': P_sink, 'conveyor': P_conveyor, 'bench': P_bench, 'locker': P_locker, 'cage': P_cage, 'balls': P_balls,
         'hurdles': P_hurdles, 'cart': P_cart, 'stall': P_stall, 'divider': P_divider, 'tub': P_tub, 'table': P_table, 'desk': P_desk,
         'sacks': P_sacks}

def paint(name, spec):
    out = template(spec); W, H = out.size
    fb = [96, spec.get('wall_h', 152) + 6, W - 96, 786]
    f = spec['floor']
    if f['k'] == 'tile': floor_tile(out, fb, tuple(f['base']), tuple(f['line']), f.get('p', 40), f.get('seed', 1))
    elif f['k'] == 'wood': floor_wood(out, fb, [tuple(c) for c in f['cols']], tuple(f['joint']), f.get('seed', 2))
    elif f['k'] == 'concrete': floor_concrete(out, fb, tuple(f['base']), tuple(f['line']))
    # floor edge shading under the back wall + inner wall trims (as the originals)
    d = ImageDraw.Draw(out)
    d.rectangle([fb[0], fb[1], fb[2], fb[1] + 3], fill=tuple(max(0, c - 18) for c in out.getpixel((300, fb[1] + 30))))
    if spec.get('wall_tint'):
        t = spec['wall_tint']; px = out.load(); src = load(spec['tpl']).load()
        bw = src[300, 70]
        for y in range(8, spec.get('wall_h', 152) - 18):
            for x in range(100, W - 100):
                c = px[x, y]
                if sum(abs(p - q) for p, q in zip(c, bw)) < 20: px[x, y] = tuple(t)
    if 'S' in spec['doors']: gap_south(out)
    if spec.get('kit_x'): kit_patch(out, spec['kit_x'])
    o = Ov(out.size)
    for dec in spec.get('wall', []):
        k = dec[0]
        if k == 'board': P_board(o, dec[1], txt=dec[2] if len(dec) > 2 else None, col=tuple(dec[3]) if len(dec) > 3 else (46, 70, 60, 255))
        if k == 'rollup': P_rollup(o, dec[1])
        if k == 'window': P_window(o, dec[1])
        if k == 'lapclock': P_lapclock(o, dec[1])
        if k == 'lever': P_lever(o, dec[1][0], dec[1][1])
        if k == 'cagewall': P_cage(o, dec[1])
        if k == 'stall': P_stall(o, dec[1])
        if k == 'divider': P_divider(o, dec[1])
    for dec in spec.get('floor_dec', []):
        k = dec[0]
        if k == 'puddle': P_puddle(o, dec[1])
        if k == 'stripes': P_stripes(o, dec[1])
        if k == 'prints': P_footprints(o, dec[1], dec[2], dec[3])
        if k == 'plant': P_plant(o, dec[1][0], dec[1][1])
        if k == 'mat': o.rr(dec[1], tuple(dec[2]), 4, 2)
    if 'W' in spec['doors']: door_west(o)
    if 'E' in spec['doors']: door_west(o, flip=True, W=W)
    if 'N' in spec['doors']: door_north(o, spec.get('n_label'))
    props = sorted(spec.get('props', []), key=lambda p: p[1][3])  # back to front
    for p in props:
        fn = PROPS[p[0]]; kw = p[2] if len(p) > 2 else {}
        kw = {k: (tuple(v) if isinstance(v, list) and v and isinstance(v[0], int) else v) for k, v in kw.items()}
        fn(o, p[1], **kw)
    out = o.put(out)
    return out

def overlay(im, spec, name):
    o = im.convert('RGBA'); d = ImageDraw.Draw(o, 'RGBA')
    for b in spec.get('blocks', []): d.rectangle(b, outline=(255, 0, 0, 255), width=2, fill=(255, 0, 0, 40))
    g = spec.get('guard')
    if g:
        for fa, col in [(g['fa'][0], (255, 200, 0, 60)), (g['fa'][1], (0, 160, 255, 60))]:
            a = g['a']; r = g['r']; x, y = g['at']
            d.pieslice([x - r, y - r, x + r, y + r], math.degrees(fa - math.radians(a)), math.degrees(fa + math.radians(a)), fill=col)
        d.ellipse([g['at'][0] - 8, g['at'][1] - 8, g['at'][0] + 8, g['at'][1] + 8], fill=(255, 0, 255, 255))
    if spec.get('crate'): c = spec['crate']; d.rectangle([c[0] - 30, c[1] - 24, c[0] + 30, c[1]], outline=(0, 255, 0, 255), width=3)
    if spec.get('hurdle'): c = spec['hurdle']; d.rectangle([c[0] - 28, c[1] - 20, c[0] + 28, c[1] + 6], outline=(0, 255, 0, 255), width=3)
    return o.convert('RGB')

if __name__ == '__main__':
    for name, spec in SPEC['rooms'].items():
        if ONLY and name != ONLY: continue
        im = paint(name, spec)
        im.save(WORLD / (name + '.webp'), 'WEBP', quality=88, method=6)
        im.save(WORK / (name + '.png'))
        if OVL:
            Path(OVL).mkdir(parents=True, exist_ok=True); overlay(im, spec, name).save(Path(OVL) / (name + '_ovl.png'))
        print('painted', name, im.size)

# ---------------- new doors on the existing rooms ----------------
EXIST = {  # room: [(door, opts)]
    'cf_kitchen': [('W', {}), ('N', {'label': 'DISH ROOM', 'x0': 690, 'x1': 837})],
    'cf_staff': [('N', {'label': 'BAKERY'})],
    'sf_bay': [('W', {})],
    'sf_lockers': [('W', {}), ('E', {})],
    'sf_coach': [('N', {'label': 'TRAINER'})],
    'sf_track': [('GATE_E', {})],
}
def track_gate(out):
    d = ImageDraw.Draw(out)
    y0, y1 = 392, 498
    d.rectangle([1216, y0, 1263, y1], fill=(138, 175, 106))
    for y in range(y0, y1, 40): d.line([(1216, y), (1263, y)], fill=(132, 168, 100))
    o = Ov(out.size)
    o.rr([1212, y0 - 12, 1266, y0], (183, 176, 163, 255), 1, 2)
    o.rr([1212, y1, 1266, y1 + 12], (183, 176, 163, 255), 1, 2)
    return o.put(out)

def patch_existing(im, room):
    o = Ov(im.size); gate = False
    for dr, opt in EXIST[room]:
        if dr == 'W': door_west(o)
        elif dr == 'E': door_west(o, flip=True, W=im.size[0])
        elif dr == 'N': door_north(o, opt.get('label'), opt.get('x0', 499), opt.get('x1', 646))
        elif dr == 'GATE_E': gate = True
    im = o.put(im)
    if gate: im = track_gate(im)
    return im

def run_existing():
    import shutil
    orig = WORK / 'orig'; orig.mkdir(exist_ok=True)
    for room in EXIST:
        src = orig / (room + '.webp')
        if not src.exists(): shutil.copy(WORLD / (room + '.webp'), src)
        im = Image.open(src).convert('RGB'); im = patch_existing(im, room)
        im.save(WORLD / (room + '.webp'), 'WEBP', quality=90, method=6); im.save(WORK / (room + '_doors.png'))
        bg = WORK / ('wkitbg_' + room + '.png')
        if bg.exists():
            b = Image.open(bg).convert('RGB'); b = patch_existing(b, room)
            b.save(WORK / ('wkitbg_' + room + '_new.webp'), 'WEBP', quality=88, method=6); b.save(WORK / ('wkitbg_' + room + '_new.png'))
        print('doors', room)

if __name__ == '__main__' and '--existing' in args:
    run_existing()
