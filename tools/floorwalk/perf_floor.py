#!/workspace/pwenv/bin/python3
"""v6566-floorwalk perf, live vs branch, interleaved, waits while 1-min load > 6.
usage: perf_floor.py LIVE_TREE BRANCH_TREE OUT.json [reps]
Rooms: Storehouse Locker Corridor (LANE 1), Gym Foyer (ORDERS), Bleacher Concourse (HOME COURT), Trophy Hall (GRAY COAT FILE).
In each room Ryo tap-walks back and forth across the prop for 8 s (live detours around it), roamers stay, fight() stubbed.
fps at 1x and 4x CPU throttle; heat = main-thread busy % (TaskDuration / wall); heap = JSHeapUsed after each room."""
import asyncio, sys, json, os, time
A = sys.argv[1:]; sys.argv = [sys.argv[0], A[1], '53201']
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib.py')).read())
LIVE, BR, OUT = Path(A[0]), Path(A[1]), A[2]; REPS = int(A[3]) if len(A) > 3 else 3
SAMPLER = """()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);}"""
NEXT = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^(Next|Got it|Close|OK)/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(b.length)b[0].click()}"""
STUB = "(function(){ fight=function(){ ev('test:fight'); }; return 1; })()"
ROOMS = [('lockers', 'fldGo', 'FLDG', [520, 480, 630, 560]), ('foyer', 'gymGo', 'GYMG', [200, 520, 380, 620]),
         ('concourse', 'gymGo', 'GYMG', [520, 200, 760, 280]), ('trophy', 'gymGo', 'GYMG', [180, 480, 420, 620])]
def fps(ft):
    ft = ft[2:]; return round(1000 * len(ft) / sum(ft), 1) if ft else 0
def p5(ft):
    ft = sorted(ft[2:]); return round(1000 / ft[int(len(ft) * 0.95)], 1) if ft else 0
async def one(p, tree, port, thr):
    global PORT, root
    root, PORT = tree, port; h = serve(tree, port)
    b, ctx, pg, errs = await boot(p); cdp = await ctx.new_cdp_session(pg); await cdp.send('Performance.enable')
    await ev(pg, CLR); await ev(pg, STUB)
    if thr > 1: await cdp.send('Emulation.setCPUThrottlingRate', {'rate': thr})
    res = {}
    for room, go, G, r in ROOMS:
        await ev(pg, f"W.dgFight=null; W.fading=false; {go}('{room}'); 1"); await pg.wait_for_timeout(1500)
        for i in range(8): await pg.evaluate(NEXT); await pg.wait_for_timeout(120)
        await ev(pg, CLR + "; W.dlg=false; W.busy=false; 1")
        s = await ev(pg, f"{G}.{room}.s"); R = [v * s for v in r]; cy = (R[1] + R[3]) / 2; L = R[0] - 45; Rt = R[2] + 45
        await ev(pg, f"W.ryo.x={L}; W.ryo.y={cy}; place(W.ryo,0); W.path=[]; 1")
        m0 = {x['name']: x['value'] for x in (await cdp.send('Performance.getMetrics'))['metrics']}; t0 = time.time()
        await pg.evaluate(SAMPLER); el = 0; side = 1
        while el < 8000:
            await ev(pg, f"W.dlg=false; W.dgFight=null; walkTo({Rt if side else L},{cy},true); 1"); side ^= 1
            await pg.wait_for_timeout(1000); el += 1000
        ft = await pg.evaluate("()=>{window.__run=false;return window.__ft}")
        m1 = {x['name']: x['value'] for x in (await cdp.send('Performance.getMetrics'))['metrics']}; wall = time.time() - t0
        res[room] = {'fps': fps(ft), 'p95fps': p5(ft), 'heat': round(100 * (m1['TaskDuration'] - m0['TaskDuration']) / wall, 1), 'heap_mb': round(m1['JSHeapUsedSize'] / 1e6, 1)}
    res['errs'] = errs; await b.close(); h.shutdown(); return res
async def main():
    out = []
    async with async_playwright() as p:
        for thr in (1, 4):
            for rep in range(REPS if thr == 4 else 1):
                for i, (tag, tree) in enumerate((('live', LIVE), ('branch', BR)) if rep % 2 == 0 else (('branch', BR), ('live', LIVE))):
                    while os.getloadavg()[0] > 6: time.sleep(15)
                    r = await one(p, tree, 53201 + i + 2 * rep + 10 * thr, thr); out.append({'tag': tag, 'thr': thr, 'rep': rep, 'load': round(os.getloadavg()[0], 1), **r}); print(json.dumps(out[-1]), flush=True)
                    json.dump(out, open(OUT, 'w'), indent=1)
asyncio.run(main())
