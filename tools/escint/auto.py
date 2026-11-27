#!/workspace/pwenv/bin/python3
"""Autoplay Ch1: walk at roaming bullies, escape every fight, flag any time the map stays locked. usage: auto.py <worktree> <port> <secs> [seed]"""
import sys, json, asyncio, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import harness as H
import os
INSTR_ON=os.environ.get('INSTR')=='1'
ROOT=sys.argv[1]; PORT=int(sys.argv[2]); SECS=int(sys.argv[3]); SEED=int(sys.argv[4]) if len(sys.argv)>4 else 1
random.seed(SEED)
ST = """(function(){var f=W.forced;return {t:+(W.t||0).toFixed(1),ig:!!FFF_UI.ST.inGame,on:W.on,live:tagsLive(),forced:f?(f.id+':'+f.st+':'+(+(f.ft||0).toFixed(1))+':'+(W.roam.indexOf(f)>=0)):null,busy:W.busy,dlg:W.dlg,cut:W.cut,runUp:W.runUp,pan:!!W.pan,paused:W.paused,fading:W.fading,lying:W.lying,scr:W.scr,ambOn:!!W.ambOn,opnOn:!!W.opnOn,snk:!!W.snk,ambT:!!W.ambT,c1eGo:W.c1eGo,dgFight:!!W.dgFight,cool:+(W.cool||0).toFixed(1),inside:W.inside&&W.inside.id,roam:W.roam.length,x:Math.round(W.ryo.x),y:Math.round(W.ryo.y),
 btn:(function(){var r=document.getElementById('btnRun');return r?(r.hidden?'h':r.disabled?'d':'e'):null})(),ph:FFF_UI.ST.phase,fbusy:FFF_UI.ST.busy,res:document.getElementById('result').classList.contains('on'),wdlg:document.getElementById('wdlg').className}})()"""
INSTR = """(function(){window.__L=[];var fv=W.forced;function lg(m){window.__L.push(Math.round(performance.now())+' '+m+' | on='+W.on+' busy='+W.busy+' ig='+FFF_UI.ST.inGame);if(window.__L.length>60)window.__L.shift()}
Object.defineProperty(W,'forced',{configurable:true,get:function(){return fv},set:function(v){var st=(new Error()).stack.split('\\n').slice(2,5).map(function(x){return x.trim().replace(/http:[^ ]*index.html:/,'L')}).join(' < ');lg('forced='+(v?(v.id+':'+v.st+' inRoam='+(W.roam.indexOf(v)>=0)):'null')+' '+st);fv=v}});
var e0=engage;engage=function(q){lg('engage '+q.id+' st='+q.st);return e0.apply(this,arguments)};
var s0=escaped;escaped=function(st){lg('escaped foes='+W.foes.length+' roam='+W.roam.length+' forced='+(fv?fv.id:null));var r=s0.apply(this,arguments);lg('escaped done roam='+W.roam.length+' forced='+(fv?fv.id+':'+fv.st+':'+(W.roam.indexOf(fv)>=0):null));return r};
var d0=dropPack;dropPack=function(q){if(q===fv)lg('dropPack of forced '+q.id);return d0.apply(this,arguments)};
var c0=crowdGone;crowdGone=function(o){if(o===fv)lg('crowdGone of forced '+o.id);return c0.apply(this,arguments)};
return 1})()"""
async def main():
    H.serve(ROOT, PORT)
    async with H.async_playwright() as p:
        b, ctx, pg, errs = await H.boot(p, PORT)
        await H.ch1_ready(pg, 1440, 3300)
        await H.ev(pg, "window.FFF_ESC_ROLL=0; SAVE.hp=MAXHP; SAVE.sp=SPMAX")
        if INSTR_ON: await H.ev(pg, INSTR)
        loop = asyncio.get_event_loop(); t0=loop.time(); nfights=0; nesc=0; lockedSince=None; lastWalk=0; log=[]
        wasFight=False
        while loop.time()-t0 < SECS:
            await pg.wait_for_timeout(400)
            s = await H.ev(pg, ST)
            if not isinstance(s, dict) or '__err' in s: print('ST err', s); continue
            if s.get('ig'):
                if not wasFight: nfights+=1; wasFight=True; fstart=loop.time()
                if s.get('btn')=='e' and s.get('ph')=='play' and not s.get('fbusy') and loop.time()-fstart>1.5:
                    c = await pg.evaluate("()=>{var r=document.getElementById('btnRun').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}")
                    await pg.touchscreen.tap(*c); nesc+=1; print(f'[{int(loop.time()-t0)}s] escape tap #{nesc}', flush=True)
                elif loop.time()-fstart>20:
                    await H.ev(pg, "(function(){var b=FFF_UI.ST.b;if(b){(b.grp||[]).forEach(function(s){s.hp=0});if(b.s[1])b.s[1].hp=0;b.over=true;b.winner=0;FFF_UI.endMatch()}})()")
                    print('   (forced win, no escape available)', flush=True); fstart=loop.time()
                if await H.ev(pg, "!!document.getElementById('fwvB')"): await H.ev(pg, "if(window.FFF_WAVE)FFF_WAVE.stop()")
                lockedSince=None; continue
            if wasFight:
                wasFight=False; print(f'[{int(loop.time()-t0)}s] back on map: '+json.dumps(s), flush=True)
            # clear dialogs / scenes by skipping
            if s.get('dlg') or s.get('cut') or s.get('scr'):
                await H.skipall(pg, 2)
            # dismiss any result screen
            if s.get('res'): await pg.evaluate("document.getElementById('rMap').click()")
            # lock detection
            if not s.get('live') and not (s.get('busy') or s.get('dlg') or s.get('cut') or s.get('runUp') or s.get('pan') or s.get('paused') or s.get('fading') or s.get('lying') or s.get('scr') or s.get('ig')) :
                lockedSince = lockedSince or loop.time()
            elif not s.get('live') and s.get('forced'):
                lockedSince = lockedSince or loop.time()
            else: lockedSince=None
            if lockedSince and loop.time()-lockedSince>8:
                print('!!! LOCKED', json.dumps(s), flush=True)
                if INSTR_ON: print('\n'.join(await H.ev(pg, 'window.__L.slice(-25)')), flush=True)
                log.append(s); lockedSince=loop.time()+30
            # walk toward a roaming bully or a random spot
            if loop.time()-lastWalk>4 and s.get('live'):
                lastWalk=loop.time()
                tgt = await H.ev(pg, "(function(){var q=W.roam.filter(function(q){return !q.ring})[0]; if(q) return [q.s.x,q.s.y]; return null})()")
                if not tgt: tgt=[random.randint(500,3500), random.randint(1500,3800)]
                await H.ev(pg, f"WORLD_API.walkToX({tgt[0]},{tgt[1]})")
            await H.ev(pg, "SAVE.hp=MAXHP")
            # keep roamers coming
            if random.random()<0.08: await H.ev(pg, "(function(){try{if(W.roam.length<4)spawnRoamer()}catch(e){}})()")
        print('DONE fights', nfights, 'escapes', nesc, 'locks', len(log), 'errs', errs[:3])
        await b.close()
asyncio.run(main())
