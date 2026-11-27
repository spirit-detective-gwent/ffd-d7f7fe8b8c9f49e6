/* v6.5.63 FFF_S2P5 (Punk-route seal 2, phase 5): Masa's Seal.
 * Quest cq2_s2_depot after Off Schedule. 13 walkable depot rooms, meet Masa
 * at the yard gate, fight him at the lift shutter with CHAR_INTRO.mb2_depot.
 * After the shutter win: add-only BOND_Q.c2_masa_after, path payoffs (leave / notes
 * / help), the shutter seal pry, and after-seal east-block tenant lines (wrap only).
 * After the seal, a residual Rider clerk (nq_depclk, provisional name Endō) opens the
 * time-clock window (FFF_S2MENUS.open('s2_depot')). Wraps only; no new always-running
 * loops. Does not edit S2 / S2P2 / S2P3 / S2P4 VO or the landmark depot path. */
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
  VO.emptyShutDone = [['', 'The lift shutter is quiet. The gray seal is off the sheet.']];

  /* Provisional clerk name — pending Erik: Endō (遠藤). */
  if (typeof NM !== 'undefined') NM.nq_depclk = 'Endō';
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
    if (typeof PT_HAS !== 'undefined') PT_HAS[figAlias + '_neutral'] = 1;
  }
  wireWho('nq_depclk', 'nq_depclk', 1.04, 'endo');

  VO.clkShut = V3(
    [],
    {
      fierce: [['ryo', 'Shuttered. Come back when the yard is ours.']],
      strategic: [['aoi', 'Closed until the seal is done. The sheet stays on that side.']],
      balanced: [['ryo', 'Someone still clocks in here. Not tonight.']]
    },
    []
  );
  VO.clkOpen = V3(
    [],
    {
      fierce: [['nq_depclk', 'Counter’s open. Sign the pad. Don’t linger.']],
      strategic: [['nq_depclk', 'Manifest window’s open. Nails’ price is on the sheet.']],
      balanced: [['nq_depclk', 'You ended the gray schedule. Sit a minute. The kettle’s on in the back.']]
    },
    []
  );

  VO.leave = V3(
    [['', 'Masa stays on the floor. His hard hat rolls once and stops.']],
    {
      fierce: [['ryo', 'The yard is ours. The seal is next.']],
      strategic: [['aoi', 'Leave him. The sheet is still on the shutter.']],
      balanced: [['aoi', 'He is out. We take the seal and go.']]
    },
    []
  );
  VO.notes = V3(
    [['mb2_depot', 'The dock code\u2026 first light. The time is on the sheet.']],
    {
      fierce: [['ryo', 'That is enough.']],
      strategic: [['ryo', 'First light. I have it.']],
      balanced: [['ryo', 'Thank you. Rest.']]
    },
    []
  );
  VO.help = V3(
    [['ryo', 'Up. The yard can still send honest freight under our color.']],
    {
      fierce: [['mb2_depot', 'You already won. Fine. I clock out.']],
      strategic: [['mb2_depot', 'Honest freight. I can do that.']],
      balanced: [['mb2_depot', 'I can still run a clean dock. Go on.']]
    },
    []
  );
  VO.tenant = {
    mori: V3([['nq_mori', 'The freight has gone quiet for good. The kettle is on. Come in when you pass.']],
      { fierce: [['ryo', 'We will.']], strategic: [['ryo', 'Lock the door anyway.']], balanced: [['ryo', 'Thank you, Mori-san.']] }, []),
    nao: V3([['nq_nao', 'If the nights stay like this I can keep the day job. Thank you \u2014 really.']],
      { fierce: [['ryo', 'They will not come back.']], strategic: [['ryo', 'The schedule is done. It should hold.']], balanced: [['ryo', 'Sleep. It stays this way.']] }, []),
    haru: V3([['nq_haru', 'The bikes are gone. Mori-san said I can sit on the sofa whenever I want now.']],
      { fierce: [['ryo', 'Sit. The street is yours.']], strategic: [['ryo', 'The sofa is fine. Keep off the road.']], balanced: [['ryo', 'Yes. The lobby is safe now.']] }, [])
  };

  /* add-only M2: PAY / Journal name already reserved in the CH2BOND block */
  if (typeof BOND_Q === 'object' && typeof BOND_TXT === 'object' && typeof BOND_MID === 'object') {
    BOND_Q.c2_masa_after = { q: '<b>Aoi asks</b><p>He is down. The seal and the manifest are on the shutter. What do we do with him?</p>',
      o: { fierce: ['Leave him. The yard is ours', 'Fierce'], strategic: ['Stay talking. I want the dock code', 'Strategic'], balanced: ['Help him up. Honest freight can still leave', 'Compassionate'] } };
    BOND_MID.c2_masa_after = 'strategic';
    BOND_TXT.c2_masa_after = { _mx: 1, _noReact: 1,
      fierce: {
        fierce: [['{LEAD}', '{shout}Leave him. The yard is ours.{/shout}', { hype: 1 }], ['{PARTNER}', 'The shutter is already ours.']],
        strategic: [['{LEAD}', '{brisk}Stay talking. I want the dock code.{/brisk}'], ['{PARTNER}', 'The time is on that sheet too.']],
        balanced: [['{LEAD}', 'Up. Honest freight can still leave this yard.'], ['{PARTNER}', '{quiet}Under our color.{/quiet}']] },
      strategic: {
        fierce: [['{LEAD}', 'He is done.{p} Leave him.'], ['{PARTNER}', 'He already lost the yard. I will not keep at him.']],
        strategic: [['{LEAD}', '{brisk}Stay talking. The code and the time.{/brisk}'], ['{PARTNER}', 'He wrote it on the sheet. Make him say it.']],
        balanced: [['{LEAD}', 'Up. The yard can still run honest.'], ['{PARTNER}', 'If the dock still runs, I want it written, not wished.']] },
      balanced: {
        fierce: [['{LEAD}', 'Leave him.{p} The yard is ours now.'], ['{PARTNER}', '{quiet}Leave him.{/quiet} I will watch his breathing.']],
        strategic: [['{LEAD}', 'The sheet. The code. The time.'], ['{PARTNER}', 'He will talk, if we stay.']],
        balanced: [['{LEAD}', '{slow}Up. Honest freight can still leave this yard under our color.{/slow}'], ['{PARTNER}', 'Help him stand. I will walk him to the clock.']] } };
  }

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
    dcrate: 'Crate stacks \u00b7 \u8ca8\u7269', dcold: 'Cold store \u00b7 \u51b7\u51cd', dcage: 'Parts cage \u00b7 \u90e8\u54c1',
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
  roomDef('dclock', { spots: [
    { id: 's2_depot_shop', r: [400, 700, 700, 830], at: [550, 780], face: 3, lab: 'Window' }
  ] });

  roomDef('dbay', { spots: [
    doorSpot('s2_d_clock', 140, '\u6253\u523b'),
    { id: 's2_d_crate', r: [1080, 400, 1190, 700], at: [1060, 700], face: 1, lab: '\u8ca8\u7269' },
    { id: 's2_d_bike', r: [90, 400, 200, 700], at: [220, 700], face: 2, lab: '\u99d0\u8f2a' }
  ] });
  roomDef('dcrate', { spots: [
    doorSpot('s2_d_bay', 140, '\u8377\u5f79'),
    doorSpot('s2_d_cold', 1050, '\u51b7\u51cd')
  ] });
  roomDef('dcold', { spots: [
    { id: 's2_d_crate', r: [140, 70, 250, 300], at: [195, 310], face: 3, lab: '\u8ca8\u7269' },
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
  function stripP5Art(keep) {
    try {
      [].forEach.call(document.querySelectorAll('[id^="s2P5Room_"], #s2P5Battle'), function (el) {
        if (keep && el.id === 's2P5Room_' + keep) return;
        if (el.parentNode) el.parentNode.removeChild(el);
      });
    } catch (eS) {}
    try {
      var keepLie = keep === 'dshut' && E().masaFate === 'leave' && !E().seal_depot;
      if (!keepLie) {
        [].forEach.call(document.querySelectorAll('.c2lie[data-npc="mb2_depot"]'), function (el) { if (el.parentNode) el.parentNode.removeChild(el); });
        if (W.c2n) W.c2n.s2masaLie = null;
      }
    } catch (eL) {}
  }
  function paintRoom() {
    var k = room();
    stripP5Art(KEYS.indexOf(k) >= 0 ? k : null);
    if (KEYS.indexOf(k) < 0) return;
    var m = document.getElementById('wimap') || document.getElementById('world');
    if (!m) return;
    var fate = (k === 'dshut') ? (E().masaFate || '') : '';
    var key = k + ':' + (cleared() || (k === 'dshut' && won()) ? (fate || 'cleared') : 'held') + (E().seal_depot ? ':seal' : '');
    if (!RCV[key]) {
      RCV[key] = document.createElement('canvas'); RCV[key].width = RW; RCV[key].height = RH;
      var g = RCV[key].getContext('2d'), fn = PAINT[k];
      if (k === 'dshut' && fate === 'leave') fn = 'depShutterLeave';
      else if (k === 'dshut' && fate === 'notes') fn = 'depShutterNotes';
      else if (k === 'dshut' && fate === 'help') fn = 'depShutterHelp';
      try { if (P5.ART && root.FFF_S2P && fn && root.FFF_S2P[fn]) root.FFF_S2P[fn](g, !!E().seal_depot); }
      catch (e) { ev('world:s2p5:err:paint:' + (e && e.message)); }
    }
    var c = RCV[key];
    /* drop a stale same-id canvas from a previous fate / seal so it cannot sit on top */
    try {
      [].forEach.call(document.querySelectorAll('#s2P5Room_' + k + ', [id="s2P5Room_' + k + '"]'), function (el) {
        if (el !== c && el.parentNode) el.parentNode.removeChild(el);
      });
    } catch (eD) {}
    if (c && c.parentNode !== m) {
      c.className = 'nqprop'; c.id = 's2P5Room_' + k; c.setAttribute('data-key', key);
      c.style.cssText = 'position:absolute;left:0;top:0;width:' + RW + 'px;height:' + RH + 'px;z-index:1;pointer-events:none';
      m.insertBefore(c, m.firstChild);
    }
  }
  P5.resetPaint = function () { RCV = {}; stripP5Art(null); };
  P5.paintRoom = paintRoom;

  /* ---------------- battle ---------------- */
  function hookBattle() {
    if (P5._bt) return true;
    if (!root.FFF_C2BT || !root.FFF_S2P || !root.FFF_S2P.battleShutter) return false;
    P5._bt = 1;
    var BT = root.FFF_C2BT;
    BT.ROOMS.sh = { name: 'Lift shutter', paint: function (x) { root.FFF_S2P.battleShutter(x); },
      lights: [[120, 90, '255,200,110', 70, 0.3, 'lamp'], [600, 90, '255,200,110', 70, 0.3, 'lamp']], rain: 0, mood: 'room', feet: 52 };
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
    if (qOn() && won() && !E().seal_depot) {
      if (inDepot()) return { x: 640, y: 400, lab: 'The shutter', loc: 'Masa\u2019s Seal \u00b7 the bond', room: 'dshut' };
      return { x: DEPOT_AT[0], y: DEPOT_AT[1], lab: 'The shutter', loc: 'Masa\u2019s Seal \u00b7 the bond', room: 'town' };
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
    if (E().seal_depot && !qDone()) { finishQuest(); ch = 1; }
    if (E().seal_depot || E().down_dep || E().eastSeal || qDone()) applySeTurf();
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
    if (k === 'dyard' && qOn() && !met()) want = [540, 590, Math.PI / 2];
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

  /* Residual Rider clerk behind the time-clock desk. Customer stays on the south side. */
  var CLK = null;
  var CLK_AT = [550, 518];
  function popClerk() {
    var k = room();
    var want = (afterSeal() && k === 'dclock') ? [CLK_AT[0], CLK_AT[1], Math.PI / 2] : null;
    if (!want) { if (CLK) { try { kill(CLK); } catch (eK) {} CLK = null; } return; }
    if (CLK && CLK.el && CLK.el.parentNode && CLK._rk === k) {
      try { if (!W.c2n) W.c2n = {}; W.c2n.s2depclk = CLK; } catch (eN) {}
      return;
    }
    if (CLK) { try { kill(CLK); } catch (eK) {} CLK = null; }
    CLK = npc('nq_depclk', want[0], want[1], want[2]);
    CLK._rk = k;
    try { if (typeof waddle === 'function') waddle(CLK, 0, want[2]); } catch (eW) {}
    try { if (!W.c2n) W.c2n = {}; W.c2n.s2depclk = CLK; } catch (eN) {}
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
    if (!won()) { setStg('won'); qStep(2); }
    whenFree(function () {
      talk(pv(VO.wonFight), function () { askBond(); });
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
    if (E().seal_depot || cleared()) { lockIn(1); talk(VO.emptyShutDone, function () { lockIn(0); }); return true; }
    if (won()) { askBond(); return true; }
    if (!qOn()) return false;
    if (!met()) { setStg('met'); qStep(1); }
    lockIn(1);
    introThenFight();
    return true;
  }

  function clerkTalk() {
    if (busy()) return true;
    if (!afterSeal()) {
      lockIn(1);
      talk(pv(VO.clkShut), function () { lockIn(0); });
      return true;
    }
    lockIn(1);
    talk(pv(VO.clkOpen), function () {
      lockIn(0);
      try {
        if (W.ryo) { W.ryo.v = 0; W.path = []; }
        if (root.FFF_S2MENUS && typeof FFF_S2MENUS.open === 'function') FFF_S2MENUS.open('s2_depot');
      } catch (eO) { ev('world:s2p5:err:shop:' + (eO && eO.message)); }
    });
    return true;
  }

  function fateOf(ans) { return ans === 'fierce' ? 'leave' : ans === 'strategic' ? 'notes' : 'help'; }
  function pickedBond() { try { return ((STORY.bond(SAVE) || {}).picks || {}).c2_masa_after; } catch (e) { return ''; } }
  function afterSeal() { return !!(E().seal_depot || qDone() || stg() === 'done'); }
  function refreshShutPaint() {
    Object.keys(RCV).forEach(function (k) { if (k.indexOf('dshut') === 0) delete RCV[k]; });
    var el = document.getElementById('s2P5Room_dshut');
    if (el && el.parentNode) el.parentNode.removeChild(el);
    paintRoom();
  }
  function applyFateArt(f) {
    if (MASA) { try { kill(MASA); } catch (eK) {} MASA = null; }
    try { if (W.c2n) W.c2n.s2masa = null; } catch (eN) {}
    if (f === 'help' && room() === 'dshut') {
      MASA = npc('mb2_depot', 640, 620, Math.PI / 2);
      MASA._rk = 'dshut';
      try { if (typeof waddle === 'function') waddle(MASA, 0, Math.PI / 2); } catch (eW) {}
      try { if (!W.c2n) W.c2n = {}; W.c2n.s2masa = MASA; } catch (eN2) {}
    } else if (f === 'leave' && room() === 'dshut' && typeof lieEl === 'function') {
      try {
        var le = lieEl('mb2_depot', 640, 620, (typeof C2K === 'object' && C2K.mb2_depot) || 1);
        if (le) { le.classList.add('c2lie'); le.dataset.npc = 'mb2_depot'; (typeof layer !== 'undefined' ? layer : document.getElementById('world')).appendChild(le); if (W.ints) W.ints.push({ el: le }); if (!W.c2n) W.c2n = {}; W.c2n.s2masaLie = le; }
      } catch (eL) { ev('world:s2p5:err:lie:' + (eL && eL.message)); }
    }
    refreshShutPaint();
  }
  function playFate(done) {
    var f = E().masaFate || 'help';
    applyFateArt(f);
    lockIn(1);
    talk(pv(VO[f] || VO.help), function () {
      if (f === 'help' && MASA) { try { kill(MASA); } catch (eK) {} MASA = null; try { if (W.c2n) W.c2n.s2masa = null; } catch (eN) {} }
      lockIn(0);
      if (done) done();
    });
  }
  function askBond() {
    if (E().seal_depot) { finishQuest(); return; }
    var ans = pickedBond();
    if (ans && !E().masaFate) { E().masaFate = fateOf(ans); if (ans === 'strategic') E().dockNotes = 1; sv(); }
    if (E().masaFate) { playFate(function () { takeSeal(); }); return; }
    lockIn(1);
    try {
      bondAsk('c2_masa_after', function (L2) {
        var pk = pickedBond() || path();
        E().masaFate = fateOf(pk);
        if (pk === 'strategic') E().dockNotes = 1;
        sv();
        ev('world:s2p5:bond:' + E().masaFate);
        function next() { playFate(function () { takeSeal(); }); }
        if (L2 && L2.length) talk(L2, next); else next();
      });
    } catch (eB) { ev('world:s2p5:err:bond:' + (eB && eB.message)); lockIn(0); playFate(function () { takeSeal(); }); }
  }
  function takeSeal() {
    var e = E();
    if (e.seal_depot) { finishQuest(); return; }
    lockIn(1);
    W.cut = true;
    try { if (typeof sLock === 'function') sLock(1, 'c2seal'); } catch (eL) {}
    function pry() {
      try { AU.play('place', { gain: 0.8 }); } catch (eA) {}
      try { AU.play('fire_whoosh', { gain: 0.6 }); } catch (eA2) {}
      try { if (typeof rdyOff === 'function' && W.ryo) rdyOff(W.ryo); } catch (eR) {}
      e.seal_depot = 1;
      var n = (typeof c2Seals === 'function') ? c2Seals() : 0;
      var f = (typeof C2S_FAC === 'object' && C2S_FAC.depot) || 'dep';
      var own = e.run_fac && f === e.run_fac;
      if (!own && f) e['down_' + f] = 1;
      if (!own && e.run_fac && !e.c2sUp) {
        e.c2sUp = 1;
        try { if (root.FFF_OPN) root.FFF_OPN.grant(C2S_SET[e.run_fac][1]); } catch (eG) {}
      }
      sv();
      ev('world:c2:seal:depot:' + n);
      ev('world:s2p5:seal');
      try { if (typeof c2sLocksSync === 'function') c2sLocksSync(); } catch (eS) {}
      W.cut = false;
      try { if (typeof sLock === 'function') sLock(0, 'c2seal'); } catch (eL2) {}
      try { if (W.ryo && typeof resetTrail === 'function') resetTrail(W.ryo.x, W.ryo.y, W.ryo.dir); } catch (eT) {}
      refreshShutPaint();
      var L2 = n >= ((typeof C2LMK !== 'undefined' && C2LMK.length) || 4)
        ? [['', '<p class="dim">The fourth token comes free. Four serials in Ryo\u2019s pocket.</p>'], ['aoi', (e.ckSlip ? 'All four. Genji can match them to the slip.' : 'All four. Now Tetsu\u2019s slip.')]]
        : [['', '<p class="dim">Ryo pries the gray seal off the shutter. A small engraved token. A serial on the back.</p>'], ['aoi', (typeof C2SC === 'object' && C2SC.sealN && C2SC.sealN[n]) || 'Another seal.']];
      if (!own && f && n < ((typeof C2LMK !== 'undefined' && C2LMK.length) || 4)) {
        try { L2.push(['ryo', 'The ' + (typeof c2sFacName === 'function' ? c2sFacName(f) : 'Riders') + ' stand down now.']); } catch (eN) {}
      }
      talk(L2, function () {
        lockIn(0);
        if (n >= ((typeof C2LMK !== 'undefined' && C2LMK.length) || 4)) {
          try { if (typeof sayKey === 'function') sayKey('c2', 'elevator_live'); } catch (eK) {}
        }
        try { if (typeof c2SqRefresh === 'function') c2SqRefresh(); } catch (eQ) {}
        finishQuest();
      });
    }
    var r = W.ryo;
    if (r && room() === 'dshut' && typeof c2Walk === 'function') {
      try {
        c2Walk(r, 640, 420, 150 / Math.max(0.25, (typeof cinK === 'function' ? cinK() : 1)), function () {
          try { if (typeof c2Face === 'function') c2Face(r, 760, 180); } catch (eF) {}
          try { if (typeof rdyOn === 'function') rdyOn(r, 3); } catch (eR) {}
          later(Math.round(500 * (typeof cinK === 'function' ? cinK() : 1)), pry);
        });
        return;
      } catch (eW) { ev('world:s2p5:err:sealing:' + (eW && eW.message)); }
    }
    pry();
  }
  /* After down_dep, the SE Rider quarter is Punk turf and X4 is Punk vs Syndicate. Re-applied on load. */
  function applySeTurf() {
    if (P5._turfOn) return;
    P5._turfOn = 1;
    try {
      var T = root.FFF_C2TURF, EAST_R = [3760, 2760, 4900, 3300];
      if (!(T && T.Q && T.Q.P)) return;
      if (!T.Q.P.some(function (r) { return r[0] === 3760 && r[1] === 2760 && r[2] === 4900; })) T.Q.P.push(EAST_R.slice());
      if (T.Q.R && T.Q.R.length) {
        T.Q.R.forEach(function (r) {
          if (!T.Q.P.some(function (p) { return p[0] === r[0] && p[1] === r[1] && p[2] === r[2] && p[3] === r[3]; })) T.Q.P.push(r.slice());
        });
        T.Q.R = [];
      }
      if (T.B && T.B.X4) T.B.X4.g = 'PS';
    } catch (eT) {}
  }
  function flipEast() {
    var n = NS(); n.won = n.won || {};
    var already = !!(n.won.east || E().vend_eastst);
    n.won.east = 1; n.won.depot = 1; E().vend_eastst = 1; E().eastSeal = 1;
    applySeTurf();
    try { if (root.FFF_NQ && root.FFF_NQ.BLK && !root.FFF_NQ.BLK.east) root.FFF_NQ.BLK.east = { n: 'MINATO-S\u014c', r: [3760, 2760, 4900, 3300] }; } catch (eB) {}
    if (!already) {
      try { var P2 = root.FFF_S2P2; if (P2 && typeof P2.takeEastTurf === 'function') P2.takeEastTurf(); } catch (eE) {}
    }
    sv();
    ev('world:s2p5:east:flip');
  }
  function finishQuest() {
    if (!E().seal_depot) return;
    if (!cleared()) { setStg('done'); qClose(); }
    flipEast();
    ev('world:s2p5:done');
    try { later(0, popClerk); } catch (eC) {}
  }
  function tenantAfter(who) {
    if (busy()) return true;
    var table = VO.tenant[who];
    if (!table) return false;
    lockIn(1);
    talk(pv(table), function () { lockIn(0); });
    return true;
  }
  P5.yardTalk = yardTalk; P5.askBond = askBond; P5.takeSeal = takeSeal; P5.flipEast = flipEast; P5.finishQuest = finishQuest; P5.applySeTurf = applySeTurf;
  P5.afterSeal = afterSeal; P5.fateOf = fateOf; P5.tenantAfter = tenantAfter;
  P5.popClerk = popClerk; P5.clerkTalk = clerkTalk; P5.CLK_AT = CLK_AT;

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

  if (typeof c2Tags === 'function') {
    var tags0 = c2Tags;
    c2Tags = function (id, D) {
      var out = tags0.apply(this, arguments);
      try {
        if (out && on()) out = out.filter(function (t) {
          if (!t || !t.key) return true;
          if (t.key.indexOf(':s2_depot_shop') >= 0) return room() === 'dclock';
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
          if (a === 'lk_depot' && p5Enter()) { chainRepair(); enterYard(); return true; }
          if (a === 'exit' && inDepot() && room() !== 'dyard') { goBack(); return true; }
          if (a && a.indexOf('s2_d_') === 0) { goDoor(a); return true; }
          if (a === 's2_talk_masa') {
            if (room() === 'dshut') return shutterTalk();
            return yardTalk();
          }
          if (a === 's2_depot_shop') return clerkTalk();
          if (afterSeal() && (a === 's2_talk_mori' || a === 's2_talk_nao' || a === 's2_talk_haru')) {
            return tenantAfter(a.replace('s2_talk_', ''));
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
          if (id === 'nq_depclk') return clerkTalk();
          if (afterSeal() && (id === 'nq_mori' || id === 'nq_nao' || id === 'nq_haru')) {
            return tenantAfter(id.replace('nq_', ''));
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
          if (id === 'nq_depclk') return clerkTalk();
          if (afterSeal() && (id === 'nq_mori' || id === 'nq_nao' || id === 'nq_haru')) {
            return tenantAfter(id.replace('nq_', ''));
          }
        }
      } catch (eT) {}
      return tn0.apply(this, arguments);
    };
  }

  var lastPaintK = null;
  if (typeof c2Frame === 'function') {
    var fr0 = c2Frame;
    c2Frame = function (dt) { fr0.apply(this, arguments); try { if (on() && p5Enter()) { chainRepair(); var k = room(); if (k !== lastPaintK) { lastPaintK = k; popMasa(); popClerk(); paintRoom(); } } } catch (e) { if (!P5.ferr) { P5.ferr = 1; ev('world:s2p5:err:frame:' + (e && e.message)); } } };
  }
  if (typeof c2Go === 'function') {
    var goX = c2Go;
    c2Go = function () {
      var r = goX.apply(this, arguments);
      try { if (on()) { later(0, function () { popMasa(); popClerk(); paintRoom(); }); later(350, function () { popMasa(); popClerk(); paintRoom(); }); } } catch (eG) {}
      return r;
    };
  }
  if (typeof c2Pop === 'function') {
    var pop0 = c2Pop;
    c2Pop = function () { pop0.apply(this, arguments); try { if (on()) { chainRepair(); hookBattle(); popMasa(); popClerk(); paintRoom(); } } catch (eP) {} };
  }
  try { chainRepair(); } catch (eC) {}
  ev('world:s2p5:ready');
  } catch (eS2) { try { ev('world:s2p5:err:init:' + (eS2 && eS2.message)); console.warn('S2P5 init', eS2); } catch (e2) {} }
})();
