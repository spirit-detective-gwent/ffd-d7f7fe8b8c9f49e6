/* v6.5.64 Game Center cabinet: SHONEN SHOWDOWN (2D fighter; was "Fox Fire Fist II"). v6564-arcade, v6566-shonen (Erik t569u).
 * Character select (six in-universe anime/game heroes on the cast models) -> arcade ladder of 5 matches, best of 3 rounds, 60 s timer.
 * v6566-shonen controls: D-pad left / right, swipe up anywhere to jump. AUTO-BLOCK: you guard on your own whenever you are not
 * attacking (no high / low; chip damage stays; a short lockout after an attack and enemy throws keep a rhythm).
 * Two buttons: ATTACK (tap; keep tapping for the P > P > K chain) and SPECIAL (tap = special, hold 0.4 s+ = charged move).
 * When the super bar is full SPECIAL glows and one tap fires the SUPER. The AI keeps its full move list.
 * Internal ids (fighter / ryo / aoi ...) are unchanged so saves and boards keep working.
 * Fighters are hand-posed skeleton models drawn every frame in each character's outfit. */
(function () {
  try {
  var root = typeof window !== 'undefined' ? window : this;
  var A = root.FFF_S2ARC = root.FFF_S2ARC || { v: 1 };
  A.GAMES = A.GAMES || {}; A.CABS = A.CABS || {};
  A.CABS.fighter = { n: 'Sh\u014dnen Showdown', jp: '\u5c11\u5e74\u5bfe\u6c7a', mqPx: 21, col: '#ff9a3a', body: '#22140e', mq: ['#4a1a06', '#140804'], deck: ['#3a2418', '#1a0e08'],
    tiers: [12000, 30000, 50000],
    seed: [['JIN', 1.45], ['NLS', 1.22], ['GDA', 1.04], ['MSA', 0.86], ['KNZ', 0.7], ['BAN', 0.55], ['TTS', 0.42], ['OGT', 0.3], ['PNT', 0.2], ['KDE', 0.12]],
    mqArt: function (p, x, y, w, h) { var g = p.createLinearGradient(x, 0, x + w, 0); g.addColorStop(0, 'rgba(255,120,40,.35)'); g.addColorStop(0.5, 'rgba(255,200,80,0)'); g.addColorStop(1, 'rgba(255,60,90,.35)'); p.fillStyle = g; p.fillRect(x, y, w, h);
      for (var i = 0; i < 9; i++) { p.fillStyle = 'rgba(255,' + (120 + i * 12) + ',40,.25)'; p.beginPath(); p.moveTo(x + 20 + i * 40, y + h); p.quadraticCurveTo(x + 30 + i * 40, y + h - 30 - (i % 3) * 10, x + 24 + i * 40, y + h - 50); p.quadraticCurveTo(x + 40 + i * 40, y + h - 20, x + 44 + i * 40, y + h); p.fill(); } } };

  var PI = Math.PI;
  /* ---------- the cast ---------- */
  var CH = {
    ryo: { n: 'KAZE TENMA', full: 'Hero of \u201cFox Spirit Kaze\u201d', hp: 100, spd: 92, w: 1, skin: '#e8b890', hair: '#14101a', top: '#e8dcc8', top2: '#a01e24', shirt: '#1a1a22', pants: '#2a1820', shoe: '#2a1a12', trim: '#c82028', style: 'openjack', hd: 'tallspike', aura: '255,120,40',
      mv: { p: ['Jab', 4], k: ['Roundhouse', 9], sp: ['Fox Fire', 8, 'proj'], spf: ['Kitsune Rush', 10, 'dash'], spu: ['Rising Fox', 11, 'rise'], su: ['Nine-Tail Barrage', 30, 'rush'] }, stage: 'roof', where: 'School roof \u00b7 after class' },
    aoi: { n: 'BLUE LOTUS', full: 'Star of \u201cShrine Maiden Blitz\u201d', hp: 95, spd: 100, w: 0.9, skin: '#f0c8a8', hair: '#121018', top: '#7ec8e8', top2: '#5ab0d8', shirt: '#f2f2f2', pants: '#1a3a5a', shoe: '#2a1a12', trim: '#f2f2f2', style: 'sailor', hd: 'pony', aura: '120,220,255',
      mv: { p: ['Palm', 4], k: ['High Kick', 9], sp: ['Ofuda Toss', 7, 'proj'], spf: ['Shrine Step', 9, 'slide'], spu: ['Crescent Kick', 10, 'rise'], su: ['Kagura Storm', 28, 'rush'] }, stage: 'shrine', where: 'Fox shrine steps' },
    goda: { n: 'IRON DAIMYO', full: 'Champ of \u201cSumo Shogun 3\u201d', hp: 118, spd: 68, w: 1.35, skin: '#e0b088', hair: '#14101a', top: '#6a3a1e', top2: '#7a4a2a', shirt: '#2a2a30', pants: '#3a2a20', shoe: '#1a1210', trim: '#e8e0d0', style: 'stripe', hd: 'topknot', aura: '255,160,90',
      mv: { p: ['Slap', 6], k: ['Belly Bump', 12], sp: ['Hundred Slaps', 12, 'multi'], spf: ['Boiler Charge', 13, 'dash'], spu: ['Steam Lift', 12, 'rise'], su: ['Steam Press', 34, 'rush'] }, stage: 'boiler', where: 'Boiler room \u00b7 Kitsune-no-Yu' },
    nails: { n: 'RAZOR REI', full: 'Punk of \u201cAlley Kings\u201d', hp: 100, spd: 96, w: 1, skin: '#c89068', hair: '#0e0c10', top: '#d8c8a0', top2: '#e8dab8', shirt: '#d0a030', pants: '#c8b890', shoe: '#5a3a1a', trim: '#e8c040', style: 'suit', hd: 'curly', aura: '255,216,96',
      mv: { p: ['Brass Jab', 4], k: ['Chain Lash', 8], sp: ['Shades Flash', 12, 'counter'], spf: ['Chain Snap', 10, 'chain'], spu: ['Pompadour Rise', 10, 'rise'], su: ['Delinquent\u2019s Honor', 30, 'rush'] }, stage: 'alley', where: 'Kitsune alley \u00b7 Punks\u2019 wall' },
    masa: { n: 'THE RONIN', full: 'Drifter of \u201cSteel Ronin\u201d', hp: 110, spd: 78, w: 1.18, skin: '#d8a078', hair: '#1a1410', top: '#3a4a62', top2: '#2a3448', shirt: '#8a2a24', pants: '#1e2430', shoe: '#1a1410', trim: '#d4b06a', style: 'kimono', hd: 'kasa', aura: '255,200,60',
      mv: { p: ['Glove Jab', 5], k: ['Wrench Swing', 11], sp: ['Bolt Toss', 8, 'proj'], spf: ['Hardhat Ram', 12, 'dash'], spu: ['Crane Hook', 11, 'rise'], su: ['Shutter Drop', 32, 'drop'] }, stage: 'depot', where: 'Freight depot \u00b7 the shutter' },
    jin: { n: 'BLACK COMET', full: 'Final boss of \u201cNeon Comet\u201d', hp: 96, spd: 108, w: 0.95, skin: '#e8c0a0', hair: '#121418', top: '#7ad82a', top2: '#9aee4a', shirt: '#141414', pants: '#18181c', shoe: '#e8e8e8', trim: '#1a1a1a', style: 'hoodie', hd: 'shaggy', aura: '120,255,80',
      mv: { p: ['Quick Jab', 3], k: ['Spin Kick', 8], sp: ['Bass Drop', 7, 'proj'], spf: ['Combo Breaker', 9, 'dash'], spu: ['1-UP Rise', 10, 'rise'], su: ['High Score', 32, 'rush'] }, stage: 'prize', where: 'Neon Game Center \u00b7 prize room' }
  };
  var ORDER = ['ryo', 'aoi', 'goda', 'nails', 'masa', 'jin'], LADDER = ['masa', 'aoi', 'goda', 'nails', 'ryo', 'jin'];
  A.FIGHT_CAST = CH;

  A.GAMES.fighter = function (K, C) {
    var rr = K.rr, txt = K.txt, otxt = K.otxt, ell = K.ell, poly = K.poly, glow = K.glow, tone = K.tone, drum = K.drum, now = K.now, SW = K.SW, SH = K.SH, INK = K.INK, clamp = K.clamp, mono = K.mono;
    var GY = 430, X0 = 26, X1 = SW - 26;
    var G = { score: 0, stage: 0, stageWord: 'MATCH', stages: [], how: ['Pick a fighter, beat the other five', '\u25c0 \u25b6 walk \u00b7 swipe up anywhere to jump', 'You block on your own when not attacking', 'ATTACK: keep tapping for a 3-hit combo', 'SPECIAL: tap for a special, hold to charge', 'Bar full? SPECIAL glows: tap for SUPER', 'Careful up close: they can grab you'],
      panel: { stick: { x: 92, y: 722, r: 56, c: '#ff9a3a', dpad: 1 }, btns: [{ k: 'a', x: 240, y: 728, r: 44, l: 'ATTACK', c: '#ffd860', sub: 'tap \u00b7 combo', fs: 14 }, { k: 'sp', x: 336, y: 700, r: 44, l: 'SPECIAL', lf: function () { return P && P.meter >= 100 && phase === 'fight' ? 'SUPER' : 'SPECIAL'; }, c: '#5ad8ff', sub: 'tap \u00b7 hold', fs: 13,
        glow: function () { return !!(P && P.meter >= 100 && (phase === 'fight' || phase === 'pre')); }, gc: '255,90,200', gcol: '#ff5ac8', ring: function () { return spHold >= 0 && phase === 'fight' ? Math.min(1, spHold / CHG) : 0; } }] } };
    G.endLine = 'Champion of the Neon Game Center.';
    /* v6566-handheld (GGD-93): C.hh = one match on the Kitsune BOY handheld { me, foe, lv (AI level), pk / ph / ps (your fighter's star boost: damage / hp / speed), dbl ('p' / 'e': DOUBLE SHOT), title, on(ev) } */
    var HH = C && C.hh || null;
    var phase, sel = 0, selT = 0, P = null, E = null, rnd = 1, wins, rT, roundT, fx, proj, shake, slow, combo, comboT, msg, msgT, bgL = {}, buf = null, bufT = 0, lad = [], sw = {}, freeze = 0, superFlash = 0;
    /* v6566-shonen: SPECIAL hold timer (-1 = up), queued swipe jump, lockout after an attack before auto-block is back */
    var spHold = -1, jumpQ = 0, jumpDir = 0, CHG = 0.4, LOCK = 0.14;
    /* ---------- poses: angles (0 = down, + = toward the front), hip height ---------- */
    var POSE = {
      idle: { hip: 52, lean: 0.06, fa: [0.9, 2.3], ba: [0.55, 2.1], fl: [0.28, -0.08], bl: [-0.26, 0.04] },
      walk: { hip: 52, lean: 0.1, fa: [0.9, 2.3], ba: [0.55, 2.1], fl: [0.28, -0.08], bl: [-0.26, 0.04] },
      crouch: { hip: 30, lean: 0.32, fa: [1.0, 2.4], ba: [0.6, 2.2], fl: [1.35, -0.25], bl: [0.5, -1.2] },
      jump: { hip: 54, lean: 0.12, fa: [1.2, 2.4], ba: [0.6, 2.0], fl: [1.3, -0.3], bl: [0.7, -1.0] },
      p: { hip: 52, lean: 0.18, fa: [1.57, 1.6], ba: [0.6, 2.2], fl: [0.36, -0.06], bl: [-0.34, 0.04] },
      k: { hip: 54, lean: -0.32, fa: [0.9, 2.2], ba: [-0.2, 1.4], fl: [1.85, 1.75], bl: [-0.15, 0.02] },
      ck: { hip: 24, lean: 0.25, fa: [1.0, 2.2], ba: [0.1, 1.0], fl: [1.5, 1.5], bl: [0.6, -1.3] },
      jk: { hip: 54, lean: -0.1, fa: [1.2, 2.2], ba: [0.4, 1.8], fl: [1.0, 0.8], bl: [0.6, -1.1] },
      block: { hip: 50, lean: -0.08, fa: [0.6, 2.9], ba: [0.4, 2.8], fl: [0.24, -0.06], bl: [-0.32, 0.06] },
      cblock: { hip: 30, lean: 0.1, fa: [0.7, 2.9], ba: [0.5, 2.8], fl: [1.35, -0.25], bl: [0.5, -1.2] },
      hit: { hip: 50, lean: -0.42, fa: [-0.4, -0.1], ba: [-0.7, -0.3], fl: [0.4, 0.1], bl: [-0.1, 0.1], hd: -0.3 },
      down: { hip: 12, lean: -1.45, fa: [-1.5, -1.5], ba: [-1.8, -1.6], fl: [1.5, 1.5], bl: [1.3, 1.4], hd: -0.2 },
      proj: { hip: 50, lean: 0.24, fa: [1.57, 1.57], ba: [1.45, 1.62], fl: [0.5, -0.1], bl: [-0.45, 0.06] },
      rise: { hip: 64, lean: -0.08, fa: [3.0, 3.05], ba: [0.4, 1.8], fl: [0.7, -0.3], bl: [-0.1, -0.2] },
      dash: { hip: 46, lean: 0.62, fa: [1.3, 0.6], ba: [0.2, 1.2], fl: [0.9, -0.2], bl: [-0.7, -0.1] },
      slide: { hip: 18, lean: -0.9, fa: [-0.6, -0.4], ba: [-1.2, -0.8], fl: [1.62, 1.6], bl: [1.2, 0.4] },
      win: { hip: 54, lean: -0.05, fa: [3.0, 3.1], ba: [0.3, 1.9], fl: [0.2, -0.04], bl: [-0.2, 0.04] },
      lose: { hip: 34, lean: 0.6, fa: [0.2, 0.1], ba: [0.1, 0.0], fl: [1.2, -0.3], bl: [0.9, -1.4], hd: 0.4 },
      counter: { hip: 48, lean: -0.15, fa: [2.2, 2.6], ba: [0.3, 2.4], fl: [0.36, -0.06], bl: [-0.4, 0.04] }
    };
    function lerpPose(a, b, k) { var o = { hip: a.hip + (b.hip - a.hip) * k, lean: a.lean + (b.lean - a.lean) * k, hd: (a.hd || 0) + ((b.hd || 0) - (a.hd || 0)) * k };
      ['fa', 'ba', 'fl', 'bl'].forEach(function (q) { o[q] = [a[q][0] + (b[q][0] - a[q][0]) * k, a[q][1] + (b[q][1] - a[q][1]) * k]; }); return o; }
    function limb(g, x, y, a1, a2, l1, l2, w, col, f) { var x1 = x + Math.sin(a1) * l1 * f, y1 = y + Math.cos(a1) * l1, x2 = x1 + Math.sin(a2) * l2 * f, y2 = y1 + Math.cos(a2) * l2;
      g.lineCap = 'round'; g.lineJoin = 'round'; g.strokeStyle = INK; g.lineWidth = w + 5; g.beginPath(); g.moveTo(x, y); g.lineTo(x1, y1); g.lineTo(x2, y2); g.stroke();
      g.strokeStyle = col; g.lineWidth = w; g.beginPath(); g.moveTo(x, y); g.lineTo(x1, y1); g.lineTo(x2, y2); g.stroke(); return [x2, y2, x1, y1]; }
    function fist(g, x, y, r, c) { ell(g, x, y, r, r, c, 2.5); }
    /* ---------- one fighter, drawn from its pose ---------- */
    function drawFighter(g, F, t, scale) {
      var c = F.c, ps = F.pose, f = F.face, w = c.w, sc = scale || 1, hurt = F.flash > 0;
      g.save(); g.translate(F.x, F.y); g.scale(sc, sc);
      ell(g, 0, 0, 30 * w, 6, 'rgba(0,0,0,.35)', 0);
      var hip = -ps.hip, lean = ps.lean, TL = 40, sx = Math.sin(lean) * TL * f, sy = hip - Math.cos(lean) * TL;
      var tw = 13 * w, lw = 11 * Math.sqrt(w), aw = 9 * Math.sqrt(w), LL = 25;
      var top = hurt ? '#fff' : c.top, pants = hurt ? '#fff' : c.pants, arm = (c.style === 'openjack' && !hurt) ? c.skin : top;
      /* back arm + back leg */
      var bh = limb(g, sx - 4 * f, sy + 6, ps.ba[0], ps.ba[1], 19, 19, aw, shade(arm), f); fist(g, bh[0], bh[1], 5.5 * Math.sqrt(w), c.skin);
      var bl = limb(g, -4 * f, hip, ps.bl[0], ps.bl[1], LL, LL, lw, shade(pants), f); shoe(g, bl[0], bl[1], f, c.shoe);
      /* torso */
      g.save(); g.translate(0, hip); g.rotate(lean * f);
      var bw = tw + 4; rr(g, -bw, -TL - 4, bw * 2, TL + 10, 9 * w, top, 3);
      outfit(g, c, bw, TL, f, hurt);
      g.restore();
      /* front leg */
      var fl = limb(g, 4 * f, hip, ps.fl[0], ps.fl[1], LL, LL, lw, pants, f); shoe(g, fl[0], fl[1], f, c.shoe);
      /* head */
      var hx = sx + Math.sin(lean) * 12 * f, hy = sy - Math.cos(lean) * 12;
      head(g, c, hx, hy, f, (ps.hd || 0) + lean * 0.4, F, t);
      /* front arm */
      var fh = limb(g, sx + 4 * f, sy + 6, ps.fa[0], ps.fa[1], 19, 19, aw, arm, f); fist(g, fh[0], fh[1], 6 * Math.sqrt(w), c.skin);
      if (c.style === 'suit' && F.st === 'atk' && F.mv && (F.mv.k === 'k' || F.mv.k === 'spf')) { g.strokeStyle = '#d8c060'; g.lineWidth = 3; g.beginPath(); g.moveTo(fh[0], fh[1]); for (var i = 1; i <= 6; i++) g.lineTo(fh[0] + f * i * 10, fh[1] + Math.sin(t * 30 + i) * 3); g.stroke(); }
      if (F.id === 'masa' && F.st === 'atk' && F.mv && F.mv.k === 'k') { g.save(); g.translate(fh[0], fh[1]); g.rotate(f * 0.6); rr(g, -3, -26, 6, 30, 2, '#8a96a8', 2.5); rr(g, -8, -32, 16, 10, 3, '#8a96a8', 2.5); g.restore(); }
      g.restore();
      F.hand = [F.x + fh[0] * sc, F.y + fh[1] * sc]; F.headP = [F.x + hx * sc, F.y + hy * sc];
    }
    function shade(h) { var n = parseInt(h.slice(1), 16), r = (n >> 16) * 0.72 | 0, gg = ((n >> 8) & 255) * 0.72 | 0, b = (n & 255) * 0.72 | 0; return 'rgb(' + r + ',' + gg + ',' + b + ')'; }
    function shoe(g, x, y, f, c) { rr(g, x - 6 + (f > 0 ? 0 : -6), y - 3, 13, 7, 3, c, 2); }
    function outfit(g, c, bw, TL, f, hurt) { if (hurt) return; var s = c.style;
      if (s === 'gakuran') { g.fillStyle = c.shirt; poly(g, [-6, -TL - 3, 6, -TL - 3, 3, -TL + 14, -3, -TL + 14], c.shirt, 0); g.fillStyle = c.trim; for (var i = 0; i < 4; i++) { g.beginPath(); g.arc(f * 2, -TL + 10 + i * 9, 1.8, 0, 7); g.fill(); } rr(g, -bw, -TL - 6, bw * 2, 6, 3, c.top2, 2); }
      else if (s === 'sailor') { poly(g, [-bw, -TL - 2, bw, -TL - 2, 0, -TL + 16], '#f2f2f2', 2); g.strokeStyle = c.top2; g.lineWidth = 2.5; g.beginPath(); g.moveTo(-bw + 3, -TL); g.lineTo(0, -TL + 14); g.lineTo(bw - 3, -TL); g.stroke(); poly(g, [-5, -TL + 12, 5, -TL + 12, 0, -TL + 22], '#f2f2f2', 1.5); g.fillStyle = c.pants; g.fillRect(-bw, -6, bw * 2, 10); }
      else if (s === 'stripe') { g.save(); g.beginPath(); g.rect(-8, -TL - 2, 16, TL + 6); g.clip(); for (var j = 0; j < 9; j++) { g.fillStyle = j % 2 ? '#2a2a30' : '#8a8a90'; g.fillRect(-8, -TL - 2 + j * 5, 16, 5); } g.restore(); g.fillStyle = c.trim; g.fillRect(-bw + 3, -TL, 4, TL + 2); }
      else if (s === 'suit') { poly(g, [-7, -TL - 2, 7, -TL - 2, 0, -TL + 18], c.shirt, 1.5); g.strokeStyle = '#e8c040'; g.lineWidth = 2; g.beginPath(); g.arc(0, -TL + 2, 7, 0.2, PI - 0.2); g.stroke(); }
      else if (s === 'hivis') { g.fillStyle = c.trim; g.fillRect(-bw, -TL + 12, bw * 2, 4); g.fillRect(-bw, -TL + 22, bw * 2, 4); g.fillRect(-6, -TL - 2, 4, TL); g.fillRect(2, -TL - 2, 4, TL); }
      else if (s === 'hoodie') { poly(g, [-6, -TL - 2, 6, -TL - 2, 0, -TL + 10], c.shirt, 1.5); g.strokeStyle = '#1a1a1a'; g.lineWidth = 2; g.beginPath(); g.moveTo(0, -TL + 10); g.lineTo(0, 2); g.stroke(); rr(g, -bw + 2, -10, bw * 2 - 4, 8, 3, c.top2, 1.5); }
      else if (s === 'openjack') { /* v6566-shonen t600u: sleeveless open jacket, undershirt shows down the middle */
        g.fillStyle = c.shirt; g.fillRect(-5, -TL - 2, 10, TL + 8);
        poly(g, [-bw, -TL - 4, -5, -TL - 2, -4, 6, -bw, 6], c.top, 2.5);
        poly(g, [bw, -TL - 4, 5, -TL - 2, 4, 6, bw, 6], c.top, 2.5);
        poly(g, [-bw + 2, -TL - 2, -6, -TL, -5, 4, -bw + 2, 4], c.top2, 0);
        poly(g, [bw - 2, -TL - 2, 6, -TL, 5, 4, bw - 2, 4], c.top2, 0);
        g.strokeStyle = c.trim; g.lineWidth = 2; g.beginPath(); g.moveTo(-5, -TL - 2); g.lineTo(-4, 6); g.moveTo(5, -TL - 2); g.lineTo(4, 6); g.stroke(); }
      else if (s === 'kimono') { /* v6566-shonen t597u: wrapped kimono, obi, hakama pleats at the hip */
        poly(g, [f * -bw, -TL - 3, f * 3, -TL - 3, f * 7, 6, f * -bw, 6], c.top2, 2);
        g.strokeStyle = c.shirt; g.lineWidth = 2.5; g.beginPath(); g.moveTo(f * 2, -TL - 2); g.lineTo(-f * 4, 6); g.stroke();
        rr(g, -bw - 1, -9, bw * 2 + 2, 11, 2, c.shirt, 2.5);
        rr(g, -5, -10, 10, 5, 2, '#5a1814', 0);
        g.strokeStyle = 'rgba(0,0,0,.35)'; g.lineWidth = 1.4;
        for (var h = -3; h <= 3; h++) { g.beginPath(); g.moveTo(h * (bw / 3), 2); g.lineTo(h * (bw / 3), 8); g.stroke(); } } }
    function head(g, c, x, y, f, tilt, F, t) { g.save(); g.translate(x, y); g.rotate(tilt * f); var r = 12.5 * (c.w > 1.2 ? 1.1 : 1);
      if (c.hd === 'pony') { g.strokeStyle = INK; g.lineWidth = 9; g.lineCap = 'round'; g.beginPath(); g.moveTo(-f * 6, -8); g.quadraticCurveTo(-f * 20, -4 + Math.sin(t * 6) * 2, -f * 18, 18); g.stroke(); g.strokeStyle = c.hair; g.lineWidth = 6; g.stroke(); }
      ell(g, 0, 0, r, r * 1.08, F.flash > 0 ? '#fff' : c.skin, 2.5);
      g.fillStyle = c.hair;
      if (c.hd === 'spiky') { poly(g, [-12, -2, -14, -10, -8, -9, -10, -17, -3, -12, 0, -19, 4, -12, 10, -16, 9, -8, 14, -6, 11, 0, f * 6, -6, -f * 4, -5], c.hair, 2); }
      else if (c.hd === 'pony') { g.beginPath(); g.arc(0, -2, r + 1, PI, 0); g.lineTo(f * 4, -4); g.lineTo(-f * 10, 4); g.closePath(); g.fill(); g.lineWidth = 2; g.strokeStyle = INK; g.stroke(); }
      else if (c.hd === 'topknot') { g.beginPath(); g.arc(0, -2, r + 1, PI, 0); g.closePath(); g.fill(); g.lineWidth = 2; g.strokeStyle = INK; g.stroke(); ell(g, -f * 2, -r - 4, 5, 4, c.hair, 2); }
      else if (c.hd === 'curly') { for (var i = 0; i < 7; i++) ell(g, -9 + i * 3, -8 - (i % 2) * 3, 5, 5, c.hair, 0); rr(g, f > 0 ? -2 : -12, -4, 14, 5, 2, '#0a0a0a', 1.5); }
      else if (c.hd === 'hardhat') { g.beginPath(); g.arc(0, -3, r + 2, PI, 0); g.closePath(); g.fillStyle = '#f2c020'; g.fill(); g.lineWidth = 2.5; g.strokeStyle = INK; g.stroke(); rr(g, -r - 5, -5, (r + 5) * 2, 4, 2, '#f2c020', 2); }
      else if (c.hd === 'tallspike') { /* v6566-shonen t600u: taller spikes + red headband */
        poly(g, [-13, 0, -16, -16, -9, -12, -12, -28, -4, -16, 0, -32, 5, -18, 11, -30, 10, -12, 16, -18, 13, 0, f * 6, -6, -f * 4, -4], c.hair, 2);
        rr(g, -r - 2, -3, (r + 2) * 2, 5, 2, '#c82028', 2);
        g.fillStyle = '#c82028'; g.fillRect(f * (r - 1), -2, 5, 2); g.fillRect(f * (r + 2), 0, 7, 2); }
      else if (c.hd === 'kasa') { /* v6566-shonen t597u: short hair under a straw kasa */
        g.beginPath(); g.arc(0, -1, r + 1, PI, 0); g.closePath(); g.fill(); g.lineWidth = 2; g.strokeStyle = INK; g.stroke();
        var straw = '#d4b06a', rib = '#a07838';
        poly(g, [0, -r - 15, -r - 16, -1, r + 16, -1], straw, 2.5);
        g.strokeStyle = rib; g.lineWidth = 1.3;
        for (var kasaI = -2; kasaI <= 2; kasaI++) { g.beginPath(); g.moveTo(0, -r - 14); g.lineTo(kasaI * 7, -1); g.stroke(); }
        ell(g, 0, -1, r + 16, 3.2, '#c4a060', 2); }
      else if (c.hd === 'shaggy') { poly(g, [-13, 2, -13, -8, -6, -15, 4, -15, 12, -9, 13, 2, f * 8, -5, f * 2, -2, -f * 6, -4], c.hair, 2); g.fillStyle = '#7ad82a'; poly(g, [f * 8, -5, f * 13, 2, f * 10, -9], '#7ad82a', 0); g.strokeStyle = '#2a2a2a'; g.lineWidth = 3; g.beginPath(); g.arc(0, 0, r + 2, PI * 0.95, PI * 0.05, false); g.stroke(); ell(g, -f * 10, 4, 4, 5, '#2a2a2a', 1.5); }
      /* eyes */
      if (c.hd !== 'curly') { g.fillStyle = INK; var ex = f * 5; g.fillRect(ex - 1, -2, 3, F.st === 'hit' || F.st === 'down' ? 1 : 3); g.fillRect(ex - 6 * f - 1, -2, 2, F.st === 'hit' ? 1 : 3); }
      g.restore(); }
    /* ---------- stages (painted once each) ---------- */
    function stageBg(k) { if (bgL[k]) return bgL[k]; bgL[k] = K.layer(SW, SH, function (g) {
      var sky = { roof: ['#ff8a4a', '#5a2a6a'], shrine: ['#1a2a4a', '#e07a5a'], boiler: ['#2a1a10', '#5a3020'], alley: ['#0a0a1a', '#3a1a3a'], depot: ['#1a2230', '#4a5a6a'], prize: ['#1a0e06', '#4a2a10'] }[k];
      var sg = g.createLinearGradient(0, 0, 0, GY); sg.addColorStop(0, sky[0]); sg.addColorStop(1, sky[1]); g.fillStyle = sg; g.fillRect(0, 0, SW, SH);
      if (k === 'roof') { for (var i = 0; i < 8; i++) rr(g, i * 48 - 10, 250 + (i % 3) * 20, 44, 200, 0, '#3a1a3a', 0); g.fillStyle = '#8a8a96'; g.fillRect(0, GY - 40, SW, 6); for (var j = 0; j < SW; j += 18) g.fillRect(j, GY - 40, 3, 40); ell(g, 300, 120, 30, 30, '#ffd860', 0); g.fillStyle = '#6a6a74'; g.fillRect(0, GY, SW, SH - GY); rr(g, 30, GY - 90, 50, 50, 2, '#7a7a84', 2); }
      if (k === 'shrine') { for (var s2 = 0; s2 < 30; s2++) { g.fillStyle = 'rgba(255,255,255,.6)'; g.fillRect((s2 * 53) % SW, (s2 * 31) % 200, 2, 2); } g.fillStyle = '#c8302a'; g.fillRect(90, 200, 14, 230); g.fillRect(258, 200, 14, 230); g.fillRect(70, 200, 222, 14); g.fillRect(84, 228, 194, 10); g.fillStyle = '#2a1a1a'; g.fillRect(64, 192, 234, 8);
        for (var st = 0; st < 5; st++) { g.fillStyle = st % 2 ? '#6a6a6a' : '#7a7a7a'; g.fillRect(0, GY - 10 + st * 16, SW, 16); } [[40, 380], [322, 380]].forEach(function (p) { rr(g, p[0] - 10, p[1] - 30, 20, 50, 4, '#9a9a9a', 2); g.drawImage(glow('255,200,90', 20), p[0] - 20, p[1] - 44); }); }
      if (k === 'boiler') { for (var pp = 0; pp < 5; pp++) { rr(g, 20 + pp * 70, 60, 26, 320, 8, '#6a4a3a', 3); } rr(g, 110, 160, 140, 200, 30, '#5a3a2a', 4); ell(g, 180, 250, 40, 40, '#2a1a10', 3); g.drawImage(glow('255,120,40', 50), 130, 200); g.fillStyle = '#3a2a20'; g.fillRect(0, GY, SW, SH - GY); for (var gr = 0; gr < SW; gr += 30) { g.fillStyle = '#2a1a14'; g.fillRect(gr, GY, 2, SH - GY); } }
      if (k === 'alley') { rr(g, -10, 60, 130, 380, 0, '#2a1a24', 0); rr(g, 250, 40, 130, 400, 0, '#24182a', 0); g.fillStyle = '#ff5ac8'; g.font = '900 20px sans-serif'; g.save(); g.translate(60, 220); g.rotate(-0.1); g.fillText('PUNKS', -30, 0); g.restore(); g.drawImage(glow('255,90,200', 50), 10, 170); g.drawImage(glow('90,216,255', 40), 270, 130); rr(g, 280, 120, 70, 28, 4, '#0a0610', 2, '#5ad8ff'); txt(g, '\u30b9\u30ca\u30c3\u30af', 315, 134, 12, '#5ad8ff'); g.fillStyle = '#1a1820'; g.fillRect(0, GY, SW, SH - GY); rr(g, 290, GY - 40, 50, 40, 4, '#3a5a3a', 2); }
      if (k === 'depot') { g.fillStyle = '#3a4250'; g.fillRect(40, 80, 282, 300); for (var sl = 0; sl < 18; sl++) { g.fillStyle = sl % 2 ? '#4a5260' : '#444c5a'; g.fillRect(44, 84 + sl * 16, 274, 14); } txt(g, 'BAY 7', 181, 70, 14, '#ffd860'); g.fillStyle = '#4a4a44'; g.fillRect(0, GY, SW, SH - GY); for (var z = 0; z < 12; z++) poly(g, [z * 34, GY + 6, z * 34 + 16, GY + 6, z * 34 + 6, GY + 16, z * 34 - 10, GY + 16], '#ffd040', 0); }
      if (k === 'prize') { [[30, 120], [100, 120], [250, 120], [320, 120]].forEach(function (p, n) { rr(g, p[0] - 26, p[1], 52, 90, 4, 'rgba(255,240,200,.25)', 2); ell(g, p[0], p[1] + 60, 12, 10, ['#f2a0c0', '#90d0f0', '#c8a0f0', '#ffd860'][n], 2); }); rr(g, 140, 90, 82, 120, 6, '#3a2a08', 3); rr(g, 148, 100, 66, 46, 3, '#ffd860', 2); txt(g, '999990', 181, 124, 11, '#3a2a08'); g.fillStyle = '#2a1a10'; g.fillRect(0, GY, SW, SH - GY); for (var tl = 0; tl < SW; tl += 40) { g.fillStyle = '#22150c'; g.fillRect(tl, GY, 20, SH - GY); } }
      /* crowd silhouettes */
      g.fillStyle = 'rgba(0,0,0,.45)'; for (var cr = 0; cr < 10; cr++) { var cx = 10 + cr * 38 + (cr % 2) * 8; ell(g, cx, GY - 46, 9, 10, 'rgba(0,0,0,.45)', 0); rr(g, cx - 13, GY - 36, 26, 40, 8, 'rgba(0,0,0,.45)', 0); }
      g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(0, GY, SW, 4); }); return bgL[k]; }
    /* ---------- fighters ---------- */
    function mk(id, x, face, ai) { var c = CH[id]; return { id: id, c: c, x: x, y: GY, vx: 0, vy: 0, face: face, hp: c.hp, max: c.hp, meter: 0, st: 'idle', stT: 0, mv: null, pose: POSE.idle, flash: 0, crouch: false, ai: ai, aiT: 0, want: {}, inv: 0, air: false, hitDone: false, rushN: 0, cancel: 0 }; }
    var MV = { /* timing: s = startup, a = active, r = recovery, reach, lvl, hs = hitstun, bs = blockstun, kb */
      p: { pose: 'p', s: 0.05, a: 0.08, r: 0.12, reach: 40, lvl: 'mid', hs: 0.24, bs: 0.14, kb: 60 },
      k: { pose: 'k', s: 0.11, a: 0.1, r: 0.24, reach: 56, lvl: 'mid', hs: 0.34, bs: 0.2, kb: 140 },
      ck: { pose: 'ck', s: 0.1, a: 0.1, r: 0.3, reach: 54, lvl: 'low', hs: 0.3, bs: 0.2, kb: 60, kd: 1 },
      jk: { pose: 'jk', s: 0.06, a: 0.5, r: 0.05, reach: 44, lvl: 'over', hs: 0.36, bs: 0.18, kb: 90, air: 1 },
      proj: { pose: 'proj', s: 0.2, a: 0.05, r: 0.36, reach: 0, lvl: 'mid', hs: 0.3, bs: 0.2, kb: 90, chip: 1 },
      dash: { pose: 'dash', s: 0.1, a: 0.26, r: 0.3, reach: 42, lvl: 'mid', hs: 0.4, bs: 0.22, kb: 200, vx: 320, chip: 1, kd: 1 },
      slide: { pose: 'slide', s: 0.08, a: 0.3, r: 0.3, reach: 50, lvl: 'low', hs: 0.4, bs: 0.2, kb: 120, vx: 300, chip: 1, kd: 1 },
      chain: { pose: 'p', s: 0.16, a: 0.12, r: 0.32, reach: 110, lvl: 'mid', hs: 0.4, bs: 0.2, kb: 160, chip: 1 },
      rise: { pose: 'rise', s: 0.03, a: 0.24, r: 0.36, reach: 40, lvl: 'mid', hs: 0.5, bs: 0.2, kb: 120, vy: -470, inv: 0.2, kd: 1, chip: 1 },
      multi: { pose: 'p', s: 0.08, a: 0.6, r: 0.3, reach: 48, lvl: 'mid', hs: 0.16, bs: 0.1, kb: 20, multi: 5, chip: 1 },
      counter: { pose: 'counter', s: 0.03, a: 0.55, r: 0.3, reach: 60, lvl: 'mid', hs: 0.6, bs: 0.2, kb: 220, kd: 1 },
      rush: { pose: 'dash', s: 0.6, a: 0.35, r: 0.4, reach: 46, lvl: 'mid', hs: 1.2, bs: 0.3, kb: 0, vx: 360, chip: 3, sup: 1 },
      drop: { pose: 'rise', s: 0.6, a: 0.25, r: 0.5, reach: 999, lvl: 'mid', hs: 1, bs: 0.3, kb: 120, chip: 4, sup: 1, kd: 1 },
      thr: { pose: 'p', s: 0.07, a: 0.06, r: 0.42, reach: 26, lvl: 'throw', hs: 0.4, bs: 0, kb: 220, kd: 1 } /* v6566-shonen: AI grab, beats auto-block */
    };
    function moveOf(F, k) { var c = F.c, base, dmg, nm;
      if (k === 'p' || k === 'k') { base = F.air ? MV.jk : (F.crouch && k === 'k') ? MV.ck : MV[k]; dmg = c.mv[k][1] * (F.air ? 1.1 : F.crouch && k === 'k' ? 0.9 : 1); nm = F.air ? 'Jump Attack' : F.crouch && k === 'k' ? 'Sweep' : c.mv[k][0]; }
      else if (k === 'thr') { base = MV.thr; dmg = c.w > 1.2 ? 12 : 10; nm = 'Grab'; }
      else { var m = c.mv[k]; base = MV[m[2]]; dmg = m[1]; nm = m[0]; }
      if (k === 'spf' && !F.ai) dmg = Math.round(dmg * 1.25); /* v6566-shonen: the player's spf is the charged SPECIAL */
      var o = {}; for (var q in base) o[q] = base[q]; o.k = k; o.dmg = dmg; o.n = nm;
      if (F.c.w > 1.2) { o.s *= 1.25; o.r *= 1.15; o.reach *= 1.12; } if (F.id === 'jin') { o.s *= 0.85; o.r *= 0.9; }
      if (F.dk) o.dmg = Math.round(o.dmg * F.dk * 10) / 10; /* v6566-handheld: star boost */
      if (k === 'k' && F.id === 'nails' && !F.air && !F.crouch) o.reach = 84; if (k === 'k' && F.id === 'masa' && !F.air && !F.crouch) { o.reach = 66; o.s *= 1.2; }
      return o; }
    function doMove(F, k, force) {
      if (force) { /* v6566-shonen: player chain / special cancel, checked by pAct */ }
      else if (F.st === 'atk' && F.cancel > 0 && F.mv && F.mv.hit && (F.mv.k === 'p' || (F.mv.k === 'k' && k !== 'p'))) { /* chain cancel */ }
      else if (!(F.st === 'idle' || F.st === 'walk' || F.st === 'crouch' || (F.st === 'jump' && (k === 'p' || k === 'k')))) return false;
      if (k === 'su') { if (F.meter < 100) return false; F.meter = 0; superFlash = 0.6; freeze = 0.5; if (HH && HH.on && !F.ai) { try { HH.on('super'); } catch (eHH) {} } say(F.c.mv.su[0].toUpperCase() + '!', 1.2); drum('k', now(), 0.6); tone(220, now(), 0.5, 'sawtooth', 0.08); tone(440, now() + 0.2, 0.5, 'square', 0.07); }
      F.mv = moveOf(F, k); F.st = 'atk'; F.stT = 0; if (k === 'thr') say('GRAB!', 0.6); if (k === 'spf' && !F.ai) flashFx(F.x, F.y - 70, F.c.aura); F.hitDone = false; F.cancel = 0; F.rushN = 0; F.mv.hit = false;
      if (F.mv.inv) F.inv = F.mv.inv; if (F.mv.vy) { F.vy = F.mv.vy; F.air = true; F.vx = F.face * 60; }
      tone(k === 'p' ? 520 : k === 'k' ? 330 : 260, now(), 0.06, 'square', 0.035); return true; }
    function say(m, d) { msg = m; msgT = d || 1; }
    function boost(F, k, h, sp) { var c = {}, q0; for (q0 in F.c) c[q0] = F.c[q0]; c.hp = Math.round(c.hp * (h || 1)); c.spd = Math.round(c.spd * (sp || 1)); F.c = c; F.hp = F.max = c.hp; F.dk = k || 1; } /* v6566-handheld: a fighter's stars */
    function setupMatch() { var me = ORDER[sel], foe = lad[G.stage]; P = mk(me, 110, 1, false); E = mk(foe, 252, -1, true);
      if (HH) { boost(P, HH.pk, HH.ph, HH.ps); boost(E, HH.ek, HH.eh, HH.es); P.dbl = String(HH.dbl || '').indexOf('p') >= 0; E.dbl = String(HH.dbl || '').indexOf('e') >= 0; }
      rnd = 1; wins = [0, 0]; startRound(); }
    function startRound() { P.x = 110; E.x = 252; P.y = E.y = GY; P.hp = P.max; E.hp = E.max; [P, E].forEach(function (F) { F.st = 'idle'; F.stT = 0; F.vx = F.vy = 0; F.air = false; F.mv = null; F.flash = 0; F.inv = 0; F.pose = POSE.idle; });
      roundT = 60; phase = 'pre'; rT = 0; spHold = -1; jumpQ = 0; buf = null; bufT = 0; fx = []; proj = []; combo = 0; comboT = 0; slow = 0; shake = 0; freeze = 0; }
    G.start = function () { selT = 0; G.stage = 0; G.score = 0;
      if (HH) { sel = Math.max(0, ORDER.indexOf(HH.me)); lad = [HH.foe]; G.stages = [{ n: 'VS ' + CH[HH.foe].n, sub: CH[HH.foe].where, k: HH.foe }]; setupMatch(); phase = 'vs'; return 'intro'; } /* v6566-handheld: one match, no select */
      phase = 'select'; return 'select'; };
    function confirmSel() { var me = ORDER[sel]; lad = LADDER.filter(function (k) { return k !== me; }).slice(0, 5);
      G.stages = lad.map(function (k) { return { n: 'VS ' + CH[k].n, sub: CH[k].where, k: k }; }); tone(1046, now(), 0.15, 'square', 0.07); tone(1568, now() + 0.12, 0.25, 'square', 0.07); setupMatch(); phase = 'vs'; }
    G.cont = function () { setupMatch(); };
    G.next = function () { G.stage++; setupMatch(); };
    G.bonus = function () { return [['Match won', 1500 + G.stage * 1000], ['Rounds dropped ' + wins[1], wins[1] ? 0 : 2500]]; };
    /* VS splash on the stage intro */
    G.introDraw = function (q, t) { if (!P || !E) return; var k = Math.min(1, t * 2.5);
      var bg = q.createLinearGradient(0, 0, SW, SH); bg.addColorStop(0, '#2a0a06'); bg.addColorStop(0.5, '#140608'); bg.addColorStop(1, '#06102a'); q.fillStyle = bg; q.fillRect(0, 0, SW, SH);
      poly(q, [0, 0, SW * 0.62, 0, SW * 0.38, SH, 0, SH], 'rgba(255,120,40,.22)', 0); poly(q, [SW * 0.62, 0, SW, 0, SW, SH, SW * 0.38, SH], 'rgba(90,160,255,.2)', 0);
      var a = { c: P.c, pose: POSE.win, face: 1, flash: 0, x: 90 - (1 - k) * 160, y: 360, st: 'idle' }, b = { c: E.c, pose: POSE.idle, face: -1, flash: 0, x: 272 + (1 - k) * 160, y: 360, st: 'idle' };
      drawFighter(q, a, t, 1.9); drawFighter(q, b, t, 1.9);
      otxt(q, P.c.n, 90, 400, P.c.n.length > 8 ? 17 : 22, '#ffd860'); otxt(q, E.c.n, 272, 400, E.c.n.length > 8 ? 17 : 22, '#7fe8ff'); txt(q, P.c.full, 90, 422, 9, '#fff', 'center', 700); txt(q, E.c.full, 272, 422, 9, '#fff', 'center', 700);
      otxt(q, 'VS', SW / 2, 230, 54 + Math.sin(t * 12) * 3, '#ff5a3a'); txt(q, HH ? (HH.title || 'VS CPU') : 'MATCH ' + (G.stage + 1) + ' / 5', SW / 2, 54, 13, '#ffd860'); txt(q, E.c.where, SW / 2, 74, 11, '#e8e0f8', 'center', 700);
      if (!HH && G.stage === 4) otxt(q, 'FINAL BOSS', SW / 2, 470, 18, '#ff4a5a'); if (HH && HH.dbl) { var dp = String(HH.dbl).indexOf('p') >= 0, de = String(HH.dbl).indexOf('e') >= 0; if (dp) otxt(q, 'CHEAT: DOUBLE SHOT', SW / 2, de ? 452 : 470, 16, '#7aff9a'); if (de) otxt(q, '???: A HIDDEN RULE', SW / 2, 470 + (dp ? 8 : 0), 16, '#ff4a5a'); } };
    /* ---------- input ---------- */
    /* v6566-shonen: ATTACK (a) / SPECIAL (sp) only. SPECIAL fires on release (tap vs hold); with a full bar it fires the SUPER on press. */
    G.press = function (k) {
      if (phase === 'select') { if (k === 'a' || k === 'sp') { if (selT > 0.3) confirmSel(); } return; }
      if (phase !== 'fight') return;
      if (k === 'a') { buf = 'a'; bufT = 0.26; return; }
      if (k === 'sp') { if (P && P.meter >= 100) { buf = 'su'; bufT = 0.3; spHold = -1; } else spHold = 0; } };
    G.release = function (k) { if (k !== 'sp' || spHold < 0) return; var h = spHold; spHold = -1; if (phase !== 'fight') return; buf = h >= CHG ? 'spf' : 'sp'; bufT = 0.3; };
    G.swipeUp = function (dx) { if (phase !== 'fight') return; jumpQ = 0.25; jumpDir = dx ? (dx > 0 ? 1 : -1) : 0; };
    G.dir = function (d) { if (phase === 'select') { if (d === 'l') sel = (sel + 5) % 6; if (d === 'r') sel = (sel + 1) % 6; if (d === 'u' || d === 'd') sel = (sel + 3) % 6; selT = 0.31; tone(660, now(), 0.04, 'square', 0.04); } };
    G.tap = function (x, y, id) { if (phase === 'select') { var i = selHit(x, y); if (i >= 0) { if (i === sel && selT > 0.25) confirmSel(); else { sel = i; selT = 0.26; tone(660, now(), 0.04, 'square', 0.04); } } return; }
      sw[id] = { x: x, y: y, t: performance.now() }; };
    /* swipe up anywhere on the screen = jump (fires as soon as the finger has gone up 32 px; a diagonal sets the jump direction) */
    G.drag = function (x, y, id) { var S0 = sw[id]; if (!S0 || S0.done || phase !== 'fight') return; var dx = x - S0.x, dy = y - S0.y; if (-dy > 32 && -dy > Math.abs(dx) * 0.8) { S0.done = 1; G.swipeUp(Math.abs(dx) > 24 ? dx : 0); } };
    G.lift = function (id) { delete sw[id]; };
    function selHit(x, y) { for (var i = 0; i < 6; i++) { var cx = 34 + (i % 3) * 102, cy = 280 + ((i / 3) | 0) * 92; if (x > cx && x < cx + 92 && y > cy && y < cy + 84) return i; } return -1; }
    G.lit = function () { return false; }; /* v6566-shonen: SPECIAL glows instead (panel.btns[1].glow) */
    /* ---------- AI ---------- */
    function aiThink(F, O, dt) { var lv = HH ? HH.lv : G.stage, W = F.want; F.aiT -= dt; var dist = Math.abs(O.x - F.x);
      if (F.aiT > 0) return; F.aiT = Math.max(0.1, 0.34 - lv * 0.05) * (0.7 + Math.random() * 0.6);
      W.mv = 0; W.crouch = false; W.block = false; W.act = null; W.jump = false;
      var oAtk = O.st === 'atk' && O.stT < O.mv.s + O.mv.a, r = Math.random();
      var incoming = proj.some(function (q) { return q.o === O && Math.abs(q.x - F.x) < 150 && (q.vx > 0) === (F.x > q.x); });
      if (incoming) { if (r < 0.25 + lv * 0.1) { W.jump = true; W.mv = 1; } else if (r < 0.55 + lv * 0.1) W.block = true; return; }
      if (oAtk && dist < 120 && r < 0.2 + lv * 0.14) { W.block = true; W.crouch = O.mv.lvl === 'low' && Math.random() < 0.5 + lv * 0.1; F.aiT = 0.35; return; }
      if (O.air && dist < 130 && O.vy > -200 && r < 0.15 + lv * 0.12) { W.act = 'spu'; return; }
      if (F.meter >= 100 && dist < 130 && r < 0.6) { W.act = 'su'; return; }
      /* v6566-shonen: the player auto-blocks, so the AI punishes recovery and grabs a turtle */
      if (!O.ai && O.st === 'atk' && O.mv && O.stT >= O.mv.s + O.mv.a && dist < 90 && r < 0.3 + lv * 0.12) { W.act = dist < 56 ? 'p' : 'k'; return; }
      if (!O.ai && !O.air && (O.st === 'idle' || O.st === 'walk' || O.st === 'block')) { if (dist < 58 && r < 0.22 + lv * 0.07) { W.act = 'thr'; return; } if (dist < 100 && r < 0.12 + lv * 0.04) { W.mv = 1; F.aiT *= 0.6; return; } }
      if (dist > 170) { if (r < 0.28 && F.c.mv.sp[2] === 'proj') W.act = 'sp'; else if (r < 0.4) W.act = 'spf'; else W.mv = 1; return; }
      if (dist > 70) { if (r < 0.15) { W.jump = true; W.mv = 1; F.jumpAtk = true; } else if (r < 0.35) W.act = 'k'; else if (r < 0.45 && F.c.mv.spf[2] === 'chain') W.act = 'spf'; else W.mv = 1; return; }
      if (r < 0.36) { W.act = 'p'; F.chainPlan = lv >= 2 && Math.random() < 0.3 + lv * 0.1; } else if (r < 0.56) W.act = 'k'; else if (r < 0.7) { W.crouch = true; W.act = 'k'; } else if (r < 0.78) W.act = 'sp'; else if (r < 0.88) W.mv = -1; else W.block = true; }
    /* ---------- simulation ---------- */
    function ctrl(F, O, dt) {
      var W, away;
      if (F.ai) { aiThink(F, O, dt); W = F.want; }
      else { var I = G.in, fwd = F.face > 0 ? I.r : I.l, bk = F.face > 0 ? I.l : I.r; W = { mv: fwd ? 1 : bk ? -1 : 0, crouch: false, jump: jumpQ > 0 || !!I.u, block: false, act: null };
        if (W.jump && !W.mv && jumpDir) W.mv = jumpDir * F.face;
        if (pAct(F)) return; }
      F.crouch = false; F.blockW = W.block || (!F.ai && W.mv < 0);
      if (F.st === 'idle' || F.st === 'walk' || F.st === 'crouch') {
        if (W.act && doMove(F, W.act)) { if (!F.ai) { buf = null; bufT = 0; } else W.act = null; return; }
        if (W.jump) { if (!F.ai) { jumpQ = 0; jumpDir = 0; } F.st = 'jump'; F.air = true; F.vy = -540; F.vx = W.mv * F.c.spd * 1.25 * F.face; F.stT = 0; tone(300, now(), 0.05, 'triangle', 0.03); W.jump = false; return; }
        if (W.crouch) { F.st = 'crouch'; F.crouch = true; F.vx = 0; return; }
        if (W.mv) { F.st = 'walk'; F.vx = W.mv * F.c.spd * (W.mv < 0 ? 0.8 : 1) * F.face; } else { F.st = 'idle'; F.vx = 0; }
      } else if (F.st === 'jump') { if (W.act === 'p' || W.act === 'k') { doMove(F, W.act); if (!F.ai) { buf = null; bufT = 0; } else W.act = null; } else if (F.ai && F.jumpAtk && O && Math.abs(O.x - F.x) < 90 && F.vy > -100) { doMove(F, 'k'); F.jumpAtk = false; } }
      else if (F.st === 'atk' && W.act && F.cancel > 0) { if (doMove(F, W.act)) { if (!F.ai) { buf = null; bufT = 0; } else W.act = null; } }
      if (F.ai && F.chainPlan && F.st === 'atk' && F.cancel > 0) { F.chainPlan = false; doMove(F, Math.random() < 0.5 ? 'k' : 'spf'); }
    }
    /* v6566-shonen: the player's two buttons. ATTACK chains P > P > K (tap again from the end of the active frames, or on hit);
       SPECIAL / charged / SUPER come out from neutral or cancel a connected ATTACK. */
    function pAct(F) { if (!(bufT > 0 && buf)) return false; var k = buf, ok = false, m = F.mv;
      if (k === 'a') {
        if (F.st === 'atk' && m && !F.air && F.chainN > 0 && F.chainN < 3 && (m.k === 'p' || m.k === 'k') && (F.cancel > 0 || F.stT >= m.s + m.a)) { ok = doMove(F, F.chainN === 1 ? 'p' : 'k', true); if (ok) F.chainN++; }
        else if (F.st === 'idle' || F.st === 'walk') { ok = doMove(F, 'p'); if (ok) F.chainN = 1; }
        else if (F.st === 'jump') { ok = doMove(F, 'k'); F.chainN = 0; }
      } else if (!F.air) {
        if (F.st === 'idle' || F.st === 'walk') ok = doMove(F, k);
        else if (F.st === 'atk' && m && F.cancel > 0 && m.hit && (m.k === 'p' || m.k === 'k')) { if (k !== 'su' || F.meter >= 100) ok = doMove(F, k, true); }
        if (ok) F.chainN = 0; }
      if (ok) { buf = null; bufT = 0; } return ok; }
    function hitTest(F, O) { var m = F.mv; if (!m || m.k === 'sp' && m.pose === 'proj') return;
      if (m.reach >= 999) return true; /* drop: hits anywhere */
      var dx = (O.x - F.x) * F.face; if (dx < -10) return false; if (dx > m.reach + 18 * O.c.w) return false;
      if (m.lvl === 'low' && O.air) return false; if (!m.air && O.air && O.y < GY - 70 && m.k !== 'spu') return false; return true; }
    /* v6566-shonen t606u: hitstop on a landed hit. Jab ~0.045s, kick/special ~0.06s, scaled by damage and capped at 0.09s.
       Blocked hits ~0.03s. Follow-up hits of a multi are shorter so a slap string does not freeze the round. Super's own 0.5s freeze is never shortened.
       bufT / jumpQ do not tick while freeze > 0 (see G.step), so a buffered ATTACK or SPECIAL is still there after the pause; F.cancel also holds because stepF is skipped. */
    function hitStop(m, blocked, follow) {
      if (G.noHS) return;
      if (follow) { freeze = Math.max(freeze, 0.02); return; }
      if (blocked) { freeze = Math.max(freeze, 0.03); return; }
      var base = (m && m.k === 'p') ? 0.045 : 0.06, dmg = (m && m.dmg) || 8;
      freeze = Math.max(freeze, Math.min(0.09, base * Math.max(1, dmg / 9)));
    }
    function land(F, O, m, mult) {
      if (O.inv > 0) return 'whiff';
      if (O.st === 'atk' && O.mv && O.mv.pose === 'counter' && O.stT >= O.mv.s && O.stT < O.mv.s + O.mv.a && !m.sup) { /* Shades Flash */ O.stT = O.mv.s + O.mv.a; O.inv = 0.3; flashFx(O.x, O.y - 70, '255,216,96'); say('COUNTER!', 0.8); var mm = moveOf(O, 'sp'); mm.dmg = 12; applyHit(O, F, mm, 1); return 'counter'; }
      if (m.lvl === 'throw') { if (O.air || O.st === 'hit' || O.st === 'down') return 'whiff'; applyHit(F, O, m, 1); return 'hit'; }
      var canBlock, crouchB = false;
      if (!O.ai) canBlock = !O.air && !(O.lockT > 0) && (O.st === 'idle' || O.st === 'walk' || O.st === 'block'); /* v6566-shonen: auto-block, no high / low */
      else { canBlock = O.blockW && !O.air && (O.st === 'idle' || O.st === 'walk' || O.st === 'crouch' || O.st === 'block'); crouchB = O.want.crouch;
        if (canBlock && ((m.lvl === 'low' && !crouchB) || (m.lvl === 'over' && crouchB))) canBlock = false; }
      if (canBlock) { O.st = 'block'; O.stT = 0; O.bsT = m.bs; O.crouch = crouchB; O.vx = -O.face * 80; O.hp = Math.max(1, O.hp - (m.chip || 0)); O.meter = Math.min(100, O.meter + (O.ai ? 3 : 2)); F.meter = Math.min(100, F.meter + 2); if (!O.ai) G._blocks = (G._blocks | 0) + 1; fx.push({ k: 'blk', x: (F.x + O.x) / 2, y: O.y - 60, t: 0 }); tone(900, now(), 0.04, 'square', 0.04); hitStop(m, true, F.rushN > 1); return 'block'; }
      applyHit(F, O, m, mult || 1); return 'hit'; }
    function applyHit(F, O, m, mult) { var d = Math.round(m.dmg * mult); O.hp = Math.max(0, O.hp - d); O.flash = 0.08; O.meter = Math.min(100, O.meter + 5); F.meter = Math.min(100, F.meter + 8);
      var kb = m.kb || 60;
      if (F.chainN === 3 && !m.kd) kb = Math.round(kb * 1.2); /* v6566-shonen: a little more push on the P>P>K finisher */
      if (m.kd || O.air || O.hp <= 0) { O.st = 'down'; O.stT = 0; O.vy = O.air ? O.vy : -260; O.air = true; O.vx = -O.face * 120; } else { O.st = 'hit'; O.stT = 0; O.hsT = m.hs; O.vx = -O.face * kb; }
      if (m) m.hit = true; F.cancel = 0.2; hitStop(m, false, F.rushN > 1);
      if (F === P) { combo = comboT > 0 ? combo + 1 : 1; comboT = 0.9; G.score += d * 10 + (combo >= 3 ? combo * 60 : 0); } else { combo = 0; }
      shake = Math.min(0.25, 0.05 + d * 0.008); fx.push({ k: 'hit', x: (F.x + O.x) / 2 + O.face * -10, y: O.y - 64 - Math.random() * 20, t: 0, big: d >= 9 }); drum(d >= 9 ? 'k' : 's', now(), d >= 9 ? 0.5 : 0.3); tone(180 + d * 10, now(), 0.06, 'square', 0.04);
      if (O.hp <= 0) { slow = 1; say('K.O.', 2); drum('k', now(), 0.7); drum('k', now() + 0.2, 0.6); } }
    function flashFx(x, y, c) { fx.push({ k: 'flash', x: x, y: y, t: 0, c: c }); }
    function stepF(F, O, dt) {
      F.stT += dt; F.lockT = Math.max(0, (F.lockT || 0) - dt); F.flash = Math.max(0, F.flash - dt); F.inv = Math.max(0, F.inv - dt); F.cancel = Math.max(0, F.cancel - dt);
      if (F.st === 'atk') { var m = F.mv, T = F.stT;
        if (m.vx && T > m.s && T < m.s + m.a) F.vx = F.face * m.vx; else if (!F.air) F.vx *= 0.8;
        if (T >= m.s && T < m.s + m.a) {
          if (m.pose === 'proj' && !F.hitDone) { F.hitDone = true; var sp = F.id === 'aoi' ? 200 : F.id === 'jin' ? 330 : 260; proj.push({ x: F.x + F.face * 30, y: F.y - 66, vx: F.face * sp, o: F, m: m, t: 0, col: F.c.aura }); tone(400, now(), 0.15, 'sawtooth', 0.05); }
          else if (m.multi && hitTest(F, O)) { var n = Math.floor((T - m.s) / (m.a / m.multi)); if (n > (F.rushN | 0) - 1 && F.rushN < m.multi) { F.rushN++; var mm = {}; for (var q in m) mm[q] = m[q]; mm.dmg = m.dmg / m.multi; land(F, O, mm, 1); } }
          else if (m.sup && hitTest(F, O)) { if (!F.hitDone) { F.hitDone = true; F.rushN = 1; if (land(F, O, m, 0.3) === 'hit') { F.rushHit = true; } } else if (F.rushHit && F.rushN < 7 && T > m.s + F.rushN * 0.05) { F.rushN++; O.hp = Math.max(0, O.hp - Math.round(m.dmg * 0.1)); O.flash = 0.06; if (F === P) G.score += 60; fx.push({ k: 'hit', x: O.x, y: O.y - 50 - Math.random() * 40, t: 0, big: true }); drum('s', now(), 0.3); if (O.hp <= 0 && O.st !== 'down') { O.st = 'down'; O.air = true; O.vy = -300; slow = 1; say('K.O.', 2); if (F === P) G.score += 2000; } } }
          else if (!m.multi && !m.sup && m.pose !== 'proj' && m.pose !== 'counter' && !F.hitDone && hitTest(F, O)) { F.hitDone = true; land(F, O, m, 1); }
        }
        /* v6566-handheld DOUBLE SHOT: the special fires again the moment its active frames end, skipping the recovery (no recharge) */
        if (F.dbl && !m.twin && (m.k === 'sp' || m.k === 'spf') && T >= m.s + m.a && F.hp > 0 && phase === 'fight') { var k2 = m.k; if (doMove(F, k2, true)) { F.mv.twin = true; F.mv.s = Math.min(F.mv.s, 0.06); say('DOUBLE SHOT!', 0.6); } return; }
        if (m.air) { if (!F.air) { F.st = 'idle'; F.mv = null; if (!F.ai) F.lockT = LOCK; } }
        else if (T >= m.s + m.a + m.r && !F.air) { F.st = 'idle'; F.mv = null; F.rushHit = false; if (!F.ai) { F.lockT = LOCK; F.chainN = 0; } }
      }
      else if (F.st === 'hit') { F.vx *= 0.85; if (F.stT > F.hsT) F.st = 'idle'; }
      else if (F.st === 'block') { F.vx *= 0.8; if (F.stT > F.bsT) F.st = 'idle'; }
      else if (F.st === 'down') { if (!F.air) { F.vx *= 0.8; if (F.hp > 0 && F.stT > 0.9) { F.st = 'idle'; F.inv = 0.4; } } }
      /* physics */
      if (F.air) { F.vy += 1500 * dt; F.y += F.vy * dt; if (F.y >= GY) { F.y = GY; F.vy = 0; F.air = false; if (F.st === 'jump') F.st = 'idle'; if (F.st === 'down') F.stT = Math.min(F.stT, 0.3); } }
      F.x = clamp(F.x + F.vx * dt, X0, X1);
      /* pose */
      var tgt = POSE[F.st === 'atk' ? F.mv.pose : F.st === 'walk' ? 'walk' : F.st === 'jump' ? 'jump' : F.st === 'crouch' ? 'crouch' : F.st === 'block' ? (F.crouch ? 'cblock' : 'block') : F.st === 'hit' ? 'hit' : F.st === 'down' ? 'down' : F.st === 'win' ? 'win' : F.st === 'lose' ? 'lose' : 'idle'] || POSE.idle;
      if (F.st === 'walk') { var ph = Math.sin(F.stT * 10); tgt = { hip: 52 + Math.abs(ph) * 2, lean: 0.1, fa: tgt.fa, ba: tgt.ba, fl: [0.3 * ph + 0.1, -0.2 - Math.max(0, ph) * 0.4], bl: [-0.3 * ph - 0.1, -0.2 - Math.max(0, -ph) * 0.4] }; }
      if (F.st === 'idle') { var b2 = Math.sin(performance.now() / 160 + (F.ai ? 1 : 0)); tgt = lerpPose(POSE.idle, POSE.idle, 0); tgt.hip += b2 * 1.5; }
      var snap = F.st === 'atk' || F.st === 'hit' ? 0.6 : 0.3; F.pose = lerpPose(F.pose, tgt, Math.min(1, snap * dt * 60));
    }
    G.step = function (dt) {
      if (phase === 'select') { selT += dt; return; }
      if (phase === 'vs') { phase = 'pre'; rT = 0; return 'go'; }
      fx.forEach(function (F) { F.t += dt; }); fx = fx.filter(function (F) { return F.t < 0.35; }); msgT = Math.max(0, (msgT || 0) - dt); shake = Math.max(0, shake - dt); superFlash = Math.max(0, superFlash - dt);
      if (freeze > 0) { freeze = Math.max(0, freeze - dt); if (freeze > 0) return; } /* v6566-shonen t606u: bufT holds through hitstop so a buffered input is not eaten */
      bufT = Math.max(0, bufT - dt); jumpQ = Math.max(0, jumpQ - dt); if (spHold >= 0 && phase === 'fight') spHold += dt; comboT -= dt;
      var sdt = slow > 0 ? dt * 0.3 : dt; slow = Math.max(0, slow - dt);
      rT += dt;
      if (phase === 'pre') { if (rT < 0.05) say('ROUND ' + rnd, 1); if (rT > 1.0 && rT - dt <= 1.0) { say('FIGHT!', 0.7); tone(880, now(), 0.2, 'square', 0.07); } if (rT > 1.4) { phase = 'fight'; rT = 0; } stepF(P, E, sdt); stepF(E, P, sdt); return; }
      if (phase === 'fight') {
        roundT -= sdt;
        ctrl(P, E, sdt); ctrl(E, P, sdt);
        if (P.st !== 'atk' && P.st !== 'down' && !P.air) P.face = E.x >= P.x ? 1 : -1; if (E.st !== 'atk' && E.st !== 'down' && !E.air) E.face = P.x >= E.x ? 1 : -1;
        stepF(P, E, sdt); stepF(E, P, sdt);
        var gap = Math.abs(P.x - E.x), mn = 30 * (P.c.w + E.c.w) / 2; if (gap < mn && !P.air && !E.air) { var push = (mn - gap) / 2, d = P.x < E.x ? -1 : 1; P.x = clamp(P.x + d * push, X0, X1); E.x = clamp(E.x - d * push, X0, X1); }
        proj.forEach(function (q) { q.t += sdt; q.x += q.vx * sdt; var O = q.o === P ? E : P; if (!q.dead && Math.abs(O.x - q.x) < 22 * O.c.w && (O.y - 120 < q.y && O.y > q.y - 10) && !(O.st === 'down')) { q.dead = 1; var mm = q.m; land(q.o, O, mm, 1); } });
        for (var i = 0; i < proj.length; i++) for (var j = i + 1; j < proj.length; j++) { var a = proj[i], b = proj[j]; if (a.o !== b.o && Math.abs(a.x - b.x) < 20) { a.dead = b.dead = 1; flashFx((a.x + b.x) / 2, a.y, '255,255,255'); } }
        proj = proj.filter(function (q) { return !q.dead && q.x > -20 && q.x < SW + 20; });
        if (P.hp <= 0 || E.hp <= 0 || roundT <= 0) { phase = 'ko'; rT = 0; if (roundT <= 0 && P.hp > 0 && E.hp > 0) say('TIME', 1.2); }
        return; }
      if (phase === 'ko') { stepF(P, E, sdt); stepF(E, P, sdt); if (rT > 1.6) { var pw = P.hp / P.max >= E.hp / E.max && P.hp > 0;
          if (pw) { wins[0]++; P.st = 'win'; E.st = E.hp > 0 ? 'lose' : 'down'; var tb = Math.max(0, Math.ceil(roundT)) * 40, vb = P.hp * 20, pb = P.hp >= P.max ? 3000 : 0; G.score += tb + vb + pb; say(pb ? 'PERFECT!' : 'YOU WIN', 1.6); fx.push({ k: 'tally', t: 0, s: 'TIME +' + tb + '  VITALITY +' + vb + (pb ? '  PERFECT +3000' : '') }); }
          else { wins[1]++; E.st = 'win'; P.st = P.hp > 0 ? 'lose' : 'down'; say('YOU LOSE', 1.6); }
          phase = 'post'; rT = 0; } return; }
      if (phase === 'post') { stepF(P, E, sdt); stepF(E, P, sdt); if (rT > 2.2) { if (wins[0] >= 2) { phase = 'done'; return G.stage >= 4 ? 'win' : 'clear'; } if (wins[1] >= 2) { phase = 'done'; return 'dead'; } rnd++; startRound(); } return; }
    };
    /* ---------- drawing ---------- */
    G.draw = function (g, t) {
      if (phase === 'select') return drawSelect(g, t);
      if (!P) return;
      var ox = shake > 0 ? (Math.random() - 0.5) * shake * 40 : 0; g.save(); g.translate(ox, 0);
      K.blit(g, stageBg(E.c.stage), 0, 0);
      if (superFlash > 0) { g.fillStyle = 'rgba(0,0,0,' + Math.min(0.6, superFlash * 1.5) + ')'; g.fillRect(0, 0, SW, SH); }
      proj.forEach(function (q) { var r = 14 + Math.sin(q.t * 30) * 2; g.drawImage(glow(q.col, 30), q.x - 30, q.y - 30); ell(g, q.x, q.y, r * 0.7, r * 0.55, 'rgba(' + q.col + ',.9)', 2);
        if (q.o.id === 'aoi') { rr(g, q.x - 6, q.y - 10, 12, 20, 2, '#f8f0d8', 2); g.fillStyle = '#c8302a'; g.fillRect(q.x - 3, q.y - 6, 6, 10); } if (q.o.id === 'masa') { ell(g, q.x, q.y, 6, 6, '#8a96a8', 2); } });
      var back = P.st === 'atk' ? E : P, front = back === P ? E : P; drawFighter(g, back, t); drawFighter(g, front, t);
      if (superFlash > 0) { var F0 = P.meter === 0 && P.st === 'atk' && P.mv && P.mv.sup ? P : E; g.drawImage(glow(F0.c.aura, 80), F0.x - 80, F0.y - 150); }
      fx.forEach(function (F) { var a = 1 - F.t / 0.35;
        if (F.k === 'hit') { g.globalAlpha = a; g.drawImage(glow('255,240,160', F.big ? 34 : 24), F.x - (F.big ? 34 : 24), F.y - (F.big ? 34 : 24)); g.strokeStyle = '#fff'; g.lineWidth = 3; for (var i = 0; i < 6; i++) { var an = i * 1.05, r1 = 6 + F.t * 80; g.beginPath(); g.moveTo(F.x + Math.cos(an) * r1, F.y + Math.sin(an) * r1); g.lineTo(F.x + Math.cos(an) * (r1 + 10), F.y + Math.sin(an) * (r1 + 10)); g.stroke(); } g.globalAlpha = 1; }
        else if (F.k === 'blk') { g.globalAlpha = a; g.strokeStyle = '#7fe8ff'; g.lineWidth = 4; g.beginPath(); g.arc(F.x, F.y, 10 + F.t * 60, -1, 1); g.stroke(); g.globalAlpha = 1; }
        else if (F.k === 'flash') { g.globalAlpha = a; g.drawImage(glow(F.c, 50), F.x - 50, F.y - 50); g.globalAlpha = 1; } });
      g.restore();
      hud(g, t);
    };
    function bar(g, x, y, w, v, max, flip, col) { rr(g, x, y, w, 16, 4, '#1a0a0a', 2.5); var k = clamp(v / max, 0, 1), bw = (w - 4) * k; rr(g, flip ? x + w - 2 - bw : x + 2, y + 2, bw, 12, 3, k > 0.3 ? col : '#ff3a3a', 0); }
    function hud(g, t) {
      bar(g, 10, 30, 146, P.hp, P.max, false, '#ffd860'); bar(g, SW - 156, 30, 146, E.hp, E.max, true, '#ffd860');
      txt(g, P.c.n, 12, 56, 12, '#fff', 'left'); txt(g, E.c.n, SW - 12, 56, 12, '#fff', 'right');
      for (var i = 0; i < 2; i++) { ell(g, SW / 2 - 34 - i * 14, 56, 5, 5, i < wins[0] ? '#ffd860' : 'rgba(255,255,255,.2)', 1.5); ell(g, SW / 2 + 34 + i * 14, 56, 5, 5, i < wins[1] ? '#ffd860' : 'rgba(255,255,255,.2)', 1.5); } /* v6566-shonen: round pips beside the timer so long names fit */
      rr(g, SW / 2 - 22, 28, 44, 34, 6, 'rgba(0,0,0,.6)', 2, '#ffd860'); mono(g, String(Math.max(0, Math.ceil(roundT))), SW / 2, 46, 20, roundT < 10 ? '#ff4a5a' : '#ffd860', 'center');
      /* super bars */
      /* v6566-shonen: one super bar (yours), wide; when full it pulses and says to tap SPECIAL */
      var full = P.meter >= 100; rr(g, 10, SH - 30, SW - 20, 18, 6, '#0a0614', 2.5); rr(g, 13, SH - 27, (SW - 26) * clamp(P.meter / 100, 0, 1), 12, 4, full ? (((t * 6) | 0) % 2 ? '#ff5ac8' : '#ffd860') : '#5ad8ff', 0);
      txt(g, full ? (HH ? 'SUPER READY \u00b7 TAP B' : 'SUPER READY \u00b7 TAP SPECIAL') : 'SUPER', SW / 2, SH - 21, full ? 11 : 10, full ? INK : 'rgba(255,255,255,.85)');
      if (combo >= 2 && comboT > 0) { otxt(g, combo + ' HITS', 70, 120, 20, '#ffd860'); }
      if (msgT > 0) otxt(g, msg, SW / 2, 200, msg.length > 10 ? 24 : 40, msg === 'K.O.' ? '#ff4a3a' : '#fff');
      fx.forEach(function (F) { if (F.k === 'tally') txt(g, F.s, SW / 2, 250, 11, '#7aff9a'); });
      if (phase === 'post' || phase === 'ko') { var tl = null; fx.forEach(function (F) { if (F.k === 'tally') tl = F; }); }
    }
    function drawSelect(g, t) {
      var bg = g.createLinearGradient(0, 0, 0, SH); bg.addColorStop(0, '#2a0a06'); bg.addColorStop(1, '#0a0614'); g.fillStyle = bg; g.fillRect(0, 0, SW, SH);
      var c = CH[ORDER[sel]]; g.drawImage(glow(c.aura, 90), 90 - 90, 170 - 90);
      drawFighter(g, { c: c, pose: lerpPose(POSE.idle, POSE.idle, 0), face: 1, flash: 0, x: 92, y: 250, st: 'idle' }, t, 1.6);
      /* v6566-shonen t604u: keep the tall hair at full size; paint the title last so it sits above the spikes */
      otxt(g, 'SELECT YOUR FIGHTER', SW / 2, 44, 20, '#ffd860');
      otxt(g, c.n, 262, 84, c.n.length > 9 ? 20 : 24, '#fff'); txt(g, c.full, 262, 108, 10, '#ffd860');
      var M = c.mv; [['TAP SPECIAL', M.sp[0]], ['HOLD SPECIAL', M.spf[0]], ['FULL BAR \u00b7 SUPER', M.su[0]]].forEach(function (q, i) { txt(g, q[0], 190, 130 + i * 30, 9, '#7fe8ff', 'left'); txt(g, q[1], 190, 143 + i * 30, 12, '#fff', 'left', 800); });
      txt(g, 'HP ' + c.hp + '  \u00b7  SPEED ' + c.spd, 262, 232, 10, 'rgba(255,255,255,.7)');
      for (var i = 0; i < 6; i++) { var C0 = CH[ORDER[i]], x = 34 + (i % 3) * 102, y = 280 + ((i / 3) | 0) * 92, on = i === sel;
        rr(g, x, y, 92, 84, 10, on ? 'rgba(' + C0.aura + ',.35)' : 'rgba(255,255,255,.06)', on ? 4 : 2, on ? '#ffd860' : 'rgba(255,255,255,.25)');
        g.save(); g.beginPath(); g.rect(x + 2, y + 2, 88, 80); g.clip(); drawFighter(g, { c: C0, pose: POSE.idle, face: 1, flash: 0, x: x + 46, y: y + 124, st: 'idle' }, t, 1.0); g.restore();
        txt(g, C0.n, x + 46, y + 74, C0.n.length > 9 ? 10 : 11, on ? '#ffd860' : '#fff'); }
      if (((t * 2) | 0) % 2) txt(g, 'Tap again or press ATTACK to fight', SW / 2, 474, 12, '#7aff9a', 'center', 800);
    }
    /* ---------- title ---------- */
    var TT = null;
    G.title = function (g, t) {
      if (!TT) TT = K.layer(SW, SH, function (q) { var bg = q.createLinearGradient(0, 0, 0, SH); bg.addColorStop(0, '#1a0604'); bg.addColorStop(0.55, '#5a1a08'); bg.addColorStop(1, '#ff8a2a'); q.fillStyle = bg; q.fillRect(0, 0, SW, SH);
        for (var i = 0; i < 14; i++) { q.fillStyle = 'rgba(255,200,90,' + (0.05 + (i % 3) * 0.04) + ')'; poly(q, [SW / 2, 260, SW / 2 + Math.cos(i * 0.45) * 400, 260 + Math.sin(i * 0.45) * 400, SW / 2 + Math.cos(i * 0.45 + 0.2) * 400, 260 + Math.sin(i * 0.45 + 0.2) * 400], q.fillStyle, 0); }
        otxt(q, '\u5c11\u5e74\u5bfe\u6c7a', SW / 2, 64, 34, '#ffd860'); otxt(q, 'SH\u014cNEN', SW / 2, 112, 46, '#fff', 'center', '#ff5a1a'); otxt(q, 'SHOWDOWN', SW / 2, 160, 44, '#ff9a3a'); });
      K.blit(g, TT, 0, 0);
      var a = CH[ORDER[((t / 2.2) | 0) % 6]], b = CH[ORDER[(((t / 2.2) | 0) + 3) % 6]];
      drawFighter(g, { c: a, pose: POSE.p, face: 1, flash: 0, x: 100, y: 410, st: 'atk' }, t, 1.6); drawFighter(g, { c: b, pose: POSE.block, face: -1, flash: 0, x: 262, y: 410, st: 'idle' }, t, 1.6);
      txt(g, '6 FIGHTERS \u00b7 5-MATCH ARCADE LADDER', SW / 2, 196, 12, '#fff'); txt(g, 'Two buttons \u00b7 auto-block \u00b7 supers', SW / 2, 216, 11, '#ffe0c0', 'center', 700);
    };
    G.dispose = function () { bgL = {}; TT = null; };
    G.dbg = function (o) { o = o || {}; if (phase === 'select') { if (o.sel != null) sel = o.sel; confirmSel(); phase = 'pre'; } if (o.lives) { P.max = P.hp = 9999; } if (o.foeHp != null) E.hp = o.foeHp; if (o.meter) P.meter = 100; return { phase: phase, p: P && P.hp, e: E && E.hp, foe: E && E.id, me: P && P.id, wins: wins, rnd: rnd }; };
    G.phase = function () { return phase; }; G._pe = function () { return [P, E]; };
    /* v6566-handheld: one still figure for the menu cards / LCD (no loop) */
    G.figure = function (q, id, x, y, sc, pose) { var c = CH[id]; if (!c) return; drawFighter(q, { c: c, pose: POSE[pose || 'win'] || POSE.idle, face: 1, flash: 0, x: x, y: y, st: 'idle' }, 0, sc || 1); };
    G.wins = function () { return wins ? wins.slice() : [0, 0]; };
    G._in = function () { return { buf: buf, bufT: bufT, spHold: spHold, jumpQ: jumpQ, blocks: G._blocks | 0, freeze: freeze }; };
    G.resetCtrl = function () { buf = null; bufT = 0; spHold = -1; jumpQ = 0; freeze = 0; G.noHS = false; if (G._rawStep) G.step = G._rawStep; };
    return G;
  };
  } catch (eTop) { try { console.warn('S2ARC fight init', eTop); } catch (e2) {} }
})();
