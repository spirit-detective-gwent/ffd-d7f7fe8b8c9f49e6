# battle-open check: the Alley Catted man must open the battle lying flat. bo.py tag ch(1|2) who(ryo|aoi) trig(tap|api)
# Ch1: my harness, dl_hall, bully1. Ch2: corners harness (read-only), c2 town street, a spawned c2_punk (FFD_INDEX picks the build).
import asyncio, sys, os, re, json
tag, ch, who, trig = sys.argv[1:5]
OUT='/workspace/alleycat/shots/raw'
SP = r"""(function(who,id,X,Y,lock){ if(who==='aoi'&&SAVE.act!=='aoi') switchChar('aoi'); if(who==='ryo'&&SAVE.act==='aoi') switchChar('ryo'); SAVE.gsk=SAVE.gsk||{}; SAVE.gsk.alley=1; W.tut=false;
 var s=intSprite(IMG[id+'_map']?id+'_map':id, SPH, 'dgfoe'); s.el.classList.add('foe'); s.x=X; s.y=Y; place(s,0); waddle(s,0,0);
 var q={key:'bo0',id:id,s:s,hx:X,hy:Y,tx:null,ty:null,wait:999,st:'walk',stun:0,fa:0,lv:playerLv()}; W.dgF=W.dgF||[]; W.dgF.push(q);
 var r=W.ryo; r.x=X-46; r.y=Y+2; r.dir=2; place(r,0); if(W.aoi){W.aoi.x=r.x-70; W.aoi.y=r.y; place(W.aoi,0);} try{camera(true)}catch(e){}
 window.__lk=setInterval(function(){ if(W.ambOn||W.opnOn||W.snk&&0||document.getElementById('game').classList.contains('on')){clearInterval(window.__lk);return} q.fa=0; q.st='walk'; q.sus=0; q.qm=0; },16);
 window.__q=q; window.__evb=[];window.__swOn=null;window.__swOff=null;window.__alT=[];(function(){var mo=new MutationObserver(function(){var sw=document.getElementById('wswirl');var t=Math.round(performance.now());if(sw&&window.__swOn==null)window.__swOn=t;if(!sw&&window.__swOn!=null&&window.__swOff==null)window.__swOff=t;});mo.observe(document.body,{childList:true});var seen=0,t0=performance.now(),iv=setInterval(function(){try{var S=root.FFF_UI&&root.FFF_UI.ST,E=S&&S.events||[];for(var i=0;i<E.length;i++){var e=E[i];if(/^match:alley:(up|down|auto|free)/.test(e)&&window.__alT.every(function(x){return x[0]!==e})){window.__alT.push([e,Math.round(performance.now())])}}}catch(e){}if(performance.now()-t0>25000){clearInterval(iv);mo.disconnect()}},5)})(); if(root.FFF_UI&&FFF_UI.ev&&!FFF_UI.__boW){var u0=FFF_UI.ev;FFF_UI.__boW=1;FFF_UI.ev=function(k){try{if(/^match:alley/.test(k))window.__evb.push(k+'@'+Math.round(performance.now()))}catch(e){};return u0.apply(this,arguments)}} var e0=ev; ev=function(k){try{if(/opn:td|amb2:(strike|fight|tap)|match:|alley/.test(k))window.__evb.push(k+'@'+Math.round(performance.now()))}catch(e){};return e0.apply(this,arguments)};
 return JSON.stringify({dbg:{tags:tagsLive(),cool:W.cool,intro:SAVE.intro,ambOn:!!W.ambOn,inside:W.inside&&W.inside.id,safe:nearSafe(W.ryo.x,W.ryo.y),bq:bossQuiet(W.ryo.x,W.ryo.y),c2:typeof c2Room==='function'?c2Room():null,xy:[W.ryo.x|0,W.ryo.y|0]},ctx:typeof ambCtxOk==='function'?ambCtxOk(q):null, inList:ambList().indexOf(q)>=0, okTap:ambOkTap(q), act:SAVE.act}); })"""
STATE = "(()=>{var k=document.querySelector('.kopose.acdown'),eF=document.getElementById('eFig'),fb=document.querySelector('#fE .fbody'),fe=document.querySelector('#fE');var kb=k&&k.getBoundingClientRect(),rb=fe&&fe.getBoundingClientRect();return JSON.stringify({sw:!!document.getElementById('wswirl'),on:document.getElementById('game').classList.contains('on'),pose:!!k,poseBox:kb?[kb.x|0,kb.y|0,kb.width|0,kb.height|0]:null,row:rb?[rb.y|0,rb.bottom|0]:null,tip:!!(eF&&eF.classList.contains('ac-down')),standOp:fb?getComputedStyle(fb).opacity:null,down:fb&&fb.closest('.fighter')?fb.closest('.fighter').dataset.down||'':'',al:(window.FFF_UI&&FFF_UI.ST&&FFF_UI.ST.events?FFF_UI.ST.events.filter(function(e){return /^match:alley:(up|down|auto)/.test(e)}):[])})})()"
async def run(pg, evf, errs):
    print('SPAWN', await evf("(%s)('%s',%s,%s,%s,1)" % (SP, who, "'bully1'" if ch=='1' else "'c2_punk'", '420' if ch=='1' else 'W.ryo.x+60', '520' if ch=='1' else 'W.ryo.y')), flush=True)
    await pg.wait_for_timeout(250)
    if trig == 'tap':
        c = await pg.evaluate("(()=>{var q=window.__ev('window.__q');var r=q.s.el.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height*0.55]})()")
        await pg.touchscreen.tap(*c)
    else:
        await evf("(function(){var q=window.__q; if(!(root.FFF_OPN_SNEAK&&FFF_OPN_SNEAK.hold(q))) opnTD(q); return 1})()")
    seen = False; t = 0; swst = None; swt = None
    while t < 15000:
        st = json.loads(await pg.evaluate(STATE))
        if st['sw']: seen = True; swst = st
        if seen and not st['sw'] and st['on']: swt = await pg.evaluate("Math.round(performance.now())"); break
        await pg.wait_for_timeout(30); t += 30
    shots = []
    for ms in (0, 300, 1000, 2000):
        if ms: await pg.wait_for_timeout(ms - shots[-1][0])
        fn = '%s/bo_%s_ch%s_%s_%dms.png' % (OUT, tag, ch, who, ms); await pg.screenshot(path=fn)
        shots.append((ms, fn, await pg.evaluate(STATE)))
    print('SWIRL_SEEN', seen, 'wait_ms', t)
    print('LAST_SWIRL_FRAME', json.dumps(swst))
    for s in shots: print('AT', s[0], s[2])
    evs = json.loads(await evf("JSON.stringify(window.__evb)"))
    pr = json.loads(await evf("JSON.stringify({on:window.__swOn,off:window.__swOff,al:window.__alT})"))
    print('PROBE', json.dumps(pr))
    up = [e for e,t in pr['al'] if e.startswith('match:alley:up:')]
    upt = [t for e,t in pr['al'] if e.startswith('match:alley:up:')]
    upms = (upt[0] - pr['off']) if (upt and pr['off']) else None
    print('SWIRL_FRAME_ALLEY_EV', (swst or {}).get('al'))
    flat = bool(swst and swst.get('pose') or swst and swst.get('tip'))
    s1 = json.loads(shots[2][2]); stood = (not s1['pose']) and (not s1['tip']) and str(s1['standOp']) in ('1', '1.0')
    print('T527 flat_at_swirl=%s up=%s up_ms_after_swirl=%s standing_by_1s=%s => %s' % (flat, up[0].split('@')[0] if up else None, upms, stood, 'PASS' if (flat and stood and up and up[0].startswith('match:alley:up:start')) else 'FAIL'))
    print('EV', json.dumps(evs[:40]))
    print('ERR', errs[:3], flush=True)
async def main():
    if ch == '1':
        sys.path.insert(0, '/workspace/alleycat/tools'); import h as H
        port = int(os.environ.get('PORT', '8801')); root = os.environ.get('ROOT', '/workspace/alleycat/wt')
        async with H.async_playwright() as p:
            errs=[]; b,ctx,pg = await H.newpage(p, port, root, errs, save=json.load(open('/workspace/alleycat/tools/save_c1.json')))
            await pg.reload(); await pg.wait_for_timeout(2500); await H.boot(pg, cont=True)
            evf = lambda c: H.ev(pg, c)
            await evf("SAVE.intro=1;SAVE.ngp=1;W.tut=false;clearRoam();W.spawnT=1e12;1"); await evf("intGo('dl_hall');1"); await pg.wait_for_timeout(2500); await evf(H.HUSH)
            await run(pg, evf, errs); await b.close()
    else:
        sys.path.insert(0, '/workspace/corners'); import h, r1
        async with h.Game(out=OUT) as g:
            pg = g.pg
            await pg.touchscreen.tap(195, 420); await pg.evaluate("WORLD_API.enter(true)"); await g.wait(1500); await g.skipall()
            await g.ev("root.FFF_NO_TUT=1"); await pg.evaluate("WORLD_API.c2Begin(true)"); await g.wait(2500); await g.skipall(); await g.hush()
            await g.ev(r1.SETUP % {'extra': ''}); await g.go('town', int(os.environ.get('CX','2400')), int(os.environ.get('CY','3190')), 0); await g.wait(3000); await g.hush()
            if os.environ.get('ROOM'):
                await g.ev("(function(k){W.dlg=false;W.cut=false;W.busy=false;intGo(k);return 1})('%s')" % os.environ['ROOM']); await g.wait(3500); await g.hush()
                print('ROOMFOES', await g.ev("JSON.stringify((W.dgF||[]).map(function(f){return [f.id,f.key,f.s?Math.round(f.s.x):0,f.s?Math.round(f.s.y):0,ambOkTap(f)]}).slice(0,12))"))
            await run(pg, g.ev, g.errs)
asyncio.run(main())
