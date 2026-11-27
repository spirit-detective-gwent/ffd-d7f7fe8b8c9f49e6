#!/workspace/pwenv/bin/python3
"""Realistic: accept sq_kenta, walk into the Library rooms, touch real foes (real fight() ctx), win via back(). MODE first|ngpcold"""
import asyncio, sys, json; sys.path.insert(0, '/workspace/ngptracker/tools'); import h, repro_lib as R
INDEX, MODE = sys.argv[1], sys.argv[2]; PFX = sys.argv[3] if len(sys.argv) > 3 else ''
async def main():
    async with h.Game(INDEX) as g:
        await R.setup(g, MODE)
        await g.ev("window.__snd.length=0; window.__evs.length=0; window.__ctxs.length=0; 1")
        await g.ev("sqStart('sq_kenta'); 1"); await g.wait(600); await g.hush()
        keys = await g.ev("Object.keys(LIBG)"); print('libg', keys, flush=True)
        slams = []
        for k in keys:
            if await g.ev("sqState('sq_kenta').kills") >= 4: break
            await g.ev("libGo('%s'); 1" % k); await g.wait(1500); await g.hush()
            for t in range(6):
                fs = await g.ev("(W.dgF||[]).filter(function(f){return f.s&&f.s.el&&f.s.el.parentNode&&!f.stun}).map(function(f){return [f.key,Math.round(f.s.x),Math.round(f.s.y),f.id]})")
                if not fs or await g.ev("sqState('sq_kenta').kills") >= 4: break
                key, fx, fy, fid = fs[0]
                n0 = await g.ev("window.__ctxs.length")
                for _ in range(20):
                    await g.ev("var f=(W.dgF||[]).filter(function(o){return o.key==='%s'})[0]; if(f){W.ryo.x=f.s.x+20;W.ryo.y=f.s.y;place(W.ryo,0)} 1" % key); await g.wait(150)
                    if await g.ev("window.__ctxs.length") > n0: break
                if await g.ev("window.__ctxs.length") == n0: print(' no fight from', key, flush=True); break
                await g.wait(1200)
                c = await g.ev("JSON.stringify(window.__ctxs[window.__ctxs.length-1].ctx)")
                r = await g.ev(R.WIN)
                got = ''
                for _ in range(20):
                    await g.wait(100); got = await g.ev("(document.getElementById('n9slam')||{}).textContent||''")
                    if got: break
                slams.append((k, key, c[:120], await g.ev("sqState('sq_kenta').kills"), got))
                print(' fight', slams[-1], flush=True)
                if PFX and got: await g.shot(f'{PFX}_realslam_{len(slams)}')
                await g.wait(1500); await g.hush()
        print('sounds', await g.ev("window.__snd.filter(function(s){return /qslam|roundwin|quest_ready/.test(s)})"), flush=True)
        print('evs', await g.ev("window.__evs.filter(function(s){return /slam|sq:kill|v6552/.test(s)})"), flush=True)
        print('errs', g.errs[:5], flush=True)
asyncio.run(main())
