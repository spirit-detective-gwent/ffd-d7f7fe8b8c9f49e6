# usage: td.py port root who dir tag [video]
import asyncio, sys, os, glob, shutil
sys.path.insert(0, '/workspace/alleycat/tools'); from h import *
port, root, who, d, tag = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
vid = len(sys.argv) > 6 and sys.argv[6] == 'v'
OUT = '/workspace/alleycat/shots/raw'; os.makedirs(OUT, exist_ok=True)
SPAWN = r"""(function(who,d){ if(who==='aoi'&&SAVE.act!=='aoi') switchChar('aoi'); SAVE.gsk={alley:1}; SAVE.intro=1; SAVE.ngp=1; W.tut=false;
 var id='bully1', s=intSprite(IMG[id+'_map']?id+'_map':id, SPH, 'dgfoe'); s.el.classList.add('foe');
 var X=420, Y=520, fa = d==='left'?0 : d==='right'?Math.PI : d==='down'?-Math.PI/2 : Math.PI/2; /* he faces AWAY from where the lead comes from */
 s.x=X; s.y=Y; place(s,0); waddle(s,0,fa); var q={key:'td0',id:id,s:s,hx:X,hy:Y,tx:null,ty:null,wait:999,st:'walk',stun:0,fa:fa,lv:(window.__KO?1:playerLv())}; W.dgF.push(q);
 var r=W.ryo, o={left:[-46,0],right:[46,0],up:[0,-46],down:[0,46]}[d]; /* d = side the lead comes FROM: left = lead left of him */
 r.x=X+o[0]; r.y=Y+o[1]+2; r.dir = d==='left'?2:d==='right'?1:d==='up'?0:3; place(r,0); W.aoi.x=r.x+(o[0]?o[0]*2:30); W.aoi.y=r.y+(o[1]?o[1]*2:0); place(W.aoi,0);
 W.cam.x=X-195/(W.S||1); W.cam.y=Y-422/(W.S||1); if(window.__HIDE)s.el.style.opacity='0.3'; window.__evlog=[]; return JSON.stringify({ctx:ambCtxOk(),ok:opnSnkFoe(q),who:opnWho()}); })"""
async def main():
  async with async_playwright() as p:
    errs=[]; vd = '/tmp/acv_'+tag if vid else None
    if vd: shutil.rmtree(vd, ignore_errors=True)
    b,ctx,pg = await newpage(p, port, root, errs, save=json.load(open('/workspace/alleycat/tools/save_c1.json')), video=vd, clock=True)
    await pg.reload(); await pg.wait_for_timeout(2500)
    await boot(pg, cont=True)
    await ev(pg, "(function(){window.__all=[];var e0=ev;ev=function(s){try{window.__all.push([Math.round(performance.now()),s])}catch(e){};return e0.apply(this,arguments)};return 1})()")
    await ev(pg, "SAVE.intro=1;SAVE.ngp=1;SAVE.gsk={alley:1};W.tut=false;clearRoam();W.spawnT=1e12;1")
    await ev(pg, "intGo('dl_hall');1"); await pg.wait_for_timeout(2500); await ev(pg, HUSH)
    gs = await pg.evaluate("(()=>{var g=document.getElementById('game');return !!(g&&g.offsetParent)})()")
    print('GAME_VISIBLE', gs)
    if os.environ.get('HIDEFOE'): await pg.evaluate("window.__HIDE=1")
    if os.environ.get('KO'): await pg.evaluate("window.__KO=1")
    if os.environ.get('NOACV'): await pg.evaluate("window.FFF_ACV=false")
    print(await ev(pg, "(%s)('%s','%s')" % (SPAWN, who, d)))
    await pg.wait_for_timeout(250)
    await ev(pg, "(function(){var e0=ev;ev=function(s){try{if(/opn:td|amb2|match:|world:opn/.test(s))window.__evlog.push([Math.round(performance.now()),s])}catch(e){};return e0.apply(this,arguments)};return 1})()")
    print('POS', await ev(pg, "(function(){var q=W.dgF.filter(function(q){return q.key==='td0'})[0],r=W.ryo;return JSON.stringify({r:[r.x|0,r.y|0],s:[q.s.x|0,q.s.y|0],fa:q.fa,st:q.st,vd:ambVdir(r,q.s,opnWho()),ok:okAt(q.s.x,q.s.y-50),okU:okAt(q.s.x-7,q.s.y+28)})})()"))
    print('PRE', await ev(pg, "JSON.stringify(window.__all.filter(function(x){return !/sfx|music|au:/.test(x[1])}).slice(-40))"))
    await ev(pg, "(function(){var q=W.dgF.filter(function(q){return q.key==='td0'})[0]; q.sus=0; q.st='walk'; q.qm=0; opnTD(q); return 1})()")
    K=float(os.environ.get('SLOWK','5')); await pg.evaluate("window.__setSlow(%s)"%K)
    t=0; shots=[]
    import time; T0=time.time()
    while t < 3000:
      bx = await pg.evaluate("(()=>{var r=window.__ev('W.ryo.el').getBoundingClientRect(),q=window.__ev('W.dgF.filter(function(q){return q.key===\\'td0\\'})[0]'),e=q&&q.s.el.getBoundingClientRect();return [r.x,r.y,r.width,r.height,e?e.x:0,e?e.y:0,Math.round(performance.now()),window.__ev('(W.ambOn?1:0)+\\':\\'+(W.on?1:0)+\\':\\'+document.body.className')]})()")
      fn='%s/%s_%05d.png'%(OUT,tag,t); await pg.screenshot(path=fn); shots.append((fn,bx)); await pg.wait_for_timeout(10); t=int((time.time()-T0)*1000/K)
    open('%s/%s_boxes.json'%(OUT,tag),'w').write(json.dumps(shots))
    await pg.evaluate('window.__setSlow(1)')
    await pg.wait_for_timeout(1500)
    await pg.screenshot(path='%s/%s_battle0.png'%(OUT,tag))
    await pg.wait_for_timeout(2000)
    await pg.screenshot(path='%s/%s_battle1.png'%(OUT,tag))
    print(await ev(pg, "JSON.stringify(window.__evlog)"))
    print('ERR', errs[:5]); await ctx.close(); await b.close()
    if vd:
      v = glob.glob(vd+'/*.webm'); print('VIDEO', v)
asyncio.run(main())
