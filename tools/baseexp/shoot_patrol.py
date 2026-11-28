#!/workspace/pwenv/bin/python3
"""t583u/t587u strips: guard patrol + spotted (BACKUP!) + real 5-enemy fight; sneak-behind solo fight; hurdle rooms with roamers.
usage: shoot_patrol.py <tree> [port] OUTDIR"""
import asyncio, sys, json, os, math
OUTD = sys.argv.pop()
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shoot_baseexp.py')).read().split('\nasync def main():')[0].replace('OUTD = sys.argv.pop()', '')
exec(src)
async def wait_fight(pg, ms=6000):
    t = 0
    while t < ms:
        if await ev(pg, "!!(W.dgFight || (typeof ST!=='undefined' && ST.b && !ST.b.over && document.querySelector('.fff-battle, #battle, .bt-root')))"): return True
        await pg.wait_for_timeout(100); t += 100
    return False
async def nfoes(pg):
    return await ev(pg, "(function(){ try{ return ST.b && ST.b.foes ? ST.b.foes.length : null; }catch(e){ return null; } })()")
async def leave_fight(pg):
    await ev(pg, "(function(){ try{ if(typeof endBattle==='function') endBattle(false,{escaped:true}); }catch(e){} })(); 1")
async def main():
    os.makedirs(os.path.join(OUTD, 'raw'), exist_ok=True)
    h = serve(root, PORT)
    async with async_playwright() as p:
        # ---- 1. patrol + spotted + 5-enemy fight (Walk-in Cooler, real fight)
        b, ctx, pg, errs = await boot(p); await enter(pg, 'caf')
        await ev(pg, "var C=cafS(); ['line','kitchen','staff','cooler','dock','dish','bakery'].forEach(function(k){C.e[k]=1;}); save(); 1")
        await go(pg, 'caf', 'cooler'); seq = []
        await ev(pg, "var f=W.dgF.find(q=>q.grd); f.s.x=420; f.s.y=270; f.pi=2; f.ph='walk'; f.fa=0; place(f.s,0); 1")
        await put(pg, 560, 466); await cam(pg, 560, 400); await pg.wait_for_timeout(1500)
        seq.append((await snap(pg, 'p1'), '1. On rounds: he walks the north aisle.\nShelves hide you; his cone turns with him.'))
        await ev(pg, "var f=W.dgF.find(q=>q.grd); f.s.x=900; f.s.y=262; f.pi=2; f.ph='walk'; f.fa=0; place(f.s,0); 1"); await cam(pg, 740, 400); await pg.wait_for_timeout(1100)
        seq.append((await snap(pg, 'p2'), '2. Corner: he stops and looks round\nbefore the next leg.'))
        await pg.wait_for_timeout(2000)
        seq.append((await snap(pg, 'p3'), '3. Next leg: down the east side\ntoward the middle aisle.'))
        await ev(pg, "W.pan=null; var f=W.dgF.find(q=>q.grd); f.hold=1; f.s.x=790; f.s.y=440; f.fa=Math.PI; f.ph='walk'; place(f.s,0); 1"); await put(pg, 610, 450)
        t = 0
        while t < 4000 and not await ev(pg, "!!document.querySelector('.wgbark')"): await pg.wait_for_timeout(50); t += 50
        await pg.wait_for_timeout(200)
        seq.append((await snap(pg, 'p4'), '4. SPOTTED: "!" and he barks BACKUP!\n(cone goes off, he charges)'))
        await pg.wait_for_timeout(500)
        seq.append((await snap(pg, 'p5'), '5. Backups burst in through the doors:\nguard + 4 = one team, all on you.'))
        await ev(pg, "W.dgF.find(q=>q.grd).hold=0; 1")
        t = 0
        while t < 8000 and not await ev(pg, "!!W.dgFight"): await pg.wait_for_timeout(100); t += 100
        await pg.wait_for_timeout(3000); await skipall(pg, 3)
        seq.append((await snap(pg, 'p6'), '6. One fight, five foes: the normal\ngroup fight (guard + 4 Cafeteria bullies)'))
        strip(seq, os.path.join(OUTD, 'strip_guard_patrol_spotted.png'), 'Room guard on rounds: spotted = BACKUP! and a fight of 5 (Walk-in Cooler)')
        print('errs1', errs); await b.close()
        # ---- 2. sneak behind: solo fight (Loading Dock)
        b, ctx, pg, errs = await boot(p); await enter(pg, 'caf')
        await ev(pg, "var C=cafS(); ['line','kitchen','staff','cooler','dock','dish','bakery'].forEach(function(k){C.e[k]=1;}); save(); 1")
        await go(pg, 'caf', 'dock'); seq = []
        await ev(pg, "var f=W.dgF.find(q=>q.grd); f.s.x=640; f.s.y=520; f.pi=3; f.ph='walk'; f.fa=Math.PI; place(f.s,0); 1")
        await put(pg, 800, 540); await pg.wait_for_timeout(700)
        seq.append((await snap(pg, 's1'), '1. He walks west along the south leg.\nYou slip in behind him.'))
        await ev(pg, "var f=W.dgF.find(q=>q.grd); W.ryo.x=f.s.x+70; W.ryo.y=f.s.y; place(W.ryo,0); 1"); await pg.wait_for_timeout(500)
        seq.append((await snap(pg, 's2'), '2. Close the gap from behind:\nyou walk faster than his rounds.'))
        for i in range(30):
            if await ev(pg, "!!W.dgFight"): break
            await ev(pg, "var f=W.dgF.find(q=>q.grd); if(f) walkTo(f.s.x+2, f.s.y, true, false); 1"); await pg.wait_for_timeout(100)
        solo = await ev(pg, "[!!W.dgFight, W.dgF.filter(o=>o.bk).length, !!document.querySelector('.wgbark')]")
        await pg.wait_for_timeout(3000); await skipall(pg, 3)
        seq.append((await snap(pg, 's3'), '3. Unseen: a SOLO fight, just him.\nNo bark, no backups.'))
        print('solo', solo)
        strip(seq, os.path.join(OUTD, 'strip_guard_sneak_solo.png'), 'Sneak up behind the guard: solo fight (Loading Dock)')
        print('errs2', errs); await b.close()
        # ---- 3. hurdle rooms with their roamers
        b, ctx, pg, errs = await boot(p); await enter(pg, 'fld', roam=True); seq = []
        await ev(pg, "var S=fldS(); ['cage','showers','trainer','booth','track','lockers','coach'].forEach(function(k){S.e[k]=1;}); save(); 1")
        for k, at, cm, lab in [('cage', [700, 700], [420, 520], 'Equipment Cage: 3 roamers\nround the hurdle'), ('showers', [300, 700], [760, 600], 'Showers: 3 roamers\nby the hurdle'), ('trainer', [400, 700], [760, 600], 'Trainer\u2019s Room: 2 roamers\nby the hurdle')]:
            await go(pg, 'fld', k); await put(pg, *at); await ev(pg, "W.cool=99; 1"); await cam(pg, *cm); await pg.wait_for_timeout(900)
            seq.append((await snap(pg, 'h_' + k), lab)); await ev(pg, "W.pan=null; W.cool=0; 1")
        strip(seq, os.path.join(OUTD, 'strip_hurdle_roamers.png'), 'Storehouse hurdle rooms: beat the roamers to reach the hurdle (library rule)')
        print('errs3', errs); await b.close()
    h.shutdown()
asyncio.run(main())
