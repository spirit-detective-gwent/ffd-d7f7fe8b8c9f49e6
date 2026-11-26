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


  function hose(g, x, y, len) {
    g.strokeStyle = INK; g.lineWidth = 6;
    g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + len * 0.4, y + 28, x + len, y + 8); g.stroke();
    g.strokeStyle = '#3a4a38'; g.lineWidth = 3.5;
    g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + len * 0.4, y + 28, x + len, y + 8); g.stroke();
  }
  function hoseCoil(g, cx, cy, r) {
    g.strokeStyle = INK; g.lineWidth = 6;
    g.beginPath(); g.arc(cx, cy, r, 0.2, Math.PI * 1.85); g.stroke();
    g.strokeStyle = '#3a4a38'; g.lineWidth = 3.6;
    g.beginPath(); g.arc(cx, cy, r, 0.2, Math.PI * 1.85); g.stroke();
    g.strokeStyle = '#2a3a28'; g.lineWidth = 2.4;
    g.beginPath(); g.arc(cx, cy, r * 0.6, 0.5, Math.PI * 1.6); g.stroke();
  }
  function handTruck(g, x, y) {
    g.strokeStyle = INK; g.lineWidth = 4;
    g.beginPath(); g.moveTo(x, y + 40); g.lineTo(x, y - 80); g.lineTo(x + 50, y - 80); g.stroke();
    g.beginPath(); g.moveTo(x, y + 40); g.lineTo(x + 36, y + 40); g.stroke();
    ellipse(g, x, y + 48, 14, 14, '#1a1220', INK, 2);
    ellipse(g, x, y + 48, 6, 6, '#6a707c', INK, 1.4);
  }
  function palletJack(g, x, y) {
    /* low manual jack — forks toward +y, tiller up */
    R(g, x, y, 40, 36, '#3a3e48', INK, 2);
    R(g, x + 6, y + 36, 10, 54, '#6a707c', INK, 2);
    R(g, x + 24, y + 36, 10, 54, '#6a707c', INK, 2);
    ellipse(g, x + 10, y + 34, 8, 8, '#1a1220', INK, 2);
    ellipse(g, x + 30, y + 34, 8, 8, '#1a1220', INK, 2);
    g.strokeStyle = INK; g.lineWidth = 4;
    g.beginPath(); g.moveTo(x + 20, y); g.lineTo(x + 20, y - 44); g.lineTo(x + 44, y - 58); g.stroke();
    R(g, x + 36, y - 64, 16, 10, '#3a3e48', INK, 1.6);
  }
  function chainHang(g, x, y0, y1) {
    var i, n = Math.max(4, Math.floor((y1 - y0) / 10));
    g.strokeStyle = '#8a8fa0'; g.lineWidth = 3;
    for (i = 0; i < n; i++) {
      g.beginPath(); g.ellipse(x, y0 + i * 10, 4, 5, 0, 0, Math.PI * 2); g.stroke();
    }
  }
  function chainCoil(g, cx, cy, r) {
    g.strokeStyle = INK; g.lineWidth = 5;
    g.beginPath(); g.arc(cx, cy, r, 0.15, Math.PI * 1.9); g.stroke();
    g.strokeStyle = '#8a8fa0'; g.lineWidth = 3;
    g.beginPath(); g.arc(cx, cy, r, 0.15, Math.PI * 1.9); g.stroke();
    g.beginPath(); g.arc(cx, cy, r * 0.55, 0.4, Math.PI * 1.7); g.stroke();
  }
  function cableRun(g, x1, y1, x2, y2) {
    /* low conduit along a wall or baseboard — never a mid-floor pole */
    g.strokeStyle = '#2a2018'; g.lineWidth = 4;
    g.beginPath(); g.moveTo(x1, y1); g.lineTo(x2, y2); g.stroke();
    g.strokeStyle = '#4a3a28'; g.lineWidth = 2;
    g.beginPath(); g.moveTo(x1, y1); g.lineTo(x2, y2); g.stroke();
  }
  function floorMat(g, x, y, w, h, col) {
    R(g, x, y, w, h, col || '#3a322c', INK, 2);
    g.fillStyle = 'rgba(0,0,0,.12)'; g.fillRect(x + 4, y + 4, w - 8, 4);
  }
  function waterCooler(g, x, y) {
    ellipse(g, x + 22, y, 18, 14, '#7ec8e8', INK, 2);
    ellipse(g, x + 22, y - 8, 14, 8, '#8ed0f0', INK, 1.5);
    R(g, x, y + 8, 44, 70, '#d8d0c4', INK, 2);
    R(g, x + 8, y + 20, 28, 16, '#3a3e48', INK, 1.4);
    R(g, x + 14, y + 50, 16, 10, '#8a8fa0', INK, 1.2);
  }
  function futonFold(g, x, y) {
    R(g, x, y, 200, 56, '#c8b090', INK, 2);
    R(g, x + 8, y + 8, 184, 18, '#efe6d2', INK, 1.4);
    R(g, x + 8, y + 30, 184, 18, '#d8c8a0', INK, 1.2);
    g.strokeStyle = 'rgba(90,60,40,.35)'; g.lineWidth = 1.5;
    g.beginPath(); g.moveTo(x + 20, y + 16); g.lineTo(x + 180, y + 16); g.stroke();
  }
  function warningBox(g, x, y, w, h) {
    caution(g, x, y, w, 14);
    caution(g, x, y + h - 14, w, 14);
    caution(g, x, y, 14, h);
    caution(g, x + w - 14, y, 14, h);
  }
  function papers(g, x, y) {
    R(g, x, y, 50, 36, '#efe6d2', INK, 1.5);
    R(g, x + 14, y + 10, 46, 32, '#e8dcc4', INK, 1.4);
    g.strokeStyle = '#5a3a28'; g.lineWidth = 1;
    g.beginPath(); g.moveTo(x + 20, y + 20); g.lineTo(x + 50, y + 20); g.stroke();
  }
  function cone(g, x, y) {
    R(g, x, y, 28, 40, '#d46028', INK, 2);
    R(g, x - 8, y - 8, 44, 10, '#d46028', INK, 2);
    R(g, x + 4, y + 10, 20, 6, '#f0e4c8', 0);
  }
  function signPlate(g, x, y, w, h, ja, bg) {
    R(g, x, y, w, h, bg || '#e8c040', INK, 2);
    txt(g, ja, x + w / 2, y + h / 2, Math.max(10, h * 0.28), '#1a1220', '800 ');
  }
  function tires(g, tx, ty, n, r) {
    r = r || 36;
    var k;
    for (k = 0; k < n; k++) {
      ellipse(g, tx, ty - k * (r * 0.42), r, r * 0.32, '#1a1220', INK, 2);
      g.strokeStyle = 'rgba(80,80,90,.5)'; g.lineWidth = 1.5;
      g.beginPath(); g.ellipse(tx, ty - k * (r * 0.42), r * 0.55, r * 0.16, 0, 0, 7); g.stroke();
    }
  }
  function jerry(g, x, y, sc) {
    var s = sc || 1;
    g.save(); g.translate(x, y); g.scale(s, s);
    R(g, 0, 8, 28, 36, '#b43428', INK, 2);
    R(g, 4, 0, 14, 12, '#b43428', INK, 2);
    R(g, 16, 2, 10, 8, '#6a707c', INK, 1.4);
    txt(g, 'F', 14, 28, 11, '#f0e4c8', '800 ');
    g.restore();
  }
  function stool(g, x, y) {
    ellipse(g, x, y, 22, 8, '#c4a060', INK, 2);
    R(g, x - 8, y, 8, 36, '#3b2a22', INK, 2);
    R(g, x - 16, y + 36, 12, 10, '#3b2a22', INK, 1.5);
    R(g, x + 4, y + 36, 12, 10, '#3b2a22', INK, 1.5);
  }
  function mesh(g, x0, y0, w, h) {
    g.save(); g.beginPath(); g.rect(x0, y0, w, h); g.clip();
    g.strokeStyle = 'rgba(140,150,160,.55)'; g.lineWidth = 1.3;
    var i;
    for (i = -h; i < w + h; i += 14) {
      g.beginPath(); g.moveTo(x0 + i, y0); g.lineTo(x0 + i + h, y0 + h); g.stroke();
      g.beginPath(); g.moveTo(x0 + i, y0 + h); g.lineTo(x0 + i + h, y0); g.stroke();
    }
    g.restore();
  }
  function fence(g, x, y, w, h) {
    R(g, x, y, 10, h, '#3a3e48', INK, 2);
    R(g, x + w - 10, y, 10, h, '#3a3e48', INK, 2);
    R(g, x, y, w, 10, '#3a3e48', INK, 2);
    R(g, x, y + h - 10, w, 10, '#3a3e48', INK, 2);
    mesh(g, x + 8, y + 8, w - 16, h - 16);
  }
  function toolWall(g, x, y, w, h) {
    var i;
    R(g, x, y, w, h, '#7a4a2e', INK, 3);
    R(g, x + 8, y + 8, w - 16, h - 16, '#8a5a38', 0);
    for (i = 0; i < 8; i++) {
      for (var j = 0; j < 6; j++) ellipse(g, x + 20 + i * ((w - 36) / 7), y + 22 + j * ((h - 36) / 5), 1.6, 1.6, '#2a2018', 0);
    }
    g.lineCap = 'round';
    g.strokeStyle = INK; g.lineWidth = 5;
    g.beginPath(); g.moveTo(x + 28, y + 30); g.lineTo(x + 28, y + h - 40); g.stroke();
    R(g, x + 16, y + h - 44, 24, 12, '#8a8fa0', INK, 1.5);
    g.beginPath(); g.moveTo(x + 58, y + 36); g.lineTo(x + 58, y + h - 50); g.stroke();
    ellipse(g, x + 58, y + 32, 8, 6, '#8a8fa0', INK, 1.4);
    R(g, x + 86, y + 40, 9, 54, '#c4a060', INK, 1.5);
    R(g, x + 76, y + 32, 28, 12, '#6a707c', INK, 1.5);
    R(g, x + 126, y + 36, 6, 58, '#c45a3a', INK, 1.5);
    R(g, x + 122, y + 28, 14, 10, '#8a8fa0', INK, 1.2);
    if (w > 180) {
      R(g, x + 160, y + 44, 14, 40, '#6a4a28', INK, 1.4);
      R(g, x + 152, y + 34, 30, 14, '#3a3e48', INK, 1.4);
    }
  }
  function liftFrame(g, x, y, w, h) {
    /* heavy steel posts, header, pulleys — the freight lift */
    R(g, x, y, 28, h, '#2a2c34', INK, 3);
    R(g, x + 8, y, 8, h, '#3a3e48', 0);
    R(g, x + w - 28, y, 28, h, '#2a2c34', INK, 3);
    R(g, x + w - 16, y, 8, h, '#3a3e48', 0);
    R(g, x, y, w, 28, '#2a2c34', INK, 3);
    caution(g, x + 28, y + 6, w - 56, 16);
    R(g, x + w / 2 - 70, y + 32, 140, 20, '#f0e4c8', INK, 2);
    txt(g, '\u8ca8\u7269\u6607\u964d\u6a5f', x + w / 2, y + 42, 12, '#5a2a28', '800 ');
    ellipse(g, x + 50, y + 40, 12, 12, '#6a707c', INK, 2);
    ellipse(g, x + w - 50, y + 40, 12, 12, '#6a707c', INK, 2);
    chainHang(g, x + 50, y + 50, y + h - 8);
    chainHang(g, x + w - 50, y + 50, y + h - 8);
  }

  /* ---------- 1. Yard gate ---------- */
  S2P.depYard = function (g, cleared) {
    rr(g);
    backWall(g, '#3a4254', '#323848');
    /* chain-link fence across the back, with a sliding gate opened onto the rainy yard */
    fence(g, 100, 60, 200, 250);
    /* right fence stops before the two steel doors */
    fence(g, 860, 60, 40, 250);
    /* open yard in the gate gap — rain stays in this opening only */
    R(g, 460, 58, 400, 252, '#1a1220', INK, 3);
    var sky = g.createLinearGradient(0, 62, 0, 300);
    sky.addColorStop(0, '#1a2238'); sky.addColorStop(1, '#1a2430');
    g.fillStyle = sky; g.fillRect(466, 64, 388, 200);
    /* outdoor yard: gravel, flowers, a far lamp */
    g.fillStyle = '#3a322c'; g.fillRect(466, 210, 388, 54);
    g.fillStyle = '#5a3040'; g.fillRect(466, 236, 388, 28);
    var i;
    g.fillStyle = '#c45a62';
    for (i = 0; i < 24; i++) g.fillRect(474 + (i * 41) % 372, 240 + (i * 11) % 16, 3, 3);
    ellipse(g, 780, 200, 6, 6, '#f0d080', INK, 1.5);
    glow(g, 780, 200, 30, 'rgba(255,200,110,.25)');
    g.save(); g.beginPath(); g.rect(466, 64, 388, 200); g.clip();
    g.strokeStyle = 'rgba(200,220,255,.35)'; g.lineWidth = 1.2;
    var r = function (s) { var v = s; return function () { v = (v * 16807) % 2147483647; return (v - 1) / 2147483646; }; }(7);
    for (i = 0; i < 22; i++) {
      var rx = 466 + r() * 388, ry = 64 + r() * 200, L = 10 + r() * 16;
      g.beginPath(); g.moveTo(rx, ry); g.lineTo(rx + 3, ry + L); g.stroke();
    }
    g.restore();
    /* sliding bar-gate leaf parked to the left of the opening, on a track */
    R(g, 300, 50, 170, 262, '#3a4250', INK, 3);
    var gi;
    for (gi = 0; gi < 8; gi++) R(g, 314 + gi * 18, 70, 12, 220, '#4a5060', INK, 1.5);
    R(g, 300, 50, 170, 16, '#2a2c34', INK, 2);
    R(g, 300, 296, 170, 16, '#2a2c34', INK, 2);
    R(g, 452, 160, 14, 36, '#c4a060', INK, 2);
    ellipse(g, 320, 312, 10, 10, '#1a1220', INK, 2);
    ellipse(g, 450, 312, 10, 10, '#1a1220', INK, 2);
    ellipse(g, 320, 312, 4, 4, '#8a8fa0', INK, 1.2);
    ellipse(g, 450, 312, 4, 4, '#8a8fa0', INK, 1.2);
    /* track */
    R(g, 280, 314, 600, 8, '#4a4e58', INK, 2);
    caution(g, 466, 270, 388, 12);
    R(g, 540, 44, 200, 22, '#f0e4c8', INK, 2);
    txt(g, '\u5730\u4e0b\u9244\u8ca8\u7269', 640, 55, 13, '#5a2a28');
    lamp(g, 220, 70); lamp(g, 1060, 70);
    concFloor(g, 90, 320, 1100, 530, '#6a6460', '#5a5450', 11);
    oilStain(g, 300, 700, 50, 16); oilStain(g, 900, 640, 60, 18); oilStain(g, 240, 500, 36, 12);
    /* threshold puddle just inside the gate — rain stays outdoors, this is tracked-in wet */
    g.fillStyle = 'rgba(80,110,140,.16)';
    g.beginPath(); g.ellipse(640, 360, 90, 16, 0, 0, 7); g.fill();
    signPlate(g, 140, 360, 90, 50, '\u7acb\u5165\u7981\u6b62', '#e8c040');
    steelDoor(g, 900, 80, 90, 200, '\u6253\u523b');
    steelDoor(g, 1020, 80, 90, 200, '\u8377\u5f79');
    /* rain coats + hats */
    R(g, 118, 200, 36, 70, '#3a463c', INK, 2);
    R(g, 160, 210, 36, 60, '#2a3858', INK, 2);
    hardhat(g, 200, 190);
    /* meeting desk in the 640 frame, walk lane to the south kept clear */
    R(g, 430, 600, 220, 22, '#5c4638', INK, 3);
    R(g, 430, 622, 220, 80, '#4a3e34', INK, 3);
    R(g, 448, 608, 48, 16, '#2a2c34', INK, 1.5);
    hardhat(g, 620, 600);
    if (!cleared) R(g, 500, 636, 70, 48, '#efe6d2', INK, 2);
    R(g, 430, 702, 220, 10, '#2a2826', INK, 1.5);
    stool(g, 560, 740);
    lockers(g, 880, 500, 4, 140);
    hardhat(g, 900, 492); hardhat(g, 960, 492);
    crate(g, 140, 700, 90, 70, '\u8ca8\u7269');
    drum(g, 240, 720, 36, 60, '#3a4a38');
    pallet(g, 140, 780, 120, 24);
    cone(g, 360, 800);
    cone(g, 820, 800);
    handTruck(g, 1080, 760);
    hose(g, 280, 820, 140);
    chainCoil(g, 1040, 820, 20);
    cableRun(g, 100, 328, 300, 328);
    /* mid-side clutter — walk from the south stays open */
    crate(g, 140, 500, 80, 60, '');
    pallet(g, 140, 564, 100, 22);
    crate(g, 1040, 620, 80, 56, '');
    pallet(g, 1030, 680, 110, 22);
    floorMat(g, 430, 720, 220, 50, '#3a322c');
    stool(g, 560, 760);
    jerry(g, 330, 760, 1);
    tires(g, 1080, 600, 3, 28);
    /* bench under the no-entry sign, painted approach to the desk */
    R(g, 140, 400, 160, 16, '#4a3a30', INK, 2);
    R(g, 148, 416, 10, 24, '#4a3a30', INK, 1.5);
    R(g, 282, 416, 10, 24, '#4a3a30', INK, 1.5);
    g.strokeStyle = 'rgba(232,192,64,.35)'; g.lineWidth = 6;
    g.beginPath(); g.moveTo(500, 360); g.lineTo(500, 600); g.stroke();
    g.beginPath(); g.moveTo(780, 360); g.lineTo(780, 600); g.stroke();
    shell(g, '\u9580', 'Yard gate');
    glow(g, 640, 200, 160, 'rgba(180,210,255,.08)');
  };

  /* ---------- 2. Time-clock office ---------- */
  S2P.depClock = function (g, cleared) {
    rr(g);
    backWall(g, '#4a5854', '#3e4c48');
    R(g, 430, 70, 420, 200, '#1a1220', INK, 3);
    corrug(g, 436, 76, 408, 188, '#3a4254', '#323848', 18);
    lamp(g, 200, 70); lamp(g, 1080, 70);
    concFloor(g, 90, 320, 1100, 530, '#6e6a62', '#5a5650', 23);
    oilStain(g, 280, 780, 40, 12); oilStain(g, 960, 700, 36, 12);
    /* card rack */
    R(g, 140, 90, 240, 200, '#3a3e48', INK, 2.5);
    txt(g, '\u30bf\u30a4\u30e0\u30ab\u30fc\u30c9', 260, 112, 12, '#f0e4c8');
    var i, j;
    for (j = 0; j < 4; j++) for (i = 0; i < 5; i++) {
      R(g, 160 + i * 40, 130 + j * 36, 32, 28, (i + j) % 3 ? '#efe6d2' : '#d8c8a0', INK, 1.2);
    }
    clockPunch(g, 400, 120);
    /* desk in frame */
    R(g, 400, 560, 300, 24, '#5c4638', INK, 3);
    R(g, 400, 584, 300, 100, '#4a3e34', INK, 3);
    R(g, 416, 568, 44, 16, '#2a2430', INK, 1.5);
    R(g, 470, 568, 70, 16, '#efe6d2', INK, 1.5);
    ellipse(g, 570, 572, 10, 8, '#3a2a22', INK, 1.5);
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(660, 560); g.lineTo(660, 528); g.lineTo(688, 516); g.stroke();
    ellipse(g, 696, 516, 14, 10, '#f0d080', INK, 2);
    glow(g, 690, 550, 70, 'rgba(255,200,110,.3)');
    R(g, 400, 684, 300, 12, '#2a2826', INK, 1.5);
    stool(g, 760, 740);
    /* coat rack + jackets, kept inside the side wall */
    g.strokeStyle = INK; g.lineWidth = 4;
    g.beginPath(); g.moveTo(1120, 200); g.lineTo(1120, 360); g.stroke();
    R(g, 1076, 200, 88, 8, '#3a3e48', INK, 2);
    R(g, 1084, 210, 28, 70, '#3a463c', INK, 2);
    R(g, 1120, 216, 28, 64, '#2a3858', INK, 2);
    /* notice board */
    R(g, 900, 90, 200, 180, '#d8c8a0', INK, 3);
    txt(g, '\u5f53\u756a\u8868', 1000, 112, 13, '#5a2a28');
    g.strokeStyle = '#5a3a28'; g.lineWidth = 1.4;
    for (i = 0; i < 6; i++) { g.beginPath(); g.moveTo(916, 130 + i * 20); g.lineTo(1084, 130 + i * 20); g.stroke(); }
    if (!cleared) { g.strokeStyle = '#a84838'; g.lineWidth = 3; g.beginPath(); g.moveTo(940, 150); g.lineTo(1060, 150); g.stroke(); }
    lockers(g, 860, 400, 5, 180);
    hardhat(g, 880, 392); hardhat(g, 940, 392);
    /* filing */
    R(g, 160, 480, 180, 180, '#4a5060', INK, 3);
    R(g, 170, 500, 160, 12, '#3a3e48', INK, 1.5);
    R(g, 170, 540, 160, 12, '#3a3e48', INK, 1.5);
    R(g, 170, 580, 160, 12, '#3a3e48', INK, 1.5);
    txt(g, '\u53f0\u5e33', 250, 470, 12, '#f0e4c8');
    /* shoe bench, umbrella stand, trash, heater, cooler — sides, walk stays open */
    R(g, 140, 700, 160, 16, '#4a3a30', INK, 2);
    R(g, 148, 716, 10, 24, '#4a3a30', INK, 1.5);
    R(g, 282, 716, 10, 24, '#4a3a30', INK, 1.5);
    R(g, 160, 684, 40, 16, '#2a2430', INK, 1.5);
    R(g, 210, 684, 36, 16, '#3a322c', INK, 1.5);
    R(g, 340, 760, 20, 50, '#3a3e48', INK, 2);
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(350, 760); g.quadraticCurveTo(330, 720, 344, 700); g.stroke();
    g.beginPath(); g.moveTo(350, 760); g.quadraticCurveTo(370, 720, 356, 694); g.stroke();
    R(g, 1000, 700, 40, 50, '#3a3e48', INK, 2);
    /* kerosene heater */
    R(g, 1080, 680, 44, 50, '#8a3a28', INK, 2);
    ellipse(g, 1102, 680, 22, 8, '#6a2a1c', INK, 2);
    glow(g, 1102, 704, 30, 'rgba(255,140,60,.25)');
    R(g, 1080, 760, 50, 40, '#efe6d2', INK, 1.5);
    cableRun(g, 800, 328, 1180, 328);
    hoseCoil(g, 240, 820, 16);
    floorMat(g, 400, 700, 300, 46, '#3a322c');
    papers(g, 320, 640);
    papers(g, 1080, 640);
    waterCooler(g, 160, 360);
    shell(g, '\u6253\u523b', 'Time clock');
  };

  /* ---------- 3. Loading bay ---------- */
  S2P.depBay = function (g, cleared) {
    rr(g);
    backWall(g, '#3a4254', '#323848');
    /* open dock to the night yard — rain stays in the bay opening */
    R(g, 280, 50, 720, 270, '#1a1220', INK, 3);
    var sky = g.createLinearGradient(0, 56, 0, 280);
    sky.addColorStop(0, '#1a2238'); sky.addColorStop(1, '#1a2430');
    g.fillStyle = sky; g.fillRect(286, 56, 708, 200);
    g.fillStyle = '#3a322c'; g.fillRect(286, 220, 708, 54);
    g.fillStyle = '#5a3040'; g.fillRect(286, 248, 708, 26);
    var i, r = function (s) { var v = s; return function () { v = (v * 16807) % 2147483647; return (v - 1) / 2147483646; }; }(9);
    g.save(); g.beginPath(); g.rect(286, 56, 708, 200); g.clip();
    g.strokeStyle = 'rgba(200,220,255,.32)'; g.lineWidth = 1.2;
    for (i = 0; i < 28; i++) {
      var rx = 286 + r() * 708, ry = 56 + r() * 200, L = 10 + r() * 16;
      g.beginPath(); g.moveTo(rx, ry); g.lineTo(rx + 3, ry + L); g.stroke();
    }
    g.restore();
    caution(g, 286, 264, 708, 16);
    lamp(g, 200, 70); lamp(g, 1080, 70);
    concFloor(g, 90, 320, 1100, 530, '#6a6460', '#5a5450', 31);
    oilStain(g, 260, 700, 70, 20); oilStain(g, 1000, 620, 50, 16); oilStain(g, 200, 480, 40, 12);
    /* KITUNE truck at the dock, nose-in */
    R(g, 500, 120, 280, 140, '#3a3e48', INK, 3);
    R(g, 510, 130, 260, 80, '#2a2c34', INK, 2);
    R(g, 520, 140, 80, 40, '#1a2230', INK, 1.5);
    R(g, 760, 150, 16, 70, '#c45a3a', INK, 1.5);
    txt(g, 'KITSUNE', 640, 200, 16, '#f0e4c8', '800 ');
    ellipse(g, 540, 266, 22, 22, '#1a1220', INK, 2);
    ellipse(g, 740, 266, 22, 22, '#1a1220', INK, 2);
    /* dock bumpers */
    R(g, 300, 280, 40, 30, '#3a2a22', INK, 2);
    R(g, 940, 280, 40, 30, '#3a2a22', INK, 2);
    signPlate(g, 140, 360, 80, 44, '\u8377\u5f79', '#e8c040');
    steelDoor(g, 140, 80, 90, 200, '\u6253\u523b');
    /* forklift mid-left, walk lane from the south kept clear */
    forklift(g, 140, 520, 1.05);
    crate(g, 140, 700, 110, 80, '\u8ca8\u7269');
    crate(g, 160, 630, 90, 70, '');
    pallet(g, 140, 790, 140, 26);
    crate(g, 1030, 700, 110, 80, '');
    crate(g, 1040, 630, 90, 70, '');
    drum(g, 260, 740, 36, 60, '#6a3a28');
    drum(g, 980, 740, 32, 56, '#3a4a38');
    cone(g, 380, 800); cone(g, 840, 800);
    handTruck(g, 1080, 520);
    hose(g, 280, 820, 160);
    chainCoil(g, 200, 840, 18);
    cableRun(g, 900, 328, 1180, 328);
    pallet(g, 880, 480, 120, 24);
    crate(g, 896, 420, 90, 60, '');
    pallet(g, 160, 460, 100, 22);
    crate(g, 180, 400, 70, 50, '');
    drum(g, 360, 500, 32, 54, '#6a3a28');
    tires(g, 1080, 600, 3, 26);
    jerry(g, 380, 740, 1);
    chainCoil(g, 360, 640, 16);
    shell(g, '\u8377\u5f79', 'Loading bay');
  };

  /* ---------- 4. Crate stacks ---------- */
  S2P.depCrates = function (g, cleared) {
    rr(g);
    backWall(g, '#3a4254', '#323848');
    lamp(g, 200, 70); lamp(g, 1080, 70);
    concFloor(g, 90, 320, 1100, 530, '#6a6460', '#5a5450', 37);
    oilStain(g, 300, 700, 50, 16); oilStain(g, 980, 760, 46, 14);
    steelDoor(g, 140, 80, 90, 200, '\u8377\u5f79');
    steelDoor(g, 1050, 80, 90, 200, '\u51b7\u51cd');
    signPlate(g, 250, 90, 90, 40, '\u8ca8\u7269', '#d8c8a0');
    /* stacked aisles left and right, a narrow walk down the middle */
    var stack = function (sx, sy, rows, cols, lab) {
      var r, c, w = 90, h = 70;
      for (r = 0; r < rows; r++) for (c = 0; c < cols; c++) {
        crate(g, sx + c * 96, sy - r * 62, w, h, r === rows - 1 && c === 0 ? lab : '');
      }
    };
    stack(140, 740, 4, 3, '\u8ca8\u7269');
    stack(860, 740, 4, 3, '');
    pallet(g, 140, 810, 280, 26);
    pallet(g, 860, 810, 280, 26);
    /* loose mid-side crates, walk still open */
    crate(g, 460, 760, 70, 50, '');
    crate(g, 750, 770, 70, 50, '');
    handTruck(g, 430, 700);
    drum(g, 250, 500, 32, 54, '#3a4a38');
    hoseCoil(g, 1080, 820, 18);
    chainCoil(g, 200, 840, 16);
    cableRun(g, 100, 328, 250, 328);
    cone(g, 540, 820); cone(g, 720, 820);
    shell(g, '\u8ca8\u7269', 'Crate stacks');
  };

  /* ---------- 5. Cold store ---------- */
  S2P.depCold = function (g, cleared) {
    rr(g);
    /* frost-blue walls */
    corrug(g, 90, 40, 1100, 280, '#4a6070', '#3e5464', 22);
    R(g, 90, 40, 1100, 18, '#2a3a44', INK, 2);
    /* frost bloom on the wall — read as ice, not just a tint */
    g.fillStyle = 'rgba(220,236,255,.22)';
    g.fillRect(90, 58, 1100, 260);
    var i, j;
    g.fillStyle = 'rgba(240,250,255,.4)';
    for (i = 0; i < 70; i++) g.fillRect(110 + (i * 73) % 1060, 70 + (i * 29) % 230, 22 + (i % 5) * 8, 8);
    g.fillStyle = 'rgba(255,255,255,.18)';
    for (i = 0; i < 30; i++) {
      g.beginPath(); g.ellipse(140 + (i * 97) % 1000, 80 + (i * 37) % 220, 18, 8, 0, 0, 7); g.fill();
    }
    lamp(g, 200, 70); lamp(g, 1080, 70);
    /* cooler glow */
    glow(g, 640, 200, 200, 'rgba(180,220,255,.16)');
    concFloor(g, 90, 320, 1100, 530, '#6a7278', '#5a6268', 41);
    /* frost on the floor, sides only */
    g.fillStyle = 'rgba(220,236,255,.14)';
    g.beginPath(); g.ellipse(240, 500, 90, 24, 0, 0, 7); g.fill();
    g.beginPath(); g.ellipse(1040, 560, 80, 20, 0, 0, 7); g.fill();
    g.beginPath(); g.ellipse(200, 760, 70, 18, 0, 0, 7); g.fill();
    g.beginPath(); g.ellipse(1080, 780, 60, 16, 0, 0, 7); g.fill();
    /* insulated door with a rubber strip curtain */
    R(g, 140, 70, 110, 230, '#4a6070', INK, 3);
    for (i = 0; i < 8; i++) {
      R(g, 148 + i * 12, 90, 10, 200, i % 2 ? '#3a4a54' : '#2a3a44', INK, 1);
    }
    txt(g, '\u51b7\u51cd', 195, 86, 11, '#d8e8f0');
    /* hanging rail with stock all the way across */
    g.strokeStyle = '#8a9aa8'; g.lineWidth = 6;
    g.beginPath(); g.moveTo(280, 90); g.lineTo(1140, 90); g.stroke();
    var hang = function (hx, col, w) {
      g.strokeStyle = INK; g.lineWidth = 2;
      g.beginPath(); g.moveTo(hx, 90); g.lineTo(hx, 130); g.stroke();
      R(g, hx - w / 2, 130, w, 70, col, INK, 2);
      g.fillStyle = 'rgba(220,236,255,.2)'; g.fillRect(hx - w / 2, 130, w, 10);
    };
    var cols = ['#8a5a50', '#6a3a38', '#9a7060', '#5a3a40', '#8a4a40', '#7a5048', '#6a4038', '#9a6058'];
    for (i = 0; i < 10; i++) hang(320 + i * 80, cols[i % cols.length], 50 + (i % 3) * 6);
    /* metal shelving left and right, frosted packages */
    var shelf = function (sx) {
      R(g, sx, 360, 160, 280, '#4a5460', INK, 3);
      for (j = 0; j < 4; j++) {
        R(g, sx + 8, 380 + j * 64, 144, 8, '#3a4450', INK, 1.5);
        for (i = 0; i < 3; i++) {
          R(g, sx + 14 + i * 46, 396 + j * 64, 40, 36, (i + j) % 2 ? '#c8d0d8' : '#d8e0e8', INK, 1.2);
          g.fillStyle = 'rgba(220,236,255,.3)'; g.fillRect(sx + 14 + i * 46, 396 + j * 64, 40, 8);
        }
      }
    };
    shelf(140); shelf(980);
    /* drain in the walk, thermometer, more hanging mid-sides */
    R(g, 610, 700, 60, 40, '#3a4250', INK, 2);
    g.strokeStyle = '#2a323c'; g.lineWidth = 1.4;
    g.beginPath(); g.moveTo(610, 720); g.lineTo(670, 720); g.stroke();
    g.beginPath(); g.moveTo(640, 700); g.lineTo(640, 740); g.stroke();
    R(g, 420, 80, 24, 60, '#d8e0e8', INK, 2);
    ellipse(g, 432, 120, 8, 8, '#c45a3a', INK, 1.4);
    txt(g, '-18\u00b0', 432, 96, 9, '#3a2a22', '800 ');
    crate(g, 340, 720, 80, 56, '');
    crate(g, 860, 730, 80, 56, '');
    pallet(g, 330, 786, 100, 22);
    pallet(g, 850, 796, 100, 22);
    hoseCoil(g, 240, 820, 16);
    signPlate(g, 860, 90, 80, 40, '\u5b88\u308c', '#7ec8e8');
    cableRun(g, 100, 328, 240, 328);
    /* mid-side carts, more frost on the packages and floor */
    pallet(g, 340, 500, 110, 22);
    crate(g, 350, 440, 80, 56, '');
    g.fillStyle = 'rgba(220,236,255,.35)'; g.fillRect(350, 440, 80, 10);
    pallet(g, 820, 520, 110, 22);
    crate(g, 830, 460, 80, 56, '');
    g.fillStyle = 'rgba(220,236,255,.35)'; g.fillRect(830, 460, 80, 10);
    shell(g, '\u51b7\u51cd', 'Cold store');
  };

  /* ---------- 6. Parts cage ---------- */
  S2P.depCage = function (g, cleared) {
    rr(g);
    backWall(g, '#3a4254', '#323848');
    lamp(g, 200, 70); lamp(g, 1080, 70);
    concFloor(g, 90, 320, 1100, 530, '#6a6460', '#5a5450', 43);
    oilStain(g, 280, 700, 50, 16); oilStain(g, 1000, 640, 46, 14); oilStain(g, 240, 500, 30, 10);
    /* the cage itself */
    R(g, 300, 70, 680, 30, '#3a3e48', INK, 3);
    R(g, 300, 100, 24, 500, '#3a3e48', INK, 3);
    R(g, 956, 100, 24, 500, '#3a3e48', INK, 3);
    mesh(g, 300, 104, 24, 496); mesh(g, 956, 104, 24, 496);
    mesh(g, 324, 80, 632, 20);
    /* shelves inside, denser */
    var i, j;
    for (j = 0; j < 5; j++) {
      R(g, 340, 140 + j * 80, 600, 10, '#4a4e58', INK, 1.5);
      for (i = 0; i < 8; i++) {
        R(g, 360 + i * 70, 152 + j * 80, 50, 36, (i + j) % 3 ? '#6a707c' : '#8a5a38', INK, 1.2);
      }
    }
    /* open cage door swung to the left */
    R(g, 220, 200, 80, 280, '#3a3e48', INK, 3);
    mesh(g, 228, 210, 64, 260);
    signPlate(g, 540, 90, 200, 28, '\u90e8\u54c1\u30b1\u30fc\u30b8', '#d8c8a0');
    /* workbench outside the cage, left of the walk */
    R(g, 140, 560, 140, 18, '#5c4638', INK, 3);
    R(g, 148, 578, 12, 50, '#4a3e34', INK, 2);
    R(g, 260, 578, 12, 50, '#4a3e34', INK, 2);
    R(g, 150, 544, 40, 16, '#6a707c', INK, 1.5);
    R(g, 200, 544, 50, 16, '#3a3e48', INK, 1.5);
    stool(g, 200, 680);
    /* bins and spill of bolts at the edges */
    R(g, 140, 700, 70, 40, '#c45a3a', INK, 2);
    R(g, 220, 710, 60, 36, '#3a4a38', INK, 2);
    g.fillStyle = '#8a8fa0';
    for (i = 0; i < 12; i++) ellipse(g, 160 + (i * 17) % 80, 760 + (i * 7) % 16, 3, 2, '#8a8fa0', INK, 0.8);
    drum(g, 1040, 700, 36, 60, '#6a3a28');
    drum(g, 1084, 720, 32, 50, '#3a4a38');
    pallet(g, 1000, 790, 140, 24);
    crate(g, 1010, 720, 80, 50, '');
    handTruck(g, 1080, 640);
    hoseCoil(g, 280, 830, 16);
    chainCoil(g, 1140, 820, 18);
    cableRun(g, 100, 328, 220, 328);
    steelDoor(g, 140, 80, 90, 200, '\u51b7\u51cd');
    crate(g, 340, 760, 70, 50, '');
    pallet(g, 330, 816, 100, 22);
    papers(g, 280, 640);
    shell(g, '\u90e8\u54c1', 'Parts cage');
  };

  /* ---------- 7. Bike bay ---------- */
  S2P.depBikes = function (g, cleared) {
    rr(g);
    backWall(g, '#3a4254', '#323848');
    lamp(g, 200, 70); lamp(g, 1080, 70);
    concFloor(g, 90, 320, 1100, 530, '#6a6460', '#5a5450', 47);
    oilStain(g, 300, 700, 70, 20); oilStain(g, 980, 640, 50, 16); oilStain(g, 240, 500, 36, 12);
    /* a real tool wall, Hase-workshop density */
    toolWall(g, 140, 70, 240, 200);
    toolWall(g, 900, 70, 200, 180);
    /* mats + bikes — four along the sides, one mid-left, walk lane clear */
    R(g, 140, 620, 200, 70, '#3a322c', INK, 2);
    moto(g, 150, 580, 1.05, '#d46028');
    R(g, 140, 760, 200, 70, '#3a322c', INK, 2);
    moto(g, 150, 720, 1.05, '#2a3a70');
    R(g, 940, 620, 200, 70, '#3a322c', INK, 2);
    moto(g, 950, 580, 1.05, '#3a8a50');
    R(g, 940, 760, 200, 70, '#3a322c', INK, 2);
    moto(g, 950, 720, 1.05, '#8a3a28');
    /* a fifth bike parked against the back-left */
    R(g, 400, 400, 180, 60, '#3a322c', INK, 2);
    moto(g, 410, 360, 0.95, '#4a4e58');
    tires(g, 260, 540, 5, 32);
    tires(g, 1080, 540, 4, 32);
    tires(g, 200, 840, 3, 28);
    jerry(g, 360, 800, 1.2);
    jerry(g, 400, 810, 1);
    /* workbench */
    R(g, 420, 760, 180, 18, '#5c4638', INK, 3);
    R(g, 430, 778, 12, 40, '#4a3e34', INK, 2);
    R(g, 590, 778, 12, 40, '#4a3e34', INK, 2);
    R(g, 440, 744, 50, 16, '#6a707c', INK, 1.5);
    R(g, 500, 744, 40, 16, '#3a3e48', INK, 1.5);
    /* helmets on a shelf */
    R(g, 900, 260, 200, 14, '#4a3e34', INK, 2);
    ellipse(g, 940, 248, 16, 12, '#1a1220', INK, 2);
    ellipse(g, 1000, 248, 16, 12, '#d46028', INK, 2);
    ellipse(g, 1060, 248, 16, 12, '#2a3a70', INK, 2);
    hose(g, 680, 820, 160);
    chainCoil(g, 820, 830, 16);
    signPlate(g, 700, 90, 80, 40, '\u99d0\u8f2a', '#d8c8a0');
    steelDoor(g, 620, 80, 70, 180, '\u914d\u8eca');
    tires(g, 820, 500, 4, 28);
    jerry(g, 800, 800, 1);
    floorMat(g, 500, 800, 140, 30, '#3a322c');
    R(g, 720, 400, 140, 50, '#3a322c', INK, 2);
    /* creeper + jack at the mid-right edge */
    R(g, 800, 700, 70, 16, '#3a3e48', INK, 2);
    ellipse(g, 812, 716, 8, 8, '#1a1220', INK, 1.4);
    ellipse(g, 858, 716, 8, 8, '#1a1220', INK, 1.4);
    shell(g, '\u99d0\u8f2a', 'Bike bay');
  };

  /* ---------- 8. Dispatch loft ---------- */
  S2P.depLoft = function (g, cleared) {
    rr(g);
    backWall(g, '#3a4254', '#323848');
    /* the canal window, lit — night water, lanterns, a little rain outside the glass */
    R(g, 420, 60, 440, 240, '#1a1220', INK, 3);
    var sky = g.createLinearGradient(0, 66, 0, 300);
    sky.addColorStop(0, '#12182a'); sky.addColorStop(1, '#1a2438');
    g.fillStyle = sky; g.fillRect(426, 66, 428, 160);
    /* canal water, lit */
    var wat = g.createLinearGradient(0, 226, 0, 296);
    wat.addColorStop(0, '#1a3a58'); wat.addColorStop(0.5, '#2a5a80'); wat.addColorStop(1, '#1a3048');
    g.fillStyle = wat; g.fillRect(426, 226, 428, 68);
    g.strokeStyle = 'rgba(180,220,255,.35)'; g.lineWidth = 1.4;
    var i;
    for (i = 0; i < 6; i++) { g.beginPath(); g.moveTo(430, 236 + i * 10); g.lineTo(850, 236 + i * 10); g.stroke(); }
    /* window lamp reflections on the water */
    glow(g, 520, 250, 30, 'rgba(255,200,110,.35)');
    glow(g, 720, 252, 30, 'rgba(255,200,110,.3)');
    g.fillStyle = '#f0d080';
    for (i = 0; i < 10; i++) g.fillRect(450 + i * 38, 248, 3, 3);
    /* a small barge */
    R(g, 600, 238, 70, 16, '#3a2a22', INK, 1.5);
    /* window panes + mullions */
    g.strokeStyle = INK; g.lineWidth = 4;
    g.beginPath(); g.moveTo(640, 66); g.lineTo(640, 294); g.stroke();
    g.beginPath(); g.moveTo(426, 180); g.lineTo(854, 180); g.stroke();
    /* warm interior light on the glass */
    glow(g, 640, 160, 140, 'rgba(255,200,110,.16)');
    /* rain only on the far side of the glass, clipped to the panes */
    g.save(); g.beginPath(); g.rect(426, 66, 428, 114); g.clip();
    g.strokeStyle = 'rgba(200,220,255,.28)'; g.lineWidth = 1.1;
    var r = function (s) { var v = s; return function () { v = (v * 16807) % 2147483647; return (v - 1) / 2147483646; }; }(13);
    for (i = 0; i < 16; i++) {
      var rx = 426 + r() * 428, ry = 66 + r() * 114, L = 8 + r() * 12;
      g.beginPath(); g.moveTo(rx, ry); g.lineTo(rx + 2, ry + L); g.stroke();
    }
    g.restore();
    lamp(g, 200, 70); lamp(g, 1080, 70);
    concFloor(g, 90, 320, 1100, 530, '#6e6a62', '#5a5650', 53);
    oilStain(g, 260, 760, 40, 12); oilStain(g, 1000, 700, 36, 12);
    /* desks */
    R(g, 200, 560, 280, 22, '#5c4638', INK, 3);
    R(g, 200, 582, 280, 90, '#4a3e34', INK, 3);
    R(g, 216, 546, 40, 16, '#2a2c34', INK, 1.5);
    R(g, 270, 546, 50, 16, '#efe6d2', INK, 1.5);
    R(g, 340, 546, 36, 16, '#3a3e48', INK, 1.5);
    R(g, 200, 672, 280, 12, '#2a2826', INK, 1.5);
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(430, 560); g.lineTo(430, 528); g.lineTo(456, 516); g.stroke();
    ellipse(g, 464, 516, 14, 10, '#f0d080', INK, 2);
    glow(g, 460, 550, 60, 'rgba(255,200,110,.3)');
    R(g, 760, 520, 260, 22, '#5c4638', INK, 3);
    R(g, 760, 542, 260, 80, '#4a3e34', INK, 3);
    R(g, 776, 506, 40, 16, '#2a2c34', INK, 1.5);
    R(g, 840, 506, 70, 16, '#efe6d2', INK, 1.5);
    R(g, 760, 622, 260, 12, '#2a2826', INK, 1.5);
    stool(g, 520, 720); stool(g, 900, 680);
    /* radio cabinet, file crates, papers, jacket */
    R(g, 140, 400, 80, 60, '#3a3e48', INK, 2);
    ellipse(g, 160, 420, 6, 6, '#c45a3a', INK, 1);
    ellipse(g, 180, 420, 6, 6, '#3a6a3a', INK, 1);
    crate(g, 140, 700, 90, 70, '\u53f0\u5e33');
    crate(g, 150, 640, 80, 60, '');
    R(g, 1040, 700, 70, 50, '#efe6d2', INK, 2);
    R(g, 1080, 740, 60, 40, '#efe6d2', INK, 2);
    R(g, 1140, 200, 28, 70, '#3a463c', INK, 2);
    cableRun(g, 100, 328, 400, 328);
    cableRun(g, 880, 328, 1180, 328);
    signPlate(g, 160, 90, 90, 40, '\u914d\u8eca', '#d8c8a0');
    steelDoor(g, 1050, 80, 90, 200, '\u4f11\u61a9');
    floorMat(g, 200, 690, 280, 40, '#3a322c');
    floorMat(g, 760, 640, 260, 40, '#3a322c');
    papers(g, 520, 640);
    papers(g, 1040, 640);
    crate(g, 1040, 500, 70, 50, '');
    R(g, 1080, 400, 50, 70, '#3a3e48', INK, 2);
    shell(g, '\u914d\u8eca', 'Dispatch loft');
  };

  /* ---------- 9. Break room ---------- */
  S2P.depBreak = function (g, cleared) {
    rr(g);
    corrug(g, 90, 40, 1100, 280, '#5a4a40', '#504038', 22);
    R(g, 90, 40, 1100, 18, '#3a2e28', INK, 2);
    lamp(g, 200, 70); lamp(g, 1080, 70);
    concFloor(g, 90, 320, 1100, 530, '#6a5e54', '#5a4e44', 59);
    oilStain(g, 260, 780, 30, 10);
    /* clock + no smoking */
    ellipse(g, 180, 120, 28, 28, '#efe6d2', INK, 2);
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(180, 120); g.lineTo(180, 102); g.stroke();
    g.beginPath(); g.moveTo(180, 120); g.lineTo(194, 126); g.stroke();
    R(g, 520, 80, 240, 140, '#1a2030', INK, 3);
    R(g, 532, 92, 216, 116, '#2a3850', 0);
    signPlate(g, 900, 90, 80, 44, '\u7981\u7159', '#f0e4c8');
    /* vending machine — a real one, with a window of cans */
    R(g, 1020, 360, 130, 280, '#3a4a68', INK, 3);
    R(g, 1030, 380, 110, 160, '#1a2030', INK, 2);
    var i, j, vc = ['#c45a3a', '#3a6a3a', '#d4a830', '#2a3a70', '#8a3a50', '#4a8aa0'];
    for (j = 0; j < 4; j++) for (i = 0; i < 4; i++) {
      R(g, 1038 + i * 24, 390 + j * 36, 20, 28, vc[(i + j) % vc.length], INK, 1);
    }
    R(g, 1034, 548, 100, 16, '#2a2c34', INK, 1.5);
    for (i = 0; i < 8; i++) ellipse(g, 1046 + i * 12, 556, 4, 4, i % 2 ? '#c45a3a' : '#3a6a3a', INK, 1);
    R(g, 1054, 580, 60, 28, '#1a1220', INK, 2);
    R(g, 1070, 614, 30, 14, '#c4a060', INK, 1.4);
    txt(g, 'HOT', 1085, 372, 10, '#f0e4c8', '800 ');
    /* kettle on a side counter, with a soft steam glow */
    R(g, 140, 520, 180, 18, '#5c4638', INK, 3);
    R(g, 148, 538, 12, 40, '#4a3e34', INK, 2);
    R(g, 300, 538, 12, 40, '#4a3e34', INK, 2);
    R(g, 160, 492, 44, 28, '#8a8fa0', INK, 2);
    ellipse(g, 182, 492, 16, 8, '#6a707c', INK, 1.5);
    R(g, 200, 484, 10, 10, '#4a4e58', INK, 1.4);
    glow(g, 182, 470, 24, 'rgba(220,230,240,.35)');
    R(g, 230, 500, 36, 20, '#efe6d2', INK, 1.5);
    R(g, 274, 504, 22, 16, '#3a3e48', INK, 1.5);
    /* microwave */
    R(g, 140, 400, 70, 50, '#4a4e58', INK, 2);
    R(g, 148, 408, 44, 30, '#1a2030', INK, 1.5);
    /* lockers with bags and hats on top */
    lockers(g, 140, 600, 4, 140);
    hardhat(g, 160, 592);
    R(g, 220, 578, 28, 20, '#3a463c', INK, 1.5);
    /* folded futon along the left wall */
    futonFold(g, 140, 760);
    txt(g, '\u5e03\u56e3', 240, 754, 11, '#f0e4c8');
    /* table, benches, cups */
    R(g, 500, 600, 280, 18, '#5c4638', INK, 3);
    R(g, 520, 618, 16, 70, '#4a3e34', INK, 2);
    R(g, 744, 618, 16, 70, '#4a3e34', INK, 2);
    R(g, 530, 580, 30, 20, '#c45a3a', INK, 1.5);
    R(g, 570, 584, 24, 16, '#2a3a70', INK, 1.5);
    ellipse(g, 630, 590, 12, 8, '#d8d0c4', INK, 1.4);
    R(g, 660, 584, 40, 16, '#efe6d2', INK, 1.5);
    R(g, 530, 700, 80, 10, '#4a3e34', INK, 2);
    R(g, 670, 700, 80, 10, '#4a3e34', INK, 2);
    /* slippers, trash, magazine crate */
    R(g, 500, 780, 28, 14, '#3a2a22', INK, 1.4);
    R(g, 536, 780, 28, 14, '#3a2a22', INK, 1.4);
    R(g, 900, 740, 44, 50, '#3a3e48', INK, 2);
    crate(g, 860, 700, 70, 40, '');
    cableRun(g, 100, 328, 240, 328);
    steelDoor(g, 1050, 80, 90, 200, '\u6a2a\u5751');
    /* a short sofa mid-right of the walk, rug under the table */
    floorMat(g, 500, 640, 280, 90, '#4a3a30');
    R(g, 820, 520, 160, 60, '#5a3a40', INK, 2);
    R(g, 828, 500, 144, 24, '#6a4a50', INK, 2);
    papers(g, 860, 640);
    shell(g, '\u4f11\u61a9', 'Break room');
  };

  /* ---------- 10. Tunnel spur ---------- */
  S2P.depTunnel = function (g, cleared) {
    rr(g);
    /* brick receding into a dark arch */
    g.fillStyle = '#2a2420'; g.fillRect(90, 40, 1100, 280);
    var i, j;
    for (j = 0; j < 10; j++) {
      for (i = 0; i < 22; i++) {
        var ox = (j % 2) ? 16 : 0;
        R(g, 100 + i * 50 + ox, 50 + j * 26, 46, 22, (i + j) % 3 ? '#5a3e36' : '#4a322c', INK, 1.2);
      }
    }
    /* receding arch cut into the brick wall */
    g.fillStyle = '#121016';
    g.beginPath();
    g.moveTo(460, 320); g.quadraticCurveTo(640, 70, 820, 320);
    g.closePath(); g.fill();
    g.fillStyle = '#0a080c';
    g.beginPath();
    g.moveTo(520, 320); g.quadraticCurveTo(640, 130, 760, 320);
    g.closePath(); g.fill();
    g.strokeStyle = INK; g.lineWidth = 4;
    g.beginPath();
    g.moveTo(460, 320); g.quadraticCurveTo(640, 70, 820, 320);
    g.stroke();
    lamp(g, 200, 70); lamp(g, 1080, 70);
    glow(g, 640, 200, 120, 'rgba(255,200,110,.1)');
    concFloor(g, 90, 320, 1100, 530, '#5a5450', '#4a4440', 61);
    /* dark throat of the spur, so the arch reads on the floor */
    g.fillStyle = '#0a080c';
    g.beginPath(); g.moveTo(520, 320); g.lineTo(760, 320); g.lineTo(700, 400); g.lineTo(580, 400); g.closePath(); g.fill();
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(520, 320); g.lineTo(580, 400); g.lineTo(700, 400); g.lineTo(760, 320); g.stroke();
    oilStain(g, 300, 700, 50, 16); oilStain(g, 980, 640, 46, 14);
    crate(g, 340, 620, 80, 56, '');
    pallet(g, 330, 680, 100, 22);
    drum(g, 880, 620, 32, 54, '#6a3a28');
    crate(g, 860, 680, 80, 56, '');
    /* puddles along the sides */
    g.fillStyle = 'rgba(80,110,140,.2)';
    g.beginPath(); g.ellipse(240, 500, 70, 16, 0, 0, 7); g.fill();
    g.beginPath(); g.ellipse(1040, 560, 60, 14, 0, 0, 7); g.fill();
    /* pipes and cables along the walls */
    g.strokeStyle = '#6a707c'; g.lineWidth = 8;
    g.beginPath(); g.moveTo(120, 80); g.lineTo(120, 500); g.quadraticCurveTo(120, 560, 200, 600); g.stroke();
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(120, 80); g.lineTo(120, 500); g.quadraticCurveTo(120, 560, 200, 600); g.stroke();
    g.strokeStyle = '#4a3a28'; g.lineWidth = 6;
    g.beginPath(); g.moveTo(1160, 80); g.lineTo(1160, 520); g.quadraticCurveTo(1160, 600, 1040, 640); g.stroke();
    cableRun(g, 100, 328, 200, 328);
    cableRun(g, 1080, 328, 1180, 328);
    /* ladder, barrels, trolley, barrier */
    R(g, 200, 200, 16, 200, '#6a707c', INK, 2);
    for (i = 0; i < 8; i++) R(g, 200, 210 + i * 22, 16, 4, '#4a4e58', INK, 1);
    drum(g, 160, 720, 36, 60, '#6a3a28');
    drum(g, 200, 740, 32, 50, '#3a4a38');
    crate(g, 1040, 700, 100, 70, '');
    pallet(g, 1040, 780, 120, 24);
    handTruck(g, 160, 640);
    chainCoil(g, 280, 820, 18);
    hose(g, 800, 820, 160);
    cone(g, 400, 800); cone(g, 840, 800);
    signPlate(g, 860, 90, 90, 44, '\u6ce8\u610f', '#e8c040');
    steelDoor(g, 140, 80, 70, 180, '\u4f11\u61a9');
    steelDoor(g, 1070, 80, 70, 180, '\u7a4d\u8377');
    shell(g, '\u6a2a\u5751', 'Tunnel spur');
  };

  /* ---------- 11. Manifest office ---------- */
  S2P.depManifest = function (g, cleared) {
    rr(g);
    backWall(g, '#4a5060', '#40465a');
    lamp(g, 200, 70); lamp(g, 1080, 70);
    concFloor(g, 90, 320, 1100, 530, '#6e6a62', '#5a5650', 67);
    oilStain(g, 260, 760, 36, 12);
    /* file cabinets */
    lockers(g, 140, 80, 6, 200);
    /* a big bulletin / schedule */
    R(g, 460, 80, 360, 200, '#d8c8a0', INK, 3);
    txt(g, '\u7a4d\u8377\u8868', 640, 106, 16, '#5a2a28');
    g.strokeStyle = '#5a3a28'; g.lineWidth = 1.4;
    var i;
    for (i = 0; i < 8; i++) { g.beginPath(); g.moveTo(480, 128 + i * 18); g.lineTo(800, 128 + i * 18); g.stroke(); }
    if (!cleared) graySeal(g, 780, 240, 22);
    /* clerk desk */
    R(g, 400, 560, 320, 24, '#5c4638', INK, 3);
    R(g, 400, 584, 320, 100, '#4a3e34', INK, 3);
    manifest(g, 430, 500, 120, 90, !cleared);
    R(g, 570, 544, 50, 16, '#efe6d2', INK, 1.5);
    R(g, 630, 544, 40, 16, '#2a2c34', INK, 1.5);
    ellipse(g, 690, 552, 10, 8, '#3a2a22', INK, 1.5);
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(680, 560); g.lineTo(680, 528); g.lineTo(704, 516); g.stroke();
    ellipse(g, 712, 516, 14, 10, '#f0d080', INK, 2);
    glow(g, 706, 550, 60, 'rgba(255,200,110,.3)');
    R(g, 400, 684, 320, 12, '#2a2826', INK, 1.5);
    stool(g, 760, 740);
    /* mail bins, file crates, overflowing trash, coat, stamp table, safe */
    crate(g, 140, 700, 90, 70, '\u53f0\u5e33');
    crate(g, 150, 640, 80, 60, '');
    R(g, 250, 720, 50, 40, '#c45a3a', INK, 2);
    R(g, 260, 704, 30, 16, '#efe6d2', INK, 1.2);
    R(g, 1040, 700, 50, 60, '#3a3e48', INK, 2);
    R(g, 1046, 686, 36, 16, '#efe6d2', INK, 1.2);
    R(g, 1048, 672, 30, 14, '#efe6d2', INK, 1.2);
    R(g, 900, 700, 90, 50, '#3a3e48', INK, 2);
    R(g, 916, 680, 40, 20, '#c4a060', INK, 1.5);
    /* small safe */
    R(g, 1080, 500, 70, 80, '#3a3e48', INK, 2);
    ellipse(g, 1115, 540, 8, 8, '#c4a060', INK, 1.4);
    /* coat rack */
    g.strokeStyle = INK; g.lineWidth = 4;
    g.beginPath(); g.moveTo(1180, 200); g.lineTo(1180, 380); g.stroke();
    R(g, 1148, 210, 28, 70, '#3a463c', INK, 2);
    handTruck(g, 160, 500);
    cableRun(g, 880, 328, 1180, 328);
    steelDoor(g, 900, 80, 90, 200, '\u6a2a\u5751');
    steelDoor(g, 1020, 80, 90, 200, '\u6607\u964d');
    signPlate(g, 250, 300, 80, 36, '\u4e8b\u52d9', '#d8c8a0');
    floorMat(g, 400, 700, 320, 46, '#3a322c');
    papers(g, 300, 560);
    papers(g, 860, 560);
    crate(g, 860, 620, 70, 50, '');
    shell(g, '\u7a4d\u8377', 'Manifest office');
  };

  /* ---------- 12. Lift anteroom ---------- */
  S2P.depAntero = function (g, cleared) {
    rr(g);
    backWall(g, '#3a4254', '#323848');
    R(g, 400, 80, 480, 200, '#1a1220', INK, 3);
    var i;
    for (i = 0; i < 10; i++) R(g, 408, 88 + i * 18, 464, 18, i % 2 ? '#3a3e4c' : '#32364a', INK, 1.3);
    caution(g, 400, 272, 480, 14);
    /* freight lift frame in front of the slats */
    liftFrame(g, 360, 44, 560, 276);
    lamp(g, 200, 70); lamp(g, 1080, 70);
    concFloor(g, 90, 320, 1100, 530, '#6a6460', '#5a5450', 71);
    oilStain(g, 260, 740, 50, 16); oilStain(g, 1020, 700, 46, 14);
    /* hanging chains at the sides of the frame */
    chainHang(g, 200, 70, 280);
    chainHang(g, 1080, 70, 280);
    chainCoil(g, 240, 820, 20);
    chainCoil(g, 1060, 820, 18);
    /* control panel on a stand */
    R(g, 940, 480, 80, 140, '#2a2c34', INK, 2);
    R(g, 964, 620, 16, 50, '#2a2c34', INK, 2);
    ellipse(g, 980, 530, 10, 10, '#3a6a3a', INK, 1.5);
    ellipse(g, 980, 560, 10, 10, '#6a3a2a', INK, 1.5);
    R(g, 952, 590, 56, 16, '#1a1220', INK, 1.5);
    txt(g, '\u540a\u308a\u6a5f', 980, 470, 11, '#f0e4c8');
    /* staged freight at the sides */
    crate(g, 140, 700, 110, 80, '\u8ca8\u7269');
    crate(g, 160, 630, 90, 70, '');
    pallet(g, 140, 790, 140, 24);
    crate(g, 1030, 700, 110, 80, '');
    drum(g, 260, 740, 36, 60, '#6a3a28');
    drum(g, 980, 740, 32, 56, '#3a4a38');
    signPlate(g, 140, 360, 70, 70, '!', '#e8c040');
    /* gray seal visible on a hanging tag */
    graySeal(g, 320, 200, 22);
    handTruck(g, 160, 520);
    hose(g, 300, 820, 140);
    cableRun(g, 100, 328, 200, 328);
    cone(g, 360, 800); cone(g, 880, 800);
    steelDoor(g, 140, 80, 70, 180, '\u7a4d\u8377');
    warningBox(g, 400, 340, 480, 90);
    crate(g, 140, 500, 80, 56, '');
    pallet(g, 140, 560, 100, 22);
    drum(g, 1080, 560, 32, 54, '#6a3a28');
    chainCoil(g, 320, 640, 16);
    shell(g, '\u6607\u964d\u6a5f\u524d', 'Lift anteroom');
  };

  /* ---------- 13. Lift shutter (boss room) ---------- */
  function shutterRoom(g, mode, broke) {
    /* mode: 'fight' | 'leave' | 'notes' | 'help' | 'cleared' */
    rr(g);
    corrug(g, 90, 40, 1100, 280, '#3a4254', '#323848', 22);
    R(g, 90, 40, 1100, 18, '#2a2e3a', INK, 2);
    R(g, 310, 70, 660, 230, '#1a1220', INK, 3);
    var i;
    for (i = 0; i < 11; i++) {
      R(g, 318, 78 + i * 18, 644, 18, i % 2 ? '#3a3e4c' : '#32364a', INK, 1.3);
    }
    if (!(mode === 'fight' || mode === 'leave')) {
      R(g, 318, 250, 644, 30, '#121018', 0);
    }
    caution(g, 318, 276, 644, 14);
    /* freight lift frame in front of the slats */
    liftFrame(g, 260, 40, 760, 280);
    /* freight manifest + a large gray seal on the shutter itself (omitted / broken after the pry) */
    manifest(g, 500, 110, 160, 120, true);
    if (broke || mode === 'cleared') {
      /* broken seal: pale ring, the 灰 is cracked off */
      g.save();
      g.strokeStyle = '#6a6a72'; g.lineWidth = 3;
      g.beginPath(); g.arc(760, 170, 36, 0.3, Math.PI * 1.6); g.stroke();
      g.strokeStyle = '#3a3a42'; g.lineWidth = 2;
      g.beginPath(); g.moveTo(748, 158); g.lineTo(772, 186); g.stroke();
      g.restore();
    } else {
      graySeal(g, 760, 170, 36);
    }
    lamp(g, 180, 70); lamp(g, 1100, 70);
    glow(g, 640, 160, 180, 'rgba(255,200,110,.16)');
    concFloor(g, 90, 320, 1100, 530, '#6a6460', '#5a5450', 67);
    warningBox(g, 360, 340, 560, 90);
    oilStain(g, 280, 780, 60, 18); oilStain(g, 1000, 740, 50, 16); oilStain(g, 220, 520, 36, 12);
    /* side props, centre lane clear for the fight */
    crate(g, 140, 700, 110, 80, '\u8ca8\u7269');
    crate(g, 160, 630, 100, 70, '');
    crate(g, 150, 560, 90, 70, '');
    drum(g, 260, 720, 36, 60, '#6a3a28');
    pallet(g, 140, 800, 140, 24);
    crate(g, 1030, 700, 110, 80, '');
    crate(g, 1040, 630, 90, 70, '');
    drum(g, 980, 720, 32, 56, '#3a4a38');
    chainHang(g, 160, 70, 300);
    chainHang(g, 1120, 70, 300);
    chainCoil(g, 240, 830, 20);
    chainCoil(g, 1080, 830, 18);
    hose(g, 300, 820, 140);
    handTruck(g, 160, 500);
    cone(g, 340, 800); cone(g, 900, 800);
    /* weighty lower-half props — chains, a pallet jack, oil drums; center lane clear */
    palletJack(g, 280, 620);
    pallet(g, 270, 710, 90, 22);
    drum(g, 300, 760, 36, 60, '#6a3a28');
    drum(g, 340, 780, 32, 56, '#3a4a38');
    drum(g, 920, 760, 36, 60, '#6a3a28');
    drum(g, 960, 780, 32, 54, '#3a4a38');
    chainHang(g, 300, 480, 620);
    chainHang(g, 980, 480, 620);
    chainCoil(g, 380, 840, 22);
    chainCoil(g, 900, 840, 20);
    /* control panel on a stand */
    R(g, 900, 500, 80, 140, '#2a2c34', INK, 2);
    R(g, 924, 640, 16, 50, '#2a2c34', INK, 2);
    ellipse(g, 940, 550, 10, 10, '#3a6a3a', INK, 1.5);
    ellipse(g, 940, 580, 10, 10, '#6a3a2a', INK, 1.5);
    if (mode === 'leave') {
      ellipse(g, 700, 760, 22, 8, '#c4a060', INK, 2);
      R(g, 692, 764, 36, 8, '#3b2a22', INK, 2);
      hardhat(g, 760, 780);
    }
    if (mode === 'notes') {
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
  S2P.depShutter = function (g, broke) { shutterRoom(g, broke ? 'cleared' : 'fight', broke); };
  S2P.depShutterLeave = function (g, broke) { shutterRoom(g, 'leave', broke); };
  S2P.depShutterNotes = function (g, broke) { shutterRoom(g, 'notes', broke); };
  S2P.depShutterHelp = function (g, broke) { shutterRoom(g, 'help', broke); };

  /* ---------- battle: lift shutter ---------- */
  S2P.battleShutter = function (g) {
    var H = (typeof window !== 'undefined' && window.FFF_C2H) || (typeof root !== 'undefined' && root.FFF_C2H);
    var WD = 720, HT = 1280, H0 = 330, x = g, i, y;
    rr(g);
    if (!H) { g.fillStyle = '#1a1410'; g.fillRect(0, 0, WD, HT); return; }
    corrug(g, 0, 0, WD, H0, '#3a4254', '#323848', 22);
    R(g, 0, 0, WD, 18, '#2a2e3a', H.INK, 2);
    R(g, 80, 36, 560, 220, '#1a1220', H.INK, 3);
    for (i = 0; i < 10; i++) R(g, 88, 44 + i * 18, 544, 18, i % 2 ? '#3a3e4c' : '#32364a', H.INK, 1.2);
    caution(g, 88, 248, 544, 12);
    /* freight lift frame in front of the slats */
    liftFrame(g, 40, 8, 640, 270);
    manifest(g, 250, 70, 140, 100, true);
    graySeal(g, 500, 130, 28);
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
    /* warning chevrons only at the sides of the floor */
    caution(g, 8, H0 + 8, 140, 12);
    caution(g, 572, H0 + 8, 140, 12);
    g.restore();
    oilStain(g, 140, 700, 50, 16);
    oilStain(g, 580, 900, 60, 18);
    oilStain(g, 160, 1100, 70, 20);
    /* side props, centre lane (~260-460) clear */
    crate(g, 16, 500, 80, 56, '\u8ca8\u7269');
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
    tires(g, 80, 780, 4, 26); tires(g, 650, 800, 3, 26);
    chainCoil(g, 80, 1050, 16);
    hose(g, 20, 820, 80);
    cone(g, 40, 680);
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
    ['depCrates', 'Crate stacks  \u8ca8\u7269'],
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
