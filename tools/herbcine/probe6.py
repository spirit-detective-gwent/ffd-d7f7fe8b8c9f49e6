#!/workspace/pwenv/bin/python3
import asyncio, sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import h
async def main():
    async with h.Game(path='compassionate', out='/workspace/herbcine/shots/scratch') as g:
        await g.boot(); await g.go('clinic', 600, 640); await g.wait(800)
        await g.ev("(function(){var su=W.c2n.sumire; celLoopOff(su); su.x=702; su.y=446; place(su,0); W.ryo.x=598;W.ryo.y=612;place(W.ryo,0); W.aoi.x=532;W.aoi.y=624;place(W.aoi,0); camera(true); var a=document.createElement('i'); a.id='hsanchor'; a.style.cssText='position:absolute;left:611px;top:451px;width:2px;height:60px'; (document.getElementById('wisp')||layer).appendChild(a); FFF_SCAM.shot({el:a},{z:1.32,ms:50,f:0.42}); return 1})()")
        await g.wait(1200)
        r = await g.ev("""(function(){ var L=document.getElementById('wisp')||layer; var out={}; 
          var P={K:[611,421],SPOUT:[668,405],BOT:[678,472],SU:[702,446],RYO:[598,612],HAND:[650,606],P1:[640,380],P2:[700,380]};
          Object.keys(P).forEach(function(k){var e=document.createElement('i'); e.style.cssText='position:absolute;width:1px;height:1px;left:'+P[k][0]+'px;top:'+P[k][1]+'px'; L.appendChild(e); var b=e.getBoundingClientRect(); out[k]=[b.x,b.y]; e.remove();});
          return out})()""")
        print(json.dumps(r))
        await g.hush()
        await g.pg.screenshot(path='/workspace/herbcine/shots/scratch/zoom_full.png')
asyncio.run(main())
