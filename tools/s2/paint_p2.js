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
    /* indoor concrete — warm grey, scored joints, not a wet street */
    R(g, 90, 230, RW - 180, 620, '#9a9488', 0);
    var rs = (function (v) { return function () { v = (v * 16807) % 2147483647; return (v - 1) / 2147483646; }; })(19);
    var i, j, xx, yy;
    g.fillStyle = 'rgba(255,248,230,.07)';
    for (i = 0; i < 220; i++) g.fillRect(100 + rs() * 1060, 240 + rs() * 600, 3 + rs() * 6, 2);
    g.fillStyle = 'rgba(40,32,24,.06)';
    for (i = 0; i < 180; i++) g.fillRect(100 + rs() * 1060, 240 + rs() * 600, 4 + rs() * 8, 2);
    /* expansion joints */
    g.strokeStyle = 'rgba(255,255,255,.14)'; g.lineWidth = 2;
    for (xx = 170; xx < 1190; xx += 110) { g.beginPath(); g.moveTo(xx, 230); g.lineTo(xx, 850); g.stroke(); }
    for (yy = 310; yy < 850; yy += 90) { g.beginPath(); g.moveTo(90, yy); g.lineTo(1190, yy); g.stroke(); }
    g.strokeStyle = 'rgba(30,24,18,.12)'; g.lineWidth = 1.5;
    for (xx = 170; xx < 1190; xx += 110) { g.beginPath(); g.moveTo(xx + 2, 230); g.lineTo(xx + 2, 850); g.stroke(); }
    for (yy = 310; yy < 850; yy += 90) { g.beginPath(); g.moveTo(90, yy + 2); g.lineTo(1190, yy + 2); g.stroke(); }
    /* a few work-area oil stains only (not a puddle carpet) */
    [[420, 620, 44, 16, 0.28], [390, 650, 28, 11, 0.2], [700, 560, 36, 14, 0.24], [640, 590, 22, 9, 0.18], [860, 610, 30, 12, 0.2]].forEach(function (o) {
      g.fillStyle = 'rgba(28,18,10,' + o[4] + ')';
      g.beginPath(); g.ellipse(o[0], o[1], o[2], o[3], 0.4, 0, 7); g.fill();
      g.fillStyle = 'rgba(90,60,20,.12)';
      g.beginPath(); g.ellipse(o[0] + 6, o[1] + 2, o[2] * 0.45, o[3] * 0.5, 0.2, 0, 7); g.fill();
    });
    /* cinder back wall */
    R(g, 90, 0, RW - 180, 230, '#5a5860', 0);
    for (yy = 8; yy < 230; yy += 28) {
      g.strokeStyle = 'rgba(20,20,28,.28)'; g.lineWidth = 2;
      g.beginPath(); g.moveTo(90, yy); g.lineTo(RW - 90, yy); g.stroke();
      for (xx = 90 + ((yy / 28) % 2) * 40; xx < RW - 90; xx += 80) {
        g.beginPath(); g.moveTo(xx, yy); g.lineTo(xx, yy + 28); g.stroke();
      }
    }
    R(g, 90, 0, RW - 180, 16, '#2a2018', 0);
    R(g, 90, 218, RW - 180, 14, '#2a2018', 0);
    /* open shutter to the night street */
    R(g, 430, 30, 300, 200, '#0e121c', INK, 3);
    glow(g, 580, 160, 130, 'rgba(255,180,90,.16)');
    g.fillStyle = '#1a2240'; g.fillRect(436, 36, 288, 80);
    winPane(g, 456, 48, 40, 36, 1, 0); winPane(g, 508, 48, 40, 36, 0, 0);
    winPane(g, 560, 48, 40, 36, 1, 0); winPane(g, 612, 48, 40, 36, 1, 0);
    winPane(g, 664, 48, 40, 36, 0, 0);
    g.fillStyle = '#1a2a48'; g.fillRect(436, 140, 288, 50);
    plank(g, 436, 190, 288, 34, '#6a4a36', '#5a3c2c', 28);
    R(g, 422, 20, 316, 16, '#6a707c', INK, 2);
    function fluo(lx, col) {
      R(g, lx - 80, 24, 160, 10, '#3a3e48', INK, 2);
      R(g, lx - 74, 26, 148, 6, col, 0);
      glow(g, lx, 80, 120, col === '#d8f0c8' ? 'rgba(180,220,140,.16)' : 'rgba(220,230,240,.14)');
    }
    fluo(220, '#e8eef4'); fluo(580, '#e8eef4'); fluo(980, '#d8f0c8');
    /* lobby door */
    R(g, 120, 80, 80, 140, '#4a342c', INK, 3);
    ellipse(g, 186, 160, 4, 4, '#c4a060', INK, 1.2);
    txt(g, '\u30ed\u30d3\u30fc', 160, 70, 10, '#efe4c8', '700 ');
    /* ---- pegboard / tool wall, left, in frame ---- */
    R(g, 120, 250, 210, 210, '#7a4a2e', INK, 3);
    R(g, 128, 258, 194, 194, '#8a5a38', 0);
    for (yy = 270; yy < 440; yy += 16) for (xx = 140; xx < 310; xx += 16) ellipse(g, xx, yy, 1.6, 1.6, '#2a2018', 0);
    g.lineCap = 'round'; g.lineJoin = 'round';
    function hook(hx, hy, w, h, col) { R(g, hx, hy, w, h, col, INK, 1.5); }
    /* wrenches */
    g.strokeStyle = INK; g.lineWidth = 5;
    g.beginPath(); g.moveTo(155, 280); g.lineTo(155, 365); g.stroke();
    R(g, 143, 360, 24, 12, '#8a8fa0', INK, 1.5);
    g.beginPath(); g.moveTo(185, 290); g.lineTo(185, 350); g.stroke();
    ellipse(g, 185, 286, 8, 6, '#8a8fa0', INK, 1.4);
    /* hammer */
    hook(214, 292, 9, 54, '#c4a060');
    R(g, 204, 284, 28, 12, '#6a707c', INK, 1.5);
    /* screwdriver + mallet */
    hook(250, 288, 6, 58, '#c45a3a');
    R(g, 246, 280, 14, 10, '#8a8fa0', INK, 1.2);
    hook(278, 300, 14, 40, '#6a4a28');
    R(g, 270, 290, 30, 14, '#3a3e48', INK, 1.4);
    /* pliers */
    g.strokeStyle = INK; g.lineWidth = 3.5;
    g.beginPath(); g.moveTo(160, 390); g.lineTo(150, 430); g.moveTo(160, 390); g.lineTo(172, 430); g.stroke();
    /* sockets */
    [0, 1, 2, 3].forEach(function (n) { ellipse(g, 220 + n * 22, 410, 8, 8, '#6a707c', INK, 1.3); });
    /* hanging rag */
    g.beginPath(); g.moveTo(300, 280); g.quadraticCurveTo(318, 310, 296, 340); g.strokeStyle = '#6a3a28'; g.lineWidth = 7; g.stroke();
    /* ---- parts shelf under the pegboard ---- */
    R(g, 120, 470, 210, 170, '#4a3a30', INK, 3);
    [478, 530, 582].forEach(function (sy) { R(g, 126, sy, 198, 8, '#5c4638', INK, 2); });
    [['#c45a3a', 140, 500], ['#3a6a8a', 188, 500], ['#c4a030', 236, 500], ['#4a6a3a', 284, 500]].forEach(function (b) {
      R(g, b[1], b[2], 42, 28, b[0], INK, 2);
    });
    function can(cx, cy, col) {
      ellipse(g, cx, cy + 22, 14, 6, col, INK, 1.4);
      R(g, cx - 14, cy, 28, 22, col, INK, 1.4);
      ellipse(g, cx, cy, 14, 6, '#d8c8a0', INK, 1.4);
    }
    can(150, 548, '#c45a3a'); can(188, 548, '#3a4a38'); can(226, 548, '#8a8fa0');
    R(g, 260, 548, 50, 26, '#efe6d2', INK, 1.5);
    txt(g, '\u90e8\u54c1', 285, 561, 10, '#4a2a20', '800 ');
    R(g, 140, 600, 50, 22, '#2a3a70', INK, 1.5);
    R(g, 198, 598, 36, 24, '#6a707c', INK, 1.5);
    R(g, 244, 600, 60, 22, '#5a4a28', INK, 1.5);
    /* tyre stacks */
    function tires(tx, ty, n) {
      for (var k = 0; k < n; k++) {
        ellipse(g, tx, ty - k * 18, 40, 13, '#1a1220', INK, 2);
        g.strokeStyle = 'rgba(80,80,90,.5)'; g.lineWidth = 1.5;
        g.beginPath(); g.ellipse(tx, ty - k * 18, 22, 6, 0, 0, 7); g.stroke();
      }
    }
    tires(200, 760, 5);
    tires(280, 748, 4);
    /* oil drum + rag */
    R(g, 330, 700, 44, 70, '#8a2a22', INK, 2);
    ellipse(g, 352, 700, 22, 10, '#6a2018', INK, 2);
    ellipse(g, 352, 770, 22, 8, '#8a2a22', INK, 2);
    txt(g, 'OIL', 352, 736, 10, '#f0e4c8', '800 ');
    g.beginPath(); g.moveTo(374, 708); g.quadraticCurveTo(392, 700, 384, 724); g.strokeStyle = '#6a4a28'; g.lineWidth = 3; g.stroke();
    /* rubber mat + bike on a stand */
    R(g, 400, 560, 220, 90, '#2a2826', INK, 2);
    g.strokeStyle = 'rgba(255,255,255,.06)'; g.lineWidth = 2;
    for (i = 0; i < 5; i++) { g.beginPath(); g.moveTo(410, 575 + i * 16); g.lineTo(610, 575 + i * 16); g.stroke(); }
    /* bike stand */
    g.strokeStyle = INK; g.lineWidth = 4;
    g.beginPath(); g.moveTo(430, 630); g.lineTo(470, 590); g.lineTo(560, 590); g.lineTo(600, 630); g.stroke();
    moto(g, 430, 545, 1.15);
    /* creeper */
    R(g, 360, 790, 90, 16, '#3a3e48', INK, 2);
    ellipse(g, 370, 806, 6, 6, '#1a1220', INK, 1.5);
    ellipse(g, 440, 806, 6, 6, '#1a1220', INK, 1.5);
    /* ---- workbench with vise + lamp, mid-right (in camera) ---- */
    R(g, 500, 380, 260, 22, '#6a5240', INK, 3);
    R(g, 508, 402, 16, 88, '#4a3a30', INK, 2);
    R(g, 736, 402, 16, 88, '#4a3a30', INK, 2);
    R(g, 500, 488, 260, 12, '#3a2e26', INK, 2);
    /* vise */
    R(g, 520, 358, 36, 24, '#6a707c', INK, 2);
    R(g, 526, 348, 10, 14, '#8a8fa0', INK, 1.5);
    R(g, 548, 352, 22, 10, '#4a4e58', INK, 1.5);
    R(g, 564, 348, 8, 18, '#c4a060', INK, 1.5);
    /* parts on the bench */
    ellipse(g, 590, 372, 16, 10, '#3a3e48', INK, 2);
    R(g, 620, 358, 44, 22, '#2a3a70', INK, 2);
    txt(g, '\u30c6\u30fc\u30d7', 642, 370, 9, '#f0e4c8', '800 ');
    R(g, 680, 350, 48, 30, '#4a4e58', INK, 2);
    R(g, 688, 344, 14, 8, '#3a3e48', INK, 1.4);
    /* desk lamp */
    g.strokeStyle = INK; g.lineWidth = 4;
    g.beginPath(); g.moveTo(730, 380); g.lineTo(730, 330); g.lineTo(700, 318); g.stroke();
    g.strokeStyle = '#8a8fa0'; g.lineWidth = 2.5;
    g.beginPath(); g.moveTo(730, 380); g.lineTo(730, 330); g.lineTo(700, 318); g.stroke();
    R(g, 722, 372, 16, 10, '#3a3e48', INK, 1.5);
    ellipse(g, 700, 322, 16, 10, '#f0d080', INK, 2);
    glow(g, 700, 360, 70, 'rgba(255,200,100,.28)');
    /* hanging work lamp over the bench */
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(630, 24); g.lineTo(630, 250); g.stroke();
    R(g, 612, 248, 36, 14, '#3a3e48', INK, 2);
    R(g, 618, 260, 24, 10, '#f0d080', 0);
    glow(g, 630, 300, 90, 'rgba(255,200,100,.22)');
    /* ---- 長谷 counter, fully in a 640-centered frame (x 760–1000) ---- */
    R(g, 760, 370, 240, 24, '#5c4638', INK, 3);
    R(g, 760, 394, 240, 100, '#3e322c', INK, 3);
    R(g, 776, 414, 208, 56, '#2a3a70', INK, 3);
    txt(g, '\u9577\u8c37  \u6574\u5099', 880, 436, 18, '#f0e4c8', '900 ');
    txt(g, 'HASE  REPAIR', 880, 458, 12, '#d8c8a0', '700 ');
    /* register + mug */
    R(g, 790, 378, 44, 16, '#2a2430', INK, 1.5);
    R(g, 794, 382, 20, 8, '#8fd6a0', INK, 1);
    ellipse(g, 960, 380, 10, 7, '#f4ead2', INK, 1.5);
    R(g, 954, 370, 12, 12, '#f4ead2', INK, 1.4);
    /* stool in front of the counter (Hase stands just left of it) */
    R(g, 700, 520, 8, 36, '#3b2a22', INK, 2);
    ellipse(g, 704, 520, 18, 7, '#c4a060', INK, 2);
    /* calendar + radio on the right wall, still in frame */
    R(g, 1020, 250, 70, 90, '#f4ead2', INK, 2);
    R(g, 1020, 250, 70, 18, '#8a2a28', INK, 2);
    txt(g, '11', 1055, 260, 11, '#f4ead2', '800 ');
    for (j = 0; j < 4; j++) for (i = 0; i < 5; i++) R(g, 1028 + i * 12, 276 + j * 14, 8, 8, '#efe6d2', INK, 0.8);
    R(g, 1020, 350, 70, 36, '#2a2430', INK, 2);
    ellipse(g, 1074, 368, 8, 8, '#3a3e48', INK, 1.5);
    R(g, 1030, 358, 24, 8, '#8a8fa0', INK, 1);
    /* rider sticker on the back wall */
    ellipse(g, 360, 280, 22, 22, '#2a2c34', INK, 2);
    txt(g, '\u9a0e', 360, 280, 12, '#c07040', '900 ');
    /* clock */
    ellipse(g, 1140, 200, 20, 20, '#f4ead2', INK, 2.2);
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(1140, 200); g.lineTo(1140, 188); g.moveTo(1140, 200); g.lineTo(1148, 206); g.stroke();
    shell(g, RW, RH);
    /* warm shop glow so the floor does not read as a night street */
    glow(g, 630, 400, 260, 'rgba(255,190,120,.08)');
    glow(g, 880, 430, 180, 'rgba(255,190,120,.06)');
  };

  S2P.battleBridge = function (g) {
    var H = (typeof window !== 'undefined' && window.FFF_C2H) || (typeof root !== 'undefined' && root.FFF_C2H);
    var WD = 720, HT = 1280, H0 = 330, x = g;
    rr(g);
    if (!H) { g.fillStyle = '#101828'; g.fillRect(0, 0, WD, HT); return; }
    var fx = H.fx0, i, j, y, uL, uR, xL, xR, ph, pw;
    H.sky(x, '#101428', '#243050', 40);
    glow(g, 600, 70, 70, 'rgba(200,210,240,.18)');
    ellipse(g, 600, 70, 22, 22, '#dce4f0', 0);
    /* far bank */
    H.R(x, 0, 200, WD, 130, '#1a2030', 0);
    /* left warehouse */
    H.R(x, -20, 150, 200, 180, '#2a3048', H.INK, 3);
    H.shutter(x, 20, 210, 130, 120, '#7d8290');
    H.R(x, 36, 170, 100, 22, '#1a1520', H.INK, 2);
    H.txt(x, '\u5009', 86, 181, 12, '#d8c8a0');
    /* boat house on the quay */
    H.poly(x, [[400, 240], [710, 240], [710, 330], [390, 330], [390, 260]], '#1c2436', H.INK, 2);
    H.R(x, 460, 220, 170, 22, '#2a2018', H.INK, 2);
    H.txt(x, '\u8239\u5c0b', 545, 231, 11, '#d8c8a0');
    H.poly(x, [[490, 292], [690, 292], [710, 318], [480, 320]], '#c8c0b4', H.INK, 2);
    H.R(x, 550, 268, 74, 24, '#8a4030', H.INK, 2);
    /* Minato-sō on the far bank */
    H.bricks(x, 430, 128, 310, 202, '#4a382c', 'rgba(20,12,16,.35)');
    H.R(x, 430, 128, 310, 16, '#2a2018', H.INK, 2);
    var lit = [1, 0, 1, 1, 0, 0, 1, 0, 1];
    for (j = 0; j < 3; j++) for (i = 0; i < 5; i++) {
      H.win(x, 448 + i * 56, 156 + j * 46, 40, 32, !!lit[(j * 3 + i) % lit.length], 2);
    }
    H.R(x, 500, 136, 140, 16, '#f0e4c8', H.INK, 2);
    H.txt(x, '\u6e2f\u8358', 570, 144, 12, '#5a2a28');
    /* stone quay lip */
    H.R(x, 0, H0 - 22, WD, 22, '#3a322c', H.INK, 2);
    g.strokeStyle = 'rgba(20,16,20,.35)'; g.lineWidth = 2;
    for (i = 0; i < 12; i++) { g.beginPath(); g.moveTo(i * 64, H0 - 22); g.lineTo(i * 64, H0); g.stroke(); }
    /* ---- canal water under and beside the deck ---- */
    g.fillStyle = H.lg(x, H0, HT, '#152038', '#0c1424');
    g.fillRect(0, H0, WD, HT - H0);
    /* soft current bands */
    g.strokeStyle = 'rgba(160,200,230,.16)'; g.lineWidth = 2;
    for (i = 0; i < 10; i++) {
      y = H0 + 28 + i * 90;
      g.beginPath(); g.moveTo(0, y); g.quadraticCurveTo(180, y + 10, 360, y); g.quadraticCurveTo(540, y - 10, 720, y + 6); g.stroke();
    }
    /* window and moon reflections in the water */
    H.streak(x, 540, H0 + 8, 36, 220, '255,190,100', 0.22);
    H.streak(x, 600, H0 + 8, 28, 180, '255,190,100', 0.16);
    H.streak(x, 488, H0 + 8, 24, 160, '255,200,120', 0.14);
    H.streak(x, 600, H0 + 4, 40, 140, '200,210,240', 0.12);
    H.pool(x, 160, 900, 70, 22, '80,140,200', 0.16);
    H.pool(x, 560, 1040, 80, 24, '80,140,200', 0.14);
    /* pilings in the side channels */
    function piling(u, y0, y1) {
      g.fillStyle = '#2a2018';
      var xa = fx(u, y0), xb = fx(u, y1), wa = 7 * (y0 - H.VP[1]) / (HT - H.VP[1]), wb = 7 * (y1 - H.VP[1]) / (HT - H.VP[1]);
      g.beginPath(); g.moveTo(xa - wa, y0); g.lineTo(xb - wb, y1); g.lineTo(xb + wb, y1); g.lineTo(xa + wa, y0); g.closePath(); g.fill();
      g.strokeStyle = INK; g.lineWidth = 2; g.stroke();
    }
    piling(40, 520, 700); piling(20, 780, 980);
    piling(700, 500, 680); piling(710, 800, 1000);
    /* tyre fender hanging off a piling */
    ellipse(g, fx(30, 860), 860, 16, 10, '#1a1220', INK, 2);
    /* ---- bridge deck: a raised roadway over the canal ---- */
    var UL = 118, UR = 602; /* world-u of the two parapets */
    function edge(u, yy) { return fx(u, yy); }
    /* deck surface */
    g.beginPath();
    g.moveTo(edge(UL, H0), H0); g.lineTo(edge(UR, H0), H0);
    g.lineTo(edge(UR, HT), HT); g.lineTo(edge(UL, HT), HT);
    g.closePath();
    g.fillStyle = H.lg(x, H0, HT, '#3a3c46', '#26242c');
    g.fill();
    /* clip deck detail to the deck polygon */
    g.save();
    g.clip();
    /* concrete grain */
    var r = H.seed(13);
    g.fillStyle = 'rgba(255,255,255,.035)';
    for (i = 0; i < 500; i++) g.fillRect(r() * WD, H0 + r() * (HT - H0), 2, 2);
    /* expansion joints across the deck */
    g.strokeStyle = 'rgba(0,0,0,.22)'; g.lineWidth = 2;
    for (j = 1; j < 12; j++) {
      y = H0 + (HT - H0) * Math.pow(j / 12, 1.45);
      g.beginPath(); g.moveTo(edge(UL, y), y); g.lineTo(edge(UR, y), y); g.stroke();
    }
    /* worn centre line, stops at the far parapet */
    for (j = 0; j < 9; j++) {
      var y1 = H0 + 36 + (HT - H0) * Math.pow(j / 10, 1.5), y2 = H0 + 36 + (HT - H0) * Math.pow((j + 0.5) / 10, 1.5);
      H.poly(x, [[fx(360 - 7, y1), y1], [fx(360 + 7, y1), y1], [fx(360 + 7, y2), y2], [fx(360 - 7, y2), y2]], 'rgba(220,200,90,.5)', 0);
    }
    /* a small drain, not a parking grate */
    ellipse(g, 360, 900, 28, 12, '#2a2c34', INK, 2);
    g.strokeStyle = 'rgba(140,150,170,.35)'; g.lineWidth = 1.4;
    for (i = -2; i <= 2; i++) { g.beginPath(); g.moveTo(360 + i * 8, 890); g.lineTo(360 + i * 8, 910); g.stroke(); }
    /* wet patches on the deck only */
    H.pool(x, 300, 620, 50, 14, '40,50,70', 0.2);
    H.pool(x, 420, 780, 40, 12, '40,50,70', 0.16);
    g.restore();
    /* deck ink outline */
    g.beginPath();
    g.moveTo(edge(UL, H0), H0); g.lineTo(edge(UL, HT), HT);
    g.moveTo(edge(UR, H0), H0); g.lineTo(edge(UR, HT), HT);
    g.strokeStyle = INK; g.lineWidth = 4; g.stroke();
    /* ---- balustrade: posts standing UP off each deck edge, plus a cap rail ---- */
    function rail(u, outer) {
      var posts = [], k, yy, x0, ht, cap = [];
      for (k = 0; k <= 14; k++) {
        yy = H0 + 8 + (HT - H0 - 8) * Math.pow(k / 14, 1.35);
        x0 = edge(u, yy);
        ht = 16 + 50 * (yy - H.VP[1]) / (HT - H.VP[1]);
        posts.push({ x: x0, y: yy, h: ht });
        cap.push([x0, yy - ht]);
      }
      /* cap rail */
      g.beginPath(); g.moveTo(cap[0][0], cap[0][1]);
      for (k = 1; k < cap.length; k++) g.lineTo(cap[k][0], cap[k][1]);
      g.strokeStyle = INK; g.lineWidth = 7; g.stroke();
      g.strokeStyle = '#8a909c'; g.lineWidth = 4; g.stroke();
      /* lower rail */
      g.beginPath();
      for (k = 0; k < posts.length; k++) {
        var ly = posts[k].y - posts[k].h * 0.45;
        if (k === 0) g.moveTo(posts[k].x, ly); else g.lineTo(posts[k].x, ly);
      }
      g.strokeStyle = INK; g.lineWidth = 4; g.stroke();
      g.strokeStyle = '#7a808c'; g.lineWidth = 2.2; g.stroke();
      /* posts */
      posts.forEach(function (p) {
        var w = Math.max(3, p.h * 0.16);
        g.fillStyle = '#6a707c';
        g.fillRect(p.x - w / 2, p.y - p.h, w, p.h);
        g.strokeStyle = INK; g.lineWidth = 2;
        g.strokeRect(p.x - w / 2, p.y - p.h, w, p.h);
        /* cap block */
        g.fillStyle = '#8a909c';
        g.fillRect(p.x - w * 0.8, p.y - p.h - 5, w * 1.6, 6);
        g.strokeStyle = INK; g.lineWidth = 1.5;
        g.strokeRect(p.x - w * 0.8, p.y - p.h - 5, w * 1.6, 6);
      });
      return posts;
    }
    var leftPosts = rail(UL, -1), rightPosts = rail(UR, 1);
    /* bridge lamps on selected posts */
    function lampOn(p) {
      var w = Math.max(4, p.h * 0.18), pole = p.h * 1.15;
      H.R(x, p.x - w / 2, p.y - p.h - pole, w, pole, '#3a3e48', H.INK, 2);
      H.R(x, p.x - 16, p.y - p.h - pole - 12, 32, 12, '#2a2c34', H.INK, 2);
      glow(g, p.x, p.y - p.h - pole + 8, 70 + p.h, 'rgba(255,190,90,.35)');
      H.R(x, p.x - 12, p.y - p.h - pole - 8, 24, 8, '#f0d080', 0);
      /* reflection in the side water, off the deck */
      H.streak(x, p.x + (p.x < 360 ? -36 : 36), p.y + 8, 22 + p.h * 0.2, 80 + p.h * 1.2, '255,190,100', 0.22);
    }
    lampOn(leftPosts[2]); lampOn(leftPosts[7]);
    lampOn(rightPosts[2]); lampOn(rightPosts[7]);
    /* wet sheen on the deck under the lamps */
    H.wet(x, [[fx(200, H0 + 40), 0, 50, '255,190,100', 0.28], [fx(520, H0 + 40), 0, 50, '255,190,100', 0.28], [360, 0, 36, '200,210,230', 0.1]], 0.5);
    /* freight crate on the deck */
    var cy = 500, cx = 200;
    H.R(x, cx, cy, 96, 70, '#8a4a28', H.INK, 3);
    H.R(x, cx + 8, cy + 10, 80, 22, '#6a3418', H.INK, 2);
    H.txt(x, '\u8ca0\u7269', cx + 48, cy + 21, 11, '#f0e4c8');
    H.R(x, cx + 14, cy + 40, 28, 16, '#2a2018', 0);
    H.R(x, cx + 54, cy + 40, 28, 16, '#2a2018', 0);
    /* parked bike on the deck */
    moto(g, 430, 560, 0.95);
    /* cone + chain on the deck */
    H.poly(x, [[260, 740], [274, 690], [288, 740]], '#d4782a', H.INK, 2);
    H.R(x, 260, 738, 28, 8, '#2a2018', H.INK, 1.5);
    g.strokeStyle = '#c4a060'; g.lineWidth = 3;
    g.beginPath(); g.moveTo(288, 730); g.quadraticCurveTo(360, 760, 430, 730); g.stroke();
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
