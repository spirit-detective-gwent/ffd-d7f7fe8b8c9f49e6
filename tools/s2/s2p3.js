/* v6.5.63 FFF_S2P3 (Punk-route seal 2, phase 3): Above the Boat.
 * Quest cq2_s2_boat after Night Runs. Clear Masa's lookouts in the Funayado
 * above the flower boat. Skip/shrink if n13r === 'dep' (Lookout Corner already
 * ran this). After a win the pin moves to the quay garage; no Phase 4 quest.
 * Path voice is new tables only. Wraps only; no new always-running loops.
 * Does not edit existing Fierce/Strategic Nails copy or S2 / S2P2 VO. */
(function () {
  try {
  if (typeof c2S !== 'function' || typeof C2W === 'undefined' || !C2W || typeof INT === 'undefined' || !INT.c2_town) {
    try { ev('world:s2p3:skip'); } catch (e0) {} return;
  }
  var root = typeof window !== 'undefined' ? window : this;
  var S2 = root.FFF_S2, P2 = root.FFF_S2P2;
  var P3 = root.FFF_S2P3 = { v: 1, ART: true };

  function on() { return (typeof c2On !== 'function' || c2On()) && (typeof chN !== 'function' || chN() === 2); }
  function S() { return c2S(); }
  function E() { return c2S().e; }
  function room() { try { return c2Room(); } catch (e) { return null; } }
  function inTown() { return room() === 'town'; }
  function nailsRun() { return on() && E().run_fac === 'arc'; }
  function busy() { return !!(W.dgFight || W.dlg || W.busy || W.cut || W.fading || W.paused); }
  function later(ms, fn) { setTimeout(function () { try { fn(); } catch (e) { ev('world:s2p3:err:later:' + (e && e.message)); } }, ms); }
  function talk(lines, done) { W.dlg = true; scene(null, lines, function () { W.dlg = false; if (done) done(); }); }
  function lockIn(on1) { if (on1) { W.cut = true; W.path = []; if (W.ryo) W.ryo.v = 0; try { stickEnd(); } catch (e) {} } else W.cut = false; }
  function sv() { try { if (typeof c2QSync === 'function') c2QSync(); } catch (e) {} save(); }
  function path() { var p = 'balanced'; try { p = c2Path(); } catch (e) {} return p === 'fierce' || p === 'strategic' ? p : 'balanced'; }
  function npc(id, x, y, fa) { var s = c2Npc(id, x, y, fa == null ? Math.PI / 2 : fa); s.el.classList.add('s2'); s.s2id = id; s.el.dataset.npc = id; return s; }
  function kill(s) { if (s && s.el && s.el.parentNode) s.el.remove(); if (s) s.gone = 1; }
  function whenFree(fn, tries) { tries = tries || 0; if (!busy() && !document.getElementById('nqsting') && !(typeof W.c2busy !== 'undefined' && W.c2busy)) { try { fn(); } catch (e) { ev('world:s2p3:err:free:' + (e && e.message)); } return; } later(tries < 120 ? 250 : 1000, function () { whenFree(fn, tries + 1); }); }
  function V3(pre, mid, post) { var o = {}, PP = ['fierce', 'strategic', 'balanced']; PP.forEach(function (p) { o[p] = (pre || []).concat(mid[p] || [], post || []); }); return o; }
  function pv(x) { try { return typeof pathLines === 'function' ? pathLines(x) : (x[path()] || x.balanced || x); } catch (e) { return x.balanced || []; } }
  function runsDone() { return P2 && typeof P2.qDone === 'function' && P2.qDone(); }
  function punkAfterSeal() { return on() && nailsRun() && !!E().seal_sento; }
  function alreadyClear() { return E().n13r === 'dep'; }

  /* ---------------- state ---------------- */
  function NS() { var e = E(); if (!e.nq || typeof e.nq !== 'object') e.nq = {}; return e.nq; }
  function stg() { return NS().boat || ''; }
  function setStg(v) { NS().boat = v; sv(); ev('world:s2p3:st:' + v); }
  var QID = 'cq2_s2_boat';
  var Q = { id: QID, n: 'Above the Boat', giver: 'the last runner, or Flip',
    quote: 'Masa still has lookouts in the boat house above the flower boat. Clear them.',
    loc: 'Kitsune-Ch\u016b\u014d \u00b7 Funayado, south quay' };
  if (typeof C2Q !== 'undefined') C2Q[QID] = { n: Q.n, steps: [Q.quote] };
  if (typeof C2QLOC !== 'undefined') C2QLOC[QID] = ['town', Q.loc];
  function qOpen() { var s = S(); if (s.q[QID] == null) s.q[QID] = 0; SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = s.q[QID] | 0; s.qa = QID; SAVE.qa = QID; SAVE.qTrack = ''; SAVE.qTrackPick = 0; sv(); ev('world:s2p3:quest:open'); }
  function qStep(n) { var s = S(); if (s.q[QID] == null || s.q[QID] === 9) return; s.q[QID] = Math.max(s.q[QID] | 0, n); SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = s.q[QID]; sv(); }
  function qClose() { var s = S(); if (s.q[QID] == null || s.q[QID] === 9) return; s.q[QID] = 9; SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = 9;
    SAVE.journalLog = SAVE.journalLog || []; if (SAVE.journalLog.indexOf(Q.n) < 0) SAVE.journalLog.push(Q.n);
    if (s.qa === QID) { s.qa = (typeof CQ !== 'undefined' && CQ.locks) || ''; SAVE.qa = s.qa; } sv(); ev('world:s2p3:quest:done');
    if (typeof window.c2QuestYen === 'function') window.c2QuestYen(QID, Q.n); }
  function qOn() { var q = S().q[QID]; return q != null && q !== 9; }
  function qDone() { return S().q[QID] === 9; }
  function roomOpen() { return on() && punkAfterSeal() && (runsDone() || qOn() || qDone()); }
  function cleared() { return qDone() || stg() === 'gone' || stg() === 'done' || (alreadyClear() && (stg() === 'skip' || stg() === 'done')); }
  P3.Q = Q; P3.stg = stg; P3.setStg = setStg; P3.qOpen = qOpen; P3.qClose = qClose; P3.qOn = qOn; P3.qDone = qDone;
  P3.roomOpen = roomOpen; P3.cleared = cleared; P3.alreadyClear = alreadyClear;

  /* ---------------- voices (new tables only) ---------------- */
  var VO = P3.VO = {};
  VO.door = V3(
    [['nq_kaji', 'Masa\u2019s watch starts at these stairs. You don\u2019t have an errand here.']],
    {
      fierce: [['ryo', 'We\u2019re going up.'], ['aoi', 'Then we go through them.'], ['nq_kaji', 'Fine. You\u2019ll have to take the room.']],
      strategic: [['ryo', 'So you\u2019re watching the stairs.'], ['aoi', 'Then we don\u2019t use the stairs.'], ['nq_kaji', 'You can try the water if you like. We still have the room.']],
      balanced: [['ryo', 'Walk. This is not your building.'], ['aoi', 'You can leave on your feet.'], ['nq_kaji', 'We\u2019re done here. Don\u2019t make me say it twice.']]
    },
    []
  );
  VO.quay = V3(
    [['aoi', 'They\u2019re watching the stairs. We come in from the water.']],
    {
      fierce: [['ryo', 'If they won\u2019t turn, we make them.'], ['nq_kaji', 'Off the quay? You\u2019re serious.']],
      strategic: [['ryo', 'Alley Cat. Don\u2019t let them turn around.'], ['nq_kaji', 'The quay\u2014 damn it\u2014']],
      balanced: [['ryo', 'Last chance. Walk, or we meet you here.'], ['nq_kaji', 'You came around the water to say that?']]
    },
    []
  );
  VO.skip = V3(
    [['aoi', 'The lookouts were already cleared at Lookout Corner.']],
    {
      fierce: [['ryo', 'Empty. Good. The garage is down the quay.']],
      strategic: [['ryo', 'We already did this work. The pin moves to the depot approach.']],
      balanced: [['ryo', 'They\u2019re gone. No one left to walk. The garage is down the quay.']]
    },
    []
  );
  VO.wonFight = V3(
    [['nq_kaji', 'The watch is yours.']],
    {
      fierce: [['nq_kaji', 'Masa still has the garage, down the quay.'], ['ryo', 'Then that\u2019s next.']],
      strategic: [['nq_kaji', 'You came in off the water. That\u2019s a dirty trick.'], ['aoi', 'The garage is still on the depot approach.'], ['ryo', 'We know.']],
      balanced: [['nq_kaji', 'You could have asked first.'], ['ryo', 'We did. The garage is down the quay.']]
    },
    []
  );
  VO.walked = V3(
    [['aoi', 'They walked. The room is ours.']],
    {
      fierce: [['ryo', 'The garage is down the quay. We don\u2019t open it yet.']],
      strategic: [['ryo', 'Lookouts gone without a fight. The garage is on the depot approach.']],
      balanced: [['ryo', 'Good. The garage is down the quay. We don\u2019t open the door yet.']]
    },
    []
  );
  VO.inside = V3(
    [['nq_kaji', 'You came up. That was the choice.']],
    {
      fierce: [['ryo', 'Then we finish it here.']],
      strategic: [['aoi', 'He\u2019s in the room. We should have come off the quay.'], ['ryo', 'We\u2019re here now.']],
      balanced: [['ryo', 'Walk. Last time I ask.'], ['nq_kaji', 'In here? No. Not now.']]
    },
    []
  );
  VO.empty = [ ['', 'The radio is off. The jackets are gone. Someone left a note and did not wait.'] ];

  /* ---------------- sprites + portraits ---------------- */
  if (typeof NM !== 'undefined') NM.nq_kaji = 'Kaji';
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
  wireWho('nq_kaji', 'nq_kaji', 1.04, 'kaji');

  /* ---------------- doors + rooms ---------------- */
  var BOAT_AT = [4830, 3580];
  /* south-quay walkway, not the canal (the old 4100,3720 pin sat in the water) */
  var QUAY_AT = [4780, 3880];
  var GARAGE_AT = [4040, 3900];
  var BOAT_DOOR = { r: [4780, 3480, 4880, 3600], at: BOAT_AT, to: 'boat', out: [BOAT_AT[0], BOAT_AT[1] + 24] };
  var QUAY_SPOT = { r: [4680, 3800, 4920, 3960], at: QUAY_AT };
  var RW = 1280, RH = 900;
  function roomDef(k, n, extra) {
    var id = 'c2_nq_' + k; C2R[k] = id;
    INT[id] = Object.assign({ id: id, n: n, w: RW, h: RH, src: 'world/nq_' + k + '.paint', tiles: 1, cell: 15, dg: 'c2', c2: k, deep: 1, safe: 1, mus: 'c2night', nq: 1, s2: 1,
      open: [[90, 250, 1190, 850], [580, 850, 700, 900]], 'in': [640, 820, 3], back: [640, 820, 3],
      spots: [{ id: 'exit', r: [575, 850, 705, 900], at: [640, 870], face: 0 }] }, extra || {});
    INT[id].base = INT[id].block; TAGS_IN[id] = {};
    return INT[id];
  }
  roomDef('boat', 'Funayado \u00b7 Lookout', { block: [[110, 380, 240, 560], [250, 480, 560, 640], [900, 470, 1160, 560], [980, 700, 1190, 840]],
    spots: [{ id: 'exit', r: [575, 850, 705, 900], at: [640, 870], face: 0 },
      { id: 's2_talk_kaji', r: [600, 480, 820, 620], at: [720, 640], face: 0, lab: 'Talk' }] });
  C2W.doors.nq_boat = BOAT_DOOR;
  if (typeof c2DoorOf === 'function') {
    var door0 = c2DoorOf;
    c2DoorOf = function (k) { if (k === 'boat') return BOAT_DOOR; return door0.apply(this, arguments); };
  }
  if (typeof c2Surf === 'function') {
    var surf0 = c2Surf;
    c2Surf = function (x, y) { var k = c2Room(); if (k === 'boat') return 'wood'; return surf0.apply(this, arguments); };
  }
  INT.c2_town.spots.push({ id: 's2_e_boat', r: BOAT_DOOR.r, at: BOAT_DOOR.at, face: 0, lab: 'Enter' });
  INT.c2_town.spots.push({ id: 's2_qy', r: QUAY_SPOT.r, at: QUAY_SPOT.at, face: 0, lab: 'Flank' });
  if (typeof TRANS !== 'undefined') { TRANS.s2_e_boat = 1; }
  delete INT.c2_town.G;
  P3.BOAT_DOOR = BOAT_DOOR; P3.BOAT_AT = BOAT_AT; P3.QUAY_AT = QUAY_AT; P3.GARAGE_AT = GARAGE_AT;

  /* façade overlay on the east boardwalk, above the flower boat, east of the lobby door */
  var FAC = null;
  function placeDoor() {
    if (!P3.ART || !on() || !inTown() || !roomOpen()) return;
    if (document.getElementById('s2BoatSouth')) return;
    if (!FAC) {
      FAC = document.createElement('canvas'); FAC.width = 360; FAC.height = 440;
      try { if (root.FFF_S2P && root.FFF_S2P.boatSouth) root.FFF_S2P.boatSouth(FAC.getContext('2d')); } catch (eF) { ev('world:s2p3:err:facade:' + (eF && eF.message)); }
    }
    FAC.className = 'nqprop'; FAC.id = 's2BoatSouth';
    FAC.style.cssText = 'position:absolute;left:4540px;top:3420px;width:360px;height:440px;z-index:' + (100 + 3550) + ';pointer-events:none';
    var host = null, sample = document.querySelector('#world .nqprop, #wimap .nqprop, .nqprop');
    if (sample && sample.parentNode) host = sample.parentNode;
    else host = document.getElementById('wisp') || document.getElementById('world') || document.getElementById('wimap');
    if (host) host.appendChild(FAC);
  }
  P3.placeDoor = placeDoor;

  var RCV = {};
  function paintRoom() {
    var k = room();
    var el = document.getElementById('s2P3Room_boat');
    if (el && k !== 'boat' && el.parentNode) el.parentNode.removeChild(el);
    if (k !== 'boat') return;
    var m = document.getElementById('wimap') || document.getElementById('world');
    if (!m) return;
    var key = cleared() ? 'cleared' : 'held';
    if (!RCV[key]) {
      RCV[key] = document.createElement('canvas'); RCV[key].width = RW; RCV[key].height = RH;
      var g = RCV[key].getContext('2d');
      try { if (P3.ART && root.FFF_S2P && root.FFF_S2P.boatLookout) root.FFF_S2P.boatLookout(g, key === 'cleared'); }
      catch (e) { ev('world:s2p3:err:paint:' + (e && e.message)); }
    }
    var c = RCV[key];
    if (c && c.parentNode !== m) { c.className = 'nqprop'; c.id = 's2P3Room_boat'; c.style.cssText = 'position:absolute;left:0;top:0;width:' + RW + 'px;height:' + RH + 'px;z-index:1;pointer-events:none'; m.insertBefore(c, m.firstChild); }
  }
  P3.paintRoom = paintRoom;

  /* battle rooms */
  function hookBattle() {
    if (P3._bt) return true;
    if (!root.FFF_C2BT || !root.FFF_S2P || !root.FFF_S2P.battleLookout || !root.FFF_S2P.battleQuay) return false;
    P3._bt = 1;
    var BT = root.FFF_C2BT;
    BT.ROOMS.lk = { name: 'Funayado \u00b7 Lookout', paint: function (x) { root.FFF_S2P.battleLookout(x); },
      lights: [[180, 90, '255,200,110', 70, 0.3, 'lamp'], [540, 90, '255,200,110', 70, 0.3, 'lamp']], rain: 0, mood: 'room', feet: 52 };
    BT.ROOMS.qy = { name: 'South quay', paint: function (x) { root.FFF_S2P.battleQuay(x); },
      lights: [[120, 200, '255,190,100', 70, 0.32, 'lamp'], [600, 200, '255,190,100', 70, 0.32, 'lamp']], rain: 50, mood: 'rain', feet: 52 };
    BT.KEY.c2_lk = 'lk'; BT.KEY.c2_qy = 'qy';
    var roomB0 = BT.room;
    BT.room = function (story) {
      var ctx = (story && story.ctx) || {}, dgk = String(ctx.dgk || '');
      if (P3.ART && (ctx.s2lk || ctx.s2k === 's2_lk' || /^s2_lk/.test(dgk))) return 'c2_lk';
      if (P3.ART && (ctx.s2qy || ctx.s2k === 's2_qy' || /^s2_qy/.test(dgk))) return 'c2_qy';
      return roomB0.apply(this, arguments);
    };
    return true;
  }
  hookBattle();
  try { later(0, hookBattle); } catch (eB) { try { setTimeout(hookBattle, 0); } catch (eB2) {} }

  /* ---------------- pin / Four Corners ---------------- */
  function s2Tgt() {
    if (!punkAfterSeal() || !runsDone()) return null;
    if (qOn() && (stg() === '' || stg() === 'open')) {
      if (path() === 'strategic' && !alreadyClear()) return { x: QUAY_AT[0], y: QUAY_AT[1], lab: 'Quay flank', loc: 'South quay, behind the watch' };
      return { x: BOAT_AT[0], y: BOAT_AT[1], lab: 'Funayado', loc: 'Above the Boat \u00b7 Lookout' };
    }
    if (qOn() && stg() === 'skip') return { x: BOAT_AT[0], y: BOAT_AT[1], lab: 'Funayado', loc: 'The lookout is empty' };
    if (qDone()) return { x: GARAGE_AT[0], y: GARAGE_AT[1], lab: 'Quay garage', loc: 'Depot approach' };
    return null;
  }
  P3.s2Tgt = s2Tgt;
  if (typeof c2LocksT === 'function') {
    var lt0 = c2LocksT;
    c2LocksT = function () {
      try { var t = s2Tgt(); if (t) return { room: 'town', x: t.x, y: t.y, lab: t.lab, loc: t.loc }; } catch (eL) {}
      return lt0.apply(this, arguments);
    };
  }

  function chainRepair() {
    if (!punkAfterSeal() || !runsDone()) return;
    if (!qOn() && !qDone()) { qOpen(); if (!stg()) setStg('open'); }
  }
  P3.chainRepair = chainRepair;

  /* ---------------- pops ---------------- */
  var KAJI = null, KAJI_OUT = null;
  function popLookout() {
    if (room() !== 'boat') { if (KAJI) { try { kill(KAJI); } catch (eK) {} KAJI = null; } return; }
    if (cleared() || alreadyClear()) { if (KAJI) { try { kill(KAJI); } catch (eK) {} KAJI = null; } return; }
    if (KAJI && KAJI.el && KAJI.el.parentNode) return;
    KAJI = npc('nq_kaji', 720, 560, Math.PI / 2);
    try { if (typeof waddle === 'function') waddle(KAJI, 0, Math.PI / 2); } catch (eW) {}
    try { if (W.c2n) W.c2n.s2kaji = KAJI; } catch (eN) {}
  }
  function popTown() {
    if (!inTown() || !qOn() || cleared() || alreadyClear()) {
      if (KAJI_OUT) { try { kill(KAJI_OUT); } catch (eK) {} KAJI_OUT = null; } return;
    }
    if (KAJI_OUT && KAJI_OUT.el && KAJI_OUT.el.parentNode) return;
    /* at the door, facing west along the boardwalk \u2014 the quay is behind him */
    KAJI_OUT = npc('nq_kaji', 4780, 3570, Math.PI);
    try { if (typeof waddle === 'function') waddle(KAJI_OUT, 0, Math.PI); } catch (eW) {}
  }

  /* ---------------- talks + fights ---------------- */
  var fighting = 0;
  function startLookoutFight() {
    if (fighting || busy()) return;
    fighting = 1;
    lockIn(0);
    var ctx = { dg: 'c2', dgk: 's2_lk_0', dgks: ['s2_lk_0', 's2_lk_1'], s2k: 's2_lk', s2: 1, s2lk: 1 };
    try { fight(['nq_kaji', 'c2_boso'], false, ctx); } catch (eF) { fighting = 0; ev('world:s2p3:err:fight:' + (eF && eF.message)); }
  }
  function startQuayFight() {
    if (fighting || busy()) return;
    fighting = 1;
    lockIn(0);
    var ctx = { dg: 'c2', dgk: 's2_qy_0', dgks: ['s2_qy_0', 's2_qy_1'], s2k: 's2_qy', s2: 1, s2qy: 1, freeOpen: 1 };
    try { fight(['nq_kaji', 'c2_boso'], false, ctx); } catch (eF) { fighting = 0; ev('world:s2p3:err:fight:' + (eF && eF.message)); }
  }
  function finishQuest() {
    setStg('done');
    qClose();
    /* pin moves to the garage; do not open unbuilt Phase 4. */
  }
  function fightWon() {
    fighting = 0;
    whenFree(function () {
      talk(pv(VO.wonFight), function () { finishQuest(); });
    });
  }
  function playSkip() {
    if (busy()) return;
    lockIn(1);
    talk(pv(VO.skip), function () { lockIn(0); setStg('skip'); finishQuest(); });
  }
  function doorTalk() {
    if (busy()) return true;
    if (alreadyClear()) { playSkip(); return true; }
    if (qDone() || cleared()) {
      lockIn(1); talk(VO.empty, function () { lockIn(0); }); return true;
    }
    if (!qOn()) return false;
    lockIn(1);
    if (path() === 'balanced') {
      talk(pv(VO.door), function () {
        lockIn(0);
        setStg('gone');
        qStep(1);
        whenFree(function () { talk(pv(VO.walked), function () { finishQuest(); }); });
      });
    } else if (path() === 'fierce') {
      talk(pv(VO.door), function () { lockIn(0); startLookoutFight(); });
    } else {
      /* strategic at the door: he is watching the stairs; the fight is on the quay */
      talk(pv(VO.door), function () { lockIn(0); });
    }
    return true;
  }
  function insideTalk() {
    if (busy()) return true;
    if (alreadyClear() || qDone() || cleared()) {
      if (alreadyClear() && qOn()) { playSkip(); return true; }
      lockIn(1); talk(VO.empty, function () { lockIn(0); }); return true;
    }
    if (!qOn()) return false;
    lockIn(1);
    if (path() === 'balanced') {
      talk(pv(VO.inside), function () {
        lockIn(0);
        /* they will not walk once you are in the room */
        startLookoutFight();
      });
    } else {
      talk(pv(VO.inside), function () { lockIn(0); startLookoutFight(); });
    }
    return true;
  }
  function quayTalk() {
    if (busy()) return true;
    if (!qOn() || alreadyClear() || cleared()) return false;
    lockIn(1);
    talk(pv(VO.quay), function () { lockIn(0); startQuayFight(); });
    return true;
  }

  if (typeof onFightEnd === 'function') {
    var of0 = onFightEnd;
    onFightEnd = function (win, c) {
      var r = of0.apply(this, arguments);
      try {
        if (c && (c.s2k === 's2_lk' || c.s2k === 's2_qy')) {
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
          if (t.key.indexOf(':s2_e_boat') >= 0) return roomOpen();
          if (t.key.indexOf(':s2_qy') >= 0) return qOn() && !alreadyClear() && !cleared() && path() === 'strategic';
          if (t.key.indexOf(':s2_talk_kaji') >= 0) return room() === 'boat' && !cleared();
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
          if (a === 's2_e_boat') {
            if (alreadyClear() && qOn() && stg() !== 'skip') {
              /* let them enter, then the empty room plays the skip */
              later(400, function () { if (room() === 'boat' && qOn()) playSkip(); });
            }
            return act0.apply(this, arguments);
          }
          if (a === 's2_qy') { quayTalk(); return true; }
          if (a === 's2_talk_kaji') { insideTalk(); return true; }
        }
      } catch (e) { ev('world:s2p3:err:act:' + (e && e.message)); }
      return act0.apply(this, arguments);
    };
  }
  if (typeof c2Talk === 'function') {
    var tk0 = c2Talk;
    c2Talk = function (s) {
      try {
        if (on() && s) {
          var id = s.s2id || s.id || (s.el && s.el.dataset && s.el.dataset.npc);
          if (id === 'nq_kaji') {
            if (room() === 'boat') return insideTalk();
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
          if (id === 'nq_kaji') {
            if (room() === 'boat') return insideTalk();
            return doorTalk();
          }
        }
      } catch (eT) {}
      return tn0.apply(this, arguments);
    };
  }

  if (typeof c2Frame === 'function') {
    var fr0 = c2Frame;
    c2Frame = function (dt) { fr0.apply(this, arguments); try { if (on()) { placeDoor(); popTown(); } } catch (e) { if (!P3.ferr) { P3.ferr = 1; ev('world:s2p3:err:frame:' + (e && e.message)); } } };
  }
  if (typeof c2Pop === 'function') {
    var pop0 = c2Pop;
    c2Pop = function () { pop0.apply(this, arguments); try { if (on()) { chainRepair(); placeDoor(); hookBattle(); popLookout(); popTown(); if (room() === 'boat') paintRoom(); } } catch (eP) {} };
  }
  try { chainRepair(); } catch (eC) {}
  ev('world:s2p3:ready');
  } catch (eS2) { try { ev('world:s2p3:err:init:' + (eS2 && eS2.message)); console.warn('S2P3 init', eS2); } catch (e2) {} }
})();
