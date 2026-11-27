# Ch2 town one-button check (uses /workspace/corners harness read-only). FFD_INDEX=<index> c2tap.py tag case...  case = own:hot:act (act tap|walk|run)
import asyncio, sys, os, json
sys.path.insert(0, '/workspace/corners'); import h, r1
tag, cases = sys.argv[1], sys.argv[2:]
PICK = """(function(hot){var r=W.ryo,best=null,bd=1e9;(ambList()||[]).forEach(function(f){if(!f.s||!f.s.el)return;var d=Math.hypot(f.s.x-r.x,f.s.y-r.y);if(d<bd){bd=d;best=f}}); if(!best) return 'none:'+(ambList()||[]).length+':'+(W.dgF||[]).length+':'+(W.roam||[]).length;
 var f=best, fac=G38T.FAC[f.id], E=c2S().e; if(hot&&fac) E['hot_'+fac]=1; var FA=0; window.__lk=setInterval(function(){ if(W.ambOn||W.opnOn||document.getElementById('game').classList.contains('on')||W.dlg){clearInterval(window.__lk);return} f.fa=FA; f.sus=0; f.qm=0; },16); f.wait=999; f.tx=f.ty=null; f.sus=0; f.qm=0; f.st='walk'; f.fa=0; waddle(f.s,0,0); r.x=f.s.x-46; r.y=f.s.y+2; r.dir=2; place(r,0); if(W.aoi){W.aoi.x=r.x-60;W.aoi.y=r.y;place(W.aoi,0)} camera(true); window.__T=f;
 window.__evlog=[]; window.__fx=[]; if(!window.__hk2){window.__hk2=1; var f0=fight; fight=function(g,b,c){try{window.__fx.push({g:g,acDown:c&&c.acDown,opnAc:c&&c.opnAc})}catch(e){} return f0.apply(this,arguments)}; var e0=ev; ev=function(s){try{if(/opn:|amb2|c2v2|greet|talk|bump/.test(s))window.__evlog.push(s)}catch(e){};return e0.apply(this,arguments)};}
 return JSON.stringify({id:f.id,key:f.key,crew:f.crew,kind:(C2V2.KIND||{})[f.crew]||null,d:Math.round(bd),fac:fac,peace:!!gangPeace(f),ambFoe:!!ambOkFoe(f),ctx:ambCtxOk(f),okTap:!!ambOkTap(f),alley:!!(SAVE.gsk&&SAVE.gsk.alley)})})(%s)"""
async def one(case):
    own, hot, act = case.split(':')
    async with h.Game(out='/workspace/alleycat/shots/raw') as g:
        pg = g.pg
        await pg.touchscreen.tap(195, 420)
        await pg.evaluate("WORLD_API.enter(true)"); await g.wait(1500); await g.skipall()
        await g.ev("root.FFF_NO_TUT=1")
        await pg.evaluate("WORLD_API.c2Begin(true)"); await g.wait(2500); await g.skipall(); await g.hush()
        await g.ev(r1.SETUP % {'extra': ''}); await g.go('town', 2400, 3190, 0); await g.wait(1500)
        await g.ev("SAVE.gsk=%s;1" % ("{alley:1}" if own=='1' else "{}")); await g.hush()
        print('PICK', case, await g.ev(PICK % ('true' if hot=='1' else 'false')), flush=True)
        await g.wait(300)
        if 'none' in str(await g.ev("window.__T?String(window.__T.id):'none'")): print('CASE', case, 'no target'); return
        c = await pg.evaluate("(()=>{var q=window.__ev('window.__T');var r=q.s.el.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height*0.55]})()")
        if act=='tap': await pg.touchscreen.tap(*c)
        else: await g.ev("W.run=%s; walkTo(W.ryo.x+110, W.ryo.y, true, %s); 1" % (('true','true') if act=='run' else ('false','false')))
        await g.wait(1200); await pg.screenshot(path='/workspace/alleycat/shots/raw/c2tap_%s_%s.png'%(tag,case.replace(':','_')))
        await g.wait(3500)
        print('CASE', case, await g.ev("JSON.stringify({ev:window.__evlog.filter(function(s){return !/fp:|sheet|sting|mute|hold:500|handoff/.test(s)}).slice(0,20),fight:window.__fx,on:document.getElementById('game').classList.contains('on'),dlg:!!W.dlg})"), 'ERR', g.errs[:3], flush=True)
async def main():
    for c in cases: await one(c)
asyncio.run(main())
