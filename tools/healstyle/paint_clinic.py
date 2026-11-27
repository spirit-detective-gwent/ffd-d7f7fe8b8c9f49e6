#!/workspace/pwenv/bin/python3
"""v6564-healstyle (Erik t418/t419): take the tatami cot out of world/c2_clinic.webp and lay floor where it stood.
The clinic floor is flat cel planks on a 34 px grid (vertical lines at 128, 162, ... 434), each plank cut into segments by
1 px joints. Each plank column under the cot is re-laid from the joint above the cot to the joint below it, continuing
the segment colors it meets at both ends, so there is no seam. The rest of the room stays pixel-identical.
usage: paint_clinic.py [--preview out.png]"""
import sys, random
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'world' / 'c2_clinic.webp'
im = Image.open(P).convert('RGB'); px = im.load(); d = ImageDraw.Draw(im)
rnd = random.Random(419)
LINE = (145, 101, 61); JOINT = (141, 99, 61)
PAL = [(168, 120, 77), (173, 127, 88), (160, 114, 75), (164, 118, 76), (172, 126, 87), (166, 119, 76)]
Y0, Y1 = 506, 728            # cot + shadow rows
LINES = list(range(128, 436, 34))   # 128 ... 434
dark = lambda c: sum(c) < 360
for i in range(len(LINES) - 1):
    L, R = LINES[i] + 2, LINES[i + 1]          # plank interior x range [L, R)
    cx = (L + R) // 2
    yt = Y0
    while yt > Y0 - 220 and not dark(px[cx, yt]): yt -= 1    # joint above
    yb = Y1
    while yb < 788 and not dark(px[cx, yb]): yb += 1         # joint below (or the wall)
    ctop = px[cx, yt + 3]; cbot = px[cx, yb - 3]
    # segments: keep the top color to a first cut, random middle pieces, the bottom color last
    cuts = [yt]; y = max(yt + 40, Y0 + rnd.randint(18, 70))
    while y < yb - 46: cuts.append(y); y += rnd.randint(58, 120)
    cuts.append(yb)
    for k in range(len(cuts) - 1):
        col = ctop if k == 0 else cbot if k == len(cuts) - 2 else rnd.choice([c for c in PAL if c != ctop])
        d.rectangle([L, cuts[k] + 1, R - 1, cuts[k + 1] - 1], fill=col)
        if 0 < k: d.line([L, cuts[k], R - 1, cuts[k]], fill=JOINT)
for x in LINES:                                    # the plank lines, 2 px, through the patched rows
    d.rectangle([x, Y0 - 1, x + 1, Y1 + 1], fill=LINE)
if '--preview' in sys.argv:
    im.save(sys.argv[sys.argv.index('--preview') + 1])
else:
    im.save(P, 'WEBP', quality=90, method=6); print('wrote', P, P.stat().st_size)
