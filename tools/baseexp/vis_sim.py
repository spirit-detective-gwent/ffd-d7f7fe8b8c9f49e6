#!/usr/bin/env python3
"""guard sight preview (same rule as seeK: cone a deg, reach r, full reach within AW.core=35 deg, AW.side=0.55 reach at the
edge, LOS sampled every 12 px against the room blocks). Yellow = seen facing A, blue = facing B, red = both.
usage: vis_sim.py <worktree> <room> [carry] -> /workspace/baseexp/work/vis_<room>.png"""
import sys, json, math
from pathlib import Path
from PIL import Image, ImageDraw
WT = Path(sys.argv[1]); room = sys.argv[2]; carry = len(sys.argv) > 3
S = json.loads((WT / 'tools/baseexp/rooms.json').read_text())['rooms'][room]
blocks = [p[1] for p in S['props']] + S.get('blocks', [])
OPEN = [100, 155, 1050, 785]
def ok(x, y):
    if not (OPEN[0] <= x <= OPEN[2] and OPEN[1] <= y <= OPEN[3]): return False
    return not any(b[0] <= x <= b[2] and b[1] <= y <= b[3] for b in blocks)
def los(x0, y0, x1, y1):
    d = math.hypot(x1 - x0, y1 - y0); n = max(1, math.ceil(d / 12))
    return all(ok(x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n) for k in range(1, n))
def angD(a, b): return (a - b + math.pi) % (2 * math.pi) - math.pi
g = S['guard']; gx, gy = g['at']; R = g['r'] * (1.25 if carry else 1); A = math.radians(g['a']); C = math.radians(35)
def seen(fa, x, y):
    dx, dy = x - gx, y - gy; d = math.hypot(dx, dy); th = abs(angD(math.atan2(dy, dx), fa))
    if th > A: return False
    rr = R if th <= C else R * (1 - 0.45 * (th - C) / max(1e-3, A - C))
    return d <= rr and los(gx, gy, x, y)
im = Image.open('/workspace/baseexp/work/%s.png' % room).convert('RGBA'); ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
st = 8
for y in range(OPEN[1], OPEN[3], st):
    for x in range(OPEN[0], OPEN[2], st):
        if not ok(x, y): continue
        a = seen(g['fa'][0], x, y); b = seen(g['fa'][1], x, y)
        col = (255, 0, 0, 110) if a and b else (255, 200, 0, 110) if a else (0, 140, 255, 110) if b else None
        if col: d.rectangle([x, y, x + st - 1, y + st - 1], fill=col)
for b in blocks: d.rectangle(b, outline=(255, 0, 0, 255), width=2)
c = S.get('crate'); d.rectangle([c[0] - 30, c[1] - 24, c[0] + 30, c[1]], outline=(0, 200, 0, 255), width=4)
d.ellipse([gx - 10, gy - 10, gx + 10, gy + 10], fill=(255, 0, 255, 255))
im.alpha_composite(ov); im.convert('RGB').save('/workspace/baseexp/work/vis_%s%s.png' % (room, '_carry' if carry else ''))
print('crate seen A/B', seen(g['fa'][0], c[0], c[1] + 20), seen(g['fa'][1], c[0], c[1] + 20))
