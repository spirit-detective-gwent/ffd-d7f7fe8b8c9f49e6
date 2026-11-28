# v6566-floorwalk (GGD-88, Erik t545): walkable floor props in the Storehouse and the Gym
Branch v6566-floorwalk off c1a3b8c (live v6.5.64). Worktree /workspace/floorwalk/wt. Nothing pushed, no version bump.

## Cause
Both bases are single painted cel backgrounds (world/sf_*.webp, world/gy_*.webp). The floor props are flat in the art,
but their rectangles were listed in the room `block:` arrays, so the grid walled them off. Ryo stopped at the edge and tap-walks detoured.

## Fix (index.html)
- Removed the floor props from `block:`; their inspect spots carry `fl: 1`.
- The FLDG/GYMG (and the other dungeon) spot builders copy `fl` into INT spots. fldTags/gymTags give those tags `floor: 1, flr: 1, cls: ' flr'`,
  so standing on the prop selects its Look (same rule as the nurse's mat).
- CSS `.wtag.obj.flr`: a flat outline only (no fill or inner glow over Ryo). tagsFrame toggles `.stand` while Ryo is inside it
  (this is the existing per-frame tag pass, not a new loop), which dims the outline.
- Art is unchanged: the pictures were already flat.

| room | prop | pic rect | spot |
|---|---|---|---|
| Storehouse · Locker Corridor (sf_lockers) | LANE 1 chalk tile | 520,480,630,560 | lane |
| Gym · Foyer (gy_foyer) | ORDERS mat | 200,520,380,620 | orders |
| Gym · Bleacher Concourse (gy_concourse) | HOME COURT mat | 520,200,760,280 | banner |
| Gym · Trophy Hall (gy_trophy) | GRAY COAT FILE mat | 180,480,420,620 | file |

Already walkable on live (no block): bay green rug, foyer blue welcome mat, trophy blue rug, court lines.
Left blocked on purpose (raised objects with a drop shadow): the stacked green gym mats in the Equipment Bay, Weight Room and Side Court
(Side Court block = drawn mats since v4.70), lockers, benches, hurdle cart, desks, sofa, bleachers.

## Merge notes
No overlap with v6566-lockeramb (it edits the fldEnt staging near FLDG.bay, not the room tables) or with the other v6566 branches.

## Tests
- tools/floorwalk/test_floorwalk.py: 21/21 PASS. For each prop: grid cell free, keyboard walk straight across (passes inside, ends past it),
  tap-walk straight across (0 px deviation), Look floor tag + standing selects it, inspect line plays, no page errors.
  Live sanity (--expect-blocked): 5/5, every prop blocks (Ryo stops at the edge; tap-walk detours 47-77 px).
- ch_smoke PASS, ngp_test 104/104, verify_wired PASS. Logs are in /workspace/floorwalk/logs.

## Perf (tools/floorwalk/perf_floor.py, live c1a3b8c vs branch, interleaved and order-alternated, waits while load > 6)
Ryo tap-walks back and forth across each prop for 8 s with the roamers present. Medians: 4x n=3, 1x n=1. Box load 3-5.6.
- 4x fps: lockers 60.0/60.0, foyer 59.9/60.0, concourse 60.0/60.0, trophy 59.8/59.8 (worst single run: branch 59.3).
- 4x heat (main-thread busy %): lockers 15.3 -> 17.5 (+2.2), foyer +0.5, concourse -4.0, trophy -0.4.
- 1x: 59.8-60.0 fps both; heat within +-1.7.
- heap 55-60 MB on both, flat; no page errors.
Before/after shot: /workspace/floorwalk/media/before_after_floorwalk.png (live vs branch, LANE 1 and the GRAY COAT FILE mat).
