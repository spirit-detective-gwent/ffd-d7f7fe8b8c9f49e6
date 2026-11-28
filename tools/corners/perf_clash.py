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

PW = float(os.environ.get('PW', '0.8'))  # pre square-off is ~1 s
CW = float(os.environ.get('CW', '3.0'))  # post cine is ~3.4 s

async def one(index, label):
    g = h.Game(out='/workspace/nailsalley/shots', index=index, throttle=THR)
    out = {}
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
        await T.seed(g); await T.walkin(g)
        # pre: new = the square-off cine; live = the same street spot right after Flip's line (it cuts to battle)
        st = await T.until(g, lambda s: s['dlg'] or s['xc'] == 'pre' or s['ig'], 40, 200)
        if label == 'new':
            st = await T.through_clash_line(g)  # returns as the square-off starts (~1 s cine)
        out['pre'] = await P.window(g.pg, cdp, PW); out['pre']['xc'] = st.get('xc')
        if label != 'new':
            await T.through_clash_line(g)  # live: tap Flip's line, it cuts to the battle
        st = await T.to_battle(g)
        await g.wait(400)
        out['battle'] = await P.window(g.pg, cdp, SECS); out['battle']['foes'] = st.get('foes'); out['battle']['side'] = st.get('side'); out['battle']['ig'] = st.get('ig')
        await T.win(g)
        st = await T.to_post(g)  # new: post cine up; live: Flip's line on the street
        out['post'] = await P.window(g.pg, cdp, CW); out['post']['xc'] = st.get('xc')
        out['label'] = label
        return out

async def main():
    print('clash cines + battle', open('/proc/loadavg').read().strip(), 'thr', THR, 'dpr', DPR, flush=True)
    runs = {'old': [], 'new': []}
    for i in range(RUNS):
        for lab, path in (('old', LIVE), ('new', NEW)):
            r = await one(path, lab)
            runs[lab].append(r)
            print(lab, 'run', i+1, {w: {k: r[w].get(k) for k in ('fps','low1','cpu_busy_pct','heap_mb','xc','foes','ig')} for w in ('pre','battle','post')}, flush=True)
    def med(lab, w, k):
        xs = [x[w][k] for x in runs[lab] if x[w].get(k) is not None]
        return round(statistics.median(xs), 1) if xs else None
    s = {}
    for w in ('pre', 'battle', 'post'):
        d = dict(fps_old=med('old', w, 'fps'), fps_new=med('new', w, 'fps'), low1_old=med('old', w, 'low1'), low1_new=med('new', w, 'low1'),
                 heat_old=med('old', w, 'cpu_busy_pct'), heat_new=med('new', w, 'cpu_busy_pct'), heap_old=med('old', w, 'heap_mb'), heap_new=med('new', w, 'heap_mb'))
        d['heat_delta'] = round(d['heat_new'] - d['heat_old'], 1) if None not in (d['heat_new'], d['heat_old']) else None
        s[w] = d
    print('CLASH SUMMARY', json.dumps(s), flush=True)
    OUT.write_text(json.dumps({'runs': runs, 'summary': s}, indent=1))
    print('wrote', OUT)

if __name__ == '__main__':
    asyncio.run(main())
