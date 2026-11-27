#!/usr/bin/env python3
"""GGD-89 base expansion: anchored code patch.
Reads work/index_base.html (the pre-patch index.html), writes index.html.
Run: python3 tools/baseexp/patch_code.py  (from the worktree root)."""
import json, sys, re, base64, pathlib
WT = pathlib.Path(__file__).resolve().parents[2]
WORK = pathlib.Path('/workspace/baseexp/work')
SRC = WORK / 'index_base.html'
src = SRC.read_text()
rooms = json.load(open(WT / 'tools/baseexp/rooms.json'))['rooms']

def rep(old, new, cnt=1):
    global src
    n = src.count(old)
    if n != cnt:
        sys.exit('anchor count %d != %d: %r' % (n, cnt, old[:140]))
    src = src.replace(old, new)

def blocks(name):
    return '[' + ', '.join('[%d, %d, %d, %d]' % tuple(p[1]) for p in rooms[name]['props']) + ']'

OPEN = 'open: [[100, 155, 1050, 785]]'
GW = "{ r: [28, 323, 91, 562], at: [110, 450], to: '%s' }"
GE = "{ r: [1055, 330, 1125, 562], at: [1032, 450], to: '%s' }"
GN = "{ r: [506, 7, 640, 150], at: [573, 178], to: '%s' }"
GS = "{ r: [453, 800, 690, 850], at: [571, 828], land: [571, 700, 3], to: '%s' }"
def look(r, at): return "{ id: 'look', r: %s, at: %s, face: 3 }" % (json.dumps(r).replace(',', ', '), json.dumps(at).replace(',', ', '))

# ======================= CAFETERIA =======================
rep("{ id: 'counter', r: [680, 260, 970, 330], at: [825, 372], face: 3 }], crate: [300, 640], foes:",
    "{ id: 'counter', r: [680, 260, 970, 330], at: [825, 372], face: 3 }], foes:")
rep("doors: { gE: { r: [1055, 330, 1125, 562], at: [1032, 450], to: 'line:gW' } },\n    spots: [{ id: 'chute', r: [860, 160, 1000, 320], at: [930, 364], face: 3 }], crate: [220, 700], foes:",
    "doors: { gE: { r: [1055, 330, 1125, 562], at: [1032, 450], to: 'line:gW' }, gW: " + GW % 'cooler:gE' + ", gN: { r: [700, 7, 830, 150], at: [763, 178], to: 'dish:gS' } },\n    spots: [{ id: 'chute', r: [860, 160, 1000, 320], at: [930, 364], face: 3 }], foes:")
rep("doors: { gW: { r: [28, 323, 91, 562], at: [110, 450], to: 'line:gE' } },\n    spots: [{ id: 'notes'",
    "doors: { gW: { r: [28, 323, 91, 562], at: [110, 450], to: 'line:gE' }, gN: " + GN % 'bakery:gS' + " },\n    spots: [{ id: 'notes'")
rep("give: ['tape'] }, crate: [930, 420], foes: [] },", "give: ['tape'] }, foes: [] },")
newc = []
newc.append("  /* GGD-89 (v6.5.66): four more rooms. Cooler / Dock / Bakery each hold a crate and ONE room guard (CAF_GRD) who turns on a beat; the handmade props are cover.\n   * after: 1 = roamers only once the Cafeteria is cleared and refilled (never before). The Dish Room is a quiet link. */")
newc.append("  cooler: { n: 'Cafeteria \\u00b7 Walk-in Cooler', pic: [1152, 864], s: 1.0, plan: [-1, 1, 0, 2],\n    %s, block: %s,\n    doors: { gE: %s, gN: %s },\n    spots: [%s], crate: [150, 486], after: 1, foes: [[620, 470], [520, 720]] }," % (OPEN, blocks('cf_cooler'), GE % 'kitchen:gW', GN % 'dock:gS', look([700, 40, 860, 96], [780, 200])))
newc.append("  dock: { n: 'Cafeteria \\u00b7 Loading Dock', pic: [1152, 864], s: 1.0, plan: [-1, 0, 0, 1],\n    %s, block: %s,\n    doors: { gS: %s, gE: %s },\n    spots: [%s], crate: [190, 310], after: 1, foes: [[460, 720], [960, 480]] }," % (OPEN, blocks('cf_dock'), GS % 'cooler:gN', GE % 'dish:gW', look([300, 40, 480, 98], [390, 200])))
newc.append("  dish: { n: 'Cafeteria \\u00b7 Dish Room', pic: [1152, 864], s: 1.0, plan: [0, 0, 1, 1],\n    %s, block: %s,\n    doors: { gS: %s, gW: %s },\n    spots: [%s], foes: [] }," % (OPEN, blocks('cf_dish'), GS % 'kitchen:gN', GW % 'dock:gE', look([200, 34, 430, 92], [315, 290])))
newc.append("  bakery: { n: 'Cafeteria \\u00b7 Bakery', pic: [1152, 864], s: 1.0, plan: [2, 0, 3, 1],\n    %s, block: %s,\n    doors: { gS: %s },\n    spots: [%s], crate: [960, 360], after: 1, foes: [[450, 620], [700, 330]] } };" % (OPEN, blocks('cf_bakery'), GS % 'staff:gN', look([180, 34, 420, 92], [600, 300])))
rep("face: 3 }], foes: [] } };\nvar CAFP", "face: 3 }], foes: [] },\n" + '\n'.join(newc) + "\nvar CAFP")
m = re.search(r"CAF_CRATES = \[[^\]]*\]", src); assert m, 'CAF_CRATES'
rep(m.group(0), "CAF_CRATES = ['cooler', 'dock', 'bakery']")

# guard tables + generic room-guard behaviour (stand, hold, turn via the wall side, on a readable beat)
G = rooms
GRD_JS = r"""
/* ---- GGD-89 room guards (v6.5.66). One per crate room, part of the main quest only. He stands at his post next to the crate and turns
 * between two facings on a fixed beat (hold, then a slow turn through the back wall). Sight is the normal seeK/susStep (vision cone,
 * "?" then "!"), with his own NOTICE (q.N). Carrying a crate widens his reach and halves his notice time. Props block his line of sight
 * (losClear), so the room furniture is cover. Beaten or slipped past, he stays resolved: S.f['g'+room] after a win, and no guard once
 * that room's crate is in the chute. No roamers in his room until the Cafeteria is cleared (R.after). No per-frame DOM work: the cone is
 * one element, rotated by a CSS transition only when he starts a turn. */
var CAF_GRD = { cooler: { at: %COOLER%, fa: [Math.PI, 0], r: %CR%, a: %CA%, id: 'bully3' }, dock: { at: %DOCK%, fa: [Math.PI, 0], r: %DR%, a: %DA%, id: 'bully4' },
  bakery: { at: %BAK%, fa: [Math.PI, 0], r: %BR%, a: %BA%, id: 'bully3' } };
var GRD_T = { hold: 3.0, turn: 0.7, t: 0.55, carryR: 1.25, carryT: 0.5 };
(function () { var st = document.createElement('style'); st.id = 'ggd89css';
  st.textContent = '.wgcone{position:absolute;pointer-events:none;border-radius:50%;background:conic-gradient(from -46deg,rgba(255,236,150,.34) 0deg 92deg,rgba(0,0,0,0) 92deg 360deg);-webkit-mask:radial-gradient(closest-side,#000 62%,rgba(0,0,0,0) 100%);mask:radial-gradient(closest-side,#000 62%,rgba(0,0,0,0) 100%);transition:transform .7s linear,opacity .25s;will-change:transform;z-index:60}'
    + '.wgcone.sus{background:conic-gradient(from -46deg,rgba(255,120,80,.42) 0deg 92deg,rgba(0,0,0,0) 92deg 360deg)}.wgcone.off{opacity:0}'
    + '.fslotring{position:absolute;width:76px;height:34px;margin:-17px 0 0 -38px;border-radius:50%;border:3px dashed rgba(255,255,255,.0);pointer-events:none;z-index:99;opacity:0;transition:opacity .2s}'
    + '.fslotring.on{opacity:1}.fslotring.ok{border-color:#7be07b;box-shadow:0 0 10px rgba(123,224,123,.6)}.fslotring.no{border-color:#e85a5a;box-shadow:0 0 10px rgba(232,90,90,.5)}'
    + '.fkick{animation:fkick .75s cubic-bezier(.2,.6,.4,1) forwards;pointer-events:none}@keyframes fkick{0%{translate:0 0;rotate:0deg;opacity:1}60%{translate:var(--kx,-120px) -70px;rotate:-260deg;opacity:1}100%{translate:calc(var(--kx,-120px)*1.6) -20px;rotate:-400deg;opacity:0}}'
    + '.fldlap.fslow{filter:saturate(.55) brightness(.92)}.fldlap.fslow::after{content:"";position:absolute;left:50%;top:-14px;width:22px;height:22px;margin-left:-11px;border-radius:50%;background:#fff;border:2px solid #1c1622;box-shadow:inset 0 0 0 3px #6fb6e8}';
  document.head.appendChild(st); })();
function grdCone(f) { var G = f.grd, e = document.createElement('i'), R = f.N0.r; e.className = 'wgcone'; e.style.width = e.style.height = (2 * R) + 'px';
  e.style.left = (f.hx - R) + 'px'; e.style.top = (f.hy - 18 - R) + 'px'; f.cdeg = f.fa * 180 / Math.PI + 90; f.cone = e; grdConeSet(f, 0); layer.appendChild(e); W.ints.push({ el: e }); }
function grdConeSet(f, tr) { var e = f.cone; if (!e) return; e.style.transitionDuration = tr ? (tr + 's, .25s') : '0s, .25s'; e.style.transform = 'rotate(' + f.cdeg.toFixed(1) + 'deg) scale(' + (W.carry ? GRD_T.carryR : 1) + ')'; }
function grdVis(f) { var on = f.st === 'grd', sus = !!f.qm, c = f.cone; if (!c) return; if (c._on !== on) { c._on = on; c.classList.toggle('off', !on); } if (c._sus !== sus) { c._sus = sus; c.classList.toggle('sus', sus); }
  var cr = !!W.carry; if (f._cr !== cr) { f._cr = cr; f.N = cr ? f.Nc : f.N0; grdConeSet(f, GRD_T.turn); ev('world:cafe:guard:carry:' + f.key + ':' + (cr ? 1 : 0)); } }
function grdHome(f) { var G = f.grd; f.st = 'grd'; f.gi = 0; f.gT = GRD_T.hold; f.turn = null; f.fa = G.fa[0]; f.rp = null; f.sus = 0; f.qm = 0; f.s.runK = 0; f.s.x = f.hx; f.s.y = f.hy;
  f.cdeg = f.fa * 180 / Math.PI + 90; grdConeSet(f, 0); waddle(f.s, 0, f.fa); ev('world:cafe:guard:home:' + f.key); }
/* the beat: hold GRD_T.hold, then turn GRD_T.turn to the other facing, always through the back wall (north), so the swing is readable */
function grdStep(f, dt) { var G = f.grd; if (f.turn) { f.turn.t += dt; var u = Math.min(1, f.turn.t / GRD_T.turn); f.fa = f.turn.a0 + f.turn.d * u; if (u >= 1) { f.fa = G.fa[f.gi]; f.turn = null; f.gT = GRD_T.hold; ev('world:cafe:guard:face:' + f.key + ':' + f.gi); } return; }
  f.gT -= dt; if (f.gT > 0) return; var a0 = G.fa[f.gi]; f.gi = 1 - f.gi; var a1 = G.fa[f.gi], d = angD(a1, a0);
  if (Math.abs(Math.abs(d) - Math.PI) < 0.05) d = angD(-Math.PI / 2, a0) * 2; /* half-turns go via north */
  f.turn = { a0: a0, d: d, t: 0 }; f.cdeg += d * 180 / Math.PI; grdConeSet(f, GRD_T.turn); }
function grdRetTo(f) { var s = f.s; if (!f.rp) f.rp = (typeof findPath === 'function' && findPath(s.x, s.y, f.hx, f.hy)) || [[f.hx, f.hy]];
  while (f.rp.length && Math.hypot(f.rp[0][0] - s.x, f.rp[0][1] - s.y) < 4) f.rp.shift(); if (!f.rp.length) { grdHome(f); return null; } return f.rp[0]; }
function cafGuard(k, R, S, b) { var G = CAF_GRD[k]; if (!G || b || S.cr[k] === 2 || S.f['g' + k]) return null;
  var gs = intSprite(G.id + '_map', SPH, 'dgfoe'); gs.el.classList.add('foe', 'wguard'); var a = lw(R, G.at); gs.x = a[0]; gs.y = a[1]; place(gs, 0);
  var f = { key: 'g' + k, id: G.id, s: gs, hx: a[0], hy: a[1], tx: null, ty: null, st: 'grd', route: 1, stun: 0, wait: 0, grd: G, gi: 0, gT: GRD_T.hold, fa: G.fa[0],
    N0: { r: G.r * R.s, a: G.a, t: GRD_T.t }, Nc: { r: G.r * R.s * GRD_T.carryR, a: G.a, t: GRD_T.t * GRD_T.carryT } }; f.N = W.carry ? f.Nc : f.N0; f._cr = !!W.carry;
  waddle(gs, 0, f.fa); W.dgF.push(f); grdCone(f); ev('world:cafe:guard:spawn:' + k); return f; }
"""
for nm, key in (('cf_cooler', ('COOLER', 'CR', 'CA')), ('cf_dock', ('DOCK', 'DR', 'DA')), ('cf_bakery', ('BAK', 'BR', 'BA'))):
    g = rooms[nm]['guard']
    GRD_JS = GRD_JS.replace('%' + key[0] + '%', '[%d, %d]' % tuple(g['at'])).replace('%' + key[1] + '%', str(g['r'])).replace('%' + key[2] + '%', str(g['a']))
rep("function cafS() {", GRD_JS.strip('\n') + "\nfunction cafS() {")

# cafPop: R.after roamers only once refilled; the room guard
rep("(R.foes || []).forEach(function (p, i) { var key = 'c' + k + i; if (!dgShouldSpawn('cafe', 'mb_cafe')) return;",
    "(R.foes || []).forEach(function (p, i) { var key = 'c' + k + i; if (!dgShouldSpawn('cafe', 'mb_cafe')) return; if (R.after && !dgRefilled('cafe')) return; /* GGD-89: guard rooms get roamers only after the clear */")
rep("  (CAFP[k] || []).forEach(function (n) { var a = lw(R, n.at), s;", "  cafGuard(k, R, S, b);\n  (CAFP[k] || []).forEach(function (n) { var a = lw(R, n.at), s;")

# help tip, arrival lines, looks
OLD_TIP = "<p>Find the three crates of possessed bread. <b>Lift</b> one, carry it to the Kitchen\\u2019s <b>disposal chute</b>. No running with a crate, and a fight knocks it back.</p><p>The Staff Room is a <b>safe room</b>.</p>"
NEW_TIP = "<p>Find the three crates of possessed bread: the <b>Walk-in Cooler</b>, the <b>Loading Dock</b> and the <b>Bakery</b>. <b>Lift</b> one, carry it to the Kitchen\\u2019s <b>disposal chute</b>. No running with a crate, and a fight knocks it back.</p><p>Each crate has a <b>guard</b> who turns on a beat. Move while he looks away and hide behind the furniture.</p><p>The Staff Room is a <b>safe room</b>.</p>"
rep(OLD_TIP, NEW_TIP)
rep("  if (a === 'menu') { scene(null, CAF_SC.menu); return; }", "  if (a === 'look' && CAF_SC['l_' + k]) { scene(null, CAF_SC['l_' + k]); return; }\n  if (a === 'menu') { scene(null, CAF_SC.menu); return; }")
CAF_ADD = r"""  /* GGD-89 rooms */
  in_cooler: [['', '<p class="dim">The Walk-in Cooler. Breath turns white. A crate sits by the shelves, glowing through the slats.</p>'], ['aoi', 'There\u2019s a guard. Watch him turn. {slow}Move when he looks away.{/slow}', { mood: 'neutral' }], ['@tip', 'cafguard', { t: 'Room guards', h: '<p>A guard stands by each crate and turns between two sides on a steady beat. His view is the pale cone.</p><p>Shelves, crates and counters block his view. Walk while he faces away, wait behind cover while he turns back.</p><p>With a crate in your arms he sees farther and notices faster. If he spots you, it\u2019s a fight and the crate goes back.</p>' }]],
  in_dock: [['', '<p class="dim">The Loading Dock. A delivery van, back doors open. Pallets of melon bread, still warm.</p>'], ['aoi', 'Another guard. Same rhythm. Use the pallets.', { mood: 'neutral' }]],
  in_dish: [['', '<p class="dim">The Dish Room. The conveyor runs with nothing on it. Nobody\u2019s washed a tray in days.</p>']],
  in_bakery: [['', '<p class="dim">The Bakery. Both ovens roaring. Trays of melon bread cool on the racks, every one of them purple.</p>'], ['aoi', 'This is where it comes from. The crate\u2019s behind him.', { mood: 'neutral' }]],
  l_cooler: [['', '<p class="dim">KEEP CLOSED. Someone has scratched out CLOSED and written FULL.</p>']],
  l_dock: [['', '<p class="dim">DELIVERY 6:00. Every morning. Same van, same order: 500 melon bread.</p>']],
  l_dish: [['', '<p class="dim">ORDER UP. The bell under the sign is wrapped in purple tape.</p>']],
  l_bakery: [['', '<p class="dim">MELON BREAD \u00d7500. The 5 has been gone over again and again.</p>'], ['aoi', 'They\u2019re baking for the whole school.', { mood: 'neutral' }]],
  guard_lost: [['aoi', 'He\u2019s back at his post. Wait for the turn.', { mood: 'neutral' }]],
"""
rep("var CAF_SC = {\n", "var CAF_SC = {\n" + CAF_ADD)

# map
rep('<svg viewBox="-0.15 -0.1 3.3 2.2" preserveAspectRatio="xMidYMid meet" aria-label="Cafeteria floor plan">',
    '<svg viewBox="-1.15 -0.1 4.3 2.2" preserveAspectRatio="xMidYMid meet" aria-label="Cafeteria floor plan">')
rep("return S.v[k]; }).length + '/4 rooms seen \\u00b7 crates ", "return S.v[k]; }).length + '/' + Object.keys(CAFG).length + ' rooms seen \\u00b7 crates ")

# ======================= SIGHT / PATROL CORE =======================
rep("function seeK(q, tx, ty, ok, noSense) { var s = q.s, dx = tx - s.x, dy = ty - s.y, d = Math.hypot(dx, dy), N = ntc(q.id),",
    "function seeK(q, tx, ty, ok, noSense) { var s = q.s, dx = tx - s.x, dy = ty - s.y, d = Math.hypot(dx, dy), N = q.N || ntc(q.id), /* GGD-89: room guards carry their own notice */")
rep("function susStep(q, k, dt) { var N = ntc(q.id);", "function susStep(q, k, dt) { var N = q.N || ntc(q.id);")
# dgFrame: the guard beat, the return-to-post state, no head-tracking on a partial notice
rep("if (f.stun > 0) { f.stun -= dt; if (f.stun <= 0 && f.wvA && typeof waveWake === 'function') { f.wvA = 0; waveWake(f, W.dgF, okAt); } return; } if (f.ambd) return; /* v4.23: being ambushed */",
    "if (f.stun > 0) { f.stun -= dt; if (f.stun <= 0 && f.wvA && typeof waveWake === 'function') { f.wvA = 0; waveWake(f, W.dgF, okAt); } if (f.grd) grdVis(f); return; } if (f.ambd) return; /* v4.23: being ambushed */\n    if (f.grd) { if (f.st === 'grd') grdStep(f, dt); grdVis(f); } /* GGD-89 room guard beat */")
rep("groupPull(f, W.dgF, okAt); } else if (k > 0) f.fa += angD(", "groupPull(f, W.dgF, okAt); } else if (k > 0 && !f.grd) f.fa += angD(")
rep("if (f.wait <= 0) { f.sus = 0; f.qm = 0; if (f.g38m) f.st = 'g38'; else routeOn(",
    "if (f.wait <= 0) { f.sus = 0; f.qm = 0; if (f.grd) { f.st = 'ret'; f.rp = null; ev('world:cafe:guard:ret:' + f.key); } else if (f.g38m) f.st = 'g38'; else routeOn(")
rep("    else if (f.st === 'g38') { to = g38tTo(f, dt); if (f.g38sp) sp = f.g38sp; }\n    else if (f.st === 'patrol') { to = f.goal;",
    "    else if (f.st === 'g38') { to = g38tTo(f, dt); if (f.g38sp) sp = f.g38sp; }\n    else if (f.st === 'ret') { to = grdRetTo(f); }\n    else if (f.st === 'patrol') { to = f.goal;")
rep("} else { if (f.st === 'g38') { to = g38tTo(f, dt); if (f.g38sp) sp = f.g38sp; } else if (f.st === 'patrol') to = f.goal;",
    "} else { if (f.st === 'g38') { to = g38tTo(f, dt); if (f.g38sp) sp = f.g38sp; } else if (f.st === 'ret') to = grdRetTo(f); else if (f.st === 'patrol') to = f.goal;")
rep("} else if (f.st === 'patrol' || f.st === 'search') { f.st = 'scan'; f.wait = AW.lookT * 0.6; f.lk0 = f.fa; } } } // blocked",
    "} else if (f.st === 'patrol' || f.st === 'search') { f.st = 'scan'; f.wait = AW.lookT * 0.6; f.lk0 = f.fa; } else if (f.st === 'ret') { f.rp = null; } } } // blocked")
rep("if (mv > 0.3) f.fa = Math.atan2(s.y - py, s.x - px); if (on) waddle(s, mv, f.fa);",
    "if (mv > 0.3) f.fa = Math.atan2(s.y - py, s.x - px); if (on && (mv > 0 || !f.grd || f.st !== 'grd' || f.turn || !f._wd)) { waddle(s, mv, f.fa); if (f.grd) f._wd = !f.turn && f.st === 'grd'; }")

# the live sight is the v6.5.30 override (x2 reach etc.): room guards use their own notice (q.N) at the v4.23 sight numbers (SIGHT23, rk 1)
rep("seeK = function (q, tx, ty, ok, noSense) { var s = q.s, dx = tx - s.x, dy = ty - s.y, d = Math.hypot(dx, dy), N = ntc(q.id), G = sightOf(q),",
    "seeK = function (q, tx, ty, ok, noSense) { var s = q.s, dx = tx - s.x, dy = ty - s.y, d = Math.hypot(dx, dy), N = q.N || ntc(q.id), G = q.grd ? SIGHT23 : sightOf(q), /* GGD-89 room guards: own reach, x1 */")
rep("susStep = function (q, k, dt) { var N = ntc(q.id), G = sightOf(q);", "susStep = function (q, k, dt) { var N = q.N || ntc(q.id), G = q.grd ? SIGHT23 : sightOf(q);")

# ======================= STOREHOUSE =======================
rep("gE: { r: [1055, 330, 1125, 562], at: [1032, 450], to: 'coach:gW' } },\n    spots: [{ id: 'board', r: [700, 30, 980, 110], at: [840, 180], face: 3 }], hurdle: [300, 640], foes:",
    "gE: { r: [1055, 330, 1125, 562], at: [1032, 450], to: 'coach:gW' }, gW: " + GW % 'cage:gE' + " },\n    spots: [{ id: 'board', r: [700, 30, 980, 110], at: [840, 180], face: 3 }], foes:")
rep("gN: { r: [506, 7, 640, 150], at: [573, 178], to: 'track:gS' } },\n    spots: [{ id: 'lane', r: [520, 480, 630, 560], at: [575, 600], face: 3 }], hurdle: [820, 560], foes:",
    "gN: { r: [506, 7, 640, 150], at: [573, 178], to: 'track:gS' }, gW: " + GW % 'showers:gE' + ", gE: " + GE % 'trainer:gW' + " },\n    spots: [{ id: 'lane', r: [520, 480, 630, 560], at: [575, 600], face: 3 }], foes:")
rep("doors: { gW: { r: [28, 323, 91, 562], at: [110, 450], to: 'bay:gE' } },\n    spots: [{ id: 'notes', r: [160, 40, 360, 140], at: [260, 200], face: 3 }],",
    "doors: { gW: { r: [28, 323, 91, 562], at: [110, 450], to: 'bay:gE' }, gN: " + GN % 'trainer:gS' + " },\n    spots: [{ id: 'notes', r: [160, 40, 360, 140], at: [260, 200], face: 3 }],")
rep("give: ['gauze'] }, hurdle: [930, 420], foes: [] },", "give: ['gauze'] }, foes: [] },")
rep("plan: [1, -0.2, 2, 0.8],", "plan: [1, -1.1, 2, -0.1],")
rep("doors: { gS: { r: [581, 625, 694, 715], at: [637, 650], land: [637, 585, 3], to: 'lockers:gN' } },",
    "doors: { gS: { r: [581, 625, 694, 715], at: [637, 650], land: [637, 585, 3], to: 'lockers:gN' }, gE: { r: [1205, 380, 1265, 510], at: [1180, 445], to: 'booth:gW' } },")
newf = []
newf.append("  /* GGD-89 (v6.5.66): four more rooms. The hurdles now live in the Cage / Showers / Trainer; the Timing Booth lever slows Bando for one lap. */")
newf.append("  cage: { n: 'Storehouse \\u00b7 Equipment Cage', pic: [1152, 864], s: 1.0, plan: [0, 1, 1, 2],\n    %s, block: %s,\n    doors: { gE: %s },\n    spots: [%s], hurdle: [300, 560], kick: { showers: [520, 600], trainer: [740, 600] }, foes: [] }," % (OPEN, blocks('sf_cage'), GE % 'bay:gW', look([120, 40, 290, 96], [300, 180])))
newf.append("  showers: { n: 'Storehouse \\u00b7 Showers', pic: [1152, 864], s: 1.0, plan: [0, 0, 1, 1],\n    %s, block: %s,\n    doors: { gE: %s },\n    spots: [%s], hurdle: [870, 650], foes: [] }," % (OPEN, blocks('sf_showers'), GE % 'lockers:gW', look([140, 20, 760, 150], [450, 200])))
newf.append("  trainer: { n: 'Storehouse \\u00b7 Trainer\\u2019s Room', pic: [1152, 864], s: 1.0, plan: [2, 0, 3, 1],\n    %s, block: %s,\n    doors: { gW: %s, gS: %s },\n    spots: [%s], hurdle: [800, 680], foes: [] }," % (OPEN, blocks('sf_trainer'), GW % 'lockers:gE', GS % 'coach:gN', look([180, 36, 400, 92], [350, 180])))
newf.append("  booth: { n: 'Storehouse \\u00b7 Timing Booth', pic: [1152, 864], s: 1.0, plan: [2, -1.1, 3, -0.1],\n    %s, block: %s,\n    doors: { gW: %s },\n    spots: [%s, { id: 'lever', r: [920, 70, 1000, 150], at: [960, 210], face: 3 }], foes: [] } };" % (OPEN, blocks('sf_booth'), GW % 'track:gE', look([300, 18, 850, 140], [575, 310])))
rep("{ id: 'slot2', r: [970, 350, 1030, 410], at: [1000, 430], face: 3 }], foes: [] } };",
    "{ id: 'slot2', r: [970, 350, 1030, 410], at: [1000, 430], face: 3 }], foes: [] },\n" + '\n'.join(newf))
rep("FLD_HURDLES = ['bay', 'lockers', 'coach']", "FLD_HURDLES = ['cage', 'showers', 'trainer']")
# kicked-hurdle pick-up spots in the Cage
rep("  if (R.hurdle) { var c = R.hurdle; spots.push({ id: 'hurdle', r: lr(R, [c[0] - 36, c[1] - 48, c[0] + 36, c[1] + 8]), at: lw(R, [c[0], c[1] + 40]), face: 3 }); }",
    "  if (R.hurdle) { var c = R.hurdle; spots.push({ id: 'hurdle', r: lr(R, [c[0] - 36, c[1] - 48, c[0] + 36, c[1] + 8]), at: lw(R, [c[0], c[1] + 40]), face: 3 }); }\n  Object.keys(R.kick || {}).forEach(function (h) { var c = R.kick[h]; spots.push({ id: 'hk_' + h, r: lr(R, [c[0] - 36, c[1] - 48, c[0] + 36, c[1] + 8]), at: lw(R, [c[0], c[1] + 40]), face: 3 }); });")
rep("function fldS() { var o = dgS('field'); ['e', 'v', 'vm', 'kit', 'hr', 'sl', 'f']", "function fldS() { var o = dgS('field'); ['e', 'v', 'vm', 'kit', 'hr', 'sl', 'f', 'kick']")
rep("  if (R.hurdle && !S.hr[k] && !beaten('mb_field')) { var c = R.hurdle; out.push(lr(R, [c[0] - 28, c[1] - 20, c[0] + 28, c[1] + 6])); }",
    "  if (R.hurdle && !S.hr[k] && !S.kick[k] && !beaten('mb_field')) { var c = R.hurdle; out.push(lr(R, [c[0] - 28, c[1] - 20, c[0] + 28, c[1] + 6])); }\n  Object.keys(R.kick || {}).forEach(function (h) { if (S.kick[h] && !S.hr[h] && !beaten('mb_field')) { var c = R.kick[h]; out.push(lr(R, [c[0] - 28, c[1] - 20, c[0] + 28, c[1] + 6])); } });")
# fldPop: hurdle props (own + kicked into the cage), lever-armed slow lap, slot rings
rep("place(s, 0); W.fldLap = { s: s, t: 0, cx: lw(R, [640, 380])[0], cy: lw(R, [640, 380])[1], rx: 360 * R.s, ry: 160 * R.s, keep: fldOpen() ? 1 : 0 }; W.libN.bando = s; }",
    "place(s, 0); W.fldLap = { s: s, t: 0, cx: lw(R, [640, 380])[0], cy: lw(R, [640, 380])[1], rx: 360 * R.s, ry: 160 * R.s, keep: fldOpen() ? 1 : 0 }; W.libN.bando = s;\n      if (S.e.slowArm && !fldOpen()) { S.e.slowArm = 0; save(); W.fldLap.slowTo = 1; s.el.classList.add('fslow'); ev('world:field:slow:start'); } fldRings(); }")
rep("  if (R.hurdle && !S.hr[k] && !b) { var c = lw(R, R.hurdle); W.fldHr = libProp('sf_hurdle', c[0], c[1], 56, 42, 'fhurdle'); }",
    "  if (R.hurdle && !S.hr[k] && !S.kick[k] && !b) { var c = lw(R, R.hurdle); W.fldHr = libProp('sf_hurdle', c[0], c[1], 56, 42, 'fhurdle'); }\n  W.fldHk = {}; Object.keys(R.kick || {}).forEach(function (h) { if (S.kick[h] && !S.hr[h] && !b) { var c = lw(R, R.kick[h]); W.fldHk[h] = libProp('sf_hurdle', c[0], c[1], 56, 42, 'fhurdle'); } });")
# lift / drop / place
rep("function fldLift(k) { var S = fldS(); if (W.carry) {", "function fldLift(k, from) { var S = fldS(); if (W.carry) {")
rep("if (S.hr[k]) return; S.hr[k] = 1; W.carry = 'h:' + k; W.run = false; save(); fldRegrid(k);\n  if (W.fldHr) { W.fldHr.el.remove(); W.fldHr = null; }",
    "if (S.hr[k]) return; S.hr[k] = 1; W.carry = 'h:' + k; W.run = false; save(); fldRegrid(fldRoom() || k);\n  if (from === 'cage') { if (W.fldHk && W.fldHk[k]) { W.fldHk[k].el.remove(); W.fldHk[k] = null; } } else if (W.fldHr) { W.fldHr.el.remove(); W.fldHr = null; }")
rep("  if (fldRoom() === id) { fldRegrid(id); var R = FLDG[id], c = lw(R, R.hurdle); if (!W.fldHr) W.fldHr = libProp('sf_hurdle', c[0], c[1], 56, 42, 'fhurdle'); }\n  if (why === 'fight') if (typeof comment === 'function') comment([['aoi', 'It skidded away. Back where we found it (' + FLDG[id].n.replace(/^Storehouse \\u00b7 /, '') + ').']]); else toast('The hurdle skidded away. Back where you found it (' + FLDG[id].n.replace(/^Storehouse \\u00b7 /, '') + ').'); }",
    "  var hm = fldHome(id); if (fldRoom() === hm) { fldRegrid(hm); if (hm === id) { var R = FLDG[id], c = lw(R, R.hurdle); if (!W.fldHr) W.fldHr = libProp('sf_hurdle', c[0], c[1], 56, 42, 'fhurdle'); } else { var c2 = lw(FLDG.cage, FLDG.cage.kick[id]); W.fldHk = W.fldHk || {}; if (!W.fldHk[id]) W.fldHk[id] = libProp('sf_hurdle', c2[0], c2[1], 56, 42, 'fhurdle'); } }\n  if (why === 'fight') if (typeof comment === 'function') comment([['aoi', 'It skidded away. Back where we found it (' + FLDG[hm].n.replace(/^Storehouse \\u00b7 /, '') + ').']]); else toast('The hurdle skidded away. Back where you found it (' + FLDG[hm].n.replace(/^Storehouse \\u00b7 /, '') + ').'); }\n/* GGD-89: a hurdle Bando kicked lives in the Equipment Cage from then on */\nfunction fldHome(id) { return fldS().kick[id] ? 'cage' : id; }")
rep("if (S.sl[slot]) { if (typeof sayKey === 'function') sayKey('hint', 'hurdle_set'); else toast('Already set.'); return; }\n  S.sl[slot] = 1;",
    "if (S.sl[slot]) { if (typeof sayKey === 'function') sayKey('hint', 'hurdle_set'); else toast('Already set.'); return; }\n  if (!fldFeeOk(slot)) { fldKick(slot, k.slice(2)); return; } /* GGD-89 lane fee: only while he is on the far side */\n  S.sl[slot] = 1;")
rep("['aoi', 'Two more marks. Then he has nowhere to run.', { mood: 'neutral' }]]); }", "['aoi', 'One more mark. Then he has nowhere to run.', { mood: 'neutral' }]]); }")

FEE_JS = r"""
/* ---- GGD-89 Lane fee (v6.5.66). A hurdle may only be set while Bando is on the far side of the oval. Set it while he is near and he
 * kicks it back to the Equipment Cage (one-shot CSS flight, no loop). The Timing Booth lever (one use) slows his next lap: the lap rate
 * in fldFrame is scaled, nothing else runs. Slot rings show ok / not now only while a hurdle is carried, updated inside the lap block. */
var FLD_FEE = { near: 100, slow: 0.45 };
function fldSlotAng(id) { var R = FLDG.track, sp = (R.spots || []).find(function (q) { return q.id === id; }), lap = W.fldLap; if (!sp || !lap) return 0;
  var c = lw(R, [(sp.r[0] + sp.r[2]) / 2, (sp.r[1] + sp.r[3]) / 2]); return Math.atan2((c[1] - lap.cy) / (lap.ry * 0.85), (c[0] - lap.cx) / lap.rx); }
function fldFeeOk(id) { var lap = W.fldLap; if (!lap || !lap.s || lap.postBond || W.fldCine || fldOpen() || beaten('mb_field')) return true;
  return Math.abs(angD(lap.t * Math.PI * 2, fldSlotAng(id))) * 180 / Math.PI >= FLD_FEE.near; }
function fldRings() { W.fldRing = []; if (fldRoom() !== 'track' || !W.fldLap) return; var R = FLDG.track, S = fldS();
  FLD_SLOTS.forEach(function (id) { if (S.sl[id]) return; var sp = (R.spots || []).find(function (q) { return q.id === id; }); if (!sp) return; var c = lw(R, [(sp.r[0] + sp.r[2]) / 2, (sp.r[1] + sp.r[3]) / 2 + 20]);
    var e = document.createElement('i'); e.className = 'fslotring'; e.style.left = c[0] + 'px'; e.style.top = c[1] + 'px'; layer.appendChild(e); W.ints.push({ el: e }); W.fldRing.push({ id: id, el: e, st: '' }); }); }
function fldRingTick() { var R = W.fldRing; if (!R || !R.length) return; var S = fldS(), hc = W.carry && String(W.carry).indexOf('h:') === 0;
  for (var i = 0; i < R.length; i++) { var q = R[i], st = !hc || S.sl[q.id] ? '' : fldFeeOk(q.id) ? 'ok' : 'no'; if (q.st !== st) { q.st = st; q.el.className = 'fslotring' + (st ? ' on ' + st : ''); } } }
function fldKick(slot, id) { var S = fldS(), lap = W.fldLap, first = !S.e.kick; S.hr[id] = 0; if (id !== 'cage') S.kick[id] = 1; W.carry = null; if (first) S.e.kick = 1; save(); fldCarryEl(); fldRegrid('track');
  AU.play('hit', { gain: 0.55 }); ev('world:field:kick:' + slot + ':' + id);
  var R = FLDG.track, sp = (R.spots || []).find(function (q) { return q.id === slot; }), c = lw(R, [(sp.r[0] + sp.r[2]) / 2, (sp.r[1] + sp.r[3]) / 2 + 20]);
  var p = libProp('sf_hurdle', c[0], c[1], 56, 42, 'fhurdle fkick'); if (p && p.el) { p.el.style.setProperty('--kx', (c[0] > lap.cx ? 1 : -1) * 140 + 'px'); setTimeout(function () { if (p.el) p.el.remove(); }, 800); }
  if (lap && lap.s && typeof bubbleOn === 'function') bubbleOn(lap.s, '!');
  if (typeof tagsBuild === 'function') tagsBuild();
  if (first) scene(null, FLD_SC.kick); else comment(FLD_SC.kick2); }
function fldLever() { var S = fldS(); if (beaten('mb_field') || fldOpen()) { scene(null, FLD_SC.lever_done); return; } if (S.e.lever) { comment(FLD_SC.lever_used); return; }
  S.e.lever = 1; S.e.slowArm = 1; save(); AU.play('place', { gain: 0.8 }); ev('world:field:lever'); if (typeof tagsBuild === 'function') tagsBuild(); scene(null, FLD_SC.lever); }
"""
rep("/* v4.70 Hold #10: a set hurdle stands on its lane mark at once", FEE_JS.strip('\n') + "\n/* v4.70 Hold #10: a set hurdle stands on its lane mark at once")
# fldFrame: lap-rate scale for the slowed lap, slot rings inside the lap block
rep("    lap.t += (dt || 0.016) * 0.38; var ang = lap.t * Math.PI * 2;",
    "    lap.t += (dt || 0.016) * 0.38 * (lap.slowTo != null ? FLD_FEE.slow : 1); if (lap.slowTo != null && lap.t >= lap.slowTo) { lap.slowTo = null; lap.s.el.classList.remove('fslow'); ev('world:field:slow:end'); } var ang = lap.t * Math.PI * 2; fldRingTick();")
# tags / acts / sig
rep("    if (s.id === 'hurdle' && (S.hr[k] || b || W.carry)) return;",
    "    if (s.id === 'hurdle' && (S.hr[k] || S.kick[k] || b || W.carry)) return;\n    if (/^hk_/.test(s.id)) { var hid = s.id.slice(3); if (!S.kick[hid] || S.hr[hid] || b || W.carry) return; out.push({ key: id + ':' + s.id, lab: 'Lift', x: (s.r[0] + s.r[2]) / 2, y: s.r[1] - 4, below: false, ax: s.at[0], ay: s.at[1], R: LIB_OBJ_R, obj: s.r, act: { int: s.id, face: s.face, id: 'int:' + s.id } }); return; }\n    if (s.id === 'lever' && (b || S.e.lever)) return;")
rep(": s.id === 'hurdle' ? 'Lift' : s.id === 'warm' ? 'Warm-up' : 'Look', x:", ": s.id === 'hurdle' ? 'Lift' : s.id === 'warm' ? 'Warm-up' : s.id === 'lever' ? 'Pull' : 'Look', x:")
rep("return ':field' + fldDone() + (W.carry || '-') + JSON.stringify(S.sl) +", "return ':field' + fldDone() + (W.carry || '-') + JSON.stringify(S.sl) + JSON.stringify(S.kick) + (S.e.lever ? 'L' : '') +")
rep("  if (a === 'hurdle') { fldLift(k); return; }", "  if (a === 'hurdle') { fldLift(k); return; } if (/^hk_/.test(a)) { fldLift(a.slice(3), 'cage'); return; } if (a === 'lever') { fldLever(); return; } if (a === 'look' && FLD_SC['l_' + k]) { scene(null, FLD_SC['l_' + k]); return; }")
OLD_FT = "<p>Find three <b>hurdles</b>. Lift one, carry it to a <b>lane mark</b> on the track. No running; a fight knocks it back.</p><p>The Coach\\u2019s Office is a <b>safe room</b>.</p>"
NEW_FT = "<p>Find three <b>hurdles</b>: the <b>Equipment Cage</b>, the <b>Showers</b> and the <b>Trainer\\u2019s Room</b>. Lift one, carry it to a <b>lane mark</b> on the track. No running; a fight knocks it back.</p><p>Set a hurdle only while Bando is on the <b>far side</b> of the oval, or he kicks it back to the Cage. The <b>Timing Booth</b> lever slows him for one lap.</p><p>The Coach\\u2019s Office is a <b>safe room</b>.</p>"
rep(OLD_FT, NEW_FT, 2)
rep('<svg viewBox="-0.15 -0.3 3.3 2.6" preserveAspectRatio="xMidYMid meet" aria-label="Sports Storehouse floor plan">',
    '<svg viewBox="-0.15 -1.25 3.3 3.4" preserveAspectRatio="xMidYMid meet" aria-label="Sports Storehouse floor plan">')
rep("return S.v[k]; }).length + '/4 rooms seen \\u00b7 hurdles ", "return S.v[k]; }).length + '/' + Object.keys(FLDG).length + ' rooms seen \\u00b7 hurdles ")
FLD_ADD = r"""  /* GGD-89 rooms */
  in_cage: [['', '<p class="dim">The Equipment Cage. Balls everywhere. One hurdle stands apart, humming.</p>']],
  in_showers: [['', '<p class="dim">The Showers. Every tap running cold. Wet footprints go round and round the drain.</p>']],
  in_trainer: [['', '<p class="dim">The Trainer\u2019s Room. Ice baths, long melted. Tape torn off in a hurry.</p>']],
  in_booth: [['', '<p class="dim">The Timing Booth. The lap clock is a blur. Below the window, a lever: TRACK SPEED.</p>'], ['aoi', 'If he slows down, even for a lap, we can work with that.', { mood: 'neutral' }]],
  l_cage: [['', '<p class="dim">SIGN OUT GEAR. Every line says BANDO.</p>']],
  l_showers: [['', '<p class="dim">Four stalls. Every tap open. The drain gurgles in time with his steps.</p>']],
  l_trainer: [['', '<p class="dim">ICE 10 MIN. Somebody wrote under it: NO TIME.</p>']],
  l_booth: [['', '<p class="dim">Through the glass, the oval. A red blur, round and round. The lap clock can\u2019t keep up.</p>']],
  lever: [['', '<p class="dim">The lever clunks down. Out on the track, a buzzer. The next lap will be slow.</p>'], ['aoi', 'One lap, Kazan. Make it count.', { mood: 'neutral' }]],
  lever_used: [['ryo', 'It\u2019s stuck. One pull was all it had.', { mood: 'neutral' }]],
  lever_done: [['', '<p class="dim">The lever is down. The track is quiet anyway.</p>']],
  kick: [['', '<p class="dim">He is on you in a breath. One kick, and the hurdle cartwheels off the lane.</p>'], ['bando', '{fast}Not in my lane, rookie.{/fast}', { mood: 'angry' }], ['', '<p class="dim">It clatters away toward the Equipment Cage.</p>'], ['aoi', 'Wait till he\u2019s on the far side. {slow}Then set it.{/slow}', { mood: 'neutral' }]],
  kick2: [['aoi', 'Too close. It\u2019s back in the Cage.', { mood: 'neutral' }]],
"""
rep("var FLD_SC = {\n", "var FLD_SC = {\n" + FLD_ADD)
rep("  in_bay: [['', '<p class=\"dim\">Mats. Hurdles. A ball cart still rolling by itself.</p>'], ['aoi', 'Do not chase him. Whatever you do.', { mood: 'neutral' }]],",
    "  in_bay: [['', '<p class=\"dim\">Mats. Hurdle racks, empty. A ball cart still rolling by itself.</p>'], ['aoi', 'Do not chase him. Whatever you do.', { mood: 'neutral' }]],")

# ======================= CARRY RECOVERY (old saves must not crash) =======================
m = re.search(r"function carryRecover\(\) \{", src); assert m, 'carryRecover'
rep("function carryRecover() {", "function carryRecover() { /* GGD-89: a carry from an older room layout is dropped (fresh playthrough expected) */ try { var cq = SAVE.carry; if (cq && typeof cq === 'string') { if (/^h:/.test(cq) && FLD_HURDLES.indexOf(cq.slice(2)) < 0) SAVE.carry = null; else if (!/^h:|:/.test(cq) && typeof CAFG !== 'undefined' && CAFG[cq] && CAF_CRATES.indexOf(cq) < 0) SAVE.carry = null; } } catch (eCq) {}")

# ======================= SUPPLIES =======================
m = re.search(r"var SUP_PAIRS = \d+", src); assert m, 'SUP_PAIRS'
rep(m.group(0), "var SUP_PAIRS = 9")
m = re.search(r"SUP_PIN = \{[^}]*\}", src); assert m, 'SUP_PIN'
print('old pin:', m.group(0))
rep(m.group(0), "SUP_PIN = { lib: 3, gym: 1, art: 1, caf: 2, fld: 2 }")

# ======================= WALL KITS for the 8 new rooms (clone cf_kitchen's back-wall entry) =======================
i = src.index('var WKIT_TABLE = '); j = src.index('\n', i); line = src[i:j]
T = json.loads(line[len('var WKIT_TABLE = '):].rstrip(';'))
base = [w for w in T['wall'] if w['id'] == 'cf_kitchen'][0]
NAMES = {'cf_cooler': 'Cafeteria \\u00b7 Walk-in Cooler', 'cf_dock': 'Cafeteria \\u00b7 Loading Dock', 'cf_dish': 'Cafeteria \\u00b7 Dish Room', 'cf_bakery': 'Cafeteria \\u00b7 Bakery',
         'sf_cage': 'Storehouse \\u00b7 Equipment Cage', 'sf_showers': 'Storehouse \\u00b7 Showers', 'sf_trainer': 'Storehouse \\u00b7 Trainer\\u2019s Room', 'sf_booth': 'Storehouse \\u00b7 Timing Booth'}
STAND = {'sf_cage': [230.0, 182.0], 'sf_trainer': [835.0, 200.0]}
have = {w['id'] for w in T['wall']}
for rid, nm in NAMES.items():
    if rid in have: continue
    kx = float(rooms[rid]['kit_x']); w = json.loads(json.dumps(base))
    w['id'] = rid; w['key'] = rid[3:]; w['go'] = 'caf' if rid.startswith('cf_') else 'fld'; w['n'] = nm
    w['kit'] = [kx, 134.0]; w['stand'] = STAND.get(rid, [kx, 194.0]); w['attach_pic'] = [kx, 134.0]
    for st in w['states'].values():
        st['pic'] = [kx - 30.0, 91.0]; st['world'] = [kx - 30.0, 91.0]; st['attach_pic'] = [kx, 134.0]
    T['wall'].append(w)
new = 'var WKIT_TABLE = ' + json.dumps(T, separators=(',', ':')) + (';' if line.endswith(';') else '')
src = src[:i] + new + src[j:]
# risk-room guarantee
rep("    for (k = 0; k < need.length && k < slots.length; k++) lay[slots[k]] = need[k];\n  });\n  return lay;",
    "    for (k = 0; k < need.length && k < slots.length; k++) lay[slots[k]] = need[k];\n"
    "    /* GGD-89: at least one piece sits in a guarded / patrolled room */\n"
    "    var RK = SUP_RISK[fac], laid = slots.slice(0, Math.min(need.length, slots.length));\n"
    "    if (RK && laid.length && !laid.some(function (c) { return RK.indexOf(c) >= 0; })) { var alt = slots.slice(laid.length).filter(function (c) { return RK.indexOf(c) >= 0; })[0], mv = laid.filter(function (c) { return f[2].indexOf(c) < 0; })[0]; if (alt && mv) { lay[alt] = lay[mv]; delete lay[mv]; } }\n"
    "  });\n  return lay;")
rep("var SUP_PIN = { lib: 3, gym: 1, art: 1, caf: 2, fld: 2 };", "var SUP_PIN = { lib: 3, gym: 1, art: 1, caf: 2, fld: 2 }; /* GGD-89 (Erik t547u): Cafeteria and Storehouse grew to 8 rooms; each yields 2 kits (9 pairs) */\nvar SUP_RISK = { caf: ['cf_cooler', 'cf_dock', 'cf_bakery'], fld: ['sf_bay', 'sf_lockers'] };")
# re-embed the baked wall-kit backgrounds that gained doors
for rid in ('cf_kitchen', 'sf_bay', 'sf_lockers', 'sf_track'):
    f = WORK / ('wkitbg_' + rid + '_new.webp')
    a = "IMG['wkitbg_" + rid + "'] = 'data:image/webp;base64,"
    i = src.index(a) + len(a); j = src.index("'", i)
    src = src[:i] + base64.b64encode(f.read_bytes()).decode() + src[j:]

open(WT / 'index.html', 'w').write(src)
print('patched ok', len(src))
