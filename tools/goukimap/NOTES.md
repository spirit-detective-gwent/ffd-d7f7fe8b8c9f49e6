# v6566-goukimap — no orange Gouki pin on the nurse desk map (Erik pt535u, item 1)
Branch v6566-goukimap off c1a3b8c (live v6.5.64). Worktree /workspace/goukimap/wt. Not pushed. No version bump.

## Change (index.html)
- The desk map (#qmap, qMap()) is only used by QTALK.q_mb_cafe (nurse office after Kurata). Removed its `['@map','gouki']` step,
  so the conversation goes red X Library -> X Art -> X Cafeteria -> (Ryo's "gym sits dead center" line, no pin) -> SE storehouse circle -> off.
- qMap('gouki') kept as a no-op that just continues (any mid-flight/legacy caller still advances, draws nothing).
- Deleted the `#qmap .qmk.qg` / `::after` CSS (the orange teardrop pin). Red X (.qx) and SE circle (.qc) untouched.
- No loops, no new timers (the 600 ms wait for the pin is gone).

## Regular in-game map (pause Map tab) — checked, left alone
- No equivalent orange pin. The gym has a standard place label "🥊 Gym · Gouki" (MARKS, same style as ✚ Nurse / ⛩ Shrine).
- campusPings shows a gold "Next: Gouki" quest ping only when Gouki is the active main objective (qtMain: q_gouki active,
  or all relays done) — that's the normal next-objective ping, not the desk-map pin. Not changed.

## Tests
- tools/goukimap/test_map.py (plays the real q_mb_cafe map rows via scene()): branch 11/11 PASS; live run shows gouki qg pin present (before).
- tools/yk/ch_smoke.py PASS. verify_wired (/workspace/v6560-review/portraits) PASS.
- Shots: /workspace/goukimap/shots/before_live_desk_map(.png,_zoom.png), after_branch_desk_map(.png,_zoom.png), before_after_desk_map.png (top live, bottom branch).
- Note: the red X marks render as "+" (map is rotated; same in live and branch) — not changed.

## Release note
- v6566-goukimap (Erik pt535u): the nurse's desk map no longer drops an orange pin on Gouki's gym; red Xs and the SE storehouse circle unchanged.
