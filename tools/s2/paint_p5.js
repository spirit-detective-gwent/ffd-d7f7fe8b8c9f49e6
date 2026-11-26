/* v6.5.63 FFF_S2P phase 5: Subway Freight Depot rooms, shutter battle, Masa line cards.
 * Canvas2D, ink outlines, two-tone cel. Preview-first; no new always-running loops.
 * Reuses Masa portraits (masa_calm/angry/beaten) and mb2_depotK sheets. */
(function (root) {
  var S2P = root.FFF_S2P = root.FFF_S2P || {};
  var INK = '#1a1220';
  var RW = 1280, RH = 900;
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
    var i, n;
    for (i = x, n = 0; i < x + w; i += step, n++) {
      g.fillStyle = n % 2 ? c2 : c1; g.fillRect(i, y, step - 1, h);
      g.fillStyle = 'rgba(255,255,255,.06)'; g.fillRect(i, y, 2, h);
      g.fillStyle = 'rgba(0,0,0,.18)'; g.fillRect(i + step - 2, y, 2, h);
    }
  }
  function concFloor(g, x, y, w, h, c1, c2, seedN) {
    g.fillStyle = c1; g.fillRect(x, y, w, h);
    var i, r = function (s) { var v = s; return function () { v = (v * 16807) % 2147483647; return (v - 1) / 2147483646; }; }(seedN || 19);
    g.fillStyle = 'rgba(0,0,0,.06)';
    for (i = 0; i < 220; i++) g.fillRect(x + r() * w, y + r() * h, 8 + r() * 18, 3 + r() * 4);
    g.fillStyle = 'rgba(255,255,255,.03)';
    for (i = 0; i < 180; i++) g.fillRect(x + r() * w, y + r() * h, 2, 2);
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
  function caution(g, x, y, w, h) {
    var i, n = Math.max(4, Math.floor(w / 22));
    for (i = 0; i < n; i++) {
      g.fillStyle = i % 2 ? '#e8c040' : '#1a1a1e';
      g.fillRect(x + i * (w / n), y, w / n + 0.5, h);
    }
    g.strokeStyle = INK; g.lineWidth = 2; g.strokeRect(x, y, w, h);
  }
  function lamp(g, x, y) {
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(x, 40); g.lineTo(x, y); g.stroke();
    ellipse(g, x, y + 14, 16, 12, '#f0d080', INK, 2);
    glow(g, x, y + 40, 90, 'rgba(255,200,110,.28)');
  }
  function steelDoor(g, x, y, w, h, label) {
    R(g, x, y, w, h, '#3a4250', INK, 3);
    R(g, x + 8, y + 10, w - 16, h - 20, '#2a323e', INK, 2);
    ellipse(g, x + w - 18, y + h * 0.55, 5, 5, '#c4a060', INK, 1.4);
    if (label) txt(g, label, x + w / 2, y + 22, 11, '#f0e4c8', '800 ');
  }
  function crate(g, x, y, w, h, label) {
    R(g, x, y, w, h, '#8a5a38', INK, 2);
    g.fillStyle = 'rgba(0,0,0,.18)'; g.fillRect(x + 4, y + 4, w - 8, 6);
    g.strokeStyle = 'rgba(40,20,10,.35)'; g.lineWidth = 2;
    g.beginPath(); g.moveTo(x + 6, y + h * 0.5); g.lineTo(x + w - 6, y + h * 0.5); g.stroke();
    g.beginPath(); g.moveTo(x + 8, y + 8); g.lineTo(x + w - 8, y + h - 8); g.stroke();
    g.beginPath(); g.moveTo(x + w - 8, y + 8); g.lineTo(x + 8, y + h - 8); g.stroke();
    if (label) txt(g, label, x + w / 2, y + h / 2 + 4, 11, '#f0e4c8');
  }
  function pallet(g, x, y, w, h) {
    R(g, x, y, w, 8, '#6a4a30', INK, 2);
    R(g, x, y + h - 8, w, 8, '#6a4a30', INK, 2);
    R(g, x + 6, y, 8, h, '#5a3e28', INK, 1.5);
    R(g, x + w / 2 - 4, y, 8, h, '#5a3e28', INK, 1.5);
    R(g, x + w - 14, y, 8, h, '#5a3e28', INK, 1.5);
  }
  function drum(g, x, y, w, h, col) {
    R(g, x, y, w, h, col || '#6a3a28', INK, 2);
    g.strokeStyle = 'rgba(255,220,160,.18)'; g.lineWidth = 2;
    g.beginPath(); g.moveTo(x + 4, y + 8); g.lineTo(x + 4, y + h - 8); g.stroke();
    ellipse(g, x + w / 2, y, w / 2, 6, '#3a2a22', INK, 1.5);
  }
  function wheel(g, x, y, r) {
    ellipse(g, x, y, r, r, '#1a1220', INK, 3);
    ellipse(g, x, y, r * 0.55, r * 0.55, '#3a3e48', INK, 1.8);
    ellipse(g, x, y, r * 0.18, r * 0.18, '#8a8fa0', INK, 1.4);
  }
  function moto(g, bx, by, s, col) {
    s = s || 1;
    g.save(); g.translate(bx, by); g.scale(s, s);
    g.fillStyle = 'rgba(0,0,0,.28)';
    g.beginPath(); g.ellipse(55, 78, 70, 10, 0, 0, 7); g.fill();
    wheel(g, 18, 70, 20); wheel(g, 100, 70, 20);
    R(g, 40, 78, 36, 6, '#6a707c', INK, 1.6);
    g.strokeStyle = INK; g.lineWidth = 4; g.lineJoin = 'round';
    g.beginPath(); g.moveTo(18, 70); g.lineTo(48, 42); g.lineTo(86, 42); g.lineTo(100, 70); g.stroke();
    ellipse(g, 58, 38, 22, 12, col || '#d46028', INK, 2);
    R(g, 68, 30, 28, 12, '#1a1520', INK, 2);
    g.beginPath(); g.moveTo(100, 70); g.lineTo(112, 28); g.stroke();
    g.beginPath(); g.moveTo(100, 24); g.lineTo(124, 20); g.stroke();
    ellipse(g, 118, 32, 7, 7, '#f0e4c0', INK, 1.6);
    g.restore();
  }
  function forklift(g, x, y, s) {
    s = s || 1;
    g.save(); g.translate(x, y); g.scale(s, s);
    R(g, 40, 20, 90, 46, '#e8c040', INK, 2.5);
    R(g, 48, 8, 36, 20, '#2a323e', INK, 2);
    R(g, 52, 12, 28, 12, '#7ec8e8', INK, 1.4);
    R(g, 100, 8, 18, 58, '#3a3e48', INK, 2);
    R(g, 118, 44, 54, 6, '#6a707c', INK, 2);
    R(g, 118, 54, 54, 6, '#6a707c', INK, 2);
    wheel(g, 60, 70, 14); wheel(g, 110, 70, 14);
    g.restore();
  }
  function graySeal(g, x, y, r) {
    ellipse(g, x, y, r, r, '#5a5e68', INK, 2);
    ellipse(g, x, y, r * 0.72, r * 0.72, '#4a4e58', INK, 1.4);
    txt(g, '\u7070', x, y, Math.max(10, r * 0.7), '#d8d0c0', '900 ');
  }
  function manifest(g, x, y, w, h, sealed) {
    R(g, x, y, w, h, '#efe6d2', INK, 2);
    R(g, x, y, w, 18, '#5a2a28', INK, 2);
    txt(g, '\u7a4d\u8377\u8868', x + w / 2, y + 9, 11, '#f0e4c8', '800 ');
    var i;
    g.strokeStyle = '#5a3a28'; g.lineWidth = 1.2;
    for (i = 0; i < 6; i++) { g.beginPath(); g.moveTo(x + 8, y + 28 + i * 12); g.lineTo(x + w - 8, y + 28 + i * 12); g.stroke(); }
    if (sealed) graySeal(g, x + w - 22, y + h - 22, 14);
  }
  function lockers(g, x, y, n, h) {
    var i, w = 44;
    for (i = 0; i < n; i++) {
      R(g, x + i * w, y, w - 2, h, i % 2 ? '#4a5060' : '#3e4654', INK, 2);
      ellipse(g, x + i * w + w - 14, y + h * 0.5, 3, 3, '#c4a060', INK, 1);
      R(g, x + i * w + 8, y + 8, w - 18, 10, '#2a323e', 0);
    }
  }
  function clockPunch(g, x, y) {
    R(g, x, y, 70, 90, '#3a3e48', INK, 2.5);
    R(g, x + 8, y + 10, 54, 36, '#1a2018', INK, 2);
    txt(g, '02:14', x + 35, y + 28, 12, '#8fd6a0', '800 ');
    R(g, x + 16, y + 54, 38, 22, '#2a2c34', INK, 2);
    txt(g, '\u6253\u523b', x + 35, y + 84, 10, '#f0e4c8', '800 ');
  }
  function hardhat(g, x, y) {
    ellipse(g, x, y, 16, 8, '#e8c040', INK, 2);
    R(g, x - 16, y - 2, 32, 6, '#d4a830', INK, 1.5);
    ellipse(g, x, y - 6, 14, 8, '#e8c040', INK, 2);
  }
  function shell(g, ja, en) {
    /* side walls + south exit cut, same family as the quay garage */
    g.fillStyle = '#1b1820';
    g.fillRect(0, 0, 90, RH); g.fillRect(RW - 90, 0, 90, RH);
    g.fillRect(0, 850, 580, 50); g.fillRect(700, 850, 580, 50);
    g.strokeStyle = INK; g.lineWidth = 4; g.strokeRect(90, 2, RW - 180, 848);
    if (ja) {
      R(g, 520, 8, 240, 28, '#f0e4c8', INK, 2.5);
      txt(g, ja + (en ? '  \u00b7  ' + en : ''), 640, 22, 13, '#5a2a28');
    }
    var vg = g.createRadialGradient(640, 520, 260, 640, 520, 820);
    vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(10,6,14,.4)');
    g.fillStyle = vg; g.fillRect(0, 0, RW, RH);
  }
  function backWall(g, col1, col2) {
    corrug(g, 90, 40, 1100, 280, col1 || '#4a5064', col2 || '#40465a', 22);
    R(g, 90, 40, 1100, 18, '#2a2e3a', INK, 2);
  }

  /* ---------- 1. Yard gate ---------- */
  S2P.depYard = function (g, cleared) {
    rr(g);
    backWall(g, '#3a4254', '#323848');
    /* open street door onto the quay night — rain stays in the opening */
    R(g, 470, 58, 340, 260, '#1a1220', INK, 3);
    var sky = g.createLinearGradient(0, 62, 0, 300);
    sky.addColorStop(0, '#1a2238'); sky.addColorStop(1, '#1a2430');
    g.fillStyle = sky; g.fillRect(474, 62, 332, 210);
    g.fillStyle = '#5a3040'; g.fillRect(474, 230, 332, 40);
    g.fillStyle = '#c45a62';
    var i;
    for (i = 0; i < 20; i++) g.fillRect(480 + (i * 41) % 320, 236 + (i * 11) % 16, 3, 3);
    g.save(); g.beginPath(); g.rect(474, 62, 332, 210); g.clip();
    g.strokeStyle = 'rgba(200,220,255,.35)'; g.lineWidth = 1.2;
    var r = function (s) { var v = s; return function () { v = (v * 16807) % 2147483647; return (v - 1) / 2147483646; }; }(7);
    for (i = 0; i < 18; i++) {
      var rx = 474 + r() * 332, ry = 62 + r() * 210, L = 10 + r() * 16;
      g.beginPath(); g.moveTo(rx, ry); g.lineTo(rx + 3, ry + L); g.stroke();
    }
    g.restore();
    caution(g, 474, 270, 332, 12);
    R(g, 540, 44, 200, 22, '#f0e4c8', INK, 2);
    txt(g, '\u5730\u4e0b\u9244\u8ca0\u7269', 640, 55, 13, '#5a2a28');
    lamp(g, 220, 70); lamp(g, 1060, 70);
    concFloor(g, 90, 320, 1100, 530, '#6a6460', '#5a5450', 11);
    oilStain(g, 300, 700, 50, 16); oilStain(g, 900, 640, 60, 18);
    /* chain-link / barrier left */
    R(g, 120, 360, 14, 280, '#3a3e48', INK, 2);
    g.strokeStyle = '#6a707c'; g.lineWidth = 1.4;
    for (i = 0; i < 8; i++) { g.beginPath(); g.moveTo(134, 380 + i * 32); g.lineTo(280, 380 + i * 32); g.stroke(); }
    for (i = 0; i < 5; i++) { g.beginPath(); g.moveTo(140 + i * 30, 360); g.lineTo(140 + i * 30, 640); g.stroke(); }
    crate(g, 160, 660, 90, 70, '\u8ca0\u7269');
    drum(g, 260, 680, 36, 60, '#3a4a38');
    /* meeting desk / stand, in the 640 frame — Masa waits here */
    R(g, 430, 600, 220, 22, '#5c4638', INK, 3);
    R(g, 430, 622, 220, 80, '#4a3e34', INK, 3);
    R(g, 448, 608, 48, 16, '#2a2c34', INK, 1.5);
    hardhat(g, 620, 600);
    if (!cleared) {
      /* clipboard of the night's yard sheet */
      R(g, 500, 636, 70, 48, '#efe6d2', INK, 2);
    }
    steelDoor(g, 900, 80, 90, 200, '\u6253\u523b');
    steelDoor(g, 1020, 80, 90, 200, '\u8377\u5f79');
    lockers(g, 880, 520, 4, 140);
    hardhat(g, 900, 500); hardhat(g, 960, 500);
    ellipse(g, 560, 740, 22, 8, '#c4a060', INK, 2);
    R(g, 552, 740, 8, 36, '#3b2a22', INK, 2);
    R(g, 360, 800, 28, 40, '#d46028', INK, 2);
    R(g, 352, 792, 44, 10, '#d46028', INK, 2);
    /* rain coats */
    R(g, 118, 200, 36, 70, '#3a463c', INK, 2);
    R(g, 160, 210, 36, 60, '#2a3858', INK, 2);
    shell(g, '\u9580', 'Yard gate');
    glow(g, 640, 200, 160, 'rgba(180,210,255,.08)');
  };

  /* ---------- 2. Time-clock office ---------- */
  S2P.depClock = function (g, cleared) {
    rr(g);
    backWall(g, '#4a5854', '#3e4c48');
    /* window into the yard */
    R(g, 430, 70, 420, 200, '#1a1220', INK, 3);
    corrug(g, 436, 76, 408, 188, '#3a4254', '#323848', 18);
    lamp(g, 200, 70); lamp(g, 1080, 70);
    concFloor(g, 90, 320, 1100, 530, '#6e6a62', '#5a5650', 23);
    /* card rack */
    R(g, 140, 90, 240, 200, '#3a3e48', INK, 2.5);
    txt(g, '\u30bf\u30a4\u30e0\u30ab\u30fc\u30c9', 260, 112, 12, '#f0e4c8');
    var i, j;
    for (j = 0; j < 4; j++) for (i = 0; i < 5; i++) {
      R(g, 160 + i * 40, 130 + j * 36, 32, 28, (i + j) % 3 ? '#efe6d2' : '#d8c8a0', INK, 1.2);
    }
    clockPunch(g, 400, 120);
    /* office desk, in frame */
    R(g, 400, 560, 300, 24, '#5c4638', INK, 3);
    R(g, 400, 584, 300, 100, '#4a3e34', INK, 3);
    R(g, 416, 568, 44, 16, '#2a2430', INK, 1.5);
    R(g, 470, 568, 70, 16, '#efe6d2', INK, 1.5);
    ellipse(g, 570, 572, 10, 8, '#3a2a22', INK, 1.5);
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(660, 560); g.lineTo(660, 528); g.lineTo(688, 516); g.stroke();
    ellipse(g, 696, 516, 14, 10, '#f0d080', INK, 2);
    glow(g, 690, 550, 70, 'rgba(255,200,110,.3)');
    lockers(g, 860, 400, 5, 200);
    /* filing */
    R(g, 160, 500, 180, 200, '#4a5060', INK, 3);
    R(g, 170, 520, 160, 12, '#3a3e48', INK, 1.5);
    R(g, 170, 560, 160, 12, '#3a3e48', INK, 1.5);
    R(g, 170, 600, 160, 12, '#3a3e48', INK, 1.5);
    txt(g, '\u53f0\u5e33', 250, 490, 12, '#f0e4c8');
    /* notice board */
    R(g, 900, 90, 200, 180, '#d8c8a0', INK, 3);
    txt(g, '\u5f53\u756a\u8868', 1000, 112, 13, '#5a2a28');
    g.strokeStyle = '#5a3a28'; g.lineWidth = 1.4;
    for (i = 0; i < 6; i++) { g.beginPath(); g.moveTo(916, 130 + i * 20); g.lineTo(1084, 130 + i * 20); g.stroke(); }
    if (!cleared) { g.strokeStyle = '#a84838'; g.lineWidth = 3; g.beginPath(); g.moveTo(940, 150); g.lineTo(1060, 150); g.stroke(); }
    ellipse(g, 760, 760, 22, 8, '#c4a060', INK, 2);
    R(g, 752, 760, 8, 36, '#3b2a22', INK, 2);
    shell(g, '\u6253\u523b', 'Time clock');
  };

  /* ---------- 3. Loading bay ---------- */
  S2P.depBay = function (g, cleared) {
    rr(g);
    backWall(g, '#4a5064', '#40465a');
    /* wide dock opening onto night */
    R(g, 280, 50, 720, 270, '#1a1220', INK, 3);
    var sky = g.createLinearGradient(0, 54, 0, 300);
    sky.addColorStop(0, '#14182a'); sky.addColorStop(1, '#1a2434');
    g.fillStyle = sky; g.fillRect(286, 56, 708, 220);
    /* far quay hint */
    g.fillStyle = '#5a3040'; g.fillRect(286, 230, 708, 30);
    /* truck at the dock: trailer + cab + wheels */
    R(g, 340, 110, 400, 150, '#3a4250', INK, 2.5);
    R(g, 350, 120, 90, 80, '#2a323e', INK, 1.5);
    R(g, 450, 120, 90, 80, '#2a323e', INK, 1.5);
    R(g, 550, 120, 90, 80, '#2a323e', INK, 1.5);
    R(g, 650, 120, 80, 80, '#2a323e', INK, 1.5);
    txt(g, 'KITSUNE', 540, 210, 13, '#f0e4c8', '800 ');
    R(g, 740, 140, 110, 120, '#2a3850', INK, 2.5);
    R(g, 752, 150, 70, 44, '#7ec8e8', INK, 1.5);
    R(g, 820, 200, 28, 36, '#e8c040', INK, 1.5);
    ellipse(g, 400, 262, 22, 22, '#1a1220', INK, 2);
    ellipse(g, 520, 262, 22, 22, '#1a1220', INK, 2);
    ellipse(g, 640, 262, 22, 22, '#1a1220', INK, 2);
    ellipse(g, 800, 262, 22, 22, '#1a1220', INK, 2);
    caution(g, 286, 276, 708, 14);
    lamp(g, 200, 70); lamp(g, 640, 40); lamp(g, 1080, 70);
    concFloor(g, 90, 320, 1100, 530, '#6a6460', '#5a5450', 31);
    oilStain(g, 280, 700, 70, 20); oilStain(g, 980, 620, 60, 18);
    pallet(g, 140, 760, 130, 28);
    crate(g, 150, 690, 110, 70, '\u8ca0\u7269');
    crate(g, 180, 620, 90, 70, '');
    crate(g, 200, 560, 80, 60, '');
    pallet(g, 1000, 760, 130, 28);
    crate(g, 1010, 690, 110, 70, '');
    crate(g, 1030, 630, 90, 60, '');
    drum(g, 300, 700, 36, 60, '#6a3a28');
    drum(g, 340, 720, 32, 50, '#3a4a38');
    drum(g, 920, 700, 36, 60, '#3a4a38');
    /* cones */
    R(g, 400, 780, 28, 40, '#d46028', INK, 2);
    R(g, 392, 772, 44, 10, '#d46028', INK, 2);
    R(g, 850, 780, 28, 40, '#d46028', INK, 2);
    R(g, 842, 772, 44, 10, '#d46028', INK, 2);
    forklift(g, 700, 600, 1.15);
    /* dock leveler, off the walking centre */
    R(g, 500, 400, 280, 18, '#4a4e58', INK, 2);
    caution(g, 500, 400, 280, 12);
    /* side tire marks only */
    g.strokeStyle = 'rgba(20,16,12,.22)'; g.lineWidth = 8;
    g.beginPath(); g.moveTo(180, 400); g.quadraticCurveTo(240, 560, 200, 820); g.stroke();
    g.beginPath(); g.moveTo(1060, 400); g.quadraticCurveTo(1100, 600, 1080, 820); g.stroke();
    shell(g, '\u8377\u5f79', 'Loading bay');
  };

  /* ---------- 4. Crate stacks ---------- */
  S2P.depCrates = function (g, cleared) {
    rr(g);
    backWall(g, '#4a4038', '#3e3630');
    lamp(g, 240, 70); lamp(g, 640, 50); lamp(g, 1040, 70);
    concFloor(g, 90, 320, 1100, 530, '#6a5e54', '#5a5048', 41);
    oilStain(g, 640, 780, 50, 14);
    function stack(x, y, rows, label) {
      var k;
      for (k = 0; k < rows; k++) crate(g, x + (k % 2) * 6, y - k * 62, 110, 66, k === 0 ? label : '');
    }
    stack(140, 720, 4, '\u8ca0\u7269');
    stack(280, 760, 3, '');
    stack(420, 700, 5, '\u5317');
    stack(860, 740, 4, '\u6771');
    stack(1000, 700, 5, '');
    /* open crate, packing list — in frame */
    crate(g, 560, 640, 140, 80, '');
    R(g, 580, 652, 100, 50, '#efe6d2', INK, 1.5);
    txt(g, '\u7a4d\u8377', 630, 676, 12, '#5a2a28');
    /* hand truck */
    g.strokeStyle = INK; g.lineWidth = 4;
    g.beginPath(); g.moveTo(740, 780); g.lineTo(740, 640); g.lineTo(800, 640); g.stroke();
    ellipse(g, 740, 790, 14, 14, '#1a1220', INK, 2);
    /* rope coil */
    g.strokeStyle = '#6a4a28'; g.lineWidth = 6;
    g.beginPath(); g.arc(780, 820, 22, 0.2, Math.PI * 1.8); g.stroke();
    /* stencil on the back wall */
    txt(g, '\u8ca0\u7269\u7f6e\u304d\u5834', 640, 180, 22, 'rgba(240,228,200,.2)', '900 ');
    shell(g, '\u8ca0\u7269', 'Crate stacks');
  };

  /* ---------- 5. Cold store ---------- */
  S2P.depCold = function (g, cleared) {
    rr(g);
    corrug(g, 90, 40, 1100, 280, '#3a5060', '#324850', 22);
    R(g, 90, 40, 1100, 18, '#1a2830', INK, 2);
    /* insulated door, left */
    R(g, 140, 80, 120, 230, '#2a3a44', INK, 3);
    R(g, 150, 90, 100, 16, '#8aa0b0', INK, 1.5);
    ellipse(g, 240, 200, 8, 8, '#c4a060', INK, 1.5);
    /* frost window */
    R(g, 430, 80, 420, 200, '#d8e8f0', INK, 3);
    g.fillStyle = 'rgba(180,210,230,.35)'; g.fillRect(436, 86, 408, 188);
    var i, r = function (s) { var v = s; return function () { v = (v * 16807) % 2147483647; return (v - 1) / 2147483646; }; }(13);
    g.fillStyle = 'rgba(255,255,255,.35)';
    for (i = 0; i < 80; i++) g.fillRect(440 + r() * 400, 90 + r() * 180, 6 + r() * 10, 2);
    txt(g, '-18\u00b0', 640, 160, 28, 'rgba(40,70,90,.45)', '900 ');
    /* gauge */
    ellipse(g, 1000, 160, 36, 36, '#efe6d2', INK, 2);
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(1000, 160); g.lineTo(1018, 148); g.stroke();
    txt(g, 'KEEP', 1000, 210, 11, '#f0e4c8');
    lamp(g, 260, 60); lamp(g, 640, 50); lamp(g, 1020, 60);
    /* cold floor, bluer */
    concFloor(g, 90, 320, 1100, 530, '#5a6a70', '#4a5a60', 17);
    g.fillStyle = 'rgba(200,230,255,.06)'; g.fillRect(90, 320, 1100, 530);
    /* hanging boxes / rails */
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(200, 320); g.lineTo(1080, 320); g.stroke();
    function hang(x, col) {
      g.strokeStyle = INK; g.lineWidth = 2;
      g.beginPath(); g.moveTo(x, 320); g.lineTo(x, 380); g.stroke();
      R(g, x - 28, 380, 56, 70, col, INK, 2);
    }
    hang(300, '#6a4a48'); hang(400, '#5a4038'); hang(500, '#6a4a48');
    hang(860, '#5a4038'); hang(960, '#6a4a48'); hang(1060, '#5a4038');
    crate(g, 180, 700, 90, 70, '');
    crate(g, 1000, 720, 90, 60, '');
    /* frost pools */
    g.fillStyle = 'rgba(220,240,255,.12)';
    g.beginPath(); g.ellipse(640, 700, 80, 18, 0, 0, 7); g.fill();
    g.beginPath(); g.ellipse(400, 800, 50, 12, 0, 0, 7); g.fill();
    glow(g, 640, 200, 200, 'rgba(180,220,240,.12)');
    shell(g, '\u51b7\u51cd', 'Cold store');
  };

  /* ---------- 6. Parts cage ---------- */
  S2P.depCage = function (g, cleared) {
    rr(g);
    backWall(g, '#4a5064', '#40465a');
    lamp(g, 220, 70); lamp(g, 1060, 70);
    concFloor(g, 90, 320, 1100, 530, '#6a6460', '#5a5450', 29);
    oilStain(g, 400, 760, 40, 14);
    /* chain-link cage around the shelves, in frame */
    function mesh(x0, y0, w, h) {
      g.save(); g.beginPath(); g.rect(x0, y0, w, h); g.clip();
      g.strokeStyle = 'rgba(140,150,160,.55)'; g.lineWidth = 1.3;
      var i;
      for (i = -h; i < w + h; i += 14) {
        g.beginPath(); g.moveTo(x0 + i, y0); g.lineTo(x0 + i + h, y0 + h); g.stroke();
        g.beginPath(); g.moveTo(x0 + i, y0 + h); g.lineTo(x0 + i + h, y0); g.stroke();
      }
      g.restore();
    }
    R(g, 300, 80, 680, 24, '#3a3e48', INK, 2);
    mesh(300, 104, 20, 500); mesh(960, 104, 20, 500);
    mesh(316, 80, 644, 20);
    R(g, 300, 80, 16, 520, '#3a3e48', INK, 2);
    R(g, 964, 80, 16, 520, '#3a3e48', INK, 2);
    var i, j;
    /* shelves inside */
    R(g, 360, 200, 560, 14, '#4a3a30', INK, 2);
    R(g, 360, 320, 560, 14, '#4a3a30', INK, 2);
    R(g, 360, 440, 560, 14, '#4a3a30', INK, 2);
    var cols = ['#c45a3a', '#3a6a8a', '#c4a030', '#4a6a3a', '#6a707c', '#8a3a28'];
    for (i = 0; i < 6; i++) {
      R(g, 380 + i * 88, 230, 70, 36, cols[i], INK, 2);
      R(g, 380 + i * 88, 350, 70, 36, cols[(i + 2) % 6], INK, 2);
      ellipse(g, 415 + i * 88, 500, 16, 12, cols[(i + 4) % 6], INK, 1.5);
    }
    txt(g, '\u90e8\u54c1', 640, 160, 16, '#f0e4c8');
    /* lock + clipboard on the gate, in frame */
    steelDoor(g, 560, 500, 80, 160, '');
    ellipse(g, 624, 580, 8, 8, '#c4a060', INK, 2);
    R(g, 660, 540, 40, 56, '#d8c8a0', INK, 2);
    /* stool and grease can outside the cage */
    ellipse(g, 240, 760, 24, 8, '#3a3e48', INK, 2);
    R(g, 232, 764, 8, 28, '#3a3e48', INK, 1.5);
    drum(g, 200, 700, 32, 50, '#3a4a38');
    shell(g, '\u90e8\u54c1', 'Parts cage');
  };

  /* ---------- 7. Bike bay ---------- */
  S2P.depBikes = function (g, cleared) {
    rr(g);
    backWall(g, '#4a5064', '#40465a');
    lamp(g, 220, 70); lamp(g, 640, 50); lamp(g, 1060, 70);
    concFloor(g, 90, 320, 1100, 530, '#6a6460', '#5a5450', 37);
    oilStain(g, 400, 700, 60, 18); oilStain(g, 880, 720, 50, 16);
    /* rubber mats + motos along the sides, centre walk clear */
    R(g, 160, 700, 200, 18, '#2a2826', INK, 2);
    moto(g, 180, 630, 1.2, '#2a3a70');
    R(g, 920, 700, 200, 18, '#2a2826', INK, 2);
    moto(g, 940, 630, 1.2, '#3a2a28');
    if (!cleared) {
      R(g, 540, 700, 200, 18, '#2a2826', INK, 2);
      moto(g, 560, 630, 1.15, '#d46028');
    }
    /* helmets */
    ellipse(g, 200, 520, 18, 14, '#2a3a70', INK, 2);
    ellipse(g, 250, 524, 18, 14, '#3a2a28', INK, 2);
    ellipse(g, 1040, 520, 18, 14, '#d46028', INK, 2);
    /* tires + fuel */
    function tires(tx, ty, n) {
      var k;
      for (k = 0; k < n; k++) {
        ellipse(g, tx, ty - k * 16, 36, 12, '#1a1220', INK, 2);
      }
    }
    tires(200, 820, 5); tires(1080, 800, 4);
    R(g, 280, 760, 28, 40, '#b43428', INK, 2);
    txt(g, 'F', 294, 780, 11, '#f0e4c8');
    /* tool hook board */
    R(g, 400, 90, 200, 160, '#7a4a2e', INK, 3);
    g.strokeStyle = INK; g.lineWidth = 4;
    g.beginPath(); g.moveTo(430, 120); g.lineTo(430, 200); g.stroke();
    g.beginPath(); g.moveTo(470, 130); g.lineTo(470, 210); g.stroke();
    g.beginPath(); g.moveTo(520, 120); g.lineTo(520, 190); g.stroke();
    shell(g, '\u99d0\u8f2a', 'Bike bay');
  };

  /* ---------- 8. Dispatcher loft ---------- */
  S2P.depLoft = function (g, cleared) {
    rr(g);
    /* warmer wood rail, window onto the bay below */
    corrug(g, 90, 40, 1100, 200, '#4a5064', '#40465a', 22);
    R(g, 90, 40, 1100, 18, '#2a2e3a', INK, 2);
    R(g, 300, 70, 680, 160, '#1a1220', INK, 3);
    /* bay below, smaller */
    concFloor(g, 306, 140, 668, 84, '#6a6460', '#5a5450', 5);
    crate(g, 340, 150, 50, 36, '');
    crate(g, 880, 160, 50, 36, '');
    /* railing */
    R(g, 90, 230, 1100, 14, '#6a5240', INK, 2);
    var i;
    g.strokeStyle = INK; g.lineWidth = 3;
    for (i = 0; i < 16; i++) { g.beginPath(); g.moveTo(120 + i * 66, 230); g.lineTo(120 + i * 66, 280); g.stroke(); }
    R(g, 90, 276, 1100, 10, '#5a4638', INK, 2);
    lamp(g, 220, 70); lamp(g, 1060, 70);
    concFloor(g, 90, 320, 1100, 530, '#6a5e54', '#5a5048', 43);
    /* dispatch desk, in frame */
    R(g, 400, 540, 300, 24, '#5c4638', INK, 3);
    R(g, 400, 564, 300, 110, '#4a3e34', INK, 3);
    R(g, 416, 548, 48, 16, '#2a2c34', INK, 1.5);
    ellipse(g, 430, 556, 6, 6, '#3a6a3a', INK, 1.3);
    ellipse(g, 448, 556, 6, 6, '#6a3a2a', INK, 1.3);
    manifest(g, 520, 548, 90, 80, false);
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(660, 540); g.lineTo(660, 508); g.lineTo(688, 496); g.stroke();
    ellipse(g, 696, 496, 14, 10, '#f0d080', INK, 2);
    glow(g, 690, 530, 70, 'rgba(255,200,110,.3)');
    /* 配車表 */
    R(g, 860, 360, 220, 180, '#d8c8a0', INK, 3);
    R(g, 860, 360, 220, 24, '#5a2a28', INK, 2);
    txt(g, '\u914d\u8eca\u8868', 970, 372, 13, '#f0e4c8');
    g.strokeStyle = '#5a3a28'; g.lineWidth = 1.4;
    for (i = 0; i < 7; i++) { g.beginPath(); g.moveTo(876, 396 + i * 18); g.lineTo(1064, 396 + i * 18); g.stroke(); }
    /* canal night window, right */
    R(g, 140, 360, 180, 140, '#1a2238', INK, 3);
    g.fillStyle = '#1a2434'; g.fillRect(146, 430, 168, 64);
    g.fillStyle = '#c45a62';
    for (i = 0; i < 12; i++) g.fillRect(152 + i * 14, 460, 3, 3);
    ellipse(g, 620, 720, 22, 8, '#c4a060', INK, 2);
    R(g, 612, 720, 8, 36, '#3b2a22', INK, 2);
    shell(g, '\u914d\u8eca\u30ed\u30d5\u30c8', 'Dispatch loft');
  };

  /* ---------- 9. Break room ---------- */
  S2P.depBreak = function (g, cleared) {
    rr(g);
    corrug(g, 90, 40, 1100, 280, '#5a4a40', '#504038', 28);
    R(g, 90, 40, 1100, 18, '#2a2018', INK, 2);
    /* warm lamps */
    lamp(g, 300, 70); lamp(g, 980, 70);
    glow(g, 640, 200, 200, 'rgba(255,180,100,.1)');
    concFloor(g, 90, 320, 1100, 530, '#6a5a4c', '#5a4a40', 47);
    /* table, in frame */
    R(g, 430, 560, 280, 22, '#6a5240', INK, 3);
    R(g, 450, 582, 16, 80, '#4a3a30', INK, 2);
    R(g, 674, 582, 16, 80, '#4a3a30', INK, 2);
    /* ramen cups, kettle, ashtray, magazine */
    R(g, 460, 536, 28, 24, '#c45a3a', INK, 1.5);
    R(g, 500, 536, 28, 24, '#3a6a8a', INK, 1.5);
    ellipse(g, 560, 548, 14, 10, '#8a8fa0', INK, 1.5);
    R(g, 600, 530, 50, 28, '#efe6d2', INK, 1.5);
    ellipse(g, 680, 548, 12, 8, '#3a3e48', INK, 1.5);
    /* benches */
    R(g, 400, 700, 140, 16, '#4a3a30', INK, 2);
    R(g, 600, 700, 140, 16, '#4a3a30', INK, 2);
    /* sofa left */
    R(g, 140, 600, 200, 80, '#4a3a48', INK, 3);
    R(g, 140, 560, 200, 44, '#5a4a58', INK, 2);
    /* fridge + kettle counter right */
    R(g, 980, 480, 120, 200, '#d8d0c4', INK, 3);
    R(g, 990, 500, 100, 50, '#3a6a8a', INK, 2);
    txt(g, 'ICE', 1040, 525, 11, '#f0e4c8');
    R(g, 980, 440, 120, 40, '#3e322c', INK, 2);
    ellipse(g, 1040, 430, 16, 12, '#8a8fa0', INK, 2);
    /* TV */
    R(g, 560, 120, 160, 100, '#1a1220', INK, 3);
    R(g, 568, 128, 144, 84, '#2a3850', 0);
    /* clock + no-smoking (ignored, ashtray is out) */
    ellipse(g, 200, 160, 22, 22, '#f4ead2', INK, 2);
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(200, 160); g.lineTo(200, 148); g.moveTo(200, 160); g.lineTo(210, 166); g.stroke();
    R(g, 900, 120, 90, 50, '#f4ead2', INK, 2);
    txt(g, '\u7981\u7159', 945, 145, 13, '#a84838');
    /* lockers */
    lockers(g, 140, 400, 4, 120);
    shell(g, '\u4f11\u61a9', 'Break room');
  };

  /* ---------- 10. Tunnel spur ---------- */
  S2P.depTunnel = function (g, cleared) {
    rr(g);
    /* staggered wet brick, not long planks */
    g.fillStyle = '#2a2428'; g.fillRect(90, 0, 1100, 320);
    var i, j, xx, yy, off;
    for (yy = 40; yy < 320; yy += 18) {
      off = ((yy / 18) % 2) * 16;
      for (xx = 90; xx < 1190; xx += 32) {
        R(g, xx + off, yy, 30, 16, ((xx + yy) % 64 < 32) ? '#4a3a36' : '#3e322e', INK, 1);
      }
    }
    /* arched mouth with a receding service tunnel */
    g.beginPath();
    g.moveTo(420, 280); g.lineTo(500, 90); g.lineTo(780, 90); g.lineTo(860, 280); g.closePath();
    g.fillStyle = '#121018'; g.fill(); g.strokeStyle = INK; g.lineWidth = 3; g.stroke();
    g.beginPath();
    g.moveTo(500, 260); g.lineTo(560, 120); g.lineTo(720, 120); g.lineTo(780, 260); g.closePath();
    g.fillStyle = '#0a0a0e'; g.fill();
    /* a hint of rail receding */
    g.strokeStyle = '#3a3e48'; g.lineWidth = 3;
    g.beginPath(); g.moveTo(560, 250); g.lineTo(620, 140); g.stroke();
    g.beginPath(); g.moveTo(720, 250); g.lineTo(660, 140); g.stroke();
    for (i = 0; i < 5; i++) lamp(g, 180 + i * 230, 64);
    concFloor(g, 90, 320, 1100, 530, '#3e3a40', '#322e34', 53);
    g.fillStyle = 'rgba(80,110,140,.08)'; g.fillRect(90, 320, 1100, 530);
    /* wet walk, puddles */
    g.fillStyle = 'rgba(120,160,190,.14)';
    g.beginPath(); g.ellipse(640, 700, 160, 20, 0, 0, 7); g.fill();
    g.beginPath(); g.ellipse(400, 800, 70, 12, 0, 0, 7); g.fill();
    g.beginPath(); g.ellipse(860, 760, 60, 12, 0, 0, 7); g.fill();
    /* pipes along both walls */
    R(g, 90, 300, 1100, 16, '#4a4e58', INK, 2);
    R(g, 110, 200, 22, 400, '#4a4e58', INK, 2);
    R(g, 1148, 200, 22, 400, '#4a4e58', INK, 2);
    R(g, 110, 360, 70, 14, '#4a4e58', INK, 2);
    R(g, 1100, 420, 70, 14, '#4a4e58', INK, 2);
    /* cables */
    g.strokeStyle = '#2a2018'; g.lineWidth = 3;
    g.beginPath(); g.moveTo(140, 40); g.quadraticCurveTo(200, 180, 140, 300); g.stroke();
    g.beginPath(); g.moveTo(1140, 40); g.quadraticCurveTo(1080, 200, 1140, 300); g.stroke();
    graySeal(g, 240, 180, 28);
    txt(g, '\u6a2a\u5751', 240, 230, 12, 'rgba(240,228,200,.35)');
    crate(g, 160, 700, 90, 70, '');
    crate(g, 200, 640, 80, 60, '');
    drum(g, 300, 720, 36, 56, '#3a4a38');
    R(g, 1000, 720, 36, 50, '#d46028', INK, 2);
    R(g, 992, 710, 52, 12, '#d46028', INK, 2);
    crate(g, 1040, 640, 90, 70, '');
    /* ladder */
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(860, 320); g.lineTo(860, 820); g.moveTo(900, 320); g.lineTo(900, 820); g.stroke();
    for (i = 0; i < 10; i++) { g.beginPath(); g.moveTo(860, 360 + i * 44); g.lineTo(900, 360 + i * 44); g.stroke(); }
    g.strokeStyle = 'rgba(180,210,230,.4)'; g.lineWidth = 2;
    g.beginPath(); g.moveTo(400, 316); g.lineTo(400, 360); g.stroke();
    g.beginPath(); g.moveTo(900, 316); g.lineTo(900, 350); g.stroke();
    shell(g, '\u6a2a\u5751', 'Tunnel spur');
  };

  /* ---------- 11. Manifest office ---------- */
  S2P.depManifest = function (g, cleared) {
    rr(g);
    backWall(g, '#4a5048', '#40463e');
    lamp(g, 220, 70); lamp(g, 1060, 70);
    /* hanging lamp over the desk */
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(640, 40); g.lineTo(640, 300); g.stroke();
    R(g, 624, 298, 32, 12, '#3a3e48', INK, 2);
    glow(g, 640, 360, 100, 'rgba(255,200,100,.24)');
    concFloor(g, 90, 320, 1100, 530, '#6a5e54', '#5a5048', 59);
    /* pigeonholes */
    R(g, 140, 80, 280, 210, '#5c4638', INK, 3);
    var i, j;
    for (j = 0; j < 3; j++) for (i = 0; i < 4; i++) {
      R(g, 156 + i * 64, 100 + j * 58, 56, 48, '#2a2018', INK, 1.5);
      if ((i + j) % 2 === 0) R(g, 162 + i * 64, 108 + j * 58, 44, 16, '#efe6d2', 0);
    }
    /* main desk, in frame — the gray-seal manifest lives here until the shutter */
    R(g, 400, 560, 360, 24, '#5c4638', INK, 3);
    R(g, 400, 584, 360, 110, '#4a3e34', INK, 3);
    manifest(g, 520, 500, 120, 100, true);
    R(g, 420, 568, 50, 16, '#2a2430', INK, 1.5);
    ellipse(g, 500, 572, 10, 8, '#3a2a22', INK, 1.5);
    /* stamp */
    ellipse(g, 680, 572, 14, 10, '#5a5e68', INK, 1.5);
    /* window to the lift */
    R(g, 860, 80, 240, 200, '#1a1220', INK, 3);
    corrug(g, 868, 88, 224, 184, '#3a3e48', '#32363e', 16);
    R(g, 920, 140, 120, 100, '#2a2c34', INK, 2);
    caution(g, 920, 230, 120, 10);
    /* filing cabinets */
    R(g, 160, 500, 160, 220, '#4a5060', INK, 3);
    R(g, 170, 530, 140, 14, '#3a3e48', INK, 1.5);
    R(g, 170, 580, 140, 14, '#3a3e48', INK, 1.5);
    R(g, 170, 630, 140, 14, '#3a3e48', INK, 1.5);
    txt(g, '\u53f0\u5e33', 240, 490, 12, '#f0e4c8');
    lockers(g, 900, 500, 4, 180);
    ellipse(g, 800, 740, 22, 8, '#c4a060', INK, 2);
    R(g, 792, 740, 8, 36, '#3b2a22', INK, 2);
    shell(g, '\u7a4d\u8377', 'Manifest office');
  };

  /* ---------- 12. Cargo-lift anteroom ---------- */
  S2P.depAntero = function (g, cleared) {
    rr(g);
    backWall(g, '#3a4254', '#323848');
    /* lift gates ahead, the shutter beyond */
    R(g, 400, 50, 480, 270, '#1a1220', INK, 3);
    corrug(g, 408, 58, 464, 200, '#3a3e48', '#2e323c', 20);
    /* inner shutter hint */
    for (i = 0; i < 8; i++) R(g, 450, 80 + i * 16, 380, 16, i % 2 ? '#3a3e4c' : '#32364a', INK, 1.2);
    caution(g, 408, 258, 464, 14);
    /* gate chains */
    var i;
    g.strokeStyle = '#8a8fa0'; g.lineWidth = 4;
    g.beginPath(); g.moveTo(420, 70); g.lineTo(420, 250); g.stroke();
    g.beginPath(); g.moveTo(860, 70); g.lineTo(860, 250); g.stroke();
    lamp(g, 200, 70); lamp(g, 1080, 70);
    glow(g, 640, 180, 140, 'rgba(255,200,110,.1)');
    concFloor(g, 90, 320, 1100, 530, '#6a6460', '#5a5450', 61);
    oilStain(g, 300, 740, 50, 16); oilStain(g, 960, 700, 44, 14);
    /* waiting pallet, in frame but off the walk to the lift */
    pallet(g, 160, 700, 140, 30);
    crate(g, 180, 630, 100, 70, '\u8ca0\u7269');
    /* control panel */
    R(g, 900, 400, 160, 200, '#2a2c34', INK, 3);
    ellipse(g, 940, 460, 14, 14, '#3a6a3a', INK, 2);
    ellipse(g, 1000, 460, 14, 14, '#6a3a2a', INK, 2);
    R(g, 920, 500, 120, 16, '#1a2018', INK, 1.5);
    txt(g, '\u6607\u964d\u6a5f', 980, 390, 12, '#f0e4c8');
    /* warning */
    R(g, 200, 400, 80, 80, '#e8c040', INK, 2);
    txt(g, '!', 240, 440, 36, '#1a1220');
    shell(g, '\u6607\u964d\u6a5f\u524d', 'Lift anteroom');
  };

  /* ---------- 13. Lift shutter (boss room) ---------- */
  function shutterRoom(g, mode) {
    /* mode: 'fight' | 'leave' | 'notes' | 'help' | 'cleared' */
    rr(g);
    corrug(g, 90, 40, 1100, 280, '#3a4254', '#323848', 22);
    R(g, 90, 40, 1100, 18, '#2a2e3a', INK, 2);
    /* the cargo-lift shutter */
    R(g, 300, 50, 680, 270, '#1a1220', INK, 3);
    var i;
    for (i = 0; i < 12; i++) {
      R(g, 308, 58 + i * 18, 664, 18, i % 2 ? '#3a3e4c' : '#32364a', INK, 1.3);
    }
    if (mode === 'fight' || mode === 'leave') {
      /* shutter down / mostly down */
    } else {
      /* a gap under the slats */
      R(g, 308, 250, 664, 30, '#121018', 0);
    }
    caution(g, 308, 270, 664, 14);
    /* the freight manifest with Kagerō's gray seal, on the shutter */
    manifest(g, 560, 120, 160, 120, true);
    lamp(g, 200, 70); lamp(g, 1080, 70);
    glow(g, 640, 160, 180, 'rgba(255,200,110,.16)');
    concFloor(g, 90, 320, 1100, 530, '#6a6460', '#5a5450', 67);
    oilStain(g, 280, 780, 60, 18); oilStain(g, 1000, 740, 50, 16);
    /* side props, centre lane clear for the fight */
    crate(g, 140, 700, 110, 80, '\u8ca0\u7269');
    crate(g, 160, 630, 100, 70, '');
    crate(g, 150, 560, 90, 70, '');
    drum(g, 260, 720, 36, 60, '#6a3a28');
    pallet(g, 240, 800, 120, 24);
    crate(g, 1030, 700, 110, 80, '');
    crate(g, 1040, 630, 90, 70, '');
    drum(g, 980, 720, 32, 56, '#3a4a38');
    /* control panel on a stand, not floating mid-floor */
    R(g, 900, 480, 80, 140, '#2a2c34', INK, 2);
    R(g, 924, 620, 16, 50, '#2a2c34', INK, 2);
    ellipse(g, 940, 530, 10, 10, '#3a6a3a', INK, 1.5);
    ellipse(g, 940, 560, 10, 10, '#6a3a2a', INK, 1.5);
    g.strokeStyle = '#8a8fa0'; g.lineWidth = 4;
    g.beginPath(); g.moveTo(360, 50); g.lineTo(360, 300); g.stroke();
    g.beginPath(); g.moveTo(920, 50); g.lineTo(920, 300); g.stroke();
    if (mode === 'leave') {
      /* knocked stool, hat on the floor */
      ellipse(g, 700, 760, 22, 8, '#c4a060', INK, 2);
      R(g, 692, 764, 36, 8, '#3b2a22', INK, 2);
      hardhat(g, 760, 780);
    }
    if (mode === 'notes') {
      /* extra annotated sheets on the floor / desk */
      R(g, 600, 700, 90, 60, '#efe6d2', INK, 2);
      R(g, 700, 720, 70, 50, '#efe6d2', INK, 2);
      g.strokeStyle = '#3a4a6a'; g.lineWidth = 2;
      g.beginPath(); g.moveTo(610, 720); g.lineTo(680, 720); g.stroke();
    }
    if (mode === 'help') {
      ellipse(g, 640, 760, 22, 8, '#c4a060', INK, 2);
      R(g, 632, 760, 8, 36, '#3b2a22', INK, 2);
      hardhat(g, 580, 600);
    }
    shell(g, '\u30b7\u30e3\u30c3\u30bf\u30fc', 'Lift shutter');
  }
  S2P.depShutter = function (g, cleared) { shutterRoom(g, cleared ? 'cleared' : 'fight'); };
  S2P.depShutterLeave = function (g) { shutterRoom(g, 'leave'); };
  S2P.depShutterNotes = function (g) { shutterRoom(g, 'notes'); };
  S2P.depShutterHelp = function (g) { shutterRoom(g, 'help'); };

  /* ---------- battle: lift shutter ---------- */
  S2P.battleShutter = function (g) {
    var H = (typeof window !== 'undefined' && window.FFF_C2H) || (typeof root !== 'undefined' && root.FFF_C2H);
    var WD = 720, HT = 1280, H0 = 330, x = g, i, y;
    rr(g);
    if (!H) { g.fillStyle = '#1a1410'; g.fillRect(0, 0, WD, HT); return; }
    corrug(g, 0, 0, WD, H0, '#3a4254', '#323848', 22);
    R(g, 0, 0, WD, 18, '#2a2e3a', H.INK, 2);
    /* shutter */
    R(g, 80, 20, 560, 250, '#1a1220', H.INK, 3);
    for (i = 0; i < 10; i++) R(g, 88, 28 + i * 18, 544, 18, i % 2 ? '#3a3e4c' : '#32364a', H.INK, 1.2);
    caution(g, 88, 248, 544, 12);
    manifest(g, 300, 70, 140, 100, true);
    /* lamps — no indoor rain */
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(120, 18); g.lineTo(120, 70); g.stroke();
    g.beginPath(); g.moveTo(600, 18); g.lineTo(600, 70); g.stroke();
    ellipse(g, 120, 86, 14, 14, '#f0d080', INK, 2);
    ellipse(g, 600, 86, 14, 14, '#f0d080', INK, 2);
    glow(g, 120, 110, 90, 'rgba(255,200,110,.34)');
    glow(g, 600, 110, 90, 'rgba(255,200,110,.34)');
    var fx = H.fx0;
    g.beginPath();
    g.moveTo(0, H0); g.lineTo(WD, H0); g.lineTo(WD, HT); g.lineTo(0, HT); g.closePath();
    g.fillStyle = H.lg(x, H0, HT, '#6a6460', '#3e3a38');
    g.fill();
    g.save(); g.beginPath(); g.rect(0, H0, WD, HT - H0); g.clip();
    /* joints only at the sides — no full bowling-lane grid */
    g.strokeStyle = 'rgba(0,0,0,.12)'; g.lineWidth = 1.6;
    for (i = 2; i < 14; i += 4) {
      y = H0 + (HT - H0) * Math.pow(i / 14, 1.5);
      g.beginPath(); g.moveTo(fx(20, y), y); g.lineTo(fx(180, y), y); g.stroke();
      g.beginPath(); g.moveTo(fx(540, y), y); g.lineTo(fx(700, y), y); g.stroke();
    }
    g.restore();
    oilStain(g, 140, 700, 50, 16);
    oilStain(g, 580, 900, 60, 18);
    oilStain(g, 160, 1100, 70, 20);
    /* side props, centre lane (~260-460) clear */
    crate(g, 16, 500, 80, 56, '\u8ca0\u7269');
    crate(g, 24, 440, 70, 50, '');
    drum(g, 20, 600, 32, 56, '#6a3a28');
    drum(g, 56, 620, 28, 48, '#3a4a38');
    crate(g, 620, 500, 80, 56, '');
    crate(g, 630, 440, 70, 50, '');
    drum(g, 660, 620, 32, 50, '#3a4a38');
    moto(g, 8, 900, 0.9, '#2a3a70');
    crate(g, 620, 960, 80, 50, '');
    crate(g, 640, 1080, 70, 46, '');
    R(g, 16, 1140, 70, 80, '#2a2c34', INK, 2);
    ellipse(g, 40, 1170, 8, 8, '#3a6a3a', INK, 1.5);
    ellipse(g, 40, 1200, 8, 8, '#6a3a2a', INK, 1.5);
    function tires(tx, ty, n) {
      var k;
      for (k = 0; k < n; k++) ellipse(g, tx, ty - k * 14, 26, 9, '#1a1220', INK, 2);
    }
    tires(80, 780, 4); tires(650, 800, 3);
    glow(g, 120, H0 + 40, 70, 'rgba(255,200,110,.16)');
    glow(g, 600, H0 + 40, 70, 'rgba(255,200,110,.16)');
    glow(g, 360, 1200, 80, 'rgba(255,210,140,.1)');
    H.vign(x, 0.58);
    H.grade(x, 'rgba(40,50,70,.18)', 'rgba(20,10,12,.28)');
  };

  /* ---------- line cards + item ---------- */
  S2P.lineCardDep = function (g, who) {
    var W = 900, H = 420;
    rr(g);
    R(g, 0, 0, W, H, '#1a1620', 0);
    R(g, 16, 16, W - 32, H - 32, '#241e2a', INK, 3);
    var title = {
      fierce: 'Fierce  \u00b7  the yard gate',
      strategic: 'Strategic  \u00b7  the yard gate',
      compassionate: 'Compassionate  \u00b7  the yard gate',
      bond: 'Aoi  \u00b7  at the shutter',
      leave: 'Fierce payoff  \u00b7  leave him',
      notes: 'Strategic payoff  \u00b7  the notes',
      help: 'Compassionate payoff  \u00b7  help him up',
      mori: 'Mori-san  \u00b7  after the seal',
      nao: 'Nao  \u00b7  after the seal',
      haru: 'Haru  \u00b7  after the seal'
    };
    var body = {
      fierce: 'Ryo: We came to put you on the floor, Masa.',
      strategic: 'Ryo: The shutter, the seal, the paperwork. That is the visit.',
      compassionate: 'Ryo: We came to end the gray-coat schedule. Not the men who punch the clock.',
      bond: 'Aoi asks: He is down. The seal and the manifest are on the shutter. What do we do with him?',
      leave: 'Ryo: Leave him. The yard is ours.',
      notes: 'Ryo: Stay talking. I want the dock code and the time on that sheet.',
      help: 'Ryo: Up. Honest freight can still leave this yard under our color.',
      mori: 'Mori-san: The freight has gone quiet for good. The kettle is on. Come in when you pass.',
      nao: 'Nao: If the nights stay like this I can keep the day job. Thank you \u2014 really.',
      haru: 'Haru: The bikes are gone. Mori-san said I can sit on the sofa whenever I want now.'
    };
    txt(g, title[who] || who, 450, 56, 18, '#f0e4c8', '800 ');
    g.fillStyle = '#d8c8a0';
    g.font = '16px "Noto Sans CJK JP",Georgia,serif';
    g.textAlign = 'left'; g.textBaseline = 'top';
    wrap(g, body[who] || '', 48, 100, 800, 28);
    txt(g, 'add only  \u00b7  preview', 850, 380, 12, '#8a8070', '700 ', 'right');
  };
  function wrap(g, s, x, y, w, lh) {
    var words = String(s).split(' '), line = '', i, m;
    for (i = 0; i < words.length; i++) {
      m = g.measureText(line + words[i] + ' ');
      if (m.width > w && line) { g.fillText(line, x, y); y += lh; line = words[i] + ' '; }
      else line += words[i] + ' ';
    }
    if (line) g.fillText(line, x, y);
  }

  S2P.manifestItem = function (g) {
    rr(g);
    R(g, 0, 0, 360, 480, '#1a1620', 0);
    manifest(g, 40, 80, 280, 320, true);
    txt(g, 'Freight manifest', 180, 40, 16, '#f0e4c8');
    txt(g, 'Gray seal  \u00b7  Kager\u014d', 180, 430, 13, '#c8b898');
  };

  S2P.DEPOT_ROOMS = [
    ['depYard', 'Yard gate  \u9580'],
    ['depClock', 'Time clock  \u6253\u523b'],
    ['depBay', 'Loading bay  \u8377\u5f79'],
    ['depCrates', 'Crate stacks  \u8ca0\u7269'],
    ['depCold', 'Cold store  \u51b7\u51cd'],
    ['depCage', 'Parts cage  \u90e8\u54c1'],
    ['depBikes', 'Bike bay  \u99d0\u8f2a'],
    ['depLoft', 'Dispatch loft  \u914d\u8eca'],
    ['depBreak', 'Break room  \u4f11\u61a9'],
    ['depTunnel', 'Tunnel spur  \u6a2a\u5751'],
    ['depManifest', 'Manifest office  \u7a4d\u8377'],
    ['depAntero', 'Lift anteroom  \u6607\u964d\u6a5f\u524d'],
    ['depShutter', 'Lift shutter  \u30b7\u30e3\u30c3\u30bf\u30fc']
  ];
})(typeof window !== 'undefined' ? window : globalThis);
