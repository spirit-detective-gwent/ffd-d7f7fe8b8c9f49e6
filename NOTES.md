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
