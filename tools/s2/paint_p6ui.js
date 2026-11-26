/* v6.5.64 FFF_S2P phase 6 UI art (GGD-51): menu boards for the strip counters, food icons, battle backdrops.
 * Painted once into canvases on demand; no loops. */
(function (root) {
  var S2P = root.FFF_S2P = root.FFF_S2P || {};
  var H = S2P.p6H; if (!H) return;
  var INK = H.INK, box = H.box, ell = H.ell, tx = H.tx, jp = H.jp, glowAt = H.glowAt, neonTx = H.neonTx, neonLine = H.neonLine, shade = H.shade;
  var SER = '"Noto Serif CJK JP","BIZ UDPMincho",serif';

  /* ---------------- menu icons (64-unit box) ---------------- */
  var IC = S2P.menuIcons = S2P.menuIcons || {};
  function ramenBowl(g, broth, top) {
    ell(g, 32, 56, 22, 5, 'rgba(40,20,10,.22)', 0);
    g.beginPath(); g.moveTo(6, 30); g.bezierCurveTo(6, 58, 58, 58, 58, 30); g.closePath(); g.fillStyle = '#9a1e22'; g.fill(); g.lineWidth = 2.4; g.strokeStyle = INK; g.stroke();
    g.strokeStyle = '#f2e6c8'; g.lineWidth = 2; g.beginPath(); g.moveTo(10, 40); g.lineTo(54, 40); g.stroke();
    ell(g, 32, 30, 26, 9, broth, 2.4);
    g.save(); g.beginPath(); g.ellipse(32, 30, 24, 7.5, 0, 0, 7); g.clip();
    g.strokeStyle = '#ecc864'; g.lineWidth = 2.2; for (var i = 0; i < 5; i++) { g.beginPath(); g.moveTo(10 + i * 4, 28); g.bezierCurveTo(20 + i * 3, 34, 30, 25, 54 - i * 3, 31); g.stroke(); } g.restore();
    ell(g, 40, 28, 7, 4, '#e0a888', 1.6); ell(g, 24, 31, 5, 3.4, '#f4ead0', 1.4); ell(g, 24, 31, 2.4, 1.8, '#f0a020', 0);
    g.fillStyle = '#1c2a22'; g.fillRect(14, 16, 6, 14); g.strokeStyle = INK; g.lineWidth = 1.4; g.strokeRect(14, 16, 6, 14);
    g.fillStyle = '#5ea83a'; [[32, 26], [35, 24], [29, 25]].forEach(function (p) { g.beginPath(); g.ellipse(p[0], p[1], 2, 1.4, 0, 0, 7); g.fill(); });
    if (top === 'corn') { g.fillStyle = '#f2c230'; [[44, 32], [47, 30], [46, 34], [50, 32]].forEach(function (p) { g.beginPath(); g.arc(p[0], p[1], 1.6, 0, 7); g.fill(); }); }
    g.strokeStyle = 'rgba(240,240,245,.6)'; g.lineWidth = 1.8; g.lineCap = 'round'; [26, 36].forEach(function (x) { g.beginPath(); g.moveTo(x, 14); g.bezierCurveTo(x - 3, 9, x + 3, 6, x, 1); g.stroke(); });
  }
  IC.r_shoyu = function (g) { ramenBowl(g, '#a0602a'); };
  IC.r_miso = function (g) { ramenBowl(g, '#c48a3a', 'corn'); };
  IC.r_tonkotsu = function (g) { ramenBowl(g, '#efe0c0'); };
  IC.r_oolong = function (g) { ell(g, 32, 58, 14, 4, 'rgba(40,20,10,.2)', 0); box(g, 22, 18, 20, 38, 'rgba(160,90,40,.85)', 2.2, 4); box(g, 26, 8, 12, 12, 'rgba(200,220,230,.8)', 2, 2); box(g, 22, 30, 20, 14, '#f2e6c8', 1.6); jp(g, '\u70cf', 32, 37, 10, '#7a1414'); g.fillStyle = 'rgba(255,255,255,.4)'; g.fillRect(25, 22, 3, 30); };
  IC.i_yakitori = function (g) { ell(g, 32, 56, 22, 5, 'rgba(40,20,10,.2)', 0); g.save(); g.translate(32, 32); g.rotate(-0.6); g.strokeStyle = INK; g.lineWidth = 4; g.beginPath(); g.moveTo(0, 28); g.lineTo(0, -30); g.stroke(); g.strokeStyle = '#e8d0a0'; g.lineWidth = 2; g.stroke(); [-18, -4, 10].forEach(function (y, i) { ell(g, 0, y, 9, 6.5, i === 1 ? '#8ab048' : '#a8501c', 2); g.fillStyle = 'rgba(40,14,4,.5)'; g.fillRect(-8, y - 1, 16, 1.6); }); g.restore(); };
  IC.i_karaage = function (g) { ell(g, 32, 56, 22, 5, 'rgba(40,20,10,.2)', 0); [[22, 36, 13], [40, 38, 12], [31, 24, 11]].forEach(function (p) { ell(g, p[0], p[1], p[2], p[2] * 0.82, '#d08a2c', 2.2); g.fillStyle = 'rgba(132,66,12,.4)'; g.beginPath(); g.ellipse(p[0] + 3, p[1] + 2, p[2] * 0.4, p[2] * 0.3, 0, 0, 7); g.fill(); }); g.beginPath(); g.moveTo(46, 22); g.lineTo(56, 26); g.lineTo(50, 32); g.closePath(); g.fillStyle = '#f2e060'; g.fill(); g.lineWidth = 1.6; g.strokeStyle = INK; g.stroke(); };
  IC.i_edamame = function (g) { ell(g, 32, 56, 24, 5, 'rgba(40,20,10,.2)', 0); ell(g, 32, 42, 26, 10, '#3a3020', 2); [[20, 34, -0.4], [34, 30, 0.2], [42, 38, 0.6], [26, 42, 0.1]].forEach(function (d) { g.save(); g.translate(d[0], d[1]); g.rotate(d[2]); g.beginPath(); g.ellipse(0, 0, 11, 5, 0, 0, 7); g.fillStyle = '#7ab048'; g.fill(); g.lineWidth = 1.6; g.strokeStyle = INK; g.stroke(); [-5, 0, 5].forEach(function (b) { g.beginPath(); g.arc(b, 0, 2.2, 0, 7); g.fillStyle = '#b8e080'; g.fill(); }); g.restore(); }); };
  IC.i_onigiri = IC.onigiri;
  IC.i_tea = function (g) { ell(g, 32, 56, 16, 4, 'rgba(40,20,10,.2)', 0); g.beginPath(); g.moveTo(16, 24); g.lineTo(48, 24); g.lineTo(44, 54); g.lineTo(20, 54); g.closePath(); g.fillStyle = '#e8e0cc'; g.fill(); g.lineWidth = 2.2; g.strokeStyle = INK; g.stroke(); ell(g, 32, 24, 16, 4, '#9ab060', 2); g.strokeStyle = 'rgba(240,240,245,.6)'; g.lineWidth = 1.8; [28, 36].forEach(function (x) { g.beginPath(); g.moveTo(x, 18); g.bezierCurveTo(x - 3, 12, x + 3, 8, x, 3); g.stroke(); }); };
  IC.h_rest = function (g) { box(g, 8, 26, 48, 26, '#f4efe6', 2.2, 4); box(g, 8, 20, 48, 10, '#c8a0d8', 2, 3); box(g, 12, 30, 16, 10, '#ffffff', 1.6, 3); g.fillStyle = '#e8c040'; g.beginPath(); g.arc(46, 12, 7, 0, 7); g.fill(); g.fillStyle = '#f4efe6'; g.beginPath(); g.arc(49, 10, 6, 0, 7); g.fill(); };

  /* ---------------- menu boards ---------------- */
  function ramenChrome(g, W, Ht) {
    g.fillStyle = '#2a1410'; g.fillRect(0, 0, W, Ht);
    for (var x = 0; x < W; x += 26) { g.fillStyle = (x / 26 | 0) % 2 ? '#4a2a1c' : '#53301f'; g.fillRect(x, 0, 24, Ht); }
    /* red noren across the top */
    var n = 5, sw = (W - 20) / n; for (var i = 0; i < n; i++) { g.fillStyle = '#9a1e22'; g.beginPath(); g.moveTo(10 + i * sw + 2, 0); g.lineTo(10 + (i + 1) * sw - 2, 0); g.lineTo(10 + (i + 1) * sw - 2, 60); g.quadraticCurveTo(10 + (i + 0.5) * sw, 66, 10 + i * sw + 2, 60); g.closePath(); g.fill(); g.strokeStyle = INK; g.lineWidth = 2; g.stroke(); }
    ['\u3089', '\u30fc', '\u3081', '\u3093', '\u72d0'].forEach(function (c, i) { jp(g, c, 10 + (i + 0.5) * sw, 32, 22, '#f2e6c8', SER); });
    /* cream menu board with a red rule */
    box(g, 16, 72, W - 32, Ht - 96, '#f2e6c8', 4, 8); g.strokeStyle = '#9a1e22'; g.lineWidth = 2; g.strokeRect(24, 80, W - 48, Ht - 112);
    g.save(); g.translate(W - 50, Ht - 52); g.rotate(-0.15); ell(g, 0, 0, 18, 18, '#9a1e22', 1.5); jp(g, '\u72d0', 0, 1, 16, '#f2e6c8', SER); g.restore();
  }
  function izakChrome(g, W, Ht) {
    g.fillStyle = '#1e1410'; g.fillRect(0, 0, W, Ht);
    for (var y = 0; y < Ht; y += 30) { g.fillStyle = (y / 30 | 0) % 2 ? '#3a2618' : '#432c1c'; g.fillRect(0, y, W, 28); }
    /* rope + red lanterns */
    g.strokeStyle = '#c9a06a'; g.lineWidth = 3; g.beginPath(); g.moveTo(0, 18); g.quadraticCurveTo(W / 2, 40, W, 18); g.stroke();
    [70, W / 2, W - 70].forEach(function (x, i) { H.lantern(g, x, 50, 18, '#d6243a', ['\u9152', '\u72f8', '\u5834'][i]); });
    box(g, 16, 92, W - 32, Ht - 116, '#efe2c0', 4, 4); g.strokeStyle = '#3a2618'; g.lineWidth = 2; g.strokeRect(24, 100, W - 48, Ht - 132);
    g.save(); g.translate(W - 52, Ht - 54); g.rotate(-0.12); ell(g, 0, 0, 18, 18, '#3a2618', 1.5); jp(g, '\u72f8', 0, 1, 16, '#efe2c0', SER); g.restore();
  }
  function hotelChrome(g, W, Ht) {
    var lg = g.createLinearGradient(0, 0, W, Ht); lg.addColorStop(0, '#1a0e2a'); lg.addColorStop(0.5, '#2a1040'); lg.addColorStop(1, '#100820'); g.fillStyle = lg; g.fillRect(0, 0, W, Ht);
    glowAt(g, 60, 80, 160, 'rgba(255,80,200,.25)'); glowAt(g, W - 50, 160, 160, 'rgba(80,200,255,.22)');
    neonTx(g, 'HOTEL CHUO', W / 2, 40, 26, '#ff6ad5', '#ff3ab0');
    tx(g, '\u30db\u30c6\u30eb\u4e2d\u592e', W / 2, 70, 11, '#c8f0ff', 700);
    H.frosted(g, 16, 92, W - 32, Ht - 116, 'rgba(220,210,245,.72)');
  }
  function prizeChrome(g, W, Ht) {
    g.fillStyle = '#120a20'; g.fillRect(0, 0, W, Ht);
    for (var i = 0; i < 26; i++) { g.fillStyle = ['rgba(255,90,200,.10)', 'rgba(90,220,255,.10)', 'rgba(255,220,90,.10)'][i % 3]; g.beginPath(); g.arc((i * 97) % W, (i * 151) % Ht, 30 + (i % 4) * 10, 0, 7); g.fill(); }
    neonTx(g, 'PRIZE', W / 2 - 50, 40, 26, '#ffd860', '#ff9020'); neonTx(g, '\u666f\u54c1', W / 2 + 70, 40, 24, '#7fe8ff', '#20a8ff');
    box(g, 16, 82, W - 32, Ht - 106, '#f6f0ff', 4, 10); g.strokeStyle = '#ff6ad5'; g.lineWidth = 2; g.strokeRect(24, 90, W - 48, Ht - 122);
  }
  if (S2P.menuChrome && !S2P._p6Chrome) {
    S2P._p6Chrome = 1;
    var mc0 = S2P.menuChrome;
    S2P.menuChrome = function (g, theme, w, h) { w = w || 390; h = h || 844;
      if (theme === 'ramen') return ramenChrome(g, w, h);
      if (theme === 'izak') return izakChrome(g, w, h);
      if (theme === 'hotel') return hotelChrome(g, w, h);
      if (theme === 'prize') return prizeChrome(g, w, h);
      return mc0.apply(this, arguments); };
  }

  /* ---------------- battle backdrops (720 x 1280, wall to H0 = 330) ---------------- */
  var B = {};
  function hb() { return root.FFF_C2H; }
  B.ramen = function (x) { var C = hb(), WD = 720, H0 = C.H0, HT = 1280;
    H.plankWall(x, 0, 0, WD, H0, '#4a2a1c', '#53301f', 26); x.fillStyle = '#9a1e22'; x.fillRect(0, H0 - 40, WD, 14); x.fillStyle = '#1f120c'; x.fillRect(0, H0 - 26, WD, 26);
    box(x, 200, 30, 320, 56, '#1a1210', 4, 4); box(x, 206, 36, 308, 44, '#f2e6c8', 2, 2); jp(x, '\u3089\u30fc\u3081\u3093 \u72d0\u5c4b', 360, 59, 26, '#9a1e22', SER);
    x.fillStyle = '#140c0a'; x.fillRect(150, 100, 420, 150); glowAt(x, 360, 190, 220, 'rgba(255,190,120,.3)');
    [[280, 200, 50], [440, 206, 44]].forEach(function (p) { box(x, p[0] - p[2], p[1] - 40, p[2] * 2, 70, '#7a7e86', 4, 6); ell(x, p[0], p[1] - 40, p[2], 12, '#a0602a', 3); H.steamW(x, p[0], p[1] - 52, 3, 22); });
    H.lantern(x, 80, 140, 30, '#d6243a', '\u3089'); H.lantern(x, 640, 140, 30, '#d6243a', '\u3081');
    box(x, 0, H0 - 90, WD, 50, '#b8823e', 4, 0); box(x, 0, H0 - 44, WD, 18, '#3a1e14', 3, 0);
    [120, 260, 460, 600].forEach(function (bx, i) { H.bowlS(x, bx, H0 - 70, 1.3, i % 2 ? '#1d1a1e' : '#9a1e22'); });
    C.floor(x, { far: '#3a1c1c', near: '#1e1012', kind: 'tile', line: 'rgba(0,0,0,.35)', n: 8, rows: 10 });
    C.vign(x, 0.5); };
  S2P.p6Battle = function (k, x) { var fn = B[k]; var C = hb(); if (!fn || !C) { x.fillStyle = '#1a1410'; x.fillRect(0, 0, 720, 1280); return; } x.save(); try { fn(x); } finally { x.restore(); } };
  S2P.p6B = B;
})(typeof window !== 'undefined' ? window : this);
