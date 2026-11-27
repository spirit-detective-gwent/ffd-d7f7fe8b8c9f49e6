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
        ok('after lesson: Ono sells ginger + dried mugwort (3/2)', r[0] == [['ginger', 'ginger', 3, 2], ['dmug', 'leaf', 3, 2]], r)
        ok('after lesson: Machi keeps cans only, Hase drops medical', r[1] == ['can'] and r[2] == [] and r[3] == 0, r)
        r = await ev(pg, "SAVE.herbs.gauze=0;SAVE.herbs.tape=0;SAVE.herbs.leaf=0;SAVE.herbs.ginger=0;healDrops({foes:['a','b','c']},{});healDrops({mini:1,foes:['m']},{firstMini:1});var o={g:herbN('gauze'),t:herbN('tape'),l:herbN('leaf'),gi:herbN('ginger')};root.FFF_MAT_P=null;root.FFF_MAT_ROLL=null;o")
        ok('after lesson: Ch2 foe + mini drops are leaf/ginger', r['g'] + r['t'] == 0 and r['l'] + r['gi'] >= 4, r)
        r = await ev(pg, "c2Shop('nq_gk2');var t=document.getElementById('wshop').innerText;shopClose();t")
        ok('Ono shop list shows Ginger Root + Dried Mugwort', 'Ginger Root' in r and 'Dried Mugwort' in r and 'Gauze' not in r, r[:200])
        r = await ev(pg, "SAVE.craft={dress:1};FFF_HS.vendors();[SHOPS.nq_gk2.items.map(function(i){return i.id}),FFF_S2P2.MENU.length]")
        ok('vendor swap reverts when not learned', 'gauze' in r[0] and r[1] == 2, r)
        ok('garden rare find -> ginger after lesson (source)', "return { k: 'ginger', n: 1, t: 'A ginger root in the mud.' }" in (root / 'index.html').read_text(encoding='utf-8'))
        # clinic fixes
        await pg.evaluate("WORLD_API.c2Go('clinic')"); await pg.wait_for_timeout(2500); await pg.evaluate(HUSH)
        r = await ev(pg, "SAVE.craft={dress:1,potion:1};var D=INT.c2_clinic,T=c2Tags('clinic',D).map(function(t){return t.act&&t.act.int||t.key});T")
        ok('clinic: no kettle / cot Look tags', not any(('kettle' in str(x)) or ('cot' == str(x)) or str(x).endswith(':cot') for x in r), r)
        r = await ev(pg, "(W.g50p||[]).map(function(o){return [o.el.parentNode.id,+o.el.style.zIndex,o.p.at[1],walkableAt(o.x,o.y-6)]})")
        ok('clinic: 9 pots in sprite layer, z = 100 + feet y', len(r) == 9 and all(q[0] == 'wisp' and q[1] == 100 + q[2] for q in r), r)
        ok('clinic: pot footprints are solid', all(q[3] is False for q in r), r)
        r = await ev(pg, "WORLD_API.c2Go('town');1"); await pg.wait_for_timeout(2500)
        r = await ev(pg, "document.querySelectorAll('.g50pot').length")
        ok('pots removed when leaving the clinic', r == 0, r)
        ok('no page errors', not errs, errs)
        await b.close()
    print('PASS: healstyle' if all(R) else 'FAIL: healstyle %d/%d' % (sum(R), len(R)))
    sys.exit(0 if all(R) else 1)
asyncio.run(main())
