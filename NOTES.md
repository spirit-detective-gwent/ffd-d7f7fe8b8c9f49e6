# v6564-angry — angry portrait variants (GGD angry)
Branch v6564-angry off main e1ba0d4, worktree /workspace/angry/wt. Never push/publish.
Scratch: /workspace/angry (ref/ = neutral PNGs, raw/ = generated 864x1152, out/ = 360x480 webp, tools/).

## Existing mechanism (main)
- PT_PAINT maps speaker id -> paint id; PT_HAS lists files portraits/<id>_<mood>.webp.
- ptMoodOf(who,opt,txt): opt.mood > kneel=beaten > {shout}/opt.shout=angry (rage if hype) > calm if <id>_calm exists > neutral.
- ptPaintUrl(who,mood): fallback chain, angry -> calm -> neutral. So adding <id>_angry + PT_HAS turns on every
  existing {mood:'angry'} / {shout} NPC line for free.
- dlgFaceStyle(key) (versus/choice boxes) zooms IMG[*_fig]; never painted. Fixed here (and on v6564-sukajan).
- Bosses already had angry/calm/beaten: bando goda gouki jin kagero kaneda kurata mai masa mizuno nails saeki shigure (+kaji, sada).

## Plan
1. Code: ptMoodOf scene rules (PT_ANGRY_SC by scene id, PT_ANGRY_LN text snippets per speaker), versus box -> angry,
   actSay text-aware, lazy per-scene preload of angry files.
2. Paint <id>_angry for every neutral-only NPC except the sukajan set.
3. Sukajan set pending until its neutrals land: c2punk(+Y2/Y3) c2hustler c2boso goda(angry redo) sabu nao nurse sota haru, nami, tatsumi.

## Log
