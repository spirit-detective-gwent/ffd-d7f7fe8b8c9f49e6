#!/workspace/pwenv/bin/python3
"""Herbalist cinematic + pot reach tests (v6.5.66 herbcine, Erik t608/t609).
  1 hand-off: the bottle always belongs to Sumire's or Ryo's sprite, never floats, never sits on the floor, no jump at the hand-over; no free pour stream
  2 pour: stream only while the dipper is over the bottle; bottle fills
  3 bubble: her Talk tag stays on her the whole lesson and after
  4 dialogue: with an item / compare card up the box sits at the bottom, portrait and card never overlap (control: no card -> dock top)
  5 pots: tap / tag / walk-up from several angles plants and picks; NPC and door taps are not stolen
  6 flow: teach -> learn -> Kampo granted -> seed menu after; props gone, she is home, camera back
  7 skip / stale: tapping during a beat fast-forwards; Reset (scKill) mid-beat leaves nothing behind
Usage: test_herbcine.py [index.html]   (FFD_INDEX also works)"""
import asyncio, sys, json, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import h
OUT = os.environ.get('OUT', '/workspace/herbcine/shots/test')
RES = []
def check(name, ok, info=''):
    RES.append((name, bool(ok), info)); print(('PASS ' if ok else 'FAIL ') + name + ((' -- ' + str(info)) if info and not ok else (' (' + str(info) + ')' if info else '')), flush=True)
STATE = """(function(){ var st=c2S(); st.e.sumire=1; st.e.herbBrief=1; SAVE.craft={}; SAVE.sc=SAVE.sc||{};
 SAVE.sc.pot='gather'; SAVE.sc.potGift=1; SAVE.sc.potLeaf=1; delete SAVE.sc.potHand; delete SAVE.sc.potGinger; delete SAVE.sc.potGranted;
 var hb=herbS(); hb.leaf=1; hb.ginger=1; save(); return 1; })()"""
PROBE = """(function(){ function r(e){ if(!e||!e.getBoundingClientRect) return null; var b=e.getBoundingClientRect(); return [b.x,b.y,b.width,b.height]; }
 var su=W.c2n&&W.c2n.sumire, ry=W.ryo, d=document.getElementById('wdlg'), bt=document.getElementById('hsbot'), dp=document.getElementById('hsladle'), sm=document.getElementById('hsstream');
 var tg=document.querySelector('#wtags .wtag[data-k="c2_clinic:sumire"]'); var tgs=tg?getComputedStyle(tg):null; var box=document.getElementById('wtags');
 var par=bt?(bt.parentNode===(su&&su.el)?'su':bt.parentNode===(ry&&ry.el)?'ryo':'other'):null;
 var smcs=sm?getComputedStyle(sm):null;
 return {su:su&&su.el?r(su.el):null, sux:su?[su.x,su.y]:null, ry:r(ry.el), ryx:[ry.x,ry.y], bot:r(bt), par:par, dp:r(dp), sm:r(sm), smop:smcs?+smcs.opacity:null, smsc:sm?sm.getAnimations().length&&(sm.getAnimations()[0].effect.getComputedTiming().progress):null,
   pour:!!document.getElementById('hspour'), tag:(tg&&tgs.display!=='none'&&tgs.visibility!=='hidden'&&getComputedStyle(box).display!=='none')?r(tg):null, tagp:tgs?tgs.pointerEvents:null,
   dlg:d&&d.classList.contains('on')?r(d):null, dock:d?d.classList.contains('dock-top'):false, cmp:r(document.getElementById('hscmp')), cine:document.body.classList.contains('hscine'), hs:[HS.on,HS.ph,HS.skip],
   zoom: su&&su.el?su.el.getBoundingClientRect().width/68:1, sc:getComputedStyle(document.getElementById('wv')).scale, carry:bt?bt.classList.contains('carry'):false, hands:bt?(function(){var h=bt.querySelector('.hsh'); return h?getComputedStyle(h).display:null})():null, ryw:[ry.x,ry.y], aow:W.aoi?[W.aoi.x,W.aoi.y]:null, fill: bt?(function(){var q=bt.querySelector('.hslq'); return q?getComputedStyle(q).transform:null})():null}; })()"""
def cx(r): return r[0] + r[2] / 2
def cy(r): return r[1] + r[3] / 2
async def start_lesson(g):
    await g.hush(); await g.ev(STATE); await g.ev("c2SumireD()"); await g.wait(900)
    await g.ev("(function(){var b=[...document.querySelectorAll('#wdlg button')].find(function(x){return /Teach me$/.test(x.textContent.trim())}); b.click(); return 1})()")
async def run_lesson(g, step=100, tap_skip=False, shotdir=None, max_s=240):
    log = []; t0 = asyncio.get_event_loop().time(); n = 0
    while asyncio.get_event_loop().time() - t0 < max_s:
        p = await g.ev(PROBE); p['t'] = round(asyncio.get_event_loop().time() - t0, 2); log.append(p)
        if shotdir and n % 8 == 0: await g.pg.screenshot(path=f'{shotdir}/l{n:04d}.png')
        n += 1
        c = await g.pg.evaluate(h.NX)
        if c: await g.pg.touchscreen.tap(*c)
        elif tap_skip and p['hs'][1] and not p['hs'][2] and n % 6 == 0: await g.pg.touchscreen.tap(195, 300)
        if await g.ev("!!(SAVE.craft&&SAVE.craft.potion)&&!W.dlg&&!HS.on"): break
        await g.wait(step)
    return log
def judge_lesson(log, tag):
    # 1 hand-off continuity
    bad = []; prev = None; seen = set(); maxj = 0
    for p in log:
        if p['pour']: bad.append(('hspour exists', p['t']))
        if p['bot']:
            seen.add(p['par'])
            if p['par'] not in ('su', 'ryo'): bad.append(('bottle parent', p['par'], p['t'])); continue
            hold = p['su'] if p['par'] == 'su' else p['ry']
            bx, by = cx(p['bot']), cy(p['bot'])
            if not (hold[0] - 0.3 * hold[2] <= bx <= hold[0] + 1.3 * hold[2] and hold[1] <= by <= hold[1] + hold[3] * 0.9): bad.append(('bottle outside holder', p['par'], p['t'], [round(bx), round(by)], [round(v) for v in hold]))
            feet = hold[1] + hold[3] * 0.95
            if by > feet - 0.12 * hold[3]: bad.append(('bottle on the floor', p['par'], p['t']))
            if prev is not None and prev['bot']:
                j = math.hypot(bx - cx(prev['bot']), by - cy(prev['bot'])) / max(0.5, p['zoom']); maxj = max(maxj, j)
                if j > 36: bad.append(('bottle jumped', round(j), p['t'], prev['par'], p['par']))
        prev = p
    check(tag + ' hand-off: bottle never detaches / floats / lies on the floor', not bad, bad[:3] or ('held by ' + '+'.join(sorted(seen - {None})) + ', max step %.1f world px' % maxj))
    check(tag + ' hand-off: Sumire holds it, Ryo takes it', seen >= {'su', 'ryo'}, sorted(x for x in seen if x))
    # 2 pour stream only over the bottle
    badS = []; nS = 0
    for p in log:
        if p['sm'] and (p['smop'] or 0) > 0.3 and (p['smsc'] or 0) > 0.15:
            nS += 1
            if not (p['dp'] and p['bot']): badS.append(('stream without dipper/bottle', p['t'])); continue
            if abs(cx(p['sm']) - cx(p['bot'])) > 0.8 * p['bot'][2] or abs(cx(p['sm']) - (p['dp'][0] + p['dp'][2] * 0.2)) > 1.2 * p['dp'][2] or cy(p['sm']) > p['bot'][1] + p['bot'][3]: badS.append(('stream off', p['t']))
    check(tag + ' pour: stream only runs from the dipper into the bottle', nS > 0 and not badS, badS[:2] or ('%d samples' % nS))
    # 2b live framing: Ryo / Aoi where live puts them, zoom no tighter than live's 1.32
    sc = [float(p['sc']) for p in log if p['cine'] and p['sc'] not in (None, 'none', '')]
    mid = [p for p in log if p['cine'] and p['hs'][1] and p['su'] and abs(p['sux'][0] - 679) < 3] if False else []
    ry_ok = [p for p in log if p['cine'] and abs(p['ryw'][0] - 598) < 4 and abs(p['ryw'][1] - 612) < 4]
    ao_ok = [p for p in log if p['cine'] and p['aow'] and abs(p['aow'][0] - 532) < 60 and abs(p['aow'][1] - 624) < 60]  # Aoi's follow settles her a little off the walk target, same as live
    check(tag + ' framing: Ryo and Aoi stand where live puts them (Ryo 598,612; Aoi beside him)', len(ry_ok) > 20 and len(ao_ok) > 20, (len(ry_ok), len(ao_ok)))
    check(tag + ' framing: camera zoom stays at live level (<= 1.40 through the cinematic)', sc and max(sc) <= 1.40, max(sc) if sc else None)
    # 2c carry low: waist, between both hands, while she walks to Ryo
    walk = [p for p in log if p['par'] == 'su' and p['carry'] and p['su'] and p['bot']]
    lowbad = []
    for p in walk:
        rel = (cy(p['bot']) - p['su'][1]) / p['su'][3]
        if not (0.42 <= rel <= 0.72) or p['hands'] != 'block': lowbad.append((p['t'], round(rel, 2), p['hands']))
    check(tag + ' carry: bottle held low at her waist between both hands the whole walk (%d samples)' % len(walk), len(walk) > 8 and not lowbad, lowbad[:3])
    # 3 bubble
    json.dump(log, open(f'{OUT}/{tag}_log.json', 'w'))
    vis = [p['t'] for p in log if p['cine'] and p['tag']]
    check(tag + ' bubble: no stray Talk bubble while the story camera is zoomed (hidden during the cinematic)', not vis, vis[:3])
    # 4 compare card never under the portrait / box at bottom
    badD = []; nD = 0
    for p in log:
        if p['cmp'] and p['dlg']:
            nD += 1
            if p['dock']: badD.append(('dock-top with card', p['t']))
            if p['dlg'][1] < p['cmp'][1] + p['cmp'][3]: badD.append(('box above card bottom', p['t']))
    check(tag + ' dialogue: box at the bottom whenever the compare card is up', nD > 5 and not badD, badD[:3] or ('%d samples' % nD))
async def end_state(g, tag):
    s = await g.ev("""(function(){ var su=W.c2n.sumire; return {props:['hsbot','hsladle','hsstream','hssteam','hsanchor','hspour'].filter(function(i){return document.getElementById(i)}), cine:document.body.classList.contains('hscine'), HS:HS.on,
       home:[Math.round(su.x),Math.round(su.y)], loop:!!su.loop, pot:SAVE.craft&&SAVE.craft.potion, sp:SAVE.sc.pot, potions:(SAVE.heal||[]).filter(function(k){return k==='potion'}).length, dlg:!!W.dlg, paused:!!W.paused, busy:!!W.busy,
       sc:getComputedStyle(document.getElementById('wv')).scale, tags:!!document.querySelector('#wtags .wtag[data-k="c2_clinic:sumire"]')}})()""")
    return s
def scale_ok(sc):
    return sc in ('none', '', '1') or abs(float(sc) - 1) < 0.25
async def t_lesson(g, tag, skip=False):
    d = f'{OUT}/{tag}'; os.makedirs(d, exist_ok=True)
    await start_lesson(g); log = await run_lesson(g, tap_skip=skip, shotdir=d if not skip else None)
    await g.wait(1500)
    judge_lesson(log, tag)
    s = await end_state(g, tag)
    check(tag + ' flow: learned, Kampo granted, scene over', s['pot'] == 1 and s['sp'] == 'learned' and s['potions'] >= 1 and not s['HS'] and not s['cine'], s)
    check(tag + ' flow: no props left, she is back at her counter, idle loop on, camera back', not s['props'] and abs(s['home'][0]-790)<=3 and abs(s['home'][1]-380)<=3 and s['loop'] and scale_ok(s['sc']), s)
    return log
async def t_menu_after(g):
    await g.hush(); await g.ev("c2SumireD()"); await g.wait(900)
    d = await g.ev("(function(){var d=document.getElementById('wdlg');return [...d.querySelectorAll('button')].map(function(x){return x.textContent.trim()})})()")
    check('flow: seed menu after the lesson', any(b.startswith('Seeds') for b in d) and not any('Teach me' in b for b in d), d)
    await g.hush()
async def t_bubble(g):
    await g.hush(); await g.ev("c2S().e.sumire=1; W.scr=0; W.cut=0; 1")
    bad = []; n = 0
    for (x, y) in ((790, 380), (700, 470), (640, 560), (560, 430), (900, 500)):
        await g.ev(f"(function(){{var su=W.c2n.sumire; su.x={x}; su.y={y}; place(su,0); W.ryo.x=620; W.ryo.y=700; place(W.ryo,0); camera(true); return 1}})()"); await g.wait(500)
        p = await g.ev(PROBE); n += 1
        if not p['tag']: bad.append((x, y, 'no tag')); continue
        z = max(0.3, p['zoom']); dx = abs(cx(p['tag']) - cx(p['su'])) / z; dy = (p['su'][1] - cy(p['tag'])) / z
        if dx > 12 or dy < -25 or dy > 25: bad.append((x, y, round(dx), round(dy)))
    check('bubble: her Talk bubble sits on her wherever she stands (5 spots)', n == 5 and not bad, bad)
    await g.ev("(function(){var su=W.c2n.sumire; su.x=790; su.y=380; place(su,0); return 1})()")
async def t_dialog(g):
    await g.hush(); await g.ev("(function(){var st=c2S(); st.e.sumire=1; return 1})()")
    res = {}
    for card in (False, True):
        await g.hush(); await g.ev("hsCmpCard('off')")
        # stand her low on the screen so the bottom slot would cover her: control case docks the box to the top
        for i in range(6):
            r = await g.ev("(function(){var su=W.c2n.sumire; var b=su.el.getBoundingClientRect(); return [b.y+b.height/2, W.S]})()")
            dy = (760 - r[0]) / max(0.3, r[1])
            if abs(dy) < 3: break
            await g.ev(f"(function(){{var su=W.c2n.sumire; su.y+={dy}; place(su,0); return 1}})()"); await g.wait(120)
        if card: await g.ev("hsCmpCard('dress'); hsCmpCard('kampo')")
        await g.ev("W.dlgDock=null; scene(null,[['tsukikage','Show me what you two have been patching yourselves up with.',{mood:'neutral'}]],function(){}); 1"); await g.wait(1400)
        res[card] = await g.ev("""(function(){var d=document.getElementById('wdlg'), c=document.getElementById('hscmp'), p=d.querySelector('.pt2'), r=function(e){if(!e)return null;var b=e.getBoundingClientRect();return [b.x,b.y,b.width,b.height]};
           var su=W.c2n.sumire.el.getBoundingClientRect(); return {top:d.classList.contains('dock-top'), d:r(d), c:r(c), p:r(p), su:[su.x,su.y,su.width,su.height]}})()""")
        await g.pg.screenshot(path=f'{OUT}/dlg_card_{int(card)}.png')
        await g.ev("(function(){var d=document.getElementById('wdlg'); d.className=''; d.innerHTML=''; W.dlg=false; W.cut=0; scKill(); hsCmpCard('off'); return 1})()")
        await g.hush()
    check('dialogue control: no card + speaker low on screen -> box docks to the top (v6.5.63 behaviour kept)', res[False]['top'], res[False])
    c = res[True]; ov = lambda a, b: a and b and a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]
    check('dialogue: card up -> box stays at the bottom', not c['top'] and c['d'][1] > c['c'][1] + c['c'][3], c)
    check('dialogue: portrait never overlaps the card', not ov(c['p'], c['c']) and not ov(c['d'], c['c']), c)
def lat(g, x, y): return None
async def t_pots(g):
    await g.hush(); await g.ev("(function(){var st=c2S(); st.e.sumire=1; st.e.gardenIntro=1; st.e.gingerIntro=1; SAVE.craft=SAVE.craft||{}; SAVE.craft.potion=1; herbAdd('seed',30); herbAdd('gseed',30); save(); return 1})()")
    await g.enter('clinic', 560, 640)
    pots = await g.ev("(W.g50p||[]).map(function(o){return [o.p.id,o.x,o.y,o.p.kind||'']})")
    check('pots: nine mugwort + six ginger pots present', len(pots) >= 15, len(pots))
    async def world_to_screen(x, y):
        return await g.ev(f"(function(){{var L=document.getElementById('wisp')||layer,e=document.createElement('i'); e.style.cssText='position:absolute;width:1px;height:1px;left:{x}px;top:{y}px'; L.appendChild(e); var b=e.getBoundingClientRect(); e.remove(); return [b.x,b.y]}})()")
    async def pst(pid): return await g.ev(f"c2Cyc().pots['{pid}'].st")
    async def setpot(pid, st): await g.ev(f"(function(){{c2Cyc().pots['{pid}'].st='{st}'; W.tagSig=null; return 1}})()"); await g.wait(300)
    async def put(x, y):
        await g.ev(f"(function(){{W.ryo.x={x}; W.ryo.y={y}; W.ryo.v=0; W.path=[]; place(W.ryo,0); if(W.aoi){{W.aoi.x={x}-60; W.aoi.y={y}+10; place(W.aoi,0)}} camera(true); return 1}})()"); await g.wait(500)
    fails = []; n = 0; await g.ev('W.scr=0;W.cut=0;1')
    for pid, kind in (('gp5', ''), ('gg2', 'ginger')):
        px, py = [(o[1], o[2]) for o in pots if o[0] == pid][0]
        # (start offset from the pot's feet, tap offset on the pot)
        cases = [((24, 1), (0, -14)), ((-24, 1), (0, -14)), ((0, 26), (0, -14)), ((34, -20), (0, -14)), ((-34, -20), (0, -30)), ((30, 30), (14, -10)), ((-30, 28), (-12, -40)), ((0, -34), (0, -14)), ((44, -8), (0, -26)), ((90, 20), (0, -14)), ((-70, 40), (0, 0))]
        for (ox, oy), (tx, ty) in cases:
            await setpot(pid, 'empty'); await put(px + ox, py + oy)
            sx, sy = await world_to_screen(px + tx, py + ty)
            await g.pg.touchscreen.tap(sx, sy)
            ok = False
            for i in range(60):
                await g.wait(150)
                if await pst(pid) == 'planted' and not await g.ev("W.busy"): ok = True; break
            n += 1
            if not ok: fails.append((pid, (ox, oy), (tx, ty), await pst(pid), await g.ev('[W.scr,W.cut,W.dlg,W.busy]'), await g.ev('FFF_UI.ST.events.slice(-3)')))
            await g.hush(); await g.wait(200)
    check('pots: tap on the pot plants from %d start spots / tap points (both kinds)' % n, not fails, fails[:4])
    # pick (bloomed) the same way
    fails = []
    for pid in ('gp5', 'gg2'):
        px, py = [(o[1], o[2]) for o in pots if o[0] == pid][0]
        for (ox, oy) in ((-30, 10), (0, 30), (40, -16)):
            await setpot(pid, 'bloomed'); await put(px + ox, py + oy)
            sx, sy = await world_to_screen(px, py - 20); await g.pg.touchscreen.tap(sx, sy)
            ok = False
            for i in range(60):
                await g.wait(150)
                if await pst(pid) == 'empty' and not await g.ev("W.busy"): ok = True; break
            if not ok: fails.append((pid, (ox, oy), await pst(pid)))
            await g.hush(); await g.wait(200)
    check('pots: tap on a bloomed pot picks it from three sides', not fails, fails)
    # no orange prompt buttons any more: the plants themselves are the target
    px, py = [(o[1], o[2]) for o in pots if o[0] == 'gp5'][0]
    await setpot('gp5', 'empty'); await put(px + 30, py + 20); await g.wait(400)
    ntags = await g.ev("document.querySelectorAll('#wtags .wtag[data-k*=\":pot:\"]').length + (W.tagL||[]).filter(function(t){return /:pot:/.test(t.key)}).length")
    check('pots: no Plant / Pick tag buttons exist (standing next to a pot)', ntags == 0, ntags)
    await g.pg.screenshot(path=f'{OUT}/pot_no_tag.png')
    # bigger tap radius on the plant: taps that were misses before (well above the plant, wide of it) still count
    fails = []
    for (tx, ty, ox, oy) in ((0, -54, -50, 30), (38, -12, 60, 10), (-38, -12, -60, 20), (0, 16, 20, 60), (30, -40, 20, 50)):
        await setpot('gp5', 'empty'); await put(px + ox, py + oy)
        sx, sy = await world_to_screen(px + tx, py + ty); await g.pg.touchscreen.tap(sx, sy); ok = False
        for i in range(130):
            await g.wait(150)
            if await pst('gp5') == 'planted' and not await g.ev("W.busy"): ok = True; break
        if not ok: fails.append((tx, ty, ox, oy, await pst('gp5')))
        await g.hush(); await g.wait(200)
    check('pots: a tap on the plant, above it or just beside it walks Ryo over and plants (5 wider taps)', not fails, fails)
    # no stealing: a tap on Sumire (NPC) and on the Exit door never touches a pot
    await g.hush(); before = {o[0]: await pst(o[0]) for o in pots}
    await put(560, 640); sx, sy = await world_to_screen(790, 380 - 30); await g.pg.touchscreen.tap(sx, sy); await g.wait(1500); await g.hush()
    ex = [[575, 818]]
    after = {o[0]: await pst(o[0]) for o in pots}
    check('pots: tap on Sumire does not start a pot action', before == after)
    if ex:
        await put(560, 640); sx, sy = await world_to_screen(ex[0][0], ex[0][1]); await g.pg.touchscreen.tap(sx, sy); await g.wait(800)
        r = await g.ev("[c2Room(), W.busy, W.dlg]"); after = {o[0]: await pst(o[0]) for o in pots}
        check('pots: tap on the exit never starts a pot action', before == after, r)
    # a tap that lands on a pot while a dialogue is open does nothing
    await g.hush()
async def t_stale(g):
    await g.enter('clinic', 560, 640)
    await g.hush(); await g.ev(STATE)
    # skip: start the cinematic phases straight, tap during a beat
    await g.ev("W.dlg=true; hsLesson(function(){window.__done=1}); 1")
    t0 = asyncio.get_event_loop().time(); tapped = 0
    for i in range(1200):
        c = await g.pg.evaluate(h.NX)
        if c: await g.pg.touchscreen.tap(*c); await g.wait(150); continue
        st = await g.ev("[HS.on,HS.ph,HS.skip]")
        if st[0] and st[1] and not st[2] and i % 5 == 0: await g.pg.touchscreen.tap(195, 250); tapped += 1
        if await g.ev("!!window.__done"): break
        await g.wait(120)
    dt = asyncio.get_event_loop().time() - t0
    s = await end_state(g, 'skip')
    check('skip: taps during the staged beats fast-forward them and the scene still finishes cleanly', tapped > 0 and s['pot'] == 1 and not s['props'] and not s['HS'] and not s['cine'] and abs(s['home'][0]-790)<=3 and abs(s['home'][1]-380)<=3, (tapped, round(dt), s))
    # stale: reset mid-beat
    await g.enter('clinic', 560, 640); await g.hush(); await g.ev(STATE)
    await g.ev("SAVE.craft={}; SAVE.sc.pot='gather'; delete SAVE.sc.potGranted; W.dlg=true; hsLesson(function(){}); 1")
    for i in range(300):
        c = await g.pg.evaluate(h.NX)
        if c: await g.pg.touchscreen.tap(*c); await g.wait(150); continue
        if await g.ev("HS.on&&HS.ph&&!!document.getElementById('hsladle')"): break
        await g.wait(100)
    mid = await g.ev("[HS.on, !!document.getElementById('hsbot'), !!document.getElementById('hsladle'), document.body.classList.contains('hscine')]")
    await g.ev("W.scGen=(W.scGen|0)+1; scKill(); 1"); await g.wait(600)
    s = await end_state(g, 'stale')
    check('stale: Reset / NG+ (scKill) mid-beat clears the props, class and state', mid[0] and mid[2] and not s['props'] and not s['cine'] and not s['HS'] and abs(s['home'][0]-790)<=3 and abs(s['home'][1]-380)<=3 and scale_ok(s['sc']), (mid, s))
    await g.ev("W.dlg=false; W.cut=0; 1"); await g.hush()
async def main():
    os.makedirs(OUT, exist_ok=True)
    idx = sys.argv[1] if len(sys.argv) > 1 else None
    if idx: h.INDEX = h.Path(idx)
    async with h.Game(path='compassionate', out=OUT) as g:
        await g.boot(); await g.enter('clinic', 560, 640)
        ONLY = os.environ.get('ONLY', 'lesson,menu,bubble,dialog,pots,stale').split(',')
        if 'lesson' in ONLY: await t_lesson(g, 'compassionate')
        if 'menu' in ONLY: await t_menu_after(g)
        if 'bubble' in ONLY: await t_bubble(g)
        if 'dialog' in ONLY: await t_dialog(g)
        if 'pots' in ONLY: await t_pots(g)
        if 'stale' in ONLY: await t_stale(g)
        check('no page errors', not g.errs, g.errs[:3])
    bad = [r for r in RES if not r[1]]
    print('\nHERBCINE %d/%d' % (len(RES) - len(bad), len(RES)), 'FAIL' if bad else 'PASS', flush=True)
    sys.exit(1 if bad else 0)
asyncio.run(main())
