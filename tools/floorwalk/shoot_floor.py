#!/workspace/pwenv/bin/python3
"""Ryo walking onto LANE 1 (Storehouse lockers) and the GRAY COAT FILE mat (Gym Trophy Hall) -> OUT/<room>.png.
Holds ArrowRight from left of the prop until Ryo reaches its centre or 2 s pass (live: he stops at the edge).
usage: shoot_floor.py <tree> <port> <outdir>"""
import asyncio, sys, os
out = sys.argv[3]; sys.argv = sys.argv[:3]
exec(open(__file__.rsplit('/', 1)[0] + '/lib.py').read())
NEXT = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^(Next|Skip|Close|OK|Got it)/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return 0;b[0].click();return 1}"""
PREP = "(function(){ fight=function(){ ev('test:fight'); }; (W.dgF||[]).forEach(function(f){ if(f.s&&f.s.el) f.s.el.remove(); }); W.dgF=[]; W.dlg=false; W.busy=false; W.cut=false; W.path=[]; W.arrive=null; W.cool=0; W.fading=false; return 1; })()"
SHOTS = [('lockers', 'fldGo', 'FLDG', [520, 480, 630, 560], 10), ('trophy', 'gymGo', 'GYMG', [180, 480, 420, 620], 30)]
async def main():
    os.makedirs(out, exist_ok=True); h = serve(root, PORT)
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p); await ev(pg, CLR)
        for room, go, G, r, dy in SHOTS:
            await ev(pg, f"W.fading=false; {go}('{room}'); 1")
            for i in range(16): await pg.evaluate(NEXT); await pg.wait_for_timeout(110)
            await ev(pg, CLR); await ev(pg, PREP)
            s = await ev(pg, f"{G}.{room}.s"); R = [v * s for v in r]; cx = (R[0] + R[2]) / 2; cy = (R[1] + R[3]) / 2 + dy
            await ev(pg, f"W.ryo.x={R[0] - 45}; W.ryo.y={cy}; place(W.ryo,0); 1"); await pg.wait_for_timeout(300); await ev(pg, PREP)
            await pg.keyboard.down('ArrowRight'); t = 0
            while t < 2000:
                await pg.wait_for_timeout(40); t += 40
                if await ev(pg, "W.ryo.x") >= cx: break
            await pg.keyboard.up('ArrowRight'); await pg.wait_for_timeout(700)
            pos = await ev(pg, "[Math.round(W.ryo.x),Math.round(W.ryo.y)]")
            await pg.screenshot(path=f'{out}/{room}.png'); print(room, 'ryo', pos, 'prop', [round(v) for v in R], flush=True)
        print('errs', errs); await b.close()
    h.shutdown()
asyncio.run(main())
