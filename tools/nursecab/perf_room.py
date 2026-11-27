#!/workspace/pwenv/bin/python3
"""Nurse's office perf, live vs branch, interleaved. usage: perf_room.py LIVE_TREE BRANCH_TREE OUT.json [reps]
fps at 1x and 4x CPU throttle; heat = main-thread busy % (TaskDuration / wall) at 4x."""
import asyncio, sys, json, os, time
sys.argv, A = [sys.argv[0], sys.argv[2], '52681'], sys.argv[1:]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_cab.py')).read().split('async def main():')[0])
LIVE, BR, OUT = Path(A[0]), Path(A[1]), A[2]; REPS = int(A[3]) if len(A) > 3 else 3
SAMPLER = """()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);}"""
def fps(ft):
    ft = ft[2:]; return round(1000 * len(ft) / sum(ft), 1) if ft else 0
async def one(p, tree, port, thr):
    global PORT, root
    root, PORT = tree, port; h = serve(tree, port)
    b, ctx, pg, errs = await boot(p); cdp = await ctx.new_cdp_session(pg); await cdp.send('Performance.enable')
    await ev(pg, CLR); await ev(pg, SETUP); await go_nurse(pg); await ev(pg, "qDoneNow()"); await ev(pg, CLR)
    if thr > 1: await cdp.send('Emulation.setCPUThrottlingRate', {'rate': thr})
    res = {}
    for name, js in [('room_idle', 'W.dlg=false'), ('room_cabinet', "root.FFF_FAST_KIT=1; n9Cabinet(); root.FFF_FAST_KIT=0")]:
        await ev(pg, js); await pg.wait_for_timeout(1500)
        m0 = {x['name']: x['value'] for x in (await cdp.send('Performance.getMetrics'))['metrics']}; t0 = time.time()
        await pg.evaluate(SAMPLER); await pg.wait_for_timeout(8000); ft = await pg.evaluate("()=>{window.__run=false;return window.__ft}")
        m1 = {x['name']: x['value'] for x in (await cdp.send('Performance.getMetrics'))['metrics']}; wall = time.time() - t0
        res[name] = {'fps': fps(ft), 'heat': round(100 * (m1['TaskDuration'] - m0['TaskDuration']) / wall, 1), 'heap_mb': round(m1['JSHeapUsedSize'] / 1e6, 1)}
    res['errs'] = errs; await b.close(); h.shutdown(); return res
async def main():
    out = []
    async with async_playwright() as p:
        for thr in (1, 4):
            for rep in range(REPS if thr == 4 else 1):
                for i, (tag, tree) in enumerate((('live', LIVE), ('branch', BR))):
                    while os.getloadavg()[0] > 6: time.sleep(15)
                    r = await one(p, tree, 52681 + i + 2 * rep + 10 * thr, thr); out.append({'tag': tag, 'thr': thr, 'rep': rep, **r}); print(json.dumps(out[-1]), flush=True)
                    json.dump(out, open(OUT, 'w'), indent=1)
asyncio.run(main())
