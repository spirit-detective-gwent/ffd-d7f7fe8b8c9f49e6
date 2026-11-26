# Club Kitsune staff screenshots only (coat check hostess, bartender, chip-cage cashier) + close crops
import asyncio, sys
sys.path.insert(0, '/workspace/ffd-idle-notes')
from h import serve, boot, ch2, ev, tele, skipall
from playwright.async_api import async_playwright
root, port = sys.argv[1], int(sys.argv[2]); OUT = '/workspace/v6560-review/gangs/wired/'
async def shot(pg, name): await pg.screenshot(path=OUT + name + '.png'); print('shot', name, flush=True)
async def main():
    h = serve(root, port)
    async with async_playwright() as p:
        b, ctx, pg, cdp, errs = await boot(p, port, 1, 2)
        await ch2(pg)
        await ev(pg, "(function(){var S=c2S();S.e.genji=1;S.e.roam=1;S.e.arrive=1;S.e.gymIn=1;})()")
        await ev(pg, "c2Go('club')"); await pg.wait_for_timeout(2500); await skipall(pg, 4)
        await tele(pg, 140, 1700, 2000); await shot(pg, 'club_coatcheck_hostess')
        await tele(pg, 200, 330, 2000); await shot(pg, 'club_bar_bartender')
        await tele(pg, 470, 470, 2000); await shot(pg, 'club_cage_cashier')
        print(await ev(pg, "(function(){return [].slice.call(document.querySelectorAll('img,div')).filter(function(e){var s=(e.src||'')+(e.style&&e.style.backgroundImage||'');return /ck_(cashier|dealer|hostess)K|npc_(ramen|attendant|clerk)/.test(s)}).map(function(e){var s=(e.src||'')+(e.style.backgroundImage||'');return s.replace(/.*world\\//,'').replace(/[\\\")].*/,'')}).slice(0,20)})()"))
        print('errs', errs[:5]); await b.close()
    h.shutdown()
asyncio.run(main())
