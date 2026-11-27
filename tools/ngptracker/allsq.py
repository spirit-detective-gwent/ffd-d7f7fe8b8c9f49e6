#!/workspace/pwenv/bin/python3
"""Every Ch1 side quest (kenta/aya/riku/yuto) + a Ch1 main-quest complete, in one mode. PASS/FAIL lines.
usage: allsq.py INDEX MODE [shotprefix]
 MODE first   : first playthrough
      ngpsame : the cleared run completed all four side quests + the main quest in THIS page session, then NG+ (Erik's case)
      ngp2    : like ngpsame, then NG+ started a second time in the same session (the same quests again)
      ngpcold : NG+ from a cleared save after a page load"""
import asyncio, sys, json; sys.path.insert(0, '/workspace/ngptracker/tools'); import h, repro_lib as R
INDEX, MODE = sys.argv[1], sys.argv[2]; PFX = sys.argv[3] if len(sys.argv) > 3 else ''
RES = []
def ok(n, c, x=''):
    RES.append(bool(c)); print(('PASS ' if c else 'FAIL ') + MODE + ' ' + n + ('' if c else ' :: ' + str(x)[:400]), flush=True)
KILL = r"""(function(dg,i){ var st={ctx:{dg:dg,dgk:'t_'+dg+'_'+i,dgks:['t_'+dg+'_'+i],dgm:'x'},endHp:40,endSpirit:0,win:true,switches:0,foes:['bully1'],drop:0};
  try{ back(true, st) }catch(e){ return 'err '+e.message } return 1 })('%s',%d)"""
PRE = """(function(){ SQ_IDS.forEach(function(id){ qBanner('QUEST COMPLETE', SQDEF[id].n, '') }); var d=qDef('q_mb_lib'); if(d) qBanner('QUEST COMPLETE', d.n, ''); return 1 })()"""
async def banner(g, want, ms=6000):
    for _ in range(ms // 100):
        t = await g.ev("(function(){var o=document.getElementById('wquest'); return o&&o.classList.contains('go')&&o.style.visibility!=='hidden'? o.textContent:''})()")
        if want in (t or ''): return t
        c = await g.pg.evaluate("()=>{var b=[...document.querySelectorAll('#wlvc.on button, #wlvc.on .wnext')].filter(e=>e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}")
        if c: await g.pg.touchscreen.tap(*c)   # a Bond level-up card holds the banner queue until dismissed (first run: low level)
        await g.wait(100)
    return ''
async def main():
    async with h.Game(INDEX) as g:
        await g.boot()
        if MODE in ('ngpsame', 'ngp2'):
            await g.ev(R.CLEARED); await g.ev(PRE); await g.wait(500)
            for _ in range(300):   # let the old run's banners finish (they happened long before NG+ in real play)
                if await g.ev("!(root.FFF_POPQ&&(FFF_POPQ.on()||FFF_POPQ.list().length))"): break
                await g.wait(100)
            await g.wait(500)
            for k in range(2 if MODE == 'ngp2' else 1):
                if k: await g.ev(R.CLEARED); await g.ev("SAVE.ngp=0; save(); 1")   # back on the cleared slot, start NG+ again
                await g.ev("v640NgStart(v640NgBase()); 1"); await g.wait(2500); await g.skipall(); await g.hush()
            await g.ev("root.FFF_NO_TUT=1"); await g.hush()
            print('setup', await g.ev(R.SETUP), flush=True)
        else:
            await R.setup(g, MODE)
        await g.ev("window.__snd.length=0; window.__evs.length=0; 1")
        for n, id in enumerate(['sq_kenta', 'sq_aya', 'sq_riku', 'sq_yuto']):
            D = await g.ev("({dg:SQDEF.%s.dg, need:SQDEF.%s.need, n:SQDEF.%s.n})" % (id, id, id))
            await g.ev("window.__snd.length=0; window.__evs.length=0; sqStart('%s'); 1" % id); await g.wait(700); await g.hush()
            seen = []
            for i in range(D['need']):
                await g.ev(KILL % (D['dg'], i)); await g.hush(); got = ''
                for _ in range(15):
                    await g.wait(100); got = await g.ev("(document.getElementById('n9slam')||{}).textContent||''")
                    if got: break
                seen.append(got)
                if PFX and n == 0 and i in (0, D['need'] - 1): await g.shot(f'{PFX}_{id}_slam_{i+1}of{D["need"]}')
                await g.wait(1000); await g.hush()
            ok(f'{id} tracker counts up {seen}', seen == [f'{i+1}/{D["need"]}' for i in range(D['need'])], seen)
            await g.ev("sqGiveItem('%s')" % id); await g.wait(500)
            rd = await g.ev("(document.querySelector('.float.qready')||{}).textContent||''")
            ok(f'{id} READY TO TURN IN pops', 'READY TO TURN IN' in rd, rd)
            await g.wait(2600); await g.hush()
            r0 = await g.ev("[SAVE.ess|0, STORY.bond(SAVE).px|0]")
            await g.ev("sqTurnIn('%s'); 1" % id); await g.wait(300); await g.adv(10)
            t = await banner(g, 'QUEST COMPLETE')
            if PFX and n == 0: await g.shot(f'{PFX}_{id}_' + ('complete' if t else 'turnin_no_banner'))
            ok(f'{id} QUEST COMPLETE banner shows', 'QUEST COMPLETE' in t and D['n'] in t, t)
            await g.wait(400)
            snd = await g.ev("window.__snd.join(',')")
            ok(f'{id} slam sfx + quest-complete sound (roundwin) fire', all(s in snd for s in ['qslam_whoosh', 'roundwin']), snd)
            r1 = await g.ev("[SAVE.ess|0, STORY.bond(SAVE).px|0]")
            await g.ev("sqTurnIn('%s'); sqOnKill('%s', 3); 1" % (id, D['dg'])); await g.wait(300); await g.adv(4)
            r2 = await g.ev("[SAVE.ess|0, STORY.bond(SAVE).px|0, sqState('%s').st]" % id)
            ok(f'{id} reward once (+5 ess), no double grant on a 2nd turn-in / extra kills', r1[0] - r0[0] == 5 and r2[0] == r1[0] and r2[1] == r1[1] and r2[2] == 9, (r0, r1, r2))
            print('  sounds', snd[:300], flush=True)
            await g.wait(3600); await g.hush()
        # Ch1 main quest complete (Library relay) through the same banner
        await g.ev("window.__snd.length=0; SAVE.qs=SAVE.qs||{}; SAVE.qs['q_mb_lib']=1; SAVE.qa='q_mb_lib'; save(); 1")
        m0 = await g.ev("[SAVE.heal.length, SAVE.items|0]")
        await g.ev("qDoneNow(); 1"); t = await banner(g, 'QUEST COMPLETE')
        ok('main quest (q_mb_lib) QUEST COMPLETE banner shows', 'QUEST COMPLETE' in t, t)
        await g.wait(300); await g.ev("qDoneNow(); 1"); await g.wait(300)
        m1 = await g.ev("[SAVE.heal.length, SAVE.items|0, SAVE.qs['q_mb_lib']]")
        ok('main quest reward once (qDoneNow again is a no-op)', m1[2] == 9, (m0, m1))
        skips = await g.ev("window.__evs.filter(function(e){return /qdone:skip/.test(e)})")
        ok('no qdone:skip in this run', not skips, skips)
        ok('no page errors', not g.errs, g.errs[:3])
    print(f'{MODE}: {sum(RES)}/{len(RES)} passed', flush=True); sys.exit(0 if all(RES) else 1)
asyncio.run(main())
