#!/workspace/pwenv/bin/python3
import asyncio, sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import h
Q = """JSON.stringify([].map.call(document.querySelectorAll('.c2npc'),function(e){var b=e.getBoundingClientRect();return [e.dataset.who,Math.round(b.x),Math.round(b.y),e.style.zIndex,e===(W.c2n.sumire&&W.c2n.sumire.el)]}))"""
async def main():
    async with h.Game(path='compassionate', out='/workspace/herbcine/shots/scratch') as g:
        await g.boot()
        print('before go', await g.ev(Q))
        await g.go('clinic', 560, 640); print('after go', await g.ev(Q)); await g.wait(1500); print('later', await g.ev(Q))
        await g.ev("c2Pop()"); await g.wait(500); print('after c2Pop', await g.ev(Q))
        await g.ev("c2Pop()"); await g.wait(500); print('after c2Pop2', await g.ev(Q))
        print(await g.ev("""JSON.stringify([].map.call(document.querySelectorAll('.c2npc'),function(e){return [e.parentNode.id||e.parentNode.className, e.dataset.cel, e.dataset.loop]}))"""))
asyncio.run(main())
