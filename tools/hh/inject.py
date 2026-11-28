#!/usr/bin/env python3
"""v6566-handheld: build the HH block into index.html (idempotent). Run from the repo root.
 - HH block (tools/hh/hh.js + hh_banter.js + hh.css) after the FFF_WKIT line, inside the main scope
 - S2ARCFIGHT block from tools/s2/s2arc_fight.js
 - SAVE.hh in fresh(); Glitch's portrait in PT_PAINT / PT_HAS"""
import json, re, sys
from pathlib import Path
R = Path(__file__).resolve().parents[2]; H = R / 'tools/hh'
idx = R / 'index.html'; s = idx.read_text(encoding='utf8')
mod = (H / 'hh.js').read_text(encoding='utf8').replace('/*@@BANTER@@*/', (H / 'hh_banter.js').read_text(encoding='utf8').strip())
css = (H / 'hh.css').read_text(encoding='utf8')
mod = mod.replace("'/*@@CSS@@*/'", json.dumps(re.sub(r'\n+', '\n', css).strip()))
B, E = '/* HH_BEGIN v6566-handheld */\n', '\n/* HH_END */\n'
if B in s:
    i = s.index(B); j = s.index(E, i) + len(E); s = s[:i] + s[j:]
anchor = 'root.FFF_WKIT = { table: function () { return WKIT_TABLE; }'
i = s.index(anchor); i = s.index('\n', i) + 1
s = s[:i] + B + mod.rstrip('\n') + E + s[i:]
fb, fe = '/* S2ARCFIGHT_BEGIN v6564-arcade */\n', '\n/* S2ARCFIGHT_END */\n'
i = s.index(fb) + len(fb); j = s.index(fe, i)
s = s[:i] + (R / 'tools/s2/s2arc_fight.js').read_text(encoding='utf8').rstrip('\n') + s[j:]
if 'hh: null /* v6566-handheld' not in s:
    s = s.replace('gsk: null', 'gsk: null, hh: null /* v6566-handheld: the Kitsune BOY (tools/hh/hh.js) */', 1)
if "glitch:'glitch'" not in s:
    s = s.replace("var PT_PAINT = {ryo:'ryo',", "var PT_PAINT = {glitch:'glitch',ryo:'ryo',", 1)
    s = s.replace('PT_HAS = {aoi_angry:1,', 'PT_HAS = {glitch_neutral:1,aoi_angry:1,', 1)
assert s.count(B) == 1 and "glitch:'glitch'" in s and 'hh: null /* v6566' in s
idx.write_text(s, encoding='utf8'); print('injected', len(mod), 'bytes')
