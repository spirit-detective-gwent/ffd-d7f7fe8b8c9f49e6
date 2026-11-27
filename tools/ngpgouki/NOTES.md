# v6566-ngpgouki — NG+ Ch1 Gouki plays like a fresh game; no outdoor 'Fight' marker
Branch v6566-ngpgouki off origin/main c1a3b8c (live v6.5.64). Worktree /workspace/ngpgouki/wt. Scratch: /workspace/ngpgouki (tools, logs, shots).
Compat: v6565-ngptracker adds one line after `var N = ngBuild(SAVE, o);` in v640NgStart + qBanner once-guard keyed per NG+ run. Do not touch those lines.
## Log
- Repro (live, tools/repro.py ngp): NG+ start resets gouki/ch1/gkPh/gym state fine (ngBuild fresh). Gym interior, seals, Main Court all work,
  but gymBoss -> gkFight() fights a single plain duel: `if (SAVE.gouki || SAVE.ch1 || SAVE.ngp) fight(['gouki'], true)` -> no gkPhase 1 / item-revival loop / Bond Double finale.
- Live repro, full tap-through (repro2): fresh = phase 1 -> loop -> Bond -> gkFin -> ending -> card -> Ch2. NG+ = ONE plain duel, Ofuda, ending, card.
  A clean NG+ tap-through still reaches Ch2, so the 'Fight' marker + reset loop is the interrupted case:
  * Gouki down (SAVE.gouki=1) but Ch1 not closed. gkEndingOpen()/gkMidOpen() had `!SAVE.ngp`, so an NG+ reload never resumed the ending.
  * tagDefs shows the outdoor 'Fight' tag whenever SAVE.gouki||SAVE.ch1 -> gymDialog 'Rematch' -> gkFight -> plain duel outdoors.
  * If the ending lines had already set SAVE.sc.ending (reload during the Wardens lines, before chapterCard), every later win has no `after`
    -> nothing closes Ch1: Gouki resets forever (fresh had the same dead end; NG+ hit it more since nothing resumed).
- FIX (93a0d34 WIP):
  * gkFight: drop SAVE.ngp from the single-duel branch -> NG+ Ch1 gets phase 1, the item-revival loop and the Bond Double finale.
  * benchOf: Double locked in gkPhase 1 / gkLoop while Gouki is not down (only changes NG+; fresh already had dbl=0 there).
  * gkEndingOpen/gkMidOpen: NG+ included (gated on chapter<=1 instead); new gkCardOpen() (ending played, no card) -> chapterCard; load() GK_RESUME uses it.
  * tagDefs: the outdoor 'Fight' tag over Gouki/the gym is gone (fresh and NG+). gymDialog: Gouki down + Ch1 open -> resume ending/card;
    after Ch1 the kneeling talk keeps only 'Leave him' (Rematch removed). gymBoss (Main Court) is the only way to fight him.
  * v640NgStart: also clears W.gymBossBusy/gkFx/gkFloor/_gkLast (new line after the W.dgF line; ngptracker's line is untouched).
- tools/ngpgouki/ngpgouki_test.py --quick (stuck saves + no Fight tag): branch 8/8, live 2/8.
- NOTE for the Ofuda job: gearOfudaOnWin -> scene -> gearFind; if #gfind is not .on synchronously, then() (chapterEnd) runs right away AND
  W.gfindThen=chapterEnd fires again on Equip/Stash (seen: Ofuda card over the ending's first line). Not touched here (ofuda worktree moves the drop).
