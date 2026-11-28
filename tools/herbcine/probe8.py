#!/workspace/pwenv/bin/python3
import asyncio, sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import h
Q = """JSON.stringify([].map.call(document.querySelectorAll('.c2npc'),function(e){return [e.dataset.who,e===(W.c2n.sumire&&W.c2n.sumire.el)]}).filter(function(r){return r[0]==='tsukikage'}))"""
async def main():
    async with h.Game(path='compassionate', out='/workspace/herbcine/shots/scratch') as g:
        await g.boot()
        print(await g.ev("c2Room()"))
        await g.ev("c2Enter('clinic')"); await g.wait(1500); await g.hush()
        print('natural enter', await g.ev("c2Room()"), await g.ev(Q))
        await g.ev("c2Out('clinic')"); await g.wait(1200)
        print('out', await g.ev("c2Room()"), await g.ev(Q))
        await g.ev("c2Enter('clinic')"); await g.wait(1500)
        print('enter again', await g.ev("c2Room()"), await g.ev(Q))
asyncio.run(main())
