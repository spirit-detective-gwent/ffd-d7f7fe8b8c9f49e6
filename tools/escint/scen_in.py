#!/workspace/pwenv/bin/python3
"""Indoor (Ch1 building) escape scenarios. usage: scen_in.py <worktree> <port> [names]"""
import sys, json, asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import harness as H
ROOT=sys.argv[1]; PORT=int(sys.argv[2]); ONLY=sys.argv[3].split(',') if len(sys.argv)>3 else None
SC = {
 'cafe_hall': ("dh_cafe", "dgPop()", "(function(){var f=W.dgF[0];W.ryo.x=f.s.x-30;W.ryo.y=f.s.y;return 1})()", 'dh_cafe:vsoda'),
 'lib_hall': ("dl_hall", "dgPop()", "(function(){var f=W.dgF[0];W.ryo.x=f.s.x-30;W.ryo.y=f.s.y;return 1})()", None),
 'field_hall': ("dh_field", "dgPop()", "(function(){var f=W.dgF[0];W.ryo.x=f.s.x-30;W.ryo.y=f.s.y;return 1})()", None),
 'art_hall': ("dh_art", "dgPop()", "(function(){var f=W.dgF[0];W.ryo.x=f.s.x-30;W.ryo.y=f.s.y;return 1})()", None),
}
async def probe(pg, key):
    """returns dict: interact worked? uses the tag button list: Ryo placed at tag, then a real tap on the screen at the tag button"""
    await H.ev(pg, f"(function(){{var t=(W.tagL||[]).find(function(t){{return t.key==='{key}'}});if(!t)return 0;W.ryo.x=t.ax;W.ryo.y=t.ay+4;W.path=[];W.arrive=null;return 1}})()")
    await pg.wait_for_timeout(700)
    live = await H.ev(pg, "({live:tagsLive(),near:(tagNear()||{}).key||null})")
    hit = None
    for _ in range(12):
        hit = await pg.evaluate("(k)=>{var b=document.querySelector('#wtags .wtag[data-k=\"'+k+'\"]');if(!b)return {nobtn:1};var r=b.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2,w:r.width}}", key)
        if hit.get('w'): break
        await pg.wait_for_timeout(250)
    await H.ev(pg, "FFF_UI.ST.events=[]")
    if hit.get('w'): await pg.touchscreen.tap(hit['x'], hit['y'])
    await pg.wait_for_timeout(900)
    post = await H.ev(pg, "({dlg:W.dlg,evs:(FFF_UI.ST.events||[]).filter(function(s){return /tag|vend|vm|dg:vend/.test(s)}).slice(-5)})")
    return {'live': live, 'hit': hit, 'post': post, 'ok': bool(post.get('dlg')) or bool(post.get('evs'))}
async def run(p, name):
    room, pop, touch, key = SC[name]
    b, ctx, pg, errs = await H.boot(p, PORT)
    await H.ch1_ready(pg, 1800, 3000); await H.ev(pg, "window.FFF_ESC_ROLL=0")
    await H.ev(pg, f"intGo('{room}',{{}})"); await pg.wait_for_timeout(3000)
    await H.ev(pg, pop); await pg.wait_for_timeout(500)
    print(f'[{name}] in={await H.ev(pg,"W.inside&&W.inside.id")} foes={await H.ev(pg,"(W.dgF||[]).length")} tags={await H.ev(pg,"(W.tagL||[]).map(function(t){return t.key})")}', flush=True)
    if key is None:
        key = await H.ev(pg, "((W.tagL||[]).find(function(t){return /vsoda|vfood|vend/.test(t.key)})||(W.tagL||[])[0]||{}).key")
    base = await probe(pg, key); print(f'[{name}] baseline probe {key}: ok={base["ok"]}', flush=True)
    await H.ev(pg, "(function(){var f=W.dgF[0],I=W.inside,D=INT[I.id];W.ryo.x=f.s.x-30;W.ryo.y=f.s.y;W.dgFight=f;W.path=[];W.ryo.v=0;W.fLv=grpLv([f]);fight([f.id],false,{dg:D.dg,dgk:f.key,dgks:[f.key],dgm:I.id});return 1})()")
    ready=None
    for i in range(100):
        await pg.wait_for_timeout(250)
        s = await H.ev(pg, "(function(){var r=document.getElementById('btnRun');return {ig:FFF_UI.ST.inGame,busy:FFF_UI.ST.busy,ph:FFF_UI.ST.phase,hid:r&&r.hidden,dis:r&&r.disabled}})()")
        if s.get('ig') and not s.get('hid') and not s.get('dis') and s.get('ph')=='play' and not s.get('busy'): ready=s; break
        await H.ev(pg, "if(window.FFF_WAVE&&document.getElementById('fwvB'))FFF_WAVE.stop()")
    if not ready: print(f'[{name}] FIGHT NEVER READY', s); await b.close(); return None
    await pg.wait_for_timeout(1200)
    c = await pg.evaluate("()=>{var r=document.getElementById('btnRun').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}")
    await pg.touchscreen.tap(*c)
    for i in range(30):
        await pg.wait_for_timeout(300)
        if not (await H.ev(pg, "FFF_UI.ST.inGame")): break
    await pg.wait_for_timeout(2500)
    fl = await H.ev(pg, "(function(){var o={};['on','runUp','busy','dlg','pan','cut','scr','forced','paused','fading','lying','dgFight','ambOn','opnOn','snk'].forEach(function(k){var v=W[k];o[k]=(v&&typeof v==='object')?'obj':v});o.live=tagsLive();o.in=W.inside&&W.inside.id;return o})()")
    res = await probe(pg, key)
    print(f'[{name}] after escape probe ok={res["ok"]} flags={json.dumps(fl)}', flush=True)
    if not res['ok']: print('   detail', json.dumps(res))
    print('   errs', errs[:3]); await b.close(); return res['ok']
async def main():
    H.serve(ROOT, PORT)
    async with H.async_playwright() as p:
        out={}
        for n in SC:
            if ONLY and n not in ONLY: continue
            out[n]=await run(p,n)
        print('SUMMARY', json.dumps(out))
if __name__=='__main__': asyncio.run(main())
