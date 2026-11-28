#!/workspace/pwenv/bin/python3
import asyncio, sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import h
async def main():
    async with h.Game(path='compassionate', out='/workspace/herbcine/shots/scratch') as g:
        await g.boot(); await g.go('clinic', 560, 640); await g.wait(1500)
        print(await g.ev("""(function(){var o=[];[].forEach.call(document.querySelectorAll('#world *'),function(e){var b=e.getBoundingClientRect(); if(b.width>0&&b.width<60&&b.height<40&&b.y>150&&b.y<560&&b.x>200&&e.children.length==0&&getComputedStyle(e).visibility!='hidden') o.push([e.tagName,e.id,String(e.className).slice(0,40),(e.textContent||'').slice(0,10),Math.round(b.x),Math.round(b.y),Math.round(b.width),Math.round(b.height), e.parentNode.id||String(e.parentNode.className).slice(0,20)])}); return o})()"""))
asyncio.run(main())
