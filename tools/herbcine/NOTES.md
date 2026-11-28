# herbcine (Erik t608 / t609)

Branch `v6566-herbcine` off live e4139c5. Tip `c1a55bc`. Not pushed, version not bumped.

## Fixes
- Natural pour: she dips the ladle in the pot lip and pours into the bottle in her hand; no free-floating stream.
- Hand-off: the bottle is parented to Sumire's sprite, then reparented to Ryo's at the same world point. It stays in her hand while she walks.
- Talk bubble follows her (`t.fol = 'sumire'`). Hidden during the cinematic so it doesn't float over the zoomed shot; back on her after.
- Compare / item card: dialogue docks at the bottom whenever a `.dlgcard` is up; portrait and card never overlap. No-card speakers still dock to the top when covered (v6.5.63).
- Skippable cinematic via existing helpers (camera, pour, walk, hand-off, camera back). `HS.g` + `scKill` wrapper clean up on Reset / NG+ / leave.
- Forgiving pot reach (~1 tile, any side) and a Plant / Pick tag. Pot-tag taps walk to the stand and act (never "Move closer"). NPC and door taps are not stolen.

## Tests (recorded, not re-run this pass)
- `tools/herbcine/test_herbcine.py` 24/24 PASS
- s2 167/167, ngp 104/104, verify_wired rc=0 (ckCage note unchanged)
- also: ch_smoke PASS, ch2ov 26/26, healstyle PASS, supply 41/41, herbalist repro PASS
- logs: `/workspace/herbcine/tests/logs/`

## Perf vs live e4139c5
Interleaved live/branch pairs in the herbalist room (clinic idle, talk, lesson). 3 pairs at 1× and at 4×, load gated at 6. Averages:

| scene | 4× fps live | 4× fps branch | 4× heat live | 4× heat branch | d heat | heap live | heap branch |
| --- | --- | --- | --- | --- | --- | --- | --- |
| clinic idle | 59.8 | 59.6 | 29.3 | 29.1 | −0.2 | 58.2 | 59.4 |
| clinic talk | 59.8 | 59.8 | 29.3 | 26.9 | −2.4 | 58.5 | 60.0 |
| lesson | 59.7 | 59.4 | 34.7 | 32.1 | −2.6 | 56.8 | 58.6 |

Gates: rooms 55+ fps, heat no more than +5, memory flat. All held. Raw: `/workspace/herbcine/perf.json`.

## Shots
`/workspace/herbcine/shots/herbcine_before_after.png` — live vs branch for pour, walk/hand-off, bubble, compare-card dock, pot reach.
Sources: `shots/trace_live` (f014, f025, f055, f000), `shots/ph_brew3/p016`, `shots/trace_new4/f039`, `shots/ph_hand3/p008`, `shots/test/dlg_card_1.png`, `shots/test_p/pot_prompt_near.png`.
