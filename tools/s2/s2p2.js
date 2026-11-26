/* v6.5.63 FFF_S2P2 (Punk-route seal 2, phase 2): Night Runs.
 * Quest cq2_s2_runs after Wagashi Row. 2–3 freight/bike runs on the east canal
 * bridge and the SE street; last runner points at the boat house (no Phase 3 pin).
 * Minato-sō: south façade, lobby + workshop, Hase's counter, three tenants,
 * Residents-only stair that does not open, east-block turf sting.
 * Path voice is new tables only. Wraps only; no new always-running loops.
 * Does not edit existing Fierce/Strategic Nails copy or S2 VO. */
(function () {
  try {
  if (typeof c2S !== 'function' || typeof C2W === 'undefined' || !C2W || typeof INT === 'undefined' || !INT.c2_town) {
    try { ev('world:s2p2:skip'); } catch (e0) {} return;
  }
  var root = typeof window !== 'undefined' ? window : this;
  var S2 = root.FFF_S2;
  var P2 = root.FFF_S2P2 = { v: 1, ART: true };
  /* Hide the town CSS rain overlay in C2 interiors. Uses the c2 / c2town
   * classes c2Pop already toggles — no new loop. Also pauses the tile animation. */
  (function hideIndoorRain() {
    var st = document.getElementById('s2p2-norain');
    if (st) return;
    st = document.createElement('style');
    st.id = 's2p2-norain';
    st.textContent = '#world.c2:not(.c2town) #wrain{display:none}#world.c2:not(.c2town) #wrain .rn{animation-play-state:paused}';
    (document.head || document.documentElement).appendChild(st);
  })();
  function syncIndoorRain() {
    var wr = document.getElementById('wrain'), k = null;
    try { k = c2Room(); } catch (eR) {}
    var hide = !!(k && k !== 'town');
    if (wr) wr.style.display = hide ? 'none' : '';
    var ws = document.getElementById('wfxs');
    if (ws && hide) ws.style.display = 'none';
    var amb = document.getElementById('c2amb');
    if (amb && hide) { amb.style.display = 'none'; try { var ag = amb.getContext('2d'); if (ag) ag.clearRect(0, 0, amb.width, amb.height); } catch (eC) {} }
  }
  P2.syncIndoorRain = syncIndoorRain;
  /* C2AMB falls back to the town grade (rain: 32) for unknown rooms like
   * mina / mshop / waga. Wrap the existing c2Frame tick — no new loop. */
  function hookAmb() {
    if (typeof c2Frame !== 'function' || c2Frame._s2p2rain) return;
    var fr0 = c2Frame;
    var known = { gym: 1, clinic: 1, sento: 1, sentoU: 1, sentoK: 1, arcade: 1, game: 1, depot: 1, hotel: 1, udon: 1, club: 1, ckback: 1, gekko: 1, motors: 1, town: 1, roof: 1 };
    var lastK = null;
    c2Frame = function (dt) {
      fr0.apply(this, arguments);
      try {
        var k = typeof c2Room === 'function' ? c2Room() : null;
        if (k === lastK) return;
        lastK = k;
        if (k && !known[k]) {
          var cv = document.getElementById('c2amb');
          if (cv) {
            cv.style.display = 'none';
            var g = cv.getContext('2d');
            if (g) g.clearRect(0, 0, cv.width, cv.height);
          }
        }
      } catch (eH) {}
    };
    c2Frame._s2p2rain = 1;
  }
  later(0, hookAmb);
  function on() { return (typeof c2On !== 'function' || c2On()) && (typeof chN !== 'function' || chN() === 2); }
  function S() { return c2S(); }
  function E() { return c2S().e; }
  function room() { try { return c2Room(); } catch (e) { return null; } }
  function inTown() { return room() === 'town'; }
  function nailsRun() { return on() && E().run_fac === 'arc'; }
  function busy() { return !!(W.dgFight || W.dlg || W.busy || W.cut || W.fading || W.paused); }
  function later(ms, fn) { setTimeout(function () { try { fn(); } catch (e) { ev('world:s2p2:err:later:' + (e && e.message)); } }, ms); }
  function talk(lines, done) { W.dlg = true; scene(null, lines, function () { W.dlg = false; if (done) done(); }); }
  function lockIn(on1) { if (on1) { W.cut = true; W.path = []; if (W.ryo) W.ryo.v = 0; try { stickEnd(); } catch (e) {} } else W.cut = false; }
  function sv() { try { if (typeof c2QSync === 'function') c2QSync(); } catch (e) {} save(); }
  function path() { var p = 'balanced'; try { p = c2Path(); } catch (e) {} return p === 'fierce' || p === 'strategic' ? p : 'balanced'; }
  function npc(id, x, y, fa) { var s = c2Npc(id, x, y, fa == null ? Math.PI / 2 : fa); s.el.classList.add('s2'); s.s2id = id; s.el.dataset.npc = id; return s; }
  function kill(s) { if (s && s.el && s.el.parentNode) s.el.remove(); if (s) s.gone = 1; }
  function inR(r, x, y) { return x >= r[0] && x < r[2] && y >= r[1] && y < r[3]; }
  function say(lines) { var tries = 0; (function go() { try { comment(lines); } catch (e) {} var b = document.getElementById('wcomment'); if ((!b || !b.innerText) && ++tries < 10) setTimeout(go, 400); })(); }
  function whenFree(fn, tries) { tries = tries || 0; if (!busy() && !document.getElementById('nqsting') && !(typeof W.c2busy !== 'undefined' && W.c2busy)) { try { fn(); } catch (e) { ev('world:s2p2:err:free:' + (e && e.message)); } return; } later(tries < 120 ? 250 : 1000, function () { whenFree(fn, tries + 1); }); }
  function V3(pre, mid, post) { var o = {}, PP = ['fierce', 'strategic', 'balanced']; PP.forEach(function (p) { o[p] = (pre || []).concat(mid[p] || [], post || []); }); return o; }
  function pv(x) { try { return typeof pathLines === 'function' ? pathLines(x) : (x[path()] || x.balanced || x); } catch (e) { return x.balanced || []; } }
  function wagaDone() { return S2 && typeof S2.qDone === 'function' && S2.qDone(); }
  function punkAfterSeal() { return on() && nailsRun() && !!E().seal_sento; }

  /* ---------------- state ---------------- */
  function NS() { var e = E(); if (!e.nq || typeof e.nq !== 'object') e.nq = {}; return e.nq; }
  function stg() { return NS().runs || ''; }
  function setStg(v) { NS().runs = v; sv(); ev('world:s2p2:st:' + v); }
  function talked() { var n = NS(); if (!n.runTalk) n.runTalk = {}; return n.runTalk; }
  var QID = 'cq2_s2_runs';
  var Q = { id: QID, n: 'Night Runs', giver: 'Flip, for Nails',
    quote: 'The Riders still run freight over the east canal bridge at night. Cut the runs.',
    loc: 'Kitsune-Ch\u016b\u014d \u00b7 East canal bridge' };
  if (typeof C2Q !== 'undefined') C2Q[QID] = { n: Q.n, steps: [Q.quote] };
  if (typeof C2QLOC !== 'undefined') C2QLOC[QID] = ['town', Q.loc];
  function qOpen() { var s = S(); if (s.q[QID] == null) s.q[QID] = 0; SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = s.q[QID] | 0; s.qa = QID; SAVE.qa = QID; SAVE.qTrack = ''; SAVE.qTrackPick = 0; sv(); ev('world:s2p2:quest:open'); }
  function qStep(n) { var s = S(); if (s.q[QID] == null || s.q[QID] === 9) return; s.q[QID] = Math.max(s.q[QID] | 0, n); SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = s.q[QID]; sv(); }
  function qClose() { var s = S(); if (s.q[QID] == null || s.q[QID] === 9) return; s.q[QID] = 9; SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = 9;
    SAVE.journalLog = SAVE.journalLog || []; if (SAVE.journalLog.indexOf(Q.n) < 0) SAVE.journalLog.push(Q.n);
    if (s.qa === QID) { s.qa = (typeof CQ !== 'undefined' && CQ.locks) || ''; SAVE.qa = s.qa; } sv(); ev('world:s2p2:quest:done');
    if (typeof window.c2QuestYen === 'function') window.c2QuestYen(QID, Q.n); }
  function qOn() { var q = S().q[QID]; return q != null && q !== 9; }
  function qDone() { return S().q[QID] === 9; }
  P2.Q = Q; P2.stg = stg; P2.setStg = setStg; P2.qOpen = qOpen; P2.qClose = qClose; P2.qOn = qOn; P2.qDone = qDone;

  /* ---------------- voices (new tables only) ---------------- */
  var VO = P2.VO = {};
  VO.brief = V3(
    [['n13flip', 'The row is ours. They still run freight over the east canal at night. Two on the bridge, one on the south street.']],
    {
      fierce: [['ryo', 'Then we run the bikes down tonight.'], ['aoi', 'No warning. Just take the street.'], ['n13flip', 'Do it loud. Masa will hear the engines stop.']],
      strategic: [['ryo', 'We cut the schedule. Stop the freight, the rest unravels.'], ['aoi', 'The last runner will tell us where the boats sit.'], ['n13flip', 'That is the plan. Hit the times, not the noise.']],
      balanced: [['ryo', 'Those runs keep the street awake. We get them off the bridge so people can sleep.'], ['aoi', 'The apartments over the workshop have been shaking all week.'], ['n13flip', 'Then go talk to them when it is quiet. I will still want the last runner pointed at the boat house.']]
    },
    [['n13flip', 'East canal. I will hear it from the row.']]
  );
  VO.run = [
    V3(
      [['c2_boso', 'Punks on the bridge? This freight is Masa\u2019s.']],
      {
        fierce: [['ryo', 'Not after tonight.']],
        strategic: [['ryo', 'Your timetable just ended.']],
        balanced: [['ryo', 'The street is trying to sleep. Take it somewhere else.']]
      },
      []
    ),
    V3(
      [['c2_boso', 'Second bike. You already hit the first?']],
      {
        fierce: [['ryo', 'And we will hit you.']],
        strategic: [['ryo', 'If the second run is late, the third never leaves.']],
        balanced: [['ryo', 'Go home. This bridge is done for the night.']]
      },
      []
    ),
    V3(
      [['c2_boso', 'Last bag of the night. You want it, you take it off me.']],
      {
        fierce: [['ryo', 'Then we take it.']],
        strategic: [['ryo', 'After this, there is no schedule left to run.']],
        balanced: [['ryo', 'Hand it over and point us at the boat. Then go.']]
      },
      []
    )
  ];
  VO.wonRun = [
    V3([], { fierce: [['aoi', 'One down.']], strategic: [['aoi', 'First slot is empty.']], balanced: [['aoi', 'The bridge just got quieter.']] }, []),
    V3([], { fierce: [['aoi', 'Second one\u2019s down. One more.']], strategic: [['aoi', 'The schedule is already broken.']], balanced: [['aoi', 'One more on the south street, then we can breathe.']] }, []),
    V3(
      [['c2_boso', 'The boat house. East, on the water. That is all you get.']],
      {
        fierce: [['ryo', 'Good. The street is ours.'], ['aoi', 'He pointed at the boat house. We still have Masa at the yards.']],
        strategic: [['ryo', 'The runs are cut. The boat house is next on the map, later.'], ['aoi', 'Four Corners still says the yards. We do not leave a pin on a door we have not opened.']],
        balanced: [['ryo', 'Thank you. Stay off this street.'], ['aoi', 'We should tell the people in the apartments it is over.']]
      },
      []
    )
  ];
  VO.held = {
    mori: V3([['nq_mori', 'They roll the bikes through at two in the morning. I asked the tall one to stop. He laughed.']],
      { fierce: [['ryo', 'He will not laugh tonight.']], strategic: [['ryo', 'If the freight stops, the bikes stop.']], balanced: [['ryo', 'We are here to get the runs off the bridge. Stay downstairs until it is quiet.']] }, []),
    nao: V3([['nq_nao', 'I get in at one and the street is still shaking. I just want to sleep before the next shift.']],
      { fierce: [['ryo', 'Then we take the street from them.']], strategic: [['ryo', 'We cut their timetable. After that the shaking stops.']], balanced: [['ryo', 'Get some rest. We will make the street quiet.']] }, []),
    haru: V3([['nq_haru', 'Mum says stay off the stairs when the bikes come. I can hear them from the lobby.']],
      { fierce: [['ryo', 'Stay here. We will handle the bikes.']], strategic: [['ryo', 'The stairs stay shut. That is safer.']], balanced: [['ryo', 'You can stay in the lobby. We will come back when it is quiet.']] }, [])
  };
  VO.taken = {
    mori: V3([['nq_mori', 'The street slept last night. First time in a month. Come in. The kettle is on.']],
      { fierce: [['ryo', 'Good. We are moving on.']], strategic: [['ryo', 'Keep the door locked anyway. Masa is not done.']], balanced: [['ryo', 'I am glad it was quiet. This block is yours again.']] }, []),
    nao: V3([['nq_nao', 'I walked home and it was quiet. Thank you. I can keep the day job if the nights stay like this.']],
      { fierce: [['ryo', 'They will not come back.']], strategic: [['ryo', 'The schedule is cut. That should hold.']], balanced: [['ryo', 'Sleep. We will keep it that way.']] }, []),
    haru: V3([['nq_haru', 'The bikes did not come. Can I sit on the sofa now? Mori-san said maybe.']],
      { fierce: [['ryo', 'Sit. The street is ours.']], strategic: [['ryo', 'The stairs are still closed. The sofa is fine.']], balanced: [['ryo', 'Yes. The lobby is safe now.']] }, [])
  };
  VO.haseHeld = V3(
    [['nq_hase', 'I fix what they break. That is the deal, as long as they hold the block.']],
    {
      fierce: [['ryo', 'The deal is over tonight. You can stay.']],
      strategic: [['ryo', 'When the runs stop, you will still have work. Honest work.']],
      balanced: [['ryo', 'We are not here to take your shop. Just the bikes off the street.']]
    },
    []
  );
  VO.haseOpen = V3(
    [['nq_hase', 'They are gone. I am still here. Tape and gauze. Nails prices, if that is the deal.']],
    {
      fierce: [['ryo', 'Just the kit. We are moving.']],
      strategic: [['ryo', 'We will be back. The yards are still his.']],
      balanced: [['ryo', 'Thank you, Hase-san. Keep the bay open.']]
    },
    []
  );
  VO.stair = V3(
    [['nq_mori', 'Residents only. The stair stays shut.']],
    {
      fierce: [['ryo', 'Fine. We work the ground floor.']],
      strategic: [['ryo', 'Good. No one walks up there tonight.']],
      balanced: [['ryo', 'Understood. We will not go up.']]
    },
    []
  );

  /* ---------------- sprites + portraits ---------------- */
  NM.nq_hase = 'Hase'; NM.nq_mori = 'Mori-san'; NM.nq_nao = 'Nao'; NM.nq_haru = 'Haru';
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
  wireWho('nq_hase', 'nq_hase', 1.04, 'hase');
  wireWho('nq_mori', 'nq_mori', 1.04, 'mori');
  wireWho('nq_nao', 'nq_nao', 1.04, 'nao');
  wireWho('nq_haru', 'nq_haru', 0.88, 'haru');

  /* ---------------- doors + rooms ---------------- */
  var SHOP_AT = [4105, 3490], LOB_AT = [4481, 3490];
  var SHOP_DOOR = { r: [4055, 3380, 4155, 3476], at: SHOP_AT, to: 'mshop', out: [SHOP_AT[0], SHOP_AT[1] + 24] };
  var LOB_DOOR = { r: [4431, 3380, 4531, 3476], at: LOB_AT, to: 'mina', out: [LOB_AT[0], LOB_AT[1] + 24] };
  var RW = 1280, RH = 900;
  function roomDef(k, n, extra) {
    var id = 'c2_nq_' + k; C2R[k] = id;
    INT[id] = Object.assign({ id: id, n: n, w: RW, h: RH, src: 'world/nq_' + k + '.paint', tiles: 1, cell: 15, dg: 'c2', c2: k, deep: 1, safe: 1, mus: 'c2night', nq: 1, s2: 1,
      open: [[90, 250, 1190, 850], [580, 850, 700, 900]], 'in': [640, 820, 3], back: [640, 820, 3],
      spots: [{ id: 'exit', r: [575, 850, 705, 900], at: [640, 870], face: 0 }] }, extra || {});
    INT[id].base = INT[id].block; TAGS_IN[id] = {};
    return INT[id];
  }
  roomDef('mshop', 'Hase Repair', { block: [[120, 250, 340, 640], [500, 350, 1000, 500], [140, 660, 300, 780]],
    spots: [{ id: 'exit', r: [575, 850, 705, 900], at: [640, 870], face: 0 },
      { id: 's2_hase_shop', r: [680, 430, 960, 560], at: [760, 580], face: 0, lab: 'Shop' },
      { id: 's2_to_lobby', r: [100, 80, 220, 230], at: [160, 250], face: 0, lab: 'Lobby' }] });
  roomDef('mina', 'Minato-s\u014d \u00b7 Lobby', { block: [[120, 250, 380, 460], [400, 250, 600, 400], [620, 300, 820, 388], [880, 248, 1090, 548], [140, 560, 390, 680]],
    spots: [{ id: 'exit', r: [575, 850, 705, 900], at: [640, 870], face: 0 },
      { id: 's2_stair', r: [880, 248, 1090, 548], at: [860, 580], face: 0, lab: 'Stair' },
      { id: 's2_to_shop', r: [1088, 560, 1190, 770], at: [1040, 700], face: 1, lab: 'Workshop' },
      { id: 's2_talk_mori', r: [620, 280, 820, 400], at: [720, 430], face: 0, lab: 'Talk' },
      { id: 's2_talk_nao', r: [140, 560, 380, 700], at: [260, 730], face: 0, lab: 'Talk' },
      { id: 's2_talk_haru', r: [120, 250, 380, 470], at: [250, 490], face: 0, lab: 'Talk' }] });
  C2W.doors.nq_mshop = SHOP_DOOR; C2W.doors.nq_mina = LOB_DOOR;
  if (typeof c2DoorOf === 'function') {
    var door0 = c2DoorOf;
    c2DoorOf = function (k) { if (k === 'mshop') return SHOP_DOOR; if (k === 'mina') return LOB_DOOR; return door0.apply(this, arguments); };
  }
  if (typeof c2Surf === 'function') {
    var surf0 = c2Surf;
    c2Surf = function (x, y) { var k = c2Room(); if (k === 'mina') return 'stone'; if (k === 'mshop') return 'concrete'; return surf0.apply(this, arguments); };
  }
  INT.c2_town.spots.push({ id: 's2_e_mshop', r: SHOP_DOOR.r, at: SHOP_DOOR.at, face: 0, lab: 'Enter' });
  INT.c2_town.spots.push({ id: 's2_e_mina', r: LOB_DOOR.r, at: LOB_DOOR.at, face: 0, lab: 'Enter' });
  INT.c2_town.spots.push({ id: 's2_p2_flip', r: [2320, 3110, 2400, 3210], at: [2360, 3190], face: 1, lab: 'Talk' });
  if (typeof TRANS !== 'undefined') { TRANS.s2_e_mshop = 1; TRANS.s2_e_mina = 1; TRANS.s2_to_lobby = 1; TRANS.s2_to_shop = 1; }
  delete INT.c2_town.G;
  function roomOpen() { return on() && punkAfterSeal(); }
  P2.roomOpen = roomOpen; P2.SHOP_DOOR = SHOP_DOOR; P2.LOB_DOOR = LOB_DOOR;

  /* façade overlay on the existing south face */
  var FAC = null;
  function placeDoor() {
    if (!P2.ART || !on() || !inTown()) return;
    if (document.getElementById('s2MinaSouth')) return;
    if (!FAC) {
      FAC = document.createElement('canvas'); FAC.width = 1140; FAC.height = 220;
      try { if (root.FFF_S2P && root.FFF_S2P.minaSouth) root.FFF_S2P.minaSouth(FAC.getContext('2d')); } catch (eF) { ev('world:s2p2:err:facade:' + (eF && eF.message)); }
    }
    FAC.className = 'nqprop'; FAC.id = 's2MinaSouth';
    FAC.style.cssText = 'position:absolute;left:3760px;top:3280px;width:1140px;height:220px;z-index:' + (100 + 3300) + ';pointer-events:none';
    var host = null, sample = document.querySelector('#world .nqprop, #wimap .nqprop, .nqprop');
    if (sample && sample.parentNode) host = sample.parentNode;
    else host = document.getElementById('wisp') || document.getElementById('world') || document.getElementById('wimap');
    if (host) host.appendChild(FAC);
  }

  var RCV = {};
  function paintRoom() {
    var k = room();
    ['mina', 'mshop'].forEach(function (id) {
      var el = document.getElementById('s2P2Room_' + id);
      if (el && k !== id && el.parentNode) el.parentNode.removeChild(el);
    });
    if (k !== 'mina' && k !== 'mshop') return;
    var m = document.getElementById('wimap') || document.getElementById('world');
    if (!m) return;
    if (!RCV[k]) {
      RCV[k] = document.createElement('canvas'); RCV[k].width = RW; RCV[k].height = RH;
      var g = RCV[k].getContext('2d');
      try {
        if (P2.ART && root.FFF_S2P) {
          if (k === 'mina' && root.FFF_S2P.minaLobby) root.FFF_S2P.minaLobby(g);
          else if (k === 'mshop' && root.FFF_S2P.minaShop) root.FFF_S2P.minaShop(g);
        }
      } catch (e) { ev('world:s2p2:err:paint:' + (e && e.message)); }
    }
    var c = RCV[k];
    if (c && c.parentNode !== m) { c.className = 'nqprop'; c.id = 's2P2Room_' + k; c.style.cssText = 'position:absolute;left:0;top:0;width:' + RW + 'px;height:' + RH + 'px;z-index:1;pointer-events:none'; m.insertBefore(c, m.firstChild); }
  }

  /* battle rooms */
  function hookBattle() {
    if (P2._bt) return true;
    if (!root.FFF_C2BT || !root.FFF_S2P || !root.FFF_S2P.battleBridge) return false;
    P2._bt = 1;
    var BT = root.FFF_C2BT;
    BT.ROOMS.br = { name: 'East canal bridge', paint: function (x) { root.FFF_S2P.battleBridge(x); },
      lights: [[130, 200, '255,190,100', 70, 0.32, 'lamp'], [590, 200, '255,190,100', 70, 0.32, 'lamp']], rain: 50, mood: 'rain', feet: 52 };
    BT.ROOMS.se = { name: 'Minato-s\u014d street', paint: function (x) { root.FFF_S2P.battleSE(x); },
      lights: [[120, 200, '255,190,100', 70, 0.36, 'lamp'], [270, 200, '255,180,90', 60, 0.22, 'lamp']], rain: 50, mood: 'rain', feet: 52 };
    BT.KEY.c2_br = 'br'; BT.KEY.c2_se = 'se';
    var roomB0 = BT.room;
    BT.room = function (story) {
      var ctx = (story && story.ctx) || {}, dgk = String(ctx.dgk || '');
      if (P2.ART && (ctx.s2br || ctx.s2k === 's2_r0' || ctx.s2k === 's2_r1' || /^s2_r[01]/.test(dgk))) return 'c2_br';
      if (P2.ART && (ctx.s2se || ctx.s2k === 's2_r2' || /^s2_r2/.test(dgk))) return 'c2_se';
      return roomB0.apply(this, arguments);
    };
    return true;
  }
  hookBattle();
  try { later(0, hookBattle); } catch (eB) { try { setTimeout(hookBattle, 0); } catch (eB2) {} }

  /* ---------------- shop ---------------- */
  /* GGD-49: Hase sells only first-aid-kit materials (electrical tape + gauze).
     Pricing is food-equivalent: a restaurant sweet roll is +14 HP for ¥8 base
     (~¥0.57/HP, same cluster as Full Heal Tea ¥26/46 HP). A 20% dressing is
     +10 HP, so 1 tape + 1 gauze costs ¥6 total — ¥3 base each. Nails 20% off
     applies (shopCost). Mugwort stays ¥1. World-found materials stay the cheap path.
     Healing in the field is eat-in or crafted dressings. Patch kit / spare tube
     stay defined (and painted) but are disabled: not sold, not usable from the
     bag. Reserved for combat-only heals later. */
  if (typeof HITEM !== 'undefined') {
    /* Keep defs + art; combat:1 means useHeal must not consume or heal from the bag. */
    if (!HITEM.patch) HITEM.patch = { n: 'Patch kit', hp: 6, ic: '\ud83e\ude79', rank: 2, combat: 1 };
    else { HITEM.patch.combat = 1; delete HITEM.patch.pct; }
    if (!HITEM.bpart) HITEM.bpart = { n: 'Spare tube', hp: 10, ic: '\ud83e\ude79', rank: 2, combat: 1 };
    else { HITEM.bpart.combat = 1; delete HITEM.bpart.pct; }
  }
  function bindHaseItems() {
    if (typeof ITEMS === 'undefined') return false;
    if (!ITEMS.etape) ITEMS.etape = { n: 'Electrical tape', k: 'herb', hb: 'tape', d: 'For wiring, or a first-aid dressing.' };
    if (!ITEMS.gauze) ITEMS.gauze = { n: 'Gauze', k: 'herb', hb: 'gauze', d: 'For a dressing. Craft with tape.' };
    if (!ITEMS.patch) ITEMS.patch = { n: 'Patch kit', k: 'heal', h: 'patch', hp: 6, combat: 1, d: 'A cheap roadside repair kit. Not for the bag.' };
    else { ITEMS.patch.combat = 1; }
    if (!ITEMS.bpart) ITEMS.bpart = { n: 'Spare tube', k: 'heal', h: 'bpart', hp: 10, combat: 1, d: 'A patched inner tube. Not for the bag.' };
    else { ITEMS.bpart.combat = 1; }
    return true;
  }
  bindHaseItems();
  try { later(0, bindHaseItems); } catch (eI) { try { setTimeout(bindHaseItems, 0); } catch (eI2) {} }
  /* Refuse bag / travel use of combat-reserved heals (and any leftover patch / bpart). */
  if (typeof useHeal === 'function' && !root._s2NoBagCombatHeal) {
    root._s2NoBagCombatHeal = 1;
    var useHeal0 = useHeal;
    useHeal = function (i) {
      var k = SAVE.heal[i], it = (typeof HITEM !== 'undefined') && HITEM[k];
      if (it && (it.combat || k === 'patch' || k === 'bpart')) {
        try { AU.play('tap'); } catch (eA) {}
        ev('world:heal:blocked:bag:' + k);
        return false;
      }
      return useHeal0.apply(this, arguments);
    };
  }
  function nailsOn() { return qDone() || !!(NS().won && NS().won.east); }
  function shopCost(base) { var c = base; if (nailsOn()) c = Math.max(1, Math.round(base * 0.8)); return c; }
  P2.MENU = [
    { id: 'etape', k: 'herb', hb: 'tape', n: 'Electrical tape', base: 3, cost: 2, stock: 3, d: 'For wiring, or a first-aid dressing.' },
    { id: 'gauze', k: 'herb', hb: 'gauze', n: 'Gauze', base: 3, cost: 2, stock: 3, d: 'For a dressing. Craft with tape.' }
  ];
  function menuNow() { return P2.MENU.map(function (it) { var o = {}; Object.keys(it).forEach(function (k) { o[k] = it[k]; }); o.cost = shopCost(it.base); return o; }); }
  if (typeof SHOPS !== 'undefined') {
    SHOPS.s2_hase = { n: 'Hase Repair', who: 'nq_hase', hi: 'Tape and gauze. That\u2019s the shop.', nq: 1, items: P2.MENU };
  }
  function openShop() {
    var items = menuNow();
    if (typeof SHOPS !== 'undefined') SHOPS.s2_hase.items = items;
    if (typeof c2Shop === 'function') c2Shop('s2_hase');
  }
  P2.shopCost = shopCost; P2.menuNow = menuNow; P2.nailsOn = nailsOn;

  /* ---------------- turf ---------------- */
  var EAST_R = [3760, 2760, 4900, 3300];
  function takeEastTurf() {
    var n = NS(); n.won = n.won || {}; n.won.east = 1; E().vend_eastst = 1;
    try {
      var T = root.FFF_C2TURF;
      if (T && T.Q && T.Q.P && !T.Q.P.some(function (r) { return r[0] === 3760 && r[1] === 2760 && r[2] === 4900; })) T.Q.P.push(EAST_R.slice());
    } catch (eT) {}
    if (root.FFF_NQ && root.FFF_NQ.BLK && !root.FFF_NQ.BLK.east) root.FFF_NQ.BLK.east = { n: 'MINATO-S\u014c', r: EAST_R.slice() };
    sv();
    try { if (typeof NQ !== 'undefined' && NQ.sting) NQ.sting('east', function () {}); } catch (eS) {}
  }
  P2.takeEastTurf = takeEastTurf;

  /* ---------------- pin / Four Corners ---------------- */
  var FLIP_AT = [2360, 3190];
  var RUNS = [
    { at: [3610, 3050], k: 's2_r0', lab: 'East canal bridge' },
    { at: [3610, 3480], k: 's2_r1', lab: 'East canal bridge' },
    { at: [4100, 3490], k: 's2_r2', lab: 'SE street' }
  ];
  function s2Tgt() {
    if (!punkAfterSeal() || !wagaDone()) return null;
    if (qOn() && (stg() === '' || stg() === 'open')) return { x: FLIP_AT[0], y: FLIP_AT[1], lab: 'Flip', loc: 'Night Runs \u00b7 Flip' };
    if (qOn() && stg() === 'r1') return { x: RUNS[0].at[0], y: RUNS[0].at[1], lab: 'Night run', loc: RUNS[0].lab };
    if (qOn() && stg() === 'r2') return { x: RUNS[1].at[0], y: RUNS[1].at[1], lab: 'Night run', loc: RUNS[1].lab };
    if (qOn() && stg() === 'r3') return { x: RUNS[2].at[0], y: RUNS[2].at[1], lab: 'Night run', loc: RUNS[2].lab };
    if (qOn() && stg() === 'talk') return { x: LOB_AT[0], y: LOB_AT[1], lab: 'Minato-s\u014d', loc: 'Talk to the tenants' };
    return null;
  }
  P2.s2Tgt = s2Tgt;
  if (typeof c2LocksT === 'function') {
    var lt0 = c2LocksT;
    c2LocksT = function () {
      try { var t = s2Tgt(); if (t) return { room: 'town', x: t.x, y: t.y, lab: t.lab, loc: t.loc }; } catch (eL) {}
      return lt0.apply(this, arguments);
    };
  }

  function chainRepair() {
    if (!punkAfterSeal() || !wagaDone()) return;
    if (!qOn() && !qDone()) { qOpen(); if (!stg()) setStg('open'); }
  }
  P2.chainRepair = chainRepair;

  /* ---------------- pops ---------------- */
  var HASE = null, MORI = null, NAO = null, HARU = null;
  function popShop() {
    if (room() !== 'mshop') { if (HASE) { try { kill(HASE); } catch (eK) {} HASE = null; } return; }
    if (HASE && HASE.el && HASE.el.parentNode) return;
    HASE = npc('nq_hase', 780, 520, Math.PI / 2);
    try { if (typeof waddle === 'function') waddle(HASE, 0, Math.PI / 2); } catch (eW) {}
    try { if (W.c2n) W.c2n.s2h = HASE; } catch (eN) {}
  }
  function popLobby() {
    if (room() !== 'mina') {
      [MORI, NAO, HARU].forEach(function (s) { if (s) try { kill(s); } catch (eK) {} });
      MORI = NAO = HARU = null; return;
    }
    if (!(MORI && MORI.el && MORI.el.parentNode)) MORI = npc('nq_mori', 720, 360, Math.PI / 2);
    if (!(NAO && NAO.el && NAO.el.parentNode)) NAO = npc('nq_nao', 260, 620, Math.PI / 2);
    if (!(HARU && HARU.el && HARU.el.parentNode)) HARU = npc('nq_haru', 250, 400, Math.PI / 2);
  }

  /* ---------------- talks + fights ---------------- */
  var fighting = 0;
  function flipTalk() {
    if (busy()) return;
    lockIn(1);
    talk(pv(VO.brief), function () { lockIn(0); setStg('r1'); qStep(1); });
  }
  function tenantTalk(who) {
    if (busy()) return true;
    var taken = nailsOn() || qDone() || stg() === 'talk' || stg() === 'done';
    var table = taken ? VO.taken[who] : VO.held[who];
    lockIn(1);
    talk(pv(table), function () {
      lockIn(0);
      var t = talked(); t[who] = 1; sv();
      if (stg() === 'talk' && t.mori && t.nao && t.haru) finishQuest();
    });
    return true;
  }
  function haseTalk() {
    if (busy()) return true;
    if (nailsOn() || qDone()) {
      lockIn(1);
      talk(pv(VO.haseOpen), function () { lockIn(0); openShop(); });
    } else {
      lockIn(1);
      talk(pv(VO.haseHeld), function () { lockIn(0); openShop(); });
    }
    return true;
  }
  function stairTalk() {
    if (busy()) return true;
    lockIn(1);
    talk(pv(VO.stair), function () { lockIn(0); });
    return true;
  }
  function startRun(i) {
    if (fighting || busy()) return;
    fighting = 1;
    lockIn(1);
    talk(pv(VO.run[i]), function () {
      lockIn(0);
      var R = 'c2_boso';
      var ctx = { dg: 'c2', dgk: 's2_r' + i + '_0', dgks: ['s2_r' + i + '_0', 's2_r' + i + '_1'], s2k: 's2_r' + i, s2: 1 };
      if (i < 2) ctx.s2br = 1; else ctx.s2se = 1;
      try { fight([R, R], false, ctx); } catch (eF) { fighting = 0; ev('world:s2p2:err:fight:' + (eF && eF.message)); }
    });
  }
  function finishQuest() {
    takeEastTurf();
    setStg('done');
    qClose();
    /* Four Corners still points at Masa; do not open unbuilt Phase 3. */
  }
  function runWon(i) {
    fighting = 0;
    whenFree(function () {
      talk(pv(VO.wonRun[i]), function () {
        if (i === 0) { setStg('r2'); qStep(2); }
        else if (i === 1) { setStg('r3'); qStep(3); }
        else {
          /* last runner pointed at the boat house in VO.wonRun[2]. Compassionate talks to the tenants; the others can close. */
          takeEastTurf();
          if (path() === 'balanced') { setStg('talk'); qStep(4); }
          else finishQuest();
        }
      });
    });
  }
  if (typeof onFightEnd === 'function') {
    var of0 = onFightEnd;
    onFightEnd = function (win, c) {
      var r = of0.apply(this, arguments);
      try {
        if (c && c.s2k && /^s2_r/.test(c.s2k)) {
          if (!win) { fighting = 0; return r; }
          var i = +String(c.s2k).replace('s2_r', '') || 0;
          runWon(i);
        }
      } catch (eE) {}
      return r;
    };
  }

  function flowTick() {
    if (!on() || !qOn() || busy() || fighting) return;
    var r = W.ryo; if (!r) return;
    var s = stg();
    if (s === 'r1' && Math.hypot(r.x - RUNS[0].at[0], r.y - RUNS[0].at[1]) < 80) startRun(0);
    else if (s === 'r2' && Math.hypot(r.x - RUNS[1].at[0], r.y - RUNS[1].at[1]) < 80) startRun(1);
    else if (s === 'r3' && Math.hypot(r.x - RUNS[2].at[0], r.y - RUNS[2].at[1]) < 80) startRun(2);
  }

  /* spots / tags / talk */
  if (typeof c2Tags === 'function') {
    var tags0 = c2Tags;
    c2Tags = function (id, D) {
      var out = tags0.apply(this, arguments);
      try {
        if (out && on()) out = out.filter(function (t) {
          if (!t || !t.key) return true;
          if (t.key.indexOf(':s2_e_mshop') >= 0 || t.key.indexOf(':s2_e_mina') >= 0) return punkAfterSeal();
          if (t.key.indexOf(':s2_p2_flip') >= 0) return wagaDone() && qOn() && (stg() === '' || stg() === 'open');
          if (t.key.indexOf(':s2_hase_shop') >= 0) return room() === 'mshop';
          if (t.key.indexOf(':s2_stair') >= 0 || t.key.indexOf(':s2_talk_') >= 0 || t.key.indexOf(':s2_to_') >= 0) return room() === 'mina' || room() === 'mshop';
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
          if (a === 's2_e_mshop' || a === 's2_e_mina') return act0.apply(this, arguments);
          if (a === 's2_p2_flip') { flipTalk(); return true; }
          if (a === 's2_to_lobby') { if (typeof c2Go === 'function') c2Go('mina', [200, 400, 1]); return true; }
          if (a === 's2_to_shop') { if (typeof c2Go === 'function') c2Go('mshop', [200, 400, 1]); return true; }
          if (a === 's2_stair') { stairTalk(); return true; }
          if (a === 's2_talk_mori') { tenantTalk('mori'); return true; }
          if (a === 's2_talk_nao') { tenantTalk('nao'); return true; }
          if (a === 's2_talk_haru') { tenantTalk('haru'); return true; }
          if (a === 's2_hase_shop') { haseTalk(); return true; }
        }
      } catch (e) { ev('world:s2p2:err:act:' + (e && e.message)); }
      return act0.apply(this, arguments);
    };
  }
  if (typeof c2Talk === 'function') {
    var tk0 = c2Talk;
    c2Talk = function (s) {
      try {
        if (on() && s) {
          var id = s.s2id || s.id || (s.el && s.el.dataset && s.el.dataset.npc);
          if (id === 'n13flip' && wagaDone() && qOn() && (stg() === '' || stg() === 'open')) { flipTalk(); return true; }
          if (id === 'nq_hase') { haseTalk(); return true; }
          if (id === 'nq_mori') { tenantTalk('mori'); return true; }
          if (id === 'nq_nao') { tenantTalk('nao'); return true; }
          if (id === 'nq_haru') { tenantTalk('haru'); return true; }
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
          if (id === 'n13flip' && wagaDone() && qOn() && (stg() === '' || stg() === 'open')) { flipTalk(); return true; }
          if (id === 'nq_hase') { haseTalk(); return true; }
          if (id === 'nq_mori') { tenantTalk('mori'); return true; }
          if (id === 'nq_nao') { tenantTalk('nao'); return true; }
          if (id === 'nq_haru') { tenantTalk('haru'); return true; }
        }
      } catch (eT) {}
      return tn0.apply(this, arguments);
    };
  }

  if (typeof c2Frame === 'function') {
    var fr0 = c2Frame;
    c2Frame = function (dt) { fr0.apply(this, arguments); try { if (on()) { placeDoor(); flowTick(); } } catch (e) { if (!P2.ferr) { P2.ferr = 1; ev('world:s2p2:err:frame:' + (e && e.message)); } } };
  }
  if (typeof c2Pop === 'function') {
    var pop0 = c2Pop;
    c2Pop = function () { pop0.apply(this, arguments); try { hookAmb(); if (on()) { chainRepair(); placeDoor(); hookBattle(); popShop(); popLobby(); if (room() === 'mina' || room() === 'mshop') paintRoom(); } syncIndoorRain(); } catch (eP) {} };
  }
  try { chainRepair(); } catch (eC) {}
  ev('world:s2p2:ready');
  } catch (eS2) { try { ev('world:s2p2:err:init:' + (eS2 && eS2.message)); console.warn('S2P2 init', eS2); } catch (e2) {} }
})();
