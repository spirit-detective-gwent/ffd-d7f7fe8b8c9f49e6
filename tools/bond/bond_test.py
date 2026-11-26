#!/workspace/pwenv/bin/python3
"""Ch2 bond-moment tests: pay table, Grinder, Journal fixes, c2_goda scene (3 answers), consequences, perk. Review-only."""
import sys, asyncio, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import bh
from playwright.async_api import async_playwright
PORT = 8986
R = []
def ok(name, cond, extra=''):
    R.append((name, bool(cond), extra)); print(('PASS ' if cond else 'FAIL ') + name + (' :: ' + str(extra) if (extra and not cond) else ''))
CLICK = """(i)=>{var b=[...document.querySelectorAll('#wdlg.on button')].filter(e=>e.offsetParent&&!e.disabled&&!/Auto/.test(e.textContent));if(!b.length)return null;var x=b[i||0]||b[0];x.click();return x.textContent.trim()}"""
POLL = """(function(){var d=document.getElementById('wdlg');var on=!!(d&&d.classList.contains('on'));return {on:on,bond:!!document.querySelector('#wdlg.on button.bondopt'),seal:!!c2S().e.seal_sento}})()"""
async def newpage(b, body, path='balanced', run=True):
    ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
    pg = await ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
    await bh.boot(pg, PORT, body); await bh.ch2(pg)
    await bh.ev(pg, "(function(){var E=c2S().e;%sSTORY.bond(SAVE).path='%s';return 1})()" % ("E.run_fac='arc';E.baseOpen_bat=1;E.guardGone_sento=1;E.arrive=1;" if run else '', path))
    return ctx, pg, errs
async def drive(pg, ans_idx, maxn=420):
    for i in range(maxn):
        await pg.wait_for_timeout(330); st = await bh.ev(pg, POLL)
        if st['seal']: return True
        if st['on']:
            await pg.evaluate(CLICK, ans_idx if st['bond'] else 0)
    return False
async def scene_case(b, body, path, idx, fate):
    ctx, pg, errs = await newpage(b, body, path)
    await bh.ev(pg, "c2Go('sento')"); await pg.wait_for_timeout(2500); await bh.ev(pg, bh.HUSH)
    r = await bh.ev(pg, "(function(){var b=W.c2n.boss;W.ryo.x=b.x-90;W.ryo.y=b.y+60;place(W.ryo,0);if(W.aoi){W.aoi.x=b.x-130;W.aoi.y=b.y+90;place(W.aoi,0)}camera(true);var p0=STORY.bond(SAVE).px;c2LmBack(true,{ctx:{c2lm:'sento',dg:'c2'}});return p0})()")
    done = await drive(pg, idx)
    ans = ['fierce', 'strategic', 'balanced'][idx]
    info = await bh.ev(pg, "(function(){var B=STORY.bond(SAVE),E=c2S().e;return {px:B.px,pick:B.picks.c2_goda,fate:E.godaFate,tip:E.ckTip||0,named:E.ckNamed,seal:E.seal_sento,old:B.picks.c2lm_sento||null}})()")
    n = f'{path}/{ans}'
    ok(f'scene {n}: finished (seal broke)', done)
    ok(f'scene {n}: pick recorded', info['pick'] == ans, info)
    exp = {'best': 700, 'mid': 350, 'clash': 140}[('best' if path == ans else ('mid' if (ans == 'balanced' and path != 'balanced') or (path == 'balanced' and ans == 'strategic') else 'clash'))]
    ok(f'scene {n}: paid {exp}', info['px'] - r == exp, (info['px'], r))
    ok(f'scene {n}: fate {fate}', info['fate'] == fate, info)
    ok(f'scene {n}: ckTip only on deal', bool(info['tip']) == (fate == 'deal'), info)
    ok(f'scene {n}: Tetsu named', info['named'] == 1)
    ok(f'scene {n}: no old c2lm_sento pick', info['old'] is None)
    gs = await bh.ev(pg, "FFF_CH2BOND.gs()===null")
    ok(f'scene {n}: staging released after seal', gs)
    ok(f'scene {n}: no page errors', not errs, errs[:3])
    return ctx, pg
async def main():
    bh.serve(PORT); body = bh.inject()
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
        # ---- pure data / pay ----
        ctx, pg, errs = await newpage(b, body, 'fierce', run=False)
        pay = await bh.ev(pg, "JSON.stringify(STORY.BOND.PAY)"); pay = json.loads(pay)
        want = {'c2_goda': (700, 350, 140), 'c2_cheap': (760, 380, 152), 'c2_offer': (820, 410, 164), 'c2_ledger': (880, 440, 176), 'c2_eve': (935, 468, 187), 'c2nq_door': (120, 60, 24)}
        for k, v in want.items(): ok(f'PAY.{k} = {v}', (pay[k]['best'], pay[k]['mid'], pay[k]['clash']) == v, pay.get(k))
        ok('M1..M5 sum 4095', sum(pay[k]['best'] for k in ['c2_goda', 'c2_cheap', 'c2_offer', 'c2_ledger', 'c2_eve']) == 4095)
        ok('Ch1 PAY untouched', pay['mini_mb_lib'] == {'best': 90, 'mid': 45, 'clash': 18} and pay['dg_gouki']['best'] == 85)
        ok('c2lm landmarks still 120/60/24', pay['c2lm_sento'] == {'best': 120, 'mid': 60, 'clash': 24} and pay['c2lm_market']['best'] == 140)
        # all 9 path x answer grades for c2_goda, normal mode
        g = await bh.ev(pg, """(function(){var o={};['fierce','strategic','balanced'].forEach(function(p){['fierce','strategic','balanced'].forEach(function(a){var S={bond:{path:p,picks:{},px:0,lock:1},chapter:2,xpMode:'normal'};var r=STORY.bondPick(S,'c2_goda',a,BOND_MID.c2_goda);o[p+'/'+a]=r.n})});return o})()""")
        exp = {'fierce/fierce': 700, 'fierce/strategic': 140, 'fierce/balanced': 350, 'strategic/fierce': 140, 'strategic/strategic': 700, 'strategic/balanced': 350, 'balanced/fierce': 140, 'balanced/strategic': 350, 'balanced/balanced': 700}
        ok('c2_goda 3x3 grades (best/mid/clash)', g == exp, g)
        gg = await bh.ev(pg, """(function(){var o={};['c2_goda','c2_cheap','c2_offer','c2_ledger','c2_eve','c2nq_door'].forEach(function(id){var S={bond:{path:'fierce',picks:{},px:0,lock:1},chapter:2,xpMode:'grinder'};o[id]=STORY.bondPick(S,id,'fierce',BOND_MID[id]).n});return o})()""")
        ok('Grinder halves every M1..M5 pick (and c2nq_door)', gg == {'c2_goda': 350, 'c2_cheap': 380, 'c2_offer': 410, 'c2_ledger': 440, 'c2_eve': 468, 'c2nq_door': 60}, gg)
        # ---- Journal (the Status > Bond block is the live "Aoi's calls" list; the old bondPane is dead code but kept consistent) ----
        h = await bh.ev(pg, """(function(){var B=STORY.bond(SAVE);B.picks={first:'fierce',c2nq_door:'fierce',c2lm_arcade:'strategic',c2lm_game:'balanced',c2lm_sento:'fierce',c2lm_depot:'fierce',c2_goda:'balanced',c2_eve:'fierce',mini_mb_lib:'fierce',dg_gouki:'fierce',c2lm_market:'fierce'};B.path='fierce';return statusBondBlock()})()""")
        ok('Journal list renders the calls', 'bpicks' in h and 'Aoi' in h, h[:200])
        for raw in ['c2nq_door', 'c2lm_', 'c2_goda', 'c2_eve']: ok(f'Journal list has no raw id {raw}', raw not in h)
        for nm in ['Kitsune-no-Yu door: <b>Straight through him</b>', 'G\u014dda on the clay: <b>Help him up and show him the fire\u2019s fine</b>', 'The night before the roof: <b>', 'The courtyard:', 'Kitsune-no-Yu Bathhouse: <b>']:
            ok(f'Journal list shows name "{nm[:34]}"', nm in h, '')
        pay = await bh.ev(pg, "(function(){var o={};['c2nq_door','c2_goda','c2_eve','c2lm_sento','c2lm_market','mini_mb_lib','dg_gouki'].forEach(function(id){o[id]=['best','mid','clash'].map(function(g){return bondCallPay(id,g)})});return o})()")
        ok('bondCallPay normal = PAY table (never the 118/59/24 default)', pay == {'c2nq_door': [120, 60, 24], 'c2_goda': [700, 350, 140], 'c2_eve': [935, 468, 187], 'c2lm_sento': [120, 60, 24], 'c2lm_market': [140, 70, 28], 'mini_mb_lib': [90, 45, 18], 'dg_gouki': [85, 43, 17]}, pay)
        await bh.ev(pg, "SAVE.xpMode='grinder'")
        pay = await bh.ev(pg, "(function(){var o={};['c2_goda','c2lm_sento','c2lm_market','mini_mb_lib'].forEach(function(id){o[id]=['best','mid','clash'].map(function(g){return bondCallPay(id,g)})});return o})()")
        ok('bondCallPay Grinder halves Ch1/Ch2 calls, not Ch3', pay == {'c2_goda': [350, 175, 70], 'c2lm_sento': [60, 30, 12], 'c2lm_market': [140, 70, 28], 'mini_mb_lib': [45, 23, 9]}, pay)
        names = await bh.ev(pg, "['c2nq_door','c2lm_arcade','c2lm_sento','c2_goda','c2_cheap','c2_offer','c2_ledger','c2_eve','first','dg_gouki','mini_mb_lib'].map(bondCallName)")
        ok('bondCallName never returns a raw Ch2 id', not any(n.startswith('c2') for n in names), names)
        ok('no page errors (data/journal)', not errs, errs[:3]); await ctx.close()
        # ---- the old pre-fight call is gone on the Punk route only ----
        ctx, pg, errs = await newpage(b, body, 'fierce', run=True)
        r = await bh.ev(pg, "(function(){var got=null;bondAsk('c2lm_sento',function(L){got=L});return {got:got,pick:STORY.bond(SAVE).picks.c2lm_sento||null}})()")
        ok('Punk run: bondAsk(c2lm_sento) skipped, no pick, no XP', r['got'] == [] and r['pick'] is None, r)
        r = await bh.ev(pg, "(function(){c2S().e.run_fac='';root.FFF_BOND='fierce';var got=null;bondAsk('c2lm_sento',function(L){got=L});root.FFF_BOND=null;return {n:got&&got.length,pick:STORY.bond(SAVE).picks.c2lm_sento||null}})()")
        ok('Other runs still ask c2lm_sento', r['pick'] == 'fierce', r)
        ok('no page errors (skip)', not errs, errs[:3]); await ctx.close()
        # ---- the scene, all three answers (Fierce/Strategic/Compassionate path x answer) ----
        for path, idx, fate in [('fierce', 0, 'ko'), ('strategic', 1, 'deal'), ('balanced', 2, 'help'), ('fierce', 2, 'help'), ('balanced', 0, 'ko')]:
            ctx, pg = await scene_case(b, body, path, idx, fate)
            if path == 'balanced' and idx == 2: keep = (ctx, pg); continue
            if path == 'strategic' and idx == 1: keep2 = (ctx, pg); continue
            await ctx.close()
        # ---- end to end on the Punk route: confront -> (no c2lm_sento call) -> acted -> fight -> win -> c2_goda ----
        ctx, pg, errs = await newpage(b, body, 'strategic', run=True)
        await bh.ev(pg, "c2Go('sento')"); await pg.wait_for_timeout(2500); await bh.ev(pg, bh.HUSH)
        await bh.ev(pg, "(function(){SAVE.bent={};var b=W.c2n.boss;(W.dgF||[]).forEach(function(f){try{f.s.el.remove()}catch(e){}});W.dgF=[];W.ryo.x=b.x;W.ryo.y=b.y+170;place(W.ryo,0);if(W.aoi){W.aoi.x=b.x+70;W.aoi.y=b.y+190;place(W.aoi,0)}camera(true);window.__fa=null;window.__f0=fight;fight=function(ids,a,o){window.__fa=o;return 0};W.c2busy=0;W.busy=false;c2LmBoss('sento');return 1})()")
        asked = []
        for i in range(260):
            await pg.wait_for_timeout(330)
            fa = await bh.ev(pg, "window.__fa&&{lm:window.__fa.c2lm,dg:window.__fa.dg}")
            if fa: break
            st = await bh.ev(pg, "(function(){var d=document.getElementById('wdlg');return {on:!!(d&&d.classList.contains('on')),bond:!!document.querySelector('#wdlg.on button.bondopt'),txt:d?((d.querySelector('.tw')||{}).textContent||'').slice(0,40):''}})()")
            if st['bond']: asked.append(st['txt'])
            if st['on']: await pg.evaluate(CLICK, 0)
            else: await pg.evaluate("()=>{var o=document.getElementById('wintro');if(o)o.click()}")
        ok('e2e: fight launched for sento with c2lm ctx', fa and fa['lm'] == 'sento' and fa['dg'] == 'c2', fa)
        ok('e2e: no bond question before the fight (c2lm_sento skipped)', not asked, asked)
        pk = await bh.ev(pg, "STORY.bond(SAVE).picks.c2lm_sento||null"); ok('e2e: no c2lm_sento pick', pk is None, pk)
        await bh.ev(pg, "(function(){fight=window.__f0;var p0=STORY.bond(SAVE).px;window.__p0=p0;c2Back(true,{ctx:{c2lm:'sento',dg:'c2',dgk:'lm_sento_boss'}});return p0})()")
        done = await drive(pg, 1)
        r = await bh.ev(pg, "(function(){var B=STORY.bond(SAVE);return {d:B.px-window.__p0,pick:B.picks.c2_goda,fate:c2S().e.godaFate,seal:c2S().e.seal_sento,asked:B.picks.c2lm_sento||null}})()")
        ok('e2e: after the win c2_goda pays 700 (Strategic path, Strategic answer) and nothing else', done and r['d'] == 700 and r['pick'] == 'strategic' and r['fate'] == 'deal' and r['asked'] is None, r)
        ok('e2e: no page errors', not errs, errs[:3]); await ctx.close()
        # ---- consequences: help -> Goda at the counter + free soak once per visit ----
        ctx, pg = keep
        r = await bh.ev(pg, "(function(){c2Go('town');return 1})()"); await pg.wait_for_timeout(2500); await bh.ev(pg, bh.HUSH)
        await bh.ev(pg, "c2Go('sento')"); await pg.wait_for_timeout(2500); await bh.ev(pg, bh.HUSH)
        r = await bh.ev(pg, "(function(){return {fate:c2S().e.godaFate,seal:c2S().e.seal_sento,g:!!(W.c2n&&W.c2n.godaC&&W.c2n.godaC.el&&W.c2n.godaC.el.parentNode),soak:W.godaSoak|0,sato:!!(W.c2n&&W.c2n.nqb)}})()")
        ok('help: Goda stands at the bath counter next to Old Sato', r['g'] and r['sato'], r)
        await bh.ev(pg, "SAVE.items=50;SAVE.hp=10;save();FFF_NQ.sentoMenu();1"); await pg.wait_for_timeout(600)
        t = await bh.ev(pg, "document.getElementById('wdlg').innerText")
        ok('help: first Hot soak shows free (\u00a50)', 'on the house' in t and '\u00a50' in t, t[:200])
        y0 = await bh.ev(pg, "SAVE.items|0")
        await pg.evaluate("()=>{var b=[...document.querySelectorAll('#wdlg.on button')].find(e=>/Hot soak/.test(e.textContent));b&&b.click()}"); await pg.wait_for_timeout(2600)
        y1 = await bh.ev(pg, "SAVE.items|0"); hp = await bh.ev(pg, "SAVE.hp|0")
        ok('help: free soak costs 0 yen and heals', y1 == y0 and hp > 10, (y0, y1, hp))
        await bh.ev(pg, "FFF_NQ.sentoMenu();1"); await pg.wait_for_timeout(600)
        t = await bh.ev(pg, "document.getElementById('wdlg').innerText")
        ok('help: second soak in the same visit costs \u00a59 (nails price \u00a57?)', 'on the house' not in t, t[:200])
        await bh.ev(pg, bh.HUSH)
        await bh.ev(pg, "c2Go('town')"); await pg.wait_for_timeout(2200); await bh.ev(pg, bh.HUSH); await bh.ev(pg, "c2Go('sento')"); await pg.wait_for_timeout(2200); await bh.ev(pg, bh.HUSH)
        r = await bh.ev(pg, "W.godaSoak|0")
        ok('help: the perk resets on the next visit', r == 0, r)
        await ctx.close()
        # ---- consequences: ko -> no counter, no perk; deal -> back office drops the dealer ----
        ctx, pg = keep2
        r = await bh.ev(pg, """(function(){var fo=null,rows=null;var f0=fight,s0=scene;fight=function(a,b,o){fo=o};scene=function(i,r,d){rows=r;d&&d()};try{ckPunkIn()}finally{fight=f0;scene=s0}return {join:fo?(fo.joinIn||null):'nofight',rows:rows&&rows.map(function(x){return x[1]}).slice(0,3)}})()""")
        ok('deal: Tetsu fight has no Club Dealer join-in', r['join'] is None and 'Thursday' in json.dumps(r['rows']), r)
        await ctx.close()
        ctx, pg, errs = await newpage(b, body, 'fierce', run=True)
        r = await bh.ev(pg, """(function(){var o={};['ko','none'].forEach(function(f){c2S().e.godaFate=f;c2S().e.ckTip=0;var fo=null,rows=null;var f0=fight,s0=scene;fight=function(a,b,x){fo=x};scene=function(i,r,d){rows=r;d&&d()};try{ckPunkIn()}finally{fight=f0;scene=s0}o[f]={join:!!(fo&&fo.joinIn),line:rows[0][1]}});return o})()""")
        ok('ko: Tetsu nods to the big man; dealer still joins', 'put the big man down' in r['ko']['line'] and r['ko']['join'] and 'big man' not in r['none']['line'] and r['none']['join'], r)
        ok('no page errors (ckPunkIn)', not errs, errs[:3]); await ctx.close()
        await b.close()
    bad = [n for n, c, e in R if not c]
    print(f'\n{len(R)-len(bad)}/{len(R)} passed'); 
    if bad: print('FAILED:', bad); sys.exit(1)
asyncio.run(main())
