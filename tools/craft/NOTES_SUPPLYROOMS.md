# v6565-supplyrooms — Ch1 supplies by room count, pairs per facility (Erik t512u/t513u)

Worktree /workspace/supplyrooms/wt, branch v6565-supplyrooms off c1a3b8c (live v6.5.64). No version bump. Not published.

## Room count per facility (from code: Object.keys of LIBG/ARTG/CAFG/FLDG/GYMG, safe rooms included)
| facility | rooms |
|---|---|
| Library | 13 (incl. 4 kit-less rooms: Silent Study, Archive, Compact Stacks Gallery, West Stacks; 2 safe rooms) |
| Art & Music Wing | 7 |
| Cafeteria | 4 |
| Sports Storehouse | 4 |
| Gym | 8 |
Main school building (hall/nurse/training/classrooms) is not a facility here: nurse cabinet covers it (other branch).

## Design
- SUP_PAIRS = 6 pairs shared by rooms (largest remainder, min 1 pair each): Library 2, Art 1, Caf 1, Storehouse 1, Gym 1.
- Every safe-room kit holds 1 piece; rest go to random wall cabinets of that facility. Gauze/tape per facility always equal.
- Rolled once per save into SAVE.supLay (added to SAVE defaults so load keeps it). Old saves: pieces already taken under v6.5.64 count.
- Street/mini drops already pick the type you hold fewer of (koDropKind) — unchanged, verified by test.

## Log
- 269db84 WIP code. test_supply 40/40: rooms lib13 art7 caf4 fld4 gym8 -> pairs 2/1/1/1/1; 400 rolls all pairs equal, 400 distinct; real open per facility g==t; reload keeps layout; old save counts taken pieces. Thorough Ch1 mean 21.85 mats (min 18, max 28), 10.7 dressings (was 17.8 / 8.64).
- 5e0edd1 tests. ngp 104/104 (ran a port-8987 copy; 8977 busy), ch_smoke PASS, verify_wired PASS. Shots: shots/library_before.png, shots/library_after.png.
- Library rooms perf (probe/perf_lib.py, live vs branch interleaved, 2 reps, DPR3): 1x all 59.4-60 both; 4x fps 58.0-60 branch / 59.0-60 live; 4x heat medians branch vs live: hall 16.2/16.1, hall kit open 16.1/15.8, foyer 15.3/13.1 (+2.2), safeA kit 12.8/12.6; heap after GC 53.7 = 53.7. perf_lib.json.
- perf_check c1a3b8c vs v6565-supplyrooms (4x, 2 runs, full; perf_report_full.md): all gates PASS except native battle fps 51.9 vs live 56.1 — noise: one branch run had a 9.9 s stall (1909 frames, fps 45.0), the other 58.8; live also had a 3.2 s stall run (53.3). Battle code untouched. Key spots new 59.5-60.0; long walks 59.75/59.85; 4x battle 55.65 vs 55.05; 4x heat (cpu_busy) all new <= old (grounds 67.75/67.3, gym 88.15/88.25, border 86.65/90.5, alley 84.55/94.85, centre 74.35/85.85, battle 62.35/63.6); Ch1 heap 49.8/49.7; soak slope 0.06. Rerunning battle only.
- [parent] battle-only rerun (logs_perf_battle.txt): x4 battle 55.2 vs 55.4 PASS, native 59.3 vs 59.25 PASS; soak 'FAIL' = not run in --only battle (full run slope 0.06). Perf DONE.
- Battle-only rerun (interleaved, perf_report_battle.md): native battle new 59.3 vs live 59.25 PASS; 4x battle 55.2 vs 55.4 PASS (within 3%); 4x battle heat 65.8/66.7 vs 64.8/65.4 (median +1.15). Its "soak FAIL" is only because --only battle skips the soak (empty slope); the full run's soak passed (0.06 MB/battle). => all perf gates PASS.
- Summary: worst fps branch 58.0 (Library safe-room kit open at 4x; live 59.6 same spot), key spots >=59.5, battle 59.3. Worst heat delta +2.2 (Library foyer at 4x); world 4x heat all <= live.

## Erik t521: pinned 7-pair split (5eecbda)
- SUP_PAIRS 7, SUP_PIN { lib 3, gym 1, art 1, caf 1, fld 1 }: Gym is the last boss and the player walks back to the nurse to craft, so Gym keeps 1; the extra pair goes to the Library. Pinned so largest-remainder can never give the Gym 2. Type mix still random per save; each facility gauze == tape.
| facility | rooms | pairs | gauze | tape |
|---|---|---|---|---|
| Library | 13 | 3 | 3 | 3 |
| Gym | 8 | 1 | 1 | 1 |
| Art & Music | 7 | 1 | 1 | 1 |
| Cafeteria | 4 | 1 | 1 | 1 |
| Storehouse | 4 | 1 | 1 | 1 |
- Thorough Ch1: mean 23.93 mats (min 20, max 32), 11.72 dressings (lesson 2, safe kits 6, wall kits 8, minis 4, street 3.93). Found = 14.
- Tests on this code: test_supply 41/41 (pinned split asserted), ngp 104/104, ch_smoke PASS, verify_wired PASS (index.html unchanged since those runs; tree clean at 5eecbda).
- Shot: shots/library_after2.png (Library 3/3, others 1/1; Reading Hall kit opened).
- Library + Gym perf (probe/perf_lg.py, live vs branch interleaved, 3 runs: perf_lg.json, perf_lg2.json, perf_lg3.json). The Gym boots in one of two states on BOTH trees (heap ~50 MB: gym heat ~54-59 at 4x, gym_weight ~48 fps; heap ~54 MB: heat ~12-16, ~60 fps). Live shows the heavy state too (perf_lg3 live 4x: gym_weight 48.7 fps / 54.8 heat), so it's not this branch. Matched-state 4x heat deltas: Gym light weight 16.6 vs 15.5 (+1.1), arena 11.8 vs 11.9, annex kit 14.2 vs 12.5 (+1.7); Gym heavy within +1 / -5; Library hall 17.4 vs 17.2, kit 18.2 vs 18.7, safeA kit 13.7 vs 13.8. Library fps 56.6-60 (one 22.4 stall at the safeA kit, heat 3.3 = starved page; rerun 59.6). Gym fps in the light state 58.7-60 at 4x; heavy-state gym_weight 47-49 on live and branch alike. Heap flat (same two values on both trees).
