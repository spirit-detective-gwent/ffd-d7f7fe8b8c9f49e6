# baseexp results (v6566-baseexp)
## Tests (code tip unchanged since 11d59f1; later commits are tools only)
- test_baseexp 57/57 PASS (logs/t_all.log)
- lane (logs/lane/summary.log): s2 167/167, ngp 104/104, ch_smoke PASS, verify_wired PASS, bond 124/124
- test_supply 41/41 after updating 4 expectations to the approved 9 pairs / 8-room bases (logs/lane2/supply.log)
- amb_check: 1 flaky fail in the lane while the box load was 7 (Art safe-room music credit; Art untouched); rerun 95/95, base also 95/95
- lockeramb: A10 flaked once in the lane; reruns section A 12/12 twice, base 12/12 (logs/lane2)
## Perf set 1 (logs/perf.json) — all spots 59.5+ p95, heat delta within +3.3 at 4x, heap flat

## Perf set 2 (logs/perf2.json; live = c1a3b8c tree, index identical to 2ee7cbf; interleaved, 2 reps per throttle)
| spot | thr | live fps / min p95 / heat / heap | branch fps / min p95 / heat / heap | heat delta |
|---|---|---|---|---|
| cooler_guard | 1x | 60.0 / 59.5 / 4.7 / 59.5 | 60.0 / 59.5 / 4.1 / 59.3 | -0.6 |
| dock_guard | 1x | 60.0 / 59.5 / 5.3 / 59.8 | 60.0 / 59.5 / 4.0 / 59.8 | -1.3 |
| bakery_guard | 1x | 59.9 / 59.5 / 4.1 / 59.9 | 60.0 / 59.9 / 3.9 / 59.8 | -0.2 |
| track_slowed | 1x | 59.8 / 59.5 / 5.0 / 60.4 | 60.0 / 59.5 / 5.1 / 60.2 | +0.1 |
| track_normal | 1x | 60.0 / 59.5 / 5.4 / 55.5 | 59.9 / 59.9 / 5.6 / 60.1 | +0.2 |
| long_walk | 1x | 60.0 / 59.9 / 4.8 / 56.3 | 60.0 / 59.5 / 6.1 / 58.4 | +1.3 |
| cooler_guard | 4x | 59.7 / 59.5 / 12.7 / 59.5 | 59.7 / 59.5 / 10.8 / 59.5 | -1.9 |
| dock_guard | 4x | 60.0 / 59.5 / 14.5 / 59.7 | 59.7 / 59.5 / 13.6 / 59.5 | -0.9 |
| bakery_guard | 4x | 58.0 / 59.5 / 13.9 / 60.1 | 60.0 / 59.5 / 11.8 / 59.6 | -2.1 |
| track_slowed | 4x | 60.0 / 59.9 / 19.6 / 60.2 | 60.0 / 59.5 / 16.1 / 60.0 | -3.5 |
| track_normal | 4x | 59.5 / 59.5 / 16.7 / 60.5 | 60.0 / 59.5 / 17.6 / 60.5 | +0.9 |
| long_walk | 4x | 59.0 / 59.5 / 16.3 / 56.0 | 59.7 / 59.9 / 20.3 / 58.5 | +4.0 |

(set 2's slowed-lap window ran past the end of the slowed lap, so set 3 re-measured it)
## Perf set 3: slowed lap only, 3 s window, slowTo still set at the end in every branch run (logs/perf3.json)
| track_slowed | 1x | 60.0 / 59.9 / 5.4 | 59.7 / 59.5 / 5.4 | +0.0 |
| track_slowed | 4x | 59.7 / 59.5 / 14.9 | 59.2 / 59.5 / 16.5 | +1.6 |
