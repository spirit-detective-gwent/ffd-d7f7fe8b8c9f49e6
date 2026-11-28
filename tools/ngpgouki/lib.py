import sys, json; sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent)); import h
CLEARED = r"""(function(){ var S=SAVE; STORY.ensure(S); S.intro=1; S.ch1=1; S.gouki=1; S.dbl=1; S.mb={mb_lib:1,mb_art:1,mb_cafe:1,mb_field:1,gouki:1}; S.sc=S.sc||{}; S.sc.nurse=1; S.sc.ending=1; S.wins=30;
  S.bond=S.bond||{}; S.bond.path='fierce'; S.bond.lock=1; S.bond.px=2000; save(); return 1})()"""
CH1 = r"""(function(){ var S=SAVE; S.intro=1; S.sc=S.sc||{}; S.sc.nurse=1; S.sc.after=1; S.mb=S.mb||{}; ['mb_lib','mb_art','mb_cafe','mb_field'].forEach(function(k){S.mb[k]=1}); S.bond=S.bond||{}; if(!S.bond.path){S.bond.path='fierce';S.bond.lock=1;}
  if(STORY&&STORY.bond){ var B=STORY.bond(S); B.picks=B.picks||{}; B.picks.dg_gouki=B.picks.dg_gouki||'fierce'; }
  W.dlg=false; W.paused=false; save(); if(typeof syncMinis==='function') syncMinis(); return 1})()"""
ST = r"""JSON.stringify({ngp:SAVE.ngp|0,ch1:SAVE.ch1|0,gouki:SAVE.gouki|0,gkPh:SAVE.gkPh,gkRev:SAVE.gkRevives|0,chapter:SAVE.chapter|0,end:!!(SAVE.sc&&SAVE.sc.ending),in:W.inside&&W.inside.id,
  dbl:SAVE.dbl|0,gym:JSON.stringify(gymS()), walkIn:gymWalkIn(), door:gkDoorNeed()})"""
KILLOPEN = r"""(function(){ try{ if(typeof unstage==='function') unstage() }catch(e){} try{ if(typeof scKill==='function') scKill() }catch(e){} W.scGen=(W.scGen|0)+1; SAVE.intro=1; W.dlg=false; W.busy=false; W.cut=false;
  document.querySelectorAll('#wintro,.cintro,#cintro,.charintro').forEach(function(e){ e.remove() }); var d=document.getElementById('wdlg'); if(d){d.className='';d.innerHTML=''}; return 1})()"""
def js(s): return json.loads(s) if isinstance(s, str) else s
TAGS = r"""JSON.stringify((function(){ var t=[]; try{ t=tagDefs().map(function(x){return x.key+'='+x.lab}) }catch(e){ t=['ERR '+e.message] } return t})())"""
GYMFRONT = "(function(){var p=PLACES.filter(function(q){return q.boss})[0]; W.ryo.x=p.x; W.ryo.y=p.y+70; W.aoi.x=p.x+40; W.aoi.y=p.y+90; resetTrail(W.ryo.x,W.ryo.y,0); W.ryo.dir=0; camera(true); place(W.ryo,0); place(W.aoi,0); syncMinis(); return 1})()"
INB = "!!(root.FFF_UI&&root.FFF_UI.ST&&root.FFF_UI.ST.inGame&&root.FFF_UI.ST.b)"
END = """(function(win){ var U=root.FFF_UI, ST=U&&U.ST; var b=ST&&ST.b; if(!b) return 'nob'; if(win){ (b.grp||[]).forEach(function(s){ if(s) s.hp=0 }); if(b.s[1]) b.s[1].hp=0; b.winner=0; } else { if(b.s[0]) b.s[0].hp=0; b.winner=1; } b.over=true; try{ U.endMatch() }catch(e){ return 'err '+e.message } return 'ended' })"""
TAPS = r"""()=>{ var vp=document.querySelector('#vPose.on'); if(vp){ var r=vp.getBoundingClientRect(); return [r.x+r.width/2, r.y+r.height*0.8, 'vpose'] }
  var vis=e=>{var r=e.getBoundingClientRect(); var cs=getComputedStyle(e); return r.width>0&&r.height>0&&cs.visibility!=='hidden'&&cs.pointerEvents!=='none'};
  var gb=[...document.querySelectorAll('#gfind.on button')].filter(vis); if(gb.length){ var q0=gb[0].getBoundingClientRect(); return [q0.x+q0.width/2,q0.y+q0.height/2,'gfind:'+gb[0].textContent.trim().slice(0,20)] }
  var b=[...document.querySelectorAll('button')].filter(e=>/^(Next|Skip|Continue|OK|Nice|Tap|Back to map|Map|Collect|Take|Wake|Equip|Got it|Keep|Let|▸ Let)/i.test((e.textContent||'').trim())&&vis(e)&&!e.closest('#wchap'));
  if(b.length){ var q=b[0].getBoundingClientRect(); return [q.x+q.width/2,q.y+q.height/2,'btn:'+b[0].textContent.trim().slice(0,20)] }
  var rs=document.querySelector('#result.on'); if(rs){ var r2=rs.getBoundingClientRect(); return [r2.x+r2.width/2, r2.y+r2.height*0.85, 'result'] }
  var gf=document.querySelector('#gfind.on'); if(gf){ var r3=gf.getBoundingClientRect(); return [r3.x+r3.width/2, r3.y+r3.height*0.9, 'gfind'] }
  var db=[...document.querySelectorAll('#wdlg.on button, .tut button, [class*=tip] button, [class*=coach] button')].filter(e=>vis(e)&&!/^(Walk away|Leave|Back out|Auto)/.test((e.textContent||'').trim())); if(db.length){ var hb=db.filter(e=>e.classList.contains('hot'))[0]||db[0]; var q5=hb.getBoundingClientRect(); return [q5.x+q5.width/2,q5.y+q5.height/2,'dbtn:'+hb.textContent.trim().slice(0,20)] }
  var lg=[...document.querySelectorAll('div,a,span')].filter(e=>/^\W*Let.s go\W*$/.test((e.textContent||'').trim())&&vis(e)); if(lg.length){ var q6=lg[lg.length-1].getBoundingClientRect(); return [q6.x+q6.width/2,q6.y+q6.height/2,'letsgo'] }
  var d=document.querySelector('#wdlg.on'); if(d){ var r4=d.getBoundingClientRect(); return [r4.x+r4.width/2, r4.y+r4.height*0.5, 'dlg'] }
  return null }"""
async def setup(g, mode):
    await g.boot()
    if mode == 'ngp':
        await g.ev(CLEARED); await g.pg.reload(); await g.wait(2500); await g.boot()
        await g.ev("v640NgStart(v640NgBase()); 1"); await g.wait(2500); await g.skipall(); await g.hush(); await g.ev("root.FFF_NO_TUT=1"); await g.hush(); await g.ev(h.HOOK)
        await g.ev(KILLOPEN); await g.wait(1500); await g.skipall(); await g.ev(KILLOPEN); await g.hush()
    await g.ev(CH1)
    return js(await g.ev(ST))
async def outside_tags(g):
    await g.ev(GYMFRONT); await g.wait(1200)
    return js(await g.ev(TAGS))
async def to_arena(g):
    await g.ev("gymEnter(); 1"); await g.wait(2500); await g.adv(30); await g.hush()
    foyer = js(await g.ev(ST))
    await g.ev("(function(){var S=gymS(); GYM_SEALS.forEach(function(k){S.sl[k]=1}); S.e.press=1; save(); gymGo('arena'); return 1})()"); await g.wait(2500); await g.adv(20); await g.hush()
    return foyer, js(await g.ev(ST))
async def finale(g, max_battles=8, log=print):
    """walk into Gouki on the Main Court, then win every battle except the item-revival loop (lose that one, as a real player does),
    tapping through scenes, until the Chapter One card. Returns (ctxs, state, chapter-card-shown)."""
    await g.ev("window.__ctxs=[]; window.__evs=[]; (function(){var gg=W.gymGouki; if(gg){W.ryo.x=gg.x; W.ryo.y=gg.y+260; place(W.ryo,0); camera(true);} W.gymBossBusy=0; W.cool=0; gymBoss(); return 1})()")
    taps = []
    nb = 0; card = False
    for step in range(400):
        await g.wait(250)
        if await g.ev("!!document.getElementById('wchap')"): card = True; break
        n = await g.ev("window.__ctxs.length")
        if n > nb and await g.ev(INB):
            await g.wait(1200); ctx = (await g.ev("JSON.stringify(window.__ctxs[window.__ctxs.length-1])"))
            c = js(ctx).get('ctx') or {}; win = not c.get('gkLoop')
            r = await g.pg.evaluate("(w)=>window.__ev('(' + " + json.dumps(END) + " + ')(' + w + ')')", 'true' if win else 'false')
            log(' battle', nb + 1, ctx, 'win' if win else 'lose', r); nb = n
            if nb >= max_battles: break
            continue
        c = await g.pg.evaluate(TAPS)
        if c: taps.append(c[2]); await g.pg.touchscreen.tap(c[0], c[1])
        if step == 12 and not nb: log(' early evs', await g.ev("window.__evs.slice(0,30)"), await g.ev("JSON.stringify({busy:W.gymBossBusy,pend:!!W.libPend,dlg:W.dlg,cut:W.cut,live:tagsLive(),room:gymRoom(),open:gymOpen()})"))
    log(' taps', taps[-25:])
    st = js(await g.ev(ST)); ctxs = js(await g.ev("JSON.stringify(window.__ctxs)"))
    return ctxs, st, card
async def to_ch2(g):
    ok = await g.ev("(function(){var b=document.querySelector('#wchap button[data-c=\"c2\"]'); if(!b) return false; b.click(); return true})()")
    await g.wait(4000); await g.skipall(10); await g.wait(1500); await g.skipall(10)
    return ok, js(await g.ev("JSON.stringify({chapter:SAVE.chapter|0,c2:c2On(),ch1:SAVE.ch1|0,ngp:SAVE.ngp|0,room:W.inside&&W.inside.id})"))
