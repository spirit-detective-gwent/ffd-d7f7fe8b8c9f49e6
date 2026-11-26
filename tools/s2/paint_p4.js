/* v6.5.63 FFF_S2P phase 4: quay garage façade, dispatch bay, and Off Schedule battle rooms.
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
  function corrug(g, x, y, w, h, c1, c2, step) {
    g.fillStyle = c1; g.fillRect(x, y, w, h);
    for (var i = x, n = 0; i < x + w; i += step, n++) {
      g.fillStyle = n % 2 ? c2 : c1; g.fillRect(i, y, step - 1, h);
      g.fillStyle = 'rgba(255,255,255,.06)'; g.fillRect(i, y, 2, h);
      g.fillStyle = 'rgba(0,0,0,.18)'; g.fillRect(i + step - 2, y, 2, h);
    }
  }
  function concFloor(g, x, y, w, h, c1, c2) {
    g.fillStyle = c1; g.fillRect(x, y, w, h);
    var i, r = function (s) { var v = s; return function () { v = (v * 16807) % 2147483647; return (v - 1) / 2147483646; }; }(19);
    g.fillStyle = 'rgba(0,0,0,.06)';
    for (i = 0; i < 220; i++) g.fillRect(x + r() * w, y + r() * h, 8 + r() * 18, 3 + r() * 4);
    g.fillStyle = 'rgba(255,255,255,.03)';
    for (i = 0; i < 180; i++) g.fillRect(x + r() * w, y + r() * h, 2, 2);
    /* short irregular cracks, never a full cross-grid */
    g.fillStyle = 'rgba(0,0,0,.16)';
    g.fillRect(x + w * 0.08, y + h * 0.38, w * 0.22, 3);
    g.fillRect(x + w * 0.62, y + h * 0.41, w * 0.2, 3);
    g.fillRect(x + w * 0.18, y + h * 0.74, w * 0.2, 3);
    g.fillRect(x + w * 0.7, y + h * 0.7, w * 0.18, 3);
    g.fillRect(x + w * 0.31, y + h * 0.12, 3, h * 0.2);
    g.fillRect(x + w * 0.68, y + h * 0.52, 3, h * 0.18);
  }
  function oilStain(g, x, y, rx, ry) {
    g.fillStyle = 'rgba(20,16,12,.28)';
    g.beginPath(); g.ellipse(x, y, rx, ry, 0.2, 0, Math.PI * 2); g.fill();
    g.fillStyle = 'rgba(40,50,30,.18)';
    g.beginPath(); g.ellipse(x + rx * 0.2, y, rx * 0.55, ry * 0.5, -0.3, 0, Math.PI * 2); g.fill();
  }
  function drum(g, x, y, w, h, col) {
    R(g, x, y, w, h, col || '#6a3a28', INK, 2);
    g.strokeStyle = 'rgba(255,220,160,.18)'; g.lineWidth = 2;
    g.beginPath(); g.moveTo(x + 4, y + 8); g.lineTo(x + 4, y + h - 8); g.stroke();
    g.strokeStyle = 'rgba(0,0,0,.3)'; g.lineWidth = 2;
    g.beginPath(); g.moveTo(x + 3, y + h * 0.35); g.lineTo(x + w - 3, y + h * 0.35); g.stroke();
    g.beginPath(); g.moveTo(x + 3, y + h * 0.65); g.lineTo(x + w - 3, y + h * 0.65); g.stroke();
    R(g, x + 2, y, w - 4, 8, '#3a2a22', INK, 1.5);
  }
  function tire(g, x, y, r) {
    ellipse(g, x, y, r, r * 0.72, '#1a1c22', INK, 2);
    ellipse(g, x, y, r * 0.45, r * 0.32, '#3a3e48', INK, 1.5);
    g.strokeStyle = '#2a2c34'; g.lineWidth = 2;
    var i;
    for (i = 0; i < 6; i++) {
      var a = i * Math.PI / 3;
      g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * r * 0.4, y + Math.sin(a) * r * 0.28); g.stroke();
    }
  }
  function clipBoard(g, x, y, rot) {
    g.save(); g.translate(x, y); if (rot) g.rotate(rot);
    R(g, -16, -22, 32, 44, '#d8c8a0', INK, 2);
    R(g, -10, -28, 20, 10, '#3a3e48', INK, 1.5);
    g.strokeStyle = '#5a3a28'; g.lineWidth = 1.4;
    var i;
    for (i = 0; i < 5; i++) { g.beginPath(); g.moveTo(-12, -12 + i * 7); g.lineTo(12, -12 + i * 7); g.stroke(); }
    g.restore();
  }
  function bike(g, x, y, sc, col) {
    g.save(); g.translate(x, y); g.scale(sc || 1, sc || 1);
    g.strokeStyle = INK; g.lineWidth = 5;
    g.beginPath(); g.arc(-28, 18, 16, 0, Math.PI * 2); g.stroke();
    g.beginPath(); g.arc(30, 18, 16, 0, Math.PI * 2); g.stroke();
    g.strokeStyle = col || '#2a2c34'; g.lineWidth = 3.2;
    g.beginPath(); g.arc(-28, 18, 16, 0, Math.PI * 2); g.stroke();
    g.beginPath(); g.arc(30, 18, 16, 0, Math.PI * 2); g.stroke();
    g.strokeStyle = INK; g.lineWidth = 4;
    g.beginPath(); g.moveTo(-28, 18); g.lineTo(-4, 0); g.lineTo(22, 18); g.lineTo(8, -16); g.lineTo(-10, -8); g.lineTo(-28, 18); g.stroke();
    g.strokeStyle = col || '#3a463c'; g.lineWidth = 2.4;
    g.beginPath(); g.moveTo(-28, 18); g.lineTo(-4, 0); g.lineTo(22, 18); g.lineTo(8, -16); g.lineTo(-10, -8); g.lineTo(-28, 18); g.stroke();
    R(g, 4, -22, 16, 6, '#2a2c34', INK, 1.5);
    g.restore();
  }
  function rain(g, W, H, n, seedN) {
    var r = function (s) { var v = s; return function () { v = (v * 16807) % 2147483647; return (v - 1) / 2147483646; }; }(seedN || 3);
    g.strokeStyle = 'rgba(200,220,255,.35)'; g.lineWidth = 1.2;
    var i;
    for (i = 0; i < n; i++) {
      var x = r() * W, y = r() * H, L = 10 + r() * 16;
      g.beginPath(); g.moveTo(x, y); g.lineTo(x + 3, y + L); g.stroke();
    }
  }
  function quayNight(g, x, y, w, h) {
    var sky = g.createLinearGradient(0, y, 0, y + h);
    sky.addColorStop(0, '#1a2238'); sky.addColorStop(0.55, '#243048'); sky.addColorStop(1, '#1a2430');
    g.fillStyle = sky; g.fillRect(x, y, w, h);
    /* far boardwalk */
    R(g, x, y + h * 0.42, w, 16, '#3a322c', 0);
    g.fillStyle = '#2a3a58'; g.fillRect(x, y + h * 0.52, w, h * 0.28);
    g.strokeStyle = 'rgba(120,180,220,.25)'; g.lineWidth = 1.5;
    var i;
    for (i = 0; i < 5; i++) {
      g.beginPath(); g.moveTo(x, y + h * 0.58 + i * 6); g.lineTo(x + w, y + h * 0.58 + i * 6); g.stroke();
    }
    /* flower bed hint */
    g.fillStyle = '#5a3040'; g.fillRect(x, y + h * 0.8, w, h * 0.2);
    g.fillStyle = '#c45a62';
    for (i = 0; i < 28; i++) g.fillRect(x + 4 + (i * 47) % (w - 8), y + h * 0.84 + (i * 13) % 10, 3, 3);
    rain(g, w, h, 18, 9);
  }
  function hose(g, x, y, len) {
    g.strokeStyle = INK; g.lineWidth = 6;
    g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + len * 0.4, y + 28, x + len, y + 8); g.stroke();
    g.strokeStyle = '#3a4a38'; g.lineWidth = 3.5;
    g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + len * 0.4, y + 28, x + len, y + 8); g.stroke();
  }
  function crate(g, x, y, w, h, label) {
    R(g, x, y, w, h, '#8a5a38', INK, 2);
    g.fillStyle = 'rgba(0,0,0,.18)'; g.fillRect(x + 4, y + 4, w - 8, 6);
    g.strokeStyle = 'rgba(40,20,10,.35)'; g.lineWidth = 2;
    g.beginPath(); g.moveTo(x + 6, y + h * 0.5); g.lineTo(x + w - 6, y + h * 0.5); g.stroke();
    if (label) txt(g, label, x + w / 2, y + h / 2 + 4, 11, '#f0e4c8');
  }

  /* ---------- façade: squat quay garage on the south bank, west of the depot door ---------- */
  S2P.garSouth = function (g, W0, H0) {
    W0 = W0 || 320; H0 = H0 || 180;
    rr(g);
    /* night above the roof (a sliver of canal dark, so the overlay does not punch a hole) */
    g.fillStyle = '#1a2434'; g.fillRect(0, 0, W0, 16);
    /* roof cap */
    R(g, 2, 8, W0 - 4, 16, '#3a3e4c', INK, 2.5);
    g.fillStyle = '#2a2e3a'; g.fillRect(6, 10, W0 - 12, 6);
    /* corrugated body, slate like the depot wall */
    corrug(g, 4, 24, W0 - 8, H0 - 28, '#4a5068', '#3e445a', 14);
    g.strokeStyle = INK; g.lineWidth = 3; g.strokeRect(4, 24, W0 - 8, H0 - 28);
    /* rust / rain streaks on the metal */
    g.strokeStyle = 'rgba(80,50,40,.35)'; g.lineWidth = 2;
    g.beginPath(); g.moveTo(28, 30); g.lineTo(32, 120); g.stroke();
    g.beginPath(); g.moveTo(260, 36); g.lineTo(256, 130); g.stroke();
    g.strokeStyle = 'rgba(180,200,220,.12)'; g.lineWidth = 1.5;
    g.beginPath(); g.moveTo(80, 28); g.lineTo(84, 90); g.stroke();
    /* bay roll-up, left-center, slightly open at the foot */
    R(g, 18, 48, 150, 118, '#2a2e3a', INK, 3);
    var i;
    for (i = 0; i < 9; i++) {
      g.fillStyle = i % 2 ? '#3a3e4c' : '#32364a';
      g.fillRect(20, 50 + i * 11, 146, 10);
      g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(20, 50 + i * 11 + 9, 146, 2);
    }
    /* a warm sliver under the half-open shutter */
    R(g, 22, 148, 142, 16, '#3a2a1c', 0);
    glow(g, 93, 156, 50, 'rgba(255,180,80,.22)');
    g.fillStyle = '#2a2018'; g.fillRect(22, 148, 142, 3);
    /* personnel door + office window, right */
    R(g, 180, 70, 52, 96, '#3a322c', INK, 2.5);
    R(g, 188, 80, 36, 44, '#2a241e', INK, 2);
    /* small window in the door */
    R(g, 196, 88, 20, 16, '#f0c878', INK, 1.5);
    glow(g, 206, 96, 22, 'rgba(255,200,110,.28)');
    ellipse(g, 222, 128, 3, 3, '#c4a060', INK, 1);
    /* office window */
    R(g, 240, 60, 64, 52, '#2a2c34', INK, 2.5);
    R(g, 244, 64, 56, 44, '#f0c070', 0);
    g.fillStyle = 'rgba(255,230,160,.35)'; g.fillRect(244, 64, 20, 44);
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(272, 64); g.lineTo(272, 108); g.stroke();
    g.beginPath(); g.moveTo(244, 86); g.lineTo(300, 86); g.stroke();
    /* clipboard / schedule silhouette in the window */
    R(g, 252, 72, 14, 18, '#d8c8a0', INK, 1);
    glow(g, 272, 86, 36, 'rgba(255,200,110,.3)');
    /* sign */
    R(g, 178, 28, 126, 26, '#f0e4c8', INK, 3);
    txt(g, '\u914d\u8eca', 216, 41, 13, '#5a2a28');
    txt(g, 'DISPATCH', 262, 41, 9, '#3a322c', '800 ');
    /* wall lamp */
    R(g, 232, 54, 10, 6, '#2a2c34', INK, 1.5);
    ellipse(g, 237, 66, 7, 6, '#f0d080', INK, 1.5);
    glow(g, 237, 72, 28, 'rgba(255,200,110,.35)');
    /* oil drum + bike, apron */
    drum(g, 8, 132, 22, 36, '#5a3a28');
    bike(g, 290, 148, 0.55, '#2a3858');
    /* concrete apron / threshold */
    R(g, 4, 166, W0 - 8, 14, '#4a4e58', INK, 2);
    g.fillStyle = 'rgba(0,0,0,.2)'; g.fillRect(18, 168, 150, 4);
    /* building ink only — no box around the night sliver */
    g.strokeStyle = INK; g.lineWidth = 3; g.strokeRect(3, 8, W0 - 6, H0 - 10);
  };

  /* ---------- interior: dispatch bay ---------- */
  function garInside(g, cleared) {
    var RW = 1280, RH = 900;
    rr(g);
    /* back wall */
    corrug(g, 90, 40, 1100, 280, '#4a5064', '#40465a', 22);
    R(g, 90, 40, 1100, 18, '#2a2e3a', INK, 2);
    /* rear bay door, open onto the night quay */
    R(g, 430, 70, 420, 250, '#1a1220', INK, 3);
    quayNight(g, 434, 74, 412, 200);
    /* shutter slats stacked above the opening */
    var i;
    for (i = 0; i < 5; i++) {
      R(g, 430, 70 + i * 8, 420, 8, i % 2 ? '#3a3e4c' : '#32364a', INK, 1.5);
    }
    R(g, 430, 268, 420, 14, '#2a2c34', INK, 2);
    /* yellow caution on the sill */
    for (i = 0; i < 14; i++) {
      g.fillStyle = i % 2 ? '#e8c040' : '#1a1a1e';
      g.fillRect(434 + i * 29, 270, 28, 10);
    }
    /* sign above the bay */
    R(g, 540, 44, 200, 24, '#f0e4c8', INK, 2.5);
    txt(g, '\u914d\u8eca\u5ba4  \u00b7  DISPATCH', 640, 56, 13, '#5a2a28');
    /* left: tool wall + shelves */
    R(g, 110, 80, 260, 200, '#3a3e4c', INK, 2.5);
    R(g, 120, 90, 240, 16, '#2a2c34', 0);
    /* hanging wrenches */
    g.strokeStyle = INK; g.lineWidth = 3;
    for (i = 0; i < 6; i++) {
      var wx = 140 + i * 36;
      g.beginPath(); g.moveTo(wx, 108); g.lineTo(wx, 148 + (i % 3) * 8); g.stroke();
      g.strokeStyle = '#8a8e98'; g.lineWidth = 2;
      g.beginPath(); g.moveTo(wx, 108); g.lineTo(wx, 148 + (i % 3) * 8); g.stroke();
      ellipse(g, wx, 108, 5, 5, '#6a6e78', INK, 1.5);
      g.strokeStyle = INK; g.lineWidth = 3;
    }
    /* bins */
    R(g, 128, 170, 70, 36, '#6a3a28', INK, 2);
    R(g, 204, 170, 70, 36, '#3a5a6a', INK, 2);
    R(g, 280, 170, 70, 36, '#6a5a28', INK, 2);
    txt(g, '\u90e8\u54c1', 239, 188, 11, '#f0e4c8');
    /* air hose reel */
    ellipse(g, 200, 230, 22, 22, '#3a3e48', INK, 2);
    hose(g, 220, 230, 90);
    /* right: schedule board + hook */
    R(g, 900, 90, 260, 170, '#d8c8a0', INK, 3);
    txt(g, '\u914d\u8eca\u8868', 1030, 112, 14, '#5a2a28');
    g.strokeStyle = '#5a3a28'; g.lineWidth = 1.6;
    for (i = 0; i < 7; i++) {
      g.beginPath(); g.moveTo(916, 130 + i * 16); g.lineTo(1144, 130 + i * 16); g.stroke();
    }
    /* a late mark in rust-red */
    g.strokeStyle = '#a84838'; g.lineWidth = 3;
    g.beginPath(); g.moveTo(980, 142); g.lineTo(1100, 142); g.stroke();
    txt(g, 'LATE', 1088, 142, 11, '#a84838', '800 ', 'left');
    /* jacket hook */
    R(g, 1170, 160, 8, 8, '#2a2c34', INK, 1.5);
    if (!cleared) {
      R(g, 1158, 168, 36, 70, '#3a463c', INK, 2);
      R(g, 1164, 178, 24, 28, '#c9a04a', 0);
    }
    /* work lamps */
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(200, 40); g.lineTo(200, 70); g.stroke();
    g.beginPath(); g.moveTo(1080, 40); g.lineTo(1080, 70); g.stroke();
    ellipse(g, 200, 84, 16, 14, '#f0d080', INK, 2);
    ellipse(g, 1080, 84, 16, 14, '#f0d080', INK, 2);
    glow(g, 200, 110, 110, 'rgba(255,200,110,.32)');
    glow(g, 1080, 110, 110, 'rgba(255,200,110,.28)');
    glow(g, 640, 180, 160, 'rgba(180,210,255,.08)');
    /* floor */
    concFloor(g, 90, 320, 1100, 530, '#6a6460', '#5a5450');
    oilStain(g, 300, 620, 70, 22);
    oilStain(g, 860, 700, 90, 26);
    oilStain(g, 640, 500, 50, 16);
    /* tire marks, not a parking-space grid */
    g.strokeStyle = 'rgba(20,16,12,.22)'; g.lineWidth = 8;
    g.beginPath(); g.moveTo(200, 400); g.quadraticCurveTo(400, 520, 360, 800); g.stroke();
    g.beginPath(); g.moveTo(240, 400); g.quadraticCurveTo(430, 530, 400, 800); g.stroke();
    /* bay left: tires + drums */
    tire(g, 160, 520, 28);
    tire(g, 160, 500, 28);
    tire(g, 160, 480, 28);
    drum(g, 210, 500, 36, 70, '#6a3a28');
    drum(g, 250, 520, 32, 60, '#3a4a38');
    crate(g, 300, 540, 80, 56, '\u8ca0\u7269');
    /* a parked bike in the bay */
    bike(g, 980, 560, 1.05, '#2a3858');
    crate(g, 1040, 600, 90, 50, '');
    /* dispatcher desk, mid-left, facing the bay */
    R(g, 200, 640, 280, 100, '#4a3e34', INK, 3);
    R(g, 210, 600, 160, 44, '#2a2c34', INK, 2);
    /* radio */
    ellipse(g, 230, 618, 7, 7, '#3a6a3a', INK, 1.5);
    ellipse(g, 250, 618, 7, 7, '#6a3a2a', INK, 1.5);
    R(g, 266, 610, 48, 18, '#1a2018', INK, 1.5);
    R(g, 330, 614, 28, 14, '#f0e4c8', INK, 1.5);
    /* coffee */
    ellipse(g, 420, 628, 10, 8, '#3a2a22', INK, 1.5);
    /* desk lamp */
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(360, 600); g.lineTo(360, 572); g.lineTo(388, 560); g.stroke();
    ellipse(g, 396, 562, 14, 10, '#f0d080', INK, 2);
    glow(g, 400, 580, 70, 'rgba(255,200,110,.3)');
    if (!cleared) clipBoard(g, 390, 636, -0.15);
    else clipBoard(g, 280, 746, 0.4);
    /* chair */
    R(g, 280, 740, 70, 14, '#3a322c', INK, 2);
    R(g, 290, 754, 12, 40, '#3a322c', INK, 1.5);
    R(g, 328, 754, 12, 40, '#3a322c', INK, 1.5);
    /* hose on the floor, right of the desk, off the centre lane */
    hose(g, 520, 780, 160);
    /* parts stool */
    ellipse(g, 880, 768, 28, 10, '#3a3e48', INK, 2);
    R(g, 868, 772, 8, 28, '#3a3e48', INK, 1.5);
    R(g, 884, 772, 8, 28, '#3a3e48', INK, 1.5);
    /* door / exit at the south */
    R(g, 580, 850, 120, 50, 'rgba(255,220,160,.10)', 0);
    /* wall legs */
    g.fillStyle = '#1b1820'; g.fillRect(0, 0, 90, RH); g.fillRect(RW - 90, 0, 90, RH);
    g.fillRect(0, 850, 580, 50); g.fillRect(700, 850, 580, 50);
    g.strokeStyle = INK; g.lineWidth = 4; g.strokeRect(90, 2, RW - 180, 848);
    var vg = g.createRadialGradient(640, 520, 260, 640, 520, 820);
    vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(10,6,14,.4)');
    g.fillStyle = vg; g.fillRect(0, 0, RW, RH);
    glow(g, 400, 620, 80, 'rgba(255,200,110,.12)');
  }
  S2P.garInside = function (g, cleared) { garInside(g, !!cleared); };

  /* ---------- battle: garage bay (Fierce) ---------- */
  S2P.battleGarage = function (g) {
    var H = (typeof window !== 'undefined' && window.FFF_C2H) || (typeof root !== 'undefined' && root.FFF_C2H);
    var WD = 720, HT = 1280, H0 = 330, x = g, i, y;
    rr(g);
    if (!H) { g.fillStyle = '#1a1410'; g.fillRect(0, 0, WD, HT); return; }
    corrug(g, 0, 0, WD, H0, '#4a5064', '#40465a', 22);
    R(g, 0, 0, WD, 18, '#2a2e3a', H.INK, 2);
    R(g, 220, 16, 280, 26, '#f0e4c8', H.INK, 3);
    txt(g, '\u914d\u8eca\u5ba4  \u00b7  DISPATCH', 360, 29, 14, '#5a2a28');
    /* open bay in the back wall */
    R(g, 160, 50, 400, 220, '#1a1220', H.INK, 3);
    quayNight(g, 164, 54, 392, 180);
    for (i = 0; i < 4; i++) R(g, 160, 50 + i * 8, 400, 8, i % 2 ? '#3a3e4c' : '#32364a', H.INK, 1.5);
    R(g, 160, 250, 400, 14, '#2a2c34', H.INK, 2);
    for (i = 0; i < 13; i++) {
      g.fillStyle = i % 2 ? '#e8c040' : '#1a1a1e';
      g.fillRect(164 + i * 30, 252, 28, 10);
    }
    /* hanging lamps */
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(140, 18); g.lineTo(140, 70); g.stroke();
    g.beginPath(); g.moveTo(580, 18); g.lineTo(580, 70); g.stroke();
    ellipse(g, 140, 86, 14, 14, '#f0d080', INK, 2);
    ellipse(g, 580, 86, 14, 14, '#f0d080', INK, 2);
    glow(g, 140, 110, 90, 'rgba(255,200,110,.34)');
    glow(g, 580, 110, 90, 'rgba(255,200,110,.34)');
    /* concrete floor in perspective */
    var fx = H.fx0;
    g.beginPath();
    g.moveTo(0, H0); g.lineTo(WD, H0); g.lineTo(WD, HT); g.lineTo(0, HT); g.closePath();
    g.fillStyle = H.lg(x, H0, HT, '#6a6460', '#3e3a38');
    g.fill();
    g.save(); g.beginPath(); g.rect(0, H0, WD, HT - H0); g.clip();
    g.strokeStyle = 'rgba(0,0,0,.16)'; g.lineWidth = 2;
    for (i = 0; i <= 14; i++) {
      var u = i * 52;
      g.beginPath(); g.moveTo(fx(u, H0), H0); g.lineTo(fx(u, HT), HT); g.stroke();
    }
    /* a few joints, not a full cross-grid */
    g.strokeStyle = 'rgba(0,0,0,.12)'; g.lineWidth = 1.6;
    for (i = 2; i < 14; i += 4) {
      y = H0 + (HT - H0) * Math.pow(i / 14, 1.5);
      g.beginPath(); g.moveTo(fx(40, y), y); g.lineTo(fx(200, y), y); g.stroke();
      g.beginPath(); g.moveTo(fx(480, y), y); g.lineTo(fx(680, y), y); g.stroke();
    }
    var r = H.seed(21);
    g.fillStyle = 'rgba(255,255,255,.03)';
    for (i = 0; i < 360; i++) g.fillRect(r() * WD, H0 + r() * (HT - H0), 2, 2);
    g.restore();
    /* oil + wear, centre lane mostly clear */
    oilStain(g, 160, 700, 50, 16);
    oilStain(g, 560, 880, 60, 18);
    oilStain(g, 200, 1100, 70, 20);
    H.pool(x, 300, 760, 70, 16, '30,24,18', 0.2);
    H.pool(x, 440, 1020, 80, 18, '30,24,18', 0.16);
    g.fillStyle = 'rgba(20,16,12,.14)';
    g.beginPath(); g.ellipse(360, 980, 80, 24, 0, 0, Math.PI * 2); g.fill();
    /* desk, left mid */
    H.R(x, 30, 500, 200, 90, '#4a3e34', H.INK, 3);
    H.R(x, 40, 464, 120, 40, '#2a2c34', H.INK, 2);
    ellipse(g, 60, 480, 6, 6, '#3a6a3a', INK, 1.5);
    ellipse(g, 80, 480, 6, 6, '#6a3a2a', INK, 1.5);
    clipBoard(g, 160, 548, -0.2);
    H.R(x, 70, 590, 60, 12, '#3a322c', H.INK, 2);
    H.R(x, 80, 602, 10, 30, '#3a322c', H.INK, 1.5);
    H.R(x, 110, 602, 10, 30, '#3a322c', H.INK, 1.5);
    /* schedule board, right wall */
    H.R(x, 560, 360, 140, 110, '#d8c8a0', H.INK, 2.5);
    txt(g, '\u914d\u8eca\u8868', 630, 378, 12, '#5a2a28');
    g.strokeStyle = '#5a3a28'; g.lineWidth = 1.4;
    for (i = 0; i < 5; i++) { g.beginPath(); g.moveTo(572, 396 + i * 14); g.lineTo(688, 396 + i * 14); g.stroke(); }
    /* tires + drums, right mid */
    tire(g, 640, 560, 24);
    tire(g, 640, 542, 24);
    drum(g, 580, 560, 32, 60, '#6a3a28');
    crate(g, 520, 600, 70, 46, '\u8ca0\u7269');
    /* hose coil + tools, lower sides */
    function hoseCoil(cx, cy, r) {
      g.strokeStyle = INK; g.lineWidth = 6;
      g.beginPath(); g.arc(cx, cy, r, 0.2, Math.PI * 1.85); g.stroke();
      g.strokeStyle = '#3a4a38'; g.lineWidth = 3.6;
      g.beginPath(); g.arc(cx, cy, r, 0.2, Math.PI * 1.85); g.stroke();
      g.strokeStyle = '#2a3a28'; g.lineWidth = 2.4;
      g.beginPath(); g.arc(cx, cy, r * 0.6, 0.5, Math.PI * 1.6); g.stroke();
    }
    hoseCoil(120, 980, 22);
    hoseCoil(90, 1020, 16);
    hoseCoil(600, 1040, 20);
    drum(g, 40, 1120, 36, 56, '#3a4a38');
    crate(g, 90, 1180, 70, 40, '');
    tire(g, 640, 1180, 26);
    /* light pools */
    glow(g, 140, H0 + 40, 70, 'rgba(255,200,110,.16)');
    glow(g, 580, H0 + 40, 70, 'rgba(255,200,110,.16)');
    glow(g, 140, 960, 90, 'rgba(255,200,110,.18)');
    glow(g, 580, 1080, 90, 'rgba(255,200,110,.16)');
    glow(g, 360, 1200, 80, 'rgba(255,210,140,.1)');
    H.vign(x, 0.58);
    H.grade(x, 'rgba(40,50,70,.18)', 'rgba(20,10,12,.28)');
  };

  /* ---------- battle: depot approach (Strategic / Compassionate) ---------- */
  S2P.battleApproach = function (g) {
    var H = (typeof window !== 'undefined' && window.FFF_C2H) || (typeof root !== 'undefined' && root.FFF_C2H);
    var WD = 720, HT = 1280, H0 = 330, x = g, i;
    rr(g);
    if (!H) { g.fillStyle = '#1a1410'; g.fillRect(0, 0, WD, HT); return; }
    /* night sky + north bank */
    var sky = g.createLinearGradient(0, 0, 0, H0);
    sky.addColorStop(0, '#14182a'); sky.addColorStop(1, '#243048');
    g.fillStyle = sky; g.fillRect(0, 0, WD, H0);
    /* far Minato-sō wall */
    R(g, 0, 40, WD, 90, '#5a4a40', INK, 2);
    for (i = 0; i < 6; i++) {
      R(g, 20 + i * 120, 55, 70, 36, '#f0c878', INK, 1.5);
      glow(g, 55 + i * 120, 73, 24, 'rgba(255,200,110,.2)');
    }
    /* canal */
    g.fillStyle = '#1a2434'; g.fillRect(0, 130, WD, 120);
    g.strokeStyle = 'rgba(120,180,220,.22)'; g.lineWidth = 1.6;
    for (i = 0; i < 5; i++) { g.beginPath(); g.moveTo(0, 150 + i * 16); g.lineTo(WD, 148 + i * 16); g.stroke(); }
    /* flower boat, right */
    g.beginPath();
    g.ellipse(620, 200, 160, 48, 0, 0, Math.PI * 2);
    g.fillStyle = '#e8e0d4'; g.fill(); g.strokeStyle = INK; g.lineWidth = 3; g.stroke();
    g.beginPath(); g.ellipse(620, 188, 148, 28, 0, 0, Math.PI * 2);
    g.fillStyle = '#c45a3a'; g.fill();
    g.fillStyle = '#2a3a20'; g.fillRect(500, 176, 230, 28);
    g.fillStyle = '#c45a62';
    for (i = 0; i < 40; i++) g.fillRect(508 + (i * 37) % 220, 180 + (i * 11) % 20, 4, 4);
    /* south lip + flowers under H0 */
    R(g, 0, 250, WD, 20, '#3a3e4c', INK, 2);
    g.fillStyle = '#5a3040'; g.fillRect(0, 270, WD, 60);
    g.fillStyle = '#c45a62';
    for (i = 0; i < 90; i++) g.fillRect((i * 53) % WD, 278 + (i * 17) % 40, 4, 4);
    g.fillStyle = '#e8e0d4';
    for (i = 0; i < 8; i++) g.beginPath(); g.ellipse(80 + i * 90, 300, 18, 8, 0, 0, Math.PI * 2); g.fill();
    /* depot wall as the back of the fight floor */
    corrug(g, 0, H0 - 8, WD, 16, '#4a5068', '#3e445a', 16);
    /* wet flower / concrete floor */
    var fx = H.fx0;
    g.beginPath();
    g.moveTo(0, H0); g.lineTo(WD, H0); g.lineTo(WD, HT); g.lineTo(0, HT); g.closePath();
    g.fillStyle = H.lg(x, H0, HT, '#5a4850', '#3a3238');
    g.fill();
    g.save(); g.beginPath(); g.rect(0, H0, WD, HT - H0); g.clip();
    g.strokeStyle = 'rgba(0,0,0,.14)'; g.lineWidth = 2;
    for (i = 0; i <= 12; i++) {
      var u = i * 60;
      g.beginPath(); g.moveTo(fx(u, H0), H0); g.lineTo(fx(u, HT), HT); g.stroke();
    }
    g.restore();
    /* depot door, mid-back, closed metal */
    H.R(x, 260, 300, 200, 120, '#2a2e3a', H.INK, 3);
    corrug(g, 266, 306, 188, 90, '#3a3e4c', '#32364a', 16);
    R(g, 330, 340, 60, 70, '#242830', INK, 2.5);
    R(g, 348, 352, 24, 16, '#8a7a40', INK, 1.5);
    txt(g, 'DEPOT', 360, 318, 11, '#d8c8a0');
    /* garage edge, left */
    corrug(g, 0, 280, 90, 200, '#4a5068', '#3e445a', 12);
    R(g, 0, 280, 90, 16, '#3a3e4c', INK, 2);
    R(g, 10, 310, 50, 36, '#f0c070', INK, 2);
    glow(g, 35, 328, 30, 'rgba(255,200,110,.25)');
    /* missed freight crates + bike, sides */
    crate(g, 40, 520, 90, 60, 'LATE');
    crate(g, 80, 570, 70, 48, '');
    crate(g, 560, 500, 100, 64, '\u8ca0\u7269');
    crate(g, 600, 554, 80, 50, '');
    bike(g, 80, 680, 0.85, '#2a3858');
    drum(g, 620, 680, 36, 64, '#6a3a28');
    /* quay lamps */
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(80, 200); g.lineTo(80, 80); g.stroke();
    g.beginPath(); g.moveTo(640, 200); g.lineTo(640, 80); g.stroke();
    ellipse(g, 80, 78, 16, 10, '#f0d080', INK, 2);
    ellipse(g, 640, 78, 16, 10, '#f0d080', INK, 2);
    glow(g, 80, 120, 90, 'rgba(255,200,110,.3)');
    glow(g, 640, 120, 90, 'rgba(255,200,110,.3)');
    /* wear + light pools, centre lane clear */
    oilStain(g, 160, 900, 60, 18);
    oilStain(g, 560, 1040, 70, 20);
    H.pool(x, 240, 860, 80, 18, '30,24,18', 0.18);
    H.pool(x, 500, 1120, 90, 20, '30,24,18', 0.16);
    g.fillStyle = 'rgba(20,12,12,.12)';
    g.beginPath(); g.ellipse(360, 1000, 86, 26, 0, 0, Math.PI * 2); g.fill();
    glow(g, 120, 980, 90, 'rgba(255,200,110,.16)');
    glow(g, 600, 1100, 90, 'rgba(255,200,110,.14)');
    glow(g, 360, 1220, 80, 'rgba(255,210,140,.1)');
    hose(g, 80, 1180, 120);
    crate(g, 40, 1200, 70, 40, '');
    drum(g, 640, 1180, 32, 50, '#3a4a38');
    rain(g, WD, HT, 70, 5);
    H.vign(x, 0.6);
    H.grade(x, 'rgba(40,50,90,.2)', 'rgba(20,10,20,.28)');
  };

  /* ---------- line cards ---------- */
  S2P.lineCardGar = function (g, who, phase) {
    var W = 900, H = 420;
    R(g, 0, 0, W, H, '#1a1520', 0);
    R(g, 8, 8, W - 16, H - 16, '#2a2230', INK, 3);
    var title = {
      sada: 'Sada, Masa\u2019s dispatcher',
      fierce: 'Fierce  \u00b7  through the bay',
      strategic: 'Strategic  \u00b7  already late',
      compassionate: 'Compassionate  \u00b7  stand aside',
      win: 'After the door is won'
    };
    var body = {
      sada: 'He runs the quay garage and the depot door. The clipboard is the schedule. If you want the yard, you go through him.',
      fierce: 'Straight through the dispatcher. No angle, no wait. You take the bay and his guards in the garage.',
      strategic: 'The freight is already late. You use the missed loads against him \u2014 he is off his own schedule. The fight is on the depot approach, in front of the door.',
      compassionate: 'You ask him to stand aside so the yard can run honest again. He will not. The fight still happens, same rule as Kaneda, out on the approach.',
      win: 'The door is open. Sada is off the quay. Four Corners points at the Subway Freight Depot. Do not start Masa\u2019s seal yet.'
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
