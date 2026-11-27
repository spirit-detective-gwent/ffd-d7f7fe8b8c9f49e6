/* v6.5.64 FFF_S2P6 (Punk-route seal 3, GGD-51): Jin's turf, the neon strip.
 * Quest cq2_s2_jin after Masa's Seal. Chain: 1 Ramen Kitsuneya (eat, overhear the Suits, fight them off Tetsuo)
 * 2 Karaoke Kitsune (song menu, lead pick, tap-along; Lt. Kanzaki in the VIP booth) 3 Hotel Chuo (elevator to 7F,
 * break up the deal, neon hallway fight) 4 Club Kitsune back office (Tetsu's ledger ties the deals to Jin)
 * 5 Izakaya Tanuki (small plates; the owner tips the back room) 6 Neon Game Center (meet Jin on the floor,
 * fight him past the staff door; the seal). Hotel ¥40 rest at Hotel Chuo and the Kitsune Hotel, once per stock cycle.
 * Wraps only; no new always-running loops (room work rides c2Frame room changes, minigames run only while open). */
(function () {
  try {
  if (typeof c2S !== 'function' || typeof C2W === 'undefined' || !C2W || typeof INT === 'undefined' || !INT.c2_town) {
    try { ev('world:s2p6:skip'); } catch (e0) {} return;
  }
  var root = typeof window !== 'undefined' ? window : this;
  var P5 = root.FFF_S2P5;
  var P6 = root.FFF_S2P6 = { v: 1, ART: true };

  function on() { return (typeof c2On !== 'function' || c2On()) && (typeof chN !== 'function' || chN() === 2); }
  function S() { return c2S(); }
  function E() { return c2S().e; }
  function room() { try { return c2Room(); } catch (e) { return null; } }
  function nailsRun() { return on() && E().run_fac === 'arc'; }
  function busy() { return !!(W.dgFight || W.dlg || W.busy || W.cut || W.fading || W.paused); }
  function later(ms, fn) { setTimeout(function () { try { fn(); } catch (e) { ev('world:s2p6:err:later:' + (e && e.message)); } }, ms); }
  function talk(lines, done) { if (P6.talk && P6.talk !== talk) return P6.talk(lines, done); W.dlg = true; scene(null, lines, function () { W.dlg = false; if (done) done(); }); }
  function lockIn(on1) { if (on1) { W.cut = true; W.path = []; if (W.ryo) W.ryo.v = 0; try { stickEnd(); } catch (e) {} } else W.cut = false; }
  function sv() { try { if (typeof c2QSync === 'function') c2QSync(); } catch (e) {} save(); }
  function path() { var p = 'balanced'; try { p = c2Path(); } catch (e) {} return p === 'fierce' || p === 'strategic' ? p : 'balanced'; }
  function npc(id, x, y, fa) { var s = c2Npc(id, x, y, fa == null ? Math.PI / 2 : fa); s.el.classList.add('s2'); s.s2id = id; s.el.dataset.npc = id; return s; }
  function kill(s) { if (s && s.el && s.el.parentNode) s.el.remove(); if (s) s.gone = 1; }
  function dlgUp() { var d = document.getElementById('wdlg'); return !!(d && d.className && /\bon\b/.test(d.className)); }
  function whenFree(fn, tries) { tries = tries || 0; if (!busy() && !dlgUp() && !document.getElementById('nqsting') && !(typeof W.c2busy !== 'undefined' && W.c2busy)) { try { fn(); } catch (e) { ev('world:s2p6:err:free:' + (e && e.message)); } return; } later(tries < 120 ? 250 : 1000, function () { whenFree(fn, tries + 1); }); }
  function V3(pre, mid, post) { var o = {}, PP = ['fierce', 'strategic', 'balanced']; PP.forEach(function (p) { o[p] = (pre || []).concat(mid[p] || [], post || []); }); return o; }
  function pv(x) { if (!x || Array.isArray(x)) return x || []; try { return typeof pathLines === 'function' ? pathLines(x) : (x[path()] || x.balanced || []); } catch (e) { return x[path()] || x.balanced || []; } }
  function p5Done() { return !!(P5 && typeof P5.qDone === 'function' && P5.qDone()) || !!E().seal_depot; }
  function toastS(m) { try { if (typeof toast === 'function') toast(m); } catch (e) {} }
  P6.later = later; P6.talk = talk; P6.lockIn = lockIn; P6.busy = busy; P6.pv = pv; P6.V3 = V3; P6.whenFree = whenFree; P6.sv = sv; P6.path = path;

  /* ---------------- state ---------------- */
  function NS() { var e = E(); if (!e.nq || typeof e.nq !== 'object') e.nq = {}; return e.nq; }
  function J() { var n = NS(); if (!n.jin || typeof n.jin !== 'object') n.jin = {}; return n.jin; }
  /* stages, in order */
  var ORDER = ['open', 'ramen', 'kara', 'hotel', 'club', 'izak', 'met', 'won', 'done'];
  function stg() { return J().st || ''; }
  function at(s) { return ORDER.indexOf(stg()) >= ORDER.indexOf(s); }
  function setStg(v) { if (ORDER.indexOf(v) < ORDER.indexOf(stg())) return; J().st = v; syncSteps(); sv(); ev('world:s2p6:st:' + v); }
  var QID = 'cq2_s2_jin';
  var Q = { id: QID, n: 'High Score', giver: 'Tetsuo, at Ramen Kitsuneya', loc: 'Kitsune-Ch\u016b\u014d \u00b7 the neon strip' };
  var STEP = {
    open: 'Eat at Ramen Kitsuneya. Tetsuo hears everything on the strip.',
    ramen: 'The Suits said booth 4. Karaoke Kitsune, next door to the ramen shop.',
    kara: 'Kanzaki talked: the Suits close a deal tonight. Hotel Chuo, seventh floor.',
    hotel: 'The deal sheets carry a Club Kitsune stamp. The club\u2019s back office.',
    club: 'The money runs to Jin. Izakaya Tanuki\u2019s owner knows the Game Center.',
    izak: 'Neon Game Center. Find Jin on the floor.',
    met: 'Jin\u2019s back room, past the staff door. Take his seal.',
    won: 'Take Jin\u2019s seal.',
    done: 'Jin\u2019s seal is off the prize-room lock. The strip breathes.'
  };
  function stepText() { return STEP[stg()] || STEP.open; }
  function syncSteps() { try { if (typeof C2Q !== 'undefined') C2Q[QID] = { n: Q.n, steps: [stepText()] }; } catch (e) {} }
  if (typeof C2Q !== 'undefined') C2Q[QID] = { n: Q.n, steps: [STEP.open] };
  if (typeof C2QLOC !== 'undefined') C2QLOC[QID] = ['town', Q.loc];
  function qOpen() { var s = S(); if (s.q[QID] == null) s.q[QID] = 0; SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = s.q[QID] | 0; s.qa = QID; SAVE.qa = QID; SAVE.qTrack = ''; SAVE.qTrackPick = 0; syncSteps(); sv(); ev('world:s2p6:quest:open'); }
  function qStep(n) { var s = S(); if (s.q[QID] == null || s.q[QID] === 9) return; s.q[QID] = Math.max(s.q[QID] | 0, n); SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = s.q[QID]; sv(); }
  function qClose() { var s = S(); if (s.q[QID] == null || s.q[QID] === 9) return; s.q[QID] = 9; SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = 9;
    SAVE.journalLog = SAVE.journalLog || []; if (SAVE.journalLog.indexOf(Q.n) < 0) SAVE.journalLog.push(Q.n);
    if (s.qa === QID) { s.qa = (typeof CQ !== 'undefined' && CQ.locks) || ''; SAVE.qa = s.qa; } sv(); ev('world:s2p6:quest:done');
    if (typeof window.c2QuestYen === 'function') window.c2QuestYen(QID, Q.n); }
  function qOn() { var q = S().q[QID]; return q != null && q !== 9; }
  function qDone() { return S().q[QID] === 9; }
  function p6Enter() { return on() && nailsRun() && !!E().seal_sento && p5Done(); }
  /* the strip buildings stay open after the chain (eat, rest, sing, play) */
  function stripOpen() { return p6Enter(); }
  P6.Q = Q; P6.QID = QID; P6.stg = stg; P6.at = at; P6.setStg = setStg; P6.qOpen = qOpen; P6.qClose = qClose; P6.qOn = qOn; P6.qDone = qDone;
  P6.p6Enter = p6Enter; P6.stripOpen = stripOpen; P6.J = J; P6.stepText = stepText; P6.ORDER = ORDER; P6.E = E; P6.room = room;

  /* ---------------- cast (aliases of existing sheets; provisional names pending Erik) ---------------- */
  function alias(id, src, k, nm, fig) {
    ['map', 'walk', 'idle', 'fig', 'run', 'hurt', 'kn', 'lie', 'fig_hurt', 'fig_down'].forEach(function (sh) { if (IMG[src + '_' + sh]) IMG[id + '_' + sh] = IMG[src + '_' + sh]; });
    if (SHC[src + '_walk']) SHC[id + '_walk'] = SHC[src + '_walk'];
    if (IMG[src + '_idle']) { SHC[id + '_idle'] = SHC[src + '_idle'] || 4; if (typeof SHR !== 'undefined' && SHR[src + '_idle'] != null) SHR[id + '_idle'] = SHR[src + '_idle']; }
    if (typeof BW_IDS !== 'undefined' && BW_IDS[src]) BW_IDS[id] = 1;
    if (typeof C2K !== 'undefined') C2K[id] = k; NM[id] = nm; PT[id] = PT[src] || (src + '_fig');
    if (fig && typeof PT_PAINT !== 'undefined') { PT_PAINT[id] = fig; if (typeof PT_HAS !== 'undefined') PT_HAS[fig + '_neutral'] = 1; }
  }
  try {
    alias('j6_tetsuo', 'npc_ramen', 1.12, 'Old Man Tetsuo', 'tetsuo');
    alias('j6_suit', 'c2_suit', (C2K && C2K.c2_suit) || 1.15, 'Syndicate Suit', 'c2suit');
    alias('j6_suit2', 'c2_suit', (C2K && C2K.c2_suit) || 1.15, 'Syndicate Suit', 'c2suit');
  } catch (eA) { ev('world:s2p6:err:alias:' + (eA && eA.message)); }
  P6.alias = alias;

  /* ---------------- rooms ---------------- */
  var RW = 1280, RH = 900;
  var KEYS = P6.KEYS = [];
  var RNAME = P6.RNAME = {};
  var TOWN_DOORS = P6.TOWN_DOORS = {
    /* strip fronts face south onto Chuo-dori (y 1580) */
    ramen: { r: [2200, 1500, 2300, 1584], at: [2250, 1626] },
    kara: { r: [2600, 1500, 2700, 1584], at: [2650, 1626] },
    izak: { r: [4010, 1500, 4110, 1584], at: [4060, 1626] },
    hchuo: { r: [4560, 1500, 4660, 1584], at: [4610, 1626] }
  };
  Object.keys(TOWN_DOORS).forEach(function (k) { var D = TOWN_DOORS[k]; D.to = k; D.out = [D.at[0], D.at[1] + 10]; C2W.doors['j6_' + k] = D; });
  function roomDef(k, n, mus, extra) {
    var id = 'c2_j6_' + k; C2R[k] = id; KEYS.push(k); RNAME[k] = n;
    var w = (extra && extra.w) || RW, h = (extra && extra.h) || RH, ex = w / 2;
    var D = INT[id] = Object.assign({ id: id, n: n, w: w, h: h, src: 'world/j6_' + k + '.paint', tiles: 1, cell: 15, dg: 'c2', c2: k, deep: 1, safe: 1, mus: mus || 'c2night', nq: 1, s2: 1, j6: 1,
      open: [[90, 250, w - 90, h - 50], [ex - 60, h - 50, ex + 60, h]], 'in': [ex, h - 80, 3], back: [ex, h - 80, 3], block: [] }, extra || {});
    D.spots = [{ id: 'exit', r: [ex - 65, h - 50, ex + 65, h], at: [ex, h - 30], face: 0 }].concat((extra && extra.spots) || []);
    D.base = D.block; TAGS_IN[id] = {};
    return D;
  }
  P6.roomDef = roomDef;
  roomDef('ramen', 'Ramen Kitsuneya \u00b7 \u72d0\u5c4b', 'c2night', {
    block: [[190, 250, 1076, 362], [1006, 250, 1076, 550], [110, 600, 202, 750], [250, 590, 320, 664], [810, 596, 1030, 684], [810, 746, 1030, 834], [1110, 740, 1190, 820]],
    spots: [{ id: 'j6_ramen_order', r: [560, 250, 720, 362], at: [640, 440], face: 3, lab: 'Order' },
      { id: 'j6_ramen_ticket', r: [110, 600, 202, 750], at: [240, 700], face: 1, lab: 'Look' }]
  });
  [['j6_e_ramen', 'ramen'], ['j6_e_kara', 'kara'], ['j6_e_izak', 'izak'], ['j6_e_hchuo', 'hchuo']].forEach(function (a) {
    var D = TOWN_DOORS[a[1]]; INT.c2_town.spots.push({ id: a[0], r: D.r, at: D.at, face: 3, lab: 'Enter' }); TRANS[a[0]] = 1; });
  delete INT.c2_town.G;
  if (typeof c2DoorOf === 'function') { var door0 = c2DoorOf; c2DoorOf = function (k) { if (TOWN_DOORS[k]) return TOWN_DOORS[k]; if (P6.innerDoor && P6.innerDoor[k]) return P6.innerDoor[k]; return door0.apply(this, arguments); }; }
  if (typeof c2Surf === 'function') { var surf0 = c2Surf; c2Surf = function (x, y) { var k = c2Room(); if (KEYS.indexOf(k) >= 0) return (P6.SURF && P6.SURF[k]) || 'stone'; return surf0.apply(this, arguments); }; }
  P6.SURF = { ramen: 'stone' };
  /* C2AMB grades for the strip interiors (read through root.FFF_AMB_X; no rain indoors) */
  var AMB = root.FFF_AMB_X = root.FFF_AMB_X || {};
  AMB.ramen = { top: 'rgba(255,170,110,.30)', bot: 'rgba(70,30,40,.28)', rain: 0, motes: 8, steamN: 2, lamps: [[200, 214, '255,140,80', 60, 0.34, 'lantern'], [1080, 214, '255,140,80', 60, 0.34, 'lantern'], [640, 170, '255,200,130', 80, 0.36, 'lamp']] };
  function inJ6() { return KEYS.indexOf(room()) >= 0; }
  P6.inJ6 = inJ6;
  function roomOpen(k) { if (!stripOpen()) return false; var f = P6.OPEN && P6.OPEN[k]; return f ? !!f() : true; }
  P6.OPEN = {};
  P6.roomOpen = roomOpen;

  /* ---------------- paint (once per entry, cached per state key) ---------------- */
  var RCV = {};
  function strip(keep) { try { [].forEach.call(document.querySelectorAll('[id^="j6Room_"]'), function (el) { if (keep && el.id === 'j6Room_' + keep) return; if (el.parentNode) el.parentNode.removeChild(el); }); } catch (e) {} }
  function paintKey(k) { var f = P6.PKEY && P6.PKEY[k]; return k + ':' + (f ? f() : ''); }
  P6.PKEY = {};
  function paintRoom() {
    var k = room(); strip(KEYS.indexOf(k) >= 0 ? k : null);
    if (KEYS.indexOf(k) < 0) return;
    var m = document.getElementById('wimap') || document.getElementById('world'); if (!m) return;
    var D = INT[C2R[k]], key = paintKey(k);
    if (!RCV[key]) {
      var c = RCV[key] = document.createElement('canvas'); c.width = D.w; c.height = D.h;
      try { if (P6.ART && root.FFF_S2P && root.FFF_S2P.p6Paint) root.FFF_S2P.p6Paint(k, c.getContext('2d'), { j: J(), e: E() }); } catch (e) { ev('world:s2p6:err:paint:' + k + ':' + (e && e.message)); }
    }
    var cv = RCV[key];
    try { [].forEach.call(document.querySelectorAll('#j6Room_' + k), function (el) { if (el !== cv && el.parentNode) el.parentNode.removeChild(el); }); } catch (eD) {}
    if (cv.parentNode !== m) { cv.className = 'nqprop'; cv.id = 'j6Room_' + k; cv.setAttribute('data-key', key); cv.style.cssText = 'position:absolute;left:0;top:0;width:' + D.w + 'px;height:' + D.h + 'px;z-index:1;pointer-events:none'; m.insertBefore(cv, m.firstChild); }
  }
  P6.paintRoom = paintRoom; P6.resetPaint = function (k) { Object.keys(RCV).forEach(function (q) { if (!k || q.indexOf(k + ':') === 0) delete RCV[q]; }); strip(null); };

  /* ---------------- battle backdrops ---------------- */
  P6.BT = {};
  function hookBattle() {
    if (P6._bt) return true;
    if (!root.FFF_C2BT || !root.FFF_S2P || !root.FFF_S2P.p6Battle) return false;
    P6._bt = 1;
    var BT = root.FFF_C2BT;
    Object.keys(P6.BT).forEach(function (k) { var o = P6.BT[k];
      BT.ROOMS['j6' + k] = { name: o.name, paint: function (x) { root.FFF_S2P.p6Battle(k, x); }, lights: o.lights || [], rain: 0, mood: o.mood || 'room', feet: 52, neon: o.neon };
      BT.KEY['c2_j6' + k] = 'j6' + k; });
    var roomB0 = BT.room;
    BT.room = function (story) { var ctx = (story && story.ctx) || {}; if (P6.ART && ctx.j6bt && P6.BT[ctx.j6bt]) return 'c2_j6' + ctx.j6bt; return roomB0.apply(this, arguments); };
    return true;
  }
  P6.hookBattle = hookBattle;
  P6.BT.ramen = { name: 'Ramen Kitsuneya', lights: [[200, 110, '255,170,110', 90, 0.32, 'lamp'], [520, 110, '255,170,110', 90, 0.32, 'lamp']] };

  /* fights: ctx.j6k routes the result */
  var FIGHT = P6.FIGHT = {};
  var fighting = 0;
  function startFight(k, ids, extra) {
    if (fighting) return;
    fighting = k; lockIn(0);
    var ctx = Object.assign({ dg: 'c2', dgk: 'j6_' + k, s2: 1, j6k: k, j6bt: (extra && extra.bt) || null, flv: 6 }, (extra && extra.ctx) || {});
    try { hookBattle(); fight(ids, false, ctx); } catch (eF) { fighting = 0; ev('world:s2p6:err:fight:' + (eF && eF.message)); }
  }
  P6.startFight = startFight;
  if (typeof onFightEnd === 'function') {
    var of0 = onFightEnd;
    onFightEnd = function (win, c) {
      var r = of0.apply(this, arguments);
      try { if (c && c.j6k) { var k = c.j6k; fighting = 0; var F = FIGHT[k]; if (F) { /* let the base's post-fight beats (reward toast, first-fight 'why' talk) claim the dialog first */ if (win) later(1100, function () { whenFree(function () { F.win(c); }); }); else if (F.lose) later(1100, function () { whenFree(function () { F.lose(c); }); }); } } } catch (eE) { ev('world:s2p6:err:fend:' + (eE && eE.message)); }
      return r;
    };
  }

  /* ---------------- shared: menus, eat ---------------- */
  function menus() { return root.FFF_S2MENUS; }
  function openShop(id) { var M = menus(); if (!M || !M.SHOPS || !M.SHOPS[id]) return false; try { if (W.ryo) { W.ryo.v = 0; W.path = []; } M.open(id); return true; } catch (e) { ev('world:s2p6:err:shop:' + (e && e.message)); return false; } }
  P6.openShop = openShop;
  /* after a counter meal closes the menu, run any hooked follow-up once (rides ev, no loop) */
  var afterMeal = null;
  P6.afterMeal = function (fn) { afterMeal = fn; };
  /* listen on FFF_UI.ev (the world's ev() forwards there); rides events, no loop */
  function hookEv() {
    var UI = root.FFF_UI; if (!UI || typeof UI.ev !== 'function' || UI.ev._j6) return !!(UI && UI.ev && UI.ev._j6);
    var ev0 = UI.ev;
    UI.ev = function (k) {
      var r = ev0.apply(this, arguments);
      try {
        if (k && typeof k === 'string') {
          if (k.indexOf('world:s2m:buy:j6_') === 0) P6._ate = 1;
          if (k.indexOf('world:s2m:buy:j6_ramen:') === 0 && /:0$/.test(k) && (J().freeBowls | 0) > 0) { J().freeBowls = (J().freeBowls | 0) - 1; sv(); }
          else if (k === 'world:shop:close' && afterMeal && P6._ate) { var f = afterMeal; afterMeal = null; P6._ate = 0; setTimeout(function () { whenFree(f); }, 400); }
          if (P6.onEv) P6.onEv(k);
        }
      } catch (e) {}
      return r;
    };
    UI.ev._j6 = 1; return true;
  }
  if (!hookEv()) later(0, hookEv);
  P6.hookEv = hookEv;

  /* ---------------- 1. Ramen Kitsuneya ---------------- */
  var RAMEN_ITEMS = [
    { id: 'shoyu', n: 'Shoyu ramen', jp: '\u91a4\u6cb9', icon: 'r_shoyu', hp: 30, base: 14, cost: 14, eat: 'shoyu',
      eff: '+30 HP  \u00b7  eat at the counter', flavor: 'Clear soy broth, chashu, a soft egg. Tetsuo\u2019s first bowl.' },
    { id: 'miso', n: 'Miso ramen', jp: '\u5473\u564c', icon: 'r_miso', hp: 34, base: 16, cost: 16, eat: 'miso',
      eff: '+34 HP  \u00b7  eat at the counter', flavor: 'Thick, sweet miso with butter-corn. Holds its heat.' },
    { id: 'tonkotsu', n: 'Tonkotsu ramen', jp: '\u8c5a\u9aa8', icon: 'r_tonkotsu', hp: 40, base: 20, cost: 20, eat: 'tonkotsu',
      eff: '+40 HP  \u00b7  eat at the counter', flavor: 'Pork-bone broth boiled since noon. The big one.' },
    { id: 'oolong', n: 'Oolong tea', jp: '\u70cf\u9f8d\u8336', icon: 'r_oolong', sp: 6, base: 4, cost: 4, drink: 1,
      eff: '+6 SP  \u00b7  drink now', flavor: 'Cold, from the glass bottle in the case.' }
  ];
  P6.RAMEN_ITEMS = RAMEN_ITEMS;
  /* after the Suits fight Tetsuo feeds them free: J().freeBowls bowls at ¥0 (tea still costs) */
  function ramenItems() { var n = J().freeBowls | 0; if (!n) return RAMEN_ITEMS; return RAMEN_ITEMS.map(function (it) { if (it.drink) return it; var o = Object.assign({}, it); o.base = 0; o.cost = 0; o.eff = it.eff + '  \u00b7  on the house (' + n + ' left)'; return o; }); }
  P6.ramenItems = ramenItems;
  function regShops() {
    var M = menus(); if (!M || !M.SHOPS) return false;
    M.SHOPS.j6_ramen = { id: 'j6_ramen', theme: 'ramen', n: 'Ramen Kitsuneya', jp: '\u3089\u30fc\u3081\u3093 \u72d0\u5c4b', who: 'j6_tetsuo', leave: '\u3054\u3061\u305d\u3046\u3055\u307e  \u00b7  Done',
      hi: { fierce: 'Sit. Eat. Don\u2019t start anything in my shop.', strategic: 'Order by the number. The machine\u2019s broken, I take yen.', balanced: 'Sit, sit. The broth\u2019s been on since noon.' },
      nails: function () { return false; }, items: function () { return ramenItems(); } };
    return true;
  }
  P6.regShops = regShops;
  regShops();
  var VO = P6.VO = {};
  VO.ramenIn = [['j6_tetsuo', 'Irasshai! Counter\u2019s free. Not the corner booth.'], ['aoi', 'Why not the corner?'], ['j6_tetsuo', '{quiet}Because it\u2019s taken. Every night this week.{/quiet}']];
  VO.ramenIn2 = [['j6_tetsuo', 'Irasshai. Sit anywhere.']];
  VO.overhear = V3(
    [['', '<p class="dim">The corner booth. Two Suits, two untouched bowls. They talk like nobody else eats here.</p>'],
      ['j6_suit', 'Jin wants the strip\u2019s cut doubled by Friday. Every door on Chuo-dori.'],
      ['j6_suit2', 'The karaoke place is short again.'],
      ['j6_suit', 'Then Kanzaki talks to them. He takes booth four tonight. He always takes booth four.'],
      ['j6_suit2', 'And the old man?'],
      ['j6_suit', 'The old man pays now.']],
    {
      fierce: [['ryo', '{quiet}Booth four.{/quiet}'], ['aoi', '{quiet}Finish your noodles first.{/quiet}']],
      strategic: [['aoi', '{quiet}Booth four. Kanzaki. Friday.{/quiet}'], ['ryo', '{quiet}Got it. Eat slow.{/quiet}']],
      balanced: [['ryo', '{quiet}They\u2019re squeezing him.{/quiet}'], ['aoi', '{quiet}Wait. Let them say it all.{/quiet}']]
    },
    [['j6_suit', 'Old man. Envelope.'], ['j6_tetsuo', 'I paid Tuesday.'], ['j6_suit2', 'Tuesday was last price. Jin plays for a higher score now.']]);
  VO.ramenStep = V3([], {
    fierce: [['ryo', 'He paid. Walk out.'], ['j6_suit', 'Kazan\u2019s schoolboys. Long way from your yard.']],
    strategic: [['aoi', 'You\u2019re collecting twice. That never ends well.'], ['j6_suit', 'For you, girl.']],
    balanced: [['ryo', 'Leave him be. He\u2019s cooking.'], ['j6_suit', 'Then cook this.']]
  }, []);
  VO.ramenWon = V3([['j6_suit', '\u2026Jin hears about this.']], {
    fierce: [['ryo', 'Good. Tell him we\u2019re coming.']],
    strategic: [['aoi', 'Tell him the price went down.']],
    balanced: [['ryo', 'Tell him the old man\u2019s closed to Suits.']]
  }, [['j6_tetsuo', '\u2026You two. You eat here free for a week.'], ['j6_tetsuo', 'Jin runs the Game Center like a high-score board. Every shop\u2019s a number. Kanzaki keeps his numbers.'],
    ['aoi', 'Booth four. Karaoke Kitsune.'], ['j6_tetsuo', 'Next door. Kanzaki sings badly and loud. You\u2019ll find him.']]);
  VO.ticket = [['', '<p class="dim">The ticket machine\u2019s screen says \u6545\u969c (broken). Someone taped a note: \u201cPAY TETSUO\u201d.</p>']];

  var R_CAST = { t: null, a: null, b: null };
  function popRamen() {
    var k = room();
    if (k !== 'ramen') { ['t', 'a', 'b'].forEach(function (q) { if (R_CAST[q]) { kill(R_CAST[q]); R_CAST[q] = null; } }); return; }
    if (!R_CAST.t || !R_CAST.t.el || !R_CAST.t.el.parentNode) { R_CAST.t = npc('j6_tetsuo', 640, 214, Math.PI / 2); try { waddle(R_CAST.t, 0, Math.PI / 2); } catch (e) {} }
    var suits = qOn() && stg() === 'open';
    if (suits) {
      if (!R_CAST.a || !R_CAST.a.el || !R_CAST.a.el.parentNode) { R_CAST.a = npc('j6_suit', 770, 640, 0); }
      if (!R_CAST.b || !R_CAST.b.el || !R_CAST.b.el.parentNode) { R_CAST.b = npc('j6_suit2', 1070, 640, Math.PI); }
    } else { ['a', 'b'].forEach(function (q) { if (R_CAST[q]) { kill(R_CAST[q]); R_CAST[q] = null; } }); }
    try { if (!W.c2n) W.c2n = {}; W.c2n.j6t = R_CAST.t; } catch (eN) {}
  }
  P6.popRamen = popRamen; P6.R_CAST = R_CAST;
  function ramenArrive() {
    if (room() !== 'ramen') return;
    var j = J();
    whenFree(function () {
      if (room() !== 'ramen') return;
      lockIn(1);
      talk(qOn() && stg() === 'open' && !j.rIn ? VO.ramenIn : VO.ramenIn2, function () { j.rIn = 1; sv(); lockIn(0); });
    });
  }
  function ramenOrder() {
    if (busy()) return true;
    if (qOn() && stg() === 'open') { P6._ate = 0; P6.afterMeal(overhear); }
    openShop('j6_ramen');
    return true;
  }
  function overhear() {
    if (room() !== 'ramen' || stg() !== 'open') return;
    lockIn(1);
    talk(pv(VO.overhear), function () {
      var a = R_CAST.a, b = R_CAST.b, t = R_CAST.t;
      /* the Suits get up and lean on the counter */
      try { if (a) { a.x = 600; a.y = 420; place(a, 0); waddle(a, 0, -Math.PI / 2); } if (b) { b.x = 700; b.y = 430; place(b, 0); waddle(b, 0, -Math.PI / 2); } } catch (eM) {}
      later(350, function () {
        talk(pv(VO.ramenStep), function () {
          J().rFight = 1; sv();
          startFight('ramen', ['c2_suit', 'c2_suit'], { bt: 'ramen' });
        });
      });
    });
  }
  FIGHT.ramen = {
    win: function () {
      ['a', 'b'].forEach(function (q) { if (R_CAST[q]) { kill(R_CAST[q]); R_CAST[q] = null; } });
      lockIn(1);
      talk(pv(VO.ramenWon), function () { lockIn(0); setStg('ramen'); qStep(1); J().freeBowls = 7; sv(); toastS('Journal: booth four, Karaoke Kitsune.'); });
    },
    lose: function () { J().rFight = 0; sv(); }
  };
  P6.overhear = overhear; P6.ramenOrder = ramenOrder;
  /* ---------------- pin ---------------- */
  var PIN = P6.PIN = {
    open: function () { return { room: 'town', x: TOWN_DOORS.ramen.at[0], y: TOWN_DOORS.ramen.at[1] - 60, lab: 'Ramen', loc: 'High Score \u00b7 Ramen Kitsuneya' }; }
  };
  function s2Tgt() {
    if (!p6Enter() || !qOn()) return null;
    var f = PIN[stg()]; if (!f) return null;
    var t = f(); if (!t) return null;
    if (t.room !== 'town' && room() !== t.room && inJ6()) return t;
    return t;
  }
  P6.s2Tgt = s2Tgt;
  if (typeof c2LocksT === 'function') { var lt0 = c2LocksT; c2LocksT = function () { try { var t = s2Tgt(); if (t) return t; } catch (eL) {} return lt0.apply(this, arguments); }; }

  function chainRepair() {
    if (!p6Enter()) return;
    if (!qOn() && !qDone()) { qOpen(); if (!stg()) setStg('open'); ev('world:s2p6:repair'); }
    if (E().seal_game && !qDone() && P6.finishQuest) P6.finishQuest();
    syncSteps();
  }
  P6.chainRepair = chainRepair;

  /* ---------------- dispatch ---------------- */
  var ACT = P6.ACT = {
    j6_ramen_order: function () { return ramenOrder(); },
    j6_ramen_ticket: function () { if (busy()) return true; lockIn(1); talk(VO.ticket, function () { lockIn(0); }); return true; }
  };
  var TALK = P6.TALK = { j6_tetsuo: function () { return ramenOrder(); } };
  var ARRIVE = P6.ARRIVE = { ramen: ramenArrive };
  var POP = P6.POP = [popRamen];
  function enterRoom(k, pos) { if (W.fading) return; W.path = []; W.dlg = true; ev('world:c2:enter:' + k);
    try { intFade(function () { W.dlg = false; if (pos) c2Go(k, pos); else c2Go(k); try { AU.play('door', { gain: 0.55 }); } catch (eA) {} }, function () { var f = ARRIVE[k]; if (f) f(); }); }
    catch (eE) { W.dlg = false; try { if (pos) c2Go(k, pos); else c2Go(k); } catch (e2) {} } }
  P6.enterRoom = enterRoom;
  function popAll() { POP.forEach(function (f) { try { f(); } catch (e) { ev('world:s2p6:err:pop:' + (e && e.message)); } }); }
  P6.popAll = popAll;

  /* ---------------- 2. Karaoke Kitsune ---------------- */
  try {
    alias('j6_kaede', 'kaedef', (C2K && C2K.kaedef) || 1.0, 'Kaede (front desk)', 'kaede');
    alias('j6_kanzaki', 'c2_suitR', (C2K && C2K.c2_suitR) || 1.15, 'Kanzaki', 'c2runner');
    alias('j6_ksuit', 'c2_suit', (C2K && C2K.c2_suit) || 1.15, 'Syndicate Suit', 'c2suit');
    if (typeof CHAR_INTRO !== 'undefined' && !CHAR_INTRO.j6_kanzaki) CHAR_INTRO.j6_kanzaki = { kind: 'mgs', name: 'Kanzaki', sub: 'Syndicate Lieutenant', tag: 'He keeps Jin\u2019s numbers.', who: 'c2runner', mood: 'calm' };
  } catch (eK) { ev('world:s2p6:err:alias2:' + (eK && eK.message)); }
  var KARA_PRICE = P6.KARA_PRICE = 8;
  roomDef('kara', 'Karaoke Kitsune \u00b7 \u30ab\u30e9\u30aa\u30b1\u72d0', 'ck_surf', {
    block: [[110, 296, 444, 400], [1066, 296, 1184, 454], [596, 596, 824, 672], [110, 740, 180, 820], [1110, 740, 1180, 820]],
    spots: [{ id: 'j6_kara_desk', r: [110, 296, 444, 400], at: [280, 450], face: 3, lab: 'Desk' },
      { id: 'j6_kara_b2', r: [478, 150, 602, 252], at: [540, 300], face: 3, lab: 'Booth 2' },
      { id: 'j6_kara_b3', r: [718, 150, 842, 252], at: [780, 300], face: 3, lab: 'Booth 3' },
      { id: 'j6_kara_b4', r: [968, 150, 1092, 252], at: [1030, 300], face: 3, lab: 'Booth 4' }]
  });
  roomDef('karaB', 'Booth 2 \u00b7 \u30ab\u30e9\u30aa\u30b1', 'c2night', { w: 1000, h: 900, open: [[90, 220, 910, 850], [440, 850, 560, 900]],
    block: [[190, 380, 810, 414], [190, 380, 226, 640], [774, 380, 810, 640], [366, 456, 634, 574], [180, 56, 290, 176], [710, 56, 820, 176]],
    spots: [{ id: 'j6_kara_sing', r: [366, 456, 634, 574], at: [500, 620], face: 3, lab: 'Sing' }] });
  roomDef('karaV', 'Booth 4 \u00b7 VIP', 'ck_backroom', { w: 1100, h: 900, open: [[90, 220, 1010, 850], [490, 850, 610, 900]],
    block: [[220, 380, 880, 414], [220, 380, 256, 660], [844, 380, 880, 660], [406, 466, 694, 594]],
    spots: [{ id: 'j6_kara_vip', r: [406, 466, 694, 594], at: [550, 640], face: 3, lab: 'Look' }] });
  P6.SURF.kara = 'wood'; P6.SURF.karaB = 'wood'; P6.SURF.karaV = 'wood';
  AMB.kara = { top: 'rgba(255,120,220,.24)', bot: 'rgba(40,20,90,.30)', rain: 0, motes: 10, lamps: [[120, 140, '255,90,200', 60, 0.3, 'neon'], [300, 180, '90,216,255', 50, 0.26, 'neon']], neon: [[120, 120, 40, '255,90,200']] };
  AMB.karaB = { top: 'rgba(160,120,255,.26)', bot: 'rgba(30,20,70,.30)', rain: 0, motes: 12, lamps: [[195, 160, '255,90,200', 60, 0.3, 'neon'], [195, 300, '90,216,255', 60, 0.24, 'neon']] };
  AMB.karaV = { top: 'rgba(255,200,110,.24)', bot: 'rgba(40,24,10,.30)', rain: 0, motes: 8, lamps: [[195, 200, '255,200,90', 70, 0.3, 'lamp']] };
  P6.PKEY.kara = function () { return at('kara') ? 'free' : 'vip'; };
  P6.OPEN.kara = function () { return true; };
  P6.BT.karaV = { name: 'Karaoke Kitsune \u00b7 Booth 4', lights: [[360, 120, '255,200,90', 100, 0.32, 'lamp']] };
  P6.innerBack = P6.innerBack || {};
  P6.innerBack.karaB = function () { enterRoom('kara', [540, 300, 0]); };
  P6.innerBack.karaV = function () { enterRoom('kara', [1030, 300, 0]); };

  VO.karaIn = V3([['j6_kaede', 'Welcome to Karaoke Kitsune! One song, \u00a5' + KARA_PRICE + '. Booth two is open.']], {
    fierce: [['ryo', 'Booth four. Who\u2019s in it?'], ['j6_kaede', '\u2026Reserved. A regular. Please don\u2019t.']],
    strategic: [['aoi', 'Booth four is taken tonight?'], ['j6_kaede', 'Every night. He books it by the month.']],
    balanced: [['ryo', 'Busy night?'], ['j6_kaede', 'Booth four is always busy. Listen.'], ['', '<p class="dim">From behind the gold door, a man is murdering an enka standard.</p>']]
  }, []);
  VO.karaIn2 = [['j6_kaede', 'Booth two\u2019s yours. \u00a5' + KARA_PRICE + ' a song.']];
  VO.b3 = [['', '<p class="dim">\u4f7f\u7528\u4e2d. Through the slit window: four office workers, ties around their heads, singing like a funeral.</p>']];
  VO.b4Shut = [['j6_kaede', 'That\u2019s a VIP booth. Members only.']];
  VO.b4Empty = [['', '<p class="dim">Booth four is empty now. Someone left a tie on the sofa.</p>']];
  VO.vipIn = V3([['', '<p class="dim">Gold carpet. A man in a sharp suit holds the mic like a cigarette. A deal sheet sits under the ice bucket.</p>'],
    ['j6_kanzaki', '\u2026and the neon cries for meeee\u2014 Who opened my door?']], {
    fierce: [['ryo', 'The ramen shop pays nothing now. Tell your boss.'], ['j6_kanzaki', 'The schoolboy from Tetsuo\u2019s. You cost me two men and a song.']],
    strategic: [['aoi', 'Kanzaki. You keep Jin\u2019s numbers.'], ['j6_kanzaki', 'And you keep poor company, Warden girl.']],
    balanced: [['ryo', 'You sing like a car alarm.'], ['j6_kanzaki', 'Everybody\u2019s a critic.']]
  }, [['j6_kanzaki', 'Sit. No? Then I\u2019ll do the next verse on your face.']]);
  VO.vipWon = V3([['j6_kanzaki', 'Okay, okay! The mic\u2019s yours!']], {
    fierce: [['ryo', 'Where\u2019s Jin\u2019s money going tonight?']],
    strategic: [['aoi', 'The sheet under the bucket. Read it to us.']],
    balanced: [['ryo', 'Talk, and you can finish your song.']]
  }, [['j6_kanzaki', 'Hotel Chuo. Seventh floor. The Suits close a deal with the strip owners tonight. New rates, Jin\u2019s rates.'],
    ['aoi', 'Who signs for Jin?'], ['j6_kanzaki', 'Not me. I just count. Go bother the man on seven.']]);
  VO.duet = V3([['', '<p class="dim">The screen fades to a sunrise. The booth is very quiet.</p>']], {
    fierce: [['ryo', '\u2026You sing better than you fight. And you fight like a demon.'], ['aoi', 'That\u2019s two compliments. Careful, Kazan.']],
    strategic: [['aoi', 'You were half a beat behind the whole song.'], ['ryo', 'I was waiting for you.'], ['aoi', '\u2026Hm.']],
    balanced: [['aoi', 'That was\u2026 fun. Don\u2019t tell anyone.'], ['ryo', 'Who would I tell? Nails?']]
  }, [['aoi', 'Again sometime. When the strip is ours.']]);

  var K_CAST = { k: null, z: null, s: null };
  function popKara() {
    var k = room();
    if (k !== 'kara' && K_CAST.k) { kill(K_CAST.k); K_CAST.k = null; }
    if (k !== 'karaV') { ['z', 's'].forEach(function (q) { if (K_CAST[q]) { kill(K_CAST[q]); K_CAST[q] = null; } }); }
    if (k === 'kara' && (!K_CAST.k || !K_CAST.k.el || !K_CAST.k.el.parentNode)) { K_CAST.k = npc('j6_kaede', 280, 268, Math.PI / 2); try { waddle(K_CAST.k, 0, Math.PI / 2); } catch (e) {} }
    if (k === 'karaV' && vipLive()) {
      if (!K_CAST.z || !K_CAST.z.el || !K_CAST.z.el.parentNode) { K_CAST.z = npc('j6_kanzaki', 550, 440, Math.PI / 2); try { waddle(K_CAST.z, 0, Math.PI / 2); } catch (e) {} }
      if (!K_CAST.s || !K_CAST.s.el || !K_CAST.s.el.parentNode) { K_CAST.s = npc('j6_ksuit', 800, 560, Math.PI); }
    }
  }
  P6.K_CAST = K_CAST; P6.popKara = popKara;
  function vipLive() { return qOn() && stg() === 'ramen'; }
  function karaArrive() {
    var j = J();
    whenFree(function () { if (room() !== 'kara') return; lockIn(1); talk(!j.kIn ? VO.karaIn : VO.karaIn2, function () { j.kIn = 1; sv(); lockIn(0); }); });
  }
  function vipArrive() {
    if (!vipLive()) return;
    whenFree(function () {
      if (room() !== 'karaV' || !vipLive()) return;
      lockIn(1);
      var lines = pv(VO.vipIn);
      function go() { lockIn(0); startFight('karaV', ['c2_suit'], { bt: 'karaV', ctx: { toughHp: 44, flv: 7, j6nm: 'Kanzaki' } }); }
      try { if (typeof bossEnt === 'function' && K_CAST.z) { bossEnt('j6_kanzaki', lines, go, { spr: K_CAST.z }); return; } } catch (eB) { ev('world:s2p6:err:bent:' + (eB && eB.message)); }
      talk(lines, go);
    });
  }
  FIGHT.karaV = {
    win: function () {
      if (K_CAST.s) { kill(K_CAST.s); K_CAST.s = null; }
      lockIn(1);
      talk(pv(VO.vipWon), function () { lockIn(0); if (K_CAST.z) { kill(K_CAST.z); K_CAST.z = null; } setStg('kara'); qStep(2); sv(); P6.resetPaint('kara'); toastS('Journal: Hotel Chuo, seventh floor.'); });
    },
    lose: function () { }
  };
  /* singing: Booth 2 */
  function canPay() { return (SAVE.items | 0) >= KARA_PRICE; }
  function sing() {
    if (busy()) return true;
    var X = root.FFF_S2ARC; if (!X || !X.karaMenu) { toastS('The song pad is rebooting.'); return true; }
    var first = !J().kSung;
    try { if (W.ryo) { W.ryo.v = 0; W.path = []; } } catch (e) {}
    X.karaMenu({ price: KARA_PRICE, first: first, canPay: canPay,
      pay: function () { SAVE.items = Math.max(0, (SAVE.items | 0) - KARA_PRICE); try { save(); hud(); } catch (e) {} ev('world:s2p6:kara:pay:' + KARA_PRICE); },
      onEnd: function (res, again) { afterSong(res, first, again); } });
    return true;
  }
  function afterSong(res, first, again) {
    var j = J();
    try { if (root.AUDIO && root.AUDIO.music) { var D = INT[C2R[room()]]; root.AUDIO.music((D && D.mus) || 'c2night'); } } catch (eM) {}
    if (res && res.quit) { if (again) sing(); return; }
    if (first) {
      j.kSung = 1; sv();
      whenFree(function () { lockIn(1); talk(pv(VO.duet), function () { lockIn(0);
        var n = 5, g = null; try { g = STORY && STORY.bondGain && STORY.bond(SAVE).path ? STORY.bondGain(SAVE, n, 'banter') : null; } catch (eG) {}
        try { if (g && typeof bxpPop === 'function') bxpPop(n, g.up); } catch (eP) {}
        j.kBond = g ? n : 0; sv(); ev('world:s2p6:kara:duet:' + (g ? n : 0)); try { hud(); } catch (eH) {}
        if (again) later(300, sing); }); });
      return;
    }
    if (res && res.great) { setEdge(res.edge); }
    if (again) later(200, sing);
  }
  P6.sing = sing; P6.afterSong = afterSong;
  /* one-fight song edge: J().edge (quest state, so NG+ starts clean) (one at a time, a new one replaces the old; spent at the next real fight's bell) */
  var EDGE_N = { anthem: 'Anthem', ballad: 'Ballad', punk: 'Punk', duet: 'Duet' };
  function setEdge(k) { if (!EDGE_N[k]) return; var had = J().edge; J().edge = k; try { save(); } catch (e) {} ev('world:s2p6:edge:set:' + k + (had ? ':over:' + had : ''));
    var X = root.FFF_S2ARC, d = X && X.EDGE && X.EDGE[k] ? X.EDGE[k].d : ''; var m = EDGE_N[k] + ' edge ready: ' + d + (had && had !== k ? ' (replaces ' + EDGE_N[had] + ')' : ''); later(700, function () { whenFree(function () { toastS(m); }); }); }
  P6.setEdge = setEdge;
  function edgeOk(o) { var c = (o && o.ctx) || {}; if (!o || o.tut || c.c2spar || c.matspar || c.c2lesson || c.gkLoop || c.ckDoom) return false; try { if (typeof c2On === 'function' && !c2On()) return false; } catch (e) {} return true; }
  function hookMatch() {
    var UI = root.FFF_UI; if (!UI || typeof UI.startMatch !== 'function') return false; if (UI.startMatch._j6) return true;
    var sm0 = UI.startMatch;
    UI.startMatch = function (ch, o) {
      var k = J().edge, use = k && edgeOk(o);
      try {
        if (o && o.ctx && o.ctx.j6nm && o.foes) { o.foeNm = o.foeNm || {}; o.foes.forEach(function (id, i) { if (i === 0) o.foeNm[id] = o.ctx.j6nm; }); }
        if (use && o && o.pst) { if (k === 'anthem') o.pst.spirit = Math.min(40, (o.pst.spirit | 0) + 10); if (k === 'punk') o.pst.buff = (o.pst.buff | 0) + 3; }
      } catch (eP) {}
      var r = sm0.apply(this, arguments);
      if (use) {
        try { var b = UI.ST && UI.ST.b; if (b && b.s && b.s[0]) { if (k === 'ballad') b.s[0].guard = (b.s[0].guard | 0) + 4; if (k === 'duet') { b.s[0].buff = (b.s[0].buff | 0) + 2; if (b.bench) b.bench.buff = (b.bench.buff | 0) + 2; } } } catch (eB) {}
        J().edge = ''; try { save(); } catch (eS) {} ev('world:s2p6:edge:use:' + k);
        try { if (typeof toast === 'function') setTimeout(function () { toast('\u266a ' + EDGE_N[k] + ' edge!'); }, 900); } catch (eT) {}
      }
      return r;
    };
    UI.startMatch._j6 = 1; return true;
  }
  if (!hookMatch()) later(0, hookMatch);
  P6.hookMatch = hookMatch;

  ACT.j6_kara_desk = function () { if (busy()) return true; lockIn(1); talk(VO.karaIn2, function () { lockIn(0); }); return true; };
  ACT.j6_kara_b2 = function () { if (busy()) return true; enterRoom('karaB'); return true; };
  ACT.j6_kara_b3 = function () { if (busy()) return true; lockIn(1); talk(VO.b3, function () { lockIn(0); }); return true; };
  ACT.j6_kara_b4 = function () { if (busy()) return true; if (vipLive()) { enterRoom('karaV'); return true; } if (at('kara')) { enterRoom('karaV'); return true; } lockIn(1); talk(VO.b4Shut, function () { lockIn(0); }); return true; };
  ACT.j6_kara_sing = function () { return sing(); };
  ACT.j6_kara_vip = function () { if (busy()) return true; if (vipLive()) return true; lockIn(1); talk(VO.b4Empty, function () { lockIn(0); }); return true; };
  TALK.j6_kaede = function () { return ACT.j6_kara_desk(); };
  ARRIVE.kara = karaArrive; ARRIVE.karaV = vipArrive;
  POP.push(popKara);
  PIN.ramen = function () { return { room: 'town', x: TOWN_DOORS.kara.at[0], y: TOWN_DOORS.kara.at[1] - 60, lab: 'Karaoke', loc: 'High Score \u00b7 Karaoke Kitsune, booth 4' }; };

  /* ---------------- 3. Hotel Chuo (lobby, 7F) + the ¥40 hotel rest ---------------- */
  try {
    alias('j6_dealer', 'c2_suit', ((C2K && C2K.c2_suit) || 1.15) * 1.1, 'Ogata', 'c2suit');
    alias('j6_hsuit', 'c2_suit', (C2K && C2K.c2_suit) || 1.15, 'Syndicate Suit', 'c2suit');
    if (typeof CHAR_INTRO !== 'undefined' && !CHAR_INTRO.j6_dealer) CHAR_INTRO.j6_dealer = { kind: 'mgs', name: 'Ogata', sub: 'Syndicate Closer', tag: 'He signs the strip over to Jin.', who: 'c2suit', mood: 'calm' };
  } catch (eH) { ev('world:s2p6:err:alias3:' + (eH && eH.message)); }
  var REST_PRICE = P6.REST_PRICE = 40;
  roomDef('hchuo', 'Hotel Chuo \u00b7 \u30db\u30c6\u30eb\u4e2d\u592e', 'ck_surf', {
    block: [[556, 238, 800, 330], [160, 600, 380, 680], [900, 600, 1120, 680], [200, 700, 340, 740], [452, 270, 488, 304], [842, 270, 878, 304], [122, 770, 158, 804], [1122, 770, 1158, 804]],
    spots: [{ id: 'j6_h_panel', r: [110, 26, 440, 262], at: [275, 320], face: 3, lab: 'Rooms' },
      { id: 'j6_h_desk', r: [556, 238, 800, 330], at: [678, 380], face: 3, lab: 'Front' },
      { id: 'j6_h_lift', r: [996, 40, 1164, 236], at: [1080, 300], face: 3, lab: 'Lift' }] });
  roomDef('hhall', 'Hotel Chuo \u00b7 7F', 'ck_backroom', {
    block: [[300, 646, 420, 732], [820, 680, 1020, 720]],
    spots: [{ id: 'j6_h_707', r: [764, 40, 876, 226], at: [820, 290], face: 3, lab: '707' },
      { id: 'j6_h_door', r: [394, 40, 506, 226], at: [450, 290], face: 3, lab: '703' }] });
  P6.SURF.hchuo = 'stone'; P6.SURF.hhall = 'wood';
  AMB.hchuo = { top: 'rgba(255,120,210,.22)', bot: 'rgba(40,20,80,.30)', rain: 0, motes: 10, lamps: [[100, 120, '255,74,176', 70, 0.28, 'neon'], [290, 120, '74,200,255', 70, 0.24, 'neon']] };
  AMB.hhall = { top: 'rgba(200,120,255,.24)', bot: 'rgba(20,10,40,.34)', rain: 0, motes: 6, lamps: [[195, 120, '255,176,64', 60, 0.26, 'lamp']] };
  P6.PKEY.hhall = function () { return at('hotel') ? 'clear' : 'deal'; };
  P6.OPEN.hchuo = function () { return true; };
  P6.BT.hhall = { name: 'Hotel Chuo \u00b7 7F', lights: [[180, 100, '255,74,176', 90, 0.3, 'neon'], [540, 100, '74,200,255', 90, 0.3, 'neon']] };
  P6.BT.hdeal = { name: 'Hotel Chuo \u00b7 707', lights: [[200, 90, '255,200,110', 110, 0.32, 'lamp'], [520, 90, '255,176,64', 100, 0.28, 'lamp']], mood: 'room' };
  P6.innerBack.hhall = function () { lift('hchuo', [1080, 300, 0], '\u25bc 1F'); };

  VO.hIn = V3([['', '<p class="dim">Velvet, brass and slow purple light. A wall of glowing room photos. Nobody at the desk but a pair of hands behind frosted glass.</p>']], {
    fierce: [['ryo', 'Seventh floor. Let\u2019s go.']],
    strategic: [['aoi', 'A love hotel. No faces, no names. Good place to sign something.']],
    balanced: [['aoi', 'It\u2019s\u2026 nicer than I expected.'], ['ryo', 'Don\u2019t look at me like that.']]
  }, []);
  VO.hDesk = [['', '<p class="dim">A voice behind the glass: \u201cRest is \u00a5' + REST_PRICE + ', two hours. Stay is by the night. Key comes through the slot.\u201d</p>']];
  VO.hPanel = [['', '<p class="dim">Lit photos are free rooms. 301 is all sea blue. 503 has a pink bathtub shaped like a shell. 7F isn\u2019t on the board at all.</p>']];
  VO.hLift0 = [['', '<p class="dim">The lift needs a room key to go up. You have no reason to be upstairs.</p>']];
  VO.hDoor = [['', '<p class="dim">Do Not Disturb signs on every handle. Somebody is laughing behind 703.</p>']];
  VO.hHall = V3([['', '<p class="dim">Seventh floor. Neon strips along the carpet. Two Suits outside 707, the door open on a table of paper.</p>'],
    ['j6_hsuit', 'Wrong floor, kids. Take the stairs. All of them.']], {
    fierce: [['ryo', 'We came for the man inside.']],
    strategic: [['aoi', 'Two at the door, one at the table. Door first.']],
    balanced: [['ryo', 'Sorry. We\u2019re with room service.']]
  }, []);
  VO.hMid = V3([['j6_dealer', 'All that noise in my hallway. The strip owners are crying in there, you know. Crying and signing.']], {
    fierce: [['ryo', 'Not tonight.']],
    strategic: [['aoi', 'Ogata. The closer. Nobody signs without you watching.']],
    balanced: [['ryo', 'Let them go home.']]
  }, [['j6_dealer', 'Jin\u2019s rates are very fair. Let me explain them to your teeth.']]);
  VO.hWon = V3([['j6_dealer', '\u2026Fine. Fine! Take the paper.'], ['', '<p class="dim">The strip owners run past you for the lift. The deal sheets are still on the table, every one stamped with a red fox: Club Kitsune.</p>']], {
    fierce: [['ryo', 'Club Kitsune. Tetsu\u2019s place.']],
    strategic: [['aoi', 'The club pays the Suits, the Suits squeeze the strip. Someone above the club gets the cut.']],
    balanced: [['aoi', 'The club\u2019s stamp. So the money goes through the back office.']]
  }, [['j6_dealer', 'Go ask the club where the money goes. See who answers.']]);
  VO.hDone = [['', '<p class="dim">707 is empty. Somebody already changed the sheets.</p>']];

  var H_CAST = { a: null, b: null, o: null };
  function hallLive() { return qOn() && stg() === 'kara'; }
  function popHotel() {
    var k = room();
    if (k !== 'hhall') { ['a', 'b', 'o'].forEach(function (q) { if (H_CAST[q]) { kill(H_CAST[q]); H_CAST[q] = null; } }); return; }
    if (!hallLive()) return;
    function alive(s) { return s && s.el && s.el.parentNode; }
    if (!J().h1) { if (!alive(H_CAST.a)) H_CAST.a = npc('j6_hsuit', 730, 340, Math.PI); if (!alive(H_CAST.b)) H_CAST.b = npc('j6_hsuit', 920, 350, 0); }
    if (!alive(H_CAST.o)) { H_CAST.o = npc('j6_dealer', 820, 262, Math.PI / 2); try { waddle(H_CAST.o, 0, Math.PI / 2); } catch (e) {} }
  }
  P6.H_CAST = H_CAST; P6.popHotel = popHotel;
  function ding(up) { try { var X = root.FFF_S2ARC; var c = X && X.actx && X.actx(); if (c && X.tone) { var t = c.currentTime + 0.02; X.tone(up ? 784 : 659, t, 0.35, 'sine', 0.12); X.tone(up ? 1047 : 523, t + 0.18, 0.5, 'sine', 0.12); } } catch (e) {} }
  function lift(k, pos, lab) { if (busy()) return; ding(lab.indexOf('\u25b2') === 0); toastS(lab); enterRoom(k, pos); }
  P6.lift = lift;
  function hotelArrive() { var j = J(); if (j.hIn) return; whenFree(function () { if (room() !== 'hchuo') return; lockIn(1); talk(pv(VO.hIn), function () { j.hIn = 1; sv(); lockIn(0); }); }); }
  function hallArrive() {
    if (!hallLive()) return;
    whenFree(function () {
      if (room() !== 'hhall' || !hallLive()) return;
      if (!J().h1) { lockIn(1); talk(pv(VO.hHall), function () { startFight('hhall1', ['c2_suit', 'c2_suit'], { bt: 'hhall', ctx: { flv: 7 } }); }); return; }
      dealer();
    });
  }
  function dealer() {
    lockIn(1);
    var lines = pv(VO.hMid);
    function go() { lockIn(0); startFight('hhall2', ['c2_suit'], { bt: 'hdeal', ctx: { toughHp: 48, flv: 7, j6nm: 'Ogata' } }); }
    try { if (typeof bossEnt === 'function' && H_CAST.o) { bossEnt('j6_dealer', lines, go, { spr: H_CAST.o }); return; } } catch (eB) { ev('world:s2p6:err:bent3:' + (eB && eB.message)); }
    talk(lines, go);
  }
  FIGHT.hhall1 = {
    win: function () { J().h1 = 1; sv(); ['a', 'b'].forEach(function (q) { if (H_CAST[q]) { kill(H_CAST[q]); H_CAST[q] = null; } }); if (room() === 'hhall' && hallLive()) dealer(); },
    lose: function () { }
  };
  FIGHT.hhall2 = {
    win: function () { lockIn(1); talk(pv(VO.hWon), function () { lockIn(0); if (H_CAST.o) { kill(H_CAST.o); H_CAST.o = null; } setStg('hotel'); qStep(3); sv(); P6.resetPaint('hhall'); paintRoom(); toastS('Journal: Club Kitsune, the back office.'); }); },
    lose: function () { }
  };

  /* the hotel rest: full HP + SP for both, ¥40, once per stock cycle (restocks when a quest turns in) */
  function restS() { return c2Cyc(); }
  function restLeft() { var S0 = restS(); return S0.rest6 == null || (S0.rest6 | 0) !== (S0.cyc | 0); }
  P6.restLeft = restLeft;
  function restFull() { var o = (typeof other === 'function' && SAVE.act) ? other(SAVE.act) : null, pc = o && SAVE.chars ? SAVE.chars[o] : null;
    return (SAVE.hp | 0) >= MAXHP && (SAVE.sp | 0) >= SPMAX && (!pc || ((pc.sp == null || (pc.sp | 0) >= SPMAX) && (pc.hp == null || (pc.hp | 0) >= MAXHP))); }
  function hotelRest(where) {
    if (busy()) return true;
    var left = restLeft(), poor = (SAVE.items | 0) < REST_PRICE, full = restFull();
    var why = !left ? ' (booked up \u00b7 after your next job)' : full ? ' (you\u2019re rested)' : poor ? ' (need \u00a5' + REST_PRICE + ')' : '';
    var q = where === 'kh' ? 'Ms. Kanda slides a key across: \u201cA real bed, two hours. \u00a5' + REST_PRICE + '. Once a job, for you two.\u201d' : 'Through the slot: \u201cRest, two hours, \u00a5' + REST_PRICE + '. One room for the pair of you.\u201d';
    try { W.path = []; if (W.ryo) W.ryo.v = 0; } catch (e) {}
    dialog('<div class="tw"><p class="q">' + q + '</p><p class="dim">Full HP and SP for Ryo and Aoi.</p></div>',
      [['Rest \u00b7 \u00a5' + REST_PRICE + why, function () { doRest(where); }, 'hot', !left || full || poor], ['Later', null]]);
    return true;
  }
  function doRest(where) {
    if (!restLeft() || (SAVE.items | 0) < REST_PRICE) return;
    var S0 = restS(); S0.rest6 = S0.cyc | 0; SAVE.items = Math.max(0, (SAVE.items | 0) - REST_PRICE); try { save(); hud(); bumpItems(); } catch (e) {}
    ev('world:s2p6:rest:' + where + ':' + REST_PRICE);
    var h0 = SAVE.hp | 0;
    W.busy = true; W.path = []; var o = $('#wrest'), rs = 2.8;
    function fin() {
      SAVE.hp = MAXHP; SAVE.sp = SPMAX; try { var oc = other(SAVE.act); SAVE.chars = SAVE.chars || {}; var pc = SAVE.chars[oc] || (SAVE.chars[oc] = {}); pc.sp = SPMAX; if (pc.hp != null) pc.hp = MAXHP; } catch (eO) {}
      save(); try { hud(); } catch (e) {} W.busy = false; W.cool = Math.max(W.cool || 0, 2);
      try { AU.play('pl_heal'); } catch (e1) {} try { if (typeof vitFlo === 'function') vitFlo('hp', MAXHP - h0); } catch (e2) {}
      ev('world:s2p6:rest:done'); later(500, function () { toastS('Rested. HP and SP full for both.'); });
    }
    if (!o) { fin(); return; }
    o.style.setProperty('--rt', rs + 's'); o.className = 'on act'; var b = o.querySelector('b'); var b0 = b ? b.innerHTML : '';
    if (b) b.textContent = where === 'kh' ? 'Resting at the Kitsune Hotel\u2026' : 'Resting at Hotel Chuo\u2026';
    if (!o.querySelector('.j6moon')) o.insertAdjacentHTML('afterbegin', '<div class="j6moon c2cup" aria-hidden="true"><svg viewBox="0 0 120 90"><path d="M70 10a34 34 0 1 0 30 50a28 28 0 1 1-30-50z" fill="#ffe9a0" stroke="#14110d" stroke-width="4"/><text x="18" y="30" font-size="18" font-weight="900" fill="#c8a0f0">z</text><text x="30" y="16" font-size="13" font-weight="900" fill="#c8a0f0">z</text></svg></div>');
    try { AU.play('heal', { gain: 0.4 }); } catch (eA) {}
    var done = function () { o.className = ''; var m = o.querySelector('.j6moon'); if (m) m.remove(); if (b) b.innerHTML = b0; fin(); };
    if (typeof restFinishArm === 'function') restFinishArm(o, (root.FFF_REST_MS || rs * 1000), done); else later(root.FFF_REST_MS || rs * 1000, done);
  }
  P6.hotelRest = hotelRest; P6.doRest = doRest;
  /* GGD-51: Full Heal Tea is gone on every Chapter 2 route (restaurants already give full heals). Seeds/herbs and free story heals stay. restReach still means a ¥40 hotel rest is available. */
  function restReach() { try { if (!on()) return false; var NQ = root.FFF_NQ; if (NQ && typeof NQ.roomOpen === 'function' && NQ.roomOpen('hotel')) return true; return stripOpen(); } catch (e) { return false; } }
  root.FFF_TEA_OFF = function () { return true; }; P6.restReach = restReach;

  /* the Kitsune Hotel desk gets the same rest (all Chapter 2 runs; the herbalist's Full Heal Tea is gone) */
  try { var KH = INT[C2R.hotel] || INT.c2_nq_hotel; if (KH && KH.spots && !KH.spots.some(function (q) { return q.id === 'j6_rest_kh'; })) KH.spots.push({ id: 'j6_rest_kh', r: [740, 250, 840, 362], at: [790, 400], face: 0, lab: 'Rest \u00a5' + REST_PRICE }); } catch (eKH) { ev('world:s2p6:err:kh:' + (eKH && eKH.message)); }

  ACT.j6_rest_kh = function () { return hotelRest('kh'); };
  ACT.j6_h_desk = function () { if (busy()) return true; lockIn(1); talk(VO.hDesk, function () { lockIn(0); later(100, function () { hotelRest('hc'); }); }); return true; };
  ACT.j6_h_panel = function () { if (busy()) return true; lockIn(1); talk(VO.hPanel, function () { lockIn(0); }); return true; };
  ACT.j6_h_lift = function () { if (busy()) return true; if (at('kara')) { lift('hhall', [700, 700, 0], '\u25b2 7F'); return true; } lockIn(1); talk(VO.hLift0, function () { lockIn(0); }); return true; };
  ACT.j6_h_door = function () { if (busy()) return true; lockIn(1); talk(VO.hDoor, function () { lockIn(0); }); return true; };
  ACT.j6_h_707 = function () { if (busy()) return true; if (hallLive()) { hallArrive(); return true; } lockIn(1); talk(VO.hDone, function () { lockIn(0); }); return true; };
  ARRIVE.hchuo = hotelArrive; ARRIVE.hhall = hallArrive;
  POP.push(popHotel);
  PIN.kara = function () { if (room() === 'hchuo') return { room: 'hchuo', x: 1080, y: 250, lab: 'Lift', loc: 'High Score \u00b7 Hotel Chuo, 7F' }; return { room: 'town', x: TOWN_DOORS.hchuo.at[0], y: TOWN_DOORS.hchuo.at[1] - 60, lab: 'Hotel Chuo', loc: 'High Score \u00b7 Hotel Chuo, 7F' }; };

  /* ---------------- 4. Club Kitsune back office (own room; the base club chain is untouched) ---------------- */
  try { alias('j6_tetsu', 'chinpira1', (C2K && C2K.chinpira1) || 1.1, 'Punk Tetsu'); alias('j6_cdealer', 'ck_dealer', (C2K && C2K.ck_dealer) || 1.1, 'Club Dealer'); } catch (eC) { ev('world:s2p6:err:alias4:' + (eC && eC.message)); }
  TOWN_DOORS.ckoff = { r: [3196, 1500, 3256, 1584], at: [3226, 1626] }; TOWN_DOORS.ckoff.to = 'ckoff'; TOWN_DOORS.ckoff.out = [3226, 1636]; C2W.doors.j6_ckoff = TOWN_DOORS.ckoff;
  INT.c2_town.spots.push({ id: 'j6_e_ckoff', r: TOWN_DOORS.ckoff.r, at: TOWN_DOORS.ckoff.at, face: 3, lab: 'Staff door' }); TRANS.j6_e_ckoff = 1;
  roomDef('ckoff', 'Club Kitsune \u00b7 back office', 'ck_backroom', { w: 1000, h: 900, open: [[90, 230, 910, 850], [440, 850, 560, 900]],
    block: [[330, 300, 670, 380], [110, 250, 200, 420], [800, 250, 890, 360], [110, 640, 330, 720], [780, 660, 890, 760]],
    spots: [{ id: 'j6_ck_desk', r: [330, 300, 670, 380], at: [500, 440], face: 3, lab: 'Desk' },
      { id: 'j6_ck_tv', r: [560, 30, 900, 200], at: [730, 290], face: 3, lab: 'Screens' },
      { id: 'j6_ck_safe', r: [800, 250, 890, 360], at: [780, 420], face: 0, lab: 'Safe' }] });
  P6.SURF.ckoff = 'wood';
  AMB.ckoff = { top: 'rgba(200,90,255,.22)', bot: 'rgba(30,10,40,.34)', rain: 0, motes: 6, lamps: [[195, 160, '255,90,200', 60, 0.26, 'neon'], [195, 300, '255,200,120', 50, 0.24, 'lamp']] };
  P6.PKEY.ckoff = function () { return tetsuDone() ? 'beat' : 'tetsu'; };
  P6.OPEN.ckoff = function () { return at('hotel'); };
  P6.BT.ckoff = { name: 'Club Kitsune \u00b7 back office', lights: [[360, 110, '200,90,255', 100, 0.3, 'neon']] };
  function tetsuDone() { try { return !!J().tetsu || (typeof c2PunkDealt === 'function' && c2PunkDealt()); } catch (e) { return !!J().tetsu; } }
  P6.tetsuDone = tetsuDone;
  function clubLive() { return qOn() && stg() === 'hotel'; }
  VO.ckShut = [['', '<p class="dim">A steel door, \u201cSTAFF ONLY\u201d in fox-red. Locked. Nothing back here for you yet.</p>']];
  VO.ckIn = V3([['', '<p class="dim">The club\u2019s back office. Six screens of the dance floor. A cash counter still warm. Punk Tetsu at the desk, feet up.</p>'],
    ['j6_tetsu', 'Staff door means staff, kids.']], {
    fierce: [['ryo', 'Ogata\u2019s deal sheets. Your stamp. Explain.']],
    strategic: [['aoi', 'The hotel deal went through your books. We want the page after it.']],
    balanced: [['ryo', 'We came about the hotel.']]
  }, [['j6_tetsu', 'You want my ledger, you take it off me.']]);
  VO.ckBeatNow = V3([['j6_tetsu', '\u2026Okay! Okay. Ow.'], ['j6_tetsu', 'You think this is my club? I rent the fox. Every yen goes up the street.']], {
    fierce: [['ryo', 'To who?']],
    strategic: [['aoi', 'The ledger, Tetsu. Last page.']],
    balanced: [['ryo', 'Up the street to who?']]
  }, [['', '<p class="dim">The last page: \u201cJ. \u2014 Thursdays. Envelope via Tanuki.\u201d A Neon Game Center prize token is taped to it.</p>'],
    ['j6_tetsu', 'Jin. The Game Center. He keeps score on all of us.'], ['aoi', 'And Tanuki?'], ['j6_tetsu', 'Izakaya Tanuki. The old owner walks the envelope over. Ask him. Not me.']]);
  VO.ckBeatOld = V3([['', '<p class="dim">Punk Tetsu at the desk, an ice pack on the jaw you gave him.</p>'], ['j6_tetsu', 'You again. I\u2019m paid up with you. What now?']], {
    fierce: [['ryo', 'Hotel Chuo. The deal sheets carry your stamp.']],
    strategic: [['aoi', 'The Suits\u2019 deal at Hotel Chuo went through your books.']],
    balanced: [['ryo', 'Ogata says ask the club where the money goes.']]
  }, [['j6_tetsu', '\u2026Fine. Take the page. I never liked the guy.'], ['', '<p class="dim">The last page: \u201cJ. \u2014 Thursdays. Envelope via Tanuki.\u201d A Neon Game Center prize token is taped to it.</p>'],
    ['j6_tetsu', 'Jin. The Game Center. Izakaya Tanuki\u2019s owner walks the envelope over. Ask him.']]);
  VO.ckDone = [['j6_tetsu', 'Door\u2019s that way. Close it on your way out.']];
  VO.ckTv = [['', '<p class="dim">Six screens: the dance floor, the bar, the cage, the coat check, the alley, and one labelled GAME CENTER that shows only static.</p>']];
  VO.ckSafe = [['', '<p class="dim">The safe is open and empty. Thursday already happened.</p>']];
  var C_CAST = { t: null, d: null };
  function staffDoor(show) { var el = document.getElementById('j6ckdoor'); if (!show) { if (el && el.parentNode) el.parentNode.removeChild(el); return; } if (el) return;
    var m = document.getElementById('wimap') || document.getElementById('world'); if (!m) return; var c = document.createElement('canvas'); c.width = 64; c.height = 92; c.id = 'j6ckdoor'; c.className = 'nqprop';
    c.style.cssText = 'position:absolute;left:3194px;top:1494px;width:64px;height:92px;z-index:2;pointer-events:none';
    try { if (root.FFF_S2P && root.FFF_S2P.p6Door) root.FFF_S2P.p6Door(c.getContext('2d')); } catch (e) {} m.appendChild(c); }
  function popClub() {
    var k = room();
    try { staffDoor(k === 'town' && stripOpen() && at('hotel')); } catch (eD) {}
    if (k !== 'ckoff') { ['t', 'd'].forEach(function (q) { if (C_CAST[q]) { kill(C_CAST[q]); C_CAST[q] = null; } }); return; }
    if (!C_CAST.t || !C_CAST.t.el || !C_CAST.t.el.parentNode) { C_CAST.t = npc('j6_tetsu', 500, 270, Math.PI / 2); try { waddle(C_CAST.t, 0, Math.PI / 2); } catch (e) {} }
    if (clubLive() && !tetsuDone() && (!C_CAST.d || !C_CAST.d.el || !C_CAST.d.el.parentNode)) C_CAST.d = npc('j6_cdealer', 220, 520, 0);
  }
  P6.popClub = popClub; P6.C_CAST = C_CAST;
  function clubLink(kind) { lockIn(1); talk(pv(kind === 'now' ? VO.ckBeatNow : VO.ckBeatOld), function () { lockIn(0); J().ckLink = 1; setStg('club'); qStep(4); sv(); P6.resetPaint('ckoff'); paintRoom(); toastS('Journal: Izakaya Tanuki, on the strip.'); }); }
  function clubArrive() {
    if (!clubLive()) return;
    whenFree(function () {
      if (room() !== 'ckoff' || !clubLive()) return;
      if (tetsuDone()) { clubLink('old'); return; }
      lockIn(1);
      talk(pv(VO.ckIn), function () { startFight('ckoff', ['chinpira1'], { bt: 'ckoff', ctx: { flv: 7, j6nm: 'Punk Tetsu', joinIn: { id: 'ck_dealer', round: 3, nm: 'Club Dealer', line: 'A Club Dealer joins Punk on round 3.' } } }); });
    });
  }
  FIGHT.ckoff = {
    win: function () { J().tetsu = 1; sv(); if (C_CAST.d) { kill(C_CAST.d); C_CAST.d = null; } P6.resetPaint('ckoff'); paintRoom(); clubLink('now'); },
    lose: function () { }
  };
  ACT.j6_ck_desk = function () { if (busy()) return true; if (clubLive()) { clubArrive(); return true; } lockIn(1); talk(VO.ckDone, function () { lockIn(0); }); return true; };
  ACT.j6_ck_tv = function () { if (busy()) return true; lockIn(1); talk(VO.ckTv, function () { lockIn(0); }); return true; };
  ACT.j6_ck_safe = function () { if (busy()) return true; lockIn(1); talk(VO.ckSafe, function () { lockIn(0); }); return true; };
  TALK.j6_tetsu = function () { return ACT.j6_ck_desk(); };
  ARRIVE.ckoff = clubArrive; POP.push(popClub);
  PIN.hotel = function () { return { room: 'town', x: TOWN_DOORS.ckoff.at[0], y: TOWN_DOORS.ckoff.at[1] - 60, lab: 'Staff door', loc: 'High Score \u00b7 Club Kitsune, back office' }; };

  /* ---------------- 5. Izakaya Tanuki ---------------- */
  try { alias('j6_ponta', 'npc_attendant', 1.08, 'Ponta (owner)'); } catch (eI) { ev('world:s2p6:err:alias5:' + (eI && eI.message)); }
  var IZAK_ITEMS = [
    { id: 'yakitori', n: 'Yakitori', jp: '\u713c\u304d\u9ce5', icon: 'i_yakitori', hp: 10, base: 6, cost: 6, eat: 'yakitori', eff: '+10 HP  \u00b7  at the counter', flavor: 'Two skewers off the grill, tare glaze, a pinch of shichimi.' },
    { id: 'karaage', n: 'Karaage', jp: '\u5510\u63da\u3052', icon: 'i_karaage', hp: 14, base: 8, cost: 8, eat: 'karaage', eff: '+14 HP  \u00b7  at the counter', flavor: 'Ginger-soy chicken, fried twice. Lemon on the side.' },
    { id: 'edamame', n: 'Edamame', jp: '\u679d\u8c46', icon: 'i_edamame', hp: 6, base: 3, cost: 3, eat: 'edamame', eff: '+6 HP  \u00b7  at the counter', flavor: 'Salted pods, still warm. Everyone orders these.' },
    { id: 'onigiri', n: 'Onigiri', jp: '\u304a\u306b\u304e\u308a', icon: 'i_onigiri', hp: 12, base: 5, cost: 5, eat: 'onigiri', eff: '+12 HP  \u00b7  at the counter', flavor: 'Grilled rice ball, miso brushed, nori wrap.' }
  ];
  P6.IZAK_ITEMS = IZAK_ITEMS;
  (function regIz() { var M = menus(); if (!M || !M.SHOPS) { later(0, regIz); return; }
    M.SHOPS.j6_izak = { id: 'j6_izak', theme: 'izak', n: 'Izakaya Tanuki', jp: '\u5c45\u9152\u5c4b \u305f\u306c\u304d', who: 'j6_ponta', leave: '\u3054\u3061\u305d\u3046\u3055\u307e  \u00b7  Done',
      hi: { fierce: 'Sit at the counter. Elbows in.', strategic: 'Small plates, small prices. Grill\u2019s hot.', balanced: 'Irasshai! Counter seats only tonight.' },
      nails: function () { return false; }, items: function () { return IZAK_ITEMS; } }; })();
  roomDef('izak', 'Izakaya Tanuki \u00b7 \u5c45\u9152\u5c4b\u305f\u306c\u304d', 'c2night', {
    block: [[190, 250, 1090, 362], [110, 600, 300, 690], [980, 600, 1170, 690], [520, 640, 760, 720], [140, 770, 200, 830]],
    spots: [{ id: 'j6_izak_order', r: [560, 250, 720, 362], at: [640, 430], face: 3, lab: 'Order' },
      { id: 'j6_izak_tags', r: [880, 30, 1180, 200], at: [1000, 420], face: 3, lab: 'Menu' },
      { id: 'j6_izak_tanuki', r: [140, 770, 200, 830], at: [240, 800], face: 1, lab: 'Look' }] });
  P6.SURF.izak = 'wood';
  AMB.izak = { top: 'rgba(255,150,90,.28)', bot: 'rgba(60,24,20,.30)', rain: 0, motes: 8, steamN: 2, lamps: [[120, 120, '255,90,60', 60, 0.32, 'lantern'], [280, 120, '255,90,60', 60, 0.32, 'lantern']] };
  P6.OPEN.izak = function () { return true; };
  VO.izIn = [['j6_ponta', 'Irasshai! Counter only. The tables are for my regulars and my regulars are dead.']];
  VO.izIn2 = [['j6_ponta', 'Irasshai. Grill\u2019s hot.']];
  VO.izTip = V3([['j6_ponta', '\u2026You\u2019re the two from the hotel. The whole strip heard.']], {
    fierce: [['ryo', 'The envelope. You walk it to Jin.'], ['j6_ponta', 'Every Thursday. Since my wife passed and he paid the funeral.']],
    strategic: [['aoi', 'Thursdays, via Tanuki. Tetsu\u2019s ledger says you carry the money.'], ['j6_ponta', 'I carry it. I don\u2019t count it.']],
    balanced: [['aoi', 'We\u2019re not here to hurt you.'], ['j6_ponta', 'I know. That\u2019s why I\u2019m going to tell you.']]
  }, [['j6_ponta', 'Jin plays the floor every night, top of the shooter board. His real room is past the staff door at the back. The prize room.'],
    ['j6_ponta', 'Tell him the old tanuki says the funeral\u2019s paid off.']]);
  VO.izTags = [['', '<p class="dim">Paper tags on the wall: \u713c\u304d\u9ce5 \u00a56, \u5510\u63da\u3052 \u00a58, \u679d\u8c46 \u00a53, \u304a\u306b\u304e\u308a \u00a55. One old tag, crossed out: \u300c\u30c4\u30b1\u300d (on credit).</p>']];
  VO.izTanuki = [['', '<p class="dim">A clay tanuki in a straw hat holds a sake flask and an IOU. Someone rubbed its belly shiny.</p>']];
  var I_CAST = { p: null };
  function popIzak() { var k = room(); if (k !== 'izak') { if (I_CAST.p) { kill(I_CAST.p); I_CAST.p = null; } return; }
    if (!I_CAST.p || !I_CAST.p.el || !I_CAST.p.el.parentNode) { I_CAST.p = npc('j6_ponta', 640, 214, Math.PI / 2); try { waddle(I_CAST.p, 0, Math.PI / 2); } catch (e) {} } }
  P6.popIzak = popIzak; P6.I_CAST = I_CAST;
  function izTipLive() { return qOn() && stg() === 'club'; }
  function izArrive() { var j = J(); whenFree(function () { if (room() !== 'izak') return; lockIn(1); talk(!j.izIn ? VO.izIn : VO.izIn2, function () { j.izIn = 1; sv(); lockIn(0); }); }); }
  function izTip() { if (room() !== 'izak' || !izTipLive()) return; lockIn(1); talk(pv(VO.izTip), function () { lockIn(0); setStg('izak'); qStep(5); sv(); toastS('Journal: Neon Game Center. Find Jin on the floor.'); }); }
  function izOrder() { if (busy()) return true; if (izTipLive()) { P6._ate = 0; P6.afterMeal(izTip); } openShop('j6_izak'); return true; }
  P6.izOrder = izOrder; P6.izTip = izTip;
  ACT.j6_izak_order = function () { return izOrder(); };
  ACT.j6_izak_tags = function () { if (busy()) return true; lockIn(1); talk(VO.izTags, function () { lockIn(0); }); return true; };
  ACT.j6_izak_tanuki = function () { if (busy()) return true; lockIn(1); talk(VO.izTanuki, function () { lockIn(0); }); return true; };
  TALK.j6_ponta = function () { return izOrder(); };
  ARRIVE.izak = izArrive; POP.push(popIzak);
  PIN.club = function () { return { room: 'town', x: TOWN_DOORS.izak.at[0], y: TOWN_DOORS.izak.at[1] - 60, lab: 'Izakaya', loc: 'High Score \u00b7 Izakaya Tanuki' }; };

  /* ---------------- 6. Neon Game Center (floor + Jin's prize room). On the strip run the base landmark door lm_game opens these. ---------------- */
  try { alias('j6_jin', 'mb2_game', (C2K && C2K.mb2_game) || 1.12, '\u201cHigh-Score\u201d Jin', 'jin'); alias('j6_prize', 'npc_clerk', 1.02, 'Prize Clerk'); alias('j6_gamer', 'npc_courier', 1.0, 'Regular'); } catch (eG) { ev('world:s2p6:err:alias6:' + (eG && eG.message)); }
  var GC_DOOR = (C2W.doors && C2W.doors.gamectr) || { r: [3624, 1500, 3736, 1580], at: [3680, 1630] };
  TOWN_DOORS.gc = { r: GC_DOOR.r, at: GC_DOOR.at, to: 'gc', out: [GC_DOOR.at[0], GC_DOOR.at[1] + 10] };
  var CAB_X = { shooter: 170, fighter: 330, ember: 490, gun: 650, street: 810 }, PLAY_PRICE = P6.PLAY_PRICE = 1;
  var gcSpots = Object.keys(CAB_X).map(function (k) { return { id: 'j6_cab_' + k, r: [CAB_X[k] - 50, 40, CAB_X[k] + 50, 180], at: [CAB_X[k], 290], face: 3, lab: 'Play' }; });
  roomDef('gc', 'Neon Game Center \u00b7 \u30b2\u30fc\u30e0\u30bb\u30f3\u30bf\u30fc', 'ck_surf', {
    block: [[110, 40, 900, 230], [960, 300, 1180, 460], [110, 560, 340, 700], [500, 560, 620, 730], [660, 560, 780, 730], [960, 600, 1180, 760]],
    spots: gcSpots.concat([{ id: 'j6_gc_prize', r: [110, 560, 340, 700], at: [225, 750], face: 0, lab: 'Prizes' },
      { id: 'j6_gc_crane', r: [500, 560, 780, 730], at: [640, 790], face: 0, lab: 'Crane' },
      { id: 'j6_gc_medal', r: [960, 600, 1180, 760], at: [920, 680], face: 2, lab: 'Medals' },
      { id: 'j6_gc_board', r: [960, 300, 1180, 460], at: [1070, 520], face: 0, lab: 'Scores' },
      { id: 'j6_gc_staff', r: [1060, 40, 1180, 230], at: [1120, 290], face: 3, lab: 'Staff door' }]) });
  roomDef('gcback', 'Neon Game Center \u00b7 prize room', 'ck_backroom', { w: 1000, h: 900, open: [[90, 230, 910, 850], [440, 850, 560, 900]],
    block: [[360, 40, 640, 200], [120, 600, 330, 690], [700, 300, 880, 420]],
    spots: [{ id: 'j6_gc_seal', r: [420, 40, 580, 200], at: [500, 300], face: 3, lab: 'Lock' }, { id: 'j6_gc_jincab', r: [700, 300, 880, 420], at: [790, 470], face: 3, lab: 'Look' }] });
  P6.SURF.gc = 'concrete'; P6.SURF.gcback = 'wood';
  AMB.gc = { top: 'rgba(120,200,255,.22)', bot: 'rgba(60,10,80,.30)', rain: 0, motes: 12, lamps: [[100, 100, '255,90,200', 70, 0.3, 'neon'], [290, 100, '90,216,255', 70, 0.3, 'neon']] };
  AMB.gcback = { top: 'rgba(255,200,90,.22)', bot: 'rgba(30,10,40,.34)', rain: 0, motes: 6, lamps: [[195, 120, '255,200,90', 70, 0.3, 'lamp']] };
  P6.PKEY.gc = function () { return (stg() === 'izak' ? 'jin' : 'x') + (J().arc && J().arc.g ? Object.keys(J().arc.g).length : 0); };
  P6.PKEY.gcback = function () { return E().seal_game ? 'open' : 'lock'; };
  P6.OPEN.gc = function () { return true; };
  P6.BT.gcback = { name: 'Neon Game Center \u00b7 prize room', lights: [[360, 110, '255,200,90', 100, 0.3, 'lamp']] };
  P6.innerBack.gcback = function () { enterRoom('gc', [1120, 300, 0]); };
  P6.innerDoor = P6.innerDoor || {}; P6.innerDoor.gc = TOWN_DOORS.gc;
  /* J().arc v2 (v6564-arcade): best/tier/g/tok/spent as before, + paid (tokens paid from best scores), rep (repeat-run tokens),
     hs (your board entries), ini (last initials). v1 saves migrate: Neon Ring Flight (rings) became Chuo Crisis (gun); every game was
     rebuilt on a new score scale, so old bests move to old{} while medals (tier, g) and tokens already earned stay. */
  function A6() { var j = J(); if (!j.arc || typeof j.arc !== 'object') j.arc = {}; var a = j.arc; a.best = a.best || {}; a.tier = a.tier || {}; a.g = a.g || {}; a.tok = a.tok | 0; a.spent = a.spent | 0;
    if ((a.v | 0) < 2) { var ob = a.best; a.old = a.old || {}; Object.keys(ob).forEach(function (k) { a.old[k] = ob[k]; });
      if (a.tier.rings != null) { a.tier.gun = Math.max(a.tier.gun | 0, a.tier.rings | 0); delete a.tier.rings; } if (a.g.rings) { a.g.gun = 1; delete a.g.rings; }
      a.paid = {}; Object.keys(a.tier).forEach(function (k) { a.paid[k] = [0, 1, 3, 6][a.tier[k] | 0] | 0; });
      a.best = {}; a.rep = {}; a.hs = {}; a.v = 2; }
    a.paid = a.paid || {}; a.rep = a.rep || {}; a.hs = a.hs || {}; return a; }
  P6.A6 = A6;
  function cab(id) {
    if (busy()) return true; var X = root.FFF_S2ARC; if (!X || !X.cabPlay || !X.GAMES || !X.GAMES[id]) { toastS('The cabinet is booting.'); return true; }
    if ((SAVE.items | 0) < PLAY_PRICE) { lockIn(1); talk([['', '<p class="dim">\u00a51 a play. Your pockets are empty.</p>']], function () { lockIn(0); }); return true; }
    try { if (W.ryo) { W.ryo.v = 0; W.path = []; } } catch (e) {}
    SAVE.items = Math.max(0, (SAVE.items | 0) - PLAY_PRICE); try { save(); hud(); } catch (e) {} ev('world:s2p6:cab:pay:' + id);
    var a = A6();
    X.cabPlay(id, { onEnd: function (res) { return cabEnd(res); }, canAgain: function () { return (SAVE.items | 0) >= PLAY_PRICE; },
      canPay: function () { return (SAVE.items | 0) >= PLAY_PRICE; }, payCont: function () { SAVE.items = Math.max(0, (SAVE.items | 0) - PLAY_PRICE); try { save(); hud(); } catch (e2) {} ev('world:s2p6:cab:cont:' + id); },
      hs: (a.hs[id] || []).slice(), ini: a.ini || 'RYO',
      onClose: function (res, again) { try { if (root.AUDIO && root.AUDIO.music) root.AUDIO.music('ck_surf'); } catch (eM) {} P6.resetPaint('gc'); paintRoom(); if (again) later(150, function () { cab(id); }); } });
    return true;
  }
  /* tokens scale with your best score (FFF_S2ARC.tokOf: medal floor 1/3/6, then +1 per 20% of gold past gold, max 10 a cabinet),
     paid once as the best climbs. A run at silver or better that doesn't beat your best pays 1 token, 5 times a cabinet. */
  function cabEnd(res) {
    var a = A6(), X = root.FFF_S2ARC, id = res.id, prevT = a.tier[id] | 0, tok = 0, note = '';
    if (!res.quit) {
      var ob = a.best[id] | 0; a.best[id] = Math.max(ob, res.score | 0);
      var due = (X.tokOf ? X.tokOf(id, a.best[id]) : 0) - (a.paid[id] | 0);
      if (due > 0) { tok += due; a.paid[id] = (a.paid[id] | 0) + due; note = a.best[id] > ob ? 'New best' : ''; }
      else if (res.tier >= 2 && (a.rep[id] | 0) < (X.TOK_REPEAT_MAX || 5)) { tok += 1; a.rep[id] = (a.rep[id] | 0) + 1; note = 'Repeat run'; }
      else note = (a.rep[id] | 0) >= (X.TOK_REPEAT_MAX || 5) ? 'Beat your best for more' : '';
      var bt = X.tierOf(id, a.best[id]); if (bt > prevT) a.tier[id] = bt; if ((a.tier[id] | 0) >= 3) a.g[id] = 1;
      if (res.ini) a.ini = String(res.ini).slice(0, 3);
      if (res.entry) { var L = a.hs[id] || []; L.push({ n: res.entry.n, s: res.entry.s | 0 }); L.sort(function (p, q) { return q.s - p.s; }); a.hs[id] = L.slice(0, 10); }
      a.tok += tok; sv(); }
    ev('world:s2p6:cab:end:' + id + ':' + res.score + ':' + res.tier + ':+' + tok);
    return { best: a.best[id] | 0, tokens: tok, note: note, medal: a.tier[id] | 0 };
  }
  P6.cab = cab; P6.cabEnd = cabEnd;
  Object.keys(CAB_X).forEach(function (k) { ACT['j6_cab_' + k] = function () { return cab(k); }; });
  /* the prize counter: tokens for cosmetics only. The run's gang uniform lives here now (the Punks' yankii set on a Nails run). */
  var UNI = { arc: [['of_yankii', 'yankii', 8], ['of_yankiis', 'yankiis', 6], ['of_yankiil', 'yankiil', 8]], neo: [['of_suit', 'suit', 8]], bat: [['of_hoodie', 'hoodie', 8]], dep: [['of_rider', 'rider', 8]] };
  P6.UNI = UNI;
  function ofName(k) { try { return (typeof OF_N !== 'undefined' && OF_N[k]) || k; } catch (e) { return k; } }
  function ownedOf(k) { try { return typeof ofOwned === 'function' && ofOwned(k); } catch (e) { return false; } }
  function prize() {
    if (busy()) return true;
    var a = A6(), fac = E().run_fac, L = UNI[fac] || [], have = a.tok - a.spent;
    var rows = L.map(function (u) { var own = ownedOf(u[1]), need = u[1] !== 'yankii' && !ownedOf('yankii') && fac === 'arc';
      var why = own ? ' (yours)' : need ? ' (needs the tokk\u014dfuku)' : have < u[2] ? ' (' + u[2] + ' tokens)' : '';
      return [ofName(u[1]) + ' \u00b7 ' + u[2] + ' \u25ce' + why, function () { buyUni(u); }, 'hot', own || need || have < u[2]]; });
    rows.push(['Later', null]);
    var G = Object.keys(a.g).length;
    try { W.path = []; if (W.ryo) W.ryo.v = 0; } catch (e) {}
    dialog('<b>Prize Counter</b><p class="q">\u201cTokens only. No yen, no cards, no favours. Looks, that\u2019s all we stock.\u201d</p><p class="dim">Tokens: ' + have + ' \u25ce  \u00b7  Mastered ' + G + ' / 5</p>', rows, 'npc_clerk_fig');
    return true;
  }
  function buyUni(u) { var a = A6(); if (a.tok - a.spent < u[2] || ownedOf(u[1])) return; a.spent += u[2];
    try { var g = gearS(); g.of = g.of || {}; g.of[u[1]] = 1; g.ofNew = g.ofNew || {}; g.ofNew[u[1]] = 1; } catch (e) {}
    sv(); ev('world:s2p6:prize:' + u[1] + ':' + u[2]); try { AU.play('place'); } catch (eA) {} later(300, function () { toastS(ofName(u[1]) + ' \u2014 wear it in Menu \u203a Player \u203a Gear \u203a Outfit.'); }); }
  P6.prize = prize; P6.buyUni = buyUni;
  /* the yankii set leaves the West Street stall on runs where the prize counter exists */
  (function moveYk() { var M = typeof SHOPS !== 'undefined' ? SHOPS : null; var Y = M && M.yk_west; if (!Y || Y._j6) return; Y._j6 = 1;
    Y.items.forEach(function (it) { var u0 = it.unlock, w0 = it.why || ''; it.unlock = function () { if (stripOpen()) return false; return u0 ? u0.apply(this, arguments) : true; };
      Object.defineProperty(it, 'why', { configurable: true, enumerable: true, get: function () { return stripOpen() ? 'At the Game Center prize counter now' : w0; } }); });
  })();
  VO.gcIn = [['', '<p class="dim">Wall-to-wall neon. Five cabinets humming, a crane full of fox plush, a medal pusher spilling tin.</p>']];
  VO.gcJin = V3([['', '<p class="dim">At the Kitsune Blaster cabinet, a lean man in a gold-trim jacket plays without looking at the screen. The board above reads JIN, JIN, JIN.</p>'],
    ['j6_jin', 'Don\u2019t touch another player\u2019s session.'], ['j6_jin', 'You\u2019re the two who cost me a ramen shop, a karaoke booth, a hotel floor and a club. Nice run.']], {
    fierce: [['ryo', 'Game over, Jin.'], ['j6_jin', 'Game over is when I say. Insert coin.']],
    strategic: [['aoi', 'The strip pays you every Thursday. That ends tonight.'], ['j6_jin', 'Everything ends. High scores don\u2019t.']],
    balanced: [['ryo', 'The old man at Tanuki says the funeral\u2019s paid off.'], ['j6_jin', '\u2026Ponta talks too much. Fine.']]
  }, [['j6_jin', 'Staff door. My room. Bring your best run.']]);
  VO.gcStaff0 = [['', '<p class="dim">STAFF ONLY. A keypad with the buttons worn on 1-U-P.</p>']];
  VO.gcBack = V3([['', '<p class="dim">The prize room. Glass cases of things nobody ever won. A gold cabinet with one name on its board. A lock on the prize safe, sealed in gray.</p>'],
    ['j6_jin', 'Two players. One credit. Let\u2019s see your score.']], {
    fierce: [['ryo', 'I don\u2019t play. I win.']],
    strategic: [['aoi', 'He reads patterns. Don\u2019t give him one, Ryo.']],
    balanced: [['ryo', 'One credit\u2019s all we need.']]
  }, []);
  VO.gcWon = V3([['j6_jin', '\u2026Ha. New high score.'], ['j6_jin', 'Take the seal. The strip\u2019s yours to keep. Try not to lose your initials.']], {
    fierce: [['ryo', 'Leave the shops alone. All of them.']],
    strategic: [['aoi', 'And the Thursday envelopes stop.']],
    balanced: [['ryo', 'Pay Ponta back while you\u2019re at it.']]
  }, []);
  VO.crane = [['', '<p class="dim">Fox plush, three to a stack. The claw is set to \u201cweak\u201d. Everyone knows. Nobody stops.</p>']];
  VO.medal = [['', '<p class="dim">The medal pusher shoves a wall of tin to the edge and never over. Jin\u2019s favourite machine, says the sticker.</p>']];
  VO.jinCab = [['', '<p class="dim">The gold cabinet: one game, one name. 999,990 points. The 10 he didn\u2019t get bothers him, you can tell.</p>']];
  VO.sealDone = [['', '<p class="dim">The prize safe stands open. Plush foxes and old IOUs.</p>']];
  var G_CAST = { j: null, p: null, r: null, jb: null };
  function popGc() {
    var k = room();
    if (k !== 'gc') { ['j', 'p', 'r'].forEach(function (q) { if (G_CAST[q]) { kill(G_CAST[q]); G_CAST[q] = null; } }); }
    if (k !== 'gcback' && G_CAST.jb) { kill(G_CAST.jb); G_CAST.jb = null; }
    if (k === 'gcback' && !(qOn() && (stg() === 'met' || stg() === 'won' || (E().jinFate === 'help' && E().seal_game)))) { if (G_CAST.jb) { kill(G_CAST.jb); G_CAST.jb = null; } if (E().jinFate !== 'wipe') sweepJin(); }
    function alive(s) { return s && s.el && s.el.parentNode; }
    if (k === 'gc') {
      if (!alive(G_CAST.p)) { G_CAST.p = npc('j6_prize', 225, 540, Math.PI / 2); }
      if (!alive(G_CAST.r)) G_CAST.r = npc('j6_gamer', 650, 300, -Math.PI / 2);
      if (qOn() && stg() === 'izak' && !alive(G_CAST.j)) { G_CAST.j = npc('j6_jin', 170, 300, -Math.PI / 2); }
      if (!(qOn() && stg() === 'izak') && G_CAST.j) { kill(G_CAST.j); G_CAST.j = null; }
    }
    if (k === 'gcback' && qOn() && !alive(G_CAST.jb) && E().jinFate !== 'wipe' && (stg() === 'met' || (stg() === 'won' && !E().seal_game) || (E().jinFate === 'help' && E().seal_game))) { G_CAST.jb = npc('j6_jin', 500, 420, Math.PI / 2); try { waddle(G_CAST.jb, 0, Math.PI / 2); } catch (e) {} }
  }
  function sweepJin() { try { [].forEach.call(document.querySelectorAll('[data-npc="j6_jin"]'), function (el) { if (!G_CAST.j || el !== G_CAST.j.el) el.remove(); }); } catch (e) {} }
  P6.popGc = popGc; P6.G_CAST = G_CAST;
  function gcArrive() { var j = J(); whenFree(function () { if (room() !== 'gc') return;
    if (qOn() && stg() === 'izak') { lockIn(1); talk(pv(VO.gcJin), function () { lockIn(0); if (G_CAST.j) { kill(G_CAST.j); G_CAST.j = null; } setStg('met'); qStep(6); sv(); toastS('Journal: Jin\u2019s prize room, past the staff door.'); }); return; }
    if (!j.gcIn) { lockIn(1); talk(VO.gcIn, function () { j.gcIn = 1; sv(); lockIn(0); }); } }); }
  function gcBackArrive() { if (!(qOn() && stg() === 'met')) return; whenFree(function () { if (room() !== 'gcback' || stg() !== 'met') return; lockIn(1);
    var lines = pv(VO.gcBack); function go() { lockIn(0); startFight('gcback', ['mb2_game'], { bt: 'gcback', ctx: { flv: 8, mini: 'mb2_game', j6nm: '\u201cHigh-Score\u201d Jin' } }); }
    try { if (typeof bossEnt === 'function' && G_CAST.jb) { bossEnt('mb2_game', lines, go, { spr: G_CAST.jb }); return; } } catch (eB) { ev('world:s2p6:err:bent6:' + (eB && eB.message)); }
    talk(lines, go); }); }
  FIGHT.gcback = { win: function () { setStg('won'); qStep(7); sv(); lockIn(1); talk(pv(VO.gcWon), function () { lockIn(0); toastS('Journal: take Jin\u2019s seal off the prize safe.'); }); }, lose: function () { } };
  /* ---------------- M3: Jin at the prize safe (add-only; karaoke duet unchanged) ---------------- */
  if (typeof BOND_Q === 'object' && typeof BOND_TXT === 'object' && typeof BOND_MID === 'object') {
    BOND_Q.c2_jin_after = { q: '<b>Aoi asks</b><p>He is still at the board. The seal is on the prize safe. What do we do with him?</p>',
      o: { fierce: ['Wipe his name off the board', 'Fierce'], strategic: ['Deal for the Thursday book', 'Strategic'], balanced: ['Help him up. The board can stay his', 'Compassionate'] } };
    BOND_MID.c2_jin_after = 'strategic';
    BOND_TXT.c2_jin_after = { _mx: 1, _noReact: 1,
      fierce: {
        fierce: [['{LEAD}', '{shout}Wipe it. His name comes off.{/shout}', { hype: 1 }], ['{PARTNER}', 'You always go for the board first.'], ['{LEAD}', 'The strip already paid for that score.'], ['{PARTNER}', 'I will stand with you. I am not going to like the sound it makes.']],
        strategic: [['{LEAD}', '{brisk}Wait. The book first. Then the seal.{/brisk}'], ['{PARTNER}', 'A deal, from you, in his prize room.'], ['{LEAD}', 'His envelopes are worth more than his initials.'], ['{PARTNER}', 'Then keep him talking. I will watch the safe.']],
        balanced: [['{LEAD}', 'Up. The board can stay his. We came for the seal.'], ['{PARTNER}', '{quiet}You would let him keep the high score.{/quiet}'], ['{LEAD}', 'I would let him keep breathing. The seal is enough.'], ['{PARTNER}', 'Then I stay close. If he reaches for the safe, I am there.']] },
      strategic: {
        fierce: [['{LEAD}', 'No book. Wipe the name. We are done talking.'], ['{PARTNER}', 'We had a cleaner read than that.'], ['{LEAD}', 'His name on that glass is the read.'], ['{PARTNER}', 'Then I cover the safe while you do it. We still leave together.']],
        strategic: [['{LEAD}', '{brisk}Sit. Your score can stay. We want the Thursday book.{/brisk}'], ['{PARTNER}', 'The envelopes, the drops, who collects.'], ['{LEAD}', 'He names them, we take the seal, nobody else gets squeezed.'], ['{PARTNER}', 'I will take the book. You take the safe. Same plan.']],
        balanced: [['{LEAD}', 'Help him stand. Keep the board. We still need the book.'], ['{PARTNER}', 'Mercy and the ledger. I can run both.'], ['{LEAD}', 'He talks easier if he is on his feet.'], ['{PARTNER}', 'Then I get the names. You get him standing.']] },
      balanced: {
        fierce: [['{LEAD}', 'I am sorry. The name comes off.'], ['{PARTNER}', '{quiet}You do not have to sound sorry while you do it.{/quiet}'], ['{LEAD}', 'I will not hit him twice. The board is enough.'], ['{PARTNER}', 'I will watch him. You watch the glass.']],
        strategic: [['{LEAD}', 'Hear us out. The book for your board.'], ['{PARTNER}', 'Let him keep the initials if the envelopes stop.'], ['{LEAD}', 'That is the deal. He can still be first on the glass.'], ['{PARTNER}', 'I will hold the safe. You hold the offer.']],
        balanced: [['{LEAD}', '{slow}Come on. Up.{/slow} The board stays yours. We only came for the seal.'], ['{PARTNER}', 'After everything he did to this street.'], ['{LEAD}', 'I stand in front of him anyway. That is the point.'], ['{PARTNER}', '{quiet}I still think he has not earned it.{/quiet} I will help you lift him.']] } };
  }
  if (typeof BANTER === 'object') {
    BANTER.c2_jin_after = {
      fierce: [
        ['aoi', 'He is already laughing. Do not make this another man you have to carry.'],
        ['ryo', '{fast}He squeezed every shop on this strip. I am not leaving his name up there.{/fast}', { hype: 1 }],
        ['aoi', 'That is not what I said. I said think for one second before you wreck the board.'],
        ['ryo', 'I am thinking. About the envelopes. About Ponta.'],
        ['aoi', 'Then we do this as a pair. Not you charging the cabinet alone.'],
        ['ryo', 'As a pair. I am still not going soft.']],
      strategic: [
        ['aoi', '{brisk}He keeps a book. Thursday envelopes, prize slips, the lot.{/brisk}'],
        ['ryo', 'And a score he cannot stand leaving at 999,990.'],
        ['aoi', 'So we do not smash the board. We make him use it.'],
        ['ryo', '{brisk}He talks, we take the seal. You watch the safe.{/brisk}'],
        ['aoi', 'Already on it. You keep him talking.'],
        ['ryo', 'That was my next line.']],
      balanced: [
        ['ryo', 'He is down. I am not putting him through that cabinet.'],
        ['aoi', 'He stamped every shop on this strip, Ryo.'],
        ['ryo', 'I know. That is why I stand in front. Not why I kick him while he is down.'],
        ['aoi', 'You are protecting him. After all of that.'],
        ['ryo', 'I am protecting us from turning into him.'],
        ['aoi', '{quiet}I do not like how easy you make that sound.{/quiet} I am still here.']]
    };
  }
  try {
    if (STORY && STORY.BOND && STORY.BOND.PAY && !STORY.BOND.PAY.c2_jin_after) STORY.BOND.PAY.c2_jin_after = { best: 790, mid: 395, clash: 158 };
    if (typeof BCALL_NAME === 'object') BCALL_NAME.c2_jin_after = 'Jin at the prize safe';
    if (root.FFF_CH2BOND && FFF_CH2BOND.ids && FFF_CH2BOND.ids.indexOf('c2_jin_after') < 0) FFF_CH2BOND.ids.push('c2_jin_after');
  } catch (ePay) { ev('world:s2p6:err:jinpay:' + (ePay && ePay.message)); }

  VO.jinWipe = V3(
    [['', '<p class="dim">Ryo drags a sleeve across the gold cabinet. The initials smear. A Thursday slip falls from the coin lip.</p>'],
     ['j6_jin', 'Tch. You even take a man\u2019s score.']],
    { fierce: [['ryo', 'The shops already paid that debt.']], strategic: [['aoi', 'The slip is enough. We are done here.']], balanced: [['ryo', 'I will not hit you again. The board is enough.']] },
    [['aoi', 'We have the slip. The seal is next.']]
  );
  VO.jinDeal = V3(
    [['j6_jin', 'Thursday. Back office first. Tetsu counts. I only ran the floor.'],
     ['j6_jin', 'The book is in the safe, under the plush. Don\u2019t crease it.']],
    { fierce: [['ryo', 'I have the book.']], strategic: [['aoi', 'We will hold you to every name in it.']], balanced: [['ryo', 'Your initials can stay. The book cannot.']] },
    []
  );
  VO.jinHelp = V3(
    [['ryo', 'Up. The board stays yours.'],
     ['j6_jin', '\u2026Ha. Nobody offers the loser his initials back.'],
     ['j6_jin', 'Safe\u2019s yours. Leave the 990. I\u2019ll get it later.']],
    { fierce: [['aoi', 'Keep that promise.']], strategic: [['aoi', 'The envelopes stop too. That was not free.']], balanced: [['aoi', 'We will be back if that 990 starts climbing on anyone else.']] },
    []
  );

  function fateOfJin(ans) { return ans === 'fierce' ? 'wipe' : ans === 'strategic' ? 'deal' : 'help'; }
  function pickedJin() { try { return ((STORY.bond(SAVE) || {}).picks || {}).c2_jin_after; } catch (e) { return ''; } }
  function applyJinFate(f) {
    if (f === 'wipe') {
      if (G_CAST.jb) { try { kill(G_CAST.jb); } catch (eK) {} G_CAST.jb = null; }
      try {
        if (typeof lieEl === 'function' && !document.querySelector('[data-npc="j6_jin"].c2lie')) {
          var le = lieEl('j6_jin', 500, 420, (typeof C2K === 'object' && C2K.mb2_game) || 1);
          if (le) { le.classList.add('c2lie'); le.dataset.npc = 'j6_jin'; (typeof layer !== 'undefined' ? layer : document.getElementById('world')).appendChild(le); if (W.ints) W.ints.push({ el: le }); if (!W.c2n) W.c2n = {}; W.c2n.s2jinLie = le; }
        }
      } catch (eL) { ev('world:s2p6:err:lie:' + (eL && eL.message)); }
    } else if (f === 'deal') {
      if (G_CAST.jb) { try { kill(G_CAST.jb); } catch (eK) {} G_CAST.jb = null; }
    }
    /* help: leave him standing; popGc will keep him after the seal */
  }
  function playJinFate(done) {
    var f = E().jinFate || 'help';
    applyJinFate(f);
    var vo = f === 'wipe' ? VO.jinWipe : f === 'deal' ? VO.jinDeal : VO.jinHelp;
    lockIn(1);
    talk(pv(vo), function () { lockIn(0); if (done) done(); });
  }
  function stampJin(pk) {
    E().jinFate = fateOfJin(pk);
    if (pk === 'strategic') E().jinBook = 1;
    if (pk === 'fierce') E().jinSlip = 1;
    sv();
    ev('world:s2p6:bond:' + E().jinFate);
  }
  function askJinThenSeal() {
    if (E().seal_game) { finishQuest(); return; }
    var ans = pickedJin();
    if (ans && !E().jinFate) stampJin(ans);
    if (E().jinFate) { playJinFate(function () { (P6.doTakeSeal || doTakeSeal)(); }); return; }
    lockIn(1);
    try {
      bondAsk('c2_jin_after', function (L2) {
        stampJin(pickedJin() || path());
        function next() { playJinFate(function () { (P6.doTakeSeal || doTakeSeal)(); }); }
        if (L2 && L2.length) talk(L2, next); else next();
      });
    } catch (eB) { ev('world:s2p6:err:bond:' + (eB && eB.message)); lockIn(0); playJinFate(function () { (P6.doTakeSeal || doTakeSeal)(); }); }
  }
  P6.askJinThenSeal = askJinThenSeal;

  function doTakeSeal() {
    if (busy() || dlgUp() || E().seal_game) return; var e = E(); lockIn(1);
    try { AU.play('place', { gain: 0.8 }); } catch (eA) {} try { AU.play('fire_whoosh', { gain: 0.6 }); } catch (eA2) {}
    e.seal_game = 1; var n = (typeof c2Seals === 'function') ? c2Seals() : 0;
    var f = (typeof C2S_FAC === 'object' && C2S_FAC.game) || 'neo', own = e.run_fac && f === e.run_fac;
    if (!own && f) e['down_' + f] = 1;
    if (!own && e.run_fac && !e.c2sUp) { e.c2sUp = 1; try { if (root.FFF_OPN) root.FFF_OPN.grant(C2S_SET[e.run_fac][1]); } catch (eG) {} }
    sv(); ev('world:c2:seal:game:' + n); ev('world:s2p6:seal');
    try { if (typeof c2sLocksSync === 'function') c2sLocksSync(); } catch (eS) {}
    P6.resetPaint('gcback'); paintRoom();
    var last = n >= ((typeof C2LMK !== 'undefined' && C2LMK.length) || 4);
    var L2 = [['', '<p class="dim">Ryo pries the gray seal off the prize safe. A small engraved token, a serial on the back. Jin\u2019s initials scratched under it.</p>'], ['aoi', last ? 'All four. Now Tetsu\u2019s slip.' : ((typeof C2SC === 'object' && C2SC.sealN && C2SC.sealN[n]) || 'Three down.')]];
    if (!own && f) { try { L2.push(['ryo', 'The ' + (typeof c2sFacName === 'function' ? c2sFacName(f) : 'Syndicate') + ' stand down now.']); } catch (eN) {} }
    talk(L2, function () { lockIn(0); if (last) { try { if (typeof sayKey === 'function') sayKey('c2', 'elevator_live'); } catch (eK) {} } try { if (typeof c2SqRefresh === 'function') c2SqRefresh(); } catch (eQ) {} finishQuest(); });
  }
  P6.takeSeal = askJinThenSeal; P6.doTakeSeal = doTakeSeal;
  function flipStrip() { var n = NS(); n.won = n.won || {}; n.won.strip = 1; E().stripPunk = 1; /* Club Kitsune flies the Punks' colours now; shop prices are unchanged (no Nails discount on the strip) */
    try { if (root.FFF_NQ && root.FFF_NQ.BLK && !root.FFF_NQ.BLK.strip) root.FFF_NQ.BLK.strip = { n: 'NEON STRIP', r: [2100, 1400, 3800, 1800] }; } catch (eB) {} sv(); ev('world:s2p6:strip:flip'); }
  function finishQuest() { if (!E().seal_game) return; if (!qDone()) { setStg('done'); qClose(); } flipStrip(); ev('world:s2p6:done'); }
  P6.finishQuest = finishQuest; P6.flipStrip = flipStrip;
  ACT.j6_gc_prize = function () { return prize(); };
  TALK.j6_prize = function () { return prize(); };
  TALK.j6_gamer = function () { if (busy()) return true; lockIn(1); var a = A6(); talk([['j6_gamer', Object.keys(a.g).length >= 5 ? 'You mastered all five? I\u2019m telling everyone.' : 'Gold on all five and your initials go up. Jin\u2019s are on everything.']], function () { lockIn(0); }); return true; };
  ACT.j6_gc_crane = function () { if (busy()) return true; lockIn(1); talk(VO.crane, function () { lockIn(0); }); return true; };
  ACT.j6_gc_medal = function () { if (busy()) return true; lockIn(1); talk(VO.medal, function () { lockIn(0); }); return true; };
  ACT.j6_gc_board = function () { if (busy()) return true; var a = A6(), X = root.FFF_S2ARC, TN = ['\u2014', 'Bronze', 'Silver', 'Gold'];
    var L = (X && X.CAB_ORDER || []).filter(function (k) { return X.CABS[k]; }).map(function (k) { var B = X.board ? X.board(k, a.hs[k]) : [], me = -1; B.forEach(function (e, i) { if (me < 0 && e.me) me = i; });
      return '<b>' + X.CABS[k].n + '</b>: ' + (B[0] ? B[0].n + ' ' + B[0].s : '') + ' \u00b7 you ' + (a.best[k] | 0) + (me >= 0 ? ' (#' + (me + 1) + ')' : '') + ' \u00b7 ' + TN[a.tier[k] | 0]; }).join('<br>');
    lockIn(1); talk([['', '<p class="dim">HIGH SCORES<br>' + L + '</p>']], function () { lockIn(0); }); return true; };
  ACT.j6_gc_staff = function () { if (busy()) return true; if (at('met')) { enterRoom('gcback'); return true; } lockIn(1); talk(VO.gcStaff0, function () { lockIn(0); }); return true; };
  ACT.j6_gc_seal = function () { if (busy()) return true; if (at('won') && !E().seal_game) { askJinThenSeal(); return true; } if (stg() === 'met') { gcBackArrive(); return true; } lockIn(1); talk(E().seal_game ? VO.sealDone : VO.gcStaff0, function () { lockIn(0); }); return true; };
  ACT.j6_gc_jincab = function () { if (busy()) return true; lockIn(1); talk(VO.jinCab, function () { lockIn(0); }); return true; };
  ARRIVE.gc = gcArrive; ARRIVE.gcback = gcBackArrive; POP.push(popGc);
  PIN.izak = function () { return { room: 'town', x: GC_DOOR.at[0], y: GC_DOOR.at[1] - 60, lab: 'Game Center', loc: 'High Score \u00b7 Neon Game Center' }; };
  PIN.met = function () { if (room() === 'gc') return { room: 'gc', x: 1120, y: 250, lab: 'Staff door', loc: 'High Score \u00b7 Jin\u2019s prize room' }; return { room: 'town', x: GC_DOOR.at[0], y: GC_DOOR.at[1] - 60, lab: 'Game Center', loc: 'High Score \u00b7 Jin\u2019s prize room' }; };
  PIN.won = function () { if (room() === 'gcback') return { room: 'gcback', x: 500, y: 240, lab: 'Seal', loc: 'High Score \u00b7 Jin\u2019s seal' }; return PIN.met(); };

  if (typeof c2Tags === 'function') {
    var tags0 = c2Tags;
    c2Tags = function (id, D) {
      var out = tags0.apply(this, arguments);
      try { if (out && on()) out = out.filter(function (t) { if (!t || !t.key) return true; var m = /:j6_e_(\w+)$/.exec(t.key); if (m) return roomOpen(m[1]); return true; }); } catch (e) {}
      return out;
    };
  }
  if (typeof c2ActC === 'function') {
    var act0 = c2ActC;
    c2ActC = function (k, a) {
      try {
        if (on() && a) {
          var m = /^j6_e_(\w+)$/.exec(a);
          if (m) { if (roomOpen(m[1])) { chainRepair(); enterRoom(m[1]); } return true; }
          if (a === 'lm_game' && stripOpen()) { chainRepair(); enterRoom('gc'); return true; }
          if (a === 'exit' && inJ6() && P6.innerBack && P6.innerBack[room()]) { P6.innerBack[room()](); return true; }
          if (ACT[a]) return ACT[a](k) !== false;
        }
      } catch (e) { ev('world:s2p6:err:act:' + (e && e.message)); }
      return act0.apply(this, arguments);
    };
  }
  function talkHook(s) {
    if (!on() || !s) return null;
    var id = s.s2id || s.id || (s.el && s.el.dataset && (s.el.dataset.npc || s.el.dataset.who));
    if (id && TALK[id] && (inJ6() || P6.TALK_ANY && P6.TALK_ANY[id])) return TALK[id](s);
    return null;
  }
  if (typeof c2Talk === 'function') { var tk0 = c2Talk; c2Talk = function (s) { try { var r = talkHook(s); if (r != null) return r; } catch (eT) {} return tk0.apply(this, arguments); }; }
  else if (typeof talkNpc === 'function') { var tn0 = talkNpc; talkNpc = function (s) { try { var r = talkHook(s); if (r != null) return r; } catch (eT) {} return tn0.apply(this, arguments); }; }

  var lastK = null;
  if (typeof c2Frame === 'function') {
    var fr0 = c2Frame;
    c2Frame = function (dt) { fr0.apply(this, arguments); try { if (on() && p6Enter()) { var k = room(); if (k !== lastK) { lastK = k; chainRepair(); popAll(); paintRoom(); } } } catch (e) { if (!P6.ferr) { P6.ferr = 1; ev('world:s2p6:err:frame:' + (e && e.message)); } } };
  }
  if (typeof c2Go === 'function') {
    var goX = c2Go;
    c2Go = function () { var r = goX.apply(this, arguments); try { if (on()) { later(0, function () { popAll(); paintRoom(); }); } } catch (eG) {} return r; };
  }
  if (typeof c2Pop === 'function') {
    var pop0 = c2Pop;
    c2Pop = function () { pop0.apply(this, arguments); try { if (on()) { chainRepair(); hookBattle(); popAll(); paintRoom(); } } catch (eP) {} };
  }
  try { chainRepair(); } catch (eC) {}
  ev('world:s2p6:ready');
  } catch (eS2) { try { ev('world:s2p6:err:init:' + (eS2 && eS2.message)); console.warn('S2P6 init', eS2); } catch (e2) {} }
})();
