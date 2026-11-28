#!/workspace/pwenv/bin/python3
"""Storehouse bay perf, live vs branch, interleaved. usage: perf_bay.py LIVE_TREE BRANCH_TREE OUT.json [reps]
Scenes: arrival (first entry cinematic incl. the walk-up; fight() stubbed so both stay on the map), bay_roam (entry done,
2 roamers), lockers (next room). fps at 1x and 4x CPU throttle; heat = main-thread busy % (TaskDuration / wall)."""
import asyncio, sys, json, os, time
A = sys.argv[1:]; sys.argv = [sys.argv[0], A[1], '52881']
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib.py')).read())
LIVE, BR, OUT = Path(A[0]), Path(A[1]), A[2]; REPS = int(A[3]) if len(A) > 3 else 3
SAMPLER = """()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);}"""
NEXT = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^(Next|Got it|Close|OK)/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(b.length)b[0].click()}"""
STUB = "(function(){ fight=function(){ ev('test:fight'); }; return 1; })()"
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
    for name, js, ms in [('arrival', 'fldEnter()', 9000),
                         ('bay_roam', "W.dgFight=null; W.dlg=false; W.busy=false; fldS().e.entry=1; W.fading=false; fldGo('bay'); W.dlg=false; W.busy=false; W.ryo.x=1000; W.ryo.y=740; place(W.ryo,0)", 8000),
                         ('lockers', "W.dgFight=null; W.fading=false; fldGo('lockers'); W.dlg=false; W.busy=false", 8000)]:
        await ev(pg, js + '; 1'); await pg.wait_for_timeout(300 if name == 'arrival' else 1500)
        m0 = {x['name']: x['value'] for x in (await cdp.send('Performance.getMetrics'))['metrics']}; t0 = time.time()
        await pg.evaluate(SAMPLER); el = 0
        while el < ms:
            if name == 'arrival': await pg.evaluate(NEXT)
            await pg.wait_for_timeout(1000); el += 1000
        ft = await pg.evaluate("()=>{window.__run=false;return window.__ft}")
        m1 = {x['name']: x['value'] for x in (await cdp.send('Performance.getMetrics'))['metrics']}; wall = time.time() - t0
        res[name] = {'fps': fps(ft), 'p95fps': p5(ft), 'heat': round(100 * (m1['TaskDuration'] - m0['TaskDuration']) / wall, 1), 'heap_mb': round(m1['JSHeapUsedSize'] / 1e6, 1)}
    res['errs'] = errs; await b.close(); h.shutdown(); return res
async def main():
    out = []
    async with async_playwright() as p:
        for thr in (1, 4):
            for rep in range(REPS if thr == 4 else 1):
                for i, (tag, tree) in enumerate((('live', LIVE), ('branch', BR))):
                    while os.getloadavg()[0] > 6: time.sleep(15)
                    r = await one(p, tree, 52881 + i + 2 * rep + 10 * thr, thr); out.append({'tag': tag, 'thr': thr, 'rep': rep, **r}); print(json.dumps(out[-1]), flush=True)
                    json.dump(out, open(OUT, 'w'), indent=1)
asyncio.run(main())
