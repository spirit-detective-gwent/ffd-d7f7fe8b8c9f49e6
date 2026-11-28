#!/workspace/pwenv/bin/python3
"""v6.5.66 FFF_HP tests (Erik t614u-t622u): two-at-a-time pulls on every Ch2 gang crew, the hotel crews turning, wins that stick
(Kissa Gekko round trip + reload), the lock guard, the load-time save repair of a stuck / respawned hotel save, and card input in
the rematch.  usage: test_hotelpull.py [section ...]   (FFD_INDEX=... to point at another index.html; PORT is picked free)"""
import asyncio, sys, json, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); import h
from real import real_win
HERE = Path(__file__).resolve().parent
OUT = os.environ.get('HP_SHOTS', '/workspace/hotelpull/shots')
SETUP = """(function(){
  SAVE.chapter=2; SAVE.ch1=1; SAVE.ch2=1; SAVE.bond=SAVE.bond||{}; SAVE.bond.path='balanced'; SAVE.bond.lock=1;
  try { STORY.ensure(SAVE); } catch(e){}
  var st=c2S(); st.e=st.e||{}; st.e.arrive=1; st.e.gymIn=1; st.e.genji=1; st.e.c2sRep=1; st.e.roam=1; st.e.called=1; st.e.c2lMap=1; st.e.sealKnown=1;
  st.q.cq2_arrive=9; st.q.cq2_hq=9; st.q.cq2_scout=9; st.q.cq2_locks=0; st.qa='cq2_locks';
  st.e.run_fac='arc'; st.e.n13='done';
  %s
  try { c2QSync(); save(); } catch(e){}
  return 1; })()"""
HOOK = """(function(){ if(window.__hk) return 1; window.__hk=1; window.__ctxs=[]; var f0=fight; fight=function(grp,boss,ctx){ try{ window.__ctxs.push({grp:grp,ctx:ctx}) }catch(e){} return f0.apply(this,arguments) };
  window.__evs=[]; var e0=ev; ev=function(k){ try{ if(/world:(qs|c2v2|nq|s2|hp|13u)/.test(k)) window.__evs.push(k)}catch(e){}; return e0.apply(this,arguments)}; return 1})()"""
ST = {
 'cold': "st.q.cq2_n_look=9; st.e.n13corner='dep'; st.q.cq2_nq_west=9; st.e.nq={udon:1,won:{udon:1,west:1}};",
 'west': "st.q.cq2_n_look=9; st.e.n13corner='dep'; st.e.nq={udon:1,won:{udon:1}};",
 'paint': "st.q.cq2_n_look=9; st.e.n13corner='dep'; st.q.cq2_nq_west=9; st.q.cq2_nq_cold=9; st.e.nq={udon:1,won:{udon:1,west:1,hotel:1}};",
}
LOCK = "JSON.stringify({busy:!!W.busy,cut:!!W.cut,dlg:!!W.dlg,scr:!!W.scr,amb:!!W.ambOn,dgF:!!W.dgFight,on:!!W.on,game:document.getElementById('game').classList.contains('on')})"
HUD = "(function(){ var o={}; [['swap','#wSwap'],['map','#wMap'],['menu','#wMenu']].forEach(function(p){var b=document.querySelector(p[1]); if(!b){o[p[0]]=false;return} var r=b.getBoundingClientRect(); var e=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2); o[p[0]]=!!(e&&(e===b||b.contains(e)))}); return o})()"
FAIL = []
def ok(name, cond, info=''):
    print(('PASS ' if cond else 'FAIL ') + name + ('' if cond else '  ' + str(info)[:600]), flush=True)
    if not cond: FAIL.append(name)
async def boot(g, extra, x, y):
    pg = g.pg
    await pg.touchscreen.tap(195, 420); await pg.evaluate("WORLD_API.enter(true)"); await g.wait(1500); await g.skipall()
    await g.ev("root.FFF_NO_TUT=1"); await pg.evaluate("WORLD_API.c2Begin(true)"); await g.wait(2500); await g.skipall(); await g.hush()
    await g.ev(HOOK); await g.ev(SETUP % extra); await g.go('town', x, y, 0); await g.wait(1500)
    await g.ev("try{FFF_NQ.chainRepair(); FFF_NQ.crewSync()}catch(e){}"); await g.wait(1500); await g.hush()
async def wait_battle(g, n0, tries=30):
    for i in range(tries):
        await g.wait(400)
        if await g.ev("window.__ctxs.length") > n0 and await g.ev("document.getElementById('game').classList.contains('on')"): return True
    return False
async def settle(g, n=10):
    for i in range(n): await g.wait(500); await g.adv(2)
def foes_js(crew_re): return "(W.dgF||[]).filter(function(o){return %s.test(o.crew)&&o.s&&o.s.el&&o.s.el.parentNode}).map(function(o){return o.key})" % crew_re
TAP = """(function(re){var r=W.ryo; var L=(W.dgF||[]).filter(function(o){return re.test(o.crew)&&o.s&&o.s.el&&o.s.el.parentNode&&!o.gone}); if(!L.length) return null; L.sort(function(a,b){return Math.hypot(a.s.x-r.x,a.s.y-r.y)-Math.hypot(b.s.x-r.x,b.s.y-r.y)}); var f=L[0];
 W.ryo.x=f.s.x; W.ryo.y=f.s.y-70; place(W.ryo,0); camera(true); f.hpNear=0; f.hpTurn=0; f.clashFa=null; if(f.face!=null) f.fa=f.face; return [f.key, ambTap({x:f.s.x,y:f.s.y-30})]})(%s)"""
TOUCH = """(function(re){var L=(W.dgF||[]).filter(function(o){return re.test(o.crew)&&o.s&&o.s.el&&o.s.el.parentNode&&!o.gone}); if(!L.length) return null; var f=L[0]; W.ryo.x=f.s.x; W.ryo.y=f.s.y+22; place(W.ryo,0); camera(true); return f.key})(%s)"""
BATTLE = "(function(){var b=FFF_UI.ST.b; if(!b) return null; var g=(b.grp&&b.grp.length)?b.grp:[b.s[1]]; return {n:g.length, ids:g.map(function(s){return s.ch||s.id}), feet:(document.getElementById('fE')||{}).className}})()"

async def pull_run(g, crew_re, how, expect_sizes, label):
    """engage the crew until nobody is left; every engagement must pull min(2, men left of THAT crew)"""
    sizes = []
    for k in range(8):
        left = await g.ev(foes_js(crew_re))
        if not left: break
        n0 = await g.ev("window.__ctxs.length")
        if await g.ev("document.getElementById('game').classList.contains('on')"): n0 -= 1; r = 'already on (a man stood on Ryo)'  # the next crewmate walked into Ryo
        else: r = await g.ev((TAP if how == 'tap' else TOUCH) % crew_re)
        if not await wait_battle(g, n0):
            ok(label + ' battle %d starts' % k, False, r); return sizes
        ctx = (await g.ev("window.__ctxs.slice(-1)[0].ctx.dgks"))
        crews = set(x.rsplit('_', 1)[0] for x in ctx)
        await g.wait(1500); bt = await g.ev(BATTLE)
        if k == 0: await g.shot(label + '_battle', hush=False)
        sizes.append(len(ctx))
        same = await g.ev("(function(ks){ var c=ks[0].replace(/_\\d+$/,''); return (W.dgF||[]).filter(function(o){return o.crew===c && ks.indexOf(o.key)<0 && o.s&&o.s.el&&o.s.el.parentNode}).length })(%s)" % json.dumps(ctx))
        exp = min(2, len(ctx) + same)
        ok('%s fight %d pulls %d (got %s, one crew)' % (label, k, exp, ctx), len(ctx) == exp and len(crews) == 1, ctx)
        ok('%s fight %d battle has %d foes' % (label, k, len(ctx)), bt and bt['n'] == len(ctx), bt)
        ok('%s fight %d grounded' % (label, k), bt and 'bt-feet-c2' in (bt.get('feet') or ''), bt)
        res = await real_win(g)
        await settle(g, 8)
        gone = await g.ev("(function(ks){ return ks.every(function(k){ var f=c2S().f[k]; var w=(W.dgF||[]).some(function(o){return o.key===k&&o.s&&o.s.el&&o.s.el.parentNode}); return f&&!w; }) })(%s)" % json.dumps(ctx))
        ok('%s fight %d: both flagged + world sprites gone (%s)' % (label, k, res), gone, ctx)
        if await g.ev("document.getElementById('game').classList.contains('on')"): continue
        for t in range(14):  # a crew's last fight may roll a short story beat: let it play, then the world must be free
            lk = json.loads(await g.ev(LOCK)); hud = await g.ev(HUD)
            if not (lk['busy'] or lk['cut'] or lk['dlg'] or lk['amb'] or lk['dgF']) and all(hud.values()): break
            await g.adv(4); await g.skipall(2); await g.wait(600)
        ok('%s fight %d: no lock after' % (label, k), not (lk['busy'] or lk['cut'] or lk['dlg'] or lk['amb'] or lk['dgF']) and all(hud.values()), [lk, hud])
    return sizes

async def sec_hotel(alley):
    async with h.Game(out=OUT) as g:
        await boot(g, ST['cold'], 1890, 870)
        if alley: await g.ev("SAVE.gsk={alley:1}; save(); 1")
        sizes = await pull_run(g, '/^nq_c\\d$/', 'tap', None, 'hotel-' + ('alley' if alley else 'tap'))
        ok('hotel: three fights of two (%s)' % sizes, sizes == [2, 2, 2], sizes)
        c = await g.ev("[FFF_NQ.stg('cold'), c2S().q.cq2_nq_cold, (FFF_QS.count?JSON.stringify(FFF_QS.count('cq2_nq_cold')):'')]")
        ok('hotel: stage 3, quest stepped to the desk (%s)' % c, c[0] == 3 and c[1] == 1, c)
        if alley: await g.shot('after_2enemy_battle_end', hush=False)

async def sec_ko():
    """a high-level back attack used to knock a quest man out alone (no fight, no quest beat): now a fight of two on cut HP"""
    async with h.Game(out=OUT) as g:
        await boot(g, ST['cold'], 1890, 870)
        await g.ev("SAVE.gsk={alley:1}; save(); playerLv=function(){return 14}; 1")
        sizes = await pull_run(g, '/^nq_c\\d$/', 'tap', None, 'hotel-ko')
        ok('ko: no lone knockouts (%s)' % sizes, sizes == [2, 2, 2], sizes)
        evs = await g.ev("window.__evs.filter(function(e){return /hp:noko/.test(e)}).length")
        ok('ko: knockouts turned into fights (%d)' % evs, evs >= 3, evs)
        c = await g.ev("[FFF_NQ.stg('cold'), c2S().q.cq2_nq_cold]"); ok('ko: quest counted (%s)' % c, c == [3, 1], c)

async def sec_groups():
    async with h.Game(out=OUT) as g:
        await boot(g, ST['west'], 1760, 2120)
        s1 = await pull_run(g, '/^nq_w1$/', 'touch', None, 'west-w1')
        ok('west w1 (2 men): one fight of two (%s)' % s1, s1 == [2], s1)
        await settle(g, 6); await g.hush(); await g.ev("if(FFF_NQ.stg('west')!=='w2'){FFF_NQ.setStg('west','w2')} FFF_NQ.crewSync(); 1"); await g.wait(1500)
        sizes = await pull_run(g, '/^nq_w2$/', 'touch', None, 'west-w2')
        ok('west w2 (3 men): 2 then 1 (%s)' % sizes, sizes == [2, 1], sizes)
    async with h.Game(out=OUT) as g:
        await boot(g, ST['paint'], 330, 1200)
        sizes = await pull_run(g, '/^nq_p\\d$/', 'touch', None, 'wall')
        ok('west wall: three fights of two (%s)' % sizes, sizes == [2, 2, 2], sizes)
    async with h.Game(out=OUT) as g:
        await boot(g, "st.e.n13='look'; st.q.cq2_n_look=0; st.qa='cq2_n_look';", 1050, 3300)
        await g.ev("try{ var C=FFF_13U; if(C&&C.chainRepair) C.chainRepair(); c2Pop(); }catch(e){} 1"); await g.wait(2500)
        L = await g.ev(foes_js('/^n13_look$/'))
        if L:
            sizes = await pull_run(g, '/^n13_look$/', 'touch', None, 'lookouts')
            ok('lookouts (3 men): 2 then 1 (%s)' % sizes, sizes[:2] == [2, 1], sizes)
        else: print('SKIP lookouts: none spawned in this setup')

async def sec_turn():
    async with h.Game(out=OUT) as g:
        await boot(g, ST['cold'], 1890, 870)
        await g.ev("W.ryo.x=1700; W.ryo.y=760; place(W.ryo,0); camera(true); 1"); await g.wait(800)
        await g.shot('facing_far', hush=False)
        b = await g.ev("(W.dgF||[]).filter(function(o){return o.crew==='nq_c1'}).map(function(o){return [o.key, ambSide(o)]})")
        # quick approach: struck within the notice time = still from behind
        await g.ev("W.ryo.x=1864; W.ryo.y=860; place(W.ryo,0); camera(true); 1"); await g.wait(300)
        q = await g.ev("(function(){var f=(W.dgF||[]).filter(function(o){return o.key==='nq_c1_0'})[0]; return [ambSide(f), !!f.hpTurn]})()")
        ok('turn: a quick approach from behind still gets the back attack (%s)' % q, q[0] == 'back' and not q[1], q)
        await g.wait(1600)
        a = await g.ev("(W.dgF||[]).filter(function(o){return o.crew==='nq_c1'}).map(function(o){return [o.key, ambSide(o), !!o.hpTurn, +o.fa.toFixed(2)]})")
        ok('turn: after standing near, the men face Ryo (%s)' % a, all(x[1] == 'front' and x[2] for x in a), a)
        dd = await g.ev("(W.dgF||[]).filter(function(o){return o.crew==='nq_c1'}).map(function(o){return o.s.el.getAttribute('data-dir')})")
        ok('turn: the turn shows on screen (sprite row for the new facing, not the front row) (%s)' % dd, all(x not in (None, '0') for x in dd), dd)
        await g.shot('after_facing', hush=False)
        far = await g.ev("(W.dgF||[]).filter(function(o){return /^nq_c/.test(o.crew)&&Math.hypot(o.s.x-W.ryo.x,o.s.y-W.ryo.y)>260}).map(function(o){return !!o.hpTurn})")
        ok('turn: far crews keep their post (%s)' % far, not any(far), far)
        await g.ev("W.ryo.x=1890; W.ryo.y=700; place(W.ryo,0); camera(true); 1"); await g.wait(1200)
        bk = await g.ev("(W.dgF||[]).filter(function(o){return o.crew==='nq_c1'}).map(function(o){return [!!o.hpTurn, ambSide(o)]})")
        ok('turn: they look back to the door when Ryo leaves (%s)' % bk, all((not x[0]) for x in bk), bk)

async def sec_guard():
    async with h.Game(out=OUT) as g:
        await boot(g, ST['paint'], 1890, 960)
        await g.ev("W.busy=true; W.cut=true; W.ambOn={q:null}; W.dgFight={key:'x'}; 1")
        await g.wait(3000); mid = json.loads(await g.ev(LOCK))
        ok('guard: holds a few seconds (no early release)', mid['busy'], mid)
        await g.wait(7000); lk = json.loads(await g.ev(LOCK)); hud = await g.ev(HUD)
        ok('guard: a lock with nothing on screen is released in <= 10 s (%s)' % lk, not (lk['busy'] or lk['cut'] or lk['amb'] or lk['dgF']), lk)
        ok('guard: HUD reachable after (%s)' % hud, all(hud.values()), hud)
        mv = await g.drag(0, 80); ok('guard: stick moves Ryo after (%s)' % mv, abs(mv[1]) > 40, mv)
        await g.ev("scene(null,[['aoi','Hold on.']]); W.busy=true; 1"); await g.wait(10500)
        lk2 = json.loads(await g.ev(LOCK)); ok('guard: a live dialog is never cut', lk2['busy'] and lk2['dlg'], lk2)
        await g.adv(4); await g.wait(9500)
        lk3 = json.loads(await g.ev(LOCK)); ok('guard: released once the dialog closed', not lk3['busy'], lk3)
        await g.ev("(function(){var o=document.createElement('div'); o.id='nqsting'; o.className='v2'; document.body.appendChild(o); W.cut=true; return 1})()")
        await g.wait(22000); s = await g.ev("[!!document.getElementById('nqsting'), !!W.cut]")
        ok('guard: a dead block-win overlay is removed (%s)' % s, s == [False, False], s)
        hud = await g.ev(HUD); ok('guard: HUD reachable after the overlay (%s)' % hud, all(hud.values()), hud)

async def sec_door():
    """Erik's street lock: standing on the shut hotel door's lip re-fired the doorway every frame (stick killed at touch)"""
    async with h.Game(out=OUT) as g:
        await g.load_fixture(str(HERE / 'fixtures' / 'erik_hotel_respawned.json')); await g.ev(HOOK)
        await g.ev("(function(){window.__wk=0;var e0=ev;ev=function(k){if(/int:walkin:c2_town:nq_e_hotel/.test(k))window.__wk++;return e0.apply(this,arguments)};return 1})()")
        await g.ev("W.ryo.x=1890; W.ryo.y=900; place(W.ryo,0); camera(true); 1"); await g.wait(500)
        up = await g.drag(0, -80); await g.ev("window.__wk=0"); await g.wait(2000); n = await g.ev("window.__wk")
        ok('door: the shut hotel door fires at most once, not every frame (%d in 2 s after walking in)' % n, n <= 1, n)
        await g.shot('door_after_walk_in', hush=False)
        dn = await g.drag(0, 80); sd = await g.drag(-90, 0)
        ok('door: Ryo walks away from the shut door (up %s, down %s, side %s)' % (up, dn, sd), abs(dn[1]) > 40 and abs(sd[0]) > 40, [up, dn, sd])
        await g.ev("W.ryo.x=1890; W.ryo.y=830; place(W.ryo,0); save(); 1"); await g.wait(500)
        await g.pg.reload(); await g.wait(2500); await g.pg.touchscreen.tap(195, 420); await g.pg.evaluate("WORLD_API.enter(true)"); await g.wait(5000); await g.hush()
        p0 = await g.ev("[Math.round(W.ryo.x),Math.round(W.ryo.y),c2Room&&c2Room()]")
        a = await g.drag(0, 80); b = await g.drag(0, -60); c = await g.drag(0, 90); d = await g.drag(90, 0)
        ok('door: reloaded on the lip, movement still works (%s: %s %s %s %s)' % (p0, a, b, c, d), abs(a[1]) > 30 and abs(c[1]) > 30 and abs(d[0]) > 30, [p0, a, b, c, d])

async def sec_stick():
    """win, Kissa Gekko and back, timers run out, reload twice: the hotel men stay down"""
    async with h.Game(out=OUT) as g:
        await boot(g, ST['cold'], 1890, 870)
        await pull_run(g, '/^nq_c[12]$/', 'touch', None, 'stick-setup')
        await g.ev("c2Enter('gekko'); 1"); await g.wait(4000); await g.adv(6)
        await g.ev("c2Out('gekko'); 1"); await g.wait(4000); await g.adv(6)
        await g.ev("Object.keys(SAVE.crewDown||{}).forEach(function(k){SAVE.crewDown[k]-=900000}); W.ryo.x=2150; W.ryo.y=2650; place(W.ryo,0); save(); 1"); await g.wait(3000)
        for rl in range(2):
            await g.pg.reload(); await g.wait(2500); await g.pg.touchscreen.tap(195, 420); await g.pg.evaluate("WORLD_API.enter(true)"); await g.wait(5000)
        s = await g.ev("[Object.keys(c2S().f).filter(function(k){return /^nq_c/.test(k)}).length, (W.dgF||[]).filter(function(o){return /^nq_c[12]$/.test(o.crew)}).length, FFF_NQ.stg('cold'), JSON.stringify(SAVE.crewDown||{})]")
        ok('stick: 4 win flags kept, 0 of them back on the street, stage 2 (%s)' % s, s[0] == 4 and s[1] == 0 and s[2] == 2 and 'nq_' not in s[3], s)

async def sec_repair(fx):
    """Erik's save: the hotel men he beat are back on the street (flags wiped by the respawn timer) and the count says 2"""
    async with h.Game(out=OUT) as g:
        await g.load_fixture(fx); await g.ev(HOOK)
        s = await g.ev("[Object.keys(c2S().f).filter(function(k){return /^nq_c/.test(k)}).sort().join(','), (W.dgF||[]).filter(function(o){return /^nq_c/.test(o.crew)}).map(function(o){return o.key}).join(','), FFF_NQ.stg('cold'), JSON.stringify(SAVE.crewDown||{}), (FFF_QS.count?JSON.stringify(FFF_QS.count('cq2_nq_cold')):'')]")
        ok('repair: the two beaten crews are down again (c1, c2) and off the street (%s)' % s, s[0] == 'nq_c1_0,nq_c1_1,nq_c2_0,nq_c2_1' and s[1] == 'nq_c0_0,nq_c0_1' and s[2] == 2 and 'nq_' not in s[3], s)
        lk = json.loads(await g.ev(LOCK)); hud = await g.ev(HUD)
        ok('repair: loads unlocked (%s %s)' % (lk, hud), not (lk['busy'] or lk['cut'] or lk['dlg']) and all(hud.values()), [lk, hud])
        await g.shot('repair_loaded', hush=False)
        m = await g.ev("(function(){ pause(); var on=document.getElementById('wpause').className; var p=!!W.paused; try{ phClose(); }catch(e){ try{ unpause(); }catch(e2){} } W.paused=false; W.dlg=false; return [on, p] })()")
        ok('repair: the menu opens (%s)' % m, m[1], m)
        a0 = await g.ev("SAVE.act"); await g.ev("swapTap(); 1"); await g.wait(1200); a1 = await g.ev("SAVE.act")
        ok('repair: swap works (%s -> %s)' % (a0, a1), a0 != a1, [a0, a1])
        await g.ev("W.ryo.x=1890; W.ryo.y=900; place(W.ryo,0); camera(true); 1"); await g.wait(500)
        mv = await g.drag(0, 80); mv0 = await g.drag(0, -80); mv2 = await g.drag(90, 0)
        ok('repair: town movement down / up / sideways (%s %s %s)' % (mv, mv0, mv2), abs(mv[1]) > 40 and abs(mv0[1]) > 40 and abs(mv2[0]) > 40, [mv, mv0, mv2])
        # the rematch: the last crew, a stale world lock and a dead overlay left over; the cards must still take a tap
        await g.ev("(function(){var o=document.createElement('div'); o.id='nqsting'; o.className='v2'; o.hpT=performance.now()-20000; document.body.appendChild(o); return 1})()")
        n0 = await g.ev("window.__ctxs.length"); await g.ev(TOUCH % '/^nq_c0$/')
        started = await wait_battle(g, n0); await g.wait(3000); await g.skipall(3)
        hd = await g.ev("(function(){var c=[...document.querySelectorAll('#hand .card')]; if(!c.length) return null; var r=c[0].getBoundingClientRect(); var e=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2); return {n:c.length, x:r.x+r.width/2, y:r.y+r.height/2, top:!!(e&&(c[0]===e||c[0].contains(e)||(e.closest&&e.closest('#hand'))))}})()")
        sel = None
        if hd: await g.tap(hd['x'], hd['y']); await g.wait(700); sel = await g.ev("document.querySelectorAll('#hand .card.sel').length")
        ok('repair: rematch starts and a card takes the tap (%s sel=%s)' % (hd, sel), started and hd and hd['top'] and sel == 1, [started, hd, sel])
        await g.shot('repair_rematch_cards', hush=False)
        await real_win(g); await settle(g, 10)
        c = await g.ev("[FFF_NQ.stg('cold'), c2S().q.cq2_nq_cold, c2S().qa]")
        ok('repair: the last crew finishes the hotel door (stage 3, desk objective) (%s)' % c, c[0] == 3 and c[1] == 1, c)
        await g.ev("W.ryo.x=1890; W.ryo.y=884; place(W.ryo,0); c2Enter('hotel'); 1"); await g.wait(4500); await g.adv(6); await g.hush()
        rm = await g.ev("c2Room()"); mv = await g.drag(0, -80); mv2 = await g.drag(0, 80); mv3 = await g.drag(80, 0)
        ok('repair: hotel lobby walkable up / down / sideways (%s %s %s %s)' % (rm, mv, mv2, mv3), rm == 'hotel' and abs(mv[1]) > 40 and abs(mv2[1]) > 40 and abs(mv3[0]) > 40, [rm, mv, mv2, mv3])
        await g.ev("W.ryo.x=640; W.ryo.y=400; place(W.ryo,0); 1")
        await g.ev("(function(){ try { var A=WORLD_API; } catch(e){} var sp=INT[W.inside.id].spots.filter(function(s){return s.id==='nq_hotel_desk'})[0]; return !!sp })()")
        await g.ev("c2ActC('hotel','nq_hotel_desk'); 1"); await g.wait(800); await g.adv(30); await g.wait(6000); await g.adv(30); await g.wait(3000)
        q = await g.ev("[c2S().q.cq2_nq_cold, c2S().q.cq2_nq_paint, c2S().qa]")
        print('  desk ->', q)
        ok('repair: front desk closes the hotel job and opens the next (%s)' % q, q[0] == 9 and q[1] is not None, q)
        lk = json.loads(await g.ev(LOCK)); ok('repair: no lock at the end (%s)' % lk, not (lk['busy'] or lk['cut'] or lk['dlg']), lk)
        print('  errs', g.errs[:4]); ok('repair: no page errors', not g.errs, g.errs[:4])

SECS = {'hotel': lambda: sec_hotel(False), 'alley': lambda: sec_hotel(True), 'ko': sec_ko, 'groups': sec_groups, 'turn': sec_turn, 'guard': sec_guard, 'door': sec_door, 'stick': sec_stick,
        'repair': lambda: sec_repair(str(HERE / 'fixtures' / 'erik_hotel_respawned.json'))}
async def main():
    names = sys.argv[1:] or list(SECS)
    for n in names:
        print('== ' + n, flush=True)
        try: await SECS[n]()
        except Exception as e: ok(n + ' ran', False, repr(e))
    print('RESULT', 'FAIL %d: %s' % (len(FAIL), FAIL) if FAIL else 'ALL PASS', flush=True)
    sys.exit(1 if FAIL else 0)
asyncio.run(main())
