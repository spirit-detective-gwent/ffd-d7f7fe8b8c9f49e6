#!/workspace/pwenv/bin/python3
"""v6566-rc integration fixes found in the Ch2 playthrough. usage: test_rcfix.py   (FFD_INDEX=... for another index.html)
 1. Wagashi Row on Compassionate (balanced): at stage 'open' the pin points at Flip (journal step 1), not Chiyo's door
    (the door talk never advanced the quest, so the pin looped there forever)."""
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
    n = sum(R); print(f'RESULT {n}/{len(R)} passed'); sys.exit(0 if n == len(R) else 1)
asyncio.run(main())
