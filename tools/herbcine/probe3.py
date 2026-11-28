#!/workspace/pwenv/bin/python3
import asyncio, sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import h
async def main():
    async with h.Game(path='compassionate', out='/workspace/herbcine/shots/scratch') as g:
        await g.boot(); await g.go('clinic', 640, 520); await g.wait(1200)
        print(await g.ev("""(function(){ var su=W.c2n.sumire; var L=document.getElementById('wisp')||layer; var out=[];
          var P={K:[611,421],SPOUT:[668,405],BOT:[678,472],SU:[702,446],RYO:[598,612],HAND:[650,606], home:[su.x,su.y]};
          Object.keys(P).forEach(function(k){var e=document.createElement('i'); e.className='dbg'; e.style.cssText='position:absolute;width:5px;height:5px;background:red;z-index:9999;left:'+(P[k][0]-2)+'px;top:'+(P[k][1]-2)+'px'; L.appendChild(e); var t=document.createElement('i'); t.className='dbg'; t.textContent=k; t.style.cssText='position:absolute;font:8px sans-serif;color:#f0f;z-index:9999;left:'+(P[k][0]+4)+'px;top:'+(P[k][1]-4)+'px'; L.appendChild(t);});
          var b=su.el.getBoundingClientRect(); return {cam:[W.cam.x,W.cam.y],S:W.S, su:[su.x,su.y,su.dir], r:[b.x,b.y,b.width,b.height], el:su.el.style.cssText, w:W.vw}})()"""))
        await g.shot('dbg_clinic')
        import PIL
asyncio.run(main())
