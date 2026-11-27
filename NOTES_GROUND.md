# v6564-ground — battle grounding audit (GGD-72)
Branch v6564-ground off main e1ba0d4 (live v6.5.63). Worktree /workspace/ground/wt. Nothing pushed, nothing published, no version bump (the release job does that).

## Problem
Foe column (#fE) sits at a fixed foot y=164 (390x844). Painted Ch2 rooms have their floor seam at H0=330/1280 -> 217 px on screen, so on a room with no `feet:`
the foe stands 53 px above the floor, against the wall / signs / cabinets.

## System (unchanged)
FFF_C2BT.feetPx(roomKey) -> `#fE.bt-feet-c2{transform:translateY(var(--bt-feet))}` (set by FFF_BTFEET in startMatch). Ch1 photo rooms use the default foot (or `bt-feet-lo`, 32 px).
All foes share one foot (the #eFig canvas is 92x74 for every foe, bottom-aligned), so no per-foe override is needed: measured sprite bottom == fbody bottom for every foe on every stage.

## Fix
`GROUND` table + `GROUND_DEF` (60) in the C2BT module; feetPx = room.feet ?? GROUND[id] ?? GROUND_DEF.
Any painted room without an explicit ground line now gets 60, so a future backdrop cannot leave a foe on the wall.

## Merge notes
- v6564-ch2ov: sets `feet: 52` inline on ROOMS.lantern_alley (the `lights:` line). I did NOT edit that line; GROUND.lantern_alley = 52 is the same value, and the inline value wins. No conflict expected (verified with a trial merge).
  52 puts Ban's feet exactly on the wall seam (216 vs 217). If it should be deeper, change both to 60.
- v6564-jin: adds j6ramen/j6karaV/j6hhall/j6hdeal/j6ckoff/j6gcback with `feet: 52` in the hook (S2P6). Checked read-only on 4dff155: foot 216, on the floor seam, all fine. The hook's inline value wins over my default.
  If you want Jin's rooms to match the deeper 60, change the one `feet: 52` in P6 hookBattle.
- Kagero's roof fight maps to room '0' (no painted backdrop, dimmed overworld); not changed.
