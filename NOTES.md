# v6565-runup (Erik t534): Ch1 sub-boss run-up stalls in place

Branch v6565-runup off c1a3b8c (live v6.5.64). Worktree /workspace/runup/wt. Not pushed.

## Suspected cause (from code read)
- v6.5.63 GGD-22: frame() returns early (no moveRyo / follow) while FFF_SCAM.st.boss is set, to hold the world still during a boss arrival.
- v6.5.64 mizunocam: Ch1 minis (BENT_EASE) set st.ease + st.bridge in bossEnt, and FFF_SCAM.end() keeps st.boss on while bridged, until swirl() clears it.
- So on a first visit (entrance plays) st.boss stays true through miniDialog AND the run-up: walkTo fills W.path but frame() never moves Ryo; runUp's wait() only ends at its timeout lim = max(3 s, d/200 + 1.5 s) -> ~3-5 s running in place, then fight starts where he stands.
