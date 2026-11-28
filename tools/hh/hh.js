/* v6566-handheld (GGD-93, Erik pt623u): the Kitsune BOY handheld. Chapter One side quest + six walk-up challengers + a menu tab.
 * Arai Sota (Library, Silent Study) tips Ryo off after the Library; the handheld sits in the confiscation box on a desk in the new
 * Staff Room (Nurse's Hallway, where the first lockers stood). Walk up to a gold-ringed Talk bubble (handheld badge) to play one
 * Shonen Showdown match on the handheld's green LCD. A first win vs a new player gives your fighter 1/4 star (4 quarters = a star,
 * all stats up) and unlocks the challenger's fighter (like a deck); rematch wins pay 2-3 yen. Beat the five, the fifth names Glitch
 * Kono (Coach's Office); beating him gives the DOUBLE SHOT cheat and the arcade-tournament lead. Menu > More > Handheld: VS CPU
 * practice anytime, rivals, the cheat pocket (one cheat, loads on start). Banter: BANTER.md as approved (tools/hh/hh_banter.js).
 * The handheld overlay runs its own rAF only while open and freezes the world layers like the Game Center cabinets. */
(function () {
  try {
  /*@@BANTER@@*/
  var HHA = function () { return root.FFF_S2ARC || null; };
  var HH_FIG = { ryo: 'Kaze Tenma', aoi: 'Blue Lotus', masa: 'The Ronin', nails: 'Razor Rei', goda: 'Iron Daimyo', jin: 'Black Comet' };
  var HH_FORDER = ['ryo', 'aoi', 'masa', 'nails', 'goda', 'jin'];
  var HH_ORDER = ['sota', 'rin', 'kaito', 'haru', 'yuto', 'glitch'];
  /* where / who. at, talk: dungeon room px (lw for the library); fa: facing; seat: [sheet, row] for the seated pair */
  var HH_CH = {
    sota: { n: 'Arai Sota', npc: 's_boy', dg: 'lib', mb: 'mb_lib', room: 'ante', id: 'dl_ante', where: 'Library \u00b7 Silent Study', f: 'aoi', st: 1, seat: ['lshp_boy_sit', 2], art: 'dl_boy_sit', lib: 's_boy',
      q: 'You found one too? Okay, quick match. Loser buys my soda.' },
    rin: { n: 'Ueda Rin', npc: 's_pony', dg: 'lib', mb: 'mb_lib', room: 'ante', id: 'dl_ante', where: 'Library \u00b7 Silent Study', f: 'masa', st: 1.25, seat: ['lshp_pony_sit', 2], art: 'dl_pony_sit', lib: 's_pony',
      q: 'Sound off, volume down. Librarian rules. Now hand me a fighter.' },
    kaito: { n: 'Fujii Kaito', npc: 'art_stu', dg: 'art', mb: 'mb_art', room: 'hall', id: 'am_hall', where: 'Art & Music \u00b7 Music Hall', f: 'nails', st: 1.5, at: [1010, 404], fa: Math.PI,
      q: 'You got us out. I\u2019ll pay you back with a beating. Kidding.' },
    haru: { n: 'Taniguchi Haru', npc: 'cafe_stu', dg: 'cafe', mb: 'mb_cafe', room: 'staff', id: 'cf_staff', where: 'Cafeteria \u00b7 Staff Room', f: 'goda', st: 1.75, at: [760, 330], fa: Math.PI / 2,
      q: 'Iron Daimyo hits like a vending machine. Want to feel it?' },
    yuto: { n: 'Sakai Yuto', npc: 'yuto', dg: 'field', mb: 'mb_field', room: 'coach', id: 'sf_coach', where: 'Storehouse \u00b7 Coach\u2019s Office', f: 'ryo', st: 2, at: [760, 330], fa: Math.PI / 2,
      q: 'Kaze Tenma versus Kaze Tenma. Let\u2019s see who plays him better.' },
    glitch: { n: 'Glitch K\u014dno', npc: 'glitch', dg: 'field', mb: 'mb_field', room: 'coach', id: 'sf_coach', where: 'Storehouse \u00b7 Coach\u2019s Office', f: 'jin', st: 2, at: [300, 640], seat: ['lshp_boy_sit', 2], art: 'dl_boy_sit', cheat: 1,
      q: 'So you finished the list. Black Comet. And I don\u2019t play fair.' }
  };
  var HH_SVG = '<svg viewBox="0 0 12 12" aria-hidden="true"><rect x="3" y="0.8" width="6" height="10.4" rx="1.2" fill="#2a1c00"/><rect x="4" y="2" width="4" height="3.4" fill="#9bbc0f"/><rect x="4.1" y="7.6" width="1.8" height=".7" fill="#f2b632"/><rect x="4.65" y="7.05" width=".7" height="1.8" fill="#f2b632"/><circle cx="7.4" cy="8" r=".6" fill="#f2b632"/></svg>';
  function hhEv(k) { try { ev('world:hh:' + k); } catch (e) {} }
  /* ---------- save (SAVE.hh, a key in fresh() so load keeps it) ---------- */
  function hhS() { var h = SAVE.hh; if (!h || typeof h !== 'object') h = SAVE.hh = {};
    if (!h.unl) h.unl = { ryo: 1 }; if (!h.qs) h.qs = {}; if (!h.beat) h.beat = {}; if (!h.bn) h.bn = []; if (!h.cheats) h.cheats = {}; if (!h.bp) h.bp = {}; if (!h.named) h.named = {}; if (!h.gl) h.gl = {};
    if (!h.sel || !h.unl[h.sel]) h.sel = 'ryo'; return h; }
  function hhOwn() { return !!(SAVE.hh && SAVE.hh.own); }
  function hhStars(f) { var q = (hhS().qs[f] | 0); return Math.min(5, 1 + Math.floor(q / 4)); }
  function hhQ(f) { var q = (hhS().qs[f] | 0); return hhStars(f) >= 5 ? 4 : q % 4; }
  function hhBoost(st) { var k = Math.max(0, st - 1); return { k: 1 + 0.06 * k, h: 1 + 0.06 * k, s: 1 + 0.04 * k }; }
  function hhStarTxt(st) { var w = Math.floor(st), r = st - w; return '\u2605' + w + (r >= 0.74 ? '\u00be' : r >= 0.49 ? '\u00bd' : r >= 0.24 ? '\u00bc' : ''); }
  function hhFive() { var h = hhS(); return ['sota', 'rin', 'kaito', 'haru', 'yuto'].filter(function (k) { return h.beat[k]; }).length; }
  function hhPath() { try { var B = STORY && STORY.bond ? STORY.bond(SAVE) : null, p = B && B.path; return p === 'fierce' || p === 'strategic' ? p : 'balanced'; } catch (e) { return 'balanced'; } }
  /* ---------- banter (no repeats until a pool cycles) ---------- */
  function hhPick(key, list) { if (!list || !list.length) return null; var h = hhS(), used = h.bp[key] || [], free = []; for (var i = 0; i < list.length; i++) if (used.indexOf(i) < 0) free.push(i);
    if (!free.length) { used = []; free = list.map(function (q, i) { return i; }); } var k = free[Math.floor(Math.random() * free.length)]; used.push(k); h.bp[key] = used; return list[k]; }
  function hhLines(ex) { return (ex || []).map(function (l) { return [l[0], l[1], { mood: 'neutral' }]; }); }
  function hhWalkUp(id) { var p = hhPath(), B = HH_BANTER[p]; if (!B) return null; var h = hhS();
    if (id === 'glitch') { if (h.gl.ap) return null; h.gl.ap = 1; return hhPick(p + ':gap', B.glitch.ap); }
    var nk = p + ':' + id; if (B.named[id] && !h.named[nk]) { h.named[nk] = 1; return B.named[id]; }
    return hhPick(p + ':walk', B.walk); }
  function hhAfterLines(id, won, first) { var p = hhPath(), B = HH_BANTER[p], h = hhS(); if (!B || !id) return null;
    if (id === 'glitch') { if (won) { if (!first) return null; return hhPick(p + ':gwin', B.glitch.win); } if (h.gl.loss) return null; h.gl.loss = 1; return hhPick(p + ':gloss', B.glitch.loss); }
    if (!won) return hhPick(p + ':loss', B.loss); return first ? hhPick(p + ':first', B.first) : hhPick(p + ':rematch', B.rematch); }
  function hhMidLines(kind) { var p = hhPath(), B = HH_BANTER[p]; if (!B) return null; return hhPick(p + ':' + kind, B[kind]); }
  function hhStrip(t) { return String(t || '').replace(/\{\/?[a-z]+(=\d+)?\}/g, ''); }
  /* ---------- CSS ---------- */
  var HH_CSS = '/*@@CSS@@*/';
  function hhCss() { if (document.getElementById('hh-css')) return; var s = document.createElement('style'); s.id = 'hh-css'; s.textContent = HH_CSS; (document.head || document.documentElement).appendChild(s); }
  hhCss();
  /* ---------- fighter art (drawn by the fighter engine itself, cached) ---------- */
  var HH_IMG = {};
  function hhFigUrl(f, w, h, sc, lcd) { var key = f + ':' + w + ':' + h + ':' + (lcd ? 1 : 0); if (HH_IMG[key]) return HH_IMG[key]; var A = HHA(); if (!A || !A.GAMES || !A.GAMES.fighter || !A.K) return '';
    try { var G = A.GAMES.fighter(A.K, A.CABS.fighter), c = document.createElement('canvas'); c.width = w; c.height = h; var q = c.getContext('2d');
      if (!lcd) { var gr = q.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#3a2a4e'); gr.addColorStop(1, '#1a1228'); q.fillStyle = gr; q.fillRect(0, 0, w, h); }
      G.figure(q, f, w / 2, h - 4, sc, 'win'); if (lcd) hhGreen(q, w, h, true); HH_IMG[key] = c.toDataURL('image/png'); try { if (G.dispose) G.dispose(); } catch (e2) {} c.width = c.height = 0; } catch (e) { HH_IMG[key] = ''; }
    return HH_IMG[key]; }
  /* the green LCD: keep the picture's light, swap its colour for the four greens, then the dot grid */
  var HH_DOTS = null;
  function hhDots(w, h) { if (HH_DOTS && HH_DOTS.width === w && HH_DOTS.height === h) return HH_DOTS; var c = document.createElement('canvas'); c.width = w; c.height = h; var q = c.getContext('2d'); q.fillStyle = 'rgba(15,56,15,.10)';
    for (var y = 0; y < h; y += 3) q.fillRect(0, y, w, 1); for (var x = 0; x < w; x += 3) q.fillRect(x, 0, 1, h); HH_DOTS = c; return c; }
  function hhGreen(q, w, h, noDots) { q.save(); q.globalCompositeOperation = 'color'; q.fillStyle = '#8bac0f'; q.fillRect(0, 0, w, h);
    q.globalCompositeOperation = 'multiply'; q.fillStyle = '#c8d89a'; q.fillRect(0, 0, w, h);
    q.globalCompositeOperation = 'screen'; q.fillStyle = '#0f2a0f'; q.fillRect(0, 0, w, h); q.restore(); if (!noDots) q.drawImage(hhDots(w, h), 0, 0); }

  /* ======================= the handheld (overlay) ======================= */
  var HHP = null; /* the open handheld */
  /* keys: one capture listener installed at load, ahead of the controller layer (which stops arrows while the world is paused) */
  root.addEventListener('keydown', function (e) { if (HHP && HHP.key) HHP.key(e, true); }, true); root.addEventListener('keyup', function (e) { if (HHP && HHP.key) HHP.key(e, false); }, true);
  var SX = 14, SY = 78, SW = 362, SH = 500;
  function hhPaint(p) { var K = HHA().K, rr = K.rr, txt = K.txt;
    p.fillStyle = '#10141c'; p.fillRect(-80, -20, 560, 900);
    var bg = p.createLinearGradient(0, 0, 0, 844); bg.addColorStop(0, '#ece6d6'); bg.addColorStop(1, '#d6cdb6'); rr(p, 3, 4, 384, 836, [18, 18, 70, 18], bg, 3, '#1b2a3c');
    p.fillStyle = 'rgba(0,0,0,.07)'; p.fillRect(8, 30, 374, 2); p.fillRect(8, 36, 374, 1);
    rr(p, 6, 44, 378, 548, [10, 10, 40, 10], '#4a5262', 2, '#1b2a3c');
    p.fillStyle = '#7a3a5a'; p.fillRect(22, 54, 120, 2); p.fillStyle = '#2a3a6a'; p.fillRect(22, 58, 120, 2); p.fillStyle = '#7a3a5a'; p.fillRect(248, 54, 120, 2); p.fillStyle = '#2a3a6a'; p.fillRect(248, 58, 120, 2);
    txt(p, 'DOT MATRIX WITH STEREO SOUND', 195, 58, 8, '#b8c0d0', 'center', 800);
    rr(p, SX - 3, SY - 3, SW + 6, SH + 6, 4, '#306230', 0);
    p.beginPath(); p.arc(22, 586, 4, 0, 7); p.fillStyle = '#ff3a4a'; p.fill(); txt(p, 'BATTERY', 32, 586, 7, '#b8c0d0', 'left', 800);
    p.font = 'italic 900 22px Georgia,serif'; p.textAlign = 'left'; p.textBaseline = 'middle'; p.fillStyle = '#1b2a3c'; p.fillText('Kitsune', 22, 622); p.font = '900 22px system-ui,sans-serif'; p.fillStyle = '#1f7a72'; p.fillText('BOY', 110, 622); txt(p, '\u2122', 158, 614, 9, '#1b2a3c');
    /* D-pad */
    var dx = 88, dy = 724; p.fillStyle = 'rgba(0,0,0,.12)'; p.beginPath(); p.arc(dx, dy, 62, 0, 7); p.fill();
    rr(p, dx - 19, dy - 56, 38, 112, 6, '#1b2a3c', 0); rr(p, dx - 56, dy - 19, 112, 38, 6, '#1b2a3c', 0);
    p.fillStyle = '#2a3a50'; p.beginPath(); p.arc(dx, dy, 11, 0, 7); p.fill();
    [[0, -40, 0], [0, 40, 1], [-40, 0, 2], [40, 0, 3]].forEach(function (a) { p.fillStyle = '#5a6a80'; p.beginPath(); var x = dx + a[0], y = dy + a[1], r = 7;
      if (a[2] === 0) { p.moveTo(x, y - r); p.lineTo(x - r, y + r * 0.6); p.lineTo(x + r, y + r * 0.6); } else if (a[2] === 1) { p.moveTo(x, y + r); p.lineTo(x - r, y - r * 0.6); p.lineTo(x + r, y - r * 0.6); }
      else if (a[2] === 2) { p.moveTo(x - r, y); p.lineTo(x + r * 0.6, y - r); p.lineTo(x + r * 0.6, y + r); } else { p.moveTo(x + r, y); p.lineTo(x - r * 0.6, y - r); p.lineTo(x - r * 0.6, y + r); } p.closePath(); p.fill(); });
    txt(p, 'JUMP', dx, dy - 72, 8, '#5c6b7c', 'center', 800);
    /* A / B on a tilted pad */
    p.save(); p.translate(296, 716); p.rotate(-0.42); rr(p, -78, -36, 156, 72, 36, 'rgba(0,0,0,.1)', 0); p.restore();
    [[258, 740, 'B', 'SPECIAL'], [334, 696, 'A', 'ATTACK']].forEach(function (b) { p.fillStyle = 'rgba(0,0,0,.25)'; p.beginPath(); p.arc(b[0], b[1] + 3, 31, 0, 7); p.fill(); p.fillStyle = '#a3324a'; p.beginPath(); p.arc(b[0], b[1], 31, 0, 7); p.fill(); p.lineWidth = 2; p.strokeStyle = '#1b2a3c'; p.stroke(); txt(p, b[2], b[0], b[1] + 1, 18, '#f6e9ec'); txt(p, b[3], b[0], b[1] + 46, 9, '#1b2a3c', 'center', 800); });
    /* select / start */
    [[160, 'SELECT'], [230, 'START']].forEach(function (b) { p.save(); p.translate(b[0], 806); p.rotate(-0.42); rr(p, -20, -6, 40, 12, 6, '#8a8f9a', 1.5, '#1b2a3c'); p.restore(); txt(p, b[1], b[0] + 4, 826, 8, '#1b2a3c', 'center', 800); });
    /* speaker */
    p.save(); p.translate(330, 790); p.rotate(-0.42); for (var i = 0; i < 6; i++) rr(p, -30 + i * 11, -22, 5, 44, 2.5, 'rgba(27,42,60,.55)', 0); p.restore();
  }
  function hhFreeze(on) { var skip = document.getElementById('j6hh');
    if (on) { var hid = []; function hide(e) { if (!e || e === skip || (skip && skip.contains(e))) return; hid.push([e, e.style.visibility]); e.style.visibility = 'hidden'; }
      ['world', 'wv', 'wimap', 'wmap', 'wsky', 'wrain', 'wisp'].forEach(function (id) { hide(document.getElementById(id)); }); [].forEach.call(document.querySelectorAll('canvas'), hide); return hid; }
    return null; }
  function hhUnfreeze(hid) { (hid || []).forEach(function (p) { try { p[0].style.visibility = p[1]; } catch (e) {} }); }
  /* hhPlay(o): o = { foe, foeSt, me, title, ch (challenger id or ''), dbl, onEnd(won, quit) } */
  function hhPlay(o) { var A = HHA(); if (!A || !A.GAMES || !A.GAMES.fighter) { toast('The handheld will not turn on.'); return false; }
    if (HHP) HHP.kill(true);
    var prev = { paused: W.paused, dlg: W.dlg }, h = hhS(), me = o.me || h.sel, mb = hhBoost(hhStars(me)), eb = hhBoost(o.foeSt || 1);
    var mid = 0, t = 0, st = 'boot', stT = 0, done = false, res = null, last = performance.now(), raf = 0;
    var cfg = { me: me, foe: o.foe, lv: Math.max(0, ((o.foeSt || 1) - 1) * 1.6), pk: mb.k, ph: mb.h, ps: mb.s, ek: eb.k, eh: eb.h, es: eb.s, dbl: o.dbl || '', title: o.title || 'VS CPU',
      on: function (k) { if (k === 'super' && o.ch && !mid) midSay('super'); } };
    var C = Object.create(A.CABS.fighter); C.hh = cfg;
    var G = A.GAMES.fighter(A.K, C); G.in = G.in || {};
    var el = document.createElement('div'); el.id = 'j6hh'; (document.body || document.documentElement).appendChild(el);
    var hid = hhFreeze(true); W.paused = true; W.dlg = true; W.path = []; if (W.ryo) W.ryo.v = 0;
    try { if (root.AUDIO && root.AUDIO.music) root.AUDIO.music(null); } catch (e1) {} try { var ac = A.actx && A.actx(); if (ac && ac.state !== 'running' && ac.resume) ac.resume(); } catch (e2) {}
    var cv = document.createElement('canvas'), W0 = el.clientWidth || innerWidth, H0 = el.clientHeight || innerHeight; cv.width = Math.round(W0); cv.height = Math.round(H0); el.appendChild(cv);
    var g = cv.getContext('2d'); g.imageSmoothingEnabled = false; var s = Math.min(W0 / 390, H0 / 844), ox = (W0 - 390 * s) / 2, oy = (H0 - 844 * s) / 2;
    var plate = document.createElement('canvas'); plate.width = cv.width; plate.height = cv.height; var pq = plate.getContext('2d'); pq.setTransform(s, 0, 0, s, ox, oy); hhPaint(pq);
    var scr = document.createElement('canvas'); scr.width = SW; scr.height = SH; var sg = scr.getContext('2d');
    var lv = document.createElement('button'); lv.type = 'button'; lv.className = 'hhx'; lv.textContent = 'Leave'; el.appendChild(lv);
    lv.addEventListener('click', function (e) { e.stopPropagation(); if (st === 'result') { finish(); return; } kill(true); });
    var bx = document.createElement('div'); bx.className = 'hhmid'; bx.style.cssText = 'left:' + (ox + (SX + 8) * s) + 'px;top:' + (oy + (SY + 64) * s) + 'px;width:' + ((SW - 16) * s) + 'px'; el.appendChild(bx);
    var rb = null;
    function midSay(kind) { if (mid || !o.ch) return; mid = 1; var ex = hhMidLines(kind); if (!ex || !ex.length) return; hhEv('mid:' + kind); var i = 0;
      (function next() { if (done || i >= ex.length) { bx.classList.remove('on'); return; } var l = ex[i++], who = l[0];
        bx.innerHTML = '<i class="pt" style="background-image:url(' + (typeof dlgPtUrl === 'function' ? dlgPtUrl(who) : '') + ')"></i><span><b>' + (who === 'aoi' ? 'Aoi' : 'Ryo') + '</b>' + hhStrip(l[1]) + '</span>'; bx.classList.add('on');
        setTimeout(next, Math.max(1700, 900 + hhStrip(l[1]).length * 45)); })(); }
    function des(e) { var r = cv.getBoundingClientRect(); return [(e.clientX - r.left - ox) / s, (e.clientY - r.top - oy) / s]; }
    var ptr = {}, BT = { a: [334, 696], sp: [258, 740] }, DP = [88, 724];
    function padSet(P, x, y) { var dx = (x - DP[0]) / 56, dy = (y - DP[1]) / 56, I = G.in; I.l = dx < -0.3; I.r = dx > 0.3; if (dy < -0.45 && !P.up && st === 'play') { P.up = 1; if (G.swipeUp) G.swipeUp(I.l ? -30 : I.r ? 30 : 0); } if (dy > -0.2) P.up = 0; }
    function padOff() { G.in.l = G.in.r = false; }
    function down(e) { if (done) return; e.preventDefault(); var q = des(e), x = q[0], y = q[1];
      if (st === 'intro') { if (stT > 0.8) go('play'); return; } if (st === 'boot') return; if (st === 'result') return;
      if (Math.abs(x - DP[0]) < 80 && Math.abs(y - DP[1]) < 80) { var P = ptr[e.pointerId] = { k: 'pad' }; padSet(P, x, y); return; }
      for (var k in BT) { var b = BT[k]; if ((x - b[0]) * (x - b[0]) + (y - b[1]) * (y - b[1]) < 44 * 44) { ptr[e.pointerId] = { k: 'btn', b: k }; G.in[k] = true; if (G.press) G.press(k); return; } } }
    function move(e) { var P = ptr[e.pointerId]; if (!P || done) return; var q = des(e); if (P.k === 'pad') padSet(P, q[0], q[1]); }
    function up(e) { var P = ptr[e.pointerId]; if (!P) return; delete ptr[e.pointerId]; if (P.k === 'pad') padOff(); else if (P.k === 'btn') { G.in[P.b] = false; if (G.release) G.release(P.b); } }
    cv.addEventListener('pointerdown', down); cv.addEventListener('pointermove', move); cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', up);
    var KD = { ArrowLeft: 'l', ArrowRight: 'r', a: 'l', d: 'r' }, KU = { ArrowUp: 1, w: 1, ' ': 1 }, KA = { z: 'a', j: 'a', x: 'sp', k: 'sp' }, held = {};
    function key(e, dn) { if (done) return; var k = e.key; if (!(k in KD || k in KU || k in KA || k === 'Escape' || k === 'Enter')) return; e.preventDefault(); e.stopPropagation(); if (e.stopImmediatePropagation) e.stopImmediatePropagation();
      if (k === 'Escape') { if (dn) { if (st === 'result') finish(); else kill(true); } return; }
      if (st === 'intro') { if (dn && stT > 0.8) go('play'); return; } if (st === 'result') { if (dn && k === 'Enter') finish(); return; } if (st !== 'play') return;
      if (KD[k]) { G.in[KD[k]] = dn; return; } if (KU[k]) { if (dn && !held[k] && G.swipeUp) G.swipeUp(G.in.l ? -30 : G.in.r ? 30 : 0); held[k] = dn; return; }
      if (KA[k]) { var b = KA[k]; if (dn && !held[k]) { G.in[b] = true; if (G.press) G.press(b); } else if (!dn && held[k]) { G.in[b] = false; if (G.release) G.release(b); } held[k] = dn; } }
    function kd(e) { key(e, true); } function ku(e) { key(e, false); }
    function go(k) { st = k; stT = 0; hhEv('st:' + k); }
    function tick(ts) { if (done) return; var dt = Math.min(0.05, Math.max(0, (ts - last) / 1000)); last = ts; t += dt; stT += dt;
      if (st === 'boot' && stT > 1.1) { G.start(); go('intro'); }
      if (st === 'intro' && stT > 2.6) go('play');
      if (st === 'play') { var r = G.step(dt); if (o.ch && !mid) { try { var pe = G._pe(), P = pe && pe[0]; if (P && P.hp > 0 && P.hp / P.max < 0.3 && G.phase() === 'fight') midSay('low'); } catch (eP) {} }
        if (r === 'clear' || r === 'win') end(true); else if (r === 'dead') end(false); }
      draw(); raf = requestAnimationFrame(tick); }
    function draw() { var K = A.K; sg.setTransform(1, 0, 0, 1, 0, 0);
      if (st === 'boot') { sg.fillStyle = '#9bbc0f'; sg.fillRect(0, 0, SW, SH); var y = Math.min(200, -40 + stT * 300); K.txt(sg, 'Kitsune', SW / 2 - 20, y, 34, '#0f380f', 'center', 900); K.txt(sg, 'BOY', SW / 2 + 74, y, 30, '#306230', 'center', 900); if (stT > 0.75) K.txt(sg, '\u00ae KITSUNE SOFT', SW / 2, 240, 12, '#306230', 'center', 800); }
      else { if (st === 'intro' && G.introDraw) { G.draw(sg, t); G.introDraw(sg, stT); } else G.draw(sg, t);
        if (st === 'result' && res) { sg.fillStyle = 'rgba(0,0,0,.5)'; sg.fillRect(0, 0, SW, SH); K.otxt(sg, res.won ? 'YOU WIN!' : 'YOU LOSE', SW / 2, 150, 38, res.won ? '#ffd860' : '#ff5a6a');
          (res.lines || []).forEach(function (l, i) { K.txt(sg, l, SW / 2, 214 + i * 30, 15, '#fff', 'center', 800); }); }
        hhGreen(sg, SW, SH); }
      g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(plate, 0, 0); g.drawImage(scr, ox + SX * s, oy + SY * s, SW * s, SH * s);
      if (st === 'play') { var pr = G.in; hl(BT.a, pr.a); hl(BT.sp, pr.sp); var gl = G.panel && G.panel.btns && G.panel.btns[1] && G.panel.btns[1].glow && G.panel.btns[1].glow(); if (gl) { g.save(); g.globalAlpha = 0.45 + 0.35 * Math.sin(t * 8); g.strokeStyle = '#9bfa6a'; g.lineWidth = 4 * s; g.beginPath(); g.arc(ox + BT.sp[0] * s, oy + BT.sp[1] * s, 37 * s, 0, 7); g.stroke(); g.restore(); } } }
    function hl(b, on) { if (!on) return; g.fillStyle = 'rgba(0,0,0,.22)'; g.beginPath(); g.arc(ox + b[0] * s, oy + b[1] * s, 31 * s, 0, 7); g.fill(); }
    function end(won) { if (res) return; res = { won: won, lines: [] }; try { if (o.onResult) res.lines = o.onResult(won) || []; } catch (eR) { hhEv('err:res:' + (eR && eR.message)); } go('result'); bx.classList.remove('on');
      rb = document.createElement('div'); rb.className = 'hhres'; rb.style.cssText = 'left:' + (ox + 40 * s) + 'px;width:' + (310 * s) + 'px;top:' + (oy + (SY + SH - 86) * s) + 'px';
      var b1 = document.createElement('button'); b1.type = 'button'; b1.textContent = 'Done'; b1.addEventListener('click', function (e) { e.stopPropagation(); finish(); }); rb.appendChild(b1);
      if (o.again) { var b2 = document.createElement('button'); b2.type = 'button'; b2.className = 'hot'; b2.textContent = 'Again'; b2.addEventListener('click', function (e) { e.stopPropagation(); finish(true); }); rb.appendChild(b2); }
      el.appendChild(rb); hhEv('end:' + (o.ch || 'cpu') + ':' + (won ? 'win' : 'loss')); }
    function finish(again) { var r = res; kill(false); if (o.onEnd) o.onEnd(r ? r.won : false, false, again); }
    function kill(quit) { if (done) return; done = true; cancelAnimationFrame(raf);
      try { if (G.dispose) G.dispose(); } catch (eD) {} plate.width = plate.height = 0; scr.width = scr.height = 0; cv.width = cv.height = 0; if (el.parentNode) el.parentNode.removeChild(el); hhUnfreeze(hid);
      W.paused = prev.paused; W.dlg = prev.dlg; if (W.ryo) W.ryo.v = 0; W.path = []; HHP = null; try { wMus(); } catch (eM) {} hhEv('close:' + (quit ? 'quit' : 'done'));
      if (quit && o.onEnd) o.onEnd(false, true); }
    HHP = { key: key, kill: kill, st: function () { return st; }, G: G, cfg: cfg, go: go, end: end, res: function () { return res; } };
    hhEv('open:' + (o.ch || 'cpu') + ':' + me + ':' + o.foe); raf = requestAnimationFrame(tick); return true; }

  /* ======================= challengers in the world ======================= */
  function hhSpawnable(id) { var C = HH_CH[id], h = hhS(); if (!beaten(C.mb)) return false;
    if (id === 'sota') return true; /* the tipster sits in the Silent Study once the Library is clear */
    return !!h.own; }
  function hhMarked(id) { var h = hhS(); if (!h.own || h.beat[id]) return false; if (id === 'glitch') return hhFive() >= 5; return true; }
  function hhSpawn() { var I = W.inside; W.hhS = (W.hhS || []).filter(function (q) { return q.s.el && q.s.el.parentNode; }); if (!I) return; var D = INT[I.id]; if (!D || !D.dg) return;
    if (W.cut || W.intBul) return;
    HH_ORDER.forEach(function (id) { var C = HH_CH[id]; if (C.id !== I.id || !hhSpawnable(id)) return; if (W.hhS.some(function (q) { return q.id === id; })) return;
      var at, talk, R = null, s;
      if (C.lib) { R = LIBG[C.room]; var q = LSHP[C.lib]; at = lw(R, q.at); talk = lw(R, q.talk); } else { at = C.at.slice(); talk = [C.at[0], C.at[1] + 44]; }
      if (C.seat) { s = intSprite(C.art, SPH, 'ldaze'); s.el.classList.add('hhstu'); s.x = at[0]; s.y = at[1]; place(s, 0); celLoop(s, C.seat[0], C.seat[1], { ms: 420 }); }
      else { s = stuSprite0(C.npc, 1); if (!s) return; s.el.classList.add('hhstu'); s.x = at[0]; s.y = at[1]; place(s, 0); waddle(s, 0, C.fa || 0); }
      s.el.dataset.hh = id; if (id === 'glitch') { s.el.classList.add('hhglitch'); talk = [at[0] + 56, at[1] + 20]; }
      W.hhS.push({ id: id, s: s, talk: talk, th: C.seat ? 84 : 96 }); hhEv('spawn:' + id); }); }
  function hhTags() { var I = W.inside; if (!I || !W.hhS || !W.hhS.length) return []; return W.hhS.filter(function (q) { return q.s.el && q.s.el.parentNode && HH_CH[q.id].id === I.id; }).map(function (q) { var mk = hhMarked(q.id);
      return { key: I.id + ':hh:' + q.id, lab: 'Talk', x: q.s.x, y: q.s.y - q.th, below: false, ax: q.talk[0], ay: q.talk[1], R: 78, vm: false, cls: mk ? ' vs' : '', hhIcon: mk, fn: function () { hhTalk(q.id, q); } }; }); }
  function hhSig() { var h = SAVE.hh; return h ? ':hh' + (h.own ? 1 : 0) + (h.tip ? 1 : 0) + Object.keys(h.beat || {}).join('') + (W.hhS || []).length : ''; }
  function hhFace(q) { if (!q || !q.s || HH_CH[q.id].seat) return; try { waddle(q.s, 0, Math.atan2(W.ryo.y - q.s.y, W.ryo.x - q.s.x)); } catch (e) {} }
  function hhTalk(id, q) { var h = hhS(), C = HH_CH[id]; hhEv('talk:' + id); hhFace(q);
    if (id === 'sota' && !h.own) {
      if (!h.tip) { h.tip = 1; save(); W.dlg = true; scene(null, [['s_boy', 'Hey. You\u2019re the two who pulled the headphones off. Thanks. Really.', { mood: 'neutral' }],
          ['s_boy', 'Mine got confiscated last week. The teachers keep them in a box in the Staff Room.', { mood: 'neutral' }],
          ['s_boy', 'Staff Room\u2019s by the nurse. Get yours and play me. I\u2019m good.', { mood: 'neutral' }],
          ['ryo', 'A fighting game. Fine. Don\u2019t cry when you lose.', { mood: 'neutral' }]], function () { W.dlg = false; hhEv('tip'); toast('Journal: A Game in the Staff Room'); tagsRebuild(); });
        return; }
      W.dlg = true; scene(null, [['s_boy', 'Staff Room, by the nurse. A box on the desks. Go on.', { mood: 'neutral' }]], function () { W.dlg = false; }); return; }
    if (id === 'glitch' && hhFive() < 5) { W.dlg = true; scene(null, [['glitch', 'Five names first. Then we\u2019ll talk.', { mood: 'neutral' }]], function () { W.dlg = false; }); return; }
    hhAsk(id); }
  function hhAsk(id) { var h = hhS(), C = HH_CH[id], first = !h.beat[id];
    var info = 'Sh\u014dnen Showdown \u00b7 plays ' + HH_FIG[C.f] + ' (CPU ' + hhStarTxt(C.st) + ')' + (C.cheat ? ' + a hidden rule' : '') + ' \u00b7 ' + (first ? 'first win: +\u00bc\u2605 for ' + HH_FIG[h.sel] + (C.f !== 'ryo' && !h.unl[C.f] ? ', and ' + HH_FIG[C.f] : '') : 'rematch win: \u00a52\u20133');
    dialog('<b>' + C.n + '</b><p class="q">\u201c' + (first ? C.q : 'Again? Fine. Same stakes, smaller.') + '\u201d</p><p class="dim">' + info + '</p>', [['Not now', function () { hhEv('ask:no:' + id); }], ['Play', function () { hhGo(id); }, 'hot']], C.npc, { versus: 1 });
    hhEv('ask:' + id); }
  function hhGo(id) { var ex = hhWalkUp(id); save(); W.dlg = true;
    function start() { hhChallenge(id); }
    if (ex && ex.length) scene(null, hhLines(ex), function () { start(); }); else start(); }
  function hhChallenge(id) { var h = hhS(), C = HH_CH[id], first = !h.beat[id], me = h.sel, dbl = (h.cOn === 'dbl' && h.cheats.dbl ? 'p' : '') + (C.cheat ? 'e' : '');
    hhPlay({ foe: C.f, foeSt: C.st, me: me, ch: id, dbl: dbl, title: 'VS ' + C.n.toUpperCase(),
      onResult: function (won) { return hhReward(id, won, first, me); },
      onEnd: function (won, quit) { W.dlg = true; if (quit) { W.dlg = false; return; } hhAfter(id, won, first); } }); }
  function hhReward(id, won, first, me) { var h = hhS(), C = HH_CH[id], out = []; if (won) h.w = (h.w | 0) + 1; else h.l = (h.l | 0) + 1;
    if (won && first) { var s0 = hhStars(me); h.beat[id] = 1; if (h.bn.indexOf(id) < 0) h.bn.push(id); h.qs[me] = (h.qs[me] | 0) + 1; out.push('+\u00bc\u2605 ' + HH_FIG[me].toUpperCase());
      if (hhStars(me) > s0) { out.push(HH_FIG[me].toUpperCase() + ' ' + hhStarTxt(hhStars(me)) + ' \u00b7 ALL STATS UP'); h.starUp = me; }
      if (!h.unl[C.f]) { h.unl[C.f] = 1; out.push('NEW FIGHTER: ' + HH_FIG[C.f].toUpperCase()); h.newF = C.f; }
      if (id === 'glitch') { h.cheats.dbl = 1; if (!h.cOn) h.cOn = 'dbl'; h.lead = 1; out.push('CHEAT: DOUBLE SHOT'); } }
    else if (won) { var y = 2 + (Math.random() < 0.5 ? 1 : 0); SAVE.items = (SAVE.items | 0) + y; out.push('+\u00a5' + y); try { hud(); } catch (eH) {} }
    else out.push(first ? 'No star this time. Talk to them again.' : 'Rematch anytime.');
    save(); hhEv('reward:' + id + ':' + (won ? 'w' : 'l') + ':' + (first ? 1 : 0)); return out; }
  function hhAfter(id, won, first) { var h = hhS(), C = HH_CH[id], L = [], ex = hhAfterLines(id, won, won && first);
    if (won && first && id === 'glitch') L.push(['glitch', 'Fine. The code\u2019s yours. Real players settle it at the arcade tournament. Later.', { mood: 'neutral' }]);
    if (ex) L = L.concat(hhLines(ex));
    if (won && first && id !== 'glitch' && hhFive() === 5 && !h.hint) { h.hint = id; L.push([C.npc, 'There\u2019s one more. K\u014dno. Back of the Coach\u2019s Office. He plays dirty.', { mood: 'neutral' }]); }
    save(); var fin = function () { W.dlg = false; tagsRebuild(); if (won && first) { if (id === 'glitch') toast('Cheat pocket: DOUBLE SHOT \u00b7 Journal: a new lead'); else if (h.newF) toast('New fighter: ' + HH_FIG[h.newF]); }
      h.newF = null; h.starUp = null; save(); hhEv('after:' + id); };
    if (L.length) scene(null, L, fin); else fin(); }
  function tagsRebuild() { try { W.tagSig = ''; tagsBuild(); } catch (e) {} }
  function hhPractice() { var h = hhS(), pool = HH_FORDER.filter(function (f) { return f !== h.sel; }), foe = pool[Math.floor(Math.random() * pool.length)];
    hhPlay({ foe: foe, foeSt: 1.5, me: h.sel, ch: '', dbl: h.cOn === 'dbl' && h.cheats.dbl ? 'p' : '', title: 'VS CPU \u00b7 PRACTICE', again: 1,
      onResult: function (won) { var hs = hhS(); if (won) hs.w = (hs.w | 0) + 1; else hs.l = (hs.l | 0) + 1; save(); return ['Practice \u00b7 no stars, no yen']; },
      onEnd: function (won, quit, again) { if (again) { hhPractice(); return; } if (W.ptab === 'hh') pause('hh'); } }); }

  /* ======================= the Staff Room ======================= */
  INT.hall.spots.forEach(function (s) { if (s.id === 'lockers' && s.r[0] === 1604) { s.r = [1700, 72, 1766, 224]; s.at = [1733, 246]; } });
  INT.hall.spots.push({ id: 'sdoor', r: [1600, 70, 1690, 214], at: [1645, 246], face: 3 });
  TRANS.sdoor = 1; CLS_DOOR.sdoor = 'hstaff';
  CLS_OBJ.hstaff = [{ id: 'cbox', r: [640, 336, 712, 380], at: [676, 458], face: 3 }, { id: 'cab', r: [96, 176, 202, 250], at: [150, 268], face: 3 }, { id: 'tea', r: [736, 172, 882, 252], at: [808, 270], face: 3 }];
  INT.hstaff = clsInt('hstaff', 'Staff Room', 'sdoor', [[96, 170, 204, 254], [736, 160, 884, 254], [204, 262, 420, 442], [514, 262, 730, 442], [96, 466, 300, 542], [128, 542, 264, 570], [750, 450, 854, 552], [846, 494, 902, 570]]);
  INT.hstaff.src = 'world/int_staff.webp'; INT.hstaff.stu = 1;
  TAGS_IN.hstaff = { chalk: 1, cbox: 1, cab: 1, tea: 1 }; OBJ.cbox = 1; OBJ.tea = 1;
  CLS_TXT.hstaff = 'The duty roster. Every name is crossed out except the nurse\u2019s, circled twice.';
  CLS_LOOK.hstaff = { cab: 'Report cards, filed by class. One drawer is labelled \u201cHums?\u201d in red.', tea: 'A kettle and five mugs. One is still warm.', cbox: 'A box marked \u6ca1\u53ce. Confiscated. Comics, a yo-yo, somebody\u2019s phone charm.' };
  var HH_PATCH = { src: 'world/int_hall_sdoor.webp', box: [1594, 48, 176, 188] };
  function hhDoorSync() { var m = document.getElementById('wimap'); if (!m) return; var e = m.querySelector('.hhsdoor'), on = W.inside && W.inside.id === 'hall' && /int_hall\.webp/.test(INT.hall.src || '') && !INT.hall.tiles;
    if (!on) { if (e) e.style.display = 'none'; return; }
    if (!e) { e = document.createElement('i'); e.className = 'hhsdoor'; var b = HH_PATCH.box; e.style.cssText = 'position:absolute;left:' + b[0] + 'px;top:' + b[1] + 'px;width:' + b[2] + 'px;height:' + b[3] + 'px;background:url(' + HH_PATCH.src + '?v=' + BUILD + ') 0 0/100% 100% no-repeat;pointer-events:none;z-index:0'; m.insertBefore(e, m.firstChild); }
    e.style.display = 'block'; }
  function hhBoxProp() { if (!W.inside || W.inside.id !== 'hstaff' || hhOwn()) return; var e = document.createElement('i'); e.className = 'wprop hhboy'; e.style.cssText = 'left:663px;top:330px;width:28px;height:20px;background-image:url(world/hh_boy.webp?v=' + BUILD + ');z-index:' + (100 + 352); (layer || document.getElementById('wisp')).appendChild(e); W.ints.push({ el: e, x: 677, y: 352 }); }
  function hhPickup() { var h = hhS(); h.own = 1; h.tip = 1; save(); var p = document.querySelector('.hhboy'); if (p) p.remove(); AU.play('pickup', { gain: 0.8 }); hhEv('pickup');
    W.dlg = true; scene(null, [['', '<p class="dim">Under a confiscated yo-yo: a cream handheld, KITSUNE BOY on the front. A Sh\u014dnen Showdown cartridge is still in it.</p>'],
      ['aoi', 'Sota said play him. I think he meant borrow it.', { mood: 'neutral' }], ['ryo', 'Borrow. Sure.', { mood: 'neutral' }],
      ['', '<p class="dim">New: Menu \u203a More \u203a Handheld. Gold-ringed Talk bubbles are challengers.</p>']], function () { W.dlg = false; tagsRebuild(); toast('Got the Kitsune BOY'); }); }

  /* ======================= hooks ======================= */
  var hhIntGo0 = intGo; intGo = function (id, o) { var r = hhIntGo0.apply(this, arguments); try { hhDoorSync(); hhBoxProp(); hhSpawn(); } catch (e) { hhEv('err:go:' + (e && e.message)); } return r; };
  var hhIntAct0 = intAct; intAct = function (a) { var I = W.inside;
    if (I && I.id === 'hall' && a === 'sdoor' && !beaten('mb_lib')) { hhEv('sdoor:locked'); W.dlg = true; scene(null, [['', '<p class="dim">' + HALL_TXT.d5 + '</p>']], function () { W.dlg = false; }); return; }
    if (I && I.id === 'hstaff' && a === 'cbox' && !hhOwn()) { hhPickup(); return; }
    return hhIntAct0.apply(this, arguments); };
  var hhDg0 = dgTags; dgTags = function (id, D) { var o = hhDg0.apply(this, arguments) || []; try { if (!W.cut) o = o.concat(hhTags()); } catch (e) {} return o; };
  var hhSig0 = tagSig; tagSig = function () { return hhSig0.apply(this, arguments) + hhSig(); };
  var hhBuild0 = tagsBuild; tagsBuild = function () { var r = hhBuild0.apply(this, arguments); try { (W.tagL || []).forEach(function (t) { if (!t.hhIcon || !t.el) return; var tb = t.el.querySelector('.tb'); if (tb && !tb.querySelector('.vsi')) { var i = document.createElement('i'); i.className = 'vsi'; i.innerHTML = HH_SVG; tb.appendChild(i); } }); } catch (e) {} return r; };
  /* menu: Menu > More > Handheld */
  PH_IC.hh = phSvg('<rect x="15" y="7" width="18" height="34" rx="3"/><rect x="18.5" y="11" width="11" height="10" rx="1"/><path d="M20 29h4M22 27v4"/><circle cx="28.5" cy="28" r="1.4"/><circle cx="26" cy="32" r="1.4"/>');
  var hhHome0 = phHome; phHome = function () { var hs = hhHome0.apply(this, arguments); if (!hhOwn()) return hs; var b = '<button type="button" class="ph-m" data-a="go" data-s="hh">' + PH_IC.hh + 'Handheld</button>', k = hs.indexOf('</div><p class="ph-foot">'); return k < 0 ? hs : hs.slice(0, k) + b + hs.slice(k); };
  var hhTitle0 = phTitle; phTitle = function (tab) { return tab === 'hh' ? 'Handheld' : hhTitle0.apply(this, arguments); };
  var hhBody0 = phBody; phBody = function (tab) { return tab === 'hh' ? hhPane() : hhBody0.apply(this, arguments); };
  var hhClicks0 = phClicks; phClicks = function (o, tab) { hhClicks0.apply(this, arguments); if (tab !== 'hh') return;
    o.querySelectorAll('[data-hh]').forEach(function (b) { b.onclick = function (e) { e.stopPropagation(); var a = b.dataset.hh; AU.play('ui_sel'); hhEv('menu:' + a + ':' + (b.dataset.v || ''));
      if (a === 'tab') { W.hhTab = b.dataset.v; pause('hh'); return; }
      if (a === 'cpu') { hhPractice(); return; }
      if (a === 'sel') { var h = hhS(); if (h.unl[b.dataset.v]) { h.sel = b.dataset.v; save(); toast('Bringing ' + HH_FIG[h.sel] + '.'); } else toast('Beat its owner to unlock it.'); pause('hh'); return; }
      if (a === 'cheat') { var h2 = hhS(); if (!h2.cheats[b.dataset.v]) { toast('Locked.'); return; } h2.cOn = h2.cOn === b.dataset.v ? '' : b.dataset.v; save(); toast(h2.cOn ? 'DOUBLE SHOT loads on your next match.' : 'Cheat off.'); pause('hh'); return; } }; }); };
  function hhStarsHtml(n) { var s = ''; for (var i = 0; i < 5; i++) s += i < n ? '\u2605' : '<s>\u2605</s>'; return '<span class="sr">' + s + '</span>'; }
  function hhPips(k) { var s = ''; for (var i = 0; i < 4; i++) s += '<i' + (i < k ? ' class="on"' : '') + '></i>'; return '<span class="pp">' + s + '</span>'; }
  function hhPane() { var h = hhS(), tab = W.hhTab === 'riv' || W.hhTab === 'cht' ? W.hhTab : 'play', nb = HH_ORDER.filter(function (k) { return h.beat[k]; }).length, nc = Object.keys(h.cheats).filter(function (k) { return h.cheats[k]; }).length;
    var x = '<div class="ph-tabs" role="tablist">' + [['play', 'Play', ''], ['riv', 'Rivals', nb + '/6'], ['cht', 'Cheats', nc ? String(nc) : '']].map(function (t) { return '<button type="button" data-hh="tab" data-v="' + t[0] + '"' + (t[0] === tab ? ' class="on"' : '') + '>' + t[1] + (t[2] ? '<em>' + t[2] + '</em>' : '') + '</button>'; }).join('') + '</div>';
    if (tab === 'play') {
      x += '<div class="hh-dev"><div class="hh-bez"><i class="led"></i><span class="bl">DOT MATRIX \u00b7 STEREO SOUND</span><div class="hh-lcd"><img class="hhfig" alt="" src="' + hhFigUrl(h.sel, 72, 118, 0.62, true) + '"><div class="hhside"><span class="logo">SH\u014cNEN<br>SHOWDOWN</span><span class="jp">\u5c11\u5e74\u5bfe\u6c7a</span><div class="mn"><div><i>\u25b6</i><span class="on">VS CPU</span></div><div><i></i>RIVALS ' + nb + '/6</div><div><i></i>CHEATS' + (h.cOn ? ' \u00b7 ON' : '') + '</div></div><span class="st">' + HH_FIG[h.sel].toUpperCase() + ' ' + hhStarTxt(hhStars(h.sel)) + '</span></div></div></div><div class="hh-brand">Kitsune<i>BOY</i></div><div class="hh-ctl"><i class="hh-dpad"></i><div class="hh-ab"><i>B</i><i>A</i></div></div></div>';
      x += '<button type="button" class="hh-go" data-hh="cpu"><span class="pl">\u25b6</span><span><b>VS CPU</b><small>Practice anytime \u00b7 no stars, no yen</small></span></button>';
      x += '<h3 class="hh3">Your fighters <small>pick one to bring</small></h3><div class="hh-fg">' + HH_FORDER.map(function (f) { var u = !!h.unl[f], src = HH_ORDER.filter(function (k) { return HH_CH[k].f === f && k !== 'yuto'; })[0], sub;
        if (u) sub = hhStars(f) >= 5 ? 'max' : hhQ(f) + ' / 4 to \u2605' + (hhStars(f) + 1); else sub = 'Beat ' + (src === 'glitch' && hhFive() < 5 ? '???' : HH_CH[src] ? HH_CH[src].n.split(' ')[1] : '???');
        return '<button type="button" class="hh-f' + (h.sel === f ? ' sel' : '') + (u ? '' : ' lock') + '" data-hh="sel" data-v="' + f + '"><div class="im" style="background-image:url(' + hhFigUrl(f, 120, 112, 0.5, false) + ')"></div><b>' + (u ? HH_FIG[f] : '???') + '</b>' + (u ? hhStarsHtml(hhStars(f)) + hhPips(hhQ(f)) : '') + '<small>' + sub + '</small></button>'; }).join('') + '</div>';
      x += '<button type="button" class="hh-cp" data-hh="tab" data-v="cht"><span class="ic">' + (h.cOn ? 'ON' : '?') + '</span><span><b>Cheat pocket</b><small>' + (h.cheats.dbl ? (h.cOn ? 'DOUBLE SHOT loads on your next match.' : 'DOUBLE SHOT is in the pocket, switched off.') : 'Empty. Shady players carry codes.') + '<br>One cheat per match.</small></span><u>Open</u></button>';
    } else if (tab === 'riv') {
      HH_ORDER.forEach(function (k) { var C = HH_CH[k], b = !!h.beat[k], hide = k === 'glitch' && !h.hint && !b, pt = hide ? '' : (typeof dlgPtUrl === 'function' ? dlgPtUrl(C.npc) : '');
        var cc = b ? 'ok' : hide ? 'lk' : 'new', c = b ? '\u2713 Beaten' : hide ? '\ud83d\udd12' : 'NEW', cs = b ? 'rematch \u00a52\u20133' : hide ? 'beat the<br>other five' : 'win: \u00bc\u2605';
        x += '<div class="hh-r' + (b ? ' beat' : '') + (k === 'glitch' ? ' shady' : '') + '"><i class="pt" style="' + (pt ? 'background-image:url(' + pt + ')' : '') + '">' + (pt ? '' : '?') + '</i><span class="tx"><b>' + (hide ? '???' : C.n) + '</b><small>' + (hide ? 'Nobody talks about him yet' : C.where) + '</small><em>' + (hide ? 'Plays dirty' : HH_FIG[C.f]) + ' \u00b7 CPU ' + hhStarTxt(C.st) + (C.cheat ? ' + cheat' : '') + '</em></span><span class="ch ' + cc + '">' + c + '<small>' + cs + '</small></span></div>'; });
      x += '<p class="hh-note">\u2605 Gold-ringed Talk bubbles are new challengers. ' + (h.hint ? 'K\u014dno waits in the Coach\u2019s Office.' : 'The fifth student you beat tells you where the sixth one hides.') + '</p>';
    } else {
      x += '<h3 class="hh3" style="display:block">Cheat pocket<small style="display:block;margin-top:3px">Loads when the handheld starts \u00b7 one cheat per match</small></h3><div class="hh-cg">';
      x += h.cheats.dbl ? '<button type="button" class="hh-c' + (h.cOn === 'dbl' ? ' on' : '') + '" data-hh="cheat" data-v="dbl"><span class="cd">\u2191\u2191\u2193\u2193 B A</span><b>DOUBLE SHOT</b><small>Your special fires twice with no recharge. Won from Glitch K\u014dno. Tap to switch ' + (h.cOn === 'dbl' ? 'off' : 'on') + '.</small></button>'
        : '<div class="hh-c lk"><span class="cd">? ? ? ?</span><b>Locked</b><small>A shady player carries this one.</small></div>';
      x += '<div class="hh-c lk"><span class="cd">? ? ? ?</span><b>Locked</b><small>An arcade tournament prize, later</small></div><div class="hh-c lk"><span class="cd">? ? ? ?</span><b>Locked</b><small>Another shady player, somewhere in town</small></div><div class="hh-c lk"><span class="cd">? ? ? ?</span><b>Locked</b><small>The tournament finals</small></div></div>';
      x += '<div class="hh-cp"><span class="ic">VS</span><span><b>Next match: ' + HH_FIG[h.sel] + ' ' + hhStarTxt(hhStars(h.sel)) + '</b><small>Cheat: ' + (h.cOn === 'dbl' && h.cheats.dbl ? 'DOUBLE SHOT' : 'none') + '</small></span></div>';
      if (h.lead) x += '<p class="hh-note">\ud83c\udfc6 K\u014dno: real players settle it at the arcade tournament. Later. (Journal lead)</p>';
    }
    return x; }
  /* journal: the side quest + the lead */
  function hhQSteps() { var h = hhS(); return [['Talk to Sota in the Library\u2019s Silent Study', !!h.tip], ['Find the handheld on a desk in the Staff Room (Nurse\u2019s Hallway)', !!h.own], ['Challenge Sota', !!h.beat.sota]]; }
  var hhRows0 = sideRows; sideRows = function (mode) { var rows = hhRows0.apply(this, arguments) || []; try { var h = SAVE.hh || {}, on = beaten('mb_lib');
      if (mode === 'active') { if (on && !(h.beat && h.beat.sota)) rows.push({ id: 'hh_q', kind: 'side', n: 'A Game in the Staff Room', st: 'on' }); if (h.lead) rows.push({ id: 'hh_lead', kind: 'side', n: 'Lead: The Arcade Tournament', st: 'on' }); }
      else if (mode === 'done') { if (h.beat && h.beat.sota) rows.push({ id: 'hh_q', kind: 'side', n: 'A Game in the Staff Room', st: 'done' }); } } catch (e) {} return rows; };
  var hhQD0 = questDetail; questDetail = function (id) { if (id === 'hh_q') { var st = hhQSteps(), done = st[2][1]; return { id: id, kind: 'side', n: 'A Game in the Staff Room', giver: 'Arai Sota', reward: 'The Kitsune BOY handheld \u00b7 Blue Lotus', steps: st, prog: done ? 'Completed \u2014 the handheld is yours.' : '', loc: !st[0][1] ? 'Library \u00b7 Silent Study' : !st[1][1] ? 'Nurse\u2019s Hallway \u00b7 Staff Room' : 'Library \u00b7 Silent Study', story: 'Sota got his handheld confiscated. Yours is waiting in the Staff Room box.' }; }
    if (id === 'hh_lead') return { id: id, kind: 'side', n: 'Lead: The Arcade Tournament', giver: 'Glitch K\u014dno', reward: '', steps: [['Beat Glitch K\u014dno', true], ['Find the arcade tournament, later, on real cabinets', false]], prog: '', loc: 'Somewhere in town \u00b7 later', story: 'K\u014dno says real players settle it at an arcade tournament.' };
    return hhQD0.apply(this, arguments); };
  root.FFF_HH = { S: hhS, play: hhPlay, practice: hhPractice, cur: function () { return HHP; }, CH: HH_CH, ORDER: HH_ORDER, spawn: hhSpawn, tags: hhTags, talk: function (id) { var q = (W.hhS || []).filter(function (r) { return r.id === id; })[0]; hhTalk(id, q); }, ask: hhAsk, go: hhGo, pickup: hhPickup, stars: hhStars, banter: function () { return HH_BANTER; }, path: hhPath, walkUp: hhWalkUp, after: hhAfterLines, mid: hhMidLines, five: hhFive, pane: hhPane, fig: hhFigUrl };
  } catch (eHH) { try { console.warn('HH init', eHH); ev('world:hh:err:init:' + (eHH && eHH.message)); } catch (e2) {} }
})();
