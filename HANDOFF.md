# Fox Fire Fist — HANDOFF notes

Shared notes between the assistants who take turns on this game. Only one assistant works at a time.
**Start of every turn:** `git pull`, read this file top to bottom.
**End of every turn / every publish:** add a new entry at the TOP of the log below.
Each entry: date, who, version + commit, what changed (functions/tables touched), half-done work, new rules or decisions from Ernest (with date).
Tag every code edit in index.html with `/* v6.5.xx: ... */` so the other assistant can find and merge it.
Full rules, story and process: see the handoff doc Ernest shared (FoxFireFist_Handoff).

---

## Log (newest first)

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
