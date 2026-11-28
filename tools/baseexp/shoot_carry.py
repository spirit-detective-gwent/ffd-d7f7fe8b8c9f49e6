#!/workspace/pwenv/bin/python3
"""Hurdle-carry draw per facing (Erik t588u). usage: shoot_carry.py <tree> <port> <outprefix>
Writes <outprefix>_{up,down,left,right}.png crops of Ryo carrying a hurdle in the Storehouse bay, plus <outprefix>.png strip."""
import asyncio, sys, os
exec(open(__file__.rsplit('/', 1)[0] + '/../lockeramb/lib.py').read())
OUT = args[2]
FA = [('up', (0, -200)), ('down', (0, 200)), ('left', (-200, 0)), ('right', (200, 0))]
async def main():
    from PIL import Image
    h = serve(root, PORT)
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p)
        await ev(pg, "fldEnter(); 1"); await pg.wait_for_timeout(1500); await skipall(pg, 8); await ev(pg, CLR)
        await ev(pg, "var S=fldS(); S.e.entry=1; S.f.fbay0=1; S.f.fbay1=1; S.e.surprise=1; save(); W.fading=false; fldGo('lockers'); 1"); await pg.wait_for_timeout(900); await skipall(pg, 6); await ev(pg, CLR)
        await ev(pg, "W.dgF.forEach(f=>{f.s.el.style.display='none'}); W.dgF=[]; W.dlg=false; W.busy=false; W.cool=0; 1")
        await ev(pg, "W.carry='h:showers'; fldCarryEl(); W.ryo.x=575; W.ryo.y=430; place(W.ryo,0); 1")
        ims = []
        for nm, a in FA:
            await ev(pg, "W.path=[]; W.ryo.v=0; W.ryo.x=575; W.ryo.y=480; place(W.ryo,0); walkTo(575+%d, 480+%d, true, false); 1" % a); await pg.wait_for_timeout(420)
            d = await ev(pg, "W.ryo.el.dataset.dir"); bb = await ev(pg, "(function(){var r=W.ryo.el.getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
            x, y, w, hh = bb; pad = 30
            fn = '%s_%s.png' % (OUT, nm)
            await pg.screenshot(path=fn, clip={'x': max(0, x - pad), 'y': max(0, y - pad), 'width': w + 2 * pad, 'height': hh + 2 * pad})
            print(nm, 'dir', d, bb); ims.append(Image.open(fn).convert('RGB').resize((int((w + 2 * pad) * 2), int((hh + 2 * pad) * 2))))
        W_ = sum(i.width for i in ims) + 10 * (len(ims) - 1); H_ = max(i.height for i in ims)
        st = Image.new('RGB', (W_, H_), (30, 26, 34)); x = 0
        for i in ims: st.paste(i, (x, 0)); x += i.width + 10
        st.save(OUT + '.png'); print('errs', errs); await b.close()
    h.shutdown()
asyncio.run(main())
