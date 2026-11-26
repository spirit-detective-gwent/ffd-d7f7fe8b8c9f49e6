#!/usr/bin/env python3
"""GGD-51 seal 3: idempotent base edits to the EATG eat game.
Adds Ramen Kitsuneya bowls (shoyu, miso, tonkotsu: noodles game, ramen toppings, no tofu beat)
and Izakaya Tanuki plates (yakitori, karaage, edamame: bite game). Tagged /* GGD-51 */."""
import sys
from pathlib import Path
INDEX = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent.parent / 'index.html')
s = INDEX.read_text(encoding='utf8')
TAG = '/* GGD-51 eatg */'
if TAG in s:
    print('eatg already patched'); sys.exit(0)

ROWS = "rows: { win: ['WIN', 'FULL HP', 'back to 55 / 55'], close: ['CLOSE MISS', '+30 HP', 'the normal heal'], bad: ['BAD RUN', '+15 HP', 'half of normal'] } }"
ITEMS_ADD = TAG + """
  shoyu: { game: 'noodles', ramen: 'shoyu', jp: '醤油らーめん', en: 'SHOYU RAMEN', tag: 'BLOW · SLURP · DON\\u2019T BURN', bg: '#ffe2b0', ray1: 'rgba(200,110,50,.42)', ray2: 'rgba(140,70,30,.22)', broth: '#a0602a',
    tapP: 0.034, tapH: 0.08, cool: 0.29, stat: 'hp', base: 30, win: 'x1.5', startHp: 4,
    """ + ROWS + """,
  miso: { game: 'noodles', ramen: 'miso', jp: '味噌らーめん', en: 'MISO RAMEN', tag: 'THICK BROTH HOLDS THE HEAT', bg: '#ffdca0', ray1: 'rgba(214,140,40,.42)', ray2: 'rgba(160,90,30,.22)', broth: '#c48a3a',
    tapP: 0.032, tapH: 0.09, cool: 0.26, stat: 'hp', base: 34, win: 'x1.5', startHp: 4,
    """ + ROWS + """,
  tonkotsu: { game: 'noodles', ramen: 'tonkotsu', jp: '豚骨らーめん', en: 'TONKOTSU RAMEN', tag: 'MILKY BROTH · BIG BOWL', bg: '#fff0d6', ray1: 'rgba(230,190,140,.45)', ray2: 'rgba(170,120,80,.22)', broth: '#e8d4ae',
    tapP: 0.03, tapH: 0.085, cool: 0.27, stat: 'hp', base: 40, win: 'x1.5', startHp: 4,
    """ + ROWS + """,
  yakitori: { game: 'bite', kind: 'yakitori', jp: '焼き鳥', en: 'YAKITORI', tag: 'MASH · TARE GLAZE OFF THE SKEWER', bg: '#f2dcc0', ray1: 'rgba(170,80,30,.3)', ray2: 'rgba(90,40,20,.16)',
    tapP: 0.12, tapsNeed: 8, stat: 'hp', startHp: 4,
    rows: { win: ['WIN', '+15 HP', 'a generous plate'], close: ['CLOSE MISS', '+10 HP', 'the normal heal'], bad: ['BAD RUN', '+5 HP', 'half of normal'] } },
  karaage: { game: 'bite', kind: 'lunch', jp: '唐揚げ', en: 'KARAAGE', tag: 'MASH · CRUNCHY, STRAIGHT FROM THE OIL', bg: '#f0e0c0', ray1: 'rgba(200,160,80,.28)', ray2: 'rgba(120,90,40,.14)',
    tapP: 0.11, tapsNeed: 9, stat: 'hp', startHp: 4,
    rows: { win: ['WIN', '+21 HP', 'a generous plate'], close: ['CLOSE MISS', '+14 HP', 'the normal heal'], bad: ['BAD RUN', '+7 HP', 'half of normal'] } },
  edamame: { game: 'bite', kind: 'edamame', jp: '枝豆', en: 'EDAMAME', tag: 'MASH · POP THE PODS', bg: '#e4f0d0', ray1: 'rgba(90,160,60,.28)', ray2: 'rgba(40,100,40,.14)',
    tapP: 0.13, tapsNeed: 7, stat: 'hp', startHp: 4,
    rows: { win: ['WIN', '+9 HP', 'a generous plate'], close: ['CLOSE MISS', '+6 HP', 'the normal heal'], bad: ['BAD RUN', '+3 HP', 'half of normal'] } },
"""
i = s.index("var ITEMS = {\n  kitsune:")
k = s.index("\n  kitsune:", i)
s = s[:k + 1] + ITEMS_ADD + s[k + 1:]

# ramen toppings in the bowl: yellow noodles, chashu, egg, nori, menma; replaces the udon naruto block when C.ramen
RAMEN_FN = TAG + """
function ramenTop(cx, cy, R, lvl, kind) {
  var dy = -R * 0.1 - lvl * R * 0.1;
  /* nori sheets standing at the back rim */
  [[-0.62, -0.2, -0.25], [-0.46, -0.24, -0.08]].forEach(function (n) { ctx.save(); ctx.translate(cx + R * n[0], cy + R * n[1] + dy * 0.3); ctx.rotate(n[2]); ctx.beginPath(); ctx.rect(-R * 0.09, -R * 0.36, R * 0.18, R * 0.34); ctx.fillStyle = '#1c2a22'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = INK; ctx.stroke(); ctx.fillStyle = 'rgba(120,170,120,.18)'; ctx.fillRect(-R * 0.07, -R * 0.33, R * 0.03, R * 0.28); ctx.restore(); });
  /* two chashu slices */
  [[0.18, -0.12, 0.2], [0.4, -0.02, -0.15]].forEach(function (c) { ctx.save(); ctx.translate(cx + R * c[0], cy + R * c[1] + dy * 0.5); ctx.rotate(c[2]); ctx.beginPath(); ctx.ellipse(0, 0, R * 0.2, R * 0.11, 0, 0, 7); ctx.fillStyle = kind === 'miso' ? '#d49a6a' : '#e0a888'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = INK; ctx.stroke();
    ctx.beginPath(); ctx.ellipse(0, 0, R * 0.14, R * 0.07, 0, 0, 7); ctx.strokeStyle = 'rgba(250,236,220,.85)'; ctx.lineWidth = 2.5; ctx.stroke(); ctx.beginPath(); ctx.ellipse(R * 0.03, 0, R * 0.06, R * 0.03, 0, 0, 7); ctx.fillStyle = 'rgba(150,70,40,.45)'; ctx.fill(); ctx.restore(); });
  /* ajitama half egg */
  ctx.save(); ctx.translate(cx - R * 0.18, cy + R * 0.06 + dy * 0.4); ctx.rotate(-0.15); ctx.beginPath(); ctx.ellipse(0, 0, R * 0.15, R * 0.1, 0, 0, 7); ctx.fillStyle = '#f4ead0'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = INK; ctx.stroke();
  ctx.beginPath(); ctx.ellipse(R * 0.01, 0, R * 0.075, R * 0.055, 0, 0, 7); ctx.fillStyle = '#f0a020'; ctx.fill(); ctx.fillStyle = 'rgba(255,240,180,.7)'; ctx.beginPath(); ctx.ellipse(-R * 0.02, -R * 0.015, R * 0.025, R * 0.012, 0, 0, 7); ctx.fill(); ctx.restore();
  /* menma */
  ctx.fillStyle = '#c99a4a'; for (var q = 0; q < 4; q++) { ctx.save(); ctx.translate(cx + R * (0.02 + q * 0.06), cy + R * 0.12 + dy * 0.3); ctx.rotate(0.5 + q * 0.2); ctx.fillRect(-2.5, -9, 5, 18); ctx.strokeStyle = INK; ctx.lineWidth = 1.4; ctx.strokeRect(-2.5, -9, 5, 18); ctx.restore(); }
  /* scallions, sesame for tonkotsu, butter-corn for miso */
  ctx.fillStyle = '#5ea83a'; for (var m = 0; m < 8; m++) { ctx.beginPath(); ctx.ellipse(cx - R * 0.02 + (m % 4) * 11, cy - R * 0.06 + ((m / 4) | 0) * 8 + dy * 0.6, 5, 3.4, 0, 0, 7); ctx.fill(); }
  if (kind === 'miso') { ctx.fillStyle = '#f2c230'; for (var k2 = 0; k2 < 10; k2++) { ctx.beginPath(); ctx.arc(cx - R * 0.42 + (k2 % 5) * 8, cy + R * 0.08 + ((k2 / 5) | 0) * 7, 3.2, 0, 7); ctx.fill(); } }
  if (kind === 'tonkotsu') { ctx.fillStyle = 'rgba(250,240,220,.95)'; for (var s2 = 0; s2 < 14; s2++) { ctx.beginPath(); ctx.ellipse(cx - R * 0.3 + (s2 * 23 % 60), cy - R * 0.02 + (s2 * 11 % 18), 1.6, 1, 0.4, 0, 7); ctx.fill(); } }
  /* fox naruto: Ramen Kitsuneya's mark */
  ctx.save(); ctx.translate(cx + R * 0.6, cy + R * 0.1); ctx.beginPath(); ctx.ellipse(0, 0, R * 0.12, R * 0.075, 0, 0, 7); ctx.fillStyle = '#fbf3f0'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = INK; ctx.stroke();
  ctx.strokeStyle = '#e8508a'; ctx.lineWidth = 3; ctx.beginPath(); for (var a = 0; a < 10; a += 0.25) { var rr2 = a * R * 0.01; ctx.lineTo(Math.cos(a) * rr2, Math.sin(a) * rr2 * 0.6); } ctx.stroke(); ctx.restore();
}
"""
k = s.index('function bowl(cx, cy, R, rot, eaten) {', i)
s = s[:k] + RAMEN_FN + s[k:]
# noodle colour + topping switch inside bowl()
OLD_N = "ctx.strokeStyle = '#e8d4a4'; ctx.lineWidth = 10; ctx.lineCap = 'round';"
assert s.count(OLD_N) == 1, 'noodle stroke'
s = s.replace(OLD_N, "ctx.strokeStyle = C.ramen ? '#ecc864' : '#e8d4a4'; ctx.lineWidth = C.ramen ? 7 : 10; ctx.lineCap = 'round';" + TAG)
OLD_M = "ctx.fillStyle = '#f6efd8'; ctx.fill(); ctx.lineWidth = 4; ctx.stroke();\n    ctx.save(); ctx.clip(); ctx.restore();"
assert s.count(OLD_M) == 1, 'mound'
s = s.replace(OLD_M, "ctx.fillStyle = C.ramen ? '#f0d478' : '#f6efd8'; ctx.fill(); ctx.lineWidth = 4; ctx.stroke();\n    ctx.save(); ctx.clip(); ctx.restore();")
OLD_T = "    /* naruto + scallions */\n    ctx.save(); ctx.translate(cx + R * 0.5, cy - R * 0.06);"
assert s.count(OLD_T) == 1, 'naruto'
s = s.replace(OLD_T, "    if (C.ramen) { ramenTop(cx, cy, R, lvl, C.ramen); } else {\n    /* naruto + scallions */\n    ctx.save(); ctx.translate(cx + R * 0.5, cy - R * 0.06);")
OLD_E = "ctx.fillStyle = '#5ea83a'; for (var m = 0; m < 6; m++) { ctx.beginPath(); ctx.ellipse(cx - R * 0.05 + (m % 3) * 14, cy + R * 0.02 + ((m / 3) | 0) * 8, 6, 4, 0, 0, 7); ctx.fill(); }\n  } else {"
assert s.count(OLD_E) == 1, 'scallion end'
s = s.replace(OLD_E, "ctx.fillStyle = '#5ea83a'; for (var m = 0; m < 6; m++) { ctx.beginPath(); ctx.ellipse(cx - R * 0.05 + (m % 3) * 14, cy + R * 0.02 + ((m / 3) | 0) * 8, 6, 4, 0, 0, 7); ctx.fill(); }\n    }\n  } else {")
# broth gradient: milky tonkotsu / miso
OLD_B = "br.addColorStop(0, C.curry ? '#e8a24a' : '#f0d09a'); br.addColorStop(0.45, C.broth); br.addColorStop(1, C.curry ? '#6a3a0c' : '#8a6230');"
assert s.count(OLD_B) == 1, 'broth'
s = s.replace(OLD_B, "br.addColorStop(0, C.curry ? '#e8a24a' : C.ramen === 'tonkotsu' ? '#fff6e4' : '#f0d09a'); br.addColorStop(0.45, C.broth); br.addColorStop(1, C.curry ? '#6a3a0c' : C.ramen === 'tonkotsu' ? '#b89a70' : C.ramen === 'shoyu' ? '#5a3010' : '#8a6230');")

# bite pieces: yakitori skewer + edamame pods
PIECES = TAG + """
function pcYakitori(p, A) {
  ctx.save(); ctx.scale(1 + 0.06 * A.pop, 1 - 0.07 * A.pop); ctx.rotate(-0.55 + A.wob * 0.05);
  seg(-6, 62, -6, -64, 5, '#e8d0a0');
  [[-6, -40, 0], [-6, -12, 1], [-6, 16, 0], [-6, 42, 2]].forEach(function (b, bi) { var neg = b[2] === 1;
    blobPath(b[0], b[1], neg ? 18 : 20, neg ? 11 : 13, 0.14, 1.7 + bi, 24);
    var g = ctx.createRadialGradient(b[0] - 6, b[1] - 5, 2, b[0], b[1], 24); g.addColorStop(0, neg ? '#e8f0c0' : '#e8a050'); g.addColorStop(0.55, neg ? '#9ab850' : '#a8501c'); g.addColorStop(1, neg ? '#5a7a28' : '#6a2c0c'); ctx.fillStyle = g; ctx.fill();
    ctx.save(); ctx.clip(); ctx.fillStyle = 'rgba(40,14,4,.55)'; for (var c = 0; c < 3; c++) ctx.fillRect(b[0] - 18, b[1] - 8 + c * 7, 36, 2.2); ctx.restore();
    blobPath(b[0], b[1], neg ? 18 : 20, neg ? 11 : 13, 0.14, 1.7 + bi, 24); inkFood(3);
    ctx.fillStyle = 'rgba(255,230,180,.6)'; ctx.beginPath(); ctx.ellipse(b[0] - 7, b[1] - 6, 5, 2.2, -0.4, 0, 7); ctx.fill(); });
  ctx.fillStyle = 'rgba(255,220,150,.8)'; for (var s2 = 0; s2 < 10; s2++) { ctx.beginPath(); ctx.arc(-18 + (s2 * 13 % 26), -50 + (s2 * 23 % 100), 1.2, 0, 7); ctx.fill(); }
  ctx.restore();
}
function pcEdamame(p, A) {
  ctx.save(); ctx.scale(1 + 0.06 * A.pop, 1 - 0.07 * A.pop); ctx.rotate(A.wob * 0.05);
  [[-22, -18, -0.5], [14, -8, 0.4], [-8, 18, -0.1]].forEach(function (d, di) { ctx.save(); ctx.translate(d[0], d[1]); ctx.rotate(d[2]);
    ctx.beginPath(); ctx.moveTo(-34, 0); ctx.bezierCurveTo(-30, -16, -12, -12, 0, -14); ctx.bezierCurveTo(14, -16, 30, -14, 36, -2); ctx.bezierCurveTo(30, 14, 12, 12, 0, 13); ctx.bezierCurveTo(-14, 14, -30, 14, -34, 0); ctx.closePath();
    var g = ctx.createLinearGradient(0, -14, 0, 14); g.addColorStop(0, '#a8d070'); g.addColorStop(1, '#4a8a2a'); ctx.fillStyle = g; ctx.fill(); inkFood(3);
    [-20, 0, 20].forEach(function (bx) { ctx.beginPath(); ctx.ellipse(bx, 0, 8, 7, 0, 0, 7); ctx.fillStyle = 'rgba(200,236,140,.7)'; ctx.fill(); ctx.strokeStyle = 'rgba(42,60,20,.5)'; ctx.lineWidth = 1.5; ctx.stroke(); });
    ctx.fillStyle = 'rgba(255,255,255,.85)'; for (var s2 = 0; s2 < 5; s2++) ctx.fillRect(-26 + s2 * 12, -10 + (s2 % 2) * 4, 2.4, 2.4);
    ctx.restore(); });
  ctx.restore();
}
"""
k = s.index('var BITE_SPEC = {')
s = s[:k] + PIECES + s[k:]
OLD_S = "  dango: { draw: pcDango, cut: '#fff6e8', bites: [[-6, -28, 10], [8, 0, 10], [-8, 24, 9], [10, -8, 8]], up: 18 }\n};"
assert s.count(OLD_S) == 1, 'bite spec'
s = s.replace(OLD_S, "  dango: { draw: pcDango, cut: '#fff6e8', bites: [[-6, -28, 10], [8, 0, 10], [-8, 24, 9], [10, -8, 8]], up: 18 },\n  yakitori: { draw: pcYakitori, cut: '#f6e0b8', bites: [[-20, -52, 12], [-22, -26, 12], [-16, -2, 11], [-14, 26, 10]], up: 16, steam: 1 }, " + TAG + "\n  edamame: { draw: pcEdamame, cut: '#e8f4d0', bites: [[-44, -26, 11], [-30, -10, 10], [-4, -16, 10], [-30, 24, 9]], up: 14 }\n};")
INDEX.write_text(s, encoding='utf8')
print('eatg patched')
