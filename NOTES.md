# v6564-sukajan — portrait fix (GGD-68 follow-up)
Branch v6564-sukajan off main e1ba0d4, worktree /workspace/sukajan/wt. Never push/publish.
Audit: /workspace/sukajan/REPORT.md, mismatches.png.

## Plan (priority order)
1. dlgFaceStyle prefers painted portrait (ptPaintUrl) over zoomed *_fig.
2. New Punks portrait (Y1) + Y2 Leopard, Y3 Hachimaki, Alley Hustler, Bosozoku Rider repaints.
3. Repaint Goda, Sabu, Nao, Nurse, Sota, Haru to match sprites; Goda reveal/VS/eye screens (introsfx branch).
4. New Obaa Nami + Coach Tatsumi portraits.
5. Own in-engine sprites for 8 shopkeepers.

## Log
- WIP1: dlgFaceStyle -> dlgPaintKey (painted first, *_fig fallback; _kneel/_down = beaten). ptPaintId: c2_punk follows IMG.c2_punk_fig Y look.
  PT_PAINT: c2_punkY1/Y2/Y3 -> c2punk / c2punkleo / c2punkhachi; nami, tatsumi. chAlias swaps PT_PAINT for kurogane/tsukikage in Ch3.
  Obaa Nami's three raw nami_fig heads -> ptFace + ptLift.
  Paintings (GenerateImage 3:4 + existing portraits as style refs + sprite as design ref, LANCZOS 360x480, webp q78 m6). Raws in /workspace/sukajan/work/raw.
- WIP2: 8 shopkeepers get own cel looks via nqOwnLook(id, pre, base) right after their alias() calls (alias keeps name + scale):
  Oda-san nq_udonY <- npc_ramen (whiter cap, dark trousers); Ms. Kanda nq_clerkY <- nq_haru (teal blazer/skirt, black shoes, bob+clip);
  Old Sato nq_bandaiY <- npc_ramen (bald crown, navy happi sleeves, white at the neck); Grandma Fumi nq_dagashiY <- nami (green kerchief, cream blouse, green vest);
  Tome-baa nq_tomeY <- nami (white hair, lilac cardigan); Mr. Hon nq_booksY <- kenta (gray hair, glasses, brown cardigan);
  Pharmacist Ono nq_drugY <- kenta (black hair, glasses, white coat); Gacha Kid nq_gachaY <- npc3_kid (orange tee).
  Tool: /workspace/sukajan/work/shop (recolor.py, specs.py, build.py): per-frame bbox regions + hue/sat/value picks, value-ratio shading. Baked once to world/*.webp, nothing at run time.

## Goda intro screens (v6564-introsfx, /workspace/slam-audition/wt)
goda_reveal / goda_eyes / vs_goda read portraits/goda_angry.webp by id (FFF intro table p: ['goda','angry']), so they pick up the
repaint with no code change. That branch touches index.html only (no portraits/), this branch replaces portraits/goda_*.webp and adds
PT_PAINT/PT_HAS keys + dlgFaceStyle/ptPaintId/chAlias/nqOwnLook hunks that do not overlap its hunks -> merges cleanly either order.
Checked by rendering that branch's screens with this branch's portraits (work/render_goda.py, work/goda_sfx/). The reveal crop [180,236,320]
now cuts the tip of the topknot (face fully in); retune crop y in introsfx if Erik wants the knot in.

## Notes
- Gōda's sprite (mb2_sentoY) wears a rust-brown happi, a white towel over the left shoulder and a white-tied topknot (no hachimaki band);
  the repaint follows the sprite, not the brief's "black happi / towel hachimaki" wording.
- Nurse sprite also wears round glasses, so the repaint has them.
- Ch3: chAlias now also swaps PT_PAINT for kurogane/tsukikage so shared lines show Tatsumi/Nami, not Genji/Tsukikage.
