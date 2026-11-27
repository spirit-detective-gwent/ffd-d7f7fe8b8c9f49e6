#!/workspace/pwenv/bin/python3
"""v6564-healstyle checks: Ch2 start dressings, bandage migration, Kampo-lesson conversion + cap, vendor swap,
Ch2 herb drops, clinic fixes (kettle/cot tags, pot depth + footprint). usage: test_healstyle.py <worktree>"""
import asyncio, sys, json, functools, http.server, socketserver, threading
from pathlib import Path
from playwright.async_api import async_playwright
root = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test(e.textContent.trim())&&e.offsetParent);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
HUSH = """()=>{try{if(typeof c2AbortTalk==='function')c2AbortTalk()}catch(e){}try{if(typeof scKill==='function')scKill()}catch(e2){}var A=window.WORLD_API,W=A&&A.W;if(W){W.scGen=(W.scGen|0)+1;W.dlg=false;W.cut=false;W.busy=false;}var d=document.getElementById('wdlg');if(d)d.className='';var t=document.getElementById('c2trans');if(t)t.remove();return 1}"""
def serve():
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_GET(self):
            if self.path.split('?')[0] in ('/', '/index.html'):
                raw = (root / 'index.html').read_bytes(); n = b'var W = { guards: [], paused: false'
                raw = raw.replace(n, b'root.__ev=function(s){return eval(s)};' + n, 1)
                self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.end_headers(); self.wfile.write(raw); return
            return super().do_GET()
    s = socketserver.ThreadingTCPServer(('127.0.0.1', 0), functools.partial(Q, directory=str(root))); s.daemon_threads = True
    threading.Thread(target=s.serve_forever, daemon=True).start(); return s
async def ev(pg, c): return await pg.evaluate("(c)=>{var r=window.__ev(c);return r===undefined?null:JSON.parse(JSON.stringify(r))}", c)
async def skipall(pg):
    for i in range(6):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(700); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(700)
R = []
def ok(name, cond, detail=''):
    R.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + ('' if cond else '  ' + json.dumps(detail)[:400]), flush=True)
async def main():
    s = serve(); url = f'http://127.0.0.1:{s.server_address[1]}/index.html'
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True); pg = await ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        await pg.goto(url); await pg.wait_for_timeout(3500)
        await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(1500); await skipall(pg); await pg.evaluate(HUSH)
        # Ch1: drops stay gauze/tape, migration maps old bandages
        r = await ev(pg, "SAVE.heal=['bandage','candy'];SAVE.craft={};FFF_HS.migrate();[SAVE.heal,SAVE.craft]")
        ok('migrate: old bandage -> dressing, recipe on', r[0] == ['dress', 'candy'] and r[1].get('dress') == 1, r)
        r = await ev(pg, "root.FFF_MAT_P=1;root.FFF_MAT_ROLL=0;SAVE.herbs.gauze=0;SAVE.herbs.tape=0;SAVE.herbs.leaf=0;SAVE.herbs.ginger=0;healDrops({foes:['a','b']},{});var o={g:herbN('gauze'),t:herbN('tape'),l:herbN('leaf'),gi:herbN('ginger')};root.FFF_MAT_P=null;root.FFF_MAT_ROLL=null;o")
        ok('Ch1 drops stay gauze/tape', r['g'] + r['t'] == 2 and r['l'] + r['gi'] == 0, r)
        # Ch2 fresh start
        await pg.evaluate("WORLD_API.c2Begin(true)"); await pg.wait_for_timeout(2500); await skipall(pg); await pg.evaluate(HUSH); await pg.wait_for_timeout(1200)
        r = await ev(pg, "[SAVE.chapter,SAVE.heal,SAVE.craft,FFF_HS.key(),document.querySelectorAll('#wbag .phq').length,(document.querySelector('#wbag .hsrem .hsct')||{}).textContent]")
        ok('Ch2 start: 2 real dressings, one remedy slot 2/5', r[0] == 2 and r[1] == ['dress', 'dress'] and r[2].get('dress') == 1 and r[3] == 'dress' and r[4] == 1 and r[5] == '2/5', r)
        # before the lesson: vendors + drops unchanged
        r = await ev(pg, "FFF_HS.vendors();[SHOPS.nq_gk2.items.map(function(i){return i.id}),SHOPS.nq_motors.items.map(function(i){return i.id}),FFF_S2P2.MENU.map(function(i){return i.id})]")
        ok('before lesson: Ono/Machi/Hase keep tape + gauze', 'gauze' in r[0] and 'tape' in r[1] and 'gauze' in r[2], r)
        r = await ev(pg, "root.FFF_MAT_P=1;root.FFF_MAT_ROLL=0;SAVE.herbs.gauze=0;SAVE.herbs.tape=0;SAVE.herbs.leaf=0;SAVE.herbs.ginger=0;healDrops({foes:['a','b','c']},{});var o={g:herbN('gauze'),t:herbN('tape'),l:herbN('leaf'),gi:herbN('ginger')};o")
        ok('before lesson: Ch2 drops gauze/tape', r['g'] + r['t'] == 3, r)
        # conversion + cap (lesson finish path, fast)
        r = await ev(pg, "SAVE.heal=['dress','dress','dress','bandage','candy'];SAVE.herbs.gauze=2;SAVE.herbs.tape=3;SAVE.herbs.leaf=0;SAVE.herbs.ginger=0;SAVE.items=10;SAVE.craft={dress:1,potion:1};delete SAVE.sc.hsSwitch;var o=FFF_HS.convert();[o,SAVE.heal,herbN('leaf'),herbN('ginger'),herbN('gauze'),herbN('tape'),SAVE.items]")
        o, heal = r[0], r[1]
        ok('convert: 4 dressings -> 4 Kampo, 2 sets -> 2+2 herbs, 1 loose -> 1 yen', o['kampo'] == 4 and heal.count('potion') == 4 and 'dress' not in heal and 'bandage' not in heal and 'candy' in heal and r[2] == 2 and r[3] == 2 and r[4] == 0 and r[5] == 0 and r[6] == 11, r)
        r = await ev(pg, "var o=FFF_HS.convert();[o.kampo,o.dress,SAVE.heal.length]")
        ok('convert runs once', r[0] == 0 and r[1] == 0, r)
        r = await ev(pg, "SAVE.heal=['dress','dress','dress','dress','dress','dress','potion','potion'];SAVE.herbs.gauze=0;SAVE.herbs.tape=0;SAVE.herbs.leaf=0;SAVE.herbs.ginger=0;delete SAVE.sc.hsSwitch;var o=FFF_HS.convert();[o,SAVE.heal.filter(function(k){return k==='potion'}).length,herbN('leaf'),herbN('ginger')]")
        ok('cap: 6 dressings + 2 Kampo -> 5 Kampo, 3 over cap -> 3+3 herbs', r[0]['kampo'] == 3 and r[1] == 5 and r[2] == 3 and r[3] == 3, r)
        # after: vendors + drops
        r = await ev(pg, "FFF_HS.vendors();[SHOPS.nq_gk2.items.map(function(i){return [i.id,i.hb,i.base,i.cost]}),SHOPS.nq_motors.items.map(function(i){return i.id}),FFF_S2P2.MENU.map(function(i){return i.id}),SHOPS.s2_hase.items.length]")
        ok('after lesson: Ono sells ginger seeds only (3, 2 after Nails), no ginger / mugwort', r[0] == [['gseed', 'gseed', 3, 2]], r)
        ok('after lesson: Machi keeps cans only, Hase drops medical', r[1] == ['can'] and r[2] == [] and r[3] == 0, r)
        r = await ev(pg, "SAVE.herbs.gauze=0;SAVE.herbs.tape=0;SAVE.herbs.leaf=0;SAVE.herbs.ginger=0;healDrops({foes:['a','b','c']},{});healDrops({mini:1,foes:['m']},{firstMini:1});var o={g:herbN('gauze'),t:herbN('tape'),l:herbN('leaf'),gi:herbN('ginger')};root.FFF_MAT_P=null;root.FFF_MAT_ROLL=null;o")
        ok('after lesson: Ch2 foe + mini drops are leaf/ginger', r['g'] + r['t'] == 0 and r['l'] + r['gi'] >= 4, r)
        r = await ev(pg, "c2Shop('nq_gk2');var t=document.getElementById('wshop').innerText;shopClose();t")
        ok('Ono shop list shows Ginger Seeds only', 'Ginger Seeds' in r and 'Ginger Root' not in r and 'Mugwort' not in r and 'Gauze' not in r, r[:200])
        r = await ev(pg, "SAVE.craft={dress:1,potion:1};FFF_HS.vendors();var o=[];try{if(window.FFF_S2MENUS&&FFF_S2MENUS.open){FFF_S2MENUS.open('s2_hase');}else{c2Shop('s2_hase');}var e=document.getElementById('wshop')||document.querySelector('.s2m');o=[e?e.innerText:''];}catch(x){o=['ERR '+x]}try{shopClose()}catch(y){}o")
        ok('Hase menu after lesson: no medical stock rendered', 'into your pouch' not in r[0] and 'Electrical tape' not in r[0] and 'HASE' in r[0], r[0][:200] if r else r)
        r = await ev(pg, "SAVE.craft={dress:1,potion:1};SAVE.herbs.gauze=0;SAVE.herbs.tape=0;var l=herbN('leaf'),g=herbN('ginger');var s=qReward();[herbN('gauze'),herbN('tape'),herbN('leaf')-l,herbN('ginger')-g,s]")
        ok('after lesson: a quest pays 1 mugwort + 1 ginger, not gauze/tape', r[0] == 0 and r[1] == 0 and r[2] == 1 and r[3] == 1 and 'Gauze' not in str(r[4]), r)
        r = await ev(pg, "[hsHerbMark(c2Cyc()),'s'+c2Seals()]")
        ok('after lesson: wild ginger regrow mark = seal count', r[0] == r[1], r)
        # stations + mini game + beat wrap
        r = await ev(pg, "SAVE.heal=['potion','potion','potion'];SAVE.herbs.leaf=5;SAVE.herbs.ginger=5;FFF_HS.station('potion');var t=document.getElementById('hsst').innerText;FFF_HS.stClose();[t,W.dlg]")
        ok('bowl station: Kampo recipe, cap leaves room for 2', 'Brewing Bowl' in r[0] and 'Room for 2 more' in r[0] and 'Mugwort' in r[0] and r[1] is False, r)
        r = await ev(pg, "root.FFF_HS_MG_FAST=1;root.FFF_HS_MG_FORCE=1;FFF_HS.mini('potion',2);var m=document.getElementById('hsmg');function tap(){var b=document.querySelector('#hsmg .tap');b.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}))};tap();1")
        await pg.wait_for_timeout(100)
        r = await ev(pg, "root.FFF_HS_MG_FORCE=0;var b=document.querySelector('#hsmg .tap');b.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));1"); await pg.wait_for_timeout(150)
        r = await ev(pg, "var t=(document.getElementById('hsmg')||{}).innerText||'';var b=document.querySelector('#hsmg .tap');if(b)b.click();root.FFF_HS_MG_FORCE=null;root.FFF_HS_MG_FAST=null;[SAVE.heal.filter(function(k){return k==='potionF'}).length,SAVE.heal.filter(function(k){return k==='potion'}).length,herbN('leaf'),herbN('ginger'),t]")
        ok('mini game: 1 Fine + 1 normal brewed, mats spent, result card', r[0] == 1 and r[1] == 4 and r[2] == 3 and r[3] == 3 and 'Fine Kampo' in r[4], r)
        r = await ev(pg, "FFF_HS.station('potion');var t=document.getElementById('hsst').innerText;FFF_HS.stClose();t")
        ok('station at the cap: craft disabled', 'Carrying 5/5' in r, r[:200])
        r = await ev(pg, "SAVE.heal=['potion'];SAVE.hp=10;hud();root.FFF_HS_BEAT_T=1600;FFF_HS.use();var o=document.getElementById('hsbw');o.querySelector('.sk').dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));1"); await pg.wait_for_timeout(250)
        r = await ev(pg, "[SAVE.hp,Math.ceil(MAXHP*0.25*(1+gearFx('hb'))),SAVE.heal.length,!!document.getElementById('hsbw')]")
        ok('beat wrap: Skip = the full item heal', r[0] == 10 + r[1] and r[2] == 0 and not r[3], r)
        r = await ev(pg, "SAVE.heal=['potion'];SAVE.hp=10;hud();root.FFF_HS_BEAT_WIN=1e9;FFF_HS.use();var o=document.getElementById('hsbw');o.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));1"); await pg.wait_for_timeout(700)
        r = await ev(pg, "root.FFF_HS_BEAT_WIN=null;[SAVE.hp,Math.ceil(MAXHP*0.30*(1+gearFx('hb')))]")
        ok('beat wrap: perfect = +5% max HP on top', r[0] == 10 + r[1], r)
        r = await ev(pg, "SAVE.heal=['potion','potionF'];SAVE.hp=MAXHP-3;[FFF_HS.pick('potion')]")
        ok('slot uses the normal one when it covers the missing HP', r[0] == 'potion', r)
        r = await ev(pg, "pause('bag');var t=document.getElementById('wpause').innerText;phClose();t")
        ok('Bag: no Crafting tab', 'Crafting' not in r and 'Items' in r, r[:200])
        r = await ev(pg, "SAVE.craft={dress:1};FFF_HS.vendors();[SHOPS.nq_gk2.items.map(function(i){return i.id}),FFF_S2P2.MENU.length]")
        ok('vendor swap reverts when not learned', 'gauze' in r[0] and r[1] == 2, r)
        src = (root / 'index.html').read_text(encoding='utf-8')
        r = await ev(pg, """(function(){
          SAVE.chapter=2; SAVE.craft={dress:1,potion:1}; MAXHP=MAXHP||46;
          var d=v630Article('food',{id:'heal_dress',ok:true}), p=v630Article('food',{id:'heal_potion',ok:true});
          var n=Math.round(HS_PCT.dress*100), f=Math.round(HS_PCT.dressF*100), pn=Math.round(HS_PCT.potion*100), pf=Math.round(HS_PCT.potionF*100), b=Math.round(HS_BONUS*100);
          var nh=hsHp(HS_PCT.dress), fh=hsHp(HS_PCT.dressF), pnh=hsHp(HS_PCT.potion), pfh=hsHp(HS_PCT.potionF), bh=hsHp(HS_BONUS);
          function ok(h, pcts, hps){ return pcts.every(function(x){return h.indexOf(x)>=0}) && hps.every(function(x){return h.indexOf('+'+x)>=0}) && h.indexOf(String(HS_CAP))>=0 && h.indexOf('hsbig')>=0 && h.indexOf('Fine ones are used first')>=0 && h.indexOf('gold on the gauge')>=0; }
          return {dress: ok(d, [n+'% max HP', f+'%', '+'+b+'% max HP'], [nh, fh, bh]) && d.indexOf('cart in the nurse')>=0,
                  potion: ok(p, [pn+'% max HP', pf+'%', '+'+b+'% max HP'], [pnh, pfh, bh]) && p.indexOf('big bowl')>=0,
                  n:n,f:f,pn:pn,pf:pf,b:b,cap:HS_CAP};
        })()""")
        ok('codex Dressing/Kampo how-to pages use live HS_PCT, HS_CAP, beat bonus + icons', r and r['dress'] and r['potion'], r)
        r2 = await ev(pg, """(function(){ W.cxSel='heal_potion'; SAVE.chapter=2; SAVE.craft={dress:1,potion:1}; var h=v630Section('food'); return [h.indexOf('INGREDIENTS')>=0, h.indexOf('All items')>=0, h.indexOf('Kampo Potion')>=0, h.indexOf('Candy bar')<0, h.indexOf(String(HS_CAP))>=0]; })()""")
        ok('codex remedy opens a detail page (not the full item list)', r2 == [True, True, True, True, True], r2)

        src = (root / 'index.html').read_text(encoding='utf-8')
        ok('hsCxArt reads HS_PCT / HS_CAP / HS_BONUS (not baked-in percents)', 'function hsCxArt' in src and 'Math.round(HS_PCT[k] * 100)' in src and 'Math.round(HS_BONUS * 100)' in src and 'HS_CAP' in src[src.index('function hsCxArt'):src.index('function hsCxArt')+1800], 'hsCxArt missing live constants')
        ok('lessons explain using a remedy (slot tap, ring bonus, Fine first) + Use row on both cards', src.count("tap that slot under your health") == 1 and src.count("tap the slot under your health") == 1 and src.count("<span>Use</span><span>Tap the slot \\u00b7 Fine first</span>") == 2 and 'The Fine ones go first' in src and 'Fine brews go first' in src)
        ok('no stale craft-from-Bag / kettle-for-tea text in Ch1/Ch2', 'The kettle is for tea' not in src and 'Craft potions from your Bag' not in src and 'dressings crafted from your Bag.</p>\' })' not in src and 'gauze and tape in your Bag' not in src)
        ok('garden rare find -> ginger after lesson (source)', "return { k: 'ginger', n: 1, t: 'A ginger root in the mud.' }" in (root / 'index.html').read_text(encoding='utf-8'))
        # clinic fixes
        await pg.evaluate("WORLD_API.c2Go('clinic')"); await pg.wait_for_timeout(2500); await pg.evaluate(HUSH)
        r = await ev(pg, "SAVE.craft={dress:1,potion:1};var D=INT.c2_clinic,T=c2Tags('clinic',D).map(function(t){return t.act&&t.act.int||t.key});T")
        ok('clinic: no cot tag; the bowl is the Brew station after the lesson', not any(('cot' == str(x)) or str(x).endswith(':cot') for x in r) and 'kettle' in r, r)
        r = await ev(pg, "SAVE.craft={dress:1};var D=INT.c2_clinic,T=c2Tags('clinic',D).map(function(t){return t.act&&t.act.int||t.key});SAVE.craft={dress:1,potion:1};T")
        ok('clinic: no bowl tag before the lesson', 'kettle' not in r, r)
        r = await ev(pg, "[INT.c2_clinic.spots.some(function(s){return s.id==='cot'}),INT.c2_clinic.block.some(function(b){return b[0]===140&&b[1]===520})]")
        ok('clinic: cot spot + block gone', r == [False, False], r)
        r = await ev(pg, "(W.g50p||[]).map(function(o){return [o.el.parentNode.id,+o.el.style.zIndex,o.p.at[1],walkableAt(o.x,o.y-6),o.p.kind||'leaf']})")
        ok('clinic: 15 pots (9 mugwort top, 6 ginger bottom) in sprite layer, z = 100 + feet y', len(r) == 15 and sum(1 for q in r if q[4] == 'ginger') == 6 and min(q[2] for q in r if q[4] == 'ginger') > max(q[2] for q in r if q[4] != 'ginger') and all(q[0] == 'wisp' and q[1] == 100 + q[2] for q in r), r)
        ok('clinic: pot footprints are solid', all(q[3] is False for q in r), r)
        r = await ev(pg, "var G=FFF_S2GARDEN;G.potSt('gg1').st='empty';G.pop();SAVE.herbs.seed=2;SAVE.herbs.gseed=0;var o=W.g50p.find(function(q){return q.p.id==='gg1'});W.ryo.x=o.sx;W.ryo.y=o.sy;W.busy=false;W.dlg=false;var a=G.doPot(o,'plant');var m=W.g50p.find(function(q){return q.p.id==='gp1'});G.potSt('gp1').st='empty';[a,herbN('seed'),G.potSt('gg1').st]")
        ok('ginger pot refuses mugwort seed', r[0] is False and r[1] == 2 and r[2] == 'empty', r)
        r = await ev(pg, "var G=FFF_S2GARDEN;SAVE.herbs.gseed=1;var o=W.g50p.find(function(q){return q.p.id==='gg1'});W.ryo.x=o.sx;W.ryo.y=o.sy;W.busy=false;W.dlg=false;G.doPot(o,'plant')")
        await pg.wait_for_timeout(2500); await pg.evaluate(HUSH)
        r = await ev(pg, "var G=FFF_S2GARDEN;[herbN('gseed'),G.potSt('gg1').st,herbN('seed')]")
        ok('ginger pot takes ginger seed', r[0] == 0 and r[1] == 'planted' and r[2] == 2, r)
        r = await ev(pg, "WORLD_API.c2Go('town');1"); await pg.wait_for_timeout(2500)
        r = await ev(pg, "document.querySelectorAll('.g50pot').length")
        ok('pots removed when leaving the clinic', r == 0, r)
        ok('no page errors', not errs, errs)
        # Ch1 nurse office cart
        await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(1200)
        r = await ev(pg, "SAVE.chapter=1;SAVE.craft={dress:1};SAVE.sc.dress='learned';SAVE.heal=[];SAVE.herbs.gauze=2;SAVE.herbs.tape=2;intGo('room');1"); await pg.wait_for_timeout(2500); await pg.evaluate(HUSH); await skipall(pg); await pg.evaluate(HUSH)
        r = await ev(pg, "[!!document.getElementById('hscart'),tagDefs().some(function(t){return t.act&&t.act.int==='dcart'}),walkableAt(335,293)]")
        ok('nurse office: Dressing Cart prop, Craft tag, solid footprint', r == [True, True, False], r)
        r = await ev(pg, "intAct('dcart');var t=(document.getElementById('hsst')||{}).innerText||'';FFF_HS.stClose();t")
        ok('cart opens the Dressing station', 'Dressing Cart' in r and 'Healing Dressing' in r and 'Fine 30%' in r, r[:200])
        await b.close()
    print('PASS: healstyle' if all(R) else 'FAIL: healstyle %d/%d' % (sum(R), len(R)))
    sys.exit(0 if all(R) else 1)
asyncio.run(main())
