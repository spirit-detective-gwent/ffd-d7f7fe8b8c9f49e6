#!/workspace/pwenv/bin/python3
import asyncio, sys, json, os, math
SECT='X'
src=open(__file__.rsplit('/',1)[0]+'/test_baseexp.py').read().split('async def main():')[0]
exec(src)
async def main():
    h = serve(root, PORT)
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p); await ev(pg, STUB); await enter(pg, 'caf')
        await go(pg, 'caf', 'bakery'); print(await ev(pg, GF), await ev(pg,"[W.ryo.x,W.ryo.y]"))
        await ev(pg, "W.__fights=[]; var f=W.dgF.find(q=>q.grd); f.gT=99; f.gi=0; f.fa=Math.PI; f.turn=null; 1")
        await put(pg, 410, 400)
        for i in range(12):
            await pg.wait_for_timeout(150)
            print(await ev(pg, "(function(){var f=W.dgF.find(q=>q.grd);return [f.st,+(f.sus||0).toFixed(2),Math.round(W.ryo.x),Math.round(W.ryo.y),Math.round(f.s.x),Math.round(f.s.y),f.N.r, seeK(f,W.ryo.x,W.ryo.y,okAt)]})()"))
        await go(pg, 'caf', 'dock')
        print(await ev(pg, "[[400,405,410,415,418,420,424,428,430].map(x=>okAt(x,420)), [418,424,430].map(x=>okAt(x,421)), cellOf(418,420), cellOf(430,420), (INT.cf_dock.block||[]).filter(b=>b[1]<440&&b[3]>400)]"))
        await b.close()
asyncio.run(main())
