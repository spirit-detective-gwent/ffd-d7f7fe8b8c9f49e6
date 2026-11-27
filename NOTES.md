# v6565-runup (Erik t534): Ch1 sub-boss run-up stalls in place

Branch v6565-runup off c1a3b8c (live v6.5.64). Worktree /workspace/runup/wt. Not pushed.

## Suspected cause (from code read)
- v6.5.63 GGD-22: frame() returns early (no moveRyo / follow) while FFF_SCAM.st.boss is set, to hold the world still during a boss arrival.
- v6.5.64 mizunocam: Ch1 minis (BENT_EASE) set st.ease + st.bridge in bossEnt, and FFF_SCAM.end() keeps st.boss on while bridged, until swirl() clears it.
- So on a first visit (entrance plays) st.boss stays true through miniDialog AND the run-up: walkTo fills W.path but frame() never moves Ryo; runUp's wait() only ends at its timeout lim = max(3 s, d/200 + 1.5 s) -> ~3-5 s running in place, then fight starts where he stands.

## Confirmed (repro on live c1a3b8c, tools/runup/test_runup.py)
First visit (boss entrance plays) on live: Ryo moves 3 px, Aoi 0, fight starts at 3.6-4.1 s from where he stands, for ALL four Ch1 minis
(Mizuno, Mai, Kurata, Bando). Repeat visits (entrance already seen -> no st.boss) ran fine. Kurata's pre-dialogue walk-up was frozen too
(live first-visit d0 394 vs 296).

## Fix (5c0741c)
New bossHoldStill(): the GGD-22 hold (frame() early return + follow() Aoi hold) applies only while nothing scripted is moving:
not during W.runUp, not while W.path has steps, not while Aoi is still catching up. The entrance reveal itself is still frozen
(bossEnt clears path / runUp off / Aoi stopped), so GGD-22 heat savings during the reveal + miniDialog stay. Mizuno gap fix untouched
(libBossApproach runs before bossEnt; mizcam test 41/41).

## Tests (branch)
- tools/runup/test_runup.py: 48/48 (4 minis x first/repeat; fight within ~2 s (<=2.3), gap closes to 58 px, Aoi follows)
  live: 12 fail on every first visit.
  Times after: lib 0.9 s, art 1.4 s, cafe 1.6 s, field 1.2 s (repeat field 2.2 s: 430 px run, same as live 2.05 s).
- ch_smoke PASS, verify_wired PASS, mizcam test_cam 41/41, gangcam test_cam 40/40 (shots redirected to /workspace/runup/gangcam_shots).
  Note: mizcam test_cam writes its shots to /workspace/mizuno-cam/shots (tag runup_after_*).
- Shot: /workspace/runup/shots/strip_mb_art_before_after.jpg (live 0.5 s / 1.1 s vs fix 0.5 s / 1.1 s at Mai's stage)
