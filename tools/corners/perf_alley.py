#!/workspace/pwenv/bin/python3
"""Quick 4x perf in the Nails alley (X2) vs live, 3 interleaved runs, dpr 3."""
import asyncio, json, os, statistics, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import h

LIVE = os.environ.get('LIVE_INDEX', '/workspace/herbcine/live/index.html')
NEW = os.environ.get('FFD_INDEX', '/workspace/nailsalley/wt/index.html')
THR = float(os.environ.get('THR', '4'))
DPR = int(os.environ.get('DPR', '3'))
RUNS = int(os.environ.get('RUNS', '3'))
SECS = float(os.environ.get('SECS', '8'))
OUT = Path('/workspace/nailsalley/shots/perf_alley.json')

SAMP = "()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);}"

def stats(ft):
    ft = ft[2:]
    if not ft:
        return {}
    tot = sum(ft); s = sorted(ft, reverse=True); n = max(1, len(ft)//100)
    return dict(fps=round(1000*len(ft)/tot, 1), low1=round(1000/(sum(s[:n])/n), 1),
                over33=sum(1 for x in ft if x > 33.4), frames=len(ft))

async def metrics(cdp):
    m = await cdp.send('Performance.getMetrics')
    return {x['name']: x['value'] for x in m['metrics']}

async def window(pg, cdp, secs):
    await pg.evaluate(SAMP)
    m0 = await metrics(cdp)
    await pg.wait_for_timeout(int(secs * 1000))
    m1 = await metrics(cdp)
    await pg.evaluate("window.__run=false")
    ft = await pg.evaluate("window.__ft")
    wall = m1['Timestamp'] - m0['Timestamp']
    r = stats(ft)
    r['cpu_busy_pct'] = round(100 * (m1['TaskDuration'] - m0['TaskDuration']) / wall, 1)
    r['heap_mb'] = round(m1['JSHeapUsedSize'] / 1e6, 1)
    return r

async def boot_at_x2(index, label):
    g = h.Game(out='/workspace/nailsalley/shots', index=index, throttle=THR)
    # patch dpr by creating context ourselves? Game uses dpr=1. Recreate after enter is messy.
    # We'll set dpr via a custom Game: temporarily monkey the class by passing...
    # Simpler: after __aenter__, we can't change dpr. Fork a thin opener here using h helpers.
    await g.__aenter__()
    # dpr 3: recreate is hard mid-flight; throttle is set. For heat vs live, dpr 1 vs 1 is comparable;
    # official spots use dpr 3. Re-open with a patched context.
    return g

async def measure_one(index, label, cdp_extra=True):
    # Use Game then attach CDP performance + optional dpr via cdp
    g = h.Game(out='/workspace/nailsalley/shots', index=index, throttle=THR)
    async with g:
        cdp = await g.ctx.new_cdp_session(g.pg)
        await cdp.send('Performance.enable')
        try:
            await cdp.send('Emulation.setDeviceMetricsOverride', {
                'width': 390, 'height': 844, 'deviceScaleFactor': DPR, 'mobile': True
            })
        except Exception as e:
            print('dpr', e)
        if THR > 1:
            try:
                await cdp.send('Emulation.setCPUThrottlingRate', {'rate': THR})
            except Exception:
                pass
        await g.boot()
        await g.gym_exit()
        await g.go_xy(1790, 2165)
        for _ in range(8):
            try:
                await g.ev("if(typeof g38tClashCheck==='function')g38tClashCheck(); if(root.FFF_NALLEY&&FFF_NALLEY.retrigger)FFF_NALLEY.retrigger();1")
            except Exception:
                pass
            await g.wait(250)
        await g.hush()
        r = await window(g.pg, cdp, SECS)
        r['label'] = label
        r['errs'] = g.errs[:3]
        return r

async def main():
    print('load', open('/proc/loadavg').read().strip(), 'thr', THR, 'dpr', DPR, flush=True)
    runs = {'old': [], 'new': []}
    for i in range(RUNS):
        for lab, path in (('old', LIVE), ('new', NEW)):
            r = await measure_one(path, lab)
            runs[lab].append(r)
            print(lab, 'run', i+1, {k: r[k] for k in ('fps', 'low1', 'cpu_busy_pct', 'heap_mb')}, flush=True)
    def med(lab, k):
        xs = [x[k] for x in runs[lab] if k in x]
        return round(statistics.median(xs), 1) if xs else None
    summary = {
        'fps_old': med('old', 'fps'), 'fps_new': med('new', 'fps'),
        'heat_old': med('old', 'cpu_busy_pct'), 'heat_new': med('new', 'cpu_busy_pct'),
        'heap_old': med('old', 'heap_mb'), 'heap_new': med('new', 'heap_mb'),
    }
    if summary['heat_old'] is not None and summary['heat_new'] is not None:
        summary['heat_delta'] = round(summary['heat_new'] - summary['heat_old'], 1)
    print('SUMMARY', json.dumps(summary), flush=True)
    OUT.write_text(json.dumps({'thr': THR, 'dpr': DPR, 'runs': runs, 'summary': summary}, indent=1))
    print('wrote', OUT)

if __name__ == '__main__':
    asyncio.run(main())
