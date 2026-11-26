#!/usr/bin/env python3
# assemble FFF_S2P (c2bt helpers + paint) and FFF_S2 and inject them after NQ_END
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
INDEX = Path(sys.argv[1] if len(sys.argv) > 1 else HERE.parent.parent / 'index.html')
paint = (HERE / 'c2bt_lib.js').read_text(encoding='utf8').rstrip('\n') + '\n' + (HERE / 'paint.js').read_text(encoding='utf8').rstrip('\n')
p2p = HERE / 'paint_p2.js'
if p2p.exists():
    paint = paint + '\n' + p2p.read_text(encoding='utf8').rstrip('\n')
p3p = HERE / 'paint_p3.js'
if p3p.exists():
    paint = paint + '\n' + p3p.read_text(encoding='utf8').rstrip('\n')
p4p = HERE / 'paint_p4.js'
if p4p.exists():
    paint = paint + '\n' + p4p.read_text(encoding='utf8').rstrip('\n')
p5p = HERE / 'paint_p5.js'
if p5p.exists():
    paint = paint + '\n' + p5p.read_text(encoding='utf8').rstrip('\n')
pmp = HERE / 'paint_menus.js'
if pmp.exists():
    paint = paint + '\n' + pmp.read_text(encoding='utf8').rstrip('\n')
mod = (HERE / 's2.js').read_text(encoding='utf8').rstrip('\n')
BP, EP = '/* S2P_BEGIN v6563-seal2 */\n', '\n/* S2P_END */\n'
B, E = '/* S2_BEGIN v6563-seal2 */\n', '\n/* S2_END */\n'
s = INDEX.read_text(encoding='utf8')
# paint first (helpers + FFF_S2P), then S2 which hooks it
if BP in s:
    i = s.index(BP); j = s.index(EP, i) + len(EP)
    s = s[:i] + BP + paint + EP + s[j:]
elif B in s:
    i = s.index(B)
    s = s[:i] + BP + paint + EP + s[i:]
else:
    k = '/* NQ_END */'
    assert s.count(k) == 1, 'NQ_END marker missing or doubled'
    i = s.index(k) + len(k)
    s = s[:i] + '\n' + BP + paint + EP + s[i:]
if B in s:
    i = s.index(B); j = s.index(E, i) + len(E)
    s = s[:i] + B + mod + E + s[j:]
else:
    k = '/* NQ_END */'
    assert s.count(k) == 1, 'NQ_END marker missing or doubled'
    i = s.index(k) + len(k)
    # if we just inserted S2P, place S2 after S2P_END
    if EP in s[i:i+len(BP)+len(paint)+len(EP)+8]:
        i = s.index(EP, i) + len(EP)
    s = s[:i] + B + mod + E + s[i:]

# Phase 2 Night Runs, after S2
p2 = HERE / 's2p2.js'
B2, E2 = '/* S2P2_BEGIN v6563-seal2-p2 */\n', '\n/* S2P2_END */\n'
if p2.exists():
    mod2 = p2.read_text(encoding='utf8').rstrip('\n')
    if B2 in s:
        i = s.index(B2); j = s.index(E2, i) + len(E2)
        s = s[:i] + B2 + mod2 + E2 + s[j:]
    elif E in s:
        i = s.index(E) + len(E)
        s = s[:i] + B2 + mod2 + E2 + s[i:]
    else:
        raise SystemExit('S2_END missing; cannot inject S2P2')
    print('injected S2P2', len(mod2))

# Phase 3 Above the Boat, after S2P2
p3 = HERE / 's2p3.js'
B3, E3 = '/* S2P3_BEGIN v6563-seal2-p3 */\n', '\n/* S2P3_END */\n'
if p3.exists():
    mod3 = p3.read_text(encoding='utf8').rstrip('\n')
    if B3 in s:
        i = s.index(B3); j = s.index(E3, i) + len(E3)
        s = s[:i] + B3 + mod3 + E3 + s[j:]
    elif E2 in s:
        i = s.index(E2) + len(E2)
        s = s[:i] + B3 + mod3 + E3 + s[i:]
    else:
        raise SystemExit('S2P2_END missing; cannot inject S2P3')
    print('injected S2P3', len(mod3))

# Phase 4 Off Schedule, after S2P3
p4 = HERE / 's2p4.js'
B4, E4 = '/* S2P4_BEGIN v6563-seal2-p4 */\n', '\n/* S2P4_END */\n'
if p4.exists():
    mod4 = p4.read_text(encoding='utf8').rstrip('\n')
    if B4 in s:
        i = s.index(B4); j = s.index(E4, i) + len(E4)
        s = s[:i] + B4 + mod4 + E4 + s[j:]
    elif E3 in s:
        i = s.index(E3) + len(E3)
        s = s[:i] + B4 + mod4 + E4 + s[i:]
    else:
        raise SystemExit('S2P3_END missing; cannot inject S2P4')
    print('injected S2P4', len(mod4))

# Phase 5 Masa's Seal, after S2P4
p5 = HERE / 's2p5.js'
B5, E5 = '/* S2P5_BEGIN v6563-seal2-p5 */\n', '\n/* S2P5_END */\n'
if p5.exists():
    mod5 = p5.read_text(encoding='utf8').rstrip('\n')
    if B5 in s:
        i = s.index(B5); j = s.index(E5, i) + len(E5)
        s = s[:i] + B5 + mod5 + E5 + s[j:]
    elif E4 in s:
        i = s.index(E4) + len(E4)
        s = s[:i] + B5 + mod5 + E5 + s[i:]
    else:
        raise SystemExit('S2P4_END missing; cannot inject S2P5')
    print('injected S2P5', len(mod5))

# Themed shop menus (Chiyo, Hase, depot art/data). After S2P5.
pm = HERE / 's2menus.js'
BM, EM = '/* S2MENUS_BEGIN v6563-shopmenus */\n', '\n/* S2MENUS_END */\n'
if pm.exists():
    modm = pm.read_text(encoding='utf8').rstrip('\n')
    if BM in s:
        i = s.index(BM); j = s.index(EM, i) + len(EM)
        s = s[:i] + BM + modm + EM + s[j:]
    elif E5 in s:
        i = s.index(E5) + len(E5)
        s = s[:i] + BM + modm + EM + s[i:]
    else:
        raise SystemExit('S2P5_END missing; cannot inject S2MENUS')
    print('injected S2MENUS', len(modm))

INDEX.write_text(s, encoding='utf8')
print('injected S2P+S2 into', INDEX, 'paint', len(paint), 's2', len(mod))
