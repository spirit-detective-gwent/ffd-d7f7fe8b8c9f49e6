# GGD-90 eatgame (v6566-eatgame, off c1a3b8c)

Erik (t549u/t550u/t551u): keep tapping, make quick bites a little harder to perfect; soda is the reference; ramen keeps its mechanic with lighter numbers.

## Quick bites (game 'bite')
- Each tap adds `tapP`; above `BITE_FLOOR` (30%) the meter leaks `drain x (fill - 0.3)` per second, so it leaks faster near the top.
- Tiers (`BITE_TIER`, item `tier`): light 0.09 / std 0.078 / heavy 0.075, drain 0.5 for all.
  - light: pudding, candy bar, dango, edamame
  - std: onigiri, melon bread, yakisoba bread, an-toast, sweet roll, yakitori
  - heavy: hot lunch, omurice, karaage
- Win check uses `BITE_FULL` (0.9999) so float sums never need an extra tap (old omurice 0.1 x 10 bug).
- Food art follows the peak (`S.pk`) so eaten bites never grow back; the EAT gauge (`drawBiteGauge`) shows the live fill, the red striped ghost (`S.pg`) of what leaked, a LEAKING label after 0.22 s without a tap, the 70% CLOSE tick and a gold WIN edge.
- `botBite(mode)`: 'good' 6/s, 'lazy' 3/s, 'burst' 1 s at 7/s then 1 s off, 'fail' 3 taps, or a number = taps/s (+-20% wobble).
- `simulate()` accepts those modes and returns pk + tier; `EATG.sim(name, mode, seed)` runs one headless when no overlay is open.

## Ramen (numbers only)
shoyu tapP .05 (20 taps) tapH .075 cool .42; miso .048 (21) / .08 / .40; tonkotsu .045 (23) / .08 / .40.

## Soda: untouched.

## Tests
`node tools/eatgame/eat_test.js [index.html]` (80 checks: tiers at 3/4/5/6 taps/s, lazy, burst, fail; ramen careful/greedy; soda unchanged).

## Perf (eat overlay, iPhone dpr3, interleaved live 2ee7cbf vs branch)
- 4x onigiri held mid-game (3 taps then idle), 4 runs each, 2026-11-27 7:15 PM ET, load 3.3-5.3, another job's perf_check was also running:
  live 54.3 fps / heat 87.2, branch 56.8 / 82.5 (-4.7).
- 4x onigiri leak shot (branch bursty thumb, live 'good' thumb), 4 runs: live 52.1 / 85.8, branch 58.2 / 78.5 (-7.3).
- An earlier 2-run pass on a load-5 box read +10.4 / +5.2; runs spread about +-8 heat, so that was noise. No gauge change was needed.
- 1x: bites 60.0 both; shoyu 59.8 vs 59.2. Memory: 8 open/close cycles +0.43 MB both, canvases 9 both.
- World perf_check c1a3b8c vs branch (world+soak): OVERALL PASS, all key spots 59.7-60, soak slope 0.067 vs 0.062.
