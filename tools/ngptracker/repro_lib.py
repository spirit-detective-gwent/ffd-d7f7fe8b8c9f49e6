import sys; sys.path.insert(0, '/workspace/ngptracker/tools'); import h
CLEARED = r"""(function(){ var S=SAVE; STORY.ensure(S); S.intro=1; S.ch1=1; S.gouki=1; S.mb={mb_lib:1,mb_art:1,mb_cafe:1,mb_field:1,gouki:1}; S.sc=S.sc||{}; S.sc.nurse=1; S.sc.ending=1;
  S.bond=S.bond||{}; S.bond.path='fierce'; S.bond.lock=1; S.bond.px=(window.__PX!=null?window.__PX:99999); S.c2les={assist:1}; S.gsk={alley:1};
  S.sq={sq_kenta:{st:9,kills:4,item:1,pop:1},sq_aya:{st:9,kills:3,item:1,pop:1},sq_riku:{st:9,kills:3,item:1,pop:1},sq_yuto:{st:9,kills:4,item:1,pop:1}}; save(); return 1})()"""
SETUP = r"""(function(){ var S=SAVE; S.intro=1; S.sc=S.sc||{}; S.sc.nurse=1; S.mb=S.mb||{}; S.mb.mb_lib=1; S.mb.mb_art=1; S.mb.mb_cafe=1; S.mb.mb_field=1; S.bond=S.bond||{}; if(!S.bond.path){S.bond.path='fierce';S.bond.lock=1;}
  try{ var L=libS(); L.kenta=1; }catch(e){} W.dlg=false; W.paused=false; save(); SQ_IDS.forEach(sqUnlock); return {st:SQ_IDS.map(function(i){return sqState(i).st}), ngp:S.ngp|0, ch:S.chapter|0} })()"""
WIN = """(function(){ var L=window.__ctxs[window.__ctxs.length-1]; if(!L) return 'nofight'; var st={ctx:L.ctx,endHp:40,endSpirit:0,win:true,switches:0,foes:L.grp,drop:0};
  try{ document.getElementById('game').classList.remove('on'); document.getElementById('result').classList.remove('on'); }catch(e){} try{ back(true, st); }catch(e){ return 'err '+e.message } return 'back '+JSON.stringify(L.ctx.dgks)})()"""
async def setup(g, mode, same_session_done=False):
    await g.boot()
    if mode == 'ngpc2':
        # Erik's flow: playing Chapter Two in this session, then New Game Plus without reloading
        await g.ev(CLEARED)
        await g.pg.evaluate("WORLD_API.c2Begin(true)"); await g.wait(2500); await g.skipall(); await g.hush()
        await g.ev("SAVE.ch1=1; SAVE.gouki=1; SAVE.chapter=2; save(); 1")
        await g.wait(1500); await g.hush()
        print('c2 on before NG+', await g.ev("c2On()"), flush=True)
    elif mode == 'ngptitle':
        # NG+ from the title screen right after a page load (cold path in v640NgStart: the world was never entered)
        await g.ev(CLEARED)
        await g.pg.reload(); await g.wait(2500)
        await g.pg.touchscreen.tap(195, 420); await g.wait(800)
        await g.ev("1")
    elif mode.startswith('ngp'):
        await g.ev(CLEARED)
        await g.pg.reload(); await g.wait(2500); await g.boot()
    if mode.startswith('ngp'):
        if same_session_done:
            await g.ev("qBanner('QUEST COMPLETE', SQDEF.sq_kenta.n, ''); 1"); await g.wait(400)
        await g.ev("v640NgStart(v640NgBase()); 1"); await g.wait(2500); await g.skipall(); await g.hush()
        await g.ev("root.FFF_NO_TUT=1"); await g.hush(); await g.ev(h.HOOK)
    print('setup', await g.ev(SETUP), flush=True)
