# v6564-ch2ov — Ch2 overworld (Ban ground, Wagashi, Chiyo loop, Kissa door, Four Corners lines)

Date: 2026-11-26 (America/New_York)
Base: e1ba0d4 (main, live v6.5.63)
Branch: v6564-ch2ov
Worktree: /workspace/ch2ov/wt
Not published, not pushed, no FFF_BUILD bump.
Did not touch /workspace/ffd (v6564-jin) or shared nails-art inject.

## Scope (Erik t426–t431)

- KEEP Ban battle-ground float fix (fighters stand on the lantern-alley stone).
- DROP the earlier “move Ban’s knockdown staging right” request. Lie spots stay put.
- Relocate the Chiyo Wagashi storefront off the alley / Lucky 7 overlap so it occupies the Lucky 7 south frontage and no longer covers the downed bodies.
- Fix Chiyo closed-shop talk loop (“I’m sorry. I can’t open with them on the step.”).
- Shrink the Kissa Gekko (kissaten) door trigger so sidewalk walking does not auto-enter; audit other Ch2 town doors.
- Four Corners / Genji talk: Ryo asks around the gangs for info. He must not say he will join a crew or win streets. Joining is stumbled onto later.

## Ban battle ground

`ROOMS.lantern_alley` had `feet: 0` (unset), so Ban stood in the wall/sign band with a gap above the stone grid. Street already used `feet: 52`.

Fix: `sway: 1, feet: 52` on `ROOMS.lantern_alley` in index.html (`/* v6.5.64: Ban's alley — stand on the stone, not float */`). Runtime: `FFF_C2BT.feetPx('c2_lantern_alley') === 52`, `#fE` transform `translate(0, 52)`.

Source `nails-art/c2bg/c2bt.js` still lacks this; do not inject that pack into `/workspace/ffd`. Pick it up the next time C2BT is rebuilt into this tree.

## Wagashi placement

The 400×160 facade (`FFF_S2P.facadeDoor`) has the eave/sign at the top and the door/noren at the bottom. It had been planted in the sidewalk gap (top 2600, z 2860) in front of Lucky 7’s lower windows, covering Ban’s lie bodies.

New placement occupies Lucky 7’s south frontage, bottom flush on the lantern-lane wall (y=2600):

- Facade CSS / `S2.FAC_BOX`: `[2880, 2440, 3280, 2600]`, z-index `100+2600`.
- `SHOP_AT = [3080, 2640]` (was `[3080, 2680]`).
- `WAGA_DOOR.r = [3040, 2520, 3120, 2600]`, `out = [SHOP_AT.x, SHOP_AT.y+16]`, spot face 3 (walk north into the doorway).

Quests still go through `TRANS.s2_e_waga` / `doorTalk()`. Lucky 7’s rooftop sign still peeks above the 160px eave (the facade canvas is only 160 tall); bodies at y≈2744/2756 are in the clear. Visual confirm is on the Wagashi before/after sheet.

## Chiyo shopCold loop — root cause

`TRANS.s2_e_waga = 1` auto-enters the door rect. When the shop is closed, `doorTalk()` called `talk(pv(VO.shopCold))` with no state change and no leave-latch. Dialogue ended with Ryo still inside the rect, so auto-enter fired again — infinite conversation, no way to walk off.

Fix: `armWagaLatch()` sets `W._s2WagaSaid` and polls every 150ms until `inWagaDoor()` is false, then clears the latch. `doorTalk()` returns early while latched. Latch is cleared on a real enter when the shop is open (`qDone()`).

## Kissa Gekko door (and other Ch2 doors)

Old `GK_DOOR = { r: [2096, 2560, 2212, 2676], at: [2150, 2692] }` (116×116, deep into the sidewalk / lantern lane y=2600–2760). Walking near the shop auto-entered.

New: `{ r: [2108, 2520, 2190, 2600], at: [2150, 2640] }` — doorway only, bottom at the lane wall like the clinic door (`r: [330, 2520, 430, 2600], at: [380, 2640]`, face 3). `GK_CURB` unchanged.

Audit: no other Ch2 town TRANS door bites more than 48px into `G38T.LANE = [910, 2600, 4900, 2760]`.

## Four Corners / Genji wording (t429–t431)

Intent: ask around the gangs for info. Ryo must not pledge to join a crew or win streets. Joining stays a later stumble (the side quest “Where the Crews Clash” still uses “Back a crew in a border fight”).

### Genji conversation (old → new)

Mood vs no-mood copies of `c2ClubChoiceLines()` / `c2lStreetTalk()`:

- Balanced Ryo: (old, along the lines of “join a crew and win some streets”) → `Let's check out the gangs, see if someone knows anything.`
- Fierce Ryo: `Tch. Then we ask around. The gangs might know.` / Aoi: `Ask around first. Tetsu keeps.`
- Strategic Ryo: `So we ask around. One of the four might know.` / Aoi: `We ask around. Sooner or later someone tells us who Tetsu works for.`

`C2S_STEPS[0]`: `Throw in with a crew (or go it alone)` → `Check out the gangs (or go it alone)`.

`c2lCornersSteps` section `'Talk to a crew'` → `'Check out the gangs'`. tetsuHint: `'Wiser to have a crew at your back first.'` → `'Ask around first. See if someone knows anything.'`

`C2SC.locks` Genji: `'Keep working the crews, or go hunt. Your call.'` → `'Ask around the gangs, or go hunt. Your call.'`

`outsideLines` (stepping out after Four Corners): Aoi/Ryo no longer say “Help one win, and they’ll talk to us.” Fierce Aoi: `Then we look in. Someone might know something.` Balanced/strategic Ryo: `Then we go look. See if someone knows anything.`

### Four Corners quest text (old → new)

- Journal first step / `lockFirst()` / onboarding unshift: `Back a crew in a border fight` → `Check out the gangs at a border`.
- Four Corners `qBanner` (fc13s + fc51): same new label.
- Section rename hooks also accept `'Check out the gangs'` (and still rewrite leftover `'Talk to a crew'` from older saves).
- Filter still drops the old `'Back a crew in a border fight'` label from the Four Corners card so leftover saves don’t show the pledge. The later side quest “Where the Crews Clash” keeps that step text — that’s the stumble-onto-joining beat.

## Tests and shots (in progress)

- `tools/s2/s2_test.py`: Wagashi door asserts updated for Lucky 7 frontage (stand y 2600–2680; door rect ends at y=2600).
- `tools/ch2ov/test_ch2ov.py`: Ban feet, facade vs lie spots, door audit, Four Corners lines, Chiyo loop. Chiyo loop hook still being switched to an exported / latch-state path (not scoped `talk`).
- Before shots (clean e1ba0d4 tree, do not overwrite): `/workspace/ch2ov/shots/before/{ban_battle,waga_alley}.png`
- After shots (this branch): `/workspace/ch2ov/shots/after/{ban_battle,waga_alley}.png`
  - Ban: feet 52, transform `matrix(1,0,0,1,0,52)`, standing on the stone.
  - Wagashi: facade left 2880 top 2440 z 2700; lie spots unchanged; bodies visible in the alley.

## Remaining

Rebuild S2 after exporting a doorTalk hook, finish the Chiyo loop test, run s2_test + verify_wired, perf vs e1ba0d4 (Ban fight, Wagashi alley, town walk), compose one before/after sheet per fix, final commit. No publish, no push, no version bump.
