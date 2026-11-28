#!/workspace/pwenv/bin/python3
"""v6566-rc integration fixes found in the Ch2 playthrough. usage: test_rcfix.py   (FFD_INDEX=... for another index.html)
 2. S2 phase quests (Night Runs..Jin) as the active quest: the journal target is the phase's own pin, not the 'Clinic' fallback.
 1. Wagashi Row on Compassionate (balanced): at stage 'open' the pin points at Flip (journal step 1), not Chiyo's door
    (the door talk never advanced the quest, so the pin looped there forever).
 3. Funayado lookout (cq2_s2_boat) and the quay garage (cq2_s2_gar): a tap on the door walks to a reachable lip and enters the
    room (before: no handler entered either room and the door rects sat on unwalkable ground); leaving puts Ryo back on the lip.
 4. Kaji / Sada fights: they had no battle character, so the swirl crashed in newSide and froze the world. Talking to them in
    their room now starts the fight and a win returns to the world.
 5. Masa at the depot shutter: bossEnt's done fired while the cine still held W.dlg, so busy() dropped the fight and every
    talk replayed the intro. Talking to him (skipping the intro the way a player can) now starts the shutter fight.
 6. High Score at Ramen Kitsuneya with full HP/SP: every menu item is disabled ('HP full'), and the overheard-Suits beat only
    fired after a purchase, so a healthy player was stuck. Closing the menu at the counter now plays the beat.
 7. Phase room canvases (Minato-so, Funayado lookout, quay garage) stayed in the map after you left, so the garage art sat
    over the Izakaya and every room after it. Leaving now removes them.
 8. Neon Game Center during High Score: the v6551 door guard ("The floor's closed.") caught the lm_game tap before the strip
    module could open the floor, so Jin was unreachable. With the strip open the guard lets you in."""
import asyncio, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); import h
R = []
def chk(name, ok, info=''):
    R.append(bool(ok)); print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else '  ' + str(info)[:400]), flush=True)
async def main():
    for path in ('balanced', 'fierce', 'strategic'):
        async with h.Game(path=path) as g:
            await g.boot()
            await g.ev("(function(){var st=c2S(); st.q.cq2_s2_waga=0; st.qa='cq2_s2_waga'; FFF_S2.setStg('open'); c2QSync(); save(); return 1})()")
            await g.go('town', 2360, 3300); await g.wait(800)
            t = await g.ev("JSON.stringify(FFF_S2.tgt())")
            chk(f'[{path}] stage open: pin on Flip', '"lab":"Flip"' in t, t)
            await g.ev("(function(){var t=(W.tagL||[]).find(function(t){return t.key==='c2_town:s2_flip'}); if(!t){try{tagRefresh()}catch(e){}; t=(W.tagL||[]).find(function(t){return t.key==='c2_town:s2_flip'})} if(t){W.ryo.x=t.ax;W.ryo.y=t.ay;place(W.ryo,0);camera(true);} return String(interact())})()")
            for i in range(30):
                await h.adv(g, 2)
                if not await g.ev("!!(W.dlg||W.cut)"): break
            s = await g.ev("[FFF_S2.stg(), c2S().q.cq2_s2_waga, FFF_S2.tgt()&&FFF_S2.tgt().lab]")
            exp = ['sawshop', 'Sweet shop'] if path == 'balanced' else ['w1', 'Wagashi row']
            chk(f'[{path}] after Flip: stage {exp[0]}, pin {exp[1]}', s[0] == exp[0] and s[1] == 1 and s[2] == exp[1], s)
            if path == 'balanced':
                await g.go('town', 3080, 2700); await g.wait(500)
                await g.ev("walkTo(3080,2600,true)")
                for i in range(40):
                    await h.adv(g, 2)
                    if await g.ev("FFF_S2.stg()==='w1'"): break
                chk('[balanced] Chiyo at the door -> first Rider push (w1)', await g.ev("FFF_S2.stg()==='w1'"), await g.ev("FFF_S2.stg()"))
            chk(f'[{path}] no page errors', not [e for e in g.errs if '404' not in e], g.errs[:3])
    async with h.Game(path='balanced') as g:
        await g.boot()
        r = await g.ev("(function(){var st=c2S(); st.q.cq2_s2_runs=0; st.qa='cq2_s2_runs'; if(FFF_S2P2.setStg) FFF_S2P2.setStg('open'); c2QSync(); save(); var t=c2QT(); return [t&&t.lab, t&&t.x, t&&t.y, t&&t.qid]})()")
        chk('Night Runs active at stage open: journal target is Flip (2360,3190), not the clinic', r[0] == 'Flip' and r[1] == 2360 and r[3] == 'cq2_s2_runs', r)
        r = await g.ev("(function(){ if(FFF_S2P2.setStg) FFF_S2P2.setStg('r1'); var t=c2QT(); return [t&&t.lab, t&&t.x, t&&t.y]})()")
        chk('Night Runs r1: journal target is the first night run', r[0] == 'Night run' and r[1] == 3610, r)
    for qid, mod, room, start, tap in (('cq2_s2_boat', 'FFF_S2P3', 'boat', (4830, 3760), (4830, 3550)), ('cq2_s2_gar', 'FFF_S2P4', 'gar', (4200, 3735), (4040, 3900))):
        async with h.Game(path='balanced') as g:
            await g.boot()
            o = await g.ev(f"(function(){{var st=c2S(); st.q.{qid}=0; st.qa='{qid}'; c2QSync(); save(); return {mod}.roomOpen()}})()")
            await g.go('town', *start); await g.wait(800)
            await g.ev(f"String(walkTo({tap[0]},{tap[1]},true))")
            for i in range(40):
                await h.adv(g, 1)
                if await g.ev(f"c2Room()==='{room}'"): break
            r = await g.ev("JSON.stringify({room:c2Room(),r:[W.ryo.x|0,W.ryo.y|0]})")
            chk(f'{qid}: door open ({o}) and a tap on it walks in to {room}', o and f'"room":"{room}"' in r, r)
            await g.ev(f"c2Out('{room}')")
            for i in range(10): await h.adv(g, 1)
            r2 = await g.ev("JSON.stringify({room:c2Room(),r:[W.ryo.x|0,W.ryo.y|0]})")
            d = await g.ev(f"(function(){{var d=c2DoorOf('{room}'),p=findPath(W.ryo.x,W.ryo.y,d.at[0],d.at[1]);return !!p&&(!p.length||Math.hypot(p[p.length-1][0]-d.at[0],p[p.length-1][1]-d.at[1])<20)}})()")
            chk(f'{qid}: leaving puts Ryo back in town (no re-entry) and the door lip is reachable', '"room":"town"' in r2 and d, [r2, d])
            chk(f'{qid}: no page errors', not [e for e in g.errs if '404' not in e], g.errs[:3])
    BTN = "(function(){var b=[...document.querySelectorAll('button')].find(function(b){return b.offsetParent&&/^(Wake up|Continue|Next|OK|Done|Back to|Return|Collect|Leave|Nice)/.test(b.textContent.trim())}); if(b){b.click(); return b.textContent.trim().slice(0,20)} return ''})()"
    for qid, mod, room, talk, foe in (('cq2_s2_boat', 'FFF_S2P3', 'boat', (720, 560), 'nq_kaji'), ('cq2_s2_gar', 'FFF_S2P4', 'gar', (400, 680), 'nq_sada')):
        async with h.Game(path='balanced') as g:
            await g.boot()
            pre = "var st=c2S(); st.e.n13r=''; delete st.q.cq2_s2_depot; delete st.q.cq2_s2_jin;" + ("delete st.q.cq2_s2_gar; st.q.cq2_s2_boat=0; FFF_S2P3.setStg('open');" if room == 'boat' else "st.q.cq2_s2_boat=9; FFF_S2P3.setStg('done'); st.q.cq2_s2_gar=0; FFF_S2P4.setStg&&FFF_S2P4.setStg('open');")
            o = await g.ev(f"(function(){{{pre} st.qa='{qid}'; c2QSync(); save(); return JSON.stringify({{on:{mod}.qOn(), stg:{mod}.stg()}})}})()")
            await g.go('town', 4300, 3735); await g.wait(600)
            await g.ev(f"c2Enter('{room}')")
            for i in range(6): await h.adv(g, 1)
            fought = False
            for k in range(3):
                await g.ev(f"String(walkTo({talk[0]},{talk[1]},true))")
                for i in range(30):
                    await h.adv(g, 2)
                    if await g.ev("document.getElementById('game').classList.contains('on')"): fought = True; break
                if fought: break
            await g.wait(2500)
            if fought: await g.shot(f'fight_{foe}', hush=False)
            info = await g.ev("JSON.stringify({game:document.getElementById('game').classList.contains('on'), ev:FFF_UI.ST.events.filter(function(e){return /fight:ryo/.test(e)}).slice(-1)})")
            chk(f'{qid}: talking to {foe} in {room} starts the fight (no swirl crash)', fought and foe in info, [o, info, await g.ev("FFF_UI.ST.events.filter(function(e){return /swirl|ltfoe|s2:fight/.test(e)}).slice(-6)")])
            if fought:
                await g.ev("(function(){var b=FFF_UI.ST.b; b.winner=0; if(!b.over) FFF_UI.endMatch(); return 1})()")
                await g.wait(1500)
                for i in range(40):
                    await g.wait(500); b = await g.ev(BTN)
                    if not b and not await g.ev("document.getElementById('game').classList.contains('on')"): await h.adv(g, 2)
                    if await g.ev(f"{mod}.qDone()||{mod}.stg()==='done'||(!document.getElementById('game').classList.contains('on')&&!W.dlg&&FFF_UI.ST.events.join(' ').indexOf('s2:won:')>=0)"): break
                r = await g.ev(f"JSON.stringify({{stg:{mod}.stg(), done:{mod}.qDone(), on:W.on, room:c2Room(), game:document.getElementById('game').classList.contains('on'), ev:FFF_UI.ST.events.filter(function(e){{return /s2p[34]|fightEnd|result|match:end|won/.test(e)}}).slice(-8)}})")
                chk(f'{qid}: after the win the world runs again (no freeze; the quest close itself is covered by the Ch2 playthrough)', '"game":false' in r and '"on":true' in r and 's2:won:' in await g.ev("FFF_UI.ST.events.join(' ')"), r)
            chk(f'{qid} fight: no page errors', not [e for e in g.errs if '404' not in e], g.errs[:3])
    async with h.Game(path='balanced') as g:
        await g.boot()
        o = await g.ev("(function(){var st=c2S(); delete st.q.cq2_s2_jin; delete st.e.seal_depot; st.q.cq2_s2_boat=9; st.q.cq2_s2_gar=9; st.q.cq2_s2_depot=1; FFF_S2P5.setStg('met'); st.qa='cq2_s2_depot'; c2QSync(); save(); return JSON.stringify({on:FFF_S2P5.qOn(),stg:FFF_S2P5.stg(),open:FFF_S2P5.roomOpen()})})()")
        await g.go('town', 4300, 3735); await g.wait(600)
        await g.ev("c2Enter('dshut')")
        for i in range(6): await h.adv(g, 1)
        fought = False
        for k in range(2):
            await g.ev("String(walkTo(640,640,true))")
            for i in range(40):
                await h.adv(g, 2)
                if await g.ev("document.getElementById('game').classList.contains('on')"): fought = True; break
            if fought: break
        r = await g.ev("JSON.stringify({room:c2Room(),stg:FFF_S2P5.stg(),ev:FFF_UI.ST.events.filter(function(e){return /bent:|s2p5|fight:ryo/.test(e)}).slice(-6)})")
        chk('cq2_s2_depot: Masa at the shutter starts the fight after his intro', fought and 'mb2_depot' in r, [o, r])
        chk('cq2_s2_depot: no page errors', not [e for e in g.errs if '404' not in e], g.errs[:3])
    async with h.Game(path='balanced') as g:
        await g.boot()
        o = await g.ev("(function(){var st=c2S(); st.q.cq2_s2_jin=0; st.qa='cq2_s2_jin'; FFF_S2P6.setStg('open'); c2QSync(); save(); return JSON.stringify({on:FFF_S2P6.qOn(),stg:FFF_S2P6.stg()})})()")
        await g.go('town', 2250, 1700); await g.wait(600)
        await g.ev("String(walkTo(2250,1540,true))")
        for i in range(20):
            await h.adv(g, 1)
            if await g.ev("c2Room()==='ramen'"): break
        for i in range(4): await h.adv(g, 2)
        await g.ev("String(walkTo(640,300,true))")
        shop = False
        for i in range(20):
            await g.wait(400)
            if await g.ev("[...document.querySelectorAll('button')].some(function(b){return b.offsetParent&&/Done/.test(b.textContent)})"): shop = True; break
        full = await g.ev("[...document.querySelectorAll('button')].filter(function(b){return b.offsetParent&&/full/.test(b.textContent)}).length")
        await g.ev("(function(){var b=[...document.querySelectorAll('button')].find(function(b){return b.offsetParent&&/Done/.test(b.textContent)}); if(b) b.click(); return !!b})()")
        moved = False
        for i in range(30):
            await h.adv(g, 2)
            if await g.ev("FFF_S2P6.stg()!=='open'||FFF_UI.ST.events.join(' ').indexOf('s2p6')>=0&&document.getElementById('game').classList.contains('on')"): moved = True; break
        r = await g.ev("JSON.stringify({room:c2Room(),stg:FFF_S2P6.stg(),game:document.getElementById('game').classList.contains('on')})")
        chk(f'cq2_s2_jin ramen: at full HP ({full} items read full) closing the menu plays the overheard beat', shop and moved, [o, shop, full, r])
        chk('cq2_s2_jin ramen: no page errors', not [e for e in g.errs if '404' not in e], g.errs[:3])
    async with h.Game(path='balanced') as g:
        await g.boot()
        await g.ev("(function(){var st=c2S(); st.q.cq2_s2_gar=0; st.qa='cq2_s2_gar'; c2QSync(); save(); return 1})()")
        await g.go('town', 4040, 3735); await g.wait(600)
        res = {}
        for k in ('gar', 'boat', 'mina'):
            await g.ev(f"c2Enter('{k}')")
            for i in range(5): await h.adv(g, 1)
            res[k + '_in'] = await g.ev(f"c2Room()")
            await g.ev(f"c2Out('{k}')")
            for i in range(5): await h.adv(g, 1)
        await g.ev("c2Enter('izak')")
        for i in range(5): await h.adv(g, 1)
        left = await g.ev("JSON.stringify({room:c2Room(),left:['s2P4Room_gar','s2P3Room_boat','s2P2Room_mina','s2P2Room_mshop'].filter(function(id){return !!document.getElementById(id)})})")
        chk('phase room canvases do not follow you into later rooms (Izakaya)', '"left":[]' in left and '"room":"izak"' in left, [res, left])
    async with h.Game(path='balanced') as g:
        await g.boot()
        o = await g.ev("(function(){var st=c2S(); delete st.e.guardGone_game; delete st.e.baseOpen_neo; delete st.e.seal_game; st.q.cq2_s2_jin=5; st.qa='cq2_s2_jin'; FFF_S2P6.setStg('izak'); c2QSync(); save(); return JSON.stringify({strip:FFF_S2P6.stripOpen(), guard:window.c2DoorGuardOpen('game')})})()")
        await g.go('town', 3680, 1700); await g.wait(800)
        await g.ev("String(walkTo(3680,1540,true))")
        for i in range(20):
            await h.adv(g, 1)
            if await g.ev("c2Room()==='gc'"): break
        r = await g.ev("JSON.stringify({room:c2Room(),said:FFF_UI.ST.events.filter(function(e){return /guard:talk:game/.test(e)}).length})")
        chk('High Score: with the strip open the Game Center guard lets you onto the floor (lm_game -> gc)', '"room":"gc"' in r and '"strip":true' in o, [o, r])
        chk('Game Center: no page errors', not [e for e in g.errs if '404' not in e], g.errs[:3])
    n = sum(R); print(f'RESULT {n}/{len(R)} passed'); sys.exit(0 if n == len(R) else 1)
asyncio.run(main())
