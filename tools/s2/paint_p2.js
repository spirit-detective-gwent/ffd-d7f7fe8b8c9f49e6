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
    /* worn stone / linoleum floor */
    tiles(g, 90, 230, RW - 180, 620, '#8a8490', '#7a7480', 52);
    /* scuffs */
    g.fillStyle = 'rgba(30,24,28,.12)';
    for (var s = 0; s < 18; s++) {
      g.beginPath(); g.ellipse(180 + (s * 173) % 980, 400 + (s * 97) % 380, 24 + (s % 5) * 6, 8, 0.2, 0, 7); g.fill();
    }
    /* wall: warm plaster, darker wainscot */
    R(g, 90, 0, RW - 180, 230, '#c4b49a', 0);
    plank(g, 90, 168, RW - 180, 62, '#6a5040', '#5c4638', 48);
    R(g, 90, 0, RW - 180, 18, '#3a2a22', 0);
    R(g, 90, 220, RW - 180, 12, '#3a2a22', 0);
    /* pendant lamps */
    function pend(lx) {
      g.strokeStyle = INK; g.lineWidth = 2;
      g.beginPath(); g.moveTo(lx, 18); g.lineTo(lx, 70); g.stroke();
      R(g, lx - 28, 70, 56, 10, '#3a2a22', INK, 2);
      glow(g, lx, 120, 90, 'rgba(255,200,130,.28)');
      ellipse(g, lx, 92, 22, 16, '#f0d4a0', INK, 2);
      g.fillStyle = 'rgba(255,255,230,.35)'; g.beginPath(); g.ellipse(lx - 6, 88, 7, 6, 0, 0, 7); g.fill();
    }
    pend(280); pend(640); pend(1000);
    /* mailboxes, left wall */
    R(g, 120, 250, 260, 210, '#3a3e48', INK, 3);
    txt(g, '\u90f5\u4fbf\u7bb1', 250, 268, 13, '#efe4c8', '800 ');
    var r, c;
    for (r = 0; r < 4; r++) for (c = 0; c < 5; c++) {
      var mx = 132 + c * 48, my = 282 + r * 42;
      R(g, mx, my, 42, 36, (r + c) % 2 ? '#d8c8a8' : '#c8b898', INK, 1.8);
      R(g, mx + 6, my + 8, 18, 8, '#efe8d8', INK, 1);
      ellipse(g, mx + 32, my + 22, 3, 3, '#8a6a30', INK, 1);
      /* a couple overflowing flyers */
      if ((r === 1 && c === 2) || (r === 3 && c === 0)) {
        R(g, mx + 4, my + 20, 20, 14, '#f4ead2', INK, 1);
      }
    }
    /* notice board */
    R(g, 400, 250, 200, 150, '#6a4430', INK, 3);
    R(g, 408, 258, 184, 134, '#c4a878', INK, 2);
    txt(g, 'NOTICE', 500, 276, 11, '#5a2a28', '800 ');
    R(g, 420, 292, 70, 40, '#f4ead2', INK, 1.4);
    R(g, 500, 292, 78, 28, '#f4ead2', INK, 1.4);
    R(g, 420, 340, 150, 36, '#efe4c8', INK, 1.4);
    txt(g, '\u81ea\u8ee2\u8eca\u7981\u6b62', 495, 358, 11, '#5a2a28', '700 ');
    /* sofa, left-front */
    R(g, 140, 600, 240, 28, '#5a3048', INK, 3);
    R(g, 140, 628, 240, 50, '#4a283c', INK, 3);
    R(g, 130, 560, 36, 90, '#5a3048', INK, 3);
    R(g, 354, 560, 36, 90, '#5a3048', INK, 3);
    R(g, 176, 572, 90, 18, '#6a4058', INK, 2);
    R(g, 270, 572, 80, 18, '#6a4058', INK, 2);
    /* plant */
    R(g, 420, 640, 44, 40, '#a0582e', INK, 2);
    ['#2f6b3a', '#3f8a4a', '#2a5a33'].forEach(function (col, i) {
      for (var k = 0; k < 4; k++) {
        var a = -Math.PI / 2 + (k - 1.5) * 0.5 + i * 0.1;
        g.beginPath(); g.ellipse(442 + Math.cos(a) * 22, 620 + Math.sin(a) * 20, 8, 18, a + 1.2, 0, 7);
        g.fillStyle = col; g.fill(); g.strokeStyle = INK; g.lineWidth = 1.5; g.stroke();
      }
    });
    /* stair door — Residents only, does not open */
    R(g, 900, 248, 200, 280, '#3a2a22', INK, 4);
    R(g, 912, 260, 176, 250, '#5c4030', INK, 3);
    /* narrow glass with a dark stairwell */
    R(g, 970, 280, 50, 160, '#1a1520', INK, 2);
    g.fillStyle = 'rgba(80,70,60,.35)';
    g.beginPath(); g.moveTo(978, 430); g.lineTo(1012, 300); g.lineTo(1012, 430); g.closePath(); g.fill();
    /* steps hinted */
    g.strokeStyle = 'rgba(200,190,170,.25)'; g.lineWidth = 2;
    for (var st = 0; st < 6; st++) { g.beginPath(); g.moveTo(978, 420 - st * 20); g.lineTo(1000, 400 - st * 22); g.stroke(); }
    ellipse(g, 1070, 400, 5, 5, '#c4a060', INK, 1.5);
    R(g, 930, 400, 30, 10, '#2a2018', INK, 1.5); /* deadbolt plate */
    R(g, 920, 248, 160, 28, '#efe4c8', INK, 2);
    txt(g, '\u4f4f\u6c11\u5c02\u7528', 1000, 256, 13, '#5a2a28', '900 ');
    txt(g, 'RESIDENTS ONLY', 1000, 270, 9, '#5a2a28', '700 ');
    /* a chain / lock hint */
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.arc(1070, 430, 10, 0, 6.28); g.stroke();
    g.beginPath(); g.moveTo(1064, 430); g.lineTo(1040, 430); g.stroke();
    /* small table + a mug */
    R(g, 620, 640, 120, 16, '#6b4a33', INK, 2);
    R(g, 632, 656, 10, 28, '#4a3224', INK, 2);
    R(g, 718, 656, 10, 28, '#4a3224', INK, 2);
    ellipse(g, 660, 636, 10, 7, '#f4ead2', INK, 1.8);
    R(g, 668, 628, 8, 6, '#f4ead2', INK, 1.4);
    /* workshop wing doorway on the right wall, through to the shop */
    R(g, 1090, 500, 100, 200, '#1a1520', INK, 3);
    glow(g, 1090, 600, 80, 'rgba(255,180,80,.16)');
    R(g, 1094, 508, 88, 16, '#2a3a70', INK, 2);
    txt(g, '\u6574\u5099', 1138, 516, 11, '#f0e4c8', '800 ');
    /* wall clock */
    ellipse(g, 820, 200, 22, 22, '#f4ead2', INK, 2.5);
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(820, 200); g.lineTo(820, 188); g.moveTo(820, 200); g.lineTo(830, 206); g.stroke();
    /* rug under the sofa */
    g.fillStyle = 'rgba(90,40,50,.35)';
    g.beginPath(); g.ellipse(260, 700, 140, 28, 0, 0, 7); g.fill();
    shell(g, RW, RH);
    glow(g, 280, 140, 180, 'rgba(255,190,140,.10)');
    glow(g, 640, 140, 180, 'rgba(255,190,140,.10)');
    glow(g, 1000, 140, 180, 'rgba(255,190,140,.10)');
  };

  /* ---------- workshop 1280 x 900 ---------- */
  S2P.minaShop = function (g) {
    var RW = 1280, RH = 900; rr(g);
    /* concrete floor, oil blooms */
    R(g, 90, 230, RW - 180, 620, '#6a686c', 0);
    var i;
    for (i = 0; i < 40; i++) {
      g.fillStyle = 'rgba(20,16,14,' + (0.08 + (i % 5) * 0.03) + ')';
      g.beginPath(); g.ellipse(160 + (i * 211) % 980, 360 + (i * 89) % 430, 28 + (i % 7) * 8, 10 + (i % 3) * 4, 0.3, 0, 7); g.fill();
    }
    /* painted floor lane */
    g.fillStyle = 'rgba(200,140,40,.18)'; g.fillRect(90, 620, RW - 180, 10);
    /* back wall, cinder / wood */
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
    /* open shutter to the night street, centre back */
    R(g, 470, 30, 340, 200, '#0e121c', INK, 3);
    glow(g, 640, 160, 140, 'rgba(255,180,90,.16)');
    /* night hint: a window row and a canal tint */
    g.fillStyle = '#1a2240'; g.fillRect(476, 36, 328, 80);
    winPane(g, 500, 48, 44, 36, 1, 0); winPane(g, 556, 48, 44, 36, 0, 0);
    winPane(g, 612, 48, 44, 36, 1, 0); winPane(g, 668, 48, 44, 36, 1, 0);
    winPane(g, 724, 48, 44, 36, 0, 0);
    g.fillStyle = '#1a2a48'; g.fillRect(476, 140, 328, 84);
    R(g, 462, 20, 356, 16, '#6a707c', INK, 2);
    /* fluorescent lights */
    function fluo(lx, col) {
      R(g, lx - 80, 24, 160, 10, '#3a3e48', INK, 2);
      R(g, lx - 74, 26, 148, 6, col, 0);
      glow(g, lx, 80, 120, col === '#d8f0c8' ? 'rgba(180,220,140,.16)' : 'rgba(220,230,240,.16)');
    }
    fluo(250, '#e8eef4'); fluo(640, '#e8eef4'); fluo(1030, '#d8f0c8');
    /* pegboard left */
    R(g, 120, 250, 200, 200, '#8a5a3a', INK, 3);
    for (var py = 262; py < 440; py += 16) for (var px = 132; px < 308; px += 16) {
      ellipse(g, px, py, 1.6, 1.6, '#2a2018', 0);
    }
    /* hanging tools */
    g.strokeStyle = INK; g.lineWidth = 4; g.lineCap = 'round';
    g.beginPath(); g.moveTo(160, 280); g.lineTo(160, 360); g.stroke(); /* bar */
    R(g, 148, 360, 24, 10, '#8a8fa0', INK, 1.5);
    g.beginPath(); g.arc(210, 320, 16, 0.2, 6); g.stroke(); /* wrench */
    R(g, 206, 300, 8, 40, '#8a8fa0', INK, 1.5);
    R(g, 240, 280, 8, 50, '#c4a060', INK, 1.5);
    R(g, 260, 290, 30, 8, '#3a3e48', INK, 1.5);
    /* parts bins */
    ['#c45a3a', '#3a6a8a', '#c4a030', '#4a6a3a'].forEach(function (col, n) {
      R(g, 130 + n * 46, 470, 42, 36, col, INK, 2);
    });
    /* motorcycle on a stand, mid-left */
    function bike(bx, by) {
      g.fillStyle = 'rgba(0,0,0,.28)';
      g.beginPath(); g.ellipse(bx + 20, by + 86, 70, 10, 0, 0, 7); g.fill();
      ellipse(g, bx, by + 70, 22, 22, '#1a1220', INK, 3);
      ellipse(g, bx, by + 70, 12, 12, '#3a3e48', INK, 2);
      ellipse(g, bx + 110, by + 70, 22, 22, '#1a1220', INK, 3);
      ellipse(g, bx + 110, by + 70, 12, 12, '#3a3e48', INK, 2);
      g.strokeStyle = INK; g.lineWidth = 4;
      g.beginPath(); g.moveTo(bx, by + 70); g.lineTo(bx + 40, by + 30); g.lineTo(bx + 90, by + 30);
      g.lineTo(bx + 110, by + 70); g.stroke();
      R(g, bx + 36, by + 8, 58, 18, '#2a3a70', INK, 2);
      R(g, bx + 44, by + 26, 36, 22, '#2a2430', INK, 2);
      g.beginPath(); g.moveTo(bx + 90, by + 30); g.lineTo(bx + 130, by + 22); g.stroke(); /* bars */
      R(g, bx + 50, by + 70, 16, 8, '#8a8fa0', INK, 1.5); /* stand */
    }
    bike(400, 520);
    /* workbench + counter (shop) on the right */
    R(g, 760, 380, 360, 26, '#5c4638', INK, 3);
    R(g, 760, 406, 360, 90, '#4a3a30', INK, 3);
    /* tools on the bench */
    R(g, 780, 360, 70, 20, '#8a8fa0', INK, 2);
    R(g, 860, 354, 16, 26, '#c4a060', INK, 2);
    ellipse(g, 910, 372, 16, 10, '#3a3e48', INK, 2);
    R(g, 940, 358, 40, 22, '#2a3a70', INK, 2);
    txt(g, 'TAPE', 960, 370, 9, '#f0e4c8', '800 ');
    /* shop sign on the counter front */
    R(g, 820, 430, 240, 50, '#2a3a70', INK, 3);
    txt(g, '\u9577\u8c37  \u6574\u5099', 940, 448, 16, '#f0e4c8', '900 ');
    txt(g, 'HASE  REPAIR', 940, 468, 11, '#d8c8a0', '700 ');
    /* register / tin */
    R(g, 1080, 350, 50, 30, '#8a8fa0', INK, 2);
    /* tyre stack */
    for (i = 0; i < 4; i++) ellipse(g, 200, 700 - i * 18, 36, 12, '#1a1220', INK, 2);
    /* oil can */
    R(g, 280, 680, 24, 36, '#c45a3a', INK, 2);
    ellipse(g, 292, 680, 10, 5, '#c45a3a', INK, 2);
    /* calendar */
    R(g, 1100, 250, 70, 90, '#f4ead2', INK, 2);
    R(g, 1100, 250, 70, 18, '#8a2a28', INK, 2);
    txt(g, '11', 1135, 260, 11, '#f4ead2', '800 ');
    /* radio */
    R(g, 1000, 250, 70, 36, '#2a2430', INK, 2);
    ellipse(g, 1054, 268, 8, 8, '#3a3e48', INK, 1.5);
    R(g, 1010, 258, 24, 8, '#8a8fa0', INK, 1);
    /* internal door back to the lobby, left rear */
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
    /* faint moon */
    glow(g, 600, 70, 70, 'rgba(200,210,240,.18)');
    ellipse(g, 600, 70, 22, 22, '#dce4f0', 0);
    /* far bank + boat house silhouette */
    H.R(x, 0, 210, WD, 120, '#1a2030', 0);
    H.poly(x, [[420, 250], [700, 250], [700, 330], [400, 330], [400, 270]], '#1c2436', H.INK, 2);
    H.R(x, 470, 230, 160, 20, '#2a2018', H.INK, 2);
    /* a low boat */
    H.poly(x, [[500, 300], [680, 300], [700, 320], [490, 322]], '#c8c0b4', H.INK, 2);
    H.R(x, 560, 276, 70, 24, '#8a4030', H.INK, 2);
    /* Minato-sō apartments on the right, mixed windows */
    H.bricks(x, 430, 140, 310, 190, '#4a382c', 'rgba(20,12,16,.35)');
    H.R(x, 430, 140, 310, 16, '#2a2018', H.INK, 2);
    var lit = [1, 0, 1, 1, 0, 0, 1, 0, 1];
    var i, j;
    for (j = 0; j < 3; j++) for (i = 0; i < 5; i++) {
      H.win(x, 448 + i * 56, 168 + j * 46, 40, 32, !!lit[(j * 3 + i) % lit.length], 2);
    }
    H.R(x, 500, 148, 140, 16, '#f0e4c8', H.INK, 2);
    H.txt(x, '\u6e2f\u8358', 570, 156, 12, '#5a2a28');
    /* left: a warehouse wall + lamp */
    H.R(x, -20, 160, 200, 170, '#2a3048', H.INK, 3);
    H.shutter(x, 20, 220, 130, 110, '#7a8090');
    /* canal walls under the horizon */
    H.R(x, 0, H0 - 16, WD, 16, '#3a2a22', H.INK, 2);
    /* wet asphalt + lane + a hint of the grate in the mid-ground painted on the floor */
    H.floor(x, { kind: 'asphalt', far: '#2a2c38', near: '#1a1c26', line: 'rgba(255,255,255,.06)', seed: 11, lanes: [360], paint: 'rgba(220,200,90,.5)' });
    /* metal grate suggestion mid-floor (the bridge deck) */
    g.save();
    g.beginPath(); g.rect(0, 700, WD, 260); g.clip();
    g.strokeStyle = 'rgba(140,150,170,.28)'; g.lineWidth = 2;
    for (i = 0; i < 18; i++) { g.beginPath(); g.moveTo(H.fx0(-200 + i * 80, 700), 700); g.lineTo(H.fx0(-200 + i * 80, 960), 960); g.stroke(); }
    for (j = 0; j < 8; j++) {
      var y = 700 + j * 32;
      g.beginPath(); g.moveTo(0, y); g.lineTo(WD, y); g.stroke();
    }
    g.restore();
    /* water visible at the far sides, just under the wall */
    g.fillStyle = '#152038';
    g.fillRect(0, H0, 70, 40); g.fillRect(WD - 70, H0, 70, 40);
    g.fillStyle = 'rgba(80,140,200,.18)'; g.fillRect(0, H0, 70, 40); g.fillRect(WD - 70, H0, 70, 40);
    /* rails */
    function rail(X0, X1) {
      g.strokeStyle = INK; g.lineWidth = 5;
      g.beginPath(); g.moveTo(H.fx0(X0, H0 + 8), H0 + 8); g.lineTo(H.fx0(X0, 900), 900); g.stroke();
      g.beginPath(); g.moveTo(H.fx0(X1, H0 + 8), H0 + 8); g.lineTo(H.fx0(X1, 900), 900); g.stroke();
      g.strokeStyle = '#8a909c'; g.lineWidth = 3;
      g.beginPath(); g.moveTo(H.fx0(X0, H0 + 8), H0 + 8); g.lineTo(H.fx0(X0, 900), 900); g.stroke();
      g.beginPath(); g.moveTo(H.fx0(X1, H0 + 8), H0 + 8); g.lineTo(H.fx0(X1, 900), 900); g.stroke();
      for (var k = 0; k < 7; k++) {
        var yy = H0 + 20 + k * 80;
        g.beginPath(); g.moveTo(H.fx0(X0, yy), yy); g.lineTo(H.fx0(X1, yy), yy);
        g.strokeStyle = INK; g.lineWidth = 4; g.stroke();
        g.strokeStyle = '#8a909c'; g.lineWidth = 2; g.stroke();
      }
    }
    rail(-40, 80); rail(640, 760);
    /* sodium lamps */
    function lamp(X, Y) {
      H.R(x, X - 6, Y - 140, 12, 140, '#3a3e48', H.INK, 2);
      H.R(x, X - 22, Y - 150, 50, 16, '#2a2c34', H.INK, 2);
      glow(g, X, Y - 120, 80, 'rgba(255,190,90,.35)');
      H.R(x, X - 16, Y - 146, 38, 10, '#f0d080', 0);
    }
    lamp(130, H0 + 4); lamp(590, H0 + 4);
    H.wet(x, [[130, 0, 60, '255,190,100', 0.36], [590, 0, 60, '255,190,100', 0.36], [360, 0, 40, '200,210,230', 0.12]], 0.62);
    /* freight crate + a parked bike in the mid-ground */
    var cy = 520, cx = 160;
    H.R(x, cx, cy, 90, 64, '#8a4a28', H.INK, 3);
    H.R(x, cx + 6, cy + 8, 78, 20, '#6a3418', H.INK, 2);
    H.txt(x, 'FREIGHT', cx + 45, cy + 18, 9, '#f0e4c8');
    /* bike */
    var bx = 500, by = 600;
    g.fillStyle = 'rgba(0,0,0,.3)'; g.beginPath(); g.ellipse(bx + 30, by + 50, 50, 8, 0, 0, 7); g.fill();
    ellipse(g, bx, by + 40, 16, 16, '#1a1220', INK, 3);
    ellipse(g, bx + 70, by + 40, 16, 16, '#1a1220', INK, 3);
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(bx, by + 40); g.lineTo(bx + 28, by + 10); g.lineTo(bx + 58, by + 10); g.lineTo(bx + 70, by + 40); g.stroke();
    R(g, bx + 24, by - 4, 36, 12, '#2a3a70', INK, 2);
    /* manhole */
    ellipse(g, 360, 820, 36, 14, '#3a3e48', INK, 2);
    g.strokeStyle = 'rgba(0,0,0,.35)'; g.lineWidth = 1.5;
    g.beginPath(); g.ellipse(360, 820, 20, 7, 0, 0, 7); g.stroke();
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
    /* the south façade fills the horizon */
    H.R(x, -20, 110, 760, 220, '#4a362c', H.INK, 3);
    plank(g, 0, 110, WD, 220, '#5a4034', '#4e372c', 46);
    H.R(x, 0, 110, WD, 16, '#2a2018', H.INK, 2);
    H.R(x, 240, 122, 240, 28, '#f0e4c8', H.INK, 3);
    H.txt(x, '\u6e2f\u8358', 320, 136, 16, '#5a2a28');
    H.txt(x, 'MINATO-S\u014c', 430, 136, 11, '#3a2a22');
    var lit = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1];
    var i;
    for (i = 0; i < 10; i++) H.win(x, 18 + i * 70, 160, 52, 44, !!lit[i], 2);
    /* shutters + open workshop bay */
    for (i = 0; i < 7; i++) {
      if (i === 2) {
        H.R(x, 16 + i * 100, 220, 92, 110, '#1a1520', H.INK, 3);
        glow(g, 16 + i * 100 + 46, 260, 70, 'rgba(255,180,90,.32)');
        H.R(x, 16 + i * 100 + 10, 228, 72, 14, '#2a3a70', H.INK, 2);
        H.txt(x, '\u9577\u8c37', 16 + i * 100 + 46, 235, 11, '#f0e4c8');
        /* bike inside */
        ellipse(g, 40 + i * 100, 310, 10, 10, '#1a1220', INK, 2);
        ellipse(g, 80 + i * 100, 310, 10, 10, '#1a1220', INK, 2);
      } else {
        H.shutter(x, 16 + i * 100, 220, 92, 110, '#8a8fa0');
      }
    }
    /* wooden boardwalk floor */
    H.floor(x, { kind: 'board', far: '#6a4a36', near: '#3a2a20', line: 'rgba(20,10,8,.28)', seed: 9, cols: 8, rows: 16 });
    /* canal strip on the right, with a wet lip */
    H.poly(x, [[560, H0], [WD, H0], [WD, HT], [640, HT]], '#152038', 0);
    g.fillStyle = 'rgba(80,140,200,.12)'; g.fillRect(600, H0, 120, HT - H0);
    /* ripples */
    g.strokeStyle = 'rgba(160,200,230,.18)'; g.lineWidth = 2;
    for (i = 0; i < 10; i++) {
      var yy = H0 + 40 + i * 90;
      g.beginPath(); g.moveTo(600, yy); g.quadraticCurveTo(660, yy + 8, 720, yy); g.stroke();
    }
    /* bollard + rope */
    H.R(x, 580, H0 + 8, 16, 50, '#6a4030', H.INK, 2);
    ellipse(g, 588, H0 + 8, 10, 6, '#8a5a3a', INK, 2);
    /* lamp */
    H.R(x, 200, H0 - 150, 12, 150, '#3a3e48', H.INK, 2);
    H.R(x, 184, H0 - 160, 44, 16, '#2a2c34', H.INK, 2);
    glow(g, 206, H0 - 130, 90, 'rgba(255,190,90,.32)');
    H.R(x, 190, H0 - 156, 32, 10, '#f0d080', 0);
    H.wet(x, [[206, 0, 70, '255,190,100', 0.4], [270, 0, 80, '255,180,90', 0.22], [500, 0, 40, '255,200,120', 0.18]], 0.55);
    /* leaning bicycle, left */
    ellipse(g, 80, 620, 16, 16, '#1a1220', INK, 3);
    ellipse(g, 150, 624, 16, 16, '#1a1220', INK, 3);
    g.strokeStyle = INK; g.lineWidth = 3;
    g.beginPath(); g.moveTo(80, 620); g.lineTo(110, 580); g.lineTo(140, 584); g.lineTo(150, 624); g.stroke();
    R(g, 100, 568, 40, 12, '#2a3a70', INK, 2);
    /* crate */
    H.R(x, 400, 700, 70, 50, '#7a4a28', H.INK, 3);
    H.R(x, 408, 708, 54, 14, '#5a3418', 0);
    /* cat silhouette on a shutter lip */
    g.fillStyle = '#1a1220';
    g.beginPath(); g.ellipse(620, 214, 10, 6, 0, 0, 7); g.fill();
    g.beginPath(); g.moveTo(612, 210); g.lineTo(614, 200); g.lineTo(618, 210); g.fill();
    g.beginPath(); g.moveTo(622, 210); g.lineTo(626, 200); g.lineTo(628, 210); g.fill();
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
