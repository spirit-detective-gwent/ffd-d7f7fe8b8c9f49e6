#!/workspace/pwenv/bin/python3
"""Regression: escaping a Chapter 1 fight must not leave the map input-locked.

Bug (live v6.5.63): a roaming bully who was running you down (W.forced) got pulled into a Ch1 gang fight
(engage -> startPackFight does not clear W.forced). Escaping rebuilt the bullies as NEW roam objects and
returned early from back(), so W.forced kept pointing at the old object: tagsLive() false, walkTo() false,
stick dead, forever (the old safety net in ambCheck() has been a no-op since v6.5.62). A win/loss clears it
in back(); only the escape path did not.

Cases (each: start the fight, tap the real ESCAPE button, then check the map and use a vending machine):
  A) gang fight while another gang member is the forced chaser  (the reported bug)
  B) plain roaming-bully fight while a different bully is forced (that one stays on the map)
  C) a stale forced pointer injected on the map clears by itself within ~1 s (safety net)
  D) a normal WIN still returns to a working map
  E) a normal LOSS still wakes you up (nurse), no page errors
  F) ESCAPE still works and returns to the map with no rewards

usage: test_escape_lock.py <worktree> [port]
"""
import sys, json, asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import harness as H
ROOT = sys.argv[1]; PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 53811

MK = """window.__mk=function(dx,dy,id){var s=sprite((id||'bully1')+'_map',false);s.el.classList.add('foe','roam');s.x=W.ryo.x+dx;s.y=W.ryo.y+dy;place(s,0);var q={id:id||'bully1',s:s,hx:s.x,hy:s.y,path:[],wait:1,st:'wander',door:null,t:0};W.roam.push(q);return q};
window.__pack=function(n){var G={x:W.ryo.x+60,y:W.ryo.y,cap:n,mem:[],id:'t'+Math.random()};for(var i=0;i<n;i++){var q=window.__mk(70+i*20,-10+i*14,'bully'+(1+i%4));q.outGang=1;q.grp=G.id;q.grpO=G;G.mem.push(q)}return G.mem};
window.__reset=function(){W.roam.forEach(function(q){q.s.el.remove()});W.roam=[];W.foes=[];W.forced=null;W.cool=0;W.safe=0;W.ambNext=1e9;W.roamT=1e9;return 1};
window.FFF_ESC_ROLL=0; window.FFF_AMB_BAN_MS=0; 1"""
MACHINE = """(function(){var t=(W.tagL||[]).find(function(t){return t.key==='out:vm_cafe'}); if(!t) return 0; W.ryo.x=t.ax;W.ryo.y=t.ay+4;W.path=[];W.arrive=null;return 1})()"""
STATE = """(function(){var f=W.forced;return {live:tagsLive(),on:W.on,busy:W.busy,dlg:W.dlg,cut:W.cut,runUp:W.runUp,forced:f?{id:f.id,st:f.st,inRoam:W.roam.indexOf(f)>=0}:null,ig:!!FFF_UI.ST.inGame,btn:(function(){var r=document.getElementById('btnRun');return r?(r.hidden?'h':r.disabled?'d':'e'):null})(),ph:FFF_UI.ST.phase,fbusy:FFF_UI.ST.busy}})()"""
RES = []
def ok(name, cond, extra=''):
    RES.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + ((' :: ' + str(extra)[:300]) if (extra and not cond) else ''), flush=True)

async def wait_ready(pg, tries=100):
    for i in range(tries):
        await pg.wait_for_timeout(250)
        s = await H.ev(pg, STATE)
        if s.get('ig') and s.get('btn') == 'e' and s.get('ph') == 'play' and not s.get('fbusy'): return s
        await H.ev(pg, "if(window.FFF_WAVE&&document.getElementById('fwvB'))FFF_WAVE.stop()")
    return None

async def tap_escape(pg):
    c = await pg.evaluate("()=>{var r=document.getElementById('btnRun').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}")
    await pg.touchscreen.tap(*c)
    for i in range(40):
        await pg.wait_for_timeout(300)
        if not (await H.ev(pg, "FFF_UI.ST.inGame")): break

async def use_machine(pg):
    """stand at the cafeteria vending machine and tap the map there: the menu must open (W.dlg) or the tag must fire"""
    await H.ev(pg, "(function(){W.dlg=false;var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''}return 1})()")
    await H.ev(pg, MACHINE); await pg.wait_for_timeout(900)
    await H.ev(pg, "FFF_UI.ST.events=[]")
    pos = await pg.evaluate("(()=>{var b=document.querySelector('#wtags .wtag[data-k=\"out:vm_cafe\"]');if(!b)return null;var r=b.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
    if not pos: return False
    await pg.touchscreen.tap(*pos); await pg.wait_for_timeout(1000)
    r = await H.ev(pg, "({dlg:W.dlg,evs:(FFF_UI.ST.events||[]).filter(function(s){return /tag:use|vend/.test(s)}).length})")
    return bool(r.get('dlg')) or r.get('evs', 0) > 0

async def fresh(p):
    b, ctx, pg, errs = await H.boot(p, PORT)
    await H.ch1_ready(pg, 1800, 3000); await H.ev(pg, MK); await H.ev(pg, "__reset()")
    return b, pg, errs

async def case_A(p):
    b, pg, errs = await fresh(p)
    await H.ev(pg, "(function(){var m=__pack(3);W.forced=m[1];m[1].st='force';m[1].ft=0.1;engage(m[0]);return 1})()")
    rdy = await wait_ready(pg); ok('A: gang fight started, ESCAPE available', rdy, rdy)
    if rdy:
        await tap_escape(pg); await pg.wait_for_timeout(1500)
        s = await H.ev(pg, STATE)
        ok('A: back on the map after ESCAPE', not s['ig'] and s['on'], s)
        f = s['forced']
        ok('A: no stale forced chaser after ESCAPE (null, or a live roamer)', f is None or f.get('inRoam'), s)
        ok('A: map input is live (tagsLive)', s['live'], s)
        ok('A: vending machine still opens', await use_machine(pg))
        await pg.wait_for_timeout(3000)
        s2 = await H.ev(pg, STATE)
        ok('A: still unlocked 3 s later', s2['live'] or s2['busy'] or s2['dlg'] or s2['ig'] or (s2['forced'] and s2['forced']['inRoam']), s2)
    ok('A: no page errors', not errs, errs[:3]); await b.close()

async def case_B(p):
    b, pg, errs = await fresh(p)
    await H.ev(pg, "(function(){var a=__mk(70,0,'bully1'),c=__mk(260,40,'bully2');W.forced=c;c.st='force';c.ft=0.1;engage(a);return 1})()")
    rdy = await wait_ready(pg); ok('B: roam fight started, ESCAPE available', rdy, rdy)
    if rdy:
        await tap_escape(pg); await pg.wait_for_timeout(1500)
        s = await H.ev(pg, STATE)
        ok('B: map input is live after ESCAPE', s['live'], s)
        ok('B: vending machine still opens', await use_machine(pg))
    ok('B: no page errors', not errs, errs[:3]); await b.close()

async def case_C(p):
    b, pg, errs = await fresh(p)
    await H.ev(pg, "(function(){W.forced={id:'ghost',st:'force',ft:0.2,s:W.ryo};return 1})()")
    await pg.wait_for_timeout(1500)
    s = await H.ev(pg, STATE)
    ok('C: a stale forced pointer is cleared by itself', s['live'] and s['forced'] is None, s)
    ok('C: no page errors', not errs, errs[:3]); await b.close()

async def case_DEF(p):
    # D) win
    b, pg, errs = await fresh(p)
    await H.ev(pg, "(function(){var q=__mk(70,0);engage(q);return 1})()")
    rdy = await wait_ready(pg); ok('D: fight started', rdy, rdy)
    if rdy:
        await H.ev(pg, "window.FFF_VC_K=0.25")
        await H.ev(pg, "(function(){var b=FFF_UI.ST.b;(b.grp||[]).forEach(function(s){s.hp=0});if(b.s[1])b.s[1].hp=0;b.over=true;b.winner=0;FFF_UI.endMatch();return 1})()")
        s = None
        for i in range(70):
            await pg.wait_for_timeout(400)
            await H.ev(pg, "if(typeof VC!=='undefined'&&VC&&VC.tap&&!VC.over)VC.tap()")
            await pg.evaluate("(()=>{var r=document.getElementById('rMap');if(r&&document.getElementById('result').classList.contains('on'))r.click()})()")
            await H.skipall(pg, 1)
            s = await H.ev(pg, STATE)
            if s['live'] and not s['ig']: break
        ok('D: a normal WIN returns to a live map', s['live'] and not s['ig'], s)
    ok('D: no page errors', not errs, errs[:3]); await b.close()
    # E) loss
    b, pg, errs = await fresh(p)
    await H.ev(pg, "(function(){var q=__mk(70,0);engage(q);return 1})()")
    rdy = await wait_ready(pg); ok('E: fight started', rdy, rdy)
    if rdy:
        await H.ev(pg, "FFF_UI.ST.events=[]")
        await H.ev(pg, "(function(){var b=FFF_UI.ST.b;b.s[0].hp=0;b.over=true;b.winner=1;FFF_UI.endMatch();return 1})()")
        woke = False
        for i in range(60):
            await pg.wait_for_timeout(400)
            ev = await H.ev(pg, "(FFF_UI.ST.events||[]).filter(function(s){return /world:back:lose|world:wake|world:room:on:wake|world:penalty/.test(s)}).length")
            await pg.evaluate("(()=>{var r=document.getElementById('rMap');if(r&&document.getElementById('result').classList.contains('on'))r.click()})()")
            if ev: woke = True
            if woke and not await H.ev(pg, "FFF_UI.ST.inGame"): break
        ok('E: a normal LOSS goes through the wake-up path', woke)
    ok('E: no page errors', not errs, errs[:3]); await b.close()
    # F) escape basic
    b, pg, errs = await fresh(p)
    await H.ev(pg, "(function(){var q=__mk(70,0);engage(q);return 1})()")
    rdy = await wait_ready(pg)
    if rdy:
        wins0 = await H.ev(pg, "SAVE.wins|0"); await tap_escape(pg); await pg.wait_for_timeout(1200)
        s = await H.ev(pg, STATE); wins1 = await H.ev(pg, "SAVE.wins|0")
        ok('F: ESCAPE returns to the map, no win booked', (not s['ig']) and s['on'] and wins1 == wins0, [s, wins0, wins1])
    else: ok('F: fight started', False)
    await b.close()

async def main():
    H.serve(ROOT, PORT)
    async with H.async_playwright() as p:
        for c in (case_A, case_B, case_C, case_DEF):
            try: await c(p)
            except Exception as e: ok(c.__name__ + ' crashed', False, repr(e))
    n = len(RES); print(f'{sum(RES)}/{n} checks passed'); sys.exit(0 if all(RES) else 1)
asyncio.run(main())
