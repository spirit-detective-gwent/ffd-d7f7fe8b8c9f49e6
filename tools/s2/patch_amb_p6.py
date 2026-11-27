#!/usr/bin/env python3
"""GGD-51: let C2AMB read extra room grades from root.FFF_AMB_X (seal-3 interiors: no rain, own light pools).
Idempotent; tagged /* GGD-51 amb */."""
import sys
from pathlib import Path
INDEX = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent.parent / 'index.html')
s = INDEX.read_text(encoding='utf8')
TAG = '/* GGD-51 amb */'
if TAG in s: print('amb already patched'); sys.exit(0)
OLD = "    var g = GRADE[rm] || GRADE.town;\n    if (cv.style.display === 'none') cv.style.display = '';"
assert s.count(OLD) == 1, 'amb grade line'
s = s.replace(OLD, "    var g = GRADE[rm] || (root.FFF_AMB_X && root.FFF_AMB_X[rm]) || GRADE.town; " + TAG + "\n    if (cv.style.display === 'none') cv.style.display = '';")
INDEX.write_text(s, encoding='utf8'); print('amb patched')
