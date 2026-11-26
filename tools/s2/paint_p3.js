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
    /* elongated white hull, orange gunwale, dense flower cargo, sitting in the water */
    var cx = x + w / 2, wl = y + h * 0.62;
    g.beginPath();
    g.moveTo(x + w * 0.08, y + h * 0.38);
    g.bezierCurveTo(x + w * 0.18, y + h * 0.12, x + w * 0.82, y + h * 0.12, x + w * 0.92, y + h * 0.38);
    g.quadraticCurveTo(x + w * 0.98, y + h * 0.48, x + w * 0.94, y + h * 0.7);
    g.quadraticCurveTo(cx, y + h * 0.86, x + w * 0.06, y + h * 0.7);
    g.quadraticCurveTo(x + w * 0.02, y + h * 0.48, x + w * 0.08, y + h * 0.38);
    g.closePath();
    g.fillStyle = '#eceae4'; g.fill();
    g.strokeStyle = INK; g.lineWidth = 2.2; g.stroke();
    /* gunwale */
    g.beginPath();
    g.moveTo(x + w * 0.1, y + h * 0.4);
    g.bezierCurveTo(x + w * 0.22, y + h * 0.2, x + w * 0.78, y + h * 0.2, x + w * 0.9, y + h * 0.4);
    g.strokeStyle = '#c45a32'; g.lineWidth = Math.max(3, h * 0.08); g.stroke();
    /* cargo well */
    g.save();
    g.beginPath();
    g.moveTo(x + w * 0.16, y + h * 0.4);
    g.bezierCurveTo(x + w * 0.26, y + h * 0.26, x + w * 0.74, y + h * 0.26, x + w * 0.84, y + h * 0.4);
    g.lineTo(x + w * 0.86, y + h * 0.6);
    g.quadraticCurveTo(cx, y + h * 0.7, x + w * 0.14, y + h * 0.6);
    g.closePath();
    g.clip();
    g.fillStyle = '#1a2018'; g.fill();
    var cols = ['#c43a3a', '#e07040', '#e8d060', '#f0e8e0', '#d4608a', '#c09030', '#e8a0a0', '#f4f0c8', '#a03030', '#d84848', '#c8a040'];
    var i, n = Math.max(280, (w * h) / 5);
    for (i = 0; i < n; i++) {
      var fx = x + w * (0.16 + (i * 17 % 70) / 100), fy = y + h * (0.32 + (i * 29 % 30) / 100);
      g.fillStyle = cols[i % cols.length];
      g.fillRect(fx, fy, 2 + (i % 2), 2 + ((i * 3) % 2));
    }
    g.restore();
    /* pale reflection under the hull */
    g.save();
    g.globalAlpha = 0.28;
    g.beginPath();
    g.moveTo(x + w * 0.1, wl + 4);
    g.quadraticCurveTo(cx, y + h * 1.05, x + w * 0.9, wl + 4);
    g.quadraticCurveTo(cx, y + h * 0.78, x + w * 0.1, wl + 4);
    g.fillStyle = 'rgba(220,230,240,.5)'; g.fill();
    var j;
    for (j = 0; j < 9; j++) {
      g.fillStyle = cols[j % cols.length];
      g.globalAlpha = 0.16;
      g.fillRect(x + w * (0.2 + j * 0.07), wl + 2, 8, 5);
    }
    g.restore();
  }
  function canalView(g, x, y, w, h, pan) {
    /* night canal + one flower boat. pan shifts the scene so adjacent windows share a view. */
    pan = (pan == null) ? 0 : pan;
    g.save();
    g.beginPath(); g.rect(x, y, w, h); g.clip();
    var lg = g.createLinearGradient(x, y, x, y + h);
    lg.addColorStop(0, '#151828'); lg.addColorStop(0.38, '#1a2438'); lg.addColorStop(1, '#0c1424');
    g.fillStyle = lg; g.fillRect(x, y, w, h);
    var pitch = w * 1.15, sh = -pan * pitch;
    var i, cols = ['#8a3030', '#6a2020', '#a04040', '#c8c8c0', '#704040', '#b05050'];
    /* far south bank, continuous across panes */
    R(g, x - 40, y + h * 0.64, w + 80, h * 0.16, '#3a2a28', 0);
    for (i = 0; i < 70; i++) {
      g.fillStyle = cols[i % cols.length];
      g.fillRect(x + sh + (i * 23 % (w + 200)) - 40, y + h * 0.64 + (i * 13 % 16), 3, 3);
    }
    R(g, x - 40, y + h * 0.78, w + 80, 7, '#4a4a58', 0);
    g.strokeStyle = 'rgba(160,200,230,.2)'; g.lineWidth = 1.5;
    for (i = 0; i < 6; i++) {
      var yy = y + h * (0.4 + i * 0.06);
      g.beginPath(); g.moveTo(x - 10, yy); g.quadraticCurveTo(x + w * 0.5 + sh, yy + 4, x + w + 10, yy - 2); g.stroke();
    }
    var bw = w * 1.55, bh = h * 0.55;
    flowerBoat(g, x + w / 2 - bw / 2 + sh, y + h * 0.2, bw, bh);
    /* lamp streaks, fixed in the scene so they travel with the boat house on the far bank */
    g.fillStyle = 'rgba(255,190,100,.15)';
    g.fillRect(x + w * 0.45 + sh, y + h * 0.55, 8, h * 0.22);
    g.fillRect(x + w * 0.62 + sh, y + h * 0.55, 6, h * 0.18);
    g.restore();
  }
  function jacketHook(g, x, y, col, shirt, gone) {
    R(g, x + 10, y - 10, 14, 8, '#3a3e48', INK, 1.5);
    if (gone) return;
    R(g, x, y, 44, 70, col, INK, 2);
    /* sleeves hanging */
    R(g, x - 12, y + 8, 16, 44, col, INK, 2);
    R(g, x + 40, y + 8, 16, 44, col, INK, 2);
    if (shirt) {
      g.fillStyle = shirt;
      g.beginPath(); g.moveTo(x + 12, y + 4); g.lineTo(x + 22, y + 26); g.lineTo(x + 32, y + 4); g.closePath(); g.fill();
    }
  }

  function winPane(g, x, y, w, h, lit, scene) {
    R(g, x - 4, y - 4, w + 8, h + 10, '#3a2a22', INK, 2.5);
    if (scene === true || typeof scene === 'number') canalView(g, x, y, w, h, typeof scene === 'number' ? scene : 0);
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
    W0 = W0 || 360; H0 = H0 || 440; rr(g);
    /* night / water fill for the tall overlay (building + the boat below) */
    R(g, 0, 0, W0, H0, '#14101c', 0);
    var lg = g.createLinearGradient(0, 230, 0, H0);
    lg.addColorStop(0, '#152038'); lg.addColorStop(1, '#0c1424');
    g.fillStyle = lg; g.fillRect(0, 230, W0, H0 - 230);
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
    txt(g, '\u8239\u5bbf', 156, 52, 16, '#5a2a28');
    txt(g, 'FUNAYADO', 228, 52, 10, '#3a2a22');
    /* upper lookout windows, lit */
    winPane(g, 24, 72, 70, 52, 1, false);
    winPane(g, 110, 72, 70, 52, 1, false);
    glow(g, 59, 98, 36, 'rgba(255,190,100,.22)');
    glow(g, 145, 98, 36, 'rgba(255,190,100,.22)');
    /* door porch on the boardwalk (right bay, over the old cream doors) */
    R(g, 230, 70, 116, 114, '#2a2018', INK, 3);
    /* transom */
    winPane(g, 248, 76, 80, 22, 1, false);
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
    g.fillStyle = 'rgba(80,100,140,.18)';
    g.fillRect(20, 196, 70, 8); g.fillRect(200, 200, 90, 6);
    g.fillRect(120, 188, 40, 5);
    /* short wooden posts at the left, not a bar across the door */
    R(g, 12, 160, 8, 28, '#3a2a22', INK, 1.5);
    R(g, 86, 160, 8, 28, '#3a2a22', INK, 1.5);
    R(g, 12, 158, 82, 6, '#4a382c', INK, 1.5);
    /* gutter drip from the tin roof */
    R(g, 8, 30, 6, 14, '#3a4048', INK, 1.5);
    /* quay rail under the apron */
    R(g, 0, 218, W0, 10, '#6a7078', INK, 2);
    g.fillStyle = '#8a9098';
    for (i = 0; i < 12; i++) g.fillRect(16 + i * 30, 216, 4, 14);
    /* canal water + a clean flower boat, covering the noisy town composite under the lookout */
    g.strokeStyle = 'rgba(160,200,230,.2)'; g.lineWidth = 1.6;
    for (i = 0; i < 5; i++) {
      var yy = 250 + i * 18;
      g.beginPath(); g.moveTo(0, yy); g.quadraticCurveTo(180, yy + 4, W0, yy - 2); g.stroke();
    }
    /* east end of the flower boat, snug under the quay lip (hull continues west) */
    flowerBoat(g, -40, 226, 330, 175);
    /* gangplank from the boardwalk down onto the cargo */
    R(g, 8, 208, 70, 14, '#6a4a36', INK, 2);
    R(g, 16, 220, 66, 70, '#5a3e2e', INK, 2);
    g.strokeStyle = 'rgba(0,0,0,.25)'; g.lineWidth = 1.5;
    for (i = 0; i < 6; i++) { g.beginPath(); g.moveTo(20, 228 + i * 11); g.lineTo(76, 228 + i * 11); g.stroke(); }
    /* mooring hook on the stern gunwale */
    R(g, 262, 248, 6, 18, '#3a3e48', INK, 1.5);
    g.strokeStyle = '#c4a060'; g.lineWidth = 2;
    g.beginPath(); g.moveTo(265, 264); g.quadraticCurveTo(278, 278, 268, 238); g.stroke();
    /* ink the building only — do not box the water */
    g.strokeStyle = INK; g.lineWidth = 4;
    g.strokeRect(1, 1, W0 - 2, 218);
  };

  /* ---------- interior: lookout room, 1280 x 900 ---------- */
  S2P.boatLookout = function (g, cleared) {
    var RW = 1280, RH = 900; rr(g);
    /* timber room, scored floor — not a wet street */
    R(g, 0, 0, RW, RH, '#2a2018', 0);
    boards(g, 90, 80, 1100, 280, '#4a3428', '#3e2c22', 28);
    /* horizontal floorboards, warm scored wood — not a wet street, not a vertical stripe */
    boards(g, 90, 480, 1100, 370, '#6a4e3a', '#5c4432', 32);
    var i, j;
    g.fillStyle = 'rgba(255,220,160,.04)';
    for (i = 0; i < 40; i++) g.fillRect(120 + (i * 97 % 1040), 500 + (i * 53 % 330), 18, 3);
    g.fillStyle = 'rgba(20,12,8,.16)';
    g.beginPath(); g.ellipse(420, 700, 50, 14, 0, 0, Math.PI * 2); g.fill();
    g.beginPath(); g.ellipse(880, 760, 40, 10, 0.2, 0, Math.PI * 2); g.fill();
    /* back wall lintel + three canal windows sharing one view */
    R(g, 90, 80, 1100, 18, '#2a2018', INK, 2);
    R(g, 200, 110, 200, 18, '#f0e4c8', INK, 3);
    txt(g, '\u8239\u5bbf  \u00b7  \u671b\u697c', 300, 119, 14, '#5a2a28');
    winPane(g, 160, 150, 280, 210, 1, -1);
    winPane(g, 500, 150, 280, 210, 1, 0);
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
    jacketHook(g, 992, 390, '#2a3858', '#c45a3a', !!cleared);
    jacketHook(g, 1070, 390, '#243048', 0, !!cleared);
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
    /* kettle cables to the radio */
    g.strokeStyle = '#1a1220'; g.lineWidth = 2;
    g.beginPath(); g.moveTo(230, 700); g.quadraticCurveTo(200, 640, 280, 524); g.stroke();
    /* kerosene heater by the cot */
    R(g, 1088, 600, 46, 56, '#4a3a32', INK, 2);
    ellipse(g, 1111, 600, 20, 8, '#3a2a22', INK, 1.5);
    R(g, 1098, 616, 26, 16, '#2a2018', INK, 1.5);
    glow(g, 1111, 624, 28, 'rgba(255,140,60,.2)');
    /* boots at the foot of the stairs */
    ellipse(g, 940, 820, 16, 8, '#1a1816', INK, 2);
    ellipse(g, 968, 822, 16, 8, '#1a1816', INK, 2);
    R(g, 928, 800, 22, 22, '#1a1816', INK, 2);
    R(g, 956, 802, 22, 22, '#1a1816', INK, 2);
    /* wall clock */
    ellipse(g, 650, 420, 22, 22, '#d8c8a0', INK, 2);
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(650, 420); g.lineTo(650, 408); g.stroke();
    g.beginPath(); g.moveTo(650, 420); g.lineTo(660, 424); g.stroke();
    /* raincoat on a peg near the exit */
    R(g, 140, 620, 12, 8, '#3a3e48', INK, 1.5);
    if (!cleared) {
      R(g, 126, 628, 44, 64, '#2a4a48', INK, 2);
      R(g, 118, 636, 12, 40, '#2a4a48', INK, 2);
      R(g, 166, 636, 12, 40, '#2a4a48', INK, 2);
    }
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
    txt(g, '\u8239\u5bbf  \u00b7  \u671b\u697c', 360, 33, 14, '#5a2a28');
    /* three canal windows in the back wall */
    function bwin(wx, wy, ww, wh, pan) {
      R(g, wx - 4, wy - 4, ww + 8, wh + 10, '#3a2a22', H.INK, 2.5);
      canalView(g, wx, wy, ww, wh, pan);
      g.strokeStyle = INK; g.lineWidth = 2;
      g.beginPath(); g.moveTo(wx + ww / 2, wy); g.lineTo(wx + ww / 2, wy + wh); g.stroke();
      g.beginPath(); g.moveTo(wx, wy + wh * 0.45); g.lineTo(wx + ww, wy + wh * 0.45); g.stroke();
      R(g, wx - 6, wy + wh, ww + 12, 6, '#4a382c', H.INK, 1.5);
      glow(g, wx + ww / 2, wy + wh + 8, 40, 'rgba(255,190,100,.16)');
    }
    bwin(40, 70, 200, 150, -1);
    bwin(260, 70, 200, 150, 0);
    bwin(480, 70, 200, 150, 1);
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
    lifeRing(g, 50, 200, 16);
    /* wooden floor in perspective */
    var fx = H.fx0, i, y, UL = 40, UR = 680;
    g.beginPath();
    g.moveTo(0, H0); g.lineTo(WD, H0); g.lineTo(WD, HT); g.lineTo(0, HT); g.closePath();
    g.fillStyle = H.lg(x, H0, HT, '#6a4e3a', '#3e2c22');
    g.fill();
    g.save(); g.beginPath();
    g.rect(0, H0, WD, HT - H0); g.clip();
    /* planks run toward the camera; no graph-paper grid */
    g.strokeStyle = 'rgba(0,0,0,.2)'; g.lineWidth = 2;
    for (i = 0; i <= 18; i++) {
      var u = i * 40;
      g.beginPath(); g.moveTo(fx(u, H0), H0); g.lineTo(fx(u, HT), HT); g.stroke();
    }
    /* occasional board-end joints, not a full cross-grid */
    g.strokeStyle = 'rgba(0,0,0,.12)'; g.lineWidth = 1.5;
    for (i = 2; i < 16; i += 3) {
      y = H0 + (HT - H0) * Math.pow(i / 16, 1.5);
      var u0 = ((i * 5) % 7) * 40, u1 = u0 + 40;
      g.beginPath(); g.moveTo(fx(u0, y), y); g.lineTo(fx(u1, y), y); g.stroke();
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
    jacketHook(g, 662, 236, '#2a3858', '#c45a3a', 0);
    /* stairs down on the right, leading toward the door */
    for (i = 0; i < 4; i++) {
      H.R(x, 500 - i * 10, 700 + i * 40, 200 + i * 16, 36, i % 2 ? '#5a3e2e' : '#4a3428', H.INK, 2);
    }
    /* ---- lower floor: wear, light pools, rope, tackle — keep the centre lane clear ---- */
    H.pool(x, 200, 920, 80, 18, '40,24,16', 0.2);
    H.pool(x, 480, 1080, 90, 22, '40,24,16', 0.16);
    H.pool(x, 320, 1180, 70, 16, '40,24,16', 0.14);
    /* worn traffic path down the aisle */
    g.fillStyle = 'rgba(20,12,8,.12)';
    g.beginPath(); g.ellipse(360, 1020, 90, 28, 0, 0, Math.PI * 2); g.fill();
    g.beginPath(); g.ellipse(340, 1160, 70, 20, 0.1, 0, Math.PI * 2); g.fill();
    /* plank scratches */
    g.strokeStyle = 'rgba(20,12,8,.22)'; g.lineWidth = 1.4;
    g.beginPath(); g.moveTo(80, 960); g.lineTo(200, 980); g.stroke();
    g.beginPath(); g.moveTo(500, 1100); g.lineTo(620, 1120); g.stroke();
    g.beginPath(); g.moveTo(100, 1140); g.lineTo(180, 1180); g.stroke();
    /* lamp pools in the foreground, soft and short */
    glow(g, 180, H0 + 40, 70, 'rgba(255,200,110,.16)');
    glow(g, 540, H0 + 40, 70, 'rgba(255,200,110,.16)');
    glow(g, 160, 980, 90, 'rgba(255,200,110,.18)');
    glow(g, 560, 1040, 90, 'rgba(255,200,110,.16)');
    glow(g, 360, 1200, 80, 'rgba(255,210,140,.1)');
    /* rope coils, left foreground and at the foot of the stairs */
    function ropeCoil(cx, cy, r) {
      g.strokeStyle = INK; g.lineWidth = 5;
      g.beginPath(); g.arc(cx, cy, r, 0.2, Math.PI * 1.85); g.stroke();
      g.strokeStyle = '#c4a060'; g.lineWidth = 3.2;
      g.beginPath(); g.arc(cx, cy, r, 0.2, Math.PI * 1.85); g.stroke();
      g.strokeStyle = '#a48450'; g.lineWidth = 2.4;
      g.beginPath(); g.arc(cx, cy, r * 0.62, 0.5, Math.PI * 1.6); g.stroke();
      g.beginPath(); g.arc(cx, cy, r * 0.28, 0.1, Math.PI * 1.9); g.stroke();
    }
    ropeCoil(110, 1020, 28);
    ropeCoil(90, 1060, 18);
    ropeCoil(600, 980, 24);
    /* tackle box, lower left, out of the fight lane */
    H.R(x, 70, 1120, 110, 70, '#3a5a6a', H.INK, 2.5);
    H.R(x, 70, 1120, 110, 16, '#2a3a44', H.INK, 2);
    H.R(x, 78, 1142, 28, 18, '#c45a3a', H.INK, 1.5);
    H.R(x, 112, 1142, 28, 18, '#c8b070', H.INK, 1.5);
    H.R(x, 146, 1142, 26, 18, '#2a3858', H.INK, 1.5);
    H.R(x, 78, 1164, 44, 18, '#1a2028', H.INK, 1.5);
    H.R(x, 128, 1164, 44, 18, '#4a3428', H.INK, 1.5);
    /* a second, smaller closed box by the stairs */
    H.R(x, 80, 880, 70, 36, '#6a3a22', H.INK, 2);
    H.R(x, 88, 886, 54, 10, '#4a2818', H.INK, 1.5);
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
    /* far (north) bank, pushed up so the canal has room */
    var lit = [0, 1, 0, 1, 0], i;
    plank(g, 0, 80, WD, 100, '#4a3428', '#3e2c22', 40);
    R(g, 0, 80, WD, 12, '#2a2018', H.INK, 2);
    for (i = 0; i < 5; i++) H.win(x, 16 + i * 48, 102, 36, 28, !!lit[i], 2);
    /* 船宿 itself, right-of-centre on the far bank */
    R(g, 280, 70, 360, 116, '#4a3428', H.INK, 3);
    R(g, 280, 62, 360, 16, '#3a4048', H.INK, 2);
    R(g, 360, 74, 200, 22, '#f0e4c8', H.INK, 3);
    txt(g, '\u8239\u5bbf', 460, 85, 14, '#5a2a28');
    H.win(x, 300, 108, 50, 36, 1, 2);
    H.win(x, 366, 108, 50, 36, 1, 2);
    H.R(x, 480, 120, 44, 70, '#5a3a28', H.INK, 2);
    H.R(x, 532, 120, 44, 70, '#523626', H.INK, 2);
    glow(g, 325, 126, 30, 'rgba(255,190,100,.28)');
    glow(g, 391, 126, 30, 'rgba(255,190,100,.28)');
    glow(g, 528, 132, 36, 'rgba(255,190,100,.3)');
    lifeRing(g, 620, 150, 14);
    /* north boardwalk lip */
    plank(g, 0, 186, WD, 20, '#6a4a36', '#5a3e2e', 28);
    /* ---- canal, a real band of water under the boat ---- */
    g.fillStyle = H.lg(x, 200, H0, '#152038', '#0c1424');
    g.fillRect(0, 206, WD, H0 - 206);
    g.strokeStyle = 'rgba(160,200,230,.2)'; g.lineWidth = 2;
    for (i = 0; i < 7; i++) {
      var yy = 216 + i * 14;
      g.beginPath(); g.moveTo(0, yy); g.quadraticCurveTo(200, yy + 5, 400, yy); g.quadraticCurveTo(560, yy - 4, 720, yy + 3); g.stroke();
    }
    /* flower boat sitting in the water, not on the lip */
    flowerBoat(g, 70, 200, 580, 120);
    /* gangplank from the boardwalk down onto the boat */
    H.poly(x, [[430, 186], [470, 186], [500, 230], [450, 230]], '#6a4a36', H.INK, 2);
    g.strokeStyle = 'rgba(0,0,0,.25)'; g.lineWidth = 1.5;
    for (i = 0; i < 4; i++) { g.beginPath(); g.moveTo(438 + i * 8, 190 + i * 8); g.lineTo(462 + i * 8, 190 + i * 8); g.stroke(); }
    /* window and moon streaks on the water, under the hull */
    H.streak(x, 325, 250, 18, 70, '255,190,100', 0.22);
    H.streak(x, 391, 250, 16, 64, '255,190,100', 0.18);
    H.streak(x, 528, 250, 20, 68, '255,190,100', 0.2);
    H.streak(x, 580, 248, 26, 60, '200,210,240', 0.12);
    /* pilings in the water */
    function piling(px, y0, y1) {
      g.fillStyle = '#2a2018';
      g.fillRect(px, y0, 10, y1 - y0);
      g.strokeStyle = INK; g.lineWidth = 2; g.strokeRect(px, y0, 10, y1 - y0);
    }
    piling(24, 220, H0 - 8); piling(686, 224, H0 - 8);
    ellipse(g, 29, 260, 14, 8, '#1a1220', INK, 2);
    /* ---- south quay lip + flower bed ---- */
    R(g, 0, H0 - 26, WD, 16, '#4a1820', 0);
    var cols = ['#8a3030', '#6a2020', '#a04040', '#c8c8c0', '#704040', '#b05050', '#c06060'];
    for (i = 0; i < 140; i++) {
      g.fillStyle = cols[i % cols.length];
      g.fillRect((i * 17) % WD, H0 - 26 + (i * 7 % 14), 3, 3);
    }
    for (i = 0; i < 24; i++) {
      g.fillStyle = '#d8d8d0';
      g.fillRect(140 + (i * 11 % 80), H0 - 22 + (i * 5 % 10), 3, 3);
      g.fillRect(500 + (i * 13 % 80), H0 - 22 + (i * 7 % 10), 3, 3);
    }
    R(g, 0, H0 - 10, WD, 10, '#4a4a58', H.INK, 2);
    g.strokeStyle = 'rgba(20,16,20,.35)'; g.lineWidth = 2;
    for (i = 0; i < 12; i++) { g.beginPath(); g.moveTo(i * 64, H0 - 10); g.lineTo(i * 64, H0); g.stroke(); }
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
    /* lamp sheen on the wet stone, short pools not tall columns */
    glow(g, 120, H0 + 24, 60, 'rgba(255,190,100,.2)');
    glow(g, 600, H0 + 24, 60, 'rgba(255,190,100,.2)');
    /* mooring bollard + rope to the near piling, a cone, crates off the lane */
    H.R(x, 70, 520, 28, 36, '#3a3e48', H.INK, 2);
    ellipse(g, 84, 520, 18, 8, '#3a3e48', H.INK, 2);
    g.strokeStyle = '#c4a060'; g.lineWidth = 3;
    g.beginPath(); g.moveTo(84, 520); g.quadraticCurveTo(60, 400, 34, 260); g.stroke();
    H.poly(x, [[520, 700], [534, 650], [548, 700]], '#d4782a', H.INK, 2);
    H.R(x, 520, 698, 28, 8, '#2a2018', H.INK, 1.5);
    crate(g, 80, 780, 96, 70, '\u8ca0\u7269');
    crate(g, 560, 860, 80, 58, '');
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
