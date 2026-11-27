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
