#!/workspace/pwenv/bin/python3
"""Before/after of Flip's south-end clash battle: live 3-foe vs branch 1-foe + ally brawls."""
import asyncio, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import h
import t13_clash as T

LIVE = os.environ.get('LIVE_INDEX', '/workspace/herbcine/live/index.html')
NEW = os.environ.get('FFD_INDEX', '/workspace/nailsalley/wt/index.html')
OUT = Path('/workspace/nailsalley/shots')

async def capture(index, name):
    g = h.Game(out=str(OUT), index=index)
    async with g:
        await g.boot()
        await T.seed_at_clash(g)
        await T.start_walkin(g)
        # street walk-in (same on both)
        await g.wait(800)
        if 'after' in name:
            await g.shot('t13_walkin_after', hush=False)
        else:
            await g.shot('t13_walkin_before', hush=False)
        st = await T.to_fight(g)
        await g.wait(600)
        path = await g.shot(name, hush=False)
        return path, st

async def main():
    b, sb = await capture(LIVE, 't13_battle_before')
    print('before', b, sb)
    a, sa = await capture(NEW, 't13_battle_after')
    print('after', a, sa)
    # compose
    try:
        from PIL import Image, ImageDraw, ImageFont
        im1 = Image.open(OUT/'t13_battle_before.png').convert('RGB')
        im2 = Image.open(OUT/'t13_battle_after.png').convert('RGB')
        w,h = im1.size
        im2 = im2.resize((w,h))
        pad, lab = 16, 48
        canvas = Image.new('RGB', (w*2+pad*3, h+pad*2+lab), (18,14,16))
        canvas.paste(im1, (pad, pad+lab))
        canvas.paste(im2, (pad*2+w, pad+lab))
        d = ImageDraw.Draw(canvas)
        d.text((pad, 12), 'LIVE  —  Ryo fights all three', fill=(230,220,210))
        d.text((pad*2+w, 12), 'BRANCH  —  Ryo fights one; two allies take the others', fill=(230,220,210))
        out = OUT/'before_after_clash.png'
        canvas.save(out)
        print('wrote', out)
    except Exception as e:
        print('compose failed', e)

if __name__ == '__main__':
    asyncio.run(main())
