#!/usr/bin/env python3
"""tools/yk/gangs/wire.py : wire the Ch2 gang looks (v6.5.63 ch2-gangs) into index.html. Idempotent: run it again after a merge.

  python3 tools/yk/gangs/wire.py [--art /path/to/baked]     (from the repo root)

1. --art: copies baked/<spec>_<kind>.webp (tools/yk bake2.py + mkidle.py) to world/<pre>_<kind>.webp
2. strips every old sheet for these characters from index.html (ASSETS data + roster URLs, N13U_ART Sabu, embedded
   c2x_act_suit / c2x_act_boso street-act sheets), so nothing can fall back to the old models
3. (re)writes the FFF_GANGS block (between its begin/end markers) that points the game at the new world/ files
4. Jin's codex text matches his new look
Old world/, roster/, pcfig/ files for these ids are removed with git rm (see README)."""
import re, sys, os, shutil

IDS = ['bouncer', 'jin', 'masa', 'mb2_game', 'mb2_depot', 'c2_suit', 'c2_boso', 'n13sb']
KINDS = ['walk', 'run', 'hurt', 'kn', 'lie', 'map', 'fig', 'fig_hurt', 'fig_down', 'idle']
# world file prefix <- yk spec
ART = {'mb2_gameK': 'ksJin2', 'bouncerK': 'ksBouncer2', 'c2_suitK1': 'ksSuit2', 'c2_suitK2': 'ksRun2', 'n13sbK': 'sabu2',
       'mb2_depotK': 'dpMasa2', 'c2_bosoK1': 'dpRider2', 'c2_bosoK2': 'dpDock2'}
# club staff (portraits ckhostess_neutral / ckdealer_neutral): the hostess is on the Hina rig (no run / hurt / kneel / lie sheets; she never needs them)
STAFF = {'ck_hostessK': ('ckHostess', ['walk', 'map', 'fig', 'fig_hurt', 'fig_down', 'idle']), 'ck_dealerK': ('ckDealer', KINDS)}
ACT = {'c2x_act_suitK1': 'ksSuit2', 'c2x_act_suitK2': 'ksRun2', 'c2x_act_bosoK1': 'dpRider2', 'c2x_act_bosoK2': 'dpDock2'}
B0, B1 = '/* FFF_GANGS begin */', '/* FFF_GANGS end */'
ANCHOR = '/* v6.5.51 (t3039u'

BLOCK = B0 + r"""
/* v6.5.63 FFF_GANGS (ch2-gangs): the Ch2 gangs redrawn in-engine with tools/yk (specs ksJin2, ksBouncer2, ksSuit2, ksRun2, sabu2,
 * dpMasa2, dpRider2, dpDock2; matched to the dialogue portraits where there is one), baked once to world/*.webp (no run-time painting,
 * no new loops). The old sheets for these men are gone from the file, so no state can fall back to them.
 * Club Kitsune: Suit (A) and Runner (B) mixed per sprite; Depot: Rider (A) and Dock Hand (B) mixed per sprite. One man keeps one look
 * through walk / idle / act / hurt / kneel / down and into the fight (same lock as the Punks). */
(function () {
  try {
  var KS = ['walk', 'run', 'hurt', 'kn', 'lie', 'map', 'fig', 'fig_hurt', 'fig_down', 'idle'];
  function cp(a, b) { if (SHC[a] != null) SHC[b] = SHC[a]; if (typeof SHR !== 'undefined' && SHR[a] != null) SHR[b] = SHR[a]; }
  function wire(id, pre, k) { KS.forEach(function (s) { IMG[id + '_' + s] = wUrl(pre + '_' + s); cp('c2_punk_' + s, id + '_' + s); });
    SHC[id + '_walk'] = SHC[id + '_run'] = 8; SHC[id + '_idle'] = SHC[id + '_hurt'] = SHC[id + '_kn'] = 4; SHR[id + '_idle'] = 4;
    BW_IDS[id] = 1; if (k) C2K[id] = k; PT[id] = id + '_fig'; }
  /* bosses and named men: one look each */
  wire('mb2_game', 'mb2_gameK', C2K.mb2_game); wire('mb2_depot', 'mb2_depotK', C2K.mb2_depot); wire('bouncer', 'bouncerK', C2K.bouncer); wire('n13sb', 'n13sbK', 1.15);
  NM.n13sb = 'Sabu';
  /* the crews: look A under the plain id, look B under its own id */
  var GV = { c2_suit: ['c2_suit', 'c2_suitR'], c2_boso: ['c2_boso', 'c2_bosoD'] }, GW = [2, 1], GPRE = { c2_suit: 'c2_suitK1', c2_suitR: 'c2_suitK2', c2_boso: 'c2_bosoK1', c2_bosoD: 'c2_bosoK2' };
  var GACT = { c2_suit: 'c2x_act_suit', c2_suitR: 'c2x_act_suitK2', c2_boso: 'c2x_act_boso', c2_bosoD: 'c2x_act_bosoK2' };
  var GNM = { c2_suitR: 'Kitsune Runner', c2_bosoD: 'Depot Dock Hand' };
  Object.keys(GPRE).forEach(function (v) { wire(v, GPRE[v], C2K.c2_suit && /suit/.test(v) ? C2K.c2_suit : C2K.c2_boso); if (GNM[v]) NM[v] = GNM[v]; });
  IMG.c2x_act_suit = wUrl('c2x_act_suitK1'); IMG.c2x_act_suitK2 = wUrl('c2x_act_suitK2'); IMG.c2x_act_boso = wUrl('c2x_act_bosoK1'); IMG.c2x_act_bosoK2 = wUrl('c2x_act_bosoK2');
  ['c2x_act_suit', 'c2x_act_suitK2', 'c2x_act_boso', 'c2x_act_bosoK2'].forEach(function (k) { SHC[k] = 4; SHR[k] = 5; });
  var BASE = {}; ['c2_suit', 'c2_boso'].forEach(function (g) { ['fig', 'fig_hurt', 'fig_down'].forEach(function (s) { BASE[g + '_' + s] = IMG[g + '_' + s]; }); });
  /* the PC arena's hi-res figures for these men were the old models: not loaded any more */
  if (typeof PC_FIG !== 'undefined') for (var i = PC_FIG.length - 1; i >= 0; i--) if (/^(bouncer|c2_suit|c2_boso|mb2_game|mb2_depot)_fig$/.test(PC_FIG[i])) PC_FIG.splice(i, 1);
  /* one man, one look */
  var REG = [], nPick = { c2_suit: 0, c2_boso: 0 };
  function pick(g) { var r = (nPick[g]++ * 2 + 1) % (GW[0] + GW[1]); return GV[g][r < GW[0] ? 0 : 1]; }
  function lock(s, g, v) { s.gGrp = g; s.gv = v; if (v === g) return; var re = new RegExp('^' + g + '_');
    ['bw', 'sheet'].forEach(function (p) { var cur = s[p]; Object.defineProperty(s, p, { configurable: true, enumerable: true, get: function () { return cur; }, set: function (x) { cur = typeof x === 'string' ? x.replace(re, v + '_') : x; } }); s[p] = cur; }); }
  var cl0 = celLoop; celLoop = function (s, sh, row, o) { if (s && s.gv && s.gv !== s.gGrp && typeof sh === 'string') { if (sh.indexOf(s.gGrp + '_') === 0) sh = s.gv + sh.slice(s.gGrp.length); else if (sh === GACT[s.gGrp]) sh = GACT[s.gv]; } return cl0.call(this, s, sh, row, o); };
  var sprite0 = sprite; sprite = function (sheet, walker, k) { var g = !walker && /^(c2_suit|c2_boso)_map$/.test(sheet) ? sheet.slice(0, -4) : null;
    if (g) { var v = pick(g), s = sprite0.call(this, v + '_map', walker, k); lock(s, g, v); REG.push(s); if (REG.length > 40) REG = REG.filter(function (q) { return q.el && q.el.isConnected; }); return s; } return sprite0.apply(this, arguments); };
  function grpOf(id) { var m = /^(c2_suit|c2_boso)g?$/.exec(id || ''); return m ? m[1] : null; }
  function near(g, x, y, R) { var b = null, bd = R || 1e9; REG.forEach(function (q) { if (q.gGrp !== g || !q.el || !q.el.isConnected) return; var d = Math.hypot(q.x - x, q.y - y); if (d < bd) { bd = d; b = q; } }); return b; }
  var hp0 = hurtPlay; hurtPlay = function (s, id) { var g = grpOf(id); if (s && s.gv && g && s.gGrp === g) { var a = [].slice.call(arguments); a[1] = s.gv; return hp0.apply(this, a); } return hp0.apply(this, arguments); };
  var le0 = lieEl; lieEl = function (id, x, y) { var g = grpOf(id); if (g) { var q = near(g, x, y, 90), a = [].slice.call(arguments); a[0] = q ? q.gv : g; return le0.apply(this, a); } return le0.apply(this, arguments); };
  if (typeof opnFoePrep === 'function') { var fp0 = opnFoePrep; opnFoePrep = function (q) { return fp0.call(this, q && q.s && q.s.gv && q.s.gv !== q.s.gGrp ? { id: q.s.gv, s: q.s } : q); }; }
  if (typeof opnFoeShow === 'function') { var fs0 = opnFoeShow; opnFoeShow = function (q) { var a = [].slice.call(arguments); if (q && q.s && q.s.gv && q.s.gv !== q.s.gGrp) a[0] = { id: q.s.gv, s: q.s }; return fs0.apply(this, a); }; }
  /* the fight: the crew there wears the look of the man you engaged (nearest to the lead) */
  var fight1 = fight; fight = function (grp) { try { ['c2_suit', 'c2_boso'].forEach(function (g) { if (!(grp || []).some(function (c) { return grpOf(c) === g; })) return;
      var q = W.ryo ? near(g, W.ryo.x, W.ryo.y, 600) : null, v = q ? q.gv : g; ['fig', 'fig_hurt', 'fig_down'].forEach(function (s) { IMG[g + '_' + s] = v === g ? BASE[g + '_' + s] : IMG[v + '_' + s]; });
      var CH = root.ENGINE && root.ENGINE.chars && root.ENGINE.chars(); if (CH) [g, g + 'g'].forEach(function (c) { if (CH[c]) { if (!CH[c].gN0) CH[c].gN0 = CH[c].name; CH[c].name = GNM[v] || CH[c].gN0; } }); ev('world:gangs:fight:' + v); }); } catch (e) {} return fight1.apply(this, arguments); };
  /* idle-time warm-up of the crew looks (files, fetched once when the town is up; no loop) */
  var warmed = 0; function warm() { if (warmed) return; warmed = 1; var L = []; Object.keys(GPRE).forEach(function (v) { L.push(GPRE[v] + '_map', GPRE[v] + '_walk', GPRE[v] + '_idle'); }); L.push('c2x_act_suitK1', 'c2x_act_suitK2', 'c2x_act_bosoK1', 'c2x_act_bosoK2'); var i = 0;
    (function next() { if (i >= L.length) { ev('world:gangs:warm'); return; } var im = new Image(); im.decoding = 'async'; im.onload = im.onerror = function () { (root.requestIdleCallback || setTimeout)(next, root.requestIdleCallback ? { timeout: 2000 } : 120); }; im.src = wUrl(L[i++]); })(); }
  setTimeout(function () { try { if (typeof c2On === 'function' && c2On()) (root.requestIdleCallback || setTimeout)(warm, root.requestIdleCallback ? { timeout: 4000 } : 600); } catch (e) {} }, 4000);
  /* Club Kitsune staff: the Hostess (back-office pair + the coat check) and the Dealer (back-office count table + the bartender), their own
   * looks instead of the Hustler / clerk / cook stand-ins */
  wire('ck_dealer', 'ck_dealerK', C2K.c2_hustler || 1.15); NM.ck_dealer = 'Club Dealer';
  ['walk', 'map', 'fig', 'fig_hurt', 'fig_down', 'idle'].forEach(function (s) { IMG['ck_hostess_' + s] = wUrl('ck_hostessK_' + s); });
  SHC.ck_hostess_walk = 8; SHC.ck_hostess_idle = 4; SHR.ck_hostess_idle = 4; if (SHR.c2_punk_walk != null) SHR.ck_hostess_walk = SHR.c2_punk_walk; BW_IDS.ck_hostess = 1; C2K.ck_hostess = 1.08; PT.ck_hostess = 'ck_hostess_fig'; NM.ck_hostess = 'Club Hostess';
  if (typeof ckChar === 'function') { var ckc0 = ckChar; ckChar = function (id, name, base) { var r = ckc0.apply(this, arguments); try { if (id === 'ck_hostess' || id === 'ck_dealer') { var CH = root.ENGINE && root.ENGINE.chars ? root.ENGINE.chars() : null;
    if (CH) [id, id + 'g'].forEach(function (c) { if (CH[c]) { CH[c].fig = id + '_fig'; if (CH[c].art) CH[c].art = id + '_fig'; if (CH[c].alt) CH[c].alt = id + '_fig'; } }); PT[id] = id + '_fig'; } } catch (e) {} return r; }; }
  root.FFF_GANGS = { ids: Object.keys(GPRE).concat(['mb2_game', 'mb2_depot', 'bouncer', 'n13sb']), pre: GPRE, warm: warm, pick: pick };
  } catch (eG) { try { ev('world:gangs:err:init:' + (eG && eG.message)); } catch (e2) {} }
})();
""" + B1 + "\n\n"

JIN_A0 = "Neon-green bomber, headphones, two-tone hair."
JIN_A1 = "Lime zip hoodie, shaggy black hair with green tips, headphones round his neck."
JIN_D0 = "CXD.mb2_game.a = 'High-Score Jin. Desire: never lose."
JIN_D1 = "CXD.mb2_game.a = 'High-Score Jin. Lime hoodie, green-tipped shag, headphones. Desire: never lose."

SWAPS = [  # the club's stand-ins -> the club staff
    ("ckFoePut('ck2', 'c2_hustler', 500, 1420, 0);", "ckFoePut('ck2', 'ck_hostess', 500, 1420, 0);"),
    ("ckFoePut('ck2', 'c2_hustler', 150, 1252, 0); ", "ckFoePut('ck2', 'ck_hostess', 150, 1252, 0); "),
    ("ckFoePut('ck2', 'c2_hustler', 382, 1222, Math.PI / 2);", "ckFoePut('ck2', 'ck_hostess', 382, 1222, Math.PI / 2);"),
    ("ckFoePut('ck3', 'c2_hustler', 508, 1100, Math.PI / 2); ", "ckFoePut('ck3', 'ck_dealer', 508, 1100, Math.PI / 2); "),
    ("  ckFoePut('ck3', 'c2_suit', 160, 800, 0);\n  ckFoePut('ck4'", "  ckFoePut('ck3', 'c2_suit', 160, 800, 0);\n  ckFoePut('ck3', 'ck_dealer', 220, 830, 0);\n  ckFoePut('ck4'"),
    ("ckCel('npc_clerk_idle', 96, 1844, 0);", "ckCel('ck_hostess_idle', 96, 1844, 0);"),
    ("life(ckCel('npc_clerk_idle', 106, 1848, 0), 'stand');", "life(ckCel('ck_hostess_idle', 106, 1848, 0), 'stand');"),
    ("ckCel('npc_ramen_idle', 170, 172, 0);", "ckCel('ck_dealer_idle', 170, 172, 0);"),
    ("life(ckCel('npc_ramen_idle', 122, 160, 0), 'stand');", "life(ckCel('ck_dealer_idle', 122, 160, 0), 'stand');"),
]

def main():
    root = os.getcwd(); a = sys.argv[1:]
    if '--art' in a:
        src = a[a.index('--art') + 1]
        for pre, spec in ART.items():
            for k in KINDS: shutil.copyfile(os.path.join(src, f'{spec}_{k}.webp'), os.path.join(root, 'world', f'{pre}_{k}.webp'))
        for pre, (spec, ks) in STAFF.items():
            for k in ks: shutil.copyfile(os.path.join(src, f'{spec}_{k}.webp'), os.path.join(root, 'world', f'{pre}_{k}.webp'))
        for pre, spec in ACT.items(): shutil.copyfile(os.path.join(src, f'{spec}_act.webp'), os.path.join(root, 'world', f'{pre}.webp'))
    p = os.path.join(root, 'index.html'); s = open(p, encoding='utf-8').read(); n0 = len(s)
    key = r'(?:%s)_[a-z0-9_]+' % '|'.join(IDS)
    # ASSETS-style "key":"value" pairs (data: URLs and roster/ URLs), wherever they sit in a JSON object line
    pair = re.compile(r'"(%s)":"[^"]*"(,?)' % key)
    def strip_line(line):
        out = pair.sub('', line); return re.sub(r',(\s*[}\]])', r'\1', out).replace('{,', '{')
    lines = s.split('\n'); nstrip = 0
    for i, line in enumerate(lines):
        if line.startswith('window.ASSETS=') or line.startswith('root.N13U_ART = '):
            new = strip_line(line); nstrip += len(pair.findall(line)); lines[i] = new
    s = '\n'.join(lines)
    # embedded old street-act sheets
    s, nact = re.subn(r'<script type="text/plain" id="c2x_act_(?:suit|boso)-src">[^<]*</script>\n?', '', s)
    # block
    if B0 in s: s = s[:s.index(B0)] + s[s.index(B1) + len(B1):].lstrip('\n')
    assert s.count(ANCHOR) == 1, 'anchor'
    s = s.replace(ANCHOR, BLOCK + ANCHOR, 1)
    s = s.replace(JIN_A0, JIN_A1).replace(JIN_D0, JIN_D1)
    for a, b in SWAPS: s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)
    print(f'stripped {nstrip} old sheet entries, {nact} act sheets; {n0 - len(s)} bytes smaller')
    left = re.findall(r'"(%s)":"(?:data:|roster/)' % key, s)
    assert not left, left

if __name__ == '__main__': main()
