#!/workspace/pwenv/bin/python3
"""Frames of the first Storehouse bay entry (live or branch) -> OUT/f_###.png. usage: shoot_entry.py <tree> <port> <outdir> [secs]"""
import asyncio, sys, os
out = sys.argv[3]; secs = float(sys.argv[4]) if len(sys.argv) > 4 else 13
sys.argv = sys.argv[:3]
exec(open(__file__.rsplit('/', 1)[0] + '/lib.py').read())
NEXT = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^(Next|Got it|Close|OK)/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return 0;b[0].click();return 1}"""
async def main():
    os.makedirs(out, exist_ok=True); h = serve(root, PORT)
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p)
        await ev(pg, CLR); await ev(pg, "fldEnter(); 1")
        t0 = asyncio.get_event_loop().time(); i = 0; nx = 0
        while asyncio.get_event_loop().time() - t0 < secs:
            el = asyncio.get_event_loop().time() - t0
            await pg.screenshot(path=f'{out}/f_{i:03d}.png'); i += 1
            if el > nx: await pg.evaluate(NEXT); nx = el + 1.4
            await pg.wait_for_timeout(60)
        print('frames', i, 'errs', errs); await b.close()
    h.shutdown()
asyncio.run(main())
