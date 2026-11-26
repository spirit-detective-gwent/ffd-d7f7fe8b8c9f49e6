/* C2BT paint helpers, extracted for Seal 2 preview battle backdrops. Not wired. */
(function (root) {
var WD = 720, HT = 1280, INK = '#1a1220';
function rr(x, a, b) { return a + Math.random() * (b - a); }
function seed(s) { var v = s; return function () { v = (v * 16807) % 2147483647; return (v - 1) / 2147483646; }; }
function R(x, X, Y, w, h, f, ink, lw) { x.fillStyle = f; x.fillRect(X, Y, w, h); if (ink !== 0) { x.strokeStyle = ink || INK; x.lineWidth = lw || 3; x.strokeRect(X, Y, w, h); } }
function poly(x, P, f, ink, lw) { x.beginPath(); x.moveTo(P[0][0], P[0][1]); for (var i = 1; i < P.length; i++) x.lineTo(P[i][0], P[i][1]); x.closePath(); if (f) { x.fillStyle = f; x.fill(); } if (ink !== 0) { x.strokeStyle = ink || INK; x.lineWidth = lw || 3; x.stroke(); } }
function lg(x, y0, y1, a, b) { var g = x.createLinearGradient(0, y0, 0, y1); g.addColorStop(0, a); g.addColorStop(1, b); return g; }
function pool(x, X, Y, rx, ry, col, a) { x.save(); x.globalCompositeOperation = 'lighter'; x.translate(X, Y); x.scale(1, ry / rx); var g = x.createRadialGradient(0, 0, 0, 0, 0, rx); g.addColorStop(0, 'rgba(' + col + ',' + a + ')'); g.addColorStop(0.5, 'rgba(' + col + ',' + a * 0.35 + ')'); g.addColorStop(1, 'rgba(' + col + ',0)'); x.fillStyle = g; x.beginPath(); x.arc(0, 0, rx, 0, 6.2832); x.fill(); x.restore(); }
function streak(x, X, Y, w, h, col, a) { x.save(); x.globalCompositeOperation = 'lighter'; var g = x.createLinearGradient(0, Y, 0, Y + h); g.addColorStop(0, 'rgba(' + col + ',' + a + ')'); g.addColorStop(1, 'rgba(' + col + ',0)'); x.fillStyle = g; x.beginPath(); x.ellipse(X, Y + h / 2, w / 2, h / 2, 0, 0, 6.2832); x.fill(); x.restore(); }
function txt(x, s, X, Y, px, col, font, al) { x.font = (font || '900 ') + px + 'px "Noto Sans CJK JP","Noto Serif CJK JP",system-ui,sans-serif'; x.textAlign = al || 'center'; x.textBaseline = 'middle'; x.fillStyle = col; x.fillText(s, X, Y); }
/* the floor: perspective lanes converging on a vanishing point above the wall, like the Ch1 rooms */
var H0 = 330, VP = [360, -260];
function fx0(u, y) { var k = (y - VP[1]) / (HT - VP[1]); return VP[0] + (u - VP[0]) * k; }
function floor(x, o) { var r = seed(o.seed || 7);
  x.fillStyle = lg(x, H0, HT, o.far, o.near); x.fillRect(0, H0, WD, HT - H0);
  var n = o.cols || 9, i, j, u;
  if (o.kind === 'board' || o.kind === 'tile' || o.kind === 'stone') {
    for (i = -n; i <= n * 2; i++) { u = -360 + i * (1440 / n) ; x.beginPath(); x.moveTo(fx0(u, H0), H0); x.lineTo(fx0(u, HT), HT); x.strokeStyle = o.line; x.lineWidth = o.kind === 'tile' ? 3 : 2; x.stroke(); }
    var rows = o.rows || 14; for (j = 0; j < rows; j++) { var q = j / rows, y = H0 + (HT - H0) * Math.pow(q, 1.55); if (o.kind === 'board') { for (i = -n; i <= n * 2; i++) { if (r() < 0.55) continue; u = -360 + (i + 0.5) * (1440 / n); var ya = y, yb = H0 + (HT - H0) * Math.pow((j + 1) / rows, 1.55); x.beginPath(); x.moveTo(fx0(u - 1440 / n / 2, ya), ya); x.lineTo(fx0(u + 1440 / n / 2, ya), ya); x.strokeStyle = o.line; x.lineWidth = 1.5; x.stroke(); } }
      else { x.beginPath(); x.moveTo(0, y); x.lineTo(WD, y); x.strokeStyle = o.line; x.lineWidth = o.kind === 'tile' ? 3 : 2; x.stroke(); } }
    if (o.kind === 'stone') for (i = 0; i < 160; i++) { var yy = H0 + (HT - H0) * Math.pow(r(), 1.3), xx = r() * WD, s = 6 + (yy - H0) / 40; x.fillStyle = 'rgba(0,0,0,' + (0.05 + r() * 0.08) + ')'; x.beginPath(); x.ellipse(xx, yy, s * 1.6, s * 0.5, 0, 0, 6.28); x.fill(); } }
  if (o.kind === 'asphalt') { for (i = 0; i < 900; i++) { var ay = H0 + r() * (HT - H0); x.fillStyle = 'rgba(255,255,255,' + r() * 0.035 + ')'; x.fillRect(r() * WD, ay, 2, 2); }
    (o.lanes || []).forEach(function (L) { for (j = 0; j < 10; j++) { var y1 = H0 + (HT - H0) * Math.pow(j / 10, 1.5), y2 = H0 + (HT - H0) * Math.pow((j + 0.55) / 10, 1.5); poly(x, [[fx0(L - 8, y1), y1], [fx0(L + 8, y1), y1], [fx0(L + 8, y2), y2], [fx0(L - 8, y2), y2]], o.paint || 'rgba(230,220,180,.55)', 0); } });
    (o.zebra || []).forEach(function (Z) { for (i = 0; i < 9; i++) { var u1 = -100 + i * 110, ya = Z[0], yb = Z[1]; poly(x, [[fx0(u1, ya), ya], [fx0(u1 + 55, ya), ya], [fx0(u1 + 55, yb), yb], [fx0(u1, yb), yb]], 'rgba(220,222,230,.42)', 0); } }); }
  if (o.kind === 'clay') { x.fillStyle = 'rgba(0,0,0,.06)'; for (i = 0; i < 400; i++) x.fillRect(r() * WD, H0 + r() * (HT - H0), 3, 2); }
  /* a soft dark at the wall foot (contact shadow) */
  x.fillStyle = lg(x, H0, H0 + 70, 'rgba(10,6,16,.45)', 'rgba(10,6,16,0)'); x.fillRect(0, H0, WD, 70); }
function wet(x, srcs, k) { /* light reflections on a wet floor: long vertical streaks under each light */ srcs.forEach(function (s) { streak(x, s[0], H0 + 6, s[2] || 46, (HT - H0) * (k || 0.55), s[3] || '255,190,120', s[4] || 0.32); }); }
function vign(x, a) { var g = x.createRadialGradient(360, 760, 300, 360, 760, 900); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(8,4,14,' + (a || 0.6) + ')'); x.fillStyle = g; x.fillRect(0, 0, WD, HT); }
function grade(x, top, bot) { x.save(); x.globalCompositeOperation = 'soft-light'; x.fillStyle = lg(x, 0, HT, top, bot); x.fillRect(0, 0, WD, HT); x.restore(); }
/* props */
function lantern(x, X, Y, s, col, ch) { x.save(); x.translate(X, Y); x.beginPath(); x.moveTo(0, -s * 1.15); x.lineTo(0, -s * 0.7); x.strokeStyle = INK; x.lineWidth = 2; x.stroke();
  R(x, -s * 0.36, -s * 0.72, s * 0.72, s * 0.14, '#2a1c20'); R(x, -s * 0.36, s * 0.58, s * 0.72, s * 0.14, '#2a1c20');
  x.beginPath(); x.ellipse(0, 0, s * 0.5, s * 0.64, 0, 0, 6.2832); x.fillStyle = col; x.fill(); x.lineWidth = 3; x.strokeStyle = INK; x.stroke();
  x.fillStyle = 'rgba(255,255,220,.35)'; x.beginPath(); x.ellipse(-s * 0.12, -s * 0.06, s * 0.16, s * 0.42, 0, 0, 6.2832); x.fill();
  for (var i = -2; i <= 2; i++) { x.beginPath(); x.ellipse(0, i * s * 0.22, s * 0.5 * Math.cos(i * 0.4), s * 0.03, 0, 0, 6.28); x.strokeStyle = 'rgba(60,20,20,.35)'; x.lineWidth = 1.5; x.stroke(); }
  if (ch) txt(x, ch, 0, 2, s * 0.42, '#2a0a0a'); x.restore(); }
function win(x, X, Y, w, h, lit, cols) { R(x, X, Y, w, h, lit ? lg(x, Y, Y + h, '#ffd98c', '#e79a4a') : '#2a3048'); if (cols) for (var i = 1; i < cols; i++) { x.beginPath(); x.moveTo(X + w * i / cols, Y); x.lineTo(X + w * i / cols, Y + h); x.strokeStyle = INK; x.lineWidth = 2; x.stroke(); } }
function neon(x, X, Y, w, h, s, col, px) { R(x, X, Y, w, h, '#14101c'); x.save(); x.shadowColor = 'rgb(' + col + ')'; x.shadowBlur = 18; txt(x, s, X + w / 2, Y + h / 2, px || h * 0.6, 'rgb(' + col + ')'); x.restore(); txt(x, s, X + w / 2, Y + h / 2, px || h * 0.6, 'rgba(255,255,255,.75)'); }
function noren(x, X, Y, w, h, col, s) { var n = 3; for (var i = 0; i < n; i++) poly(x, [[X + i * w / n + 2, Y], [X + (i + 1) * w / n - 2, Y], [X + (i + 1) * w / n - 2, Y + h], [X + i * w / n + 2, Y + h]], col); if (s) txt(x, s, X + w / 2, Y + h * 0.45, h * 0.42, '#fff6e6'); R(x, X - 6, Y - 8, w + 12, 10, '#3a2618'); }
function shutter(x, X, Y, w, h, c) { R(x, X, Y, w, h, c || '#7d8290'); for (var y = Y + 10; y < Y + h; y += 12) { x.beginPath(); x.moveTo(X, y); x.lineTo(X + w, y); x.strokeStyle = 'rgba(20,20,30,.4)'; x.lineWidth = 2; x.stroke(); } }
function pipe(x, P, w, c) { x.beginPath(); x.moveTo(P[0][0], P[0][1]); for (var i = 1; i < P.length; i++) x.lineTo(P[i][0], P[i][1]); x.lineCap = 'round'; x.lineJoin = 'round'; x.strokeStyle = INK; x.lineWidth = w + 6; x.stroke(); x.strokeStyle = c; x.lineWidth = w; x.stroke(); x.strokeStyle = 'rgba(255,255,255,.18)'; x.lineWidth = w * 0.3; x.stroke(); }
function bricks(x, X, Y, w, h, c, l) { R(x, X, Y, w, h, c, 0); x.strokeStyle = l; x.lineWidth = 2; for (var j = 0, y = Y; y < Y + h; y += 26, j++) { x.beginPath(); x.moveTo(X, y); x.lineTo(X + w, y); x.stroke(); for (var xx = X + (j % 2) * 30; xx < X + w; xx += 60) { x.beginPath(); x.moveTo(xx, y); x.lineTo(xx, y + 26); x.stroke(); } } }
function sky(x, a, b, stars) { x.fillStyle = lg(x, 0, H0, a, b); x.fillRect(0, 0, WD, H0); if (stars) { var r = seed(3); for (var i = 0; i < stars; i++) { x.fillStyle = 'rgba(255,255,255,' + r() * 0.6 + ')'; x.fillRect(r() * WD, r() * H0 * 0.5, 2, 2); } } }
function skyline(x, c, seedN, top) { var r = seed(seedN || 5), X = 0; while (X < WD) { var w = 60 + r() * 90, h = (top || 140) + r() * 120; R(x, X, H0 - h, w, h, c, INK, 2); for (var yy = H0 - h + 14; yy < H0 - 20; yy += 22) for (var xx = X + 8; xx < X + w - 12; xx += 18) if (r() < 0.35) R(x, xx, yy, 9, 12, r() < 0.7 ? '#f6c983' : '#8fd6ff', 0); X += w; } }
  root.FFF_C2H = { WD: WD, HT: HT, INK: INK, H0: H0, VP: VP, rr: rr, seed: seed, R: R, poly: poly, lg: lg, pool: pool, streak: streak, txt: txt, fx0: fx0, floor: floor, wet: wet, vign: vign, grade: grade, lantern: lantern, win: win, neon: neon, noren: noren, shutter: shutter, pipe: pipe, bricks: bricks, sky: sky, skyline: skyline };
})(typeof window !== 'undefined' ? window : this);
