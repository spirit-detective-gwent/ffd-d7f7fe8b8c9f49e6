#!/workspace/pwenv/bin/python3
"""Record the Flip clash cines (walk-in -> square-off -> fight -> finish/regroup -> Flip's line) to mp4."""
import asyncio, os, sys, time, subprocess, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import h, t13_clash as T
FR = Path('/workspace/nailsalley/rec/flipfight2'); OUTV = '/workspace/nailsalley/shots/flipfight_cine_v2.mp4'
REC = {'on': False, 'n': 0, 't': []}
async def grab(g):
    while True:
        if REC['on']:
            t0 = time.time()
            try:
                await g.pg.screenshot(path=str(FR / ('f%04d.jpg' % REC['n'])), type='jpeg', quality=85)
                REC['t'].append(time.time()); REC['n'] += 1
            except Exception:
                pass
            await asyncio.sleep(max(0, 0.08 - (time.time() - t0)))
        else:
            await asyncio.sleep(0.05)
async def main():
    shutil.rmtree(FR, ignore_errors=True); FR.mkdir(parents=True)
    orig_walkin, orig_inputs = T.walkin, T.inputs_ok
    async def walkin(g):
        REC['on'] = True; return await orig_walkin(g)
    async def inputs_ok(g, tag):
        REC['on'] = False
    T.walkin, T.inputs_ok = walkin, inputs_ok
    async with h.Game(out='/workspace/nailsalley/rec') as g:
        await g.boot()
        task = asyncio.create_task(grab(g))
        await T.t_main(g)
        task.cancel()
    ts = REC['t']; lines = []
    for i in range(len(ts)):
        d = (ts[i + 1] - ts[i]) if i + 1 < len(ts) else 0.5
        lines.append("file '%s'\nduration %.3f" % (FR / ('f%04d.jpg' % i), d))
    lines.append("file '%s'" % (FR / ('f%04d.jpg' % (len(ts) - 1))))
    (FR / 'list.txt').write_text('\n'.join(lines))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(FR / 'list.txt'), '-vf', 'fps=30,scale=390:844,format=yuv420p', '-c:v', 'libx264', '-crf', '22', OUTV], check=True)
    print('frames', len(ts), 'secs', round(ts[-1] - ts[0], 1), OUTV)
asyncio.run(main())
