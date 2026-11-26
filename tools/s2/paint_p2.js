/* v6.5.63 FFF_S2P phase 2: Minato-sō façades, lobby, workshop, Night Runs battle rooms.
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
  function tiles(g, x, y, w, h, c1, c2, s) {
    for (var j = y, b = 0; j < y + h; j += s, b++)
      for (var i = x, a = 0; i < x + w; i += s, a++) {
        g.fillStyle = (a + b) % 2 ? c1 : c2; g.fillRect(i, j, s, s);
      }
    g.strokeStyle = 'rgba(0,0,0,.14)'; g.lineWidth = 1.5;
    for (var yy = y; yy <= y + h; yy += s) { g.beginPath(); g.moveTo(x, yy); g.lineTo(x + w, yy); g.stroke(); }
    for (var xx = x; xx <= x + w; xx += s) { g.beginPath(); g.moveTo(xx, y); g.lineTo(xx, y + h); g.stroke(); }
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
  function winPane(g, x, y, w, h, lit, sill) {
    R(g, x - 3, y - 3, w + 6, h + 8, '#3a2a22', INK, 2);
    if (lit) {
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
    if (sill !== 0) R(g, x - 5, y + h, w + 10, 5, '#4a382c', INK, 1.5);
  }
  function shutterBay(g, x, y, w, h, open) {
    if (open) {
      R(g, x, y, w, h, '#1a1520', INK, 3);
      glow(g, x + w / 2, y + h * 0.4, Math.max(40, w * 0.7), 'rgba(255,180,90,.28)');
      /* rolled shutter box at the top */
      R(g, x - 4, y - 10, w + 8, 16, '#6a707c', INK, 2);
      for (var k = 0; k < 3; k++) R(g, x + 4, y - 8 + k * 4, w, 3, k % 2 ? '#7a8090' : '#5a606c', 0);
    } else {
      R(g, x, y, w, h, '#8a8fa0', INK, 3);
      for (var yy = y + 8; yy < y + h - 4; yy += 10) {
        g.beginPath(); g.moveTo(x + 3, yy); g.lineTo(x + w - 3, yy);
        g.strokeStyle = 'rgba(20,20,30,.35)'; g.lineWidth = 2; g.stroke();
      }
      R(g, x - 4, y - 8, w + 8, 14, '#6a707c', INK, 2);
      /* handle */
      R(g, x + w / 2 - 10, y + h * 0.55, 20, 8, '#3a3e48', INK, 1.5);
    }
  }


  function rain(g, H, n, seedN) {
    var r = (H && H.seed) ? H.seed(seedN || 3) : function () { return Math.random(); };
    g.strokeStyle = 'rgba(200,210,230,.22)'; g.lineWidth = 1.2;
    for (var i = 0; i < (n || 50); i++) {
      var rx = r() * 720, ry = r() * 1280, rl = 10 + r() * 16;
      g.beginPath(); g.moveTo(rx, ry); g.lineTo(rx - 2, ry + rl); g.stroke();
    }
  }
  function wheel(g, x, y, r) {
    ellipse(g, x, y, r, r, '#1a1220', INK, 3);
    ellipse(g, x, y, r * 0.55, r * 0.55, '#3a3e48', INK, 1.8);
    ellipse(g, x, y, r * 0.18, r * 0.18, '#8a8fa0', INK, 1.4);
    g.strokeStyle = 'rgba(200,200,210,.25)'; g.lineWidth = 1;
    for (var i = 0; i < 6; i++) {
      var a = i * Math.PI / 3;
      g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * r * 0.9, y + Math.sin(a) * r * 0.9); g.stroke();
    }
  }
  function moto(g, bx, by, s) {
    s = s || 1;
    g.save(); g.translate(bx, by); g.scale(s, s);
    g.fillStyle = 'rgba(0,0,0,.28)';
    g.beginPath(); g.ellipse(55, 78, 70, 10, 0, 0, 7); g.fill();
    wheel(g, 18, 70, 20);
    wheel(g, 100, 70, 20);
    /* exhaust */
    R(g, 40, 78, 36, 6, '#6a707c', INK, 1.6);
    /* swingarm / frame */
    g.strokeStyle = INK; g.lineWidth = 4; g.lineJoin = 'round';
    g.beginPath(); g.moveTo(18, 70); g.lineTo(48, 42); g.lineTo(86, 42); g.lineTo(100, 70); g.stroke();
    g.beginPath(); g.moveTo(48, 42); g.lineTo(48, 62); g.lineTo(18, 70); g.stroke();
    /* tank + seat */
    ellipse(g, 58, 38, 22, 12, '#2a3a70', INK, 2);
    R(g, 68, 30, 28, 12, '#1a1520', INK, 2);
    /* fork + bars + lamp */
    g.beginPath(); g.moveTo(100, 70); g.lineTo(112, 28); g.stroke();
    g.beginPath(); g.moveTo(100, 24); g.lineTo(124, 20); g.stroke();
    ellipse(g, 118, 32, 7, 7, '#f0e4c0', INK, 1.6);
    glow(g, 118, 32, 16, 'rgba(255,220,140,.35)');
    g.restore();
  }
  function puddles(g, H, H0) {
    var r = H.seed(9), yy, xx, s, i;
    for (i = 0; i < 80; i++) {
      yy = H0 + 8 + r() * 70; xx = r() * 720; s = 10 + (yy - H0) / 8;
      g.fillStyle = 'rgba(0,0,0,' + (0.06 + r() * 0.1) + ')';
      g.beginPath(); g.ellipse(xx, yy, s * 1.8, s * 0.45, 0, 0, 6.28); g.fill();
    }
  }

  /* ---------- north façade overlay, 1140 x 168, sits on eastS north street edge ---------- */
  S2P.minaNorth = function (g, W0, H0) {
    W0 = W0 || 1140; H0 = H0 || 168; rr(g);
    /* wood siding, same family as the south face of eastS */
    plank(g, 0, 0, W0, H0, '#5a4034', '#4e372c', 42);
    R(g, 0, 0, W0, 14, '#2a2018', INK, 0);
    R(g, 0, H0 - 18, W0, 18, '#3a2a22', INK, 0);
    /* cornice shadow */
    g.fillStyle = 'rgba(0,0,0,.28)'; g.fillRect(0, 14, W0, 6);
    /* signboard */
    R(g, W0 / 2 - 130, 18, 260, 36, '#f0e4c8', INK, 3);
    txt(g, '\u6e2f\u8358', W0 / 2 - 70, 36, 22, '#5a2a28', '900 ');
    txt(g, 'MINATO-S\u014c', W0 / 2 + 50, 36, 13, '#3a2a22', '800 ');
    /* upper windows: mixed lit / dark */
    var litN = [1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1];
    var i, wx, gap = 18, ww = 70, wh = 58, x0 = 28;
    for (i = 0; i < 12; i++) {
      wx = x0 + i * (ww + gap);
      if (wx + ww > W0 - 20) break;
      winPane(g, wx, 64, ww, wh, litN[i]);
      if (i === 4) { /* plant in a dark window */
        g.fillStyle = '#2f5a38';
        g.beginPath(); g.ellipse(wx + 22, 64 + 40, 8, 14, 0.4, 0, 7); g.fill();
        g.beginPath(); g.ellipse(wx + 30, 64 + 36, 7, 12, -0.3, 0, 7); g.fill();
      }
      if (i === 8 && litN[i]) { /* curtain edge */
        g.fillStyle = 'rgba(180,80,80,.45)'; g.fillRect(wx + 2, 66, 10, wh - 4);
      }
    }
    /* warm spill under lit panes */
    for (i = 0; i < 12; i++) if (litN[i]) {
      wx = x0 + i * (ww + gap);
      glow(g, wx + ww / 2, H0 - 8, 36, 'rgba(255,190,100,.18)');
    }
    /* lobby door, right of centre */
    var dx = 820, dw = 88, dh = 70, dy = H0 - dh - 4;
    R(g, dx - 8, dy - 8, dw + 16, dh + 12, '#3a2a22', INK, 3);
    R(g, dx, dy, dw, dh, '#2a2430', INK, 3);
    /* glass panels */
    R(g, dx + 6, dy + 6, 34, 36, '#c8d8d0', INK, 2);
    R(g, dx + 46, dy + 6, 34, 36, '#c8d8d0', INK, 2);
    g.fillStyle = 'rgba(255,255,255,.28)'; g.fillRect(dx + 8, dy + 8, 12, 20);
    R(g, dx + 6, dy + 46, 74, 20, '#4a3428', INK, 2);
    ellipse(g, dx + dw - 14, dy + 56, 4, 4, '#c4a060', INK, 1.5);
    glow(g, dx + dw / 2, dy + 20, 50, 'rgba(255,200,130,.22)');
    R(g, dx + 8, dy - 20, 72, 14, '#efe4c8', INK, 2);
    txt(g, '\u30ed\u30d3\u30fc', dx + dw / 2, dy - 13, 10, '#5a2a28', '800 ');
    /* ink outline of the whole overlay */
    g.strokeStyle = INK; g.lineWidth = 3; g.strokeRect(1, 1, W0 - 2, H0 - 2);
  };

  /* ---------- south façade overlay, 1140 x 220: windows, shutters, workshop door ---------- */
  S2P.minaSouth = function (g, W0, H0) {
    W0 = W0 || 1140; H0 = H0 || 220; rr(g);
    plank(g, 0, 0, W0, H0, '#5a4034', '#4e372c', 46);
    R(g, 0, 0, W0, 16, '#2a2018', INK, 0);
    g.fillStyle = 'rgba(0,0,0,.28)'; g.fillRect(0, 16, W0, 6);
    /* building name, left of centre so it does not sit on the workshop door */
    R(g, 360, 14, 300, 32, '#f0e4c8', INK, 3);
    txt(g, '\u6e2f\u8358', 470, 30, 20, '#5a2a28', '900 ');
    txt(g, 'MINATO-S\u014c', 590, 30, 12, '#3a2a22', '800 ');
    /* upper windows */
    var litS = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1];
    var i, wx, ww = 68, wh = 52, gap = 20, x0 = 24;
    for (i = 0; i < 12; i++) {
      wx = x0 + i * (ww + gap);
      if (wx + ww > W0 - 16) break;
      winPane(g, wx, 54, ww, wh, litS[i]);
    }
    /* shutter bays along the ground. Bay 3 (0-index) is the open workshop. */
    var bayY = 122, bayH = 90, bw = 86, bgap = 8, bx0 = 20;
    for (i = 0; i < 12; i++) {
      var bx = bx0 + i * (bw + bgap);
      if (bx + bw > W0 - 12) break;
      if (i === 3) {
        shutterBay(g, bx, bayY, bw, bayH, 1);
        /* workbench + a bike silhouette inside the bay */
        R(g, bx + 8, bayY + 54, 70, 14, '#4a3428', INK, 2);
        g.fillStyle = '#1a1220';
        g.beginPath();
        g.ellipse(bx + 22, bayY + 78, 10, 10, 0, 0, 7);
        g.ellipse(bx + 62, bayY + 78, 10, 10, 0, 0, 7);
        g.fill();
        g.strokeStyle = INK; g.lineWidth = 3;
        g.beginPath(); g.moveTo(bx + 22, bayY + 78); g.lineTo(bx + 40, bayY + 50);
        g.lineTo(bx + 62, bayY + 78); g.lineTo(bx + 40, bayY + 58); g.closePath(); g.stroke();
        R(g, bx + 10, bayY + 8, 66, 14, '#2a3a70', INK, 2);
        txt(g, '\u9577\u8c37', bx + 43, bayY + 15, 11, '#f0e4c8', '800 ');
      } else if (i === 7) {
        /* a residential service door among the shutters (south back way) */
        shutterBay(g, bx, bayY, bw, 20, 0);
        R(g, bx + 8, bayY + 22, bw - 16, bayH - 24, '#4a342c', INK, 3);
        R(g, bx + 14, bayY + 28, 24, 28, '#8aa0a8', INK, 2);
        R(g, bx + 44, bayY + 28, 24, 28, '#8aa0a8', INK, 2);
        ellipse(g, bx + bw - 22, bayY + 70, 3, 3, '#c4a060', INK, 1.2);
      } else {
        shutterBay(g, bx, bayY, bw, bayH, 0);
      }
    }
    g.strokeStyle = INK; g.lineWidth = 3; g.strokeRect(1, 1, W0 - 2, H0 - 2);
  };

  /* ---------- lobby 1280 x 900 ---------- */
  S2P.minaLobby = function (g) {
    var RW = 1280, RH = 900; rr(g);
    tiles(g, 90, 230, RW - 180, 620, '#8a8490', '#7a7480', 52);
    /* a worn runner down the middle, not random scuff-blobs */
    g.fillStyle = 'rgba(70,40,48,.28)';
    g.fillRect(560, 360, 160, 480);
    g.fillStyle = 'rgba(90,50,58,.12)';
    for (var ry = 370; ry < 820; ry += 36) g.fillRect(568, ry, 144, 4);
    /* wall */
    R(g, 90, 0, RW - 180, 230, '#c4b49a', 0);
    plank(g, 90, 168, RW - 180, 62, '#6a5040', '#5c4638', 48);
    R(g, 90, 0, RW - 180, 18, '#3a2a22', 0);
    R(g, 90, 220, RW - 180, 12, '#3a2a22', 0);
    function pend(lx) {
      g.strokeStyle = INK; g.lineWidth = 2;
      g.beginPath(); g.moveTo(lx, 18); g.lineTo(lx, 70); g.stroke();
      R(g, lx - 28, 70, 56, 10, '#3a2a22', INK, 2);
      glow(g, lx, 120, 90, 'rgba(255,200,130,.28)');
      ellipse(g, lx, 92, 22, 16, '#f0d4a0', INK, 2);
      g.fillStyle = 'rgba(255,255,230,.35)'; g.beginPath(); g.ellipse(lx - 6, 88, 7, 6, 0, 0, 7); g.fill();
    }
    pend(280); pend(640); pend(1000);
    /* mailboxes */
    R(g, 120, 250, 260, 210, '#3a3e48', INK, 3);
    txt(g, '\u90f5\u4fbf\u7bb1', 250, 268, 13, '#efe4c8', '800 ');
    var r, c;
    for (r = 0; r < 4; r++) for (c = 0; c < 5; c++) {
      var mx = 132 + c * 48, my = 282 + r * 42;
      R(g, mx, my, 42, 36, (r + c) % 2 ? '#d8c8a8' : '#c8b898', INK, 1.8);
      R(g, mx + 6, my + 8, 18, 8, '#efe8d8', INK, 1);
      ellipse(g, mx + 32, my + 22, 3, 3, '#8a6a30', INK, 1);
      if ((r === 1 && c === 2) || (r === 3 && c === 0) || (r === 0 && c === 4)) {
        R(g, mx + 4, my + 18, 22, 16, '#f4ead2', INK, 1);
      }
    }
    /* a dropped flyer on the floor */
    R(g, 180, 480, 28, 18, '#f4ead2', INK, 1.4);
    /* notice board with pins */
    R(g, 400, 250, 200, 150, '#6a4430', INK, 3);
    R(g, 408, 258, 184, 134, '#c4a878', INK, 2);
    txt(g, 'NOTICE', 500, 276, 11, '#5a2a28', '800 ');
    R(g, 420, 292, 70, 40, '#f4ead2', INK, 1.4);
    R(g, 500, 292, 78, 28, '#f4ead2', INK, 1.4);
    R(g, 420, 340, 150, 36, '#efe4c8', INK, 1.4);
    txt(g, '\u81ea\u8ee2\u8eca\u7981\u6b62', 495, 358, 11, '#5a2a28', '700 ');
    ellipse(g, 428, 296, 2, 2, '#8a2a28', 0);
    ellipse(g, 508, 296, 2, 2, '#8a2a28', 0);
    /* landlady desk, right of the notice board */
    R(g, 620, 300, 200, 18, '#6b4a33', INK, 3);
    R(g, 620, 318, 200, 70, '#5c3e2a', INK, 3);
    ellipse(g, 650, 296, 12, 8, '#f4ead2', INK, 1.8);
    R(g, 700, 286, 50, 14, '#efe4c8', INK, 1.6);
    txt(g, '\u68ee', 725, 293, 10, '#5a2a28', '800 ');
    /* sofa */
    R(g, 140, 600, 240, 28, '#5a3048', INK, 3);
    R(g, 140, 628, 240, 50, '#4a283c', INK, 3);
    R(g, 130, 560, 36, 90, '#5a3048', INK, 3);
    R(g, 354, 560, 36, 90, '#5a3048', INK, 3);
    R(g, 176, 572, 90, 18, '#6a4058', INK, 2);
    R(g, 270, 572, 80, 18, '#6a4058', INK, 2);
    g.fillStyle = 'rgba(90,40,50,.3)';
    g.beginPath(); g.ellipse(260, 700, 140, 22, 0, 0, 7); g.fill();
    /* plant */
    R(g, 420, 640, 44, 40, '#a0582e', INK, 2);
    ['#2f6b3a', '#3f8a4a', '#2a5a33'].forEach(function (col, i) {
      for (var k = 0; k < 4; k++) {
        var a = -Math.PI / 2 + (k - 1.5) * 0.5 + i * 0.1;
        g.beginPath(); g.ellipse(442 + Math.cos(a) * 22, 620 + Math.sin(a) * 20, 8, 18, a + 1.2, 0, 7);
        g.fillStyle = col; g.fill(); g.strokeStyle = INK; g.lineWidth = 1.5; g.stroke();
      }
    });
    /* umbrella stand + shoes */
    R(g, 500, 660, 28, 36, '#3a3e48', INK, 2);
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(510, 658); g.lineTo(504, 620); g.moveTo(516, 658); g.lineTo(524, 624); g.stroke();
    R(g, 540, 688, 22, 10, '#3a2a22', INK, 1.5);
    R(g, 568, 688, 20, 10, '#5a3040', INK, 1.5);
    /* stair door — Residents only */
    R(g, 880, 248, 210, 300, '#3a2a22', INK, 4);
    R(g, 894, 262, 182, 268, '#5c4030', INK, 3);
    R(g, 954, 286, 54, 170, '#1a1520', INK, 2);
    g.fillStyle = 'rgba(80,70,60,.35)';
    g.beginPath(); g.moveTo(962, 444); g.lineTo(1000, 300); g.lineTo(1000, 444); g.closePath(); g.fill();
    g.strokeStyle = 'rgba(200,190,170,.28)'; g.lineWidth = 2;
    for (var st = 0; st < 6; st++) { g.beginPath(); g.moveTo(962, 436 - st * 22); g.lineTo(992, 414 - st * 24); g.stroke(); }
    ellipse(g, 1058, 420, 5, 5, '#c4a060', INK, 1.5);
    R(g, 914, 420, 28, 10, '#2a2018', INK, 1.5);
    R(g, 900, 248, 170, 28, '#efe4c8', INK, 2);
    txt(g, '\u4f4f\u6c11\u5c02\u7528', 985, 256, 13, '#5a2a28', '900 ');
    txt(g, 'RESIDENTS ONLY', 985, 270, 9, '#5a2a28', '700 ');
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.arc(1058, 450, 10, 0, 6.28); g.stroke();
    g.beginPath(); g.moveTo(1050, 450); g.lineTo(1028, 450); g.stroke();
    /* coffee table + mug + magazine */
    R(g, 200, 720, 130, 14, '#6b4a33', INK, 2);
    R(g, 212, 734, 10, 24, '#4a3224', INK, 2);
    R(g, 308, 734, 10, 24, '#4a3224', INK, 2);
    ellipse(g, 230, 716, 10, 7, '#f4ead2', INK, 1.8);
    R(g, 238, 708, 8, 6, '#f4ead2', INK, 1.4);
    R(g, 260, 712, 36, 16, '#8a2a28', INK, 1.4);
    /* workshop wing doorway, lower right wall — clear of the stair */
    R(g, 1088, 560, 102, 210, '#1a1520', INK, 3);
    glow(g, 1088, 660, 90, 'rgba(255,180,80,.22)');
    R(g, 1096, 640, 70, 16, '#5c4638', 0);
    ellipse(g, 1160, 720, 22, 10, '#1a1220', 0);
    R(g, 1094, 568, 90, 16, '#2a3a70', INK, 2);
    txt(g, '\u6574\u5099', 1138, 576, 11, '#f0e4c8', '800 ');
    /* clock */
    ellipse(g, 820, 200, 22, 22, '#f4ead2', INK, 2.5);
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(820, 200); g.lineTo(820, 188); g.moveTo(820, 200); g.lineTo(830, 206); g.stroke();
    /* framed photo */
    R(g, 760, 250, 70, 54, '#6b4a33', INK, 2);
    R(g, 766, 256, 58, 42, '#c8b898', INK, 1.4);
    shell(g, RW, RH);
    glow(g, 280, 140, 180, 'rgba(255,190,140,.10)');
    glow(g, 640, 140, 180, 'rgba(255,190,140,.10)');
    glow(g, 1000, 140, 180, 'rgba(255,190,140,.10)');
  };

  /* ---------- workshop 1280 x 900 ---------- */
  S2P.minaShop = function (g) {
    var RW = 1280, RH = 900; rr(g);
    R(g, 90, 230, RW - 180, 620, '#6a686c', 0);
    /* organic oil blooms, seeded, not a regular chain */
    var rs = (function (v) { return function () { v = (v * 16807) % 2147483647; return (v - 1) / 2147483646; }; })(19);
    var i;
    for (i = 0; i < 14; i++) {
      var ox = 160 + rs() * 960, oy = 360 + rs() * 420, orx = 18 + rs() * 50, ory = 8 + rs() * 16;
      g.fillStyle = 'rgba(16,12,10,' + (0.16 + rs() * 0.22) + ')';
      g.beginPath(); g.ellipse(ox, oy, orx, ory, rs() * 1.2, 0, 7); g.fill();
      if (rs() < 0.5) { g.beginPath(); g.ellipse(ox + orx * 0.4, oy + 4, orx * 0.5, ory * 0.6, 0, 0, 7); g.fill(); }
    }
    g.fillStyle = 'rgba(200,140,40,.18)'; g.fillRect(90, 620, RW - 180, 10);
    /* cinder back wall */
    R(g, 90, 0, RW - 180, 230, '#4a4e58', 0);
    for (var yy = 8; yy < 230; yy += 28) {
      g.strokeStyle = 'rgba(20,20,28,.28)'; g.lineWidth = 2;
      g.beginPath(); g.moveTo(90, yy); g.lineTo(RW - 90, yy); g.stroke();
      for (var xx = 90 + ((yy / 28) % 2) * 40; xx < RW - 90; xx += 80) {
        g.beginPath(); g.moveTo(xx, yy); g.lineTo(xx, yy + 28); g.stroke();
      }
    }
    R(g, 90, 0, RW - 180, 16, '#2a2018', 0);
    R(g, 90, 218, RW - 180, 14, '#2a2018', 0);
    /* open shutter to the night street */
    R(g, 470, 30, 340, 200, '#0e121c', INK, 3);
    glow(g, 640, 160, 140, 'rgba(255,180,90,.16)');
    g.fillStyle = '#1a2240'; g.fillRect(476, 36, 328, 80);
    winPane(g, 500, 48, 44, 36, 1, 0); winPane(g, 556, 48, 44, 36, 0, 0);
    winPane(g, 612, 48, 44, 36, 1, 0); winPane(g, 668, 48, 44, 36, 1, 0);
    winPane(g, 724, 48, 44, 36, 0, 0);
    g.fillStyle = '#1a2a48'; g.fillRect(476, 140, 328, 50);
    /* boardwalk hint */
    plank(g, 476, 190, 328, 34, '#6a4a36', '#5a3c2c', 28);
    R(g, 462, 20, 356, 16, '#6a707c', INK, 2);
    function fluo(lx, col) {
      R(g, lx - 80, 24, 160, 10, '#3a3e48', INK, 2);
      R(g, lx - 74, 26, 148, 6, col, 0);
      glow(g, lx, 80, 120, col === '#d8f0c8' ? 'rgba(180,220,140,.16)' : 'rgba(220,230,240,.16)');
    }
    fluo(250, '#e8eef4'); fluo(640, '#e8eef4'); fluo(1030, '#d8f0c8');
    /* pegboard + tools */
    R(g, 120, 250, 200, 200, '#8a5a3a', INK, 3);
    for (var py = 262; py < 440; py += 16) for (var px = 132; px < 308; px += 16) ellipse(g, px, py, 1.6, 1.6, '#2a2018', 0);
    g.strokeStyle = INK; g.lineWidth = 4; g.lineCap = 'round';
    g.beginPath(); g.moveTo(160, 280); g.lineTo(160, 360); g.stroke();
    R(g, 148, 360, 24, 10, '#8a8fa0', INK, 1.5);
    g.beginPath(); g.arc(210, 320, 16, 0.2, 6); g.stroke();
    R(g, 206, 300, 8, 40, '#8a8fa0', INK, 1.5);
    R(g, 240, 280, 8, 50, '#c4a060', INK, 1.5);
    R(g, 260, 290, 30, 8, '#3a3e48', INK, 1.5);
    ['#c45a3a', '#3a6a8a', '#c4a030', '#4a6a3a'].forEach(function (col, n) {
      R(g, 130 + n * 46, 470, 42, 36, col, INK, 2);
    });
    /* the bike, mid floor */
    moto(g, 380, 500, 1.15);
    /* creeper / jack */
    R(g, 300, 700, 80, 14, '#3a3e48', INK, 2);
    ellipse(g, 308, 714, 6, 6, '#1a1220', INK, 1.5);
    ellipse(g, 372, 714, 6, 6, '#1a1220', INK, 1.5);
    /* workbench + shop counter */
    R(g, 760, 380, 360, 26, '#5c4638', INK, 3);
    R(g, 760, 406, 360, 90, '#4a3a30', INK, 3);
    R(g, 780, 360, 70, 20, '#8a8fa0', INK, 2);
    R(g, 860, 354, 16, 26, '#c4a060', INK, 2);
    ellipse(g, 910, 372, 16, 10, '#3a3e48', INK, 2);
    R(g, 940, 358, 44, 22, '#2a3a70', INK, 2);
    txt(g, '\u30c6\u30fc\u30d7', 962, 370, 9, '#f0e4c8', '800 ');
    /* engine block on the bench */
    R(g, 1000, 348, 40, 32, '#4a4e58', INK, 2);
    R(g, 1006, 342, 12, 8, '#3a3e48', INK, 1.4);
    R(g, 820, 430, 240, 50, '#2a3a70', INK, 3);
    txt(g, '\u9577\u8c37  \u6574\u5099', 940, 448, 16, '#f0e4c8', '900 ');
    txt(g, 'HASE  REPAIR', 940, 468, 11, '#d8c8a0', '700 ');
    R(g, 1080, 350, 50, 30, '#8a8fa0', INK, 2);
    /* tyre stack + oil can + rag */
    for (i = 0; i < 4; i++) ellipse(g, 200, 700 - i * 18, 36, 12, '#1a1220', INK, 2);
    R(g, 280, 680, 24, 36, '#c45a3a', INK, 2);
    ellipse(g, 292, 680, 10, 5, '#c45a3a', INK, 2);
    g.beginPath(); g.moveTo(300, 678); g.quadraticCurveTo(318, 670, 310, 690); g.strokeStyle = '#6a4a28'; g.lineWidth = 3; g.stroke();
    /* calendar + radio + a faded rider sticker */
    R(g, 1100, 250, 70, 90, '#f4ead2', INK, 2);
    R(g, 1100, 250, 70, 18, '#8a2a28', INK, 2);
    txt(g, '11', 1135, 260, 11, '#f4ead2', '800 ');
    R(g, 1000, 250, 70, 36, '#2a2430', INK, 2);
    ellipse(g, 1054, 268, 8, 8, '#3a3e48', INK, 1.5);
    R(g, 1010, 258, 24, 8, '#8a8fa0', INK, 1);
    ellipse(g, 390, 280, 22, 22, '#2a2c34', INK, 2);
    txt(g, '\u9a0e', 390, 280, 12, '#c07040', '900 ');
    /* lobby door */
    R(g, 120, 80, 80, 140, '#4a342c', INK, 3);
    ellipse(g, 186, 160, 4, 4, '#c4a060', INK, 1.2);
    txt(g, '\u30ed\u30d3\u30fc', 160, 70, 10, '#efe4c8', '700 ');
    /* stool */
    R(g, 700, 500, 8, 40, '#3b2a22', INK, 2);
    ellipse(g, 704, 500, 20, 8, '#c4a060', INK, 2);
    shell(g, RW, RH);
  };

  /* ---------- battle: east canal bridge, 720 x 1280 ---------- */
  S2P.battleBridge = function (g) {
    var H = (typeof window !== 'undefined' && window.FFF_C2H) || (typeof root !== 'undefined' && root.FFF_C2H);
    var WD = 720, HT = 1280, H0 = 330, x = g;
    rr(g);
    if (!H) { g.fillStyle = '#101828'; g.fillRect(0, 0, WD, HT); return; }
    H.sky(x, '#101428', '#243050', 40);
    glow(g, 600, 70, 70, 'rgba(200,210,240,.18)');
    ellipse(g, 600, 70, 22, 22, '#dce4f0', 0);
    /* far bank + boat house */
    H.R(x, 0, 200, WD, 130, '#1a2030', 0);
    H.poly(x, [[400, 240], [710, 240], [710, 330], [390, 330], [390, 260]], '#1c2436', H.INK, 2);
    H.R(x, 460, 220, 170, 22, '#2a2018', H.INK, 2);
    H.txt(x, '\u8239\u5c0b', 545, 231, 11, '#d8c8a0');
    H.poly(x, [[490, 292], [690, 292], [710, 318], [480, 320]], '#c8c0b4', H.INK, 2);
    H.R(x, 550, 268, 74, 24, '#8a4030', H.INK, 2);
    /* Minato-sō */
    H.bricks(x, 430, 128, 310, 202, '#4a382c', 'rgba(20,12,16,.35)');
    H.R(x, 430, 128, 310, 16, '#2a2018', H.INK, 2);
    var lit = [1, 0, 1, 1, 0, 0, 1, 0, 1];
    var i, j;
    for (j = 0; j < 3; j++) for (i = 0; i < 5; i++) {
      H.win(x, 448 + i * 56, 156 + j * 46, 40, 32, !!lit[(j * 3 + i) % lit.length], 2);
    }
    H.R(x, 500, 136, 140, 16, '#f0e4c8', H.INK, 2);
    H.txt(x, '\u6e2f\u8358', 570, 144, 12, '#5a2a28');
    /* left warehouse */
    H.R(x, -20, 150, 200, 180, '#2a3048', H.INK, 3);
    H.shutter(x, 20, 210, 130, 120, '#7d8290');
    H.R(x, 36, 170, 100, 22, '#1a1520', H.INK, 2);
    H.txt(x, '\u5009', 86, 181, 12, '#d8c8a0');
    /* canal under the wall, both sides, with a wet lip */
    H.R(x, 0, H0 - 18, WD, 18, '#3a2a22', H.INK, 2);
    g.fillStyle = '#152038'; g.fillRect(0, H0, 86, 56); g.fillRect(WD - 86, H0, 86, 56);
    g.fillStyle = 'rgba(80,140,200,.2)'; g.fillRect(0, H0, 86, 56); g.fillRect(WD - 86, H0, 86, 56);
    g.strokeStyle = 'rgba(160,200,230,.25)'; g.lineWidth = 2;
    g.beginPath(); g.moveTo(0, H0 + 24); g.quadraticCurveTo(40, H0 + 32, 86, H0 + 20); g.stroke();
    g.beginPath(); g.moveTo(WD - 86, H0 + 20); g.quadraticCurveTo(WD - 40, H0 + 32, WD, H0 + 24); g.stroke();
    /* wet asphalt */
    H.floor(x, { kind: 'asphalt', far: '#2a2c38', near: '#1a1c26', line: 'rgba(255,255,255,.06)', seed: 11, lanes: [360], paint: 'rgba(220,200,90,.5)' });
    puddles(g, H, H0);
    /* subtle grate, mid-deck only, fading out */
    g.save();
    g.beginPath(); g.rect(80, 680, 560, 200); g.clip();
    g.strokeStyle = 'rgba(140,150,170,.18)'; g.lineWidth = 1.6;
    for (i = 0; i < 14; i++) { g.beginPath(); g.moveTo(H.fx0(-40 + i * 70, 680), 680); g.lineTo(H.fx0(-40 + i * 70, 880), 880); g.stroke(); }
    for (j = 0; j < 6; j++) { var y = 680 + j * 32; g.beginPath(); g.moveTo(80, y); g.lineTo(640, y); g.stroke(); }
    g.restore();
    /* rails */
    function rail(X0, X1) {
      g.strokeStyle = INK; g.lineWidth = 5;
      g.beginPath(); g.moveTo(H.fx0(X0, H0 + 8), H0 + 8); g.lineTo(H.fx0(X0, 860), 860); g.stroke();
      g.beginPath(); g.moveTo(H.fx0(X1, H0 + 8), H0 + 8); g.lineTo(H.fx0(X1, 860), 860); g.stroke();
      g.strokeStyle = '#8a909c'; g.lineWidth = 3;
      g.beginPath(); g.moveTo(H.fx0(X0, H0 + 8), H0 + 8); g.lineTo(H.fx0(X0, 860), 860); g.stroke();
      g.beginPath(); g.moveTo(H.fx0(X1, H0 + 8), H0 + 8); g.lineTo(H.fx0(X1, 860), 860); g.stroke();
      for (var k = 0; k < 6; k++) {
        var yy = H0 + 24 + k * 90;
        g.beginPath(); g.moveTo(H.fx0(X0, yy), yy); g.lineTo(H.fx0(X1, yy), yy);
        g.strokeStyle = INK; g.lineWidth = 4; g.stroke();
        g.strokeStyle = '#8a909c'; g.lineWidth = 2; g.stroke();
      }
    }
    rail(-20, 90); rail(630, 740);
    function lamp(X, Y) {
      H.R(x, X - 6, Y - 140, 12, 140, '#3a3e48', H.INK, 2);
      H.R(x, X - 22, Y - 150, 50, 16, '#2a2c34', H.INK, 2);
      glow(g, X, Y - 120, 80, 'rgba(255,190,90,.35)');
      H.R(x, X - 16, Y - 146, 38, 10, '#f0d080', 0);
    }
    lamp(130, H0 + 4); lamp(590, H0 + 4);
    H.wet(x, [[130, 0, 60, '255,190,100', 0.36], [590, 0, 60, '255,190,100', 0.36], [360, 0, 40, '200,210,230', 0.12]], 0.62);
    /* freight crate */
    var cy = 500, cx = 130;
    H.R(x, cx, cy, 96, 70, '#8a4a28', H.INK, 3);
    H.R(x, cx + 8, cy + 10, 80, 22, '#6a3418', H.INK, 2);
    H.txt(x, '\u8ca0\u7269', cx + 48, cy + 21, 11, '#f0e4c8');
    H.R(x, cx + 14, cy + 40, 28, 16, '#2a2018', 0);
    H.R(x, cx + 54, cy + 40, 28, 16, '#2a2018', 0);
    /* parked bike */
    moto(g, 470, 560, 0.95);
    /* cone + chain */
    H.poly(x, [[200, 740], [214, 690], [228, 740]], '#d4782a', H.INK, 2);
    H.R(x, 200, 738, 28, 8, '#2a2018', H.INK, 1.5);
    g.strokeStyle = '#c4a060'; g.lineWidth = 3;
    g.beginPath(); g.moveTo(228, 730); g.quadraticCurveTo(300, 760, 380, 730); g.stroke();
    ellipse(g, 360, 820, 36, 14, '#3a3e48', INK, 2);
    g.strokeStyle = 'rgba(0,0,0,.35)'; g.lineWidth = 1.5;
    g.beginPath(); g.ellipse(360, 820, 20, 7, 0, 0, 7); g.stroke();
    rain(g, H, 50, 3);
    H.vign(x, 0.62);
    H.grade(x, 'rgba(40,50,90,.2)', 'rgba(20,10,20,.25)');
  };

  /* ---------- battle: SE street in front of Minato-sō, 720 x 1280 ---------- */
  S2P.battleSE = function (g) {
    var H = (typeof window !== 'undefined' && window.FFF_C2H) || (typeof root !== 'undefined' && root.FFF_C2H);
    var WD = 720, HT = 1280, H0 = 330, x = g;
    rr(g);
    if (!H) { g.fillStyle = '#141220'; g.fillRect(0, 0, WD, HT); return; }
    H.sky(x, '#12101c', '#2a2438', 36);
    /* south façade */
    plank(g, 0, 110, WD, 220, '#5a4034', '#4e372c', 46);
    H.R(x, 0, 110, WD, 16, '#2a2018', H.INK, 2);
    H.R(x, 240, 122, 240, 28, '#f0e4c8', H.INK, 3);
    H.txt(x, '\u6e2f\u8358', 320, 136, 16, '#5a2a28');
    H.txt(x, 'MINATO-S\u014c', 430, 136, 11, '#3a2a22');
    var lit = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1];
    var i;
    for (i = 0; i < 10; i++) H.win(x, 18 + i * 70, 160, 52, 44, !!lit[i], 2);
    for (i = 0; i < 7; i++) {
      if (i === 2) {
        H.R(x, 16 + i * 100, 220, 92, 110, '#1a1520', H.INK, 3);
        glow(g, 16 + i * 100 + 46, 260, 70, 'rgba(255,180,90,.32)');
        H.R(x, 16 + i * 100 + 10, 228, 72, 14, '#2a3a70', H.INK, 2);
        H.txt(x, '\u9577\u8c37', 16 + i * 100 + 46, 235, 11, '#f0e4c8');
        moto(g, 28 + i * 100, 268, 0.42);
      } else {
        H.shutter(x, 16 + i * 100, 220, 92, 110, '#8a8fa0');
      }
    }
    /* cat on a shutter lip, left of the lamp */
    g.fillStyle = '#1a1220';
    g.beginPath(); g.ellipse(520, 214, 10, 6, 0, 0, 7); g.fill();
    g.beginPath(); g.moveTo(512, 210); g.lineTo(514, 200); g.lineTo(518, 210); g.fill();
    g.beginPath(); g.moveTo(522, 210); g.lineTo(526, 200); g.lineTo(528, 210); g.fill();
    /* boardwalk */
    H.floor(x, { kind: 'board', far: '#6a4a36', near: '#3a2a20', line: 'rgba(20,10,8,.28)', seed: 9, cols: 8, rows: 16 });
    puddles(g, H, H0);
    /* canal on the right with pilings, a tyre fender, ripples */
    H.poly(x, [[580, H0], [WD, H0], [WD, HT], [660, HT]], '#152038', 0);
    g.fillStyle = 'rgba(80,140,200,.12)'; g.fillRect(600, H0, 120, HT - H0);
    g.strokeStyle = 'rgba(160,200,230,.18)'; g.lineWidth = 2;
    for (i = 0; i < 10; i++) {
      var yy = H0 + 40 + i * 90;
      g.beginPath(); g.moveTo(600, yy); g.quadraticCurveTo(660, yy + 8, 720, yy); g.stroke();
    }
    /* pilings */
    H.R(x, 600, H0 + 20, 16, 80, '#4a3020', H.INK, 2);
    H.R(x, 600, H0 + 220, 16, 100, '#4a3020', H.INK, 2);
    H.R(x, 600, H0 + 480, 16, 120, '#4a3020', H.INK, 2);
    ellipse(g, 608, H0 + 200, 14, 10, '#1a1220', INK, 2);
    /* bollard + rope */
    H.R(x, 568, H0 + 8, 16, 50, '#6a4030', H.INK, 2);
    ellipse(g, 576, H0 + 8, 10, 6, '#8a5a3a', INK, 2);
    g.strokeStyle = '#c4a060'; g.lineWidth = 3;
    g.beginPath(); g.moveTo(576, H0 + 20); g.quadraticCurveTo(640, H0 + 40, 608, H0 + 70); g.stroke();
    /* street lamp on the boardwalk, left of the façade, head under the windows */
    H.R(x, 114, H0 - 150, 12, 150, '#3a3e48', H.INK, 2);
    H.R(x, 98, H0 - 160, 44, 16, '#2a2c34', H.INK, 2);
    glow(g, 120, H0 - 130, 90, 'rgba(255,190,90,.32)');
    H.R(x, 104, H0 - 156, 32, 10, '#f0d080', 0);
    H.wet(x, [[120, 0, 70, '255,190,100', 0.4], [270, 0, 80, '255,180,90', 0.22], [500, 0, 40, '255,200,120', 0.18]], 0.55);
    /* leaning bike, crate, bag */
    moto(g, 70, 560, 0.9);
    H.R(x, 400, 700, 70, 50, '#7a4a28', H.INK, 3);
    H.R(x, 408, 708, 54, 14, '#5a3418', 0);
    H.R(x, 430, 640, 36, 28, '#2a3a70', H.INK, 2);
    H.R(x, 438, 632, 20, 10, '#1a1520', INK, 1.5);
    rain(g, H, 50, 4);
    H.vign(x, 0.6);
    H.grade(x, 'rgba(60,40,30,.15)', 'rgba(10,8,16,.3)');
  };

  /* ---------- tenant line cards (held vs taken) ---------- */
  S2P.lineCard = function (g, who, phase) {
    /* 900 x 420 */
    var W = 900, H = 420; rr(g);
    R(g, 0, 0, W, H, '#1a1520', 0);
    R(g, 8, 8, W - 16, H - 16, '#2a2230', INK, 3);
    var title = { mori: 'Mori-san, the landlady', nao: 'Nao, night shift', haru: 'Haru, from upstairs', hase: 'Hase, the mechanic' };
    var held = {
      mori: 'They roll the bikes through at two in the morning. I asked the tall one to stop. He laughed.',
      nao: 'I get in at one and the street is still shaking. I just want to sleep before the next shift.',
      haru: 'Mum says stay off the stairs when the bikes come. I can hear them from the lobby.',
      hase: 'I fix what they break. That is the deal, as long as they hold the block.'
    };
    var taken = {
      mori: 'The street slept last night. First time in a month. Come in. The kettle is on.',
      nao: 'I walked home and it was quiet. Thank you. I can keep the day job if the nights stay like this.',
      haru: 'The bikes did not come. Can I sit on the sofa now? Mori-san said maybe.',
      hase: 'They are gone. I am still here. Parts, tape, a cheap patch. Nails prices, if that is the deal.'
    };
    txt(g, (title[who] || who) + '  \u00b7  ' + (phase === 'taken' ? 'after the block flips' : 'while the Riders hold it'), 450, 40, 18, '#f0e4c8', '800 ');
    var body = (phase === 'taken' ? taken : held)[who] || '';
    /* wrap */
    g.font = '700 20px "Noto Sans CJK JP",Georgia,serif';
    g.fillStyle = '#efe4d0'; g.textAlign = 'left'; g.textBaseline = 'top';
    var words = body.split(' '), line = '', y = 90, maxW = 820;
    for (var i = 0; i < words.length; i++) {
      var test = line ? line + ' ' + words[i] : words[i];
      if (g.measureText(test).width > maxW) { g.fillText(line, 40, y); y += 32; line = words[i]; }
      else line = test;
    }
    if (line) g.fillText(line, 40, y);
    txt(g, phase === 'taken' ? 'TAKEN' : 'RIDER-HELD', 820, 380, 14, phase === 'taken' ? '#c07070' : '#8aa0c8', '900 ', 'right');
  };
})(typeof window !== 'undefined' ? window : this);
