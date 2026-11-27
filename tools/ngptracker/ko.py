#!/workspace/pwenv/bin/python3
"""NG+ ambush-KO path (high-level Ryo knocks Ch1 bullies out from behind, no fight): real ambStrike on an unaware lib foe."""
import asyncio, sys, json; sys.path.insert(0, '/workspace/ngptracker/tools'); import h, repro_lib as R
INDEX, MODE = sys.argv[1], sys.argv[2]; PFX = sys.argv[3] if len(sys.argv) > 3 else ''
async def main():
    async with h.Game(INDEX) as g:
        await R.setup(g, MODE)
        print('bondLv', await g.ev("playerLv()"), flush=True)
        await g.ev("window.__snd.length=0; window.__evs.length=0; 1")
        await g.ev("sqStart('sq_kenta'); 1"); await g.wait(600); await g.hush()
        await g.ev("libGo('hall'); 1"); await g.wait(1800); await g.hush()
        res = []
        for i in range(3):
            fs = await g.ev("(W.dgF||[]).filter(function(f){return f.s&&f.s.el&&f.s.el.parentNode&&!f.stun}).map(function(f){return f.key})")
            if not fs: break
            key = fs[0]
            r = await g.ev("(function(){var q=(W.dgF||[]).filter(function(o){return o.key==='%s'})[0]; q.lv=1; q.st='patrol'; q.sus=0; q.qm=0; var fa=q.fa||0; W.ryo.x=q.s.x-Math.cos(fa)*40; W.ryo.y=q.s.y-Math.sin(fa)*40; place(W.ryo,0); try{ ambStrike(q,'test','back'); return 'strike' }catch(e){return 'err '+e.message}})()" % key)
            slam = ''
            for _ in range(40):
                await g.wait(150); slam = await g.ev("(document.getElementById('n9slam')||{}).textContent||''")
                if slam: break
            res.append((key, r, await g.ev("sqState('sq_kenta').kills"), slam))
            print(' ko', res[-1], flush=True)
            if PFX and slam: await g.shot(f'{PFX}_ko_slam_{i+1}')
            await g.wait(2500); await g.hush()
        print('sounds', await g.ev("window.__snd.filter(function(s){return /qslam|roundwin|quest_ready/.test(s)})"), flush=True)
        print('evs', await g.ev("window.__evs.filter(function(s){return /slam|sq:kill|amb2:(ko|fight|now)/.test(s)})"), flush=True)
        print('errs', g.errs[:5], flush=True)
asyncio.run(main())
