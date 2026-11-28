#!/usr/bin/env python3
"""inject tools/hotelpull/hp.js into index.html right after the FFF_QS module (between markers; re-runnable)."""
import sys, re
p = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
src = open('tools/hotelpull/hp.js', encoding='utf-8').read().rstrip('\n')
h = open(p, encoding='utf-8').read()
A, B = '/* @@FFF_HP_BEGIN */\n', '\n/* @@FFF_HP_END */\n'
if A in h:
    i = h.index(A); j = h.index(B, i) + len(B); h = h[:i] + A + src + B + h[j:]
else:
    k = h.index("  ev('world:qs:ready');"); k = h.index('})(window);\n', k) + len('})(window);\n'); h = h[:k] + A + src + B + h[k:]
open(p, 'w', encoding='utf-8').write(h); print('ok', len(src))
