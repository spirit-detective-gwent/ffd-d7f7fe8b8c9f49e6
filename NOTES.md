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
