#!/workspace/pwenv/bin/python3
"""phase 2 frame: Gouki finale in the gym arena (NG+ or fresh), revive loop -> Bond -> the Double. usage: shot_phase2.py <tree> <port> <outprefix> [ngp]"""
import sys, asyncio, json
from pathlib import Path
here = Path(__file__).resolve().parent
NG = len(sys.argv) > 4 and sys.argv[4] == 'ngp'; OUTP = sys.argv[3]
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], 'X']
src = open(here / 'test_ofuda.py').read().split('async def main():')[0]
exec(compile(src, 'test_ofuda', 'exec'))
async def m():
    H.serve(ROOT, PORT)
    async with H.async_playwright() as p:
        b, ctx, pg, errs = await H.boot(p, PORT)
        await H.ch1_ready(pg, 1440, 3300)
        print(await H.ev(pg, SET + "(" + json.dumps({'path': 'fierce', 'ngp': 1 if NG else 0, 'lamp': 1}) + ")"))
        await H.ev(pg, "var S=gymS();S.e.press=1;gymGo('arena');1"); await pg.wait_for_timeout(2500); await adv(pg)
        await H.ev(pg, "FFF_UI.ST.events.length=0;root.FFF_NO_VC=1;gkFight();1")
        print('p1', await wait_play(pg), await H.ev(pg, CTX)); await pg.wait_for_timeout(1500)
        await H.ev(pg, WIN); print('loop', await wait_play(pg, 60), await H.ev(pg, CTX)); await pg.wait_for_timeout(1500)
        await H.ev(pg, LOSE); print('fin', await wait_play(pg, 60), await H.ev(pg, CTX))
        await pg.wait_for_timeout(2500)
        await pg.evaluate("()=>{var b=FFF_UI.ST.b;b.s[0].spirit=40;if(b.bench)b.bench.spirit=40;if(FFF_UI.render)FFF_UI.render()}"); await pg.wait_for_timeout(800)
        await pg.screenshot(path=OUTP + '_prompt.png')
        db = await pg.evaluate("()=>{var e=document.getElementById('btnDbl');if(!e||!e.offsetParent)return null;var r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}")
        print('dbl btn', db)
        if db:
            await pg.touchscreen.tap(*db)
            for i, t in enumerate((900, 700, 700, 900)):
                await pg.wait_for_timeout(t); await pg.screenshot(path=f'{OUTP}_double{i}.png')
        print('errs', errs[:3]); await b.close()
asyncio.run(m())
