#!/workspace/pwenv/bin/python3
"""v6566-ofuda tests. usage: test_ofuda.py <tree> [port] [only]
 P: Gouki finale on Fierce + Strategic, fresh + NG+: phase 1 KO -> revive loop -> Bond -> Double (gkFin) -> win; no Ofuda popup in the gym.
 C: held Ofuda shows exactly once at the first Ch2 free walk (after the arrival cine), not during it.
 R: reload before it shows -> shows once after reload; reload after -> never again.
 O: old saves that own it never get it again (hold / wait / Gouki rematch); NG+ hide clears a stale hold."""
import sys, asyncio, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'escint')); import harness as H
ROOT = sys.argv[1]; PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 52911; ONLY = sys.argv[3] if len(sys.argv) > 3 else ''
SHOTS = Path('/workspace/ofuda/shots'); SHOTS.mkdir(parents=True, exist_ok=True)
TAG = 'live' if 'live' in ROOT else 'branch'
RES = []
def ok(name, cond, extra=''):
    RES.append((bool(cond), name)); print(('PASS ' if cond else 'FAIL ') + name + ((' :: ' + str(extra)[:300]) if extra and not cond else ''), flush=True)
SET = """(function(a){var B=STORY.bond(SAVE);B.path=a.path;B.picks=B.picks||{};B.picks.dg_gouki=a.path;var l=0;while(STORY.bondLv(SAVE)<5&&l<400){B.px=(B.px|0)+50;l++}
SAVE.gouki=0;SAVE.ch1=0;SAVE.gkPh=0;SAVE.gkRevives=0;SAVE.gkPhp=null;SAVE.gkPsp=null;SAVE.dbl=0;SAVE.ngp=a.ngp;SAVE.sc=SAVE.sc||{};delete SAVE.sc.ending;var g=gearS();delete g.own.ofuda;delete g.ofudaHold;delete g.ofudaWait;
if(a.lamp){g.own.lampglass=1;g.eq.ryo=g.eq.ryo||{};g.eq.ryo.acc='lampglass'}save();return {lv:STORY.bondLv(SAVE),gate:gearGate('ofuda'),dbl:dblUnlocked()}})"""
WIN = "(function(){var b=FFF_UI.ST.b;(b.grp||[]).forEach(function(s){s.hp=0});if(b.s[1])b.s[1].hp=0;b.over=true;b.winner=0;FFF_UI.endMatch();return 1})()"
LOSE = "(function(){var b=FFF_UI.ST.b;b.s[0].hp=0;b.over=true;b.winner=1;FFF_UI.endMatch();return 1})()"
INPLAY = "!!(FFF_UI.ST.inGame&&FFF_UI.ST.b&&!FFF_UI.ST.b.over&&FFF_UI.ST.phase==='play')"
CTX = "JSON.stringify(FFF_UI.ST.story&&FFF_UI.ST.story.ctx||null)"
EVS = "FFF_UI.ST.events.slice()"
ADV = """()=>{var d=document.getElementById('wdlg');if(!d||!d.classList.contains('on'))return 0;var b=[...d.querySelectorAll('button')].find(x=>/^\\W*(Next|OK|Nice|Continue|Got it|Let)/.test((x.textContent||'').trim())&&x.offsetParent);if(b){b.click();return 1}return 0}"""
async def adv(pg, n=3):
    for i in range(n):
        if not await pg.evaluate(ADV): break
        await pg.wait_for_timeout(200)
    await H.skipall(pg, 2)
async def wait_play(pg, secs=40, skip=True):
    for i in range(int(secs * 2)):
        if await H.ev(pg, INPLAY): return True
        if skip: await adv(pg)
        await pg.wait_for_timeout(500)
    return False
async def drive(pg, secs, skip=True):
    for i in range(int(secs * 2)):
        if skip: await adv(pg)
        r = await pg.evaluate("()=>{var e=document.getElementById('rMap');if(e&&document.getElementById('result').classList.contains('on')&&e.offsetParent){e.click();return 1}return 0}")
        await pg.wait_for_timeout(500)
async def gfind_count(pg):
    return len([e for e in await H.ev(pg, EVS) if e.startswith('world:gfind:show:ofuda')])
async def finale(p, path, ngp):
    nm = f'{path}/{"ngp" if ngp else "fresh"}'
    b, ctx, pg, errs = await H.boot(p, PORT)
    await H.ch1_ready(pg, 1440, 3300)
    s = await H.ev(pg, SET + "(" + json.dumps({'path': path, 'ngp': 1 if ngp else 0, 'lamp': 1}) + ")")
    await H.ev(pg, "FFF_UI.ST.events.length=0;root.FFF_NO_VC=1;gkFight();1")
    ok(f'{nm}: phase 1 fight starts', await wait_play(pg), await H.ev(pg, CTX))
    c1 = await H.ev(pg, CTX); ok(f'{nm}: first fight is phase 1 (not a one-round rematch)', '"gkPhase":1' in (c1 or ''), c1)
    await H.ev(pg, WIN)
    ok(f'{nm}: after the first KO Gouki revives into the endurance round', await wait_play(pg, 60), await H.ev(pg, "({ctx:" + CTX + ",ph:SAVE.gkPh,rev:SAVE.gkRevives})"))
    c2 = await H.ev(pg, CTX); ok(f'{nm}: round 2 is gkLoop', '"gkLoop":1' in (c2 or ''), c2)
    ok(f'{nm}: no Ofuda popup after the first KO', await gfind_count(pg) == 0 and not await H.ev(pg, "!!gearS().own.ofuda"))
    await H.ev(pg, LOSE)
    ok(f'{nm}: Bond awakening -> the Double fight (gkFin)', await wait_play(pg, 60), await H.ev(pg, "({ctx:" + CTX + ",dbl:SAVE.dbl})"))
    c3 = await H.ev(pg, CTX); ok(f'{nm}: final fight ctx gkFin, SAVE.dbl=1', '"gkFin":1' in (c3 or '') and await H.ev(pg, "SAVE.dbl") == 1, c3)
    evs = await H.ev(pg, EVS); ok(f'{nm}: world:dbl:unlock:finale fired', 'world:dbl:unlock:finale' in evs)
    # play the Double
    await pg.evaluate("""()=>{var F=FFF_UI.ST,b=F.b;b.turn=0;F.busy=false;F.phase='play';b.s[0].spirit=40;if(b.bench)b.bench.spirit=40;b.s[1].hp=b.s[1].max=999;if(FFF_UI.render)FFF_UI.render()}""")
    await pg.wait_for_timeout(600)
    db = await pg.evaluate("()=>{var e=document.getElementById('btnDbl');if(!e)return null;var r=e.getBoundingClientRect();return {vis:!!e.offsetParent&&!e.hidden,dis:!!e.disabled,x:r.x+r.width/2,y:r.y+r.height/2}}")
    ok(f'{nm}: Double button is up in the final fight', isinstance(db, dict) and db.get('vis') and not db.get('dis'), db)
    if isinstance(db, dict) and db.get('vis'):
        n0 = len(await H.ev(pg, EVS)); await pg.touchscreen.tap(db['x'], db['y']); await pg.wait_for_timeout(1400)
        if ngp is False and path == 'fierce': await pg.screenshot(path=str(SHOTS / f'{TAG}_phase2_double_{path}.png'))
        await pg.wait_for_timeout(1200)
        d_ev = [e for e in (await H.ev(pg, EVS))[n0:] if 'dbl' in e.lower() or 'double' in e.lower()]
        ok(f'{nm}: the Double plays', len(d_ev) > 0, (await H.ev(pg, EVS))[n0:n0 + 20])
    await pg.wait_for_timeout(2500)
    if await H.ev(pg, "!!(FFF_UI.ST.inGame&&FFF_UI.ST.b&&!FFF_UI.ST.b.over)"): await H.ev(pg, WIN)
    await drive(pg, 10)
    g = await H.ev(pg, "({hold:gearS().ofudaHold|0,wait:gearS().ofudaWait|0,own:!!gearS().own.ofuda,gouki:SAVE.gouki,ch:SAVE.chapter})")
    ok(f'{nm}: no Ofuda popup in the gym after the final win', await gfind_count(pg) == 0, g)
    if path == 'fierce': ok(f'{nm}: Fierce -> Ofuda held for Ch2 (hold=1, not owned yet)', g.get('hold') == 1 and not g.get('own'), g)
    else: ok(f'{nm}: Strategic -> no Ofuda', g.get('hold') == 0 and not g.get('own'), g)
    ok(f'{nm}: no page errors', not errs, errs[:3]); await b.close()

CLOSEHELP = """()=>{var n=0;document.querySelectorAll('#whelp.on button, #wcomment.on button').forEach(function(b){if(b.offsetParent&&n<1){b.click();n++}});return n}"""
ST2 = """({ch:SAVE.chapter,arrive:!!(typeof c2S==='function'&&c2S().e.arrive),cut:!!W.cut,dlg:!!W.dlg,gf:!!document.querySelector('#gfind.on'),hold:(SAVE.gear&&SAVE.gear.ofudaHold)|0,own:!!(SAVE.gear&&SAVE.gear.own&&SAVE.gear.own.ofuda),trans:!!document.getElementById('c2trans'),help:!!document.querySelector('#whelp.on'),lvc:!!document.querySelector('#wlvc.on')})"""
async def ch2_setup(pg, hold=1, own=0, wait=0, path='fierce'):
    await H.ch1_ready(pg, 1440, 3300)
    await H.ev(pg, SET + "(" + json.dumps({'path': path, 'ngp': 0, 'lamp': 1}) + ")")
    await H.ev(pg, "(function(a){var g=gearS();if(a.hold)g.ofudaHold=1;if(a.own)g.own.ofuda=1;if(a.wait)g.ofudaWait=1;SAVE.gouki=1;SAVE.sc.ending=1;STORY.bond(SAVE).lq=[];save();FFF_UI.ST.events.length=0;return 1})(" + json.dumps({'hold': hold, 'own': own, 'wait': wait}) + ")")
async def walk_until_gf(pg, secs, log=None, nskip=True):
    """drive the Ch2 arrival without Skip (Next on dialogs, close help tips); returns the state when the Ofuda card shows, else None"""
    for i in range(int(secs * 3)):
        s = await H.ev(pg, ST2)
        if log is not None: log.append(s)
        if s.get('gf'): return s
        if s.get('lvc'): await pg.evaluate("()=>{var b=document.querySelector('#wlvc.on .wnext');if(b&&!b.disabled)b.click()}")
        await pg.evaluate(ADV); await pg.evaluate(CLOSEHELP)
        await pg.wait_for_timeout(330)
    return None
async def ch2_flow(p):
    b, ctx, pg, errs = await H.boot(p, PORT)
    await ch2_setup(pg)
    await H.ev(pg, "WORLD_API.c2Begin(false);1")
    log = []; s = await walk_until_gf(pg, 60, log)
    ok('C: the Ofuda card shows in Ch2', bool(s), log[-1:] if log else None)
    early = [q for q in log if q.get('gf') and (not q.get('arrive') or q.get('cut') or q.get('trans'))]
    ok('C: not during the crane pan / arrival cine', not early, early[:2])
    evs = await H.ev(pg, EVS)
    ce = evs.index('world:c2:cine:end') if 'world:c2:cine:end' in evs else -1; ge = next((i for i, e in enumerate(evs) if e.startswith('world:gfind:show:ofuda')), -1)
    ok('C: shown after the arrival cine ends (first free walk)', ce >= 0 and ge > ce, (ce, ge))
    ok('C: owned + hold cleared the moment it shows', s and s.get('own') and s.get('hold') == 0, s)
    if s:
        await pg.wait_for_timeout(700); await pg.screenshot(path=str(SHOTS / f'{TAG}_ch2_freewalk_ofuda.png'))
        sw = await pg.evaluate("()=>{var b=document.querySelector('#gfind.on button[data-a=swap]')||document.querySelector('#gfind.on button[data-a=equip]');if(b){b.click();return b.dataset.a}return null}")
        ok('C: swap card (CURRENT Lampglass vs NEW Ofuda)', sw == 'swap', sw)
        await pg.wait_for_timeout(1500)
        r = await H.ev(pg, "({eq:gearEq('acc',SAVE.act||'ryo'),dlg:W.dlg,gf:!!document.querySelector('#gfind.on')})")
        ok('C: Swap equips it and frees the map', r.get('eq') == 'ofuda' and not r.get('gf'), r)
        await walk_until_gf(pg, 6)
        ok('C: shown exactly once', await gfind_count(pg) == 1, await gfind_count(pg))
    ok('C: no page errors', not errs, errs[:3]); await b.close()
async def reload_flow(p):
    b, ctx, pg, errs = await H.boot(p, PORT)
    await ch2_setup(pg)
    await H.ev(pg, "root.FFF_LVC_WAIT=1e9;WORLD_API.c2Begin(false);1")
    await walk_until_gf(pg, 25)
    s0 = await H.ev(pg, ST2); ok('R: held while blocked (arrived, not shown yet)', s0.get('arrive') and s0.get('hold') == 1 and not s0.get('gf'), s0)
    await H.ev(pg, "save();1")
    await ctx.add_init_script("window.FFF_LVC_WAIT=window.__lvcBlock?1e9:1e9")
    await pg.reload(); await pg.wait_for_timeout(3500); await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(1500)
    s1 = await H.ev(pg, ST2); ok('R: after reload the save is in Ch2 with the hold', s1.get('ch') == 2 and s1.get('hold') == 1 and not s1.get('own'), s1)
    await H.ev(pg, "root.FFF_LVC_WAIT=null;1")
    s = await walk_until_gf(pg, 30)
    ok('R: shows after the reload', bool(s), await H.ev(pg, ST2))
    await pg.evaluate("()=>{var b=document.querySelector('#gfind.on button[data-a=keep]')||document.querySelector('#gfind.on button[data-a=stash]');if(b)b.click()}"); await pg.wait_for_timeout(1200)
    await pg.reload(); await pg.wait_for_timeout(3500); await pg.evaluate("WORLD_API.enter(true)"); await H.ev(pg, "root.FFF_LVC_WAIT=null;1"); await pg.wait_for_timeout(1500)
    s2 = await walk_until_gf(pg, 12)
    st = await H.ev(pg, ST2)
    ok('R: second reload never shows it again', not s2 and st.get('own') and st.get('hold') == 0, st)
    ok('R: no page errors', not errs, errs[:3]); await b.close()
async def old_saves(p):
    b, ctx, pg, errs = await H.boot(p, PORT)
    # O1: old save already owns it, a stray hold -> nothing shows, hold cleared
    await ch2_setup(pg, hold=1, own=1)
    await H.ev(pg, "root.FFF_SKIP_C2_TRANS=1;root.FFF_SKIP_C2_CINE=1;WORLD_API.c2Begin(false);1")
    s = await walk_until_gf(pg, 15); st = await H.ev(pg, ST2)
    ok('O1: owned + stray hold -> no card, hold cleared', not s and st.get('hold') == 0 and await gfind_count(pg) == 0, st)
    # O2: owned + old ofudaWait + bond change -> no grant
    await H.ev(pg, "gearS().ofudaWait=1;save();WORLD_API.gearCapCheck();1"); s = await walk_until_gf(pg, 6); st = await H.ev(pg, ST2)
    ok('O2: owned + ofudaWait + bond check -> no card', not s and st.get('hold') == 0 and await gfind_count(pg) == 0, st)
    # O3: Gouki rematch win on a save that owns it -> no hold
    await H.ev(pg, "SAVE.ch1=1;SAVE.gouki=1;gearS().ofudaWait=0;save();WORLD_API.gearOfudaOnWin(null);1"); st = await H.ev(pg, ST2)
    ok('O3: owned -> Gouki win marks nothing', st.get('hold') == 0, st)
    # O4: not owned, old ofudaWait (bond was < Lv4 at Gouki), gate opens on a bond change -> held, then shown once on the free walk
    await H.ev(pg, "delete gearS().own.ofuda;gearS().ofudaWait=1;save();WORLD_API.gearCapCheck();1"); st = await H.ev(pg, ST2)
    ok('O4: late grant goes to the hold (no card straight away)', st.get('hold') == 1 and not st.get('gf'), st)
    s = await walk_until_gf(pg, 15); ok('O4: then shows on the Ch2 free walk', bool(s))
    await pg.evaluate("()=>{var b=document.querySelector('#gfind.on button[data-a=keep]');if(b)b.click()}"); await pg.wait_for_timeout(800)
    await walk_until_gf(pg, 5); ok('O4: once', await gfind_count(pg) == 1, await gfind_count(pg))
    # O5: hold set in Ch1 (Gouki down, ending pending) never shows in Ch1
    await H.ev(pg, "SAVE.chapter=1;gearS().ofudaHold=1;delete gearS().own.ofuda;save();FFF_UI.ST.events.length=0;1")
    s = await walk_until_gf(pg, 6); ok('O5: hold never shows in Chapter One', not s and await gfind_count(pg) == 0)
    # O6: NG+ with accessories hidden drops a stale hold; kept accessories keep ownership (no re-award)
    n1 = await H.ev(pg, "(function(){var o=FFF_NG.base();o.acc='hide';var N=FFF_NG.build(SAVE,o);return {hold:(N.gear||{}).ofudaHold|0,own:!!((N.gear||{}).own||{}).ofuda}})()")
    ok('O6: NG+ hide -> no stale hold, not owned', n1 == {'hold': 0, 'own': False}, n1)
    n2 = await H.ev(pg, "(function(){gearS().own.ofuda=1;delete gearS().ofudaHold;var o=FFF_NG.base();o.acc='keep';var N=FFF_NG.build(SAVE,o);return {hold:(N.gear||{}).ofudaHold|0,own:!!((N.gear||{}).own||{}).ofuda}})()")
    ok('O6: NG+ keep -> still owned, no hold', n2 == {'hold': 0, 'own': True}, n2)
    ok('O: no page errors', not errs, errs[:3]); await b.close()
async def main():
    H.serve(ROOT, PORT)
    async with H.async_playwright() as p:
        for path in ('fierce', 'strategic'):
            for ngp in (False, True):
                if ONLY and ONLY != 'P': continue
                await finale(p, path, ngp)
        if not ONLY or ONLY == 'C': await ch2_flow(p)
        if not ONLY or ONLY == 'R': await reload_flow(p)
        if not ONLY or ONLY == 'O': await old_saves(p)
    print(f'{sum(1 for r in RES if r[0])}/{len(RES)} PASS'); sys.exit(0 if all(r[0] for r in RES) else 1)
asyncio.run(main())
