# v6566-ngpgouki — NG+ Ch1 Gouki plays like a fresh game; no outdoor 'Fight' marker
Branch v6566-ngpgouki off origin/main c1a3b8c (live v6.5.64). Worktree /workspace/ngpgouki/wt. Scratch: /workspace/ngpgouki (tools, logs, shots).
Compat: v6565-ngptracker adds one line after `var N = ngBuild(SAVE, o);` in v640NgStart + qBanner once-guard keyed per NG+ run. Do not touch those lines.
## Log
- Repro (live, tools/repro.py ngp): NG+ start resets gouki/ch1/gkPh/gym state fine (ngBuild fresh). Gym interior, seals, Main Court all work,
  but gymBoss -> gkFight() fights a single plain duel: `if (SAVE.gouki || SAVE.ch1 || SAVE.ngp) fight(['gouki'], true)` -> no gkPhase 1 / item-revival loop / Bond Double finale.
