# GGD-93 Kitsune BOY handheld (branch v6566-handheld)

Build: `python3 tools/hh/inject.py index.html` (idempotent; re-injects hh.js/hh.css/hh_banter.js between
`/* HH_BEGIN v6566-handheld */ … /* HH_END */` and S2ARCFIGHT from tools/s2/s2arc_fight.js).
Art: `tools/hh/paint_staff.py` (Staff Room, hall door patch, hh_boy, Glitch portrait). Banter: `tools/hh/banter_js.py` (BANTER.md verbatim).

## Flow
- Sota tips Ryo off -> Staff Room door in the hall (opens after mb_lib) -> desk box pickup -> Menu > More > Handheld.
- Challengers (gold border + VS badge): Sota, Rin (Library Ante), Kaito (Art Music Hall), Haru (Cafeteria staff room),
  Yuto + Glitch/Kono (Coach's Office). Glitch talks only after the other five; the 5th win gives the hint.
- First win vs a challenger: +1/4 star to the fighter used, unlocks the opponent's fighter. Rematch: Y2-3.
- Glitch first win: DOUBLE SHOT cheat in the pocket + journal lead "The Arcade Tournament" (no "Chapter 2" in-world).
- Stars = 1 + floor(quarters/4), max 5; +6% dmg, +6% hp, +4% speed per star over 1.
- Save: SAVE.hh (fresh in NG+, declared in tools/ngp/ngp_test.py FRESH_OK).

## Tests
`tools/hh/hh_test.py <root> [shots]` (76 checks, shots to /workspace/handheld/shots); ngp, s2, test_shonen, verify_wired.

## Open
- BANTER.md Glitch Approach A/B mention "showers"/"stall wall"; Glitch sits in the Coach's Office here. Wired verbatim.
- Walk-in doors (incl. pre-existing d2) enter by tap, not keyboard Up.
