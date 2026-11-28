# v6566-baseexp — GGD-89: Cafeteria + Storehouse grow to 8 rooms each (Erik t546u/t547u/t548u)
Branch v6566-baseexp off v6566-lockeramb (f5a8f72) + merge of rc-v6565 d3dc51e (supply rooms; lockeramb is off live and lacks
SUP_PAIRS). Worktree /workspace/baseexp/wt. Not pushed. No version bump. Merge into v6.5.66 later.
All code changes are made by tools/baseexp/patch_code.py from /workspace/baseexp/work/index_base.html (pre-patch index.html,
= ba39461) — rerun it after editing; it also re-embeds the 4 baked wall-kit backgrounds that gained doors.


## Follow-ups (Erik t583u / t587u / t588u) — supersede the guard/roamer lines below
- Room rules: crate rooms (Cooler / Dock / Bakery) hold ONLY the quest guard, never roamers (foes: [], R.after gate
  removed). Interpretation: "lunch box rooms" = the three crate rooms. Dish Room: none. Lunch Line / Kitchen keep theirs.
- Guard patrol (all three cafe guards): CAF_GRD[k].pts = a 4-corner loop round the room (picture px, all walkable:
  cooler round the north shelf, dock + bakery round the middle). GRD_T: sp 58 px/s, corner pause 1.3 s with a +-0.5 rad
  look, 0.55 s turn to the next leg. grdStep runs only inside dgFrame (Cafeteria rooms only) - no new always-on loop.
  The cone (.wgcone) is translated + rotated to his spot/facing each frame, one transform write only when it changes.
  Doorway landings are safe to peek from (grdPeek, 80 px) so entering a room never insta-spots you.
- Spotted (any alert/chase): grdCall -> BACKUP! bark (.wgbark one-shot) + toast + door sound, 4 backups (CAF_FOES)
  spawn at the room's door landings already alerted (f.team). Touching any team member = ONE fight of 5 (the normal
  group fight, guard first; dgks = all 5). Unseen touch from behind = noticedPack finds nobody else = solo fight.
  Win: all 5 keys down, guard resolved. Flee/lose: cafBack -> grdDismiss (backups leave), guard stunned -> scan -> 'ret'
  to the nearest loop corner -> rounds resume. A lost chase also dismisses the backups when he returns.
- Side quests moved into new rooms: sq_riku rations prop -> Dish Room (SQ_SPOT.rations [640,380]); sq_yuto spikes ->
  Timing Booth ([560,430]); step texts name the rooms.
- Hurdle rooms get library-style roamers (t587u/t588u): Cage 3, Showers 3, Trainer 2 (FLDG foes, FLD_FOES). Beaten =
  S.f[key] (persisted, main quest; refill rules as every base). Keys are per room, so a kicked hurdle back in the Cage
  never respawns anything. No special mechanics before pickup.
- Hurdle carry facing away (t588u): .wcarry.fh in dir 3 is wider than Ryo with the middle masked out, so his full back
  shows and only the hurdle's two ends stick out. Down / left / right unchanged (checked).
- Tests: test_baseexp sections G (patrol/cone/peek/cover/solo/5/flee/carry), R (room rules), H (hurdle roamers,
  reload), Q (side-quest props). Shots: shoot_patrol.py, shoot_carry.py.

## Cafeteria — "Lunch Duty" (modified: no Alley Cat in Ch1)
- New rooms: Walk-in Cooler (cf_cooler), Loading Dock (cf_dock), Dish Room (cf_dish), Bakery (cf_bakery).
  Doors: kitchen.gW<->cooler.gE, kitchen.gN (custom x 700-830, the fridge blocks the usual spot)<->dish.gS,
  cooler.gN<->dock.gS, dock.gE<->dish.gW, staff.gN<->bakery.gS. Map viewBox widened, "/8 rooms seen".
- CAF_CRATES = cooler, dock, bakery (line/kitchen/staff crates removed). Chute is still the Kitchen.
- One ROOM GUARD per crate room (CAF_GRD, bully3/bully4), quest-only: stands at his post next to the crate and turns
  between west/east on a fixed beat (GRD_T: hold 3.0 s, turn 0.7 s, always through the back wall). Sight = the normal
  seeK/susStep (the v6.5.30 override), with his own notice q.N at SIGHT23 numbers (rk 1, core 35, side .55); props are
  blocks so losClear makes them cover. Carrying: reach x1.25, notice time x0.5. Spotted -> "?" "!" chase -> touch fight
  (fight + crate home = existing cafBack). Flee: search, then 'ret' (findPath back to the post) and the beat resumes.
  Win: S.f['g'+room] -> never again. Crate dumped (cr==2) -> no guard. Cone = one .wgcone element per guard, rotated by
  a CSS transition only when a turn starts (no per-frame DOM writes); scaled when carrying, red while "?".
- No roamers in Cooler/Dock/Bakery before the clear (R.after: only once dgRefilled('cafe')). Dish Room: never.
  Lunch Line + Kitchen keep their live roamers (judgment call).
## Storehouse — "Lane fee's due" (no runner chase)
- New rooms: Equipment Cage (sf_cage), Showers (sf_showers), Trainer's Room (sf_trainer), Timing Booth (sf_booth).
  Doors: bay.gW<->cage.gE, lockers.gW<->showers.gE, lockers.gE<->trainer.gW, trainer.gS<->coach.gN,
  track.gE (gate in the east fence, clear of the wall kit)<->booth.gW. Track plan moved up; map viewBox taller.
- FLD_HURDLES = cage, showers, trainer (bay/lockers/coach hurdles removed).
- Lane fee: fldPlace checks Bando's oval angle vs the mark (fldFeeOk, >= 100 deg away = far side). Too close -> fldKick:
  hurdle flies (one-shot .fkick CSS, removed on a timer), S.kick[id]=1, it now lives in the Cage (hk_<id> spot/prop,
  fldHome); first kick plays FLD_SC.kick, later ones a comment. Slot rings (.fslotring ok/no) show only while carrying,
  updated inside the existing lap block.
- Timing Booth lever (one use): S.e.lever + slowArm; the next track pop sets lap.slowTo=1 and .fslow; fldFrame scales
  the existing lap rate (0.38 * 0.45) until lap.t reaches 1. No new loop.
## Supplies (Erik t547u)
- SUP_PAIRS 9, SUP_PIN lib 3 / art 1 / gym 1 / caf 2 / fld 2. 8 new WKIT_TABLE back-wall boxes (cloned cf_kitchen entry).
  Caf and Fld: 8 boxes each (7 wall + safe kit), 4 pieces -> 4 empty. SUP_RISK: at least one piece in cf_cooler/
  cf_dock/cf_bakery (guarded) and sf_bay/sf_lockers (patrolled) — supRoll swaps a piece in if the roll missed.
## Old saves (Erik: fresh playthrough, no migration)
- No supLay v2 / crate / hurdle remap. carryRecover drops a carry key that is no longer a crate/hurdle room. Tested: loads, no errors.
## Art
- tools/baseexp/paint_rooms.py + rooms.json: 8 rooms painted in-engine from existing room shells (walls/thresholds/kit
  sprites cut from cf_kitchen / cf_line / sf_lockers / sf_coach / sf_bay) + procedural cel floors and outlined props.
  `--existing` adds the new doors / track gate to cf_kitchen, cf_staff, sf_bay, sf_lockers, sf_coach, sf_track
  (world files; originals kept in /workspace/baseexp/work/orig) and the baked wkitbg PNGs re-embedded by patch_code.py.
## Tools
- tools/baseexp/test_baseexp.py (SECT=DGRHQLSCO), shoot_baseexp.py / shoot_patrol.py / shoot_carry.py / compose_followups.py, perf_baseexp.py (SET=5 = patrol + hurdle rooms),
  vis_sim.py (guard sight preview), smoke.py, dbg.py.

# v6566-lockeramb — Storehouse bay arrival: two bullies, no locker (Erik t536/t537/t538)
Branch v6566-lockeramb off c1a3b8c (live v6.5.64). Worktree /workspace/lockeramb/wt. Not pushed. No version bump.

## Room
"Racing boss" = Bando Rikiya (Sports Storehouse / Outdoor Track, mb_field). Room = Storehouse · Equipment Bay (sf_bay),
first entry. v6.5.63 (76bfb58) added fldEntryScene: froze every bay foe (stun 1e9), TELEPORTED W.dgF[0] to the
locker mouth (hidden), burst the locker, ran him at Ryo, 1-foe fight. The 2nd roamer kept stun 1e9 forever -> stuck.

## Change
- Locker burst removed entirely (CSS + fldLockBurst/fldEntryLocker/fldFreezeFoes gone).
- While pending (!S.e.entry, Bando not beaten, no refill): fldPop stages the bay's 2 foes on marks mid-room
  (pic 505,430 / 645,430) facing the door, stunned (no roam / no touch). fldArrive('bay') plays the arrival on every
  bay entry: FLD_ARR talk (first time; short version after) -> both "!" -> both walk to Ryo -> one fight with both
  (dgks both keys, ctx.fldEnt).
- Win: dgAfter downs both keys -> bay clear; S.e.entry=1 set only on win.
- Flee: both back on their marks, re-armed; walking within 150px of them (or re-entering) replays (short).
- Loss: Aoi carries you out (existing); next entry replays.
- After Bando: existing refill (dgMarkRefill on exit) brings back the 2 bay roamers, normal roaming (sq_yuto).
- NG+: SAVE.dg is fresh -> pending again.
## Log
- 98888d1 WIP code. tools/lockeramb/test_lockeramb.py **29/29 PASS** (logs: /workspace/lockeramb/test_after.log):
  A fresh: staged pair on marks facing door, no .wlockburst, max step <=60px/100ms and never hidden (no teleport), one fight
    group == [fbay0,fbay1], W.dgFight set, win -> 0 foes (W.dgF + DOM), entry set, controls free, Locker Corridor roamers move,
    bay re-entry and reload stay clear.
  B flee: both back on marks (exactly 2), no replay at distance, walk-up replays short confront -> same 2, win clears.
  C loss: carried to the nurse, re-entry replays with the same 2 (no dups); reload while pending -> fight with both.
  D Bando beaten + exit: 2 bay roamers back, not scripted, roaming (one touch-fought Ryo like live); persists over reload.
  E NG+: field fresh, pair staged, one fight with the 2, win clears.
  F real battle opens after the walk-up (2 foe portraits).
- ch_smoke PASS, ngp_test 104/104, verify_wired PASS (logs in /workspace/lockeramb/logs).
- Media: /workspace/lockeramb/media/before_after_entry_strip.png, before_after_entry.mp4 (live left / branch right),
  live_entry.mp4, branch_entry.mp4. Script tools/lockeramb/shoot_entry.py.
