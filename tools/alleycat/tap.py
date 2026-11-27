# one-button check: tap.py port root case...  case = lock:pos:act  (lock 0/1 = Alley Cat owned, pos back|front, act tap|hold|run|walk)
import asyncio, sys, os, re, json
sys.path.insert(0, '/workspace/alleycat/tools'); from h import *
src = open('/workspace/alleycat/tools/td.py').read(); SPAWN = re.search(r'SPAWN = r"""(.*?)"""', src, re.S).group(1)
port, root, cases = int(sys.argv[1]), sys.argv[2], sys.argv[3:]
OUT='/workspace/alleycat/shots/raw'
async def one(p, case):
    own, pos, act = case.split(':')
    errs=[]; b,ctx,pg = await newpage(p, port, root, errs, save=json.load(open('/workspace/alleycat/tools/save_c1.json')))
    await pg.reload(); await pg.wait_for_timeout(2500); await boot(pg, cont=True)
    await ev(pg, "SAVE.intro=1;SAVE.ngp=1;W.tut=false;clearRoam();W.spawnT=1e12;1"); await ev(pg, "intGo('dl_hall');1"); await pg.wait_for_timeout(2500); await ev(pg, HUSH)
    await ev(pg, "(%s)('ryo','left')" % SPAWN)
    await ev(pg, "(function(){var q=W.dgF.filter(function(q){return q.key==='td0'})[0]; q.sus=0; q.st='walk'; q.qm=0; %s %s var FA=%s; q.fa=FA; waddle(q.s,0,FA); window.__lk=setInterval(function(){ if(W.ambOn||W.opnOn||document.getElementById('game').classList.contains('on')){clearInterval(window.__lk);return} q.fa=FA; q.st='walk'; q.sus=0; q.qm=0; },16); window.__evlog=[]; window.__fx=[]; var f0=fight; fight=function(g,b,c){try{window.__fx.push({g:g,c:c?{acDown:c.acDown,opnAc:c.opnAc,amb:c.amb}:null})}catch(e){} return f0.apply(this,arguments)}; var e0=ev; ev=function(s){try{if(/opn:|amb2|match:/.test(s))window.__evlog.push(s)}catch(e){};return e0.apply(this,arguments)}; return 1})()"
        % ("" if own=='1' else "SAVE.gsk={};", "", "Math.PI" if pos=='front' else "0"))
    await pg.wait_for_timeout(200)
    c = await pg.evaluate("(()=>{var q=window.__ev('W.dgF.filter(function(q){return q.key===\\'td0\\'})[0]');var r=q.s.el.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height*0.55]})()")
    print('DBG', case, await ev(pg, "(function(){var q=W.dgF.filter(function(q){return q.key==='td0'})[0],r=W.ryo;return JSON.stringify({fa:q.fa,st:q.st,sus:q.sus,qm:q.qm,see:seeK(q,r.x,r.y,W.inside?okAt:okSee,true),side:ambSide(q),hot:noticeHot(q),sees:ambSees(q),r:[r.x|0,r.y|0],s:[q.s.x|0,q.s.y|0],run:W.run,mv:r.moving,up:typeof acTapUp==='function'?acTapUp(q):'na'})})()"), flush=True)
    if act == 'tap': await pg.touchscreen.tap(*c)
    elif act == 'hold': await pg.mouse.move(*c); await pg.mouse.down(); await pg.wait_for_timeout(700); await pg.mouse.up()
    else: await ev(pg, "W.run=%s; walkTo(W.ryo.x+110, W.ryo.y, true, %s); 1" % (('true','true') if act=='run' else ('false','false')))
    await pg.wait_for_timeout(1200); await pg.screenshot(path='%s/tap_%s.png'%(OUT,case.replace(':','_')))
    await pg.wait_for_timeout(3500)
    lg = await ev(pg, "JSON.stringify({ev:window.__evlog.filter(function(s){return !/fp:|sheet|sting|mute|hold:500|handoff/.test(s)}).slice(0,24),fight:window.__fx,on:document.getElementById('game').classList.contains('on'),pose:!!document.querySelector('.kopose.acdown, #eFig.ac-down')})")
    print('CASE', case, lg, 'ERR', errs[:3], flush=True); await ctx.close(); await b.close()
async def main():
  async with async_playwright() as p:
    for c in cases: await one(p, c)
asyncio.run(main())
