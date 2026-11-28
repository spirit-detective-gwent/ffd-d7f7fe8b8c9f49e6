#!/workspace/pwenv/bin/python3
"""v6566-prices perf sanity, live v6.5.64 vs branch, interleaved. usage: perf_prices.py LIVE_TREE BRANCH_TREE OUT.json [reps]
fps (mean, p95) at 1x and 4x CPU throttle; heat = main-thread busy % (TaskDuration / wall); heap after each scene.
Scenes: Cafeteria Staff Room (soda + food machines) idle, a walk past the machines, and the food machine prompt open."""
import asyncio, sys, json, os, time
A = sys.argv[1:]; sys.argv = [sys.argv[0], A[1], '53181']
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib.py')).read())
LIVE, BR, OUT = Path(A[0]), Path(A[1]), A[2]; REPS = int(A[3]) if len(A) > 3 else 2
SAMPLER = """()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);}"""
STUB = "(function(){ fight=function(){ ev('test:fight'); }; return 1; })()"
FREE = "W.dgFight=null; W.dlg=false; W.busy=false; W.cool=0; W.pan=null; W.fading=false"
SC1 = [('vend_room', "cafGo('staff')", None), ('vend_walk', "cafGo('staff')", "W.ryo.x=900; W.ryo.y=450; place(W.ryo,0); setTimeout(function(){ walkTo(300,450,true,false); },200)"),
       ('vend_prompt', "cafGo('staff')", "SAVE.items=30; SAVE.hp=20; cafVend('c2')")]
SC2 = [('line_room', "cafGo('line')", "W.ryo.x=520; W.ryo.y=560; place(W.ryo,0)"), ('line_walk', "cafGo('line')", "W.ryo.x=900; W.ryo.y=600; place(W.ryo,0); setTimeout(function(){ walkTo(250,450,true,false); },200)"),
       ('ch2_shop_fumi', "cafGo('line')", "SAVE.items=30; SAVE.shops=SAVE.shops||{}; delete SAVE.shops.nq_gk1; c2Shop('nq_gk1')")]
SCENES = SC2 if os.environ.get('SET') == '2' else SC1
def fps(ft):
    ft = ft[2:]; return round(1000 * len(ft) / sum(ft), 1) if ft else 0
def p5(ft):
    ft = sorted(ft[2:]); return round(1000 / ft[int(len(ft) * 0.95)], 1) if ft else 0
async def one(p, tree, port, thr):
    global PORT, root
    root, PORT = tree, port; h = serve(tree, port)
    b, ctx, pg, errs = await boot(p); cdp = await ctx.new_cdp_session(pg); await cdp.send('Performance.enable')
    await ev(pg, CLR); await ev(pg, STUB); await ev(pg, "cafEnter(); 1"); await pg.wait_for_timeout(1500); await skipall(pg, 6); await ev(pg, CLR)
    if thr > 1: await cdp.send('Emulation.setCPUThrottlingRate', {'rate': thr})
    res = {}
    for name, go, act in SCENES:
        await ev(pg, FREE + "; " + go + "; 1"); await pg.wait_for_timeout(900); await skipall(pg, 4); await ev(pg, CLR + "; " + FREE + "; 1")
        if act: await ev(pg, act + "; 1")
        await pg.wait_for_timeout(600)
        m0 = {x['name']: x['value'] for x in (await cdp.send('Performance.getMetrics'))['metrics']}; t0 = time.time()
        await pg.evaluate(SAMPLER); await pg.wait_for_timeout(7000)
        ft = await pg.evaluate("()=>{window.__run=false;return window.__ft}")
        m1 = {x['name']: x['value'] for x in (await cdp.send('Performance.getMetrics'))['metrics']}; wall = time.time() - t0
        res[name] = {'fps': fps(ft), 'p95fps': p5(ft), 'heat': round(100 * (m1['TaskDuration'] - m0['TaskDuration']) / wall, 1), 'heap_mb': round(m1['JSHeapUsedSize'] / 1e6, 1), 'at': await ev(pg, "(W.inside||{}).id")}
        await ev(pg, CLR + "; try{ var m=document.getElementById('wshop'); if(m) m.className=''; }catch(e){} 1")
    res['errs'] = errs; await b.close(); h.shutdown(); return res
async def main():
    out = []
    async with async_playwright() as p:
        for thr in (1, 4):
            for rep in range(REPS):
                for i, (tag, tree) in enumerate((('live', LIVE), ('branch', BR)) if rep % 2 == 0 else (('branch', BR), ('live', LIVE))):
                    while os.getloadavg()[0] > 6: time.sleep(15)
                    r = await one(p, tree, 53181 + i + 2 * rep + 10 * thr, thr); out.append({'tag': tag, 'thr': thr, 'rep': rep, **r}); print(json.dumps(out[-1]), flush=True)
                    json.dump(out, open(OUT, 'w'), indent=1)
    for thr in (1, 4):
        for sc in [s[0] for s in SCENES]:
            row = {}
            for tag in ('live', 'branch'):
                xs = [o[sc] for o in out if o['tag'] == tag and o['thr'] == thr]
                row[tag] = (round(sum(x['fps'] for x in xs) / len(xs), 1), round(sum(x['heat'] for x in xs) / len(xs), 1), max(x['heap_mb'] for x in xs))
            print('SUMMARY %dx %-12s live fps/heat/heap %s  branch %s' % (thr, sc, row['live'], row['branch']), flush=True)
    print('PERF DONE')
asyncio.run(main())
