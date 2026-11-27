#!/workspace/pwenv/bin/python3
"""Full battle path: touch a Library foe, the card battle opens, force a win inside the battle (b.over, winner 0, endMatch),
tap through the victory pose / result screen like a player, then read the n9slam popup. MODE first|ngpcold|ngpc2"""
import asyncio, sys, json; sys.path.insert(0, '/workspace/ngptracker/tools'); import h, repro_lib as R
INDEX, MODE = sys.argv[1], sys.argv[2]; PFX = sys.argv[3] if len(sys.argv) > 3 else ''
WINB = """(function(){ var U=root.FFF_UI, ST=U&&U.ST; var b=ST&&ST.b; if(!b) return 'nob'; (b.grp||[]).forEach(function(s){ if(s) s.hp=0 }); if(b.s[1]) b.s[1].hp=0; b.over=true; b.winner=0; try{ U.endMatch() }catch(e){ return 'err '+e.message } return 'ended' })()"""
TAPS = """()=>{ var c=[...document.querySelectorAll('#vPose.on, #result.on, .wnext, button')].filter(e=>e.offsetParent!==null && (/^(#|)/.test('') ) ); 
  var vp=document.querySelector('#vPose.on'); if(vp){ var r=vp.getBoundingClientRect(); return [r.x+r.width/2, r.y+r.height*0.8, 'vpose'] }
  var b=[...document.querySelectorAll('button')].filter(e=>/^(Next|Continue|OK|Nice|Tap|Back to map|Map|Collect|Take)/i.test((e.textContent||'').trim())&&e.offsetParent!==null);
  if(b.length){ var q=b[0].getBoundingClientRect(); return [q.x+q.width/2,q.y+q.height/2,'btn:'+b[0].textContent.trim().slice(0,20)] }
  var rs=document.querySelector('#result.on'); if(rs){ var r2=rs.getBoundingClientRect(); return [r2.x+r2.width/2, r2.y+r2.height*0.85, 'result'] }
  return null }"""
async def main():
    async with h.Game(INDEX) as g:
        await R.setup(g, MODE)
        await g.ev("window.__snd.length=0; window.__evs.length=0; window.__ctxs.length=0; 1")
        await g.ev("sqStart('sq_kenta'); 1"); await g.wait(600); await g.hush()
        out = []
        for k in ['foyer', 'hall', 'peri', 'av']:
            if await g.ev("sqState('sq_kenta').kills") >= 4: break
            await g.ev("libGo('%s'); 1" % k); await g.wait(1500); await g.hush()
            for t in range(4):
                if await g.ev("sqState('sq_kenta').kills") >= 4: break
                fs = await g.ev("(W.dgF||[]).filter(function(f){return f.s&&f.s.el&&f.s.el.parentNode&&!f.stun}).map(function(f){return f.key})")
                if not fs: break
                key = fs[0]; n0 = await g.ev("window.__ctxs.length")
                for _ in range(20):
                    await g.ev("var f=(W.dgF||[]).filter(function(o){return o.key==='%s'})[0]; if(f){W.ryo.x=f.s.x+20;W.ryo.y=f.s.y;place(W.ryo,0)} 1" % key); await g.wait(150)
                    if await g.ev("window.__ctxs.length") > n0: break
                if await g.ev("window.__ctxs.length") == n0: break
                for _ in range(60):
                    await g.wait(200)
                    if await g.ev("!!(root.FFF_UI&&root.FFF_UI.ST&&root.FFF_UI.ST.inGame&&root.FFF_UI.ST.b)"): break
                await g.wait(1500)
                print(' battle', key, await g.ev(WINB), flush=True)
                slam = ''; taps = []
                for _ in range(90):
                    await g.wait(250)
                    s = await g.ev("(document.getElementById('n9slam')||{}).textContent||''")
                    if s: slam = s; break
                    c = await g.pg.evaluate(TAPS)
                    if c: taps.append(c[2]); await g.pg.touchscreen.tap(c[0], c[1])
                out.append((key, await g.ev("sqState('sq_kenta').kills"), slam, taps[:8]))
                print(' after', out[-1], flush=True)
                if PFX and slam: await g.shot(f'{PFX}_battle_slam_{len(out)}')
                await g.wait(1500); await g.adv(6); await g.hush()
        print('sounds', await g.ev("window.__snd.filter(function(s){return /qslam|roundwin|quest_ready/.test(s)})"), flush=True)
        print('evs', await g.ev("window.__evs.filter(function(s){return /slam|sq:kill|v6552|back:win|match:end/.test(s)})"), flush=True)
        print('errs', g.errs[:5], flush=True)
asyncio.run(main())
