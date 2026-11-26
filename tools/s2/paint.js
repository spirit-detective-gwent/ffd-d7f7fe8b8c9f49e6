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

  /* ---------- interior 1280x900, same shell as Kitsune Udon ---------- */
  S2P.interior = function (g) {
    var RW = 1280, RH = 900; rr(g);
    boards(g, 90, 230, RW - 180, 620, '#f3e4cf', '#ebd6bc', 48);
    plank(g, 90, 0, RW - 180, 230, '#8a4a3a', '#965244', 36);
    R(g, 90, 0, RW - 180, 20, '#5a2c28', INK, 0);
    R(g, 90, 212, RW - 180, 18, '#3b2a22', INK, 0);
    /* noren bar + curtains */
    R(g, 200, 40, 880, 16, '#3b2a22', INK, 3);
    var i, x;
    for (i = 0; i < 8; i++) {
      x = 210 + i * 108;
      R(g, x, 56, 100, 130, i % 2 ? '#c45a6a' : '#e8c9c4', INK, 3);
      txt(g, i % 2 ? '\u548c' : '\u83d3', x + 50, 110, 36, i % 2 ? '#f8ece8' : '#8e3b52', '900 ', 'center');
    }
    /* shelves of sweets */
    function jar(jx, jy, c, lid) {
      ellipse(g, jx, jy + 8, 28, 16, c, INK, 2.5);
      R(g, jx - 28, jy - 36, 56, 44, c, INK, 2.5);
      ellipse(g, jx, jy - 36, 28, 12, lid || '#efe6d2', INK, 2.5);
    }
    R(g, 140, 250, 320, 140, '#6b3e2e', INK, 3);
    R(g, 148, 258, 304, 36, '#3b2a22', 0);
    jar(200, 360, '#f2c4cf', '#f7efe4'); jar(280, 360, '#9ec27a', '#f7efe4'); jar(360, 360, '#e8b23a', '#f7efe4');
    R(g, 820, 250, 320, 140, '#6b3e2e', INK, 3);
    jar(880, 360, '#d96b5c', '#f7efe4'); jar(960, 360, '#f4ead2', '#c45a6a'); jar(1040, 360, '#7a4a2a', '#f7efe4');
    /* counter */
    R(g, 360, 430, 560, 90, '#7a4a32', INK, 4);
    R(g, 360, 500, 560, 70, '#5c3424', INK, 3);
    R(g, 380, 448, 200, 28, '#f4ead2', INK, 2);
    /* tray of rolls and dango */
    R(g, 620, 448, 160, 36, '#efe6d2', INK, 2);
    ellipse(g, 650, 466, 16, 11, '#e8b060', INK, 2);
    ellipse(g, 682, 466, 16, 11, '#d4783a', INK, 2);
    ellipse(g, 714, 466, 16, 11, '#e8b060', INK, 2);
    ellipse(g, 748, 458, 7, 7, '#f2c4cf', INK, 1.5);
    ellipse(g, 748, 470, 7, 7, '#9ec27a', INK, 1.5);
    ellipse(g, 748, 482, 7, 7, '#f4ead2', INK, 1.5);
    R(g, 744, 452, 3, 36, '#6b4a33', INK, 1.5);
    /* sign on the back wall */
    R(g, 520, 70, 240, 70, '#f4ead2', INK, 4);
    txt(g, '\u5343\u4ee3', 640, 96, 28, '#8e3b52', '900 ');
    txt(g, 'WAGASHI CHIYO', 640, 122, 13, '#5a2c28', '700 ');
    /* paper lanterns */
    function lan(lx, ly) {
      glow(g, lx, ly + 20, 70, 'rgba(255,180,120,.28)');
      ellipse(g, lx, ly, 22, 28, '#f3c9a0', INK, 2.5);
      R(g, lx - 4, ly - 36, 8, 10, '#3b2a22', INK, 2);
    }
    lan(250, 90); lan(1030, 90);
    /* side walls + door band */
    g.fillStyle = '#1b1820'; g.fillRect(0, 0, 90, RH); g.fillRect(RW - 90, 0, 90, RH);
    g.fillRect(0, 850, 580, 50); g.fillRect(700, 850, 580, 50);
    g.strokeStyle = INK; g.lineWidth = 4; g.strokeRect(90, 2, RW - 180, 848);
    g.fillStyle = 'rgba(255,220,160,.10)'; g.fillRect(580, 850, 120, 50);
    var vg = g.createRadialGradient(640, 520, 260, 640, 520, 820);
    vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(10,6,14,.38)');
    g.fillStyle = vg; g.fillRect(0, 0, RW, RH);
    /* floor glow from lanterns */
    glow(g, 640, 520, 280, 'rgba(255,190,140,.10)');
  };

  /* ---------- storefront (existing Wagashi block, with a door) ---------- */
  S2P.exterior = function (g) {
    var W = 900, H = 640; rr(g);
    /* night street */
    g.fillStyle = '#1a1520'; g.fillRect(0, 0, W, H);
    var sky = g.createLinearGradient(0, 0, 0, 280);
    sky.addColorStop(0, '#1c1630'); sky.addColorStop(1, '#2a2038');
    g.fillStyle = sky; g.fillRect(0, 0, W, 300);
    /* pavement */
    g.fillStyle = '#3a3340'; g.fillRect(0, 420, W, 220);
    g.fillStyle = '#2e2833'; g.fillRect(0, 500, W, 20);
    /* building body */
    R(g, 80, 70, 740, 380, '#c4a07a', INK, 5);
    plank(g, 80, 70, 740, 90, '#8a4a3a', '#965244', 40);
    R(g, 80, 70, 740, 18, '#5a2c28', INK, 0);
    /* signboard */
    R(g, 250, 100, 400, 70, '#f4ead2', INK, 4);
    txt(g, '\u548c\u83d3\u5b50  \u5343\u4ee3', 450, 128, 28, '#8e3b52', '900 ');
    txt(g, 'WAGASHI CHIYO', 450, 154, 14, '#5a2c28', '700 ');
    /* windows */
    function win(x, y, lit) {
      R(g, x, y, 120, 110, lit ? '#f3d7a0' : '#2a2230', INK, 4);
      g.beginPath(); g.moveTo(x + 60, y); g.lineTo(x + 60, y + 110); g.moveTo(x, y + 55); g.lineTo(x + 120, y + 55);
      g.strokeStyle = INK; g.lineWidth = 3; g.stroke();
      if (lit) glow(g, x + 60, y + 55, 80, 'rgba(255,200,120,.25)');
    }
    win(140, 210, 1); win(640, 210, 1);
    /* noren over the new door */
    R(g, 360, 200, 180, 16, '#3b2a22', INK, 3);
    R(g, 368, 216, 80, 70, '#c45a6a', INK, 3);
    R(g, 452, 216, 80, 70, '#e8c9c4', INK, 3);
    txt(g, '\u548c', 408, 250, 26, '#f8ece8', '900 ');
    txt(g, '\u83d3', 492, 250, 26, '#8e3b52', '900 ');
    /* door */
    R(g, 385, 286, 130, 164, '#6b3e2e', INK, 4);
    R(g, 400, 300, 48, 70, '#d8c4a0', INK, 2.5);
    R(g, 452, 300, 48, 70, '#d8c4a0', INK, 2.5);
    ellipse(g, 500, 370, 5, 5, '#e0b23a', INK, 2);
    /* step */
    R(g, 370, 450, 160, 16, '#5c3424', INK, 3);
    /* lanterns */
    glow(g, 200, 200, 90, 'rgba(255,170,100,.3)');
    glow(g, 700, 200, 90, 'rgba(255,170,100,.3)');
    ellipse(g, 200, 190, 20, 26, '#f3c9a0', INK, 2.5);
    ellipse(g, 700, 190, 20, 26, '#f3c9a0', INK, 2.5);
    /* street edge */
    g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(0, 460, W, 180);
  };

  /* ---------- battle backdrop 720x1280, C2BT style ---------- */
  S2P.battle = function (g) {
    var WD = 720, HT = 1280, H0 = 330, VP = [360, -260];
    rr(g);
    function fx0(u, y) { var k = (y - VP[1]) / (HT - VP[1]); return VP[0] + (u - VP[0]) * k; }
    /* dusk sky */
    var sky = g.createLinearGradient(0, 0, 0, H0);
    sky.addColorStop(0, '#2a1c38'); sky.addColorStop(0.6, '#5a3048'); sky.addColorStop(1, '#8a4a4a');
    g.fillStyle = sky; g.fillRect(0, 0, WD, H0);
    /* shop wall behind the fight */
    R(g, 40, 80, 640, 250, '#c4a07a', INK, 4);
    plank(g, 40, 80, 640, 70, '#8a4a3a', '#965244', 36);
    R(g, 180, 100, 360, 50, '#f4ead2', INK, 3);
    txt(g, '\u548c\u83d3\u5b50', 360, 126, 28, '#8e3b52', '900 ');
    /* noren */
    R(g, 240, 160, 240, 14, '#3b2a22', INK, 3);
    R(g, 248, 174, 108, 80, '#c45a6a', INK, 3);
    R(g, 364, 174, 108, 80, '#e8c9c4', INK, 3);
    txt(g, '\u548c', 302, 214, 28, '#f8ece8', '900 ');
    txt(g, '\u83d3', 418, 214, 28, '#8e3b52', '900 ');
    /* lanterns */
    glow(g, 120, 160, 80, 'rgba(255,170,100,.4)');
    glow(g, 600, 160, 80, 'rgba(255,170,100,.4)');
    ellipse(g, 120, 150, 22, 28, '#f3c9a0', INK, 2.5);
    ellipse(g, 600, 150, 22, 28, '#f3c9a0', INK, 2.5);
    /* floor: warm stone of Wagashi row, perspective lanes */
    var fl = g.createLinearGradient(0, H0, 0, HT);
    fl.addColorStop(0, '#4a3a40'); fl.addColorStop(1, '#2a2228');
    g.fillStyle = fl; g.fillRect(0, H0, WD, HT - H0);
    var n = 9, i, j, u;
    g.strokeStyle = 'rgba(230,190,170,.22)'; g.lineWidth = 2;
    for (i = -n; i <= n * 2; i++) {
      u = -360 + i * (1440 / n);
      g.beginPath(); g.moveTo(fx0(u, H0), H0); g.lineTo(fx0(u, HT), HT); g.stroke();
    }
    for (j = 0; j < 14; j++) {
      var q = j / 14, y = H0 + (HT - H0) * Math.pow(q, 1.55);
      g.beginPath(); g.moveTo(0, y); g.lineTo(WD, y); g.stroke();
    }
    /* broken sweet-shop glass on the stones */
    g.fillStyle = 'rgba(180,220,230,.35)';
    [[200, 700, 40, 12], [480, 820, 28, 10], [300, 960, 36, 11], [520, 1100, 22, 8]].forEach(function (s) {
      g.save(); g.translate(s[0], s[1]); g.rotate(-0.3);
      g.beginPath(); g.moveTo(0, 0); g.lineTo(s[2], 2); g.lineTo(s[2] * 0.6, s[3]); g.closePath(); g.fill();
      g.strokeStyle = INK; g.lineWidth = 1.5; g.stroke(); g.restore();
    });
    /* soft lantern pools on the floor */
    glow(g, 180, 500, 140, 'rgba(255,170,100,.18)');
    glow(g, 540, 500, 140, 'rgba(255,170,100,.18)');
  };

  /* ---------- sweets ---------- */
  S2P.sweetRoll = function (g, s) {
    s = s || 1; g.save(); g.scale(s, s); rr(g);
    ellipse(g, 80, 92, 62, 28, 'rgba(40,20,10,.25)', 0);
    ellipse(g, 80, 70, 58, 36, '#e8b060', INK, 3);
    ellipse(g, 80, 58, 50, 24, '#f3c97a', INK, 0);
    /* swirl / anko peek */
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
    /* two halves, anko stretch */
    ellipse(g, 50, 70, 32, 26, '#e8b060', INK, 3);
    ellipse(g, 110, 70, 32, 26, '#e8b060', INK, 3);
    g.beginPath(); g.moveTo(70, 62); g.quadraticCurveTo(80, 90, 90, 62);
    g.quadraticCurveTo(80, 50, 70, 62);
    g.fillStyle = '#7a3a22'; g.fill(); g.strokeStyle = INK; g.lineWidth = 2; g.stroke();
    g.restore();
  };

  /* ---------- Chiyo cel sprite, front idle (one figure + a 4-frame walk strip) ---------- */
  function chiyoFig(g, x, y, sc, walk, frame) {
    sc = sc || 1; g.save(); g.translate(x, y); g.scale(sc, sc); rr(g);
    var bob = walk ? Math.sin(frame * 1.2) * 2 : 0;
    var step = walk ? ((frame % 2) ? 6 : -6) : 0;
    /* shadow */
    ellipse(g, 0, 78, 28, 8, 'rgba(0,0,0,.28)', 0);
    /* legs */
    g.fillStyle = '#5a3a3a';
    g.beginPath(); g.ellipse(-10, 62 + bob, 7, 16, 0.1 * step, 0, 7); g.fill();
    g.beginPath(); g.ellipse(10, 62 - bob, 7, 16, -0.1 * step, 0, 7); g.fill();
    g.strokeStyle = INK; g.lineWidth = 2.5;
    g.beginPath(); g.ellipse(-10, 62 + bob, 7, 16, 0.1 * step, 0, 7); g.stroke();
    g.beginPath(); g.ellipse(10, 62 - bob, 7, 16, -0.1 * step, 0, 7); g.stroke();
    /* shoes */
    ellipse(g, -10 + step * 0.3, 76 + bob, 10, 5, '#3b2a22', INK, 2);
    ellipse(g, 10 - step * 0.3, 76 - bob, 10, 5, '#3b2a22', INK, 2);
    /* body / happi + apron */
    R(g, -28, 8, 56, 50, '#c47a7a', INK, 3);
    R(g, -18, 16, 36, 44, '#e8b8b0', INK, 2.5);
    /* cream collar */
    g.beginPath(); g.moveTo(-10, 10); g.lineTo(0, 22); g.lineTo(10, 10);
    g.fillStyle = '#f4ead2'; g.fill(); g.strokeStyle = INK; g.lineWidth = 2; g.stroke();
    /* apron knot */
    ellipse(g, 0, 14, 7, 5, '#e8b8b0', INK, 2);
    /* arms */
    var ax = walk ? step * 0.8 : 0;
    R(g, -36, 16 + bob * 0.3, 10, 28, '#c47a7a', INK, 2.5);
    R(g, 26, 16 - bob * 0.3, 10, 28, '#c47a7a', INK, 2.5);
    ellipse(g, -31, 46 + bob * 0.3, 6, 6, '#e8c4b0', INK, 2);
    ellipse(g, 31, 46 - bob * 0.3, 6, 6, '#e8c4b0', INK, 2);
    /* head */
    ellipse(g, 0, -18, 22, 24, '#f0c8b0', INK, 3);
    /* hair bun */
    ellipse(g, 0, -36, 20, 14, '#4a3a3a', INK, 2.5);
    ellipse(g, 16, -30, 8, 8, '#5a4a4a', INK, 2);
    /* silver streak */
    g.beginPath(); g.moveTo(-14, -28); g.quadraticCurveTo(-6, -38, 4, -32);
    g.strokeStyle = '#b8b0b4'; g.lineWidth = 3; g.stroke();
    /* sakura pin */
    ellipse(g, 16, -32, 4, 4, '#e8a0b4', INK, 1.5);
    /* face */
    ellipse(g, -8, -20, 3, 3.5, '#2a1a18', 0);
    ellipse(g, 8, -20, 3, 3.5, '#2a1a18', 0);
    g.beginPath(); g.arc(0, -8, 6, 0.15, Math.PI - 0.15);
    g.strokeStyle = INK; g.lineWidth = 2; g.stroke();
    /* blush */
    ellipse(g, -12, -12, 5, 3, 'rgba(220,100,90,.35)', 0);
    ellipse(g, 12, -12, 5, 3, 'rgba(220,100,90,.35)', 0);
    g.restore();
  }
  S2P.chiyoFig = chiyoFig;
  S2P.chiyoIdle = function (g) { g.clearRect(0, 0, g.canvas.width, g.canvas.height); chiyoFig(g, 80, 90, 1.6, 0, 0); };
  S2P.chiyoWalk = function (g) {
    g.clearRect(0, 0, g.canvas.width, g.canvas.height);
    for (var i = 0; i < 4; i++) chiyoFig(g, 70 + i * 140, 100, 1.35, 1, i);
  };

  S2P.sizes = {
    interior: [1280, 900],
    exterior: [900, 640],
    battle: [720, 1280],
    sweetRoll: [160, 140],
    dango: [100, 160],
    rollSplit: [160, 140],
    chiyoIdle: [160, 200],
    chiyoWalk: [560, 200]
  };
})(typeof window !== 'undefined' ? window : globalThis);
