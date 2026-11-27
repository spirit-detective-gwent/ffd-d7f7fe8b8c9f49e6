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
