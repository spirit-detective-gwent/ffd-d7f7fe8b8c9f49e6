#!/usr/bin/env python3
"""GGD-51: the herbalist's paid Full Heal Tea goes away once a ¥40 hotel rest is reachable
(window.FFF_TEA_OFF(), set by s2p6.js). Seeds/herbs stay; free story heals (c2HealAsk(true)) stay.
Covers the base c2SumireMenu and both v630PotOffer 'Tea' buttons. Idempotent; tagged /* GGD-51 tea */."""
import sys
from pathlib import Path
INDEX = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent.parent / 'index.html')
s = INDEX.read_text(encoding='utf8')
TAG = '/* GGD-51 tea */'
if TAG in s: print('tea already patched'); sys.exit(0)
OFF = "(window.FFF_TEA_OFF && window.FFF_TEA_OFF())"
i = s.index("function c2SumireMenu() { var S = c2Cyc(), full = SAVE.hp >= MAXHP, poor = (SAVE.items | 0) < C2_TEA")
j = s.index("['Later', null]];", i) + len("['Later', null]];")
assert j - i < 900, 'sumire menu span'
s = s[:j] + " if " + OFF + " b.shift(); " + TAG + s[j:]
OLD = "if (SAVE.hp < MAXHP) b.push(['Tea \\u00b7 \\u00a5'"
n = s.count(OLD); assert n == 2, 'tea push count %d' % n
s = s.replace(OLD, "if (SAVE.hp < MAXHP && !" + OFF + ") " + TAG + " b.push(['Tea \\u00b7 \\u00a5'")
INDEX.write_text(s, encoding='utf8'); print('tea patched')
