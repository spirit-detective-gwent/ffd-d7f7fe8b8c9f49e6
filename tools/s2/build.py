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

INDEX.write_text(s, encoding='utf8')
print('injected S2P+S2 into', INDEX, 'paint', len(paint), 's2', len(mod))
