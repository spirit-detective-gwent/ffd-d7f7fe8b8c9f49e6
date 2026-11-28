/* v6.5.66 FFF_HP: the hotel-door fights and every Ch2 street gang fight (Erik t614u-t622u).
 *  - Two at a time: an engagement (walk-up touch, tap / Alley Cat from behind, the crew walk-up) pulls in the man you hit plus the nearest
 *    man of his crew - never the whole crew. One left = one. A back attack on a quest crew (or on a man with a mate close by) starts that
 *    fight with him on cut HP instead of a lone knockout, so the quest beats (guest thanks, counts, the next objective) always run.
 *  - They turn: held crews (the hotel door, the west wall, the takeover corners) face Ryo once he has stood near them for a moment, and look
 *    back to their post when he leaves. A quick approach from behind still gets the sneak attack.
 *  - Wins stick: quest crews are never put on the street-gang respawn timer (SAVE.crewDown 'c2_nq_c1' ... wiped their win flags once the
 *    timer ran out while Ryo was away, e.g. in Kissa Gekko). Every quest-crew win is also recorded in c2S().e.hpWin, and a repair on each town
 *    pop puts lost flags back, lifts a legacy stage (cold / paint) the flags lost, drops beaten men still standing, and re-runs the quest chain.
 *  - Never stuck: a guard on the existing per-frame dlgGuard hook releases every world lock (busy / cut / dlg / scr / forced / runUp / ambOn /
 *    opnOn / dgFight) and removes a dead block-win overlay when nothing is on screen to own them (no dialog, battle, result, menu, fade,
 *    banner, rest, sting or scripted walk) for 8 s. A fight start also clears leftover world overlays that would sit over the cards.
 * Wraps only; no new rAF / interval (frame work rides c2Frame and dlgGuard). Not on the Fierce / Strategic copies (shared engine only). */
(function (root) {
  try {
  if (typeof c2S !== 'function' || typeof c2v2Go !== 'function' || typeof ambFight !== 'function' || typeof noticedPack !== 'function') { try { ev('world:hp:skip'); } catch (e0) {} return; }
  var HP = root.FFF_HP = { v: 1, unlocks: 0, repairs: 0, last: '' };
  var QK = /^(n13_look|nq_(w[12]|c[0-2]|p[0-2])|s2_w[12])$/; /* quest crews: scripted, never on the respawn timer */
  var QKEY = /^(n13_look|nq_[a-z]\d?|s2_[a-z]+\d?)_\d+$/;
  var SCRIPTED = /^(nq_x|nq_d|s2_x)$/; /* the staged three-man beats (Flip's clash, Kaneda's door, Wagashi clash) keep their own line-up */
  function now() { return performance.now(); }
  function town() { try { return typeof chN === 'function' && chN() === 2 && typeof c2Room === 'function' && c2Room() === 'town'; } catch (e) { return false; } }
  function live(o) { return !!(o && o.s && o.s.el && o.s.el.parentNode && !o.gone && !o.downed && !(o.stun > 0) && (W.dgF || []).indexOf(o) >= 0); }
  function gangFoe(f) { return !!(f && f.c2 && f.crew && f.s && town() && !f.g39ally && !/^(lm_|gaunt_|g39bk)/.test(String(f.crew)) && !/^(mb|c2_boss)/.test(String(f.id || '')) && !SCRIPTED.test(String(f.crew))); }
  function mate(f, R) { var best = null, bd = R || 260; if (!f || !f.s) return null;
    (W.dgF || []).forEach(function (o) { if (o === f || !live(o) || o.crew !== f.crew || o.g39ally) return; var d = Math.hypot(o.s.x - f.s.x, o.s.y - f.s.y); if (d < bd) { bd = d; best = o; } }); return best; }
  HP.mate = mate;
  /* ---------------- 1) two at a time ---------------- */
  var hpQ = null;
  var as0 = ambStrike; ambStrike = function (q) { var p = hpQ; hpQ = q; try { return as0.apply(this, arguments); } finally { hpQ = p; } };
  var fx0 = ambFx; ambFx = function (side) { var r = fx0.apply(this, arguments);
    try { var q = hpQ; if (r && r.ko && q && gangFoe(q) && (QK.test(String(q.crew)) || mate(q))) { r = { k: side === 'back' ? SNK.back.even : SNK.front.ko }; ev('world:hp:noko:' + q.key); } } catch (e) {} return r; };
  var np0 = noticedPack; noticedPack = function (p) { var g = np0.apply(this, arguments);
    try { if (gangFoe(p) && W.ambOn && W.ambOn.q === p) { var m = mate(p); g = [p].concat(m ? [m] : []); if (m && m.s && m.s.el) m.s.el.style.visibility = 'hidden'; ev('world:hp:pull:amb:' + p.crew + ':' + g.length); } } catch (e) {} return g; };
  var capF = null;
  var mn0 = c2v2Men; c2v2Men = function (k) { var L = mn0.apply(this, arguments); try { if (capF && k === capF.crew) { var m = mate(capF); L = [capF].concat(m ? [m] : []); } } catch (e) {} return L; };
  var go0 = c2v2Go; c2v2Go = function (f, why) { var p = capF; capF = gangFoe(f) ? f : null; try { var r = go0.apply(this, arguments); if (capF && r) ev('world:hp:pull:go:' + f.crew + ':' + why); return r; } finally { capF = p; } };
  /* ---------------- 2) they turn ---------------- */
  var TURN = { R: 125, OUT: 200, T: 0.8 }; HP.TURN = TURN;
  function postFa(f) { return f.face != null ? f.face : (f.fa0 != null ? f.fa0 : f.fa); }
  /* waddle draws a standing street foe (.dgfoe) on its front row whatever its facing (and the street frame re-waddles it), so a turn
     changed nothing on screen. A turned man carries s.hpFa and keeps the walk sheet's still frame for that facing (no new loop). */
  function rowFor(s) { var bw = !s.loop && !s.hurtA && bwSheet(s); if (!bw) return; var k = s.k || 1, d = bwDir(s, s.hpFa), nc = shCols(bw);
    frameBg(s.el, bw, nc === 8 ? 2 : 0, d, SPW * k, SPH * k); if (s.el.getAttribute('data-dir') !== '' + d) s.el.setAttribute('data-dir', d); }
  if (typeof waddle === 'function') { var wd0 = waddle; waddle = function (s, moved) { var r = wd0.apply(this, arguments); if (s && s.hpFa != null && !(moved > 0)) { try { rowFor(s); } catch (e) {} } return r; }; }
  function turnTo(f, fa, keep) { f.clashFa = fa; f.fa = fa; f.s.hpFa = keep ? fa : null; try { f.s.flip = !bwSheet(f.s) && Math.cos(fa) < -0.1; waddle(f.s, 0, fa); } /* a walk sheet has its own left row: no mirror */ catch (e) {} }
  function turner(f) { return f && f.c2 && f.s && f.st === 'g38' && !f.clashTo && !f.g38x && (f.qsHold || (f.nq && f.face != null)) && live(f); }
  var tAcc = 0;
  function turnTick(dt) { tAcc += dt; if (tAcc < 0.1) return; var step = tAcc; tAcc = 0; var r = W.ryo; if (!r || !W.dgF) return;
    var quiet = W.dgFight || W.busy || W.dlg || W.cut || W.paused;
    W.dgF.forEach(function (f) { if (!turner(f)) return; var d = Math.hypot(f.s.x - r.x, f.s.y - r.y);
      if (f.hpTurn) { if (d > TURN.OUT && !quiet) { f.hpTurn = 0; f.hpNear = 0; f.clashFa = null; turnTo(f, postFa(f)); f.clashFa = null; f.s.hpFa = null; ev('world:hp:turn:back:' + f.key); } else if (!quiet) turnTo(f, Math.atan2(r.y - f.s.y, r.x - f.s.x), 1); return; }
      if (d < TURN.R && !W.hid && !quiet) { f.hpNear = (f.hpNear || 0) + step; if (f.hpNear >= TURN.T) { if (f.fa0 == null) f.fa0 = postFa(f); f.hpTurn = 1; turnTo(f, Math.atan2(r.y - f.s.y, r.x - f.s.x), 1); try { bubbleOn(f.s, '?'); } catch (eB) {} ev('world:hp:turn:' + f.key); } }
      else if (d > TURN.R) f.hpNear = 0; }); }
  HP.turnTick = turnTick;
  /* after a fight the men of that crew who are still standing saw it: they face Ryo at once */
  function sawIt(ks) { var crews = {}; (ks || []).forEach(function (k) { var m = /^(.*)_\d+$/.exec(String(k || '')); if (m) crews[m[1]] = 1; });
    (W.dgF || []).forEach(function (f) { if (crews[f.crew] && turner(f)) f.hpNear = TURN.T; }); }
  /* ---------------- 3) wins stick ---------------- */
  function rec() { var e = c2S().e || (c2S().e = {}); if (!e.hpWin || typeof e.hpWin !== 'object') e.hpWin = {}; return e.hpWin; }
  if (typeof c2v2Mark === 'function') { var mk0 = c2v2Mark; c2v2Mark = function (k) { if (QK.test(String(k))) { ev('world:hp:nomark:' + k); return; } return mk0.apply(this, arguments); }; }
  function purgeDown() { var D = SAVE.crewDown, n = 0; if (!D) return 0; for (var kk in D) if (Object.prototype.hasOwnProperty.call(D, kk) && /^c2_/.test(kk) && QK.test(kk.slice(3))) { delete D[kk]; n++; } if (n) ev('world:hp:purgedown:' + n); return n; }
  HP.purgeDown = purgeDown;
  if (typeof c2v2Sweep === 'function') { var sw0 = c2v2Sweep; c2v2Sweep = function () { if (SAVE.crewDown) purgeDown(); return sw0.apply(this, arguments); }; }
  var da0 = dgAfter; dgAfter = function (win, st) {
    try { var c = st && st.ctx; if (win && !(st && st.escaped) && c && c.dg === 'c2') { var R = rec(), n = 0; (c.dgks || [c.dgk]).forEach(function (k) { if (QKEY.test(String(k || ''))) { R[k] = 1; n++; } }); if (n) ev('world:hp:rec:' + n); } } catch (e) {}
    return da0.apply(this, arguments); };
  function fullDown(f, p, i) { return !!(f[p + i + '_0'] && f[p + i + '_1']); }
  function repair(why) {
    var N = root.FFF_NQ, S = c2S(), f = S.f || (S.f = {}), q = S.q || {}, ch = 0, R = rec(), D0 = SAVE.crewDown || {}, hint = {};
    Object.keys(D0).forEach(function (kk) { if (/^c2_nq_[cp]\d$/.test(kk)) hint[kk.slice(3)] = 1; }); /* the respawn timer remembers which crews were beaten */
    ch += purgeDown();
    Object.keys(R).forEach(function (k) { if (!f[k]) { f[k] = 1; ch++; } });
    if (N && N.stg && N.setStg) [['c', 'cold', 'cq2_nq_cold'], ['p', 'paint', 'cq2_nq_paint']].forEach(function (L) {
      if (!(q[L[2]] != null && q[L[2]] !== 9)) return; var p = 'nq_' + L[0], st = Math.min(3, N.stg(L[1]) | 0), down = [0, 1, 2].filter(function (i) { return fullDown(f, p, i); });
      /* a save from before the record: the stage remembers how many crews were beaten even after the flags went; put them back */
      var ord = [0, 1, 2].sort(function (a, b) { return (hint[p + b] ? 1 : 0) - (hint[p + a] ? 1 : 0) || a - b; });
      for (var oi = 0; oi < 3 && down.length < st; oi++) { var i = ord[oi]; if (down.indexOf(i) >= 0) continue; f[p + i + '_0'] = 1; f[p + i + '_1'] = 1; R[p + i + '_0'] = 1; R[p + i + '_1'] = 1; down.push(i); ch++; ev('world:hp:restore:' + p + i); }
      if (down.length > st && down.length < 3) { N.setStg(L[1], down.length); ch++; } /* a knockout win that skipped the count (3/3 is left to the quest chain: it steps the quest) */ });
    /* men whose win is on the books do not stand on the street */
    (W.dgF || []).slice().forEach(function (o) { if (o && o.key && f[o.key] && QKEY.test(o.key) && W.dgFight !== o) { try { g38tDrop(o); } catch (eD) {} ch++; } });
    if (ch) { HP.repairs++; try { if (N && N.crewSync && town()) N.crewSync(); } catch (e1) {} try { if (N && N.chainRepair) N.chainRepair(); } catch (e2) {} try { if (root.FFF_QS && FFF_QS.repair) FFF_QS.repair(); } catch (e3) {} save(); ev('world:hp:repair:' + why + ':' + ch); }
    return ch; }
  HP.repair = repair;
  /* ---------------- 4) never stuck ---------------- */
  var LK = ['busy', 'cut', 'dlg', 'scr', 'forced', 'runUp', 'ambOn', 'opnOn', 'dgFight'];
  var SCN = '#wdlg.on,#game.on,#result.on,#wpause.on,#wrest.on,#wban.on,#wspot.on,#wlvc.on,#eatg.on,.eatg.on,#title.on';
  function owned() { var st = document.getElementById('nqsting');
    if (st) { st.hpT = st.hpT || now(); if (now() - st.hpT < 12000) return 'sting'; }
    if (document.querySelector(SCN)) return 'dom'; if (W.fading || W.pan || W.paused) return 'w';
    /* soft owners (a scripted walk, an action clip, a cut runner): trusted for 30 s, then the lock goes anyway */
    if (W.cutRun || W.snk || (W.ryo && (W.ryo.actMove || W.ryo.act)) || (W.aoi && W.aoi.actMove) || (W.path && W.path.length && W.cut)) return 'soft'; return ''; }
  function held() { var o = []; LK.forEach(function (k) { if (W[k]) o.push(k); }); return o; }
  function release(why) { var was = held(); var st = document.getElementById('nqsting'); if (st && st.hpT && now() - st.hpT >= 12000) { try { st.remove(); } catch (e) {} was.push('sting'); }
    W.busy = false; W.cut = false; W.dlg = false; W.scr = 0; W.forced = null; W.runUp = null; W.ambOn = null; W.opnOn = null; W.ambT = null; W.dgFight = null; W.c2v2Go = 0; W.g38gPick = null; W.c1eGo = 0;
    try { if (typeof stickEnd === 'function') stickEnd(); } catch (e2) {} try { var b = document.getElementById('wban'); if (b) b.className = ''; } catch (e3) {}
    HP.unlocks++; HP.last = why + ':' + was.join('+'); ev('world:hp:unlock:' + HP.last); return was; }
  HP.release = release; HP.held = held; HP.owned = owned;
  var gT = 0, sT = 0, gAcc = 0; HP.GUARD_S = 8; HP.SOFT_S = 30;
  function guard(dt) { gAcc += dt; if (gAcc < 0.5) return; var step = gAcc; gAcc = 0; if (!W.on) { gT = sT = 0; return; }
    var h = held(), st = document.getElementById('nqsting'); if (!h.length && !st) { gT = sT = 0; return; }
    var o = owned(); if (o === 'soft') { gT = 0; sT += step; if (sT >= HP.SOFT_S) { sT = 0; release('soft'); } return; } sT = 0;
    if (o) { gT = 0; return; } gT += step; if (gT < HP.GUARD_S) return; gT = 0; release('idle'); }
  HP.guard = guard;
  if (typeof dlgGuard === 'function') { var dg0 = dlgGuard; dlgGuard = function (dt) { dg0.apply(this, arguments); try { guard(dt || 0); } catch (e) { ev('world:hp:err:guard:' + (e && e.message)); } }; }
  /* a fight start: a world overlay left over from the street (a dead block-win sting, a banner) must not sit over the cards */
  if (typeof fight === 'function') { var fi0 = fight; fight = function () { try { var st = document.getElementById('nqsting'); if (st && st.hpT && now() - st.hpT >= 12000) { st.remove(); ev('world:hp:fight:sting'); } } catch (e) {} return fi0.apply(this, arguments); }; }
  /* ---------------- a shut doorway must not trap the player ----------------
     intDoorsFrame walks Ryo through any doorway whose lip he stands on (useDoor: kills the stick, clears the path, acts). The NQ
     shopfront doors (Kitsune Hotel, udon, motors) act by doing nothing while their room is shut, and useDoor clears doorHold, so
     standing on a shut door's lip re-fired useDoor every frame: the stick died the instant it was touched (only pinch zoom got
     through, it runs before the stick), and the handler ran 60 times a second (the hot phone). A doorway that did nothing is now
     held until Ryo steps off its lip, and the shut hotel door says why once. */
  HP.doorHolds = 0;
  if (typeof useDoor === 'function') { var ud0 = useDoor; useDoor = function (sp) { var I = W.inside, id = I && I.id, r = ud0.apply(this, arguments);
    try { if (sp && W.inside === I && !W.fading && !W.dlg && !W.busy && !W.cut && !W.scr && !(I && I.id !== id)) { W.doorHold = sp.id; W.arrive = null; HP.doorHolds++; ev('world:hp:doorhold:' + sp.id);
      if (sp.id === 'nq_e_hotel' && W.hpDoorSaid !== sp.id) { W.hpDoorSaid = sp.id; try { toast('Locked. The crews out front run this door.'); } catch (e1) {} } }
      else if (sp) W.hpDoorSaid = null; } catch (e) { ev('world:hp:err:door:' + (e && e.message)); } return r; }; }
  /* ---------------- hooks: town pop, fight back, frame ---------------- */
  if (typeof c2Pop === 'function') { var pp0 = c2Pop; c2Pop = function () { var r = pp0.apply(this, arguments); try { if (typeof chN === 'function' && chN() === 2) repair('pop'); } catch (e) { ev('world:hp:err:pop:' + (e && e.message)); } return r; }; }
  if (typeof c2Back === 'function') { var cb0 = c2Back; c2Back = function (win, st0) { var r = cb0.apply(this, arguments); try { var c = (st0 && st0.ctx) || {}; sawIt(c.dgks || [c.dgk]); if (town()) setTimeout(function () { try { repair('back'); } catch (e) {} }, 900); } catch (e) {} return r; }; }
  if (typeof c2Frame === 'function') { var fr0 = c2Frame; c2Frame = function (dt) { var r = fr0.apply(this, arguments); try { if (town()) turnTick(dt || 0); } catch (e) { ev('world:hp:err:turn:' + (e && e.message)); } return r; }; }
  ev('world:hp:ready');
  } catch (eH) { try { ev('world:hp:err:init:' + (eH && eH.message)); } catch (e2) {} }
})(window);
