#!/workspace/pwenv/bin/python3
import asyncio, sys, json
exec(open(__file__.rsplit('/', 1)[0] + '/../lockeramb/lib.py').read())
async def main():
    h = serve(root, PORT)
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p)
        await ev(pg, CLR)
        await ev(pg, "cafEnter(); 1"); await pg.wait_for_timeout(1500); await skipall(pg, 6); await ev(pg, CLR)
        for k in ['cooler','dock','dish','bakery']:
            await ev(pg, "W.fading=false; cafGo('%s'); 1" % k); await pg.wait_for_timeout(1200); await skipall(pg, 6); await ev(pg, CLR)
            print(k, await ev(pg, "[(W.dgF||[]).map(f=>[f.key,f.st,Math.round(f.s.x),Math.round(f.s.y),+f.fa.toFixed(2)]), W.ryo.x|0, W.ryo.y|0, document.querySelectorAll('.wgcone').length]"))
            await pg.screenshot(path='/workspace/baseexp/shots/smoke_%s.png' % k)
        await ev(pg, "fldEnter(); 1"); await pg.wait_for_timeout(1500); await skipall(pg, 6); await ev(pg, CLR)
        for k in ['cage','showers','trainer','booth','track']:
            await ev(pg, "W.fading=false; fldGo('%s'); 1" % k); await pg.wait_for_timeout(1200); await skipall(pg, 6); await ev(pg, CLR)
            print(k, await ev(pg, "[W.ryo.x|0, W.ryo.y|0, (INT['sf_%s'].spots||[]).map(s=>s.id)]" % k))
            await pg.screenshot(path='/workspace/baseexp/shots/smoke_%s.png' % k)
        print('errs', errs)
        await b.close()
asyncio.run(main())
