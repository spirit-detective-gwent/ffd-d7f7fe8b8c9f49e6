#!/workspace/pwenv/bin/python3
"""Heat A/B inside one tree (4x): guard patrol variants. usage: heat_ab.py TREE PORT"""
import asyncio, sys, json, os, time
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../lockeramb/lib.py')).read())
CFG = {'patrol': "1", 'hold': "W.dgF.find(q=>q.grd).hold=1", 'nocone': "W.dgF.find(q=>q.grd).cone.style.display='none'",
       'fightbg': "__fo(['bully3','bully4','bully3','bully4','bully3'], false, { dg: 'cafe', dgk: 'gperf', dgks: ['gperf'], dgm: W.inside.id })",
       'fighthold': "W.dgF.find(q=>q.grd).hold=1; __fo(['bully3','bully4','bully3','bully4','bully3'], false, { dg: 'cafe', dgk: 'gperf', dgks: ['gperf'], dgm: W.inside.id })"}
ORDER = os.environ.get('ORDER', 'patrol,hold,nocone,patrol,hold,nocone').split(',')
async def main():
    h = serve(root, PORT)
    async with async_playwright() as p:
        for c in ORDER:
            while os.getloadavg()[0] > 6: time.sleep(10)
            b, ctx, pg, errs = await boot(p); cdp = await ctx.new_cdp_session(pg); await cdp.send('Performance.enable')
            await ev(pg, "window.__fo=fight; cafEnter(); 1"); await pg.wait_for_timeout(1500); await skipall(pg, 6); await ev(pg, CLR)
            await ev(pg, "W.fading=false; cafGo('cooler'); 1"); await pg.wait_for_timeout(900); await skipall(pg, 4); await ev(pg, CLR + "; W.dlg=false; W.busy=false; W.cool=0; W.pan=null; W.ryo.x=972; W.ryo.y=450; place(W.ryo,0); 1")
            await cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4}); await ev(pg, CFG[c] + "; 1"); await pg.wait_for_timeout(1500)
            m0 = {x['name']: x['value'] for x in (await cdp.send('Performance.getMetrics'))['metrics']}; t0 = time.time()
            await pg.wait_for_timeout(6000)
            m1 = {x['name']: x['value'] for x in (await cdp.send('Performance.getMetrics'))['metrics']}; wall = time.time() - t0
            g = await ev(pg, "(function(){var f=W.dgF.find(q=>q.grd); return f?[f.st,Math.round(f.s.x),Math.round(f.s.y)]:null})()")
            print(c, round(100 * (m1['TaskDuration'] - m0['TaskDuration']) / wall, 1), 'layout', round(m1['LayoutDuration'] - m0['LayoutDuration'], 3), 'style', round(m1['RecalcStyleDuration'] - m0['RecalcStyleDuration'], 3), 'script', round(m1['ScriptDuration'] - m0['ScriptDuration'], 3), g, flush=True)
            await b.close()
    h.shutdown()
asyncio.run(main())
