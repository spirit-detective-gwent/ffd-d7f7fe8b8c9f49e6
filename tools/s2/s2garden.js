/* GGD-50: mugwort garden, chance picks, yard map, meal edge.
 * Injected after S2MENUS. No new always-running loops. */
(function (root) {
  'use strict';

  var G = {
    TAP_R: 22,
    NEAR: 12,
    REACH: 26,
    SKIP_GUARD: 400,
    /* 3x3 pot feet in the clinic nook (paint_garden.py pot_feet) */
    POTS: [
      { id: 'gp1', at: [194, 218] },
      { id: 'gp2', at: [298, 218] },
      { id: 'gp3', at: [402, 218] },
      { id: 'gp4', at: [194, 296] },
      { id: 'gp5', at: [298, 296] },
      { id: 'gp6', at: [402, 296] },
      { id: 'gp7', at: [194, 380] },
      { id: 'gp8', at: [298, 380] },
      { id: 'gp9', at: [402, 380] }
    ],
    /* aisle stand: east of the pot, feet on the boards */
    stand: function (p) { return [p.at[0] + 24, p.at[1] + 1]; },
    INTRO: [
      ['tsukikage', 'That corner gets good light. I\'ve set out pots, if you\'d like mugwort of your own.', { mood: 'neutral' }],
      ['tsukikage', 'Buy seeds, plant them, and I\'ll water and tend them while you\'re out.', { mood: 'neutral' }],
      ['tsukikage', 'Finish whatever job you\'re on, then come back. They\'ll be ready to pick.', { mood: 'neutral' }]
    ],
    BUY_LINE: 'Seeds are ¥1 a packet',
    GINGER_TIP: 'Ginger grows at the water\'s edge — the canal beds, the flower boat, and the pier.',
    MULT_P2: 0.06,
    MULT_P3: 0.01,
    RARE_P: 0.005
  };

  function ev(k) { try { if (typeof root.ev === 'function') root.ev(k); } catch (e) {} }
  function S0() { return typeof c2S === 'function' ? c2S() : (SAVE && SAVE.c2) || {}; }
  function cyc() { return typeof c2Cyc === 'function' ? c2Cyc() : S0(); }
  function met() { var S = S0(); return !!(S && S.e && S.e.sumire); }
  function introDone() { var S = S0(); return !!(S && S.e && S.e.gardenIntro); }

  /* ---------- save: pots + seed herb + migration ---------- */
  function potsS() {
    var S = cyc();
    if (!S.pots || typeof S.pots !== 'object') S.pots = {};
    G.POTS.forEach(function (p) {
      if (!S.pots[p.id]) S.pots[p.id] = { st: 'empty' };
    });
    return S.pots;
  }
  function potSt(id) { return potsS()[id] || { st: 'empty' }; }

  function herbSeed() {
    if (typeof herbS !== 'function') {
      SAVE.herbs = SAVE.herbs && typeof SAVE.herbs === 'object' ? SAVE.herbs : (SAVE.herbs = {});
      SAVE.herbs.seed = SAVE.herbs.seed | 0;
      return SAVE.herbs;
    }
    var h = herbS();
    h.seed = h.seed | 0;
    return h;
  }

  /* enter() is what calls load(). Title boot runs first and SAVE is still fresh();
   * writing the autosave here would wipe a cleared run and lock New Game+ on the title. */
  function saveReady() {
    try { return !!(typeof built !== 'undefined' && built); } catch (e) { return false; }
  }
  function migrateGarden() {
    if (!saveReady()) return;
    var S = cyc();
    if (S.gardenMig) return;
    S.gardenMig = 1;
    /* leftover shop mugwort (mugLeft packets) stays the packet count; the shop now sells seeds */
    if (S.mugLeft == null) S.mugLeft = (typeof C2_MUG !== 'undefined' ? C2_MUG : 3);
    herbSeed();
    /* old saves that still have shop mugwort stock already have mugLeft; seeds are bought from it */
    try { save(); } catch (e) {}
    ev('world:garden:mig');
  }

  /* ---------- clinic geometry ---------- */
  function applyClinic() {
    var H = typeof C2HUB !== 'undefined' && C2HUB.clinic;
    if (!H) return;
    var blocks = (H.block || []).filter(function (b) {
      return !(b[0] === 130 && b[1] === 150 && b[2] === 470 && b[3] === 300);
    });
    /* sill + window wall, mini cabinet foot, per-pot footprints */
    blocks.push([132, 40, 464, 172]);
    blocks.push([476, 150, 572, 214]);
    G.POTS.forEach(function (p) {
      var x = p.at[0], y = p.at[1];
      blocks.push([x - 16, y - 20, x + 16, y + 4]);
    });
    H.block = blocks;
    H.spots = (H.spots || []).filter(function (s) { return s.id !== 'drawers'; });
    H.spots.push({ id: 'garden', r: [132, 172, 464, 428], at: [336, 400], face: 3, lab: 'Garden' });
    var I = typeof INT !== 'undefined' && INT.c2_clinic;
    if (I) { I.base = I.block = H.block; I.spots = H.spots; }
  }

  /* ---------- pot props ---------- */
  function css() {
    if (G.css) return;
    G.css = 1;
    try {
      var st = document.createElement('style');
      st.textContent = [
        '.g50pot{position:absolute;display:block;pointer-events:none;background-repeat:no-repeat;background-size:100% 100%;z-index:3}',
        '.g50pot.spark .g50sp,.g50glint{position:absolute;width:10px;height:10px;margin:-5px 0 0 -5px;background:radial-gradient(circle,#fff8d0 0%,#f4d060 40%,rgba(244,200,60,0) 70%);pointer-events:none}',
        '.g50pot.spark .g50sp{animation:g50sp 1.2s ease-in-out infinite}',
        '@keyframes g50sp{0%,100%{opacity:.35;transform:scale(.8)}50%{opacity:1;transform:scale(1.15)}}',
        '.g38sprig.g50pin{box-shadow:0 0 0 2px rgba(232,192,64,.95),0 0 10px 3px rgba(232,192,64,.55);border-radius:2px}',
        '.g50flash{filter:brightness(1.45) saturate(1.15)}',
        '.g50meal{position:absolute;top:8px;right:48px;width:22px;height:22px;z-index:8;pointer-events:none;background:#1a1220;color:#f4d060;border:2px solid #1a1220;box-shadow:0 0 0 1px #e8c040;font:700 11px/18px sans-serif;text-align:center}'
      ].join('');
      document.head.appendChild(st);
    } catch (e) {}
  }

  function potSvg(st) {
    /* tiny inline cel pot, matches the room painter */
    var plant = '', soil = '<ellipse cx="16" cy="9" rx="10" ry="5" fill="#3a2a1c" stroke="#1a1220" stroke-width="1.5"/>';
    if (st === 'planted') {
      soil = '<ellipse cx="16" cy="9" rx="10" ry="5" fill="#3a2a1c" stroke="#1a1220" stroke-width="1.5"/><ellipse cx="16" cy="7" rx="6" ry="3.5" fill="#5a4030"/><ellipse cx="16" cy="5.5" rx="2" ry="1.5" fill="#d6c48c" stroke="#1a1220" stroke-width="0.8"/>';
    } else if (st === 'bloomed') {
      plant = '<path d="M16 8 C16 2 10 0 8 4 C12 3 14 6 16 8 C16 2 22 0 24 4 C20 3 18 6 16 8 C11 6 9 11 12 13 C14 10 16 10 16 8 C21 6 23 11 20 13 C18 10 16 10 16 8" fill="#6a8a58" stroke="#1a1220" stroke-width="1.2"/><path d="M16 14 L16 8" stroke="#3a5a38" stroke-width="1.4"/>';
    }
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 36" width="32" height="36">' +
      '<ellipse cx="16" cy="33" rx="11" ry="2.4" fill="rgba(90,62,40,.45)"/>' +
      '<path d="M6 14 L26 14 L22 32 L10 32 Z" fill="#c46a3a" stroke="#1a1220" stroke-width="1.6"/>' +
      '<path d="M8 16 L11 30" stroke="#e08a58" stroke-width="1.5"/>' +
      '<ellipse cx="16" cy="14" rx="12" ry="5" fill="#8a4a2c" stroke="#1a1220" stroke-width="1.6"/>' +
      soil + plant + '</svg>';
    return 'url("data:image/svg+xml,' + encodeURIComponent(svg) + '")';
  }

  function gardenPop() {
    css();
    migrateGarden();
    (W.g50p || []).forEach(function (o) { if (o.el) o.el.remove(); });
    W.g50p = [];
    if (typeof c2Room !== 'function' || c2Room() !== 'clinic') return;
    var box = document.getElementById('wimap') || (typeof layer !== 'undefined' ? layer : null);
    if (!box) return;
    var spark = met() && !introDone();
    G.POTS.forEach(function (p, i) {
      var st = potSt(p.id).st || 'empty';
      var e = document.createElement('i');
      e.className = 'g50pot' + (spark && i === 0 ? ' spark' : '');
      e.dataset.gp = p.id;
      e.style.left = (p.at[0] - 16) + 'px';
      e.style.top = (p.at[1] - 32) + 'px';
      e.style.width = '32px';
      e.style.height = '36px';
      e.style.backgroundImage = potSvg(st);
      if (spark && i === 0) {
        var sp = document.createElement('i');
        sp.className = 'g50sp';
        sp.style.left = '26px';
        sp.style.top = '4px';
        e.appendChild(sp);
      }
      box.appendChild(e);
      var stand = G.stand(p);
      var o = { el: e, p: p, x: p.at[0], y: p.at[1], sx: stand[0], sy: stand[1] };
      W.ints.push(o);
      W.g50p.push(o);
    });
    ev('world:garden:pots:' + W.g50p.length);
  }

  function bloomPots() {
    var P = potsS(), n = 0;
    G.POTS.forEach(function (p) {
      var q = P[p.id];
      if (q && q.st === 'planted') { q.st = 'bloomed'; n++; }
    });
    if (n) ev('world:garden:bloom:' + n);
    return n;
  }

  /* ---------- chance pick (once per pick, inside the existing handler) ---------- */
  function rollMult(rand) {
    var r = rand == null ? Math.random() : rand;
    if (r < G.MULT_P3) return 3;
    if (r < G.MULT_P3 + G.MULT_P2) return 2;
    return 1;
  }
  function rollRare(rand) {
    var r = rand == null ? Math.random() : rand;
    if (r >= G.RARE_P) return null;
    var t = Math.random();
    if (t < 0.5) return { k: 'yen', n: 5, t: '¥5 in the dirt.' };
    if (t < 0.75) return { k: 'gauze', n: 1, t: 'A length of gauze in the mud.' };
    return { k: 'tape', n: 1, t: 'A length of tape in the mud.' };
  }

  function fxMult(n) {
    if (n <= 1) return;
    try {
      var el = W.ryo && W.ryo.el;
      if (el) {
        el.classList.add('g50flash');
        setTimeout(function () { try { el.classList.remove('g50flash'); } catch (e) {} }, 280);
      }
    } catch (eF) {}
    try { AU.play('ginger_pick', { gain: 1, rate: n === 3 ? 1.35 : 1.2 }); } catch (eA) {
      try { AU.play('ginger_pick', { gain: 1 }); } catch (e2) {}
    }
  }

  function fxRare(o, find) {
    try {
      if (typeof toast === 'function') toast(find.t);
    } catch (eT) {}
    try { AU.play('pl_heal', { gain: 0.45 }); } catch (eA) {}
    try {
      var host = (o && o.el) || (W.ryo && W.ryo.el);
      if (!host || !host.parentNode) return;
      var g = document.createElement('i');
      g.className = 'g50glint';
      g.style.left = '50%';
      g.style.top = '20%';
      host.appendChild(g);
      setTimeout(function () { if (g.parentNode) g.parentNode.removeChild(g); }, 420);
    } catch (eG) {}
  }

  function chanceGrant(kind, o, evId) {
    var n = rollMult();
    if (typeof herbAdd === 'function') herbAdd(kind, n);
    else { herbSeed(); SAVE.herbs[kind] = (SAVE.herbs[kind] | 0) + n; }
    fxMult(n);
    var find = rollRare();
    if (find) {
      if (find.k === 'yen') { SAVE.items = (SAVE.items | 0) + find.n; try { if (typeof bumpItems === 'function') bumpItems(); if (typeof hud === 'function') hud(); } catch (eY) {} }
      else if (typeof herbAdd === 'function') herbAdd(find.k, find.n);
      fxRare(o, find);
      ev('world:garden:rare:' + find.k + ':' + (evId || ''));
    }
    ev('world:garden:pick:' + (evId || kind) + ':' + n);
    return { n: n, rare: find };
  }

  /* ---------- plant / pot-pick animation (same act slot as gpick) ---------- */
  function ensureSheets() {
    if (G.sh) return;
    G.sh = 1;
    ['ryo', 'aoi'].forEach(function (w) {
      if (typeof IMG !== 'undefined') {
        if (!IMG[w + '_gplant'] && typeof wUrl === 'function') IMG[w + '_gplant'] = wUrl(w + '_gplant');
        if (!IMG[w + '_ppick'] && typeof wUrl === 'function') IMG[w + '_ppick'] = wUrl(w + '_ppick');
      }
      if (typeof SHC !== 'undefined') { SHC[w + '_gplant'] = 6; SHC[w + '_ppick'] = 6; }
      if (typeof SHR !== 'undefined') { SHR[w + '_gplant'] = 1; SHR[w + '_ppick'] = 1; }
    });
  }

  function gardenAct(s, sh, onLift, done) {
    ensureSheets();
    if (!s || !s.el || !IMG[sh] || !s.walker) {
      if (typeof actPlay === 'function') return actPlay('pick', s, function () { if (onLift) onLift(); if (done) done(); });
      if (onLift) onLift(); if (done) done(); return false;
    }
    if (typeof actStop === 'function') actStop(s, true);
    var a = s.act = { row: 0, fr: 0, n: 6, sh: sh, x: s.x, y: s.y, t: null, done: done, bi: s.el.style.backgroundImage, bs: s.el.style.backgroundSize, dir: s.dir, g50: 1 };
    s.dir = 0; ev('world:act:' + (typeof actWho === 'function' ? actWho(s) : 'ryo') + ':' + sh);
    s.el.classList.add('acting');
    (function step() {
      if (s.act !== a) return;
      if (Math.hypot(s.x - a.x, s.y - a.y) > 2 || a.fr >= a.n) { if (typeof actStop === 'function') actStop(s); return; }
      if (typeof actPaint === 'function') actPaint(s);
      if (a.fr >= 2 && onLift) onLift();
      var ms = (typeof ACT6_MS !== 'undefined' ? ACT6_MS : [300, 340, 380, 400, 400, 440]);
      a.t = setTimeout(function () { a.fr++; step(); }, Math.round(ms[a.fr] * (root.FFF_ACT_K != null ? root.FFF_ACT_K : 1)));
    })();
    return true;
  }

  function doPot(o, kind) {
    var r = W.ryo;
    if (!o || !o.el || o.busy || W.busy || W.dlg) return false;
    if (Math.hypot(r.x - o.sx, r.y - o.sy) > G.REACH) return false;
    var st = potSt(o.p.id);
    if (kind === 'plant' && st.st !== 'empty') return false;
    if (kind === 'pick' && st.st !== 'bloomed') return false;
    if (kind === 'plant' && (typeof herbN === 'function' ? herbN('seed') : herbSeed().seed) <= 0) {
      try { if (typeof toast === 'function') toast('Need mugwort seeds.'); } catch (e) {}
      return false;
    }
    o.busy = 1; W.path = []; W.arrive = null;
    r.x = o.sx; r.y = o.sy; r.v = 0; r.moving = false; r.run = false; r.dir = 0;
    if (typeof place === 'function') place(r, 0);
    W.busy = true;
    var who = (typeof actWho === 'function' ? actWho(r) : (SAVE.act || 'ryo'));
    var sh = who + (kind === 'plant' ? '_gplant' : '_ppick');
    ev('world:garden:' + kind + ':start:' + o.p.id);
    var fin = 0, lifted = 0;
    function lift() {
      if (lifted) return; lifted = 1;
      if (kind === 'pick') { st.st = 'empty'; o.el.style.backgroundImage = potSvg('empty'); }
      if (kind === 'plant') { st.st = 'planted'; o.el.style.backgroundImage = potSvg('planted'); }
      ev('world:garden:' + kind + ':lift:' + o.p.id);
    }
    function done() {
      if (fin) return; fin = 1; lift();
      document.removeEventListener('pointerdown', skip, true);
      W.busy = false; o.busy = 0;
      if (kind === 'plant') {
        if (typeof herbAdd === 'function') herbAdd('seed', -1);
        else { var h = herbSeed(); h.seed = Math.max(0, (h.seed | 0) - 1); }
        try { save(); } catch (e) {}
        ev('world:garden:planted:' + o.p.id);
      } else {
        chanceGrant('leaf', o, o.p.id);
        try { AU.play('ginger_pick', { gain: 0.9 }); } catch (eA) {}
      }
    }
    function skip(e) {
      if (fin) return;
      G.skipT = (typeof performance !== 'undefined' ? performance.now() : Date.now());
      if (r.act && r.act.g50) { clearTimeout(r.act.t); if (typeof actStop === 'function') actStop(r); }
      done();
    }
    setTimeout(function () { if (!fin) document.addEventListener('pointerdown', skip, true); }, 120);
    if (!gardenAct(r, sh, lift, done)) done();
    return true;
  }

  function potHit(x, y) {
    var best = null;
    (W.g50p || []).forEach(function (o) {
      if (!o.el || !o.el.isConnected || o.busy) return;
      var d = Math.hypot(x - o.x, y - o.y);
      if (d <= G.TAP_R && (!best || d < best.d)) best = { o: o, d: d };
    });
    return best && best.o;
  }

  function potKind(o) {
    var st = potSt(o.p.id).st;
    if (st === 'bloomed') return 'pick';
    if (st === 'empty') return 'plant';
    return ''; /* planted: she is tending it; no interact */
  }

  function maybeIntro(then) {
    if (!met() || introDone()) { if (then) then(); return; }
    var S = S0();
    if (typeof scene !== 'function') { S.e.gardenIntro = 1; if (then) then(); return; }
    scene(null, G.INTRO, function () {
      S.e.gardenIntro = 1;
      try { save(); } catch (e) {}
      ev('world:garden:intro');
      gardenPop(); /* drop the sparkle */
      if (then) then();
    });
  }

  function potGo(o, run) {
    var r = W.ryo, kind = potKind(o);
    ev('world:garden:tap:' + o.p.id);
    maybeIntro(function () {
      if (!kind) return;
      if (Math.hypot(r.x - o.sx, r.y - o.sy) <= G.NEAR) { doPot(o, kind); return; }
      /* v6563: the 'Garden' spot box covers every pot stand, so a plain walk
       * resolved to that spot (walk to its edge, or 'Nothing useful.' when
       * close) and never reached the pot. Walk to the stand itself. */
      var ok;
      G.noSpot = 1;
      try { ok = (G.walk0 || walkTo)(o.sx, o.sy, true, run); } finally { G.noSpot = 0; }
      if (!ok) return;
      W.arrive = { id: 'g50:' + o.p.id, tagFn: function () { doPot(o, kind); } };
      if (!W.path || !W.path.length) doPot(o, kind);
    });
    return true;
  }

  /* ---------- Tsukikage lines (first scene untouched) ---------- */
  function wrapMugShop() {
    if (G.mug) return; G.mug = 1;
    if (typeof c2MugShop === 'function') {
      var mug0 = c2MugShop, buy0 = c2MugBuy, menu0 = c2SumireMenu;
      c2MugBuy = function (n) {
        var S = cyc();
        n = Math.min(n | 0, S.mugLeft | 0, SAVE.items | 0);
        if (n <= 0) return;
        S.mugLeft -= n; SAVE.items -= n;
        if (typeof herbAdd === 'function') herbAdd('seed', n * (typeof C2_HERB_PER !== 'undefined' ? C2_HERB_PER : 3));
        else { var h = herbSeed(); h.seed = (h.seed | 0) + n * 3; }
        try { if (typeof hud === 'function') hud(); if (typeof bumpItems === 'function') bumpItems(); AU.play('place'); } catch (e) {}
        ev('world:c2:mug:buy:' + n + ':' + S.mugLeft);
        setTimeout(c2MugShop, 0);
      };
      c2MugShop = function () {
        maybeIntro(function () {
          var S = cyc(), m = S.mugLeft | 0, y = SAVE.items | 0, all = Math.min(m, y);
          var tip = introDone() && ((S.gTip = (S.gTip | 0) + 1) % 3 === 0);
          var line = G.BUY_LINE + (tip ? '. ' + G.GINGER_TIP : '');
          var per = typeof C2_HERB_PER !== 'undefined' ? C2_HERB_PER : 3;
          var ic = (typeof herbSvg === 'function') ? herbSvg('seed') : '';
          dialog(ptFace('tsukikage', 'Seeds', IMG.tsukikage_fig) +
            '<div class="tw"><p class="kmug">' + ic + '<span>' + line + ' · ' + per + ' seeds each. <b>' + m + '/' + (typeof C2_MUG !== 'undefined' ? C2_MUG : 3) + '</b> left until the next restock (after a finished quest or side quest).</span></p></div>',
            [['Back', function () { setTimeout(c2SumireMenu, 0); }],
             ['Buy 1 · ¥1', function () { c2MugBuy(1); }, '', !m || y < 1],
             ['Buy ' + (all || m) + ' · ¥' + (all || m), function () { c2MugBuy(all); }, 'hot', all < 2]]);
          try { $('#wdlg').classList.add('scene'); if (typeof ptLift === 'function') ptLift(); } catch (e) {}
          ev('world:c2:mug:open:' + m);
        });
      };
      c2SumireMenu = function () {
        if (!met()) return menu0.apply(this, arguments);
        var S = cyc(), full = SAVE.hp >= (typeof MAXHP !== 'undefined' ? MAXHP : 55), tea = typeof C2_TEA !== 'undefined' ? C2_TEA : 26;
        var poor = (SAVE.items | 0) < tea, m = S.mugLeft | 0;
        /* GGD-51: Full Heal Tea is gone on every route. Seeds and herbs stay. */
        var b = [[full ? 'Full Heal Tea · ¥' + tea + ' (HP full)' : 'Full Heal Tea · ¥' + tea + (poor ? ' (need ¥' + tea + ')' : ''), function () { c2Heal(tea); }, 'hot', full || poor],
          ['Seeds · ' + m + '/' + (typeof C2_MUG !== 'undefined' ? C2_MUG : 3) + ' packets', function () { setTimeout(c2MugShop, 0); }],
          ['Later', null]]; if (window.FFF_TEA_OFF && window.FFF_TEA_OFF()) b.shift();
        var say = (typeof C2_TEA_SAY !== 'undefined' ? C2_TEA_SAY[(S.tsi = ((S.tsi | 0) + 1)) % C2_TEA_SAY.length] : 'Sit. Drink.');
        dialog(ptFace('tsukikage', 'Dr. Tsukikage', IMG.tsukikage_fig) +
          '<div class="tw"><p class="q">“' + say + '”</p><p class="vst"><span>HP <b>' + SAVE.hp + '/' + (typeof MAXHP !== 'undefined' ? MAXHP : 55) + '</b></span><span>¥' + (SAVE.items | 0) + '</span></p></div>', b);
        try { $('#wdlg').classList.add('scene'); if (typeof ptLift === 'function') ptLift(); } catch (e) {}
        ev('world:c2:sumire:menu:' + (full ? 'full' : 'hurt') + ':' + m);
      };
    }
  }

  /* ---------- yard map ---------- */
  function yardActive() {
    var S = cyc();
    return !!(S.yardMap && S.yardMap.cyc === (S.cyc | 0));
  }
  function yardMark() {
    var on = yardActive() && typeof c2Room === 'function' && c2Room() === 'town';
    (W.g5h || []).forEach(function (o) {
      if (o && o.el) o.el.classList.toggle('g50pin', !!on);
    });
  }
  function buyYardMap() {
    var S = cyc();
    S.yardMap = { cyc: S.cyc | 0 };
    try { save(); } catch (e) {}
    ev('world:garden:yardmap:' + S.cyc);
    yardMark();
    try { if (typeof toast === 'function') toast('Yard map: live ginger, this cycle.'); } catch (eT) {}
  }

  /* ---------- meal edge ---------- */
  var SIP_ITEMS = { hojicha: 1, blend: 1, iced: 1, lait: 1, wiener: 1, coffee: 1, cancoffee: 1, ramune: 1, soda: 1, fizz: 1, cola: 1, orange: 1, energy: 1, milk: 1, cmilk: 1, fmilk: 1, coffeemilk: 1, fruitmilk: 1 };
  function mealKind(item) {
    if (!item || item === 'candy') return '';
    if (SIP_ITEMS[item]) return 'sip';
    /* bite / plate meals */
    if (/onigiri|sweetroll|yakisoba|melon|pudding|ramen|curry|don|plate|bentou|bento|wagashi|roll|pan|bread/i.test(item)) return 'plate';
    return 'plate';
  }
  function mealEligible(o) {
    if (!o || o.mealEdge === false || o.from === 'bag' || o.from === 'vend' || o.item === 'candy') return false;
    if (o.mealEdge === true || o.from === 'counter' || o.from === 'restaurant') return true;
    /* default: eat-in if the opener did not mark bag/vend */
    return !!o.item && o.item !== 'candy';
  }
  function grantMeal(o) {
    if (!mealEligible(o)) return;
    var k = mealKind(o.item);
    if (!k) return;
    SAVE.mealEdge = { k: k, item: o.item };
    try { save(); } catch (e) {}
    ev('world:garden:meal:' + k + ':' + o.item);
    try {
      if (typeof toast === 'function') toast(k === 'sip' ? 'First sip' : 'Clean plate');
    } catch (eT) {}
    paintMealIcon();
  }
  function paintMealIcon() {
    var m = SAVE && SAVE.mealEdge;
    var el = document.getElementById('g50meal');
    if (!m) { if (el && el.parentNode) el.parentNode.removeChild(el); return; }
    if (!el) {
      el = document.createElement('i');
      el.id = 'g50meal';
      el.className = 'g50meal';
      var host = document.getElementById('world') || document.body;
      host.appendChild(el);
    }
    el.textContent = m.k === 'sip' ? 'SP' : 'S+';
    el.title = m.k === 'sip' ? 'First sip' : 'Clean plate';
  }
  function consumeSip() {
    var m = SAVE && SAVE.mealEdge;
    if (!m || m.k !== 'sip') return 0;
    SAVE.mealEdge = null;
    paintMealIcon();
    ev('world:garden:meal:sip:used');
    return 5;
  }
  function consumePlate() {
    var m = SAVE && SAVE.mealEdge;
    if (!m || m.k !== 'plate') return 0;
    SAVE.mealEdge = null;
    paintMealIcon();
    ev('world:garden:meal:plate:used');
    return 2;
  }

  function wrapEatg() {
    if (G.eatg) return;
    function hook() {
      if (!root.EATG || !root.EATG.open || G.eatg) return false;
      G.eatg = 1;
      var open0 = root.EATG.open;
      root.EATG.open = function (o) {
        if (o && !o._g50) {
          o._g50 = 1;
          if (G.denyMeal || o.item === 'candy' || o.from === 'bag' || o.from === 'vend') o.mealEdge = false;
          var prev = o.onEnd;
          o.onEnd = function (res, cause) {
            try { if (res === 'win') grantMeal(o); } catch (e) {}
            if (prev) prev(res, cause);
          };
        }
        return open0.apply(this, arguments);
      };
      return true;
    }
    if (!hook()) setTimeout(hook, 0);
    if (typeof drinkSoda === 'function' && !G.sodaWrap) {
      G.sodaWrap = 1;
      var soda0 = drinkSoda;
      drinkSoda = function () {
        G.denyMeal = 1;
        try { return soda0.apply(this, arguments); }
        finally { /* open() is sync; onEnd reads o.mealEdge already stamped */ }
      };
    }
  }

  function wrapGrade() {
    if (G.grade) return;
    var Eobj = root.ENGINE || root.E;
    var grade0 = (Eobj && Eobj.grade) || (typeof grade === 'function' ? grade : null);
    if (!grade0) return;
    G.grade = 1;
    var ranks = (Eobj && Eobj.GRADE && Eobj.GRADE.ranks) || (typeof GRADE !== 'undefined' && GRADE.ranks);
    var wrapped = function (gs, hpEnd) {
      var gr = grade0(gs, hpEnd);
      var bonus = 0;
      try { bonus = consumePlate(); } catch (e) { bonus = 0; }
      if (bonus && gr) {
        /* +2 after the 70% HP S-gate. Never lower cutoffs. A failed gate cannot become S. */
        var wasS = gr.k === 'S';
        var hpOk = hpEnd >= 0.7 * Math.max(1, (gs && gs.hp0) || 1);
        gr.score = (gr.score | 0) + bonus;
        if (ranks) {
          var r = ranks[0];
          ranks.forEach(function (q) { if (gr.score >= q.min) r = q; });
          if (r.k === 'S' && !hpOk) { /* keep the gated rank */ }
          else { gr.k = r.k; if (r.w != null) gr.w = r.w; if (r.m != null) gr.m = r.m; }
        }
        ev('world:garden:meal:plate:sc:' + gr.score + ':' + gr.k);
      }
      return gr;
    };
    if (Eobj) Eobj.grade = wrapped;
    try { if (typeof grade === 'function') grade = wrapped; } catch (eG) {}
  }

  function wrapFightStart() {
    if (G.fight) return;
    /* +5 SP at story fight start, then consume. Hook common entry points. */
    function apply() {
      var add = consumeSip();
      if (!add) return;
      try {
        var mx = typeof SPMAX !== 'undefined' ? SPMAX : 40;
        var side = (typeof ST !== 'undefined' && ST && ST.b && ST.b.s && ST.b.s[0]) ? ST.b.s[0] : null;
        if (side && side.sp != null) side.sp = Math.min(side.spmax || mx, (side.sp | 0) + add);
        if (SAVE) SAVE.sp = Math.min(mx, (SAVE.sp | 0) + add);
        if (typeof hud === 'function') hud();
        ev('world:garden:meal:sip:sp:' + add);
      } catch (e) {}
    }
    G.fight = 1;
    G.applySip = apply;
    if (typeof root.ev === 'function') {
      /* listen by wrapping ev */
      var ev0 = root.ev;
      root.ev = function (k) {
        var r = ev0.apply(this, arguments);
        if (k && String(k).indexOf('match:start:') === 0) {
          setTimeout(function () {
            try {
              if (typeof ST !== 'undefined' && ST && ST.story && !ST.story.tut && !(ST.story.ctx && ST.story.ctx.c2lesson)) apply();
            } catch (eA) {}
          }, 0);
        }
        return r;
      };
    }
  }

  /* ---------- help / herb copy ---------- */
  function patchCopy() {
    try {
      if (typeof HERB !== 'undefined') {
        HERB.seed = HERB.seed || { n: 'Mugwort Seeds', d: 'Plant one seed per pot at the clinic. The doctor waters them. They bloom after the next quest.', w: 'Dr. Tsukikage sells packets of 3 for ¥1, up to 3 packets per quest cycle.' };
        if (HERB.leaf) {
          HERB.leaf.d = 'Leaf + Ginger = Kampo Potion (+35% HP). Grown in the clinic garden, or found as a first gift.';
          HERB.leaf.w = 'Buy seeds from Dr. Tsukikage, plant them in her pots, and pick a leaf after the next main or side quest.';
        }
        if (HERB.ginger) {
          HERB.ginger.w = 'Ginger grows wild at the water\'s edge: canal flower beds, the flower boat at the east pier, and other waterfront sprigs. Endō\'s Yard map marks the live spots for one cycle.';
        }
      }
      if (typeof C2_HERB_NOTE !== 'undefined') {
        /* assigned as a var; reassign on the root if needed */
      }
      try { C2_HERB_NOTE = 'Buy mugwort seeds at the clinic (¥1 a packet of 3), plant them, and pick leaves after the next quest. Ginger grows at the waterfront. Craft from your Bag: Gauze + Tape = 20% Healing Dressing, Mugwort + Ginger = Kampo Potion.'; } catch (eN) {}
      if (typeof herbSvg === 'function' && !G.svg) {
        G.svg = 1;
        var svg0 = herbSvg;
        herbSvg = function (k) {
          if (k === 'seed') return '<svg class="hbsvg" viewBox="0 0 40 40" aria-hidden="true"><rect x="8" y="6" width="24" height="28" rx="3" fill="#c45a3a" stroke="#1a1220" stroke-width="2"/><rect x="11" y="10" width="18" height="10" fill="#f4e6c8" stroke="#1a1220" stroke-width="1.4"/><circle cx="16" cy="26" r="2.2" fill="#5a4030"/><circle cx="20" cy="28" r="2.2" fill="#5a4030"/><circle cx="24" cy="26" r="2.2" fill="#5a4030"/></svg>';
          return svg0(k);
        };
      }
      if (typeof herbS === 'function' && !G.herbS) {
        G.herbS = 1;
        var hs0 = herbS;
        herbS = function () { var h = hs0(); h.seed = h.seed | 0; return h; };
      }
    } catch (e) {}
  }

  /* ---------- wrap world hooks ---------- */
  function wrapWorld() {
    if (G.world) return; G.world = 1;
    if (typeof c2PopD === 'function') {
      var pop0 = c2PopD;
      c2PopD = function (k) { var r = pop0.apply(this, arguments); if (k === 'clinic') gardenPop(); if (k === 'town') yardMark(); return r; };
    }
    if (typeof c2RefreshCycle === 'function') {
      var ref0 = c2RefreshCycle;
      c2RefreshCycle = function (why) {
        var r = ref0.apply(this, arguments);
        try {
          if (!(why && String(why).indexOf('wake') === 0)) {
            bloomPots();
            var S = cyc();
            if (S.yardMap && S.yardMap.cyc !== (S.cyc | 0)) { /* expired on the new cycle */ }
            gardenPop();
            yardMark();
          }
        } catch (e) {}
        return r;
      };
    }
    if (typeof c2Tags === 'function' && !G.tagsWrap) {
      G.tagsWrap = 1;
      var tags0 = c2Tags;
      c2Tags = function () {
        var out = tags0.apply(this, arguments);
        (out || []).forEach(function (t) {
          /* the Garden spot's .wtag.obj drew a rounded box over the nook; keep the
           * spot for taps (intSpotAt) but do not paint a highlight. */
          if (t && t.key && /:garden$/.test(t.key)) { t.obj = null; t.lab = ''; t.silent = 1; }
        });
        return out;
      };
    }
    if (typeof intSpotAt === 'function' && !G.spotWrap) {
      G.spotWrap = 1;
      var spot0 = intSpotAt;
      intSpotAt = function () {
        var s = spot0.apply(this, arguments);
        return (G.noSpot && s && s.id === 'garden') ? null : s;
      };
    }
    if (typeof walkTo === 'function') {
      G.walk0 = walkTo;
      walkTo = function (x, y, fromTap, run) {
        if (fromTap && G.skipT && (typeof performance !== 'undefined' ? performance.now() : Date.now()) - G.skipT < G.SKIP_GUARD) return false;
        if (fromTap && !W.busy && !W.dlg && typeof c2Room === 'function' && c2Room() === 'clinic') {
          var o = potHit(x, y); if (o) return potGo(o, run);
        }
        return G.walk0.apply(this, arguments);
      };
    }
    /* chance rolls inside the existing ginger pick handler */
    if (typeof g38gPick === 'function' && !G.pickWrap) {
      G.pickWrap = 1;
      var add0 = herbAdd;
      herbAdd = function (k, n) {
        if (G.inPick && n === 1 && (k === 'ginger' || k === 'leaf')) {
          G.inPick = 0;
          return chanceGrant(k, G.pickObj, G.pickObj && G.pickObj.h && G.pickObj.h.id);
        }
        return add0.apply(this, arguments);
      };
      var pick0 = g38gPick;
      g38gPick = function (o) {
        G.inPick = 1; G.pickObj = o;
        return pick0.apply(this, arguments);
      };
    }
    if (typeof c2Pop === 'function') {
      var cpop0 = c2Pop;
      c2Pop = function () {
        var r = cpop0.apply(this, arguments);
        try {
          if (typeof c2Room === 'function' && c2Room() === 'clinic') gardenPop();
          if (typeof c2Room === 'function' && c2Room() === 'town') yardMark();
        } catch (eP) {}
        return r;
      };
    }
    if (typeof c2Go === 'function') {
      var go0 = c2Go;
      c2Go = function (k, at) {
        var r = go0.apply(this, arguments);
        if (k === 'clinic') setTimeout(gardenPop, 0);
        return r;
      };
    }
    if (typeof enter === 'function' && !G.enterWrap) {
      G.enterWrap = 1;
      var enter0 = enter;
      enter = function () {
        var r = enter0.apply(this, arguments);
        try { migrateGarden(); } catch (eE) {}
        return r;
      };
    }
  }

  /* boot */
  function boot() {
    css();
    applyClinic();
    migrateGarden();
    patchCopy();
    wrapMugShop();
    wrapWorld();
    wrapEatg();
    wrapGrade();
    wrapFightStart();
    paintMealIcon();
    ev('world:garden:boot');
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();

  root.FFF_S2GARDEN = {
    G: G,
    potsS: potsS,
    potSt: potSt,
    pop: gardenPop,
    bloom: bloomPots,
    rollMult: rollMult,
    rollRare: rollRare,
    chanceGrant: chanceGrant,
    migrate: migrateGarden,
    intro: maybeIntro,
    introDone: introDone,
    yardActive: yardActive,
    yardMark: yardMark,
    buyYardMap: buyYardMap,
    mealKind: mealKind,
    grantMeal: grantMeal,
    consumeSip: consumeSip,
    consumePlate: consumePlate,
    mealEligible: mealEligible,
    applyClinic: applyClinic,
    doPot: doPot
  };
})(typeof window !== 'undefined' ? window : this);
