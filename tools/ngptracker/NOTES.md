# v6565-ngptracker — NG+ Ch1 side-quest tracker popup/sound
Branch v6565-ngptracker off origin/main c1a3b8c (live v6.5.64). Worktree /workspace/ngptracker/wt.
## Log
- Tracker = n9Slam(step, need) (big "1/4".."4/4" + qslam_* sfx), fired from sqOnKill (Ch1 SQ_IDS kenta/aya/riku/yuto) via dgAfter->sqAfterFight;
  "Complete" = qBanner('QUEST COMPLETE', D.n) in sqTurnIn (+ roundwin via FFF_QDONE_SFX), "READY TO TURN IN" float = v640ReadyPop (s.pop gate, save-scoped, fresh in NG+).
- Harness tools/h.py + repro_lib.py. Live repro results (logs_*.txt):
  * first run, NG+ cold load, NG+ after Ch2 in same session: slam 1/4..4/4 fires on synthetic back(), real lib touch fights, real card battle end, ambush KO.
  * NG+ started in a session where that quest title already hit QUEST COMPLETE: banner + roundwin SKIPPED -> ev world:v6552:qdone:skip:<title>.
    Cause: v6.5.52 once-guard `playedDone` (page-lifetime, keyed by title only) wrapped around qBanner. Never cleared on NG+ / Reset story / new chapter.
- FIX (commit 9d3f671, WIP): v6552 qBanner once-guard keys by NG+ run (`ngp<N>|title`; first playthrough key = title, unchanged) +
  root.FFF_QDONE_RESET(why) clears it; v640NgStart calls it right after ngBuild. n9Slam / qBanner signatures untouched.
- tools/allsq.py (4 Ch1 SQs + q_mb_lib main complete, rewards once): LIVE ngpsame = 14/24 (all 4 SQ banners + roundwin + main banner skipped; qdone:skip evs).
- Branch results: allsq ngpsame 24/24, ngp2 24/24, ngpcold 24/24 (live ngpsame 14/24 twice). ngp_test.py 104/104. verify_wired PASS.
  (first-mode main-quest banner miss on BOTH live+branch was a harness artifact: a Bond level-up card holds the pop queue; harness now taps it.)
  (¥NaN in early shots = harness: fake back() st had no .drop -> settle() items += undefined. Real fights always pass drop. Harness fixed, shots retaken.)
- first-mode allsq (harness fixed): branch 24/24, live 24/24 -> first playthrough unchanged.
- shot: shots/before_live_ngp_complete.png (live NG+ Kenta turn-in, no banner; ngpsame: 14/24 passed)
- shot: shots/after_branch_ngp_complete.png (branch NG+ QUEST COMPLETE; ngpsame: 24/24 passed)
- perf (4x CPU, dpr3, 3 interleaved runs, live c1a3b8c vs branch): SUMMARY {"map_ngp": {"old": {"fps": 57.3, "low1": 25.7, "busy": 70.3}, "new": {"fps": 55.9, "low1": 22.9, "busy": 69.8}, "heat_delta": -0.5}, "lib_hall_ngp": {"old": {"fps": 59.5, "low1": 44.7, "busy": 11.3}, "new": {"fps": 59.6, "low1": 45.1, "busy": 11.0}, "heat_delta": -0.3}, "slam_turnin_ngp": {"old": {"fps": 59.0, "low1": 30.4, "busy": 14.3}, "new": {"fps": 59.9, "low1": 54.6, "busy": 12.7}, "heat_delta": -1.6}}
- perf read: averages live/branch fps map 57.3/55.9, lib hall 59.5/59.6ish, slam+turn-in see SUMMARY; heat delta <=0 everywhere. Map spot is ~56-58 on BOTH builds under 4x throttle + box load (live worst run 55.8, branch worst 54.0); fix adds no per-frame work (only runs on a QUEST COMPLETE call).
