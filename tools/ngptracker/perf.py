#!/workspace/pwenv/bin/python3
"""Interleaved perf: live (c1a3b8c) vs v6565-ngptracker, NG+ Ch1 spots, CPU throttle 4, dpr 3. heat = CPU busy % (TaskDuration / wall).
usage: perf.py [runs] [secs]"""
import asyncio, sys, json, os, threading, http.server, socketserver, functools
sys.path.insert(0, '/workspace/ngptracker/tools'); import repro_lib as R, h
from playwright.async_api import async_playwright
RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 3; SECS = float(sys.argv[2]) if len(sys.argv) > 2 else 6
PATHS = {'old': '/workspace/ngptracker/live_index.html', 'new': '/workspace/ngptracker/wt/index.html'}
SAMP = "()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);}"
def stats(ft):
    ft = ft[2:]; tot = sum(ft); s = sorted(ft, reverse=True); n = max(1, len(ft) // 100)
    return dict(fps=round(1000 * len(ft) / tot, 1), low1=round(1000 / (sum(s[:n]) / n), 1), over33=sum(1 for x in ft if x > 33.4))
async def metrics(cdp):
    m = await cdp.send('Performance.getMetrics'); return {x['name']: x['value'] for x in m['metrics']}
async def window(g, cdp):
    await g.pg.evaluate(SAMP); m0 = await metrics(cdp); await g.wait(int(SECS * 1000)); m1 = await metrics(cdp)
    await g.pg.evaluate("window.__run=false"); ft = await g.pg.evaluate("window.__ft"); r = stats(ft)
    r['busy'] = round(100 * (m1['TaskDuration'] - m0['TaskDuration']) / (m1['Timestamp'] - m0['Timestamp']), 1); return r
SPOTS = {
  'map_ngp': "(function(){ try{ if(W.inside) intExit(true) }catch(e){} W.ryo.x=1400; W.ryo.y=1500; place(W.ryo,0); camera(true); return 1 })()",
  'lib_hall_ngp': "(function(){ libGo('hall'); return 1 })()",
  'slam_turnin_ngp': None,
}
async def one(p, lab, out):
    g = h.Game(PATHS[lab]); g.dpr = 3
    await g.__aenter__()
    try:
        await R.setup(g, 'ngpcold')
        cdp = await g.ctx.new_cdp_session(g.pg); await cdp.send('Performance.enable'); await cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4})
        for k, js in SPOTS.items():
            if js: await g.ev(js); await g.wait(2500); await g.hush()
            else:
                await g.ev("sqStart('sq_kenta'); [0,1,2].forEach(function(i){ back(true,{ctx:{dg:'lib',dgk:'p'+i,dgks:['p'+i],dgm:'x'},endHp:40,endSpirit:0,win:true,switches:0,foes:['bully1'],drop:0}) }); 1"); await g.wait(1500); await g.hush()
                await g.ev("setTimeout(function(){ back(true,{ctx:{dg:'lib',dgk:'p9',dgks:['p9'],dgm:'x'},endHp:40,endSpirit:0,win:true,switches:0,foes:['bully1'],drop:0}); sqGiveItem('sq_kenta'); setTimeout(function(){ W.dlg=false; sqTurnIn('sq_kenta'); },1500); },300); 1")
            r = await window(g, cdp); out.setdefault(k, {}).setdefault(lab, []).append(r); print(lab, k, r, flush=True)
            await g.hush()
    finally:
        await g.__aexit__()
async def main():
    out = {}
    async with async_playwright() as p:
        for i in range(RUNS):
            for lab in (['old', 'new'] if i % 2 == 0 else ['new', 'old']):
                await one(p, lab, out)
    summ = {}
    for k, d in out.items():
        def avg(lab, f): v = [x[f] for x in d.get(lab, [])]; return round(sum(v) / len(v), 1) if v else None
        summ[k] = {lab: {f: avg(lab, f) for f in ('fps', 'low1', 'busy')} for lab in ('old', 'new')}
        summ[k]['heat_delta'] = round(summ[k]['new']['busy'] - summ[k]['old']['busy'], 1)
    print('SUMMARY', json.dumps(summ), flush=True)
    json.dump({'raw': out, 'summary': summ}, open('/workspace/ngptracker/perf.json', 'w'), indent=1)
asyncio.run(main())
