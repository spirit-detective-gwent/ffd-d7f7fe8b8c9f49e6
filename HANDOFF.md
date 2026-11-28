# Fox Fire Fist — HANDOFF notes

Shared notes between the assistants who take turns on this game. Only one assistant works at a time.
**Start of every turn:** `git pull`, read this file top to bottom.
**End of every turn / every publish:** add a new entry at the TOP of the log below.
Each entry: date, who, version + commit, what changed (functions/tables touched), half-done work, new rules or decisions from Ernest (with date).
Tag every code edit in index.html with `/* v6.5.xx: ... */` so the other assistant can find and merge it.
Full rules, story and process: see the handoff doc Ernest shared (FoxFireFist_Handoff).

---

## Log (newest first)

### 2026-11-27 — executor (Grok Bot) — v6.5.65 (commit eb3079c) — LIVE after Erik's OK
Versions: `window.FFF_BUILD="v6565"`, title `.vtag` "v6.5.65", `#ver` text "v6.5.65" (bumped in 269a7c9). Approved by Erik (t606, publish card). Fast-forward c1a3b8c..eb3079c; published commit `eb3079c`. Built on origin/main c1a3b8c (live v6.5.64, published 2ee7cbf).

Merged into `rc-v6565` in this order (each merge is its own commit). Alley Cat was merged last (Erik t531/t532: it finished before the v6.5.65 checks, so it ships in this release).

- **Herbalist re-offer (v6565-herbalist 78eaf23, Erik t493):** the GGD-50 garden wrapper (`wrapMugShop`) replaced `c2SumireMenu` and only showed seeds once you had met Dr. Tsukikage, so the potion lesson was only reachable from the first-meet scene. Now in Ch2 with the recipe not learned it goes to `v630PotOffer()` (later / none / gather / ready). Gather talk: "Teach me" when both herbs are held, a disabled "Teach me · need X" plus the line about what's needed otherwise; "Seeds" is always there.
- **Music stays dimmed after an evolve (v6565-evolvemusic b2ca119, Erik t495):** Genji's lesson scene (`matGenjiDrill`) hushed music at T.focus and only un-hushed it on the T.back timer; tap-skip cleared the timers and left the low-pass + 8% gain in the WebAudio graph for good. `teachMusUp()` / `W.tcMus` owns the hush and lifts it on T.back, in `finish()` and at the start of a superseding lesson.
- **Sync Break in NG+ Ch1 (v6565-syncbreak 7000d1b, Erik t494):** `SB_TYPE1` / `SB_BOSS1` give the Ch1 cast their Sync Break types, read only when `b.sbC1` (world sets `story.sbC1` = assist && ngp && chapter<=1 && !c2On()). First playthrough unchanged. Scoped `.sbboth` chip CSS for a two-icon foe; codex line. Tests: tools/syncbreak/t_sb.py.
- **NG+ quest-complete banner + sound (v6565-ngptracker 3439987, Erik t504):** the v6.5.52 `qBanner` once-guard (`playedDone`, page lifetime, keyed by title) swallowed QUEST COMPLETE and its sound for a whole NG+ run started in the same session. Key is now `ngp<N>|title` in NG+ (plain title on a first playthrough), and `v640NgStart` calls `FFF_QDONE_RESET('ngp')` after `ngBuild`. Harness: tools/ngptracker/.
- **Street takeovers / corners (v6565-corners 2528545, Erik t487/t488/t492/t501):** new `FFF_QS` module (IIFE right after C2BT; `/workspace/corners/qs/qs.js` is an older copy, index.html is the truth). After Four Corners every quest street (udon block, Wagashi east X3, west side street X2, Hotel Row top, west wall, Kitsune-no-Yu door) purges roamers, c2ev scenes (EX_RECT), clash/standoff extras and their `p_*` respawns; scripted quest crews are held (gangPeace) with red pins. **UI (t501):** no yellow "Take the corner" tag and no red chip — the standard walk-up touch starts the whole-crew fight, and each win pops the Ch1 side-quest tracker (`n9Slam` 1/3, 2/3 …) from the 1 Hz sweep, then the quest's own QUEST COMPLETE banner; the journal count line stays. 3.5 s touch immunity after a win; two friendly Punks posted per won street. 13u: both rivals' lookouts on the udon block, c2_udon backdrop, `udonBeat` follows the fought corner; `chainRepair()` / `QS.repair()` fix the ambKO hole and mid-quest saves. Non-quest streets keep the Ch2-entry greeting and no ambush. Not built (Erik's call): udon cart, gang-skill ambush on non-quest streets (hook: `qsTags` / `QS.held`). Verified on the rc with the ngptracker guard (t11): count slams + QUEST COMPLETE fire on a first run and in NG+; the guard still drops a same-run repeat.
- **Nurse cabinet (v6565-nursecab 45bb7f8, Erik t506–t511):** the Ch1 white cabinet restocks once after each Ch1 MAIN quest (relays + Gouki; not side quests): 1 Clean Gauze + 1 Medical Tape = one Dressing Cart. No timer, no stacking (`SAVE.cabR` 0/1, NG+ fresh), text shows the amount; `cabQuestDone(id)` from `qDoneNow` and the Gouki path. When empty, `CAB_EMPTY_IMG` (#wcabempty) covers the painted packs; they show again while a restock waits and during the dressing lesson fetch (`cabArtSync`). Lesson 1+1 and +12 HP / 90 s unchanged; old `cabT` saves load clean. Test: tools/nursecab/test_cab.py.
- **Supplies by room count (v6565-supplyrooms 8409178, Erik t512/t513/t521):** Ch1 cabinet supplies follow each facility's room count, pinned (`SUP_PIN`, 7 pairs): Library (13 rooms) 3 pairs, Gym 1, Art & Music 1, Cafeteria 1, Sports Storehouse 1. The Gym is pinned to 1 because it is the last boss and the player walks back to the nurse to craft. Each facility's gauze and tape come in matching pairs (always enough for whole dressings); every safe-room kit holds 1 piece, the rest go to random wall cabinets of that facility; the layout is rolled once per save into `SAVE.supLay` (NG+ rolls a fresh one). Old saves count pieces already taken under v6.5.64. Street/mini drops still give the type you hold fewer of (`koDropKind`). Thorough Ch1 is about 24 mats / 11.7 dressings before nurse restocks. Test: tools/craft/test_supply.py; notes tools/craft/NOTES_SUPPLYROOMS.md.
- **Alley Cat (v6565-alleycat de737c8, code 54f2764; Erik t497/t502/t503/t518/t522/t523/t527):** Ryo's map takedown is the standing punch — he steps in and plants the arm straight (`plantStraight()`; side = OPN_SH row 1 frame 3, front = ambv row 0 col 1 step-in, back = ambv row 2), from the side, front or back (`FFF_AMBV` vertical takedowns, kill switch `FFF_ACV=false`). Aoi keeps her original Alley Cat (low knee sweep -> he kneels -> spin -> hilt; `aoiGo` / `aoiGoV`, `OPN_VFOOT` aoi entry only). `OPN_HB` / `opnHbSheet` is Hanabi's sheet only (the takedown no longer borrows it; `OPN.HB.lunge`/fist back to live 54/[284,178]). The fight opens with the man lying down (`ctx.acDown` -> `acDownOpen`, sneak back takedown, non-KO, non-boss, wave 1; `snapMap` draws the `.wlie` cels so the swirl shows him down); he gets up on his own right after the swirl clears (`acDownAuto` one-shot 60 ms check, gives up at 8 s, then `acDownRise('start')` 0.38 s; kill switch `FFF_AC_UPSTART=false`). One button (t503): once Alley Cat is unlocked, a plain tap from behind on a man who hasn't seen you IS the Alley Cat (no hold; hold does the same); front tap = plain front ambush, running = plain run strike, crews of 4+/bosses = normal back strike. Codex and New Move card now say "tap from behind". Harness/notes: tools/alleycat/ (NOTES.md, td.py, tap.py, bo.py v3 battle-open probe).

Merge conflicts: tools/ngp/ngp_test.py `FRESH_OK` (nursecab `cabR` vs supplyrooms `supLay` on the same line) — kept both keys and both comments. index.html auto-merged everywhere.
Verification (rc tip 3281ca7 vs live 2ee7cbf; logs /workspace/rc6565/NOTES.md, /workspace/rc6565/tests/, /workspace/rc6565/perf/):
- Post-Alley-Cat tests: s2 167/167, amb_check 95, ngp 104/104, ch_smoke PASS, verify_wired PASS, bo.py v3 battle-open (ch1/ch2 × ryo/aoi) all PASS (flat at swirl, up:start +159–207 ms, standing by 1 s).
- Full perf_check (2 runs, some overlap with another job): 27/27 official gates PASS. Native key spots 58.75–60.0 (live 57.8–60.0), battle 59.65 vs 59.5, long walks 59.8 / 59.0 (live 59.85 / 59.35), x4 battle 56.7 vs 56.4, gym p95 16.8 = 16.8, Ch1 heap 49.8 vs 49.7, soak 0.059 vs 0.063 MB/battle.
- A later 3-run world/battle `--only` reported soak `slope []` FAIL: that is a tool bug (perf_check drops soak from the plan when `--only` is set, then the gate reads an empty list). Real soak is the full-run pass above.
- 4× heat, official 2-run medians, looked high on ch1_grounds (+13.9) and genji_gym (+7.3). A 3-run world recheck still read grounds 70.6→79.6 (+9.0) and gym +4.4. A clean 4-run 4× recheck of just those two spots, interleaved vs live, no other perf, load ~2: grounds heat 80.75 live vs 80.25 rc (−0.5), fps 58.45 vs 57.95; gym heat 98.05 vs 97.8 (−0.2), fps 50.9 vs 53.45 (both trees CPU-saturated, p95 33.3). Verdict: the earlier +9 was run-to-run / box noise, not a real rc regression. No merge bisect.
- Rooms: Library 4× 58.9–60 fps, heat within ~+3 of live. Gym Weight Room has the known two-state load on BOTH trees (live also ~48–49 fps / high heat in the heavy state) — judge vs live, not the 55 gate. Nurse's office 59–60 fps, 4× heat at or under live.
Published commit: _(fill in after publish)_
Notes, logs and harness copies: /workspace/rc6565/NOTES.md, /workspace/rc6565/tests/, /workspace/rc6565/perf/.
**Not published. Waiting on Erik's explicit OK before anything is pushed to main.**

### 2026-11-27 — executor (Grok Bot) — v6.5.64 (commit 2ee7cbf) — LIVE after Erik's OK
Versions: `window.FFF_BUILD="v6564"`, title `.vtag` "v6.5.64", `#ver` text "v6.5.64" (bumped in aab258d).
Approved by Erik (t475u). Fast-forward onto e1ba0d4 (v6.5.63). Published commit `2ee7cbf`; origin/main is `2ee7cbf` and the build strings read v6564 / v6.5.64.

What shipped (merged into `v6564-rc` in this order; each merge is its own commit):

- **Gym ring, Flip lean, Nails lesson (ch2-fixes, GGD-25/26/27):** the Kurogane sparring battle backdrop is a boxing ring (ropes sway on hits, three hanging lamps, dust only in the lamp shafts; reduced motion = painted ropes); fighters stand inside the ropes and the HUD plates are not lifted. Flip waits leaning with his back on the café tree trunk (`GK_CURB` [2226,2712], in front of the canopy). The Nails Alley Cat lesson no longer freezes (the demo aimed at a ghost target with no element): Ryo practises the takedown on a glowing shadow form, Nails faces straight the whole scene (`n13still`), 20 s watchdog + 15 s stall guard, idempotent grant, reload resumes.
- **Paper-card ink (v6564-notefix):** clean dark ink on paper / washi cards (the stacked outline that smeared the type is gone).
- **Nurse Shiraishi (v6564-nurse):** her name card holds until she says her name; her painted bust shows in choice dialogs.
- **Double-tap at ROUND 2 (v6564-dbltap, Erik t391u):** a double-tap can no longer leave the fight.
- **ESCAPE input lock (v6564-escint):** ESCAPE no longer leaves a stale `W.forced` that locked overworld input; `roam()` safety net restored.
- **Mini-boss reveal camera (v6564-mizunocam):** Ch1 mini-boss reveals (Mizuno and the shared mini path) are centred and eased (`BENT_EASE`), the framing holds through the run-up (`runUpClash`), no snaps.
- **Street/ambush camera (v6564-gangcam):** the overworld camera eases back after street / ambush / pack fights and cancelled run-ups (`encCamRestore`, `encCamHandoffIntoFight`); stale restore finishes are ignored; pinch zoom cancels a leftover restore. Boss / Archive cams untouched.
- **Genji post-lesson camera (v6564-genjicam, Erik t438):** after a lesson spar the gym camera starts centred on Ryo, Aoi and Genji (was at the left).
- **Music (v6564-ambsafe, includes c2music + postfog; GGD-60/61):** Ch2 building themes while a target, per-boss fight themes (incl. Shigure; group boss fights keep the theme via `C2_FOE_BOSS`), seal revert never asks for `c2night`; Ch1 weather clears after the four relay bosses (rain, fog, puddles, warm light) with the `map_post` "Undaunted" track; back-ambush tracks (Ryo "Ready Aim Fire", Aoi "Eighties Action"); Ch1 safe room "Stay the Course"; Nails fight credited as "Bet You Can ver 2". Every CC BY track is in `MUS_CRED` and the credits list.
- **Ch2 opening (v6564-c2intro, GGD-62):** anime-ending shot (they run up the road from behind, camera falls back and tilts up to the town); skyline/neon cached once per play, no full-screen overdraw.
- **Intro SFX and screens (v6564-introsfx, GGD-53):** hero slow-mo punch, mini cinematic shot, boss canyon echo; eyes + VS cues for mini and boss tiers; missing Nails, Gōda, Saeki and Shigure intro screens added (`BENT_REVEAL` / `BENT_BEAT` / `BENT_VS`).
- **K.O. screen (v6564-defeat):** one data-driven K.O. screen for every loss (winner's painted bust and taunt, where you wake, the real cost from `koPlan`, and after a boss / mini-boss the partner's hint from the foe's deck plus where he waits). Spars are free (no yen, no mats). The post-KO nurse gauze + tape handout is gone.
- **Ch1 supply cut (v6564-craft, GGD-65):** street drop 8% with a queued `+1 Gauze` / `+1 Tape` popup; item scarcity removed (old saves load as normal); no Ch1 quest mats; nurse cabinet restock and post-KO 1+1 removed (lesson 1+1 and the free +12 HP / 90 s kept); Ch1 mini first-win is 1 mat (Ch2 minis stay 2); kits are 6 safe rooms × 1 plus 2 wall kits (`WKIT_STOCK`); dressing carry cap 5.
- **Healing redesign (v6564-healstyle, GGD-66):** one remedy slot under your health (tap; the ring closes on the wrap, tap on the meet for +5% max HP; Fine first unless a regular covers the gap); Ch1 Dressing Cart in the nurse's office and Ch2 Brewing Bowl stations with the Fine gauge (needle driven by transform); Kampo lesson + cinematic; garden ginger pots; leftover conversion; clinic cot removed. Hase's post-lesson greeting keeps the Fierce/Strategic Nails line (add-only).
- **Codex remedy pages (v6564-healstyle):** Items & Food → Heals lists Candy bar, Healing Dressing and Kampo Potion; Healing Dressing / Kampo Potion open a detail page with two tabs (Dressing, Kampo) and Heals / Use / Carry / Make / Ingredients sections, built from the live `HS_PCT`, `HS_CAP` and `HS_BONUS` values, with icons.
- **Ch2 town (v6564-ch2ov, GGD-67):** Ban stands on the ground (no float); the Wagashi shop is the ground-floor tenant under the Lucky 7 Arcade frontage (Erik t455); Chiyo's latch/loop fixed; the kissaten doorway is the doorway only, flush with the lane wall (`GK_DOOR` r [2108,2520,2190,2600]); Four Corners ask-around lines.
- **Battle ground lines (v6564-ground, GGD-73):** per-backdrop ground lines (`GROUND` table + `GROUND_DEF` 60 feed `feetPx`; a room's inline `feet:` still wins) so foes stand on the floor in the painted Ch2 stages (13 stages fixed).
- **Portraits match sprites (v6564-sukajan, GGD-68):** painted faces on choice boxes (120% crop), new crew / six / Nami / Tatsumi / Sukajan Punk / Punks recruiter portraits, shopkeepers get their own cel looks (Oda, Kanda, Sato, Hon, Fumi, Tome, Ono, Gacha Kid). Gōda's crop kept as is (Erik t468).
- **Angry portraits (v6564-angry, GGD-72):** angry busts for the NPCs; only explicitly shouted / rage lines get the screen slam, the rest just switch face; opener busts decode off-frame and are idle-warmed (`ptWarmFoes` in `runUp`) so a new face never stalls a frame. Reviewed and signed off by the executor (Erik t471).
- **Jin's turf (v6564-jin, GGD-51/52):** the south Chuo strip — Ramen Kitsuneya, Karaoke Kitsune, Hotel Chuo, Club 707 / Ogata's deal room, Izakaya Tanuki, and the Neon Game Center (plus the back room). Bond scene at the prize safe. Full Heal Tea is removed (no tea for sale at Tsukikage's; greetings and the codex no longer advertise a paid full-heal tea). `j6_kanzaki` and `j6_dealer` use the mini-boss intro cue. Jin's own final gates (4980c6a): soak 0.061 MB/battle, bond shot fully typed.
- **Arcade cabinets (v6564-arcade, GGD-71):** five new Neon Game Center cabinets (Chuo Crisis light-gun, Fox Fire Fist II, Midnight Chuo, Kitsune Blaster, Ember Run) with attract / coin / continue / initials / top-10, token payout, and v1→v2 save migration (rings→gun). Cabinets render at design 1× (fixed 362×500 offscreen buffer; the world stack is hidden while a cabinet is open). Arcade's own final gates are in `/workspace/arcade/NOTES.md`.
- **Integration fixes on v6564-rc:** Masa's depot shutter fight no longer crashes (`fight()` used `mb2_depotg`, which never existed; a foe with no group twin now fights as himself; this was broken on live too). The gym ring foe keeps the approved GGD-25 spot under the new C2BT ground offset (`#fE .fbody{top:-54px}` for `c2_gym`; `test_ground` band for the ring = 140).

Merge conflicts resolved (both sides kept unless noted): ch2-fixes CSS vs C2BT foot offset; gangcam vs mizunocam run-up/fight-start; introsfx `BENT_*` vs mizunocam `BENT_EASE`; defeat vs gangcam wake line; healstyle/craft vs defeat (defeat's K.O. screen and `koPlan` kept, both drop the nurse grant; craft's closed cabinet with the nurse branch's bust); ch2ov `GK_DOOR` + ch2-fixes `GK_CURB`; angry `ptWarmFoes` + mizunocam `runUpClash`. Job NOTES.md files moved to `tools/<job>/NOTES.md`. Jin merge (5a667ba) also conflicted in `index.html` and `tools/s2/s2.js` (codex / clinic / intro tables); follow-up 682249d added `j6_kanzaki` and `j6_dealer` to `intro_mini` and took the remaining Full Heal Tea wording out of Tsukikage's greetings (`C2_TEA_SAY`), the clinic loc line, and the Kampo / Tsukikage codex pages. Arcade merge (481da70) conflicted in `index.html`, `tools/s2/NOTES_JIN.md`, and `tools/s2/s2p6.js` (RC already held the other v6564 jobs in `index.html`; arcade was built on Jin). 6d56523 merged Jin's final NOTES_JIN tip (conflict on `NOTES_JIN.md` only).

Tests on the combined RC tree (tip 6d56523, after Jin + arcade + tea/intro_mini follow-up; /workspace/release/tests/logs2/, lane done 05:11 ET / 10:11 UTC): s2 167/167, ngp 104/104, bond 124/124 (Jin cases included), ch_smoke PASS, no_old_art PASS, verify_wired PASS, amb_check 95/95, c2intro e2e PASS, ground 172/172, healstyle PASS, supply 30/30, ch2ov 26/26, nurse PASS, dbltap 10/10, escint 20/20, mizcam 42/42, gangcam 40/40, t_gc / t_tea / t_kara / t_hotel / t_club all clean, angry func PASS (82 angry files). Arcade regs (s2, ngp, bond, ch_smoke, no_old_art, verify_wired) are that same suite, all rc=0 on this tree. Known harness artifacts, not merge regressions: genjicam 7/8 (empty PERF {} sample, same on that branch); defeat t_spar c1_matspar dict compare fails only because healstyle adds zero keys (leaf/ginger/seed/gseed=0), gauze/tape unchanged; slam_check 5/10 on this RC and on the angry branch itself (stale script from before 957ba4b).
Perf vs live (e1ba0d4) on the combined tip 6d56523 (Jin + arcade included), 4x, after remasure of noisy/contaminated spots: all gates PASS. Native fps: title 59.8 / 59.85, pick 59.7 / 59.9, battle 59.65 / 59.65, ch1_grounds 59.9 / 59.9, ch2_genji_gym 59.65 / 59.95, ch2_chuo_border 60.0 / 58.5 (remeasured 3-run on a quiet box; the full-check live run2 was 14.1 fps / 9216ms hitch), ch2_lantern_alley 60.0 / 60.0, ch2_town_centre 59.15 / 59.35, long walk ch1 59.8 / 59.7, long walk ch2 59.8 / 59.65. Card-pick, battle, rooms and cabinets >=55; walks >=50. 4x heat (cpu_busy_pct, new-old): ch1_grounds -1.0, ch2_genji_gym -6.3, ch2_chuo_border -4.2 (remeasured; a first remasure right after the chain was noisy at +6.0), ch2_lantern_alley -11.15, ch2_town_centre -13.3, battle +1.00, Ban fight +2.9, Wagashi +2.8, town walk +0.4 (remeasured; full-check +5.1 was a 2-run median after Ban + Wagashi on the same page). Worst kept 4x heat is Ban +2.9, all <= +5. Memory flat (Ch1 heap after GC 49.75 vs 49.4 MB; soak slope 0.066 vs 0.061 MB/battle). Intro (incl. Saeki eyes and Shigure reveal) PASS after remasure of Nails reveal 58.9 and Shigure VS 59.2 (full-check 57.6 figures were 2-run noise); x4 battle-start heat +1.1. Angry opener 1x 59.8 vs 60.0, 4x heat +1.4. Jin rooms at 4x 58.8–60.0 (ckoff remasured 60.0; a single 53.2 was contamination). Arcade cabinets at 4x dpr3: 59.0–60.0. Game Center room vs live 59.8 / 60.0 fps, heat 33.3 vs 35.6 (delta -2.3). Full table in /workspace/release/perf/RC_PERF.md.
Review shots: `/workspace/release/review/` including `jin/` and `arcade/` (see `review/INDEX.md`).
Open for Erik: Ch2 three-foe group fights give every foe `GROUP3_HP` (6), the boss too (Kaneda with two hustlers on live, now also Masa at the shutter). Balance call, not changed here.


### 2026-11-26 — executor (Grok Bot) — v6.5.63 (commit c7efb9f) — LIVE after Erik's OK
Versions: `window.FFF_BUILD="v6563"`, title `.vtag` "v6.5.63", `#ver` text "v6.5.63" (bumped in cdcc7f8).
Approved by Erik ("Yes, publish v6.5.63."). Fast-forward onto b15775f (v6.5.62). Published commit `c7efb9f`; live serves v6.5.63 with no console errors. Ch1/Ch2 smoke against the published tree passed; a live boot check also saw v6563 / v6.5.63 and no console errors.

What shipped (v6563-mai at b649f38, plus the version bump):

- **Boss entrance hold (GGD-22, `7be2184`):** the world stays still through a boss entrance, so the hold no longer lets the map keep ticking under the intro.
- **GGD-49 shop and healing rules (`3ded809`):** no bag-heal from Hase's old patch kit / spare tube or yard gauze (defs kept, disabled). Hase sells only tape and gauze at ¥3 (Nails 20% off applies); mugwort stays ¥1; world-found mats stay the cheap path. Depot is onigiri and canned coffee only; Machi Motors: tape, gauze, soda; Ono: tape and gauze. Ch2 supply shops and herb cycles (`c2RefreshCycle`) restock after a quest or side-quest turn-in, never on a KO / gym wake. Restaurants are eat-in only. Chiyo stands at the counter (no walk). The clinic Brass Kettle craft UI is retired; bag crafting is the only bench. Ch1 First Aid no longer sells ready-made bandages. Nurse cabinet 60s cooldown kept by design.
- **S2 frame gating (GGD-37, `25d54f3`):** unused S2 frame work is gated so 4x heat stays fair vs live.
- **Herbalist garden and seeds (GGD-50):** 9 pots in the clinic nook; Dr. Tsukikage sells seed packets (3 seeds for ¥1, up to 3 packets per quest). Plant, tend (she waters between quests), bloom after a quest refresh, then pick. New plant / pick animations for Ryo and Aoi. The yellow window-light pool on the clinic floor is kept (Erik, 2026-11-26).
- **Rare finds:** chance rolls on pick (~6% twice, ~1% three times) can yield yen or a length of tape / gauze, with a toast.
- **Yard map:** the depot Yard map marks the current herb cycle only.
- **Meal edge:** a Clean-plate (or sip) restaurant win grants a next-fight edge; it is a counter, never bag candy. `mealEdge` is kept on load (`5229623`); no migrate-save on the title screen.
- **Pot-tap fix (`77add26`):** tapping a pot walks to that stand and plants it, instead of resolving to the generic Garden spot ("Nothing useful.").
- **Garden toasts (`7cb2f61`):** '¥5 in the dirt.', 'A length of tape in the mud.' / gauze, and 'Need mugwort seeds.' are on the Ch1/Ch2 toast allowlist so they actually show.
- **Seed and mugwort shop icon (`7cb2f61`):** d2 dialog icons (Seeds and Mugwort Bundles, including live's bundle shops) are restored to 40px.
- **Garden tag box removal (`b649f38`):** the pale rounded `.wtag.obj` box around the 3x3 pots is hidden; the Garden spot stays tappable. Sun wash unchanged.

Also in this publish (already merged into v6563-mai, previously unpublished): Seal 2 (Wagashi / Night Runs / Above the Boat / Off Schedule / Masa depot), hand-drawn shop boards, Ch2 bond M1 (`c2_goda`) and M2 at Masa's shutter, Sync Break skipping the rest of the enemy line, Genji "Evolve moves" / "Learn a basic", eating-games bag-use close, NG+ carry whitelist, Ch2 portraits / gang looks / idle sheets, Gray Coats at the shrine, silent Four Corners beacon, and the mid-street ellipsis drop.

Open issues / next:
- Seal 3 (Jin's turf) waits until after this release so Erik can weigh in on the building designs first.
- Ch2 bond M3–M5 are reserved (ids / Journal / PAY) but the scenes are not written yet.
- In tight garden frames Aoi can stand just in front of pot gp8 (draw order, not a gameplay bug).

New rules (Erik, 2026-11-26): shops and herbs restock only after a quest or side quest, never after a knockout; no new bag-heal items (healing is restaurants + crafting); material shops price tape/gauze like food of equal healing value; mugwort stays ¥1; keep the clinic's yellow sunlight pool; remove only the garden tag box.

### 2026-11-26 — executor (Grok Bot) — v6.5.63 GGD-49 shop and healing rules (not published)
Erik’s shop / healing rules. FFF_BUILD was not bumped.

- Bag: no use-to-heal from Hase’s old patch kit / spare tube. Those item defs and menu-icon art stay in the code (`HITEM.patch` / `HITEM.bpart`, `ITEMS.*`, `ICONS.patch` / `ICONS.bpart`) but are disabled (`combat: 1`) — not sold, not usable from the bag. Reserved for combat-only heals later. Yard gauze as a bag heal is gone. Crafted 20% dressings, candy/bandage/potion drops, and restaurant eat-in stay.
- Hase sells only electrical tape and gauze, ¥3 base each (food-equivalent: a dressing is +10 HP ≈ restaurant yen-per-HP × 10 ≈ ¥6 for 1+1). Nails 20% off applies. Mugwort stays ¥1. World-found mats stay the cheap path.
- Depot keeps only onigiri and canned coffee. Machi Motors: tape, gauze, canned soda (no bandage). Ono: tape and gauze only (no bandage/potion).
- Ch2 supply shops (Machi, Ono, Hase, depot) and herb cycles (`c2RefreshCycle`) restock after a quest or side-quest turn-in, never on a KO / gym wake.
- All restaurant menus are eat-in only: Chiyo and udon to-go rows are gone.
- Ms. Chiyo stands at the front of her counter at all times. No walk on Order (the walk dropped fps). Area behind the counter stays blocked.
- Gōda’s Genji-map pin uses the grey X / “stood down” style after he is beaten (`down_bat` on fight win; `c2lDown` also honors a taken rival seal), same as Masa.
- `c2RefreshCycle('wake')` call sites removed (`c2GymWake`, `v640GymTravel`, two g38 gym-wake wraps). Herbs and Ch2 supply shops refill only on main-quest and side-quest turn-ins. Shop buy-counts (`SAVE.shops[id].b`) for Machi, Ono, Hase and the depot are cleared there; other shops never reset.
- Unused depot packing-tape pouch (`ptape`) is gone from the shop catalog. Icon painter left in place, unused.
- Ch1 nurse cabinet (`n9Cabinet` / `SAVE.cabT`) keeps its 60-second real-time cooldown (by design).
- The Ch1 First Aid machine no longer sells bag bandages (`buyBandage` is a no-op). The machine stays in the nurse\'s office and tells you to craft dressings from the Bag. The Ch3 pier fence no longer sells ready-made bandages. Candy, enemy drops, and quest-reward bandages were left alone pending Erik.
- Clinic Brass Kettle craft UI is retired (`c2Kettle` points at Bag crafting; `kBrew` does not brew). Phone Bag crafting is the only bench. The Kampo lesson flavor still uses the kettle. Help and codex copy no longer send you to the kettle to brew.

- Stale copy fixed: mugwort/ginger no longer say they restock “after a knockout”; gauze/tape blurbs no longer claim they lie near the clinic and alley crates or that tape has no shop price.


### 2026-11-26 — executor (Grok Bot) — v6.5.63 ch2-bond (not published, not merged)
Erik previewed c2_goda and asked for: a staged Sato/Tome-baa carry-off (keep the quick cut to the seal), the bondAsk nameplate to say Aoi, a proper kneeling Gōda sprite (the Y sheet’s side head was split), and the post-seal pointer to go east to Masa / Wagashi row (Club Kitsune is optional, Jin’s ground). Seal 2 is Masa. FFF_BUILD was not bumped.

What changed (tip will be this branch HEAD):
- **Carry-off (Fierce):** `stageCarryIn` / `stageCarryOut` in the CH2BOND module. Old Sato (`nq_bandai`) and Tome-baa (`nq_tome`) enter from the boiler corridor (~780, 500), lift the lying sprite (it tracks between them), and walk him back out of the held camera frame. No zoom-out (`FFF_SCAM.st.keep`). Then the slip / rumor / Masa lines, then the existing `c2LmSeal` pry (the transition Erik liked).
- **bondAsk:** `ask()` now treats a question headed “Aoi …” as Aoi. Nameplate and portrait use `asker` and pass `{ speaker:1, name, face }` into `dialog()` so the d2 choice box shows Aoi, not Ryo.
- **Kneel sheet:** redrew `world/mb2_sentoY_kn.webp` (front/left/right heads composited from `mb2_sentoY_idle`, broken gold side-head wiped). Preview: `/workspace/v6560-review/bond/goda_kneel_sheet.png`. Old sheet backed up as `mb2_sentoY_kn_old.webp` in that folder. Back row unchanged.
- **Story pointer (Gōda scene + post-seal only):** all three answers: Gōda names Tetsu as a rumor (“Tetsu sits in Jin’s club, but you can’t touch Jin’s ground yet”) and his last pointer is east to Masa and the Riders at Wagashi row. Path voice stays distinct (VQ + Gōda’s line). `c2LmSeal` when `n===1 && k==='sento'`: Aoi says “Wagashi row. Masa and the Riders.” / `c2sSay` “Wagashi row is next. The club will keep.” Club still opens after the first seal (`c2Bouncer` unchanged). `ckNamed` and the deal’s `ckTip` (Thursday crates, if they optionally visit) stay.
- **M2:** slot moved to Masa’s depot shutter. Id `c2_masa_after`, Journal name “Masa at the shutter”, pay still 760/380/152. `PAY.c2_cheap` is an alias. Scene still comes with seal-2 phase 5.

**Exact strings / functions touched (for a clean merge with the phase-1 journal-to-Masa branch):**
- `bondAsk` → `ask()` (nameplate / `dialog()` args only)
- `BCALL_NAME`, `PAY`, `BOND_CH2` (M2 id/name/pay)
- CH2BOND: `VQ`, `seqFor`, new `stageCarryIn` / `stageCarryOut` / `carryPlace` / `carryTick`
- Nails `c2LmSeal`: only the `n===1` Aoi line and the `c2sSay` call, gated on `k==='sento'`
- `world/mb2_sentoY_kn.webp`

**Left alone (phase 1 / other routes):** `C2LMK` order, Four Corners “next corner” text (may still list Jin’s Game Center until that branch lands), `c2sReveal(1)` (“Loud shirt. Punk Tetsu. Back office…” — not played on Punk Gōda because we replace `c2BossOut`), `c2Bouncer`.

Preview recorded (not in git):
- `/workspace/v6560-review/bond/c2_goda_preview_v2.mp4` (SHA256 90477764d59661d9d9f91b815b1d9b3fcb97fdffac26ade56863be077c2ec471, 255.6s, captioned FIERCE / STRATEGIC / COMPASSIONATE)
- per-answer clips `c2_goda_{fierce,strategic,balanced}_v2.mp4`
- key shots `c2_goda_*_v2.png` (carry-off, carry walk, Aoi nameplate + fixed kneel on `04_bond_choices`, rumor/Masa pointers, seal pry). Missing only the stale `20_strategic_sit_offer` needle (that line is gone).
- kneel preview: `goda_kneel_sheet.png`

**nails-art:** free-soak (`godaSoak` / first Hot soak on the house after the Compassionate answer) plus the existing `FFF_EATG_MILK` hook are now in `/workspace/nails-art/nq/h_shop.js` `sentoMenu`, so a Nails pack rebuild will not drop them. nails-art is not a git repo.

Tests on this branch (re-run after the polish): bond_test 104/104. ngp pending in this entry until it finishes.

### 2026-11-25 — executor (Grok Bot) — v6.5.63 ch2-bond (branch `ch2-bond`, not published, not merged into v6563-mai)
Erik asked for the five Ch2 bond moments (spec `/workspace/v6560-review/ch2_bond_moments.md`). This branch is for him to preview **M1** (`c2_goda`) first. FFF_BUILD was not bumped.

What landed (commits a2a5994 … 9cae616, tip will be this HANDOFF commit):
- **M1 `c2_goda`**: after the Punk/Nails bathhouse fight (`c2BossOut('sento')` when `run_fac==='arc'`), a staged scene on the clay. Aoi asks what to do with a beaten Gōda. Answers: Fierce KO (`godaFate=ko`), Strategic deal (`godaFate=deal`, `ckTip=1`), Compassionate help (`godaFate=help`, Gōda later stands at the bath counter, first Hot soak is free that visit). All three name Tetsu. The pre-fight `c2lm_sento` call is skipped on this route (`bondAsk` wrapper). Lying sprite is held by `c2LieHold` until the scene ends.
- **PAY** for M1–M5 is wired (`c2_goda` 700/350/140, `c2_cheap` 760/380/152, `c2_offer` 820/410/164, `c2_ledger` 880/440/176, `c2_eve` 935/468/187). Grinder still halves chapter ≤2 picks. `c2nq_door` now pays 120/60/24 (same as the other Ch2 landmark calls, not the 118/59/24 default).
- **M2–M5** ids and Journal names are reserved only. Scenes are not written yet.
  - M2 `c2_cheap`: second seal / Cheap Shot unlock (`c2LmSeal` / `C2S_SET.arc[1]`).
  - M3 `c2_offer`: third seal, Genji turn-in or the walk back (`c2sGenjiTurn`).
  - M4 `c2_ledger`: fourth seal, Tetsu’s book in Club Kitsune’s back office (`ckSlip`).
  - M5 `c2_eve`: night before the roof, after the fifth line (`c2sFifth`) and Ban at the door.
- **Journal fix** (live list is `statusBondBlock`, not the dead `bondPane`): `bondCallName` / `bondCallPay` so Ch2 calls show a title and the real PAY, not a raw id or 118/59/24. Also named `dg_gouki` and the Ch3 landmark calls (`c2lm_market` / `pier` / `dock`).
- Tagged `/* v6.5.63 ch2-bond */`. New module between `CH2BOND_BEGIN v6563-bond` and `CH2BOND_END`, inserted just before `C2BG_BEGIN`.

**Merge-back:** the free-soak patch lives in `index.html` (`FFF_NQ.sentoMenu`). It also needs to go into `/workspace/nails-art/nq/` so a Nails pack rebuild does not drop it. The `c2BossOut` / `bondAsk` / `c2LmSeal` / `c2Pop` wrappers are in the CH2BOND module on purpose, so a pack rebuild does not wipe the scene.

Known skips / flags (not done):
- Carry-off on the Fierce answer is narration only (Old Sato and Tome-baa are not staged; the KO sprite fades after the line). The old-folks wave / bigSting was skipped.
- No dedicated “talk to Gōda” spot beyond the counter sprite after Help.
- Do not merge into `v6563-mai` and do not publish until Erik has previewed `c2_goda`.

Preview: `/workspace/v6560-review/bond/c2_goda_preview.mp4` and key-beat pngs in the same folder. Tests: `tools/bond/bond_test.py`.

### 2026-11-25 — executor (Grok Bot) — v6.5.62 (commit b16ca27) — LIVE after Ernest's OK
Ernest asked for the entire ambush mechanic to be removed from the game, every chapter, including Chapter 2 lane jumps (`laneAmb` / `c2v2AmbTick`). Story-scripted and quest fights stay, plus walk-up fights the player starts, and the Ban Shigure losses.
What changed (commits after the D-style dialogue work; versions still v6.5.62):
- `f374478`: `ambCheck` is a no-op after the last (g38) wrap, so Chapter 1 bushes / trees / doorways no longer jump a fight on their own. The world tick still calls it; it just returns.
- `ffc33db`: `c2v2AmbTick` is a no-op, so the three Ch2 lane spots (`p_amb_hus` / `p_amb_pnk` / `p_amb_syn`) never spawn a mid-walk gang. The unused `c2v2Ambush` function is left in place. Visible door crews, street patrols, and the Ch2 events-director walk-ups stay.
- `aba7e33`: the Gameplay "Street ambushes" Fewer/Normal/More row and its click handler are gone. `gpAmbK()` always returns 1, so a leftover `ambRate` in an old save cannot change fight, suspicion, or roam rates.
Quest check: no quest depended on a surprise or lane ambush. The three `p_amb_*` flags are only cleaned after those jump fights. Four Corners border clashes are visible stand-ups, not ambushes, and were left alone. Bath Tax / "the Hustler ambush" (`t_alley`) was already taken out of `C2CREW` in an earlier batch and replaced by the visible Kitsune-no-Yu door crew (`p_g_bath`); this work did not convert that quest. (The Ch2 events director already empties `C2V2.AMBS` when it loads, so the lane tick was already a leftover — it is now hard off anyway.)
Player sneak stays: the Ambush button, behind-foe sneak (`ambTap` / `ambushPick`), Genji's sneak lesson, the Alley Cat Stealth Takedown perk, and the front / back / Alley Cat stings those still use. Shared story-camera code (`#wv` WAAPI, `cuMusic`, `FFF_SCAM`) was not stripped. Only automatic jump-out triggers were removed.
Checks: Chapter 1, all 64 cover spots with force-on, no jump fight and no errors; settings show Enemy strength / Item scarcity / XP mode and no Street ambushes row; leftover `ambRate` few/more still yields `gpAmbK()===1`. Chapter 2, the three lane spots restored and force-on, the no-op tick ran and no gang jumped out; visible event crews still spawn. All 3 Nails door paths (Fierce / Strategic / Compassionate) still open the Kaneda fight on `c2_street` with no page errors. Official `perf_check origin/main` vs `b16ca27` OVERALL PASS (native spots ~60 fps, battle 59.85 vs 59.9, card-pick 59.95, long walks 59.95 / 59.9, x4 battle 55.85 vs 56.25, soak heap slope 0.064 MB/battle).
Approved by Erik. Fast-forward onto def995f (v6.5.61). Published commit `b16ca27`; live serves v6.5.62 with no console errors.

### 2026-11-25 — executor (Grok Bot) — v6.5.62 (commit b16ca27) — LIVE after Ernest's OK
Versions: `window.FFF_BUILD="v6562"`, title `.vtag` "v6.5.62", `#ver` text "v6.5.62" (bumped in e95863b).
Ernest asked for the dark-blue talk box to be translucent so the scene shows through, without white words disappearing on bright tiles, and he disliked B's black scrim behind the words. He picked option D (A's approach, B's lightness).
What shipped (same publish as the ambush removal):
- D-style `#wdlg`: 50% dark-blue wash, no scrim. White quotes are 16.5px / 700 with a 1px 8-way text outline, `paint-order: stroke fill`, and a soft glow. Names and narrator lines get the same outline. Auto gets a solid fill so it stays readable. Full-screen choice overlays (`#wdlg.d2` / `.d3`, shops, versus prompts) keep their own type and veil.
- Auto-dock (`dlgPlace`, `DLG_DOCK_COVER = 0.18`): when a line opens, if a speaker's on-screen bbox overlaps the default bottom slot by more than 18%, or their feet would sit under it, the box docks to the top, under the safe area and clear of the HP/SP HUD (`#wstat`). The slot is chosen once per line and never flips mid-line. Runs after `FFF_SCAM.line()` has started, and again after Auto is added. d2/d3 overlays are skipped.
Commits: `50f826c` CSS, `51e2c66` auto-dock, `e95863b` version bump, this handoff entry.
Checks: Ch1 and Ch2 scenes, Lucky 7 (Ban) battle-adjacent talk, bath-hall typography, herbalist shop, a 2-button choice, and a vending machine — no console errors; choices stayed d2 and were not auto-docked. Preview shots in `/workspace/v6560-review/dlg_final_*.png`. Official `perf_check origin/main` vs the dialogue tip (`43e4fe9`) and vs `b16ca27` both OVERALL PASS.
Not in git (dev only): `index_fffonly.html`, `page.canvas.tsx.txt`.

### 2026-11-24 — executor (Grok Bot) — v6.5.61 (commit 44a0391) — LIVE after Ernest's OK
Versions: `window.FFF_BUILD="v6561"`, title `.vtag` "v6.5.61", `#ver` text "v6.5.61" (bumped in 2d95937).
Approved by Ernest after the previews ("add everything from the previews and then it's finished"; "once you verify everything, you can release it to the live build and update our folder"). Fast-forward onto 62b3c59 (v6.5.60). Published commit `44a0391`; live serves v6.5.61 with no console errors.
What shipped:
- Story camera (`FFF_SCAM`): light frame on scene lines; push / pull / hold / shake / bars on `#wv` (one WAAPI animation, gated by the camera setting). Heavy beats hold the push, then ease out slowly (1.5–2.5s, no snap) when the scene leaves that moment — including Aoi "breaking them on purpose", Gouki's deal, Ryo's "knowing" shake, the school-gate and Four Corners pull-outs, Gōda's seal and defeat, and Ban Shigure's push-in after each loss. A push also turns the world camera onto its target.
- Ambush stings hold the punch-in into the fight and settle behind the board; they no longer zoom out before the battle. A KO eases out slowly.
- Nails path voice (Fierce / Strategic / Compassionate) plus Kaneda's door decision (`BOND_Q.c2nq_door`); pacing marks on the heavy NQ scenes; Gōda's "Thirty years" beat plays before the Tetsu reveal.
- Ban Shigure losses: Ryo and Aoi stay down through Ban's lines and the camera push / hold / ease-out; the fade to Genji's gym waits until the ease finishes, and leftover zoom is cleared in the black. All three Lucky 7 losses still wake at the gym (loss 3 still starts Genji's first lesson).
- Ch2 battle backdrops (`FFF_C2BT`): every Ch2 fight location except the roof gets a procedural cel room (cached still in `#bfxB`, lantern / steam / rain / neon on the existing bfx rAF). Kissa Gekko keeps its own cafe art. Reduced motion is still-only.
- Luminescent Ch2 overworld (`FFF_C2AMB`): grade and bloom cached per room; motes, steam, rain, lanterns, and neon ride the existing `c2Frame` loop (one overlay canvas, no new loop). Roof is skipped; reduced motion is still-only.
Checks before publish: backdrops and overworld ambience confirmed in-game at the key spots; Kaneda door on all 3 bond paths; Gōda boiler, street ambushes, club bouncer, gym spar, and a Ban Shigure loss (alley backdrop, fade, gym wake); `perf_check origin/main` vs HEAD OVERALL PASS (all key spots 60 fps, battle 60.0 vs 59.9, card-pick 59.9, long walks 59.9 / 59.8, x4 battle 57.7 vs 57.2, Ch2 draw items +1, soak heap slope 0.053 MB/battle).
Not in git (dev only): `index_fffonly.html`, `page.canvas.tsx.txt`.

### 2026-11-24 — executor (Grok Bot) — v6.5.60 (commit 4374579) — LIVE after Ernest's OK
Versions: `window.FFF_BUILD="v6560"`, title `.vtag` "v6.5.60", `#ver` text "v6.5.60" (bumped in 14a796c).
Everything below is approved by Ernest and published in one push on top of d3c83e4 (v6.5.59 base). Fast-forward, nothing on main to merge.
What shipped:
- Nails questline (Punk route, NQ module, source in `/workspace/nails-art/nq/*.js`, built by `nq/build.py` into index.html, `root.FFF_NQ`): udon corner → Hold the West Street → Cold Water (Kitsune Hotel door) → Wet Paint (west wall tag crews) → The Door Man (Kaneda) → Gōda's Seal in the boiler room → Gōda names Tetsu, club path opens. Journal steps/pins (`d_quest.js`), self-repairing beats (`chainRepair`, `whenFree` never drops a beat, crew counts derived from beaten flags).
- New interiors: Kitsune Udon, Machi Motors, Kitsune Hotel desk (c2_nq_udon/motors/hotel) with Nails' price (20% off) counters, Ginko stall openings n1–n4 (dagashi, drugstore, used books, gacha + capsule-opening beat).
- Kitsune-no-Yu bathhouse: 13 rooms (bath side A genkan, B changing, C bath hall, D steam corridor, E boiler; staff side U1 laundry, U2 staff kitchen, U3 storeroom, U4 stairwell; upstairs K1 Gōda's room, K2 trophy corridor, K3 altar, K4 drying deck), lore beats per room (ōzeki Kitsuneyama, the knee, father's letter vs the city's CONDEMNED letter, THE LOAN with the gray coats), key/stair/chute gates, fog veils, all dressed in-engine once per entry (`k_dress.js`, `PAINT.sento/sentoU/sentoK`), every tub/large prop solid (collision walk-tested in all rooms + udon/motors/hotel).
- Gōda's crew looks (cel, painted by `FFF_YK` / tools in nails-art `yk.js` + `jobs.py` + `bake.py`): Gōda sumo-sized with top-knot and planted standing pose, Kaneda, bath-house Hustlers (happi, irezumi, haramaki, geta), gray coats (+ own dialogue portrait `world/c2_gray_fig.webp`), 3 Punk variants, bulky Flip.
- Ryo/Aoi yankii overworld outfits (overworld only) sold at the West Street stall (850/800/900 yen).
- Layout: informant + his two gray coats and Ban's lantern post moved to Lantern Alley (informant stays all chapter, by decision), herbalist into the old yakitori building (KAMPO noren/neon), bathhouse in the Fox Mart slot by the station, Fox Mart sign + awning.
- Block-win sting v2 (zoom, ink flood with hot edge, hanko slam, crest flare, brushed block name, turf tally); Kissa Gekko + station quarter turn red only at Gōda's seal.
- Ambush surprise stings (front / back / Alley Cat tiers; Alley Cat reworked as quiet flashiness with slow-mo + freeze); fight waits for the sting.
- Hundred Fist Barrage: rush camera centered on the foe, fists land on chest/chin.
- Ginko Shotengai rebuilt as the big covered shopping street (stall slots reserved, `FFF_GINKO`).
- Fixes: distant brawl punches (v6.5.55 brawl ambience `heardList`) played all chapter after leaving Genji's (bug was on live too) — now only in the Four Corners hearing window, outdoors, no dialog; herbalist no-gang zone follows her new building, quest location text says west end; gray coats no longer show a Hustler portrait.
Checks before publish: real-battle six-quest chain to the seal (no errors/stuck steps), Ch1/Ch2 smoke, room-by-room audio audit (no stray SFX/loops), perf_check origin/main vs HEAD OVERALL PASS (all spots 60 fps; long walk ch2 1% low 57.2 vs 51.0; x4 battle 56.95 vs 57.65).
Not in git (dev only): `index_fffonly.html`, `page.canvas.tsx.txt`.

### 2026-11-23 — executor (Grok Bot) — v6.5.59 (commit b0627a2) — LIVE after Ernest's OK
Versions: `window.FFF_BUILD="v6559"`, title `.vtag` "v6.5.59", `#ver` text "v6.5.59" (bumped in b34c591, checked consistent before publish).
Everything below is approved by Ernest and published in one push on top of 70dbe47 (v6.5.58 base).
What shipped:
- BASE close-up camera on every Ryo/Aoi/enemy double and triple: 2x push-in, fighters redrawn hi-res at 2x, HUD blur/dim/vignette, backdrop parallax push-in, per-hit burst, hurt flinch/knock-back, 95 ms freeze, unblurred x1/x2/x3 counter. Code: `cuIn/cuOut/cuBeat/cuDmg` before `comboAnim`; hooks in `comboAnim`, `clashAnim`, `chainAnim`; `drawFigs`.
- `ST.set.cam` ('on'/'off', default on, off for reduced motion, skipped on fast-forward `ST.ff`); switch in Settings > Display and the battle-menu button `#setCam`; per-save, kept across new games. Phone portrait only.
- Aoi per-hit swings (ready/cut/follow-through cells, `SWING_AOI`, `aoiSwing`, `clip.cells`/`clip.snap`) with cyan blade trail, 0.20 s gaps.
- Ryo 4- and 6-hit cards (Kazan Rush, Hundred-Fist Barrage): one beat, burst and flinch per hit.
- Energy and Guard stacks: flare/meter step per Energy card, shield-ring stamp per Guard card (no zoom).
- Signature banners: names word by word (stamp, brush stroke), final blow in slow motion (last 0.30 s at half speed, ~1.2 s zoom, freeze, music dip).
- JoJo-style rushes via the rush director: Hundred Fist Barrage, Hundred Petal Cut, Spring Tide (Ryo rush, stagger beat, Aoi follow-up, slow-mo finish; split-screen dropped for Spring Tide only).
- Five-Step Cut: camera beat per cut (x1-x5 counter), then slow-mo final blow.
- Detention Slip: spirit-gun camera (fingertip close-ups, charge glow, bounce to the slip, pull-out to the blast).
- Partner doubles: two-color word-by-word names (Ryo fire orange, Aoi cyan) and the showpiece (tag-in camera, split-screen beat, slow-mo final blow, fire+cyan burst) for Burn the Line and Final Bell.
- Final-hit red hurt pose: target holds its existing hurt pose with a red flash through the slow-mo zoom and freeze, then recovers/KOs normally.
- Enemy close-up gate (`cuFor`): story.boss, mb_*, mb2_*, plus enforcer, chinpira1, c2_boss, hall_mon, c3_boss. Regular enemies and mb3_* excluded; own side always.
- Fix: enemy doubles/triples drew Aoi's swing frames and cyan trail (Aoi-only swing was keyed on "not Ryo"); enemies now attack with their own sprite (cb730b0). Chapter 1 library/arts/cafeteria bosses (Mizuno, Mai Kurosawa, Kurata) ship as-is with the lunge.
Commits (oldest first):
- `446be6b` add a Combo close-up camera On/Off setting beside Screen shake (default On, Off when the device asks for reduced motion)
- `7e319a4` add the close-up camera (push-in, per-hit burst, white flash, hurt frame, knock-back, 95 ms freeze) to same-card doubles and triples
- `50be5db` give multi-hit single cards, partner chains and enemy 2-3 hit strings the same close-up
- `b34c591` bump the version (FFF_BUILD and the 3 visible version strings)
- `9305678` add the Combo close-up camera switch to Settings > Display (saved and kept across new games)
- `fe090d1` handoff log entry (local, not published)
- `0f60f3b` Aoi swings once per hit on doubles and triples (a re-sequenced cut pose per hit, her burst behind her sword)
- `2cd38ef` handoff entry covers the Aoi swing fix
- `a11fb19` stacked Energy cards flare and step the Spirit meter per card; stacked Guard cards stamp a shield ring per card (no zoom)
- `b9d4032` signature specials: names come in word by word (stamp, brush stroke, thud per word, about 0.4 s) and the final blow gets a 2.4x close-up with a 200 ms freeze, flash and a music dip (in-engine field finishers only)
- `076bb3c` Aoi per-hit strikes, 0.20s gaps, sword trail, retimed combo audio
- `f95c717` enemy close-up is boss-only (cuFor: story.boss; your own side always); regular enemies keep the normal animation
- `75271de` 4-6 hit cards (Kazan Rush 4, Hundred-Fist Barrage 6) get one beat, burst and flinch per hit inside the same clip window
- `36289c7` fix signature name word gap (spacer class collided with the overworld .wsp sprite class)
- `6a76de4` signature final blow: slow-motion approach (last 0.30 s of the lead-in at half speed) so the 2.4x push-in runs about 1.2 s with the freeze at its peak; music dip covers it; audio cues after the window move out with it
- `2d5789e` Chapter 1 and 2 mini-bosses (mb_*, mb2_*) get the enemy close-up like bosses; regular enemies and Chapter 3 harbor minis stay excluded
- `94e0716` partner double names come in word by word, split between Ryo (fire orange) and Aoi (cyan)
- `9c4b05f` partner doubles showpiece: tag-in camera (push on one, whip to the other), split-screen beat, slow-motion final blow with a 280 ms freeze and music dip, fire + cyan burst (respects cam setting / reduced motion / fast-forward)
- `395d82b` close-up gate also covers the named story fighters that are not flagged mini: Hall Monitor Saeki, Ban Shigure, Punk Tetsu, Kagero, Preceptor Hakuen
- `b0a8ed2` rush director (speed ramp, per-punch hitstop, tight camera, warped sound clock) + Ryo's Hundred Fist Barrage: every punch felt, then the slow-mo final blow
- `cc49496` Aoi's Hundred Petal Cut: tight blade rush, every cut felt, then the slow-mo final blow
- `b68dff0` Aoi's Five-Step Cut: a camera beat per cut (push/shift, trail, flinch, short freeze, x1-x5 counter), then the slow-mo final blow
- `f9785ff` Ryo's Detention Slip: Spirit Gun camera (fingertip close-ups, charge glow, bounce to the slip, pull-out to the blast, slow-mo and a long freeze)
- `9680a11` fix the partner-double hit counter (it used the finisher module's screen scale, which the doubles module does not have)
- `180e131` Spring Tide: Ryo's JoJo-style rush (speed ramp, per-punch hitstop/flinch/echo), a stagger beat, then Aoi's 150 felt cuts and the slow-mo final blow; split-screen dropped for this double only
- `b6d4809` final hit of every signature/double: the target holds its existing hurt pose and red hit-flash through the slow-mo zoom and the freeze (softer warm flash while held), then recovers/KOs normally
- `cb730b0` fix enemy doubles/triples drawing Aoi's swing frames and cyan blade trail (the Aoi-only swing was keyed on 'not Ryo'); enemies now attack with their own sprite
Open issues:
- Enemies have no attack-pose art (battle sheets only have idle/walk/run/hurt/kneel/down). Ernest chose to skip drawing them (2026-11-23); they use the lunge.
- No boss or mini-boss has a signature special in the game (Gouki's big move is Disciplinary Barrage, already close-up).
- Harmless `kfocus` marker left in the rush/spirit-gun camera code.
- A hover tooltip on the double-move button seen in recordings is the browser's, already in the game, not on touch.
New rules (Ernest, 2026-11-23): no push until all moves are done and pass; then one push plus a HANDOFF entry; publish only after Ernest's OK.

### 2026-11-23 — main assistant — v6.5.58 (commit 35573d5) — LIVE
State of the game at handoff start.
- Recent changes (v6.5.55–v6.5.58):
  - Quest-complete jingle only on real side-quest hand-ins; distant fight sound bed toward NW (Chuo) and east (Wagashi) borders.
  - New gym exit lines (Ryo/Aoi hear fighting NW and east; Aoi: "What if it's one of the gangs? It might be a way in.").
  - Nails "Kuroda" uses the approved chibi cel art (tan suit, sunglasses, gold shirt) in every Nails key; toll booth idle moved so his feet are on the floor in front of the desk.
  - Gym cinematic entries snap the camera to the stage (leftover W.pan fix).
  - Ban Shigure: after neck roll (thr 0.55/0.35/0.2) he keeps unlimited turns and plays only double/triple strings until Ryo is KO'd. No one-shot, no 1-HP floor.
  - Flip (lieutenant): own cel sheets on suit-guy body at scale 1.18, teal jacket, blond hair, sunglasses; leans on coat rack painted into Kissa Gekko art and on the cafe door post outside; one trash-talk line per return after a loss.
  - Nails TOLL demo restaged: mark stays down and fades; Ryo/Aoi hide behind the red takoyaki cart; Ryo practices Alley Cat on thin air; camera frames them above the dialogue box.
  - NG+: learned gang skills (SAVE.gsk) carry into Ch1 without the outfit, skipping scripted/tutorial fights.
- Half-done / next up:
  - Ch2 boss retune plan (Ban rematch must be unwinnable without Cover Up, winnable with it). Design stage only.
  - Kagero ending cleanup (keep the "quieter" ending; its first narration line looks doubled) and a Ch2 beat that gives the freight manifest.
  - Ch3 redo with crew reputation system; rename Bilge-Rat Sabu.
  - Lucky 7 Arcade on hold.
- Merge note: the main assistant builds from local source packs, not by editing this index.html. Keep edits small and tagged so they can be merged back.

## GGD-37 / GGD-22 — 4x heat vs live (v6563-mai, after GGD-49)

**Cause (not a new always-on loop):** Official `perf_check` skipall only taps buttons whose text starts with `Skip`, then Close. On live (`b15775f`), the Chapter Two crane-pan Skip does **not** set `W._c2SkipCine`, so the arrival cinematic starts after the trans. Those scenes have no `Skip` button, so official live stays in `#wdlg.on.scene` / `W.dlg` / `W.cut` with no roamers (`dgF=0`) — the overworld is held still, which understates live 4x heat (gym 58, town 48). On mai, trans Skip sets `_c2SkipCine` and `c2Cine` aborts the arrival talk (`c2AbortTalk`), so official mai is already true town idle (roamers running). That skip-behavior difference is the entire official "mai is heavier" gap.

At a fair true idle (skip flags + `c2AbortTalk` on both), mai is **lighter** than live at every official Ch2 spot (~10–16 cpu_busy points), with fewer world DOM nodes (439 vs 498 at the gym) and lower script/recalc. Disabling S2 c2Frame extras on mai did not close the official gap (it was never the 10-point cause). Ch1 4x heat was already even.

**Fixes (look preserved, no new loops, FFF_BUILD not bumped):**
- Seal-2 `c2Frame` hooks no longer call `hookBattle` every frame (still at init + `c2Pop`). Wagashi `flowTick` / crew sync runs only when that quest is on or done (or after the sento seal). Indoor-rain hide runs only when the room changes. Phase 5 chain/paint/turf runs only when `p5Enter()`, and `applySeTurf` applies once.
- C2AMB: cache the overlay size for 500ms (avoids a forced `clientWidth` reflow every frame), only set `display` when hidden, and hide while EATG is busy.
- EATG: pause the hidden world (`W.paused`) for the duration of the eat overlay so eat-anim 4x is not world+minigame stacked.

**Official perf_check:** run with a leftover-talk hush after skipall so live also reaches true overworld idle (same cleanup extra_perf already uses). Do not freeze mai to match stuck live cine.

## Merge ggd50-garden into v6563-mai (274dccc)

Merged `55ddcad` (clinic garden, chance picks, yard map, meal edge) into `25d54f3` (GGD-37 S2 frame gates). Auto-merge was clean. `tools/s2/build.py` re-injected both; FFF_BUILD stays v6562.

Garden adds no `c2Frame` / rAF / interval hook. Clinic pots pop on clinic enter; yard-map pins update on town pop and quest refresh only. GGD-37 gates (no per-frame hookBattle, quest-gated flowTick, rain hide on room change, p5 turf once, C2AMB size cache, EATG world pause) are intact.
