/* v6.5.64 Game Center cabinet: MIDNIGHT CHUO (top-down night street racer). v6564-arcade.
 * 7 night routes, each with its own road, traffic, hazards and look. Checkpoints extend the clock (run out = continue?).
 * Steer with the arrows (slide between them), BRAKE, NITRO (pick up N cans). Near misses at speed score big. */
(function () {
  try {
  var root = typeof window !== 'undefined' ? window : this;
  var A = root.FFF_S2ARC = root.FFF_S2ARC || { v: 1 };
  A.GAMES = A.GAMES || {}; A.CABS = A.CABS || {};
  A.CABS.street = { n: 'Midnight Chuo', jp: '\u771f\u591c\u4e2d\u592e\u7dda', col: '#7aff9a', body: '#0e1a14', mq: ['#0a2a1a', '#04100a'], deck: ['#1a2a22', '#0a140e'],
    tiers: [12000, 28000, 50000],
    seed: [['MSA', 1.38], ['JIN', 1.25], ['BAN', 1.06], ['MCH', 0.9], ['TTS', 0.72], ['KNZ', 0.58], ['HSE', 0.44], ['OGT', 0.32], ['PNT', 0.2], ['CHY', 0.12]],
    mqArt: function (p, x, y, w, h) { p.fillStyle = 'rgba(122,255,154,.18)'; for (var i = 0; i < 6; i++) p.fillRect(x + 10 + i * 64, y + h - 10, 40, 4); p.fillStyle = 'rgba(255,90,60,.5)'; p.fillRect(x + 8, y + 30, 10, 6); p.fillRect(x + w - 18, y + 30, 10, 6); },
    panelArt: function (p, PY) { var K = A.K; p.save(); p.globalAlpha = 0.9; K.ell(p, 105, PY + 102, 70, 70, null, 0); p.lineWidth = 12; p.strokeStyle = '#0a0a0e'; p.beginPath(); p.arc(105, PY + 102, 62, Math.PI * 1.05, Math.PI * 1.95); p.stroke(); p.lineWidth = 7; p.strokeStyle = '#2a2a32'; p.stroke(); p.restore(); K.txt(p, 'STEER', 105, PY + 40, 9, 'rgba(255,255,255,.55)'); } };

  A.GAMES.street = function (K, C) {
    var rr = K.rr, txt = K.txt, otxt = K.otxt, ell = K.ell, poly = K.poly, glow = K.glow, tone = K.tone, drum = K.drum, now = K.now, SW = K.SW, SH = K.SH, INK = K.INK, clamp = K.clamp, mono = K.mono;
    var ROUTES = [
      { n: 'Chuo-dori Run', sub: 'Pachinko lights \u00b7 taxis everywhere', len: 26000, time: 41, cp: 2, hw: 104, vmax: 560, traf: 1.0, kinds: ['taxi', 'sedan', 'taxi'], curve: [40, 0.00012, 20, 0.0004], side: 'city', road: '#2a2830', haz: ['cone'], sky: '#140c24' },
      { n: 'Canal Bridge', sub: 'Narrow deck \u00b7 watch the gusts', len: 24000, time: 37, cp: 2, hw: 80, vmax: 600, traf: 0.9, kinds: ['sedan', 'van'], curve: [24, 0.0002, 12, 0.0006], side: 'canal', road: '#30303a', haz: ['gust'], sky: '#0a1430' },
      { n: 'Ginko Shotengai', sub: 'Arcade roof \u00b7 cones and carts', len: 24000, time: 39, cp: 2, hw: 90, vmax: 580, traf: 0.8, kinds: ['scooter', 'sedan', 'van'], curve: [56, 0.00018, 30, 0.0005], side: 'arcade', road: '#3a3238', haz: ['cone', 'cart'], sky: '#1a0e18' },
      { n: 'Harbor Highway', sub: 'Four lanes \u00b7 trucks merging', len: 32000, time: 41, cp: 3, hw: 132, vmax: 700, traf: 1.3, kinds: ['truck', 'sedan', 'truck', 'bus'], curve: [30, 0.0001, 18, 0.00035], side: 'harbor', road: '#24262c', haz: ['merge'], sky: '#0a1020' },
      { n: 'Rain District', sub: 'Wet roads \u00b7 puddles steal your grip', len: 28000, time: 41, cp: 3, hw: 100, vmax: 620, traf: 1.1, kinds: ['taxi', 'sedan', 'van'], curve: [60, 0.00016, 26, 0.0005], side: 'rain', road: '#1e2430', haz: ['puddle'], wet: 1, sky: '#0a1018' },
      { n: 'Chuo Tunnel', sub: 'Orange lights \u00b7 oncoming lane', len: 28000, time: 39, cp: 3, hw: 112, vmax: 680, traf: 1.0, kinds: ['sedan', 'truck'], curve: [36, 0.00014, 14, 0.0004], side: 'tunnel', road: '#22201c', haz: ['oncoming'], dark: 1, sky: '#100a04' },
      { n: 'Neon Expressway', sub: 'Final route \u00b7 everyone is out tonight', len: 36000, time: 43, cp: 4, hw: 118, vmax: 760, traf: 1.5, kinds: ['taxi', 'truck', 'bus', 'sedan', 'police'], curve: [64, 0.00016, 34, 0.00045], side: 'neon', road: '#1c1a26', haz: ['cone', 'oncoming', 'puddle'], sky: '#0c0420' }
    ];
    var G = { score: 0, stage: 0, stages: ROUTES, stageWord: 'ROUTE', how: ['Steer with \u25c0 \u25b6 (slide between them)', 'Stay on the road, sidewalks slow you', 'Checkpoints add time: beat the clock', 'Pass cars close at speed: NEAR MISS', 'Grab N cans, tap NITRO to burn', 'BRAKE for the tight bends', '7 routes from Chuo-dori to the Expressway'],
      panel: { btns: [{ k: 'l', x: 62, y: 718, r: 38, l: '\u25c0', c: '#7aff9a', fs: 26, slide: 1 }, { k: 'r', x: 148, y: 718, r: 38, l: '\u25b6', c: '#7aff9a', fs: 26, slide: 1 }, { k: 'brake', x: 252, y: 744, r: 30, l: 'BRAKE', c: '#ff5a6a', fs: 11 }, { k: 'nitro', x: 328, y: 700, r: 34, l: 'NITRO', c: '#5ad8ff', fs: 12, dim: function () { return !nit; } }] } };
    G.endLine = 'Last train\u2019s gone. The night is yours.';
    var R, d, v, x, timeL, cars, objs, pick, fx, spin, inv, nit, nT, cpI, near, nearN, side, rainP, gust, gustT, msg, msgT, wobble, spawnD, sideD, offT;
    var PY = 400;
    function cx(z) { var c = R.curve; return SW / 2 + c[0] * Math.sin(z * c[1]) + c[2] * Math.sin(z * c[3] + 1.3); }
    function hwz(z) { return R.hw + (R.k === 'bridge' ? 0 : 0); }
    function setup() { R = ROUTES[G.stage]; d = 0; v = 200; x = cx(0); timeL = R.time; cars = []; objs = []; pick = []; fx = []; spin = 0; inv = 0; nT = 0; cpI = 1; near = {}; nearN = 0; gust = 0; gustT = 3; spawnD = 600; sideD = 0; offT = 0; side = buildSide(); }
    G.start = function () { G.stage = 0; G.score = 0; nit = 1; setup(); };
    G.cont = function () { timeL = Math.max(timeL, 20); v = 200; spin = 0; inv = 1.5; };
    G.next = function () { G.stage++; setup(); };
    G.bonus = function () { return [['Time left ' + Math.ceil(timeL) + 's', Math.ceil(timeL) * 120], ['Near misses x' + nearN, nearN * 60]]; };
    function say(m, t) { msg = m; msgT = t || 1; }
    G.press = function (k) { if (k === 'nitro' && nit > 0 && nT <= 0) { nit--; nT = 2.6; tone(220, now(), 0.6, 'sawtooth', 0.06); tone(440, now() + 0.1, 0.5, 'sawtooth', 0.05); say('NITRO!', 0.8); } };
    G.dir = function () {};
    /* side scenery tiles (painted once a route): a 362x600 strip that repeats */
    function buildSide() { var k = R.side; return K.layer(SW, 600, function (g) { g.fillStyle = R.sky; g.fillRect(0, 0, SW, 600);
      for (var i = 0; i < 6; i++) { var y = i * 100, L = i % 2;
        if (k === 'city' || k === 'neon' || k === 'rain') { [[0, 50], [SW - 50, 50]].forEach(function (q, j) { rr(g, q[0], y + 4, q[1], 92, 3, ['#2a1a34', '#1a2034', '#301a24'][(i + j) % 3], 2); for (var w = 0; w < 4; w++) { g.fillStyle = (i + w + j) % 3 ? 'rgba(255,220,140,.6)' : 'rgba(0,0,0,.4)'; g.fillRect(q[0] + 8 + (w % 2) * 20, y + 14 + ((w / 2) | 0) * 34, 12, 20); } });
          var nc = ['#ff5ac8', '#5ad8ff', '#ffd860', '#7aff9a'][i % 4]; g.drawImage(glow(K.hexRgb(nc), 30), (L ? SW - 50 : 50) - 30, y + 50 - 30); rr(g, L ? SW - 60 : 46, y + 40, 14, 40, 3, '#0a0610', 2, nc); }
        if (k === 'canal') { g.fillStyle = '#0a1a3a'; g.fillRect(0, y, SW, 100); g.fillStyle = 'rgba(120,180,255,.25)'; for (var wv = 0; wv < 5; wv++) g.fillRect((wv * 79 + i * 31) % SW, y + 20 + wv * 16, 30, 2); g.drawImage(glow('255,200,120', 16), 30, y + 40); g.drawImage(glow('255,200,120', 16), SW - 62, y + 40); }
        if (k === 'arcade') { g.fillStyle = '#2a1a20'; g.fillRect(0, y, SW, 100); [[0, 56], [SW - 56, 56]].forEach(function (q, j) { rr(g, q[0], y + 6, q[1], 88, 4, ['#6a2a2a', '#2a4a6a', '#5a4a1a'][(i + j) % 3], 2); rr(g, q[0] + 4, y + 10, q[1] - 8, 16, 3, ['#ff5a5a', '#5ad8ff', '#ffd860'][(i + j) % 3], 1.5); }); g.drawImage(glow('255,180,120', 24), SW / 2 - 24, y + 26); }
        if (k === 'harbor') { g.fillStyle = '#0a1424'; g.fillRect(0, y, SW, 100); [[4, '#c8402a'], [SW - 44, '#2a6ac8']].forEach(function (q, j) { rr(g, q[0], y + 10 + j * 20, 40, 70, 2, (i + j) % 2 ? q[1] : '#6a6a3a', 2); }); g.drawImage(glow('255,60,60', 8), 20, y + 4); }
        if (k === 'tunnel') { g.fillStyle = '#1a140c'; g.fillRect(0, y, SW, 100); g.fillStyle = '#3a3024'; g.fillRect(0, y, 40, 100); g.fillRect(SW - 40, y, 40, 100); g.drawImage(glow('255,150,40', 40), 20 - 40, y + 50 - 40); g.drawImage(glow('255,150,40', 40), SW - 20 - 40, y + 50 - 40); rr(g, 14, y + 46, 12, 8, 3, '#ffb040', 0); rr(g, SW - 26, y + 46, 12, 8, 3, '#ffb040', 0); }
        if (k === 'rain') { g.fillStyle = 'rgba(90,140,200,.12)'; g.fillRect(0, y, SW, 100); } } }); }
    function carDraw(g, cx2, cy, kind, col, me, ang) { var w = kind === 'truck' || kind === 'bus' ? 38 : kind === 'scooter' ? 14 : 30, h = kind === 'truck' ? 92 : kind === 'bus' ? 100 : kind === 'van' ? 60 : kind === 'scooter' ? 30 : 52;
      g.save(); g.translate(cx2, cy); if (ang) g.rotate(ang);
      rr(g, -w / 2 + 3, -h / 2 + 4, w, h, 8, 'rgba(0,0,0,.35)', 0);
      if (kind === 'scooter') { rr(g, -5, -15, 10, 30, 5, col, 2.5); ell(g, 0, -2, 7, 7, '#2a2a2a', 2); g.restore(); return [w, h]; }
      rr(g, -w / 2, -h / 2, w, h, kind === 'truck' || kind === 'bus' ? 4 : 9, col, 3);
      if (kind === 'truck') { rr(g, -w / 2 + 2, -h / 2 + 2, w - 4, 26, 4, me ? col : '#d8d8e0', 2); rr(g, -w / 2 + 4, -h / 2 + 30, w - 8, h - 34, 2, '#8a8a96', 2); }
      else if (kind === 'bus') { for (var i = 0; i < 5; i++) rr(g, -w / 2 + 4, -h / 2 + 10 + i * 17, 6, 12, 2, '#9ad8f0', 1.5), rr(g, w / 2 - 10, -h / 2 + 10 + i * 17, 6, 12, 2, '#9ad8f0', 1.5); rr(g, -w / 2 + 6, -h / 2 + 3, w - 12, 8, 3, '#9ad8f0', 1.5); }
      else { rr(g, -w / 2 + 4, -h / 2 + 10, w - 8, h * 0.22, 4, 'rgba(150,210,240,.85)', 2); rr(g, -w / 2 + 5, h / 2 - h * 0.28, w - 10, h * 0.16, 4, 'rgba(40,40,60,.8)', 2);
        if (kind === 'taxi') { rr(g, -7, -4, 14, 8, 2, '#fff', 1.5); txt(g, 'TAXI', 0, 0, 5, INK); }
        if (kind === 'police') { rr(g, -w / 2 + 3, -4, w - 6, 8, 2, '#fff', 1); g.drawImage(glow(((now() * 6) | 0) % 2 ? '255,40,40' : '40,80,255', 16), -16, -18); }
        if (me) { g.fillStyle = '#1a1220'; g.fillRect(-3, -h / 2 + 2, 6, h - 4); g.fillStyle = '#ffd860'; g.fillRect(-2, -h / 2 + 2, 4, h - 4); } }
      /* lights: heads at the top for us/same-direction traffic, tail at the bottom */
      g.fillStyle = '#fff6c0'; g.fillRect(-w / 2 + 3, -h / 2 - 1, 6, 3); g.fillRect(w / 2 - 9, -h / 2 - 1, 6, 3); g.fillStyle = '#ff3040'; g.fillRect(-w / 2 + 3, h / 2 - 2, 6, 3); g.fillRect(w / 2 - 9, h / 2 - 2, 6, 3);
      g.restore(); return [w, h]; }
    var KC = { taxi: '#f2c020', sedan: ['#c8302a', '#2a6ac8', '#e8e8f0', '#3a3a44', '#6a2a8a'], van: '#d8d8d0', truck: '#5a6a7a', bus: '#2a8a5a', scooter: '#e85aa0', police: '#1a1a24' };
    function spawn() { var kinds = R.kinds, k = kinds[(Math.random() * kinds.length) | 0], onc = R.haz.indexOf('oncoming') >= 0 && Math.random() < 0.35, merge = R.haz.indexOf('merge') >= 0 && Math.random() < 0.25;
      var off = (Math.random() * 2 - 1) * (R.hw - 30); if (onc) off = -Math.abs(off) - 10;
      var col = KC[k]; if (col.push) col = col[(Math.random() * col.length) | 0];
      cars.push({ k: k, z: d + 900 + Math.random() * 200, off: clamp(off, -R.hw + 24, R.hw - 24), v: onc ? -260 - Math.random() * 120 : 180 + Math.random() * 160 + (k === 'police' ? 220 : 0), col: col, onc: onc, drift: merge ? (Math.random() < 0.5 ? -1 : 1) * 40 : 0 });
      if (Math.random() < 0.45) { var h = R.haz[(Math.random() * R.haz.length) | 0]; if (h === 'cone' || h === 'cart' || h === 'puddle') objs.push({ k: h, z: d + 950 + Math.random() * 300, off: (Math.random() * 2 - 1) * (R.hw - 20) }); }
      if (Math.random() < 0.12) pick.push({ k: 'n', z: d + 1000, off: (Math.random() * 2 - 1) * (R.hw - 30) });
      else if (Math.random() < 0.35) pick.push({ k: 'y', z: d + 1000, off: (Math.random() * 2 - 1) * (R.hw - 30) }); }
    G.step = function (dt) {
      var I = G.in; msgT = Math.max(0, (msgT || 0) - dt); inv = Math.max(0, inv - dt); fx.forEach(function (F) { F.t += dt; }); fx = fx.filter(function (F) { return F.t < 0.8; });
      var vmax = R.vmax * (nT > 0 ? 1.4 : 1); nT = Math.max(0, nT - dt);
      var off = Math.abs(x - cx(d)) > R.hw - 14; if (off) { vmax *= 0.45; offT += dt; if (((offT * 10) | 0) % 2) tone(60, now(), 0.05, 'square', 0.02); }
      if (spin > 0) { spin -= dt; v *= Math.pow(0.4, dt); }
      else if (I.brake) v = Math.max(120, v - 600 * dt); else v = v < vmax ? Math.min(vmax, v + (nT > 0 ? 500 : 190) * dt) : Math.max(vmax, v - 300 * dt);
      var grip = R.wet ? 0.55 : 1, steer = (I.r ? 1 : 0) - (I.l ? 1 : 0); if (spin > 0) steer = 0;
      wobble = (wobble || 0) + (steer * 300 - (wobble || 0)) * Math.min(1, dt * (R.wet ? 3 : 10)); x += wobble * dt * (0.7 + v / 1400) * grip;
      if (R.haz.indexOf('gust') >= 0) { gustT -= dt; if (gustT <= 0) { gust = (Math.random() < 0.5 ? -1 : 1) * 70; gustT = 3 + Math.random() * 2; say(gust < 0 ? '\u2190 GUST' : 'GUST \u2192', 0.8); } x += gust * dt; gust *= Math.pow(0.5, dt); }
      x = clamp(x, 18, SW - 18); d += v * dt; timeL -= dt;
      G.score += Math.round(v * dt / 10);
      spawnD -= v * dt * R.traf; if (spawnD <= 0) { spawn(); spawnD = 380 + Math.random() * 360 - G.stage * 25; }
      /* checkpoints */
      var cpLen = R.len / (R.cp + 1); if (d > cpI * cpLen && cpI <= R.cp) { cpI++; var ext = 16 - Math.min(3, G.stage * 0.5) | 0; timeL += ext; say('CHECKPOINT  +' + ext + 's', 1.2); tone(988, now(), 0.12, 'square', 0.06); tone(1318, now() + 0.12, 0.2, 'square', 0.06); G.score += 300; }
      if (d >= R.len) return G.stage >= ROUTES.length - 1 ? 'win' : 'clear';
      if (timeL <= 0) { timeL = 0; return 'dead'; }
      /* traffic */
      cars.forEach(function (Cr) { Cr.z += Cr.v * dt; if (Cr.drift) { Cr.off = clamp(Cr.off + Cr.drift * dt, -R.hw + 24, R.hw - 24); if (Math.abs(Cr.off) >= R.hw - 25) Cr.drift = -Cr.drift; }
        var sy = PY - (Cr.z - d), sx = cx(Cr.z) + Cr.off, w = Cr.k === 'truck' || Cr.k === 'bus' ? 38 : Cr.k === 'scooter' ? 14 : 30, h = Cr.k === 'truck' ? 92 : Cr.k === 'bus' ? 100 : Cr.k === 'van' ? 60 : Cr.k === 'scooter' ? 30 : 52;
        Cr.sx = sx; Cr.sy = sy;
        if (!inv && Math.abs(sx - x) < (w + 28) / 2 - 2 && Math.abs(sy - PY) < (h + 52) / 2 - 4) { crash(Cr); }
        else if (!Cr.nm && v > 380 && Math.abs(sy - PY) < 30 && Math.abs(sx - x) < (w + 28) / 2 + 16) { Cr.nm = 1; nearN++; var b = 100 + Math.round(v / 10); G.score += b; fx.push({ k: 'pts', x: x, y: PY - 40, t: 0, s: 'NEAR MISS +' + b }); tone(1568, now(), 0.06, 'square', 0.04); } });
      cars = cars.filter(function (Cr) { return Cr.z > d - 300 && Cr.z < d + 1400; });
      objs.forEach(function (O) { var sy = PY - (O.z - d), sx = cx(O.z) + O.off; if (!O.hit && Math.abs(sx - x) < 22 && Math.abs(sy - PY) < 30) { O.hit = 1; if (O.k === 'puddle') { spin = 0.5; say('AQUAPLANE!', 0.8); tone(200, now(), 0.3, 'sine', 0.05); } else { v *= 0.6; fx.push({ k: 'boom', x: sx, y: sy, t: 0 }); drum('s', now(), 0.3); } } });
      objs = objs.filter(function (O) { return O.z > d - 300; });
      pick.forEach(function (Pk) { var sy = PY - (Pk.z - d), sx = cx(Pk.z) + Pk.off; if (!Pk.got && Math.abs(sx - x) < 26 && Math.abs(sy - PY) < 34) { Pk.got = 1; if (Pk.k === 'n') { nit = Math.min(3, nit + 1); say('NITRO +1', 0.7); tone(880, now(), 0.15, 'square', 0.05); } else { G.score += 100; fx.push({ k: 'pts', x: sx, y: sy, t: 0, s: '+100' }); tone(1318, now(), 0.06, 'triangle', 0.05); } } });
      pick = pick.filter(function (Pk) { return !Pk.got && Pk.z > d - 300; });
    };
    function crash(Cr) { inv = 1.2; spin = 0.7; v *= 0.35; Cr.v += 120; drum('k', now(), 0.6); drum('s', now() + 0.05, 0.4); tone(80, now(), 0.4, 'sawtooth', 0.1); fx.push({ k: 'boom', x: x, y: PY - 20, t: 0 }); say('CRASH!', 0.8); }
    G.draw = function (g, t) {
      /* scenery scroll */
      var so = (d * 0.9) % 600; K.blit(g, side, 0, so - 600); K.blit(g, side, 0, so);
      /* road slices */
      for (var sy = -10; sy < SH + 10; sy += 10) { var z = d + (PY - sy), c = cx(z), hw = R.hw;
        g.fillStyle = '#4a4650'; g.fillRect(c - hw - 18, sy, hw * 2 + 36, 11);
        g.fillStyle = R.road; g.fillRect(c - hw, sy, hw * 2, 11);
        var stripe = ((z / 40) | 0) % 2; g.fillStyle = stripe ? '#e8e8f0' : '#c8302a'; g.fillRect(c - hw - 6, sy, 6, 11); g.fillRect(c + hw, sy, 6, 11);
        if (((z / 60) | 0) % 2) { g.fillStyle = 'rgba(255,255,255,.7)'; if (R.hw > 110) { g.fillRect(c - hw / 2 - 2, sy, 4, 11); g.fillRect(c + hw / 2 - 2, sy, 4, 11); } else g.fillRect(c - 2, sy, 4, 11); }
        if (R.haz.indexOf('oncoming') >= 0) { g.fillStyle = '#ffd040'; g.fillRect(c - 7, sy, 3, 11); g.fillRect(c - 2, sy, 3, 11); } }
      /* checkpoint / goal banners */
      var cpLen = R.len / (R.cp + 1); for (var ci = 1; ci <= R.cp + 1; ci++) { var zz = ci * cpLen, by = PY - (zz - d); if (by < -40 || by > SH + 40) continue; var bc = cx(zz), last = ci === R.cp + 1;
        g.fillStyle = last ? '#fff' : '#7aff9a'; for (var q = -R.hw; q < R.hw; q += 16) { g.fillStyle = ((q / 16) | 0) % 2 ? (last ? '#1a1a1a' : '#0a3a1a') : (last ? '#fff' : '#7aff9a'); g.fillRect(bc + q, by - 6, 16, 12); }
        otxt(g, last ? 'GOAL' : 'CHECKPOINT', bc, by - 22, 16, last ? '#ffd860' : '#7aff9a'); }
      objs.forEach(function (O) { var y = PY - (O.z - d), sx = cx(O.z) + O.off; if (y < -40 || y > SH + 40 || O.hit && O.k !== 'puddle') return;
        if (O.k === 'cone') { poly(g, [sx, y - 12, sx + 8, y + 8, sx - 8, y + 8], '#ff7a1a', 2); g.fillStyle = '#fff'; g.fillRect(sx - 4, y - 2, 8, 3); }
        else if (O.k === 'cart') { rr(g, sx - 14, y - 10, 28, 20, 3, '#8a6a3a', 2.5); rr(g, sx - 10, y - 16, 20, 8, 3, '#e8d8b0', 2); }
        else { ell(g, sx, y, 26, 12, 'rgba(120,170,230,.45)', 0); ell(g, sx - 6, y - 3, 10, 3, 'rgba(255,255,255,.35)', 0); } });
      pick.forEach(function (Pk) { var y = PY - (Pk.z - d), sx = cx(Pk.z) + Pk.off; if (y < -30 || y > SH + 30) return; if (Pk.k === 'n') { g.drawImage(glow('90,216,255', 22), sx - 22, y - 22); rr(g, sx - 8, y - 12, 16, 24, 5, '#5ad8ff', 2.5); txt(g, 'N', sx, y, 12, INK); } else { g.drawImage(glow('255,216,96', 16), sx - 16, y - 16); txt(g, '\u00a5', sx, y, 16, '#ffd860'); } });
      cars.forEach(function (Cr) { if (Cr.sy < -80 || Cr.sy > SH + 80) return; carDraw(g, Cr.sx, Cr.sy, Cr.k, Cr.col, false, Cr.onc ? Math.PI : 0); });
      /* the player: headlight cones then the car */
      g.globalAlpha = 0.5; g.drawImage(glow('255,240,190', 50), x - 50, PY - 110); g.globalAlpha = 1;
      if (!(inv > 0 && ((t * 12) | 0) % 2)) carDraw(g, x, PY, 'sedan', '#ff8a2a', true, spin > 0 ? spin * 9 : (wobble || 0) / 3000);
      if (nT > 0) { g.drawImage(glow('90,200,255', 26), x - 26, PY + 16); g.drawImage(glow('255,255,255', 12), x - 12, PY + 28); }
      if (R.dark) { g.fillStyle = 'rgba(0,0,0,.42)'; g.fillRect(0, 0, SW, SH); g.globalAlpha = 0.6; g.drawImage(glow('255,240,190', 70), x - 70, PY - 150); g.globalAlpha = 1; }
      if (R.wet) { g.strokeStyle = 'rgba(180,210,255,.35)'; g.lineWidth = 1; g.beginPath(); for (var rn = 0; rn < 40; rn++) { var rx = (rn * 97 + t * 40) % SW, ry = (rn * 53 + t * 900) % SH; g.moveTo(rx, ry); g.lineTo(rx - 4, ry + 14); } g.stroke(); }
      fx.forEach(function (F) { var a = 1 - F.t / 0.8; if (F.k === 'boom') { g.globalAlpha = a; g.drawImage(glow('255,160,60', 40), F.x - 40, F.y - 40); g.globalAlpha = 1; } else { g.globalAlpha = a; otxt(g, F.s, F.x, F.y - F.t * 50, 13, '#7aff9a'); g.globalAlpha = 1; } });
      /* HUD */
      rr(g, SW / 2 - 44, 30, 88, 32, 8, 'rgba(0,0,0,.6)', 2, timeL < 8 ? '#ff3a4a' : '#7aff9a'); txt(g, 'TIME', SW / 2, 38, 8, '#fff'); mono(g, String(Math.max(0, Math.ceil(timeL))), SW / 2, 52, 17, timeL < 8 ? '#ff4a5a' : '#7aff9a', 'center');
      rr(g, 8, SH - 64, 112, 54, 10, 'rgba(0,0,0,.6)', 2, '#7aff9a'); mono(g, String(Math.round(v * 0.36)), 92, SH - 40, 24, '#fff', 'right'); txt(g, 'km/h', 100, SH - 32, 9, '#7aff9a', 'left');
      var pr = clamp(d / R.len, 0, 1); rr(g, 14, SH - 20, 100, 6, 3, 'rgba(255,255,255,.2)', 0); rr(g, 14, SH - 20, 100 * pr, 6, 3, '#7aff9a', 0);
      for (var n = 0; n < 3; n++) { rr(g, SW - 26 - n * 20, SH - 40, 14, 22, 4, n < nit ? '#5ad8ff' : 'rgba(255,255,255,.15)', 1.5); } txt(g, 'NITRO', SW - 52, SH - 50, 8, '#5ad8ff');
      if (msgT > 0) otxt(g, msg, SW / 2, 130, 20, '#fff');
    };
    var TT = null;
    G.title = function (g, t) {
      if (!TT) TT = K.layer(SW, SH, function (q) { var sg = q.createLinearGradient(0, 0, 0, SH); sg.addColorStop(0, '#04100a'); sg.addColorStop(0.5, '#0a2a2a'); sg.addColorStop(1, '#3a0a3a'); q.fillStyle = sg; q.fillRect(0, 0, SW, SH);
        poly(q, [SW / 2 - 20, 230, SW / 2 + 20, 230, SW + 60, SH, -60, SH], '#24222c', 0); for (var i = 0; i < 8; i++) { var y = 240 + i * i * 4.5; q.fillStyle = 'rgba(255,255,255,.8)'; q.fillRect(SW / 2 - 1 - i * 0.6, y, 2 + i * 1.2, 4 + i * 2); }
        for (var b = 0; b < 9; b++) { var bx = b < 5 ? b * 30 : SW - (b - 4) * 30; q.fillStyle = '#0c1c18'; q.fillRect(bx - 12, 140 + (b % 3) * 20, 26, 100); }
        otxt(q, '\u771f\u591c\u4e2d\u592e\u7dda', SW / 2, 54, 22, '#7aff9a'); otxt(q, 'MIDNIGHT', SW / 2, 100, 46, '#fff', 'center', '#1a8a4a'); otxt(q, 'CHUO', SW / 2, 150, 52, '#7aff9a'); txt(q, '7 NIGHT ROUTES \u00b7 BEAT THE CLOCK', SW / 2, 196, 12, '#fff'); });
      K.blit(g, TT, 0, 0);
      var k = (t * 0.6) % 1; carDraw(g, SW / 2 + Math.sin(t * 1.4) * 40, 400 - k * 30, 'sedan', '#ff8a2a', true, Math.sin(t * 1.4) * 0.1);
      g.globalAlpha = 0.5; g.drawImage(glow('255,240,190', 50), SW / 2 + Math.sin(t * 1.4) * 40 - 50, 290); g.globalAlpha = 1;
    };
    G.dispose = function () { TT = null; side = null; };
    G.dbg = function (o) { o = o || {}; if (o.lives) timeL = 999; if (o.d) d = o.d; return { d: d, v: v, timeL: timeL, route: R.n, cars: cars.length }; };
    G._s = function () { return { x: x, d: d, cx: cx, cars: cars, objs: objs, R: R, PY: PY }; };
    return G;
  };
  } catch (eTop) { try { console.warn('S2ARC race init', eTop); } catch (e2) {} }
})();
