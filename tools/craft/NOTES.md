# v6564-craft — Ch1 crafting supply cut (unpublished)

Worktree branch `v6564-craft` off main `e1ba0d4`. Version not bumped. Not published.
Crafting later moves to stations on `v6564-healstyle`; this branch does not change the crafting UI beyond the dressing-cap message.

## What landed (Erik pt412u)

1. Ch1 street material drop 20% → 8% per foe. `+1 Gauze` / `+1 Tape` popup (queued until the result screen is gone). Ch2 stays 4%. Bosses drop nothing.
2. Item scarcity removed from the menu and the mechanic (`koDropScarce`, `gpItem` scarce, `SAVE.itemScarce`, wkit scarce stock). Old scarce saves load as normal (keys dropped, mats kept, 8% street rate).
3. No Ch1 quest material rewards (Bond XP only). Ch2 `qReward` unchanged.
4. Nurse: white-cabinet restock gone; post-KO 1 gauze + 1 tape gone. One-time dressing lesson (1+1) and free +12 HP / 90 s kept. Reach animation only during the lesson fetch.
5. Ch1 mini-boss first win: 1 material (balanced gauze/tape). Ch2 minis stay at 2.
6. Kits: six safe-room kits are 1 piece each (gauze/tape alternating). Wall kits cut to a fixed stock of two (`WKIT_STOCK = { dl_hall: 'gauze', gy_weight: 'tape' }`); other wall cabinets use the existing empty open + "Nothing else here."
7. Dressing carry cap 5. Crafting stops at the cap with "Dressing bag is full (5). Use one first." Extra materials stay as materials. Saves with more than 5 keep them but cannot craft until under the cap. Potions are unaffected.

Extra source found and neutralised: a later `settle()` wrapper had been granting +1 gauze +1 tape on Ch1 mini and Gouki wins; Ch1 side is now null (Gouki drops nothing; Ch1 minis come only from `healDrops` on first win).

## Kit arithmetic (flag)

The original per-source sketch (6 safe kits × 1+1, ~10 wall kits × 1, lesson, minis, 8% street) summed well above 15–18. Erik asked to drop kit amounts so the thorough-Ch1 total fits 15–18. Chosen layout:

| source | mats |
|---|---|
| dressing lesson | 2 |
| 6 safe-room kits × 1 | 6 |
| 2 wall kits × 1 | 2 |
| 4 Ch1 minis × 1 (first win) | 4 |
| ~48 street foes × 8% | ~3.8 |
| Ch1 quests | 0 |
| **expected total** | **~17–18** |

Alternative of 0 wall kits would land around 16. Safe kits were cut from 1+1 to 1 because leaving them at 1+1 already hits 18 before street drops.

## Tests

- `tools/craft/test_supply.py` **30/30**. Thorough Ch1 (48 street foes, 600 runs): **mean 17.8 materials** (min 14, max 25); mean craftable dressings 8.64. Per-source means: lesson 2, safe 6, wall 2, minis 4, quests 0, street 3.8.
- `tools/yk/ch_smoke.py` **PASS**
- `tools/yk/test_no_old_art.py` quick **PASS** (first run flaked with a closed browser; rerun passed)
- `/workspace/v6560-review/portraits/verify_wired.py` **PASS** (no `verify_wired` in-repo; ran the review copy against this worktree)
- perf vs live: `perf_check.py c7efb9f v6564-craft --throttle 4 --repo /workspace/craft/wt`. `c7efb9f` is the published live tree; `e1ba0d4` only amends `HANDOFF.md` (game `index.html` identical). First run (box busy, a second perf_check in flight) skipped battle / pick / 4×. Rerun **OVERALL: PASS**. Report: `/workspace/perf-check/runs/v6564-craft/` and `/workspace/craft/out/perf_report.md`.

### Perf gates (medians of 2, 390×844 DPR3)

| gate | new | old | result |
|---|---|---|---|
| key spots fps ≥58 | grounds 59.75, gym 60.0, border 59.8, alley 60.0, centre 59.4 | 59.95–60.0 | PASS |
| card-pick fps ≥55 | 59.75 | 59.55 | PASS |
| battle fps ≥55 | 59.7 | 59.8 | PASS |
| long walk fps ≥50 | ch1 59.85, ch2 59.6 | 59.75 / 59.75 | PASS |
| 4× heat (cpu_busy, ≤ +5 pts) | grounds 61.0 (−3.8), gym 81.4 (+2.1), border 75.5 (−6.2), alley 77.9 (−0.6), centre 69.55 (−9.5), battle 60.05 (+1.0) | see old | PASS |
| 4× ft_med / ft_p95 not heavier | 16.7 / ~16.8 ms both sides; 4× battle fps 56.6 vs 56.85 | — | PASS |
| memory flat | Ch1 heap after GC 49.4 = 49.4; soak slope 0.064 MB/battle (old 0.07) | — | PASS |

## Before / after (thorough Ch1)

Measured on the old tree (`e1ba0d4`) vs this branch:

| source | before | after |
|---|---|---|
| street drop rate | 20.2% | 8% (measured ~7.4–8.5%) |
| Ch1 mini first win | 2 (healDrops) + 2 (settle wrapper) | 1 |
| Gouki | 2 (settle wrapper) | 0 |
| 4 quest hand-ins | 16 mats | 0 |
| wall kits | 60 listed in WKIT_TABLE.normal (scarce mode stocked a subset) | 2 |
| 6 safe-room kits | 1+1 each (12) | 1 each (6) |
| nurse cabinet / post-KO | 2+2 restock, 1+1 after KO | 0 |
| dressing lesson | 1+1 | 1+1 (unchanged) |
| thorough Ch1 total | far above 40 in play (Erik ended with ~40 crafted bandages) | **mean 17.8 mats** (~8.6 dressings) |

Ch2 unchanged: street 4%, minis 2, quest mats still granted.

## Other flags

- A KO still strips raw materials (harsher now that supply is tight). Not changed.
- No Fierce / Strategic-specific content was removed (`foeStr` stays in settings; only `itemScarce` came out).
- Garden rare finds can still yield a length of gauze or tape (Ch2 herbalist; out of scope, left alone).
- Popup shot: `/workspace/craft/out/drop_popup.png` (pill sits just under the HP HUD, pointer-events none, one CSS fade).
- Tune wall stock in `WKIT_STOCK` if Erik wants more or fewer kits without touching drop rates.

## Commits

- `d4e2951` WIP: the seven supply edits
- `2446d91` supply test, popup cap 4
- `2b33d17` popup below HUD, poll flush, test free-world shot
