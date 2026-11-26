/* v6.5.63 FFF_S2P4 (Punk-route seal 2, phase 4): Off Schedule.
 * Quest cq2_s2_gar after Above the Boat. Beat Masa's dispatcher at the quay
 * garage. Sets e.baseOpen_dep / e.guardGone_depot; the depot door opens only
 * after the win. Path voice only — no bond pick, no Phase 5 quest. Wraps only;
 * no new always-running loops. Does not edit existing Fierce/Strategic Nails
 * copy, the Door Man path, or S2 / S2P2 / S2P3 VO. */
(function () {
  try {
  if (typeof c2S !== 'function' || typeof C2W === 'undefined' || !C2W || typeof INT === 'undefined' || !INT.c2_town) {
    try { ev('world:s2p4:skip'); } catch (e0) {} return;
  }
  var root = typeof window !== 'undefined' ? window : this;
  var P3 = root.FFF_S2P3;
  var P4 = root.FFF_S2P4 = { v: 1, ART: true };

  function on() { return (typeof c2On !== 'function' || c2On()) && (typeof chN !== 'function' || chN() === 2); }
  function S() { return c2S(); }
  function E() { return c2S().e; }
  function room() { try { return c2Room(); } catch (e) { return null; } }
  function inTown() { return room() === 'town'; }
  function nailsRun() { return on() && E().run_fac === 'arc'; }
  function busy() { return !!(W.dgFight || W.dlg || W.busy || W.cut || W.fading || W.paused); }
  function later(ms, fn) { setTimeout(function () { try { fn(); } catch (e) { ev('world:s2p4:err:later:' + (e && e.message)); } }, ms); }
  function talk(lines, done) { W.dlg = true; scene(null, lines, function () { W.dlg = false; if (done) done(); }); }
  function lockIn(on1) { if (on1) { W.cut = true; W.path = []; if (W.ryo) W.ryo.v = 0; try { stickEnd(); } catch (e) {} } else W.cut = false; }
  function sv() { try { if (typeof c2QSync === 'function') c2QSync(); } catch (e) {} save(); }
  function path() { var p = 'balanced'; try { p = c2Path(); } catch (e) {} return p === 'fierce' || p === 'strategic' ? p : 'balanced'; }
  function npc(id, x, y, fa) { var s = c2Npc(id, x, y, fa == null ? Math.PI / 2 : fa); s.el.classList.add('s2'); s.s2id = id; s.el.dataset.npc = id; return s; }
  function kill(s) { if (s && s.el && s.el.parentNode) s.el.remove(); if (s) s.gone = 1; }
  function whenFree(fn, tries) { tries = tries || 0; if (!busy() && !document.getElementById('nqsting') && !(typeof W.c2busy !== 'undefined' && W.c2busy)) { try { fn(); } catch (e) { ev('world:s2p4:err:free:' + (e && e.message)); } return; } later(tries < 120 ? 250 : 1000, function () { whenFree(fn, tries + 1); }); }
  function V3(pre, mid, post) { var o = {}, PP = ['fierce', 'strategic', 'balanced']; PP.forEach(function (p) { o[p] = (pre || []).concat(mid[p] || [], post || []); }); return o; }
  function pv(x) { try { return typeof pathLines === 'function' ? pathLines(x) : (x[path()] || x.balanced || x); } catch (e) { return x.balanced || []; } }
  function boatDone() { return P3 && typeof P3.qDone === 'function' && P3.qDone(); }
  function punkAfterSeal() { return on() && nailsRun() && !!E().seal_sento; }

  /* ---------------- state ---------------- */
  function NS() { var e = E(); if (!e.nq || typeof e.nq !== 'object') e.nq = {}; return e.nq; }
  function stg() { return NS().gar || ''; }
  function setStg(v) { NS().gar = v; sv(); ev('world:s2p4:st:' + v); }
  var QID = 'cq2_s2_gar';
  var Q = { id: QID, n: 'Off Schedule', giver: 'Sada, at the quay garage',
    quote: 'Masa\u2019s dispatcher still holds the depot door. Take the garage.',
    loc: 'Kitsune-Ch\u016b\u014d \u00b7 Quay garage, depot approach' };
  if (typeof C2Q !== 'undefined') C2Q[QID] = { n: Q.n, steps: [Q.quote] };
  if (typeof C2QLOC !== 'undefined') C2QLOC[QID] = ['town', Q.loc];
  function qOpen() { var s = S(); if (s.q[QID] == null) s.q[QID] = 0; SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = s.q[QID] | 0; s.qa = QID; SAVE.qa = QID; SAVE.qTrack = ''; SAVE.qTrackPick = 0; sv(); ev('world:s2p4:quest:open'); }
  function qStep(n) { var s = S(); if (s.q[QID] == null || s.q[QID] === 9) return; s.q[QID] = Math.max(s.q[QID] | 0, n); SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = s.q[QID]; sv(); }
  function qClose() { var s = S(); if (s.q[QID] == null || s.q[QID] === 9) return; s.q[QID] = 9; SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = 9;
    SAVE.journalLog = SAVE.journalLog || []; if (SAVE.journalLog.indexOf(Q.n) < 0) SAVE.journalLog.push(Q.n);
    if (s.qa === QID) { s.qa = (typeof CQ !== 'undefined' && CQ.locks) || ''; SAVE.qa = s.qa; } sv(); ev('world:s2p4:quest:done');
    if (typeof window.c2QuestYen === 'function') window.c2QuestYen(QID, Q.n); }
  function qOn() { var q = S().q[QID]; return q != null && q !== 9; }
  function qDone() { return S().q[QID] === 9; }
  function roomOpen() { return on() && punkAfterSeal() && (boatDone() || qOn() || qDone()); }
  function cleared() { return qDone() || stg() === 'done'; }
  P4.Q = Q; P4.stg = stg; P4.setStg = setStg; P4.qOpen = qOpen; P4.qClose = qClose; P4.qOn = qOn; P4.qDone = qDone;
  P4.roomOpen = roomOpen; P4.cleared = cleared;

  /* ---------------- voices (new tables only) ---------------- */
  var VO = P4.VO = {};
  VO.door = V3(
    [['nq_sada', 'Freight only. You don\u2019t have a slot on this board.']],
    {
      fierce: [['ryo', 'Then we go through you.'], ['aoi', 'The bay first.'], ['nq_sada', 'You want the yard, you take the garage.']],
      strategic: [['ryo', 'You\u2019re already late.'], ['aoi', 'The missed loads are still on the quay.'], ['nq_sada', 'You read my board? That doesn\u2019t get you the door.']],
      balanced: [['ryo', 'Stand aside. Let the yard run honest again.'], ['aoi', 'The men on the clock should not have to wait on this.'], ['nq_sada', 'Masa\u2019s door stays mine. I will not stand aside.']]
    },
    []
  );
  VO.inside = V3(
    [['nq_sada', 'You walked into my bay. That was the choice.']],
    {
      fierce: [['ryo', 'Then we finish it here.']],
      strategic: [['aoi', 'We should have taken him on the approach.'], ['ryo', 'We\u2019re here now.']],
      balanced: [['ryo', 'Last chance. Stand aside.'], ['nq_sada', 'In here? No.']]
    },
    []
  );
  VO.approach = V3(
    [['aoi', 'The door is right there. He\u2019s off his own schedule.']],
    {
      fierce: [['ryo', 'Then we take him here.'], ['nq_sada', 'On my approach? Fine.']],
      strategic: [['ryo', 'You\u2019re already late. The missed freight is still sitting here.'], ['nq_sada', 'You don\u2019t use my board against me.']],
      balanced: [['ryo', 'Stand aside. The yard can run honest without you on this door.'], ['nq_sada', 'I said no. The door stays shut.']]
    },
    []
  );
  VO.wonFight = V3(
    [['nq_sada', 'The door is yours.']],
    {
      fierce: [['nq_sada', 'Masa\u2019s in the yard. You want him, go in.'], ['ryo', 'Then that\u2019s next.']],
      strategic: [['nq_sada', 'You used a late load to walk in.'], ['aoi', 'The depot door is open.'], ['ryo', 'We know.']],
      balanced: [['nq_sada', 'You asked. I wouldn\u2019t move.'], ['ryo', 'The yard can run honest now. The door is open.']]
    },
    []
  );
  VO.empty = [ ['', 'The radio is quiet. The clipboard is on the floor. The bay is empty.'] ];

  /* ---------------- sprites + portraits ---------------- */
  if (typeof NM !== 'undefined') NM.nq_sada = 'Sada';
  function wireWho(id, pre, ck, figAlias) {
    if (typeof wUrl !== 'function' || typeof IMG === 'undefined') return;
    IMG[id + '_walk'] = wUrl(pre + '_walk');
    IMG[id + '_idle'] = wUrl(pre + '_idle');
    IMG[id + '_map'] = wUrl(pre + '_map');
    IMG[id + '_fig'] = wUrl(pre + '_fig');
    IMG[id + '_run'] = IMG[id + '_walk'];
    ['hurt', 'kn', 'lie', 'fig_hurt', 'fig_down'].forEach(function (sh) { IMG[id + '_' + sh] = IMG[id + '_fig']; });
    if (typeof SHC !== 'undefined') { SHC[id + '_walk'] = 8; SHC[id + '_idle'] = 4; }
    if (typeof SHR !== 'undefined') { SHR[id + '_idle'] = 4; if (SHR.c2_punk_walk != null) SHR[id + '_walk'] = SHR.c2_punk_walk; }
    if (typeof BW_IDS !== 'undefined') BW_IDS[id] = 1;
    if (typeof C2K !== 'undefined') C2K[id] = ck;
    PT[id] = id + '_fig';
    if (typeof PT_PAINT !== 'undefined') PT_PAINT[id] = figAlias;
    if (typeof PT_HAS !== 'undefined') {
      PT_HAS[figAlias + '_neutral'] = 1;
      PT_HAS[figAlias + '_angry'] = 1;
      PT_HAS[figAlias + '_calm'] = 1;
    }
  }
  wireWho('nq_sada', 'nq_sada', 1.04, 'sada');

  /* ---------------- doors + rooms ---------------- */
  /* west of the locked depot door, on the south-quay flower walkway */
  var GAR_AT = [4040, 3900];
  var AP_AT = [4220, 3880];
  var DEPOT_AT = [4300, 3720];
  var GAR_DOOR = { r: [3920, 3840, 4160, 3960], at: GAR_AT, to: 'gar', out: [GAR_AT[0], GAR_AT[1] - 16] };
  var AP_SPOT = { r: [4140, 3800, 4360, 3960], at: AP_AT };
  var RW = 1280, RH = 900;
  function roomDef(k, n, extra) {
    var id = 'c2_nq_' + k; C2R[k] = id;
    INT[id] = Object.assign({ id: id, n: n, w: RW, h: RH, src: 'world/nq_' + k + '.paint', tiles: 1, cell: 15, dg: 'c2', c2: k, deep: 1, safe: 1, mus: 'c2night', nq: 1, s2: 1,
      open: [[90, 250, 1190, 850], [580, 850, 700, 900]], 'in': [640, 820, 3], back: [640, 820, 3],
      spots: [{ id: 'exit', r: [575, 850, 705, 900], at: [640, 870], face: 0 }] }, extra || {});
    INT[id].base = INT[id].block; TAGS_IN[id] = {};
    return INT[id];
  }
  roomDef('gar', 'Quay garage \u00b7 Dispatch', { block: [[110, 470, 260, 620], [180, 630, 500, 770], [1000, 540, 1180, 690]],
    spots: [{ id: 'exit', r: [575, 850, 705, 900], at: [640, 870], face: 0 },
      { id: 's2_talk_sada', r: [240, 600, 520, 760], at: [400, 800], face: 0, lab: 'Talk' }] });
  C2W.doors.nq_gar = GAR_DOOR;
  if (typeof c2DoorOf === 'function') {
    var door0 = c2DoorOf;
    c2DoorOf = function (k) { if (k === 'gar') return GAR_DOOR; return door0.apply(this, arguments); };
  }
  if (typeof c2Surf === 'function') {
    var surf0 = c2Surf;
    c2Surf = function (x, y) { var k = c2Room(); if (k === 'gar') return 'stone'; return surf0.apply(this, arguments); };
  }
  INT.c2_town.spots.push({ id: 's2_e_gar', r: GAR_DOOR.r, at: GAR_DOOR.at, face: 0, lab: 'Enter' });
  INT.c2_town.spots.push({ id: 's2_ap', r: AP_SPOT.r, at: AP_SPOT.at, face: 0, lab: 'Approach' });
  if (typeof TRANS !== 'undefined') { TRANS.s2_e_gar = 1; }
  delete INT.c2_town.G;
  P4.GAR_DOOR = GAR_DOOR; P4.GAR_AT = GAR_AT; P4.AP_AT = AP_AT; P4.DEPOT_AT = DEPOT_AT;

  /* façade on the south bank, west of the depot door — must not cover 4180–4420 */
  var FAC = null;
  function placeDoor() {
    if (!P4.ART || !on() || !inTown() || !roomOpen()) return;
    if (document.getElementById('s2GarSouth')) return;
    if (!FAC) {
      FAC = document.createElement('canvas'); FAC.width = 320; FAC.height = 180;
      try { if (root.FFF_S2P && root.FFF_S2P.garSouth) root.FFF_S2P.garSouth(FAC.getContext('2d')); } catch (eF) { ev('world:s2p4:err:facade:' + (eF && eF.message)); }
    }
    FAC.className = 'nqprop'; FAC.id = 's2GarSouth';
    FAC.style.cssText = 'position:absolute;left:3840px;top:3850px;width:320px;height:180px;z-index:' + (100 + 3900) + ';pointer-events:none';
    var host = null, sample = document.querySelector('#world .nqprop, #wimap .nqprop, .nqprop');
    if (sample && sample.parentNode) host = sample.parentNode;
    else host = document.getElementById('wisp') || document.getElementById('world') || document.getElementById('wimap');
    if (host) host.appendChild(FAC);
  }
  P4.placeDoor = placeDoor;

  var RCV = {};
  function paintRoom() {
    var k = room();
    var el = document.getElementById('s2P4Room_gar');
    if (el && k !== 'gar' && el.parentNode) el.parentNode.removeChild(el);
    if (k !== 'gar') return;
    var m = document.getElementById('wimap') || document.getElementById('world');
    if (!m) return;
    var key = cleared() ? 'cleared' : 'held';
    if (!RCV[key]) {
      RCV[key] = document.createElement('canvas'); RCV[key].width = RW; RCV[key].height = RH;
      var g = RCV[key].getContext('2d');
      try { if (P4.ART && root.FFF_S2P && root.FFF_S2P.garInside) root.FFF_S2P.garInside(g, key === 'cleared'); }
      catch (e) { ev('world:s2p4:err:paint:' + (e && e.message)); }
    }
    var c = RCV[key];
    if (c && c.parentNode !== m) { c.className = 'nqprop'; c.id = 's2P4Room_gar'; c.style.cssText = 'position:absolute;left:0;top:0;width:' + RW + 'px;height:' + RH + 'px;z-index:1;pointer-events:none'; m.insertBefore(c, m.firstChild); }
  }
  P4.paintRoom = paintRoom;

  /* battle rooms */
  function hookBattle() {
    if (P4._bt) return true;
    if (!root.FFF_C2BT || !root.FFF_S2P || !root.FFF_S2P.battleGarage || !root.FFF_S2P.battleApproach) return false;
    P4._bt = 1;
    var BT = root.FFF_C2BT;
    BT.ROOMS.gg = { name: 'Quay garage \u00b7 Dispatch', paint: function (x) { root.FFF_S2P.battleGarage(x); },
      lights: [[140, 110, '255,200,110', 70, 0.3, 'lamp'], [580, 110, '255,200,110', 70, 0.3, 'lamp']], rain: 0, mood: 'room', feet: 52 };
    BT.ROOMS.ap = { name: 'Depot approach', paint: function (x) { root.FFF_S2P.battleApproach(x); },
      lights: [[80, 120, '255,190,100', 70, 0.3, 'lamp'], [640, 120, '255,190,100', 70, 0.3, 'lamp']], rain: 50, mood: 'rain', feet: 52 };
    BT.KEY.c2_gg = 'gg'; BT.KEY.c2_ap = 'ap';
    var roomB0 = BT.room;
    BT.room = function (story) {
      var ctx = (story && story.ctx) || {}, dgk = String(ctx.dgk || '');
      if (P4.ART && (ctx.s2gg || ctx.s2k === 's2_gg' || /^s2_gg/.test(dgk))) return 'c2_gg';
      if (P4.ART && (ctx.s2ap || ctx.s2k === 's2_ap' || /^s2_ap/.test(dgk))) return 'c2_ap';
      return roomB0.apply(this, arguments);
    };
    return true;
  }
  hookBattle();
  try { later(0, hookBattle); } catch (eB) { try { setTimeout(hookBattle, 0); } catch (eB2) {} }

  /* ---------------- pin / Four Corners ---------------- */
  function s2Tgt() {
    if (!punkAfterSeal() || !boatDone()) return null;
    if (qOn() && (stg() === '' || stg() === 'open')) {
      if (path() === 'strategic') return { x: AP_AT[0], y: AP_AT[1], lab: 'Depot approach', loc: 'Off Schedule \u00b7 the missed freight' };
      return { x: GAR_AT[0], y: GAR_AT[1], lab: 'Quay garage', loc: 'Off Schedule \u00b7 Dispatch' };
    }
    if (qDone()) return { x: DEPOT_AT[0], y: DEPOT_AT[1], lab: 'Subway Freight Depot', loc: 'The yard door is open' };
    return null;
  }
  P4.s2Tgt = s2Tgt;
  if (typeof c2LocksT === 'function') {
    var lt0 = c2LocksT;
    c2LocksT = function () {
      try { var t = s2Tgt(); if (t) return { room: 'town', x: t.x, y: t.y, lab: t.lab, loc: t.loc }; } catch (eL) {}
      return lt0.apply(this, arguments);
    };
  }

  /* open the depot door the same way The Door Man opens the bathhouse */
  function openDepot() {
    var e = E(); e.baseOpen_dep = 1; e.guardGone_depot = 1; sv();
    try {
      var bg = window.c2DoorGuard && window.c2DoorGuard('depot');
      if (bg && bg.el) bg.el.remove();
      if (window.c2GuardLeave) window.c2GuardLeave('depot', 's2p4');
    } catch (e1) {}
  }
  function chainRepair() {
    if (!punkAfterSeal() || !boatDone()) return;
    var ch = 0;
    if (!qOn() && !qDone()) { qOpen(); if (!stg()) setStg('open'); ch = 1; }
    if (qDone()) {
      var e = E();
      if (!e.baseOpen_dep || !e.guardGone_depot) { openDepot(); ch = 1; }
    }
    if (ch) ev('world:s2p4:repair');
  }
  P4.chainRepair = chainRepair;
  P4.openDepot = openDepot;

  if (typeof c2LmOpen === 'function') {
    var lmo4 = c2LmOpen;
    c2LmOpen = function (k) {
      if (k === 'depot' && (qDone() || !!(E().baseOpen_dep || E().guardGone_depot))) return true;
      return lmo4.apply(this, arguments);
    };
  }

  /* ---------------- pops ---------------- */
  var SADA = null, SADA_OUT = null;
  function popGarage() {
    if (room() !== 'gar') { if (SADA) { try { kill(SADA); } catch (eK) {} SADA = null; } return; }
    if (cleared()) { if (SADA) { try { kill(SADA); } catch (eK) {} SADA = null; } return; }
    if (SADA && SADA.el && SADA.el.parentNode) return;
    SADA = npc('nq_sada', 500, 700, Math.PI / 2);
    try { if (typeof waddle === 'function') waddle(SADA, 0, Math.PI / 2); } catch (eW) {}
    try { if (W.c2n) W.c2n.s2sada = SADA; } catch (eN) {}
  }
  function popTown() {
    if (!inTown() || !qOn() || cleared()) {
      if (SADA_OUT) { try { kill(SADA_OUT); } catch (eK) {} SADA_OUT = null; } return;
    }
    if (SADA_OUT && SADA_OUT.el && SADA_OUT.el.parentNode) return;
    /* at the garage door, facing north onto the quay */
    SADA_OUT = npc('nq_sada', 4040, 3920, -Math.PI / 2);
    try { if (typeof waddle === 'function') waddle(SADA_OUT, 0, -Math.PI / 2); } catch (eW) {}
  }

  /* ---------------- talks + fights ---------------- */
  var fighting = 0;
  function startGarageFight() {
    if (fighting || busy()) return;
    fighting = 1;
    lockIn(0);
    var ctx = { dg: 'c2', dgk: 's2_gg_0', dgks: ['s2_gg_0', 's2_gg_1', 's2_gg_2'], s2k: 's2_gg', s2: 1, s2gg: 1 };
    try { fight(['nq_sada', 'c2_boso', 'c2_boso'], false, ctx); } catch (eF) { fighting = 0; ev('world:s2p4:err:fight:' + (eF && eF.message)); }
  }
  function startApproachFight() {
    if (fighting || busy()) return;
    fighting = 1;
    lockIn(0);
    var ctx = { dg: 'c2', dgk: 's2_ap_0', dgks: ['s2_ap_0', 's2_ap_1', 's2_ap_2'], s2k: 's2_ap', s2: 1, s2ap: 1, freeOpen: 1 };
    try { fight(['nq_sada', 'c2_boso', 'c2_boso'], false, ctx); } catch (eF) { fighting = 0; ev('world:s2p4:err:fight:' + (eF && eF.message)); }
  }
  function finishQuest() {
    setStg('done');
    openDepot();
    qClose();
    /* pin moves to the depot door; do not open unbuilt Phase 5. */
  }
  function fightWon() {
    fighting = 0;
    whenFree(function () {
      talk(pv(VO.wonFight), function () { finishQuest(); });
    });
  }
  function doorTalk() {
    if (busy()) return true;
    if (qDone() || cleared()) {
      lockIn(1); talk(VO.empty, function () { lockIn(0); }); return true;
    }
    if (!qOn()) return false;
    lockIn(1);
    if (path() === 'fierce') {
      talk(pv(VO.door), function () { lockIn(0); startGarageFight(); });
    } else if (path() === 'strategic') {
      talk(pv(VO.door), function () { lockIn(0); startApproachFight(); });
    } else {
      /* compassionate: he will not stand aside; the fight still happens, on the approach */
      talk(pv(VO.door), function () { lockIn(0); startApproachFight(); });
    }
    return true;
  }
  function insideTalk() {
    if (busy()) return true;
    if (qDone() || cleared()) {
      lockIn(1); talk(VO.empty, function () { lockIn(0); }); return true;
    }
    if (!qOn()) return false;
    lockIn(1);
    talk(pv(VO.inside), function () { lockIn(0); startGarageFight(); });
    return true;
  }
  function approachTalk() {
    if (busy()) return true;
    if (!qOn() || cleared()) return false;
    lockIn(1);
    talk(pv(VO.approach), function () { lockIn(0); startApproachFight(); });
    return true;
  }

  if (typeof onFightEnd === 'function') {
    var of0 = onFightEnd;
    onFightEnd = function (win, c) {
      var r = of0.apply(this, arguments);
      try {
        if (c && (c.s2k === 's2_gg' || c.s2k === 's2_ap')) {
          if (!win) { fighting = 0; return r; }
          fightWon();
        }
      } catch (eE) {}
      return r;
    };
  }

  /* spots / tags / talk */
  if (typeof c2Tags === 'function') {
    var tags0 = c2Tags;
    c2Tags = function (id, D) {
      var out = tags0.apply(this, arguments);
      try {
        if (out && on()) out = out.filter(function (t) {
          if (!t || !t.key) return true;
          if (t.key.indexOf(':s2_e_gar') >= 0) return roomOpen();
          if (t.key.indexOf(':s2_ap') >= 0) return qOn() && !cleared() && path() === 'strategic';
          if (t.key.indexOf(':s2_talk_sada') >= 0) return room() === 'gar' && !cleared();
          return true;
        });
      } catch (e) {}
      return out;
    };
  }
  if (typeof c2ActC === 'function') {
    var act0 = c2ActC;
    c2ActC = function (k, a) {
      try {
        if (on()) {
          if (a === 's2_e_gar') return act0.apply(this, arguments);
          if (a === 's2_ap') { approachTalk(); return true; }
          if (a === 's2_talk_sada') { insideTalk(); return true; }
        }
      } catch (e) { ev('world:s2p4:err:act:' + (e && e.message)); }
      return act0.apply(this, arguments);
    };
  }
  if (typeof c2Talk === 'function') {
    var tk0 = c2Talk;
    c2Talk = function (s) {
      try {
        if (on() && s) {
          var id = s.s2id || s.id || (s.el && s.el.dataset && s.el.dataset.npc);
          if (id === 'nq_sada') {
            if (room() === 'gar') return insideTalk();
            return doorTalk();
          }
        }
      } catch (eT) {}
      return tk0.apply(this, arguments);
    };
  } else if (typeof talkNpc === 'function') {
    var tn0 = talkNpc;
    talkNpc = function (s) {
      try {
        if (on() && s) {
          var id = s.s2id || s.id;
          if (id === 'nq_sada') {
            if (room() === 'gar') return insideTalk();
            return doorTalk();
          }
        }
      } catch (eT) {}
      return tn0.apply(this, arguments);
    };
  }

  if (typeof c2Frame === 'function') {
    var fr0 = c2Frame;
    c2Frame = function (dt) { fr0.apply(this, arguments); try { hookBattle(); if (on()) { placeDoor(); popTown(); } } catch (e) { if (!P4.ferr) { P4.ferr = 1; ev('world:s2p4:err:frame:' + (e && e.message)); } } };
  }
  if (typeof c2Pop === 'function') {
    var pop0 = c2Pop;
    c2Pop = function () { pop0.apply(this, arguments); try { if (on()) { chainRepair(); placeDoor(); hookBattle(); popGarage(); popTown(); if (room() === 'gar') paintRoom(); } } catch (eP) {} };
  }
  try { chainRepair(); } catch (eC) {}
  ev('world:s2p4:ready');
  } catch (eS2) { try { ev('world:s2p4:err:init:' + (eS2 && eS2.message)); console.warn('S2P4 init', eS2); } catch (e2) {} }
})();
