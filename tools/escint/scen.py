#!/workspace/pwenv/bin/python3
"""Run escape scenarios and print the world state after each. usage: scen.py <worktree> [port] [names,...]"""
import sys, json, asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import harness as H
ROOT = sys.argv[1]; PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 53713
ONLY = sys.argv[3].split(',') if len(sys.argv) > 3 else None

MK = """window.__mk=function(dx,dy,id,grp){var s=sprite((id||'bully1')+'_map',false);s.el.classList.add('foe','roam');s.x=W.ryo.x+dx;s.y=W.ryo.y+dy;place(s,0);var q={id:id||'bully1',s:s,hx:s.x,hy:s.y,path:[],wait:1,st:'wander',door:null,t:0};W.roam.push(q);return q};
window.__pack=function(n){var G={x:W.ryo.x+60,y:W.ryo.y,cap:n,mem:[],id:'t'+Math.random()};for(var i=0;i<n;i++){var q=window.__mk(70+i*20,-10+i*14,'bully'+(1+i%4));q.outGang=1;q.grp=G.id;q.grpO=G;G.mem.push(q)}return G.mem};
window.__reset=function(){W.roam.forEach(function(q){q.s.el.remove()});W.roam=[];W.foes=[];W.cool=0;W.safe=0;W.ambNext=1e9;return 1};
window.__reset(); 1"""

SCEN = {
 'roam_engage': "(function(){var q=__mk(70,0);engage(q);return 1})()",
 'amb_back': "(function(){var q=__mk(90,0);ambStrike(q,'tap','back');return 1})()",
 'amb_front': "(function(){var q=__mk(90,0);ambStrike(q,'tap','front');return 1})()",
 'pack_gang': "(function(){var m=__pack(3);g38PackFight(m[0]);return 1})()",
 'pack_5_waves': "(function(){var m=__pack(5);g38PackFight(m[0]);return 1})()",
 'vend_guard': "(function(){var q=__mk(70,0);encounter({id:'vm_cafe',vend:1,n:'cafeteria vending machine',x:W.ryo.x+60,y:W.ryo.y,roam:[q],exact:1},1);return 1})()",
 'mini': "(function(){fight(['bully1'],false,{mini:'mb_cafe',flv:3});return 1})()",
 'gouki': "(function(){fight(['gouki'],true,{});return 1})()",
 'plain_fightX': "(function(){fight(['bully1','bully2'],false,{flv:1});return 1})()",
}

FLAGS = """(function(){var o={};['on','runUp','busy','dlg','pan','cut','scr','forced','paused','fading','lying','cool','ambT','ambOn','opnOn','dgFight','g5busy','g38Gating','c2busy','waveGo','fightT'].forEach(function(k){var v=W[k];o[k]=(v&&typeof v==='object')?'obj':v});
 o.tagsLive=tagsLive(); o.nroam=W.roam.length; o.nfoes=W.foes.length;
 o.game=document.getElementById('game').className; o.stInGame=FFF_UI.ST.inGame; o.stInWorld=FFF_UI.ST.inWorld;
 return o})()"""

PROBE = """(function(){var t=(W.tagL||[]).find(function(t){return t.key==='out:vm_cafe'}); if(!t) return {err:'no tag'};
 W.ryo.x=t.ax;W.ryo.y=t.ay+4;W.path=[];W.arrive=null; return {ok:1}})()"""

async def can_interact(pg):
    """put Ryo at the cafeteria vending machine, then check (1) tag button hit-test, (2) a real tap on it opens the machine / sets a lock"""
    await H.ev(pg, PROBE); await pg.wait_for_timeout(700)
    pre = await H.ev(pg, "({live:tagsLive(),near:(tagNear()||{}).key||null,dlg:W.dlg,busy:W.busy})")
    for _ in range(12):
        hit = await pg.evaluate("""()=>{var b=document.querySelector('#wtags .wtag[data-k="out:vm_cafe"]');if(!b)return {nobtn:1};var r=b.getBoundingClientRect();var x=r.x+r.width/2,y=r.y+r.height/2;var e=document.elementFromPoint(x,y);return {x:x,y:y,w:r.width,onbtn:!!(e&&e.closest&&e.closest('.wtag')),top:e&&(e.id||e.className||e.tagName)}}""")
        if hit.get('w'): break
        await pg.wait_for_timeout(250)
    await H.ev(pg, "FFF_UI.ST.events=[]")
    if hit.get('x') is not None:
        await pg.touchscreen.tap(hit['x'], hit['y'])
    await pg.wait_for_timeout(800)
    post = await H.ev(pg, "({dlg:W.dlg,busy:W.busy,evs:(FFF_UI.ST.events||[]).filter(function(s){return /tag|vend|vm/.test(s)}).slice(-6),wdlg:document.getElementById('wdlg').className})")
    used = bool(post.get('dlg')) or any('tag:use' in s or 'vend' in s for s in post.get('evs', []))
    return {'pre': pre, 'hit': hit, 'post': post, 'ok': used}

async def run_one(p, name, code, mode='escape'):
    b, ctx, pg, errs = await H.boot(p, PORT)
    await H.ch1_ready(pg, 1800, 3000)
    await H.ev(pg, MK)
    await H.ev(pg, "window.FFF_ESC_ROLL=0; window.FFF_AMB_BAN_MS=0")
    base = await can_interact(pg)
    print(f'[{name}] baseline interact ok={base["ok"]} hit={base["hit"]}', flush=True)
    await H.ch1_ready(pg, 1800, 3000); await H.ev(pg, "__reset()")
    await H.ev(pg, code)
    # wait for the fight board with Escape available
    ready = None
    for i in range(80):
        await pg.wait_for_timeout(250)
        s = await H.ev(pg, "(function(){var r=document.getElementById('btnRun');var wv=document.getElementById('fwvB');return {ig:FFF_UI.ST.inGame,busy:FFF_UI.ST.busy,ph:FFF_UI.ST.phase,hid:r&&r.hidden,dis:r&&r.disabled,ban:!!wv}})()")
        if s.get('ig') and not s.get('hid') and not s.get('dis') and s.get('ph') == 'play' and not s.get('busy'):
            ready = s; break
        if s.get('ban'): await H.ev(pg, "if(window.FFF_WAVE)FFF_WAVE.stop()")
    if not ready:
        print(f'[{name}] FIGHT NEVER READY', json.dumps(s)); await b.close(); return None
    await pg.wait_for_timeout(1200)
    if mode == 'escape':
        c = await pg.evaluate("()=>{var r=document.getElementById('btnRun').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}")
        await pg.touchscreen.tap(*c)
        for i in range(30):
            await pg.wait_for_timeout(300)
            if not (await H.ev(pg, "FFF_UI.ST.inGame")): break
    await pg.wait_for_timeout(2500)
    fl = await H.ev(pg, FLAGS)
    res = await can_interact(pg)
    print(f'[{name}] after {mode}: interact ok={res["ok"]}  flags={json.dumps(fl)}', flush=True)
    if not res['ok']: print('   detail', json.dumps(res))
    print('   errs', errs[:3]); 
    await b.close(); return res['ok']

async def main():
    H.serve(ROOT, PORT)
    async with H.async_playwright() as p:
        out = {}
        for n, code in SCEN.items():
            if ONLY and n not in ONLY: continue
            out[n] = await run_one(p, n, code)
        print('SUMMARY', json.dumps(out))
if __name__ == "__main__": asyncio.run(main())
