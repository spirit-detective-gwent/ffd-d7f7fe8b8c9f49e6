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

## Results on 0ebdd56 (glow cache) — 2026-11-27 evening ET
perf2.log started at 00:24:29 UTC, the same minute as commit 0ebdd56 (2026-11-28 00:24:29 +0000 / 19:24 ET). Three interleaved 4x dpr3 match reps (labels 3–5) vs live 2ee7cbf, 1-min load under 6:
- match fps avg live 59.1, branch 59.0 (all branch reps 58.6–59.5). Gate 58+ PASS.
- match heat avg live 60.4%, branch 59.5% (delta −0.9). +5 cap PASS.
- heap ~50.6 → 51.4 MB, overlay gone, A._cab null. Memory flat.

final.sh on 0ebdd56 (before costumes): test_shonen 29/29 PASS; ladder sim idle 0 clears, mash mid, smart 5/60 full without continues and 22/30 with continues; t_cab gun/street/shooter/ember errs []; first fighter t_cab errs []; second fighter t_cab failed on G.next() past match 5 (same harness issue on live 2ee7cbf, not a game regression); s2 167 PASS; verify_wired PASS.

## Arcade costumes (Erik t597u, t600u) — arcade sprites only, main-game Ryo/Aoi/Masa untouched
In s2arc_fight.js CH + drawFighter (select, VS, match, title all use the same path). No new loops; extra shapes are drawn only while the cabinet is open.
- Blue Lotus: sailor top #7ec8e8 (was green #24503a), navy waist/pants, white collar with a blue stripe.
- The Ronin: style kimono (indigo wrap, crimson obi, hakama pleats at the hip) and hd kasa (straw cone). Was hivis vest + hardhat. Kick still shows the wrench (keyed off id, not the old style).
- Kaze Tenma (t600u; still named Kaze, not renamed): style openjack (cream sleeveless open jacket, crimson lining, bare arms, dark shirt) and hd tallspike (taller spikes + red headband). Was navy gakuran + short spikes, the Ryo look-alike.
Shot: /workspace/shonen/shots/costumes_before_after.png (Kaze select, Lotus select, Lotus vs Ronin match).

## Costume retest
test_shonen 32/32 PASS (3 new costume checks + previous 29). ngp 104 PASS (also covers 0ebdd56, was not in final.sh).
Short 4x dpr3 match vs live 2ee7cbf, two interleaved reps (labels 6–7), load under 6:
- match fps avg live 59.0 (57.9 / 60.0), branch 58.9 (58.9 / 58.8). Gate 58+ PASS.
- match heat avg live 59.7%, branch 64.9% (deltas +3.4 and +6.9). The +6.9 pair is live7 running cool at 57.1% vs branch 64.0%; branch heat is in the same band as earlier live reps (62–67%). Superfull fps 60.0 vs 59.7, heat +1.9.
- heap branch 50.6 → 51.4 MB, closed clean. Memory flat.
Not pushed. No version bump.

## Title z-order (Erik t604u)
SELECT YOUR FIGHTER is drawn after the big select portrait (same x/y/scale as before: 92, 250, 1.6). No clip, no shrink. Kaze's tall spikes go behind the letters; the title stays fully readable. Same for every fighter.

## Hit feel (Erik t606u)
hitStop() on landed hits. Jab 0.045s, kick/special 0.06s, scaled by dmg/9, cap 0.09s. Blocks 0.03s. Multi follow-ups 0.02s. Super's 0.5s freeze is never shortened. White flash, spark, shake and drum unchanged. Chain finisher (chainN===3) gets 1.2x knockback.
G.step skips bufT / jumpQ / spHold / comboT and stepF while freeze > 0, so a buffered ATTACK or SPECIAL is still there after the pause and the cancel window does not tick away. G.resetCtrl() clears buf/freeze (test hook). G.noHS disables hitstop for before/after strips.

## Tests and shots
test_shonen 36 checks: 35/36 on the first in-page rerun after RESET was cleaned up (SPECIAL tap then passed). The remaining miss was the in-page bot: it reached all 5 matches but the 900s cap ended while the cabinet was still in 'play'. A previous run of the same hitstop build did reach ALL CLEAR. Node ladder: 18/18 full clears with continues, idle player 0/18 (still loses); without continues a smart bot still gets some full clears (3/30).
Shots: /workspace/shonen/shots/costumes_before_after.png, /workspace/shonen/shots/hitfeel_before_after.png.

## Heat, 3 interleaved 4x dpr3 match pairs vs live 2ee7cbf (perf3, load under 6, no other perf)
Pairs 8–10 (costume/title build, before hitstop): heat deltas +6.2, +3.6, +4.0. Median +4.0 (mean +4.6). Under the +5 cap; no draw-cache fix. Both sides ran a bit low on fps this set (live 56.3/59.8/54.8, branch 56.2/55.7/56.1) with the machine warmer (~70% cpu). Earlier quieter sets were ~59 fps.
After hitstop (2 pairs): clean pair live 59.7 fps / 71.6% vs branch 59.2 / 72.8% (heat +1.2). Second pair had a hitch on the branch (51.4 fps, +12.8) then superfull recovered to 58.8. Heap 50.5→51.4 MB, flat.
Not pushed. No version bump.
