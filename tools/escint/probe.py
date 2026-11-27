#!/workspace/pwenv/bin/python3
import sys, json, asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import harness as H
async def main():
    H.serve(sys.argv[1], 53712)
    async with H.async_playwright() as p:
        b, ctx, pg, errs = await H.boot(p, 53712)
        await H.ch1_ready(pg)
        print(json.dumps(await H.ev(pg, "W.tagL.map(function(t){return [t.key,t.cls,Math.round(t.ax),Math.round(t.ay),t.R]}).slice(0,40)")))
        print(json.dumps(await H.ev(pg, "({x:W.ryo.x,y:W.ryo.y,start:WD.start,vms:(W.vms||[]).map(function(m){return [m.v.id,m.v.x,m.v.y]}),places:PLACES.slice(0,40).map(function(p){return [p.id,p.x,p.y]})})")))
        await b.close()
asyncio.run(main())
