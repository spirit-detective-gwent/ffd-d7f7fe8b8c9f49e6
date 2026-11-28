#!/workspace/pwenv/bin/python3
import asyncio, sys
sys.argv=[sys.argv[0]]+sys.argv[1:]
exec(open(__file__.rsplit('/',1)[0]+'/lib.py').read())
async def main():
    h = serve(root, PORT)
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p)
        await ev(pg, CLR)
        print(await ev(pg, "fldEnter(); 1"))
        for t in range(12):
            await pg.wait_for_timeout(500)
            if t in (2,4,6): await skipall(pg, 3)
            if t==3: await pg.screenshot(path='/tmp/lk_probe.png'); print(await ev(pg, DLG)); print(await pg.evaluate("[...document.querySelectorAll('button')].filter(e=>e.offsetParent).map(e=>e.textContent.trim()).slice(0,12)"))
            print(t, await ev(pg, "[W.inside&&W.inside.id, W.dlg, W.busy, (W.dgF||[]).map(f=>[f.key,f.id,Math.round(f.s.x),Math.round(f.s.y),f.st,f.stun>1e6?'S':f.stun, f.s.el.style.visibility]), W.dgFight&&W.dgFight.key, W.fading, W.cut, W.fldEntOn, (FFF_UI.events||ST&&ST.events||[]).filter(e=>/field|scene/.test(e)).slice(-6), document.querySelector('#battle, .battle')?1:0]"))
        print(errs)
        await b.close()
    h.shutdown()
asyncio.run(main())
