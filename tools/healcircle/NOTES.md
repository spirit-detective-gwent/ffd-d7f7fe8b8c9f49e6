# v6566-healcircle (Erik t549u): first-aid heal ring vs perfect hit test

Minigame: `hsBeat()` (HEALSTYLE block, index.html ~57586), opened by `hsUse()` when you tap the remedy slot.
A white ring shrinks onto the gold target; a tap "on the beat" = PERFECT (+5% max HP).

## Cause (live v6.5.64)
The hit test was not spatial at all: it compared the tap's clock time with T (1600 ms), +/-110 ms.
The drawing and that clock disagreed in two ways:
1. `sc(t) = 1 + 1.6*max(0, 1 - t/T)` clamps at 1, so the ring STOPS on the target at T and sits there until T+420.
   From T+110 to T+420 (310 ms, most of the time the ring looks "inside the circle") every tap scored Good.
   The `Math.max(0.55, ...)` in frame() shows the ring was meant to keep closing; the max(0,...) made it dead code.
2. The ring's white line was an OUTER box-shadow (radius 60s..64s) while the gold target was an INSET shadow
   (56..60), so at the perfect moment the white ring sat outside the gold, never on it; and at T-110 (still perfect)
   the ring was ~6.6 px outside the circle.
Not a DPR / canvas-scale issue: it is DOM + CSS transform, and the tap position is not used.

## Fix
One shared value: `HS_BEAT = { R:60, grow:1.6, min:0.55, winMs:110 }`, `tol = grow*winMs/T` (= 0.11).
- Ring white line is centred on radius R*scale (inset+outset 1.5 px).
- Gold band is drawn from R*(1-tol) to R*(1+tol) (`.pz>i`, border-width = band width).
- Hit test `hsBeatHit(shown, tol)`: |scale on screen - 1| <= tol, i.e. ring line inside the gold band.
- Ring keeps closing through the target down to 0.55 (no resting).
Difficulty unchanged: still a +/-110 ms window at the same speed (window was symmetric in code, now in the picture too).

## Tests
`tools/healcircle/test_healcircle.py <wt>`: 28/28 (4 viewports/DPR x edge taps +/-0.6 px x 8 angles, ring-past, live rAF taps).
Shot: `tools/healcircle/shot_healcircle.py` -> /workspace/healcircle/shots/healcircle_before_after.png
