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

## Stage inventory (git: ch1 photo rooms from v6.5.20; painted C2BT rooms wired in v6.5.61 (35a02e4); S2 rooms + `feet: 52` v6.5.62/63)
Foot y = 164 at default; 390x844. Floor seam: painted base rooms 217 px (H0 330/1280 x 0.659).
| stage (data-bfx) | added | foes that fight there | before foot | after foot | verdict |
|---|---|---|---|---|---|
| 1 (yard), lib_hall, lib_archive, art_studio, art_stage, cafe_line, cafe_dining, store_track, gym_arena | v6.5.20 | Ch1 bullies/minibosses | 164 | 164 | already fine |
| store_bay, gym_side | v6.5.20 | Ch1 | 196 (bt-feet-lo 32) | 196 | already fine |
| gekko_cafe | 13u | 3 Alley Hustlers | 164 | 164 | already fine (counter base ~150) |
| c2_street | 6.5.61 (+52 in 6.5.63) | gang brawls, West Street, Kaneda + 2 | 216 | 216 | already fine |
| c2_br, c2_se, c2_lk, c2_qy, c2_gg, c2_ap, c2_sh | 6.5.62-63 (S2) | Boso, Kaji, Sada, Masa | 216 | 216 | already fine |
| c2_sento_hall, sento_boiler, sento_kitchen, sento_trophy | 6.5.61 | gang members, Goda, hustlers, Kaneda | 164 | 224 | FIXED (60) |
| c2_hotel_door, west_wall, udon | 6.5.61 | Cold Water / Wet Paint / Tetsu | 164 | 224 | FIXED (60) |
| c2_lantern_alley | 6.5.61 | Ban Shigure, alley hustlers (Kagero tested too) | 164 | 216 | FIXED (52, = ch2ov) |
| c2_club, c2_gym, c2_depot, c2_arcade, c2_waga | 6.5.61 / 6.5.63 | bouncer, Tetsu, Aoi/Ryo spar, Masa, Nails, Jin, Boso x3 | 164 | 224 | FIXED (60) |
Jin branch rooms (read-only on 4dff155): j6ramen, j6karaV, j6hhall, j6hdeal (Ogata 707), j6ckoff, j6gcback: all `feet: 52` (216), fine.
Kagero's roof fight is room '0' (no painted backdrop).
Test: `/workspace/pwenv/bin/python3 tools/ground/test_ground.py [index.html]` -> 148/148 here, 172/172 on a trial merge with ch2ov + jin; on live 108/148 (40 fail).
When a new backdrop is added: give it a FLOOR entry in the test (floor top screen px + foe groups). The default ground line (60) already applies at runtime.
