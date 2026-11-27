import asyncio, sys, json
sys.path.insert(0, '/workspace/alleycat/tools'); from h import *
from PIL import Image
async def main():
  async with async_playwright() as p:
    errs=[]; b,ctx,pg = await newpage(p, 8801, '/workspace/alleycat/wt', errs, save=json.load(open('/workspace/alleycat/tools/save_c1.json')))
    await pg.reload(); await pg.wait_for_timeout(2500); await boot(pg, cont=True)
    await ev(pg, "clearRoam();W.spawnT=1e12;intGo('dl_hall');1"); await pg.wait_for_timeout(2500); await ev(pg, HUSH)
    await ev(pg, """(function(){var id='bully1';W.__q=[];[[300,0],[360,3],[420,0],[480,3],[540,1]].forEach(function(a,i){var s=intSprite(IMG[id+'_map']?id+'_map':id, SPH, 'dgfoe'); s.el.classList.add('foe'); s.x=a[0]; s.y=520; place(s,0); waddle(s,0,[Math.PI/2,0,0,-Math.PI/2][a[1]]); var q={key:'fp'+i,id:id,s:s,hx:s.x,hy:s.y,wait:999,st:'walk',stun:0,lv:1,fa:0}; W.dgF.push(q); W.__q.push(q); opnFoePrep(q);}); W.ryo.x=420; W.ryo.y=420; place(W.ryo,0); W.cam.x=420-195; W.cam.y=520-422; W.busy=true; return 1})()""")
    await pg.wait_for_timeout(1500)
    await pg.screenshot(path='/tmp/fp2_a.png')
    print(await ev(pg, "(function(){var Q=W.__q; return [opnFoeShow(Q[0],'kneelv',0,0),opnFoeShow(Q[1],'kneelv',3,0),opnFoeShow(Q[2],'foldv',0,2),opnFoeShow(Q[3],'foldv',3,2),opnFoeShow(Q[4],'kneel',1,0)].join()})()"))
    await pg.wait_for_timeout(600)
    await pg.screenshot(path='/tmp/fp2_b.png')
    print(await ev(pg, "JSON.stringify(W.__q.map(function(q){return [q.s.el.style.backgroundImage.slice(0,30),q.s.el.style.backgroundSize,q.s.el.style.backgroundPosition]}))"))
    await b.close()
asyncio.run(main())
