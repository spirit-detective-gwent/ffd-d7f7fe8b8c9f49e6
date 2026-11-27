/* v6.5.64 Game Center cabinet: CHUO CRISIS (light-gun rail shooter; replaces Neon Ring Flight). v6564-arcade.
 * Tap the screen to shoot. Hold DUCK to take cover (reloads, enemy shots miss). RELOAD button or a tap off the screen reloads too.
 * 5 stages x 3 areas + a boss each. Goons, bikers and security robots; shopkeepers are hostages (don't shoot). No gore: KO stars. */
(function () {
  try {
  var root = typeof window !== 'undefined' ? window : this;
  var A = root.FFF_S2ARC = root.FFF_S2ARC || { v: 1 };
  A.GAMES = A.GAMES || {}; A.CABS = A.CABS || {};
  A.CABS.gun = { n: 'Chuo Crisis', jp: '\u4e2d\u592e\u30af\u30e9\u30a4\u30b7\u30b9', col: '#ff4a5a', body: '#1e1020', mq: ['#3a0810', '#12040a'], deck: ['#3a1a24', '#1a0a10'],
    tiers: [30000, 70000, 120000],
    seed: [['JIN', 1.62], ['OGT', 1.31], ['KNZ', 1.12], ['TTS', 0.94], ['BAN', 0.78], ['KDE', 0.6], ['TSO', 0.46], ['PNT', 0.34], ['CLK', 0.24], ['CHY', 0.15]],
    mqArt: function (p, x, y, w, h) { for (var i = 0; i < 14; i++) { p.fillStyle = 'rgba(255,74,90,' + (0.08 + (i % 3) * 0.05) + ')'; p.fillRect(x + i * 28, y + h - 18 - (i * 37) % 30, 22, 40); }
      p.fillStyle = '#ffd860'; for (var j = 0; j < 3; j++) { p.beginPath(); p.arc(x + 30 + j * 12, y + 20, 3, 0, 7); p.fill(); } },
    panelArt: function (p, PY, Hd) { /* the holstered light gun on its cable */
      var K = A.K; p.strokeStyle = '#0a0608'; p.lineWidth = 5; p.beginPath(); p.moveTo(195, Hd - 50); p.bezierCurveTo(150, Hd - 70, 240, PY + 120, 196, PY + 92); p.stroke();
      K.rr(p, 168, PY + 44, 56, 60, 10, '#140a10', 3); gunShape(p, 196, PY + 70, 1.15, '#ff4a5a');
      K.txt(p, 'HOLSTER', 196, PY + 116, 8, 'rgba(255,255,255,.55)'); } };
  function gunShape(p, x, y, s, col) { var K = A.K; p.save(); p.translate(x, y); p.scale(s, s);
    K.poly(p, [-22, -10, 20, -10, 24, -4, 24, 2, -6, 2, -10, 18, -20, 18, -16, 2, -22, 2], col, 2.5); K.rr(p, 18, -14, 6, 5, 2, '#ffd860', 1.5); p.fillStyle = 'rgba(255,255,255,.35)'; p.fillRect(-18, -8, 30, 3); p.restore(); }

  A.GAMES.gun = function (K, C) {
    var rr = K.rr, txt = K.txt, otxt = K.otxt, ell = K.ell, poly = K.poly, glow = K.glow, tone = K.tone, drum = K.drum, now = K.now, SW = K.SW, SH = K.SH, INK = K.INK, clamp = K.clamp;
    var seed = 1; function R() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
    /* ---------- stages ---------- */
    var STG = [
      { n: 'Chuo-dori Night', sub: 'Pachinko row \u00b7 the Suits are collecting', sky: ['#1a0a3a', '#7a2a6a'], k: 'street', types: ['goon'], boss: { n: 'THE DOORMAN', kind: 'bouncer', hp: 34, col: '#2a2a34' } },
      { n: 'Hotel Chuo 7F', sub: 'The floor that isn\u2019t on the board', sky: ['#2a1a10', '#6a4a2a'], k: 'hotel', types: ['goon', 'goon', 'biker'], boss: { n: 'OGATA', kind: 'suit', hp: 44, col: '#3a3048' } },
      { n: 'Freight Depot', sub: 'Gray coats and borrowed robots', sky: ['#0e1420', '#3a4a5a'], k: 'depot', types: ['goon', 'robot', 'biker'], boss: { n: 'FORK-LIFTER MK.II', kind: 'robot', hp: 56, col: '#d8a020' } },
      { n: 'Club Kitsune', sub: 'Lights down, music up, heads down', sky: ['#1a0630', '#5a0a6a'], k: 'club', types: ['goon', 'biker', 'robot', 'goon'], boss: { n: 'KANZAKI', kind: 'suit', hp: 64, col: '#4a1a2a' } },
      { n: 'Neon Tower Roof', sub: 'Final stage \u00b7 the high score is up there', sky: ['#04081a', '#ff4ab0'], k: 'roof', types: ['robot', 'biker', 'goon', 'robot'], boss: { n: 'MECHA-JIN', kind: 'mecha', hp: 80, col: '#6aff4a' } }
    ];
    var G = { score: 0, stage: 0, stages: STG, stageWord: 'STAGE', how: ['Tap the screen to shoot', 'Six shots, then RELOAD', 'Hold DUCK: cover + reload', 'Red ring closing = duck NOW', 'Shoot thrown bottles out of the air', 'Head shots score double', 'Never shoot the shopkeepers'],
      panel: { btns: [{ k: 'duck', x: 76, y: 706, r: 50, l: 'DUCK', c: '#ffd860', sub: 'hold for cover', fs: 16 }, { k: 'reload', x: 316, y: 706, r: 40, l: 'RELOAD', c: '#5ad8ff' }] } };
    G.endLine = 'Chuo-dori sleeps easy tonight.';
    var lives, ammo, area, areas, en, fx, shots, hits, cover, coverT, inv, hurtT, timeL, waveI, waves, boss, phase, trans, transBg, msg, msgT, reloadT, combo, comboT, layers, thrown, kos, bonusAcc;
    /* ---------- painted areas: bg + fg layers (once per stage) ---------- */
    function sky(g, S) { var sg = g.createLinearGradient(0, 0, 0, SH); sg.addColorStop(0, S.sky[0]); sg.addColorStop(1, S.sky[1]); g.fillStyle = sg; g.fillRect(0, 0, SW, SH); }
    function building(g, x, y, w, h, c, lit) { rr(g, x, y, w, h, 0, c, 2); for (var j = y + 10; j < y + h - 10; j += 18) for (var i = x + 8; i < x + w - 10; i += 16) { g.fillStyle = (i * 7 + j * 3) % 5 < 2 ? lit : 'rgba(0,0,0,.35)'; g.fillRect(i, j, 9, 10); } }
    function sign(g, x, y, w, h, c, s0) { g.drawImage(glow(K.hexRgb(c), 50), x + w / 2 - 50, y + h / 2 - 50); rr(g, x, y, w, h, 5, '#0a0610', 2.5, c); txt(g, s0, x + w / 2, y + h / 2, Math.min(15, h * 0.55), c); }
    function crate(g, x, y, w, h, c) { rr(g, x, y, w, h, 3, c || '#8a5a2a', 3); g.strokeStyle = 'rgba(0,0,0,.35)'; g.lineWidth = 3; g.beginPath(); g.moveTo(x + 4, y + 4); g.lineTo(x + w - 4, y + h - 4); g.moveTo(x + w - 4, y + 4); g.lineTo(x + 4, y + h - 4); g.stroke(); rr(g, x, y, w, h, 3, null, 3); }
    function car(g, x, y, w, c) { rr(g, x, y + 20, w, 34, 10, c, 3); rr(g, x + w * 0.2, y, w * 0.55, 26, 10, c, 3); rr(g, x + w * 0.26, y + 4, w * 0.2, 18, 4, '#9ad8f0', 2); rr(g, x + w * 0.5, y + 4, w * 0.2, 18, 4, '#9ad8f0', 2); ell(g, x + w * 0.22, y + 54, 11, 11, '#111', 2); ell(g, x + w * 0.78, y + 54, 11, 11, '#111', 2); g.drawImage(glow('255,220,120', 18), x + w - 26, y + 22); }
    function paintArea(S, ai) {
      var k = S.k, bg = K.layer(SW, SH, function (g) { sky(g, S);
        if (k === 'street') { building(g, -10, 60, 120, 300, '#1c1428', 'rgba(255,200,120,.55)'); building(g, 250, 40, 130, 320, '#20162c', 'rgba(150,220,255,.5)'); building(g, 110, 110, 140, 250, '#281a30', 'rgba(255,120,200,.5)');
          sign(g, 120 + ai * 20, 130, 110, 36, ['#ff5ac8', '#5ad8ff', '#ffd860'][ai % 3], ['\u30d1\u30c1\u30f3\u30b3', 'LUCKY 7', '\u5c45\u9152\u5c4b'][ai % 3]); g.fillStyle = '#2a2430'; g.fillRect(0, 360, SW, 140); g.fillStyle = '#3a3440'; for (var i = 0; i < 6; i++) g.fillRect(i * 70 - (ai * 23) % 70, 420, 40, 6);
          rr(g, 20, 300, 90, 64, 2, '#4a4a56', 2); for (var l = 0; l < 6; l++) { g.fillStyle = '#5a5a66'; g.fillRect(22, 304 + l * 10, 86, 3); } rr(g, 252, 300, 90, 64, 2, '#4a4a56', 2); }
        if (k === 'hotel') { g.fillStyle = '#4a2a1a'; g.fillRect(0, 0, SW, SH); var vg = g.createLinearGradient(0, 0, 0, SH); vg.addColorStop(0, '#2a160c'); vg.addColorStop(1, '#6a3a20'); g.fillStyle = vg; g.fillRect(0, 0, SW, SH);
          poly(g, [0, 0, 130, 160, 130, 330, 0, 500], '#5a3020', 0); poly(g, [SW, 0, 232, 160, 232, 330, SW, 500], '#5a3020', 0); rr(g, 130, 160, 102, 170, 0, '#2a1208', 2);
          [[30, 120, 70, 220], [270, 120, 70, 220]].forEach(function (d, i) { rr(g, d[0], d[1] + ai * 6, d[2], d[3], 3, '#7a4a2a', 3); ell(g, d[0] + (i ? 10 : d[2] - 10), d[1] + d[3] / 2, 4, 4, '#ffd860', 1.5); txt(g, '70' + (ai * 2 + i + 1), d[0] + d[2] / 2, d[1] + 24, 12, '#ffd860'); });
          g.fillStyle = '#8a2a2a'; poly(g, [130, 330, 232, 330, 300, 500, 62, 500], '#8a2a2a', 0); g.fillStyle = 'rgba(255,216,96,.3)'; for (var y = 340; y < 500; y += 26) g.fillRect(150 - (y - 330) * 0.5, y, 62 + (y - 330), 3);
          g.drawImage(glow('255,200,120', 60), 181 - 60, 150 - 60); }
        if (k === 'depot') { g.fillStyle = '#2a323c'; g.fillRect(0, 0, SW, 360); for (var r2 = 0; r2 < SW; r2 += 30) { g.fillStyle = r2 % 60 ? '#323a46' : '#2a313c'; g.fillRect(r2, 0, 28, 360); } g.fillStyle = '#4a4a44'; g.fillRect(0, 360, SW, 140);
          g.fillStyle = '#ffd040'; for (var st = 0; st < 12; st++) poly(g, [st * 34, 372, st * 34 + 16, 372, st * 34 + 6, 384, st * 34 - 10, 384], '#ffd040', 0);
          rr(g, 120, 90, 120, 160, 4, '#1a1e24', 3); for (var sl = 0; sl < 10; sl++) { g.fillStyle = '#3a424c'; g.fillRect(124, 96 + sl * 15, 112, 8); } txt(g, 'BAY ' + (ai + 3), 180, 80, 13, '#ffd860');
          g.drawImage(glow('255,220,150', 40), 50, 10); g.drawImage(glow('255,220,150', 40), 240, 10); }
        if (k === 'club') { var cg = g.createLinearGradient(0, 0, 0, SH); cg.addColorStop(0, '#12041e'); cg.addColorStop(1, '#3a0a4a'); g.fillStyle = cg; g.fillRect(0, 0, SW, SH);
          for (var b = 0; b < 7; b++) { g.save(); g.globalAlpha = 0.18; g.fillStyle = ['#ff5ac8', '#5ad8ff', '#ffd860'][b % 3]; poly(g, [60 + b * 40, 0, 40 + b * 46 + ai * 10, 380, 90 + b * 46 + ai * 10, 380], g.fillStyle, 0); g.restore(); }
          for (var fy = 0; fy < 5; fy++) for (var fx2 = 0; fx2 < 9; fx2++) { g.fillStyle = (fx2 + fy + ai) % 3 === 0 ? 'rgba(255,90,200,.5)' : (fx2 + fy) % 3 === 1 ? 'rgba(90,216,255,.35)' : 'rgba(255,255,255,.08)'; g.fillRect(fx2 * 42 - fy * 6, 380 + fy * 24, 40, 22); }
          ell(g, 181, 60, 24, 24, '#c8c8d8', 2); for (var m = 0; m < 12; m++) { g.fillStyle = m % 2 ? '#fff' : '#9a9ab0'; g.fillRect(166 + (m % 4) * 8, 46 + ((m / 4) | 0) * 9, 6, 6); } sign(g, 110, 110, 142, 40, '#ff5ac8', 'CLUB KITSUNE'); }
        if (k === 'roof') { sky(g, S); for (var st2 = 0; st2 < 50; st2++) { g.fillStyle = 'rgba(255,255,255,' + (0.3 + (st2 % 3) * 0.2) + ')'; g.fillRect((st2 * 71) % SW, (st2 * 37) % 200, 2, 2); }
          building(g, 0, 240, 70, 160, '#140c24', 'rgba(255,90,200,.6)'); building(g, 300, 220, 70, 180, '#140c24', 'rgba(90,216,255,.6)'); building(g, 80, 280, 60, 120, '#1c1030', 'rgba(255,216,96,.5)'); building(g, 230, 270, 60, 130, '#1c1030', 'rgba(255,216,96,.5)');
          g.fillStyle = '#2a2a36'; g.fillRect(0, 380, SW, 120); ell(g, 181, 450, 120, 34, '#3a3a48', 2); txt(g, 'H', 181, 450, 34, '#ffd860'); rr(g, 30, 330, 40, 60, 2, '#5a5a6a', 2); rr(g, 290, 320, 50, 70, 2, '#5a5a6a', 2); g.drawImage(glow('255,40,60', 14), 300, 306); }
      });
      var fg = K.layer(SW, SH, function (g) { var c = k === 'depot' ? '#8a6a3a' : k === 'club' ? '#3a1a4a' : k === 'hotel' ? '#6a3a20' : '#5a4a3a';
        if (k === 'street') { crate(g, 14, 400, 96, 70, '#7a5a3a'); car(g, 210, 380, 150, ai % 2 ? '#c8302a' : '#2a6ac8'); }
        else if (k === 'hotel') { rr(g, 10, 400, 110, 90, 6, '#c8b8a0', 3); txt(g, 'ROOM SERVICE', 65, 420, 9, '#5a3a2a'); rr(g, 250, 410, 104, 80, 6, '#8a5a3a', 3); rr(g, 256, 404, 92, 14, 4, '#5a3a20', 2); }
        else if (k === 'depot') { crate(g, 0, 380, 110, 100, c); crate(g, 250, 390, 112, 90, '#5a6a3a'); crate(g, 120, 440, 70, 50, c); }
        else if (k === 'club') { rr(g, 0, 400, 130, 90, 10, '#2a0a2a', 3); rr(g, 6, 394, 118, 16, 6, '#ff5ac8', 2); rr(g, 240, 410, 122, 80, 10, '#2a0a2a', 3); rr(g, 246, 404, 110, 16, 6, '#5ad8ff', 2); }
        else { rr(g, 0, 400, 100, 80, 4, '#4a4a58', 3); g.fillStyle = '#6a6a7a'; for (var v = 0; v < 4; v++) g.fillRect(8, 410 + v * 16, 84, 6); rr(g, 262, 396, 100, 84, 4, '#4a4a58', 3); }
      });
      /* spawn slots [x, footY, scale, hide] — footY is where the cover top is */
      var slots = { street: [[60, 402, 0.9], [300, 384, 0.95], [70, 300, 0.6], [292, 300, 0.6], [181, 360, 0.75], [150, 250, 0.5]],
        hotel: [[64, 404, 0.95], [302, 410, 0.95], [64, 340, 0.75], [304, 340, 0.75], [181, 330, 0.55], [150, 330, 0.5]],
        depot: [[56, 382, 1], [306, 392, 0.95], [155, 442, 0.8], [180, 250, 0.6], [60, 300, 0.7], [300, 300, 0.7]],
        club: [[64, 400, 0.95], [300, 410, 0.95], [181, 380, 0.7], [120, 330, 0.6], [250, 330, 0.6], [181, 300, 0.5]],
        roof: [[50, 400, 0.95], [312, 396, 0.95], [50, 330, 0.65], [315, 320, 0.7], [181, 380, 0.75], [181, 290, 0.5]] }[k];
      return { bg: bg, fg: fg, slots: slots };
    }
    /* ---------- figures ---------- */
    function figure(g, E, t) { var sc = E.sc, x = E.x, rise = E.rise, y = E.foot + (1 - rise) * 120 * sc - 10 * sc, ty = E.type, hurt = E.flash > 0;
      g.save(); g.translate(x, y); g.scale(sc, sc); if (E.ko) { g.rotate(E.koR); g.globalAlpha = clamp(1 - E.koT / 0.8, 0, 1); }
      var lean = Math.sin(t * 3 + E.ph) * 2;
      if (ty === 'robot') { rr(g, -30, -96, 60, 70, 10, hurt ? '#fff' : '#8a94a8', 3); rr(g, -22, -136, 44, 38, 8, hurt ? '#fff' : '#a8b0c0', 3); rr(g, -16, -126, 32, 12, 5, '#1a1a24', 2); g.drawImage(glow('255,40,60', 12), -12 + Math.sin(t * 2) * 6, -132); rr(g, -6, -124, 12, 8, 3, '#ff3040', 0);
        rr(g, -46, -90, 16, 50, 6, '#6a7488', 3); rr(g, 30, -90, 16, 50, 6, '#6a7488', 3); rr(g, 32, -48, 26, 12, 3, '#2a2a34', 2); txt(g, 'SEC', 0, -66, 12, '#1a1a24'); g.lineWidth = 3; g.strokeStyle = INK; g.beginPath(); g.moveTo(0, -136); g.lineTo(0, -150); g.stroke(); ell(g, 0, -152, 4, 4, '#ff3040', 2); }
      else if (ty === 'hostage') { rr(g, -26, -92, 52, 70, 12, hurt ? '#fff' : '#e8e0d0', 3); rr(g, -20, -86, 40, 64, 8, '#5a8ac8', 2); ell(g, 0, -112, 20, 22, '#f0c8a0', 3); g.fillStyle = '#6a6a6a'; g.beginPath(); g.ellipse(0, -126, 20, 10, 0, Math.PI, 0); g.fill();
        g.fillStyle = INK; g.fillRect(-8, -114, 4, 4); g.fillRect(5, -114, 4, 4); g.lineWidth = 2; g.strokeStyle = INK; g.beginPath(); g.arc(0, -102, 5, 0, Math.PI); g.stroke(); rr(g, -48, -120, 18, 40, 8, '#f0c8a0', 2.5); rr(g, 30, -120, 18, 40, 8, '#f0c8a0', 2.5); txt(g, '\u2715', 0, -150, 18, '#7aff9a'); }
      else { var jk = ty === 'biker' ? '#2a2026' : ty === 'boss' ? E.col : '#22222c';
        rr(g, -30, -94, 60, 76, 12, hurt ? '#fff' : jk, 3); poly(g, [-10, -94, 10, -94, 0, -64], '#f2f2f2', 2); if (ty !== 'biker') poly(g, [-3, -88, 3, -88, 4, -64, 0, -58, -4, -64], '#c8202a', 1.5); else { rr(g, -26, -86, 52, 8, 2, '#ff9a3a', 0); }
        ell(g, 0, -114, 19, 21, '#e8b890', 3);
        if (ty === 'biker') { g.fillStyle = hurt ? '#fff' : '#c8302a'; g.beginPath(); g.arc(0, -116, 24, Math.PI * 1.05, Math.PI * 1.95 + 0.3); g.lineTo(22, -104); g.lineTo(-22, -104); g.closePath(); g.fill(); g.lineWidth = 3; g.strokeStyle = INK; g.stroke(); rr(g, -18, -120, 36, 12, 4, '#1a2a3a', 2); }
        else { g.fillStyle = '#16121a'; g.beginPath(); g.ellipse(0, -128, 21, 11, 0, Math.PI, 0); g.fill(); poly(g, [-19, -128, 22, -130, 14, -136], '#16121a', 0); rr(g, -15, -119, 13, 7, 3, '#0a0a10', 0); rr(g, 2, -119, 13, 7, 3, '#0a0a10', 0); g.fillStyle = '#0a0a10'; g.fillRect(-2, -117, 4, 2); g.lineWidth = 2; g.strokeStyle = INK; g.beginPath(); g.moveTo(-6, -102); g.lineTo(6, -103); g.stroke(); }
        /* arm + pistol pointing at the player */
        var aim = E.aim > 0; rr(g, 22, -86 + lean, 16, aim ? 30 : 42, 7, jk, 3); if (aim) { rr(g, 18, -64 + lean, 26, 14, 4, '#3a3a44', 2.5); rr(g, 24, -60 + lean, 14, 8, 2, '#1a1a20', 0); } rr(g, -38, -86, 16, 40, 7, jk, 3); }
      g.restore();
      if (!E.ko && E.aim > 0 && E.type !== 'hostage') { var k2 = E.aim / E.aimMax, rad = 14 + 60 * k2, cy = y - 110 * sc; g.lineWidth = 3; g.strokeStyle = k2 < 0.3 ? '#ff2030' : 'rgba(255,216,96,.9)'; g.beginPath(); g.arc(x, cy, rad * sc + 6, 0, 7); g.stroke();
        if (k2 < 0.3) { g.drawImage(glow('255,30,40', 26), x - 26, cy - 26); otxt(g, '!', x, cy - rad * sc - 18, 18, '#ff2030'); } }
    }
    function bossFig(g, B, t) { var x = B.x, y = B.y, hurt = B.flash > 0, sc = B.sc;
      g.save(); g.translate(x, y); g.scale(sc, sc); if (B.ko) { g.rotate(B.koT * 0.4); g.globalAlpha = clamp(1 - B.koT / 2, 0, 1); }
      var k = B.kind;
      if (k === 'robot') { rr(g, -90, -40, 180, 70, 10, hurt ? '#fff' : '#d8a020', 4); rr(g, -60, -120, 120, 84, 10, hurt ? '#fff' : '#c89018', 4); rr(g, -40, -104, 80, 30, 6, '#1a1a24', 3); for (var i = 0; i < 3; i++) g.drawImage(glow('255,40,60', 12), -30 + i * 24 - 12, -101); 
        rr(g, 70, -150, 14, 120, 4, '#5a5a66', 3); rr(g, 60, -60, 70, 10, 2, '#8a8a96', 3); rr(g, 60, -30, 70, 10, 2, '#8a8a96', 3); ell(g, -60, 34, 22, 22, '#111', 3); ell(g, 60, 34, 22, 22, '#111', 3); txt(g, 'MK.II', 0, -10, 18, '#1a1a24'); poly(g, [-90, -40, -60, -40, -60, -10, -90, 0], '#1a1a24', 0); }
      else if (k === 'mecha') { rr(g, -64, -100, 128, 110, 16, hurt ? '#fff' : '#202430', 4); rr(g, -50, -90, 100, 30, 6, '#6aff4a', 3); txt(g, '1-UP', 0, -75, 16, '#0a2a0a'); rr(g, -40, -170, 80, 72, 14, hurt ? '#fff' : '#2a2e3a', 4); rr(g, -30, -146, 60, 18, 6, '#0a0a10', 2); g.drawImage(glow('106,255,74', 20), -30, -157); g.drawImage(glow('106,255,74', 20), 10, -157);
        g.fillStyle = '#6aff4a'; poly(g, [-44, -170, -20, -196, 0, -176, 20, -200, 44, -172], '#1a3a10', 3); ell(g, -50, -140, 16, 22, '#111', 3); ell(g, 50, -140, 16, 22, '#111', 3); rr(g, -104, -96, 34, 90, 12, '#202430', 4); rr(g, 70, -96, 34, 90, 12, '#202430', 4); ell(g, 87, 0, 20, 20, '#6aff4a', 3); ell(g, -87, 0, 20, 20, '#6aff4a', 3); }
      else { var big = k === 'bouncer', col = hurt ? '#fff' : B.col, w = big ? 76 : 58;
        rr(g, -w, -110, w * 2, 130, 20, col, 4); poly(g, [-14, -110, 14, -110, 0, -60], '#f2f2f2', 2.5); if (!big) poly(g, [-5, -102, 5, -102, 6, -62, 0, -54, -6, -62], k === 'suit' && B.n === 'KANZAKI' ? '#e8c040' : '#c8202a', 2);
        ell(g, 0, -140, big ? 30 : 26, big ? 30 : 28, '#e0b088', 4);
        if (big) { g.fillStyle = '#111'; g.fillRect(-28, -172, 56, 14); rr(g, -24, -150, 48, 12, 4, '#0a0a10', 0); g.lineWidth = 3; g.strokeStyle = INK; g.beginPath(); g.moveTo(-10, -124); g.lineTo(10, -124); g.stroke(); txt(g, 'STAFF', 0, -40, 14, '#ffd860'); }
        else { g.fillStyle = '#16121a'; g.beginPath(); g.ellipse(0, -158, 27, 14, 0, Math.PI, 0); g.fill(); poly(g, [-26, -158, 30, -160, 18, -170], '#16121a', 0); rr(g, -20, -146, 17, 9, 3, '#0a0a10', 0); rr(g, 3, -146, 17, 9, 3, '#0a0a10', 0); if (B.n === 'KANZAKI') { g.lineWidth = 2; g.strokeStyle = '#e8c040'; g.beginPath(); g.arc(0, -70, 14, 0.3, Math.PI - 0.3); g.stroke(); } }
        rr(g, w - 8, -100, 24, 70, 10, col, 4); rr(g, -w - 16, -100, 24, 70, 10, col, 4); if (B.atk && B.atk.k === 'shot') { rr(g, w - 14, -40, 40, 20, 4, '#3a3a44', 3); } }
      g.restore();
      /* weak point */
      if (!B.ko) { var wx = x + B.wp[0] * sc, wy = y + B.wp[1] * sc, pul = 0.6 + Math.sin(t * 8) * 0.4; g.globalAlpha = pul; g.lineWidth = 3; g.strokeStyle = '#ffd860'; g.beginPath(); g.arc(wx, wy, 16, 0, 7); g.stroke(); g.beginPath(); g.moveTo(wx - 22, wy); g.lineTo(wx - 10, wy); g.moveTo(wx + 10, wy); g.lineTo(wx + 22, wy); g.stroke(); g.globalAlpha = 1; }
      if (B.atk && B.atk.k === 'shot' && !B.ko) { var k2 = B.atk.t / B.atk.max, cy = y - 80 * sc; g.lineWidth = 4; g.strokeStyle = k2 < 0.3 ? '#ff2030' : 'rgba(255,216,96,.9)'; g.beginPath(); g.arc(x, cy, 30 + 120 * k2, 0, 7); g.stroke(); if (k2 < 0.35) otxt(g, 'DUCK!', x, cy - 40 - 120 * k2, 22, '#ff2030'); }
    }
    /* ---------- flow ---------- */
    function setupStage() { var S = STG[G.stage]; seed = 101 + G.stage * 977; layers = [paintArea(S, 0), paintArea(S, 1), paintArea(S, 2)]; area = 0; areas = 3; waveI = 0; boss = null; phase = 'waves'; trans = 0; transBg = null; en = []; thrown = []; fx = []; makeWaves(); timeL = 24; shots = 0; hits = 0; }
    function makeWaves() { var S = STG[G.stage], n = 3 + Math.min(2, G.stage >> 1), L = layers[area].slots; waves = [];
      for (var w = 0; w < n; w++) { var cnt = 2 + Math.min(3, ((G.stage + w + area) / 2) | 0), wv = [];
        for (var i = 0; i < cnt; i++) wv.push({ slot: (w * 2 + i * 3 + area) % L.length, type: S.types[(w + i + area) % S.types.length], d: i * (0.55 - G.stage * 0.05) });
        if ((w + area + G.stage) % 3 === 1) wv.push({ slot: (w + 4) % L.length, type: 'hostage', d: 0.8 }); waves.push(wv); } }
    function spawnWave() { var L = layers[area].slots; en = waves[waveI].map(function (q) { var sl = L[q.slot], hp = q.type === 'robot' ? 3 : q.type === 'biker' ? 2 : 1;
        return { type: q.type, x: sl[0] + (R() - 0.5) * 16, foot: sl[1], sc: sl[2], hp: hp, rise: 0, wait: q.d + 0.2, aim: 0, aimMax: aimTime(q.type), up: false, flash: 0, ko: false, koT: 0, koR: 0, ph: R() * 6, life: q.type === 'hostage' ? 2.6 : 99, hop: 0, slotI: q.slot }; }); }
    function aimTime(ty) { return Math.max(0.85, (ty === 'robot' ? 2.0 : ty === 'biker' ? 1.6 : 1.8) - G.stage * 0.18); }
    function startBoss() { var S = STG[G.stage], b = S.boss; phase = 'boss'; en = []; thrown = []; timeL = 45;
      boss = { n: b.n, kind: b.kind, col: b.col, hp: b.hp, max: b.hp, x: 181, y: b.kind === 'robot' ? 340 : 380, sc: b.kind === 'mecha' ? 1.1 : 1, vx: 40 + G.stage * 10, flash: 0, ko: false, koT: 0, atkCd: 1.6, atk: null, wp: b.kind === 'robot' ? [0, -90] : b.kind === 'mecha' ? [0, -75] : [0, b.kind === 'bouncer' ? -140 : -142] }; say(b.n, 1.6); tone(110, now(), 0.6, 'sawtooth', 0.1); }
    function say(m, d) { msg = m; msgT = d || 0.9; }
    G.start = function () { G.stage = 0; G.score = 0; lives = 3; ammo = 6; cover = false; inv = 0; hurtT = 0; combo = 0; comboT = 0; reloadT = 0; bonusAcc = 0; setupStage(); };
    G.cont = function () { lives = 3; ammo = 6; inv = 1.5; timeL = Math.max(timeL, 20); if (phase === 'boss' && boss) { boss.atk = null; boss.atkCd = 2; } else { en.forEach(function (E) { E.aim = 0; E.up = false; E.wait = 0.8; }); } };
    G.next = function () { G.stage++; ammo = 6; setupStage(); };
    G.bonus = function () { var acc = shots ? hits / shots : 0; return [['Accuracy ' + Math.round(acc * 100) + '%', Math.round(acc * 4000 * (1 + G.stage * 0.5)) | 0], ['Time left ' + Math.ceil(timeL) + 's', Math.round(timeL * 40 * (1 + G.stage * 0.3))], ['Lives left x' + lives, lives * 1000]]; };
    function hurt(why) { if (inv > 0) return; lives--; inv = 1.2; hurtT = 0.5; combo = 0; drum('k', now(), 0.6); tone(90, now(), 0.3, 'sawtooth', 0.12); say(why || 'HIT!', 0.8); }
    function reload() { if (ammo === 6 && reloadT <= 0) return; reloadT = 0.35; ammo = 6; tone(660, now(), 0.04, 'square', 0.04); tone(880, now() + 0.12, 0.05, 'square', 0.05); }
    G.press = function (k) { if (k === 'reload') reload(); if (k === 'duck') { cover = true; reload(); } };
    G.release = function (k) { if (k === 'duck') cover = false; };
    G.lit = function (k) { return k === 'reload' && ammo === 0 && ((now() * 4) | 0) % 2; };
    G.off = function () { reload(); };
    G.tap = function (x, y) {
      if (cover || reloadT > 0) return;
      if (ammo <= 0) { tone(200, now(), 0.03, 'square', 0.04); return; }
      ammo--; shots++; drum('s', now(), 0.35); tone(140, now(), 0.08, 'square', 0.05); fx.push({ k: 'shot', x: x, y: y, t: 0 });
      /* thrown things first */
      for (var i = 0; i < thrown.length; i++) { var T = thrown[i], rad = 10 + T.z * 26; if (!T.dead && Math.abs(x - T.x) < rad + 8 && Math.abs(y - T.y) < rad + 8) { T.dead = 1; hits++; addPts(150, x, y, 'SHOT DOWN'); fx.push({ k: 'burst', x: T.x, y: T.y, t: 0, c: '255,216,96' }); return; } }
      if (boss && !boss.ko) { var B = boss, wx = B.x + B.wp[0] * B.sc, wy = B.y + B.wp[1] * B.sc;
        if (Math.abs(x - wx) < 22 && Math.abs(y - wy) < 22) { B.hp -= 2; B.flash = 0.08; hits++; addPts(300, x, y, 'WEAK POINT'); }
        else if (Math.abs(x - B.x) < 90 * B.sc && y > B.y - 190 * B.sc && y < B.y + 40) { B.hp -= 1; B.flash = 0.06; hits++; addPts(100, x, y); }
        else return miss(x, y);
        if (B.hp <= 0) { B.ko = true; B.koT = 0; addPts(5000 + G.stage * 2500, B.x, B.y - 120, 'BOSS DOWN'); [0, 0.15, 0.3, 0.5].forEach(function (d) { drum('k', now() + d, 0.6); }); }
        return; }
      for (var j = en.length - 1; j >= 0; j--) { var E = en[j]; if (E.ko || E.rise < 0.5) continue; var sc = E.sc, by = E.foot + (1 - E.rise) * 120 * sc - 10 * sc, hx = E.x, hy = by - 114 * sc;
        var head = Math.abs(x - hx) < 22 * sc && Math.abs(y - hy) < 24 * sc, body = Math.abs(x - E.x) < 36 * sc && y > by - 96 * sc && y < by - 16 * sc;
        if (!head && !body) continue;
        hits++;
        if (E.type === 'hostage') { E.ko = true; E.koT = 0; E.koR = 0; G.score = Math.max(0, G.score - 1000); combo = 0; say('DON\u2019T SHOOT CIVILIANS! -1000', 1.2); tone(150, now(), 0.4, 'square', 0.08); return; }
        E.hp -= head ? 2 : 1; E.flash = 0.08;
        if (E.hp <= 0) { E.ko = true; E.koT = 0; E.koR = (x < E.x ? 1 : -1) * 0.5; var base = E.type === 'robot' ? 300 : E.type === 'biker' ? 200 : 100; addPts(base * (head ? 2 : 1), x, y, head ? 'HEAD SHOT' : null); fx.push({ k: 'stars', x: hx, y: hy, t: 0 }); }
        else { fx.push({ k: 'spark', x: x, y: y, t: 0 }); tone(1200, now(), 0.04, 'square', 0.03); }
        return; }
      miss(x, y);
    };
    function miss(x, y) { combo = 0; fx.push({ k: 'spark', x: x, y: y, t: 0 }); }
    function addPts(p, x, y, lab) { combo++; comboT = 2; var m = 1 + Math.min(4, Math.floor(combo / 5)) * 0.25, v = Math.round(p * m / 10) * 10; G.score += v; fx.push({ k: 'pts', x: x, y: y, t: 0, s: (lab ? lab + ' ' : '') + v }); }
    G.step = function (dt) {
      inv = Math.max(0, inv - dt); hurtT = Math.max(0, hurtT - dt); reloadT = Math.max(0, reloadT - dt); msgT = Math.max(0, (msgT || 0) - dt); comboT -= dt; if (comboT <= 0) combo = 0;
      fx.forEach(function (F) { F.t += dt; }); fx = fx.filter(function (F) { return F.t < (F.k === 'pts' ? 0.9 : 0.4); });
      if (trans > 0) { trans -= dt; if (trans <= 0) { transBg = null; } return; }
      timeL -= dt; if (timeL <= 0) { timeL = 12; hurt('TIME!'); }
      if (phase === 'waves') {
        if (!en.length) spawnWave();
        en.forEach(function (E) { E.flash = Math.max(0, E.flash - dt);
          if (E.ko) { E.koT += dt; E.rise = Math.max(0, E.rise - dt * 1.2); return; }
          if (E.wait > 0) { E.wait -= dt; return; }
          if (E.rise < 1 && !E.hop) { E.rise = Math.min(1, E.rise + dt * 4); if (E.rise >= 1) E.aim = E.aimMax; return; }
          if (E.type === 'hostage') { E.life -= dt; if (E.life <= 0) { E.hop = 1; } if (E.hop) { E.rise -= dt * 3; if (E.rise <= 0) { E.ko = true; E.koT = 1; } } return; }
          if (E.hop) { E.rise -= dt * 4; if (E.rise <= 0) { E.hop = 0; E.wait = 0.5 + R() * 0.6; var L = layers[area].slots, ns = L[(E.slotI + 2 + ((R() * 3) | 0)) % L.length]; E.slotI = L.indexOf(ns); E.x = ns[0] + (R() - 0.5) * 16; E.foot = ns[1]; E.sc = ns[2]; E.aimMax = aimTime(E.type); } return; }
          if (E.aim > 0) { E.aim -= dt; if (E.aim <= 0) { drum('s', now(), 0.25); fx.push({ k: 'flash', x: E.x, y: E.foot - 60 * E.sc, t: 0 }); if (!cover) hurt('HIT!'); else { fx.push({ k: 'pts', x: 181, y: 430, t: 0, s: 'COVER!' }); } E.hop = 1; } } });
        en = en.filter(function (E) { return !(E.ko && E.koT > 0.8); });
        if (!en.length) { waveI++; if (waveI >= waves.length) { area++; if (area >= areas) { startBoss(); } else { transBg = layers[area - 1].bg; trans = 0.8; waveI = 0; makeWaves(); timeL = Math.min(40, timeL + 14); say('TIME EXTEND +14', 1); tone(1046, now(), 0.12, 'square', 0.05); } } }
      } else if (phase === 'boss' && boss) { var B = boss; B.flash = Math.max(0, B.flash - dt);
        if (B.ko) { B.koT += dt; if (B.koT > 2.2) return G.stage >= STG.length - 1 ? 'win' : 'clear'; }
        else { B.x += B.vx * dt; if (B.x < 110 || B.x > 252) { B.vx = -B.vx; B.x = clamp(B.x, 110, 252); }
          if (B.atk) { B.atk.t -= dt; if (B.atk.t <= 0) { if (B.atk.k === 'shot') { drum('k', now(), 0.5); drum('s', now(), 0.4); fx.push({ k: 'flash', x: B.x, y: B.y - 80, t: 0 }); if (!cover) hurt('BIG HIT!'); else fx.push({ k: 'pts', x: 181, y: 430, t: 0, s: 'COVER!' }); } B.atk = null; B.atkCd = Math.max(0.9, 2.0 - G.stage * 0.2); } }
          else { B.atkCd -= dt; if (B.atkCd <= 0) { var r = R(); if (r < 0.45) B.atk = { k: 'shot', t: 1.3 - G.stage * 0.06, max: 1.3 - G.stage * 0.06 };
            else if (r < 0.85) { var nT = 1 + (G.stage >> 1); for (var i = 0; i < nT; i++) thrown.push({ x: B.x + (i - nT / 2) * 30, y: B.y - 120, z: 0, vx: (R() - 0.5) * 120, k: B.kind === 'robot' || B.kind === 'mecha' ? 'bolt' : 'bottle', sp: 0.75 + G.stage * 0.06 }); B.atkCd = 1.5; tone(500, now(), 0.15, 'triangle', 0.05); }
            else { var L = layers[2].slots; en = [0, 1].map(function (q) { var sl = L[q]; return { type: 'goon', x: sl[0], foot: sl[1], sc: sl[2], hp: 1, rise: 0, wait: 0.2 * q, aim: 0, aimMax: aimTime('goon'), flash: 0, ko: false, koT: 0, koR: 0, ph: 0, life: 99, hop: 0, slotI: q, minion: 1 }; }); B.atkCd = 2.2; } } } }
        en.forEach(function (E) { E.flash = Math.max(0, E.flash - dt); if (E.ko) { E.koT += dt; return; } if (E.wait > 0) { E.wait -= dt; return; } if (E.rise < 1) { E.rise = Math.min(1, E.rise + dt * 4); if (E.rise >= 1) E.aim = E.aimMax; return; } if (E.aim > 0) { E.aim -= dt; if (E.aim <= 0) { if (!cover) hurt('HIT!'); E.ko = true; E.koT = 0.5; } } });
        en = en.filter(function (E) { return !(E.ko && E.koT > 0.8); });
        thrown.forEach(function (T) { T.z += dt * T.sp; T.x += T.vx * dt; T.y += (300 - T.y) * dt * 1.2; if (T.z >= 1 && !T.dead) { T.dead = 1; if (!cover) hurt(T.k === 'bolt' ? 'ZAPPED!' : 'BONK!'); fx.push({ k: 'burst', x: T.x, y: T.y, t: 0, c: '255,120,80' }); } });
        thrown = thrown.filter(function (T) { return !T.dead; });
      }
      if (lives <= 0) return 'dead';
    };
    G.draw = function (g, t) {
      var L = layers[Math.min(area, 2)], sh = hurtT > 0 ? (Math.random() - 0.5) * 10 : 0;
      g.save(); g.translate(sh, 0);
      if (trans > 0 && transBg) { var k = 1 - trans / 0.8; K.blit(g, transBg, -k * SW, 0); K.blit(g, L.bg, SW - k * SW, 0); g.restore(); return drawHud(g, t); }
      K.blit(g, L.bg, 0, 0);
      if (boss) bossFig(g, boss, t);
      en.forEach(function (E) { if (E.rise > 0) figure(g, E, t); });
      K.blit(g, L.fg, 0, 0);
      thrown.forEach(function (T) { var rad = 8 + T.z * 26; g.save(); g.translate(T.x, T.y); g.rotate(t * 8); if (T.k === 'bolt') { g.drawImage(glow('120,200,255', rad * 2 | 0), -rad * 2, -rad * 2); ell(g, 0, 0, rad * 0.6, rad * 0.6, '#c8f0ff', 2); } else { rr(g, -rad * 0.3, -rad, rad * 0.6, rad * 2, rad * 0.25, '#3a8a4a', 2); } g.restore(); });
      fx.forEach(function (F) { var a = 1 - F.t / (F.k === 'pts' ? 0.9 : 0.4);
        if (F.k === 'shot') { g.globalAlpha = a; g.drawImage(glow('255,240,180', 22), F.x - 22, F.y - 22); g.globalAlpha = 1; }
        else if (F.k === 'spark') { g.strokeStyle = 'rgba(255,230,150,' + a + ')'; g.lineWidth = 2; for (var i = 0; i < 5; i++) { var an = i * 1.3 + F.x, r1 = 4 + F.t * 40; g.beginPath(); g.moveTo(F.x + Math.cos(an) * r1, F.y + Math.sin(an) * r1); g.lineTo(F.x + Math.cos(an) * (r1 + 6), F.y + Math.sin(an) * (r1 + 6)); g.stroke(); } }
        else if (F.k === 'burst') { g.globalAlpha = a; g.drawImage(glow(F.c, 40), F.x - 40, F.y - 40); g.globalAlpha = 1; }
        else if (F.k === 'flash') { g.globalAlpha = a; g.drawImage(glow('255,200,80', 30), F.x - 30, F.y - 30); g.globalAlpha = 1; }
        else if (F.k === 'stars') { for (var s2 = 0; s2 < 3; s2++) { var an2 = t * 6 + s2 * 2.1; txt(g, '\u2605', F.x + Math.cos(an2) * 18, F.y - 10 + Math.sin(an2) * 6 - F.t * 30, 14, 'rgba(255,216,96,' + a + ')'); } }
        else if (F.k === 'pts') { g.globalAlpha = a; otxt(g, F.s, F.x, F.y - F.t * 40, 13, '#fff'); g.globalAlpha = 1; } });
      g.restore();
      drawHud(g, t);
    };
    function drawHud(g, t) {
      if (cover) { g.fillStyle = 'rgba(10,6,20,.45)'; g.fillRect(0, 0, SW, SH); rr(g, -10, 330, SW + 20, 190, 14, '#5a3a24', 4); g.fillStyle = 'rgba(0,0,0,.25)'; for (var i = 0; i < 6; i++) g.fillRect(0, 350 + i * 26, SW, 4); otxt(g, 'COVER', SW / 2, 300, 22, '#ffd860'); }
      if (hurtT > 0) { g.fillStyle = 'rgba(255,30,40,' + hurtT * 0.6 + ')'; g.fillRect(0, 0, SW, SH); }
      /* timer */
      rr(g, SW / 2 - 40, 30, 80, 30, 8, 'rgba(0,0,0,.55)', 2, timeL < 6 ? '#ff2030' : '#ffd860'); K.mono(g, (Math.max(0, timeL)).toFixed(1), SW / 2, 45, 16, timeL < 6 ? '#ff4050' : '#ffd860', 'center');
      for (var l = 0; l < 3; l++) { txt(g, '\u2665', 16 + l * 20, 44, 18, l < lives ? '#ff4a5a' : 'rgba(255,255,255,.18)'); }
      for (var a = 0; a < 6; a++) { var on = a < ammo; rr(g, SW - 18 - a * 13, SH - 40, 9, 26, 3, on ? '#ffd860' : 'rgba(255,255,255,.15)', 1.5); if (on) { g.fillStyle = '#c8702a'; g.fillRect(SW - 18 - a * 13, SH - 22, 9, 8); } }
      if (ammo === 0 && !cover && ((t * 4) | 0) % 2) otxt(g, 'RELOAD!', SW / 2, SH - 60, 24, '#ff4050');
      if (boss) { rr(g, 60, 66, SW - 120, 16, 6, 'rgba(0,0,0,.6)', 2); rr(g, 62, 68, Math.max(0, (SW - 124) * boss.hp / boss.max), 12, 5, '#ff4a5a', 0); txt(g, boss.n, SW / 2, 92, 11, '#fff'); }
      else txt(g, 'AREA ' + (Math.min(area, 2) + 1) + '-' + (Math.min(waveI, (waves || []).length - 1) + 1), SW / 2, 72, 10, 'rgba(255,255,255,.75)');
      if (combo >= 5) otxt(g, combo + ' CHAIN', SW - 60, 44, 13, '#7aff9a');
      if (msgT > 0) otxt(g, msg, SW / 2, 120, msg.length > 18 ? 15 : 22, '#fff');
    }
    /* ---------- title / attract ---------- */
    var TT = null;
    G.title = function (g, t) {
      if (!TT) TT = K.layer(SW, SH, function (q) { var sg = q.createLinearGradient(0, 0, 0, SH); sg.addColorStop(0, '#0a0418'); sg.addColorStop(0.6, '#3a0a2a'); sg.addColorStop(1, '#ff4a5a'); q.fillStyle = sg; q.fillRect(0, 0, SW, SH);
        building(q, -10, 250, 90, 250, '#140818', 'rgba(255,120,150,.5)'); building(q, 80, 200, 70, 300, '#180a1e', 'rgba(255,216,96,.45)'); building(q, 220, 220, 80, 280, '#140818', 'rgba(90,216,255,.45)'); building(q, 300, 270, 80, 230, '#180a1e', 'rgba(255,120,150,.5)');
        q.fillStyle = '#0a0408'; for (var i = 0; i < 4; i++) { var x = 40 + i * 90; ell(q, x, 400, 16, 18, '#0a0408', 0); rr(q, x - 26, 416, 52, 90, 14, '#0a0408', 0); }
        otxt(q, '\u4e2d\u592e', SW / 2, 70, 30, '#ffd860'); otxt(q, 'CHUO', SW / 2, 120, 56, '#fff', 'center', '#ff4a5a'); otxt(q, 'CRISIS', SW / 2, 176, 56, '#ff4a5a');
        gunShape(q, SW / 2, 236, 2.2, '#ffd860'); txt(q, 'A LIGHT-GUN SHOWDOWN IN 5 STAGES', SW / 2, 290, 12, '#fff'); txt(q, 'Tap to shoot \u00b7 hold DUCK to take cover', SW / 2, 312, 12, '#ffd0d8', 'center', 700); });
      K.blit(g, TT, 0, 0);
      var cx = SW / 2 + Math.sin(t * 1.3) * 120, cy = 400 + Math.cos(t * 1.7) * 30; g.lineWidth = 2.5; g.strokeStyle = '#ff4a5a'; g.beginPath(); g.arc(cx, cy, 16, 0, 7); g.moveTo(cx - 24, cy); g.lineTo(cx + 24, cy); g.moveTo(cx, cy - 24); g.lineTo(cx, cy + 24); g.stroke();
    };
    G.dispose = function () { layers = null; TT = null; };
    G._tg = function () { /* test/clip hook: live targets in screen coords */ var o = []; thrown.forEach(function (T) { if (!T.dead) o.push([T.x, T.y, 't']); });
      if (boss && !boss.ko) o.push([boss.x + boss.wp[0] * boss.sc, boss.y + boss.wp[1] * boss.sc, 'b']);
      en.forEach(function (E) { if (E.ko || E.rise < 0.5 || E.type === 'hostage') return; var by = E.foot + (1 - E.rise) * 120 * E.sc - 10 * E.sc; o.push([E.x, by - 114 * E.sc, 'e']); }); return { t: o, ammo: ammo, cover: cover, reload: reloadT > 0 }; };
    G.dbg = function (o) { o = o || {}; if (o.lives) lives = o.lives; if (o.boss) { area = 2; startBoss(); } return { lives: lives, ammo: ammo, phase: phase, area: area, en: en.length, boss: boss && boss.hp }; };
    return G;
  };
  } catch (eTop) { try { console.warn('S2ARC gun init', eTop); } catch (e2) {} }
})();
