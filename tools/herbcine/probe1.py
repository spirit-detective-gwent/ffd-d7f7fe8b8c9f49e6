#!/workspace/pwenv/bin/python3
import asyncio, sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import h
async def main():
    async with h.Game(path='compassionate', out='/workspace/herbcine/shots/scratch') as g:
        await g.boot(); await g.go('clinic', 560, 640)
        print(await g.ev("""(function(){var o=[];var L=document.getElementById('wisp')||layer; [].forEach.call(L.children,function(e){var b=e.getBoundingClientRect(); o.push([e.tagName,e.id,e.className.toString().slice(0,30),e.dataset&&JSON.stringify(e.dataset).slice(0,60),Math.round(b.x),Math.round(b.y),Math.round(b.width),Math.round(b.height)])}); return o.filter(function(r){return r[6]>0&&r[6]<80})})()"""))
        print(await g.ev("Object.keys(W.c2n||{})"))
        print(await g.ev("(function(){var s=W.c2n.sumire; return [s.x,s.y,s.dir, s.el.className, s.el.dataset.npc]})()"))
        print(await g.ev("document.getElementById('wbub')? document.getElementById('wbub').outerHTML.slice(0,300):null"))
asyncio.run(main())
