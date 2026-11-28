#!/workspace/pwenv/bin/python3
"""4x perf of Flip's south-end clash battle vs live. 3 interleaved runs, dpr 3."""
import asyncio, json, os, statistics, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import h, t13_clash as T, perf_alley as P

LIVE = os.environ.get('LIVE_INDEX', '/workspace/herbcine/live/index.html')
NEW = os.environ.get('FFD_INDEX', '/workspace/nailsalley/wt/index.html')
THR = float(os.environ.get('THR', '4'))
DPR = int(os.environ.get('DPR', '3'))
RUNS = int(os.environ.get('RUNS', '3'))
SECS = float(os.environ.get('SECS', '8'))
OUT = Path('/workspace/nailsalley/shots/perf_clash.json')

async def one(index, label):
    g = h.Game(out='/workspace/nailsalley/shots', index=index, throttle=THR)
    async with g:
        cdp = await g.ctx.new_cdp_session(g.pg)
        await cdp.send('Performance.enable')
        try:
            await cdp.send('Emulation.setDeviceMetricsOverride', {
                'width': 390, 'height': 844, 'deviceScaleFactor': DPR, 'mobile': True
            })
        except Exception:
            pass
        if THR > 1:
            try: await cdp.send('Emulation.setCPUThrottlingRate', {'rate': THR})
            except Exception: pass
        await g.boot()
        await T.seed_at_clash(g)
        await T.start_walkin(g)
        st = await T.to_fight(g)
        await g.wait(400)
        r = await P.window(g.pg, cdp, SECS)
        r['label'] = label
        r['foes'] = (st or {}).get('foes')
        r['side'] = (st or {}).get('side')
        r['ig'] = (st or {}).get('ig')
        return r

async def main():
    print('clash battle remasure', open('/proc/loadavg').read().strip(), 'thr', THR, 'dpr', DPR, flush=True)
    runs = {'old': [], 'new': []}
    for i in range(RUNS):
        for lab, path in (('old', LIVE), ('new', NEW)):
            r = await one(path, lab)
            runs[lab].append(r)
            print(lab, 'run', i+1, {k: r.get(k) for k in ('fps','low1','cpu_busy_pct','heap_mb','foes','side')}, flush=True)
    def med(lab, k):
        xs = [x[k] for x in runs[lab] if k in x and x[k] is not None]
        return round(statistics.median(xs), 1) if xs else None
    s = dict(fps_old=med('old','fps'), fps_new=med('new','fps'),
             heat_old=med('old','cpu_busy_pct'), heat_new=med('new','cpu_busy_pct'),
             heap_old=med('old','heap_mb'), heap_new=med('new','heap_mb'))
    s['heat_delta'] = round(s['heat_new']-s['heat_old'], 1) if s['heat_new'] is not None and s['heat_old'] is not None else None
    print('CLASH SUMMARY', json.dumps(s), flush=True)
    OUT.write_text(json.dumps({'runs': runs, 'summary': s}, indent=1))
    print('wrote', OUT)

if __name__ == '__main__':
    asyncio.run(main())
