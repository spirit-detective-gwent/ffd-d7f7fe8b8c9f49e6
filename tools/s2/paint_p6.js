/* v6.5.64 FFF_S2P phase 6 (GGD-51, seal 3 · Jin's turf): cel interiors drawn in-engine once per entry.
 * Ramen Kitsuneya, Karaoke Kitsune (lobby, booth, VIP booth), Hotel Chuo (lobby, 7F hall), Izakaya Tanuki,
 * Neon Game Center (floor, Jin's back room). Canvas2D, ink outlines, two-tone cel, same kit as the NQ rooms.
 * No loops: every painter runs once into a cached canvas. */
(function (root) {
  var S2P = root.FFF_S2P = root.FFF_S2P || {};
  var INK = '#1a1220', RW = 1280, RH = 900;
  var JP = '"Noto Sans CJK JP","Noto Serif CJK JP",sans-serif', SER = '"Noto Serif CJK JP","BIZ UDPMincho",serif';
  function box(g, x, y, w, h, f, lw, r) {
    g.beginPath(); if (r) { if (g.roundRect) g.roundRect(x, y, w, h, r); else g.rect(x, y, w, h); } else g.rect(x, y, w, h);
    if (f) { g.fillStyle = f; g.fill(); } if (lw !== 0) { g.lineWidth = lw || 3; g.strokeStyle = INK; g.stroke(); }
  }
  function ell(g, x, y, rx, ry, f, lw) { g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, 7); if (f) { g.fillStyle = f; g.fill(); } if (lw !== 0) { g.lineWidth = lw || 3; g.strokeStyle = INK; g.stroke(); } }
  function tx(g, s, x, y, px, col, wt, al, font) { g.font = (wt || 900) + ' ' + px + 'px ' + (font || JP); g.textAlign = al || 'center'; g.textBaseline = 'middle'; g.fillStyle = col; g.fillText(s, x, y); }
  function jp(g, s, x, y, px, col, font) { tx(g, s, x, y, px, col, 900, 'center', font || SER); }
  function vjp(g, s, x, y, px, col, gap, font) { s.split('').forEach(function (ch, i) { jp(g, ch, x, y + i * (gap || px * 1.08), px, col, font); }); }
  function glowAt(g, x, y, r, col) { var gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, col); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(x - r, y - r, r * 2, r * 2); }
  function neonTx(g, s, x, y, px, col, glow, font) {
    g.save(); g.font = '900 ' + px + 'px ' + (font || JP); g.textAlign = 'center'; g.textBaseline = 'middle';
    g.shadowColor = glow || col; g.shadowBlur = px * 0.6; g.lineWidth = Math.max(2, px * 0.12); g.strokeStyle = glow || col; g.strokeText(s, x, y);
    g.shadowBlur = px * 0.3; g.fillStyle = '#fff8fc'; g.fillText(s, x, y); g.restore();
  }
  function neonLine(g, pts, col, w) { g.save(); g.shadowColor = col; g.shadowBlur = 14; g.strokeStyle = col; g.lineWidth = w || 5; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); pts.forEach(function (p, i) { i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]); }); g.stroke(); g.shadowBlur = 0; g.strokeStyle = 'rgba(255,255,255,.75)'; g.lineWidth = Math.max(1.5, (w || 5) * 0.35); g.stroke(); g.restore(); }
  function plankWall(g, x, y, w, h, c1, c2, step) { g.fillStyle = c1; g.fillRect(x, y, w, h); for (var i = x; i < x + w; i += step) { g.fillStyle = ((i / step) | 0) % 2 ? c2 : c1; g.fillRect(i, y, step - 2, h); g.fillStyle = 'rgba(0,0,0,.18)'; g.fillRect(i + step - 2, y, 2, h); } }
  function boards(g, x, y, w, h, c1, c2, bh) { for (var j = y, n = 0; j < y + h; j += bh, n++) { g.fillStyle = n % 2 ? c1 : c2; g.fillRect(x, j, w, bh); g.fillStyle = 'rgba(0,0,0,.16)'; g.fillRect(x, j + bh - 2, w, 2); for (var i = x + ((n * 97) % 220); i < x + w; i += 220) g.fillRect(i, j, 2, bh); } }
  function tiles(g, x, y, w, h, c1, c2, s) { for (var j = y, b = 0; j < y + h; j += s, b++) for (var i = x, a = 0; i < x + w; i += s, a++) { g.fillStyle = (a + b) % 2 ? c1 : c2; g.fillRect(i, j, Math.min(s, x + w - i), Math.min(s, y + h - j)); } g.strokeStyle = 'rgba(0,0,0,.14)'; g.lineWidth = 1.5; for (var yy = y; yy <= y + h; yy += s) { g.beginPath(); g.moveTo(x, yy); g.lineTo(x + w, yy); g.stroke(); } for (var xx = x; xx <= x + w; xx += s) { g.beginPath(); g.moveTo(xx, y); g.lineTo(xx, y + h); g.stroke(); } }
  function carpet(g, x, y, w, h, c1, c2, c3, s) { g.fillStyle = c1; g.fillRect(x, y, w, h); g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip(); for (var j = y, b = 0; j < y + h + s; j += s, b++) for (var i = x - s, a = 0; i < x + w + s; i += s, a++) { var cx = i + (b % 2 ? s / 2 : 0), cy = j; g.fillStyle = c2; g.beginPath(); g.moveTo(cx, cy - s * 0.32); g.lineTo(cx + s * 0.32, cy); g.lineTo(cx, cy + s * 0.32); g.lineTo(cx - s * 0.32, cy); g.closePath(); g.fill(); if (c3) { g.fillStyle = c3; g.fillRect(cx - 2, cy - 2, 4, 4); } } g.restore(); }
  function shellWalls(g, wallTop, w, h, exitX) {
    w = w || RW; h = h || RH; exitX = exitX == null ? w / 2 : exitX; var ey = h - 50;
    g.fillStyle = '#1b1820'; g.fillRect(0, 0, 90, h); g.fillRect(w - 90, 0, 90, h); g.fillRect(0, ey, exitX - 60, 50); g.fillRect(exitX + 60, ey, w - exitX - 60, 50);
    g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(90, wallTop, w - 180, 14);
    g.strokeStyle = INK; g.lineWidth = 4; g.strokeRect(90, 2, w - 180, ey - 2); g.fillStyle = 'rgba(255,220,160,.10)'; g.fillRect(exitX - 60, ey, 120, 50);
    var vg = g.createRadialGradient(w / 2, h * 0.58, 260, w / 2, h * 0.58, Math.max(w, h) * 0.66); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(10,6,14,.38)'); g.fillStyle = vg; g.fillRect(0, 0, w, h);
  }
  function stool(g, x, y, c) { g.fillStyle = 'rgba(0,0,0,.25)'; g.beginPath(); g.ellipse(x, y + 18, 20, 6, 0, 0, 7); g.fill(); box(g, x - 3, y, 6, 18, '#3b2a22', 1); ell(g, x, y, 19, 9, c, 3); g.fillStyle = 'rgba(255,255,255,.25)'; g.beginPath(); g.ellipse(x - 5, y - 3, 7, 3, 0, 0, 7); g.fill(); }
  function bowlS(g, x, y, s, c) { g.beginPath(); g.ellipse(x, y, 16 * s, 6 * s, 0, 0, 7); g.fillStyle = '#f2e8d6'; g.fill(); g.beginPath(); g.moveTo(x - 16 * s, y); g.quadraticCurveTo(x, y + 20 * s, x + 16 * s, y); g.fillStyle = c || '#b8332a'; g.fill(); g.lineWidth = 2; g.strokeStyle = INK; g.stroke(); g.beginPath(); g.ellipse(x, y, 16 * s, 6 * s, 0, 0, 7); g.stroke(); }
  function plant(g, x, y, s) { g.fillStyle = 'rgba(0,0,0,.25)'; g.beginPath(); g.ellipse(x, y + 4, 26 * s, 8 * s, 0, 0, 7); g.fill(); box(g, x - 18 * s, y - 30 * s, 36 * s, 34 * s, '#a0582e', 4);
    ['#2f6b3a', '#3f8a4a', '#2a5a33'].forEach(function (c, i) { for (var k = 0; k < 5; k++) { var a = -Math.PI / 2 + (k - 2) * 0.45 + i * 0.12; g.beginPath(); g.ellipse(x + Math.cos(a) * 26 * s, y - 40 * s + Math.sin(a) * 30 * s, 9 * s, 22 * s, a + Math.PI / 2, 0, 7); g.fillStyle = c; g.fill(); g.lineWidth = 2; g.strokeStyle = INK; g.stroke(); } }); }
  function shade(hex, k) { var n = parseInt(hex.slice(1), 16), r = n >> 16, gg = (n >> 8) & 255, b = n & 255, f = function (c) { return Math.max(0, Math.min(255, Math.round(k < 0 ? c * (1 + k) : c + (255 - c) * k))); }; return 'rgb(' + f(r) + ',' + f(gg) + ',' + f(b) + ')'; }
  function lantern(g, x, y, r, col, word) { g.strokeStyle = INK; g.lineWidth = 2; g.beginPath(); g.moveTo(x, y - r * 1.6); g.lineTo(x, y - r * 1.25); g.stroke(); glowAt(g, x, y, r * 3.2, 'rgba(255,140,80,.22)'); ell(g, x, y, r, r * 1.25, col, 3); box(g, x - r * 0.55, y - r * 1.32, r * 1.1, r * 0.2, '#2a1a12', 2); box(g, x - r * 0.55, y + r * 1.12, r * 1.1, r * 0.2, '#2a1a12', 2); g.strokeStyle = 'rgba(0,0,0,.25)'; g.lineWidth = 1.5; for (var i = -2; i <= 2; i++) { g.beginPath(); g.ellipse(x, y + i * r * 0.4, r * 0.98, r * 0.12, 0, 0, Math.PI); g.stroke(); } if (word) jp(g, word, x, y + 2, r * 0.8, '#2a0e0a'); }
  function steamW(g, x, y, n, sp) { g.strokeStyle = 'rgba(240,240,245,.42)'; g.lineWidth = 5; g.lineCap = 'round'; for (var i = 0; i < n; i++) { var px = x + (i - (n - 1) / 2) * sp; g.beginPath(); g.moveTo(px, y); g.bezierCurveTo(px - 8, y - 16, px + 8, y - 28, px, y - 46); g.stroke(); } }
  function chair(g, x, y, c) { box(g, x - 22, y - 30, 44, 18, c, 4); box(g, x - 22, y - 14, 44, 28, shade(c, -0.2), 4); }
  function sofaU(g, x, y, w, h, c) { /* a U sofa seen from above, opening south */
    box(g, x, y, w, 34, shade(c, -0.25), 3, 8); box(g, x, y, 34, h, shade(c, -0.25), 3, 8); box(g, x + w - 34, y, 34, h, shade(c, -0.25), 3, 8);
    box(g, x + 30, y + 26, w - 60, 26, c, 3, 6); box(g, x + 26, y + 30, 26, h - 34, c, 3, 6); box(g, x + w - 52, y + 30, 26, h - 34, c, 3, 6);
    g.fillStyle = 'rgba(255,255,255,.14)'; g.fillRect(x + 40, y + 30, w - 80, 5); }
  function frosted(g, x, y, w, h, tint) { var lg = g.createLinearGradient(x, y, x + w, y + h); lg.addColorStop(0, 'rgba(230,240,255,.78)'); lg.addColorStop(0.5, tint || 'rgba(200,215,240,.62)'); lg.addColorStop(1, 'rgba(240,235,255,.78)'); box(g, x, y, w, h, lg, 3, 6); g.fillStyle = 'rgba(255,255,255,.5)'; g.fillRect(x + 8, y + 6, w * 0.3, 4); g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip(); g.strokeStyle = 'rgba(255,255,255,.35)'; g.lineWidth = 10; for (var i = -h; i < w; i += 46) { g.beginPath(); g.moveTo(x + i, y + h); g.lineTo(x + i + h, y); g.stroke(); } g.restore(); }
  function arcadeCab(g, x, y, scr, trim, label, dark) { /* a sit-down cabinet seen from above-front (3/4), screen faces south */
    g.fillStyle = 'rgba(0,0,0,.3)'; g.beginPath(); g.ellipse(x + 50, y + 140, 62, 14, 0, 0, 7); g.fill();
    box(g, x, y, 100, 132, dark ? '#24222c' : '#2c2838', 3, 6); box(g, x + 6, y + 4, 88, 22, trim, 2, 4);
    if (label) tx(g, label, x + 50, y + 15, label.length > 8 ? 9 : 11, '#1a1220', 900);
    box(g, x + 10, y + 32, 80, 56, dark ? '#101018' : scr, 3, 4);
    if (!dark) { glowAt(g, x + 50, y + 60, 70, 'rgba(160,230,255,.16)'); g.fillStyle = 'rgba(255,255,255,.18)'; g.fillRect(x + 14, y + 36, 30, 4); }
    else { tx(g, '故障中', x + 50, y + 54, 12, '#e8c040', 900); tx(g, 'OUT OF ORDER', x + 50, y + 72, 7, '#e8c040', 900); }
    box(g, x + 4, y + 94, 92, 30, shade(trim, -0.35), 3, 4); ell(g, x + 28, y + 108, 8, 6, '#e8e0d0', 2); [62, 76].forEach(function (bx, i) { ell(g, x + bx, y + 106, 6, 5, i ? '#e85050' : '#50a0e8', 2); });
    box(g, x + 30, y + 132, 40, 18, '#3a3444', 2, 6); }
  function crane(g, x, y, col) { g.fillStyle = 'rgba(0,0,0,.3)'; g.beginPath(); g.ellipse(x + 55, y + 168, 64, 14, 0, 0, 7); g.fill(); box(g, x, y, 110, 160, col, 3, 6); box(g, x + 8, y + 22, 94, 92, 'rgba(200,235,255,.5)', 3, 3); g.fillStyle = 'rgba(255,255,255,.4)'; g.fillRect(x + 12, y + 26, 30, 4);
    [[30, 96, '#f2a0c0'], [56, 100, '#f0d060'], [80, 94, '#90d0f0'], [44, 82, '#c8a0f0'], [70, 84, '#f2a0c0']].forEach(function (p) { ell(g, x + p[0], y + p[1], 12, 10, p[2], 2); g.fillStyle = INK; g.fillRect(x + p[0] - 4, y + p[1] - 3, 2, 2); g.fillRect(x + p[0] + 3, y + p[1] - 3, 2, 2); });
    g.strokeStyle = INK; g.lineWidth = 2; g.beginPath(); g.moveTo(x + 55, y + 24); g.lineTo(x + 55, y + 52); g.stroke(); g.beginPath(); g.moveTo(x + 47, y + 62); g.lineTo(x + 55, y + 52); g.lineTo(x + 63, y + 62); g.stroke();
    box(g, x + 4, y + 4, 102, 16, '#fff0f6', 2, 4); tx(g, 'CRANE', x + 55, y + 12, 10, '#e8508a', 900); box(g, x + 6, y + 120, 98, 34, shade(col, -0.3), 2, 4); ell(g, x + 34, y + 136, 7, 6, '#e8e0d0', 2); box(g, x + 64, y + 128, 24, 16, '#e8c040', 2, 3); }
  function medalPusher(g, x, y, w) { g.fillStyle = 'rgba(0,0,0,.3)'; g.fillRect(x + 6, y + 150, w, 14); box(g, x, y, w, 150, '#3a2c48', 3, 8); box(g, x + 10, y + 12, w - 20, 70, 'rgba(255,220,120,.35)', 3, 4);
    for (var i = 0; i < 18; i++) ell(g, x + 22 + (i * 37 % (w - 44)), y + 30 + (i * 13 % 46), 8, 4, '#e8c040', 1.5);
    neonTx(g, 'MEDAL', x + w / 2, y + 100, 18, '#ffd860', '#ff9020'); box(g, x + 10, y + 118, w - 20, 22, '#22182c', 2, 4); for (var k = 0; k < 4; k++) ell(g, x + 30 + k * (w - 60) / 3, y + 129, 6, 5, ['#e85050', '#50c0e8', '#e8c040', '#80e060'][k], 1.5); }

  var P6 = S2P.p6 = {};

  /* ---------------- 1. Ramen Kitsuneya (Tetsuo's shop) ---------------- */
  P6.ramen = function (g) {
    /* dark red-and-black checker floor, worn */
    tiles(g, 90, 230, RW - 180, 620, '#3a1c1c', '#241416', 52);
    g.fillStyle = 'rgba(255,220,180,.05)'; for (var i = 0; i < 60; i++) g.fillRect(100 + (i * 197) % 1060, 240 + (i * 131) % 600, 22, 3);
    /* back wall: soot-dark cedar with a red band */
    plankWall(g, 90, 0, RW - 180, 230, '#4a2a1c', '#53301f', 30); g.fillStyle = '#1f120c'; g.fillRect(90, 0, RW - 180, 16); g.fillStyle = '#9a1e22'; g.fillRect(90, 196, RW - 180, 16); g.fillStyle = '#1f120c'; g.fillRect(90, 212, RW - 180, 18);
    /* the shop sign over the kitchen pass: らーめん 狐屋 */
    box(g, 430, 18, 420, 62, '#1a1210', 4, 4); box(g, 436, 24, 408, 50, '#f2e6c8', 2, 2); jp(g, '\u3089\u30fc\u3081\u3093', 560, 49, 30, '#9a1e22'); jp(g, '\u72d0\u5c4b', 730, 49, 34, '#1a1210');
    ell(g, 806, 49, 18, 18, '#9a1e22', 2); tx(g, 'KITSUNEYA', 640, 92, 12, '#f2e6c8', 900);
    /* the menu tags (wooden plaques, red ink) left and right */
    var M = [['\u91a4\u6cb9', 'SHOYU'], ['\u5473\u564c', 'MISO'], ['\u8c5a\u9aa8', 'TONKOTSU'], ['\u5869', 'SHIO'], ['\u9903\u5b50', 'GYOZA'], ['\u70cf\u9f8d\u8336', 'OOLONG']];
    M.forEach(function (m, i) { var x = 120 + i * 50 + (i > 2 ? 870 : 0); box(g, x, 26, 42, 132, '#e9d8b0', 3, 2); vjp(g, m[0], x + 21, 46, m[0].length > 2 ? 15 : 19, '#7a1414'); tx(g, m[1], x + 21, 150, 6.5, '#2a1a12', 900); });
    /* kitchen pass: the noodle boiler, the stock pots, the ladles */
    g.fillStyle = '#140c0a'; g.fillRect(430, 96, 420, 116); glowAt(g, 640, 170, 220, 'rgba(255,190,120,.25)');
    box(g, 446, 112, 120, 84, '#8a8e96', 4, 4); for (var b = 0; b < 3; b++) { ell(g, 470 + b * 36, 140, 14, 9, '#3a3c42', 2); g.strokeStyle = '#c9a06a'; g.lineWidth = 3; g.beginPath(); g.moveTo(470 + b * 36, 132); g.lineTo(476 + b * 36, 108); g.stroke(); }
    steamW(g, 506, 118, 3, 26);
    [[640, 150, 46], [740, 156, 40]].forEach(function (p) { box(g, p[0] - p[2], p[1] - 34, p[2] * 2, 64, '#7a7e86', 4, 6); ell(g, p[0], p[1] - 34, p[2], 12, '#5a3a20', 3); g.fillStyle = '#a0602a'; g.beginPath(); g.ellipse(p[0], p[1] - 34, p[2] - 6, 8, 0, 0, 7); g.fill(); steamW(g, p[0], p[1] - 44, 3, 20); });
    box(g, 800, 110, 36, 90, '#d8d0c0', 3, 2); for (var h = 0; h < 4; h++) { g.strokeStyle = '#3a2a1c'; g.lineWidth = 2; g.beginPath(); g.moveTo(806 + h * 8, 116); g.lineTo(806 + h * 8, 160); g.stroke(); ell(g, 806 + h * 8, 164, 5, 4, '#9aa0a8', 1.5); }
    /* paper lanterns + the fox mask charm + a poster */
    lantern(g, 200, 214, 26, '#d6243a', '\u3089'); lantern(g, 1080, 214, 26, '#d6243a', '\u3081');
    box(g, 300, 30, 100, 130, '#f2e6c8', 3, 2); tx(g, '\u5927\u76db\u7121\u6599', 350, 56, 15, '#9a1e22', 900); bowlS(g, 350, 102, 1.6, '#9a1e22'); tx(g, 'BIG BOWL FREE', 350, 142, 8, '#2a1a12', 900);
    box(g, 878, 30, 92, 120, '#20161a', 3, 4); g.save(); g.translate(924, 86); ell(g, 0, 0, 32, 38, '#f4f0ea', 3); g.fillStyle = '#d6243a'; g.beginPath(); g.moveTo(-26, -22); g.lineTo(-14, -48); g.lineTo(-4, -26); g.closePath(); g.fill(); g.beginPath(); g.moveTo(26, -22); g.lineTo(14, -48); g.lineTo(4, -26); g.closePath(); g.fill(); g.strokeStyle = '#d6243a'; g.lineWidth = 3; g.beginPath(); g.moveTo(-18, -4); g.lineTo(-6, 2); g.moveTo(18, -4); g.lineTo(6, 2); g.stroke(); ell(g, 0, 18, 5, 4, INK, 0); g.restore();
    /* the L counter: long run under the pass, return down the right side */
    box(g, 190, 250, 820, 46, '#b8823e', 4, 3); g.fillStyle = 'rgba(255,255,255,.2)'; g.fillRect(196, 254, 808, 6); box(g, 196, 292, 808, 70, '#3a1e14', 3); for (var v = 214; v < 1000; v += 40) { g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(v, 296, 3, 62); }
    box(g, 1006, 250, 70, 300, '#b8823e', 4, 3); box(g, 1010, 296, 62, 254, '#3a1e14', 3);
    /* counter top: bowls, condiment trays, the pitcher, chopstick boxes */
    [270, 420, 560, 760, 900].forEach(function (x, i) { bowlS(g, x, 272, 0.95, i % 2 ? '#1d1a1e' : '#9a1e22'); });
    [[340, 266], [640, 266], [840, 266]].forEach(function (p) { box(g, p[0] - 22, p[1] - 10, 44, 20, '#2a1a12', 2, 3); box(g, p[0] - 18, p[1] - 14, 10, 12, '#d6243a', 1.5); box(g, p[0] - 4, p[1] - 14, 10, 12, '#f0d060', 1.5); box(g, p[0] + 10, p[1] - 14, 8, 12, '#3a3020', 1.5); });
    box(g, 1022, 300, 36, 46, 'rgba(200,230,255,.55)', 3, 6); box(g, 1022, 380, 36, 30, '#7a5236', 3, 2);
    for (var t = 250; t <= 950; t += 100) stool(g, t, 400, '#9a1e22');
    [440, 520].forEach(function (y) { stool(g, 1120, y, '#9a1e22'); });
    /* the ticket machine by the door (left), glowing buttons */
    box(g, 110, 600, 92, 150, '#c8ccd2', 4, 6); box(g, 118, 608, 76, 22, '#1a1220', 2, 3); tx(g, '\u98df\u5238', 156, 619, 13, '#7fe8ff', 900);
    for (var r2 = 0; r2 < 4; r2++) for (var c2 = 0; c2 < 3; c2++) { box(g, 120 + c2 * 25, 638 + r2 * 22, 22, 18, ['#f2e6c8', '#ffd860', '#f2a0a0'][(r2 + c2) % 3], 1.5, 2); }
    box(g, 130, 728, 52, 14, '#1a1220', 2, 3); glowAt(g, 156, 660, 70, 'rgba(180,240,255,.18)');
    /* two booth tables on the right (the Suits like the corner) */
    [[920, 640], [920, 790]].forEach(function (p) { box(g, p[0] - 110, p[1] - 44, 40, 88, '#5a1a1c', 3, 6); box(g, p[0] + 70, p[1] - 44, 40, 88, '#5a1a1c', 3, 6); box(g, p[0] - 64, p[1] - 34, 128, 68, '#a8743a', 4, 4); bowlS(g, p[0] - 24, p[1] - 6, 0.7, '#1d1a1e'); bowlS(g, p[0] + 28, p[1] + 4, 0.7, '#9a1e22'); });
    /* water cooler + a plant + a stack of crates */
    box(g, 250, 600, 70, 64, '#8e939c', 5); box(g, 266, 580, 38, 24, '#c9ccd2', 4); jp(g, '\u304a\u6c34', 285, 634, 14, '#2a211c');
    plant(g, 1150, 800, 0.9);
    glowAt(g, 640, 300, 420, 'rgba(255,180,110,.15)');
    shellWalls(g, 230);
  };

  S2P.p6Paint = function (k, g, st) { var fn = P6[k]; if (!fn) return false; g.save(); try { fn(g, st || {}); } finally { g.restore(); } return true; };
  S2P.p6Size = function (k) { var D = P6[k + '_size']; return D || [RW, RH]; };
  S2P.p6H = { INK: INK, RW: RW, RH: RH, box: box, ell: ell, tx: tx, jp: jp, vjp: vjp, glowAt: glowAt, neonTx: neonTx, neonLine: neonLine, plankWall: plankWall, boards: boards, tiles: tiles, carpet: carpet, shellWalls: shellWalls, stool: stool, bowlS: bowlS, plant: plant, shade: shade, lantern: lantern, steamW: steamW, chair: chair, sofaU: sofaU, frosted: frosted, arcadeCab: arcadeCab, crane: crane, medalPusher: medalPusher };
})(typeof window !== 'undefined' ? window : this);
