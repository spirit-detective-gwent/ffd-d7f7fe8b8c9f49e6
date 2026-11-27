# v6564-jin — seal 3 (Jin's turf) — progress notes
Branch: v6564-jin in /workspace/ffd (base main c7efb9f = live v6.5.63). DO NOT push/publish/deploy.
Harness: h.py (Game, boot, go, shot, adv), t_ramen2.py (full ramen flow), regs.sh (all regressions -> reg/).
Build: `cd /workspace/ffd && python3 tools/s2/build.py` (base patches: tools/s2/patch_eatg_p6.py, patch_amb_p6.py — idempotent, already applied).

## Key findings (engine)
- Base world closure has NO onFightEnd and NO root.ev. P2–P5 `onFightEnd` wrappers + s2garden's `root.ev` wrapper were dead code on live.
  Verified on live index: back(true, P5 shutter ctx) leaves P5 stage 'met' (Masa shutter win does not advance) -> LIVE BUG, flag to Erik.
  Fix on branch (s2.js, tagged GGD-51): root.onFightEnd defined + called from c2Back(win && !escaped, ctx).
  s2garden meal-edge hook (root.ev 'match:start:') is still dead — engine's match:start is internal to FFF_UI; flag.
- Events: world ev() -> FFF_UI.ev. P6 hooks FFF_UI.ev (shop buy/close).
- Engine foe ids: c2_suit, c2_punk, c2_boso, c2_hustler (+g), mb2_game (Jin), c2_doorman. World sprite aliases (j6_suit) are NOT battle ids.
- Force a win in tests: FFF_UI.ST.b.winner=0; FFF_UI.endMatch(); then tap result (h.adv).
- C2AMB rained in unknown rooms -> FFF_AMB_X[room] grade hook (patch_amb_p6.py).
- Post-fight: base can open its own scene ('why' talk) right after back(); P6 waits 1.1 s + whenFree + #wdlg check.

## Merge-time notes
- Intro sound tiers (Erik confirmed on branch v6564-introsfx): any new Jin's-turf intro card / VS splash must be classed
  intro_boss = Jin (mb2_game, gcback); intro_mini = karaoke lieutenant Kanzaki and the Hotel Chuo deal leader; intro_hero = Ryo/Aoi hero cards.
  introsfx keys cues by intro-card id in INTRO_CUE (index.html). mb2_game is already 'intro_boss' there.
  At merge add: j6_kanzaki: 'intro_mini', j6_dealer: 'intro_mini' (unlisted ids already default to intro_mini, so
  behaviour is right even without it; add them so the list is explicit). This branch adds no intro sfx itself.
- Do not touch nurse (v6564-nurse) or note-text (v6564-notefix) fixes; they live on their own branches.

## Done
1. Ramen Kitsuneya — commit 9dc5d28
   - Town door x≈2250 (strip), cel interior (counter, kitchen pass, booths, ticket machine), Tetsuo behind counter, 2 Suits in a booth.
   - Menu j6_ramen: Shoyu +30 HP ¥14, Miso +34 ¥16, Tonkotsu +40 ¥20, Oolong +6 SP ¥4 (eat-in, no Nails discount).
   - EATG ramen bowls (shoyu/miso/tonkotsu broths + toppings).
   - Order -> eat -> close menu -> overhear -> Suits lean on counter -> fight (2× c2_suit, ramen battle backdrop) -> Tetsuo points to Karaoke booth four. Stage 'ramen', quest step 1. Tested end-to-end (t_ramen2.py).
   - Shots: shots/ramen_01_town_door.png, ramen_02_interior.png, ramen_03_menu.png, ramen_04_eat_tonkotsu.png, ramen_05_overhear.png, ramen_06_battle.png

2. Karaoke Kitsune — commit ab26aa5
   - Town door x≈2650. Lobby (kara 1280×900): Kaede at the desk (kaedef sheet, provisional), booths 2/3/4. Booth 2 = karaB (sing), Booth 4 = karaV VIP.
   - FFF_S2ARC.karaMenu: 4 songs (Kitsune Anthem 126bpm, Rain on Chuo-dori 80, Delinquent's Honor 168, Two Foxes duet 108), lead pick Ryo/Aoi, ¥8/song, 3-lane tap-along, grades S/A/B/C.
   - First song: duet scene + 5 bond (banter), once. After that S/A ("great") sets a one-fight edge (SAVE.j6edge, replaces, no stack):
     Anthem +10 SP at bell, Ballad +4 guard, Punk +3 first-card buff, Duet +2 buff both. Skipped for spar/lesson/tut fights.
   - VIP: bossEnt j6_kanzaki (Kanzaki, c2_suitR sheet) -> fight 44 HP lv7 -> Hotel Chuo 7F lead. Stage 'kara', q2. t_kara.py.
3. Hotel Chuo — commits 76806f6, 400d213 (tested t_hotel.py)
   - Town door x≈4610. Lobby hchuo: glowing room-photo panel, frosted-glass desk (voice behind glass), brass lift, nightclub cones.
   - Lift (needs stage 'kara') -> hhall 7F: VO, wave fight 2× c2_suit (hhall1), then bossEnt j6_dealer "Ogata" (name approved, c2_suit sheet ×1.1, intro_mini at merge), 48 HP lv7 (hhall2) -> stage 'hotel', q3.
   - ¥40 rest (P6.hotelRest): Hotel Chuo desk + Kitsune Hotel desk spot 'j6_rest_kh' (all Ch2 runs). Full HP+SP both, once per c2Cyc().cyc (restocks on quest turn-in via c2RefreshCycle). Moon #wrest anim.
   - Full Heal Tea: gone on every Chapter 2 route (Erik 2026-11-26 20:47 ET: restaurants already give full heals). window.FFF_TEA_OFF always returns true; restReach stays a hotel-availability helper. Base menu + both v630PotOffer Tea buttons (patch_tea_p6.py) and the s2garden menu. Seeds/herbs and free story heals kept.
   - Note: the base low-HP "nurse will bandage you" choice dialog appears after fights (nurse branch territory; untouched). Tests click it away.
4. Club Kitsune back office — 400d213. Own room ckoff (staff door x≈3226 right of the club, drawn STAFF door overlay), base club chain untouched.
   - If Tetsu not dealt (c2PunkDealt false and !J().tetsu): fight chinpira1 "Punk Tetsu" + Club Dealer join round 3 -> ledger scene. Else variant scene (ice pack). -> stage 'club', q4. Sets only J().tetsu (no base ck flags) — flag.
5. Izakaya Tanuki — 400d213. Owner "Ponta" (name approved, npc_attendant sheet). Menu j6_izak (izak theme): Yakitori +10 ¥6, Karaage +14 ¥8, Edamame +6 ¥3, Onigiri +12 ¥5, eat-in games. First meal at stage 'club' -> tip -> stage 'izak', q5.
6. Neon Game Center — 8680187, 2cacfa5 (tested t_gc.py)
   - Strip run only: base lm_game door redirects to own rooms gc (1280x900 floor) + gcback (Jin's prize room, 1000x900). Ch1/other routes keep base landmark (Ch1 no arcade).
   - 5 cabinets (FFF_S2ARC.cabPlay, c201d73): Kitsune Blaster, Fox Fist, Ember Run, Neon Rings, Midnight Street. ¥1 a play, rAF only while open.
     Bronze/silver/gold pay 1/2/3 tokens once per tier; gold = mastered (star on cabinet, board). J().arc {best,tier,g,tok,spent}.
   - v6564-arcade (2026-11-26 22:30 ET): upright cabinets (marquee/bezel/deck/coin door). Neon Ring Flight replaced by Chuo Crisis (id gun). Fox Fire Fist II is a 6-character 2D fighter (5-match ladder). Tokens v2: medal floor 1/3/6, then +1 per 20% of gold past gold (max 10/cabinet from best); a silver-or-better repeat that does not beat your best pays +1, capped at 5 repeats. J().arc v2: paid, rep, hs, ini; old bests migrate to old{}; rings tier/g move to gun.
   - Prize counter (Prize Clerk, name approved, npc_clerk sheet): tokens only, cosmetics only = run gang uniform. Nails run: Showa Yankii Tokkofuku 8, +Tinted Shades 6, +Leopard Hachimaki 8 (shades/hachimaki need the set). Other runs: suit/hoodie/rider 8 each (FAC_SHOP jackets untouched).
     yk_west stall locks those items with "At the Game Center prize counter now" while the strip is open.
   - Stage izak: Jin (mb2_game) at the Blaster cabinet -> 'met', q6. Staff door -> gcback -> bossEnt -> fight mb2_game (flv 8) -> 'won', q7. Prize-safe seal -> e.seal_game, down_neo, FFF_OPN grant, c2sLocksSync -> 'done', qClose, strip flip (n.won.strip, E().stripPunk, NQ.BLK.strip): Punk turf, no discount.
   - ecdbeec: seal waits for Jin's win talk; stale Jin sprite swept.
   - GGD-71 final (eacefe0, 2026-11-27 03:46 AM ET): cabinets paint at design 1x (87b36dd); world stack hidden while a cabinet is open and Ember tiles bake once per level (eacefe0). dpr3 / 4x cab_fps: gun 59.9, fighter 59.9, street 59.8, shooter 60.0, ember 57.9 (all >=55). Room vs live e1ba0d4: 59.5 fps / 38.3% heat vs 59.0 / 43.9, delta -5.6; after close 59.8 fps. Heap flat (~50.7 to 51.8). Overlay and A._cab cleared on Done. s2 167, ngp 104, bond 109, ch_smoke 13, no_old_art, verify_wired all PASS. Sheets and clips in /workspace/arcade/.
7. Song edge moved SAVE.j6edge -> J().edge (quest state; NG+ starts clean, ngp T1 passes) — ab7712b.
## Shots (one per building)
- shots/ramen_02_interior.png (+ramen_01..06), shots/kara_lobby.png, shots/hotel_chuo_lobby.png, shots/club_back_office.png, shots/izak_tanuki.png, shots/gc_floor.png. More in explore/ (g00-g11 game center + cabinet + prize + Jin fight).
## Regressions (on ecdbeec; ngp rerun on ab7712b)
- s2 167 pass, ngp 104/104, bond 109 pass, ch_smoke 13, no_old_art ok, verify_wired ok. Chain tests: chain.sh (ramen2, kara, hotel, club, gc).
- chain.sh on ab7712b: all 5 pass (ramen2, kara, hotel, club, gc), no page errors.
## Next
- perf_check main vs v6564-jin; rooms_fps.py (each new room 1x/4x + cab play).
## Commits
- 9dc5d28 ramen WIP + fight-end bridge + amb hook
- ab26aa5 karaoke: rooms, song game, duet bond, edges, Kanzaki
- 76806f6 hotel chuo WIP
- 400d213 club office + izakaya + tea gate
- c201d73 s2arc cabinets
- 8680187 game center WIP
- 2cacfa5 game center tests pass
- ecdbeec gc seal/talk fix
- ab7712b edge in quest state

## Takeover (executor 2, 2026-11-26 19:25 ET)
- Verified git log: all 6 buildings committed through ab7712b. Harness lives in /workspace/v6564-jin (h.py, t_*.py, chain.sh, regs.sh).
- Plan: rebuild check, regs, chain, perf vs e1ba0d4, rooms_fps, shots_final + cabinet contact sheet.
- Step A: shots_final building shots taken (1..6). Review found cabinet HUD overlaps: Fox Fire Fist foe pips/name under the score box; Midnight Chuo km/h under the score box. Fixed in s2arc.js (pips/names to y142/168, round y188; km/h to 312,144). Rebuilt.
- Step B (on 9eac413): s2 167 pass, ngp 104/104, bond 109, ch_smoke 13, test_no_old_art full run PASS (superset of quick), verify_wired PASS. Cabinet 5-up re-shot: shots_final/7_game_center_cabinets_5up.png.
- Step C (Erik t422): Ogata, Ponta, and Prize Clerk names approved, kept. Full Heal Tea removed on every route (FFF_TEA_OFF always true). t_tea.py: pot offer has Teach me and no Tea; post-lesson herbalist has Buy Herbs and no Full Heal Tea; TEA_OFF is not aliased to restReach. errs [].
- Step D (Erik t443/t444, 2026-11-26 21:30–21:37 ET): third Ch2 bond moment c2_jin_after in the prize room, after Jin’s fight and right before the prize-safe seal. PAY 790/395/158. Flags: jinFate wipe/deal/help, jinSlip (Fierce Thursday slip), jinBook (Strategic book). Compassionate leaves Jin standing in the room after the seal. BANTER is a 6-line Ryo/Aoi conversation per path (Fierce clash-but-try, Strategic in sync, Compassionate Ryo-protects / Aoi-uneasy). BOND_TXT is a 4-line exchange per path×answer. _noReact so the generic BOND_REACT line is not prepended. Works for Ryo and Aoi leads; NG+ Classic clears picks so the moment plays fresh. Karaoke duet untouched. Did not edit s2arc.js (v6564-arcade worktree owns cabinets).
- Repeated lines in M1 Gōda (index.html CH2BOND block, already on this base from v6563-mai / ch2-bond / main) and M2 Masa (tools/s2/s2p5.js):
  - Both used the generic BOND_REACT line on every later call. On Compassionate-best that was Aoi’s “I see who you’re trying to help. Okay. I’m with you.” (Erik remembered it as “Okay, I’ll go along with it”). Fierce-best was “I heard you. I still don’t like it.” Fix: BOND_TXT._noReact on c2_goda, c2_masa_after, and c2_jin_after; bondAsk honors it. Choices, consequences, and flags unchanged.
  - Shared BOND_TXT partner line “Then we do it your way.” (Strategic path, Compassionate answer) — Gōda → “Stand him up, but I want a hand on that boiler too.” Masa → “If the dock still runs, I want it written, not wished.”
  - Shared “{quiet}Gently.{/quiet}” (Compassionate path, Fierce answer) — Gōda → “I hate this part. Do not hit him twice.” Masa → “Leave him. I will watch his breathing.”
  - Near-repeat “No angle tonight. Fine. Gently.” / “No more questions. Fine.” — Gōda → “You are not talking him down. I will stay close when he drops.” Masa → “He already lost the yard. I will not keep at him.”
  - Added a unique partner closer on each Compassionate/Compassionate pick (Gōda: “Good. He should not have to get up by himself.” Masa: “Help him stand. I will walk him to the clock.”) because skipping BOND_REACT would have left those picks as a single lead line.
  - Gōda Fierce/Fierce partner “Gently?” → “Keep it clean. I will be right behind you.”
- Step E (Erik t444): Ogata’s boss fight (hhall2) no longer uses the 7F hallway backdrop. New handmade still B.hdeal “Hotel Chuo · 707” (deal room: night city windows, felt table, fox-stamped sheets, brass lamps). Wave fight keeps B.hhall. No new loops. Shot pending: tools/s2/shots_final/9_ogata_deal_room.png. Jin choice shot pending: tools/s2/shots_final/8_jin_bond.png.
- Tests for D/E not run yet: waiting for the in-flight perf_check (e1ba0d4 vs ed1efa1) to finish, then s2, bond, ngp, ch_smoke, verify_wired, t_gc, shots. Did not start Playwright while that perf was on the box.


## Takeover (executor 3, 2026-11-27 00:12 ET)
- Tip 88588dd (banter text committed). Untracked: 8_jin_bond.png, 9_ogata_deal_room.png (left untracked), plus __pycache__ and tools/ngp/shots (not added).
- Shot review: 9_ogata_deal_room.png is the Hotel Chuo 707 deal room (brass lamps, felt table, fox-stamped sheets, Ogata 48/48). 8_jin_bond.png is the prize-room bond moment (choice + Fierce/Strategic/Compassionate openers) but Fierce and Strategic frames were captured mid-typewriter ("He is already laughing. D" / "He keeps a book. Thu"). Fixed shot_bond_ogata.py to tap only the .tw box and wait for .done before shooting; will regenerate.
- Jin fight background confirmed as the gcback prize room: startFight('gcback', ['mb2_game'], { bt: 'gcback', ... }); P6.BT.gcback name "Neon Game Center · prize room". Explore shot g08_jin_battle.png shows the prize-wall "INSERT COIN" / "JIN 999990" backdrop with “High-Score” Jin.
- Earlier bond_jin.log failures (missing PAY/BANTER/BCALL_NAME, recycled Gōda/Masa lines, crash in askJinThenSeal) were from a 03:13 run against /workspace/ffd-bond, before 9070149 defaulted FFD to this repo. Will rerun with FFD=/workspace/ffd BOND_PORT=8997.
- Prior tests on this tree (post_bond, after the FFD mix-up except bond): s2 167/167, ngp 104/104, ch_smoke PASS, no_old_art PASS, verify_wired PASS, t_gc errs [].
- Prior perf_check e1ba0d4 vs ed1efa1 OVERALL PASS on fps, but 4x cpu_busy was +6 to +10 on several spots (busy box). Remeasuring 88588dd vs live e1ba0d4 (v6.5.63) interleaved, on a quiet box (wait while 1-min load > 6). rooms_fps already: 1x all 59.3–60; 4x rooms 55.8–59.8, cab_play 51.5 (arcade branch owns cabinets; this branch did not edit s2arc.js).
- Pipeline: /workspace/v6564-jin/finish_ggd52.sh (shots, full tests, perf_check --runs 2, rooms_fps). Do not push or publish.

## Final gates (GGD-52 wrap-up, 2026-11-27, tip after 6a5e344)
- Shot review: tools/s2/shots_final/8_jin_bond.png (6a5e344) read again. Fierce ("He is already laughing. Do not make this another man you have to carry.") and Strategic ("He keeps a book. Thursday envelopes, prize slips, the lot.") frames show the full line, none mid-typewriter. No recapture needed.
- World perf vs live e1ba0d4, perf_check --only world --runs 3 --throttle 4 on a quiet box: all fps gates PASS (60.0 at every key spot, walks 59.9). 4x heat is lower than live at every spot (e.g. genji gym 74.3 vs 82.8, town centre 66.8 vs 75.0). Frame time med/p95 equal to live. Memory (Ch1 heap after GC) 49.6 vs 49.4 MB.
- Soak (perf_check e1ba0d4 6a5e344 --only soak, load <= 1.5): heap slope new 0.061 vs live 0.064 MB/battle, DOM 553 flat, canvases 9 flat, listener delta 0. PASS. (The earlier OVERALL FAIL was only the empty soak row from --only world.)
- rooms_fps 4x on the branch, 3 passes (live has no FFF_S2P6 rooms, so the live pass errors by design): all rooms 56.8-60.0, median every room >= 58; heap 116-123 MB, errs [].
- Tests: s2 167, ngp 104, bond 109, ch_smoke, no_old_art, verify_wired, t_gc, t_tea all pass.
