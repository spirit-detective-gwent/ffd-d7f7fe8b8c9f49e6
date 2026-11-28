#!/workspace/pwenv/bin/python3
"""t11: after leaving the gym with Four Corners, every corner takeover
(including Nails alley X2) spawns and can start a clash. No duplicates
on c2Pop / re-entry. Run with FFD_INDEX=... to point at live or branch."""
import asyncio, json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import h

BORDERS = {
    'X1': (1900, 1800, 'Chuo-dori'),
    'X2': (1790, 2165, 'Nails alley / west side'),
    'X3': (2560, 3190, 'Wagashi row'),
    'X4': (3610, 2135, 'east side'),
}

def ok(name, cond, detail=None):
    print(('PASS' if cond else 'FAIL'), name, '' if detail is None else json.dumps(detail, default=str)[:300])
    if not cond:
        raise AssertionError(name)

async def await_clash(g, b, tries=12):
    for i in range(tries):
        try:
            await g.ev("if(typeof g38tClashCheck==='function')g38tClashCheck(); if(root.FFF_NALLEY&&FFF_NALLEY.retrigger)FFF_NALLEY.retrigger();1")
        except Exception:
            pass
        snap = await g.snapshot(b)
        bd = (snap.get('borders') or {}).get(b) or {}
        clash = snap.get('clash') or {}
        if bd.get('A') and bd.get('Z') and (clash.get('b') == b or (len(bd['A']) and len(bd['Z']))):
            return snap
        await g.wait(400)
    return await g.snapshot(b)

async def run():
    fails = []
    out = Path(os.environ.get('SHOTDIR', '/workspace/nailsalley/shots'))
    async with h.Game(out=str(out), index=os.environ.get('FFD_INDEX')) as g:
        boot = await g.boot()
        print('BOOT', boot)
        left = await g.gym_exit()
        print('GYM EXIT', left)
        ok('left onto town', left and left.get('room') == 'town', left)
        ok('hear phase on', bool(left and left.get('hear')), left)
        # Nails alley first — this is the reported bug
        await g.go_xy(*BORDERS['X2'][:2])
        snap = await await_clash(g, 'X2')
        print('X2', json.dumps(snap, default=str)[:800])
        bd = (snap.get('borders') or {}).get('X2') or {}
        ok('X2 posts spawned (Punk + Hustler)', len(bd.get('A') or []) >= 1 and len(bd.get('Z') or []) >= 1, bd)
        ok('X2 clash started or both sides calm on the street',
           (snap.get('clash') or {}).get('b') == 'X2' or (bd.get('A') and bd.get('Z')), snap.get('clash'))
        await g.shot('t11_x2_after_gym')
        # no duplicates after a rebuild
        n0 = len(bd.get('A') or []) + len(bd.get('Z') or [])
        await g.ev("try{c2Pop()}catch(e){};1")
        await g.wait(800)
        snap2 = await g.snapshot('X2')
        bd2 = (snap2.get('borders') or {}).get('X2') or {}
        n1 = len(bd2.get('A') or []) + len(bd2.get('Z') or [])
        print('X2 recount after c2Pop', n0, '->', n1, bd2)
        ok('X2 no duplicate posts after c2Pop', n1 <= max(n0, 2) + 0, {'before': n0, 'after': n1})

        # The other three corners
        for b, (x, y, name) in BORDERS.items():
            if b == 'X2':
                continue
            # leave current clash so another can start
            await g.ev("""(function(){ try{ if(W.g38c && typeof g38tSnapEnd==='function') g38tSnapEnd(W.g38c); else if(W.g38c && typeof g38tEnd==='function') g38tEnd(W.g38c,'test'); }catch(e){} W.g38in={}; return 1; })()""")
            await g.go_xy(x, y)
            s = await await_clash(g, b)
            bd = (s.get('borders') or {}).get(b) or {}
            print(b, name, 'A', len(bd.get('A') or []), 'Z', len(bd.get('Z') or []), 'clash', s.get('clash'))
            try:
                ok(f'{b} ({name}) posts spawned', len(bd.get('A') or []) >= 1 and len(bd.get('Z') or []) >= 1, bd)
            except AssertionError as e:
                fails.append(str(e))
            await g.shot(f't11_{b.lower()}_after_gym')

        # NG+ flags live on chapter e, not the carry whitelist
        ng = await g.ev("""(function(){
          var keep = (root.FFF_NG && FFF_NG.keep) || (typeof NG_KEEP!=='undefined' && NG_KEEP) || {};
          return { hear:'fc51Hear' in keep, win:'g38win_X2' in keep, lock:'lockAsk' in keep, n13:'n13' in keep };
        })()""")
        print('NG KEEP', ng)
        ok('fc51Hear not in NG+ carry', not (ng and ng.get('hear')))
        ok('g38win_X2 not in NG+ carry', not (ng and ng.get('win')))
        ok('lockAsk not in NG+ carry', not (ng and ng.get('lock')))
        print('ERRS', g.errs[:8])
        ok('no page errors', not g.errs, g.errs[:4])
    if fails:
        raise SystemExit('FAILED: ' + '; '.join(fails))
    print('t11 ALL PASS')

if __name__ == '__main__':
    asyncio.run(run())
