# Fox Fire Fist — HANDOFF notes

Shared notes between the assistants who take turns on this game. Only one assistant works at a time.
**Start of every turn:** `git pull`, read this file top to bottom.
**End of every turn / every publish:** add a new entry at the TOP of the log below.
Each entry: date, who, version + commit, what changed (functions/tables touched), half-done work, new rules or decisions from Ernest (with date).
Tag every code edit in index.html with `/* v6.5.xx: ... */` so the other assistant can find and merge it.
Full rules, story and process: see the handoff doc Ernest shared (FoxFireFist_Handoff).

---

## Log (newest first)

### 2026-11-23 — executor (Grok Bot) — v6.5.59 (local branch v6559-closeup, NOT pushed, NOT published)
- Combo close-up camera ("base" from the prototype) on every Ryo/Aoi/enemy double and triple: 2x push-in on the contact point, fighters redrawn at 2x, HUD blur/dim/vignette, backdrop push-in, per-hit burst + white flash + hurt frame + knock-back, 95 ms freeze 34 ms after each hit, unblurred x1/x2/x3 counter. Code: `cuIn/cuOut/cuBeat/cuDmg` before `comboAnim`; hooks in `comboAnim`, `clashAnim` (cards with 2-3 hits), `chainAnim` (shared camera); `drawFigs` (CU_Z resolution + `pw` white tint); `sparks` follows the camera.
- Setting `ST.set.cam` ('on'/'off', default on, off by default when the device asks for reduced motion). Battle-menu cycle button `#setCam` beside Screen shake; Settings > Display switch; per-save + kept across new games.
- Phone portrait only (skipped in pc-arena and landscape), skipped under fast-forward (`ST.ff`). Signature cut-ins, double moves, Energy and Guard are untouched. Cards with 4-5 hits are not zoomed.
- No A/B/C extras, no music dip.
- Aoi swing fix (commit 0f60f3b): each hit of an Aoi double/triple plays its own ready/cut/follow-through cells from her existing board sheets (`SWING_AOI`, `aoiSwing`, `clip.cells` + `clip.snap` support in `drawBoard`/`drawFigs`); close-up bursts and sparks sit behind her sprite during the camera. Flurry beats now follow the clip's own slash cues.
- Tested: KO right after a close-up combo cleans up (no freeze, no overlays, result screen shows); overworld loads, no console errors.
- Half-done / not decided: Energy and Guard stacking beats (recommendation only, not built).

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
