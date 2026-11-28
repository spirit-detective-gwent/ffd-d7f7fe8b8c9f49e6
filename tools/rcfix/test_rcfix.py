#!/workspace/pwenv/bin/python3
"""v6566-rc integration fixes found in the Ch2 playthrough. usage: test_rcfix.py   (FFD_INDEX=... for another index.html)
 2. S2 phase quests (Night Runs..Jin) as the active quest: the journal target is the phase's own pin, not the 'Clinic' fallback.
 1. Wagashi Row on Compassionate (balanced): at stage 'open' the pin points at Flip (journal step 1), not Chiyo's door
    (the door talk never advanced the quest, so the pin looped there forever).
 3. Funayado lookout (cq2_s2_boat) and the quay garage (cq2_s2_gar): a tap on the door walks to a reachable lip and enters the
    room (before: no handler entered either room and the door rects sat on unwalkable ground); leaving puts Ryo back on the lip."""
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
    n = sum(R); print(f'RESULT {n}/{len(R)} passed'); sys.exit(0 if n == len(R) else 1)
asyncio.run(main())
