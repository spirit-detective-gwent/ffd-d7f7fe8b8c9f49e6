# GGD-genjicam — camera after Genji's three lessons (t438)

Date: 2026-11-26 (America/New_York)
Base: e1ba0d4 (main, live v6.5.63)
Branch: v6564-genjicam
Worktree: /workspace/genjicam/wt
Final commit: 8019bf9
Not published, not pushed, no version bump.
Did not touch /workspace/ffd (v6564-jin), index_fffonly.html, or page.canvas.tsx.txt.

## Bug (Erik t438)

After Ryo and Aoi learn Genji's three lessons, the scene that follows starts
with the camera on the far left of the gym. It should start centered on the
pair, in the room, with Genji visible, and with no sudden zoom-out.

## Root cause

`back()` for a ring spar does `enter(true)` while Ryo and Aoi are still in the
ring (x≈500–650). That is the first visible gym frame after the fight board
lifts: the left/center of the room, Genji only at the right ropes.

`g38OutOfRing` does put them at the east ropes (OUT x=955) and snaps the
camera onto the trio, but only in the mid-callback of `fadeBlack` — 300ms
delay plus an 800ms fade after that first left-side frame has already been
seen.

A leftover `W.pan` makes it worse: `camera()` keeps the current `W.cam`,
which is often `{x:0,y:0}`, so the first frame is the left wall (lockers and
couch) with Aoi and Genji off-screen. Same family of bug as the v6.5.58
t3113 teaching-stage snap, which only covers `g38Place` / lesson *start*,
not the post-spar return.

## Fix

Before `enter(true)` reveals the gym, place Ryo and Aoi at `G38.OUT`, keep
Genji at the referee mark, clear `W.pan`, set `W.camFocus` to the trio, and
snap through `FFF_G38_CINE_CAM`. The first visible frame is already the
group on the east floor. No new loop, no zoom-out.

Also:
- Teach cine (`teachCamTo`): if the world camera is still more than 220px off
  the marks (leftover left-edge view), snap instead of easing across the room.
- `enter()` while in the gym: if the camera is still on the left wall
  (`cam.x < 80`) and Ryo is in the room, snap onto the trio (reload safety).

## Tests (`tools/test_cam.py`)

7/7 camera checks PASS:
- leftover W.pan + cam at 0
- third lesson (cover), Ryo lead, balanced, and reload
- first lesson (sneak), Ryo lead
- second lesson (assist), Aoi lead, fierce
- third lesson, Aoi lead, strategic, and reload

First frame after `back()`: cam x=640, Ryo/Aoi at OUT (955), Genji at 850,
all in the 390px view. Reload: cam x=675, not the left wall.

verify_wired.py (from /workspace/v6560-review/portraits) PASS.

## Perf vs live (post-lesson gym frame, 5s, 390×844)

fps 59.8, heat 11.7 (1×). At 4× throttle: fps 59.6, heat 25.7 (live 27.2, delta −1.5). Memory flat (heap delta 0).

## Deliverable

/workspace/genjicam/before_after.png — old start frame (in-ring, left/center
of the room) on the left; new start frame (centered on Ryo, Aoi and Genji)
on the right.
