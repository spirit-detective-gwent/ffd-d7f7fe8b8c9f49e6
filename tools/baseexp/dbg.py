#!/workspace/pwenv/bin/python3
import asyncio, sys, json, os, math
SECT='X'
src=open(__file__.rsplit('/',1)[0]+'/test_baseexp.py').read().split('async def main():')[0]
exec(src)
async def main():
    h = serve(root, PORT)
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p); await ev(pg, STUB)
        await enter(pg, 'fld'); await go(pg, 'fld', 'showers'); await ev(pg, "fldLift('showers'); 1"); await pg.wait_for_timeout(400); await skipall(pg, 4); await free(pg)
        print(await ev(pg, "[W.carry, fldS().hr]"))
        await go(pg, 'fld', 'track'); await pg.wait_for_timeout(500); await free(pg)
        print(await ev(pg, "[W.carry, fldS().hr, !!W.fldLap, (W.fldRing||[]).map(q=>q.st+'|'+q.el.className)]"))
        await ev(pg, "var R=FLDG.track, sp=R.spots.find(q=>q.id==='slot0'), a=lw(R,[280,440]); W.ryo.x=a[0]; W.ryo.y=a[1]+20; place(W.ryo,0); var g=fldSlotAng('slot0'); W.fldLap.t=Math.floor(W.fldLap.t)+(g/(2*Math.PI)-0.1+1)%1; 1")
        await pg.wait_for_timeout(250)
        print(await ev(pg, "[W.carry, fldFeeOk('slot0'), (W.fldRing||[]).map(q=>q.st+'|'+q.el.className+'|'+getComputedStyle(q.el).opacity+'|'+q.el.style.left)]"))
        print(await ev(pg, "(function(){ var c=W.carry; fldPlace('slot0'); return [c, W.carry, fldS().kick, ST&&0]; })()"))
        await b.close()
asyncio.run(main())
