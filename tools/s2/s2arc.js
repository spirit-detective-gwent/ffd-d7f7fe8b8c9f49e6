/* v6.5.64 FFF_S2ARC (GGD-51, seal 3 · Jin's turf): strip minigames.
 * Karaoke Kitsune tap-along (song menu, lead pick, 3-lane tap-along, grade, one-fight song edge).
 * One overlay; its rAF runs only while the overlay is open. Audio is a tiny WebAudio synth on the game's own context. */
(function () {
  try {
  var root = typeof window !== 'undefined' ? window : this;
  var A = root.FFF_S2ARC = root.FFF_S2ARC || { v: 1 };
  var INK = '#1a1220';
  function ev(k) { try { if (root.FFF_UI && root.FFF_UI.ev) root.FFF_UI.ev(k); } catch (e) {} }
  A.ev = ev;
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

  /* ---------------- audio (shared) ---------------- */
  function actx() { try { var st = root.AUDIO && root.AUDIO.st; if (st && st.ctx) return st.ctx; } catch (e) {} return null; }
  function sfxOn() { try { var st = root.AUDIO && root.AUDIO.st; return !st || st.sfxOn !== false; } catch (e) { return true; } }
  var OUT = null;
  function out(c) { if (OUT && OUT.context === c) return OUT; OUT = c.createGain(); OUT.gain.value = 0.55; OUT.connect(c.destination); return OUT; }
  function tone(f, t, d, type, g, vib) { var c = actx(); if (!c || !sfxOn()) return; try {
    var o = c.createOscillator(), a = c.createGain(); o.type = type || 'triangle'; o.frequency.setValueAtTime(f, t);
    if (vib) { var l = c.createOscillator(), lg = c.createGain(); l.frequency.value = 5.5; lg.gain.value = f * 0.012; l.connect(lg); lg.connect(o.frequency); l.start(t + d * 0.3); l.stop(t + d + 0.05); }
    a.gain.setValueAtTime(0.0001, t); a.gain.exponentialRampToValueAtTime(g || 0.2, t + 0.015); a.gain.exponentialRampToValueAtTime(0.0001, t + d);
    o.connect(a); a.connect(out(c)); o.start(t); o.stop(t + d + 0.05); } catch (e) {} }
  var NB = null;
  function noise(c) { if (NB && NB.sampleRate === c.sampleRate) return NB; NB = c.createBuffer(1, c.sampleRate * 0.3, c.sampleRate); var d = NB.getChannelData(0); for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; return NB; }
  function drum(kind, t, g) { var c = actx(); if (!c || !sfxOn()) return; try {
    if (kind === 'k') { var o = c.createOscillator(), a = c.createGain(); o.frequency.setValueAtTime(140, t); o.frequency.exponentialRampToValueAtTime(42, t + 0.12); a.gain.setValueAtTime(g || 0.5, t); a.gain.exponentialRampToValueAtTime(0.0001, t + 0.2); o.connect(a); a.connect(out(c)); o.start(t); o.stop(t + 0.22); return; }
    var s = c.createBufferSource(), f = c.createBiquadFilter(), b = c.createGain(); s.buffer = noise(c);
    f.type = kind === 'h' ? 'highpass' : 'bandpass'; f.frequency.value = kind === 'h' ? 7000 : 1800;
    var d = kind === 'h' ? 0.05 : 0.16; b.gain.setValueAtTime(g || (kind === 'h' ? 0.12 : 0.3), t); b.gain.exponentialRampToValueAtTime(0.0001, t + d);
    s.connect(f); f.connect(b); b.connect(out(c)); s.start(t); s.stop(t + d + 0.02); } catch (e) {} }
  A.tone = tone; A.drum = drum; A.actx = actx;
  function now() { var c = actx(); return c && c.state === 'running' ? c.currentTime : performance.now() / 1000; }
  A.now = now;
  function musicOff() { try { if (root.AUDIO && root.AUDIO.music) root.AUDIO.music(null); } catch (e) {} }
  function wake() { try { var c = actx(); if (c && c.state !== 'running' && c.resume) c.resume(); } catch (e) {} }

  /* ---------------- overlay ---------------- */
  var CSS = '#j6arc{position:fixed;inset:0;z-index:9200;background:#0a0612;touch-action:none;user-select:none;-webkit-user-select:none;font-family:system-ui,sans-serif}'
    + '#j6arc canvas{position:absolute;left:0;top:0;width:100%;height:100%}'
    + '#j6arc .ab{position:absolute;border:3px solid #1a1220;border-radius:14px;font:900 15px system-ui;color:#1a1220;background:#ffd860;box-shadow:0 4px 0 #1a1220;padding:8px 14px;cursor:pointer}'
    + '#j6arc .ab:active{transform:translateY(2px);box-shadow:0 2px 0 #1a1220}'
    + '#j6arc .ab.x{right:10px;top:10px;background:#f2e6ff;font-size:13px;padding:6px 10px}'
    + '#j6arc .ab.dim{background:#6a6478;color:#d8d0e8}'
    + '#j6arc .sm{position:absolute;left:12px;right:12px;top:64px;bottom:12px;overflow-y:auto;-webkit-overflow-scrolling:touch}'
    + '#j6arc .song{display:flex;gap:10px;align-items:center;margin:0 0 10px;padding:10px;border:3px solid #1a1220;border-radius:14px;background:#f6f0ff;box-shadow:0 4px 0 #1a1220;cursor:pointer;width:100%;text-align:left;font:inherit;color:#1a1220}'
    + '#j6arc .song.on{background:#fff4c8;outline:4px solid #ff5ac8}'
    + '#j6arc .song i{flex:0 0 52px;height:52px;border-radius:10px;border:3px solid #1a1220;display:flex;align-items:center;justify-content:center;font:900 24px system-ui;font-style:normal;color:#fff}'
    + '#j6arc .song b{display:block;font:900 16px system-ui}#j6arc .song small{display:block;font:700 12px system-ui;color:#5a4a70}#j6arc .song em{display:inline-block;margin-top:3px;font:800 11px system-ui;font-style:normal;color:#9a1e8a}'
    + '#j6arc .lead{display:flex;gap:10px;margin:6px 0 12px}#j6arc .lead button{flex:1;display:flex;align-items:center;gap:8px;padding:6px;border:3px solid #1a1220;border-radius:14px;background:#e8e4f4;box-shadow:0 4px 0 #1a1220;font:900 15px system-ui;color:#1a1220;cursor:pointer}'
    + '#j6arc .lead button.on{background:#7fe8ff;outline:4px solid #ff5ac8}#j6arc .lead img{width:54px;height:54px;border-radius:10px;border:2px solid #1a1220;object-fit:cover;object-position:50% 12%;background:#2a1a3a}'
    + '#j6arc .hd{font:900 13px system-ui;color:#ffd0f0;letter-spacing:.06em;margin:4px 2px 6px}'
    + '#j6arc .go{position:relative;display:block;width:100%;margin:6px 0 0;padding:12px;font-size:18px;background:#ff5ac8;color:#fff;text-shadow:0 2px 0 #1a1220}'
    + '#j6arc .go.dim{background:#6a6478}';
  function css() { if (document.getElementById('j6arc-css')) return; var s = document.createElement('style'); s.id = 'j6arc-css'; s.textContent = CSS; (document.head || document.documentElement).appendChild(s); }
  var OV = null;
  function openOv() { css(); closeOv(); OV = document.createElement('div'); OV.id = 'j6arc'; (document.body || document.documentElement).appendChild(OV); try { if (root.W) { W.paused = true; } } catch (e) {} return OV; }
  function closeOv() { if (OV && OV.parentNode) OV.parentNode.removeChild(OV); OV = null; try { if (root.W) W.paused = false; } catch (e) {} }
  A.openOv = openOv; A.closeOv = closeOv; A.isOpen = function () { return !!OV; };
  function canvasIn(el) { var c = document.createElement('canvas'), d = Math.min(2, root.devicePixelRatio || 1), w = el.clientWidth || innerWidth, h = el.clientHeight || innerHeight; c.width = Math.round(w * d); c.height = Math.round(h * d); el.appendChild(c); var g = c.getContext('2d'); g.setTransform(d, 0, 0, d, 0, 0); return { c: c, g: g, w: w, h: h, d: d }; }
  function btn(el, cls, label, fn, st) { var b = document.createElement('button'); b.className = 'ab ' + (cls || ''); b.innerHTML = label; if (st) b.style.cssText += st; b.addEventListener('click', function (e) { e.stopPropagation(); try { fn(); } catch (er) { ev('world:s2arc:err:btn:' + (er && er.message)); } }); el.appendChild(b); return b; }
  A.btn = btn; A.canvasIn = canvasIn;
  function ptImg(who) { var i = new Image(); i.src = 'portraits/' + who + '_neutral.webp'; return i; }
  function ptHappy(who) { var i = new Image(); i.src = 'portraits/' + who + '_happy.webp'; return i; }
  var GLOW = {};
  function glowSpr(col, r) { var k = col + r; if (GLOW[k]) return GLOW[k]; var c = document.createElement('canvas'); c.width = c.height = r * 2; var g = c.getContext('2d'), rg = g.createRadialGradient(r, r, 0, r, r, r); rg.addColorStop(0, 'rgba(' + col + ',.9)'); rg.addColorStop(0.35, 'rgba(' + col + ',.35)'); rg.addColorStop(1, 'rgba(' + col + ',0)'); g.fillStyle = rg; g.fillRect(0, 0, r * 2, r * 2); return (GLOW[k] = c); }
  A.glowSpr = glowSpr;
  function rr(g, x, y, w, h, r, f, lw, sc) { g.beginPath(); if (g.roundRect) g.roundRect(x, y, w, h, r); else g.rect(x, y, w, h); if (f) { g.fillStyle = f; g.fill(); } if (lw) { g.lineWidth = lw; g.strokeStyle = sc || INK; g.stroke(); } }
  A.rr = rr;
  function txt(g, s, x, y, px, col, al, wt) { g.font = (wt || 900) + ' ' + px + 'px system-ui,"Noto Sans CJK JP",sans-serif'; g.textAlign = al || 'center'; g.textBaseline = 'middle'; g.fillStyle = col; g.fillText(s, x, y); }
  function otxt(g, s, x, y, px, col, al) { g.font = '900 ' + px + 'px system-ui,"Noto Sans CJK JP",sans-serif'; g.textAlign = al || 'center'; g.textBaseline = 'middle'; g.lineJoin = 'round'; g.lineWidth = Math.max(3, px * 0.22); g.strokeStyle = INK; g.strokeText(s, x, y); g.fillStyle = col; g.fillText(s, x, y); }
  A.txt = txt; A.otxt = otxt;

  /* ---------------- karaoke ---------------- */
  /* melody strings: one char per half beat; 1-8 = scale degree, '-' = rest. 16 chars per lyric line (two 4/4 bars). */
  var MAJ = [0, 2, 4, 5, 7, 9, 11, 12], MIN = [0, 2, 3, 5, 7, 8, 10, 12];
  var SONGS = [
    { id: 'anthem', edge: 'anthem', n: 'Kitsune Anthem', jp: '\u72d0\u706b\u30a2\u30f3\u30bb\u30e0', genre: 'ANTHEM', col: '#ff5ac8', ic: '\u2605', bpm: 126, root: 60, sc: MAJ, beat: 'four',
      sky: ['#2a1a6a', '#e0508a'], scene: 'city',
      lines: [['Light the lamps on Chuo-dori', '1-3-5-5-6-5-3---'], ['Nine tails burning through the rain', '5-6-8-8-6-5-3-5-'], ['Every sign is calling our name', '6-6-5-3-5-6-8---'],
        ['Fox fire, never fade away', '8-8-6-5-6-5-3---'], ['Hands up, the whole street sings', '1-3-5-3-5-6-5---'], ['Kitsune! We run the night!', '5-6-8---8-6-8---']] },
    { id: 'ballad', edge: 'ballad', n: 'Rain on Chuo-dori', jp: '\u4e2d\u592e\u901a\u308a\u306e\u96e8', genre: 'BALLAD', col: '#5ad8ff', ic: '\u2614', bpm: 80, root: 57, sc: MIN, beat: 'soft',
      sky: ['#0e1a3a', '#5a6aa0'], scene: 'rain',
      lines: [['Umbrellas close like evening flowers', '5--3-2-1-2-3-5--'], ['I wait beneath the station light', '3--5-6-5-3-2----'], ['The last train hums your name', '1--3-5-6-5-3-2--'], ['Stay. The rain will keep us here', '5---6-5-3-2-1---']] },
    { id: 'punk', edge: 'punk', n: 'Delinquent\u2019s Honor', jp: '\u4e0d\u826f\u306e\u4ec1\u7fa9', genre: 'PUNK', col: '#ffd860', ic: '\u26a1', bpm: 168, root: 64, sc: MIN, beat: 'punk',
      sky: ['#3a0a0a', '#e05a1a'], scene: 'alley',
      lines: [['Collar up! Shoes untied!', '1-1-3-1-5-5-3---'], ['Teacher says we\u2019re trouble!', '1-1-3-1-6-5-3---'], ['Back alley, hold the line!', '5-5-6-5-3-3-1---'], ['Never sell a friend out!', '5-5-6-8-6-5-3---'],
        ['Gakuran in the neon!', '1-1-3-1-5-5-3---'], ['Fists up, heads high!', '1-1-3-1-6-5-3---'], ['One more round, one more round!', '5-5-6-5-5-5-6-5-'], ['Honor! Honor! Yeah!', '8---8---6-8-----']] },
    { id: 'duet', edge: 'duet', n: 'Two Foxes', jp: '\u4e8c\u5339\u306e\u72d0', genre: 'DUET', col: '#7aff9a', ic: '\u2665', bpm: 108, root: 62, sc: MAJ, beat: 'four', duet: 1,
      sky: ['#1a2a4a', '#f0a060'], scene: 'dawn',
      lines: [['You walk too fast', '3-5-5-6-5-------', 'ryo'], ['You walk too slow', '3-5-5-3-2-------', 'aoi'], ['Same street, same rain', '5-6-8-6-5-------', 'ryo'], ['Same lights below', '5-6-5-3-2-------', 'aoi'],
        ['Two foxes, one road', '1-3-5-6-8-6-5---', 'both'], ['Home before the dawn', '5-6-8-6-5-3-1---', 'both']] }
  ];
  var EDGE = {
    anthem: { n: 'Anthem', d: '+10 Spirit at the bell of your next fight' },
    ballad: { n: 'Ballad', d: '+4 Guard at the bell (soaks the first hit) next fight' },
    punk: { n: 'Punk', d: 'Your first attack next fight hits +3' },
    duet: { n: 'Duet', d: 'Next fight, Ryo and Aoi each hit +2 on their first attack' }
  };
  A.SONGS = SONGS; A.EDGE = EDGE;
  function chart(S) {
    var spb = 60 / S.bpm, lead = 4 * spb * 2; /* two bars of count-in */
    var notes = [], L = [];
    S.lines.forEach(function (ln, li) {
      var t0 = lead + li * 8 * spb; L.push({ t0: t0, t1: t0 + 8 * spb, s: ln[0], who: ln[2] || null });
      for (var i = 0; i < ln[1].length; i++) { var ch = ln[1][i]; if (ch === '-') continue; var dg = +ch; if (!dg) continue;
        var hold = 0; for (var j = i + 1; j < ln[1].length && ln[1][j] === '-'; j++) hold++;
        notes.push({ t: t0 + i * spb / 2, dg: dg, lane: dg <= 3 ? 0 : dg <= 5 ? 1 : 2, f: 440 * Math.pow(2, (S.root + S.sc[dg - 1] - 69) / 12), d: Math.min(1.2, (hold + 1) * spb / 2), li: li, hit: 0 }); }
    });
    return { notes: notes, lines: L, spb: spb, end: lead + S.lines.length * 8 * spb + 1.2, lead: lead };
  }
  A.chart = chart;
  function grade(p) { return p >= 0.92 ? 'S' : p >= 0.8 ? 'A' : p >= 0.6 ? 'B' : 'C'; }
  A.grade = grade;

  /* song menu: opts { price, yen(), canPay(), pay(), first, onStart(song, lead), onEnd(res), onCancel() } */
  function karaMenu(opts) {
    opts = opts || {};
    var el = openOv(), cv = canvasIn(el), g = cv.g, sel = A._lastSong || 'anthem', lead = A._lastLead || 'ryo';
    /* backdrop: neon booth wall */
    var bg = g.createLinearGradient(0, 0, 0, cv.h); bg.addColorStop(0, '#1c0e30'); bg.addColorStop(1, '#0a0612'); g.fillStyle = bg; g.fillRect(0, 0, cv.w, cv.h);
    for (var i = 0; i < 40; i++) { g.globalAlpha = 0.5; g.drawImage(glowSpr(['255,90,200', '90,216,255', '255,216,96'][i % 3], 40), (i * 97) % cv.w - 40, (i * 173) % cv.h - 40); } g.globalAlpha = 1;
    otxt(g, '\u30ab\u30e9\u30aa\u30b1 \u72d0', cv.w / 2 - 40, 30, 24, '#ffb8ec'); txt(g, 'BOOTH 2', cv.w / 2 + 78, 32, 13, '#7fe8ff');
    btn(el, 'x', 'Leave', function () { closeOv(); ev('world:s2arc:kara:cancel'); if (opts.onCancel) opts.onCancel(); });
    var sm = document.createElement('div'); sm.className = 'sm'; el.appendChild(sm);
    function render() {
      var h = '<div class="hd">PICK A SONG \u00b7 \u00a5' + (opts.price | 0) + ' A SONG</div>';
      SONGS.forEach(function (S) { var E = EDGE[S.edge];
        h += '<button class="song' + (S.id === sel ? ' on' : '') + '" data-s="' + S.id + '"><i style="background:' + S.col + '">' + S.ic + '</i><span><b>' + S.n + '</b><small>' + S.jp + ' \u00b7 ' + S.genre + (S.duet ? ' \u00b7 Ryo & Aoi' : '') + '</small><em>' + (opts.first ? 'First song: a moment for the two of you' : 'A or S: ' + E.n + ' \u00b7 ' + E.d) + '</em></span></button>'; });
      var S0 = SONGS.filter(function (q) { return q.id === sel; })[0];
      h += '<div class="hd">' + (S0 && S0.duet ? 'A DUET \u00b7 BOTH OF YOU SING' : 'WHO TAKES THE MIC?') + '</div>';
      if (!(S0 && S0.duet)) h += '<div class="lead">' + ['ryo', 'aoi'].map(function (k) { return '<button data-l="' + k + '" class="' + (k === lead ? 'on' : '') + '"><img src="portraits/' + k + '_neutral.webp" alt="">' + (k === 'ryo' ? 'Ryo leads' : 'Aoi leads') + '</button>'; }).join('') + '</div>';
      var ok = !opts.canPay || opts.canPay();
      h += '<button class="ab go' + (ok ? '' : ' dim') + '" data-go="1">' + (ok ? '\u266a Sing \u00b7 \u00a5' + (opts.price | 0) : 'Not enough yen \u00b7 \u00a5' + (opts.price | 0)) + '</button>';
      sm.innerHTML = h;
    }
    sm.addEventListener('click', function (e) {
      var t = e.target.closest ? e.target.closest('button') : null; if (!t) return;
      if (t.dataset.s) { sel = t.dataset.s; render(); try { if (root.AUDIO) AUDIO.play('place', { gain: 0.4 }); } catch (eA) {} return; }
      if (t.dataset.l) { lead = t.dataset.l; render(); return; }
      if (t.dataset.go) { if (opts.canPay && !opts.canPay()) return; var S = SONGS.filter(function (q) { return q.id === sel; })[0]; if (!S) return;
        A._lastSong = sel; A._lastLead = lead; if (opts.pay) opts.pay(); if (opts.onStart) opts.onStart(S, S.duet ? 'both' : lead);
        karaPlay(S, S.duet ? 'both' : lead, opts); }
    });
    render(); wake(); ev('world:s2arc:kara:menu');
    return el;
  }
  A.karaMenu = karaMenu;

  var RUN = null;
  function karaPlay(S, lead, opts) {
    opts = opts || {}; stopRun();
    var el = openOv(), cv = canvasIn(el), g = cv.g, W0 = cv.w, H0 = cv.h, s = Math.min(W0 / 390, H0 / 844), ox = (W0 - 390 * s) / 2;
    musicOff(); wake();
    var C = chart(S), t0 = now() + 0.35, sched = 0, beatN = 0, fb = [], combo = 0, best = 0, pts = 0, nP = 0, nG = 0, nM = 0, laneFlash = [0, 0, 0], done = false;
    var ptR = ptImg('ryo'), ptA = ptImg('aoi');
    /* static plate: frame, screen, highway (painted once) */
    var plate = document.createElement('canvas'); plate.width = cv.c.width; plate.height = cv.c.height; var p = plate.getContext('2d'); p.setTransform(cv.d * s, 0, 0, cv.d * s, ox * cv.d, 0);
    var Hh = H0 / s;
    p.fillStyle = '#0a0612'; p.fillRect(-ox / s, 0, W0 / s, Hh);
    var sk = p.createLinearGradient(0, 64, 0, 316); sk.addColorStop(0, S.sky[0]); sk.addColorStop(1, S.sky[1]); rr(p, 10, 60, 370, 258, 14, sk, 4);
    sceneArt(p, S.scene, 10, 60, 370, 258);
    rr(p, 10, 60, 370, 258, 14, null, 4); p.fillStyle = 'rgba(0,0,0,.45)'; p.fillRect(14, 238, 362, 76);
    otxt(p, S.n, 140, 30, 19, S.col, 'center'); txt(p, S.jp + ' \u00b7 ' + S.genre, 140, 50, 11, '#d8c8f0');
    /* highway */
    var HX = [70, 195, 320], HY0 = 470, HY1 = 700;
    rr(p, 18, 452, 354, 268, 16, '#120a1e', 3);
    HX.forEach(function (x, i) { var col = ['255,106,213', '90,216,255', '255,216,96'][i]; var lg = p.createLinearGradient(0, HY0, 0, HY1); lg.addColorStop(0, 'rgba(' + col + ',0)'); lg.addColorStop(1, 'rgba(' + col + ',.22)'); p.fillStyle = lg; p.fillRect(x - 52, HY0 - 14, 104, HY1 - HY0 + 20); p.strokeStyle = 'rgba(' + col + ',.35)'; p.lineWidth = 2; p.beginPath(); p.moveTo(x, HY0 - 10); p.lineTo(x, HY1); p.stroke(); });
    p.strokeStyle = '#fff'; p.lineWidth = 4; p.beginPath(); p.moveTo(24, HY1); p.lineTo(366, HY1); p.stroke();
    /* pads */
    var PADY = 772, PL = [['\u4f4e', 'LOW', '#ff6ad5'], ['\u4e2d', 'MID', '#5ad8ff'], ['\u9ad8', 'HIGH', '#ffd860']];
    PL.forEach(function (q, i) { rr(p, HX[i] - 56, PADY - 44, 112, 88, 18, q[2], 4); rr(p, HX[i] - 50, PADY - 40, 100, 30, 14, 'rgba(255,255,255,.3)', 0); otxt(p, q[0], HX[i], PADY - 6, 30, '#fff'); txt(p, q[1], HX[i], PADY + 26, 12, INK); });
    ev('world:s2arc:kara:start:' + S.id + ':' + lead);
    var stopB = btn(el, 'x', 'Stop', function () { finish(true); });
    function laneAt(x) { var lx = (x - ox) / s; return lx < 132 ? 0 : lx < 258 ? 1 : 2; }
    function press(lane) {
      var tn = now() - t0, bestN = null, bd = 9;
      for (var i = 0; i < C.notes.length; i++) { var n = C.notes[i]; if (n.hit || n.lane !== lane) continue; var d = Math.abs(n.t - tn); if (d < bd) { bd = d; bestN = n; } if (n.t - tn > 0.3) break; }
      laneFlash[lane] = 1;
      if (bestN && bd <= 0.16) { var pf = bd <= 0.075; bestN.hit = pf ? 2 : 1; pts += pf ? 100 : 60; if (pf) nP++; else nG++; combo++; best = Math.max(best, combo);
        tone(bestN.f, now(), Math.max(0.18, bestN.d), 'triangle', 0.22, bestN.d > 0.3); tone(bestN.f * 2, now(), 0.12, 'sine', 0.05);
        fb.push({ s: pf ? 'PERFECT' : 'GOOD', c: pf ? '#ffd860' : '#7fe8ff', x: HX[lane], y: HY1 - 40, t: 0 }); }
      else { tone(110 + lane * 30, now(), 0.06, 'square', 0.03); }
    }
    function onDown(e) { if (done) return; var r = cv.c.getBoundingClientRect(), y = (e.clientY - r.top) / s; if (y < 440) return; e.preventDefault(); press(laneAt(e.clientX - r.left)); }
    cv.c.addEventListener('pointerdown', onDown);
    function keyD(e) { var k = e.key; var m = { a: 0, s: 1, d: 2, j: 0, k: 1, l: 2, ArrowLeft: 0, ArrowDown: 1, ArrowRight: 2 }; if (m[k] != null && !done) { e.preventDefault(); press(m[k]); } if (k === 'Escape') finish(true); }
    document.addEventListener('keydown', keyD);
    function backing(tn) { /* lookahead scheduler: next 0.25 s of beat */
      var spb = C.spb;
      while (sched < tn + 0.25 && sched < C.end - 0.8) { var b = beatN, t = t0 + sched;
        if (S.beat === 'soft') { if (b % 4 === 0) drum('k', t, 0.25); if (b % 2 === 1) drum('h', t, 0.06); tone(440 * Math.pow(2, (S.root - 24 + S.sc[[0, 5, 3, 4][(b / 4 | 0) % 4]] - 69) / 12), t, spb * 0.9, 'sine', 0.07); }
        else if (S.beat === 'punk') { drum('k', t, 0.4); drum(b % 2 ? 's' : 'h', t, b % 2 ? 0.28 : 0.1); tone(440 * Math.pow(2, (S.root - 24 + S.sc[[0, 0, 5, 4][(b / 4 | 0) % 4]] - 69) / 12), t, spb * 0.8, 'sawtooth', 0.05); }
        else { if (b % 2 === 0) drum('k', t, 0.4); else drum('s', t, 0.24); drum('h', t + spb / 2, 0.07); tone(440 * Math.pow(2, (S.root - 24 + S.sc[[0, 4, 5, 3][(b / 4 | 0) % 4]] - 69) / 12), t, spb * 0.7, 'triangle', 0.08); }
        if (sched < C.lead - 0.01 && b % 2 === 0) tone(880, t, 0.05, 'square', 0.04); /* count-in click */
        sched += spb; beatN++; }
    }
    var last = performance.now();
    function frame() {
      if (!RUN || RUN.id !== myId) return;
      var tn = now() - t0, tms = performance.now(), dt = Math.min(0.05, (tms - last) / 1000); last = tms;
      backing(tn);
      for (var i = 0; i < C.notes.length; i++) { var n = C.notes[i]; if (!n.hit && tn - n.t > 0.16) { n.hit = -1; nM++; combo = 0; fb.push({ s: 'MISS', c: '#ff8a8a', x: HX[n.lane], y: HY1 - 40, t: 0 }); } }
      draw(tn, dt);
      if (tn > C.end) { finish(false); return; }
      RUN.raf = requestAnimationFrame(frame);
    }
    function draw(tn, dt) {
      g.setTransform(cv.d, 0, 0, cv.d, 0, 0); g.drawImage(plate, 0, 0, W0, H0);
      g.setTransform(cv.d * s, 0, 0, cv.d * s, ox * cv.d, 0);
      /* lyrics: current line with a colour wipe, next line dim */
      var li = -1; for (var k = 0; k < C.lines.length; k++) if (tn >= C.lines[k].t0 - C.spb * 2 && tn < C.lines[k].t1) li = k;
      if (li < 0 && tn < C.lead) { otxt(g, tn < C.lead / 2 ? '\u266a  Ready\u2026' : '\u266a  Here we go!', 195, 270, 20, '#fff'); }
      if (li >= 0) { var L = C.lines[li], f = clamp((tn - L.t0) / (L.t1 - L.t0 - C.spb), 0, 1), col = L.who === 'ryo' ? '#ff9a5a' : L.who === 'aoi' ? '#7fe8ff' : S.col;
        g.font = '900 19px system-ui,sans-serif'; var tw = Math.min(350, g.measureText(L.s).width);
        otxt(g, L.s, 195, 262, 19, '#fff'); g.save(); g.beginPath(); g.rect(195 - tw / 2 - 4, 240, (tw + 8) * f, 44); g.clip(); otxt(g, L.s, 195, 262, 19, col); g.restore();
        if (L.who) txt(g, L.who === 'both' ? 'RYO & AOI' : L.who.toUpperCase(), 195, 244, 10, col);
        var N = C.lines[li + 1]; if (N) txt(g, N.s, 195, 296, 13, 'rgba(230,220,255,.6)'); }
      /* singer(s) + score */
      var bob = Math.sin(tn * Math.PI * 2 / C.spb) * 2;
      if (lead === 'both') { pt(g, ptR, 18, 326 + bob, 104); pt(g, ptA, 128, 326 - bob, 104); }
      else pt(g, lead === 'aoi' ? ptA : ptR, 18, 326 + bob, 120);
      var tot = C.notes.length * 100, pc = tot ? pts / tot : 0;
      rr(g, 244, 330, 136, 110, 14, '#160c24', 3); txt(g, 'SCORE', 312, 346, 11, '#d8c8f0'); otxt(g, String(pts), 312, 372, 24, '#ffd860'); txt(g, 'COMBO ' + combo, 312, 400, 13, combo > 4 ? '#7aff9a' : '#d8c8f0');
      rr(g, 256, 416, 112, 12, 6, '#2a1a3a', 2); rr(g, 256, 416, 112 * clamp(pc, 0, 1), 12, 6, pc >= 0.8 ? '#7aff9a' : '#ff5ac8', 0);
      /* notes */
      var span = 2.1 * Math.max(0.8, C.spb * 2.2);
      for (var i = 0; i < C.notes.length; i++) { var n = C.notes[i]; var dtn = n.t - tn; if (dtn > span) break; if (n.hit && n.hit !== -1 && dtn < -0.05) continue; if (dtn < -0.3) continue;
        var y = 700 - (dtn / span) * 230; if (y < 456) continue; var x = HX[n.lane], col = ['255,106,213', '90,216,255', '255,216,96'][n.lane];
        if (n.d > 0.3 && !n.hit) { var y2 = 700 - ((dtn + n.d) / span) * 230; rr(g, x - 9, Math.max(456, y2), 18, y - Math.max(456, y2), 9, 'rgba(' + col + ',.35)', 0); }
        g.globalAlpha = n.hit === -1 ? 0.3 : 1; rr(g, x - 34, y - 13, 68, 26, 13, 'rgb(' + col + ')', 3); txt(g, '\u266a', x, y, 16, INK); g.globalAlpha = 1; }
      for (var l = 0; l < 3; l++) if (laneFlash[l] > 0) { g.globalAlpha = laneFlash[l]; g.drawImage(glowSpr(['255,106,213', '90,216,255', '255,216,96'][l], 70), HX[l] - 70, 700 - 70); g.globalAlpha = 1; laneFlash[l] = Math.max(0, laneFlash[l] - dt * 5); }
      for (var q = fb.length - 1; q >= 0; q--) { var F = fb[q]; F.t += dt; if (F.t > 0.6) { fb.splice(q, 1); continue; } g.globalAlpha = 1 - F.t / 0.6; otxt(g, F.s, F.x, F.y - F.t * 40, 16, F.c); g.globalAlpha = 1; }
      if (combo >= 8) otxt(g, combo + ' COMBO!', 195, 470, 15, '#7aff9a');
    }
    function pt(g2, im, x, y, sz) { rr(g2, x, y, sz, sz, 14, '#2a1a3a', 3); if (im && im.complete && im.naturalWidth) { g2.save(); rr(g2, x + 2, y + 2, sz - 4, sz - 4, 12, null, 0); g2.clip(); var iw = im.naturalWidth, ih = im.naturalHeight, sw = iw * 0.62, sh = sw; g2.drawImage(im, (iw - sw) / 2, ih * 0.04, sw, sh, x + 2, y + 2, sz - 4, sz - 4); g2.restore(); } rr(g2, x, y, sz, sz, 14, null, 3);
      g2.drawImage(glowSpr('255,216,96', 16), x + sz - 30, y + sz - 30); txt(g2, '\ud83c\udfa4', x + sz - 14, y + sz - 14, 18, '#fff'); }
    function finish(quit) {
      if (done) return; done = true; if (RUN && RUN.raf) cancelAnimationFrame(RUN.raf); RUN = null;
      document.removeEventListener('keydown', keyD); cv.c.removeEventListener('pointerdown', onDown); if (stopB.parentNode) stopB.remove();
      var tot = C.notes.length * 100, pc = tot ? pts / tot : 0, gr = grade(pc), res = { song: S.id, edge: S.edge, lead: lead, pct: pc, grade: gr, quit: !!quit, perfect: nP, good: nG, miss: nM, best: best, great: !quit && (gr === 'S' || gr === 'A') };
      A.lastRes = res; ev('world:s2arc:kara:end:' + S.id + ':' + gr + ':' + Math.round(pc * 100) + (quit ? ':quit' : ''));
      if (quit) { closeOv(); if (opts.onEnd) opts.onEnd(res); return; }
      resultCard(el, cv, s, ox, S, res, opts);
    }
    var myId = Math.random(); RUN = { id: myId, raf: 0, finish: finish };
    A._run = RUN; RUN.raf = requestAnimationFrame(frame);
    A.karaPress = press; A.karaChart = C; A.karaT0 = function () { return t0; };
  }
  A.karaPlay = karaPlay;
  function stopRun() { if (RUN) { try { cancelAnimationFrame(RUN.raf); } catch (e) {} RUN = null; } }
  function resultCard(el, cv, s, ox, S, res, opts) {
    var g = cv.g; g.setTransform(cv.d * s, 0, 0, cv.d * s, ox * cv.d, 0);
    g.fillStyle = 'rgba(8,4,16,.72)'; g.fillRect(-ox / s, 0, cv.w / s, cv.h / s);
    rr(g, 30, 170, 330, 420, 22, '#f6f0ff', 4); rr(g, 30, 170, 330, 64, 22, S.col, 4);
    otxt(g, S.n, 195, 202, 20, '#fff');
    var gc = { S: '#ffb020', A: '#ff5ac8', B: '#5ad8ff', C: '#8a8aa0' }[res.grade];
    g.drawImage(glowSpr('255,216,96', 90), 195 - 90, 300 - 90); otxt(g, res.grade, 195, 300, 86, gc);
    txt(g, Math.round(res.pct * 100) + '%  \u00b7  best combo ' + res.best, 195, 372, 15, INK);
    txt(g, 'Perfect ' + res.perfect + '   Good ' + res.good + '   Miss ' + res.miss, 195, 398, 13, '#5a4a70', 'center', 700);
    var E = EDGE[S.edge], line1 = '', line2 = '';
    if (opts.first) { line1 = 'First song in the booth.'; line2 = 'Something to remember.'; }
    else if (res.great) { line1 = E.n + ' edge ready'; line2 = E.d; }
    else { line1 = 'Score A or S for the ' + E.n + ' edge.'; line2 = E.d; }
    rr(g, 50, 420, 290, 84, 14, res.great && !opts.first ? '#fff4c8' : '#ece6f8', 3);
    txt(g, line1, 195, 446, 15, res.great && !opts.first ? '#9a1e8a' : INK); wrap(g, line2, 195, 474, 270, 12, '#5a4a70');
    var again = btn(el, '', 'Sing again', function () { closeOv(); if (opts.onEnd) opts.onEnd(res, true); }, 'left:' + (ox + 50 * s) + 'px;top:' + (520 * s) + 'px;width:' + (138 * s) + 'px;background:#7fe8ff');
    var ok = btn(el, '', 'Done', function () { closeOv(); if (opts.onEnd) opts.onEnd(res, false); }, 'left:' + (ox + 202 * s) + 'px;top:' + (520 * s) + 'px;width:' + (138 * s) + 'px;background:#ffd860');
    try { if (root.AUDIO) AUDIO.play(res.great ? 'victory' : 'place', { gain: 0.5 }); } catch (eA) {}
  }
  function wrap(g, s0, x, y, w, px, col) { g.font = '700 ' + px + 'px system-ui,sans-serif'; var words = s0.split(' '), line = '', yy = y; words.forEach(function (wd) { var t = line ? line + ' ' + wd : wd; if (g.measureText(t).width > w && line) { txt(g, line, x, yy, px, col, 'center', 700); line = wd; yy += px + 4; } else line = t; }); if (line) txt(g, line, x, yy, px, col, 'center', 700); }
  A.wrap = wrap;
  function sceneArt(p, k, x, y, w, h) { /* the karaoke video: a painted still per song */
    p.save(); p.beginPath(); p.rect(x + 2, y + 2, w - 4, h - 4); p.clip();
    if (k === 'city' || k === 'alley') { for (var i = 0; i < 9; i++) { var bw = 30 + (i * 17) % 30, bh = 70 + (i * 53) % 110, bx = x + i * 42 - 6; p.fillStyle = k === 'alley' ? '#1a0a0a' : '#14102a'; p.fillRect(bx, y + h - 70 - bh, bw, bh + 70); p.fillStyle = k === 'alley' ? 'rgba(255,160,80,.6)' : 'rgba(255,220,140,.6)'; for (var j = 0; j < 10; j++) if ((i * 7 + j * 3) % 4) p.fillRect(bx + 5 + (j % 3) * 9, y + h - 66 - bh + 10 + ((j / 3) | 0) * 16, 5, 7); }
      p.drawImage(glowSpr(k === 'alley' ? '255,120,40' : '255,90,200', 90), x + w * 0.7 - 90, y + 40 - 90); }
    if (k === 'rain') { p.fillStyle = 'rgba(200,220,255,.3)'; for (var r = 0; r < 90; r++) p.fillRect(x + (r * 41) % w, y + (r * 67) % h, 1.5, 12); p.fillStyle = '#0a1020'; p.fillRect(x, y + h - 100, w, 100); p.drawImage(glowSpr('255,220,150', 60), x + 60 - 60, y + h - 150 - 60); p.fillStyle = '#2a3048'; p.fillRect(x + 56, y + h - 150, 6, 90); }
    if (k === 'dawn') { p.drawImage(glowSpr('255,200,120', 120), x + w / 2 - 120, y + h - 120 - 120); p.fillStyle = '#1a2038'; p.beginPath(); p.moveTo(x, y + h - 80); for (var m = 0; m <= 8; m++) p.lineTo(x + w * m / 8, y + h - 90 - ((m * 37) % 4) * 14); p.lineTo(x + w, y + h); p.lineTo(x, y + h); p.fill();
      [[x + w * 0.42, '#ff9a5a'], [x + w * 0.58, '#7fe8ff']].forEach(function (f) { p.fillStyle = f[1]; p.beginPath(); p.moveTo(f[0] - 8, y + h - 92); p.lineTo(f[0] + 8, y + h - 92); p.lineTo(f[0], y + h - 116); p.fill(); }); }
    p.restore();
  }
  A.sceneArt = sceneArt;
  /* Neon Game Center cabinets moved to s2arc_cab.js (shell, boards, tokens) + one file per game (v6564-arcade). */
  A.wrap = wrap; A.stopKara = stopRun; A.hexRgb = function (h) { var n = parseInt(h.slice(1), 16); return (n >> 16) + ',' + ((n >> 8) & 255) + ',' + (n & 255); };
  ev('world:s2arc:ready');
  } catch (eTop) { try { console.warn('S2ARC init', eTop); } catch (e2) {} }
})();
