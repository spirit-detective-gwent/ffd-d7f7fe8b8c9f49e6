#!/workspace/pwenv/bin/python3
"""Diff W.* (shallow) and key DOM state before a fight vs after escaping it. usage: wdiff.py <worktree> <port> <scenario,...> [escape|win]"""
import sys, json, asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import harness as H
import scen
ROOT=sys.argv[1]; PORT=int(sys.argv[2]); NAMES=sys.argv[3].split(','); MODE=sys.argv[4] if len(sys.argv)>4 else 'escape'
SNAP = """(function(){var o={};Object.keys(W).forEach(function(k){var v=W[k];var t=typeof v;if(v===null||t==='undefined'||t==='boolean'||t==='string'||t==='number')o[k]=v;else if(Array.isArray(v))o[k]='[arr '+v.length+']';else if(t==='function')o[k]='fn';else o[k]='{'+(v.nodeType?'el':Object.keys(v).length)+'}'});
 var d={};['game','result','world','wban','wdlg','wpause','wtags'].forEach(function(i){var e=document.getElementById(i);d[i]=e?e.className+'|'+(e.style.cssText||'').slice(0,60):null});
 o.__dom=d; o.__st={inGame:FFF_UI.ST.inGame,inWorld:FFF_UI.ST.inWorld,busy:FFF_UI.ST.busy}; return o})()"""
SKIP={'t','x','y','roamT','ambNext','fightT','safe','S','cam','tagSig','lastTap','hudT','ecgT','trail','fLv','fLvA','dropCh','vx','vy','walkT','dirty','camT','lastDir','sky','tick'}
async def run(p, name):
    b, ctx, pg, errs = await H.boot(p, PORT)
    await H.ch1_ready(pg, 1800, 3000); await H.ev(pg, scen.MK); await H.ev(pg, "window.FFF_ESC_ROLL=0; W.ambNext=1e9")
    await pg.wait_for_timeout(500)
    A = await H.ev(pg, SNAP)
    await H.ev(pg, scen.SCEN[name])
    for i in range(80):
        await pg.wait_for_timeout(250)
        s = await H.ev(pg, "(function(){var r=document.getElementById('btnRun');return {ig:FFF_UI.ST.inGame,busy:FFF_UI.ST.busy,ph:FFF_UI.ST.phase,hid:r&&r.hidden,dis:r&&r.disabled}})()")
        if s.get('ig') and not s.get('hid') and not s.get('dis') and s.get('ph')=='play' and not s.get('busy'): break
        await H.ev(pg, "if(window.FFF_WAVE&&document.getElementById('fwvB'))FFF_WAVE.stop()")
    await pg.wait_for_timeout(1200)
    c = await pg.evaluate("()=>{var r=document.getElementById('btnRun').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}")
    await pg.touchscreen.tap(*c)
    for i in range(30):
        await pg.wait_for_timeout(300)
        if not (await H.ev(pg, "FFF_UI.ST.inGame")): break
    await pg.wait_for_timeout(1500)
    B = await H.ev(pg, SNAP)
    print(f'== {name}')
    for k in sorted(set(A)|set(B)):
        if k in SKIP: continue
        if k=='__dom' or k=='__st':
            for kk in (set(A[k])|set(B[k])):
                if A[k].get(kk)!=B[k].get(kk): print(f'   {k}.{kk}: {A[k].get(kk)!r} -> {B[k].get(kk)!r}')
        elif A.get(k)!=B.get(k): print(f'   W.{k}: {A.get(k)!r} -> {B.get(k)!r}')
    print('   errs', errs[:2]); await b.close()
async def main():
    H.serve(ROOT, PORT)
    async with H.async_playwright() as p:
        for n in NAMES: await run(p, n)
if __name__=='__main__': asyncio.run(main())
