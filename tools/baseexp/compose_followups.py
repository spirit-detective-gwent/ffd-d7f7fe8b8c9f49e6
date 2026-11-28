#!/usr/bin/env python3
"""Compose follow-ups before/after contact sheet. usage: compose_followups.py [SHOTDIR] [OUT]"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
SRC = sys.argv[1] if len(sys.argv) > 1 else '/workspace/baseexp/shots'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(SRC, 'followups_before_after.png')
RAW, OLD = os.path.join(SRC, 'raw'), os.path.join(SRC, 'old')
BG, INK, GOLD, MUTED, RULE = (24, 22, 30), (240, 232, 210), (255, 231, 160), (160, 154, 146), (60, 54, 66)
def font(n):
    p = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    return ImageFont.truetype(p, n) if os.path.exists(p) else ImageFont.load_default()
F26, F18, F14, F12 = font(26), font(18), font(14), font(12)
def load(p):
    return Image.open(p).convert('RGB')
def crop_play(im, top=210, bot=36):
    """Drop the HUD / music footer so the room is the focus."""
    w, h = im.size
    if h >= 800: return im.crop((0, top, w, h - bot))
    return im
def scale(im, w):
    h = int(im.height * w / im.width)
    return im.resize((w, h), Image.LANCZOS)
def cell(path, w=200, play=True):
    im = load(path)
    if play: im = crop_play(im)
    return scale(im, w)
W = 200  # cell width
# ---- sections ----
# Patrol: before = standing-post cover sequence; after = loop + spotted + 5-fight
before_p = [os.path.join(RAW, 'g%d.png' % i) for i in range(1, 7)]
after_p  = [os.path.join(RAW, 'p%d.png' % i) for i in range(1, 7)]
before_p_lab = ['Faces the crate (west)', 'Cover behind sacks', 'Turns on the beat', 'Walk up behind him', 'Crate up, cone grows', 'Caught: "!" then chase']
after_p_lab  = ['Walks the north aisle', 'Stops, looks at the corner', 'Next leg, cone follows', 'SPOTTED: BACKUP! bark', '4 backups through the doors', 'One fight of 5']
after_s = [os.path.join(RAW, 's%d.png' % i) for i in (1, 2, 3)]
after_s_lab = ['Slip in behind him', 'Close the gap unseen', 'SOLO fight, just him']
before_h = [os.path.join(RAW, 'room_%s.png' % k) for k in ('cage', 'showers', 'trainer')]
after_h  = [os.path.join(RAW, 'h_%s.png' % k) for k in ('cage', 'showers', 'trainer')]
h_lab = ['Equipment Cage', 'Showers', "Trainer's Room"]
carry_b = [os.path.join(RAW, 'carry_before_%s.png' % d) for d in ('up', 'down', 'left', 'right')]
carry_a = [os.path.join(RAW, 'carry_after_%s.png' % d) for d in ('up', 'down', 'left', 'right')]
carry_lab = ['UP (facing away)', 'DOWN', 'LEFT', 'RIGHT']
missing = [p for p in before_p + after_p + after_s + before_h + after_h + carry_b + carry_a if not os.path.exists(p)]
if missing:
    sys.exit('missing frames: ' + ', '.join(missing))

pad, cap, title_h, row_lab = 10, 36, 44, 28
# layout widths
# patrol: 6 cells
pw = pad + 90 + 6 * (W + pad)
# sneak: 3 cells
# hurdle: 3+3 with a before/after label column
# carry: 4+4
width = max(pw, 1100)
# heights
def row_h(ims, extra=0):
    return max(i.height for i in ims) + cap + extra

p_b = [cell(p) for p in before_p]
p_a = [cell(p) for p in after_p]
s_a = [cell(p) for p in after_s]
h_b = [cell(p) for p in before_h]
h_a = [cell(p) for p in after_h]
# carry crops are already tight portraits; don't HUD-crop, just scale to similar height
def cell_carry(p, h=220):
    im = load(p)
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
c_b = [cell_carry(p) for p in carry_b]
c_a = [cell_carry(p) for p in carry_a]

sections = []
# header later
y = 16
blocks = []
# title + 4 sections
H = 16 + 70  # page title
H += title_h + row_lab + row_h(p_b) + row_lab + row_h(p_a) + pad  # patrol
H += title_h + row_lab + row_h(s_a) + pad  # sneak
H += title_h + row_lab + row_h(h_b) + row_lab + row_h(h_a) + pad  # hurdles
H += title_h + row_lab + max(c_b[0].height, c_a[0].height) + cap
H += row_lab + max(c_b[0].height, c_a[0].height) + cap + 24

out = Image.new('RGB', (width, H), BG)
d = ImageDraw.Draw(out)

def text(xy, t, f=F18, fill=INK):
    d.text(xy, t, fill=fill, font=f)

y = 14
text((pad, y), "Fox Fire Fist  ·  baseexp follow-ups  (t583u / t587u / t588u)", F26, GOLD)
y += 32
text((pad, y), "Before = earlier baseexp build (standing guard, empty hurdle rooms, old carry).   After = this commit (patrol loop, spotted = 5, sneak = solo, 2–3 roamers, back-carry).", F14, MUTED)
y += 28
d.line((pad, y, width - pad, y), fill=RULE, width=1)
y += 10

def paste_row(ims, labs, x0, y0, label=None):
    if label:
        text((pad, y0), label, F18, GOLD); y0 += row_lab
    h = max(i.height for i in ims)
    x = x0
    for im, lab in zip(ims, labs):
        out.paste(im, (x, y0))
        # caption
        for j, ln in enumerate(lab.split('\n')[:2]):
            text((x + 2, y0 + h + 4 + j * 14), ln, F12, INK)
        x += im.width + pad
    return y0 + h + cap

y += 4
text((pad, y), "1. Cafeteria guard: patrol, spotted alert, 5-enemy fight", F18, GOLD); y += title_h - 16
y = paste_row(p_b, before_p_lab, 90, y, "BEFORE  ·  stands at his post, turns on a beat")
y = paste_row(p_a, after_p_lab, 90, y, "AFTER  ·  walks a loop, cone follows; if he sees you he barks BACKUP! (fight of 5)")
d.line((pad, y, width - pad, y), fill=RULE, width=1); y += 10

text((pad, y), "2. Sneak up from behind (unseen)  ·  after only: no bark, solo fight", F18, GOLD); y += title_h - 16
y = paste_row(s_a, after_s_lab, 90, y)
d.line((pad, y, width - pad, y), fill=RULE, width=1); y += 10

text((pad, y), "3. Storehouse hurdle rooms: 2–3 roamers (library rule — beaten stay gone)", F18, GOLD); y += title_h - 16
y = paste_row(h_b, h_lab, 90, y, "BEFORE  ·  hurdle in the room, no roamers")
y = paste_row(h_a, h_lab, 90, y, "AFTER  ·  Cage 3, Showers 3, Trainer 2")
d.line((pad, y, width - pad, y), fill=RULE, width=1); y += 10

text((pad, y), "4. Hurdle carry draw  ·  facing up, the hurdle sits behind his back; only the two ends show", F18, GOLD); y += title_h - 16
# carry rows may be narrower cells; left-align under 90
y = paste_row(c_b, carry_lab, 90, y, "BEFORE  ·  facing away, the hurdle is drawn on top of his back")
y = paste_row(c_a, carry_lab, 90, y, "AFTER  ·  full back view, ends stick out both sides")
text((pad, y + 4), "Shots from tools/baseexp/shoot_patrol.py + shoot_carry.py + earlier room / cover strips. Not pushed.", F12, MUTED)
out.save(OUT, optimize=True)
print('wrote', OUT, out.size)
