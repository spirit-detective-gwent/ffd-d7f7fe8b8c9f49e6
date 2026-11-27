#!/workspace/pwenv/bin/python3
"""baseexp perf, live v6.5.64 vs branch, interleaved. usage: perf_baseexp.py LIVE_TREE BRANCH_TREE OUT.json [reps]
fps (mean, p95) at 1x and 4x CPU throttle; heat = main-thread busy % (TaskDuration / wall); heap after each scene.
Scenes pair each new branch room with the nearest live room of the same base."""
import asyncio, sys, json, os, time
A = sys.argv[1:]; sys.argv = [sys.argv[0], A[1], '52981']
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../lockeramb/lib.py')).read())
LIVE, BR, OUT = Path(A[0]), Path(A[1]), A[2]; REPS = int(A[3]) if len(A) > 3 else 2
SAMPLER = """()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);}"""
NEXT = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^(Next|Skip|Got it|Close|OK)/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(b.length)b[0].click()}"""
STUB = "(function(){ fight=function(){ ev('test:fight'); }; return 1; })()"
FREE = "W.dgFight=null; W.dlg=false; W.busy=false; W.cool=0; W.libPend=null; W.pan=null; W.fading=false"
FLDOK = "var S=fldS(); S.e.entry=1; S.f.fbay0=1; S.f.fbay1=1; S.e.surprise=1; S.e.bay=1; S.e.track=1; S.e.lockers=1; S.e.coach=1; S.e.cage=1; S.e.showers=1; S.e.trainer=1; S.e.booth=1"
CAFOK = "var C=cafS(); ['line','kitchen','staff','cooler','dock','dish','bakery'].forEach(function(k){C.e[k]=1;})"
def walk(x0, y0, x1, y1): return "W.ryo.x=%d; W.ryo.y=%d; place(W.ryo,0); setTimeout(function(){ walkTo(%d,%d,false,false); },200)" % (x0, y0, x1, y1)
SCENES = [  # name, live js, branch js
  ('caf_guard_room', "cafGo('kitchen')", "cafGo('cooler')"),
  ('caf_guard_walk', "cafGo('line'); " + walk(900, 450, 300, 450), "cafGo('dock'); " + walk(950, 700, 160, 700)),
  ('caf_bakery', "cafGo('staff')", "cafGo('bakery')"),
  ('track_lap', "fldGo('track')", "fldS().e.slowArm=1; fldGo('track')"),
  ('fld_new_rooms', "fldGo('bay')", "fldGo('cage')"),
  ('fld_booth_walk', "fldGo('coach'); " + walk(300, 420, 950, 520), "fldGo('booth'); " + walk(300, 420, 950, 520)),
]
def fps(ft):
    ft = ft[2:]; return round(1000 * len(ft) / sum(ft), 1) if ft else 0
def p5(ft):
    ft = sorted(ft[2:]); return round(1000 / ft[int(len(ft) * 0.95)], 1) if ft else 0
async def one(p, tree, port, thr, tag):
    global PORT, root
    root, PORT = tree, port; h = serve(tree, port)
    b, ctx, pg, errs = await boot(p); cdp = await ctx.new_cdp_session(pg); await cdp.send('Performance.enable')
    await ev(pg, CLR); await ev(pg, STUB); await ev(pg, "cafEnter(); 1"); await pg.wait_for_timeout(1500); await skipall(pg, 6); await ev(pg, CLR)
    await ev(pg, CAFOK + "; " + FLDOK + "; save(); 1")
    if thr > 1: await cdp.send('Emulation.setCPUThrottlingRate', {'rate': thr})
    res = {}
    for name, lj, bj in SCENES:
        js = lj if tag == 'live' else bj
        if name.startswith('track') or name.startswith('fld'):
            if not await ev(pg, "!!fldRoom()"): await ev(pg, FREE + "; fldEnter(); 1"); await pg.wait_for_timeout(1500); await skipall(pg, 6); await ev(pg, CLR + "; " + FLDOK + "; 1")
        await ev(pg, FREE + "; " + js + "; 1"); await pg.wait_for_timeout(900); await skipall(pg, 4); await ev(pg, CLR + "; " + FREE + "; 1")
        if 'walk' in name: await ev(pg, js.split('; ', 1)[1] + "; 1")
        await pg.wait_for_timeout(600)
        m0 = {x['name']: x['value'] for x in (await cdp.send('Performance.getMetrics'))['metrics']}; t0 = time.time()
        await pg.evaluate(SAMPLER); el = 0
        while el < 7000:
            await pg.evaluate(NEXT); await pg.wait_for_timeout(1000); el += 1000
        ft = await pg.evaluate("()=>{window.__run=false;return window.__ft}")
        m1 = {x['name']: x['value'] for x in (await cdp.send('Performance.getMetrics'))['metrics']}; wall = time.time() - t0
        info = await ev(pg, "[(W.inside||{}).id, (W.dgF||[]).length, W.fldLap&&W.fldLap.slowTo!=null]")
        res[name] = {'fps': fps(ft), 'p95fps': p5(ft), 'heat': round(100 * (m1['TaskDuration'] - m0['TaskDuration']) / wall, 1), 'heap_mb': round(m1['JSHeapUsedSize'] / 1e6, 1), 'at': info}
    res['errs'] = errs; await b.close(); h.shutdown(); return res
async def main():
    out = []
    async with async_playwright() as p:
        for thr in (1, 4):
            for rep in range(REPS):
                for i, (tag, tree) in enumerate((('live', LIVE), ('branch', BR)) if rep % 2 == 0 else (('branch', BR), ('live', LIVE))):
                    while os.getloadavg()[0] > 6: time.sleep(15)
                    r = await one(p, tree, 52981 + i + 2 * rep + 10 * thr, thr, tag); out.append({'tag': tag, 'thr': thr, 'rep': rep, **r}); print(json.dumps(out[-1]), flush=True)
                    json.dump(out, open(OUT, 'w'), indent=1)
asyncio.run(main())
