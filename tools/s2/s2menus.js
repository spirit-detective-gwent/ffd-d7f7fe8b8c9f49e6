/* v6.5.63 FFF_S2MENUS: themed shop menus for seal 2 counters.
 * Restyles #wshop for Chiyo, Hase, and (data only) the depot.
 * Food orders: handoff at the counter, then EATG or actPlay eat/drink, then heal.
 * The player is not moved. No new always-running loops. Add-only. */
(function () {
  try {
  var root = typeof window !== 'undefined' ? window : this;
  var M = root.FFF_S2MENUS = root.FFF_S2MENUS || { v: 1 };
  var INK = '#1a1220';

  function later(ms, fn) { setTimeout(function () { try { fn(); } catch (e) { ev('world:s2m:err:' + (e && e.message)); } }, ms); }
  function yen() { return (typeof SAVE !== 'undefined' ? SAVE.items : 0) | 0; }
  function payYen(c) {
    if (typeof SAVE === 'undefined') return;
    SAVE.items = Math.max(0, yen() - c);
    try { if (typeof sv === 'function') sv(); else if (typeof save === 'function') save(); } catch (e) {}
    try { if (typeof hud === 'function') hud(); if (typeof bumpItems === 'function') bumpItems(); } catch (e2) {}
  }
  function spM() { return (typeof SPMAX === 'number' && SPMAX > 0) ? SPMAX : 40; }
  function hpM() { return (typeof MAXHP === 'number' && MAXHP > 0) ? MAXHP : 55; }
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
  function path() {
    try { var p = typeof c2Path === 'function' ? c2Path() : 'balanced'; return p === 'fierce' || p === 'strategic' ? p : 'balanced'; } catch (e) { return 'balanced'; }
  }
  function iconUrl(id) {
    try { if (root.FFF_S2P && FFF_S2P.menuIconUrl) return FFF_S2P.menuIconUrl(id, 128); } catch (e) {}
    return '';
  }
  function chromeUrl(theme) {
    try { if (root.FFF_S2P && FFF_S2P.menuChromeUrl) return FFF_S2P.menuChromeUrl(theme, 390, 844); } catch (e) {}
    return '';
  }
  function ptUrl(who, theme) {
    try {
      if (who && typeof ptPaintUrl === 'function') {
        var u = ptPaintUrl(who, typeof ptMoodOf === 'function' ? ptMoodOf(who) : 'neutral');
        if (u) return u;
      }
      if (who && typeof IMG !== 'undefined') {
        if (IMG[who + '_fig']) return IMG[who + '_fig'];
        if (typeof PT !== 'undefined' && PT[who] && IMG[PT[who]]) return IMG[PT[who]];
      }
    } catch (e) {}
    try {
      if (theme === 'depot' && root.FFF_S2P && FFF_S2P.menuClerkUrl) return FFF_S2P.menuClerkUrl('depot', 128);
    } catch (e2) {}
    return '';
  }

  /* ---------------- catalog ----------------
   * GGD-49: restaurant menus are eat-in only (no to-go). Hase sells only tape + gauze
   * at food-equivalent ¥3 base each (see s2p2.js). Depot is food and drink only. */
  var CHIYO_ITEMS = [
    { id: 'roll', n: 'Sweet roll', jp: 'あんロール', icon: 'sweetroll', hp: 14, base: 8, cost: 6, eat: 'sweetroll',
      eff: '+14 HP  ·  eat now', flavor: 'Anko folded in a warm roll. Pull it apart at the table.' },
    { id: 'dango', n: 'Dango', jp: 'だんご', icon: 'dango', hp: 8, base: 5, cost: 4, eat: 'dango',
      eff: '+8 HP  ·  eat now', flavor: 'Three colors on a stick. Soft, and gone too fast.' },
    { id: 'hojicha', n: 'Hojicha', jp: 'ほうじ茶', icon: 'hojicha', sp: 6, base: 4, cost: 3, drink: 1, prov: 1,
      eff: '+6 SP  ·  drink now', flavor: 'Toasted tea, no sugar. Clears the last bite.' }
  ];
  var HASE_META = {
    etape: { jp: '電気テープ', icon: 'etape', flavor: 'For wiring, or a first-aid dressing.', eff: 'into your pouch' },
    gauze: { jp: 'ガーゼ', icon: 'gauze', flavor: 'For a dressing. Craft with tape.', eff: 'into your pouch' }
  };
  var HASE_FALLBACK = [
    { id: 'etape', n: 'Electrical tape', k: 'herb', hb: 'tape', base: 3, cost: 2, stock: 3 },
    { id: 'gauze', n: 'Gauze', k: 'herb', hb: 'gauze', base: 3, cost: 2, stock: 3 }
  ];
  function decorateHase(it) {
    var o = {}, m = HASE_META[it.id] || {};
    Object.keys(it).forEach(function (k) { o[k] = it[k]; });
    Object.keys(m).forEach(function (k) { o[k] = m[k]; });
    return o;
  }
  function haseItems() {
    var base = (root.FFF_S2P2 && FFF_S2P2.MENU && FFF_S2P2.MENU.length) ? FFF_S2P2.MENU.slice() : HASE_FALLBACK.slice();
    return base.map(function (it) { return decorateHase(it); });
  }
  var HASE_ITEMS = haseItems();
  var DEPOT_ITEMS = [
    { id: 'onigiri', n: 'Onigiri', jp: 'おにぎり', icon: 'onigiri', hp: 10, base: 6, cost: 5, eat: 'onigiri', prov: 1,
      eff: '+10 HP  ·  eat now', flavor: 'From the break-room rice cooker. Still a little warm.' },
    { id: 'cancoffee', n: 'Canned coffee', jp: '缶コーヒー', icon: 'cancoffee', sp: 6, base: 4, cost: 3, drink: 1, prov: 1,
      eff: '+6 SP  ·  drink now', flavor: 'Night-shift blend, stenciled can.' },
    { id: 'yardmap', n: 'Yard map', jp: '庭地図', icon: 'map', base: 5, cost: 4, stock: 1,
      eff: 'Marks live ginger this cycle', flavor: 'Endō’s sketch of the waterfront beds. One sheet, this cycle only. No heal.' }
  ];

  var SHOPS_M = M.SHOPS = {
    s2_chiyo: {
      id: 's2_chiyo', theme: 'chiyo', n: 'Chiyo Wagashi', jp: '千代和菓子', who: 'nq_chiyo',
      leave: 'また来る  ·  Later',
      hi: {
        fierce: 'Nails said the row is yours. The prices are too.',
        strategic: 'Nails said the row is yours. The prices are too.',
        balanced: 'Sit. The kettle’s on. Eat something warm.'
      },
      nails: function () { try { return !!(root.FFF_S2 && FFF_S2.qDone && FFF_S2.qDone()); } catch (e) { return false; } },
      items: function () { return CHIYO_ITEMS; }
    },
    s2_hase: {
      id: 's2_hase', theme: 'hase', n: 'Hase Repair', jp: '長谷 整備', who: 'nq_hase',
      leave: '戻る  ·  Leave',
      hi: {
        fierce: 'Tape and gauze. Nails prices, if that is the deal.',
        strategic: 'Tape and gauze. Nails prices, if that is the deal.',
        balanced: 'I am still here. Tape and gauze.'
      },
      nails: function () { try { return !!(root.FFF_S2P2 && FFF_S2P2.nailsOn && FFF_S2P2.nailsOn()); } catch (e) { return false; } },
      items: function () { return HASE_ITEMS = haseItems(); }
    },
    /* Opens only after FFF_S2P5.afterSeal() / e.seal_depot. Clerk talk in s2p5 calls open().
     * Provisional clerk name Endō (遠藤) — pending Erik. Stock/restock unchanged. */
    s2_depot: {
      id: 's2_depot', theme: 'depot', n: 'Depot Counter', jp: '出庫窓口', who: 'nq_depclk',
      leave: '閉じる  ·  Close',
      provName: 1,
      wired: function () {
        try { return !!(root.FFF_S2P5 && typeof FFF_S2P5.afterSeal === 'function' && FFF_S2P5.afterSeal()); }
        catch (e) { return false; }
      },
      hi: {
        fierce: 'Counter’s open. Sign the pad. Don’t linger.',
        strategic: 'Manifest window’s open. Nails’ price is on the sheet.',
        balanced: 'You ended the gray schedule. Sit a minute. The kettle’s on in the back.'
      },
      nails: function () { try { if (root.FFF_S2P5 && typeof FFF_S2P5.afterSeal === 'function' && FFF_S2P5.afterSeal()) return true; var e = typeof c2S === 'function' && c2S().e; return !!(e && (e.seal_depot || e.down_dep)); } catch (e) { return false; } },
      items: function () { return DEPOT_ITEMS; }
    }
  };
  M.CHIYO_ITEMS = CHIYO_ITEMS; M.HASE_ITEMS = HASE_ITEMS; M.DEPOT_ITEMS = DEPOT_ITEMS;
  function isWired(shop) {
    if (!shop) return false;
    var w = shop.wired;
    if (typeof w === 'function') { try { return !!w(); } catch (e) { return false; } }
    return w !== false;
  }
  M.has = function (id) { return !!(SHOPS_M[id] && isWired(SHOPS_M[id])); };
  M.hasArt = function (id) { return !!SHOPS_M[id]; };
  M.isWired = isWired;

  /* ---------------- CSS (injected once, scoped to #wshop.s2m) ---------------- */
  function css() {
    if (document.getElementById('s2m-css')) return;
    var st = document.createElement('style'); st.id = 's2m-css';
    st.textContent = [
      '#wshop.s2m{position:absolute;inset:0;z-index:60;display:none;align-items:flex-end;justify-content:center;background:rgba(8,6,10,.45);backdrop-filter:blur(1px)}',
      '#wshop.s2m.on{display:flex}',
      '#wshop.s2m .s2m-box{position:relative;width:min(100%,390px);max-height:100%;overflow-y:auto;overscroll-behavior:contain;color:#1a1220;padding:0 0 12px;box-sizing:border-box;background-size:100% 100%;background-repeat:no-repeat;background-color:#1a1220}',
      '#wshop.s2m .s2m-hd{display:flex;align-items:flex-start;gap:10px;padding:96px 22px 8px;position:relative}',
      '#wshop.s2m-hase .s2m-hd{padding-top:118px}',
      '#wshop.s2m-depot .s2m-hd{padding-top:140px}',
      '#wshop.s2m .s2m-pt{flex:none;width:58px;height:58px;border-radius:50%;background-size:cover;background-position:50% 12%;background-color:#2a2b44;box-shadow:0 0 0 2px #1a1220,0 0 0 4px #8e3b52}',
      '#wshop.s2m-hase .s2m-pt{box-shadow:0 0 0 2px #1a1220,0 0 0 4px #e8c040;border-radius:6px}',
      '#wshop.s2m-depot .s2m-pt{box-shadow:0 0 0 2px #1a1220,0 0 0 3px #8a2a28;border-radius:2px}',
      '#wshop.s2m .s2m-titles{flex:1;min-width:0}',
      '#wshop.s2m .s2m-titles b.jp{display:block;font:900 20px/1.15 "Noto Serif CJK JP","BIZ UDPMincho",serif;color:#5a2c28}',
      '#wshop.s2m-hase .s2m-titles b.jp{font-family:"Noto Sans CJK JP",system-ui,sans-serif;color:#f4ead2;font-size:18px}',
      '#wshop.s2m-depot .s2m-titles b.jp{font-family:"DotGothic16","Noto Sans CJK JP",system-ui,sans-serif;color:#2a2a28;letter-spacing:.08em}',
      '#wshop.s2m .s2m-titles small{display:block;margin-top:3px;font:700 11px/1.1 "Noto Sans CJK JP",system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#8e3b52}',
      '#wshop.s2m-hase .s2m-titles small{color:#c8d0e8;letter-spacing:.1em}',
      '#wshop.s2m-depot .s2m-titles small{color:#8a2a28}',
      '#wshop.s2m .s2m-titles p{margin:6px 0 0;font:600 italic 12px/1.3 "Noto Serif CJK JP",serif;opacity:.9}',
      '#wshop.s2m-hase .s2m-titles p{color:#d8d0c0;font-family:"Noto Sans CJK JP",system-ui,sans-serif;font-style:normal}',
      /* Name is lettered on the navy plate; keep the tags in the DOM for tests/a11y. */
      '#wshop.s2m-hase .s2m-titles b.jp,#wshop.s2m-hase .s2m-titles small{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0}',
      '#wshop.s2m .s2m-vit{margin-left:auto;text-align:right;font:800 11px/1.3 "Noto Sans CJK JP",system-ui,sans-serif;color:#5a2c28}',
      '#wshop.s2m-hase .s2m-vit{color:#ffe680}',
      '#wshop.s2m .s2m-vit .s2m-np{display:block;margin-top:3px;color:#8e3b52}',
      '#wshop.s2m-hase .s2m-vit .s2m-np{color:#e8c040}',
      '#wshop.s2m-depot .s2m-vit .s2m-np{color:#8a2a28}',
      '#wshop.s2m .s2m-list{display:flex;flex-direction:column;gap:8px;padding:4px 18px 8px}',
      '#wshop.s2m .s2m-it{display:flex;align-items:center;gap:8px;min-height:92px;padding:8px 8px 8px 8px;border-radius:10px;background:rgba(255,255,255,.38);box-shadow:inset 0 0 0 1.5px #8e3b52}',
      '#wshop.s2m-hase .s2m-it{background:#d8c49a;border-radius:6px;box-shadow:inset 0 0 0 2px #1a1220,2px 3px 0 rgba(0,0,0,.25)}',
      '#wshop.s2m-depot .s2m-it{background:rgba(255,255,255,.22);border-radius:0;box-shadow:inset 0 -1px 0 rgba(40,70,90,.4);}',
      '#wshop.s2m .s2m-it.off{opacity:.62}',
      '#wshop.s2m .s2m-ic{flex:none;width:58px;height:58px;border-radius:8px;background:#fff8ee;box-shadow:inset 0 0 0 1.5px #1a1220;background-size:contain;background-repeat:no-repeat;background-position:50%}',
      '#wshop.s2m-hase .s2m-ic{background-color:#3a3a40}',
      '#wshop.s2m .s2m-tx{flex:1;min-width:0}',
      '#wshop.s2m .s2m-tx b{display:block;font:800 13px/1.2 "Noto Sans CJK JP",system-ui,sans-serif}',
      '#wshop.s2m .s2m-tx b .jp{color:#8e3b52;margin-right:4px}',
      '#wshop.s2m-hase .s2m-tx b .jp{color:#6a2a14}',
      '#wshop.s2m-depot .s2m-tx b .jp{color:#8a2a28;font-family:"DotGothic16","Noto Sans CJK JP",sans-serif}',
      '#wshop.s2m .s2m-tx .eff{display:block;font:700 11px/1.3 "Noto Sans CJK JP",system-ui,sans-serif;color:#8e3b52}',
      '#wshop.s2m-hase .s2m-tx .eff{color:#6a2a14}',
      '#wshop.s2m-depot .s2m-tx .eff{color:#8a2a28}',
      '#wshop.s2m .s2m-tx .fl{display:block;font:600 10px/1.3 "Noto Sans CJK JP",system-ui,sans-serif;opacity:.8;margin-top:2px}',
      '#wshop.s2m .s2m-it button,#wshop.s2m .s2m-x{border:0;border-radius:12px;padding:8px 10px;min-height:44px;min-width:74px;font:800 13px/1.1 "Noto Sans CJK JP",system-ui,sans-serif;color:#fff;background:linear-gradient(180deg,#8e3b52,#6a2018);box-shadow:inset 0 1px 0 rgba(255,255,255,.2),0 3px 0 #000}',
      '#wshop.s2m-hase .s2m-it button{background:linear-gradient(180deg,#d4783a,#c2410c);border-radius:6px}',
      '#wshop.s2m-depot .s2m-it button{background:#2a323e;border-radius:0;box-shadow:inset 0 0 0 2px #e8c040,0 3px 0 #000;font-family:"DotGothic16","Noto Sans CJK JP",sans-serif}',
      '#wshop.s2m .s2m-it button:disabled{background:linear-gradient(180deg,#3a3d5a,#24263a);font-size:11px;max-width:120px;color:#ddd}',
      '#wshop.s2m .s2m-it button s{opacity:.7;padding-right:4px}',
      '#wshop.s2m .s2m-it button .nqp{color:#ffe9a8}',
      '#wshop.s2m .s2m-x{display:block;margin:12px auto 8px;background:linear-gradient(180deg,#5c3424,#3a241c);min-width:160px}',
      '#wshop.s2m-hase .s2m-x{background:linear-gradient(180deg,#2a2f55,#181b33)}',
      '#wshop.s2m-depot .s2m-x{background:#2a323e;border-radius:0;box-shadow:inset 0 0 0 2px #6a707c,0 3px 0 #000}',
      '#wshop.s2m .s2m-prov{display:inline-block;margin-left:4px;font:700 8px/1 system-ui;letter-spacing:.06em;text-transform:uppercase;opacity:.65}',
      /* handoff: one-shot, then removed */
      '.s2m-hand{position:absolute;z-index:70;width:64px;height:64px;pointer-events:none;background-size:contain;background-repeat:no-repeat;filter:drop-shadow(0 4px 6px rgba(0,0,0,.5));animation:s2mhand .8s ease-out forwards}',
      '@keyframes s2mhand{0%{opacity:0;transform:translate(-50%,-20px) scale(.6)}25%{opacity:1;transform:translate(-50%,0) scale(1)}100%{opacity:0;transform:translate(-50%,40px) scale(.8)}}',
      '@media (prefers-reduced-motion:reduce){.s2m-hand{animation:none;opacity:1}}'
    ].join('\n');
    document.head.appendChild(st);
  }

  function priceHtml(it, nails) {
    if (nails && it.base > it.cost) return '<s>¥' + it.base + '</s> <b class="nqp">¥' + it.cost + '</b>';
    return '¥' + (nails ? it.cost : it.base);
  }
  function whyOf(shop, it, nails) {
    var c = nails ? it.cost : it.base, y = yen();
    var hpFull = (typeof SAVE !== 'undefined' && SAVE.hp >= hpM());
    var spFull = (typeof SAVE !== 'undefined' && (SAVE.sp | 0) >= spM());
    if (it.bag && typeof SAVE !== 'undefined' && typeof hSlots === 'function' && SAVE.heal && SAVE.heal.length >= hSlots()) return 'Bag full';
    if (it.stock && typeof shopLeft === 'function') {
      var left = shopLeft(shop.id, it); if (left <= 0) return 'Sold out';
    }
    if (it.drink && !it.hp && spFull) return 'SP full';
    if ((it.eat || (it.hp && !it.bag && !it.k)) && hpFull) return 'HP full';
    if (y < c) return 'Need ¥' + c;
    return '';
  }

  function lineOf(shop) {
    var hi = shop.hi, p = path();
    if (typeof hi === 'string') return hi;
    return (hi && (hi[p] || hi.balanced)) || '';
  }

  function shopEl() {
    var m = document.getElementById('wshop');
    if (!m) { m = document.createElement('div'); m.id = 'wshop'; var w = document.getElementById('world') || document.body; w.appendChild(m); }
    return m;
  }

  function render(id) {
    var shop = SHOPS_M[id]; if (!shop) return;
    css();
    var nails = !!(shop.nails && shop.nails());
    var items = (typeof shop.items === 'function' ? shop.items() : shop.items) || [];
    var m = shopEl();
    m.dataset.shop = id;
    m.className = 'on s2m s2m-' + shop.theme;
    var bg = chromeUrl(shop.theme);
    var pt = ptUrl(shop.who, shop.theme);
    var head = '<div class="s2m-hd">' +
      '<i class="s2m-pt" style="' + (pt ? 'background-image:url(' + pt + ')' : '') + '"></i>' +
      '<div class="s2m-titles"><b class="jp">' + esc(shop.jp) + '</b><small>' + esc(shop.n) + '</small><p>“' + esc(lineOf(shop)) + '”</p></div>' +
      '<div class="s2m-vit"><span>HP ' + ((typeof SAVE !== 'undefined' ? SAVE.hp : 0) | 0) + '/' + hpM() + '</span><br><span>SP ' + ((typeof SAVE !== 'undefined' ? SAVE.sp : 0) | 0) + '/' + spM() + '</span><br><span>¥' + yen() + '</span>' +
      (nails ? '<em class="s2m-np">Nails’ price · 20% off</em>' : '') + '</div></div>';
    var list = '<div class="s2m-list">';
    items.forEach(function (it) {
      var why = whyOf(shop, it, nails), c = nails ? it.cost : it.base;
      var ic = iconUrl(it.icon || it.id);
      list += '<div class="s2m-it' + (why ? ' off' : '') + '" data-i="' + esc(it.id) + '">' +
        '<i class="s2m-ic" style="' + (ic ? 'background-image:url(' + ic + ')' : '') + '"></i>' +
        '<div class="s2m-tx"><b><span class="jp">' + esc(it.jp || '') + '</span> ' + esc(it.n) + (it.prov ? '<i class="s2m-prov">prov.</i>' : '') + '</b>' +
        '<span class="eff">' + esc(it.eff || '') + '</span>' +
        '<span class="fl">' + esc(it.flavor || '') + '</span></div>' +
        '<button data-a="buy" data-i="' + esc(it.id) + '"' + (why ? ' disabled' : '') + '>' + (why || priceHtml(it, nails)) + '</button></div>';
    });
    list += '</div><button class="s2m-x" data-a="shx">' + esc(shop.leave) + '</button>';
    m.innerHTML = '<div class="s2m-box" role="dialog" aria-label="' + esc(shop.n) + '" style="' + (bg ? 'background-image:url(' + bg + ')' : '') + '">' + head + list + '</div>';
    m.onclick = function (e) {
      var b = e.target.closest('button'); if (!b) { if (e.target === m) { try { AU.play('ui_back'); } catch (eA) {} close(); } return; }
      e.stopPropagation();
      if (b.dataset.a === 'shx') { try { AU.play('ui_back'); } catch (eA2) {} close(); return; }
      if (b.dataset.a === 'buy' && !b.disabled) { try { AU.play('ui_sel'); } catch (eA3) {} buy(id, b.dataset.i); }
    };
    var f = m.querySelector('.s2m-it:not(.off) button') || m.querySelector('.s2m-x'); if (f) try { f.focus(); } catch (eF) {}
  }

  function close() {
    var m = document.getElementById('wshop');
    if (m) { m.className = ''; m.innerHTML = ''; }
    later(50, function () { if (typeof W !== 'undefined' && !(document.getElementById('wdlg') && document.getElementById('wdlg').classList.contains('on'))) W.dlg = false; });
    try { if (typeof save === 'function') save(); if (typeof hud === 'function') hud(); } catch (e) {}
    ev('world:shop:close');
  }

  function hideOnly() {
    var m = document.getElementById('wshop');
    if (m) { m.className = ''; m.innerHTML = ''; }
  }

  function applyVit(it) {
    if (typeof SAVE === 'undefined') return;
    var h0 = SAVE.hp | 0, s0 = SAVE.sp | 0, mx = spM();
    if (it.hp) SAVE.hp = Math.min(hpM(), h0 + (it.hp | 0));
    if (it.sp) SAVE.sp = Math.min(mx, s0 + (it.sp | 0));
    try { if (typeof sv === 'function') sv(); else if (typeof save === 'function') save(); } catch (e) {}
    try { if (typeof hud === 'function') hud(); } catch (e2) {}
    try {
      if (SAVE.hp > h0 && typeof vitFlo === 'function') vitFlo('hp', SAVE.hp - h0);
      if (SAVE.sp > s0 && typeof vitFlo === 'function') later(260, function () { vitFlo('sp', SAVE.sp - s0); });
    } catch (e3) {}
  }

  /* Keep the player on the customer side of the counter. Never walk them or change rooms. */
  function stayPut() {
    try {
      if (typeof W !== 'undefined' && W.ryo) { W.ryo.v = 0; W.path = []; }
    } catch (e) {}
  }

  function handoff(shop, it, done) {
    stayPut();
    ev('world:s2m:handoff:' + shop.id + ':' + it.id);
    var world = document.getElementById('world') || document.body;
    var el = document.createElement('div');
    el.className = 's2m-hand'; el.setAttribute('data-item', it.id);
    var ic = iconUrl(it.icon || it.id);
    el.style.backgroundImage = ic ? 'url(' + ic + ')' : '';
    /* appear at mid-counter, drop toward the player, then vanish — one-shot CSS */
    el.style.left = '50%'; el.style.top = '46%';
    world.appendChild(el);
    try { if (typeof comment === 'function') comment((typeof NM !== 'undefined' && NM[shop.who] ? NM[shop.who] : shop.n) + ': Here.'); } catch (eC) {}
    later(820, function () { if (el.parentNode) el.remove(); stayPut(); if (done) done(); });
  }

  function reopen(id) {
    stayPut();
    later(200, function () { open(id); });
  }

  function playEat(shop, it, after) {
    stayPut();
    var id = it.eat, opened = false;
    var h0 = (typeof SAVE !== 'undefined' ? SAVE.hp : 0) | 0;
    var add = it.hp | 0, half = Math.ceil(add / 2), winAdd = Math.round(add * 1.5);
    var mx = hpM();
    applyVit(it);
    var h1 = (typeof SAVE !== 'undefined' ? SAVE.hp : 0) | 0;
    var tg = { win: Math.min(mx, h0 + winAdd), close: h1, bad: Math.min(mx, h0 + half) };
    function finish() {
      try { if (typeof AU !== 'undefined' && AU.play) AU.play('pl_heal', { gain: 0.5 }); } catch (e3) {}
      try { if (typeof actPlay === 'function' && typeof W !== 'undefined') actPlay('eat', W.ryo); } catch (e4) {}
      later(700, after);
    }
    try {
      if (id && typeof eatgOn === 'function' && eatgOn(id) && root.EATG && typeof eatgHold === 'function') {
        var b0 = typeof W !== 'undefined' ? W.busy : false;
        try { if (typeof eatgCloseBag === 'function') eatgCloseBag(); } catch (eC) {}
        if (typeof W !== 'undefined') { W.busy = true; W.path = []; }
        eatgHold(true); ev('world:eatg:open:' + id);
        opened = !!root.EATG.open({
          item: id, who: typeof eatgWho === 'function' ? eatgWho() : 'ryo',
          hp0: h0, sp0: (typeof SAVE !== 'undefined' ? SAVE.sp : 0) | 0, maxhp: mx, spmax: spM(),
          rows: { win: ['WIN', '+' + winAdd + ' HP', 'a generous plate'], close: ['CLOSE MISS', '+' + add + ' HP', 'the normal heal'], bad: ['BAD RUN', '+' + half + ' HP', 'half of normal'] },
          bot: root.FFF_EATG_BOT,
          target: function (r) { return { hp: tg[r] != null ? tg[r] : h1, sp: (typeof SAVE !== 'undefined' ? SAVE.sp : 0) | 0 }; },
          onEnd: function (res) {
            try { eatgHold(false); } catch (eH) {}
            if (typeof SAVE !== 'undefined') { SAVE.hp = Math.min(mx, tg[res] != null ? tg[res] : h1); }
            try { if (typeof sv === 'function') sv(); else if (typeof save === 'function') save(); } catch (eS) {}
            try { if (typeof hud === 'function') hud(); if (typeof vitFlo === 'function' && typeof SAVE !== 'undefined') vitFlo('hp', SAVE.hp - h0); } catch (eV) {}
            if (typeof W !== 'undefined') { W.busy = b0; W.path = []; }
            ev('world:eatg:' + id + ':' + res);
            stayPut(); finish();
          }
        });
        if (!opened) { try { eatgHold(false); } catch (eH2) {} if (typeof W !== 'undefined') W.busy = b0; }
      }
    } catch (eE) { opened = false; }
    if (!opened) finish();
  }

  function playDrink(shop, it, after) {
    stayPut();
    var s0 = (typeof SAVE !== 'undefined' ? SAVE.sp : 0) | 0;
    applyVit(it);
    var spFx = function () {
      try { if (typeof AU !== 'undefined' && AU.play) AU.play('pl_heal', { gain: 0.45 }); } catch (eA) {}
      try { if (typeof actPlay === 'function' && typeof W !== 'undefined') actPlay('drink', W.ryo); } catch (eD) {}
      later(700, after);
    };
    /* reuse a matching EATG coffee/soda if the item id is one of theirs; otherwise the drink act */
    var eatgId = it.eatg || ((it.id === 'cancoffee') ? 'blend' : null);
    try {
      if (eatgId && root.FFF_EATG_SP && typeof eatgOn === 'function' && eatgOn(eatgId)) {
        var mock = { id: eatgId };
        if (root.FFF_EATG_SP(mock, s0, function () { stayPut(); later(200, after); })) return;
      }
    } catch (eS) {}
    spFx();
  }

  function giveBag(shop, it, after) {
    if (typeof SAVE === 'undefined') { after(); return; }
    if (it.bag) {
      SAVE.heal = SAVE.heal || []; SAVE.heal.push(it.bag);
      try { if (typeof sv === 'function') sv(); else if (typeof save === 'function') save(); } catch (e) {}
      try { if (typeof AU !== 'undefined' && AU.play) AU.play('place'); } catch (eA) {}
      try { if (typeof toast === 'function' && typeof HITEM !== 'undefined' && HITEM[it.bag]) toast(HITEM[it.bag].n + ' in your bag.'); } catch (eT) {}
    } else if (it.k === 'heal' && it.h) {
      /* keep Hase / depot bag items on the existing shopBuy path when possible */
      if (typeof shopBuy === 'function' && typeof SHOPS !== 'undefined' && SHOPS[shop.id]) {
        /* yen already paid below; use shopS stock if registered */
      }
      SAVE.heal = SAVE.heal || []; SAVE.heal.push(it.h);
      try { if (typeof sv === 'function') sv(); else if (typeof save === 'function') save(); } catch (e2) {}
      try { if (typeof AU !== 'undefined' && AU.play) AU.play('place'); } catch (eA2) {}
      try { if (typeof toast === 'function' && typeof HITEM !== 'undefined' && HITEM[it.h]) toast(HITEM[it.h].n + ' in your bag.'); } catch (eT2) {}
    } else if (it.k === 'herb' && it.hb && typeof herbAdd === 'function') {
      try { herbAdd(it.hb, 1); } catch (eH) {}
      try { if (typeof AU !== 'undefined' && AU.play) AU.play('place'); } catch (eA3) {}
      try { if (typeof toast === 'function') toast((it.n || 'Item') + ' in your pouch.'); } catch (eT3) {}
    }
    later(240, after);
  }

  function buy(id, iid) {
    var shop = SHOPS_M[id]; if (!shop) return;
    var items = (typeof shop.items === 'function' ? shop.items() : shop.items) || [];
    var it = items.filter(function (q) { return q.id === iid; })[0]; if (!it) return;
    var nails = !!(shop.nails && shop.nails());
    var c = nails ? it.cost : it.base;
    if (whyOf(shop, it, nails)) return;
    stayPut();
    /* stock accounting for Hase-style items, without going through c2Shop's restyle */
    try {
      if (it.stock && typeof shopS === 'function') { var s = shopS(id); s.b[it.id] = (s.b[it.id] | 0) + 1; }
    } catch (eS) {}
    payYen(c);
    ev('world:s2m:buy:' + id + ':' + it.id + ':' + c);
    ev('world:shop:buy:' + id + ':' + it.id);
    if (id === 's2_chiyo') ev('world:s2:waga:buy:' + it.id + ':' + c);
    hideOnly();
    var after = function () { stayPut(); reopen(id); };
    if (it.id === 'yardmap') {
      try { if (root.FFF_S2GARDEN && FFF_S2GARDEN.buyYardMap) FFF_S2GARDEN.buyYardMap(); } catch (eY) {}
      after();
      return;
    }
    if (it.eat && !it.bag) {
      handoff(shop, it, function () { playEat(shop, it, after); });
    } else if (it.drink && !it.bag) {
      handoff(shop, it, function () { playDrink(shop, it, after); });
    } else {
      giveBag(shop, it, after);
    }
  }

  function open(id) {
    var shop = SHOPS_M[id]; if (!shop) return;
    if (!isWired(shop)) { ev('world:s2m:unwired:' + id); return; }
    stayPut();
    if (typeof W !== 'undefined') { W.dlg = true; W.path = []; try { if (typeof stickEnd === 'function') stickEnd(); } catch (e) {} }
    render(id);
    ev('world:shop:open:' + id);
    ev('world:s2m:open:' + id);
  }

  M.open = open; M.close = close; M.render = render; M.buy = buy; M.handoff = handoff;
  M.iconUrl = iconUrl; M.chromeUrl = chromeUrl; M.priceHtml = priceHtml; M.whyOf = whyOf;
  M.stayPut = stayPut;

  /* Register / refresh SHOPS entries so existing talk hooks can call c2Shop. */
  function syncShops() {
    try { HASE_ITEMS = haseItems(); M.HASE_ITEMS = HASE_ITEMS; } catch (eH) {}
    if (typeof SHOPS === 'undefined') return;
    var ch = SHOPS_M.s2_chiyo;
    SHOPS.s2_chiyo = { n: ch.n, who: ch.who, hi: lineOf(ch), nq: 1, s2menu: 1, items: CHIYO_ITEMS.slice() };
    var hs = SHOPS_M.s2_hase;
    var nails = !!(hs.nails && hs.nails());
    var hItems = HASE_ITEMS.map(function (it) {
      var o = {}; Object.keys(it).forEach(function (k) { o[k] = it[k]; });
      o.cost = nails ? it.cost : it.base; o.d = it.flavor; return o;
    });
    SHOPS.s2_hase = { n: hs.n, who: hs.who, hi: lineOf(hs), nq: 1, s2menu: 1, items: hItems };
  }
  M.syncShops = syncShops;
  try { syncShops(); } catch (e0) {}

  /* Wrap c2Shop so Hase and the depot (once afterSeal) get the designed menu.
   * Existing un-themed shops are unchanged. */
  if (typeof c2Shop === 'function') {
    var c2Shop0 = c2Shop;
    c2Shop = function (id) {
      if (M.has(id)) { open(id); return; }
      return c2Shop0.apply(this, arguments);
    };
  }
  if (typeof shopClose === 'function') {
    var shopClose0 = shopClose;
    shopClose = function () {
      var m = document.getElementById('wshop');
      if (m && /s2m/.test(m.className)) { close(); return; }
      return shopClose0.apply(this, arguments);
    };
  }

  /* Herb stubs so herbAdd does not throw on Hase tape. */
  try {
    if (typeof HERB !== 'undefined') {
      if (!HERB.tape) HERB.tape = { n: 'Electrical tape', ic: '🎗' };
      if (!HERB.gauze) HERB.gauze = { n: 'Gauze', ic: '🩹' };
    }
  } catch (eH) {}

  /* Wiring spec for phase 5 (read-only helper). */
  M.depotWiring = {
    shopId: 's2_depot',
    theme: 'depot',
    open: 'FFF_S2MENUS.open("s2_depot") after the seal, following the shopkeeper talk in s2p5.clerkTalk. Do not open from s2menus.js itself.',
    who: 'Provisional name Endō (遠藤) — pending Erik. Residual night-shift Rider clerk (nq_depclk, portrait endo) at the time-clock desk (出庫窓口). wired is a function of FFF_S2P5.afterSeal().',
    nails: 'Nails’ price once e.seal_depot or e.down_dep is set. Compassionate uses the warmer hi.balanced line.',
    items: DEPOT_ITEMS,
    food: 'onigiri uses EATG onigiri (already in ITEMS). Canned coffee drinks with actPlay("drink"), or FFF_EATG_SP(blend) if that game can open. Handoff plays first; the player is not moved.',
    room: 'Time-clock office (c2Room dclock / depClock). Clerk behind the 台帳 desk. Open after FFF_S2P5.afterSeal() / e.seal_depot. Break room vending stays flavor, not a second shop.'
  };

  ev('world:s2m:ready');
  } catch (eTop) { try { ev('world:s2m:err:boot:' + (eTop && eTop.message)); } catch (e2) {} }
})();
