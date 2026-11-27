#!/workspace/pwenv/bin/python3
"""v6.5.66 NG+ Gouki tests.  usage: ngpgouki_test.py [index.html] [--quick]  -> PASS/FAIL lines, exit 1 on any FAIL.
  A  NG+ start resets every Ch1 Gouki / gym flag (gouki, ch1, gkPh, gkRevives, gkPhp/gkPsp, sc.ending, gym seals) from a dirty cleared save
  B  NG+ Ch1: no 'Fight' tag outside the gym; enter the gym -> foyer -> Main Court; Gouki = phase 1 -> item-revival loop -> Bond Double finale
     (the Double stays locked in phase 1 / the loop); the win plays the ending, the Chapter One card, and Continue reaches Ch2
  C  fresh game: the same sequence, unchanged, and reaches Ch2
  D  stuck saves: Gouki down + ending unplayed (NG+) resumes the ending on reload; ending played + no card resumes the card;
     no 'Fight' tag / no outright fight from the gym doors in those states or after Chapter One (fresh or NG+)"""
import asyncio, sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE)); import h, lib
args = [a for a in sys.argv[1:] if not a.startswith('--')]; QUICK = '--quick' in sys.argv
INDEX = Path(args[0]).resolve() if args else HERE.parent.parent / 'index.html'
RES = []
def ok(name, cond, extra=''):
    RES.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + ((' :: ' + str(extra)[:400]) if (extra and not cond) else ''), flush=True)
def nofight(tags): return not any(t.endswith('=Fight') for t in tags)
DIRTY = r"""(function(){ var S=SAVE; S.gkPh=1; S.gkRevives=2; S.gkPhp=9; S.gkPsp=12; var G=gymS(); GYM_SEALS.forEach(function(k){G.sl[k]=1}); G.e.press=1; save(); return 1})()"""
NGST = r"""JSON.stringify({ngp:SAVE.ngp|0,ch1:SAVE.ch1|0,gouki:SAVE.gouki|0,gkPh:SAVE.gkPh|0,gkRev:SAVE.gkRevives|0,gkPhp:SAVE.gkPhp,gkPsp:SAVE.gkPsp,end:!!(SAVE.sc&&SAVE.sc.ending),seals:gymDone(),press:!!gymS().e.press,chapter:SAVE.chapter|0,busy:W.gymBossBusy|0,gkFx:W.gkFx|0})"""
async def full(mode):
    async with h.Game(INDEX) as g:
        if mode == 'ngp':
            await g.boot(); await g.ev(lib.CLEARED); await g.ev(DIRTY); await g.pg.reload(); await g.wait(2500); await g.boot()
            await g.ev("v640NgStart(v640NgBase()); 1"); await g.wait(2500); await g.skipall(); await g.hush(); await g.ev("root.FFF_NO_TUT=1"); await g.hush(); await g.ev(h.HOOK)
            s = lib.js(await g.ev(NGST))
            ok('A NG+ start: gouki/ch1/finale flags/ending/gym seals all fresh', s['ngp'] == 1 and not s['ch1'] and not s['gouki'] and not s['gkPh'] and not s['gkRev'] and s['gkPhp'] is None and s['gkPsp'] is None and not s['end'] and s['seals'] == 0 and not s['press'] and s['chapter'] == 1, s)
            await g.ev(lib.CH1)
        else:
            await lib.setup(g, 'fresh')
        tags = await lib.outside_tags(g)
        ok(f'{mode}: no Fight tag outside the gym before Gouki', nofight(tags), tags)
        foyer, arena = await lib.to_arena(g)
        ok(f'{mode}: the gym doors walk you inside (foyer), then the Main Court', foyer['in'] == 'gy_foyer' and arena['in'] == 'gy_arena', (foyer['in'], arena['in']))
        dbl = lib.js(await g.ev("JSON.stringify({p1:(benchOf(true,{gkPhase:1})||{}).path||null,loop:(benchOf(true,{gkPhase:2,gkLoop:1})||{}).path||null,fin:(benchOf(true,{gkPhase:2,gkFin:1})||{}).path||null})"))
        ok(f'{mode}: Double locked in phase 1 and the item-revival loop, open for the Bond finale', dbl['p1'] is None and dbl['loop'] is None and dbl['fin'], dbl)
        ctxs, st, card = await lib.finale(g, log=lambda *a: None)
        seq = [c.get('ctx', {}) for c in ctxs]; kinds = []
        for c in seq:
            k = 'p1' if c.get('gkPhase') == 1 else 'loop' if c.get('gkLoop') else 'fin' if c.get('gkFin') else 'plain'
            if not kinds or kinds[-1] != k: kinds.append(k)
        ok(f'{mode}: Gouki plays phase 1 -> item-revival loop -> Bond finale (no plain duel)', kinds == ['p1', 'loop', 'fin'], kinds)
        ok(f'{mode}: the win sets Gouki down, plays the ending and shows the Chapter One card', card and st['gouki'] and st['ch1'] and st['end'], (card, st))
        await g.shot(f'test_{mode}_chapter_card')
        okc2, c2 = await lib.to_ch2(g)
        ok(f'{mode}: Continue reaches Chapter Two' + (' (NG+ mark kept)' if mode == 'ngp' else ''), okc2 and c2['chapter'] == 2 and c2['c2'] and (c2['ngp'] == (1 if mode == 'ngp' else 0)), c2)
        ok(f'{mode}: no page errors', not g.errs, g.errs[:3])
async def rawboot(g):
    """a player's Continue: no hush, so a resumed finale / ending is not cut off"""
    await g.pg.touchscreen.tap(195, 420); await g.pg.evaluate("WORLD_API.enter(true)"); await g.wait(1500)
async def tap_to_card(g, n=260):
    for i in range(n):
        if await g.ev("!!document.getElementById('wchap')"): return True
        c = await g.pg.evaluate(lib.TAPS)
        if c: await g.pg.touchscreen.tap(c[0], c[1])
        await g.wait(300)
    return bool(await g.ev("!!document.getElementById('wchap')"))
async def stuck():
    async with h.Game(INDEX) as g:
        await lib.setup(g, 'ngp')
        # Gouki down, ending never played (e.g. closed during the confession): what Erik saw as the 'Fight' marker + reset loop
        await g.ev("SAVE.gouki=1; SAVE.dbl=1; save(); 1")
        tags = await lib.outside_tags(g)
        ok('D NG+ Gouki down / Ch1 open: no Fight tag on the gymnasium', nofight(tags), tags)
        await g.ev("window.__ctxs=[]; window.__evs=[]; gymDialog(); 1"); await g.wait(800)
        e = await g.ev("window.__evs.filter(function(s){return /resume|ending:clear/.test(s)})")
        ok('D NG+ gym doors with Gouki down resume the ending (no outright fight)', any('gym:resume:ending' in x for x in e) and not await g.ev("window.__ctxs.length"), e)
        await g.pg.reload(); await g.wait(2500); await rawboot(g)
        card = await tap_to_card(g); st = lib.js(await g.ev(lib.ST))
        ok('D NG+ reload with Gouki down and the ending unplayed resumes the ending and reaches the Chapter One card', card and st['ch1'] == 1 and st['end'], st)
        # ending played, card lost
        await g.ev("(function(){var c=document.getElementById('wchap'); if(c) c.remove(); SAVE.gouki=1; SAVE.ch1=0; SAVE.sc.ending=1; SAVE.chapter=1; save(); return 1})()")
        await g.pg.reload(); await g.wait(2500); await rawboot(g)
        card = await tap_to_card(g, 30); st = lib.js(await g.ev(lib.ST))
        ok('D NG+ reload with the ending played but no card resumes the Chapter One card', st['ch1'] == 1 and card, (st, card))
        ok('D no page errors', not g.errs, g.errs[:3])
    async with h.Game(INDEX) as g:
        await g.boot(); await g.ev(lib.CLEARED); await g.pg.reload(); await g.wait(2500); await g.boot()
        tags = await lib.outside_tags(g)
        ok('D fresh cleared run (after Chapter One): no Fight tag on the gymnasium', nofight(tags), tags)
        await g.ev("window.__ctxs=[]; gymDialog(); 1"); await g.wait(800)
        b = await g.ev("[].map.call(document.querySelectorAll('#wdlg.on button'),function(e){return e.textContent.trim()})")
        ok('D gym doors after Chapter One: Gouki talks, no Rematch/Challenge button', b and not any(('Rematch' in x or 'Challenge' in x or 'Fight' in x) for x in b), b)
        ok('D no page errors (cleared)', not g.errs, g.errs[:3])
async def main():
    print('index', INDEX, flush=True)
    await stuck()
    if not QUICK:
        await asyncio.gather(full('ngp'), full('fresh'))
    print(f'{sum(RES)}/{len(RES)} passed', flush=True); sys.exit(0 if all(RES) else 1)
asyncio.run(main())
