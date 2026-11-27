/* v6.5.64 Game Center cabinet: EMBER RUN (side-scrolling platformer). v6564-arcade.
 * You are Ember, a little fox-fire spirit. Run right across 3 worlds x 2 levels (rooftops, the shotengai, shrine hill),
 * stomp or flame the crows and tanuki, collect lanterns, and reach the torii gate at the end of each level. */
(function () {
  try {
  var root = typeof window !== 'undefined' ? window : this;
  var A = root.FFF_S2ARC = root.FFF_S2ARC || { v: 1 };
  A.GAMES = A.GAMES || {}; A.CABS = A.CABS || {};
  A.CABS.ember = { n: 'Ember Run', jp: '\u706b\u306e\u7c89\u30e9\u30f3', col: '#ffd860', body: '#22160a', mq: ['#3a2006', '#140a02'], deck: ['#3a2a14', '#1a1208'],
    tiers: [12000, 28000, 45000],
    seed: [['JIN', 1.4], ['KDE', 1.18], ['CHY', 1.0], ['PNT', 0.84], ['TSO', 0.68], ['BAN', 0.54], ['KNZ', 0.42], ['CLK', 0.3], ['OGT', 0.2], ['TTS', 0.12]],
    mqArt: function (p, x, y, w, h) { for (var i = 0; i < 8; i++) { p.fillStyle = 'rgba(232,48,58,.5)'; p.beginPath(); p.ellipse(x + 24 + i * 46, y + 14, 6, 8, 0, 0, 7); p.fill(); } } };
  A.GAMES.ember = function (K, C) {
    var rr = K.rr, txt = K.txt, otxt = K.otxt, ell = K.ell, poly = K.poly, glow = K.glow, tone = K.tone, drum = K.drum, now = K.now, SW = K.SW, SH = K.SH, INK = K.INK, clamp = K.clamp, mono = K.mono;
    var TS = 24, ROWS = 21, BASE = 17;
    var LV = [
      { n: '1-1 Rooftop Dash', sub: 'World 1 \u00b7 Chuo rooftops', w: 'roof', len: 150, seed: 11, diff: 0 },
      { n: '1-2 Water-Tank Hop', sub: 'World 1 \u00b7 higher, wider gaps', w: 'roof', len: 170, seed: 23, diff: 1 },
      { n: '2-1 Shotengai Awnings', sub: 'World 2 \u00b7 under the arcade roof', w: 'shop', len: 170, seed: 37, diff: 2 },
      { n: '2-2 Hot Vent Alley', sub: 'World 2 \u00b7 mind the steam', w: 'shop', len: 190, seed: 41, diff: 3 },
      { n: '3-1 Bamboo Steps', sub: 'World 3 \u00b7 shrine hill', w: 'shrine', len: 190, seed: 59, diff: 4 },
      { n: '3-2 The Fox Shrine', sub: 'World 3 \u00b7 final level', w: 'shrine', len: 210, seed: 67, diff: 5 }
    ];
    var G = { score: 0, stage: 0, stages: LV, stageWord: 'LEVEL', how: ['You are Ember, a fox-fire spirit', 'Run right and reach the torii gate', '\u25c0 \u25b6 to run \u00b7 JUMP (hold = higher)', 'FLAME shoots a fireball', 'Stomp crows and tanuki from above', 'Collect lanterns: 50 = extra life', 'Mid-level torii = checkpoint'],
      panel: { btns: [{ k: 'l', x: 58, y: 722, r: 36, l: '\u25c0', c: '#ffd860', fs: 24, slide: 1 }, { k: 'r', x: 142, y: 722, r: 36, l: '\u25b6', c: '#ffd860', fs: 24, slide: 1 }, { k: 'fire', x: 252, y: 750, r: 30, l: 'FLAME', c: '#ff6a3a', fs: 11 }, { k: 'jump', x: 328, y: 704, r: 38, l: 'JUMP', c: '#7fe8ff', fs: 14 }] } };
    G.endLine = 'Ember reached the Fox Shrine. The lanterns are lit.';
    var map, ents, lan, px, py, vx, vy, onG, face, lives, lanN, camX, timeL, fx, inv, fb, fireCd, cpX, deadT, L, bgA, bgB, jumpHeld, coyote, goalX, cpTX, petals;
    var seed = 1; function R() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
    function tAt(c, r) { if (c < 0 || r < 0) return 1; if (r >= ROWS) return 0; var col = map[c]; return col ? col[r] | 0 : 1; }
    function build() { L = LV[G.stage]; seed = L.seed; var W = L.len; map = []; ents = []; lan = [];
      var h = BASE, c = 0, d = L.diff;
      function col(top, plat) { var a = []; for (var r = 0; r < ROWS; r++) a.push(r >= top ? 1 : 0); if (plat) a[plat] = 2; map.push(a); return a; }
      function gapCol() { var a = []; for (var r = 0; r < ROWS; r++) a.push(0); map.push(a); return a; }
      while (c < 8) { col(h); c++; }
      cpTX = (W / 2) | 0;
      while (c < W - 12) { var k = R(), len;
        if (c >= cpTX - 2 && c <= cpTX + 2) { col(h); c++; continue; }
        if (k < 0.22) { len = 3 + ((R() * 3) | 0); for (var i = 0; i < len; i++) { var a = col(h); if (i === 1 && R() < 0.5 + d * 0.08) ents.push({ k: 'tanuki', x: (c) * TS, y: (h - 1) * TS, vx: -40 - d * 6, alive: 1 }); c++; } }
        else if (k < 0.42) { len = 2 + Math.min(3, (R() * (2 + d * 0.5)) | 0); for (var g2 = 0; g2 < len; g2++) { gapCol(); if (g2 === ((len / 2) | 0)) lan.push({ x: c * TS + 12, y: (h - 4) * TS }); c++; } }
        else if (k < 0.56) { var up = R() < 0.5 && h > 12 ? -1 : h < 18 ? 1 : -1; for (var s = 0; s < 3; s++) { h = clamp(h + up, 11, 18); col(h); c++; } }
        else if (k < 0.72) { len = 4 + ((R() * 3) | 0); var ph = Math.max(3, h - 5 - ((R() * 2) | 0)), run = 0; for (var p = 0; p < len; p++) { var gp = p > 0 && p < len - 1 && run < 2 && R() < 0.35 + d * 0.06; run = gp ? run + 1 : 0; var b = gp ? gapCol() : col(h); for (var q = 0; q < 3 && p + q < len; q++); b[ph] = 2; if (p % 2) lan.push({ x: c * TS + 12, y: (ph - 1) * TS + 6 }); c++; } }
        else if (k < 0.84) { len = 4; for (var v = 0; v < len; v++) { var vc = col(h); if (v === 1 || (v === 2 && d >= 3)) { if (d >= 1) vc[h - 1] = 3; } c++; } lan.push({ x: (c - 2) * TS, y: (h - 4) * TS }); }
        else { len = 5; for (var f = 0; f < len; f++) { col(h); if (f === 2) ents.push({ k: 'crow', x: c * TS, y: (h - 5) * TS, y0: (h - 5) * TS, vx: -60 - d * 8, t: R() * 6, alive: 1 }); lan.push({ x: c * TS + 12, y: (h - 2) * TS }); c++; } }
      }
      while (c < W) { col(h); c++; } goalX = (W - 6) * TS; for (var e = 0; e < 3; e++) lan.push({ x: (W - 10 + e) * TS, y: (h - 3) * TS });
      bgA = sky(L.w); bgB = far(L.w); }
    function sky(w) { return K.layer(SW, SH, function (g) { var c = { roof: ['#0a0620', '#3a1438'], shop: ['#1a0a10', '#4a1a1a'], shrine: ['#06101e', '#2a3a5a'] }[w]; var sg = g.createLinearGradient(0, 0, 0, SH); sg.addColorStop(0, c[0]); sg.addColorStop(1, c[1]); g.fillStyle = sg; g.fillRect(0, 0, SW, SH);
      if (w !== 'shop') { for (var i = 0; i < 50; i++) { g.fillStyle = 'rgba(255,255,255,' + (0.2 + (i % 3) * 0.2) + ')'; g.fillRect((i * 83) % SW, (i * 41) % 260, 2, 2); } ell(g, 290, 90, 30, 30, w === 'shrine' ? '#f8f0d8' : '#ffd860', 0); }
      else { for (var b = 0; b < 8; b++) { g.fillStyle = 'rgba(255,255,255,.06)'; g.fillRect(b * 50, 0, 6, 120); } g.fillStyle = '#2a1a1a'; g.fillRect(0, 0, SW, 40); for (var l = 0; l < 6; l++) { g.drawImage(glow('255,90,60', 18), 20 + l * 64 - 18, 40); ell(g, 20 + l * 64, 58, 7, 9, '#e8303a', 2); } } }); }
    function far(w) { return K.layer(SW * 2, SH, function (g) { for (var i = 0; i < 14; i++) { var x = i * 54, hh = 120 + (i * 37) % 90;
      if (w === 'roof') { rr(g, x, SH - hh - 60, 48, hh + 60, 0, '#1a1030', 0); g.fillStyle = 'rgba(255,210,120,.35)'; for (var wy = 0; wy < 5; wy++) g.fillRect(x + 8 + (wy % 2) * 18, SH - hh - 40 + wy * 26, 10, 12); }
      else if (w === 'shop') { rr(g, x, SH - 260, 50, 200, 0, i % 2 ? '#3a1a1a' : '#2a1a2a', 0); rr(g, x + 4, SH - 250, 42, 20, 4, ['#ff5a5a', '#5ad8ff', '#ffd860'][i % 3], 0); }
      else { g.fillStyle = '#16301e'; for (var bb = 0; bb < 4; bb++) g.fillRect(x + bb * 12, SH - 340 + (bb * 23) % 60, 5, 300); g.fillStyle = 'rgba(30,70,40,.8)'; ell(g, x + 20, SH - 330, 30, 12, 'rgba(30,70,40,.8)', 0); } } }); }
    var TILE = {}, mapCv = null;
    function tile(k, w) { var key = k + w; if (TILE[key]) return TILE[key]; return (TILE[key] = K.layer(TS, TS, function (g) {
      var P = { roof: ['#4a3a5a', '#6a4a7a', '#2a2036'], shop: ['#5a3a2a', '#8a5a3a', '#3a2418'], shrine: ['#5a5a5a', '#7a7a7a', '#3a3a3a'] }[w];
      if (k === 'top') { g.fillStyle = P[0]; g.fillRect(0, 0, TS, TS); g.fillStyle = P[1]; g.fillRect(0, 0, TS, 7); g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(0, 7, TS, 2); if (w === 'roof') { g.fillStyle = 'rgba(255,255,255,.12)'; g.fillRect(2, 2, 8, 2); } if (w === 'shrine') { g.fillStyle = '#3a7a3a'; g.fillRect(0, 0, TS, 4); } }
      else if (k === 'fill') { g.fillStyle = P[2]; g.fillRect(0, 0, TS, TS); g.fillStyle = 'rgba(255,255,255,.05)'; g.fillRect(0, 0, TS, 1); g.fillRect(0, 12, TS, 1); g.fillRect(12, 0, 1, 12); g.fillRect(4, 12, 1, 12); }
      else if (k === 'plat') { rr(g, 1, 2, TS - 2, 12, 3, w === 'shop' ? ['#e8403a', '#3a8ae8', '#f2c020'][0] : w === 'shrine' ? '#c8302a' : '#8a6a4a', 2); g.fillStyle = 'rgba(255,255,255,.25)'; g.fillRect(3, 4, TS - 6, 2); }
      else { g.fillStyle = '#3a3a44'; g.fillRect(0, 10, TS, 14); for (var i = 0; i < 3; i++) { g.fillStyle = '#ff6a3a'; poly(g, [i * 8, 12, i * 8 + 4, 0, i * 8 + 8, 12], '#ff8a3a', 1.5); } } })); }
    function bakeMap() {
      var w = map.length * TS, h = ROWS * TS, c, r, col, x, top, v;
      if (mapCv) { mapCv.width = 0; mapCv.height = 0; }
      mapCv = document.createElement('canvas'); mapCv.width = w; mapCv.height = h;
      var mg = mapCv.getContext('2d');
      for (c = 0; c < map.length; c++) {
        col = map[c]; if (!col) continue;
        x = c * TS; top = true;
        for (r = 0; r < ROWS; r++) {
          v = col[r]; if (!v) { top = true; continue; }
          if (v === 1) { K.blit(mg, tile(top ? 'top' : 'fill', L.w), x, r * TS); top = false; }
          else if (v === 2) { K.blit(mg, tile('plat', L.w), x, r * TS); top = true; }
          else { K.blit(mg, tile('vent', L.w), x, r * TS); top = true; }
        }
      }
    }
    function setup() { build(); bakeMap(); px = 3 * TS; py = (BASE - 1) * TS; vx = vy = 0; onG = false; face = 1; camX = 0; timeL = 150 + G.stage * 10; fx = []; fb = []; inv = 1; fireCd = 0; cpX = px; deadT = 0; petals = []; }
    G.start = function () { G.stage = 0; G.score = 0; lives = 3; lanN = 0; setup(); };
    G.cont = function () { lives = 3; respawn(); };
    G.next = function () { G.stage++; setup(); };
    G.bonus = function () { return [['Time left ' + Math.ceil(timeL), Math.ceil(timeL) * 20], ['Goal', 1000 + G.stage * 500]]; };
    function respawn() { px = cpX; camX = clamp(px - SW * 0.4, 0, map.length * TS - SW); fb = []; var c = (px / TS) | 0; for (var r = 0; r < ROWS; r++) if (tAt(c, r)) { py = (r - 1) * TS; break; } vx = vy = 0; inv = 2; deadT = 0; }
    G.press = function (k) { if (k === 'jump') { jumpHeld = true; if (onG || coyote > 0) { vy = -560; onG = false; coyote = 0; tone(523, now(), 0.08, 'triangle', 0.05); tone(784, now() + 0.05, 0.06, 'triangle', 0.04); } }
      if (k === 'fire' && fireCd <= 0) { fireCd = 0.35; fb.push({ x: px + face * 12, y: py - 14, vx: face * 300, vy: 0, t: 0 }); tone(300, now(), 0.1, 'sawtooth', 0.04); } };
    G.release = function (k) { if (k === 'jump') jumpHeld = false; };
    function solid(x, y) { var t = tAt(Math.floor(x / TS), Math.floor(y / TS)); return t === 1 || t === 2; }
    function hazard(x, y) { return tAt(Math.floor(x / TS), Math.floor(y / TS)) === 3; }
    function die(why) { if (deadT > 0 || inv > 0 && why !== 'pit') return; lives--; deadT = 1.4; vy = -420; drum('k', now(), 0.5); tone(392, now(), 0.15, 'square', 0.06); tone(262, now() + 0.15, 0.3, 'square', 0.06); }
    G.step = function (dt) {
      var I = G.in; timeL -= dt; fireCd -= dt; inv = Math.max(0, inv - dt); coyote = Math.max(0, (coyote || 0) - dt);
      fx.forEach(function (F) { F.t += dt; }); fx = fx.filter(function (F) { return F.t < 0.6; });
      if (deadT > 0) { deadT -= dt; vy += 1400 * dt; py += vy * dt; if (deadT <= 0) { if (lives <= 0) return 'dead'; respawn(); } return; }
      if (timeL <= 0) { timeL = 30; die('time'); }
      var want = (I.r ? 1 : 0) - (I.l ? 1 : 0); if (want) face = want; var acc = onG ? 1100 : 700; vx += (want * 175 - vx) * Math.min(1, acc * dt / 175);
      vy += (vy < 0 && jumpHeld ? 900 : 1700) * dt; vy = Math.min(vy, 700);
      /* horizontal */
      var nx = px + vx * dt, hw = 8; if (vx > 0 && (solid(nx + hw, py - 4) || solid(nx + hw, py - 20))) { nx = Math.floor((nx + hw) / TS) * TS - hw - 0.01; vx = 0; } if (vx < 0 && (solid(nx - hw, py - 4) || solid(nx - hw, py - 20))) { nx = Math.floor((nx - hw) / TS + 1) * TS + hw + 0.01; vx = 0; }
      px = Math.max(camX + 8, nx);
      /* vertical */
      var ny = py + vy * dt, was = onG; onG = false;
      if (vy >= 0 && (solid(px - hw + 1, ny) || solid(px + hw - 1, ny))) { ny = Math.floor(ny / TS) * TS; vy = 0; onG = true; }
      else if (vy < 0 && (solid(px - hw + 1, ny - 22) || solid(px + hw - 1, ny - 22))) { ny = Math.floor((ny - 22) / TS + 1) * TS + 22; vy = 0; }
      if (was && !onG && vy >= 0) coyote = 0.09; py = ny;
      if (hazard(px, py - 2) || hazard(px, py + 1)) die('vent');
      if (py > ROWS * TS + 40) { die('pit'); }
      /* camera */
      camX = Math.max(camX, clamp(px - SW * 0.4, 0, map.length * TS - SW));
      /* checkpoint + goal */
      if (cpX < cpTX * TS && px > cpTX * TS) { cpX = cpTX * TS; tone(988, now(), 0.15, 'square', 0.06); fx.push({ k: 'txt', x: px, y: py - 50, t: 0, s: 'CHECKPOINT' }); }
      if (px >= goalX) { G.score += 0; return G.stage >= LV.length - 1 ? 'win' : 'clear'; }
      /* lanterns */
      lan.forEach(function (Ln) { if (!Ln.got && Math.abs(Ln.x - px) < 16 && Math.abs(Ln.y - (py - 12)) < 20) { Ln.got = 1; lanN++; G.score += 50; tone(1318, now(), 0.06, 'triangle', 0.05); fx.push({ k: 'spark', x: Ln.x, y: Ln.y, t: 0 }); if (lanN % 50 === 0) { lives++; fx.push({ k: 'txt', x: px, y: py - 50, t: 0, s: '1UP!' }); tone(1568, now() + 0.1, 0.2, 'square', 0.06); } } });
      /* enemies */
      ents.forEach(function (E) { if (!E.alive) { E.dt = (E.dt || 0) + dt; return; } if (Math.abs(E.x - px) > SW * 1.2) return;
        if (E.k === 'tanuki') { var ex = E.x + E.vx * dt, ahead = E.vx > 0 ? ex + 10 : ex - 10; if (solid(ahead, E.y - 10) || !solid(ahead, E.y + 4)) E.vx = -E.vx; else E.x = ex; }
        else { E.t += dt; E.x += E.vx * dt; E.y = E.y0 + Math.sin(E.t * 3) * 26; }
        var dx = E.x - px, dy = (E.y - 10) - (py - 12);
        if (Math.abs(dx) < 18 && Math.abs(dy) < 20) { if (vy > 60 && py - 10 < E.y - 8) { E.alive = 0; vy = -380; G.score += 200; drum('s', now(), 0.3); fx.push({ k: 'txt', x: E.x, y: E.y - 30, t: 0, s: '200' }); } else die('hit'); } });
      fb.forEach(function (F) { F.t += dt; F.x += F.vx * dt; F.vy += 900 * dt; F.y += F.vy * dt; if (solid(F.x, F.y + 6)) { F.vy = -260; F.y -= 2; } if (solid(F.x + Math.sign(F.vx) * 6, F.y)) F.dead = 1;
        ents.forEach(function (E) { if (E.alive && Math.abs(E.x - F.x) < 16 && Math.abs(E.y - 10 - F.y) < 18) { E.alive = 0; F.dead = 1; G.score += 150; fx.push({ k: 'spark', x: E.x, y: E.y - 10, t: 0 }); drum('s', now(), 0.25); } }); });
      fb = fb.filter(function (F) { return !F.dead && F.t < 1.4; });
      if (L.w === 'shrine' && petals.length < 14 && Math.random() < 0.2) petals.push({ x: Math.random() * SW, y: -10, v: 40 + Math.random() * 40, ph: Math.random() * 6 });
      petals.forEach(function (Pt) { Pt.y += Pt.v * dt; Pt.ph += dt * 2; }); petals = petals.filter(function (Pt) { return Pt.y < SH; });
    };
    function ember(g, x, y, t, f) { var run = Math.abs(vx) > 20 && onG, bob = run ? Math.abs(Math.sin(t * 16)) * 3 : 0; g.save(); g.translate(x, y - bob); g.scale(f, 1);
      g.drawImage(glow('255,170,60', 22), -22, -34);
      /* flame tail */ var tw = Math.sin(t * 10) * 3; poly(g, [-6, -10, -22, -18 + tw, -26, -30 + tw, -16, -24, -10, -16], '#ff8a2a', 2); poly(g, [-9, -12, -20, -20 + tw, -15, -18], '#ffd860', 0);
      ell(g, 0, -11, 10, 9, '#ff9a3a', 2.5); ell(g, 2, -7, 6, 4, '#fff3d8', 0);
      ell(g, 6, -22, 8, 7, '#ff9a3a', 2.5); poly(g, [1, -27, 3, -36, 7, -28], '#ff9a3a', 2); poly(g, [8, -28, 12, -36, 13, -26], '#ff9a3a', 2); poly(g, [11, -22, 17, -20, 11, -18], '#fff3d8', 1.5);
      g.fillStyle = INK; g.fillRect(8, -24, 2, 3); ell(g, 16, -20, 1.5, 1.5, INK, 0);
      var lg = run ? Math.sin(t * 16) * 4 : 0; rr(g, -6 + lg, -4, 5, 6, 2, '#c85a1a', 1.5); rr(g, 3 - lg, -4, 5, 6, 2, '#c85a1a', 1.5);
      g.restore(); }
    function lantern(g, x, y, t) { g.drawImage(glow('255,90,60', 14), x - 14, y - 14); ell(g, x, y, 6, 8, '#e8303a', 2); g.fillStyle = '#2a1a1a'; g.fillRect(x - 3, y - 10, 6, 2); g.fillRect(x - 3, y + 8, 6, 2); }
    function enemyD(g, E, t) { g.save(); g.translate(E.x, E.y); if (!E.alive) { g.globalAlpha = Math.max(0, 1 - (E.dt || 0) * 2); g.scale(1, 0.4); }
      if (E.k === 'tanuki') { var f = E.vx > 0 ? 1 : -1; g.scale(f, 1); ell(g, 0, -10, 12, 10, '#8a6a4a', 2.5); ell(g, 6, -20, 8, 7, '#8a6a4a', 2.5); rr(g, 2, -24, 10, 5, 2, '#3a2a1a', 0); ell(g, 9, -21, 1.5, 1.5, '#fff', 0); ell(g, -12, -8, 6, 4, '#6a4a2a', 2); ell(g, 0, -7, 6, 5, '#e8d8b8', 0); txt(g, '\u2620', 0, -32, 1, 'rgba(0,0,0,0)'); rr(g, -14, -18, 8, 10, 3, '#f2e0b0', 1.5); }
      else { var fl = Math.sin(t * 14) * 6; ell(g, 0, -10, 10, 7, '#1a1a24', 2); poly(g, [-4, -12, -18, -18 - fl, -8, -8], '#2a2a34', 1.5); poly(g, [4, -12, 18, -18 - fl, 8, -8], '#2a2a34', 1.5); poly(g, [-10, -12, -16, -10, -10, -8], '#ffd040', 1); ell(g, -5, -12, 1.5, 1.5, '#ff3040', 0); }
      g.restore(); }
    G.draw = function (g, t) {
      K.blit(g, bgA, 0, 0); var fo = -(camX * 0.3) % (SW * 2); K.blit(g, bgB, fo, 0); if (fo + SW * 2 < SW) K.blit(g, bgB, fo + SW * 2, 0);
      g.save(); g.translate(-Math.round(camX), 0);
      if (mapCv) g.drawImage(mapCv, 0, 0);
      var c0 = Math.floor(camX / TS), c1 = Math.min(map.length - 1, c0 + Math.ceil(SW / TS) + 1);
      /* vent steam still flickers live; solid tiles come from the baked strip */
      for (var c = c0; c <= c1; c++) { var col = map[c]; if (!col) continue; var x = c * TS;
        for (var r = 0; r < ROWS; r++) { if (col[r] !== 3) continue; if (((t * 3 + c) | 0) % 3 === 0) { g.globalAlpha = 0.4; g.drawImage(glow('255,255,255', 14), x - 2, r * TS - 26); g.globalAlpha = 1; } } }
      /* checkpoint torii + goal gate */
      var cx = cpTX * TS, cy = colTop(cpTX); torii(g, cx, cy, 0.8, cpX >= cx); var gx = goalX + TS, gy = colTop((goalX / TS | 0) + 1); torii(g, gx, gy, 1.5, true); otxt(g, 'GOAL', gx, gy - 110, 16, '#ffd860');
      lan.forEach(function (Ln) { if (!Ln.got && Ln.x > camX - 20 && Ln.x < camX + SW + 20) lantern(g, Ln.x, Ln.y + Math.sin(t * 3 + Ln.x) * 2, t); });
      ents.forEach(function (E) { if (E.x > camX - 30 && E.x < camX + SW + 30 && (E.alive || (E.dt || 0) < 0.5)) enemyD(g, E, t); });
      fb.forEach(function (F) { g.drawImage(glow('255,140,40', 14), F.x - 14, F.y - 14); ell(g, F.x, F.y, 5, 5, '#ffd860', 1.5); });
      if (!(inv > 0 && ((t * 12) | 0) % 2) || deadT > 0) ember(g, px, py, t, face);
      fx.forEach(function (F) { var a = 1 - F.t / 0.6; if (F.k === 'spark') { g.globalAlpha = a; g.drawImage(glow('255,216,96', 18), F.x - 18, F.y - 18); g.globalAlpha = 1; } else { g.globalAlpha = a; otxt(g, F.s, F.x, F.y - F.t * 40, 13, '#fff'); g.globalAlpha = 1; } });
      g.restore();
      petals.forEach(function (Pt) { ell(g, Pt.x + Math.sin(Pt.ph) * 10, Pt.y, 3, 2, 'rgba(255,190,210,.8)', 0); });
      /* HUD */
      lantern(g, 18, 42, t); txt(g, '\u00d7' + lanN, 30, 42, 13, '#fff', 'left'); ember(g, SW / 2 - 30, 52, 0, 1); txt(g, '\u00d7' + lives, SW / 2 - 14, 42, 13, '#fff', 'left');
      txt(g, 'TIME ' + Math.max(0, Math.ceil(timeL)), SW - 12, 42, 13, timeL < 30 ? '#ff4a5a' : '#ffd860', 'right');
      var pr = clamp(px / goalX, 0, 1); rr(g, 60, SH - 16, SW - 120, 6, 3, 'rgba(255,255,255,.2)', 0); rr(g, 60, SH - 16, (SW - 120) * pr, 6, 3, '#ffd860', 0); ell(g, 60 + (SW - 120) * (cpTX * TS / goalX), SH - 13, 4, 4, cpX >= cpTX * TS ? '#7aff9a' : '#c8302a', 1.5);
    };
    function colTop(c) { for (var r = 0; r < ROWS; r++) if (tAt(c, r) === 1) return r * TS; return BASE * TS; }
    function torii(g, x, y, s, lit) { g.save(); g.translate(x, y); g.scale(s, s); var c = lit ? '#e8302a' : '#7a3a3a'; rr(g, -26, -60, 7, 60, 2, c, 2); rr(g, 19, -60, 7, 60, 2, c, 2); rr(g, -34, -66, 68, 8, 3, c, 2); rr(g, -30, -52, 60, 5, 2, c, 2); rr(g, -38, -72, 76, 6, 3, '#2a1a1a', 2); if (lit) g.drawImage(glow('255,120,60', 30), -30, -90); g.restore(); }
    var TT = null;
    G.title = function (g, t) {
      if (!TT) TT = K.layer(SW, SH, function (q) { var sg = q.createLinearGradient(0, 0, 0, SH); sg.addColorStop(0, '#0a0620'); sg.addColorStop(1, '#5a2a1a'); q.fillStyle = sg; q.fillRect(0, 0, SW, SH);
        for (var i = 0; i < 40; i++) { q.fillStyle = 'rgba(255,255,255,.5)'; q.fillRect((i * 83) % SW, (i * 41) % 200, 2, 2); }
        for (var c = 0; c < 16; c++) { var h = 360 + ((c * 7) % 3) * 24 - (c > 10 ? 40 : 0); if (c === 5 || c === 6) continue; q.fillStyle = '#3a2a4a'; q.fillRect(c * 24, h, 24, SH - h); q.fillStyle = '#6a4a7a'; q.fillRect(c * 24, h, 24, 6); }
        otxt(q, '\u706b\u306e\u7c89\u30e9\u30f3', SW / 2, 56, 22, '#ffd860'); otxt(q, 'EMBER', SW / 2, 104, 52, '#fff', 'center', '#ff6a1a'); otxt(q, 'RUN', SW / 2, 158, 52, '#ffd860');
        txt(q, 'A SIDE-SCROLLING PLATFORMER', SW / 2, 198, 12, '#fff'); txt(q, 'Run and jump Ember the fox-fire spirit', SW / 2, 220, 11, '#ffe0b0', 'center', 700); txt(q, 'across 3 worlds to the Fox Shrine gate', SW / 2, 238, 11, '#ffe0b0', 'center', 700); });
      K.blit(g, TT, 0, 0);
      var k = (t * 0.35) % 1, x = 20 + k * 320, y = 360 - (x > 120 && x < 168 ? Math.sin((x - 120) / 48 * Math.PI) * 60 + 0 : 0) - (x > 264 ? 0 : 0);
      var save = vx; vx = 100; onG = true; ember(g, x, y + (x > 264 ? 0 : 0), t, 1); vx = save; torii(g, 330, 336, 0.9, true);
      [[90, 320], [150, 280], [210, 330]].forEach(function (p) { lantern(g, p[0], p[1] + Math.sin(t * 3 + p[0]) * 3, t); });
    };
    G.dispose = function () { TT = null; TILE = {}; bgA = bgB = null; if (mapCv) { mapCv.width = mapCv.height = 0; } mapCv = null; };
    G.dbg = function (o) { o = o || {}; if (o.lives) { lives = 99; inv = 999; } if (o.x) { px = o.x; camX = Math.max(0, px - SW * 0.4); respawnAt(); } return { px: px, py: py, lives: lives, lan: lanN, len: map.length, goal: goalX }; };
    function respawnAt() { var c = (px / TS) | 0; for (var r = 0; r < ROWS; r++) if (tAt(c, r)) { py = (r - 1) * TS; break; } }
    G._s = function () { return { px: px, py: py, vx: vx, vy: vy, onG: onG, tAt: tAt, TS: TS, ents: ents, goalX: goalX, lan: lan, map: map }; };
    return G;
  };
  } catch (eTop) { try { console.warn('S2ARC ember init', eTop); } catch (e2) {} }
})();
