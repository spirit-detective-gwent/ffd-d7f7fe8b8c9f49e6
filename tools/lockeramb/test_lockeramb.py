#!/workspace/pwenv/bin/python3
"""v6566-lockeramb (Erik t536/t537/t538): Storehouse Equipment Bay arrival. No locker burst; the bay's 2 bullies stand
mid-room watching the door, walk up together and start ONE fight with both. Post-win the bay is clear; after Bando the
refill roamers come back roaming. Flee / loss / reload / NG+ replay cleanly.
usage: test_lockeramb.py <worktree> [port]"""
import asyncio, sys, json, os
SECT = os.environ.get('SECT', 'ABCDEF')
exec(open(__file__.rsplit('/', 1)[0] + '/lib.py').read())
NEXT = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^(Next|Skip|Close|OK|Got it)/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return 0;b[0].click();return 1}"""
STUB = "(function(){ if(!W.__fo){ W.__fo=fight; } W.__fights=[]; fight=function(g,b,c){ W.__fights.push({g:g.slice(),c:c,df:W.dgFight&&W.dgFight.key,ev:((typeof ST!=='undefined'&&ST.events)||FFF_UI.events||[]).filter(function(e){return /field/.test(e)}).slice(-8)}); ev('test:fight'); }; return 1; })()"
UNSTUB = "(function(){ if(W.__fo) fight=W.__fo; return 1; })()"
FOES = "(W.dgF||[]).map(f=>({k:f.key,id:f.id,x:Math.round(f.s.x),y:Math.round(f.s.y),st:f.st,stun:f.stun>1e6?'S':Math.round(f.stun*10)/10,vis:f.s.el.style.visibility,dom:!!f.s.el.parentNode,ent:!!f.fldEnt}))"
DOMN = "document.querySelectorAll('.dgfoe').length"
async def pump(pg, ms, sample=None):
    out = []; t = 0
    while t < ms:
        await pg.evaluate(NEXT); await pg.wait_for_timeout(100); t += 100
        if sample: out.append(await ev(pg, sample))
    return out
async def end_fight(pg, win, escaped=False):
    return await ev(pg, "(function(){ var F=W.__fights[W.__fights.length-1]; var st={ctx:F.c, escaped:%s, endHp:null}; try{ back(%s, st); }catch(e){ return 'err '+e.message; } return 1; })()" % ('true' if escaped else 'false', 'true' if win else 'false'))
def nojump(samples):
    worst = 0; hid = False
    for a, b in zip(samples, samples[1:]):
        for fa in a:
            fb = next((q for q in b if q['k'] == fa['k']), None)
            if fb: worst = max(worst, abs(fb['x'] - fa['x']) + abs(fb['y'] - fa['y']))
        for f in a: hid = hid or f['vis'] == 'hidden'
    return worst, hid
async def main():
    h = serve(root, PORT)
    async with async_playwright() as p:
        # ---- A: fresh arrival, win
        if 'A' in SECT:
            b, ctx, pg, errs = await boot(p)
            await ev(pg, CLR); await ev(pg, STUB)
            await ev(pg, "fldEnter(); 1"); await pg.wait_for_timeout(1300)
            f0 = await ev(pg, FOES)
            ok('A1 bay staged: exactly 2 foes, on mid-room marks, frozen, visible, no locker element',
               len(f0) == 2 and all(f['ent'] and f['stun'] == 'S' and f['vis'] != 'hidden' for f in f0) and sorted((f['x'], f['y']) for f in f0) == [(505, 430), (645, 430)]
               and await ev(pg, "document.querySelectorAll('.wlockburst').length") == 0, f0)
            ok('A2 the pair faces the door (down) while waiting', all(x == 0 for x in await ev(pg, "(W.dgF||[]).map(f=>+(f.s.el.dataset.dir||0))")), await ev(pg, "(W.dgF||[]).map(f=>f.s.el.dataset.dir)"))
            smp = [f0] + await pump(pg, 9000, FOES)
            worst, hid = nojump(smp)
            F = await ev(pg, "W.__fights")
            ok('A3 no teleport: max per-100ms move <= 60 px (run step ~16-32 px; old jump was ~230 px), never hidden', worst <= 60 and not hid, (worst, hid))
            ok('A4 both walked toward Ryo before the fight', (await ev(pg, "(function(){var r=W.ryo;return (W.dgF||[]).every(f=>Math.hypot(f.s.x-r.x,f.s.y-r.y)<110)})()")), await ev(pg, FOES))
            ok('A5 one fight, group = exactly the 2 bay foes', len(F) == 1 and sorted(F[0]['c'].get('dgks', [])) == ['fbay0', 'fbay1'] and len(F[0]['g']) == 2 and F[0]['c'].get('dg') == 'field', F)
            ok('A6 W.dgFight set at fight start (blocks touch/ambush double start), event entry:fight:2', F[0].get('df') == 'fbay0' and 'world:field:entry:fight:2' in F[0]['ev'], F[0])
            r = await end_fight(pg, True); await pg.wait_for_timeout(900)
            ok('A7 win: bay clear (0 foes in W.dgF and DOM), entry flag set, both keys down', r == 1 and await ev(pg, "(W.dgF||[]).length") == 0 and await ev(pg, DOMN) == 0
               and await ev(pg, "!!fldS().e.entry && !!fldS().f.fbay0 && !!fldS().f.fbay1"), (r, await ev(pg, FOES)))
            await pump(pg, 1500)
            ok('A8 controls free after the win (no stuck dlg/busy)', await ev(pg, "!W.dlg && !W.busy && !W.dgFight"), await ev(pg, "[W.dlg,W.busy,!!W.dgFight]"))
            await ev(pg, "W.fading=false; fldGo('lockers'); 1"); await pg.wait_for_timeout(600)
            l0 = await ev(pg, FOES); await pump(pg, 2500); l1 = await ev(pg, FOES)
            ok('A9 other room unaffected: Locker Corridor has its 2 roamers, not frozen, and they move', len(l0) == 2 and all(not f['ent'] and f['stun'] != 'S' for f in l0)
               and any((a['x'], a['y']) != (c['x'], c['y']) for a, c in zip(l0, l1)), (l0, l1))
            await ev(pg, "W.fading=false; fldGo('bay'); 1"); await pump(pg, 1500)
            ok('A10 bay re-entry after the win: still clear, no replay', await ev(pg, "(W.dgF||[]).length") == 0 and len(await ev(pg, "W.__fights")) == 1 and await ev(pg, "!W.busy"), await ev(pg, FOES))
            await ev(pg, "save(); 1"); await pg.reload(); await pg.wait_for_timeout(3500); await ev(pg, "WORLD_API.enter(true)"); await pg.wait_for_timeout(2500); await skipall(pg, 8)
            await ev(pg, CLR); await ev(pg, "W.fading=false; fldGo('bay'); 1"); await pump(pg, 1500)
            ok('A11 reload after the win: bay still clear', await ev(pg, "(W.dgF||[]).length") == 0 and await ev(pg, "!!fldS().e.entry"), await ev(pg, FOES))
            ok('A12 no page errors', not errs, errs); await b.close()
        # ---- B: flee, then walk up (replay), then win
        if 'B' in SECT:
            b, ctx, pg, errs = await boot(p)
            await ev(pg, CLR); await ev(pg, STUB); await ev(pg, "fldEnter(); 1"); await pump(pg, 9500)
            await end_fight(pg, False, True); await pump(pg, 1200)
            fb = await ev(pg, FOES)
            ok('B1 flee: both back on their marks, frozen, visible, exactly 2 (W.dgF and DOM), entry still pending', len(fb) == 2 and await ev(pg, DOMN) == 2
               and sorted((f['x'], f['y']) for f in fb) == [(505, 430), (645, 430)] and all(f['stun'] == 'S' for f in fb) and await ev(pg, "!fldS().e.entry && W.fldEntArm===2"), fb)
            await ev(pg, "W.dlg=false; W.busy=false; W.cool=0; W.ryo.x=575; W.ryo.y=700; place(W.ryo,0); 1"); await pump(pg, 1200)
            ok('B2 flee: no replay while Ryo keeps his distance', len(await ev(pg, "W.__fights")) == 1, await ev(pg, "W.__fights.length"))
            await ev(pg, "W.ryo.x=575; W.ryo.y=545; place(W.ryo,0); 1"); smp = await pump(pg, 6000, FOES)
            F = await ev(pg, "W.__fights"); worst, hid = nojump(smp)
            ok('B3 walk up: short confront replays, one more fight with the same 2, no teleport', len(F) == 2 and sorted(F[1]['c']['dgks']) == ['fbay0', 'fbay1'] and worst <= 60 and not hid, (len(F), worst, hid))
            await end_fight(pg, True); await pump(pg, 900)
            ok('B4 win after the retry: bay clear, entry set', await ev(pg, "(W.dgF||[]).length") == 0 and await ev(pg, DOMN) == 0 and await ev(pg, "!!fldS().e.entry"), await ev(pg, FOES))
            ok('B5 no page errors', not errs, errs); await b.close()
        # ---- C: loss (carried out), re-enter -> replay; then reload while pending -> replay
        if 'C' in SECT:
            b, ctx, pg, errs = await boot(p)
            await ev(pg, CLR); await ev(pg, STUB); await ev(pg, "fldEnter(); 1"); await pump(pg, 9500)
            await end_fight(pg, False); await pump(pg, 2500)
            ok('C1 loss: carried out of the Storehouse, entry still pending', await ev(pg, "!(W.inside&&/^sf_/.test(W.inside.id)) && !fldS().e.entry"), await ev(pg, "[W.inside&&W.inside.id, fldS().e.entry]"))
            await ev(pg, CLR); await ev(pg, "W.fading=false; fldEnter(); 1"); await pg.wait_for_timeout(1300)
            fc = await ev(pg, FOES); await pump(pg, 7000); F = await ev(pg, "W.__fights"); F = [q for q in F if q['c'].get('fldEnt')]  # the nurse office has its own (unrelated) fight
            ok('C2 re-entry after loss: same 2 on marks (no duplicates), scene replays, fight with both', len(fc) == 2 and await ev(pg, DOMN) <= 2 and sorted((f['x'], f['y']) for f in fc) == [(505, 430), (645, 430)]
               and len(F) == 2 and sorted(F[1]['c']['dgks']) == ['fbay0', 'fbay1'], (fc, [(q['df'], q['g']) for q in F]))
            await end_fight(pg, False, True); await pump(pg, 800)
            await ev(pg, "W.dlg=false; W.busy=false; save(); 1"); await pg.reload(); await pg.wait_for_timeout(3500); await ev(pg, "WORLD_API.enter(true)"); await pg.wait_for_timeout(2500)
            await ev(pg, STUB); await pump(pg, 9000)
            inside = await ev(pg, "W.inside&&W.inside.id"); F = await ev(pg, "W.__fights")
            if inside != 'sf_bay':  # the save may resume outside; walk back in
                await ev(pg, CLR); await ev(pg, "W.fading=false; fldEnter(); 1"); await pump(pg, 8000); F = await ev(pg, "W.__fights")
            ok('C3 reload while pending: pair staged again and the fight starts with both (no stuck, no dup)', len(F) >= 1 and sorted(F[-1]['c']['dgks']) == ['fbay0', 'fbay1'] and await ev(pg, DOMN) <= 2, (inside, F and F[-1]['c'].get('dgks')))
            ok('C4 no page errors', not errs, errs); await b.close()
        # ---- D: building cleared (Bando beaten) -> refill roamers back, roaming; persists over reload
        if 'D' in SECT:
            b, ctx, pg, errs = await boot(p)
            await ev(pg, CLR); await ev(pg, STUB)
            await ev(pg, "(function(){ var S=fldS(); S.e.entry=1; S.e.bay=1; S.f.fbay0=1; S.f.fbay1=1; SAVE.mb=SAVE.mb||{}; SAVE.mb.mb_field=1; save(); return 1; })()")
            await ev(pg, "fldEnter(); 1"); await pump(pg, 1500)
            await ev(pg, "W.fading=false; dgExitMaybeRefill(); intExit(true); 1"); await pg.wait_for_timeout(800)
            await ev(pg, CLR); await ev(pg, "W.fading=false; fldEnter(); 1"); await pump(pg, 1500)
            d0 = await ev(pg, FOES); await ev(pg, "W.ryo.x=1000; W.ryo.y=740; place(W.ryo,0); 1"); await pump(pg, 3000); d1 = await ev(pg, FOES)
            ok('D1 after Bando + exit: the 2 bay roamers are back, normal (not frozen, not scripted)', len(d0) == 2 and all(not f['ent'] and f['stun'] != 'S' for f in d0), d0)
            ok('D2 they roam (positions change; a roamer may touch-fight Ryo as on live), no arrival scene / scripted fight', any((a['x'], a['y']) != (c['x'], c['y']) for a, c in zip(d0, d1)) and not any(q['c'].get('fldEnt') for q in await ev(pg, "W.__fights")) and 'world:field:arrive' not in await ev(pg, "FFF_UI.events.slice(-80)"), (await ev(pg, "W.__fights"), [e for e in await ev(pg, "FFF_UI.events.slice(-80)") if 'field' in e]))
            await ev(pg, "W.dlg=false; W.busy=false; save(); 1"); await pg.reload(); await pg.wait_for_timeout(3500); await ev(pg, "WORLD_API.enter(true)"); await pg.wait_for_timeout(2500); await skipall(pg, 6)
            await ev(pg, CLR); await ev(pg, "if(W.inside) intExit(true); 1"); await pg.wait_for_timeout(500); await ev(pg, CLR); await ev(pg, "W.fading=false; fldEnter(); 1"); await pump(pg, 1500)
            d2 = await ev(pg, FOES)
            ok('D3 reload: refill roamers persist (2, roaming state)', len(d2) == 2 and all(not f['ent'] and f['stun'] != 'S' for f in d2), d2)
            ok('D4 no page errors', not errs, errs); await b.close()
        # ---- E: NG+ -> pending again, both staged, fight with both
        if 'E' in SECT:
            b, ctx, pg, errs = await boot(p)
            await ev(pg, CLR)
            await ev(pg, "(function(){ var S=fldS(); S.e.entry=1; S.f.fbay0=1; S.f.fbay1=1; SAVE.mb=SAVE.mb||{}; SAVE.mb.mb_field=1; SAVE.gouki=1; save(); return 1; })()")
            ng = await ev(pg, "(function(){ try{ v640NgStart(); }catch(e){ return 'err '+e.message; } return [SAVE.ngp, !!(SAVE.mb&&SAVE.mb.mb_field), JSON.stringify(SAVE.dg||{})]; })()")
            await pg.wait_for_timeout(1500); await skipall(pg, 10); await ev(pg, CLR); await ev(pg, STUB)
            await ev(pg, "W.fading=false; fldEnter(); 1"); await pg.wait_for_timeout(1300); fe = await ev(pg, FOES); await pump(pg, 9000); F = await ev(pg, "W.__fights")
            ok('E1 NG+: field state fresh, pair staged, one fight with exactly the 2', isinstance(ng, list) and not ng[1] and len(fe) == 2 and all(f['ent'] for f in fe) and len(F) == 1 and sorted(F[0]['c']['dgks']) == ['fbay0', 'fbay1'], (ng, fe, len(F)))
            await end_fight(pg, True); await pump(pg, 800)
            ok('E2 NG+ win: bay clear', await ev(pg, "(W.dgF||[]).length") == 0 and await ev(pg, "!!fldS().e.entry"), await ev(pg, FOES))
            ok('E3 no page errors', not errs, errs); await b.close()
        # ---- F: real battle opens with both foes (unstubbed)
        if 'F' in SECT:
            b, ctx, pg, errs = await boot(p)
            await ev(pg, CLR); await ev(pg, "fldEnter(); 1"); await pump(pg, 9500); await pg.wait_for_timeout(2500)
            bf = await ev(pg, "(function(){ var U=root.FFF_UI, s=U&&U.ST; var st=s&&(s.st||s.battle||s.B); return [!!W.dgFight, document.body.className, (FFF_UI.events||[]).filter(e=>/^match:start|foes?:|enc/.test(e)).slice(-5)]; })()")
            if shots: await pg.screenshot(path=shots + '/after_branch_battle_open.png')
            ok('F1 real fight starts after the walk-up (dgFight set, no errors)', bf[0] and not errs, bf)
            await b.close()
    h.shutdown()
    bad = [n for c, n in RES if not c]
    print(f'{len(RES) - len(bad)}/{len(RES)} PASS'); sys.exit(1 if bad else 0)
asyncio.run(main())
