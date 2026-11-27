#!/workspace/pwenv/bin/python3
import sys, json, asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import harness as H
ROOT=sys.argv[1]; PORT=int(sys.argv[2]) if len(sys.argv)>2 else 53715
async def main():
    H.serve(ROOT, PORT)
    async with H.async_playwright() as p:
        b, ctx, pg, errs = await H.boot(p, PORT)
        await H.ch1_ready(pg, 1800, 3000)
        print(await H.ev(pg, "intGoX_try=1"))
        print(json.dumps(await pg.evaluate("(()=>{WORLD_API.intGoX('dh_cafe');return 1})()")))
        await pg.wait_for_timeout(3000)
        print(json.dumps(await H.ev(pg, "({in:W.inside&&W.inside.id,dgF:(W.dgF||[]).map(function(f){return [f.key,f.id,Math.round(f.s.x),Math.round(f.s.y),f.st]}),ryo:[W.ryo.x,W.ryo.y],dlg:W.dlg,busy:W.busy,cut:W.cut,tl:tagsLive(),tags:(W.tagL||[]).map(function(t){return t.key})})")))
        print(await H.ev(pg, "(function(){try{dgPop()}catch(e){return 'ERR '+e.message}return (W.dgF||[]).length})()"))
        print(json.dumps(await H.ev(pg, "(W.dgF||[]).map(function(f){return [f.key,f.id,Math.round(f.s.x),Math.round(f.s.y),f.st]})")))
        print(errs)
        await b.close()
asyncio.run(main())
