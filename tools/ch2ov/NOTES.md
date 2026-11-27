# v6564-ch2ov — Ch2 overworld (Ban ground, Wagashi, Chiyo loop, Kissa door, Four Corners lines)

Date: 2026-11-26–27 (America/New_York)
Base: e1ba0d4 (main, live v6.5.63)
Branch: v6564-ch2ov
Worktree: /workspace/ch2ov/wt
Final commit: (see git log)
Not published, not pushed, no FFF_BUILD bump (still v6563).
Did not touch /workspace/ffd (v6564-jin) or shared nails-art inject.

WIP checkpoint: bf6c660. This note describes the finished branch.

## Scope (Erik t426–t431)

- KEEP Ban battle-ground float fix (fighters stand on the lantern-alley stone).
- DROP the earlier “move Ban’s knockdown staging right” request. Lie spots stay put.
- Relocate the Chiyo Wagashi storefront off the alley / Lucky 7 overlap so it occupies the Lucky 7 south frontage and no longer covers the downed bodies.
- Fix Chiyo closed-shop talk loop (“I’m sorry. I can’t open with them on the step.”).
- Shrink the Kissa Gekko (kissaten) door trigger so sidewalk walking does not auto-enter; audit other Ch2 town doors.
- Four Corners / Genji talk: Ryo asks around the gangs for info. He must not say he will join a crew or win streets. Joining is stumbled onto later.

## Ban battle ground

`ROOMS.lantern_alley` had no feet offset, so Ban stood in the wall/sign band with a gap above the stone grid. Street already used `feet: 52`.

Fix: `sway: 1, feet: 52` on `ROOMS.lantern_alley` in index.html (`/* v6.5.64: Ban's alley — stand on the stone, not float */`). Runtime: `FFF_C2BT.feetPx('c2_lantern_alley') === 52`, `#fE` transform `matrix(1, 0, 0, 1, 0, 52)`.

Source `nails-art/c2bg/c2bt.js` still lacks this; do not inject that pack into `/workspace/ffd`. Pick it up the next time C2BT is rebuilt into this tree.

## Wagashi placement

The 400×160 facade (`FFF_S2P.facadeDoor`) has the eave/sign at the top and the door/noren at the bottom. It had been planted in the sidewalk gap (top 2600, z 2860) in front of Lucky 7’s lower windows, covering Ban’s lie bodies.

New placement occupies Lucky 7’s south frontage, bottom flush on the lantern-lane wall (y=2600):

- Facade CSS / `S2.FAC_BOX`: `[2880, 2440, 3280, 2600]`, z-index `100+2600`.
- `SHOP_AT = [3080, 2640]` (was `[3080, 2680]`).
- `WAGA_DOOR.r = [3040, 2520, 3120, 2600]` (was `[3030, 2688, 3130, 2764]`), `out = [SHOP_AT.x, SHOP_AT.y+16]`, spot face 3 (walk north into the doorway).

Quests still go through `TRANS.s2_e_waga` / `doorTalk()`. Lucky 7’s rooftop sign still peeks above the 160px eave (the facade canvas is only 160 tall); bodies at y≈2744/2756 are in the clear.

## Chiyo shopCold loop — root cause

`TRANS.s2_e_waga = 1` auto-enters the door rect. When the shop is closed, `doorTalk()` called `talk(pv(VO.shopCold))` with no state change and no leave-latch. Dialogue ended with Ryo still inside the rect, so auto-enter fired again — infinite conversation, no way to walk off.

Fix: `armWagaLatch()` sets `W._s2WagaSaid` and polls every 150ms until `inWagaDoor()` is false, then clears the latch. `doorTalk()` returns early while latched. Latch is cleared on a real enter when the shop is open (`qDone()`). `S2.doorTalk` is exported for the regression test (no scoped `talk` hook).

## Kissa Gekko door (and other Ch2 doors)

Old `GK_DOOR = { r: [2096, 2560, 2212, 2676], at: [2150, 2692] }` (116×116, deep into the sidewalk / lantern lane y=2600–2760). Walking near the shop auto-entered.

New: `{ r: [2108, 2520, 2190, 2600], at: [2150, 2640] }` — doorway only, bottom at the lane wall like the clinic door (`r: [330, 2520, 430, 2600], at: [380, 2640]`, face 3). `GK_CURB` unchanged.

Audit: no other Ch2 town TRANS door bites more than 48px into `G38T.LANE = [910, 2600, 4900, 2760]`.

## Four Corners / Genji wording (t429–t431)

Intent: ask around the gangs for info. Ryo must not pledge to join a crew or win streets. Joining stays a later stumble (the side quest “Where the Crews Clash” still uses “Back a crew in a border fight”).

### Genji conversation (old → new)

`c2ClubChoiceLines()` / `c2lStreetTalk()` (mood and no-mood copies):

- Balanced Ryo: `So we get a crew first. Pick a side, win some streets.` → `Let's check out the gangs, see if someone knows anything.`
- Fierce Ryo: `Tch. Then we join something. Fast.` / Aoi: `A crew first. Tetsu keeps.` → Ryo: `Tch. Then we ask around. The gangs might know.` / Aoi: `Ask around first. Tetsu keeps.`
- Strategic Ryo: `So we get inside. One of the four.` / Aoi: `Win their streets. Sooner or later a boss tells us who Tetsu works for.` → Ryo: `So we ask around. One of the four might know.` / Aoi: `We ask around. Sooner or later someone tells us who Tetsu works for.`

`C2S_STEPS[0]`: `Throw in with a crew (or go it alone)` → `Check out the gangs (or go it alone)`.

`c2lCornersSteps` section `'Talk to a crew'` → `'Check out the gangs'`. tetsuHint: `'Wiser to have a crew at your back first.'` → `'Ask around first. See if someone knows anything.'`

`C2SC.locks` Genji: `'Keep working the crews, or go hunt. Your call.'` → `'Ask around the gangs, or go hunt. Your call.'`

`outsideLines` (stepping out after Four Corners): no longer “Help one win, and they’ll talk to us.” Fierce Aoi: `Then we look in. Someone might know something.` Balanced/strategic Ryo: `Then we go look. See if someone knows anything.`

### Four Corners quest text (old → new)

- Journal first step / `lockFirst()` / onboarding unshift: `Back a crew in a border fight` → `Check out the gangs at a border`.
- Four Corners `qBanner` (fc13s + fc51): same new label.
- Section rename hooks also accept `'Check out the gangs'` (and still rewrite leftover `'Talk to a crew'` from older saves).
- Filter still drops the old `'Back a crew in a border fight'` label from the Four Corners card so leftover saves don’t show the pledge. The later side quest “Where the Crews Clash” keeps that step text — that’s the stumble-onto-joining beat.

## Tests

- `tools/s2/build.py` rebuild into this worktree’s index.html: ok. `S2.doorTalk` present; non-S2 patches (Ban feet, GK_DOOR, Four Corners lines) still in place.
- `tools/s2/s2_test.py`: Wagashi door asserts updated for Lucky 7 frontage (stand y 2600–2680; door rect ends at y=2600). **167/167 PASS**.
- `tools/ch2ov/test_ch2ov.py`: Ban feet, facade vs lie spots, Kissa + other Ch2 door audit, Four Corners lines, Chiyo loop via `S2.doorTalk` + latch state. **26/26 PASS**.
- `verify_wired.py` (from `/workspace/v6560-review/portraits`, root `/workspace/ch2ov/wt`): **PASS**.

## Perf vs live e1ba0d4 (America/New_York)

Main run: 2-run medians, iPhone 390×844, Ban fight 20s, Wagashi alley 8s, town walk 20s. Combined protocol went fight → alley → walk.

Clean 1x remasure: fresh Ch2 boot (no fight first), 3-run medians, because the first combined new-alley window (50.6 fps) was taken right after leaving the Ban fight and pulled that median under the gate.

### 1x fps / heat (report these)

| scene | live fps | new fps | live heat | new heat | notes |
|---|---:|---:|---:|---:|---|
| Ban fight | 55.5 | 55.6 | 40.5 | 42.4 | combined-run median, gate >= 55 |
| Wagashi alley | 59.9 | 59.4 | 48.2 | 41.4 | clean remasure median, gate >= 58 |
| Town walk | 56.0 / 55.1 | 50.5 / 50.6 | 35.0 / 24.9 | 38.5 / 26.5 | combined / clean; gate >= 50 |

### 4x throttle heat (combined-run medians)

| scene | live heat | new heat | delta |
|---|---:|---:|---:|
| Ban fight | 85.5 | 84.2 | −1.3 |
| Wagashi alley | 82.6 | 84.6 | +2.0 |
| Town walk | 81.7 | 83.7 | +2.0 |

All 4x heat deltas <= +5. Memory flat (heap deltas about 0 to −3 MB; not climbing). Logs: `/workspace/ch2ov/perf/report.md`, `results.json`, `rerun_clean.json`.

## Before/after sheets

Under `/workspace/ch2ov/`:

- `/workspace/ch2ov/sheet_ban_ground.png` — Ban standing on the stone (feet 52).
- `/workspace/ch2ov/sheet_wagashi.png` — storefront off the alley, onto Lucky 7; bodies visible.
- `/workspace/ch2ov/sheet_kissa_door.png` — red auto-enter rect shrinks to the doorway (yellow line = lane wall y=2600).
- `/workspace/ch2ov/sheet_chiyo_loop.png` — after closing Chiyo’s line, still in the doorway: live retriggers the talk; this branch does not, and Ryo can walk south.
- `/workspace/ch2ov/sheet_four_corners.png` — Ryo’s Four Corners line, old vs new.

Source stills: `/workspace/ch2ov/shots/before/` and `/workspace/ch2ov/shots/after/`. Live baseline tree: `/workspace/ch2ov/live` (e1ba0d4 worktree).
