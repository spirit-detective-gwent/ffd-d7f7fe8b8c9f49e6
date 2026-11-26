# tools/yk/gangs: Ch2 gangs pass previews (v6.5.63 WIP, ch2-gangs; nothing wired into index.html)
New FFF_YK specs in ../yk.js: ksJin (High-Score Jin), ksBouncer (Black-Suit Bouncer), ksSuit / ksRun (Club Kitsune uniforms A/B),
sabu (Sabu), dpMasa (Foreman Masa), dpRider / dpDock (Depot uniforms A/B). New painter options: suit (V lapels, tie, buttons), foxPin,
crest.k='fox', chain, phones (round the neck), hat (hard hat), mask (bosozoku), plaster, refl/reflK (reflective tape), hair 'bald',
hairCol2 (streaked pompadour), tight, nozig/keepZig/zigCol, glyphs yoru/hashiru. Existing specs bake byte-identical.
Run from a work dir holding ext/ (c2_punk_* sheets extracted from index.html) and yk.js + bake.html, served on 127.0.0.1:8891:
  ./bake2.py ksJin,ksBouncer walk,fig   ->  baked/<spec>_<kind>.webp
  python3 kitsune.py; python3 depot.py; python3 lineups.py kd   ->  /workspace/v6560-review/gangs/*.png
v2 (matched to the dialogue portraits in portraits/*.webp): specs ksJin2, ksBouncer2, ksSuit2, ksRun2, sabu2, dpRider2, dpDock2, dpMasa2. New painter options:
noScar (drops the Punk sheet's cheek scar + fills face holes), clean (light flecks on dark cloth), face2 (clean vector face: jaw/brows/eyes/mouth per portrait,
clears old bangs and hair spikes), skinRe, pin (pinstripes), suit.collar (open collar, no tie), hair 'shag' + hairCol2 tips, part (side-parted swept hair), cap
(baseball cap), hood, zip, pockets, closeV (buttoned coverall), reflV (reflective braces), stubble, crosses (gold cross-stitch rows), cuff (wristbands), headClamp.
  ./bake2.py ksJin2,ksBouncer2,ksSuit2,ksRun2,sabu2,dpRider2,dpDock2,dpMasa2 walk,fig ; python3 lineups_v2.py kd -> kitsune_lineup_v2.png, depot_lineup_v2.png
When wired: delete the old art for these characters from index.html entirely (no fallback to old sheets; see the old/new flicker bug).
