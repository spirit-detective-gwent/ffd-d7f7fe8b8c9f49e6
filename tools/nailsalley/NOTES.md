# GGD nails alley (v6566-nailsalley off e4139c5)

Erik t610u / t611u, Ch2 compassionate playtest on live v6.5.65.

## Root cause

After Four Corners is given in the gym, 13t/v6551/v6552 run a "hear phase"
(`e.fc51Hear`) that only allows X1 (Chuo-dori) and X3 (Wagashi row) to spawn
and start a clash. X2 (west side street — Nails / Punks vs Hustlers, the
closest border to the gym door at 910,2640) and X4 are held:

- `g38tStart` returns false for X2/X4 until `fc51Seen.X1` and `.X3`
- `hearHoldOn()` / `heldCrewKeys()` strip those posts from `c2Crews` and
  drop leftovers, so the alley is empty (not even idle men)
- Distant punch bed (`heardList`) also only names X1 and X3

Walking north from the gym, X2 is first (1000px; X1 is further "at the top").
Reload can show the fight later once X1/X3 have been marked seen, or if a
fresh pop races the hold. That matches Erik: empty Nails alley, fighting
further up, appeared after close/reopen.

Second bug (same alley, t611u): v6.5.52 `markClashWon` flags both border
crews down and **drops every man on that border**, including the backed
Sukajan Punk. `c2sLockAsk` then plays "You hit like a Punk..." as a
disembodied line. After "Shake on it", 13u `flipStartAt()` spawns Flip
only 150px from Ryo (on-screen at 390px wide), so he teleports in.
`townActors` also did not resume `cutStart` after a reload mid-scene.

## Fix

- Lift the X2/X4 hear-phase hold so all four corners can spawn and clash
  right after gym exit. Won flags (`g38win_*` + `s.f` down) still block
  duplicates on reload, re-entry, and NG+.
- `g38tClashCheck` retrigger: if you entered a border's 600px radius while
  another clash was active, still start it once you're there and free.
- Keep the backed spokesman after a won clash; he walks to Ryo, says the
  line on screen, offers a hand. Shake plays a handmade in-engine clasp
  (portrait colours). Walk away lets him leave. Pending offer is saved
  (`e.lockAsk`) so a mid-scene reload resumes it.
- Flip spawns off-camera and walks in. `cutStart` resumes after reload.
  Walks are skippable.

No version bump. No new always-on loops (walks use the existing 13u rAF
step; cine ticks ride `c2Frame` / `c2Pop`).

## t614u / t615u Flip south-end clash battle (crosswalk)

Erik: after Flip's "Told you. South end, when it counts." three Nails
allies walk up, but the player still fought all three Hustlers alone.
Correction (t615u): KEEP the walk-in exactly as is (fine if they block
sneak-up). Don't change stealth or approach. Only change the battle:
two allies each take one enemy; Ryo fights just one.

Fix (FFF_NQ, walk-in bytes unchanged):
- `clashBeat` still spawns Flip + two Punks and walks them in the same
  way, then VO.clash.
- `fight([H], …, { nqAlly:1, dgks: all three })` so the player fights
  one Hustler. A win still marks nq_x_0/1/2 (allies took the other two).
- No C2HP3 bump on the 1v1.
- During the fight, two small `#nqxside` canvases show handmade punk vs
  hustler poses (sukajan purple/gold, hustler orange). 80ms timeout only
  while the fight screen is up; no new always-on rAF. Cleared on
  nqBack / beatReset / other startMatch.
- Retreat / defeat / mid-walk c2Pop still go through existing beatReset.

Tests: tools/corners/t13_clash.py 21/21.
Shots: /workspace/nailsalley/shots/before_after_clash.png
  (live 3-foe row vs branch 1-foe + two street pairs)
  also t13_battle_before.png, t13_battle_after.png, t13_walkin_*.png
Perf 4× dpr3 (3 interleaved runs): see shots/perf_clash.json
  median fps live 47.2 / branch 46.8; heat 91.5 / 88.4 (delta -3.1);
  heap 57.8 / 58.5. Both sides sit under the 55+ battle gate at 4× dpr3.

Alley spawn/handshake work (t610u/t611u) unchanged on this branch.

## t626u / t627u Flip clash: world cines replace the #nqxside canvases

Erik: helpers should visibly run at their Hustlers while Ryo steps to his;
after the win the camera is back on the street, the helpers finish theirs,
everyone regroups, then Flip's line.

- `#nqxside` canvases + their 80ms timeout removed (brawlOn/hookAllyMatch gone).
- Walk-in bytes unchanged. After VO.clash: `preCine` (punks run 290px/s with
  lean, guard poses; Ryo c2Walk + rdy sheet; Aoi steps up) -> `preDone` ->
  fight Ryo vs one Hustler (dgks all three, as before).
- Win: the stock Aoi post-fight quip plays first (it bumps scGen and would
  kill a pan), then `postCine`: camPan 'nqxcam', two timed exchanges
  (jab / swing / finisher, flash + squash poses), KO -> lieEl down, regroup
  walk, then `wonTalk` = original Flip chain.
- Skip button `#nqxskip` (single use, stops propagation). No input lock
  survives: xcAbort clears timers/poses/pan/skip/rdy and lockIn(false).
- Reload: c2Pop -> beatReset -> xcAbort. A reload after the win resumes
  clashWon from flags (crew spawns by Ryo), never a re-fight.
- Retreat/defeat: beatReset(true); Ryo is put back just outside the 190px
  trigger (y <= 2335) so a retreat does not loop straight into the walk-in.
- Only token-guarded timeouts + existing move/c2Walk/rdy rAF, during the cines.

Tests: tools/corners/t13_clash.py 79/79 (main, skip, reload, retreat, defeat;
menu home+journal, HUD map, swap, movement after each). ch_smoke PASS,
verify_wired PASS. Harness note: fake back() result now sets drop (it
made yen NaN on screen; game code fine).
Video: shots/flipfight_cine.mp4 (tools/corners/rec_clash.py).
Perf 4x dpr3 vs live e4139c5 (perf_clash.py, 3 interleaved, run 3 load-hit
both sides): pre 57.5 vs 58.8 fps, heat 81.3 vs 91.3; battle 50.7 vs 48.3,
heat 90.1 vs 87.5 (+2.6); post 59.0 vs 53.4, heat 81.4 vs 88.0.
