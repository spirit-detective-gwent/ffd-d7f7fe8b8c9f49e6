#!/workspace/pwenv/bin/python3
"""Record the c2_goda preview (one clip per answer, 60 fps virtual time) and join them. Review-only; never publishes.
usage: clip_goda.py [fierce strategic balanced]"""
import sys, asyncio, shutil, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import bh
from playwright.async_api import async_playwright
OUT = Path('/workspace/v6560-review/bond'); OUT.mkdir(exist_ok=True)
PORT = 8984
IDX = {'fierce': 0, 'strategic': 1, 'balanced': 2}
POLL = """(function(){var d=document.getElementById('wdlg');var on=!!(d&&d.classList.contains('on'));return {on:on,len:on?((d.querySelector('.d2-q,.tw,.d2-body')||{}).textContent||'').length:0,btns:on?[...d.querySelectorAll('button')].filter(x=>x.offsetParent&&!/Auto/.test(x.textContent)).map(x=>x.textContent.trim().slice(0,30)):[],bond:!!document.querySelector('#wdlg.on button.bondopt'),seal:!!c2S().e.seal_sento,scene:(W.scr|0),cut:!!W.cut}})()"""
CLICK = """(i)=>{var b=[...document.querySelectorAll('#wdlg.on button')].filter(e=>e.offsetParent&&!e.disabled&&!/Auto/.test(e.textContent));if(!b.length)return null;var x=b[i||0]||b[0];x.click();return x.textContent.trim()}"""
async def record(ans, body, errs, keep=None):
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
        pg = await ctx.new_page(); await pg.add_init_script(bh.SHIM)
        pg.on('pageerror', lambda e: errs.append(ans + ' ' + str(e)[:300]))
        await bh.boot(pg, PORT, body); await bh.ch2(pg)
        await bh.ev(pg, "(function(){ST.set.txt='normal';var E=c2S().e;E.run_fac='arc';E.baseOpen_bat=1;E.guardGone_sento=1;E.arrive=1;STORY.bond(SAVE).path='%s';SAVE.bond=SAVE.bond||{};return 1})()" % ans)
        await bh.ev(pg, "c2Go('sento')"); await pg.wait_for_timeout(2500); await bh.ev(pg, bh.HUSH)
        print(ans, await bh.ev(pg, "(function(){var b=W.c2n.boss;W.ryo.x=b.x-90;W.ryo.y=b.y+110;place(W.ryo,0);if(W.aoi){W.aoi.x=b.x-140;W.aoi.y=b.y+140;place(W.aoi,0)}camera(true);return [b.x,b.y]})()"))
        await pg.wait_for_timeout(800)
        d = f'/tmp/bondclip/{ans}'; v = bh.VT(pg, ctx, d); await v.start()
        await v.run(1.0)
        await bh.ev(pg, "c2LmBack(true,{ctx:{c2lm:'sento',dg:'c2'}})")
        still = 0; lastlen = -1; since = 0; clicks = 0; seal_at = None; maxf = 60 * 220
        while v.n < maxf:
            await v.run(0.1); st = await bh.ev(pg, POLL)
            if st['seal'] and seal_at is None: seal_at = v.n
            if seal_at and not st['on'] and v.n - seal_at > 60 * 3.5: break
            if not st['on']: lastlen = -1; since = 0; continue
            if st['len'] == lastlen: since += 1
            else: lastlen = st['len']; since = 0
            if since < 3: continue
            read = 8 + int(min(40, lastlen / 7))  # polls (0.1 s) of reading time
            if st['bond']: read = 20
            if since >= read:
                await pg.evaluate(CLICK, IDX[ans] if st['bond'] else 0); clicks += 1; lastlen = -1; since = 0
        await v.run(1.0)
        info = await bh.ev(pg, "JSON.stringify({fate:c2S().e.godaFate,tip:c2S().e.ckTip,picks:STORY.bond(SAVE).picks,px:STORY.bond(SAVE).px})")
        print(ans, 'frames', v.n, 'clicks', clicks, info); await b.close()
    mp4 = OUT / f'c2_goda_{ans}_v4.mp4'; bh.encode(d, mp4); return d, mp4
async def main():
    order = sys.argv[1:] or ['fierce', 'strategic', 'balanced']
    bh.serve(PORT); body = bh.inject(); errs = []
    for a in order: await record(a, body, errs)
    print('ERRS', errs[:6])
asyncio.run(main())
