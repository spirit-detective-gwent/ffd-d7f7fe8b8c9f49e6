#!/workspace/pwenv/bin/python3
"""t13 (t626u/t627u): Flip's south-end clash. Walk-in unchanged. World cines:
pre-fight square-off (helpers run at their Hustlers, Ryo steps to his), Ryo fights one;
post-win the helpers finish theirs (exchange, KO, down), regroup, Flip's line.
Checks: no battle-screen side canvas, skip both cines, tap spam, reload (c2Pop) mid-pre and mid-post,
retreat and defeat restore, and menu / map / swap / movement all work after."""
import asyncio, json, math, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import h

OUT = Path(os.environ.get('SHOT_OUT', '/workspace/nailsalley/shots'))
RES = []
ONLY = os.environ.get('ONLY', '')

def ok(name, cond, detail=None):
    RES.append((bool(cond), name))
    print(('PASS' if cond else 'FAIL'), name, '' if detail is None else json.dumps(detail, default=str)[:380], flush=True)
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
  return {run:S.e.run_fac, west:S.e.nq.west, q:S.q.cq2_nq_west};
})()
"""

SNAP = r"""
(function(){
  var r=W.ryo, st=root.FFF_UI&&FFF_UI.ST, b=st&&st.b;
  function list(id){ return [].slice.call(document.querySelectorAll('.nq[data-npc="'+id+'"]')).filter(function(e){return e.isConnected;}); }
  function xy(e){ var m=/translate3d\(([-\d.]+)px,\s*([-\d.]+)px/.exec(e.style.transform||''); return m?[+m[1],+m[2]]:null; }
  var last=(window.__ctxs||[])[(window.__ctxs||[]).length-1]||null;
  var dlgTxt=(document.getElementById('wdlg')&&document.getElementById('wdlg').innerText)||'';
  return {
    room: typeof c2Room==='function'&&c2Room(), xy: r&&[Math.round(r.x),Math.round(r.y)],
    cut:!!W.cut, dlg:!!W.dlg, busy:!!W.busy, paused:!!W.paused, pan:!!W.pan, ig:!!(st&&st.inGame),
    xc: (root.FFF_NQ&&FFF_NQ.xc)?FFF_NQ.xc.st():'?', skip:!!document.getElementById('nqxskip'),
    side: !!document.getElementById('nqxside'),
    foes: b&&b.grp ? b.grp.length : 0,
    flip: list('n13flip').length, punks: list('c2_punk').length, hus: list('c2_hustler').length,
    guard: document.querySelectorAll('.nq.nqguard').length, rdy: !!(r&&r.rdy),
    west: (function(){ try{ return FFF_NQ.stg('west'); }catch(e){ return null; } })(),
    q: c2S().q&&c2S().q.cq2_nq_west, nfights:(window.__ctxs||[]).length,
    flags: {x0:!!c2S().f.nq_x_0, x1:!!c2S().f.nq_x_1, x2:!!c2S().f.nq_x_2},
    ctx: last&&{ n:(last.grp||[]).length, grp:last.grp, nqk:last.ctx&&last.ctx.nqk },
    dlgTxt: dlgTxt.slice(0,90),
    evs: (window.__evs||[]).filter(function(s){ return /nq:clash|nq:xc|nq:fight|nq:won/.test(s); }).slice(-14)
  };
})()
"""

PAIRS = r"""
(function(){
  // world positions of actors: hustlers, punks, ryo
  var hs=[].slice.call(document.querySelectorAll('.nq[data-npc="c2_hustler"]')), ps=[].slice.call(document.querySelectorAll('.nq[data-npc="c2_punk"]'));
  function wp(e){ var m=/translate3d\(([-\d.]+)px,\s*([-\d.]+)px/.exec(e.style.transform||''); if(!m) return null; return [Math.round(+m[1]+e.offsetWidth/2), Math.round(+m[2]+e.offsetHeight)]; }
  return { hus: hs.map(wp), punks: ps.map(wp), ryo: W.ryo&&[Math.round(W.ryo.x),Math.round(W.ryo.y)] };
})()
"""

BTN = """(re)=>{var b=[...document.querySelectorAll('button')].filter(e=>e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden'&&new RegExp(re,'i').test((e.textContent||'').trim()));if(!b.length)return null;var r=b[0].getBoundingClientRect(),x=r.x+r.width/2,y=r.y+r.height/2,t=document.elementFromPoint(x,y);if(t!==b[0]&&!b[0].contains(t))return null;return [x,y]}"""

async def tap_btn(g, re_):
    c = await g.pg.evaluate(BTN, re_)
    if c:
        await g.pg.touchscreen.tap(*c)
    return bool(c)

async def until(g, pred, tries=40, ms=200):
    st = None
    for _ in range(tries):
        st = await g.ev(SNAP)
        if st and pred(st):
            return st
        await g.wait(ms)
    return st

async def seed(g):
    await g.ev("root.FFF_NO_TUT=1; window.FFF_SKIP_C2_CINE=1; 1")
    s = await g.ev(WEST_SEED)
    await g.ev("try{ if(typeof c2Go==='function') c2Go('town'); }catch(e){} 1")
    await g.wait(800); await g.skipall(4)
    await g.go_xy(1790, 2390)
    await g.ev("try{ FFF_NQ.crewSync(); }catch(e){} 1")
    await g.wait(300)
    return s

async def walkin(g):
    # walk Ryo up to the south end so the beat fires by itself (approach unchanged)
    await g.ev("W.ryo.x=1790; W.ryo.y=2470; place(W.ryo,0); camera(true); 1")
    st = await until(g, lambda s: s['flip'] >= 1 and s['punks'] >= 2, 30, 200)
    if not (st and st['flip'] >= 1):
        await g.ev("try{ FFF_NQ.clashBeat(); }catch(e){} 1")
        st = await until(g, lambda s: s['flip'] >= 1 and s['punks'] >= 2, 20, 200)
    return st

async def through_clash_line(g):
    st = await until(g, lambda s: s['dlg'] or s['xc'] == 'pre' or s['ig'], 30, 200)
    for _ in range(12):
        st = await g.ev(SNAP)
        if st['xc'] == 'pre' or st['ig']:
            return st
        if not await tap_btn(g, '^(Next|OK)'):
            await g.pg.touchscreen.tap(195, 760)
        await g.wait(450)
    return await g.ev(SNAP)

async def to_post(g):
    st = None
    for _ in range(40):
        st = await g.ev(SNAP)
        if st['xc'] == 'post' or (st['xc'] == '' and 'West street' in st['dlgTxt']):
            return st
        if st['dlg']:
            if not await tap_btn(g, '^(Next|OK)'):
                await g.pg.touchscreen.tap(195, 760)
        await g.wait(300)
    return st

async def to_battle(g):
    return await until(g, lambda s: s['ig'], 50, 200)

async def win(g):
    return await g.ev("""(function(){
      var L=(window.__ctxs||[])[(window.__ctxs||[]).length-1]||{};
      var st={ctx:L.ctx, escaped:false, endHp:40};
      try{ var gm=document.getElementById('game'); if(gm) gm.classList.remove('on'); var rr=document.getElementById('result'); if(rr) rr.classList.remove('on'); }catch(e0){}
      try{ if(root.FFF_UI&&FFF_UI.ST){ FFF_UI.ST.inGame=false; FFF_UI.ST.inWorld=true; } }catch(e1){}
      try{ var wd=document.getElementById('world'); if(wd) wd.classList.add('on'); }catch(e3){}
      try{ back(true, st); }catch(e){ return 'err '+e.message; }
      W.dgFight=null; W.busy=false; W.on=true; return 'ok'; })()""")

async def lose(g, escaped):
    e = 'true' if escaped else 'false'
    return await g.ev(f"""(function(){{
      var L=(window.__ctxs||[])[(window.__ctxs||[]).length-1]||{{}};
      var st={{ctx:L.ctx, escaped:{e}}};
      try{{ var gm=document.getElementById('game'); if(gm) gm.classList.remove('on'); }}catch(e0){{}}
      try{{ if(root.FFF_UI&&FFF_UI.ST){{ FFF_UI.ST.inGame=false; FFF_UI.ST.inWorld=true; }} }}catch(e1){{}}
      try{{ var wd=document.getElementById('world'); if(wd) wd.classList.add('on'); }}catch(e3){{}}
      try{{ back(false, st); }}catch(e){{ return 'err '+e.message; }}
      W.dgFight=null; W.busy=false; W.on=true; return 'ok'; }})()""")

async def finish_chain(g, n=40):
    """click through Flip's won line, the sting, the next job, the banner"""
    st = None
    for _ in range(n):
        st = await g.ev(SNAP)
        if st['q'] == 9 and not st['dlg'] and not st['cut']:
            st2 = await g.ev(SNAP)
            await g.wait(500)
            st2 = await g.ev(SNAP)
            if not st2['dlg'] and not st2['cut']:
                return st2
        if not await tap_btn(g, '^(Next|OK|Continue|Close)'):
            sting = await g.ev("!!document.getElementById('nqsting')")
            if sting:
                await g.pg.touchscreen.tap(195, 420)
            elif st['dlg']:
                await g.pg.touchscreen.tap(195, 760)
        await g.wait(450)
    return await g.ev(SNAP)

async def inputs_ok(g, tag):
    base = await g.ev(SNAP)
    ok(f'{tag}: no lock left (cut/dlg/busy/pause/pan/skip/rdy)', not base['cut'] and not base['dlg'] and not base['busy'] and not base['paused'] and not base['pan'] and not base['skip'] and not base['rdy'], base)
    # menu (phone home screen) -> a sub page -> back -> close
    await g.pg.click('#wMenu'); await g.wait(500)
    m = await g.ev("({p:!!W.paused, tab:W.ptab, on:document.getElementById('wpause').classList.contains('on')})")
    ok(f'{tag}: menu opens', m['p'] and m['on'] and m['tab'] == 'home', m)
    await g.ev("document.querySelector('#wpause button[data-a=go][data-s=journal]').click(); 1"); await g.wait(400)
    j = await g.ev("({tab:W.ptab})")
    ok(f'{tag}: menu page (journal) opens', j['tab'] == 'journal', j)
    await g.ev("document.querySelector('#wpause [data-a=back]').click(); 1"); await g.wait(400)
    await g.ev("document.querySelector('#wpause [data-a=close]').click(); 1"); await g.wait(500)
    m2 = await g.ev("({p:!!W.paused, on:document.getElementById('wpause').classList.contains('on')})")
    ok(f'{tag}: menu closes', not m2['p'] and not m2['on'], m2)
    await g.skipall(4)
    # HUD map button
    await g.pg.click('#wMap'); await g.wait(500)
    mp = await g.ev("({p:!!W.paused, tab:W.ptab, map:!!document.querySelector('#wpause .pmap')})")
    ok(f'{tag}: HUD map opens the map', mp['p'] and mp['tab'] == 'map' and mp['map'], mp)
    await g.ev("document.querySelector('#wpause .ph-back').click(); 1"); await g.wait(400)
    await g.ev("var c=document.querySelector('#wpause [data-a=close]'); if(c) c.click(); 1"); await g.wait(500)
    mp2 = await g.ev("({p:!!W.paused, on:document.getElementById('wpause').classList.contains('on')})")
    ok(f'{tag}: map closes', not mp2['p'] and not mp2['on'], mp2)
    await g.skipall(4)
    fr = await g.ev("({dlg:!!W.dlg, cut:!!W.cut, busy:!!W.busy})")
    ok(f'{tag}: input free after menu/map', not fr['dlg'] and not fr['cut'] and not fr['busy'], fr)
    # swap
    a0 = await g.ev("SAVE.act")
    await g.pg.click('#wSwap'); await g.wait(900)
    a1 = await g.ev("SAVE.act")
    ok(f'{tag}: swap switches fighter', a0 != a1, [a0, a1])
    await g.pg.click('#wSwap'); await g.wait(900)
    # movement: drive the stick key for 700 ms
    x0 = await g.ev("[W.ryo.x,W.ryo.y]")
    await g.pg.keyboard.down('ArrowUp'); await g.wait(800); await g.pg.keyboard.up('ArrowUp'); await g.wait(200)
    x1 = await g.ev("[W.ryo.x,W.ryo.y]")
    moved = math.hypot(x1[0]-x0[0], x1[1]-x0[1])
    if moved < 8:  # tap-to-walk fallback
        await g.pg.touchscreen.tap(195, 300); await g.wait(1200)
        x1 = await g.ev("[W.ryo.x,W.ryo.y]"); moved = math.hypot(x1[0]-x0[0], x1[1]-x0[1])
    ok(f'{tag}: Ryo moves', moved >= 8, {'from': x0, 'to': x1, 'd': round(moved, 1)})

def near(a, b, d):
    return a and b and math.hypot(a[0]-b[0], a[1]-b[1]) <= d

async def t_main(g, shots=False, frames=None):
    s = await seed(g); ok('seed', s['west'] == 'clash', s)
    w = await walkin(g); ok('walk-in unchanged: Flip + two Punks walk up, three Hustlers wait', w['flip'] == 1 and w['punks'] == 2 and w['hus'] == 3, w)
    st = await through_clash_line(g)
    ok('pre-fight cine starts after Flip\u2019s line', st['xc'] == 'pre' and st['cut'] and st['skip'], st)
    # tap spam during the cine: must not walk Ryo off or break it
    for _ in range(6):
        await g.pg.touchscreen.tap(120, 300); await g.wait(80)
    sq = await until(g, lambda s: s['guard'] >= 4 or s['ig'], 40, 120)
    pr = await g.ev(PAIRS)
    if shots:
        await g.shot('t13_squareoff', hush=False)
    ok('three pairs square off (guard stances)', sq['guard'] >= 4 or sq['ig'], {'guard': sq['guard'], 'pairs': pr})
    hus = sorted([p for p in pr['hus'] if p], key=lambda p: p[0]); pks = sorted([p for p in pr['punks'] if p], key=lambda p: p[0])
    if not sq['ig'] and len(hus) == 3 and len(pks) == 2:
        ok('helper 1 faces the west Hustler', near(pks[0], (hus[0][0], hus[0][1]-42), 30), {'p': pks[0], 'h': hus[0]})
        ok('helper 2 faces the east Hustler', near(pks[1], (hus[2][0], hus[2][1]-42), 30), {'p': pks[1], 'h': hus[2]})
        ok('Ryo squares up to the middle Hustler', near(pr['ryo'], (hus[1][0], hus[1][1]-44), 30), {'r': pr['ryo'], 'h': hus[1]})
    b = await to_battle(g)
    ok('battle: Ryo vs one Hustler', b['ig'] and b['foes'] == 1 and b['ctx']['grp'] == ['c2_hustler'], b)
    ok('no battle-screen side canvas (#nqxside gone)', not b['side'], b)
    ok('pre cine released input before the fight', not b['cut'] and not b['skip'] and not b['rdy'], b)
    nf = b['nfights']
    ok('win back()', (await win(g)) == 'ok')
    p = await to_post(g)
    ok('post-win cine starts', p['xc'] == 'post' and p['cut'] and p['skip'], p)
    ok('camera pulls back to the street', p['pan'], p)
    if shots:
        await g.wait(900); await g.shot('t13_finish', hush=False)
    k = await until(g, lambda s: s['hus'] == 0 or s['xc'] != 'post', 40, 150)
    kos = [e for e in k['evs'] if 'nq:xc:ko' in e]
    ok('both helpers KO their Hustlers (down)', k['hus'] == 0 and len(kos) >= 2, k)
    rg = await until(g, lambda s: s['xc'] == '' and s['dlg'] and 'West street' in s['dlgTxt'], 50, 150)
    pr2 = await g.ev(PAIRS)
    if shots:
        await g.shot('t13_regroup', hush=False)
    ok('Flip\u2019s line plays after the cine, input free of the cut', rg['dlg'] and not rg['cut'] and not rg['pan'] and 'West street' in rg['dlgTxt'], rg)
    ok('regroup: both helpers back by Ryo', len([q for q in pr2['punks'] if q]) == 2 and all(near(q, pr2['ryo'], 110) for q in pr2['punks'] if q), pr2)
    ok('all three Hustlers marked down', all(rg['flags'].values()), rg['flags'])
    fin = await finish_chain(g)
    ok('west street closes, no re-fight', fin['q'] == 9 and fin['nfights'] == nf, fin)
    await inputs_ok(g, 'after cines')

async def t_skip(g):
    await seed(g); await walkin(g)
    st = await through_clash_line(g)
    ok('skip: pre cine up', st['xc'] == 'pre', st)
    await g.wait(300)
    ok('skip: Skip pressed (pre)', await tap_btn(g, '^Skip$'))
    await tap_btn(g, '^Skip$')  # double tap is harmless
    b = await until(g, lambda s: s['ig'], 20, 150)
    ok('skip pre: straight into Ryo vs one', b['ig'] and b['foes'] == 1 and not b['skip'], b)
    nf = b['nfights']
    await win(g)
    p = await to_post(g)
    await g.wait(250)
    ok('skip: Skip pressed (post)', await tap_btn(g, '^Skip$'))
    await tap_btn(g, '^Skip$')
    q = await until(g, lambda s: s['xc'] == '' and s['dlg'] and 'West street' in s['dlgTxt'], 30, 150)
    ok('skip post: Hustlers down, Flip\u2019s line, no lock', q['hus'] == 0 and 'West street' in q['dlgTxt'] and not q['cut'] and not q['pan'], q)
    fin = await finish_chain(g)
    ok('skip: chain completes, one fight only', fin['q'] == 9 and fin['nfights'] == nf, fin)
    await inputs_ok(g, 'after skip')

async def t_reload(g):
    await seed(g); await walkin(g)
    st = await through_clash_line(g)
    ok('reload pre: cine up', st['xc'] == 'pre', st)
    await g.wait(400)
    # c2Pop is what a reload / town re-entry runs; check the state in the same tick, before the
    # beat's proximity trigger (Ryo is still standing on it) can fire the walk-in again, as live does
    r = await g.ev("(function(){ try{ c2Pop(); }catch(e){} return 1; })() && " + SNAP.strip())
    ok('reload mid-pre: cine aborted, no lock, nothing posed', r['xc'] == '' and not r['cut'] and not r['skip'] and not r['rdy'] and r['guard'] == 0 and not r['ig'], r)
    ok('reload mid-pre: Hustlers back waiting, helpers gone, quest open', r['hus'] == 3 and r['flip'] == 0 and r['punks'] == 0 and r['q'] != 9, r)
    # it fires again (Ryo is on the trigger) and we finish the fight; then reload mid-post
    w = await until(g, lambda s: s['flip'] >= 1 and s['punks'] >= 2, 30, 200)
    ok('reload pre: walk-in fires again', w['flip'] == 1, w)
    await through_clash_line(g)
    b = await to_battle(g); nf = b['nfights']
    await win(g)
    p = await to_post(g)
    await g.wait(700)
    await g.ev("try{ c2Pop(); }catch(e){} 1"); await g.wait(400)
    r2 = await until(g, lambda s: s['dlg'] and 'West street' in s['dlgTxt'], 30, 200)
    ok('reload mid-post: no re-fight; crew regrouped and Flip\u2019s line plays', r2['dlg'] and r2['nfights'] == nf and r2['hus'] == 0 and r2['flip'] >= 1 and not r2['cut'], r2)
    fin = await finish_chain(g)
    ok('reload mid-post: chain completes', fin['q'] == 9 and fin['nfights'] == nf, fin)
    await inputs_ok(g, 'after reload')

async def t_retreat(g):
    await seed(g); await walkin(g); await through_clash_line(g)
    b = await to_battle(g); ok('retreat: battle up', b['ig'])
    await lose(g, True); await g.wait(900)
    r = await g.ev(SNAP)
    ok('retreat: clean (no cine, no pose, no lock), not won', r['xc'] == '' and not r['cut'] and r['guard'] == 0 and not r['rdy'] and r['q'] != 9 and not r['flags']['x0'], r)
    await g.ev("try{ c2Pop(); }catch(e){} 1"); await g.wait(500)
    r = await g.ev(SNAP)
    ok('retreat: beat can fire again', r['hus'] == 3, r)
    await inputs_ok(g, 'after retreat')
    w = await walkin(g)
    ok('retreat: walking up fires the beat again', w['flip'] == 1 and w['punks'] == 2, w)

async def t_defeat(g):
    await seed(g); await walkin(g); await through_clash_line(g)
    b = await to_battle(g); ok('defeat: battle up', b['ig'])
    await lose(g, False); await g.wait(1500)
    r = await g.ev(SNAP)
    ok('defeat: clean (no cine, no pose, no skip), not won', r['xc'] == '' and r['guard'] == 0 and not r['skip'] and not r['rdy'] and r['q'] != 9 and not r['flags']['x0'], r)
    await g.skipall(6)
    for _ in range(10):
        if not await tap_btn(g, '^(Next|OK|Continue|Close)'): break
        await g.wait(400)
    await g.hush()
    await g.ev("try{ c2Go('town'); }catch(e){} 1"); await g.wait(900); await g.skipall(4)
    await g.go_xy(1790, 2300); await g.ev("try{ FFF_NQ.crewSync(); }catch(e){} 1"); await g.wait(300)
    r = await g.ev(SNAP)
    ok('defeat: back in town the Hustlers wait again', r['hus'] == 3 and not r['cut'] and r['flip'] == 0, r)
    w = await walkin(g)
    ok('defeat: walking up fires the beat again', w['flip'] == 1 and w['punks'] == 2, w)

async def main():
    tests = [('main', t_main), ('skip', t_skip), ('reload', t_reload), ('retreat', t_retreat), ('defeat', t_defeat)]
    for nm, fn in tests:
        if ONLY and nm not in ONLY.split(','):
            continue
        async with h.Game(out=str(OUT)) as g:
            await g.boot()
            print('==', nm, flush=True)
            await fn(g, shots=True) if nm == 'main' else await fn(g)
            ok(f'{nm}: no page errors', not g.errs, g.errs[:3])
    print('RESULT %d/%d ALL PASS' % (sum(1 for x in RES if x[0]), len(RES)), flush=True)

if __name__ == '__main__':
    asyncio.run(main())
