# GGD-75 Alley Cat (branch v6565-alleycat off origin/main c1a3b8c), worktree /workspace/alleycat/wt
Not pushed. Not published. No version bump.
## Findings
- Side takedown = opnTDPlay (index.html ~30512). Normal play uses the Hanabi planted-stance sheet (opnHbSheet) slot 2:
  lead arm stretched by OPN.HB.lunge = 54 frame px (a 1px sleeve column smeared 54 px) -> the long arm in Erik's shot.
- opnTD forces FFF_AMBV=false so the takedown is always a side strike (Ryo teleports beside the man even when he came from above/below).
- After the hit: fin() shows lieEl for 300 ms then removes it -> he stands again -> ambFight -> battle. That is the "stands up then fight".
- Battle has painted lying art IMG[fig+'_down'] (paintedKo) + hideFallenBody; freeOpen spent in afterTurn (line ~8611).
## Plan
1 short arm (tdLunge) + closer. 2 vertical takedowns from <who>_ambv rows. 3 ctx.acDown -> battle opens with paintedKo-style lying pose, rises on first player action.
## Log
- a8165fd short arm: OPN.HB.lunge 54->20, Ryo plants 8/11 px from the man (was further). Side Aoi unchanged (no stretch in her sheet; checked).
- 5834874 vertical takedowns: opnTD allows FFF_AMBV (kill: FFF_ACV=false); opnTDPlay(...,vdir) -> ryoGoV/aoiGoV from <who>_ambv rows; foe poses foldv/kneelv cut in-engine (opnFoePose).
- d4ace30 battle downed opening: ctx.acDown (sneak back takedown, non-KO, non-boss, wave1) -> acDownOpen paintedKo pose, rises (acDownRise) on first play/double/switch/run/tag; map lie stays until #game.on.
- 348c152 snapMap skips visibility:hidden sprites + draws .wlie cels (the swirl showed him standing = Erik's bug).
- f8ce53a from-below stand a step left (back view not crowded); tip fallback (#eFig.ac-down) when no real lying painting.
- 002b592 kneelv redrawn (thighs foreshortened, knees on floor; back view shows soles), foldv squash 0.68.
- Harness: tools/td.py, runv.sh, mkvid.py, strip.py, bt.py, perf_ac.py (from syncbreak perf_sb.py).
## Final chain (0c7299f), results appended below
- 16:13 UTC regen after_ryo_side (td rc=0, world:amb2:dir:right, mkvid /workspace/alleycat/shots/after_ryo_side 100 frames)
- (killed the first final chain after 1 regen; everything is re-run after the one-button change below)
## Added scope (Erik via parent, approved): one button
- 7137060: acTapUp(q) = Alley Cat owned (gskLive && gsk.alley) && opnSnkFoe && !opnSnkNoticed && opnSnkCtx && FFF_AC_TAP!==false.
  ambTap: tap on a man from behind (ambSide back) + acTapUp -> opnSnkStart (crouch in, opnTD); refused -> plain tap ambush.
  ambStrike: via 'tap'/'btn' landing from behind + acTapUp -> opnTD (run-ins 'run', cover c2ev and bumps unchanged).
  Hold no longer starts a sneak (opnHoldKind/opnHoldAny ignore alley unless FFF_AC_TAP===false); Kamikaze/Hanabi holds unchanged.
  FFF_OPN_SNEAK.hold(q) (corners hook) unchanged. Codex + New Move card: "Tap an enemy from behind who hasn't seen you".
- Perf (pre-merge, at 0c7299f; live1 failed on page.goto timeout): grounds fps1 live 60/60 br 59.6/60/60; battle1 fps1 live 56.4/58.2 br 59.8/59.4/60;
  acbattle fps1 live 60/59.2 br 60/58.4/60; heat4 all ~89-99 (CPU saturated at 4x); heap flat 49.6-50.2 MB both. Re-run after merge below.
- One-button Ch1 matrix (dl_hall, real taps, foe facing locked; tools/tap.py, logs /tmp/tap3*.log):
  branch: owned+back+tap = Alley Cat (td, downed opening); owned+back+hold = same Alley Cat (no separate hold path); owned+front+tap = plain front ambush;
  owned+back+run = plain run strike (no Alley Cat); owned+back+walk = no ambush event (plain contact fight, ctx {}); locked+back+tap = plain back tap ambush.
  live: locked back tap / front tap / back run identical to branch locked; live owned+back+tap = plain back ambush (the old hold was needed). Before-unlock unchanged.
- Codex/card shots: shots/codex_alley_{before,after,before_after}.png, shots/card_alley_{before,after,before_after}.png (tools/cx.py, harness-only __alleyCard hook in h.py).
- [7137060] regen after_ryo_side.mp4/_strip.png (td rc=0, , /workspace/alleycat/shots/after_ryo_side 110 frames)
- [7137060] regen after_aoi_side.mp4/_strip.png (td rc=0, , /workspace/alleycat/shots/after_aoi_side 104 frames)
- [7137060] regen after_ryo_back.mp4/_strip.png (td rc=0, world:opn:td:v:up, /workspace/alleycat/shots/after_ryo_back 112 frames)
- Ch2 town (non-quest street, c2_punk standoff crew, peace): branch owned tap / walk-bump / hot+tap / hot+run = no ambush, no Alley Cat, no fight; live identical. Live Ch1 owned+back+walk = same plain contact fight as branch. (tools/c2tap.py, /tmp/c2tap2.log)
- [7137060] regen after_aoi_back.mp4/_strip.png (td rc=0, world:opn:td:v:up, /workspace/alleycat/shots/after_aoi_back 104 frames)
- [7137060] regen after_ryo_front.mp4/_strip.png (td rc=0, world:opn:td:v:down, /workspace/alleycat/shots/after_ryo_front 112 frames)
- [7137060] regen after_aoi_front.mp4/_strip.png (td rc=0, world:opn:td:v:down, /workspace/alleycat/shots/after_aoi_front 111 frames)
- [7137060] test s2 rc=0 RESULT PASS 167/167
- [7137060] test ngp rc=0 104/104 passed
- [7137060] test verify_wired rc=0 NOTE: ckCage speaks as ck_cashier (Cage Cashier portrait). Overworld sprite left unchanged.
- [7137060] test amb_check rc=0 PASS: ambush / safe-room / post-fog music (95 checks)
- [7137060] test ch_smoke rc=0 PASS: Ch1/Ch2 smoke
- [7137060] perf_check c1a3b8c vs 7137060 x4 rc=0 26 PASS / 1 FAIL; OVERALL: FAIL; fails: - FAIL x4 battle fps>=55 and within 3% of OLD: new 45.6 old 54.15 
- [7137060] FINAL3 DONE
- [7137060] perf_check c1a3b8c vs 7137060 x4 (interleaved, 2 runs): 26 PASS / 1 FAIL. FAIL = x4 battle fps>=55 & within 3%: new 45.6 old 54.15 (median). Per run: old 54.0/54.3, new 54.2/37.0.
  The new 37.0 run had an 8.7 s single stall, only 3 turns played and cpu_busy 37.9% (lower than old's 55-62%) = harness stall, not load. Old fails the >=55 gate itself.
  Worst x4 world spot: ch2_town_centre new 59.0 vs old 60.0 (1x gate). Memory flat (49.7 vs 49.8 MB; soak slope 0.064). Rerunning only battle, interleaved, 3 runs.
- [parent] battle-only rerun (perf/perf_battle.log): x4 battle new 55.5 vs old 54.4 PASS, native 59.4 vs 58.9 PASS; soak 'FAIL' = not run in --only battle (full run slope 0.064). Perf DONE.
- [7137060] battle-only rerun (perf_check --only battle --runs 3, interleaved): x4 battle new 55.5 vs old 54.4 PASS; native battle new 59.4 old 58.9 PASS.
  (soak "FAIL" there = soak not in the --only set, empty slope; the full run's soak PASSed at 0.064.) An old native run stalled 11.7 s too -> the earlier 37 fps was a harness stall.
## t518u (Erik): world Alley Cat must be the NEWER standing punch (step in, arm planted straight), not the crouch lunge. Working on it.
- c8d6030 (t518u): map Alley Cat strike = the standing punch. Ryo side: OPN_SH row 1 frame 3 (lead straight from his guard frame = the Nails-lesson punch, T.stand path now always); front: ambv row 0 col 1 step-in (no crouched col 3/4); back: row 2 (standing, arm planted). Aoi: upright (6/4 px crouch dips removed), front hilt strike from row 1 col 2 (no crouched col 3).
  Old crouch lunge = Hanabi's planted wide-stance sheet (OPN_HB slot 2), which the takedown had borrowed. It is Hanabi's art (named HB/Hanabi, no alley label) and stays for Hanabi only; the takedown no longer builds or uses it. OPN.HB.lunge/fist restored to live 54/[284,178] (my earlier 20 had changed Hanabi too). OPN_VFOOT (crouch-cel foot fix) removed (no crouched cels used now). HANDOFF: "OPN_HB = Hanabi only; Alley Cat = OPN_SH row 1 / ambv standing cels".
- before_t518_* = copies of the 7137060 clips (crouch-lunge era), shots/.
- [c8d6030] t518 regen after_ryo_side.mp4/_strip.png (td rc=0, , /workspace/alleycat/shots/after_ryo_side 113 frames)
- [c8d6030] t518 regen after_aoi_side.mp4/_strip.png (td rc=0, , /workspace/alleycat/shots/after_aoi_side 114 frames)
- [c8d6030] t518 regen after_ryo_front.mp4/_strip.png (td rc=0, world:opn:td:v:down, /workspace/alleycat/shots/after_ryo_front 109 frames)
- bo br ch1 ryo (tap): swirl seen, pose=true at 0/600/1500/3000 ms after swirl end, standing fig opacity 0 (shots/raw/bo_br_ch1_ryo_*ms.png)
- [c8d6030] t518 regen after_aoi_front.mp4/_strip.png (td rc=0, world:opn:td:v:down, /workspace/alleycat/shots/after_aoi_front 92 frames)
- bo br ch1 aoi (tap): swirl SWIRL_SEEN True wait_ms 2280; pose=true tip=false standOp=0 pose=true tip=false standOp=0 pose=true tip=false standOp=0 pose=true tip=false standOp=0 
- [c8d6030] t518 regen after_ryo_back.mp4/_strip.png (td rc=0, world:opn:td:v:up, /workspace/alleycat/shots/after_ryo_back 111 frames)
- (regen518 stopped: Aoi code changed to 1ec1ebe mid-run; all 6 re-regenerated below)
- bo br ch2 ryo (api): swirl SWIRL_SEEN False wait_ms 15000; pose=false tip=false standOp=1 pose=false tip=false standOp=1 pose=false tip=false standOp=1 pose=false tip=false standOp=1 
- bo br ch2 aoi (api): swirl SWIRL_SEEN False wait_ms 15000; pose=false tip=false standOp=1 pose=false tip=false standOp=1 pose=false tip=false standOp=1 pose=false tip=false standOp=1 
- [1ec1ebe] t522 regen after_ryo_side.mp4/_strip.png (td rc=0, , /workspace/alleycat/shots/after_ryo_side 120 frames)
- bo live ch1 ryo (api): swirl SWIRL_SEEN True wait_ms 3030; pose=false tip=false standOp=1 pose=false tip=false standOp=1 pose=false tip=false standOp=1 pose=false tip=false standOp=1 
- [1ec1ebe] t522 regen after_aoi_side.mp4/_strip.png (td rc=0, , /workspace/alleycat/shots/after_aoi_side 118 frames)
- bo live ch1 aoi (api): swirl SWIRL_SEEN True wait_ms 2520; pose=false tip=false standOp=1 pose=false tip=false standOp=1 pose=false tip=false standOp=1 pose=false tip=false standOp=1 
- [1ec1ebe] t522 regen after_ryo_front.mp4/_strip.png (td rc=0, world:opn:td:v:down, /workspace/alleycat/shots/after_ryo_front 93 frames)
- bo live ch2 ryo (api): swirl SWIRL_SEEN False wait_ms 15000; pose=false tip=false standOp=1 pose=false tip=false standOp=1 pose=false tip=false standOp=1 pose=false tip=false standOp=1 
- [1ec1ebe] t522 regen after_aoi_front.mp4/_strip.png (td rc=0, world:opn:td:v:down, /workspace/alleycat/shots/after_aoi_front 105 frames)
- [1ec1ebe] t522 regen after_ryo_back.mp4/_strip.png (td rc=0, world:opn:td:v:up, /workspace/alleycat/shots/after_ryo_back 109 frames)
- [1ec1ebe] t522 regen after_aoi_back.mp4/_strip.png (td rc=0, world:opn:td:v:up, /workspace/alleycat/shots/after_aoi_back 109 frames)
- [1ec1ebe] REGEN522 DONE
- [1ec1ebe] battle-open br ch1 ryo (tap ): ; 
- [1ec1ebe] battle-open br ch1 aoi (tap ): SWIRL_SEEN True wait_ms 2940; 0ms pose=true stand=0 600ms pose=true stand=0 1500ms pose=true stand=0 3000ms pose=true stand=0 
- [1ec1ebe] battle-open br ch2 ryo (api ROOM=c2_club FFD_INDEX=/workspace/alleycat/wt/index.html): SWIRL_SEEN True wait_ms 3000; 0ms pose=true stand=0 600ms pose=true stand=0 1500ms pose=true stand=0 3000ms pose=true stand=0 
- [1ec1ebe] battle-open br ch2 aoi (api ROOM=c2_club FFD_INDEX=/workspace/alleycat/wt/index.html): SWIRL_SEEN True wait_ms 2940; 0ms pose=true stand=0 600ms pose=true stand=0 1500ms pose=true stand=0 3000ms pose=true stand=0 
- [1ec1ebe] battle-open live ch2 ryo (api ROOM=c2_club FFD_INDEX=/workspace/release/wt/index.html): SWIRL_SEEN True wait_ms 2940; 0ms pose=false stand=1 600ms pose=false stand=1 1500ms pose=false stand=1 3000ms pose=false stand=1 
- [1ec1ebe] battle-open live ch2 aoi (api ROOM=c2_club FFD_INDEX=/workspace/release/wt/index.html): SWIRL_SEEN True wait_ms 2400; 0ms pose=false stand=1 600ms pose=false stand=1 1500ms pose=false stand=1 3000ms pose=false stand=1 
- [1ec1ebe] test s2 rc=0 RESULT PASS 167/167
- [1ec1ebe] test ngp rc=1   - navigating to "http://127.0.0.1:8977/index.html", waiting until "load"
- [1ec1ebe] test verify_wired rc=0 NOTE: ckCage speaks as ck_cashier (Cage Cashier portrait). Overworld sprite left unchanged.
- [1ec1ebe] test amb_check rc=0 PASS: ambush / safe-room / post-fog music (95 checks)
- [1ec1ebe] test ch_smoke rc=0 PASS: Ch1/Ch2 smoke

## t523 (Erik): Aoi reverted to her BEFORE Alley Cat
- Erik t523: revert Aoi's takedown to the 7137060 animation (low knee sweep -> he kneels -> spin -> hilt), side/front/back; Ryo keeps the 1ec1ebe standing straight.
- Code: aoiGo / aoiGoV restored verbatim from 7137060; slide() keeps Aoi low (r.snk=1) again; go() routes ryo->ryoGo/ryoGoV, aoi->aoiGo/aoiGoV; OPN_VFOOT restored with the aoi entry only (Ryo's standing frames need none).
- Labels: the Ryo inner punch fn `lunge()` -> `plantStraight()`; leadGo* -> ryoGo* (Ryo only again); comments now say Aoi's knee sweep IS her Alley Cat; codex row 'crouch in behind him' -> 'slip in behind him, drop him in one move'. OPN_HB/opnHbSheet = Hanabi only (no alley names there; untouched).

## t527 (Erik): foe gets up as soon as the battle starts
- 54f2764: acDownOpen/tip path call acDownAuto(A): bounded one-shot check (60 ms, gives up at 8 s) waits for #wswirl to go, then 150 ms later acDownRise('start') (0.38 s rise). Flat on the map and through the swirl; standing before you can act. Old triggers (tapSwitch/sbTagGo/tapRun/swap/play) remain, no-ops once up. Kill switch root.FFF_AC_UPSTART=false.
- bo.py now expects: flat on the last swirl frame, 'match:alley:up:start', standing (pose gone, stand opacity 1) by 1000 ms; shots at 0/300/1000/2000 ms after the swirl.
- final527.sh (replaces final523, killed before it ran anything): Aoi 3 clips regen, bo br ch1 ryo/aoi + ch2 club ryo/aoi, test lane at 54f2764.
- [1ec1ebe] perf_check c1a3b8c vs 1ec1ebe x4 (world,battle; interleaved 2 runs): 22 PASS / 4 FAIL; fails: - FAIL x4 ch1_grounds ft_p95 not heavier (<=+10%): new 33.35 old 16.8 ms - FAIL x4 ch2_town_centre ft_p95 not heavier (<=+10%): new 41.65 old 33.4 ms - FAIL x4 battle fps>=55 and within 3% of OLD: new 53.3 old 51.85 - FAIL soak heap not trending up (slope<=0.3MB/battle): new slope [] 
- [1ec1ebe] FINAL522 DONE
- [54f2764] final522 finished; starting final527
- [54f2764] t523+t527 regen after_aoi_side.mp4/_strip.png (td rc=0, world:opn:td:kneel world:opn:td:spin world:opn:td:sweep , /workspace/alleycat/shots/after_aoi_side 102 frames)
- [54f2764] t523+t527 regen after_aoi_front.mp4/_strip.png (td rc=0, world:opn:td:kneel world:opn:td:sweep world:opn:td:v:down , /workspace/alleycat/shots/after_aoi_front 100 frames)
- [1ec1ebe] perf_522 note: 4 FAILs ran under load ~7.9 from other agents' browser/perf jobs (/tmp/perf_* worktrees); x4 battle new 53.3 vs live 51.85 (new faster), cpu_busy (heat proxy) 61.9 vs 65.95; soak 'FAIL' = soak not run (--only world,battle). Rerun queued in perf527.sh (battle, then world, 3 runs, waits load<6).
- [54f2764] t523+t527 regen after_aoi_back.mp4/_strip.png (td rc=0, world:opn:td:kneel world:opn:td:sweep world:opn:td:v:up , /workspace/alleycat/shots/after_aoi_back 96 frames)
- [54f2764] battle-open br ch1 ryo (tap ) rc=0: SWIRL_SEEN True wait_ms 2910; 0ms pose=true stand=1 300ms pose=false stand=1 1000ms pose=false stand=1 2000ms pose=false stand=1  T527 flat_at_swirl=True up=None up_ms_after_swirl=None standing_by_1s=True => FAIL
- [54f2764] battle-open br ch1 aoi (tap ) rc=0: SWIRL_SEEN True wait_ms 2250; 0ms pose=true stand=0 300ms pose=false stand=1 1000ms pose=false stand=1 2000ms pose=false stand=1  T527 flat_at_swirl=True up=None up_ms_after_swirl=None standing_by_1s=True => FAIL
- [54f2764] battle-open br ch2 ryo (api ROOM=c2_club FFD_INDEX=/workspace/alleycat/wt/index.html) rc=0: SWIRL_SEEN True wait_ms 2910; 0ms pose=true stand=0 300ms pose=false stand=1 1000ms pose=false stand=1 2000ms pose=false stand=1  T527 flat_at_swirl=True up=None up_ms_after_swirl=None standing_by_1s=True => FAIL
- [54f2764] battle-open br ch2 aoi (api ROOM=c2_club FFD_INDEX=/workspace/alleycat/wt/index.html) rc=0: SWIRL_SEEN True wait_ms 2460; 0ms pose=true stand=0 300ms pose=false stand=1 1000ms pose=false stand=1 2000ms pose=false stand=1  T527 flat_at_swirl=True up=None up_ms_after_swirl=None standing_by_1s=True => FAIL
- [54f2764] test s2 rc=0 RESULT PASS 167/167
- [54f2764] test ngp rc=0 104/104 passed
- [54f2764] test verify_wired rc=0 NOTE: ckCage speaks as ck_cashier (Cage Cashier portrait). Overworld sprite left unchanged.
- [54f2764] test amb_check rc=0 PASS: ambush / safe-room / post-fog music (95 checks)
- [54f2764] test ch_smoke rc=0 PASS: Ch1/Ch2 smoke
- [54f2764] FINAL527 DONE
- [54f2764] battle-open(t527 v2) br ch1 ryo (tap ) rc=0: SWIRL_SEEN True wait_ms 2880; 0ms pose=true stand=1 300ms pose=false stand=1 1000ms pose=false stand=1 2000ms pose=false stand=1  T527 flat_at_swirl=True up=None up_ms_after_swirl=None standing_by_1s=True => FAIL
- [54f2764] battle-open(t527 v2) br ch1 aoi (tap ) rc=0: SWIRL_SEEN True wait_ms 2430; 0ms pose=true stand=1 300ms pose=false stand=1 1000ms pose=false stand=1 2000ms pose=false stand=1  T527 flat_at_swirl=True up=None up_ms_after_swirl=None standing_by_1s=True => FAIL
- [54f2764] battle-open(t527 v2) br ch2 ryo (api ROOM=c2_club FFD_INDEX=/workspace/alleycat/wt/index.html) rc=0: SWIRL_SEEN True wait_ms 2850; 0ms pose=true stand=0.416829 300ms pose=false stand=1 1000ms pose=false stand=1 2000ms pose=false stand=1  T527 flat_at_swirl=True up=None up_ms_after_swirl=None standing_by_1s=True => FAIL
- [54f2764] battle-open(t527 v2) br ch2 aoi (api ROOM=c2_club FFD_INDEX=/workspace/alleycat/wt/index.html) rc=0: SWIRL_SEEN True wait_ms 2250; 0ms pose=true stand=0 300ms pose=false stand=1 1000ms pose=false stand=1 2000ms pose=false stand=1  T527 flat_at_swirl=True up=None up_ms_after_swirl=None standing_by_1s=True => FAIL
- [54f2764] BO527 DONE
- [54f2764] battle-open(t527 v2) br ch1 ryo (tap ) rc=0: SWIRL_SEEN True wait_ms 2880; 0ms pose=true stand=0 300ms pose=false stand=1 1000ms pose=false stand=1 2000ms pose=false stand=1  T527 flat_at_swirl=True up=None up_ms_after_swirl=None standing_by_1s=True => FAIL
- [54f2764] BO527 ryo-rerun DONE
- [54f2764] perf527 battle start load=5.47
- [54f2764] t527 battle-open verdicts (bo527 + ch1 ryo rerun): all 4 (ch1 dl_hall ryo/aoi via tap, ch2 c2_club ryo/aoi via API) = flat pose on the last swirl frame and at 0 ms, pose gone + stand opacity 1 at 300/1000/2000 ms with NO player input => he rose on his own (acDownRise('start') is the only rise path without input). The script's "FAIL" tag was only because bo.py could not read the battle ST.events (battle ev() writes ST.events, not FFF_UI.ev; ST not reachable from page.evaluate) -> up=None. Treat as PASS. ch1 ryo "empty" capture from final522 = slow harness at load, rerun fine.
- ngp 104/104 on retry (final527) - the final522 rc=1 was a Page.goto 30 s timeout under load ~8 (harness flake). s2 167/167, verify_wired PASS, amb_check 95/95, ch_smoke PASS at 54f2764.
- Shots: shots/battle_open_before_after_ch{1,2}_{ryo,aoi}.png (live 0/1500 vs branch 0/300/1000), battle_open_{before_live,after_flat_0ms,after_standing_1000ms}_ch*_*.png; pair_{ryo,aoi}_{side,front,back}_before_after_strip.png.
