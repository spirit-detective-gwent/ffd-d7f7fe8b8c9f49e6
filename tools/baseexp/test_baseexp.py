#!/workspace/pwenv/bin/python3
"""v6566-baseexp (GGD-89, Erik t548u): Cafeteria + Storehouse grow to 8 rooms each.
Cafeteria: crate rooms Cooler / Dock / Bakery each have ONE room guard (turns on a beat, props are cover, carrying widens his sight),
no roamers there until the base is cleared. Storehouse: hurdles in Cage / Showers / Trainer, lane fee (set only while Bando is on the
far side, else he kicks it to the Cage), one-use Timing Booth lever slows one lap. Supplies: 9 pairs, caf 2 / fld 2, 8 boxes per base.
usage: test_baseexp.py <worktree> [port]     SECT=DGRLSCO to pick sections"""
import asyncio, sys, json, os, math
SECT = os.environ.get('SECT', 'DGRLSCO')
exec(open(__file__.rsplit('/', 1)[0] + '/../lockeramb/lib.py').read())
NEXT = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^(Next|Skip|Close|OK|Got it)/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return 0;b[0].click();return 1}"""
STUB = "(function(){ if(!W.__fo){ W.__fo=fight; } W.__fights=[]; fight=function(g,b,c){ W.__fights.push({g:g.slice(),c:c}); ev('test:fight'); }; return 1; })()"
GF = "(function(){ var f=(W.dgF||[]).find(q=>q.grd); return f?{k:f.key,st:f.st,x:Math.round(f.s.x),y:Math.round(f.s.y),fa:+f.fa.toFixed(3),sus:+(f.sus||0).toFixed(3),gi:f.gi,N:f.N&&f.N.r,cone:f.cone&&f.cone.style.transform,off:f.cone&&f.cone.classList.contains('off')}:null; })()"
FOES = "(W.dgF||[]).map(f=>({k:f.key,st:f.st,g:!!f.grd}))"
async def pump(pg, ms, sample=None):
    out = []; t = 0
    while t < ms:
        await pg.evaluate(NEXT); await pg.wait_for_timeout(100); t += 100
        if sample: out.append(await ev(pg, sample))
    return out
async def free(pg):
    await ev(pg, CLR); await ev(pg, "W.dlg=false; W.busy=false; W.cool=0; W.libPend=null; W.pan=null; 1")
async def go(pg, base, k, at=None):
    fn = 'cafGo' if base == 'caf' else 'fldGo'
    await ev(pg, "W.fading=false; %s('%s'%s); 1" % (fn, k, (', ' + json.dumps(at)) if at else ''))
    await pg.wait_for_timeout(700); await skipall(pg, 6); await free(pg)
async def put(pg, x, y):
    await ev(pg, "W.path=[]; W.ryo.v=0; W.ryo.x=%d; W.ryo.y=%d; place(W.ryo,0); 1" % (x, y))
async def end_fight(pg, win, escaped=False):
    return await ev(pg, "(function(){ var F=W.__fights[W.__fights.length-1]; var st={ctx:F.c, escaped:%s, endHp:null}; try{ back(%s, st); }catch(e){ return 'err '+e.message; } return 1; })()" % ('true' if escaped else 'false', 'true' if win else 'false'))
async def enter(pg, base):
    await ev(pg, ("cafEnter(); 1" if base == 'caf' else "fldEnter(); 1")); await pg.wait_for_timeout(1500); await skipall(pg, 8); await free(pg)
    if base == 'fld':  # the bay arrival pair (lockeramb) is not part of this test: mark it done
        await ev(pg, "var S=fldS(); S.e.entry=1; S.f.fbay0=1; S.f.fbay1=1; S.e.surprise=1; save(); 1")

async def main():
    h = serve(root, PORT)
    async with async_playwright() as p:
        # ---------- D: door pairs (both bases), landing spots walkable, room counts
        if 'D' in SECT:
            b, ctx, pg, errs = await boot(p)
            st = await ev(pg, """(function(){ var out=[]; [['caf',CAFG],['fld',FLDG]].forEach(function(B){ var G=B[1]; Object.keys(G).forEach(function(k){ Object.keys(G[k].doors).forEach(function(d){ var D=G[k].doors[d]; if(!D.to) return; var t=D.to.split(':'), R2=G[t[0]]; var back=R2&&R2.doors[t[1]]; out.push([B[0],k,d,D.to, !!(back&&back.to===k+':'+d), !!D.lock]); }); }); }); return out; })()""")
            bad = [q for q in st if not q[4]]
            ok('D1 every door has a matching door back (%d doors)' % len(st), not bad and len(st) >= 26, bad)
            ok('D2 room counts: Cafeteria 8, Storehouse 8', await ev(pg, "[Object.keys(CAFG).length, Object.keys(FLDG).length]") == [8, 8])
            await enter(pg, 'caf'); walk = []
            for q in st:
                if q[0] != 'caf' or q[5]: continue
                await go(pg, 'caf', q[1]); await ev(pg, "cafDoor('%s'); 1" % q[2]); await pg.wait_for_timeout(1000); await skipall(pg, 4); await free(pg)
                walk.append([q[1], q[2], await ev(pg, "[cafRoom(), okAt(W.ryo.x,W.ryo.y)]"), q[3].split(':')[0]])
            await enter(pg, 'fld')
            for q in st:
                if q[0] != 'fld' or q[5]: continue
                await go(pg, 'fld', q[1]); await ev(pg, "fldDoor('%s'); 1" % q[2]); await pg.wait_for_timeout(1000); await skipall(pg, 4); await free(pg)
                walk.append([q[1], q[2], await ev(pg, "[fldRoom(), okAt(W.ryo.x,W.ryo.y)]"), q[3].split(':')[0]])
            badw = [w for w in walk if not (w[2][0] == w[3] and w[2][1])]
            ok('D3 walking through every door lands in the right room on a walkable spot (%d trips)' % len(walk), not badw and len(walk) == len([q for q in st if not q[5]]), badw)
            mp = await ev(pg, "(function(){ var a=cafMap(), b=fldMap(); return [/\\/8 rooms seen/.test(a), /\\/8 rooms seen/.test(b), (a.match(/<rect/g)||[]).length, (b.match(/<rect/g)||[]).length]; })()")
            ok('D4 floor plans list 8 rooms each and say /8 rooms seen', mp == [True, True, 8, 8], mp)
            ok('D5 no page errors', not errs, errs); await b.close()

        # ---------- G: guard beat, cover, detect, carry, fight sends crate home, resolved after win
        if 'G' in SECT:
            b, ctx, pg, errs = await boot(p); await ev(pg, STUB); await enter(pg, 'caf')
            await go(pg, 'caf', 'cooler'); await put(pg, 980, 470)
            smp = await pump(pg, 9000, GF)
            fas = [s['fa'] for s in smp if s]
            hold_w = sum(1 for a in fas if abs(abs(a) - math.pi) < 0.02 or abs(a - math.pi) < 0.02); hold_e = sum(1 for a in fas if abs(a) < 0.02)
            ok('G1 cooler guard stands at his post (never moves) while he turns', all(s and s['x'] == 420 and s['y'] == 466 and s['st'] == 'grd' for s in smp), smp[-1])
            ok('G2 beat: holds west and east ~3 s each, turns in between (both facings seen, mid-turn samples few)', hold_w >= 20 and hold_e >= 20 and len(fas) - hold_w - hold_e <= 18, (hold_w, hold_e, len(fas)))
            mids = [a for a in fas if 0.1 < abs(a) < 3.0]
            ok('G3 turns go through the back wall (north, fa<0) only', mids and all(a < 0 for a in mids), mids[:8])
            ok('G4 cone element follows (rotate set), visible while on post', all(s['cone'] and 'rotate' in s['cone'] and not s['off'] for s in smp if s), smp[-1])
            # dock: in-cone open line -> spotted; behind the sacks -> hidden; behind him -> unseen
            await go(pg, 'caf', 'dock')
            await ev(pg, "var f=W.dgF.find(q=>q.grd); f.gT=99; f.gi=0; f.fa=Math.PI; f.turn=null; 1")
            await put(pg, 100, 490); s1 = await pump(pg, 3000, GF)
            ok('G5 behind the sacks inside his cone: never noticed (prop blocks sight)', all(s['sus'] == 0 and s['st'] == 'grd' for s in s1), s1[-1])
            await put(pg, 760, 440); s2 = await pump(pg, 3000, GF)
            ok('G6 behind him (east, he faces west), 330 px: never noticed', all(s['sus'] == 0 and s['st'] == 'grd' for s in s2), s2[-1])
            await put(pg, 180, 420); s3 = await pump(pg, 2500, GF)
            ok('G7 in the open, inside his cone: "?" then "!" (alert/chase) within 2.5 s', any(s['st'] in ('alert', 'chase') for s in s3), s3[-1])
            await pump(pg, 4000); F = await ev(pg, "W.__fights")
            ok('G8 he reaches you: one fight with just the guard', len(F) == 1 and F[0]['c']['dgk'] == 'gdock' and F[0]['g'] == ['bully4'], F)
            await end_fight(pg, False, True); await pump(pg, 400); await free(pg)
            await put(pg, 900, 700); s4 = await pump(pg, 15000, GF)
            ok('G9 fled: he searches, then walks back to his post and resumes the beat', s4[-1] and s4[-1]['st'] == 'grd' and s4[-1]['x'] == 430 and s4[-1]['y'] == 420, s4[-1])
            # bakery: carrying widens his reach (400 px straight ahead: unseen empty-handed, seen with the crate)
            await go(pg, 'caf', 'bakery'); await ev(pg, "W.__fights=[]; var f=W.dgF.find(q=>q.grd); f.gT=99; f.gi=0; f.fa=Math.PI; f.turn=null; 1")
            await put(pg, 410, 400); s5 = await pump(pg, 2500, GF)
            ok('G10 400 px ahead, empty-handed: outside his 360 px reach, not noticed', all(s['sus'] == 0 and s['st'] == 'grd' for s in s5), s5[-1])
            await put(pg, 1000, 420); await ev(pg, "cafLift('bakery'); 1"); await pump(pg, 600); await free(pg)
            g = await ev(pg, GF)
            ok('G11 lifting the crate: carry on, guard notice switches to the carry reach (x1.25)', await ev(pg, "W.carry") == 'bakery' and abs(g['N'] - 450) < 1 and 'scale(1.25)' in g['cone'], g)
            await ev(pg, "var f=W.dgF.find(q=>q.grd); f.gT=99; f.gi=0; f.fa=Math.PI; f.turn=null; f.sus=0; f.qm=0; 1")
            await put(pg, 410, 400); s6 = await pump(pg, 2500, GF)
            ok('G12 same spot carrying the crate: spotted', any(s['st'] in ('alert', 'chase') for s in s6), s6[-1])
            await pump(pg, 4000); F = await ev(pg, "W.__fights")
            ok('G13 spotted while carrying -> fight', len(F) == 1 and F[0]['c']['dgk'] == 'gbakery', F)
            await end_fight(pg, True); await pump(pg, 900); await free(pg)
            ok('G14 the fight sends the crate home (Bakery, not carried) and the beaten guard stays resolved', await ev(pg, "[W.carry, cafS().cr.bakery|0, !!cafS().f.gbakery, !!W.cafCr]") == [None, 0, True, True], await ev(pg, "[W.carry, cafS().cr.bakery, cafS().f.gbakery, !!W.cafCr]"))
            await go(pg, 'caf', 'staff'); await go(pg, 'caf', 'bakery')
            ok('G15 re-enter the Bakery: no guard, no roamers (not cleared yet), crate there', await ev(pg, "[(W.dgF||[]).length, !!W.cafCr]") == [0, True], await ev(pg, FOES))
            ok('G16 no page errors', not errs, errs); await b.close()

        # ---------- R: roamers only after the clear; guard gone once the crate is dumped
        if 'R' in SECT:
            b, ctx, pg, errs = await boot(p); await ev(pg, STUB); await enter(pg, 'caf'); res = {}
            for k in ['cooler', 'dock', 'dish', 'bakery']:
                await go(pg, 'caf', k); await pump(pg, 1500); res[k] = await ev(pg, FOES)
            ok('R1 before the clear: guard rooms hold exactly their one guard, Dish Room none, no roamers',
               all(len(res[k]) == 1 and res[k][0]['g'] for k in ['cooler', 'dock', 'bakery']) and res['dish'] == [], res)
            line = []
            for k in ['line', 'kitchen']:
                await go(pg, 'caf', k); line.append(len(await ev(pg, FOES)))
            ok('R2 Lunch Line / Kitchen keep their live roamers', all(n >= 1 for n in line), line)
            await go(pg, 'caf', 'cooler'); await ev(pg, "cafLift('cooler'); 1"); await go(pg, 'caf', 'kitchen'); await ev(pg, "cafDump(); 1"); await pump(pg, 600); await free(pg)
            await go(pg, 'caf', 'cooler'); await pump(pg, 800)
            ok('R3 crate dumped: the Cooler guard is gone for good, still no roamers', await ev(pg, "(W.dgF||[]).length") == 0, await ev(pg, FOES))
            await ev(pg, "SAVE.mb=SAVE.mb||{}; SAVE.mb.mb_cafe=1; save(); 1"); await go(pg, 'caf', 'bakery'); await pump(pg, 600)
            ok('R4 cleared but not left yet: no guard, no roamers', await ev(pg, "(W.dgF||[]).length") == 0, await ev(pg, FOES))
            await ev(pg, "dgMarkRefill('cafe'); 1"); post = {}
            for k in ['cooler', 'dock', 'bakery', 'dish']:
                await go(pg, 'caf', k); post[k] = await ev(pg, FOES)
            ok('R5 after the clear + refill: roamers appear in Cooler / Dock / Bakery (2 each, no guard), Dish Room stays empty',
               all(len(post[k]) == 2 and not any(f['g'] for f in post[k]) for k in ['cooler', 'dock', 'bakery']) and post['dish'] == [], post)
            ok('R6 no page errors', not errs, errs); await b.close()

        # ---------- L: lane fee kick, cage pickup, far-side set, lever slow lap, rings
        if 'L' in SECT:
            b, ctx, pg, errs = await boot(p); await enter(pg, 'fld')
            await go(pg, 'fld', 'showers'); await ev(pg, "fldLift('showers'); 1"); await pump(pg, 500); await free(pg)
            ok('L1 lift the Showers hurdle', await ev(pg, "W.carry") == 'h:showers')
            await go(pg, 'fld', 'track'); await pump(pg, 600); await free(pg)
            rg = await ev(pg, "(W.fldRing||[]).map(q=>q.st)")
            ok('L2 slot rings exist on the 3 marks and show ok/no while carrying', len(rg) == 3 and all(s in ('ok', 'no') for s in rg), rg)
            near = await ev(pg, "(function(){ var a=fldSlotAng('slot0'); W.fldLap.t=Math.floor(W.fldLap.t)+(a/(2*Math.PI)+1)%1; var ok0=fldFeeOk('slot0'); fldPlace('slot0'); return [ok0, !!fldS().sl.slot0, W.carry, !!fldS().kick.showers, fldS().hr.showers|0, document.querySelectorAll('.fkick').length]; })()")
            ok('L3 set while Bando is next to the mark: kicked (not set, carry gone, hurdle marked kicked to the Cage, flight prop)', near == [False, False, None, True, 0, 1], near)
            await pump(pg, 400); dl = await ev(pg, DLG); await skipall(pg, 6); await free(pg)
            ok('L4 first kick plays the scene (Bando line)', 'my lane' in dl or 'Not in my lane' in dl or await ev(pg, "!!fldS().e.kick"), dl[:200])
            await pump(pg, 900); ok('L5 the flying hurdle prop is gone after its one-shot', await ev(pg, "document.querySelectorAll('.fkick').length") == 0)
            await go(pg, 'fld', 'showers'); ok('L6 the Showers no longer hold it', await ev(pg, "!W.fldHr"))
            await go(pg, 'fld', 'cage')
            cg = await ev(pg, "[!!(W.fldHk&&W.fldHk.showers), tagsBuild&&1, (fldTags('sf_cage',INT.sf_cage)||[]).map(t=>t.key.split(':')[1]+'='+t.lab)]")
            ok('L7 it lies in the Equipment Cage with a Lift tag (and the Cage\'s own hurdle too)', cg[0] and 'hk_showers=Lift' in cg[2] and 'hurdle=Lift' in cg[2], cg)
            await ev(pg, "fldAct('hk_showers'); 1"); await pump(pg, 400); await free(pg)
            ok('L8 lift it from the Cage', await ev(pg, "[W.carry, !(W.fldHk&&W.fldHk.showers)]") == ['h:showers', True])
            await ev(pg, "fldDrop('fight'); 1"); await pump(pg, 300); await free(pg)
            ok('L9 a fight drop sends it back to the Cage (its new home)', await ev(pg, "[W.carry, !!(W.fldHk&&W.fldHk.showers), fldHome('showers')]") == [None, True, 'cage'])
            await ev(pg, "fldAct('hk_showers'); 1"); await pump(pg, 300); await free(pg)
            await go(pg, 'fld', 'track'); await pump(pg, 400); await free(pg)
            far = await ev(pg, "(function(){ var a=fldSlotAng('slot0'); W.fldLap.t=Math.floor(W.fldLap.t)+(a/(2*Math.PI)+0.5+1)%1; var ok0=fldFeeOk('slot0'); fldRingTick(); var r=(W.fldRing||[]).find(q=>q.id==='slot0').st; fldPlace('slot0'); return [ok0, r, !!fldS().sl.slot0, W.carry]; })()")
            ok('L10 far side: ring says ok and the hurdle sets', far == [True, 'ok', True, None], far)
            await pump(pg, 500); await skipall(pg, 6); await free(pg)
            # lever
            await go(pg, 'fld', 'booth')
            tg = await ev(pg, "(fldTags('sf_booth',INT.sf_booth)||[]).map(t=>t.key.split(':')[1]+'='+t.lab)")
            ok('L11 Timing Booth: lever has a Pull tag', 'lever=Pull' in tg, tg)
            await ev(pg, "fldAct('lever'); 1"); await pump(pg, 400); await skipall(pg, 6); await free(pg)
            ok('L12 pulled: used + armed, tag gone', await ev(pg, "[!!fldS().e.lever, !!fldS().e.slowArm, (fldTags('sf_booth',INT.sf_booth)||[]).some(t=>/lever/.test(t.key))]") == [True, True, False])
            await ev(pg, "fldAct('lever'); 1"); await pump(pg, 300); await free(pg)
            ok('L13 second pull: stuck, nothing re-arms', await ev(pg, "!!fldS().e.lever") and True)
            await go(pg, 'fld', 'track'); await pump(pg, 300); await free(pg)
            s0 = await ev(pg, "[W.fldLap.slowTo, W.fldLap.s.el.classList.contains('fslow'), W.fldLap.t, !!fldS().e.slowArm]")
            await pump(pg, 2000); t1 = await ev(pg, "W.fldLap.t")
            rate = (t1 - s0[2]) / 2.0
            ok('L14 next track visit: slowed lap (slowTo=1, fslow class, rate ~0.45x of 0.38)', s0[0] == 1 and s0[1] and not s0[3] and 0.12 < rate < 0.22, (s0, rate))
            await ev(pg, "W.fldLap.t=0.97; 1"); await pump(pg, 1500)
            s2 = await ev(pg, "[W.fldLap.slowTo, W.fldLap.s.el.classList.contains('fslow'), W.fldLap.t]"); await pump(pg, 1000); t3 = await ev(pg, "W.fldLap.t")
            ok('L15 after one lap: back to full speed, class removed', s2[0] is None and not s2[1] and 0.3 < (t3 - s2[2]) / 1.0 < 0.46, (s2, t3))
            await go(pg, 'fld', 'lockers'); await go(pg, 'fld', 'track'); await pump(pg, 300)
            ok('L16 lever is one use: the following visit is full speed', await ev(pg, "[W.fldLap.slowTo==null, !W.fldLap.s.el.classList.contains('fslow')]") == [True, True])
            ok('L17 no page errors', not errs, errs); await b.close()

        # ---------- S: supply boxes
        if 'S' in SECT:
            b, ctx, pg, errs = await boot(p)
            r = await ev(pg, """(function(){ var P=FFF_SUP.pairs(), tot=0; Object.keys(P).forEach(k=>tot+=P[k]); var walls=WKIT_TABLE.wall; var box={caf:1,fld:1}; walls.forEach(w=>{ if(box[w.go]!=null) box[w.go]++; });
              var risk={caf:['cf_cooler','cf_dock','cf_bakery'], fld:['sf_bay','sf_lockers']}, bad=[], cnt={};
              for (var i=0;i<200;i++){ var L=FFF_SUP.roll(); ['caf','fld'].forEach(function(fac){ var ks=Object.keys(L).filter(c=>(walls.find(w=>w.id===c)||{}).go===fac || (fac==='caf'&&c==='cf_staff') || (fac==='fld'&&c==='sf_coach'));
                var g=ks.filter(c=>L[c]==='gauze').length, t=ks.filter(c=>L[c]==='tape').length; if(g!==2||t!==2) bad.push([fac,'gt',g,t]); if(!ks.some(c=>risk[fac].indexOf(c)>=0)) bad.push([fac,'risk',ks]);
                ks.forEach(c=>{cnt[c]=(cnt[c]||0)+1;}); }); }
              var nw=['cf_cooler','cf_dock','cf_dish','cf_bakery','sf_cage','sf_showers','sf_trainer','sf_booth'].filter(id=>!walls.find(w=>w.id===id));
              return {P:P, tot:tot, box:box, bad:bad.slice(0,5), nbad:bad.length, cnt:cnt, missing:nw}; })()""")
            ok('S1 pairs: 9 total, caf 2, fld 2, lib 3, art 1, gym 1', r['tot'] == 9 and r['P'] == {'lib': 3, 'gym': 1, 'art': 1, 'caf': 2, 'fld': 2}, r['P'])
            ok('S2 every new room has a first-aid box; 8 boxes per base', not r['missing'] and r['box'] == {'caf': 8, 'fld': 8}, (r['missing'], r['box']))
            ok('S3 200 rolls: each base gets exactly 2 gauze + 2 tape (4 of 8 boxes stocked, 4 empty), always >=1 in a guarded/patrolled room', r['nbad'] == 0, r['bad'])
            ok('S4 the stocked boxes vary between rolls (new rooms included)', all(r['cnt'].get(c, 0) > 0 for c in ['cf_cooler', 'cf_dock', 'cf_dish', 'cf_bakery', 'sf_cage', 'sf_showers', 'sf_trainer', 'sf_booth']), r['cnt'])
            await enter(pg, 'caf'); kd = []
            for base, k in [('caf', 'cooler'), ('caf', 'dock'), ('caf', 'dish'), ('caf', 'bakery'), ('fld', 'cage'), ('fld', 'showers'), ('fld', 'trainer'), ('fld', 'booth')]:
                if base == 'fld' and not await ev(pg, "!!fldRoom()"): await enter(pg, 'fld')
                await go(pg, base, k)
                kd.append(await ev(pg, "(function(){ var d=wkitDefNow(); if(!d) return null; SAVE.supLay={v:1,c:{}}; SAVE.supLay.c[d.id]='gauze'; var g0=phMatN('gauze'); var w=wkitWallById(d.id); wkitGrantWall(w); return [d.id, d.kind, okAt(d.stand[0], d.stand[1]), wkitInRange(d, d.stand[0], d.stand[1]), phMatN('gauze')-g0, wkitGive(d.id).length]; })()"))
            ok('S5 each new room: wall box found, stand point walkable and in reach, a stocked box pays once', all(q and q[1] == 'wall' and q[2] and q[3] and q[4] == 1 and q[5] == 0 for q in kd), kd)
            ok('S6 no page errors', not errs, errs); await b.close()

        # ---------- C: full completion of both bases with the real functions
        if 'C' in SECT:
            b, ctx, pg, errs = await boot(p); await ev(pg, STUB); await enter(pg, 'caf')
            for k in ['cooler', 'dock', 'bakery']:
                await go(pg, 'caf', k); await ev(pg, "cafLift('%s'); 1" % k); await pump(pg, 300); await free(pg)
                await go(pg, 'caf', 'kitchen'); await ev(pg, "cafDump(); 1"); await pump(pg, 600); await skipall(pg, 8); await free(pg)
            ok('C1 Cafeteria: 3 crates dumped -> shutter open', await ev(pg, "[cafDone(), cafOpen()]") == [3, True], await ev(pg, "[cafDone(), JSON.stringify(cafS().cr)]"))
            await go(pg, 'caf', 'line'); await ev(pg, "cafDoor('gN'); 1"); await pg.wait_for_timeout(1500)
            ok('C2 the Dining Hall door opens (boss room reached)', await ev(pg, "cafRoom()") == 'dining', await ev(pg, "cafRoom()"))
            await skipall(pg, 10); await free(pg)
            await enter(pg, 'fld')
            for i, k in enumerate(['cage', 'showers', 'trainer']):
                await go(pg, 'fld', k); await ev(pg, "fldLift('%s'); 1" % k); await pump(pg, 300); await skipall(pg, 4); await free(pg)
                await go(pg, 'fld', 'track'); await pump(pg, 300); await skipall(pg, 4); await free(pg)
                await ev(pg, "(function(){ var a=fldSlotAng('slot%d'); W.fldLap.t=Math.floor(W.fldLap.t)+(a/(2*Math.PI)+0.5+1)%%1; fldPlace('slot%d'); })(); 1" % (i, i)); await pump(pg, 500); await skipall(pg, 6); await free(pg)
            ok('C3 Storehouse: 3 hurdles set on the far side -> track open', await ev(pg, "[fldDone(), fldOpen()]") == [3, True], await ev(pg, "[fldDone(), JSON.stringify(fldS().sl), JSON.stringify(fldS().kick)]"))
            ok('C4 no page errors', not errs, errs); await b.close()

        # ---------- O: old saves (no migration, no crash)
        if 'O' in SECT:
            b, ctx, pg, errs = await boot(p)
            await ev(pg, "SAVE.carry='line'; var C=cafS(); C.cr.line=1; C.cr.kitchen=2; var F=fldS(); F.hr.bay=1; SAVE.supLay={v:1,c:{cf_kitchen:'gauze'}}; localStorage.setItem('fff_world', JSON.stringify(SAVE)); 1")
            await pg.reload(); await pg.wait_for_timeout(3500); await ev(pg, "WORLD_API.enter(true)"); await pg.wait_for_timeout(2500); await skipall(pg, 8); await free(pg)
            o = await ev(pg, "[W.carry, cafDone()]")
            ok('O1 old save with a stale crate carry loads: carry dropped, no crash', o[0] in (None, '') and o[1] == 0, o)
            await ev(pg, "SAVE.carry='h:bay'; localStorage.setItem('fff_world', JSON.stringify(SAVE)); 1")
            await pg.reload(); await pg.wait_for_timeout(3500); await ev(pg, "WORLD_API.enter(true)"); await pg.wait_for_timeout(2500); await skipall(pg, 8); await free(pg)
            ok('O2 stale hurdle carry dropped', await ev(pg, "W.carry") in (None, ''))
            await enter(pg, 'caf'); await go(pg, 'caf', 'cooler'); await enter(pg, 'fld'); await go(pg, 'fld', 'cage')
            ok('O3 old save walks the new rooms with no page errors', not errs, errs); await b.close()
    fails = [n for c, n in RES if not c]
    print('\nRESULT %d/%d PASS' % (len(RES) - len(fails), len(RES)) + ('' if not fails else ' FAILS: ' + '; '.join(fails)))
asyncio.run(main())
