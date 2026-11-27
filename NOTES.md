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
