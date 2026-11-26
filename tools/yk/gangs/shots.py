import asyncio, sys, json
sys.path.insert(0, '/workspace/ffd-idle-notes')
from h import serve, boot, ch2, ev, tele, skipall
from playwright.async_api import async_playwright
root, port = sys.argv[1], int(sys.argv[2]); OUT = '/workspace/v6560-review/gangs/wired/'
FPS = """()=>new Promise(r=>{var n=0,t0=performance.now();function f(t){n++;if(t-t0<3000)requestAnimationFrame(f);else r(Math.round(n*1000/(t-t0)))}requestAnimationFrame(f)})"""
async def shot(pg, name): await pg.screenshot(path=OUT + name + '.png'); print('shot', name, flush=True)
async def main():
    h = serve(root, port)
    async with async_playwright() as p:
        b, ctx, pg, cdp, errs = await boot(p, port, 1, 2)
        await ch2(pg)
        await ev(pg, "(function(){var S=c2S();S.e.genji=1;S.e.roam=1;S.e.arrive=1;S.e.gymIn=1;})()")
        # Kitsune: Club Kitsune street crew (Suits + Runners), the Bouncer at the door
        await ev(pg, "FFF_C2EV.clear()"); await tele(pg, 2880, 1622 + 150, 600); await ev(pg, "FFF_C2EV.force('S1K1')"); await pg.wait_for_timeout(2500)
        await ev(pg, "(function(){var r=WORLD_API.W.ryo;['c2_suit','c2_suit','c2_suit','mb2_game'].forEach(function(id,i){c2Npc(id,r.x-120+i*70,r.y-40,Math.PI/2)})})()"); await pg.wait_for_timeout(2500)
        await shot(pg, 'kitsune_crosswalk')
        print('fps town 1x', await pg.evaluate(FPS), flush=True)
        bz = await ev(pg, "C2BOUNCER"); await tele(pg, bz[0], bz[1] + 160, 2500); await shot(pg, 'kitsune_bouncer_door')
        # Depot: Riders + Dock Hands, Masa
        await ev(pg, "FFF_C2EV.clear()"); r1 = await ev(pg, "(function(){var e=FFF_C2EV.EVENTS.filter(function(e){return e.id==='R1K1'})[0];return [e.x,e.y]})()")
        await tele(pg, r1[0], r1[1] + 150, 600); await ev(pg, "FFF_C2EV.force('R1K1')"); await pg.wait_for_timeout(2500)
        await ev(pg, "(function(){var r=WORLD_API.W.ryo;['c2_boso','c2_boso','c2_boso','mb2_depot','n13sb'].forEach(function(id,i){c2Npc(id,r.x-140+i*64,r.y-40,Math.PI/2)})})()"); await pg.wait_for_timeout(2500)
        await shot(pg, 'depot_crew'); await ev(pg, "FFF_C2EV.clear()")
        # Club Kitsune inside: coat check hostess, bartender (dealer look)
        await ev(pg, "c2Go('club')"); await pg.wait_for_timeout(2500); await skipall(pg, 4)
        await tele(pg, 140, 1700, 2000); await shot(pg, 'club_coatcheck_hostess')
        await tele(pg, 200, 330, 2000); await shot(pg, 'club_bar_dealer')
        await ev(pg, "c2Go('ckback')"); await pg.wait_for_timeout(2500); await skipall(pg, 4)
        await tele(pg, 300, 1330, 2000); await shot(pg, 'club_backoffice_hostesses')
        await tele(pg, 420, 1180, 2000); await shot(pg, 'club_backoffice_dealer')
        # fights
        for grp, nm in ((['mb2_game'], 'fight_jin'), (['mb2_depot'], 'fight_masa'), (['ck_hostess', 'ck_hostess'], 'fight_hostess'), (['ck_dealer', 'c2_suit'], 'fight_dealer'), (['c2_boso', 'c2_boso'], 'fight_riders')):
            await pg.reload(); await pg.wait_for_timeout(3000); await ch2(pg)
            if nm in ('fight_hostess', 'fight_dealer'): await ev(pg, "ckFoes()")
            await tele(pg, 2180, 2000, 800)
            await ev(pg, "fight(%s,false,{dg:'c2',freeOpen:0})" % json.dumps(grp)); await pg.wait_for_timeout(5000); await skipall(pg, 3); await pg.wait_for_timeout(1500)
            await shot(pg, nm)
            if nm == 'fight_jin': print('fps battle 1x', await pg.evaluate(FPS), flush=True)
        print('errs', errs[:5]); await b.close()
    h.shutdown()
asyncio.run(main())
