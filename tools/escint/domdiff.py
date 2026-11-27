#!/workspace/pwenv/bin/python3
"""DOM leftovers after an escape: hit-test grid + new body/#world children. usage: domdiff.py <worktree> <port> <scenario,...>"""
import sys, json, asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import harness as H
import scen
ROOT=sys.argv[1]; PORT=int(sys.argv[2]); NAMES=sys.argv[3].split(',')
GRID = """(function(){var o={};for(var y=60;y<844;y+=70)for(var x=20;x<390;x+=70){var e=document.elementFromPoint(x,y);o[x+','+y]=e?(e.tagName+'#'+e.id+'.'+(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className)).slice(0,60):null}
 var kids=function(el){return [].map.call(el.children,function(c){return c.tagName+'#'+c.id+'.'+String(c.className).slice(0,40)})};
 return {grid:o,body:kids(document.body),world:kids(document.getElementById('world')),game:kids(document.getElementById('game')).length}})()"""
async def run(p, name):
    b, ctx, pg, errs = await H.boot(p, PORT)
    await H.ch1_ready(pg, 1800, 3000); await H.ev(pg, scen.MK); await H.ev(pg, "window.FFF_ESC_ROLL=0; W.ambNext=1e9")
    await pg.wait_for_timeout(500)
    A = await H.ev(pg, GRID)
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
    await pg.wait_for_timeout(3000)
    B = await H.ev(pg, GRID)
    print('==', name)
    for k in A['grid']:
        if A['grid'][k] != B['grid'][k]: print('   grid', k, A['grid'][k], '->', B['grid'][k])
    print('   body new:', [x for x in B['body'] if x not in A['body']], ' gone:', [x for x in A['body'] if x not in B['body']])
    print('   world new:', [x for x in B['world'] if x not in A['world']][:12], ' gone:', [x for x in A['world'] if x not in B['world']][:12])
    print('   errs', errs[:2]); await b.close()
async def main():
    H.serve(ROOT, PORT)
    async with H.async_playwright() as p:
        for n in NAMES: await run(p, n)
asyncio.run(main())
