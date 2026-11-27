/* v6.5.63 FFF_S2 (Punk-route seal 2, phase 1): Wagashi Row. Journal / Four Corners
 * points at Masa after Gōda's seal, not Jin. Club Kitsune / Tetsu stays optional.
 * Quest cq2_s2_waga: Flip briefing (three path voices), Rider waves, then a 3v3
 * clash with Punk backup at X3; on win the row flips to Punk ownership (recolor
 * sting) and the clash loop stops. Wagashi door + cel interior + Chiyo's counter
 * (sweet rolls, dango, Nails' price after takeover). New art is behind S2.ART
 * Art is wired (S2.ART): Chiyo, the north Wagashi door, the interior, the X3 battle backdrop, and the eat game.
 * Wraps only; no new always-running loops (frame work rides c2Frame).
 * Does not edit existing Fierce/Strategic Nails copy. */
(function () {
  try {
  if (typeof c2S !== 'function' || typeof C2W === 'undefined' || !C2W || typeof INT === 'undefined' || !INT.c2_town) {
    try { ev('world:s2:skip'); } catch (e0) {} return;
  }
  var S2 = root.FFF_S2 = { v: 1, ART: true };
  /* GGD-51 fight-end bridge: the S2P2-P6 modules listen on onFightEnd(win, ctx), which the base never defines.
   * Define it once on root and call it from c2Back (every Ch2 dungeon / interior fight result). Wraps only. */
  if (typeof root.onFightEnd !== 'function') root.onFightEnd = function () {};
  if (typeof c2Back === 'function' && !c2Back._ofe) {
    var cbOfe = c2Back;
    c2Back = function (win, st0) {
      var r = cbOfe.apply(this, arguments);
      try { if (typeof root.onFightEnd === 'function') root.onFightEnd(!!win && !(st0 && st0.escaped), (st0 && st0.ctx) || {}); } catch (eO) { ev('world:s2:err:ofe:' + (eO && eO.message)); }
      return r;
    };
    c2Back._ofe = 1;
  }
  function on() { return (typeof c2On !== 'function' || c2On()) && (typeof chN !== 'function' || chN() === 2); }
  function S() { return c2S(); }
  function E() { return c2S().e; }
  function room() { try { return c2Room(); } catch (e) { return null; } }
  function inTown() { return room() === 'town'; }
  function nailsRun() { return on() && E().run_fac === 'arc'; }
  function busy() { return !!(W.dgFight || W.dlg || W.busy || W.cut || W.fading || W.paused); }
  function later(ms, fn) { setTimeout(function () { try { fn(); } catch (e) { ev('world:s2:err:later:' + (e && e.message)); } }, ms); }
  function talk(lines, done) { W.dlg = true; scene(null, lines, function () { W.dlg = false; if (done) done(); }); }
  function lockIn(on1) { if (on1) { W.cut = true; W.path = []; if (W.ryo) W.ryo.v = 0; try { stickEnd(); } catch (e) {} } else W.cut = false; }
  function sv() { try { if (typeof c2QSync === 'function') c2QSync(); } catch (e) {} save(); }
  function path() { var p = 'balanced'; try { p = c2Path(); } catch (e) {} return p === 'fierce' || p === 'strategic' ? p : 'balanced'; }
  function npc(id, x, y, fa) { var s = c2Npc(id, x, y, fa == null ? Math.PI / 2 : fa); s.el.classList.add('s2'); s.s2id = id; s.el.dataset.npc = id; return s; }
  function face(s, x, y) { if (!s) return; if (s.walker) c2Face(s, x, y); else waddle(s, 0, Math.atan2(y - s.y, x - s.x)); }
  function kill(s) { if (s && s.el && s.el.parentNode) s.el.remove(); if (s) s.gone = 1; }
  function inR(r, x, y) { return x >= r[0] && x < r[2] && y >= r[1] && y < r[3]; }
  function say(lines) { var tries = 0; (function go() { try { comment(lines); } catch (e) {} var b = document.getElementById('wcomment'); if ((!b || !b.innerText) && ++tries < 10) setTimeout(go, 400); })(); }
  function move(s, pts, sp, done) {
    if (!s || !s.el) { if (done) done(); return; }
    var i = 0, last = performance.now(), tok = s.s2tok = (s.s2tok | 0) + 1; s.runK = 0;
    (function step() {
      if (s.s2tok !== tok || !s.el || !s.el.parentNode) return;
      var now = performance.now(), dt = Math.min(0.05, (now - last) / 1000); last = now;
      var p = pts[i];
      if (!p) {
        if (s.walker) { s.actMove = 0; s.run = false; if (typeof animWalk === 'function') animWalk(s, 0); }
        else waddle(s, 0, s.fa);
        place(s, 0); if (done) done(); return;
      }
      var dx = p[0] - s.x, dy = p[1] - s.y, d = Math.hypot(dx, dy), mv = Math.min(d, sp * dt);
      if (d < 1.5) { i++; requestAnimationFrame(step); return; }
      s.x += dx / d * mv; s.y += dy / d * mv;
      if (s.walker) {
        s.actMove = 1; s.run = false;
        s.dir = typeof faceDir === 'function' ? faceDir(s.dir, dx, dy) : (Math.abs(dx) > Math.abs(dy) ? (dx < 0 ? 1 : 2) : (dy < 0 ? 3 : 0));
        if (typeof animWalk === 'function') animWalk(s, mv); else place(s, 0);
      } else { s.fa = Math.atan2(dy, dx); place(s, 0); waddle(s, mv, s.fa); }
      requestAnimationFrame(step);
    })();
  }
  /* Turn a c2Npc (map sheet + waddle) into a walker so existing walk-sheet frames play.
     c2Npc's waddle starts a cel idle loop; that loop sizes frames as the 4-col idle sheet.
     If it keeps ticking after we switch to the 8-col walk sheet, two Chiyos appear in one box. */
  function asWalker(s, who) {
    if (!s || !s.el) return s;
    try { if (typeof celLoopOff === 'function') celLoopOff(s); } catch (eL) {}
    s.walker = true; s.el.classList.add('walker');
    s.el.dataset.who = who; s.el.dataset.gait = 'walk';
    if (s.el.dataset.loop) delete s.el.dataset.loop;
    if (s.el.dataset.bw) s.el.dataset.bw = '';
    if (s.dir == null) s.dir = 0; if (s.fr == null) s.fr = 1; if (s.ph == null) s.ph = 1;
    s.sheet = null; s.loop = null;
    try { if (typeof SHC === 'object' && SHC) { SHC[who + '_walk'] = 8; SHC[who + '_idle'] = 4; } } catch (eS) {}
    try { if (typeof SHR === 'object' && SHR) { SHR[who + '_walk'] = 4; SHR[who + '_idle'] = 4; } } catch (eR) {}
    if (typeof animWalk === 'function') animWalk(s, 0); else place(s, 0);
    return s;
  }
  function esc(x) { return String(x == null ? '' : x).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function whenFree(fn, tries) { tries = tries || 0; if (!busy() && !document.getElementById('nqsting') && !(typeof W.c2busy !== 'undefined' && W.c2busy)) { try { fn(); } catch (e) { ev('world:s2:err:free:' + (e && e.message)); } return; } later(tries < 120 ? 250 : 1000, function () { whenFree(fn, tries + 1); }); }
  function V3(pre, mid, post) { var o = {}, PP = ['fierce', 'strategic', 'balanced']; PP.forEach(function (p) { o[p] = (pre || []).concat(mid[p] || [], post || []); }); return o; }
  function pv(x) { try { return typeof pathLines === 'function' ? pathLines(x) : (x[path()] || x.balanced || x); } catch (e) { return x.balanced || []; } }

  /* ---------------- state ---------------- */
  function NS() { var e = E(); if (!e.nq || typeof e.nq !== 'object') e.nq = {}; return e.nq; }
  function stg() { return NS().waga || ''; }
  function setStg(v) { NS().waga = v; sv(); ev('world:s2:st:' + v); }
  var QID = 'cq2_s2_waga';
  var Q = { id: QID, n: 'Wagashi Row', giver: 'Flip, for Nails',
    quote: 'Masa\u2019s Riders have the sweet-shop row. Take it.',
    loc: 'Kitsune-Ch\u016b\u014d \u00b7 Wagashi row' };
  if (typeof C2Q !== 'undefined') C2Q[QID] = { n: Q.n, steps: [Q.quote] };
  if (typeof C2QLOC !== 'undefined') C2QLOC[QID] = ['town', Q.loc];
  function qOpen() { var s = S(); if (s.q[QID] == null) s.q[QID] = 0; SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = s.q[QID] | 0; s.qa = QID; SAVE.qa = QID; SAVE.qTrack = ''; SAVE.qTrackPick = 0; sv(); ev('world:s2:quest:open'); }
  function qStep(n) { var s = S(); if (s.q[QID] == null || s.q[QID] === 9) return; s.q[QID] = Math.max(s.q[QID] | 0, n); SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = s.q[QID]; sv(); }
  function qClose() { var s = S(); if (s.q[QID] == null || s.q[QID] === 9) return; s.q[QID] = 9; SAVE.qs = SAVE.qs || {}; SAVE.qs[QID] = 9;
    SAVE.journalLog = SAVE.journalLog || []; if (SAVE.journalLog.indexOf(Q.n) < 0) SAVE.journalLog.push(Q.n);
    if (s.qa === QID) { s.qa = (typeof CQ !== 'undefined' && CQ.locks) || ''; SAVE.qa = s.qa; } sv(); ev('world:s2:quest:done');
    if (typeof window.c2QuestYen === 'function') window.c2QuestYen(QID, Q.n); }
  function qOn() { var q = S().q[QID]; return q != null && q !== 9; }
  function qDone() { return S().q[QID] === 9; }
  S2.Q = Q; S2.stg = stg; S2.setStg = setStg; S2.qOpen = qOpen; S2.qClose = qClose; S2.qOn = qOn; S2.qDone = qDone;

  /* ---------------- voices (new tables only) ---------------- */
  var VO = S2.VO = {};
  VO.brief = V3(
    [['n13flip', 'Masa\u2019s Riders have Wagashi row. Two waves, then they hold the middle.']],
    {
      fierce: [['ryo', 'We take the row tonight.'], ['aoi', 'Then we start it.'], ['n13flip', 'I\u2019ll bring two when you hit the middle. Don\u2019t wait.']],
      strategic: [['ryo', 'We let the waves spend themselves. Then we hit the middle with your crew.'], ['aoi', 'So the backup is the plan, not the cleanup.'], ['n13flip', 'That\u2019s it. Time it. I\u2019ll be there for the last one.']],
      balanced: [['ryo', 'The sweet shop first. I want to know who\u2019s behind that door.'], ['aoi', 'The Riders have been on it all week.'], ['n13flip', 'Then get them off it. I\u2019ll still back the clash.']]
    },
    [['n13flip', 'Punk side of the row. I\u2019ll hear it from the street.']]
  );
  VO.shopFirst = V3(
    [['nq_chiyo', 'You\u2026 you\u2019re not with them? They stand on my door every night. The glass goes first. Then the customers.']],
    {
      fierce: [['ryo', 'They won\u2019t be there after tonight.'], ['nq_chiyo', 'Then go. Please.']],
      strategic: [['ryo', 'If we take the row, the runs stop coming through your door.'], ['nq_chiyo', 'I just bake. I don\u2019t want a war on the step.']],
      balanced: [['ryo', 'We\u2019re here to get them off your door. Stay inside until it\u2019s quiet.'], ['aoi', 'We\u2019ll knock when it\u2019s safe.'], ['nq_chiyo', 'Thank you. I\u2019m Chiyo. The shop is\u2026 was\u2026 Chiyo Wagashi.']]
    },
    []
  );
  VO.clash = V3(
    [['n13flip', 'Told you. The middle, when it counts.'], ['c2_boso', 'Punks on Masa\u2019s row?']],
    {
      fierce: [['ryo', 'It\u2019s ours tonight.']],
      strategic: [['ryo', 'Your schedule just ran out.']],
      balanced: [['ryo', 'Get off her door.']]
    },
    []
  );
  VO.won = V3(
    [],
    {
      fierce: [['n13flip', 'Row\u2019s red. Masa will feel that.'], ['ryo', 'Good. Next.'], ['aoi', 'The shop\u2019s still standing. Barely.']],
      strategic: [['n13flip', 'That was the schedule. Masa\u2019s runs go through this row.'], ['ryo', 'Then we just cut his first street.'], ['aoi', 'The shop can open honest now.']],
      balanced: [['nq_chiyo', 'They\u2019re gone? They stood on my door every night.'], ['ryo', 'They won\u2019t come back. This street\u2019s ours, and it\u2019s yours too.'], ['aoi', 'We\u2019ll keep it that way.'], ['n13flip', 'Nails hears it from me. The row\u2019s red.']]
    },
    []
  );
  VO.shopOpen = V3(
    [['nq_chiyo', 'Come in, come in. The kettle\u2019s on. Nails said the row is yours now, so the prices are too.']],
    {
      fierce: [['ryo', 'Just the food. We\u2019re moving on.']],
      strategic: [['ryo', 'We\u2019ll be back. Masa still has the yards.']],
      balanced: [['ryo', 'Thank you, Chiyo-san. We\u2019ll keep the door clear.']]
    },
    []
  );
  VO.shopCold = V3(
    [['nq_chiyo', 'I\u2019m sorry. I can\u2019t open with them on the step.']],
    {
      fierce: [['ryo', 'Then we take the step.']],
      strategic: [['aoi', 'We clear the row first. Then you open.']],
      balanced: [['ryo', 'We\u2019ll get them off it. Stay inside.']]
    },
    []
  );

  /* ---------------- Four Corners / journal: Masa next, not Jin ---------------- */
  function punkAfterSeal() { return on() && nailsRun() && !!E().seal_sento; }
  function nextRival() {
    /* After Gōda, Punk route goes Masa (depot) then Jin (game). Skip already-sealed and own landmark. */
    var e = E(), own = 'arcade', order = ['depot', 'game', 'sento'];
    if (!punkAfterSeal()) return null;
    for (var i = 0; i < order.length; i++) if (order[i] !== own && !e['seal_' + order[i]]) return order[i];
    return null;
  }
  S2.nextRival = nextRival;
  function cornersQuote() {
    if (!punkAfterSeal()) return '';
    var e = E(), nR = 0, riv = ['depot', 'game', 'sento'];
    riv.forEach(function (k) { if (e['seal_' + k]) nR++; });
    var nx = nextRival(), T = { depot: 'freight yards', game: 'Neon Game Center', sento: 'Lantern Alley' };
    if (nR && nR < 3 && nx) return (nR === 1 ? 'One seal from rival ground.' : nR + ' seals from rival ground.') + ' Next door: ' + T[nx] + '.';
    if (nR === 0) return 'We shook on it with Nails. First door: Masa\u2019s freight yards.';
    return '';
  }
  function fixCornerSteps(steps) {
    if (!punkAfterSeal() || !steps || !steps.length) return steps;
    var e = E(), nx = nextRival(), curSet = false;
    steps.forEach(function (r) {
      if (!r || r.state === 'ok' || r.state === 'closed' || r.state === 'locked') return;
      var isMasa = /freight yards|Riders/.test(r.lab || '');
      var isJin = /Neon Game|Syndicate/.test(r.lab || '');
      var isGoda = /Lantern Alley|Hustlers/.test(r.lab || '');
      if (isGoda && e.seal_sento) { r.state = 'ok'; r.hint = null; return; }
      if (!curSet && nx === 'depot' && isMasa) {
        r.state = 'cur';
        r.hint = qOn() ? (stg() === 'clash' ? 'The middle of Wagashi row. Flip brings two.' : 'Wagashi row. Flip is on the Punk side.') : 'Flip, on the Punk side of Wagashi row.';
        curSet = true;
      } else if (!curSet && nx === 'game' && isJin) { r.state = 'cur'; curSet = true; }
      else if (r.state === 'cur' && !((nx === 'depot' && isMasa) || (nx === 'game' && isJin))) r.state = 'pend';
    });
    return steps;
  }
  S2.cornersQuote = cornersQuote;
  if (typeof c2LocksT === 'function') {
    var lt0 = c2LocksT;
    c2LocksT = function () {
      try {
        var t = s2Tgt(); if (t) return { room: 'town', x: t.x, y: t.y, lab: t.lab, loc: t.loc };
        if (punkAfterSeal() && !qDone() && nextRival() === 'depot') {
          return { room: 'town', x: 2560, y: 3120, lab: 'Wagashi', loc: 'Wagashi row \u00b7 Masa\u2019s Riders' };
        }
      } catch (eL) {}
      return lt0.apply(this, arguments);
    };
  }

  /* ---------------- journal card for Wagashi Row ---------------- */
  var X3C = [2560, 3190], FLIP_AT = [2360, 3190], SHOP_AT = [3080, 2640]; /* v6.5.64: stand in the lane, south of the Lucky 7 frontage */
  function rich() {
    var s = stg(), done = qDone(), out = [];
    var brief = s !== '' && s !== 'open';
    out.push({ lab: 'Hear Flip\u2019s job on Wagashi row', state: done || brief ? 'ok' : 'cur', sec: 'Wagashi row', hint: 'Punk side of the row. Flip is waiting.' });
    if (path() === 'balanced') out.push({ lab: 'Check on the sweet shop', state: done || s === 'sawshop' || s === 'w1' || s === 'w2' || s === 'clash' || s === 'done' ? 'ok' : (brief ? 'cur' : 'pend'), hint: 'Chiyo is behind the door.' });
    var w = { w1: 0, w2: 1, clash: 2, done: 3, sawshop: -1, open: -1 }[s]; if (w == null) w = -1; if (done) w = 3;
    out.push({ lab: 'Break the first Rider push', state: w > 0 ? 'ok' : w === 0 ? 'cur' : 'pend', hint: 'West end of the row. Walk up behind them.' });
    out.push({ lab: 'Break the second push', state: w > 1 ? 'ok' : w === 1 ? 'cur' : 'pend' });
    out.push({ lab: 'Clash with Flip\u2019s crew at your back', state: w > 2 ? 'ok' : w === 2 ? 'cur' : 'pend', hint: w === 2 ? 'The middle of the row. Flip brings two.' : '' });
    return out;
  }
  function detail(id, o) { o = o || {}; o.id = QID; o.kind = 'main'; o.n = Q.n; o.giver = Q.giver; o.quote = Q.quote;
    o.rich = rich(); o.steps = o.rich.map(function (x) { return [x.lab, x.state === 'ok']; }); var q = S().q[QID]; o.status = q === 9 ? 'done' : q != null ? 'on' : 'lock'; o.prog = o.quote; o.canTrack = q != null && q !== 9; o.loc = Q.loc; return o; }
  function stepsHtml(steps) { var h = '<ul class="chk">', last = ''; steps.forEach(function (x) { if (x.sec && x.sec !== last) { h += '</ul><p class="jsec">' + esc(x.sec) + '</p><ul class="chk">'; last = x.sec; }
      var cls = x.state === 'ok' ? 'ok' : x.state === 'cur' ? 'cur now' : 'now'; h += '<li class="' + cls + '">' + esc(x.lab) + '</li>'; if (x.hint && x.state !== 'ok') h += '</ul><p class="jhint">' + esc(x.hint) + '</p><ul class="chk">'; });
    return (h + '</ul>').replace(/<ul class="chk"><\/ul>/g, ''); }
  function cardHtml(cls) { var o = detail(), s = S(), q = s.q[QID], done = q === 9, mine = s.qa === QID;
    var h = '<div class="badges"><span class="badge">Main</span>' + (done ? '<span class="badge turn">Completed</span>' : '<span class="badge turn">In progress</span>') + (mine ? '<span class="badge track">Tracked</span>' : '') + '</div><h2>' + esc(o.n) + '</h2><p class="jquote">\u201c' + esc(o.quote) + '\u201d</p>' + stepsHtml(o.rich);
    if (!done) { if (!mine) h += '<button type="button" class="ph-cta" data-a="track" data-q="' + QID + '">Track</button>'; h += '<button type="button" class="ph-cta" data-a="showmap" data-q="' + QID + '">Show on map</button>'; }
    return '<article class="jcard' + (cls || '') + '" data-q="' + QID + '">' + h + '</article>'; }
  if (typeof c2QDetail === 'function') { var qd0 = c2QDetail; c2QDetail = function (id, o) {
    if (id === QID) return detail(id, o);
    var r = qd0.apply(this, arguments);
    try {
      if (on() && r && typeof CQ !== 'undefined' && id === CQ.locks && punkAfterSeal()) {
        var q2 = cornersQuote();
        if (q2) { r.quote = q2; r.prog = q2; }
        if (r.rich) { fixCornerSteps(r.rich); r.steps = r.rich.map(function (x) { return [x.lab, x.state === 'ok']; }); }
      }
    } catch (eD) {}
    return r;
  }; }
  if (typeof v640Rows === 'function') { var rows0 = v640Rows; v640Rows = function (done) { var rows = rows0.apply(this, arguments) || [], s = S(); try { if (on()) { var q = s.q[QID]; if (q != null && !rows.some(function (r) { return r.id === QID; }) && (done ? q === 9 : q !== 9)) rows.unshift({ id: QID, kind: 'main', n: Q.n }); } } catch (e) {} return rows; }; }
  if (typeof mainQuestRows === 'function') { var mq0 = mainQuestRows; mainQuestRows = function (mode) { var rows = mq0.apply(this, arguments) || [], s = S(); try { if (on() && mode !== 'done') { var q = s.q[QID]; if (q != null && q !== 9 && !rows.some(function (r) { return r.id === QID; })) rows.unshift({ id: QID, kind: 'main', n: Q.n, st: 'on' }); } } catch (e) {} return rows; }; }
  if (typeof v640From === 'function') { var from0 = v640From; v640From = function (id) { if (id === QID) return Q.giver; return from0.apply(this, arguments); }; }
  if (typeof phJournal === 'function') { var ph0 = phJournal; phJournal = function () { var h = ph0.apply(this, arguments); try { if (!on()) return h;
      h = h.replace(/<article class="jcard([^"]*)"[^>]*>[\s\S]*?<\/article>/g, function (m, cls) { if (m.indexOf('data-q="' + QID + '"') >= 0 || m.indexOf('<h2>' + Q.n + '</h2>') >= 0) return cardHtml(cls); return m; });
    } catch (e) { ev('world:s2:err:ph:' + (e && e.message)); } return h; }; }
  if (typeof questDetailHtml === 'function') { var qdh0 = questDetailHtml; questDetailHtml = function (id) { if (!on() || id !== QID) return qdh0.apply(this, arguments); var o = detail(id), Sst = (typeof JST !== 'undefined' && JST[o.status]) || ['', ''];
      return '<div class="jdet main" data-q="' + QID + '"><div class="jdh"><button class="jback" data-a="jqback" aria-label="Back to quests">\u2039 Back</button><span class="jbadge story">Main Quest</span><i class="jst ' + Sst[1] + '">' + Sst[0] + '</i></div><h3>' + esc(o.n) + '</h3><p class="jquote">\u201c' + esc(o.quote) + '\u201d</p><dl class="jdl"><dt>Quest giver</dt><dd class="jd-giver">' + esc(o.giver) + '</dd><dt>Progress</dt><dd class="jd-prog">' + esc(o.prog) + '</dd></dl>' + stepsHtml(o.rich) + '</div>'; }; }
  function s2Tgt() {
    if (!on() || !qOn()) return null;
    var t = stg(), p = FLIP_AT, lab = 'Flip';
    if (t === 'sawshop' || (path() === 'balanced' && t === 'open')) { p = SHOP_AT; lab = 'Sweet shop'; }
    if (t === 'w1') { p = [2460, 3190]; lab = 'Wagashi row'; }
    if (t === 'w2') { p = [2520, 3190]; lab = 'Wagashi row'; }
    if (t === 'clash') { p = X3C; lab = 'Wagashi row'; }
    return { qid: QID, kind: 'main', lab: lab, x: p[0], y: p[1] - 70, dg: 'c2', c2: 'town', rooms: [], loc: Q.loc, n: Q.n };
  }
  if (typeof c2QT === 'function') { var qt0 = c2QT; c2QT = function () { try { var t = s2Tgt(); if (t) return t; } catch (e) {} return qt0.apply(this, arguments); }; }
  S2.tgt = s2Tgt;

  /* ---------------- names / Chiyo sprite + portrait ---------------- */
  NM.nq_chiyo = 'Chiyo';
  (function wireChiyo() {
    if (typeof wUrl !== 'function' || typeof IMG === 'undefined') return;
    IMG.nq_chiyo_walk = wUrl('nq_chiyo_walk');
    IMG.nq_chiyo_idle = wUrl('nq_chiyo_idle');
    IMG.nq_chiyo_map = wUrl('nq_chiyo_map');
    IMG.nq_chiyo_fig = wUrl('nq_chiyo_fig');
    /* kinds we do not paint: keep the engine off the old clerk alias */
    IMG.nq_chiyo_run = IMG.nq_chiyo_walk;
    ['hurt', 'kn', 'lie', 'fig_hurt', 'fig_down'].forEach(function (sh) { IMG['nq_chiyo_' + sh] = IMG.nq_chiyo_fig; });
    if (typeof SHC !== 'undefined') { SHC.nq_chiyo_walk = 8; SHC.nq_chiyo_idle = 4; }
    if (typeof SHR !== 'undefined') { SHR.nq_chiyo_idle = 4; if (SHR.c2_punk_walk != null) SHR.nq_chiyo_walk = SHR.c2_punk_walk; }
    if (typeof BW_IDS !== 'undefined') BW_IDS.nq_chiyo = 1;
    if (typeof C2K !== 'undefined') C2K.nq_chiyo = 1.04;
    PT.nq_chiyo = 'nq_chiyo_fig';
    if (typeof PT_PAINT !== 'undefined') PT_PAINT.nq_chiyo = 'chiyo';
    if (typeof PT_HAS !== 'undefined') PT_HAS.chiyo_neutral = 1;
  })();

  /* ---------------- door + room (Lucky 7 south frontage, x≈3080) ----------------
     v6.5.64: occupy the Lucky 7 storefront on shopsE (base at the lantern-lane
     wall y=2600). The old overlay sat in the sidewalk (y=2600–2760) on top of
     Lucky 7 and covered Ban's downed bodies. */
  var WAGA_DOOR = { r: [3040, 2520, 3120, 2600], at: SHOP_AT, to: 'waga', out: [SHOP_AT[0], SHOP_AT[1] + 16] };
  var RW = 1280, RH = 900;
  function roomDef() {
    var id = 'c2_nq_waga'; C2R.waga = id;
    INT[id] = { id: id, n: 'Chiyo Wagashi', w: RW, h: RH, src: 'world/nq_waga.paint', tiles: 1, cell: 15, dg: 'c2', c2: 'waga', deep: 1, safe: 1, mus: 'c2night', nq: 1, s2: 1,
      open: [[90, 250, 1190, 850], [580, 850, 700, 900]], 'in': [640, 820, 3], back: [640, 820, 3],
      /* Staff side + visual counter front (paint: top 470, face 550-630). Wall-to-wall so the player cannot walk around or behind the counter. */
      block: [[90, 230, 1190, 630]],
      spots: [{ id: 'exit', r: [575, 850, 705, 900], at: [640, 870], face: 0 }, { id: 's2_waga_order', r: [400, 630, 880, 760], at: [640, 670], face: 3, lab: 'Order' }] };
    INT[id].base = INT[id].block; TAGS_IN[id] = {}; C2W.doors.nq_waga = WAGA_DOOR;
    return INT[id];
  }
  roomDef();
  if (typeof c2DoorOf === 'function') { var door0 = c2DoorOf; c2DoorOf = function (k) { if (k === 'waga') return WAGA_DOOR; return door0.apply(this, arguments); }; }
  if (typeof c2Surf === 'function') { var surf0 = c2Surf; c2Surf = function (x, y) { if (c2Room() === 'waga') return 'wood'; return surf0.apply(this, arguments); }; }
  INT.c2_town.spots.push({ id: 's2_e_waga', r: WAGA_DOOR.r, at: WAGA_DOOR.at, face: 3, lab: 'Enter' });
  if (typeof TRANS !== 'undefined') TRANS.s2_e_waga = 1;
  delete INT.c2_town.G;
  /* painted storefront, 400×160, center 3080, bottom flush on y=2600 (Lucky 7 south wall).
     NQ's FAC / propEl / facades live inside the NQ IIFE, so we append the canvas ourselves and hook c2Pop. */
  var WAGA_FAC = null;
  function placeDoor() {
    if (!S2.ART || !on() || !inTown()) return;
    if (document.getElementById('s2WagaDoor')) return;
    if (!WAGA_FAC) {
      WAGA_FAC = document.createElement('canvas'); WAGA_FAC.width = 400; WAGA_FAC.height = 160;
      try { if (root.FFF_S2P && root.FFF_S2P.facadeDoor) root.FFF_S2P.facadeDoor(WAGA_FAC.getContext('2d')); } catch (eF) { ev('world:s2:err:facade:' + (eF && eF.message)); }
    }
    WAGA_FAC.className = 'nqprop'; WAGA_FAC.id = 's2WagaDoor';
    WAGA_FAC.style.cssText = 'position:absolute;left:2880px;top:2440px;width:400px;height:160px;z-index:' + (100 + 2600) + ';pointer-events:none';
    var host = null, sample = document.querySelector('#world .nqprop, #wimap .nqprop, .nqprop');
    if (sample && sample.parentNode) host = sample.parentNode;
    if (!host) host = document.getElementById('world') || document.getElementById('wimap') || (W && W.el);
    if (!host) return;
    host.appendChild(WAGA_FAC);
    try { if (W && W.ints) W.ints.push({ el: WAGA_FAC }); } catch (eI) {}
  }
  S2.placeDoor = placeDoor;
  if (typeof facades === 'function') {
    var fac0 = facades;
    facades = function () { fac0.apply(this, arguments); try { placeDoor(); } catch (eD) {} };
  }
  function hookBattle() {
    if (S2._bt) return true;
    if (!root.FFF_C2BT || !root.FFF_S2P || !root.FFF_S2P.battle) return false;
    S2._bt = 1;
    var BT = root.FFF_C2BT;
    BT.ROOMS.waga = { name: 'Wagashi row', paint: function (x) { root.FFF_S2P.battle(x); },
      lights: [[200, 144, '255,170,100', 70, 0.32, 'lamp'], [520, 144, '255,170,100', 70, 0.32, 'lamp']], rain: 48, mood: 'rain' };
    BT.KEY.c2_waga = 'waga';
    var roomB0 = BT.room;
    BT.room = function (story) {
      var ctx = (story && story.ctx) || {}, dgk = String(ctx.dgk || '');
      if (S2.ART && (ctx.s2waga || ctx.s2k === 's2_x' || ctx.s2k === 's2_waga' || /^s2_x/.test(dgk))) return 'c2_waga';
      return roomB0.apply(this, arguments);
    };
    return true;
  }
  hookBattle();
  try { later(0, hookBattle); } catch (eB) { try { setTimeout(hookBattle, 0); } catch (eB2) {} }
  function roomOpen() { return on() && qDone(); }
  S2.roomOpen = roomOpen; S2.DOOR = WAGA_DOOR; S2.FAC_BOX = [2880, 2440, 3280, 2600]; S2.inWagaDoor = inWagaDoor; S2.doorTalk = doorTalk;

  function paintPlaceholder(g) {
    g.fillStyle = '#2a1c1c'; g.fillRect(0, 0, RW, RH);
    g.fillStyle = '#f3e4cf'; g.fillRect(90, 230, RW - 180, 620);
    g.fillStyle = '#8a4a3a'; g.fillRect(90, 0, RW - 180, 230);
    g.fillStyle = '#1b1820'; g.fillRect(0, 0, 90, RH); g.fillRect(RW - 90, 0, 90, RH);
    g.fillRect(0, 850, 580, 50); g.fillRect(700, 850, 580, 50);
    g.fillStyle = '#f4ead2'; g.font = '900 36px "Noto Sans CJK JP",serif'; g.textAlign = 'center';
    g.fillText('WAGASHI  \u00b7  placeholder', 640, 360);
    g.font = '18px "Noto Sans CJK JP",serif'; g.fillText('Interior art waits on preview approval', 640, 400);
    g.fillStyle = '#7a4a32'; g.fillRect(360, 430, 560, 90);
  }
  var RCV = null;
  function paintRoom() {
    var m = document.getElementById('wimap') || document.getElementById('world');
    if (!m || room() !== 'waga') return;
    /* Drop leftover Minato / depot canvases (z-index 1) so they cannot sit on the wagashi board. */
    try {
      [].forEach.call(document.querySelectorAll('[id^="s2P2Room_"], [id^="s2P5Room_"]'), function (el) {
        if (el.parentNode) el.parentNode.removeChild(el);
      });
    } catch (eS) {}
    if (!RCV) {
      RCV = document.createElement('canvas'); RCV.width = RW; RCV.height = RH;
      var g = RCV.getContext('2d');
      try { if (S2.ART && root.FFF_S2P && root.FFF_S2P.interior) root.FFF_S2P.interior(g); else paintPlaceholder(g); } catch (e) { paintPlaceholder(g); }
      RCV.complete = true; RCV.naturalWidth = RW; RCV.naturalHeight = RH;
    }
    RCV.id = 's2Room'; RCV.style.cssText = 'position:absolute;left:0;top:0;width:' + RW + 'px;height:' + RH + 'px;pointer-events:none;z-index:0';
    if (RCV.parentNode !== m) m.insertBefore(RCV, m.firstChild); m.style.backgroundImage = 'none';
  }

  /* ---------------- menu (prices proposed; Nails 20% off after takeover) ---------------- */
  function disc(c) { return Math.max(1, Math.round(c * 0.8)); }
  var WAGA_MENU = S2.MENU = [
    { id: 'roll', n: 'Sweet roll', jp: '\u3042\u3093\u30ed\u30fc\u30eb', hp: 14, base: 8, cost: 6, eat: 'sweetroll' },
    { id: 'dango', n: 'Dango', jp: '\u3060\u3093\u3054', hp: 8, base: 5, cost: 4, eat: 'dango' }
  ];
  function yen() { return SAVE.items | 0; }
  function payYen(c) { SAVE.items = Math.max(0, yen() - c); sv(); try { hud(); bumpItems(); } catch (e) {} }
  function spM() { return (typeof SPMAX === 'number' && SPMAX > 0) ? SPMAX : 40; }
  function applyVit(it) { var h0 = SAVE.hp | 0; if (it.hp) SAVE.hp = Math.min(MAXHP, h0 + it.hp); sv(); try { hud(); if (SAVE.hp > h0 && typeof vitFlo === 'function') vitFlo('hp', SAVE.hp - h0); } catch (e) {} }
  function counterMenu() {
    var nails = qDone(), y = yen(), hpFull = SAVE.hp >= MAXHP, NP = '<i class="nqnp">Nails\u2019 price</i>';
    var line = nails ? (path() === 'balanced' ? 'Sit. The kettle\u2019s on. Eat something warm.' : 'Nails said the row is yours. The prices are too.') : 'I can\u2019t sell with them on the step.';
    if (!nails) { talk(pv(VO.shopCold)); return; }
    if (root.FFF_S2MENUS && typeof root.FFF_S2MENUS.open === 'function') { root.FFF_S2MENUS.open('s2_chiyo'); return; }
    var NQd = root.FFF_NQ;
    /* reuse NQ counter if present; otherwise a simple dialog list */
    var rows = WAGA_MENU.map(function (it) {
      var c = nails ? it.cost : it.base, poor = y < c, bagFull = it.bag && SAVE.heal.length >= (typeof hSlots === 'function' ? hSlots() : 6), full = it.bag ? bagFull : hpFull;
      var eff = it.bag ? ((HITEM[it.bag] && HITEM[it.bag].ic) || '') + ' into your bag' : '+' + it.hp + ' HP';
      var price = nails && it.base > it.cost ? '¥' + it.base + ' → ¥' + it.cost : '¥' + (nails ? it.cost : it.base);
      var why = full ? ' (full)' : poor ? ' (need ¥' + c + ')' : '';
      return [(it.jp ? it.jp + ' ' : '') + it.n + ' · ' + eff + ' · ' + price + why, function () { buy(it, c); }, '', poor || full];
    });
    rows.push(['Later', null]);
    var head = '<div class="sh"><b class="snm">Chiyo</b></div><div class="tw"><p class="q">\u201c' + esc(line) + '\u201d</p>' + (nails ? '<p class="nqnpl">' + NP + ' · 20% off on Nails\u2019 turf</p>' : '') +
      '<p class="vst"><span>HP <b>' + (SAVE.hp | 0) + '/' + MAXHP + '</b></span><span>\u00a5' + y + '</span></p></div>';
    dialog(head, rows);
  }
  function buy(it, c) {
    payYen(c); ev('world:s2:waga:buy:' + it.id + ':' + c);
    var h0 = SAVE.hp | 0, add = it.hp | 0, half = Math.ceil(add / 2), winAdd = Math.round(add * 1.5);
    applyVit(it);
    var h1 = SAVE.hp | 0, id = it.eat, opened = false;
    var tg = { win: Math.min(MAXHP, h0 + winAdd), close: h1, bad: Math.min(MAXHP, h0 + half) };
    function afterEat() {
      try { AU.play('pl_heal', { gain: 0.5 }); } catch (e3) {}
      try { actPlay('eat', W.ryo); } catch (e4) {}
      later(700, counterMenu);
    }
    try {
      if (id && typeof eatgOn === 'function' && eatgOn(id) && root.EATG && typeof eatgHold === 'function') {
        var b0 = W.busy;
        try { eatgCloseBag(); } catch (eC) {}
        W.busy = true; W.path = []; eatgHold(true); ev('world:eatg:open:' + id);
        opened = !!root.EATG.open({ item: id, who: typeof eatgWho === 'function' ? eatgWho() : 'ryo',
          hp0: h0, sp0: SAVE.sp | 0, maxhp: MAXHP, spmax: typeof SPMAX === 'number' ? SPMAX : 40,
          rows: { win: ['WIN', '+' + winAdd + ' HP', 'a generous plate'], close: ['CLOSE MISS', '+' + add + ' HP', 'the normal heal'], bad: ['BAD RUN', '+' + half + ' HP', 'half of normal'] },
          bot: root.FFF_EATG_BOT,
          target: function (r) { return { hp: tg[r] != null ? tg[r] : h1, sp: SAVE.sp | 0 }; },
          onEnd: function (res) {
            try { eatgHold(false); } catch (eH) {}
            SAVE.hp = Math.min(MAXHP, tg[res] != null ? tg[res] : h1); sv();
            try { hud(); if (typeof vitFlo === 'function') vitFlo('hp', SAVE.hp - h0); } catch (eV) {}
            W.busy = b0; W.path = []; ev('world:eatg:' + id + ':' + res); afterEat();
          } });
        if (!opened) { try { eatgHold(false); } catch (eH2) {} W.busy = b0; }
      }
    } catch (eE) { opened = false; }
    if (!opened) afterEat();
  }
  S2.menu = counterMenu;

  /* ---------------- Flip, waves, clash ---------------- */
  var H = 'c2_hustler', Pnk = 'c2_punk', R = 'c2_boso';
  var FL = null, CL = null, CHI = null;
  function crewDown(k) { var s = S(), c = C2CREW.find(function (x) { return x.k === k; }), n = c ? c.ids.length : (k === 's2_w2' ? 3 : 2); for (var i = 0; i < n; i++) if (!s.f[k + '_' + i]) return false; return true; }
  function CRW() {
    var L = [], t = stg();
    if (qOn() && t === 'w1') L.push({ k: 's2_w1', ids: [R, R], at: [2480, 3190], route: [[2440, 3175], [2520, 3175], [2520, 3210], [2440, 3210]], tr: 30, z: 'Wagashi row', n: 'the Rider push' });
    if (qOn() && t === 'w2') L.push({ k: 's2_w2', ids: [R, R, R], at: [2520, 3190], route: [[2480, 3175], [2580, 3175], [2580, 3210], [2480, 3210]], tr: 30, z: 'Wagashi row', n: 'the second push' });
    return L;
  }
  function crewSync() {
    if (!on() || !inTown()) return; var s = S(), want = CRW(), keys = want.map(function (c) { return c.k; });
    for (var j = C2CREW.length - 1; j >= 0; j--) if (/^s2_/.test(C2CREW[j].k) && keys.indexOf(C2CREW[j].k) < 0) C2CREW.splice(j, 1);
    want.forEach(function (c) { if (!C2CREW.some(function (x) { return x.k === c.k; })) C2CREW.push(c);
      c.ids.forEach(function (id, i) { var key = c.k + '_' + i; if (s.f[key] || (W.dgF || []).some(function (o) { return o.key === key; })) return;
        try { var f = g38tSpawn(c, id, i, key); f.c2v2 = 1; f.s2 = 1; try { c2v2Street(c, f, i, 0); } catch (eS) {} } catch (e2) { ev('world:s2:err:spawn:' + (e2 && e2.message)); } }); });
  }
  function suppressX3Loop() {
    if (!(qOn() || qDone())) return;
    for (var b = C2CREW.length - 1; b >= 0; b--) {
      var ck = C2CREW[b].k;
      if (ck === 'p_x3_pnk' || ck === 'p_x3_rid') {
        C2CREW.splice(b, 1);
        (W.dgF || []).forEach(function (o) { if (o.crew === ck && o.s && o.s.el) { o.s.el.remove(); o.gone = 1; } });
        W.dgF = (W.dgF || []).filter(function (o) { return o.crew !== ck; });
      }
    }
  }
  function takeX3Turf() {
    var n = NS(); n.won = n.won || {}; n.won.x3 = 1; E().vend_x3st = 1;
    /* stop the live border */
    var s = S(); s.f = s.f || {}; s.f.p_x3_pnk = 1; s.f.p_x3_rid = 1; s.f.p_x3_pnk_0 = 1; s.f.p_x3_rid_0 = 1;
    try {
      var T = root.FFF_C2TURF;
      if (T && T.Q && T.Q.P && !T.Q.P.some(function (r) { return r[0] === 2420 && r[1] === 2760 && r[2] === 3460; })) T.Q.P.push([2420, 2760, 3460, 3300]);
      if (T && T.B && T.B.X3) T.B.X3.g = 'P';
    } catch (eT) {}
    if (root.FFF_NQ && root.FFF_NQ.BLK && !root.FFF_NQ.BLK.x3) root.FFF_NQ.BLK.x3 = { n: 'WAGASHI ROW', r: [2420, 2760, 3460, 3300] };
    sv();
  }
  /* Serving stand is at the counter front at all times, facing the customer.
     No walk on Order — the walk dropped fps. Area behind the counter stays blocked. */
  var CHI_BACK = [780, 380], CHI_FRONT = [640, 455], chiReady = 1;
  S2.CHI_BACK = CHI_BACK; S2.CHI_FRONT = CHI_FRONT;
  function chiyoPop() {
    if (room() !== 'waga') { if (CHI) { try { kill(CHI); } catch (eK) {} CHI = null; } return; }
    if (CHI && CHI.el && CHI.el.parentNode) return;
    CHI = npc('nq_chiyo', CHI_FRONT[0], CHI_FRONT[1], 0);
    asWalker(CHI, 'nq_chiyo');
    chiReady = 1;
    chiyoFaceCustomer();
    try { if (W.c2n) W.c2n.s2 = CHI; } catch (eN) {}
  }
  function chiyoFaceCustomer() {
    if (!CHI) return;
    if (typeof c2Face === 'function') c2Face(CHI, CHI.x, CHI.y + 80);
    else { CHI.dir = 0; if (typeof animWalk === 'function') animWalk(CHI, 0); place(CHI, 0); }
  }
  /* No-op face: she already stands at the counter. Kept so older callers still resolve. */
  function chiyoToCounter(done) {
    if (CHI) chiyoFaceCustomer();
    if (done) done();
  }
  S2.chiyoToCounter = chiyoToCounter;
  S2.chiyoPop = chiyoPop;
  S2.paintRoom = paintRoom;
  function flipPop() {
    if (!on() || !inTown() || !qOn() || stg() !== 'open') return;
    if (FL && FL.el && FL.el.parentNode) return;
    FL = npc('n13flip', FLIP_AT[0], FLIP_AT[1], 0);
    face(FL, FLIP_AT[0] + 80, FLIP_AT[1]);
  }
  function flipTalk() {
    if (stg() !== 'open' && stg() !== '') return false;
    lockIn(true); if (FL) face(FL, W.ryo.x, W.ryo.y); if (W.ryo) c2Face(W.ryo, FL ? FL.x : FLIP_AT[0], FL ? FL.y : FLIP_AT[1]);
    talk(pv(VO.brief), function () {
      if (path() === 'balanced') { setStg('sawshop'); qStep(1); }
      else { setStg('w1'); qStep(1); crewSync(); }
      if (FL) { move(FL, [[2200, 3300]], 140, function () { kill(FL); FL = null; }); }
      lockIn(false); try { qBanner('WAGASHI ROW', Q.n, Q.giver); } catch (e) {}
    });
    return true;
  }
  function inWagaDoor() {
    var r = WAGA_DOOR.r, p = W.ryo;
    return !!(p && p.x >= r[0] && p.x < r[2] && p.y >= r[1] && p.y < r[3]);
  }
  function armWagaLatch() {
    /* v6.5.64: TRANS auto-enter retriggered shopCold forever while you stood in the door. */
    W._s2WagaSaid = 1;
    var poll = function () {
      if (!W._s2WagaSaid) return;
      if (!inWagaDoor()) { W._s2WagaSaid = 0; return; }
      (root.FFF_NATIVE_TO || setTimeout)(poll, 150);
    };
    (root.FFF_NATIVE_TO || setTimeout)(poll, 150);
  }
  function doorTalk() {
    if (qDone()) { W._s2WagaSaid = 0; c2Enter('waga'); return; }
    if (W._s2WagaSaid) return;
    armWagaLatch();
    if (qOn() && (stg() === 'open' || stg() === 'sawshop' || stg() === '')) {
      talk(pv(stg() === 'sawshop' || path() === 'balanced' ? VO.shopFirst : VO.shopCold), function () {
        if (path() === 'balanced' && stg() === 'sawshop') { setStg('w1'); qStep(1); crewSync(); }
      });
      return;
    }
    talk(pv(VO.shopCold));
  }
  function clashBeat() {
    if (CL && CL.f) return; if (CL) { kill(CL.flip); (CL.pk || []).forEach(kill); }
    var r = W.ryo; lockIn(true); ev('world:s2:clash');
    CL = { f: 0 }; var fx = r.x, fy = r.y - 200;
    CL.flip = npc('n13flip', fx - 40, fy, Math.PI / 2); CL.pk = [npc(Pnk, fx - 80, fy - 16, Math.PI / 2), npc(Pnk, fx + 40, fy - 16, Math.PI / 2)];
    var n = 0, fin = function () { if (++n < 3) return; [CL.flip].concat(CL.pk).forEach(function (q) { face(q, X3C[0] + 80, X3C[1]); }); lockIn(false);
      talk(pv(VO.clash), function () {
        CL.f = 1; fight([R, R, R], false, { dg: 'c2', dgk: 's2_x_0', dgks: ['s2_x_0', 's2_x_1', 's2_x_2'], s2k: 's2_x', s2waga: 1, s2: 1, toughHp: typeof C2HP3 === 'number' ? C2HP3 : undefined }); }); };
    move(CL.flip, [[r.x - 70, r.y + 10]], 210, fin); move(CL.pk[0], [[r.x - 110, r.y - 4]], 210, fin); move(CL.pk[1], [[r.x + 80, r.y + 4]], 210, fin);
  }
  function clashWon() {
    if (CL) { [CL.flip].concat(CL.pk || []).forEach(function (q, i) { if (q) move(q, [[2200 + i * 20, 3300]], 120, function () { kill(q); }); }); CL = null; }
    takeX3Turf(); setStg('done'); qClose(); suppressX3Loop();
    var sting = root.FFF_NQ && root.FFF_NQ.sting;
    var after = function () { talk(pv(VO.won), function () { try { qBanner('WAGASHI ROW', 'The sweet shop is open.', 'Chiyo Wagashi'); } catch (e) {} }); };
    if (typeof sting === 'function') sting('x3', after); else after();
  }
  function s2Back(win, c) {
    var s = S(); if (!win) { if (c.s2k === 's2_x') whenFree(function () { beatReset(true); setStg('clash'); }); return; }
    (c.dgks || []).forEach(function (k) { if (/^s2_/.test(k)) s.f[k] = 1; }); sv();
    var k = c.s2k; ev('world:s2:won:' + k);
    if (k === 's2_w1' && crewDown(k)) whenFree(function () { setStg('w2'); crewSync(); say([['aoi', path() === 'strategic' ? 'Second wave, on schedule. Three this time.' : 'Second push coming up the row.']]); });
    if (k === 's2_w2' && crewDown(k)) whenFree(function () { setStg('clash'); crewSync(); say([['aoi', 'The middle. Flip said he\u2019d bring two.']]); });
    if (k === 's2_x') whenFree(clashWon);
  }
  if (typeof fight === 'function') {
    var fightS = fight;
    fight = function (grp, boss, ctx) {
      try {
        if (ctx && on()) {
          var ks = ctx.dgks || [ctx.dgk];
          ks.forEach(function (k) { var m = /^(s2_[a-z]\d?)_\d+$/.exec(String(k || '')); if (m) ctx.s2k = ctx.s2k || m[1]; });
          if (ctx.s2k) ev('world:s2:fight:' + ctx.s2k);
        }
      } catch (eF) {}
      return fightS.apply(this, arguments);
    };
  }
  if (typeof c2Back === 'function') {
    var back0 = c2Back;
    c2Back = function (win, st0) {
      var r = back0.apply(this, arguments);
      try { var c = st0 && st0.ctx; if (on() && c && c.s2k) s2Back(win && !st0.escaped, c); } catch (eB) { ev('world:s2:err:back:' + (eB && eB.message)); }
      return r;
    };
  }

  function beatReset(force) {
    if (CL && (force || !CL.f)) { kill(CL.flip); (CL.pk || []).forEach(kill); CL = null; }
    try { lockIn(false); } catch (e2) {}
  }
  function chainRepair() {
    if (!punkAfterSeal()) return;
    var ch = 0;
    if (!qOn() && !qDone()) { qOpen(); if (!stg()) setStg('open'); ch = 1; }
    if (qDone()) { takeX3Turf(); suppressX3Loop(); }
    if (qOn() && stg() === 'w1' && crewDown('s2_w1')) { setStg('w2'); ch = 1; }
    if (qOn() && stg() === 'w2' && crewDown('s2_w2')) { setStg('clash'); ch = 1; }
    if (ch) { crewSync(); sv(); ev('world:s2:repair'); }
  }
  S2.chainRepair = chainRepair; S2.crewSync = crewSync; S2.takeX3Turf = takeX3Turf;

  /* approach the clash marker */
  function flowTick() {
    if (!on() || !inTown()) return;
    /* quest/side work only — official idle and off-row streets stay cheap */
    if (!qOn() && !qDone() && !punkAfterSeal()) return;
    chainRepair(); flipPop(); crewSync(); suppressX3Loop();
    if (qOn() && stg() === 'clash' && !busy() && !CL && W.ryo && Math.hypot(W.ryo.x - X3C[0], W.ryo.y - X3C[1]) < 90) clashBeat();
    if (room() === 'waga') paintRoom();
    /* Flip talk if walking up */
    if (qOn() && stg() === 'open' && FL && W.ryo && !busy() && Math.hypot(W.ryo.x - FL.x, W.ryo.y - FL.y) < 70) { /* tag handles talk */ }
  }

  /* ---------------- actions ---------------- */
  if (typeof c2ActC === 'function') {
    var act0 = c2ActC;
    c2ActC = function (k, a) {
      try {
        if (on()) {
          if (a === 's2_e_waga') { doorTalk(); return true; }
          if (a === 's2_waga_order') { if (CHI) chiyoFaceCustomer(); counterMenu(); return true; }
          if (a === 's2_flip' || (FL && a && /n13flip/.test(a) && qOn() && stg() === 'open')) { flipTalk(); return true; }
        }
      } catch (e) { ev('world:s2:err:act:' + (e && e.message)); }
      return act0.apply(this, arguments);
    };
  }
  /* talking to Flip's sprite (world NPC) */
  if (typeof c2Talk === 'function') {
    var tk0 = c2Talk;
    c2Talk = function (s) {
      try { if (on() && qOn() && stg() === 'open' && s && (s.s2id === 'n13flip' || (s.el && s.el.dataset && s.el.dataset.npc === 'n13flip') || (s.id === 'n13flip'))) { flipTalk(); return true; } } catch (eT) {}
      return tk0.apply(this, arguments);
    };
  } else if (typeof talkNpc === 'function') {
    var tn0 = talkNpc;
    talkNpc = function (s) {
      try { if (on() && qOn() && stg() === 'open' && s && (s.s2id === 'n13flip' || s.id === 'n13flip')) { flipTalk(); return true; } } catch (eT) {}
      return tn0.apply(this, arguments);
    };
  }
  /* also a talk spot on Flip */
  INT.c2_town.spots.push({ id: 's2_flip', r: [FLIP_AT[0] - 40, FLIP_AT[1] - 80, FLIP_AT[0] + 40, FLIP_AT[1] + 20], at: FLIP_AT, face: 1, lab: 'Talk' });
  delete INT.c2_town.G;
  if (typeof c2Tags === 'function') {
    var tags0 = c2Tags;
    c2Tags = function (id, D) {
      var out = tags0.apply(this, arguments);
      try {
        if (out && on()) out = out.filter(function (t) {
          if (!t || !t.key) return true;
          if (t.key.indexOf(':s2_flip') >= 0) return qOn() && stg() === 'open';
          if (t.key.indexOf(':s2_e_waga') >= 0) return punkAfterSeal();
          if (t.key.indexOf(':s2_waga_order') >= 0) return room() === 'waga';
          return true;
        });
      } catch (e) {}
      return out;
    };
  }

  /* ride c2Frame, no new loop */
  if (typeof c2Frame === 'function') {
    var fr0 = c2Frame;
    c2Frame = function (dt) { fr0.apply(this, arguments); try { if (on()) { placeDoor(); flowTick(); } } catch (e) { if (!S2.ferr) { S2.ferr = 1; ev('world:s2:err:frame:' + (e && e.message)); } } };
  }
  if (typeof c2Pop === 'function') {
    var pop0 = c2Pop;
    c2Pop = function () { pop0.apply(this, arguments); try { if (on()) { chainRepair(); crewSync(); flipPop(); suppressX3Loop(); placeDoor(); chiyoPop(); if (room() === 'waga') paintRoom(); } } catch (eP) {} };
  }
  try { chainRepair(); } catch (eC) {}
  ev('world:s2:ready');
  } catch (eS2) { try { ev('world:s2:err:init:' + (eS2 && eS2.message)); console.warn('S2 init', eS2); } catch (e2) {} }
})();
