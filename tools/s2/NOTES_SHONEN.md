# v6566-shonen: arcade fighter -> Shōnen Showdown (Erik t569u)
Branch v6566-shonen off c1a3b8c, worktree /workspace/shonen/wt. Not pushed. No version bump (integration does that).
Edited sources: tools/s2/s2arc_fight.js, tools/s2/s2arc_cab.js, tools/s2/paint_p6.js; spliced into index.html
(S2ARCFIGHT / S2ARCCAB blocks replaced from source; paint_p6 label edited in both places). Note: tools/s2/build.py
does NOT reproduce index.html byte-for-byte at c1a3b8c (healstyle/ginger edits live only in index.html), so splice blocks, don't rebuild.
## What changed
- Visible name: CABS.fighter.n 'Shōnen Showdown', jp 少年対決 (marquee, title, boards, Game Center lists, room cabinet label). Internal id stays 'fighter'.
- Fighter display names (CH[id].n/full): ryo KAZE TENMA, aoi BLUE LOTUS, goda IRON DAIMYO, nails RAZOR REI, masa THE RONIN, jin BLACK COMET. Ids/models unchanged. Board seed initials (JIN, NLS...) unchanged (in-world players).
- Controls: panel = left/right D-pad (stick.dpad) + ATTACK (a) + SPECIAL (sp). Swipe up on the screen, D-pad or bare deck = jump (G.swipeUp).
  Auto-block whenever the player is idle/walking/blockstun on the ground and not in LOCK (0.14 s after an attack ends); no high/low. Chip stays.
  ATTACK chains P > P > K (pAct, chainN). SPECIAL release <0.4 s = mv.sp, >=0.4 s = mv.spf x1.25 (charge ring on the button). Full bar: SPECIAL glows, reads SUPER, press fires mv.su.
  AI: new 'thr' grab (unblockable, close), punishes the player's recovery. AI move list otherwise unchanged.
- HUD: one wide super bar (player), round pips beside the timer.
- Cab shell (shared): stick.dpad, btn.lf (label fn), btn.glow/gc/gcol (halo, drawn only in the open cabinet's frame), btn.ring, 'pan' pointer swipes when G.swipeUp exists, C.mqPx marquee size. Other cabinets unchanged (none set these).
## Tests: /workspace/shonen/test_shonen.py, sim /workspace/shonen/sim/ssim.js, regs /workspace/shonen/regs.sh, perf /workspace/shonen/perf.sh
