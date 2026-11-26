/* v6.5.63 FFF_S2P phase 3: Funayado lookout façade, interior, and Above the Boat battle rooms.
 * Canvas2D, ink outlines, two-tone cel. Preview-first; no new always-running loops. */
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
      for (var i = x + ((n * 97) % 220); i < x + w; i += 220) g.fillRect(i, j, 2, bh);
    }
  }
  function shell(g, RW, RH) {
    g.fillStyle = '#1b1820'; g.fillRect(0, 0, 90, RH); g.fillRect(RW - 90, 0, 90, RH);
    g.fillRect(0, 850, 580, 50); g.fillRect(700, 850, 580, 50);
    g.strokeStyle = INK; g.lineWidth = 4; g.strokeRect(90, 2, RW - 180, 848);
    g.fillStyle = 'rgba(255,220,160,.10)'; g.fillRect(580, 850, 120, 50);
    var vg = g.createRadialGradient(640, 520, 260, 640, 520, 820);
    vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(10,6,14,.38)');
    g.fillStyle = vg; g.fillRect(0, 0, RW, RH);
  }
  function lifeRing(g, x, y, r) {
    g.lineWidth = Math.max(6, r * 0.38);
    g.strokeStyle = INK; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.stroke();
    g.strokeStyle = '#e8e0d4'; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.stroke();
    g.strokeStyle = '#c4302a'; g.lineWidth = Math.max(5, r * 0.32);
    for (var i = 0; i < 4; i++) {
      var a = i * Math.PI / 2 - 0.28, b = a + 0.56;
      g.beginPath(); g.arc(x, y, r, a, b); g.stroke();
    }
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.arc(x, y, r + g.lineWidth, 0, Math.PI * 2); g.stroke();
  }
  function flowerBoat(g, x, y, w, h) {
    /* white hull, orange gunwale, dense flower cargo — matches the town canal boat */
    g.beginPath();
    g.moveTo(x + w * 0.06, y + h * 0.55);
    g.quadraticCurveTo(x + w * 0.5, y + h * 1.08, x + w * 0.94, y + h * 0.55);
    g.lineTo(x + w * 0.9, y + h * 0.22);
    g.quadraticCurveTo(x + w * 0.5, y + h * 0.05, x + w * 0.1, y + h * 0.22);
    g.closePath();
    g.fillStyle = '#eceae4'; g.fill();
    g.strokeStyle = INK; g.lineWidth = 2.2; g.stroke();
    g.beginPath();
    g.moveTo(x + w * 0.1, y + h * 0.26);
    g.quadraticCurveTo(x + w * 0.5, y + h * 0.12, x + w * 0.9, y + h * 0.26);
    g.strokeStyle = '#c45a32'; g.lineWidth = Math.max(3, h * 0.09); g.stroke();
    /* cargo well */
    g.save();
    g.beginPath();
    g.moveTo(x + w * 0.16, y + h * 0.3);
    g.quadraticCurveTo(x + w * 0.5, y + h * 0.18, x + w * 0.84, y + h * 0.3);
    g.lineTo(x + w * 0.86, y + h * 0.52);
    g.quadraticCurveTo(x + w * 0.5, y + h * 0.7, x + w * 0.14, y + h * 0.52);
    g.closePath();
    g.clip();
    g.fillStyle = '#1a2018'; g.fill();
    var cols = ['#c43a3a', '#e07040', '#e8d060', '#f0e8e0', '#d4608a', '#c09030', '#e8a0a0', '#f4f0c8'];
    var i, n = Math.max(80, (w * h) / 14);
    for (i = 0; i < n; i++) {
      var fx = x + w * (0.16 + (i * 37 % 70) / 100), fy = y + h * (0.24 + (i * 53 % 42) / 100);
      g.fillStyle = cols[i % cols.length];
      g.fillRect(fx, fy, 2 + (i % 3), 2 + ((i * 3) % 3));
    }
    g.restore();
    /* reflection */
    g.globalAlpha = 0.28;
    g.beginPath();
    g.moveTo(x + w * 0.1, y + h * 0.62);
    g.quadraticCurveTo(x + w * 0.5, y + h * 0.92, x + w * 0.9, y + h * 0.62);
    g.strokeStyle = 'rgba(200,210,230,.5)'; g.lineWidth = 2; g.stroke();
    g.globalAlpha = 1;
  }
  function canalView(g, x, y, w, h) {
    /* night canal + flower boat, clipped to a window pane */
    g.save();
    g.beginPath(); g.rect(x, y, w, h); g.clip();
    var lg = g.createLinearGradient(x, y, x, y + h);
    lg.addColorStop(0, '#151828'); lg.addColorStop(0.45, '#1a2438'); lg.addColorStop(1, '#0c1424');
    g.fillStyle = lg; g.fillRect(x, y, w, h);
    /* far south bank flowers */
    R(g, x, y + h * 0.62, w, h * 0.14, '#3a2a28', 0);
    var i, cols = ['#8a3030', '#6a2020', '#a04040', '#c8c8c0', '#704040'];
    for (i = 0; i < 40; i++) {
      g.fillStyle = cols[i % cols.length];
      g.fillRect(x + (i * 17 % w), y + h * 0.62 + (i * 13 % 14), 3, 3);
    }
    R(g, x, y + h * 0.74, w, 6, '#4a4a58', 0);
    /* water ripples */
    g.strokeStyle = 'rgba(160,200,230,.18)'; g.lineWidth = 1.4;
    for (i = 0; i < 5; i++) {
      var yy = y + h * (0.38 + i * 0.07);
      g.beginPath(); g.moveTo(x, yy); g.quadraticCurveTo(x + w * 0.5, yy + 3, x + w, yy - 2); g.stroke();
    }
    flowerBoat(g, x + w * 0.12, y + h * 0.22, w * 0.78, h * 0.48);
    /* lamp streak */
    g.fillStyle = 'rgba(255,190,100,.16)';
    g.fillRect(x + w * 0.55, y + h * 0.5, 10, h * 0.3);
    g.restore();
  }
  function winPane(g, x, y, w, h, lit, scene) {
    R(g, x - 4, y - 4, w + 8, h + 10, '#3a2a22', INK, 2.5);
    if (scene) canalView(g, x, y, w, h);
    else if (lit) {
      var lg = g.createLinearGradient(x, y, x, y + h);
      lg.addColorStop(0, '#ffe7b0'); lg.addColorStop(1, '#e29a4a');
      g.fillStyle = lg; g.fillRect(x, y, w, h);
      g.fillStyle = 'rgba(255,255,230,.28)'; g.fillRect(x + 2, y + 2, w * 0.35, h * 0.55);
    } else {
      R(g, x, y, w, h, '#2a3048', 0);
      g.fillStyle = 'rgba(80,100,140,.25)'; g.fillRect(x + 2, y + 2, w * 0.4, h * 0.45);
    }
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(x + w / 2, y); g.lineTo(x + w / 2, y + h); g.stroke();
    g.beginPath(); g.moveTo(x, y + h * 0.45); g.lineTo(x + w, y + h * 0.45); g.stroke();
    R(g, x - 6, y + h, w + 12, 6, '#4a382c', INK, 1.5);
  }
  function rain(g, H, n, seedN) {
    if (!H) return;
    var r = H.seed(seedN || 5), i, x, y;
    g.strokeStyle = 'rgba(180,200,230,.28)'; g.lineWidth = 1.2;
    for (i = 0; i < (n || 50); i++) {
      x = r() * 720; y = r() * 1280;
      g.beginPath(); g.moveTo(x, y); g.lineTo(x - 6, y + 18); g.stroke();
    }
  }
  function crate(g, x, y, w, h, label) {
    R(g, x, y, w, h, '#8a4a28', INK, 2.5);
    R(g, x + 6, y + 6, w - 12, 16, '#6a3418', INK, 1.5);
    if (label) txt(g, label, x + w / 2, y + 14, 10, '#f0e4c8');
    R(g, x + 8, y + h - 22, 22, 14, '#2a2018', 0);
    R(g, x + w - 30, y + h - 22, 22, 14, '#2a2018', 0);
    g.strokeStyle = 'rgba(0,0,0,.25)'; g.lineWidth = 1.5;
    g.beginPath(); g.moveTo(x + 4, y + h * 0.55); g.lineTo(x + w - 4, y + h * 0.55); g.stroke();
  }

  /* ---------- façade: 船宿 on the east boardwalk, 360 x 220 ---------- */
  S2P.boatSouth = function (g, W0, H0) {
    W0 = W0 || 360; H0 = H0 || 220; rr(g);
    /* night behind the east wall cut */
    R(g, 0, 0, W0, H0, '#14101c', 0);
    /* tin roof */
    R(g, 4, 2, W0 - 8, 28, '#3a4048', INK, 2);
    g.fillStyle = '#4a5058';
    var i;
    for (i = 0; i < 14; i++) g.fillRect(10 + i * 25, 4, 18, 22);
    g.fillStyle = 'rgba(0,0,0,.25)';
    for (i = 0; i < 14; i++) g.fillRect(10 + i * 25 + 18, 4, 2, 22);
    R(g, 0, 24, W0, 10, '#2a2018', INK, 2);
    /* timber walls, a shade duskier than Minato-sō so the lookout reads as an add-on */
    plank(g, 6, 34, W0 - 12, 146, '#4a3428', '#3e2c22', 36);
    R(g, 6, 34, W0 - 12, 8, '#2a2018', 0);
    /* fascia sign */
    R(g, 88, 38, 184, 28, '#f0e4c8', INK, 3);
    txt(g, '\u8239\u5c0b', 156, 52, 16, '#5a2a28');
    txt(g, 'FUNAYADO', 228, 52, 10, '#3a2a22');
    /* upper lookout windows, lit */
    winPane(g, 24, 72, 70, 52, 1, 0);
    winPane(g, 110, 72, 70, 52, 1, 0);
    glow(g, 59, 98, 36, 'rgba(255,190,100,.22)');
    glow(g, 145, 98, 36, 'rgba(255,190,100,.22)');
    /* door porch on the boardwalk (right bay, over the old cream doors) */
    R(g, 230, 70, 116, 114, '#2a2018', INK, 3);
    /* transom */
    winPane(g, 248, 76, 80, 22, 1, 0);
    /* door leaves */
    R(g, 246, 102, 40, 78, '#5a3a28', INK, 2);
    R(g, 290, 102, 40, 78, '#523626', INK, 2);
    R(g, 252, 110, 28, 36, '#3a281c', INK, 1.5);
    R(g, 296, 110, 28, 36, '#3a281c', INK, 1.5);
    ellipse(g, 282, 142, 3, 3, '#c8b070', INK, 1);
    ellipse(g, 294, 142, 3, 3, '#c8b070', INK, 1);
    /* lamp over the door */
    R(g, 278, 58, 6, 16, '#3a3e48', INK, 1.5);
    R(g, 268, 50, 26, 12, '#2a2c34', INK, 2);
    R(g, 272, 52, 18, 8, '#f0d080', 0);
    glow(g, 288, 70, 50, 'rgba(255,190,90,.4)');
    /* life ring + hook + rope on the left wall */
    lifeRing(g, 54, 160, 16);
    R(g, 200, 150, 8, 10, '#3a3e48', INK, 1.5);
    g.strokeStyle = '#c4a060'; g.lineWidth = 2.5;
    g.beginPath(); g.arc(206, 168, 10, 0.2, Math.PI * 1.6); g.stroke();
    g.beginPath(); g.arc(206, 168, 6, 0.4, Math.PI * 1.4); g.stroke();
    /* wet boardwalk apron */
    plank(g, 0, 180, W0, 40, '#6a4a36', '#5a3e2e', 28);
    g.fillStyle = 'rgba(80,100,140,.16)';
    g.fillRect(20, 196, 70, 8); g.fillRect(200, 200, 90, 6);
    /* posts of a short porch rail */
    R(g, 12, 168, 8, 28, '#3a2a22', INK, 1.5);
    R(g, 200, 168, 8, 28, '#3a2a22', INK, 1.5);
    g.strokeStyle = '#8a909c'; g.lineWidth = 3;
    g.beginPath(); g.moveTo(16, 172); g.lineTo(204, 172); g.stroke();
    g.strokeStyle = INK; g.lineWidth = 4; g.strokeRect(1, 1, W0 - 2, H0 - 2);
  };

  /* ---------- interior: lookout room, 1280 x 900 ---------- */
  S2P.boatLookout = function (g, cleared) {
    var RW = 1280, RH = 900; rr(g);
    /* timber room, scored floor — not a wet street */
    R(g, 0, 0, RW, RH, '#2a2018', 0);
    boards(g, 90, 80, 1100, 280, '#4a3428', '#3e2c22', 28);
    /* floor */
    plank(g, 90, 480, 1100, 370, '#6a4e3a', '#5c4432', 48);
    g.fillStyle = 'rgba(0,0,0,.08)';
    var i, j;
    for (i = 0; i < 18; i++) {
      var fy = 500 + i * 20;
      g.fillRect(90, fy, 1100, 1.5);
    }
    /* scored concrete-like wear only in the work aisle, oil-free wood scuffs */
    g.fillStyle = 'rgba(20,12,8,.16)';
    g.beginPath(); g.ellipse(420, 700, 50, 14, 0, 0, Math.PI * 2); g.fill();
    g.beginPath(); g.ellipse(880, 760, 40, 10, 0.2, 0, Math.PI * 2); g.fill();
    /* back wall lintel + three canal windows */
    R(g, 90, 80, 1100, 18, '#2a2018', INK, 2);
    R(g, 200, 110, 200, 18, '#f0e4c8', INK, 3);
    txt(g, '\u8239\u5c0b  \u00b7  \u671b\u697c', 300, 119, 14, '#5a2a28');
    winPane(g, 160, 150, 280, 210, 1, 1);
    winPane(g, 500, 150, 280, 210, 1, 1);
    winPane(g, 840, 150, 280, 210, 1, 1);
    /* binoculars on the centre sill */
    R(g, 610, 348, 60, 16, '#2a2c34', INK, 2);
    ellipse(g, 622, 348, 12, 10, '#1a2028', INK, 2);
    ellipse(g, 658, 348, 12, 10, '#1a2028', INK, 2);
    R(g, 628, 342, 24, 8, '#3a3e48', INK, 1.5);
    /* freight schedule / map on the left wall */
    R(g, 110, 390, 130, 160, '#d8c8a0', INK, 2);
    txt(g, '\u8ca0\u7269', 175, 410, 13, '#5a2a28');
    g.strokeStyle = '#6a5a40'; g.lineWidth = 1.4;
    for (i = 0; i < 7; i++) { g.beginPath(); g.moveTo(124, 430 + i * 16); g.lineTo(226, 430 + i * 16); g.stroke(); }
    g.fillStyle = '#a03030'; g.fillRect(128, 436, 8, 8); g.fillRect(128, 468, 8, 8);
    g.fillStyle = '#2a5080'; g.fillRect(128, 500, 8, 8);
    /* radio desk, left */
    R(g, 250, 500, 320, 24, '#3a2a22', INK, 2); /* top */
    R(g, 260, 524, 300, 110, '#4a3428', INK, 2.5);
    R(g, 270, 548, 70, 70, '#2a2018', INK, 1.5);
    R(g, 470, 548, 70, 70, '#2a2018', INK, 1.5);
    /* radio set */
    R(g, 280, 454, 140, 50, '#2a2c34', INK, 2);
    ellipse(g, 300, 478, 8, 8, '#3a6a3a', INK, 1.5);
    ellipse(g, 322, 478, 8, 8, '#6a3a2a', INK, 1.5);
    R(g, 340, 468, 64, 22, '#1a2018', INK, 1.5);
    /* frequency ticks */
    g.strokeStyle = '#c8c0a0'; g.lineWidth = 1;
    for (i = 0; i < 8; i++) { g.beginPath(); g.moveTo(344 + i * 7, 472); g.lineTo(344 + i * 7, 484); g.stroke(); }
    /* mic on a stand */
    R(g, 430, 470, 6, 34, '#3a3e48', INK, 1.5);
    ellipse(g, 433, 464, 10, 14, '#2a2c34', INK, 2);
    /* log book, thermos, mug, ashtray */
    R(g, 470, 478, 54, 36, '#f0e4c8', INK, 2);
    g.strokeStyle = '#6a5a40'; g.lineWidth = 1;
    for (i = 0; i < 4; i++) { g.beginPath(); g.moveTo(476, 486 + i * 6); g.lineTo(518, 486 + i * 6); g.stroke(); }
    R(g, 534, 468, 22, 40, '#4a2a22', INK, 2);
    R(g, 538, 460, 14, 12, '#3a2018', INK, 1.5);
    ellipse(g, 545, 458, 8, 4, '#c8b070', INK, 1.5);
    ellipse(g, 512, 512, 12, 8, '#d8d0c4', INK, 1.5);
    ellipse(g, 548, 516, 10, 5, '#3a3a40', INK, 1.5);
    if (!cleared) {
      /* chair pulled up to the desk */
      R(g, 340, 630, 70, 14, '#3a2a22', INK, 2);
      R(g, 350, 644, 12, 40, '#3a2a22', INK, 1.5);
      R(g, 388, 644, 12, 40, '#3a2a22', INK, 1.5);
      R(g, 348, 582, 54, 50, '#4a3428', INK, 2);
    } else {
      /* chair pushed back, a note left on the book */
      R(g, 400, 650, 70, 14, '#3a2a22', INK, 2);
      R(g, 410, 664, 12, 36, '#3a2a22', INK, 1.5);
      R(g, 448, 664, 12, 36, '#3a2a22', INK, 1.5);
      R(g, 478, 470, 40, 28, '#f8f0d8', INK, 1.5);
      txt(g, '\u2026', 498, 484, 14, '#5a2a28');
    }
    /* hanging bulb over the desk */
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(400, 80); g.lineTo(400, 200); g.stroke();
    R(g, 388, 200, 24, 10, '#3a3e48', INK, 1.5);
    ellipse(g, 400, 226, 14, 16, '#f0d080', INK, 2);
    glow(g, 400, 240, 120, 'rgba(255,200,110,.32)');
    /* cot + bedrolls, right mid */
    R(g, 900, 500, 230, 18, '#3a2a22', INK, 2);
    R(g, 910, 518, 12, 40, '#3a2a22', INK, 1.5);
    R(g, 1108, 518, 12, 40, '#3a2a22', INK, 1.5);
    R(g, 910, 478, 210, 24, '#5a4a62', INK, 2);
    ellipse(g, 940, 488, 22, 12, '#c8c0b4', INK, 1.5);
    if (!cleared) {
      R(g, 980, 470, 80, 28, '#3a3850', INK, 2); /* second bedroll */
    }
    /* crates, rope, helmet */
    crate(g, 760, 560, 110, 80, '\u8ca0\u7269');
    crate(g, 820, 620, 90, 64, '');
    g.strokeStyle = '#c4a060'; g.lineWidth = 3;
    g.beginPath(); g.arc(790, 700, 22, 0.2, Math.PI * 1.8); g.stroke();
    g.beginPath(); g.arc(790, 700, 14, 0.4, Math.PI * 1.5); g.stroke();
    /* helmet on the crate */
    ellipse(g, 860, 548, 22, 12, '#1a2028', INK, 2);
    R(g, 844, 528, 32, 20, '#1a2028', INK, 2);
    /* jackets on hooks — indigo + rust, matches Kaji; gone once they walk */
    R(g, 1000, 380, 14, 10, '#3a3e48', INK, 1.5);
    R(g, 1070, 380, 14, 10, '#3a3e48', INK, 1.5);
    if (!cleared) {
      R(g, 992, 390, 44, 70, '#2a3858', INK, 2);
      R(g, 1000, 400, 28, 22, '#c45a3a', 0);
      R(g, 1062, 390, 44, 64, '#243048', INK, 2);
    }
    /* life ring on the right wall */
    lifeRing(g, 1160, 430, 22);
    /* stairs down to the door, lower right of the aisle, leading to the exit */
    var sx = 980, sy = 700;
    for (i = 0; i < 5; i++) {
      R(g, sx - i * 18, sy + i * 22, 200 + i * 8, 22, i % 2 ? '#5a3e2e' : '#4a3428', INK, 2);
    }
    R(g, 1170, 700, 12, 130, '#3a2a22', INK, 2); /* handrail post */
    g.strokeStyle = '#8a909c'; g.lineWidth = 3;
    g.beginPath(); g.moveTo(1176, 704); g.lineTo(1176, 840); g.stroke();
    /* tide chart near the stairs */
    R(g, 700, 400, 80, 70, '#d0c4a8', INK, 2);
    g.strokeStyle = '#2a5080'; g.lineWidth = 2;
    g.beginPath(); g.moveTo(712, 440); g.quadraticCurveTo(730, 410, 750, 430); g.quadraticCurveTo(770, 450, 772, 420); g.stroke();
    txt(g, '\u6f6e', 740, 414, 11, '#5a2a28');
    /* hanging lamp over the aisle */
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(640, 80); g.lineTo(640, 160); g.stroke();
    R(g, 624, 160, 32, 12, '#2a2c34', INK, 2);
    R(g, 628, 164, 24, 8, '#f0d080', 0);
    glow(g, 640, 200, 160, 'rgba(255,200,110,.28)');
    /* a mug crate / kettle on a low block near the exit so the room isn't empty at the door */
    R(g, 200, 720, 120, 16, '#3a2a22', INK, 2);
    R(g, 210, 700, 40, 24, '#6a7a8c', INK, 2);
    ellipse(g, 230, 698, 14, 6, '#6a7a8c', INK, 1.5);
    ellipse(g, 280, 716, 16, 10, '#d8d0c4', INK, 1.5);
    ellipse(g, 310, 716, 12, 8, '#4a2a22', INK, 1.5);
    shell(g, RW, RH);
  };

  /* ---------- battle: inside the lookout, 720 x 1280 ---------- */
  S2P.battleLookout = function (g) {
    var H = (typeof window !== 'undefined' && window.FFF_C2H) || (typeof root !== 'undefined' && root.FFF_C2H);
    var WD = 720, HT = 1280, H0 = 330, x = g;
    rr(g);
    if (!H) { g.fillStyle = '#1a1410'; g.fillRect(0, 0, WD, HT); return; }
    /* back wall, not a sky */
    boards(g, 0, 0, WD, H0, '#4a3428', '#3e2c22', 28);
    R(g, 0, 0, WD, 18, '#2a2018', H.INK, 2);
    R(g, 240, 20, 240, 26, '#f0e4c8', H.INK, 3);
    txt(g, '\u8239\u5c0b  \u00b7  \u671b\u697c', 360, 33, 14, '#5a2a28');
    /* three canal windows in the back wall */
    function bwin(wx, wy, ww, wh) {
      R(g, wx - 4, wy - 4, ww + 8, wh + 10, '#3a2a22', H.INK, 2.5);
      canalView(g, wx, wy, ww, wh);
      g.strokeStyle = INK; g.lineWidth = 2;
      g.beginPath(); g.moveTo(wx + ww / 2, wy); g.lineTo(wx + ww / 2, wy + wh); g.stroke();
      g.beginPath(); g.moveTo(wx, wy + wh * 0.45); g.lineTo(wx + ww, wy + wh * 0.45); g.stroke();
      R(g, wx - 6, wy + wh, ww + 12, 6, '#4a382c', H.INK, 1.5);
      glow(g, wx + ww / 2, wy + wh + 8, 40, 'rgba(255,190,100,.16)');
    }
    bwin(40, 70, 200, 150);
    bwin(260, 70, 200, 150);
    bwin(480, 70, 200, 150);
    /* binoculars on the centre sill */
    R(g, 330, 214, 60, 14, '#2a2c34', H.INK, 2);
    ellipse(g, 342, 214, 11, 9, '#1a2028', H.INK, 2);
    ellipse(g, 378, 214, 11, 9, '#1a2028', H.INK, 2);
    /* hanging lamps */
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(180, 18); g.lineTo(180, 58); g.stroke();
    g.beginPath(); g.moveTo(540, 18); g.lineTo(540, 58); g.stroke();
    ellipse(g, 180, 74, 14, 16, '#f0d080', H.INK, 2);
    ellipse(g, 540, 74, 14, 16, '#f0d080', H.INK, 2);
    glow(g, 180, 90, 90, 'rgba(255,200,110,.34)');
    glow(g, 540, 90, 90, 'rgba(255,200,110,.34)');
    /* map on the left wall */
    R(g, 8, 230, 70, 90, '#d8c8a0', H.INK, 2);
    txt(g, '\u8ca0\u7269', 43, 246, 10, '#5a2a28');
    /* wooden floor in perspective */
    var fx = H.fx0, i, y, UL = 40, UR = 680;
    g.beginPath();
    g.moveTo(0, H0); g.lineTo(WD, H0); g.lineTo(WD, HT); g.lineTo(0, HT); g.closePath();
    g.fillStyle = H.lg(x, H0, HT, '#6a4e3a', '#3e2c22');
    g.fill();
    g.save(); g.beginPath();
    g.rect(0, H0, WD, HT - H0); g.clip();
    g.strokeStyle = 'rgba(0,0,0,.18)'; g.lineWidth = 2;
    for (i = 0; i < 16; i++) {
      var u = 20 + i * 46;
      g.beginPath(); g.moveTo(fx(u, H0), H0); g.lineTo(fx(u, HT), HT); g.stroke();
    }
    for (i = 1; i < 12; i++) {
      y = H0 + (HT - H0) * Math.pow(i / 12, 1.45);
      g.beginPath(); g.moveTo(0, y); g.lineTo(WD, y); g.stroke();
    }
    /* scuffs, not puddles */
    H.pool(x, 300, 620, 50, 12, '40,24,16', 0.18);
    H.pool(x, 460, 860, 40, 10, '40,24,16', 0.14);
    var r = H.seed(11);
    g.fillStyle = 'rgba(255,255,255,.03)';
    for (i = 0; i < 400; i++) g.fillRect(r() * WD, H0 + r() * (HT - H0), 2, 2);
    g.restore();
    /* radio desk, left foreground-mid */
    var dy = 480, dx = 40;
    H.R(x, dx, dy, 200, 90, '#4a3428', H.INK, 3);
    H.R(x, dx + 10, dy - 40, 110, 40, '#2a2c34', H.INK, 2);
    ellipse(g, dx + 30, dy - 20, 7, 7, '#3a6a3a', H.INK, 1.5);
    ellipse(g, dx + 50, dy - 20, 7, 7, '#6a3a2a', H.INK, 1.5);
    H.R(x, dx + 70, dy - 28, 40, 16, '#1a2018', H.INK, 1.5);
    H.R(x, dx + 130, dy - 16, 40, 16, '#f0e4c8', H.INK, 2);
    /* chair */
    H.R(x, dx + 50, dy + 90, 60, 12, '#3a2a22', H.INK, 2);
    H.R(x, dx + 58, dy + 102, 10, 36, '#3a2a22', H.INK, 1.5);
    H.R(x, dx + 90, dy + 102, 10, 36, '#3a2a22', H.INK, 1.5);
    /* crates + rope, right */
    crate(g, 520, 470, 100, 70, '\u8ca0\u7269');
    crate(g, 580, 530, 80, 56, '');
    g.strokeStyle = '#c4a060'; g.lineWidth = 3;
    g.beginPath(); g.arc(620, 620, 18, 0.2, Math.PI * 1.8); g.stroke();
    /* cot hint far right near the wall */
    H.R(x, 600, 300, 110, 14, '#3a2a22', H.INK, 2);
    H.R(x, 610, 286, 90, 16, '#5a4a62', H.INK, 2);
    /* jackets on the right wall */
    H.R(x, 670, 240, 36, 56, '#2a3858', H.INK, 2);
    H.R(x, 676, 250, 24, 16, '#c45a3a', 0);
    lifeRing(g, 40, 250, 18);
    /* stairs down on the right, leading toward the door */
    for (i = 0; i < 4; i++) {
      H.R(x, 500 - i * 10, 700 + i * 40, 200 + i * 16, 36, i % 2 ? '#5a3e2e' : '#4a3428', H.INK, 2);
    }
    /* wet sheen from the lamps, warm interior grade, no rain */
    H.wet(x, [[180, 0, 40, '255,200,110', 0.22], [540, 0, 40, '255,200,110', 0.22], [360, 0, 28, '255,210,140', 0.1]], 0.45);
    H.vign(x, 0.55);
    H.grade(x, 'rgba(80,50,20,.16)', 'rgba(20,10,8,.28)');
  };

  /* ---------- battle: south quay, looking north at the boat and 船宿, 720 x 1280 ---------- */
  S2P.battleQuay = function (g) {
    var H = (typeof window !== 'undefined' && window.FFF_C2H) || (typeof root !== 'undefined' && root.FFF_C2H);
    var WD = 720, HT = 1280, H0 = 330, x = g;
    rr(g);
    if (!H) { g.fillStyle = '#101828'; g.fillRect(0, 0, WD, HT); return; }
    H.sky(x, '#101428', '#243050', 40);
    glow(g, 580, 64, 70, 'rgba(200,210,240,.18)');
    ellipse(g, 580, 64, 20, 20, '#dce4f0', 0);
    /* far (north) bank: Minato wood + the 船宿 lookout, east of the lobby */
    plank(g, 0, 128, WD, 110, '#4a3428', '#3e2c22', 40);
    R(g, 0, 128, WD, 12, '#2a2018', H.INK, 2);
    /* dim Minato windows on the left */
    var lit = [0, 1, 0, 1, 0], i;
    for (i = 0; i < 5; i++) H.win(x, 16 + i * 48, 150, 36, 28, !!lit[i], 2);
    /* 船宿 itself, right-of-centre on the far bank */
    R(g, 280, 118, 360, 120, '#4a3428', H.INK, 3);
    R(g, 280, 110, 360, 16, '#3a4048', H.INK, 2);
    R(g, 360, 122, 200, 22, '#f0e4c8', H.INK, 3);
    txt(g, '\u8239\u5c0b', 460, 133, 14, '#5a2a28');
    H.win(x, 300, 156, 50, 36, 1, 2);
    H.win(x, 366, 156, 50, 36, 1, 2);
    /* door */
    H.R(x, 480, 168, 44, 70, '#5a3a28', H.INK, 2);
    H.R(x, 532, 168, 44, 70, '#523626', H.INK, 2);
    glow(g, 325, 174, 30, 'rgba(255,190,100,.28)');
    glow(g, 391, 174, 30, 'rgba(255,190,100,.28)');
    glow(g, 528, 180, 36, 'rgba(255,190,100,.3)');
    lifeRing(g, 620, 200, 14);
    /* north boardwalk lip */
    plank(g, 0, 238, WD, 22, '#6a4a36', '#5a3e2e', 28);
    /* ---- canal ---- */
    g.fillStyle = H.lg(x, 260, H0, '#152038', '#0c1424');
    g.fillRect(0, 260, WD, H0 - 260);
    g.strokeStyle = 'rgba(160,200,230,.16)'; g.lineWidth = 2;
    for (i = 0; i < 5; i++) {
      var yy = 270 + i * 14;
      g.beginPath(); g.moveTo(0, yy); g.quadraticCurveTo(200, yy + 5, 400, yy); g.quadraticCurveTo(560, yy - 4, 720, yy + 3); g.stroke();
    }
    /* the flower boat, close, filling the canal — this fight is above it */
    flowerBoat(g, 80, 250, 560, 90);
    /* gangplank hint */
    H.poly(x, [[480, 248], [520, 248], [500, 268], [470, 268]], '#6a4a36', H.INK, 2);
    /* window and moon streaks on the water */
    H.streak(x, 325, 270, 20, 50, '255,190,100', 0.22);
    H.streak(x, 391, 270, 18, 46, '255,190,100', 0.18);
    H.streak(x, 528, 270, 22, 48, '255,190,100', 0.2);
    H.streak(x, 580, 268, 28, 40, '200,210,240', 0.12);
    /* pilings */
    function piling(px, y0, y1) {
      g.fillStyle = '#2a2018';
      g.fillRect(px, y0, 10, y1 - y0);
      g.strokeStyle = INK; g.lineWidth = 2; g.strokeRect(px, y0, 10, y1 - y0);
    }
    piling(30, 280, H0); piling(680, 284, H0);
    ellipse(g, 35, 310, 14, 8, '#1a1220', INK, 2);
    /* ---- south quay lip + flower bed at the horizon ---- */
    R(g, 0, H0 - 28, WD, 16, '#5a2030', 0);
    var cols = ['#8a3030', '#6a2020', '#a04040', '#c8c8c0', '#704040', '#b05050'];
    for (i = 0; i < 80; i++) {
      g.fillStyle = cols[i % cols.length];
      g.fillRect((i * 19) % WD, H0 - 26 + (i * 7 % 12), 3, 3);
    }
    /* two pale flower patches */
    for (i = 0; i < 18; i++) {
      g.fillStyle = '#d8d8d0';
      g.fillRect(140 + (i * 11 % 70), H0 - 24 + (i * 5 % 10), 3, 3);
      g.fillRect(500 + (i * 13 % 70), H0 - 24 + (i * 7 % 10), 3, 3);
    }
    R(g, 0, H0 - 12, WD, 12, '#4a4a58', H.INK, 2);
    g.strokeStyle = 'rgba(20,16,20,.35)'; g.lineWidth = 2;
    for (i = 0; i < 12; i++) { g.beginPath(); g.moveTo(i * 64, H0 - 12); g.lineTo(i * 64, H0); g.stroke(); }
    /* stone flag floor in perspective */
    var fx = H.fx0;
    g.beginPath();
    g.moveTo(0, H0); g.lineTo(WD, H0); g.lineTo(WD, HT); g.lineTo(0, HT); g.closePath();
    g.fillStyle = H.lg(x, H0, HT, '#3a3c46', '#26242c');
    g.fill();
    g.save();
    g.beginPath(); g.rect(0, H0, WD, HT - H0); g.clip();
    g.strokeStyle = 'rgba(0,0,0,.22)'; g.lineWidth = 2;
    for (i = 1; i < 14; i++) {
      var y = H0 + (HT - H0) * Math.pow(i / 14, 1.4);
      g.beginPath(); g.moveTo(0, y); g.lineTo(WD, y); g.stroke();
      /* flag joints */
      var k, nx = 3 + ((i * 3) % 2);
      for (k = 1; k < nx + 2; k++) {
        var u = (k / (nx + 2)) * 720;
        g.beginPath(); g.moveTo(fx(u, y), y); g.lineTo(fx(u, y + 40), Math.min(HT, y + 40)); g.stroke();
      }
    }
    var r = H.seed(17);
    g.fillStyle = 'rgba(255,255,255,.035)';
    for (i = 0; i < 500; i++) g.fillRect(r() * WD, H0 + r() * (HT - H0), 2, 2);
    /* wet patches */
    H.pool(x, 240, 620, 60, 16, '40,50,70', 0.2);
    H.pool(x, 480, 860, 50, 14, '40,50,70', 0.16);
    H.pool(x, 360, 1040, 70, 18, '40,50,70', 0.14);
    g.restore();
    /* quay lamps */
    function lamp(px, py) {
      H.R(x, px - 5, py - 90, 10, 90, '#3a3e48', H.INK, 2);
      H.R(x, px - 18, py - 104, 36, 14, '#2a2c34', H.INK, 2);
      H.R(x, px - 12, py - 100, 24, 8, '#f0d080', 0);
      glow(g, px, py - 90, 80, 'rgba(255,190,90,.35)');
    }
    lamp(120, H0); lamp(600, H0);
    H.wet(x, [[120, 0, 50, '255,190,100', 0.28], [600, 0, 50, '255,190,100', 0.28], [360, 0, 30, '200,210,230', 0.1]], 0.5);
    /* mooring cleat + rope + a cone */
    H.R(x, 160, 520, 36, 14, '#3a3e48', H.INK, 2);
    H.R(x, 166, 512, 10, 10, '#3a3e48', H.INK, 1.5);
    H.R(x, 180, 512, 10, 10, '#3a3e48', H.INK, 1.5);
    g.strokeStyle = '#c4a060'; g.lineWidth = 3;
    g.beginPath(); g.moveTo(196, 520); g.quadraticCurveTo(260, 560, 200, 260); g.stroke();
    H.poly(x, [[520, 700], [534, 650], [548, 700]], '#d4782a', H.INK, 2);
    H.R(x, 520, 698, 28, 8, '#2a2018', H.INK, 1.5);
    /* crate on the quay */
    crate(g, 80, 780, 96, 70, '\u8ca0\u7269');
    rain(g, H, 50, 4);
    H.vign(x, 0.62);
    H.grade(x, 'rgba(40,50,90,.2)', 'rgba(20,10,20,.25)');
  };

  /* ---------- line cards ---------- */
  S2P.lineCardBoat = function (g, who, phase) {
    var W = 900, H = 420;
    R(g, 0, 0, W, H, '#1a1520', 0);
    R(g, 8, 8, W - 16, H - 16, '#2a2230', INK, 3);
    var title = {
      kaji: 'Kaji, Masa\u2019s lookout',
      fierce: 'Fierce  \u00b7  the stairs',
      strategic: 'Strategic  \u00b7  the quay flank',
      compassionate: 'Compassionate  \u00b7  walk away',
      skip: 'Lookout Corner already done',
      win: 'After the lookout clears'
    };
    var body = {
      kaji: 'He keeps the night watch above the boat. If you have something to say, say it to him.',
      fierce: 'No talk. Straight up the stairs. The lookouts are in the room. You go in first.',
      strategic: 'Around the quay side, behind the watch. Alley Cat if you have it. They are looking the other way.',
      compassionate: 'You tell them to walk. This is not their building. If they go, the room is yours. If they will not, then you fight.',
      skip: 'The lookouts were already cleared at Lookout Corner. The room is empty. The pin moves on to the quay garage.',
      win: 'The boat house is quiet. Four Corners points at the garage on the depot approach. Do not open the door yet.'
    };
    txt(g, title[who] || who, 450, 40, 18, '#f0e4c8', '800 ');
    g.font = '700 20px "Noto Sans CJK JP",Georgia,serif';
    g.fillStyle = '#efe4d0'; g.textAlign = 'left'; g.textBaseline = 'top';
    var words = (body[who] || '').split(' '), line = '', y = 90, maxW = 820, i;
    for (i = 0; i < words.length; i++) {
      var test = line ? line + ' ' + words[i] : words[i];
      if (g.measureText(test).width > maxW) { g.fillText(line, 40, y); y += 32; line = words[i]; }
      else line = test;
    }
    if (line) g.fillText(line, 40, y);
    txt(g, phase || who, 820, 380, 14, '#8aa0c8', '900 ', 'right');
  };
})(typeof window !== 'undefined' ? window : this);
