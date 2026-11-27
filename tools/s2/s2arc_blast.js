/* v6.5.64 Game Center cabinet: KITSUNE BLASTER (vertical shooter). v6564-arcade.
 * 5 stages, each with its own scrolling backdrop, enemy wave script and a boss. Power-ups: P (shot level 1-5), B (bomb), S (shield), 1UP.
 * Steer with the stick or drag anywhere on the screen. The ship fires on its own; BOMB clears bullets. */
(function () {
  try {
  var root = typeof window !== 'undefined' ? window : this;
  var A = root.FFF_S2ARC = root.FFF_S2ARC || { v: 1 };
  A.GAMES = A.GAMES || {}; A.CABS = A.CABS || {};
  A.CABS.shooter = { n: 'Kitsune Blaster', jp: '\u72d0\u30d6\u30e9\u30b9\u30bf\u30fc', col: '#ff5ac8', body: '#1a0e26', mq: ['#2a0a3a', '#0a0418'], deck: ['#2a1a3a', '#120a1e'],
    tiers: [20000, 60000, 150000],
    seed: [['JIN', 1.6], ['JIN', 1.42], ['JIN', 1.3], ['KNZ', 1.05], ['TTS', 0.84], ['BAN', 0.66], ['KDE', 0.5], ['OGT', 0.36], ['PNT', 0.24], ['CHY', 0.14]],
    mqArt: function (p, x, y, w, h) { for (var i = 0; i < 30; i++) { p.fillStyle = 'rgba(255,255,255,' + (0.2 + (i % 3) * 0.2) + ')'; p.fillRect(x + (i * 53) % w, y + (i * 29) % h, 2, 2); } } };
  A.GAMES.shooter = function (K, C) {
    var rr = K.rr, txt = K.txt, otxt = K.otxt, ell = K.ell, poly = K.poly, glow = K.glow, tone = K.tone, drum = K.drum, now = K.now, SW = K.SW, SH = K.SH, INK = K.INK, clamp = K.clamp, mono = K.mono;
    var STG = [
      { n: 'Chuo Skyline', sub: 'Over the night market', bg: 'city', boss: { n: 'TANUKI TANK', k: 'tank', hp: 140, col: '#8a6a4a' }, mix: ['dart', 'drone'] },
      { n: 'Canal Lights', sub: 'Lanterns on the water', bg: 'canal', boss: { n: 'KARAOKE MECHA', k: 'speaker', hp: 190, col: '#ff5ac8' }, mix: ['dart', 'drone', 'turret'] },
      { n: 'Hotel Chuo Heights', sub: 'Searchlights and helicopters', bg: 'hotel', boss: { n: 'NIGHT HELI', k: 'heli', hp: 240, col: '#3a4a5a' }, mix: ['drone', 'kami', 'turret', 'carrier'] },
      { n: 'Club Kitsune Storm', sub: 'Lasers on the dance floor', bg: 'club', boss: { n: 'DISCO DOOM', k: 'disco', hp: 300, col: '#c8c8e0' }, mix: ['dart', 'kami', 'drone', 'carrier'] },
      { n: 'Neon Game Center', sub: 'Final stage \u00b7 the gold cabinet', bg: 'neon', boss: { n: 'GOLD CABINET', k: 'cab', hp: 380, col: '#ffd860' }, mix: ['dart', 'drone', 'kami', 'turret', 'carrier'] }
    ];
    var G = { score: 0, stage: 0, stages: STG, how: ['Drag the screen or use the stick to fly', 'Your ship fires on its own', 'P powers up your shot (5 levels)', 'BOMB clears every bullet on screen', 'S = shield, B = bomb, 1UP = life', 'A boss waits at the end of each stage', 'No miss + bombs left = big bonus'],
      panel: { stick: { x: 96, y: 726, r: 46, c: '#ff5ac8' }, btns: [{ k: 'bomb', x: 300, y: 716, r: 40, l: 'BOMB', c: '#ffd860', fs: 14, dim: function () { return !bombs; } }] } };
    G.endLine = 'The gold cabinet is quiet. New high score.';
    var px, py, lives, bombs, lvl, shield, inv, fire, bul, eb, en, items, fx, t0, script, si, boss, scrollY, bgTile, bombT, msg, msgT, miss, drag = null, bossT, warnT;
    var SPR = {};
    function bspr(col, r) { var k = col + r; if (SPR[k]) return SPR[k]; return (SPR[k] = K.layer(r * 4, r * 4, function (g) { g.drawImage(glow(col, r * 2), 0, 0); ell(g, r * 2, r * 2, r * 0.75, r * 0.75, '#fff', 0); })); }
    function tile(k) { return K.layer(SW, SH, function (g) { var top = { city: ['#060818', '#1a1040'], canal: ['#04101e', '#0a2440'], hotel: ['#100a06', '#2a1a10'], club: ['#12041e', '#2a0a3a'], neon: ['#060410', '#1a0a2a'] }[k];
      var sg = g.createLinearGradient(0, 0, 0, SH); sg.addColorStop(0, top[0]); sg.addColorStop(1, top[1]); g.fillStyle = sg; g.fillRect(0, 0, SW, SH);
      for (var i = 0; i < 40; i++) { g.fillStyle = 'rgba(255,255,255,' + (0.15 + (i % 4) * 0.12) + ')'; g.fillRect((i * 89) % SW, (i * 61) % SH, 2, 2); }
      if (k === 'city') { for (var b = 0; b < 14; b++) { var x = (b * 61) % SW, y = (b * 113) % SH; rr(g, x, y, 40, 30, 3, '#1a1830', 1.5, '#2a2850'); g.fillStyle = 'rgba(255,200,120,.5)'; for (var w = 0; w < 6; w++) g.fillRect(x + 4 + (w % 3) * 12, y + 5 + ((w / 3) | 0) * 12, 7, 6); } }
      if (k === 'canal') { g.fillStyle = '#0a2a4a'; g.fillRect(120, 0, 122, SH); for (var l = 0; l < 10; l++) { g.drawImage(glow('255,140,60', 14), 110 - 14 + (l % 2) * 142, l * 50 - 14); } g.fillStyle = 'rgba(120,180,255,.2)'; for (var wv = 0; wv < 20; wv++) g.fillRect(130 + (wv * 37) % 100, (wv * 47) % SH, 20, 2); }
      if (k === 'hotel') { for (var r2 = 0; r2 < 6; r2++) { rr(g, 20 + (r2 % 3) * 110, r2 * 90, 90, 70, 4, '#2a1e14', 2, '#4a3420'); txt(g, 'H', 65 + (r2 % 3) * 110, r2 * 90 + 35, 22, 'rgba(255,216,96,.35)'); } }
      if (k === 'club') { for (var s = 0; s < 12; s++) for (var q = 0; q < 8; q++) { g.fillStyle = (s + q) % 3 === 0 ? 'rgba(255,90,200,.18)' : (s + q) % 3 === 1 ? 'rgba(90,216,255,.14)' : 'rgba(0,0,0,0)'; g.fillRect(q * 46, s * 42, 44, 40); } }
      if (k === 'neon') { for (var c2 = 0; c2 < 8; c2++) { var cx = 30 + (c2 % 4) * 100, cy = (c2 * 70) % SH; rr(g, cx, cy, 50, 60, 4, '#101828', 2, ['#ff5ac8', '#5ad8ff', '#ffd860', '#7aff9a'][c2 % 4]); } } }); }
    /* wave script for a stage: [time, pattern, type, n] */
    function mkScript(s) { var S = STG[s], L = [], tt = 1.5, pats = ['line', 'vee', 'sine', 'side', 'rain'];
      for (var w = 0; w < 14 + s * 2; w++) { var ty = S.mix[w % S.mix.length], p = pats[(w + s) % pats.length]; L.push([tt, p, ty, ty === 'carrier' ? 1 : ty === 'turret' ? 2 : 4 + Math.min(3, s)]); tt += Math.max(1.6, 3.6 - s * 0.35) + (ty === 'carrier' ? 1 : 0); }
      L.push([tt + 2, 'boss']); return L; }
    function setup() { var S = STG[G.stage]; bgTile = tile(S.bg); script = mkScript(G.stage); si = 0; t0 = 0; en = []; eb = []; bul = []; items = []; fx = []; boss = null; scrollY = 0; warnT = 0; miss = 0; px = SW / 2; py = SH - 80; }
    G.start = function () { G.stage = 0; G.score = 0; lives = 3; bombs = 2; lvl = 1; shield = 0; inv = 2; fire = 0; bombT = 0; setup(); };
    G.cont = function () { lives = 3; bombs = 2; inv = 2.5; eb = []; };
    G.next = function () { G.stage++; inv = 2; setup(); };
    G.bonus = function () { return [['No-miss bonus', miss ? 0 : 5000 + G.stage * 2000], ['Bombs left x' + bombs, bombs * 1000], ['Power level ' + lvl, lvl * 300]]; };
    function say(m, d) { msg = m; msgT = d || 1; }
    G.press = function (k) { if (k === 'bomb' && bombs > 0 && bombT <= 0) { bombs--; bombT = 1.2; inv = Math.max(inv, 1.4); eb = []; en.forEach(function (E) { E.hp -= 12; }); if (boss) boss.hp -= 18; drum('k', now(), 0.7); tone(110, now(), 0.8, 'sawtooth', 0.1); say('BOMB!', 0.8); } };
    G.tap = function (x, y, id) { drag = { id: id, x: x, y: y, px: px, py: py }; };
    G.drag = function (x, y, id) { if (!drag || drag.id !== id) return; px = clamp(drag.px + (x - drag.x) * 1.3, 14, SW - 14); py = clamp(drag.py + (y - drag.y) * 1.3, 60, SH - 30); };
    G.lift = function (id) { if (drag && drag.id === id) drag = null; };
    function addEn(ty, x, y, o) { var E = { ty: ty, x: x, y: y, t: 0, hp: { dart: 2, drone: 3, kami: 2, turret: 8, carrier: 26 }[ty] * (1 + G.stage * 0.25), fire: 1 + Math.random() * 2, pts: { dart: 100, drone: 150, kami: 120, turret: 300, carrier: 1500 }[ty], flash: 0 }; for (var q in o) E[q] = o[q]; en.push(E); }
    function wave(p, ty, n) { var i;
      if (ty === 'turret') { for (i = 0; i < n; i++) addEn('turret', 70 + i * (SW - 140) / Math.max(1, n - 1), -30, { vy: 50 }); return; }
      if (ty === 'carrier') { addEn('carrier', SW / 2, -50, { vy: 40, stop: 120 }); return; }
      for (i = 0; i < n; i++) {
        if (p === 'line') addEn(ty, 50 + i * (SW - 100) / (n - 1), -30 - i * 4, { vy: 120, vx: 0 });
        else if (p === 'vee') addEn(ty, SW / 2 + (i - (n - 1) / 2) * 40, -30 - Math.abs(i - (n - 1) / 2) * 30, { vy: 130, vx: 0 });
        else if (p === 'sine') addEn(ty, SW / 2, -30 - i * 44, { vy: 110, sine: 1, amp: 120, ph: 0 });
        else if (p === 'side') addEn(ty, i % 2 ? SW + 20 + i * 20 : -20 - i * 20, 80 + i * 20, { vx: i % 2 ? -150 : 150, vy: 40 });
        else addEn(ty, 30 + Math.random() * (SW - 60), -30 - i * 60, { vy: 160 + Math.random() * 60 }); } }
    function aimed(x, y, sp, spread, n, col) { var a = Math.atan2(py - y, px - x); for (var i = 0; i < n; i++) { var aa = a + (i - (n - 1) / 2) * spread; eb.push({ x: x, y: y, vx: Math.cos(aa) * sp, vy: Math.sin(aa) * sp, c: col || '255,90,200' }); } }
    function ring(x, y, sp, n, off, col) { for (var i = 0; i < n; i++) { var a = off + i * Math.PI * 2 / n; eb.push({ x: x, y: y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp, c: col || '255,216,96' }); } }
    function startBoss() { var b = STG[G.stage].boss; warnT = 2.2; boss = { n: b.n, k: b.k, hp: b.hp, max: b.hp, col: b.col, x: SW / 2, y: -80, t: 0, ph: 0, flash: 0, ko: 0 }; tone(80, now(), 1.2, 'sawtooth', 0.1); say('WARNING', 2); }
    function hitP() { if (inv > 0) return; if (shield) { shield = 0; inv = 1; tone(600, now(), 0.2, 'square', 0.06); fx.push({ k: 'ring', x: px, y: py, t: 0 }); return; }
      lives--; miss++; inv = 2.2; lvl = Math.max(1, lvl - 1); eb = []; drum('k', now(), 0.7); tone(70, now(), 0.6, 'sawtooth', 0.1); fx.push({ k: 'boom', x: px, y: py, t: 0, r: 40 }); }
    function kill(E) { G.score += E.pts; fx.push({ k: 'boom', x: E.x, y: E.y, t: 0, r: E.ty === 'carrier' ? 50 : 24 }); drum('s', now(), 0.25);
      var r = Math.random(); if (E.ty === 'carrier' || r < 0.06) items.push({ k: E.ty === 'carrier' ? 'P' : ['P', 'P', 'B', 'S'][(Math.random() * 4) | 0], x: E.x, y: E.y, vy: 60 }); else if (r < 0.065 && G.stage > 1) items.push({ k: '1UP', x: E.x, y: E.y, vy: 60 }); }
    G.step = function (dt) {
      var I = G.in; t0 += dt; scrollY = (scrollY + dt * (60 + G.stage * 10)) % SH; inv = Math.max(0, inv - dt); bombT = Math.max(0, bombT - dt); msgT = Math.max(0, (msgT || 0) - dt); warnT = Math.max(0, warnT - dt);
      var sp = 230; px = clamp(px + (I.sx || 0) * sp * dt, 14, SW - 14); py = clamp(py + (I.sy || 0) * sp * dt, 60, SH - 30);
      /* shots */
      fire -= dt; if (fire <= 0) { fire = 0.11; var pat = [[0], [-7, 7], [-10, 0, 10], [-14, -5, 5, 14], [-16, -8, 0, 8, 16]][lvl - 1]; pat.forEach(function (o, i) { bul.push({ x: px + o, y: py - 18, vx: lvl >= 3 ? o * 6 : 0, vy: -620, d: 1 }); }); if (lvl >= 5) { bul.push({ x: px - 20, y: py, vx: -90, vy: -560, d: 1 }); bul.push({ x: px + 20, y: py, vx: 90, vy: -560, d: 1 }); } if (((t0 * 9) | 0) % 2) tone(1400, now(), 0.025, 'square', 0.01); }
      bul.forEach(function (B) { B.x += B.vx * dt; B.y += B.vy * dt; }); bul = bul.filter(function (B) { return B.y > -10 && !B.dead; });
      while (si < script.length && t0 >= script[si][0]) { var S0 = script[si]; if (S0[1] === 'boss') startBoss(); else wave(S0[1], S0[2], S0[3]); si++; }
      en.forEach(function (E) { E.t += dt; E.flash = Math.max(0, E.flash - dt);
        if (E.sine) { E.y += E.vy * dt; E.x = SW / 2 + Math.sin(E.t * 2 + E.ph) * E.amp; } else if (E.ty === 'kami' && E.t > 0.8 && !E.dive) { E.dive = 1; var a = Math.atan2(py - E.y, px - E.x); E.vx = Math.cos(a) * 260; E.vy = Math.sin(a) * 260; } else { E.x += (E.vx || 0) * dt; E.y += (E.vy || 0) * dt; }
        if (E.stop && E.y > E.stop) { E.vy = 0; E.y = E.stop; E.x = SW / 2 + Math.sin(E.t * 0.8) * 100; }
        E.fire -= dt; if (E.fire <= 0 && E.y > 20 && E.y < SH - 120) { E.fire = (E.ty === 'turret' ? 1.3 : E.ty === 'carrier' ? 0.9 : 2.9) / (1 + G.stage * 0.22); if (E.ty === 'carrier') ring(E.x, E.y, 120, 10 + G.stage * 2, E.t, '255,216,96'); else if (E.ty !== 'kami') aimed(E.x, E.y, 150 + G.stage * 15, 0.2, E.ty === 'turret' ? 3 : 1); }
        bul.forEach(function (B) { if (!B.dead && Math.abs(B.x - E.x) < (E.ty === 'carrier' ? 40 : 16) && Math.abs(B.y - E.y) < (E.ty === 'carrier' ? 28 : 16)) { B.dead = 1; E.hp -= B.d; E.flash = 0.05; } });
        if (inv <= 0 && Math.abs(E.x - px) < 18 && Math.abs(E.y - py) < 18) { hitP(); E.hp = 0; }
        if (E.hp <= 0 && !E.dead) { E.dead = 1; kill(E); } });
      en = en.filter(function (E) { return !E.dead && E.y < SH + 40 && E.x > -80 && E.x < SW + 80; });
      if (boss) { var B = boss; B.t += dt; B.flash = Math.max(0, B.flash - dt);
        if (B.ko) { B.ko += dt; if (((B.ko * 10) | 0) % 2) fx.push({ k: 'boom', x: B.x + (Math.random() - 0.5) * 120, y: B.y + (Math.random() - 0.5) * 60, t: 0, r: 30 }); if (B.ko > 2.4) return G.stage >= STG.length - 1 ? 'win' : 'clear'; }
        else { if (B.y < 110) B.y += 40 * dt; else { B.x = SW / 2 + Math.sin(B.t * 0.7) * 100; B.ph += dt;
            var stage = G.stage, hp = B.hp / B.max, rate = 1 + (1 - hp) * 0.8;
            if (B.ph > 1.1 / rate) { B.ph = 0; var m = ((B.t / 4) | 0) % 3;
              if (B.k === 'tank') { if (m === 0) aimed(B.x, B.y + 30, 170, 0.18, 5); else if (m === 1) ring(B.x, B.y, 130, 12, B.t, '255,160,60'); else { aimed(B.x - 50, B.y + 20, 200, 0, 1); aimed(B.x + 50, B.y + 20, 200, 0, 1); } }
              else if (B.k === 'speaker') { ring(B.x, B.y, 120 + m * 20, 14, B.t * 2, '255,90,200'); if (m === 2) aimed(B.x, B.y, 220, 0.12, 3, '90,216,255'); }
              else if (B.k === 'heli') { aimed(B.x, B.y + 20, 240, 0.08, 3 + m, '255,255,160'); if (m === 1) ring(B.x, B.y, 100, 16, 0, '255,90,90'); }
              else if (B.k === 'disco') { for (var s2 = 0; s2 < 3; s2++) ring(B.x, B.y, 110 + s2 * 25, 10, B.t * 1.7 + s2 * 0.3, ['255,90,200', '90,216,255', '255,216,96'][s2]); }
              else { ring(B.x, B.y, 140, 18, B.t * 2, '255,216,96'); aimed(B.x, B.y, 260, 0.1, 5, '122,255,154'); if (m === 2) ring(B.x, B.y, 90, 24, -B.t, '255,90,200'); } } }
          bul.forEach(function (Bu) { if (!Bu.dead && Math.abs(Bu.x - B.x) < 60 && Math.abs(Bu.y - B.y) < 40) { Bu.dead = 1; B.hp -= Bu.d; B.flash = 0.04; G.score += 10; } });
          if (B.hp <= 0) { B.ko = 0.01; eb = []; G.score += 10000 + G.stage * 5000; say(B.n + ' DOWN', 2); drum('k', now(), 0.8); } } }
      eb.forEach(function (Bu) { Bu.x += Bu.vx * dt; Bu.y += Bu.vy * dt; if (inv <= 0 && Math.abs(Bu.x - px) < 6 && Math.abs(Bu.y - py) < 7) { Bu.dead = 1; hitP(); } });
      eb = eb.filter(function (Bu) { return !Bu.dead && Bu.x > -10 && Bu.x < SW + 10 && Bu.y > -10 && Bu.y < SH + 10; }); if (eb.length > 220) eb.splice(0, eb.length - 220);
      items.forEach(function (It) { It.y += It.vy * dt; if (Math.abs(It.x - px) < 22 && Math.abs(It.y - py) < 22) { It.got = 1; if (It.k === 'P') { if (lvl < 5) lvl++; else G.score += 1000; say(lvl < 5 ? 'POWER UP' : 'MAX POWER +1000', 0.8); } else if (It.k === 'B') { bombs = Math.min(5, bombs + 1); say('BOMB +1', 0.8); } else if (It.k === 'S') { shield = 1; say('SHIELD', 0.8); } else { lives++; say('1UP!', 1); } tone(1046, now(), 0.1, 'square', 0.06); tone(1568, now() + 0.08, 0.15, 'square', 0.06); } });
      items = items.filter(function (It) { return !It.got && It.y < SH + 20; });
      fx.forEach(function (F) { F.t += dt; }); fx = fx.filter(function (F) { return F.t < 0.5; });
      if (lives <= 0) return 'dead';
    };
    function ship(g, x, y, t) { g.save(); g.translate(x, y); poly(g, [0, -20, 9, -4, 18, 8, 6, 6, 0, 14, -6, 6, -18, 8, -9, -4], '#ff9a3a', 2.5); poly(g, [-9, -4, -14, -18, -5, -8], '#ff9a3a', 2); poly(g, [9, -4, 14, -18, 5, -8], '#ff9a3a', 2); ell(g, 0, -4, 4, 6, '#7fe8ff', 1.5);
      g.drawImage(glow('255,160,60', 12 + (((t * 20) | 0) % 2) * 3), -14, 6); g.restore(); }
    function enemy(g, E, t) { var c = E.flash > 0 ? '#fff' : null; g.save(); g.translate(E.x, E.y);
      if (E.ty === 'dart') { poly(g, [0, 14, -14, -8, 0, -2, 14, -8], c || '#ff5ac8', 2); }
      else if (E.ty === 'drone') { ell(g, 0, 0, 13, 10, c || '#5ad8ff', 2); ell(g, 0, 0, 5, 5, '#1a1220', 0); g.fillStyle = '#ff3040'; g.fillRect(-2, -2, 4, 4); poly(g, [-13, 0, -20, -6, -18, 4], c || '#3a8ab0', 1.5); poly(g, [13, 0, 20, -6, 18, 4], c || '#3a8ab0', 1.5); }
      else if (E.ty === 'kami') { g.rotate(Math.atan2(E.vy || 1, E.vx || 0) - Math.PI / 2); poly(g, [0, 16, -8, -10, 8, -10], c || '#ffd860', 2); g.drawImage(glow('255,120,40', 10), -10, -22); }
      else if (E.ty === 'turret') { rr(g, -16, -16, 32, 32, 6, c || '#6a6a7a', 2.5); ell(g, 0, 0, 9, 9, '#3a3a44', 2); var a = Math.atan2(py - E.y, px - E.x); g.rotate(a - Math.PI / 2); rr(g, -3, 0, 6, 18, 2, '#2a2a34', 1.5); }
      else { rr(g, -44, -22, 88, 44, 10, c || '#7a5aa0', 3); rr(g, -30, -30, 60, 14, 6, c || '#9a7ac0', 2.5); ell(g, -26, 6, 7, 7, '#ff3040', 2); ell(g, 26, 6, 7, 7, '#ff3040', 2); txt(g, 'P', 0, 2, 16, '#ffd860'); }
      g.restore(); }
    function bossDraw(g, B, t) { var c = B.flash > 0 ? '#fff' : B.col; g.save(); g.translate(B.x, B.y);
      if (B.k === 'tank') { rr(g, -70, -30, 140, 60, 12, c, 3); rr(g, -40, -54, 80, 34, 10, '#6a4a2a', 3); ell(g, 0, -40, 14, 14, '#f0d8a0', 2.5); g.fillStyle = INK; g.fillRect(-6, -44, 3, 3); g.fillRect(3, -44, 3, 3); rr(g, -6, 20, 12, 30, 3, '#3a3a44', 2.5); [-50, 50].forEach(function (q) { ell(g, q, -10, 12, 16, '#e8302a', 2); g.drawImage(glow('255,90,60', 18), q - 18, -28); }); }
      else if (B.k === 'speaker') { rr(g, -64, -50, 128, 100, 12, '#2a1a3a', 3); [-30, 30].forEach(function (q) { ell(g, q, 0, 24, 24, c, 3); ell(g, q, 0, 10 + Math.sin(t * 12) * 3, 10 + Math.sin(t * 12) * 3, '#1a1220', 0); }); txt(g, '\u266a', 0, -36, 18, '#ffd860'); }
      else if (B.k === 'heli') { rr(g, -50, -24, 100, 48, 20, c, 3); rr(g, 40, -6, 70, 10, 4, c, 2.5); g.strokeStyle = 'rgba(220,220,240,.6)'; g.lineWidth = 4; g.beginPath(); g.moveTo(-90 * Math.cos(t * 30), -30); g.lineTo(90 * Math.cos(t * 30), -30); g.stroke(); rr(g, -30, -14, 30, 18, 6, '#9ad8f0', 2); g.drawImage(glow('255,255,200', 30), -30, 10); }
      else if (B.k === 'disco') { ell(g, 0, 0, 56, 56, c, 3); for (var i = 0; i < 24; i++) { g.fillStyle = (i + ((t * 6) | 0)) % 3 === 0 ? '#ff5ac8' : (i % 3 === 1 ? '#5ad8ff' : '#f2f2ff'); g.fillRect(-40 + (i % 6) * 14, -32 + ((i / 6) | 0) * 16, 11, 13); } g.lineWidth = 3; g.strokeStyle = INK; g.beginPath(); g.moveTo(0, -56); g.lineTo(0, -100); g.stroke(); }
      else { rr(g, -60, -70, 120, 140, 10, '#3a2a08', 4); rr(g, -50, -60, 100, 24, 6, c, 3); txt(g, 'JIN', 0, -48, 16, '#3a2a08'); rr(g, -44, -28, 88, 60, 6, '#0a0a10', 3); mono(g, '999990', 0, 2, 13, '#ffd860', 'center'); rr(g, -50, 40, 100, 20, 4, '#5a4a20', 2.5); ell(g, -20, 50, 6, 6, '#ff3040', 2); ell(g, 10, 50, 6, 6, '#5ad8ff', 2); }
      g.restore(); }
    G.draw = function (g, t) {
      K.blit(g, bgTile, 0, scrollY - SH); K.blit(g, bgTile, 0, scrollY);
      items.forEach(function (It) { g.drawImage(glow(It.k === 'P' ? '255,90,90' : It.k === 'B' ? '255,216,96' : It.k === 'S' ? '90,216,255' : '122,255,154', 18), It.x - 18, It.y - 18); rr(g, It.x - 11, It.y - 9, 22, 18, 5, '#fff', 2); txt(g, It.k, It.x, It.y, It.k.length > 1 ? 8 : 12, INK); });
      en.forEach(function (E) { enemy(g, E, t); });
      if (boss) bossDraw(g, boss, t);
      bul.forEach(function (B) { g.fillStyle = '#ffe9a0'; g.fillRect(B.x - 1.5, B.y - 8, 3, 12); });
      if (!(inv > 0 && ((t * 14) | 0) % 2)) ship(g, px, py, t); if (shield) { g.strokeStyle = 'rgba(90,216,255,.8)'; g.lineWidth = 2; g.beginPath(); g.arc(px, py, 24, 0, 7); g.stroke(); }
      var bs = null; for (var i = 0; i < eb.length; i++) { var Bu = eb[i]; bs = bspr(Bu.c, 5); g.drawImage(bs, Bu.x - 10, Bu.y - 10, 20, 20); }
      fx.forEach(function (F) { var a = 1 - F.t / 0.5; g.globalAlpha = a; if (F.k === 'boom') { g.drawImage(glow('255,180,80', F.r), F.x - F.r, F.y - F.r); } else { g.strokeStyle = '#5ad8ff'; g.lineWidth = 3; g.beginPath(); g.arc(F.x, F.y, 20 + F.t * 80, 0, 7); g.stroke(); } g.globalAlpha = 1; });
      if (bombT > 0.8) { g.fillStyle = 'rgba(255,255,255,' + (bombT - 0.8) * 2 + ')'; g.fillRect(0, 0, SW, SH); }
      /* HUD */
      for (var l = 0; l < Math.min(6, lives); l++) { g.save(); g.translate(14 + l * 18, 42); g.scale(0.45, 0.45); poly(g, [0, -20, 9, -4, 18, 8, 0, 14, -18, 8, -9, -4], '#ff9a3a', 3); g.restore(); }
      for (var b = 0; b < bombs; b++) { ell(g, SW - 16 - b * 16, 42, 6, 6, '#ffd860', 2); }
      txt(g, 'PWR ' + lvl, SW - 16, 60, 9, '#ff5a5a', 'right');
      if (boss && !boss.ko) { rr(g, 50, 52, SW - 100, 10, 4, 'rgba(0,0,0,.6)', 2); rr(g, 52, 54, (SW - 104) * Math.max(0, boss.hp / boss.max), 6, 3, '#ff5ac8', 0); txt(g, boss.n, SW / 2, 72, 10, '#fff'); }
      if (warnT > 0 && ((t * 4) | 0) % 2) { rr(g, 0, 210, SW, 60, 0, 'rgba(255,30,40,.35)', 0); otxt(g, 'WARNING', SW / 2, 240, 34, '#ff4a5a'); }
      else if (msgT > 0) otxt(g, msg, SW / 2, 160, 20, '#fff');
    };
    var TT = null;
    G.title = function (g, t) {
      if (!TT) TT = K.layer(SW, SH, function (q) { var sg = q.createLinearGradient(0, 0, 0, SH); sg.addColorStop(0, '#04020e'); sg.addColorStop(1, '#3a0a4a'); q.fillStyle = sg; q.fillRect(0, 0, SW, SH);
        for (var i = 0; i < 90; i++) { q.fillStyle = 'rgba(255,255,255,' + (0.2 + (i % 4) * 0.2) + ')'; q.fillRect((i * 89) % SW, (i * 47) % SH, 2, 2); }
        otxt(q, '\u72d0\u30d6\u30e9\u30b9\u30bf\u30fc', SW / 2, 58, 22, '#ff5ac8'); otxt(q, 'KITSUNE', SW / 2, 104, 46, '#fff', 'center', '#ff5ac8'); otxt(q, 'BLASTER', SW / 2, 156, 46, '#ff5ac8'); txt(q, '5 STAGES \u00b7 5 BOSSES \u00b7 POWER UP TO LEVEL 5', SW / 2, 200, 11, '#fff'); });
      K.blit(g, TT, 0, 0);
      ship(g, SW / 2 + Math.sin(t) * 80, 380, t); for (var i = 0; i < 5; i++) { g.fillStyle = '#ffe9a0'; g.fillRect(SW / 2 + Math.sin(t) * 80 - 1, 360 - ((t * 400 + i * 50) % 250), 3, 12); }
      [0, 1, 2].forEach(function (i) { enemy(g, { ty: 'dart', x: 100 + i * 80, y: 260 + Math.sin(t * 2 + i) * 20, flash: 0 }, t); });
    };
    G.dispose = function () { TT = null; bgTile = null; SPR = {}; };
    G.dbg = function (o) { o = o || {}; if (o.lives) { lives = 99; } if (o.boss) { si = script.length - 1; t0 = script[si][0]; } if (o.lvl) lvl = o.lvl; return { lives: lives, en: en.length, eb: eb.length, t0: t0, boss: boss && boss.hp }; };
    G._s = function () { return { px: px, py: py, en: en, eb: eb, items: items, boss: boss, set: function (x, y) { px = x; py = y; } }; };
    return G;
  };
  } catch (eTop) { try { console.warn('S2ARC blast init', eTop); } catch (e2) {} }
})();
