/* v6.5.64 FFF_S2ARC cabinet shell (v6564-arcade, Erik t447).
 * A real upright cabinet around every Game Center game: marquee, bezel, CRT screen, control panel (the touch controls),
 * attract loop (title / high scores / how to play), INSERT COIN -> CREDIT -> PRESS START, stage intro + stage clear tally,
 * CONTINUE? countdown (¥1, score resets, stage kept), GAME OVER, initials entry, per-cabinet top-10 board (seeded rivals).
 * One overlay; its rAF runs only while a cabinet is open. Games register in FFF_S2ARC.GAMES (s2arc_<game>.js). */
(function () {
  try {
  var root = typeof window !== 'undefined' ? window : this;
  var A = root.FFF_S2ARC = root.FFF_S2ARC || { v: 1 };
  var INK = '#1a1220';
  function ev(k) { try { if (root.FFF_UI && root.FFF_UI.ev) root.FFF_UI.ev(k); } catch (e) {} }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function rnd(a, b) { return a + Math.random() * (b - a); }
  function tone() { if (A.tone) A.tone.apply(null, arguments); }
  function drum() { if (A.drum) A.drum.apply(null, arguments); }
  function now() { return A.now ? A.now() : performance.now() / 1000; }
  function rr(g, x, y, w, h, r, f, lw, sc) { g.beginPath(); if (g.roundRect) g.roundRect(x, y, w, h, r); else g.rect(x, y, w, h); if (f) { g.fillStyle = f; g.fill(); } if (lw) { g.lineWidth = lw; g.strokeStyle = sc || INK; g.stroke(); } }
  function txt(g, s, x, y, px, col, al, wt) { g.font = (wt || 900) + ' ' + px + 'px system-ui,"Noto Sans CJK JP",sans-serif'; g.textAlign = al || 'center'; g.textBaseline = 'middle'; g.fillStyle = col; g.fillText(s, x, y); }
  function otxt(g, s, x, y, px, col, al, oc) { g.font = '900 ' + px + 'px system-ui,"Noto Sans CJK JP",sans-serif'; g.textAlign = al || 'center'; g.textBaseline = 'middle'; g.lineJoin = 'round'; g.lineWidth = Math.max(3, px * 0.22); g.strokeStyle = oc || INK; g.strokeText(s, x, y); g.fillStyle = col; g.fillText(s, x, y); }
  function mono(g, s, x, y, px, col, al) { g.font = '900 ' + px + 'px ui-monospace,"DejaVu Sans Mono",monospace'; g.textAlign = al || 'left'; g.textBaseline = 'middle'; g.fillStyle = col; g.fillText(s, x, y); }
  var GLOW = {};
  function glow(col, r) { var k = col + r; if (GLOW[k]) return GLOW[k]; var c = document.createElement('canvas'); c.width = c.height = r * 2; var g = c.getContext('2d'), rg = g.createRadialGradient(r, r, 0, r, r, r); rg.addColorStop(0, 'rgba(' + col + ',.9)'); rg.addColorStop(0.35, 'rgba(' + col + ',.35)'); rg.addColorStop(1, 'rgba(' + col + ',0)'); g.fillStyle = rg; g.fillRect(0, 0, r * 2, r * 2); return (GLOW[k] = c); }
  function hexRgb(h) { var n = parseInt(h.slice(1), 16); return (n >> 16) + ',' + ((n >> 8) & 255) + ',' + (n & 255); }
  function pad(n, w) { var s = String(Math.max(0, n | 0)); while (s.length < w) s = '0' + s; return s; }
  /* shared kit for games */
  var K = A.K = { INK: INK, clamp: clamp, rnd: rnd, tone: tone, drum: drum, now: now, rr: rr, txt: txt, otxt: otxt, mono: mono, glow: glow, hexRgb: hexRgb, pad: pad, SW: 362, SH: 500 };
  K.ell = function (g, x, y, rx, ry, f, lw) { g.beginPath(); g.ellipse(x, y, Math.max(0.1, rx), Math.max(0.1, ry), 0, 0, 7); if (f) { g.fillStyle = f; g.fill(); } if (lw) { g.lineWidth = lw; g.strokeStyle = INK; g.stroke(); } };
  K.poly = function (g, pts, f, lw) { g.beginPath(); g.moveTo(pts[0], pts[1]); for (var i = 2; i < pts.length; i += 2) g.lineTo(pts[i], pts[i + 1]); g.closePath(); if (f) { g.fillStyle = f; g.fill(); } if (lw) { g.lineWidth = lw; g.strokeStyle = INK; g.stroke(); } };
  /* Never size cabinet / layer canvases off devicePixelRatio. At dpr 3 the old
     Math.min(2, dpr) path rasterized the 362x500 screen at 724x1000 and missed
     the 55 fps gate at 4x throttle (23-35 fps, CPU pegged). Design 1x is the
     same path that already cleared 55 fps at dpr 1; phones are dpr 3, so this
     is the release raster size. */
  K.layer = function (w, h, fn) { var c = document.createElement('canvas'); c.width = Math.ceil(w); c.height = Math.ceil(h); var g = c.getContext('2d'); fn(g); c.lw = w; c.lh = h; return c; };
  K.blit = function (g, c, x, y) { g.drawImage(c, x, y, c.lw, c.lh); };

  /* ---------------- cabinets ---------------- */
  var CABS = A.CABS = A.CABS || {};
  A.CAB_ORDER = ['gun', 'fighter', 'street', 'shooter', 'ember'];
  var GAMES = A.GAMES = A.GAMES || {};
  function tierOf(id, sc) { var C = CABS[id]; if (!C) return 0; var T = C.tiers; return sc >= T[2] ? 3 : sc >= T[1] ? 2 : sc >= T[0] ? 1 : 0; }
  A.tierOf = tierOf;
  /* tokens from a best score: the old once-per-medal payout (1/2/3 = 1, 3, 6 cumulative) is the floor,
     then +1 for every 20% of gold beyond gold, up to +4 (10 a cabinet from best scores). */
  function tokOf(id, sc) { var C = CABS[id]; if (!C || !sc) return 0; var T = C.tiers, t = tierOf(id, sc), b = [0, 1, 3, 6][t]; if (t === 3) b += Math.min(4, Math.floor((sc - T[2]) / (T[2] * 0.2))); return b; }
  A.tokOf = tokOf; A.TOK_BEST_MAX = 10; A.TOK_REPEAT_MAX = 5;
  /* seeded top-10: [initials, share of gold] */
  function seeds(id) { var C = CABS[id]; if (!C) return []; var G0 = C.tiers[2]; return (C.seed || []).map(function (q) { return { n: q[0], s: Math.round(G0 * q[1] / 10) * 10, seed: 1 }; }); }
  function board(id, mine) { var L = seeds(id).concat((mine || []).map(function (m) { return { n: m.n, s: m.s | 0, me: 1, k: m.k }; })); L.sort(function (a, b) { return b.s - a.s || (a.me ? 1 : -1); }); return L.slice(0, 10); }
  A.board = board; A.seeds = seeds;

  /* ---------------- overlay + shell ---------------- */
  var CSS = '#j6arc{position:fixed;inset:0;z-index:9200;background:#07050c;touch-action:none;user-select:none;-webkit-user-select:none;font-family:system-ui,sans-serif}'
    + '#j6arc canvas{position:absolute;left:0;top:0;width:100%;height:100%}'
    + '#j6arc .ab{position:absolute;border:3px solid #1a1220;border-radius:14px;font:900 15px system-ui;color:#1a1220;background:#ffd860;box-shadow:0 4px 0 #1a1220;padding:8px 14px;cursor:pointer}'
    + '#j6arc .ab:active{transform:translateY(2px);box-shadow:0 2px 0 #1a1220}'
    + '#j6arc .ab.x{right:8px;top:8px;background:#f2e6ff;font-size:12px;padding:5px 9px;z-index:4}';
  function css() { if (document.getElementById('j6cab-css')) return; var s = document.createElement('style'); s.id = 'j6cab-css'; s.textContent = CSS; (document.head || document.documentElement).appendChild(s); }
  /* The Game Center room leaves large canvases in the tree (c2bake, j6Room_gc,
     nqRoom, c2amb, the 1280x900 wimap). W.paused already stops the world loop to a
     100 ms keepalive, but those layers still composite under the opaque overlay.
     At dpr 3 / 4x throttle that alone dropped every cabinet below 55 fps; hiding
     them for the play held gun/fighter/street/shooter at 58-60 fps. Ember still
     needed its own tile bake (in s2arc_ember.js). Restored on close. */
  function worldFreeze(on) {
    var skip = document.getElementById('j6arc');
    if (on) {
      var hid = [];
      function hide(e) {
        if (!e || e === skip || (skip && skip.contains(e))) return;
        hid.push([e, e.style.visibility]);
        e.style.visibility = 'hidden';
      }
      ['world', 'wv', 'wimap', 'wmap', 'wsky', 'wrain', 'wisp'].forEach(function (id) { hide(document.getElementById(id)); });
      [].forEach.call(document.querySelectorAll('canvas'), hide);
      A._worldHid = hid;
    } else if (A._worldHid) {
      A._worldHid.forEach(function (p) { try { p[0].style.visibility = p[1]; } catch (eH) {} });
      A._worldHid = null;
    }
  }
  function openOv() { css(); if (A.closeOv) A.closeOv(); var el = document.createElement('div'); el.id = 'j6arc'; (document.body || document.documentElement).appendChild(el); try { if (root.W) W.paused = true; } catch (e) {} try { worldFreeze(true); } catch (eF) {} A._cabEl = el; return el; }
  function closeCab() { try { worldFreeze(false); } catch (eF) {} var el = A._cabEl; if (el && el.parentNode) el.parentNode.removeChild(el); A._cabEl = null; try { if (A.closeOv) A.closeOv(); else if (root.W) W.paused = false; } catch (e) {} try { if (root.W) W.paused = false; } catch (e2) {} }
  function canvasIn(el) { var c = document.createElement('canvas'), d = 1, w = el.clientWidth || innerWidth, h = el.clientHeight || innerHeight; c.width = Math.round(w * d); c.height = Math.round(h * d); el.appendChild(c); var g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.setTransform(d, 0, 0, d, 0, 0); return { c: c, g: g, w: w, h: h, d: d }; }
  function btnEl(el, cls, label, fn, st) { var b = document.createElement('button'); b.className = 'ab ' + (cls || ''); b.innerHTML = label; if (st) b.style.cssText += st; b.addEventListener('click', function (e) { e.stopPropagation(); try { fn(); } catch (er) { ev('world:s2arc:err:btn:' + (er && er.message)); } }); el.appendChild(b); return b; }

  var SX = 14, SY = 92, SW = 362, SH = 500, PY = 604; /* screen rect + control panel top (design units, 390x844) */
  A.SCR = [SX, SY, SW, SH, PY];
  /* the cabinet body, painted once per open */
  function paintCab(p, C, Hd) {
    var col = C.col, rgb = hexRgb(col);
    p.fillStyle = '#07050c'; p.fillRect(-60, 0, 510, Hd);
    /* side panels with the game's side art stripe */
    var sg = p.createLinearGradient(0, 0, 390, 0); sg.addColorStop(0, '#0e0a18'); sg.addColorStop(0.03, C.body || '#1c1430'); sg.addColorStop(0.97, C.body || '#1c1430'); sg.addColorStop(1, '#0e0a18');
    rr(p, 0, 0, 390, Hd, 0, sg, 0);
    p.fillStyle = col; p.globalAlpha = 0.85; p.fillRect(0, 0, 5, Hd); p.fillRect(385, 0, 5, Hd); p.globalAlpha = 1;
    /* marquee: lit box with the logo */
    rr(p, 8, 6, 374, 78, 10, '#0a0612', 4);
    var mg = p.createLinearGradient(0, 10, 0, 80); mg.addColorStop(0, C.mq ? C.mq[0] : '#2a0e3a'); mg.addColorStop(1, C.mq ? C.mq[1] : '#0e0620'); rr(p, 13, 11, 364, 68, 7, mg, 0);
    p.drawImage(glow(rgb, 140), 195 - 140, 44 - 140);
    if (C.mqArt) { p.save(); rr(p, 13, 11, 364, 68, 7, null, 0); p.clip(); C.mqArt(p, 13, 11, 364, 68); p.restore(); }
    otxt(p, C.n.toUpperCase(), C.mqPx ? 186 : 195, 38, C.mqPx || (C.n.length > 14 ? 24 : 28), '#fff', 'center', col); txt(p, C.jp, 195, 66, 12, col);
    p.fillStyle = 'rgba(255,255,255,.12)'; p.fillRect(16, 14, 358, 8);
    /* bezel */
    rr(p, 6, 86, 378, 514, 16, '#0c0912', 4);
    var bz = p.createLinearGradient(0, 86, 0, 600); bz.addColorStop(0, '#2a2236'); bz.addColorStop(1, '#141020'); rr(p, 9, 88, 372, 510, 14, bz, 0);
    rr(p, SX - 3, SY - 3, SW + 6, SH + 6, 10, '#000', 3, '#000');
    txt(p, '1 PLAYER', 30, 597, 7, 'rgba(255,255,255,.35)', 'left'); txt(p, C.jp + ' \u00b7 NEON GAME CENTER', 360, 597, 7, 'rgba(255,255,255,.35)', 'right');
    /* control panel: a sloped deck with a coin door */
    var cp = p.createLinearGradient(0, PY, 0, Hd); cp.addColorStop(0, C.deck ? C.deck[0] : '#3a2a4e'); cp.addColorStop(1, C.deck ? C.deck[1] : '#1a1228');
    p.beginPath(); p.moveTo(2, PY + 12); p.lineTo(388, PY + 12); p.lineTo(390, Hd); p.lineTo(0, Hd); p.closePath(); p.fillStyle = cp; p.fill(); p.lineWidth = 4; p.strokeStyle = INK; p.stroke();
    p.fillStyle = 'rgba(255,255,255,.14)'; p.fillRect(4, PY + 14, 382, 4);
    p.fillStyle = col; p.globalAlpha = 0.55; p.fillRect(4, PY + 18, 382, 3); p.globalAlpha = 1;
    /* coin door */
    rr(p, 156, Hd - 44, 78, 38, 6, '#141018', 3); rr(p, 164, Hd - 38, 28, 26, 4, '#2a2030', 2); p.fillStyle = '#ff3040'; p.fillRect(176, Hd - 34, 4, 18);
    txt(p, '\u00a51', 213, Hd - 31, 11, '#ffd860'); txt(p, 'COIN', 213, Hd - 18, 8, '#ffd860');
    if (C.panelArt) C.panelArt(p, PY, Hd);
  }
  /* CRT overlay: scanlines + vignette (one blit a frame) */
  var CRT = null;
  function crt() { if (CRT) return CRT; CRT = K.layer(SW, SH, function (g) { g.fillStyle = 'rgba(0,0,0,.16)'; for (var y = 0; y < SH; y += 3) g.fillRect(0, y, SW, 1);
    var vg = g.createRadialGradient(SW / 2, SH / 2, SH * 0.35, SW / 2, SH / 2, SH * 0.72); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,.42)'); g.fillStyle = vg; g.fillRect(0, 0, SW, SH);
    g.fillStyle = 'rgba(255,255,255,.05)'; g.beginPath(); g.ellipse(SW * 0.3, SH * 0.12, SW * 0.32, SH * 0.06, -0.2, 0, 7); g.fill(); }); return CRT; }

  var LET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ.&!'.split('');
  var CUR = null;
  /* cabPlay(id, opts): opts { onEnd(res)->{best,tokens,note,medal}, canAgain(), onClose(res, again), canPay(), payCont(), hs: [{n,s}], ini } */
  function cabPlay(id, opts) {
    opts = opts || {}; var C = CABS[id], mk = GAMES[id]; if (!C || !mk) return false;
    try { if (A.stopKara) A.stopKara(); } catch (e0) {} if (CUR) CUR.kill();
    var el = openOv(), cv = canvasIn(el), g = cv.g, W0 = cv.w, H0 = cv.h, s = Math.min(W0 / 390, H0 / 844), ox = (W0 - 390 * s) / 2, Hd = H0 / s;
    try { if (root.AUDIO && root.AUDIO.music) root.AUDIO.music(null); } catch (e1) {}
    try { var ac = A.actx && A.actx(); if (ac && ac.state !== 'running' && ac.resume) ac.resume(); } catch (e2) {}
    var G = mk(K, C), st = 'coin', stT = 0, t = 0, last = performance.now(), done = false, myId = Math.random();
    var credits = [], runScore = 0, ini = (opts.ini || 'RYO').slice(0, 3).split(''), slot = 0, contN = 9, contT = 0, info = null, res = null, mine = (opts.hs || []).slice(), fin = null, guard = 0;
    while (ini.length < 3) ini.push('A');
    var plate = document.createElement('canvas'); plate.width = cv.c.width; plate.height = cv.c.height; var p = plate.getContext('2d'); p.setTransform(cv.d * s, 0, 0, cv.d * s, ox * cv.d, 0);
    paintCab(p, C, Hd);
    /* Fixed 1x game buffer (design SW x SH). Games always paint here; one nearest-neighbor blit goes to the display each frame. */
    var scr = document.createElement('canvas'); scr.width = SW; scr.height = SH; var sg = scr.getContext('2d');
    G.in = G.in || {}; var PN = G.panel || { btns: [] };
    ev('world:s2arc:cab:open:' + id);
    var stopB = btnEl(el, 'x', 'Leave', function () { kill(true); });
    function go(k) { st = k; stT = 0; ev('world:s2arc:cab:st:' + id + ':' + k); }
    /* ---- input: multi-touch panel (stick + buttons) + screen taps ---- */
    var ptr = {};
    function des(e) { var r = cv.c.getBoundingClientRect(); return [(e.clientX - r.left - ox) / s, (e.clientY - r.top) / s]; }
    function hitBtn(x, y) { var B = PN.btns || []; for (var i = 0; i < B.length; i++) { var b = B[i]; if (b.hide && b.hide()) continue; var dx = x - b.x, dy = y - b.y; if (dx * dx + dy * dy <= (b.r + 10) * (b.r + 10)) return b; } return null; }
    function stickSet(x, y) { var S = PN.stick, dx = (x - S.x) / S.r, dy = (y - S.y) / S.r, m = Math.sqrt(dx * dx + dy * dy); if (m > 1) { dx /= m; dy /= m; } var I = G.in, ol = I.l, or2 = I.r, ou = I.u, od = I.d;
      if (S.dpad) { I.sx = dx; I.sy = 0; I.l = dx < -0.2; I.r = dx > 0.2; I.u = I.d = false; } /* v6566-shonen: left / right D-pad */
      else { I.sx = dx; I.sy = dy; I.l = dx < -0.38; I.r = dx > 0.38; I.u = dy < -0.45; I.d = dy > 0.45; }
      if (G.dir && st === 'play') { if (I.l && !ol) G.dir('l'); if (I.r && !or2) G.dir('r'); if (I.u && !ou) G.dir('u'); if (I.d && !od) G.dir('d'); } }
    function stickOff() { var I = G.in; I.sx = I.sy = 0; I.l = I.r = I.u = I.d = false; }
    function btnDown(b) { G.in[b.k] = true; b.dn = 1; if (st === 'play' && G.press) G.press(b.k); }
    function btnUp(b) { G.in[b.k] = false; b.dn = 0; if (st === 'play' && G.release) G.release(b.k); }
    function onDown(e) { if (done) return; e.preventDefault(); var q = des(e), x = q[0], y = q[1];
      if (st !== 'play') { metaTap(x, y); return; }
      if (guard > 0) return;
      if (y >= PY) { var S = PN.stick; if (S && Math.abs(x - S.x) < S.r * 1.6 && Math.abs(y - S.y) < S.r * 1.6) { ptr[e.pointerId] = { k: 'stick', x0: x, y0: y }; stickSet(x, y); return; }
        var b = hitBtn(x, y); if (b) { ptr[e.pointerId] = { k: 'btn', b: b }; btnDown(b); return; } if (G.swipeUp) ptr[e.pointerId] = { k: 'pan', x0: x, y0: y }; if (G.off) G.off(); return; }
      if (x >= SX && x <= SX + SW && y >= SY && y <= SY + SH) { if (G.tap) { ptr[e.pointerId] = { k: 'scr' }; G.tap(x - SX, y - SY, e.pointerId); } } else if (G.off) G.off(); }
    function onMove(e) { var P = ptr[e.pointerId]; if (!P || done) return; var q = des(e);
      /* v6566-shonen: games with G.swipeUp jump on an upward swipe that starts on the D-pad or on bare deck */
      if ((P.k === 'stick' || P.k === 'pan') && G.swipeUp && !P.up && st === 'play' && P.y0 - q[1] > 32 && P.y0 - q[1] > Math.abs(q[0] - P.x0) * 0.8) { P.up = 1; G.swipeUp(Math.abs(q[0] - P.x0) > 24 ? q[0] - P.x0 : 0); }
      if (P.k === 'stick') stickSet(q[0], q[1]); else if (P.k === 'scr' && G.drag) G.drag(q[0] - SX, q[1] - SY, e.pointerId);
      else if (P.k === 'btn' && P.b.slide) { var b = hitBtn(q[0], q[1]); if (b && b !== P.b) { btnUp(P.b); P.b = b; btnDown(b); } } }
    function onUp(e) { var P = ptr[e.pointerId]; if (!P) return; delete ptr[e.pointerId]; if (P.k === 'pan') return; if (P.k === 'stick') stickOff(); else if (P.k === 'btn') btnUp(P.b); else if (P.k === 'scr' && G.lift) G.lift(e.pointerId); }
    cv.c.addEventListener('pointerdown', onDown); cv.c.addEventListener('pointermove', onMove); cv.c.addEventListener('pointerup', onUp); cv.c.addEventListener('pointercancel', onUp);
    var KEYS = { ArrowLeft: 'l', ArrowRight: 'r', ArrowUp: 'u', ArrowDown: 'd', a: 'l', d: 'r', w: 'u', s: 'd' }, KB = ['z', 'x', 'c', 'v', 'b'];
    function keyEv(e, dn) { if (done) return; var k = e.key; if (k === 'Escape' && dn) { kill(true); return; }
      if (st !== 'play') { if (dn && (k === 'Enter' || k === ' ')) metaTap(195, 420); return; }
      if (KEYS[k] && PN.stick) { e.preventDefault(); var I = G.in, was = I[KEYS[k]]; I[KEYS[k]] = dn; I.sx = (I.r ? 1 : 0) - (I.l ? 1 : 0); I.sy = (I.d ? 1 : 0) - (I.u ? 1 : 0); if (dn && !was && G.dir) G.dir(KEYS[k]); return; }
      var bi = KB.indexOf(k === ' ' ? 'z' : k); var B = PN.btns || []; if (bi >= 0 && B[bi]) { e.preventDefault(); if (dn && !B[bi].dn) btnDown(B[bi]); else if (!dn && B[bi].dn) btnUp(B[bi]); } }
    function kd(e) { keyEv(e, true); } function ku(e) { keyEv(e, false); }
    document.addEventListener('keydown', kd); document.addEventListener('keyup', ku);
    /* ---- meta screens (attract / continue / initials / board) ---- */
    function startGame() { if (st !== 'attract') return; credits = []; runScore = 0; G.score = 0; var r0 = G.start(); tone(988, now(), 0.12, 'square', 0.07); tone(1318, now() + 0.1, 0.18, 'square', 0.07); go(r0 === 'select' ? 'play' : 'intro'); }
    function qualifies(sc) { if (sc <= 0) return false; var B = board(id, mine); return B.length < 10 || sc > B[B.length - 1].s; }
    function finishRun(score, cleared) {
      fin = { score: score, cleared: cleared };
      if (qualifies(score)) { slot = 0; go('name'); } else endRun();
    }
    function endRun() {
      var sc = fin.score | 0; res = { id: id, score: sc, tier: tierOf(id, sc), quit: false, ini: ini.join(''), stage: (G.stage | 0) + 1, cleared: !!fin.cleared, t: t };
      if (qualifies(sc)) { mine.push({ n: res.ini, s: sc, k: Date.now() }); mine.sort(function (a, b) { return b.s - a.s; }); mine = mine.slice(0, 10); res.entry = mine[0] && mine.filter(function (m) { return m.s === sc; })[0]; }
      A.lastCab = res; ev('world:s2arc:cab:end:' + id + ':' + sc + ':' + res.tier);
      info = (opts.onEnd ? opts.onEnd(res) : null) || {}; go('board'); boardBtns();
    }
    function boardBtns() {
      var row = document.createElement('div'); row.className = 'cabres'; row.style.cssText = 'position:absolute;left:' + (ox + 20 * s) + 'px;width:' + (350 * s) + 'px;top:' + ((PY + 34) * s) + 'px;display:flex;gap:12px;z-index:3';
      function bb(lab, fn, hot) { var b = document.createElement('button'); b.textContent = lab; b.style.cssText = 'flex:1;padding:14px 8px;border-radius:14px;border:3px solid #000;box-shadow:0 4px 0 #000;font:900 16px system-ui;background:' + (hot ? C.col : '#2a1a3a') + ';color:' + (hot ? '#140a20' : '#fff'); b.addEventListener('click', function (e) { e.stopPropagation(); fn(); }); row.appendChild(b); }
      bb('Done', function () { close(false); });
      if (!opts.canAgain || opts.canAgain()) bb('Again \u00b7 \u00a51', function () { close(true); }, true);
      el.appendChild(row);
    }
    function metaTap(x, y) {
      if (st === 'attract') { if (stT > 0.5) startGame(); return; }
      if (st === 'cont') { var lx = x - SX, ly = y - SY;
        if (ly > 300 && ly < 360 && lx > 30 && lx < 170) { contYes(); return; }
        if (ly > 300 && ly < 360 && lx > 192 && lx < 332) { contNo(); return; }
        contT += 0.5; return; }
      if (st === 'name') { var nx = x - SX, ny = y - SY; if (nx < 0 || ny < 0 || nx > SW || ny > SH) return;
        var gx = Math.floor((nx - 21) / 40), gy = Math.floor((ny - 210) / 46); if (gy < 0 || gy > 3 || gx < 0 || gx > 7) return; var k = gy * 8 + gx;
        if (k < LET.length) { ini[Math.min(2, slot)] = LET[k]; slot = Math.min(3, slot + 1); tone(880, now(), 0.06, 'square', 0.05); }
        else if (k === 29) { slot = Math.max(0, slot - 1); tone(440, now(), 0.06, 'square', 0.04); }
        else { tone(1318, now(), 0.15, 'square', 0.06); endRun(); }
        return; }
    }
    function contYes() { if (opts.canPay && !opts.canPay()) { tone(110, now(), 0.12, 'square', 0.04); return; } if (opts.payCont) opts.payCont(); credits.push(G.score | 0); runScore = Math.max(runScore, G.score | 0); G.score = 0; G.cont(); tone(1046, now(), 0.15, 'square', 0.07); ev('world:s2arc:cab:cont:' + id); go('intro'); }
    function contNo() { credits.push(G.score | 0); runScore = Math.max(runScore, G.score | 0); go('over'); }
    function close(again) { kill(false); if (opts.onClose) opts.onClose(res || { id: id, score: 0, tier: 0, quit: true }, again); }
    function kill(quit) {
      if (done) return; done = true; if (CUR && CUR.id === myId) { cancelAnimationFrame(CUR.raf); if (A._cab === CUR) A._cab = null; CUR = null; }
      document.removeEventListener('keydown', kd); document.removeEventListener('keyup', ku);
      cv.c.removeEventListener('pointerdown', onDown); cv.c.removeEventListener('pointermove', onMove); cv.c.removeEventListener('pointerup', onUp); cv.c.removeEventListener('pointercancel', onUp);
      try { if (G.dispose) G.dispose(); } catch (eD) {}
      plate.width = plate.height = 0; scr.width = scr.height = 0; cv.c.width = cv.c.height = 0;
      if (quit) { ev('world:s2arc:cab:end:' + id + ':0:0:quit'); closeCab(); if (!res && opts.onClose) opts.onClose({ id: id, score: 0, tier: 0, quit: true }, false); return; }
      closeCab();
    }
    /* ---- draw helpers for meta screens (screen-local) ---- */
    function drawBoard(q, hl) {
      q.fillStyle = 'rgba(6,4,14,.92)'; q.fillRect(0, 0, SW, SH);
      otxt(q, 'HIGH SCORES', SW / 2, 34, 24, '#fff', 'center', C.col); txt(q, C.n.toUpperCase(), SW / 2, 58, 11, C.col);
      var B = board(id, mine), T = C.tiers, rgb = ['#9a90b0', '#e0a060', '#d8e0f0', '#ffd860'];
      for (var i = 0; i < 10; i++) { var e = B[i]; if (!e) break; var y = 92 + i * 27, me = e.me && hl && e.s === hl.s && e.n === hl.n, blink = me && ((t * 4) | 0) % 2;
        if (me) { rr(q, 14, y - 12, SW - 28, 24, 6, 'rgba(' + hexRgb(C.col) + ',.28)', 0); }
        var ti = tierOf(id, e.s), cc = blink ? '#fff' : e.me ? '#7aff9a' : i === 0 ? '#ffd860' : '#e8e0f8';
        mono(q, (i + 1 < 10 ? ' ' : '') + (i + 1) + (['ST', 'ND', 'RD'][i] || 'TH'), 24, y, 14, cc); mono(q, e.n, 98, y, 16, cc); mono(q, pad(e.s, 7), 236, y, 16, cc, 'right');
        if (ti) { K.ell(q, 262, y, 7, 7, rgb[ti], 1.5); } if (e.me) txt(q, 'YOU', 312, y, 10, '#7aff9a'); }
      var y0 = 372; rr(q, 14, y0 - 14, SW - 28, 64, 10, 'rgba(255,255,255,.06)', 2, 'rgba(255,255,255,.2)');
      [['BRONZE', T[0], 1], ['SILVER', T[1], 2], ['GOLD', T[2], 3]].forEach(function (m, k) { var x = 66 + k * 116; K.ell(q, x - 34, y0 + 4, 8, 8, rgb[m[2]], 1.5); txt(q, m[0], x + 4, y0 - 2, 10, rgb[m[2]]); mono(q, pad(m[1], 6), x + 4, y0 + 14, 13, '#fff', 'center'); });
      txt(q, 'Medals and tokens come from your best score', SW / 2, y0 + 38, 10, 'rgba(255,255,255,.6)', 'center', 700);
    }
    function drawMeta(q) {
      var bl = ((t * 2.2) | 0) % 2;
      if (st === 'coin' || st === 'attract') {
        var ph = st === 'coin' ? 0 : ((stT / 5) | 0) % 3;
        if (ph === 1) drawBoard(q, null);
        else if (ph === 2) { q.fillStyle = 'rgba(6,4,14,.9)'; q.fillRect(0, 0, SW, SH); otxt(q, 'HOW TO PLAY', SW / 2, 40, 22, '#fff', 'center', C.col);
          (G.how || []).forEach(function (l, i) { txt(q, l, SW / 2, 86 + i * 28, 13, i % 2 ? '#e8e0f8' : '#fff', 'center', 700); });
          if (G.howArt) G.howArt(q, t); }
        else G.title(q, t);
        rr(q, 0, SH - 46, SW, 46, 0, 'rgba(0,0,0,.55)', 0);
        if (st === 'coin') { if (bl) otxt(q, 'INSERT COIN', SW / 2, SH - 24, 20, '#ffd860'); }
        else { txt(q, 'CREDIT 1', 50, SH - 24, 12, '#fff'); if (bl) otxt(q, 'PRESS START', SW / 2 + 30, SH - 24, 20, '#7aff9a'); }
        return; }
      if (st === 'intro' && G.introDraw) { G.introDraw(q, stT); return; }
      if (st === 'intro') { q.fillStyle = 'rgba(0,0,0,' + clamp(1.2 - stT, 0, 0.7) + ')'; q.fillRect(0, 0, SW, SH); var Sg = (G.stages || [])[G.stage | 0] || {};
        rr(q, 20, 170, SW - 40, 130, 14, 'rgba(8,6,18,.85)', 3, C.col); txt(q, (G.stageWord || 'STAGE') + ' ' + ((G.stage | 0) + 1) + (G.stages ? ' / ' + G.stages.length : ''), SW / 2, 200, 15, C.col);
        otxt(q, Sg.n || '', SW / 2, 236, Sg.n && Sg.n.length > 16 ? 20 : 26, '#fff'); if (Sg.sub) txt(q, Sg.sub, SW / 2, 272, 12, '#e8e0f8', 'center', 700);
        if (stT > 1.2) otxt(q, 'GO!', SW / 2, 336, 30, '#ffd860'); return; }
      if (st === 'clear') { q.fillStyle = 'rgba(0,0,0,.45)'; q.fillRect(0, 0, SW, SH); otxt(q, (G.stageWord || 'STAGE') + ' CLEAR!', SW / 2, 150, 28, '#ffd860');
        (G._tally || []).forEach(function (b, i) { if (stT < 0.5 + i * 0.4) return; txt(q, b[0], 60, 210 + i * 30, 15, '#fff', 'left'); mono(q, '+' + b[1], SW - 60, 210 + i * 30, 16, '#7aff9a', 'right'); }); return; }
      if (st === 'cont') { q.fillStyle = 'rgba(0,0,0,.72)'; q.fillRect(0, 0, SW, SH); otxt(q, 'CONTINUE?', SW / 2, 120, 32, '#fff', 'center', C.col); otxt(q, String(contN), SW / 2, 210, 72, '#ffd860');
        var ok = !opts.canPay || opts.canPay(); rr(q, 30, 300, 140, 60, 14, ok ? C.col : '#4a4458', 3); otxt(q, 'YES \u00b7 \u00a51', 100, 330, 18, '#fff'); rr(q, 192, 300, 140, 60, 14, '#2a1a3a', 3); otxt(q, 'NO', 262, 330, 18, '#fff');
        txt(q, 'Score resets to 0. You keep the stage.', SW / 2, 392, 12, '#e8e0f8', 'center', 700); txt(q, 'Best this credit: ' + (G.score | 0), SW / 2, 414, 12, '#9a90b0', 'center', 700); return; }
      if (st === 'over' || st === 'win') { q.fillStyle = 'rgba(0,0,0,.6)'; q.fillRect(0, 0, SW, SH);
        if (st === 'win') { if (G.ending) G.ending(q, stT); otxt(q, 'ALL CLEAR!', SW / 2, 120, 34, '#ffd860'); txt(q, G.endLine || 'Thanks for playing', SW / 2, 160, 13, '#fff', 'center', 700); }
        else otxt(q, 'GAME OVER', SW / 2, 220, 36, '#ff5a6a');
        mono(q, 'SCORE ' + pad(Math.max(runScore, G.score | 0), 7), SW / 2, st === 'win' ? 420 : 280, 18, '#fff', 'center'); return; }
      if (st === 'name') { q.fillStyle = 'rgba(6,4,14,.94)'; q.fillRect(0, 0, SW, SH); otxt(q, 'NEW HIGH SCORE!', SW / 2, 40, 24, '#ffd860'); mono(q, pad(fin.score, 7), SW / 2, 78, 22, '#fff', 'center');
        txt(q, 'ENTER YOUR INITIALS', SW / 2, 108, 12, C.col);
        for (var i = 0; i < 3; i++) { var x = SW / 2 - 70 + i * 70; rr(q, x - 26, 128, 52, 60, 8, i === slot && bl ? 'rgba(' + hexRgb(C.col) + ',.4)' : 'rgba(255,255,255,.08)', 2, C.col); otxt(q, ini[i], x, 160, 34, '#fff'); }
        for (var k = 0; k < 31; k++) { var gx = k % 8, gy = (k / 8) | 0; var lab = k < LET.length ? LET[k] : k === 29 ? '\u2190' : 'END'; var w = k === 30 ? 76 : 36, x0 = 21 + gx * 40, en = k === 30 || (slot >= 3 && k === 30);
          rr(q, x0, 210 + gy * 46, w, 40, 8, k === 30 ? (slot >= 3 && bl ? '#fff' : C.col) : 'rgba(255,255,255,.1)', 2, 'rgba(255,255,255,.3)'); txt(q, lab, x0 + w / 2, 230 + gy * 46, k >= 29 ? 15 : 18, en ? INK : '#fff'); }
        txt(q, 'Tap letters, then END', SW / 2, 404, 11, 'rgba(255,255,255,.6)', 'center', 700);
        return; }
      if (st === 'board') { drawBoard(q, res && res.entry);
        var y1 = 452; rr(q, 14, y1 - 14, SW - 28, 50, 10, 'rgba(' + hexRgb(C.col) + ',.18)', 2, C.col);
        var TN = ['NO MEDAL', 'BRONZE', 'SILVER', 'GOLD'];
        txt(q, 'SCORE ' + res.score + '  \u00b7  BEST ' + (info.best != null ? info.best : res.score) + '  \u00b7  ' + TN[tierOf(id, info.best != null ? info.best : res.score)], SW / 2, y1 - 2, 12, '#fff');
        txt(q, info.tokens ? '+' + info.tokens + ' PRIZE TOKEN' + (info.tokens > 1 ? 'S' : '') + (info.note ? ' \u00b7 ' + info.note : '') : (info.note || 'No tokens this run'), SW / 2, y1 + 16, 11, info.tokens ? '#7aff9a' : '#c8c0d8', 'center', 800);
        return; }
    }
    function drawPanel(q) { var S = PN.stick, B = PN.btns || [];
      if (S && S.dpad) { /* v6566-shonen: wide two-key D-pad, the held side sinks */ var I0 = G.in, hw = S.r * 1.5, hh = S.r * 0.66;
        rr(q, S.x - hw - 6, S.y - hh - 4, (hw + 6) * 2, hh * 2 + 14, hh * 0.7, '#0a0610', 0); rr(q, S.x - hw - 6, S.y - hh - 8, (hw + 6) * 2, hh * 2 + 14, hh * 0.7, '#0c0812', 3);
        [-1, 1].forEach(function (d) { var on = d < 0 ? I0.l : I0.r, kx = S.x + d * hw * 0.5, ky = S.y - 2 + (on ? 3 : 0), kw = hw * 0.92;
          rr(q, kx - kw / 2, ky - hh + 4, kw, hh * 2 - 8, 12, on ? '#f0e0c8' : '#2a2034', 3); if (!on) rr(q, kx - kw / 2 + 6, ky - hh + 8, kw - 12, 8, 4, 'rgba(255,255,255,.12)', 0);
          K.poly(q, [kx + d * 16, ky, kx - d * 12, ky - 18, kx - d * 12, ky + 18], on ? INK : (S.c || '#e83040'), 2.5); });
        rr(q, S.x - 5, S.y - hh + 2, 10, hh * 2 - 10, 4, '#0c0812', 0); txt(q, 'swipe \u2191 jump', S.x, S.y + hh + 16, 9, 'rgba(255,255,255,.7)'); }
      else if (S) { K.ell(q, S.x, S.y, S.r + 6, S.r + 6, '#0c0812', 3); K.ell(q, S.x, S.y, S.r, S.r, '#1e1828', 0); var I = G.in, kx = S.x + (I.sx || 0) * S.r * 0.55, ky = S.y + (I.sy || 0) * S.r * 0.55;
        q.lineWidth = 9; q.strokeStyle = '#d8d0e0'; q.beginPath(); q.moveTo(S.x, S.y); q.lineTo(kx, ky - 4); q.stroke(); K.ell(q, kx, ky - 6, 17, 17, S.c || '#e83040', 3); K.ell(q, kx - 5, ky - 11, 5, 4, 'rgba(255,255,255,.5)', 0); }
      for (var i = 0; i < B.length; i++) { var b = B[i]; if (b.hide && b.hide()) continue; var dn = b.dn || (st === 'play' && G.lit && G.lit(b.k)), off = dn ? 3 : 0;
        var gl = st === 'play' && b.glow && b.glow(); /* v6566-shonen: a ready button glows; this only runs inside the open cabinet's own frame */
        if (gl) { var gr = b.r + 36; q.globalAlpha = 0.7 + 0.3 * Math.sin(t * 9); q.drawImage(glow(b.gc || '255,255,255', gr), b.x - gr, b.y - gr); q.globalAlpha = 1; /* unscaled cached halo: alpha pulse only */ q.lineWidth = 3; q.strokeStyle = 'rgba(255,255,255,' + (0.5 + 0.4 * Math.sin(t * 9)) + ')'; q.beginPath(); q.arc(b.x, b.y, b.r + 6, 0, 7); q.stroke(); }
        K.ell(q, b.x, b.y + 4, b.r, b.r * 0.92, '#0a0610', 0); K.ell(q, b.x, b.y + off, b.r, b.r * 0.92, gl ? (b.gcol || b.c) : b.c, 3);
        var rg = st === 'play' && b.ring ? b.ring() : 0; if (rg > 0) { q.lineWidth = 6; q.strokeStyle = rg >= 1 ? '#fff' : 'rgba(255,255,255,.8)'; q.beginPath(); q.arc(b.x, b.y + off, b.r + 7, -Math.PI / 2, -Math.PI / 2 + rg * Math.PI * 2); q.stroke(); }
        if (!dn) K.ell(q, b.x - b.r * 0.3, b.y - b.r * 0.35, b.r * 0.35, b.r * 0.22, 'rgba(255,255,255,.45)', 0);
        if (b.dim && b.dim()) { q.globalAlpha = 0.55; K.ell(q, b.x, b.y + off, b.r, b.r * 0.92, '#000', 0); q.globalAlpha = 1; }
        var bl = b.lf ? b.lf() : b.l; txt(q, bl, b.x, b.y + off, b.fs || (bl.length > 4 ? 10 : 13), INK); if (b.sub) txt(q, b.sub, b.x, b.y + b.r + 12, 9, 'rgba(255,255,255,.7)'); } }
    /* ---- main loop (only while open) ---- */
    function frame() {
      if (!CUR || CUR.id !== myId) return;
      var tms = performance.now(), dt = Math.min(0.05, (tms - last) / 1000); last = tms; t += dt; stT += dt; guard = Math.max(0, guard - dt);
      if (st === 'coin' && stT > 0.9) { drum('k', now(), 0.3); tone(1568, now(), 0.08, 'square', 0.05); tone(2093, now() + 0.07, 0.12, 'square', 0.05); go('attract'); }
      else if (st === 'attract' && G.attract) G.attract(dt, stT);
      else if (st === 'intro') { if (G.introStep) G.introStep(dt); if (stT > 1.6) { go('play'); guard = 0.15; } }
      else if (st === 'play') { var r = G.step(dt); if (r === 'go') go('intro'); else if (r === 'clear') { G._tally = G.bonus ? G.bonus() : []; G._tally.forEach(function (b) { G.score += b[1] | 0; }); tone(784, now(), 0.15, 'square', 0.07); tone(1046, now() + 0.15, 0.15, 'square', 0.07); tone(1568, now() + 0.3, 0.3, 'square', 0.07); go('clear'); }
        else if (r === 'win') { G._tally = G.bonus ? G.bonus() : []; G._tally.forEach(function (b) { G.score += b[1] | 0; }); runScore = Math.max(runScore, G.score | 0); [523, 659, 784, 1046, 1318].forEach(function (f, i) { tone(f, now() + i * 0.12, 0.25, 'square', 0.06); }); go('win'); }
        else if (r === 'dead') { stickOff(); contN = 9; contT = 0; tone(220, now(), 0.3, 'sawtooth', 0.08); tone(110, now() + 0.25, 0.5, 'sawtooth', 0.08); go('cont'); } }
      else if (st === 'clear') { if (stT > 1.2 + (G._tally || []).length * 0.4) { G.next(); go('intro'); } }
      else if (st === 'cont') { contT += dt; if (contT >= 1) { contT = 0; contN--; tone(440, now(), 0.06, 'square', 0.04); if (contN < 0) contNo(); } }
      else if (st === 'over') { if (stT > 1.8) { runScore = Math.max(runScore, G.score | 0); finishRun(runScore, false); } }
      else if (st === 'win') { if (stT > 4) finishRun(runScore, true); }
      /* draw: cached plate + one scaled blit of the 1x game buffer, then the live control deck */
      g.setTransform(cv.d, 0, 0, cv.d, 0, 0); g.drawImage(plate, 0, 0, W0, H0);
      sg.setTransform(1, 0, 0, 1, 0, 0); sg.fillStyle = '#000'; sg.fillRect(0, 0, SW, SH);
      if (st === 'play' || st === 'intro' || st === 'clear' || st === 'cont' || st === 'over' || st === 'win') { G.draw(sg, t); if (G.hud !== false) hud(sg); }
      drawMeta(sg); K.blit(sg, crt(), 0, 0);
      g.setTransform(cv.d * s, 0, 0, cv.d * s, (ox + SX * s) * cv.d, SY * s * cv.d);
      g.imageSmoothingEnabled = false;
      g.drawImage(scr, 0, 0, SW, SH);
      g.setTransform(cv.d * s, 0, 0, cv.d * s, ox * cv.d, 0);
      if (st !== 'board') drawPanel(g);
      if (st === 'attract' && ((t * 2) | 0) % 2) { K.ell(g, 50, Hd - 25, 14, 14, '#7aff9a', 3); txt(g, '1P', 50, Hd - 25, 10, INK); }
      CUR.raf = requestAnimationFrame(frame);
    }
    function hud(q) { rr(q, 0, 0, SW, 24, 0, 'rgba(0,0,0,.5)', 0); var B = board(id, mine);
      mono(q, '1UP', 8, 12, 11, '#ff5a6a'); mono(q, pad(G.score, 7), 40, 12, 13, '#fff'); mono(q, 'HI', 150, 12, 11, '#ffd860'); mono(q, pad(Math.max(B[0] ? B[0].s : 0, G.score | 0), 7), 170, 12, 13, '#ffd860');
      if (G.stages) mono(q, (G.stageWord ? G.stageWord.slice(0, 2) : 'ST') + ' ' + ((G.stage | 0) + 1) + '/' + G.stages.length, SW - 8, 12, 11, '#7fe8ff', 'right'); }
    CUR = { id: myId, raf: 0, G: G, kill: kill, go: go, st: function () { return st; },
      force: function (sc) { G.score = sc; runScore = sc; if (qualifies(sc)) { fin = { score: sc, cleared: false }; endRun(); } else { fin = { score: sc, cleared: false }; endRun(); } },
      start: startGame, tap: metaTap, contYes: contYes, contNo: contNo };
    A._cab = CUR; CUR.raf = requestAnimationFrame(frame);
    return true;
  }
  A.cabPlay = cabPlay;
  /* test hooks */
  A.cabForce = function (sc) { if (!CUR) return false; CUR.force(sc | 0); return true; };
  A.cabStart = function () { if (!CUR) return false; if (CUR.st() === 'coin') CUR.go('attract'); CUR.start(); return CUR.st(); };
  A.cabSt = function () { return CUR ? CUR.st() : null; };
  A.cabG = function () { return CUR ? CUR.G : null; };
  A.cabGo = function (k) { if (CUR) CUR.go(k); return !!CUR; };
  ev('world:s2arc:cab:ready');
  } catch (eTop) { try { console.warn('S2ARC cab init', eTop); } catch (e2) {} }
})();
