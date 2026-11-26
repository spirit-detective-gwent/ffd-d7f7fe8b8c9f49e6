/* v6.5.63 FFF_S2P shop-menu art: hand-drawn boards and item icons for
 * Chiyo Wagashi, Hase Repair, and the depot counter. Add-only; no loops. */
(function () {
  var root = typeof window !== 'undefined' ? window : this;
  var S2P = root.FFF_S2P = root.FFF_S2P || {};
  var INK = '#1a1220';
  var FONT = '"Noto Sans CJK JP","Noto Serif CJK JP","BIZ UDPMincho",system-ui,sans-serif';
  var SERIF = '"Noto Serif CJK JP","BIZ UDPMincho","Hiragino Mincho ProN",serif';
  var GOTH = '"DotGothic16","Noto Sans CJK JP",system-ui,sans-serif';

  function R(g, x, y, w, h, f, ink, lw) {
    if (f) { g.fillStyle = f; g.fillRect(x, y, w, h); }
    if (ink !== 0) { g.strokeStyle = ink || INK; g.lineWidth = lw || 3; g.strokeRect(x, y, w, h); }
  }
  function rr(g, x, y, w, h, r, f, ink, lw) {
    r = Math.min(r || 8, w / 2, h / 2);
    g.beginPath();
    g.moveTo(x + r, y); g.lineTo(x + w - r, y); g.quadraticCurveTo(x + w, y, x + w, y + r);
    g.lineTo(x + w, y + h - r); g.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    g.lineTo(x + r, y + h); g.quadraticCurveTo(x, y + h, x, y + h - r);
    g.lineTo(x, y + r); g.quadraticCurveTo(x, y, x + r, y); g.closePath();
    if (f) { g.fillStyle = f; g.fill(); }
    if (ink !== 0) { g.strokeStyle = ink || INK; g.lineWidth = lw || 2.5; g.stroke(); }
  }
  function ellipse(g, x, y, rx, ry, f, ink, lw) {
    g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, Math.PI * 2);
    if (f) { g.fillStyle = f; g.fill(); }
    if (ink !== 0) { g.strokeStyle = ink || INK; g.lineWidth = lw == null ? 2.5 : lw; g.stroke(); }
  }
  function txt(g, s, x, y, px, col, weight, font, al) {
    g.font = (weight || '800 ') + px + 'px ' + (font || FONT);
    g.textAlign = al || 'center'; g.textBaseline = 'middle';
    g.fillStyle = col || INK; g.fillText(s, x, y);
  }
  function wood(g, x, y, w, h, c1, c2, step) {
    step = step || 22;
    g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip();
    g.fillStyle = c1; g.fillRect(x, y, w, h);
    for (var i = x, n = 0; i < x + w; i += step, n++) {
      g.fillStyle = n % 2 ? c2 : c1; g.fillRect(i, y, step - 2, h);
      g.fillStyle = 'rgba(0,0,0,.14)'; g.fillRect(i + step - 2, y, 2, h);
      g.strokeStyle = 'rgba(255,230,180,.08)'; g.lineWidth = 1;
      g.beginPath(); g.moveTo(i + 4, y); g.bezierCurveTo(i + 8, y + h * 0.4, i - 2, y + h * 0.7, i + 6, y + h); g.stroke();
    }
    g.restore();
  }
  function paperGrain(g, x, y, w, h, a) {
    g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip();
    for (var i = 0; i < 48; i++) {
      var px = x + ((i * 47) % w), py = y + ((i * 89) % h);
      g.fillStyle = 'rgba(40,20,10,' + (a || 0.04) + ')';
      g.fillRect(px, py, 2 + (i % 3), 1);
    }
    g.restore();
  }
  function stain(g, x, y, rx, ry, col) {
    g.fillStyle = col || 'rgba(40,30,16,.18)';
    g.beginPath(); g.ellipse(x, y, rx, ry, 0.3, 0, 7); g.fill();
  }

  /* ---------------- item icons (64x64 design space, scalable) ---------------- */
  var ICONS = S2P.menuIcons = {};

  ICONS.sweetroll = function (g) {
    ellipse(g, 32, 50, 26, 7, 'rgba(40,20,10,.22)', 0);
    ellipse(g, 32, 36, 26, 18, '#e8b060', INK, 2.4);
    ellipse(g, 32, 30, 22, 13, '#f3c97a', 0);
    g.beginPath(); g.ellipse(32, 30, 8, 6, 0, 0, 7);
    g.fillStyle = '#7a3a22'; g.fill(); g.strokeStyle = INK; g.lineWidth = 1.8; g.stroke();
    g.beginPath(); g.moveTo(14, 36); g.quadraticCurveTo(32, 20, 50, 36);
    g.strokeStyle = 'rgba(90,40,20,.45)'; g.lineWidth = 2; g.stroke();
    ellipse(g, 22, 28, 4, 3, 'rgba(255,255,230,.4)', 0);
  };
  ICONS.dango = function (g) {
    g.strokeStyle = INK; g.lineWidth = 3.2; g.lineCap = 'round';
    g.beginPath(); g.moveTo(32, 6); g.lineTo(32, 58); g.stroke();
    ellipse(g, 32, 16, 11, 9.5, '#f2c4cf', INK, 2);
    ellipse(g, 32, 33, 11, 9.5, '#9ec27a', INK, 2);
    ellipse(g, 32, 50, 11, 9.5, '#f4ead2', INK, 2);
    ellipse(g, 28, 14, 3, 2.4, 'rgba(255,255,255,.5)', 0);
  };
  ICONS.hojicha = function (g) {
    ellipse(g, 32, 56, 18, 5, 'rgba(40,20,10,.22)', 0);
    /* handle-less yunomi, toasted-tea brown */
    g.beginPath(); g.moveTo(16, 26); g.lineTo(14, 48); g.quadraticCurveTo(32, 58, 50, 48); g.lineTo(48, 26);
    g.closePath(); g.fillStyle = '#c4a882'; g.fill(); g.strokeStyle = INK; g.lineWidth = 2.2; g.stroke();
    /* foot ring */
    g.beginPath(); g.ellipse(32, 50, 12, 3.2, 0, 0, 7); g.fillStyle = '#a88860'; g.fill(); g.stroke();
    /* tea surface */
    g.beginPath(); g.ellipse(32, 26, 16, 5, 0, 0, 7); g.fillStyle = '#5a3a1c'; g.fill(); g.stroke();
    g.beginPath(); g.ellipse(32, 25, 10, 3, 0, 0, 7); g.fillStyle = '#7a5428'; g.fill();
    /* rim highlight */
    g.beginPath(); g.ellipse(32, 26, 16, 5, 0, Math.PI * 1.1, Math.PI * 1.85); g.strokeStyle = 'rgba(255,240,210,.45)'; g.lineWidth = 1.6; g.stroke();
    /* steam */
    g.strokeStyle = 'rgba(230,230,235,.7)'; g.lineWidth = 2; g.lineCap = 'round';
    [[22, 20], [32, 16], [42, 20]].forEach(function (p) {
      g.beginPath(); g.moveTo(p[0], p[1]); g.bezierCurveTo(p[0] - 4, p[1] - 6, p[0] + 4, p[1] - 10, p[0], p[1] - 16); g.stroke();
    });
  };
  ICONS.etape = function (g) {
    ellipse(g, 32, 50, 20, 6, 'rgba(40,20,10,.2)', 0);
    /* tape roll */
    ellipse(g, 32, 32, 22, 22, '#2a2a2e', INK, 2.4);
    ellipse(g, 32, 32, 16, 16, '#1a1a1e', INK, 1.8);
    ellipse(g, 32, 32, 8, 8, '#6a6a70', INK, 1.6);
    ellipse(g, 32, 32, 4, 4, '#c8c4b8', 0);
    /* loose end */
    g.beginPath(); g.moveTo(50, 24); g.quadraticCurveTo(58, 18, 56, 10);
    g.strokeStyle = '#2a2a2e'; g.lineWidth = 5; g.lineCap = 'butt'; g.stroke();
    g.strokeStyle = INK; g.lineWidth = 1.6; g.stroke();
    g.fillStyle = '#3a3a40'; g.fillRect(53, 8, 6, 5); g.strokeRect(53, 8, 6, 5);
  };
  ICONS.patch = function (g) {
    ellipse(g, 32, 54, 22, 5, 'rgba(40,20,10,.2)', 0);
    /* tin */
    rr(g, 10, 16, 44, 34, 5, '#c4a882', INK, 2.2);
    rr(g, 14, 20, 36, 18, 3, '#8a5a38', INK, 1.6);
    txt(g, 'PATCH', 32, 30, 7, '#f4ead2', '900 ', FONT);
    /* glue tube peeking */
    rr(g, 18, 40, 10, 14, 2, '#e8e0d0', INK, 1.5);
    g.fillStyle = '#c2410c'; g.fillRect(20, 40, 6, 5);
    /* oval patch */
    ellipse(g, 42, 46, 10, 7, '#5a3a28', INK, 1.5);
  };
  ICONS.bpart = function (g) {
    ellipse(g, 32, 54, 22, 5, 'rgba(40,20,10,.2)', 0);
    /* inner tube loop */
    g.lineWidth = 8; g.strokeStyle = '#2a2a2e';
    g.beginPath(); g.ellipse(32, 30, 20, 16, -0.2, 0, 7); g.stroke();
    g.lineWidth = 2.2; g.strokeStyle = INK; g.stroke();
    g.lineWidth = 3; g.strokeStyle = '#4a4a50';
    g.beginPath(); g.ellipse(32, 30, 14, 10, -0.2, 0, 7); g.stroke();
    /* valve */
    g.save(); g.translate(32, 14); g.rotate(-0.2);
    R(g, -3, -8, 6, 10, '#c8c4b8', INK, 1.4);
    g.restore();
    /* patch on the tube */
    ellipse(g, 46, 36, 7, 5, '#5a3a28', INK, 1.4);
  };
  ICONS.chainoil = function (g) {
    ellipse(g, 32, 56, 16, 4, 'rgba(40,20,10,.2)', 0);
    /* squeeze can */
    rr(g, 22, 14, 20, 36, 4, '#d4783a', INK, 2.2);
    R(g, 22, 22, 20, 10, '#c2410c', INK, 0);
    txt(g, 'OIL', 32, 28, 7, '#f4ead2', '900 ', FONT);
    /* cap + spout */
    R(g, 28, 8, 8, 8, '#2a2a2e', INK, 1.6);
    g.beginPath(); g.moveTo(36, 10); g.lineTo(48, 4); g.lineWidth = 3; g.strokeStyle = '#2a2a2e'; g.stroke();
    g.strokeStyle = INK; g.lineWidth = 1.4; g.stroke();
    /* drip */
    ellipse(g, 50, 8, 3, 4, '#5a3a14', INK, 1.2);
  };
  ICONS.cancoffee = function (g) {
    ellipse(g, 32, 56, 16, 5, 'rgba(40,20,10,.2)', 0);
    /* steel can */
    rr(g, 18, 10, 28, 44, 4, '#6a3a22', INK, 2.2);
    R(g, 18, 18, 28, 12, '#8a2a28', INK, 0);
    ellipse(g, 32, 12, 13, 4, '#c8c4b8', INK, 1.6);
    ellipse(g, 32, 52, 13, 4, '#4a2a18', INK, 1.6);
    txt(g, 'HOT', 32, 25, 8, '#f4ead2', '900 ', FONT);
    R(g, 22, 34, 20, 10, '#c9953b', INK, 1.4);
    /* pull tab */
    ellipse(g, 32, 12, 4, 2, '#e8e0d0', INK, 1.2);
    /* steam */
    g.strokeStyle = 'rgba(230,230,235,.55)'; g.lineWidth = 1.6;
    g.beginPath(); g.moveTo(40, 8); g.bezierCurveTo(44, 2, 36, -2, 42, -6); g.stroke();
  };
  ICONS.onigiri = function (g) {
    ellipse(g, 32, 56, 20, 5, 'rgba(40,20,10,.2)', 0);
    g.beginPath(); g.moveTo(32, 8); g.lineTo(54, 46); g.quadraticCurveTo(32, 58, 10, 46); g.closePath();
    g.fillStyle = '#f4efe6'; g.fill(); g.strokeStyle = INK; g.lineWidth = 2.2; g.stroke();
    /* nori wrap */
    g.beginPath(); g.moveTo(18, 36); g.lineTo(14, 48); g.quadraticCurveTo(32, 58, 50, 48); g.lineTo(46, 36); g.closePath();
    g.fillStyle = '#1a2420'; g.fill(); g.stroke();
    /* grain dots */
    g.fillStyle = 'rgba(90,70,50,.25)';
    [[28, 22], [36, 24], [30, 30], [38, 32]].forEach(function (p) { g.beginPath(); g.arc(p[0], p[1], 1.2, 0, 7); g.fill(); });
  };
  ICONS.ptape = function (g) {
    ellipse(g, 32, 54, 20, 5, 'rgba(40,20,10,.2)', 0);
    ellipse(g, 32, 32, 24, 24, '#d8c49a', INK, 2.4);
    ellipse(g, 32, 32, 18, 18, '#c4b080', INK, 1.6);
    ellipse(g, 32, 32, 9, 9, '#8a8fa0', INK, 1.6);
    ellipse(g, 32, 32, 5, 5, '#d8dce4', 0);
    /* loose tan end */
    g.beginPath(); g.moveTo(52, 22); g.quadraticCurveTo(62, 16, 58, 8);
    g.strokeStyle = '#d8c49a'; g.lineWidth = 6; g.stroke();
    g.strokeStyle = INK; g.lineWidth = 1.5; g.stroke();
  };
  ICONS.gauze = function (g) {
    ellipse(g, 32, 54, 18, 5, 'rgba(40,20,10,.2)', 0);
    /* roll */
    ellipse(g, 32, 30, 22, 16, '#f4efe6', INK, 2.2);
    ellipse(g, 32, 30, 14, 10, '#e8e0d0', INK, 1.5);
    ellipse(g, 32, 30, 6, 5, '#c8c4b8', INK, 1.3);
    /* loose wrap */
    g.beginPath(); g.moveTo(50, 36); g.quadraticCurveTo(58, 44, 48, 52); g.lineTo(22, 52);
    g.strokeStyle = '#f4efe6'; g.lineWidth = 7; g.lineCap = 'round'; g.stroke();
    g.strokeStyle = INK; g.lineWidth = 1.5; g.stroke();
    /* red cross */
    g.fillStyle = '#8a2a28';
    g.fillRect(30, 24, 4, 12); g.fillRect(26, 28, 12, 4);
  };

  function paintIcon(g, id, s) {
    s = s || 64;
    g.save(); g.scale(s / 64, s / 64);
    var fn = ICONS[id]; if (fn) fn(g); else { R(g, 8, 8, 48, 48, '#ccc', INK, 2); txt(g, '?', 32, 32, 18, INK, '900 '); }
    g.restore();
  }
  S2P.menuIcon = paintIcon;
  S2P.menuIconCanvas = function (id, size) {
    size = size || 128;
    var c = document.createElement('canvas'); c.width = size; c.height = size;
    var g = c.getContext('2d'); g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
    paintIcon(g, id, size);
    return c;
  };
  S2P.menuIconUrl = function (id, size) { return S2P.menuIconCanvas(id, size).toDataURL('image/png'); };

  /* ---------------- board chrome (390 x 844 phone, or any size) ---------------- */
  function norenStripe(g, x, y, w, h, c1, c2) {
    var n = 7, sw = w / n;
    for (var i = 0; i < n; i++) {
      g.fillStyle = i % 2 ? c2 : c1; g.fillRect(x + i * sw, y, sw + 0.5, h);
    }
    /* scallop */
    g.fillStyle = c1;
    for (var j = 0; j < n; j++) {
      g.beginPath(); g.ellipse(x + (j + 0.5) * sw, y + h, sw * 0.42, 8, 0, 0, 7); g.fill();
    }
    g.strokeStyle = INK; g.lineWidth = 2;
    g.beginPath(); g.moveTo(x, y + h); g.lineTo(x + w, y + h); g.stroke();
  }

  function chiyoChrome(g, W, H) {
    /* warm shop interior wash behind the board */
    g.fillStyle = '#3a241c'; g.fillRect(0, 0, W, H);
    wood(g, 0, 0, W, H, '#6a3e2c', '#5c3424', 28);
    /* dark edges */
    g.fillStyle = 'rgba(20,10,8,.35)'; g.fillRect(0, 0, 14, H); g.fillRect(W - 14, 0, 14, H);
    /* hanging noren */
    norenStripe(g, 10, 0, W - 20, 54, '#8e3b52', '#f4ead2');
    txt(g, '和', 28, 28, 16, '#6a2018', '900 ', SERIF);
    txt(g, '代', W - 28, 28, 16, '#6a2018', '900 ', SERIF);
    /* washi board */
    rr(g, 16, 64, W - 32, H - 88, 10, '#f4ead2', INK, 4);
    paperGrain(g, 20, 68, W - 40, H - 96, 0.05);
    /* inner burgundy rule */
    g.strokeStyle = '#8e3b52'; g.lineWidth = 2;
    rr(g, 24, 72, W - 48, H - 104, 6, 0, '#8e3b52', 2);
    /* brush stamp in the corner */
    g.save(); g.translate(W - 54, H - 54); g.rotate(-0.2);
    ellipse(g, 0, 0, 16, 16, '#8e3b52', INK, 1.5);
    txt(g, '千', 0, 1, 14, '#f4ead2', '900 ', SERIF);
    g.restore();
  }

  function haseChrome(g, W, H) {
    /* concrete bay */
    g.fillStyle = '#6a6860'; g.fillRect(0, 0, W, H);
    for (var y = 0; y < H; y += 48) {
      g.strokeStyle = 'rgba(40,40,36,.18)'; g.lineWidth = 2;
      g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke();
    }
    stain(g, 80, 200, 50, 18, 'rgba(30,24,12,.28)');
    stain(g, W - 70, 520, 40, 16, 'rgba(30,24,12,.22)');
    stain(g, 120, 700, 60, 20, 'rgba(80,50,10,.16)');
    /* greasy plywood board */
    wood(g, 14, 18, W - 28, H - 36, '#5a4634', '#4a3a2a', 26);
    R(g, 14, 18, W - 28, H - 36, 0, INK, 4);
    /* duct-tape corners */
    function tapeCorner(cx, cy, rot) {
      g.save(); g.translate(cx, cy); g.rotate(rot);
      g.fillStyle = '#c8c4b0'; g.fillRect(-22, -8, 44, 16);
      g.strokeStyle = INK; g.lineWidth = 1.6; g.strokeRect(-22, -8, 44, 16);
      g.restore();
    }
    tapeCorner(22, 26, -0.4); tapeCorner(W - 22, 26, 0.5);
    tapeCorner(22, H - 26, 0.5); tapeCorner(W - 22, H - 26, -0.35);
    /* navy shop plate like the counter sign */
    rr(g, 28, 36, W - 56, 70, 4, '#2a3a70', INK, 3);
    /* oil smear on the board */
    stain(g, 60, 180, 30, 10, 'rgba(20,16,8,.3)');
    stain(g, W - 80, 400, 36, 12, 'rgba(80,40,8,.2)');
  }

  function depotChrome(g, W, H) {
    /* time-clock office: teal slats + concrete */
    g.fillStyle = '#3a4a48'; g.fillRect(0, 0, W, H);
    for (var x = 0; x < W; x += 14) {
      g.fillStyle = x % 28 ? '#3a4a48' : '#334440';
      g.fillRect(x, 0, 14, 80);
    }
    g.fillStyle = '#6a6660'; g.fillRect(0, 80, W, H - 80);
    /* hazard bar under the header */
    var hy = 80;
    for (var i = 0; i < W; i += 18) {
      g.fillStyle = (i / 18 | 0) % 2 ? '#e8c040' : '#1a1a1e';
      g.beginPath(); g.moveTo(i, hy); g.lineTo(i + 12, hy); g.lineTo(i + 4, hy + 14); g.lineTo(i - 8, hy + 14); g.closePath(); g.fill();
    }
    R(g, 0, hy, W, 14, 0, INK, 2);
    /* manila ledger clipboard */
    rr(g, 16, 110, W - 32, H - 130, 4, '#e8dcc0', INK, 4);
    /* clip at the top */
    rr(g, W / 2 - 36, 98, 72, 22, 3, '#6a707c', INK, 2);
    R(g, W / 2 - 10, 102, 20, 14, '#c4a060', INK, 1.4);
    /* ruled lines */
    g.save();
    g.beginPath(); g.rect(24, 130, W - 48, H - 160); g.clip();
    g.strokeStyle = 'rgba(40,70,90,.22)'; g.lineWidth = 1;
    for (var ly = 168; ly < H - 40; ly += 22) {
      g.beginPath(); g.moveTo(28, ly); g.lineTo(W - 28, ly); g.stroke();
    }
    /* left margin rule */
    g.strokeStyle = '#8a2a28'; g.lineWidth = 1.5;
    g.beginPath(); g.moveTo(58, 140); g.lineTo(58, H - 36); g.stroke();
    g.restore();
    /* stencil stamp */
    g.save(); g.translate(W - 70, H - 70); g.rotate(-0.15);
    g.strokeStyle = '#8a2a28'; g.lineWidth = 2;
    g.strokeRect(-28, -16, 56, 32);
    txt(g, '出庫', 0, 0, 12, '#8a2a28', '900 ', GOTH);
    g.restore();
  }

  S2P.menuChrome = function (g, theme, w, h) {
    w = w || 390; h = h || 844;
    if (theme === 'hase') haseChrome(g, w, h);
    else if (theme === 'depot') depotChrome(g, w, h);
    else chiyoChrome(g, w, h);
  };
  S2P.menuChromeCanvas = function (theme, w, h) {
    w = w || 390; h = h || 844;
    var c = document.createElement('canvas'); c.width = w; c.height = h;
    var g = c.getContext('2d'); g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
    S2P.menuChrome(g, theme, w, h);
    return c;
  };
  S2P.menuChromeUrl = function (theme, w, h) { return S2P.menuChromeCanvas(theme, w, h).toDataURL('image/png'); };

  /* A full static preview of a shop menu (for stills / self-review). */
  S2P.menuPreview = function (g, theme, opt) {
    opt = opt || {};
    var W = opt.w || 390, H = opt.h || 844, nails = !!opt.nails, items = opt.items || [];
    S2P.menuChrome(g, theme, W, H);
    var fonts = theme === 'depot' ? GOTH : theme === 'hase' ? FONT : SERIF;
    var ink = theme === 'chiyo' ? '#5a2c28' : theme === 'hase' ? '#f0e4c0' : '#2a2a28';
    var accent = theme === 'chiyo' ? '#8e3b52' : theme === 'hase' ? '#e8c040' : '#8a2a28';
    var titleY = theme === 'depot' ? 148 : theme === 'hase' ? 70 : 100;
    txt(g, opt.jp || '', W / 2, titleY, theme === 'hase' ? 20 : 22, theme === 'hase' ? '#f4ead2' : ink, '900 ', fonts);
    txt(g, opt.en || '', W / 2, titleY + 20, 11, theme === 'hase' ? '#c8d0e8' : accent, '700 ', fonts);
    /* portrait + quote + vit, kept on separate columns so nothing collides */
    var px = 32, py = titleY + 36;
    var pcx = px + 30, pcy = py + 30;
    g.save();
    g.beginPath();
    if (theme === 'chiyo') g.arc(pcx, pcy, 30, 0, 7);
    else { var r = 6; g.moveTo(px + r, py); g.lineTo(px + 60 - r, py); g.quadraticCurveTo(px + 60, py, px + 60, py + r); g.lineTo(px + 60, py + 60 - r); g.quadraticCurveTo(px + 60, py + 60, px + 60 - r, py + 60); g.lineTo(px + r, py + 60); g.quadraticCurveTo(px, py + 60, px, py + 60 - r); g.lineTo(px, py + r); g.quadraticCurveTo(px, py, px + r, py); }
    g.closePath(); g.fillStyle = theme === 'chiyo' ? '#f4ead2' : theme === 'depot' ? '#4a5458' : '#2a2b44'; g.fill();
    g.clip();
    if (opt.portrait && opt.portrait.width) {
      try { g.drawImage(opt.portrait, px - 4, py - 10, 68, 90); } catch (eP) {}
    } else if (theme === 'depot') {
      /* stencil clerk: hard hat + work shoulders, until p5 supplies a portrait */
      g.fillStyle = '#2a323e'; g.fillRect(px, py, 60, 60);
      g.fillStyle = '#e8c040';
      g.beginPath(); g.moveTo(pcx - 14, pcy - 2); g.lineTo(pcx - 12, pcy - 16); g.lineTo(pcx + 12, pcy - 16); g.lineTo(pcx + 16, pcy - 2); g.closePath(); g.fill();
      g.fillRect(pcx - 18, pcy - 4, 36, 4);
      g.strokeStyle = INK; g.lineWidth = 1.6; g.stroke();
      g.fillStyle = '#c4a882';
      g.beginPath(); g.ellipse(pcx, pcy + 6, 10, 9, 0, 0, 7); g.fill(); g.stroke();
      g.fillStyle = '#3a4a70';
      g.beginPath(); g.moveTo(pcx - 16, pcy + 30); g.lineTo(pcx - 12, pcy + 14); g.lineTo(pcx + 12, pcy + 14); g.lineTo(pcx + 16, pcy + 30); g.closePath(); g.fill(); g.stroke();
    } else {
      txt(g, (opt.who || '?').charAt(0), pcx, pcy, 18, '#f4ead2', '900 ', fonts);
    }
    g.restore();
    g.strokeStyle = theme === 'chiyo' ? '#8e3b52' : INK; g.lineWidth = theme === 'chiyo' ? 3 : 2.4;
    g.beginPath();
    if (theme === 'chiyo') g.arc(pcx, pcy, 30, 0, 7);
    else { rr(g, px, py, 60, 60, 6, 0, INK, 2.4); }
    if (theme === 'chiyo') g.stroke();
    /* vit, right column */
    var vitC = theme === 'hase' ? '#ffe680' : ink;
    txt(g, 'HP ' + (opt.hp || 40) + '/' + (opt.maxhp || 55), W - 28, py + 10, 11, vitC, '800 ', FONT, 'right');
    txt(g, '¥' + (opt.yen != null ? opt.yen : 40), W - 28, py + 26, 12, vitC, '900 ', FONT, 'right');
    if (nails) txt(g, 'Nails’ price', W - 28, py + 42, 10, accent, '800 ', FONT, 'right');
    if (nails) txt(g, '20% off', W - 28, py + 56, 10, accent, '700 ', FONT, 'right');
    /* quote sits between the portrait and the yen, wrapped */
    if (opt.line) {
      var qx = px + 72, qw = W - 28 - 80 - qx, qy = py + 14;
      g.font = '600 italic 11px ' + fonts; g.fillStyle = theme === 'hase' ? '#d8d0c0' : ink;
      g.textAlign = 'left'; g.textBaseline = 'top';
      var words = ('“' + opt.line + '”').split(' '), line = '', ly = qy;
      words.forEach(function (wrd) {
        var t = line ? line + ' ' + wrd : wrd;
        if (g.measureText(t).width > qw && line) { g.fillText(line, qx, ly); ly += 14; line = wrd; }
        else line = t;
      });
      if (line) g.fillText(line, qx, ly);
    }

    var y0 = py + 76;
    var rowH = items.length > 4 ? 102 : 108;
    var priceW = 72;
    items.forEach(function (it, i) {
      var y = y0 + i * rowH, rh = rowH - 8;
      if (theme === 'chiyo') {
        rr(g, 24, y, W - 48, rh, 8, 'rgba(255,255,255,.35)', '#8e3b52', 1.6);
      } else if (theme === 'hase') {
        rr(g, 24, y, W - 48, rh, 6, '#d8c49a', INK, 2);
        ellipse(g, 40, y + 14, 5, 5, '#6a6860', INK, 1.4);
        stain(g, W - 80, y + rh - 16, 20, 8, 'rgba(40,30,10,.18)');
      } else {
        R(g, 24, y, W - 48, rh, 'rgba(255,255,255,.18)', 0, 0);
        g.strokeStyle = 'rgba(40,70,90,.35)'; g.lineWidth = 1;
        g.beginPath(); g.moveTo(24, y + rh); g.lineTo(W - 24, y + rh); g.stroke();
      }
      rr(g, 32, y + 14, 62, 62, 8, theme === 'hase' ? '#3a3a40' : '#fff8ee', INK, 1.8);
      g.save(); g.translate(31, y + 13); paintIcon(g, it.icon || it.id, 64); g.restore();
      var tx = 104, textR = W - 28 - priceW - 8;
      txt(g, it.jp || '', tx, y + 18, 13, accent, '800 ', fonts, 'left');
      txt(g, it.n || '', tx, y + 36, 12, ink, '700 ', FONT, 'left');
      txt(g, it.eff || '', tx, y + 52, 10, accent, '700 ', FONT, 'left');
      if (it.flavor) {
        g.font = '600 10px ' + FONT; g.textAlign = 'left'; g.textBaseline = 'top'; g.fillStyle = ink; g.globalAlpha = 0.8;
        var fw = textR - tx, fl = '', fy = y + 64, fwords = it.flavor.split(' ');
        fwords.forEach(function (wrd) {
          var t = fl ? fl + ' ' + wrd : wrd;
          if (g.measureText(t).width > fw && fl) { g.fillText(fl, tx, fy); fy += 12; fl = wrd; }
          else fl = t;
        });
        if (fl) g.fillText(fl, tx, fy);
        g.globalAlpha = 1;
      }
      /* reserved price column */
      var prx = W - 28 - priceW / 2, pry = y + rh / 2;
      if (nails && it.base > it.cost) {
        txt(g, '¥' + it.base, prx, pry - 16, 12, ink, '700 ', FONT);
        var tw = g.measureText ? 0 : 0;
        g.font = '700 12px ' + FONT; var sw = g.measureText('¥' + it.base).width;
        g.strokeStyle = accent; g.lineWidth = 1.8;
        g.beginPath(); g.moveTo(prx - sw / 2 - 2, pry - 16); g.lineTo(prx + sw / 2 + 2, pry - 16); g.stroke();
        txt(g, '¥' + it.cost, prx, pry + 8, 18, accent, '900 ', FONT);
      } else {
        txt(g, '¥' + (nails ? it.cost : it.base), prx, pry, 18, accent, '900 ', FONT);
      }
      if (it.prov) txt(g, 'prov.', prx, pry + 26, 8, ink, '700 ', FONT);
    });
    /* leave */
    var ly = H - 64;
    rr(g, W / 2 - 80, ly, 160, 40, 10, theme === 'chiyo' ? '#5c3424' : theme === 'hase' ? '#2a2f55' : '#2a323e', INK, 2);
    txt(g, opt.leave || 'Later', W / 2, ly + 20, 13, '#f4ead2', '800 ', fonts);
  };
})();
