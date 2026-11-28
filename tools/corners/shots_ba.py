#!/workspace/pwenv/bin/python3
"""Before (live) / after (branch) shots of X2 right after gym exit, plus a short handshake video."""
import asyncio, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import h
from PIL import Image, ImageDraw, ImageFont

LIVE = os.environ.get('LIVE_INDEX', '/workspace/herbcine/live/index.html')
NEW = os.environ.get('FFD_INDEX', '/workspace/nailsalley/wt/index.html')
OUT = Path(os.environ.get('SHOTDIR', '/workspace/nailsalley/shots'))

async def alley_shot(index, name, video=False):
    kw = dict(out=str(OUT), index=index)
    async with h.Game(**kw) as g:
        await g.boot()
        left = await g.gym_exit()
        await g.go_xy(1790, 2165)
        for _ in range(10):
            try:
                await g.ev("if(typeof g38tClashCheck==='function')g38tClashCheck(); if(root.FFF_NALLEY&&FFF_NALLEY.retrigger)FFF_NALLEY.retrigger();1")
            except Exception:
                pass
            await g.wait(300)
        snap = await g.snapshot('X2')
        path = await g.shot(name, hush=True)
        print('SHOT', name, path, {k: snap[k] for k in ('clash','xy','hear') if k in snap},
              'A', len(((snap.get('borders') or {}).get('X2') or {}).get('A') or []),
              'Z', len(((snap.get('borders') or {}).get('X2') or {}).get('Z') or []))
        return path, snap

def composite(before, after, dest):
    a = Image.open(before).convert('RGB')
    b = Image.open(after).convert('RGB')
    h = max(a.height, b.height)
    a = a.resize((a.width, h)) if a.height != h else a
    b = b.resize((b.width, h)) if b.height != h else b
    pad, label_h = 8, 36
    w = a.width + b.width + pad * 3
    canvas = Image.new('RGB', (w, h + label_h + pad), (18, 16, 20))
    canvas.paste(a, (pad, label_h))
    canvas.paste(b, (pad * 2 + a.width, label_h))
    d = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
    except Exception:
        font = ImageFont.load_default()
    d.text((pad + 8, 8), 'LIVE v6.5.65 — empty alley', fill=(240, 220, 200), font=font)
    d.text((pad * 2 + a.width + 8, 8), 'Branch — Nails alley fight on', fill=(240, 220, 200), font=font)
    canvas.save(dest)
    print('COMPOSITE', dest, canvas.size)

async def handshake_video():
    """Record the handshake cine on the branch."""
    # Use Playwright video on a dedicated context by temporarily wrapping Game — simpler: screenshot burst.
    frames = []
    async with h.Game(out=str(OUT), index=NEW) as g:
        await g.boot(); await g.gym_exit(); await g.go_xy(1790, 2165)
        for _ in range(10):
            await g.ev("if(typeof g38tClashCheck==='function')g38tClashCheck();1")
            s = await g.snapshot('X2')
            if (s.get('clash') or {}).get('b') == 'X2':
                break
            await g.wait(300)
        # join + win
        await g.ev("""(function(){ var C=W.g38c; if(!C) return 0; var side=(G38T.FAC[C.A.id]==='arc')?'A':'Z'; g38tBack(side); return 1; })()""")
        await g.wait(400)
        await g.ev("""(function(){ var b=[...document.querySelectorAll('button')].filter(function(x){return /Back the Punks/i.test(x.textContent||'');})[0]; if(b) b.click(); return 1; })()""")
        await g.wait(500)
        await g.win_fight(True)
        # capture frames through cine
        for i in range(40):
            evs = await g.ev("window.__evs||[]") or []
            if any('nalley:cine:start' in str(e) for e in evs):
                await g.ev("if(W.nalleyCine&&W.nalleyCine.st==='walk'){W.nalleySkipWalk=1;}1")
            if any('nalley:ask' in str(e) for e in evs):
                await g.ev("""(function(){ var b=[...document.querySelectorAll('button')].filter(function(x){return /Shake on it/i.test(x.textContent||'');})[0]; if(b) b.click(); return 1; })()""")
            fp = OUT / f'hs_frame_{i:02d}.png'
            await g.pg.screenshot(path=str(fp), type='png')
            frames.append(fp)
            if any('nalley:flip:walk' in str(e) or '13u:cut' in str(e) for e in evs) and i > 20:
                break
            await g.wait(200)
    # stitch to mp4 if ffmpeg exists
    if frames:
        import subprocess
        out = OUT / 'handshake.mp4'
        cmd = ['ffmpeg', '-y', '-framerate', '5', '-i', str(OUT / 'hs_frame_%02d.png'),
               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'scale=390:844', str(out)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        print('FFMPEG', r.returncode, out if r.returncode == 0 else r.stderr[-400:])
        return str(out) if r.returncode == 0 else None
    return None

async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    before, sb = await alley_shot(LIVE, 'x2_before_live')
    after, sa = await alley_shot(NEW, 'x2_after_branch')
    composite(before, after, OUT / 'before_after.png')
    try:
        vid = await handshake_video()
        print('VIDEO', vid)
    except Exception as e:
        print('VIDEO err', e)

if __name__ == '__main__':
    asyncio.run(main())
