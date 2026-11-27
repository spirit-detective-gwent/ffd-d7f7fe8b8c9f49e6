#!/workspace/pwenv/bin/python3
"""Map fps / heat at key spots, new vs live. usage: map_perf.py NEW OLD [pn] [po]"""
import sys, json, asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import harness as H
NEW, OLD = sys.argv[1], sys.argv[2]; PN=int(sys.argv[3]) if len(sys.argv)>3 else 53861; PO=int(sys.argv[4]) if len(sys.argv)>4 else 53862
SPOTS = [(1440,3300),(1440,1560),(2160,2850),(1800,3000)]
RAF = "new Promise(function(res){var n=0,t0=performance.now(),w=0,l=t0;(function f(t){n++;w=Math.max(w,t-l);l=t;if(t-t0<4000)requestAnimationFrame(f);else res({fps:+(n*1000/(t-t0)).toFixed(1),worst:+w.toFixed(0)})})(t0)})"
async def bench(p, root, port, thr):
    H.serve(root, port)
    b, ctx, pg, errs = await H.boot(p, port)
    cdp = await ctx.new_cdp_session(pg); await cdp.send('Performance.enable')
    await cdp.send('Emulation.setCPUThrottlingRate', {'rate': thr})
    out=[]; heat=[]
    for (x,y) in SPOTS:
        await H.ch1_ready(pg, x, y); await H.ev(pg, "W.ambNext=1e9"); await pg.wait_for_timeout(800)
        m0 = {m['name']:m['value'] for m in (await cdp.send('Performance.getMetrics'))['metrics']}
        r = await pg.evaluate(RAF)
        m1 = {m['name']:m['value'] for m in (await cdp.send('Performance.getMetrics'))['metrics']}
        out.append(r); heat.append(round((m1['TaskDuration']-m0['TaskDuration'])/4*100,1))
    await b.close(); return {'fps': out, 'heat': heat, 'errs': errs[:2]}
async def main():
    async with H.async_playwright() as p:
        res={}
        for name, root, port in (('new',NEW,PN),('live',OLD,PO)):
            res[name]={}
            for thr in (1,4):
                res[name][f'{thr}x']=await bench(p, root, port+ (0 if thr==1 else 10), thr)
            print(name, json.dumps(res[name]), flush=True)
asyncio.run(main())
