# v6.5.66 hotelpull (FFF_HP), Erik t616u to t622u

`hp.js` is injected into index.html between `@@FFF_HP_BEGIN/END`, right after FFF_QS. Re-inject with `python3 tools/hotelpull/inject.py index.html`.
No NQ/QS module lines are edited; everything goes through wrappers: fight, c2Back, c2Pop, c2Frame, dgAfter, ambStrike, ambFx, noticedPack,
c2v2Go, c2v2Men, c2v2Mark, c2v2Sweep, dlgGuard, useDoor.

## Root causes
1. **The street/lobby "freeze, only pinch zoom works, hot phone" lock is a shut-door trap.**
   - The NQ shopfront doors (Kitsune Hotel / udon / motors) are walk-in doorways (TRANS). While their room is shut, their act does nothing.
   - useDoor clears W.doorHold, so on the shut hotel door's lip (rect 1840,776 to 1940,852) intDoorsFrame re-fired useDoor **every frame**.
   - Each fire ran stickEnd(), cleared the path and set v=0, so the joystick died the instant it was touched. Pinch zoom runs before the stick, so it still worked.
   - That is about 60 door acts a second (measured 120 in 2 s on live), which is the heat.
   - SAVE.int {x,y} keeps the position, so a reload near the door re-traps him on the first step.
   - The door stays shut because of 2 below.
   - Fix: a useDoor that did nothing (no fade, dialog or room change) holds the door until Ryo steps off its lip, with a one-time "Locked" toast.
2. **The beaten hotel men came back, the count stayed at 2/3 and the quest never completed.**
   - FFF_QS marks quest crews as KIND 'street', so a win wrote `SAVE.crewDown['c2_nq_c1']`.
   - Once 180 s had passed and Ryo was away (Kissa Gekko), c2v2Sweep deleted `SAVE.dg.c2.f` flags, so the crew respawned.
   - `SAVE.dg.c2.e.nq.cold` stayed behind, so the hotel stayed shut and the journal could never advance.
   - Also, a high-level Alley Cat back attack KO (ambKO) skipped c2Back/nqBack, so no count, no guest thanks and no Aoi line.
   - Fixes:
     - Quest crews are never marked for respawn (c2v2Mark skip, purgeDown).
     - Wins are recorded in `c2S().e.hpWin`.
     - A KO on a quest man or one with a mate becomes a fight at cut HP.
3. **Load-time repair.** Runs from c2Pop and 900 ms after c2Back:
   - Purge the quest crewDown entries.
   - Restore the win flags (hpWin first, else the stage count, preferring the crews named in the old crewDown keys).
   - Drop respawned men whose flag is set.
   - Run NQ.crewSync/chainRepair and FFF_QS.repair, then save.
4. **Global lock guard** (on dlgGuard, every 0.5 s, only while the world is on):
   - Releases busy/cut/dlg/scr/forced/runUp/ambOn/opnOn/dgFight after 8 s with nothing on screen, or 30 s with only a "soft" owner.
   - Clears a dead #nqsting overlay (12 s or older). Before battle, a stale sting is also removed so the cards take taps.

## Tests
`/workspace/pwenv/bin/python3 tools/hotelpull/test_hotelpull.py [hotel alley ko groups turn guard door stick repair]`
(FFD_INDEX=<other>/index.html runs against live). The fixture fixtures/erik_hotel_respawned.json is Erik's state: c1/c2 beaten, flags swept, men back, cold=2, Ryo at the door.

## Final results (branch vs live e4139c5)
- tools/hotelpull/test_hotelpull.py: all sections pass (133 checks). s2 167/167, ngp 104/104 (ngp_test hard-codes port 8977; run via a copy with another port), verify_wired ok, plus amb_check 95, ground 172, gangcam 40, escint 20, ch2ov 26, ch_smoke.
- Perf, 4x CPU throttle, dpr 3, 2 interleaved pairs, medians live / branch (fps; main-thread busy %; heap MB):
  hotel street 59.9 / 59.6; 71.6 / 67.0; 61.7 / 65.0.
  hotel door lip 57.7 / 54.6; 78.4 / 76.7; 58.7 / 59.8.
  2-enemy hotel battle 43.6 / 40.3; 80.2 / 71.9; 57.5 / 57.7.
  The battle is below 55 on both builds under swiftshader at 4x; the branch adds no CPU.
