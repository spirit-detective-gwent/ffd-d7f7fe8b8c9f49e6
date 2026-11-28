#!/workspace/pwenv/bin/python3
"""Gouki battle perf, live vs branch, interleaved (waits while 1-min load > 6). usage: perf_gouki.py LIVE BRANCH OUT.json [reps]
fps at 1x and 4x CPU throttle; heat = main-thread busy % (TaskDuration / wall)."""
import sys, asyncio, json, os, time
from pathlib import Path
here = Path(__file__).resolve().parent
A = sys.argv[1:]; LIVE, BR, OUT = A[0], A[1], A[2]; REPS = int(A[3]) if len(A) > 3 else 2
sys.argv = [sys.argv[0], BR, '53001', 'X']
exec(compile(open(here / 'test_ofuda.py').read().split('async def main():')[0], 'test_ofuda', 'exec'))
SAMPLER = """()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);}"""
def fps(ft):
    ft = ft[2:]; return round(1000 * len(ft) / sum(ft), 1) if ft else 0
async def window(pg, cdp, secs, act=None):
    m0 = {x['name']: x['value'] for x in (await cdp.send('Performance.getMetrics'))['metrics']}; t0 = time.time()
    await pg.evaluate(SAMPLER)
    if act: await act()
    await pg.wait_for_timeout(int(secs * 1000)); ft = await pg.evaluate("()=>{window.__run=false;return window.__ft}")
    m1 = {x['name']: x['value'] for x in (await cdp.send('Performance.getMetrics'))['metrics']}; wall = time.time() - t0
    s = sorted(ft[2:]) or [16.7]
    return {'fps': fps(ft), 'p95ms': round(s[int(len(s) * 0.95)], 1), 'heat': round(100 * (m1['TaskDuration'] - m0['TaskDuration']) / wall, 1), 'heap_mb': round(m1['JSHeapUsedSize'] / 1e6, 1)}
async def one(p, tree, port, thr):
    global ROOT, PORT
    ROOT, PORT = tree, port; h = H.serve(tree, port)
    b, ctx, pg, errs = await H.boot(p, port); cdp = await ctx.new_cdp_session(pg); await cdp.send('Performance.enable')
    await H.ch1_ready(pg, 1440, 3300)
    res = {}
    for ng in (0, 1):
        await H.ev(pg, SET + "(" + json.dumps({'path': 'fierce', 'ngp': ng, 'lamp': 1}) + ")")
        await H.ev(pg, "var S=gymS();S.e.press=1;gymGo('arena');1"); await pg.wait_for_timeout(2000); await adv(pg)
        await H.ev(pg, "root.FFF_NO_VC=1;gkFight();1"); await wait_play(pg); await pg.wait_for_timeout(2500)
        if thr > 1: await cdp.send('Emulation.setCPUThrottlingRate', {'rate': thr})
        res['battle_idle' + ('_ngp' if ng else '')] = await window(pg, cdp, 8)
        if thr > 1: await cdp.send('Emulation.setCPUThrottlingRate', {'rate': 1})
        await H.ev(pg, "FFF_UI.ST.b.s[0].hp=0;FFF_UI.ST.b.over=true;FFF_UI.ST.b.winner=1;FFF_UI.ST.story.ctx={};FFF_UI.endMatch();1"); await pg.wait_for_timeout(1500)
        await drive(pg, 6)
    # the Double finale (gkFin) straight from a resumed finale save
    await H.ev(pg, SET + "(" + json.dumps({'path': 'fierce', 'ngp': 0, 'lamp': 1}) + ")")
    await H.ev(pg, "SAVE.dbl=1;SAVE.gkPh=1;SAVE.gkRevives=1;save();var S=gymS();S.e.press=1;gymGo('arena');FFF_UI.ST.inGame=false;W.dlg=false;W.cut=false;gkFight();1")
    await wait_play(pg); await pg.wait_for_timeout(2500)
    await pg.evaluate("()=>{var b=FFF_UI.ST.b;b.s[0].spirit=40;if(b.bench)b.bench.spirit=40;if(FFF_UI.render)FFF_UI.render()}"); await pg.wait_for_timeout(600)
    db = await pg.evaluate("()=>{var e=document.getElementById('btnDbl');if(!e||!e.offsetParent)return null;var r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}")
    if thr > 1: await cdp.send('Emulation.setCPUThrottlingRate', {'rate': thr})
    async def tapd():
        if db: await pg.touchscreen.tap(*db)
    res['double_cine'] = await window(pg, cdp, 6, tapd); res['double_cine']['tapped'] = bool(db)
    if thr > 1: await cdp.send('Emulation.setCPUThrottlingRate', {'rate': 1})
    res['errs'] = errs; await b.close(); h.shutdown(); return res
async def main():
    out = []
    async with H.async_playwright() as p:
        for thr in tuple(int(x) for x in os.environ.get('THR', '1,4').split(',')):
            for rep in range(REPS):
                order = (('live', LIVE), ('branch', BR)) if rep % 2 == 0 else (('branch', BR), ('live', LIVE))
                for i, (tag, tree) in enumerate(order):
                    while os.getloadavg()[0] > 6: time.sleep(15)
                    r = await one(p, tree, 53001 + i + 2 * rep + 10 * thr, thr); out.append({'tag': tag, 'thr': thr, 'rep': rep, 'load': round(os.getloadavg()[0], 1), **r}); print(json.dumps(out[-1]), flush=True)
                    json.dump(out, open(OUT, 'w'), indent=1)
asyncio.run(main())
