#!/workspace/pwenv/bin/python3
"""before shot: on live, NG+ Fierce Gouki -> one-round fight -> Ofuda swap popup in the gym. usage: shot_before.py <tree> <port> <out.png>"""
import sys, asyncio, json
from pathlib import Path
here = Path(__file__).resolve().parent
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], 'X', sys.argv[3]]
OUT = sys.argv[4]
src = open(here / 'test_ofuda.py').read().split('async def main():')[0]
exec(compile(src, 'test_ofuda', 'exec'))
async def m():
    H.serve(ROOT, PORT)
    async with H.async_playwright() as p:
        b, ctx, pg, errs = await H.boot(p, PORT)
        await H.ch1_ready(pg, 1440, 3300)
        print(await H.ev(pg, SET + "(" + json.dumps({'path': 'fierce', 'ngp': 1, 'lamp': 1}) + ")"))
        await H.ev(pg, "FFF_UI.ST.events.length=0;root.FFF_NO_VC=1;gymGo&&0;gkFight();1")
        print('play', await wait_play(pg)); print('ctx', await H.ev(pg, CTX))
        await H.ev(pg, WIN)
        for i in range(80):
            await adv(pg)
            await pg.evaluate("()=>{var e=document.getElementById('rMap');if(e&&document.getElementById('result').classList.contains('on')&&e.offsetParent)e.click()}")
            if await H.ev(pg, "!!document.querySelector('#gfind.on')"): break
            await pg.wait_for_timeout(400)
        gf = await H.ev(pg, "!!document.querySelector('#gfind.on')"); print('gfind', gf, await H.ev(pg, "({gouki:SAVE.gouki,gkPh:SAVE.gkPh,dbl:SAVE.dbl})"))
        await pg.wait_for_timeout(800); await pg.screenshot(path=OUT); await b.close()
asyncio.run(m())
