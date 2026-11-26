#!/usr/bin/env python3
# assemble FFF_S2 and inject it after NQ_END (replaceable between markers)
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
INDEX = Path(sys.argv[1] if len(sys.argv) > 1 else HERE.parent.parent / 'index.html')
mod = (HERE / 's2.js').read_text(encoding='utf8').rstrip('\n')
B = '/* S2_BEGIN v6563-seal2 */\n'
E = '\n/* S2_END */\n'
s = INDEX.read_text(encoding='utf8')
if B in s:
    i = s.index(B); j = s.index(E, i) + len(E)
    s = s[:i] + B + mod + E + s[j:]
else:
    k = '/* NQ_END */'
    assert s.count(k) == 1, 'NQ_END marker missing or doubled'
    i = s.index(k) + len(k)
    s = s[:i] + '\n' + B + mod + E + s[i:]
INDEX.write_text(s, encoding='utf8')
print('injected S2 into', INDEX, 'bytes', len(mod))
