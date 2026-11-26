/* v6.5.63 FFF_S2 paint: Wagashi interior, storefront, battle backdrop, sweets, Chiyo sprite.
 * Canvas2D, ink outlines, two-tone cel shading. Preview-only until Erik approves. */
(function (root) {
  var S2P = root.FFF_S2P = root.FFF_S2P || {};
  var INK = '#1a1220';
  function R(g, x, y, w, h, f, ink, lw) {
    g.fillStyle = f; g.fillRect(x, y, w, h);
    if (ink !== 0) { g.strokeStyle = ink || INK; g.lineWidth = lw || 3; g.strokeRect(x, y, w, h); }
  }
  function rr(g) { g.lineJoin = 'round'; g.lineCap = 'round'; }
  function ellipse(g, x, y, rx, ry, f, ink, lw) {
    g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, Math.PI * 2);
    if (f) { g.fillStyle = f; g.fill(); }
    if (ink !== 0) { g.strokeStyle = ink || INK; g.lineWidth = lw || 2.5; g.stroke(); }
  }
  function txt(g, s, x, y, px, col, wt, al) {
    g.font = (wt || '900 ') + px + 'px "Noto Sans CJK JP","Noto Serif CJK JP",Georgia,serif';
    g.textAlign = al || 'center'; g.textBaseline = 'middle'; g.fillStyle = col; g.fillText(s, x, y);
  }
  function glow(g, x, y, r, col) {
    var gr = g.createRadialGradient(x, y, 0, x, y, r);
    gr.addColorStop(0, col); gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gr; g.fillRect(x - r, y - r, r * 2, r * 2);
  }
  function plank(g, x, y, w, h, c1, c2, step) {
    g.fillStyle = c1; g.fillRect(x, y, w, h);
    for (var i = x, n = 0; i < x + w; i += step, n++) {
      g.fillStyle = n % 2 ? c2 : c1; g.fillRect(i, y, step - 2, h);
      g.fillStyle = 'rgba(0,0,0,.16)'; g.fillRect(i + step - 2, y, 2, h);
    }
  }
  function boards(g, x, y, w, h, c1, c2, bh) {
    for (var j = y, n = 0; j < y + h; j += bh, n++) {
      g.fillStyle = n % 2 ? c1 : c2; g.fillRect(x, j, w, bh);
      g.fillStyle = 'rgba(0,0,0,.14)'; g.fillRect(x, j + bh - 2, w, 2);
    }
  }


  /* ---------- interior 1280x900, Kitsune Udon / Machi Motors density ---------- */
  S2P.interior = function (g) {
    var RW = 1280, RH = 900; rr(g);
    boards(g, 90, 230, RW - 180, 620, '#f3e4cf', '#ebd6bc', 48);
    plank(g, 90, 0, RW - 180, 230, '#8a4a3a', '#965244', 36);
    R(g, 90, 0, RW - 180, 20, '#5a2c28', INK, 0);
    R(g, 90, 212, RW - 180, 18, '#3b2a22', INK, 0);
    /* noren: hang under the beam, lanterns sit OUTSIDE the curtains so the kanji stay clear */
    R(g, 280, 36, 720, 14, '#3b2a22', INK, 3);
    var i, x;
    var glyphs = ['\u548c', '\u83d3', '\u5b50', '\u5343', '\u4ee3', '\u548c', '\u83d3', '\u5b50'];
    for (var i = 0; i < 8; i++) {
      x = 286 + i * 88;
      R(g, x, 50, 80, 128, i % 2 ? '#c45a6a' : '#e8c9c4', INK, 3);
      txt(g, glyphs[i], x + 40, 114, 34, i % 2 ? '#f8ece8' : '#8e3b52', '900 ', 'center');
    }
    /* paper lanterns on the far left and right of the beam, clear of the noren */
    function lan(lx, ly, ch) {
      glow(g, lx, ly + 24, 80, 'rgba(255,180,120,.32)');
      R(g, lx - 4, ly - 40, 8, 12, '#3b2a22', INK, 2);
      ellipse(g, lx, ly, 22, 28, '#f3c9a0', INK, 2.5);
      g.fillStyle = 'rgba(255,255,220,.35)';
      g.beginPath(); g.ellipse(lx - 6, ly - 4, 7, 14, 0, 0, 7); g.fill();
      if (ch) txt(g, ch, lx, ly + 2, 14, '#6a2018', '900 ');
    }
    lan(160, 96, '\u548c'); lan(1120, 96, '\u4ee3');
    /* wall menu, left of the shelves */
    R(g, 130, 248, 150, 210, '#3b2a22', INK, 3);
    R(g, 138, 256, 134, 194, '#f4ead2', INK, 2);
    txt(g, 'MENU', 205, 276, 13, '#8e3b52', '900 ');
    txt(g, '\u3042\u3093\u30ed\u30fc\u30eb', 205, 310, 15, '#5a2c28', '800 ');
    txt(g, '\u00a58', 205, 332, 16, '#8e3b52', '900 ');
    txt(g, '\u56e3\u5b50', 205, 368, 15, '#5a2c28', '800 ');
    txt(g, '\u00a55', 205, 390, 16, '#8e3b52', '900 ');
    txt(g, 'Nails  20% off', 205, 428, 11, '#6a4a38', '700 ');
    /* glass display case (front, with sweets) */
    R(g, 300, 300, 280, 150, '#6b3e2e', INK, 3);
    R(g, 308, 308, 264, 86, '#d8ecf0', INK, 2);
    g.fillStyle = 'rgba(255,255,255,.35)'; g.fillRect(312, 312, 80, 78);
    /* trays inside the case */
    function roll(rx, ry, c) { ellipse(g, rx, ry, 16, 10, c, INK, 1.8); ellipse(g, rx, ry - 2, 7, 5, '#7a3a22', 0); }
    function dang(dx, dy) {
      R(g, dx - 2, dy - 22, 4, 44, '#6b4a33', INK, 1.4);
      ellipse(g, dx, dy - 14, 7, 6, '#f2c4cf', INK, 1.4);
      ellipse(g, dx, dy, 7, 6, '#9ec27a', INK, 1.4);
      ellipse(g, dx, dy + 14, 7, 6, '#f4ead2', INK, 1.4);
    }
    roll(340, 350, '#e8b060'); roll(380, 350, '#d4783a'); roll(420, 350, '#e8b060');
    dang(470, 350); dang(510, 350);
    R(g, 308, 394, 264, 48, '#5c3424', INK, 2);
    g.fillStyle = 'rgba(255,255,255,.18)'; g.fillRect(318, 316, 40, 70);
    /* steamer, right side, with a wisp of steam */
    function steamer(sx, sy) {
      R(g, sx, sy + 70, 90, 18, '#3b2a22', INK, 2);
      for (var k = 0; k < 3; k++) {
        ellipse(g, sx + 45, sy + 62 - k * 22, 42, 10, '#d8c4a0', INK, 2);
        R(g, sx + 8, sy + 42 - k * 22, 74, 20, k % 2 ? '#c4a882' : '#d8c4a0', INK, 2);
      }
      g.strokeStyle = 'rgba(235,235,240,.55)'; g.lineWidth = 3; g.lineCap = 'round';
      [[sx + 24, sy], [sx + 45, sy - 8], [sx + 68, sy]].forEach(function (p) {
        g.beginPath(); g.moveTo(p[0], p[1] + 16); g.bezierCurveTo(p[0] - 8, p[1] + 4, p[0] + 8, p[1] - 4, p[0], p[1] - 14); g.stroke();
      });
    }
    steamer(980, 280);
    /* jar shelf behind the steamer */
    R(g, 820, 250, 150, 130, '#6b3e2e', INK, 3);
    function jar(jx, jy, c, lid) {
      ellipse(g, jx, jy + 8, 22, 12, c, INK, 2);
      R(g, jx - 22, jy - 28, 44, 36, c, INK, 2);
      ellipse(g, jx, jy - 28, 22, 9, lid || '#efe6d2', INK, 2);
    }
    jar(860, 340, '#f2c4cf'); jar(920, 340, '#9ec27a');
    /* back-wall shop sign, BETWEEN the noren and the shelves, not over the curtains */
    R(g, 500, 248, 280, 64, '#f4ead2', INK, 4);
    txt(g, '\u548c\u83d3\u5b50  \u5343\u4ee3', 640, 272, 22, '#8e3b52', '900 ');
    txt(g, 'CHIYO WAGASHI', 640, 296, 12, '#5a2c28', '700 ');
    /* counter */
    R(g, 300, 470, 680, 100, '#7a4a32', INK, 4);
    R(g, 300, 550, 680, 80, '#5c3424', INK, 3);
    /* register */
    R(g, 330, 490, 90, 50, '#2a2430', INK, 2.5);
    R(g, 338, 498, 74, 20, '#8fd6a0', INK, 1.5);
    txt(g, '\u00a50', 375, 509, 11, '#1a3a22', '900 ');
    R(g, 348, 524, 54, 10, '#3a3448', INK, 1.5);
    ellipse(g, 410, 528, 5, 5, '#e0b23a', INK, 1.5);
    /* tea set */
    ellipse(g, 470, 520, 18, 12, '#f4ead2', INK, 2);
    R(g, 458, 500, 24, 20, '#f4ead2', INK, 2);
    ellipse(g, 470, 500, 16, 7, '#efe6d2', INK, 2);
    R(g, 478, 506, 16, 5, '#f4ead2', INK, 1.5); /* spout */
    ellipse(g, 510, 524, 10, 7, '#f4ead2', INK, 2);
    ellipse(g, 534, 524, 10, 7, '#f4ead2', INK, 2);
    g.fillStyle = '#6b8a4a'; g.beginPath(); g.ellipse(510, 522, 6, 3, 0, 0, 7); g.fill();
    g.beginPath(); g.ellipse(534, 522, 6, 3, 0, 0, 7); g.fill();
    /* tray of rolls + dango on the counter */
    R(g, 580, 498, 200, 44, '#efe6d2', INK, 2);
    roll(610, 520, '#e8b060'); roll(646, 520, '#d4783a'); roll(682, 520, '#e8b060');
    dang(730, 518);
    /* clock */
    ellipse(g, 200, 200, 22, 22, '#f4ead2', INK, 2.5);
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(200, 200); g.lineTo(200, 188); g.moveTo(200, 200); g.lineTo(210, 204); g.stroke();
    /* side walls + door band (same shell as Udon) */
    g.fillStyle = '#1b1820'; g.fillRect(0, 0, 90, RH); g.fillRect(RW - 90, 0, 90, RH);
    g.fillRect(0, 850, 580, 50); g.fillRect(700, 850, 580, 50);
    g.strokeStyle = INK; g.lineWidth = 4; g.strokeRect(90, 2, RW - 180, 848);
    g.fillStyle = 'rgba(255,220,160,.10)'; g.fillRect(580, 850, 120, 50);
    var vg = g.createRadialGradient(640, 520, 260, 640, 520, 820);
    vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(10,6,14,.38)');
    g.fillStyle = vg; g.fillRect(0, 0, RW, RH);
    glow(g, 160, 200, 200, 'rgba(255,190,140,.10)');
    glow(g, 1120, 200, 200, 'rgba(255,190,140,.10)');
    glow(g, 640, 520, 280, 'rgba(255,190,140,.08)');
  };

  /* ---------- door overlay for the existing Wagashi north facade (facSento scale) ---------- */
  S2P.facadeDoor = function (g, W0, H0) {
    W0 = W0 || 400; H0 = H0 || 160; rr(g);
    /* dark timber frame, tiled eave, plaster, a proper shop door under noren — sits on the town block's cream placeholder */
    g.fillStyle = '#3b2a22'; g.fillRect(0, 0, W0, H0);
    g.fillStyle = '#2b3240'; g.fillRect(0, 0, W0, 16);
    for (var i = 0; i < W0; i += 16) {
      g.fillStyle = i % 32 ? '#39445a' : '#323b4f';
      g.beginPath(); g.arc(i + 8, 16, 8, Math.PI, 0); g.fill();
    }
    g.strokeStyle = INK; g.lineWidth = 3; g.beginPath(); g.moveTo(0, 17); g.lineTo(W0, 17); g.stroke();
    R(g, 60, 22, 280, 34, '#e9dfc8', INK, 3);
    txt(g, '\u548c\u83d3\u5b50', 130, 39, 20, '#8e3b52', '900 ');
    txt(g, 'CHIYO WAGASHI', 250, 40, 13, '#2a211c', '900 ');
    /* side windows, warm */
    function wlit(x, y, w, h) {
      R(g, x, y, w, h, '#f3d7a0', INK, 3);
      g.beginPath(); g.moveTo(x + w / 2, y); g.lineTo(x + w / 2, y + h); g.moveTo(x, y + h / 2); g.lineTo(x + w, y + h / 2);
      g.strokeStyle = INK; g.lineWidth = 2; g.stroke();
      glow(g, x + w / 2, y + h / 2, 40, 'rgba(255,200,120,.22)');
    }
    wlit(16, 64, 86, 88); wlit(W0 - 102, 64, 86, 88);
    /* lanterns either side of the door */
    function lan2(lx, ly) {
      glow(g, lx, ly + 10, 36, 'rgba(255,170,100,.4)');
      ellipse(g, lx, ly, 12, 16, '#f3c9a0', INK, 2);
      R(g, lx - 3, ly - 20, 6, 8, '#2a1c20', INK, 1.5);
    }
    lan2(118, 78); lan2(282, 78);
    /* door + noren */
    R(g, 148, 62, 104, 98, '#4a2c22', INK, 3);
    R(g, 154, 100, 42, 54, '#d8c4a0', INK, 2);
    R(g, 204, 100, 42, 54, '#d8c4a0', INK, 2);
    ellipse(g, 238, 130, 4, 4, '#e0b23a', INK, 1.5);
    var k, nx;
    for (k = 0; k < 3; k++) {
      nx = 150 + k * 33;
      g.fillStyle = k % 2 ? '#c45a6a' : '#e8c9c4';
      g.beginPath(); g.moveTo(nx, 60); g.lineTo(nx + 30, 60); g.lineTo(nx + 30, 118); g.quadraticCurveTo(nx + 15, 126, nx, 118); g.closePath();
      g.fill(); g.strokeStyle = INK; g.lineWidth = 2; g.stroke();
    }
    R(g, 148, 56, 104, 6, '#3b2a22', INK, 2);
    /* 千 / 代 centered on the left and right flaps (not on the seams) */
    txt(g, '\u5343', 165, 86, 20, '#f8ece8', '900 ');
    txt(g, '\u4ee3', 231, 86, 20, '#8e3b52', '900 ');
  };

  /* standalone storefront kept only as a leftover; the preview uses facadeDoor on the town block */
  S2P.exterior = function (g) {
    S2P.facadeDoor(g, 400, 160);
  };

  /* ---------- battle backdrop: Wagashi row at night, C2BT helpers ---------- */
  function vend(H, x, X, Y) {
    H.R(x, X, Y, 70, 128, '#c0282e', H.INK, 3);
    H.R(x, X + 6, Y + 10, 58, 72, '#1a1520', H.INK, 2);
    var r, c;
    for (r = 0; r < 3; r++) for (c = 0; c < 3; c++) {
      H.R(x, X + 10 + c * 18, Y + 16 + r * 22, 14, 16, (r + c) % 2 ? '#f3d7a0' : '#8fd6ff', 0);
    }
    H.R(x, X + 10, Y + 86, 50, 18, '#2a2430', H.INK, 2);
    for (c = 0; c < 4; c++) H.R(x, X + 14 + c * 12, Y + 90, 8, 6, '#e0b23a', 0);
    H.R(x, X + 14, Y + 108, 42, 14, '#1a1520', H.INK, 2);
    x.fillStyle = 'rgba(255,80,60,.25)'; x.fillRect(X - 6, Y + 20, 82, 40);
  }
  S2P.battle = function (g) {
    var H = (typeof window !== 'undefined' && window.FFF_C2H) || (typeof root !== 'undefined' && root.FFF_C2H);
    var WD = 720, HT = 1280, H0 = 330, x = g;
    /* Lift the shop row 56px so the sidewalk sits under the foe (who stands near H0).
       Unchanged H0 keeps the shared C2BT floor/lane math. */
    var LIFT = 56, FOOT = H0 - LIFT;
    rr(g);
    if (!H) { g.fillStyle = '#141830'; g.fillRect(0, 0, WD, HT); return; }
    H.sky(x, '#141830', '#2c2a48', 48);
    H.skyline(x, '#262840', 21, 150);
    /* -- shop row, sitting on a sidewalk above the horizon -- */
    /* left: shuttered neighbour */
    H.R(x, -8, 148 - LIFT, 168, 182, '#3a3448', H.INK, 3);
    H.R(x, 8, 156 - LIFT, 140, 28, '#2a2434', H.INK, 2);
    H.txt(x, '\u5840', 78, 171 - LIFT, 16, '#c8c0b0', '900 ');
    H.shutter(x, 16, 196 - LIFT, 124, 134, '#6a7080');
    /* centre: Chiyo Wagashi, timber + plaster, lit */
    H.R(x, 156, 118 - LIFT, 360, 212, '#c4a07a', H.INK, 3);
    /* tiled eave */
    x.fillStyle = '#2b3240'; x.fillRect(148, 108 - LIFT, 376, 18);
    for (var ti = 148; ti < 524; ti += 16) { x.fillStyle = ti % 32 ? '#39445a' : '#323b4f'; x.beginPath(); x.arc(ti + 8, 126 - LIFT, 8, Math.PI, 0); x.fill(); }
    x.strokeStyle = H.INK; x.lineWidth = 3; x.beginPath(); x.moveTo(148, 128 - LIFT); x.lineTo(524, 128 - LIFT); x.stroke();
    H.R(x, 200, 136 - LIFT, 272, 36, '#f4ead2', H.INK, 3);
    H.txt(x, '\u548c\u83d3\u5b50  \u5343\u4ee3', 336, 154 - LIFT, 18, '#8e3b52', '900 ');
    /* display window */
    H.win(x, 168, 184 - LIFT, 100, 70, 1, 2);
    /* door + noren */
    H.R(x, 284, 184 - LIFT, 110, 146, '#4a2c22', H.INK, 3);
    H.noren(x, 286, 186 - LIFT, 106, 70, '#c45a6a', '\u5343\u4ee3');
    H.R(x, 296, 258 - LIFT, 40, 64, '#d8c4a0', H.INK, 2);
    H.R(x, 342, 258 - LIFT, 40, 64, '#d8c4a0', H.INK, 2);
    /* right window */
    H.win(x, 408, 184 - LIFT, 92, 70, 1, 2);
    /* vertical sign */
    H.R(x, 508, 140 - LIFT, 22, 120, '#8e3b52', H.INK, 2);
    H.txt(x, '\u548c', 519, 170 - LIFT, 14, '#f4ead2', '900 ');
    H.txt(x, '\u83d3', 519, 200 - LIFT, 14, '#f4ead2', '900 ');
    H.txt(x, '\u5b50', 519, 230 - LIFT, 14, '#f4ead2', '900 ');
    /* lanterns lit */
    H.lantern(x, 250, 168 - LIFT, 26, '#f3c9a0', '');
    H.lantern(x, 430, 168 - LIFT, 26, '#f3c9a0', '');
    /* neighbour tea/noodle shop, half-shutter */
    H.R(x, 530, 150 - LIFT, 130, 180, '#4a3a40', H.INK, 3);
    H.noren(x, 544, 188 - LIFT, 102, 56, '#3a5080', '\u8336');
    H.shutter(x, 544, 250 - LIFT, 102, 80, '#7d8290');
    H.R(x, 544, 158 - LIFT, 102, 24, '#1a1520', H.INK, 2);
    H.neon(x, 548, 160 - LIFT, 94, 20, 'TEA', '255,180,90', 12);
    /* vending + pole on the far right */
    vend(H, x, 648, 200 - LIFT);
    H.pipe(x, [[710, 80 - LIFT], [710, 328 - LIFT]], 6, '#4a4658');
    x.fillStyle = '#2a2430'; x.fillRect(702, 70 - LIFT, 16, 14);
    /* stone sidewalk the shops sit on, so the rider's feet land on ground in front of the door, not in the wall */
    H.R(x, 0, FOOT, WD, H0 - FOOT, '#5c5868', 0);
    x.fillStyle = '#6a6578'; x.fillRect(0, FOOT, WD, 10);
    x.fillStyle = 'rgba(20,16,28,.35)'; x.fillRect(0, H0 - 8, WD, 8);
    var r0 = H.seed(11), i0, xx0, yy0, s0;
    for (i0 = 0; i0 < 70; i0++) {
      yy0 = FOOT + 8 + r0() * (H0 - FOOT - 6); xx0 = r0() * WD; s0 = 8 + (yy0 - FOOT) / 6;
      x.fillStyle = 'rgba(0,0,0,' + (0.08 + r0() * 0.12) + ')';
      x.beginPath(); x.ellipse(xx0, yy0, s0 * 1.8, s0 * 0.4, 0, 0, 6.28); x.fill();
    }
    /* wet asphalt street */
    H.floor(x, { kind: 'asphalt', far: '#3a3a50', near: '#1c1c2a', lanes: [360], seed: 13 });
    /* curb, same 26px band as the default street room */
    H.R(x, 0, H0, WD, 26, '#4a4658', 0);
    /* stone paving continuing a little onto the street edge */
    var r = H.seed(9), yy, xx, s;
    for (var i = 0; i < 80; i++) {
      yy = H0 + 8 + r() * 70; xx = r() * WD; s = 10 + (yy - H0) / 8;
      x.fillStyle = 'rgba(0,0,0,' + (0.06 + r() * 0.1) + ')';
      x.beginPath(); x.ellipse(xx, yy, s * 1.8, s * 0.45, 0, 0, 6.28); x.fill();
    }
    /* puddles / wet reflections of lanterns, neon, vending */
    H.wet(x, [
      [250, 0, 54, '255,190,120', 0.34],
      [430, 0, 54, '255,190,120', 0.34],
      [595, 0, 40, '255,180,90', 0.26],
      [683, 0, 36, '255,80,70', 0.22]
    ], 0.62);
    /* a manhole and a few stone slabs in the foreground */
    x.save(); x.strokeStyle = 'rgba(200,200,220,.28)'; x.lineWidth = 2;
    x.beginPath(); x.ellipse(200, 980, 36, 14, 0, 0, 7); x.stroke();
    x.beginPath(); x.ellipse(200, 980, 20, 7, 0, 0, 7); x.stroke();
    x.restore();
    /* light rain streaks (still) */
    x.strokeStyle = 'rgba(200,210,230,.22)'; x.lineWidth = 1.2;
    var rr2 = H.seed(3);
    for (var i = 0; i < 50; i++) {
      var rx = rr2() * WD, ry = rr2() * HT, rl = 10 + rr2() * 16;
      x.beginPath(); x.moveTo(rx, ry); x.lineTo(rx - 2, ry + rl); x.stroke();
    }
    H.vign(x, 0.55);
  };

  /* ---------- sweets ---------- */
  S2P.sweetRoll = function (g, s) {
    s = s || 1; g.save(); g.scale(s, s); rr(g);
    ellipse(g, 80, 92, 62, 28, 'rgba(40,20,10,.25)', 0);
    ellipse(g, 80, 70, 58, 36, '#e8b060', INK, 3);
    ellipse(g, 80, 58, 50, 24, '#f3c97a', INK, 0);
    g.beginPath(); g.ellipse(80, 58, 18, 12, 0, 0, Math.PI * 2);
    g.fillStyle = '#7a3a22'; g.fill(); g.strokeStyle = INK; g.lineWidth = 2; g.stroke();
    g.beginPath(); g.moveTo(40, 70); g.quadraticCurveTo(80, 40, 120, 70);
    g.strokeStyle = 'rgba(90,40,20,.45)'; g.lineWidth = 3; g.stroke();
    g.restore();
  };
  S2P.dango = function (g, s) {
    s = s || 1; g.save(); g.scale(s, s); rr(g);
    g.strokeStyle = INK; g.lineWidth = 4;
    g.beginPath(); g.moveTo(40, 20); g.lineTo(40, 130); g.stroke();
    ellipse(g, 40, 42, 22, 20, '#f2c4cf', INK, 3);
    ellipse(g, 40, 78, 22, 20, '#9ec27a', INK, 3);
    ellipse(g, 40, 114, 22, 20, '#f4ead2', INK, 3);
    ellipse(g, 32, 38, 6, 5, 'rgba(255,255,255,.5)', 0);
    g.restore();
  };
  S2P.rollSplit = function (g, s) {
    s = s || 1; g.save(); g.scale(s, s); rr(g);
    ellipse(g, 50, 70, 32, 26, '#e8b060', INK, 3);
    ellipse(g, 110, 70, 32, 26, '#e8b060', INK, 3);
    g.beginPath(); g.moveTo(70, 62); g.quadraticCurveTo(80, 90, 90, 62);
    g.quadraticCurveTo(80, 50, 70, 62);
    g.fillStyle = '#7a3a22'; g.fill(); g.strokeStyle = INK; g.lineWidth = 2; g.stroke();
    g.restore();
  };

  /* ---------- Chiyo: blit the yk-baked Hina-rig sheets (club-staff proportions) ---------- */
  S2P.sheets = {};
  function blit(g, im, sx, sy, sw, sh, dx, dy, dw, dh) {
    if (!im) return false;
    g.drawImage(im, sx, sy, sw, sh, dx, dy, dw || sw, dh || sh);
    return true;
  }
  S2P.chiyoIdle = function (g) {
    var im = S2P.sheets.idle || S2P.sheets.walk;
    g.fillStyle = '#2a2030'; g.fillRect(0, 0, 160, 200);
    if (!blit(g, im, 0, 0, 208, 272, -10, -16, 180, 236)) {
      g.fillStyle = '#f4ead2'; g.font = '12px sans-serif'; g.fillText('chiyo sheet missing', 10, 100);
    }
  };
  S2P.chiyoWalk = function (g) {
    var im = S2P.sheets.walk;
    g.fillStyle = '#2a2030'; g.fillRect(0, 0, 560, 200);
    if (!im) { g.fillStyle = '#f4ead2'; g.font = '12px sans-serif'; g.fillText('chiyo walk missing', 10, 100); return; }
    for (var c = 0; c < 4; c++) blit(g, im, c * 208, 0, 208, 272, c * 140 - 8, -16, 150, 196);
  };
  S2P.chiyoFacings = function (g) {
    var im = S2P.sheets.idle || S2P.sheets.walk;
    g.fillStyle = '#2a2030'; g.fillRect(0, 0, 720, 220);
    if (!im) return;
    for (var r = 0; r < 4; r++) blit(g, im, 0, r * 272, 208, 272, 20 + r * 175, -8, 160, 210);
  };
  S2P.chiyoTalk = function (g) {
    var im = S2P.sheets.map || S2P.sheets.idle || S2P.sheets.walk;
    g.fillStyle = '#2a2030'; g.fillRect(0, 0, 200, 240);
    if (!im) return;
    if (S2P.sheets.map) blit(g, im, 0, 0, im.naturalWidth || im.width, im.naturalHeight || im.height, 10, 10, 180, 220);
    else blit(g, im, 0, 0, 208, 272, -4, -8, 200, 250);
  };
})(typeof window !== 'undefined' ? window : this);
