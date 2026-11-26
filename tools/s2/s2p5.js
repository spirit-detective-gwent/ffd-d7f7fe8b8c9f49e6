/* v6.5.63 FFF_S2P5 (Punk-route seal 2, phase 5): Masa's Seal.
 * Quest cq2_s2_depot after Off Schedule. 13 walkable depot rooms, meet Masa
 * at the yard gate, fight him at the lift shutter with CHAR_INTRO.mb2_depot.
 * Path voice only in this file — the bond pick and east-block flip come later.
 * Wraps only; no new always-running loops. Does not edit S2 / S2P2 / S2P3 / S2P4 VO
 * or the landmark depot path. */
(function () {
  try {
  if (typeof c2S !== 'function' || typeof C2W === 'undefined' || !C2W || typeof INT === 'undefined' || !INT.c2_town) {
    try { ev('world:s2p5:skip'); } catch (e0) {} return;
  }
  var root = typeof window !== 'undefined' ? window : this;
  var P4 = root.FFF_S2P4;
  var P5 = root.FFF_S2P5 = { v: 1, ART: true };

  function on() { return (typeof c2On !== 'function' || c2On()) && (typeof chN !== 'function' || chN() === 2); }
  function S() { return c2S(); }
  function E() { return c2S().e; }
  function room() { try { return c2Room(); } catch (e) { return null; } }
  function inTown() { return room() === 'town'; }
  function nailsRun() { return on() && E().run_fac === 'arc'; }
  function busy() { return !!(W.dgFight || W.dlg || W.busy || W.cut || W.fading || W.paused); }
  function later(ms, fn) { setTimeout(function () { try { fn(); } catch (e) { ev('world:s2p5:err:later:' + (e && e.message)); } }, ms); }
  function talk(lines, done) { W.dlg = true; scene(null, lines, function () { W.dlg = false; if (done) done(); }); }
  function lockIn(on1) { if (on1) { W.cut = true; W.path = []; if (W.ryo) W.ryo.v = 0; try { stickEnd(); } catch (e) {} } else W.cut = false; }
  function sv() { try { if (typeof c2QSync === 'function') c2QSync(); } catch (e) {} save(); }
  function path() { var p = 'balanced'; try { p = c2Path(); } catch (e) {} return p === 'fierce' || p === 'strategic' ? p : 'balanced'; }
  function npc(id, x, y, fa) { var s = c2Npc(id, x, y, fa == null ? Math.PI / 2 : fa); s.el.classList.add('s2'); s.s2id = id; s.el.dataset.npc = id; return s; }
  function kill(s) { if (s && s.el && s.el.parentNode) s.el.remove(); if (s) s.gone = 1; }
  function whenFree(fn, tries) { tries = tries || 0; if (!busy() && !document.getElementById('nqsting') && !(typeof W.c2busy !== 'undefined' && W.c2busy)) { try { fn(); } catch (e) { ev('world:s2p5:err:free:' + (e && e.message)); } return; } later(tries < 120 ? 250 : 1000, function () { whenFree(fn, tries + 1); }); }
  function V3(pre, mid, post) { var o = {}, PP = ['fierce', 'strategic', 'balanced']; PP.forEach(function (p) { o[p] = (pre || []).concat(mid[p] || [], post || []); }); return o; }
  function pv(x) { try { return typeof pathLines === 'function' ? pathLines(x) : (x[path()] || x.balanced || x); } catch (e) { return x.balanced || []; } }
  function p4Done() { return P4 && typeof P4.qDone === 'function' && P4.qDone(); }
  function punkAfterSeal() { return on() && nailsRun() && !!E().seal_sento; }

  /* ---------------- state ---------------- */
  function NS() { var e = E(); if (!e.nq || typeof e.nq !== 'object') e.nq = {}; return e.nq; }
  function stg() { return NS().dep || ''; }
  function setStg(v) { NS().dep = v; sv(); ev('world:s2p5:st:' + v); }
  var QID = 'cq2_s2_depot';
  var Q = { id: QID, n: 'Masa\u2019s Seal', giver: 'Masa, at the yard gate',
    quote: 'The depot door is open. Masa is in the yard. The seal is on the lift shutter.',
    loc: 'Kitsune-Ch\u016b\u014d \u00b7 Subway Freight Depot' };
  if (typeof C2Q !== 'undefined') C2Q[QID] = { n: Q.n, steps: [Q.quote] };
  if (typeof C2QLOC !== 'undefined') C2QLOC[QID] = ['town', Q.loc];
  function qOpen() { var s = S(); if (s.q[QID] == null) s.q[QID] = 0; SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = s.q[QID] | 0; s.qa = QID; SAVE.qa = QID; SAVE.qTrack = ''; SAVE.qTrackPick = 0; sv(); ev('world:s2p5:quest:open'); }
  function qStep(n) { var s = S(); if (s.q[QID] == null || s.q[QID] === 9) return; s.q[QID] = Math.max(s.q[QID] | 0, n); SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = s.q[QID]; sv(); }
  function qClose() { var s = S(); if (s.q[QID] == null || s.q[QID] === 9) return; s.q[QID] = 9; SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = 9;
    SAVE.journalLog = SAVE.journalLog || []; if (SAVE.journalLog.indexOf(Q.n) < 0) SAVE.journalLog.push(Q.n);
    if (s.qa === QID) { s.qa = (typeof CQ !== 'undefined' && CQ.locks) || ''; SAVE.qa = s.qa; } sv(); ev('world:s2p5:quest:done');
    if (typeof window.c2QuestYen === 'function') window.c2QuestYen(QID, Q.n); }
  function qOn() { var q = S().q[QID]; return q != null && q !== 9; }
  function qDone() { return S().q[QID] === 9; }
  function p5Enter() { return on() && punkAfterSeal() && p4Done(); }
  function roomOpen() { return p5Enter(); }
  function met() { return stg() === 'met' || stg() === 'won' || stg() === 'done' || qDone(); }
  function won() { return stg() === 'won' || stg() === 'done' || qDone(); }
  function cleared() { return qDone() || stg() === 'done'; }
  P5.Q = Q; P5.stg = stg; P5.setStg = setStg; P5.qOpen = qOpen; P5.qClose = qClose; P5.qOn = qOn; P5.qDone = qDone;
  P5.p5Enter = p5Enter; P5.roomOpen = roomOpen; P5.met = met; P5.won = won; P5.cleared = cleared;

  /* ---------------- voices (new tables only) ---------------- */
  var VO = P5.VO = {};
  VO.yard = V3(
    [['mb2_depot', 'You used a late load to walk my yard.']],
    {
      fierce: [['ryo', 'We came to put you on the floor, Masa.'], ['aoi', 'The shutter first. Then him.'], ['mb2_depot', 'The shutter is mine. You want it, you come get it.']],
      strategic: [['ryo', 'The shutter, the seal, the paperwork. That is the visit.'], ['aoi', 'The manifest is still on the way.'], ['mb2_depot', 'You read a board. You have not read the yard.']],
      balanced: [['ryo', 'We came to end the gray-coat schedule. Not the men who punch the clock.'], ['aoi', 'The freight can still leave honest.'], ['mb2_depot', 'Honest freight still goes through me. The shutter stays shut.']]
    },
    []
  );
  VO.shutter = V3(
    [['mb2_depot', 'End of the line. The lift does not move without my seal.']],
    {
      fierce: [['ryo', 'Then we take it here.'], ['mb2_depot', '{shout}Off my dock, kid!{/shout}']],
      strategic: [['ryo', 'The manifest is already on that shutter.'], ['aoi', 'The code and the time are on the sheet.'], ['mb2_depot', 'You do not use my paperwork against me.']],
      balanced: [['ryo', 'Stand aside. The yard can run without a gray seal on the lift.'], ['mb2_depot', 'I said no. The schedule never stops.']]
    },
    []
  );
  VO.wonFight = V3(
    [['mb2_depot', 'Freight\u2019s\u2026 late.']],
    {
      fierce: [['ryo', 'The shutter is ours.'], ['aoi', 'He is down.']],
      strategic: [['aoi', 'The seal and the manifest are on the shutter.'], ['ryo', 'We have them.']],
      balanced: [['ryo', 'The schedule stops here.'], ['aoi', 'The men on the clock can go home.']]
    },
    []
  );
  VO.emptyYard = [['', 'The desk is empty. Masa is not at the gate.']];
  VO.emptyShut = [['', 'The lift shutter is quiet. The gray seal is still on the sheet.']];

  /* ---------------- rooms ---------------- */
  var RW = 1280, RH = 900;
  var DEPOT_AT = [4300, 3840];
  var DEPOT_DOOR = { r: [4180, 3770, 4420, 3800], at: DEPOT_AT, to: 'dyard', out: [4300, 3880] };
  var KEYS = ['dyard', 'dclock', 'dbay', 'dcrate', 'dcold', 'dcage', 'dbike', 'dloft', 'dbreak', 'dtun', 'dman', 'dant', 'dshut'];
  var PAINT = {
    dyard: 'depYard', dclock: 'depClock', dbay: 'depBay', dcrate: 'depCrates',
    dcold: 'depCold', dcage: 'depCage', dbike: 'depBikes', dloft: 'depLoft',
    dbreak: 'depBreak', dtun: 'depTunnel', dman: 'depManifest', dant: 'depAntero',
    dshut: 'depShutter'
  };
  var NAMES = {
    dyard: 'Yard gate \u00b7 \u9580', dclock: 'Time clock \u00b7 \u6253\u523b', dbay: 'Loading bay \u00b7 \u8377\u5f79',
    dcrate: 'Crate stacks \u00b7 \u8ca0\u7269', dcold: 'Cold store \u00b7 \u51b7\u51cd', dcage: 'Parts cage \u00b7 \u90e8\u54c1',
    dbike: 'Bike bay \u00b7 \u99d0\u8f2a', dloft: 'Dispatch loft \u00b7 \u914d\u8eca', dbreak: 'Break room \u00b7 \u4f11\u61a9',
    dtun: 'Tunnel spur \u00b7 \u6a2a\u5751', dman: 'Manifest office \u00b7 \u7a4d\u8377', dant: 'Lift anteroom \u00b7 \u6607\u964d\u6a5f\u524d',
    dshut: 'Lift shutter \u00b7 \u30b7\u30e3\u30c3\u30bf\u30fc'
  };
  /* south exit of each inner room returns here; yard exit goes to town */
  var BACK = {
    dclock: 'dyard', dbay: 'dyard', dcrate: 'dbay', dcold: 'dcrate', dcage: 'dcold',
    dbike: 'dbay', dloft: 'dbike', dbreak: 'dloft', dtun: 'dbreak', dman: 'dtun',
    dant: 'dman', dshut: 'dant'
  };
  /* arrive at the parent when walking out the south */
  var BACK_AT = {
    dclock: [945, 320, 0], dbay: [1065, 320, 0], dcrate: [1100, 700, 1], dcold: [1095, 320, 0],
    dcage: [200, 320, 0], dbike: [200, 700, 2], dloft: [655, 300, 0], dbreak: [1095, 320, 0],
    dtun: [1095, 320, 0], dman: [1105, 320, 0], dant: [1065, 320, 0], dshut: [640, 400, 0]
  };
  function doorSpot(id, x, lab, face) {
    return { id: id, r: [x, 70, x + 90, 300], at: [x + 45, 310], face: face == null ? 3 : face, lab: lab };
  }
  var BLOCKS = {
    dyard: [[110, 460, 280, 600], [110, 680, 280, 820], [860, 480, 1180, 700]],
    dclock: [[140, 360, 250, 680], [400, 540, 700, 700], [860, 390, 1180, 600]],
    dbay: [[110, 500, 340, 820], [860, 400, 1180, 820]],
    dcrate: [[110, 400, 480, 840], [820, 400, 1180, 840]],
    dcold: [[110, 350, 330, 680], [960, 350, 1180, 680], [320, 700, 460, 820], [820, 700, 960, 820]],
    dcage: [[110, 540, 300, 680], [300, 70, 980, 620], [980, 680, 1180, 840]],
    dbike: [[110, 540, 360, 840], [900, 540, 1180, 840], [400, 350, 600, 470]],
    dloft: [[180, 540, 500, 690], [740, 500, 1040, 640]],
    dbreak: [[110, 500, 340, 840], [1000, 350, 1180, 680]],
    dtun: [[110, 600, 260, 840], [1000, 680, 1180, 840]],
    dman: [[110, 620, 280, 820], [400, 540, 740, 700], [1040, 490, 1180, 800]],
    dant: [[110, 600, 300, 840], [900, 470, 1180, 840]],
    dshut: [[110, 540, 300, 840], [880, 480, 1180, 840]]
  };
  function roomDef(k, extra) {
    var id = 'c2_nq_' + k; C2R[k] = id;
    var spots = [{ id: 'exit', r: [575, 850, 705, 900], at: [640, 870], face: 0 }];
    if (extra && extra.spots) spots = spots.concat(extra.spots);
    INT[id] = Object.assign({ id: id, n: NAMES[k], w: RW, h: RH, src: 'world/nq_' + k + '.paint', tiles: 1, cell: 15, dg: 'c2', c2: k, deep: 1, safe: 1, mus: 'c2night', nq: 1, s2: 1, s2dep: 1,
      open: [[90, 250, 1190, 850], [580, 850, 700, 900]], 'in': [640, 820, 3], back: [640, 820, 3],
      block: BLOCKS[k] || [], spots: spots }, extra || {});
    INT[id].spots = spots;
    INT[id].base = INT[id].block;
    TAGS_IN[id] = {};
    return INT[id];
  }

  roomDef('dyard', { spots: [
    doorSpot('s2_d_clock', 900, '\u6253\u523b'),
    doorSpot('s2_d_bay', 1020, '\u8377\u5f79'),
    { id: 's2_talk_masa', r: [400, 580, 660, 760], at: [530, 790], face: 0, lab: 'Talk' }
  ] });
  roomDef('dclock');
  roomDef('dbay', { spots: [
    doorSpot('s2_d_clock', 140, '\u6253\u523b'),
    { id: 's2_d_crate', r: [1080, 400, 1190, 700], at: [1060, 700], face: 1, lab: '\u8ca0\u7269' },
    { id: 's2_d_bike', r: [90, 400, 200, 700], at: [220, 700], face: 2, lab: '\u99d0\u8f2a' }
  ] });
  roomDef('dcrate', { spots: [
    doorSpot('s2_d_bay', 140, '\u8377\u5f79'),
    doorSpot('s2_d_cold', 1050, '\u51b7\u51cd')
  ] });
  roomDef('dcold', { spots: [
    { id: 's2_d_crate', r: [140, 70, 250, 300], at: [195, 310], face: 3, lab: '\u8ca0\u7269' },
    { id: 's2_d_cage', r: [1080, 400, 1190, 700], at: [1060, 700], face: 1, lab: '\u90e8\u54c1' }
  ] });
  roomDef('dcage', { spots: [doorSpot('s2_d_cold', 140, '\u51b7\u51cd')] });
  roomDef('dbike', { spots: [doorSpot('s2_d_loft', 620, '\u914d\u8eca')] });
  roomDef('dloft', { spots: [doorSpot('s2_d_break', 1050, '\u4f11\u61a9')] });
  roomDef('dbreak', { spots: [doorSpot('s2_d_tun', 1050, '\u6a2a\u5751')] });
  roomDef('dtun', { spots: [
    doorSpot('s2_d_break', 140, '\u4f11\u61a9'),
    doorSpot('s2_d_man', 1070, '\u7a4d\u8377')
  ] });
  roomDef('dman', { spots: [
    doorSpot('s2_d_tun', 900, '\u6a2a\u5751'),
    doorSpot('s2_d_ant', 1020, '\u6607\u964d')
  ] });
  roomDef('dant', { spots: [
    doorSpot('s2_d_man', 140, '\u7a4d\u8377'),
    { id: 's2_d_shut', r: [400, 70, 880, 320], at: [640, 340], face: 3, lab: '\u30b7\u30e3\u30c3\u30bf\u30fc' }
  ] });
  roomDef('dshut', { spots: [
    { id: 's2_talk_masa', r: [520, 520, 760, 760], at: [640, 800], face: 0, lab: 'Talk' }
  ] });

  if (typeof TRANS !== 'undefined') {
    ['s2_d_clock', 's2_d_bay', 's2_d_crate', 's2_d_cold', 's2_d_cage', 's2_d_bike',
      's2_d_loft', 's2_d_break', 's2_d_tun', 's2_d_man', 's2_d_ant', 's2_d_shut'].forEach(function (id) { TRANS[id] = 1; });
  }
  if (typeof c2DoorOf === 'function') {
    var door0 = c2DoorOf;
    c2DoorOf = function (k) { if (k === 'dyard') return DEPOT_DOOR; return door0.apply(this, arguments); };
  }
  if (typeof c2Surf === 'function') {
    var surf0 = c2Surf;
    c2Surf = function (x, y) { var k = c2Room(); if (KEYS.indexOf(k) >= 0) return 'concrete'; return surf0.apply(this, arguments); };
  }
  P5.KEYS = KEYS; P5.DEPOT_DOOR = DEPOT_DOOR; P5.DEPOT_AT = DEPOT_AT; P5.BACK = BACK;

  var GO = {
    s2_d_clock: ['dclock', [640, 820, 3]],
    s2_d_bay: ['dbay', [640, 820, 3]],
    s2_d_crate: ['dcrate', [640, 820, 3]],
    s2_d_cold: ['dcold', [640, 820, 3]],
    s2_d_cage: ['dcage', [640, 820, 3]],
    s2_d_bike: ['dbike', [640, 820, 3]],
    s2_d_loft: ['dloft', [640, 820, 3]],
    s2_d_break: ['dbreak', [640, 820, 3]],
    s2_d_tun: ['dtun', [640, 820, 3]],
    s2_d_man: ['dman', [640, 820, 3]],
    s2_d_ant: ['dant', [640, 820, 3]],
    s2_d_shut: ['dshut', [640, 820, 3]]
  };
  /* when the same action id is used from two rooms, pick by current room */
  var GO_FROM = {
    dbay: { s2_d_clock: ['dclock', [640, 820, 3]] },
    dcrate: { s2_d_bay: ['dbay', [1100, 700, 1]] },
    dcold: { s2_d_crate: ['dcrate', [1095, 320, 0]] },
    dcage: { s2_d_cold: ['dcold', [1100, 700, 1]] },
    dloft: {},
    dbreak: {},
    dtun: { s2_d_break: ['dbreak', [1095, 320, 0]] },
    dman: { s2_d_tun: ['dtun', [1105, 320, 0]] },
    dant: { s2_d_man: ['dman', [1065, 320, 0]] }
  };
  function goDoor(a) {
    var k = room(), pair = (GO_FROM[k] && GO_FROM[k][a]) || GO[a];
    if (!pair) return false;
    try { if (typeof c2Go === 'function') c2Go(pair[0], pair[1]); } catch (eG) { ev('world:s2p5:err:go:' + (eG && eG.message)); }
    return true;
  }
  function goBack() {
    var k = room(), to = BACK[k];
    if (!to) return false;
    try { if (typeof c2Go === 'function') c2Go(to, BACK_AT[k] || [640, 820, 3]); } catch (eG) { ev('world:s2p5:err:back:' + (eG && eG.message)); }
    return true;
  }
  function inDepot() { return KEYS.indexOf(room()) >= 0; }

  /* ---------------- paint ---------------- */
  var RCV = {};
  function paintRoom() {
    var k = room();
    KEYS.forEach(function (rk) {
      var el = document.getElementById('s2P5Room_' + rk);
      if (el && k !== rk && el.parentNode) el.parentNode.removeChild(el);
    });
    if (KEYS.indexOf(k) < 0) return;
    var m = document.getElementById('wimap') || document.getElementById('world');
    if (!m) return;
    var key = k + ':' + (cleared() || (k === 'dshut' && won()) ? 'cleared' : 'held');
    if (!RCV[key]) {
      RCV[key] = document.createElement('canvas'); RCV[key].width = RW; RCV[key].height = RH;
      var g = RCV[key].getContext('2d'), fn = PAINT[k];
      try { if (P5.ART && root.FFF_S2P && fn && root.FFF_S2P[fn]) root.FFF_S2P[fn](g, key.indexOf('cleared') >= 0); }
      catch (e) { ev('world:s2p5:err:paint:' + (e && e.message)); }
    }
    var c = RCV[key];
    if (c && c.parentNode !== m) {
      c.className = 'nqprop'; c.id = 's2P5Room_' + k;
      c.style.cssText = 'position:absolute;left:0;top:0;width:' + RW + 'px;height:' + RH + 'px;z-index:1;pointer-events:none';
      m.insertBefore(c, m.firstChild);
    }
  }
  P5.paintRoom = paintRoom;

  /* ---------------- battle ---------------- */
  function hookBattle() {
    if (P5._bt) return true;
    if (!root.FFF_C2BT || !root.FFF_S2P || !root.FFF_S2P.battleShutter) return false;
    P5._bt = 1;
    var BT = root.FFF_C2BT;
    BT.ROOMS.sh = { name: 'Lift shutter', paint: function (x) { root.FFF_S2P.battleShutter(x); },
      lights: [[120, 90, '255,200,110', 70, 0.3, 'lamp'], [600, 90, '255,200,110', 70, 0.3, 'lamp']], rain: 0, mood: 'room' };
    BT.KEY.c2_sh = 'sh';
    var roomB0 = BT.room;
    BT.room = function (story) {
      var ctx = (story && story.ctx) || {}, dgk = String(ctx.dgk || '');
      if (P5.ART && (ctx.s2sh || ctx.s2k === 's2_sh' || /^s2_sh/.test(dgk))) return 'c2_sh';
      return roomB0.apply(this, arguments);
    };
    return true;
  }
  hookBattle();
  try { later(0, hookBattle); } catch (eB) { try { setTimeout(hookBattle, 0); } catch (eB2) {} }

  /* ---------------- pin ---------------- */
  function s2Tgt() {
    if (!p5Enter()) return null;
    if (qDone() || stg() === 'done') return null;
    if (qOn() && !met()) return { x: DEPOT_AT[0], y: DEPOT_AT[1], lab: 'Yard gate', loc: 'Masa\u2019s Seal \u00b7 the yard', room: 'town' };
    if (qOn() && met() && !won()) {
      if (inDepot()) return { x: 640, y: 620, lab: 'Lift shutter', loc: 'Masa\u2019s Seal \u00b7 the shutter', room: 'dshut' };
      return { x: DEPOT_AT[0], y: DEPOT_AT[1], lab: 'Lift shutter', loc: 'Masa\u2019s Seal \u00b7 the shutter', room: 'town' };
    }
    return null;
  }
  P5.s2Tgt = s2Tgt;
  if (typeof c2LocksT === 'function') {
    var lt0 = c2LocksT;
    c2LocksT = function () {
      try { var t = s2Tgt(); if (t) return t; } catch (eL) {}
      return lt0.apply(this, arguments);
    };
  }

  function chainRepair() {
    if (!p5Enter()) return;
    var ch = 0;
    if (!qOn() && !qDone()) { qOpen(); if (!stg()) setStg('open'); ch = 1; }
    if (ch) ev('world:s2p5:repair');
  }
  P5.chainRepair = chainRepair;

  /* ---------------- enter: punk path uses the 13 rooms, not the landmark hall ---------------- */
  function enterYard() {
    if (W.fading) return;
    W.path = []; W.dlg = true; ev('world:c2:enter:dyard');
    try {
      intFade(function () {
        W.dlg = false;
        c2Go('dyard');
        try { AU.play('door', { gain: 0.55 }); } catch (eA) {}
      }, function () {});
    } catch (eE) {
      W.dlg = false;
      try { c2Go('dyard'); } catch (e2) { ev('world:s2p5:err:enter:' + (e2 && e2.message)); }
    }
  }
  P5.enterYard = enterYard;
  if (typeof c2Enter === 'function') {
    var enter0 = c2Enter;
    c2Enter = function (k) {
      try { if (k === 'depot' && p5Enter()) { chainRepair(); enterYard(); return; } } catch (eE) { ev('world:s2p5:err:c2enter:' + (eE && eE.message)); }
      return enter0.apply(this, arguments);
    };
  }

  /* ---------------- pops ---------------- */
  var MASA = null;
  function popMasa() {
    var k = room();
    var want = null;
    if (k === 'dyard' && qOn() && !met()) want = [500, 700, Math.PI / 2];
    if (k === 'dshut' && qOn() && met() && !won()) want = [640, 620, Math.PI / 2];
    if (!want) { if (MASA) { try { kill(MASA); } catch (eK) {} MASA = null; } return; }
    if (MASA && MASA.el && MASA.el.parentNode && MASA._rk === k) {
      try { if (!W.c2n) W.c2n = {}; W.c2n.s2masa = MASA; } catch (eN) {}
      return;
    }
    if (MASA) { try { kill(MASA); } catch (eK) {} MASA = null; }
    MASA = npc('mb2_depot', want[0], want[1], want[2]);
    MASA._rk = k;
    try { if (typeof waddle === 'function') waddle(MASA, 0, want[2]); } catch (eW) {}
    try { if (!W.c2n) W.c2n = {}; W.c2n.s2masa = MASA; } catch (eN) {}
  }

  /* ---------------- talks + fight ---------------- */
  var fighting = 0;
  function startShutterFight() {
    if (fighting || busy()) return;
    fighting = 1;
    lockIn(0);
    var ctx = { dg: 'c2', dgk: 's2_sh_0', dgks: ['s2_sh_0', 's2_sh_1', 's2_sh_2'], s2k: 's2_sh', s2: 1, s2sh: 1 };
    try { fight(['mb2_depot', 'c2_boso', 'c2_boso'], false, ctx); } catch (eF) { fighting = 0; ev('world:s2p5:err:fight:' + (eF && eF.message)); }
  }
  function introThenFight() {
    var lines = pv(VO.shutter);
    function go() { startShutterFight(); }
    try {
      if (typeof bossEnt === 'function') {
        if (MASA) W.bentS = { id: 'mb2_depot', s: MASA };
        bossEnt('mb2_depot', lines, function () { lockIn(0); go(); }, { spr: MASA });
        return;
      }
    } catch (eI) { ev('world:s2p5:err:intro:' + (eI && eI.message)); }
    talk(lines, function () { lockIn(0); go(); });
  }
  function fightWon() {
    fighting = 0;
    setStg('won');
    qStep(2);
    whenFree(function () {
      talk(pv(VO.wonFight), function () {
        /* after-win beats and the east-block flip land in the next stage */
      });
    });
  }
  function yardTalk() {
    if (busy()) return true;
    if (won() || cleared()) { lockIn(1); talk(VO.emptyYard, function () { lockIn(0); }); return true; }
    if (met()) { lockIn(1); talk(VO.emptyYard, function () { lockIn(0); }); return true; }
    if (!qOn()) return false;
    lockIn(1);
    talk(pv(VO.yard), function () {
      setStg('met'); qStep(1);
      if (MASA) { try { kill(MASA); } catch (eK) {} MASA = null; }
      lockIn(0);
    });
    return true;
  }
  function shutterTalk() {
    if (busy()) return true;
    if (won() || cleared()) { lockIn(1); talk(VO.emptyShut, function () { lockIn(0); }); return true; }
    if (!qOn()) return false;
    if (!met()) { setStg('met'); qStep(1); }
    lockIn(1);
    introThenFight();
    return true;
  }

  if (typeof onFightEnd === 'function') {
    var of0 = onFightEnd;
    onFightEnd = function (win, c) {
      var r = of0.apply(this, arguments);
      try {
        if (c && c.s2k === 's2_sh') {
          if (!win) { fighting = 0; return r; }
          fightWon();
        }
      } catch (eE) {}
      return r;
    };
  }

  if (typeof c2ActC === 'function') {
    var act0 = c2ActC;
    c2ActC = function (k, a) {
      try {
        if (on()) {
          if (a === 'lk_depot' && p5Enter()) { chainRepair(); enterYard(); return true; }
          if (a === 'exit' && inDepot() && room() !== 'dyard') { goBack(); return true; }
          if (a && a.indexOf('s2_d_') === 0) { goDoor(a); return true; }
          if (a === 's2_talk_masa') {
            if (room() === 'dshut') return shutterTalk();
            return yardTalk();
          }
        }
      } catch (e) { ev('world:s2p5:err:act:' + (e && e.message)); }
      return act0.apply(this, arguments);
    };
  }
  if (typeof c2Talk === 'function') {
    var tk0 = c2Talk;
    c2Talk = function (s) {
      try {
        if (on() && s) {
          var id = s.s2id || s.id || (s.el && s.el.dataset && (s.el.dataset.npc || s.el.dataset.who));
          if (id === 'mb2_depot' && inDepot()) {
            if (room() === 'dshut') return shutterTalk();
            return yardTalk();
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
          if (id === 'mb2_depot' && inDepot()) {
            if (room() === 'dshut') return shutterTalk();
            return yardTalk();
          }
        }
      } catch (eT) {}
      return tn0.apply(this, arguments);
    };
  }

  if (typeof c2Frame === 'function') {
    var fr0 = c2Frame;
    c2Frame = function (dt) { fr0.apply(this, arguments); try { hookBattle(); if (on()) chainRepair(); } catch (e) { if (!P5.ferr) { P5.ferr = 1; ev('world:s2p5:err:frame:' + (e && e.message)); } } };
  }
  if (typeof c2Pop === 'function') {
    var pop0 = c2Pop;
    c2Pop = function () { pop0.apply(this, arguments); try { if (on()) { chainRepair(); hookBattle(); popMasa(); if (inDepot()) paintRoom(); } } catch (eP) {} };
  }
  try { chainRepair(); } catch (eC) {}
  ev('world:s2p5:ready');
  } catch (eS2) { try { ev('world:s2p5:err:init:' + (eS2 && eS2.message)); console.warn('S2P5 init', eS2); } catch (e2) {} }
})();
