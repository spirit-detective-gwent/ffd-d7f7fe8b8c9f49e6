# Fox Fire Fist — HANDOFF notes

Shared notes between the assistants who take turns on this game. Only one assistant works at a time.
**Start of every turn:** `git pull`, read this file top to bottom.
**End of every turn / every publish:** add a new entry at the TOP of the log below.
Each entry: date, who, version + commit, what changed (functions/tables touched), half-done work, new rules or decisions from Ernest (with date).
Tag every code edit in index.html with `/* v6.5.xx: ... */` so the other assistant can find and merge it.
Full rules, story and process: see the handoff doc Ernest shared (FoxFireFist_Handoff).

---

## Log (newest first)

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

