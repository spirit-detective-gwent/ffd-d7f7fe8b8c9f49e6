#!/workspace/pwenv/bin/python3
import sys, json, asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import harness as H
import scen
ROOT=sys.argv[1]; PORT=int(sys.argv[2])
async def main():
    H.serve(ROOT, PORT)
    async with H.async_playwright() as p:
        b, ctx, pg, errs = await H.boot(p, PORT)
        await H.ch1_ready(pg, 1800, 3000); await H.ev(pg, scen.MK); await H.ev(pg, "window.FFF_ESC_ROLL=0; W.ambNext=1e9")
        await H.ev(pg, scen.PROBE); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='/workspace/escint/logs/s_base.png')
        print(json.dumps(await pg.evaluate("(()=>{var b=document.querySelector('#wtags .wtag[data-k=\"out:vm_cafe\"]');var r=b.getBoundingClientRect();var out=[];for(var dx=-30;dx<=30;dx+=15)for(var dy=-30;dy<=30;dy+=15){var e=document.elementFromPoint(r.x+r.width/2+dx,r.y+r.height/2+dy);out.push((e&&(e.id||e.className||e.tagName)).toString().slice(0,20))}return {r:[r.x,r.y,r.width,r.height],cls:b.className,out:out,disp:getComputedStyle(b).display,pe:getComputedStyle(b).pointerEvents,box:getComputedStyle(document.getElementById('wtags')).display}})()")))
        await b.close()
asyncio.run(main())
