#!/workspace/pwenv/bin/python3
"""Repro: Ch1 side quest sq_kenta: start -> 4 lib kills (slam 1/4..4/4) -> item -> ready pop -> turn in (QUEST COMPLETE).
usage: repro.py INDEX MODE [shotprefix]   MODE = first | ngp (cleared run -> NG+ in the same session) | ngpcold (NG+ save loaded fresh)"""
import asyncio, sys, json; sys.path.insert(0, '/workspace/ngptracker/tools'); import h
INDEX, MODE = sys.argv[1], sys.argv[2]; PFX = sys.argv[3] if len(sys.argv) > 3 else ''
CLEARED = r"""(function(){ var S=SAVE; STORY.ensure(S); S.intro=1; S.ch1=1; S.gouki=1; S.mb={mb_lib:1,mb_art:1,mb_cafe:1,mb_field:1,gouki:1}; S.sc=S.sc||{}; S.sc.nurse=1; S.sc.ending=1;
  S.bond=S.bond||{}; S.bond.path='fierce'; S.bond.lock=1; S.c2les={assist:1}; S.gsk={alley:1};
  S.sq={sq_kenta:{st:9,kills:4,item:1,pop:1},sq_aya:{st:9,kills:3,item:1,pop:1},sq_riku:{st:9,kills:3,item:1,pop:1},sq_yuto:{st:9,kills:4,item:1,pop:1}}; save(); return 1})()"""
SETUP = r"""(function(){ var S=SAVE; S.intro=1; S.sc=S.sc||{}; S.sc.nurse=1; S.mb=S.mb||{}; S.mb.mb_lib=1; S.bond=S.bond||{}; if(!S.bond.path){S.bond.path='fierce';S.bond.lock=1;}
  try{ var L=libS(); L.kenta=1; }catch(e){} W.dlg=false; W.paused=false; save(); sqUnlock('sq_kenta'); return {st:sqState('sq_kenta').st, ngp:S.ngp|0, ch:S.chapter|0} })()"""
KILL = r"""(function(i){ var st={ctx:{dg:'lib',dgk:'lib_test_'+i,dgks:['lib_test_'+i],dgm:'lib_stacks'},endHp:40,endSpirit:0,win:true,switches:0,foes:['bully1'],drop:0};
  try{ back(true, st) }catch(e){ return 'err '+e.message } return sqState('sq_kenta').kills })(%d)"""
async def turn_in(g, tag, i):
    pass
async def main():
    async with h.Game(INDEX) as g:
        await g.boot()
        if MODE.startswith('ngp'):
            await g.ev(CLEARED)
            if MODE == 'ngpcold':
                # cleared save on disk, reload the page fresh, then start NG+
                await g.pg.reload(); await g.wait(2500); await g.boot()
            # play some quest completes in this session as a first run would have (mainly matters for same-session NG+)
            if MODE == 'ngp':
                await g.ev("qBanner('QUEST COMPLETE', SQDEF.sq_kenta.n, ''); qBanner('QUEST COMPLETE', SQDEF.sq_aya.n, ''); 1")
                await g.wait(500)
            await g.ev("v640NgStart(v640NgBase()); 1"); await g.wait(2500); await g.skipall(); await g.hush()
            await g.ev("root.FFF_NO_TUT=1"); await g.hush()
        print('setup', await g.ev(SETUP), flush=True)
        await g.ev("window.__snd.length=0; window.__evs.length=0; 1")
        await g.ev("sqStart('sq_kenta'); 1"); await g.wait(600); await g.hush()
        slams = []
        for i in range(4):
            k = await g.ev(KILL % i); await g.hush()
            got = None
            for _ in range(15):
                await g.wait(100)
                got = await g.ev("(document.getElementById('n9slam')||{}).textContent||''")
                if got: break
            slams.append((k, got))
            if PFX and got and i in (0, 3): await g.shot(f'{PFX}_slam_{i+1}')
            await g.wait(1200); await g.hush()
        print('kills/slam', slams, flush=True)
        r = await g.ev("sqGiveItem('sq_kenta')"); await g.wait(400)
        rd = await g.ev("(document.querySelector('.float.qready')||{}).textContent||''")
        print('item', r, 'st', await g.ev("sqState('sq_kenta').st"), 'ready float', rd, flush=True)
        if PFX and rd: await g.shot(f'{PFX}_ready')
        await g.wait(2500); await g.hush()
        before = await g.ev("[SAVE.ess|0, (STORY.bond(SAVE).px|0)]")
        await g.ev("sqTurnIn('sq_kenta'); 1"); await g.wait(300)
        await g.adv(12); await g.wait(200)
        wq = await g.ev("(function(){var o=document.getElementById('wquest'); return o? [o.className, o.textContent, o.style.visibility]:null})()")
        print('banner', wq, flush=True)
        if PFX: await g.shot(f'{PFX}_complete')
        await g.wait(800)
        after = await g.ev("[SAVE.ess|0, (STORY.bond(SAVE).px|0)]")
        print('reward ess/px before', before, 'after', after, flush=True)
        # second turn-in attempt must not grant again
        await g.ev("sqTurnIn('sq_kenta'); 1"); await g.wait(300); await g.adv(6)
        print('reward after 2nd turn-in try', await g.ev("[SAVE.ess|0, (STORY.bond(SAVE).px|0)]"), flush=True)
        snd = await g.ev("window.__snd.filter(function(s){return /qslam|roundwin|quest_ready|katana|select/.test(s)})")
        evs = await g.ev("window.__evs.filter(function(s){return /slam|sq:|banner|v6552|quest:ready/.test(s)})")
        print('sounds', snd, flush=True); print('evs', evs, flush=True); print('errs', g.errs[:5], flush=True)
asyncio.run(main())
