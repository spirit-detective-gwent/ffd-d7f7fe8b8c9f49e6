# v6566-goukicine (Erik t535): Gouki Main Court entry as one cinematic

Branch v6566-goukicine off c1a3b8c (live v6.5.64). Worktree /workspace/goukicine/wt. Not pushed. No version bump.

## Cause (live, probed with tools/goukicine/probe.py)
- gymFrame starts gymBoss when Ryo comes within 160 px while moving. gymBoss zeroes v / path, then bossEnt sets FFF_SCAM.st.boss,
  and the GGD-22 hold makes frame() return early, so animWalk never settles the pose: Ryo stays frozen on a sprint frame (fr 4 of 12)
  and Aoi on a stride frame (fr 7) for ~16 s through the camera push, the name card and all the lines ("No more doors between us.").
  That is the "running in place" in Erik's shot. Gouki's own run-up after the lines works on live (st.boss is cleared by then).
- Related but separate: v6565-runup (/workspace/runup/wt, 5c0741c) changes frame()/follow() to bossHoldStill() so a scripted
  run-up / path still ticks during the eased Ch1-mini bridge. This branch does NOT touch frame()/follow() (no conflict); the two
  compose: our walk finishes before bossEnt raises st.boss, and our stopped poses are settled so the hold freezes a standing frame.

## Change (index.html, gym block only)
- gymGo arms W.gkCineArm on entering the Main Court with Gouki present; gymFrame fires gymBoss as soon as the court is free
  (after the first-visit "in_arena" lines). The old walk-up trigger (d < 160 while moving) stays as the fallback (e.g. back in the
  court after a loss without a room change) and plays the same cinematic.
- gkCine: input locked (sLock 'gkcine'); camera frames Ryo + Aoi + Gouki (W.camFocus); they come in from the door and stop on set
  marks south of him (Ryo g+(-34,150), Aoi g+(40,162); falls back to a line 150 px out if a mark is blocked). A long way in
  (> 300 px, e.g. the Trophy Hall door) runs most of it on the normal mover (sprint sheet) and eases into a walk for the last 120 px.
  On arrival both face him and are settled on a standing frame (animWalk(s,0) x2) before bossEnt; Aoi is held (actMove) through the
  lines so the trail-follow can't walk her into Ryo; input is handed to bossEnt / the dialogue; after the last line the existing
  run-up carries Ryo the last ~90 px and the board opens. gymGo (leaving mid-scene) cleans up.
- No new always-running loop: c2Walk rAF ends on arrival; the run-phase poll is a bounded setTimeout.

## Tests
- tools/goukicine/test_goukicine.py: 56/56 PASS (logs/test_branch3.log). Modes fierce, strategic, repeat (entrance seen), west door,
  ngp, near (walk-up trigger, no room change), aoi (SAVE.act aoi). Per mode: starts on its own, input locked during the walk,
  Ryo moves 400-573 px and stops 154 px from Gouki, Aoi stops beside (167 px), nobody runs in place while stopped (frame holds,
  run/moving off, standing frame 2/6 whenever position is unchanged), fight starts, no page errors.
  Live (probe.py): Ryo frozen on sprint fr 4 / Aoi on stride fr 7 for ~16 s (the fail case).
- ch_smoke PASS; ngp_test 104 PASS / 0 FAIL (run on port 8987 copy: 8977 was busy with another agent); verify_wired PASS.
  Logs in /workspace/goukicine/logs.

## Perf (tools/goukicine/perf_scene.py, live c1a3b8c vs branch, interleaved, waits while load > 6, iPhone dpr 3)
Window = 16 s from entering the court: walk-in, arrival push, name card, first lines.
- 4x: live 56.2 fps / branch 57.3 fps (median of 3); heat (cpu busy) 22.0 vs 23.2 (+1.2); p95 16.8 both; heap 55 MB flat.
- 1x: live 59.5 / branch 59.4 fps; heat 8.1 vs 7.8.
(box load drifted 5.5-10 during runs from other agents; 1% lows noisy on both.)

## Media (/workspace/goukicine/media)
- gouki_entry_before_after.mp4: side by side, 26 s, entry -> lines.
- gouki_entry_strip.png: before/after strip (walking in, arriving, camera push, stopped, dialogue).
