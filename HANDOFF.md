# Fox Fire Fist — HANDOFF notes

Shared notes between the assistants who take turns on this game. Only one assistant works at a time.
**Start of every turn:** `git pull`, read this file top to bottom.
**End of every turn / every publish:** add a new entry at the TOP of the log below.
Each entry: date, who, version + commit, what changed (functions/tables touched), half-done work, new rules or decisions from Ernest (with date).
Tag every code edit in index.html with `/* v6.5.xx: ... */` so the other assistant can find and merge it.
Full rules, story and process: see the handoff doc Ernest shared (FoxFireFist_Handoff).

---

## Log (newest first)

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
