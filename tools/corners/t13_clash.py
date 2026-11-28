#!/workspace/pwenv/bin/python3
"""t13: Flip's south-end clash — walk-in stays as-is; in battle two allies
each take a Hustler and Ryo fights one. No stuck states on reload, retreat, or defeat."""
import asyncio, json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import h

OUT = Path(os.environ.get('SHOT_OUT', '/workspace/nailsalley/shots'))
RES = []

def ok(name, cond, detail=None):
    RES.append((bool(cond), name, detail))
    print(('PASS' if cond else 'FAIL'), name, '' if detail is None else json.dumps(detail, default=str)[:420], flush=True)
    if not cond:
        raise AssertionError(name)

WEST_SEED = r"""
(function(){
  var S=c2S(); S.e=S.e||{}; S.q=S.q||{}; S.f=S.f||{};
  ['arrive','gymIn','genji','c2sRep','roam','called','c2lMap'].forEach(function(k){ S.e[k]=1; });
  S.e.run_fac='arc'; S.e.n13='done'; S.e.nq=S.e.nq||{}; S.e.nq.udon=1; S.e.nq.west='clash';
  delete S.f.nq_x_0; delete S.f.nq_x_1; delete S.f.nq_x_2;
  S.q.cq2_nq_west=0; S.qa='cq2_nq_west';
  SAVE.chapter=2; SAVE.qa='cq2_nq_west'; SAVE.qs=SAVE.qs||{}; SAVE.qs.cq2_nq_west=0;
  SAVE.bond=SAVE.bond||{}; SAVE.bond.path=SAVE.bond.path||'balanced'; SAVE.bond.lock=1;
  try{ if(root.FFF_NQ&&FFF_NQ.setStg) FFF_NQ.setStg('west','clash'); }catch(e){}
  try{ if(root.FFF_NQ&&FFF_NQ.qOpen) FFF_NQ.qOpen('west'); }catch(e2){}
  try{ if(typeof c2QSync==='function') c2QSync(); }catch(e3){}
  try{ save(); }catch(e4){}
  return {run:S.e.run_fac, n13:S.e.n13, west:S.e.nq.west, qa:S.qa, q:S.q.cq2_nq_west};
})()
"""

SNAP = r"""
(function(){
  var r=W.ryo, st=root.FFF_UI&&FFF_UI.ST, b=st&&st.b;
  var nq=[].slice.call(document.querySelectorAll('.nq')).map(function(e){ return e.dataset.npc||e.dataset.who||e.className; });
  function n(id){ return document.querySelectorAll('.nq[data-npc="'+id+'"]').length; }
  var last=(window.__ctxs||[])[(window.__ctxs||[]).length-1]||null;
  return {
    room: typeof c2Room==='function'&&c2Room(),
    xy: r&&[Math.round(r.x),Math.round(r.y)],
    cut:!!W.cut, dlg:!!W.dlg, busy:!!W.busy, ig:!!(st&&st.inGame),
    foes: b&&b.grp ? b.grp.length : 0,
    foeIds: b&&b.grp ? b.grp.map(function(s){return s.ch;}) : [],
    side: !!document.getElementById('nqxside'),
    flip: n('n13flip'), punks: n('c2_punk'), hus: n('c2_hustler'),
    nq: nq.slice(0,12),
    west: (function(){ try{ return FFF_NQ.stg('west'); }catch(e){ return c2S().e.nq&&c2S().e.nq.west; } })(),
    q: c2S().q&&c2S().q.cq2_nq_west,
    flags: {x0:!!c2S().f.nq_x_0, x1:!!c2S().f.nq_x_1, x2:!!c2S().f.nq_x_2},
    ctx: last&&{ n: (last.grp||[]).length, grp: last.grp, nqAlly:!!(last.ctx&&last.ctx.nqAlly), nqk: last.ctx&&last.ctx.nqk, dgks: last.ctx&&last.ctx.dgks },
    evs: (window.__evs||[]).filter(function(s){ return /nq:clash|allybrawl|nq:fight|nq:won/.test(s); }).slice(-16)
  };
})()
"""

async def advance_dlg(g, n=14):
    for _ in range(n):
        st = await g.ev(SNAP)
        if st and st.get('ig'):
            return st
        # click Next / OK / the dialog itself
        clicked = await g.pg.evaluate("""()=>{
          var btns=[...document.querySelectorAll('#wdlg button, #wcomment button, button')].filter(e=>e.offsetParent&&/^(OK|Next|Skip|Continue)$/i.test((e.textContent||'').trim()));
          if(btns[0]){ var r=btns[0].getBoundingClientRect(); return [r.x+r.width/2,r.y+r.height/2]; }
          var d=document.getElementById('wdlg');
          if(d&&d.offsetParent&&(d.innerText||'').trim()){ var r=d.getBoundingClientRect(); return [r.x+r.width/2, Math.min(r.bottom-20, r.y+r.height*0.8)]; }
          return null;
        }""")
        if clicked:
            await g.pg.touchscreen.tap(*clicked)
        else:
            await g.pg.touchscreen.tap(195, 700)
        await g.wait(450)
    return await g.ev(SNAP)

async def seed_at_clash(g):
    await g.ev("root.FFF_NO_TUT=1; window.FFF_SKIP_C2_CINE=1; 1")
    seed = await g.ev(WEST_SEED)
    await g.ev("try{ if(typeof c2Go==='function') c2Go('town'); }catch(e){} 1")
    await g.wait(800)
    await g.skipall(4)
    # go_xy hush/cut-clear, then crewSync via c2Pop
    await g.go_xy(1790, 2550)
    await g.ev("try{ if(root.FFF_NQ&&FFF_NQ.crewSync) FFF_NQ.crewSync(); }catch(e){} 1")
    await g.wait(300)
    return seed

async def start_walkin(g):
    evs_before = await g.ev("(window.__evs||[]).slice()")
    # if already in range, flowTick may have fired; otherwise call clashBeat
    st = await g.ev(SNAP)
    if st and st.get('flip', 0) < 1:
        await g.ev("try{ if(root.FFF_NQ&&FFF_NQ.clashBeat) FFF_NQ.clashBeat(); }catch(e){ } 1")
    # wait for Flip + two punks to exist (walk-in)
    got = None
    for _ in range(20):
        got = await g.ev(SNAP)
        if got and got.get('flip') >= 1 and got.get('punks') >= 2:
            break
        await g.wait(200)
    return got

async def to_fight(g):
    # wait out the walk (speed 210, ~240px + settle)
    for _ in range(25):
        st = await g.ev(SNAP)
        if st and (st.get('dlg') or st.get('ig')):
            break
        await g.wait(200)
    st = await advance_dlg(g, 16)
    if not (st and st.get('ig')):
        # swirl may still be running
        for _ in range(16):
            await g.wait(250)
            st = await g.ev(SNAP)
            if st and st.get('ig'):
                break
    return st

async def run_main(g):
    seed = await seed_at_clash(g)
    ok('west clash seeded', seed and seed.get('run')=='arc' and seed.get('west')=='clash', seed)
    walk = await start_walkin(g)
    ok('walk-in: Flip and two Punks are on the street', walk and walk.get('flip')>=1 and walk.get('punks')>=2, walk)
    ok('walk-in: three Hustlers still waiting', walk and walk.get('hus')>=3, walk)
    st = await to_fight(g)
    ok('battle opened', st and st.get('ig'), st)
    ok('player fights one foe', st and st.get('foes')==1, st)
    ctx = st and st.get('ctx') or {}
    ok('fight() was called with one Hustler', ctx.get('n')==1 and ctx.get('grp')==['c2_hustler'], ctx)
    ok('nqAlly flag on the fight ctx', ctx.get('nqAlly') is True, ctx)
    ok('ally side-brawl canvas is up', st and st.get('side'), st)
    await g.shot('t13_battle_after', hush=False)
    wr = await g.ev("""(function(){
      var L=(window.__ctxs||[])[(window.__ctxs||[]).length-1]||{};
      var st={ctx:L.ctx||{nqk:'nq_x',nqAlly:1,dgks:['nq_x_0','nq_x_1','nq_x_2']}, escaped:false, endHp:40};
      try{ var g=document.getElementById('game'); if(g) g.classList.remove('on','screen'); }
      catch(e0){}
      try{ var r=document.getElementById('result'); if(r) r.classList.remove('on'); }catch(e1){}
      try{ if(root.FFF_UI&&FFF_UI.ST){ FFF_UI.ST.inGame=false; FFF_UI.ST.inWorld=true; } }catch(e2){}
      try{ back(true, st); }catch(e){ return 'err '+e.message; }
      W.dgFight=null; W.busy=false; W.cut=false;
      return 'ok';
    })()""")
    ok('win back() accepted', wr=='ok', wr)
    after=None
    for _ in range(20):
        after = await g.ev(SNAP)
        if after and after.get('flags',{}).get('x0') and after.get('flags',{}).get('x1') and after.get('flags',{}).get('x2'):
            break
        await g.wait(250)
    ok('win marks all three Hustlers down (allies took two)', after and after.get('flags',{}).get('x0') and after.get('flags',{}).get('x1') and after.get('flags',{}).get('x2'), after)
    ok('side brawl cleared after the fight', not await g.ev("!!document.getElementById('nqxside')"), after)
    # only advance a real dialog button — a bare tap walks Ryo and can drop the won scene
    for _ in range(12):
        after = await g.ev(SNAP)
        if after and (after.get('q')==9 or after.get('west')=='done'):
            break
        clicked = await g.pg.evaluate("""()=>{
          var b=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&/^(OK|Next|Skip|Continue)$/i.test((e.textContent||'').trim()));
          if(b[0]){ var r=b[0].getBoundingClientRect(); return [r.x+r.width/2,r.y+r.height/2]; }
          return null;
        }""")
        if not clicked:
            break
        await g.pg.touchscreen.tap(*clicked)
        await g.wait(450)
    after = await g.ev(SNAP)
    ok('win leaves the battle and does not stick a cut', after and not after.get('ig') and not after.get('cut'), after)
    return after

async def run_retreat(g):
    await seed_at_clash(g)
    await start_walkin(g)
    st = await to_fight(g)
    ok('retreat setup: in battle', st and st.get('ig') and st.get('foes')==1, st)
    await g.ev("""(function(){
      var L=(window.__ctxs||[])[(window.__ctxs||[]).length-1]||{};
      var st={ctx:L.ctx||{nqk:'nq_x',nqAlly:1}, escaped:true};
      try{ var g=document.getElementById('game'); if(g) g.classList.remove('on'); }catch(e0){}
      try{ var r=document.getElementById('result'); if(r) r.classList.remove('on'); }catch(e1){}
      try{ if(root.FFF_UI&&FFF_UI.ST){ FFF_UI.ST.inGame=false; FFF_UI.ST.inWorld=true; } }catch(e2){}
      try{ back(false, st); }catch(e){ return 'err '+e.message; }
      W.dgFight=null; W.busy=false;
      return 1;
    })()""")
    await g.wait(800)
    after = await g.ev(SNAP)
    ok('retreat: left the battle (quest still open, foes not marked down)', after and not after.get('ig') and after.get('q')!=9 and not after.get('flags',{}).get('x0'), after)
    ok('retreat: side brawl cleared', not await g.ev("!!document.getElementById('nqxside')"), after)
    # retrigger
    await g.go_xy(1790, 2550)
    await g.ev("try{ if(root.FFF_NQ&&FFF_NQ.clashBeat) FFF_NQ.clashBeat(); }catch(e){} 1")
    got = None
    for _ in range(16):
        got = await g.ev(SNAP)
        if got and got.get('flip')>=1:
            break
        await g.wait(200)
    ok('retreat: walk-in can fire again', got and got.get('flip')>=1 and got.get('punks')>=2, got)

async def run_defeat(g):
    await seed_at_clash(g)
    await start_walkin(g)
    st = await to_fight(g)
    ok('defeat setup: in battle', st and st.get('ig'), st)
    await g.ev("""(function(){
      var L=(window.__ctxs||[])[(window.__ctxs||[]).length-1]||{};
      var st={ctx:L.ctx||{nqk:'nq_x',nqAlly:1}, escaped:false};
      try{ var g=document.getElementById('game'); if(g) g.classList.remove('on'); }catch(e0){}
      try{ var r=document.getElementById('result'); if(r) r.classList.remove('on'); }catch(e1){}
      try{ if(root.FFF_UI&&FFF_UI.ST){ FFF_UI.ST.inGame=false; FFF_UI.ST.inWorld=true; } }catch(e2){}
      try{ back(false, st); }catch(e){ return 'err '+e.message; }
      W.dgFight=null; W.busy=false;
      return 1;
    })()""")
    await g.wait(800)
    after = await g.ev(SNAP)
    ok('defeat: left the battle (quest still open, foes not marked down)', after and not after.get('ig') and after.get('q')!=9 and not after.get('flags',{}).get('x0'), after)
    ok('defeat: side brawl cleared', not await g.ev("!!document.getElementById('nqxside')"), after)
    # mid-scene "reload": c2Pop while a walk-in is live (before fight)
    await g.go_xy(1790, 2550)
    await g.ev("try{ FFF_NQ.clashBeat(); }catch(e){} 1")
    await g.wait(300)
    mid = await g.ev(SNAP)
    await g.ev("try{ c2Pop(); }catch(e){} 1")
    await g.wait(400)
    popped = await g.ev(SNAP)
    ok('reload mid-walk: street is not stuck in a cut', popped and not popped.get('cut') or popped.get('ig')==False, popped)
    await g.ev("try{ FFF_NQ.clashBeat(); }catch(e){} 1")
    got=None
    for _ in range(16):
        got=await g.ev(SNAP)
        if got and got.get('flip')>=1:
            break
        await g.wait(200)
    ok('reload mid-walk: clash walk-in can fire again', got and got.get('flip')>=1, got)

async def main():
    async with h.Game(out=str(OUT)) as g:
        await g.boot()
        await run_main(g)
    async with h.Game(out=str(OUT)) as g:
        await g.boot()
        await run_retreat(g)
    async with h.Game(out=str(OUT)) as g:
        await g.boot()
        await run_defeat(g)
    fails = [n for ok_, n, _ in RES if not ok_]
    print('RESULT', '%s/%s' % (sum(1 for ok_,_,__ in RES if ok_), len(RES)), 'FAIL' if fails else 'ALL PASS', flush=True)
    if fails:
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
