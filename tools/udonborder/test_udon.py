#!/workspace/pwenv/bin/python3
"""v6.5.66 udon / border tests (t612u): door alignment, beat lock release (3 paths), reload mid-beat, watchdog, east row, Wagashi.
Usage: test_udon.py [index.html]  (needs playwright; serves the index's folder)."""
import asyncio, sys, os, json, functools, http.server, socketserver, threading, socket
from pathlib import Path
from playwright.async_api import async_playwright
INDEX = Path(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', '..', 'index.html')).resolve()
NX = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^(Next|Skip|Continue|OK)/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
SK = NX.replace('Next|Skip|Continue|OK', 'Skip')
HUSH = "(function(){try{if(typeof phClose==='function')phClose()}catch(e){}W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};return 1})()"
SETUP = """(function(){SAVE.chapter=2;SAVE.ch1=1;SAVE.ch2=1;SAVE.bond=SAVE.bond||{};SAVE.bond.path='%(path)s';SAVE.bond.lock=1;try{STORY.ensure(SAVE)}catch(e){}
var st=c2S();st.e=st.e||{};st.e.arrive=1;st.e.gymIn=1;st.e.genji=1;st.e.c2sRep=1;st.e.roam=1;st.e.called=1;st.e.c2lMap=1;st.e.sealKnown=1;
st.q.cq2_arrive=9;st.q.cq2_hq=9;st.q.cq2_scout=9;st.q.cq2_locks=0;st.qa='cq2_locks';
st.e.run_fac='arc';st.e.n13='done';st.q.cq2_n_look=9;st.e.n13corner='bat';st.e.nq=%(nq)s;
try{c2QSync();save()}catch(e){} return 1})()"""
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True; daemon_threads = True
R = []
def chk(name, ok, info=''):
    R.append(bool(ok)); print(('PASS ' if ok else 'FAIL ') + name + (' :: ' + str(info) if info and not ok else ''), flush=True)
class G:
    async def start(self, p, path='balanced', nq='{}', at=(950, 3380), vw=390, vh=844, extra=''):
        self.errs = []
        self.pg = await self.ctx.new_page() if False else await p.new_page(viewport={'width': vw, 'height': vh}, is_mobile=True, has_touch=True)
        self.pg.on('pageerror', lambda e: self.errs.append(str(e)))
        html = INDEX.read_text(encoding='utf-8').replace('root.FFF_13U = { CONTEST', 'root.__ev=function(s){return eval(s)};root.FFF_13U = { CONTEST', 1)
        async def rt(route): await route.fulfill(body=html, content_type='text/html')
        await self.pg.route('**/index.html', rt)
        await self.pg.goto(f'http://127.0.0.1:{PORT}/index.html', timeout=120000); await self.pg.wait_for_timeout(2200)
        await self.boot(path, nq, at, extra)
    async def ev(self, c):
        return await self.pg.evaluate("(c)=>{var r=window.__ev(c);try{return (typeof r==='string')?r:JSON.parse(JSON.stringify(r===undefined?null:r))}catch(e){return String(r)}}", c)
    async def wait(self, ms): await self.pg.wait_for_timeout(ms)
    async def skipall(self, n=8):
        for i in range(n):
            c = await self.pg.evaluate(SK)
            if not c:
                await self.wait(200); c = await self.pg.evaluate(SK)
                if not c: break
            await self.pg.touchscreen.tap(*c); await self.wait(200)
    async def boot(self, path, nq, at, extra=''):
        pg = self.pg
        await pg.touchscreen.tap(195, 420); await pg.evaluate("WORLD_API.enter(true)"); await self.wait(1500); await self.skipall()
        await self.ev("root.FFF_NO_TUT=1"); await pg.evaluate("WORLD_API.c2Begin(true)"); await self.wait(2500); await self.skipall(); await self.ev(HUSH)
        await self.ev("""(function(){if(window.__hk)return;window.__hk=1;window.__evs=[];var e0=ev;ev=function(k){try{if(/world:nq/.test(k))window.__evs.push(k)}catch(e){}return e0.apply(this,arguments)}})()""")
        await self.ev(SETUP % {'path': path, 'nq': nq})
        if extra: await self.ev(extra)
        await self.go(*at)
    async def go(self, x, y):
        await self.ev("(function(){c2Go('town',[%d,%d,0]);try{c2Pop()}catch(e){}W.ryo.x=%d;W.ryo.y=%d;place(W.ryo,0);W.aoi.x=%d;W.aoi.y=%d;place(W.aoi,0);camera(true)})()" % (x, y, x, y, x - 60, y + 30))
        await self.wait(1500); await self.ev(HUSH)
    async def adv_until(self, js, n=80):
        for i in range(n):
            if await self.ev(js): return i
            c = await self.pg.evaluate(NX)
            if c: await self.pg.touchscreen.tap(*c)
            await self.wait(400)
        return -1
FREE = "(!W.cut&&!W.dlg&&!(W.scr|0)&&!document.getElementById('nqsting')&&!(document.getElementById('wdlg')||{className:''}).className.match(/(^| )on( |$)/))"
async def moves(g):
    x0 = await g.ev("W.ryo.x"); await g.pg.keyboard.down('ArrowLeft'); await g.wait(700); await g.pg.keyboard.up('ArrowLeft'); x1 = await g.ev("W.ryo.x"); return x0 - x1
async def main():
    global PORT
    s = socket.socket(); s.bind(('127.0.0.1', 0)); PORT = s.getsockname()[1]; s.close()
    srv = TS(('127.0.0.1', PORT), functools.partial(Q, directory=str(INDEX.parent))); threading.Thread(target=srv.serve_forever, daemon=True).start()
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required'])
        # ---- 1. door alignment (udon + Machi) ----
        g = G(); await g.start(b, nq='{udon:1,udonFin:1,won:{udon:1}}')
        r = await g.ev("""(function(){var o={};var bl=C2W.bld.filter(function(b){return b.id==='udon'||b.id==='garage'||b.id==='eastS'||b.id==='shopsE'})
          o.bld=bl.map(function(b){return b.id+':'+b.r.join(',')});var D=FFF_NQ.P;
          var sp=INT.c2_town.spots.filter(function(s){return /^nq_e_(udon|motors)$/.test(s.id)});o.sp=sp.map(function(s){return [s.id,s.r,s.at,s.lab,!!TRANS[s.id]]});
          var f=[...layer.querySelectorAll('canvas.nqprop')].filter(function(c){return c.width===220&&c.height===104});o.front=f.map(function(c){return [parseFloat(c.style.left),parseFloat(c.style.top),c.width,c.height]});
          o.tag=tagDefs().filter(function(t){return /nq_e_udon/.test(t.key)}).map(function(t){return [t.lab,t.x,t.y]});
          o.bench=(C2W.props.place||[]).filter(function(q){return q[0]==='bench'&&q[2]===3330}).map(function(q){return q[1]});
          o.walk=[[950,3340],[950,3320],[925,3340],[975,3340]].map(function(p){return WORLD_API.walkableAt(p[0],p[1])});return o})()""")
        u = [bb for bb in r['bld'] if bb.startswith('udon:')][0]; ub = [int(v) for v in u.split(':')[1].split(',')]
        sp = {x[0]: x for x in r['sp']}; d = sp['nq_e_udon']; fr = r['front'][0] if r['front'] else None
        chk('udon: door rect sits on the udon building (x inside, bottom at its wall)', ub[0] <= d[1][0] and d[1][2] <= ub[2] and d[1][3] <= 3300 and d[1][3] > 3250, (ub, d[1]))
        chk('udon: open shopfront is painted over the door (door centre within the front, front bottom on the wall)', fr and fr[0] <= (d[1][0] + d[1][2]) / 2 <= fr[0] + fr[2] and abs(fr[1] + fr[3] - 3284) < 30, fr)
        chk('udon: Enter spot stands on open sidewalk under the door', d[2][1] <= 3340 and d[2][1] >= 3300 and r['walk'][0] is not False or r['walk'][1] is not False, (d[2], r['walk']))
        chk('udon: word tag "Eat" shows once open', any(t[0] == 'Eat' for t in r['tag']), r['tag'])
        chk('udon: not a silent walk-in (no TRANS)', not d[4], d)
        chk('udon: bench no longer on the door step', r['bench'] and r['bench'][0] > 1000, r['bench'])
        await g.ev("walkTo(950,3260,true,false)")
        i = await g.adv_until("c2Room()==='udon'", 20); chk('udon: tapping the door walks in', i >= 0, await g.ev("c2Room()"))
        chk('udon: interior has the Order spot + exit', await g.ev("INT[W.inside.id].spots.some(function(s){return s.id==='nq_udon_order'})"))
        # tag act
        await g.go(950, 3352); await g.ev("c2ActC('c2_town','nq_e_udon')"); i = await g.adv_until("c2Room()==='udon'", 20); chk('udon: the Eat tag action enters', i >= 0)
        await g.pg.close()
        g = G(); await g.start(b, nq='{}', at=(950, 2700))
        r = await g.ev("[tagDefs().some(function(t){return /nq_e_udon/.test(t.key)}), [...layer.querySelectorAll('canvas.nqprop')].some(function(c){return c.width===220&&c.height===104})]")
        chk('udon: closed (corner not won) shows no Eat tag; shutter is up on the same facade', r[0] is False and r[1] is True, r)
        await g.pg.close()
        # ---- 2. beat lock release, 3 paths ----
        for path in ('fierce', 'strategic', 'balanced'):
            g = G(); await g.start(b, path=path, nq='{}', at=(950, 2900)); await g.ev("W.ryo.x=950;W.ryo.y=3380;place(W.ryo,0);camera(true)")
            i = await g.adv_until("window.__evs.indexOf('world:nq:udon:fin')>=0&&" + FREE, 120); await g.wait(600)
            st = await g.ev("[W.cut,W.dlg,W.scr|0,c2S().q.cq2_nq_west,!FFF_NQ.UDB,c2S().e.nq.udonFin]")
            chk(f'beat[{path}]: runs to the end, free, west quest open', i >= 0 and not st[0] and not st[1] and st[2] == 0 and st[3] == 0 and st[4] and st[5], st)
            m = await moves(g); chk(f'beat[{path}]: player walks afterwards', m > 40, m)
            chk(f'beat[{path}]: no page errors', not g.errs, g.errs[:2]); await g.pg.close()
        # ---- 3. watchdog: leak the lock in every beat step, never stuck ----
        for step in ('talk', 'sting', 'flip'):
            g = G(); await g.start(b, nq='{}', at=(950, 2900)); await g.ev("W.ryo.x=950;W.ryo.y=3380;place(W.ryo,0);camera(true)")
            await g.adv_until("FFF_NQ.UDB&&FFF_NQ.UDB.step==='%s'" % step, 100)
            # simulate a lost callback: kill the scene and leave the locks on
            await g.ev("(function(){W.scGen=(W.scGen|0)+1;try{scKill()}catch(e){};var n=document.getElementById('nqsting');if(n)n.remove();var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};W.cut=true;W.dlg=true;W.scr=1})()")
            await g.wait(5500)
            ue = await g.ev("window.__evs.filter(function(e){return /unstick/.test(e)})")
            await g.adv_until("c2S().q.cq2_nq_west===0&&" + FREE, 80); await g.wait(500)
            st = await g.ev("[W.cut,W.dlg,W.scr|0,c2S().q.cq2_nq_west]")
            chk(f'watchdog[{step}]: lock released by the watchdog within 5.5 s, hand-off completed, free', not st[0] and not st[1] and st[2] == 0 and st[3] == 0 and ue, (st, ue))
            await g.pg.close()
        # idle leak (non-beat): 12 s
        g = G(); await g.start(b, nq='{udon:1,udonFin:1,won:{udon:1}}'); await g.ev("W.cut=true;W.scr=1"); await g.wait(13500)
        chk('watchdog[idle]: a stray lock with nothing on screen frees in 12 s', await g.ev("!W.cut&&(W.scr|0)===0"))
        await g.ev("W.dlg=true;scene(null,[['aoi','hello']],function(){W.dlg=false});"); await g.wait(14000)
        chk('watchdog: a real dialogue is NOT cut off', await g.ev("(document.getElementById('wdlg')||{className:''}).className.indexOf('on')>=0"))
        await g.pg.close()
        # ---- 4. reload mid-beat: saved state e.udon=1 without udonFin ----
        for path in ('fierce', 'balanced'):
            g = G(); await g.start(b, path=path, nq='{udon:1,udonTry:1}', at=(950, 3380)); await g.go(950, 3380)
            i = await g.adv_until("window.__evs.indexOf('world:nq:udon:resume')>=0", 40); chk(f'reload[{path}]: Oda-san steps out again (resume fires)', i >= 0, await g.ev("window.__evs"))
            i = await g.adv_until("window.__evs.indexOf('world:nq:udon:fin')>=0&&" + FREE, 120); await g.wait(500)
            st = await g.ev("[c2S().q.cq2_nq_west,W.cut,W.dlg]")
            chk(f'reload[{path}]: finishes, west quest open, free', i >= 0 and st[0] == 0 and not st[1] and not st[2], st)
            chk(f'reload[{path}]: walks after', (await moves(g)) > 40); await g.pg.close()
        g = G(); await g.start(b, nq='{udon:1,udonTry:3}')
        chk('reload: after 3 tries the old fallback hands the quest off (never stranded)', await g.ev("c2S().q.cq2_nq_west===0||FFF_NQ.stg('west')==='w1'"))
        await g.pg.close()
        # ---- 5. east row ----
        g = G(); await g.start(b, nq='{udon:1,udonFin:1,won:{udon:1}}', at=(4300, 3360), extra="var st=c2S();st.e.seal_sento=1;st.q.cq2_s2_waga=9;if(root.FFF_S2&&root.FFF_S2.setStg)root.FFF_S2.setStg('done');c2QSync();save()")
        r = await g.ev("""(function(){var o={};var P2=FFF_S2P2;o.shop=P2.SHOP_DOOR;o.lob=P2.LOB_DOOR;var e=C2W.bld.filter(function(b){return b.id==='eastS'})[0];o.eastS=e.r;
          var f=document.getElementById('s2MinaSouth');o.fac=f?[parseFloat(f.style.left),parseFloat(f.style.top),f.width,f.height]:null;
          o.walk=[P2.SHOP_DOOR.at,P2.LOB_DOOR.at].map(function(p){return WORLD_API.walkableAt(p[0],p[1])});return o})()""")
        e = r['eastS']; f = r['fac']
        chk('east: Hase / Minato doors are on the eastS building (x inside, bottom at its wall y)', all(e[0] <= d['r'][0] and d['r'][2] <= e[2] and d['r'][3] <= e[3] and d['r'][3] >= e[3] - 40 for d in (r['shop'], r['lob'])), (e, r['shop'], r['lob']))
        chk('east: the Minato-so facade is drawn on the building, bottom flush with its wall (was 200 px under it)', f and f[0] >= e[0] - 1 and abs(f[1] + f[3] - e[3]) <= 4, (f, e))
        chk('east: both door stand points are on the sidewalk (walkable)', all(r['walk']), r['walk'])
        for nm, door, room in (('mshop', 'shop', 'mshop'), ('mina', 'lob', 'mina')):
            await g.go(4300, 3360); at = r[door]['at']; await g.ev("walkTo(%d,%d,true,false)" % (at[0], r[door]['r'][1] + 40)); await g.wait(2500); await g.ev("c2ActC('c2_town','%s')" % ('s2_e_mshop' if door == 'shop' else 's2_e_mina'))
            i = await g.adv_until("c2Room()==='%s'" % room, 30); chk(f'east: tap the {nm} door, then its tag, enters it', i >= 0, await g.ev("c2Room()"))
        await g.pg.close()
        # ---- 6. Wagashi ----
        g = G(); await g.start(b, nq='{udon:1,udonFin:1,won:{udon:1}}', at=(3080, 2700), extra="var st=c2S();st.e.seal_sento=1;st.q.cq2_s2_waga=9;if(root.FFF_S2&&root.FFF_S2.setStg)root.FFF_S2.setStg('done');c2QSync();save()")
        r = await g.ev("""(function(){var o={};o.tree=(C2W.props.place||[]).filter(function(q){return q[0]==='tree'&&q[2]===2700}).map(function(q){return q[1]});o.fac=(function(){var f=document.getElementById('s2WagaDoor');return f?[parseFloat(f.style.left),parseFloat(f.style.top),f.width,f.height]:null})();
          o.pb=(C2W.pblocks||[]).filter(function(b){return b[1]===2684}).map(function(b){return b[0]});o.door=FFF_S2.DOOR;return o})()""")
        chk('wagashi: storefront is drawn', r['fac'] is not None, r)
        chk('wagashi: the lane tree no longer stands in front of the shop (and its trunk block moved too)', r['tree'] and all(x < 2880 or x > 3280 for x in r['tree']) and all(x < 2880 or x > 3280 for x in r['pb']), r)
        chk('wagashi: door rect bottom is on the Lucky 7 wall (2600)', r['door']['r'][3] == 2600, r['door'])
        await g.ev("walkTo(3080,2560,true,false)"); i = await g.adv_until("c2Room()==='waga'", 30); chk('wagashi: tapping the door enters Chiyo Wagashi', i >= 0, await g.ev("c2Room()"))
        await g.go(3080, 3352)
        r = await g.ev("""(function(){var o={};var bl=C2W.bld.filter(function(b){return b.id==='shopsE2'})[0].r;var d=FFF_S2.WAGA_S;o.bld=bl;o.d=d;
          var f=document.getElementById('s2WagaSouth');o.fac=f?[parseFloat(f.style.left),parseFloat(f.style.top),f.width,f.height]:null;
          o.tag=tagDefs().filter(function(t){return /s2_e_waga_s/.test(t.key)}).map(function(t){return t.lab});o.walk=WORLD_API.walkableAt(d.at[0],d.at[1]);return o})()""")
        chk('wagashi south: the SWEETS building (shopsE2) has a door on its wall, painted front + sign, and an open-sidewalk stand point', r['fac'] and r['bld'][0] <= r['d']['r'][0] and r['d']['r'][2] <= r['bld'][2] and r['d']['r'][3] == 3300 and r['fac'][0] <= 3080 <= r['fac'][0] + r['fac'][2] and r['walk'], r)
        chk('wagashi south: word tag "Sweets" shows', r['tag'] == ['Sweets'], r['tag'])
        await g.ev("c2ActC('c2_town','s2_e_waga_s')"); i = await g.adv_until("c2Room()==='waga'", 30); chk('wagashi south: the south door enters Chiyo Wagashi', i >= 0, await g.ev("c2Room()"))
        await g.ev("c2Go('town',[3080,3352,0]);try{c2Pop()}catch(e){}"); await g.wait(1500)
        y = await g.ev("W.ryo.y"); chk('wagashi south: leaving puts you back on the south street (not teleported to the north lane)', y > 3300, y)
        chk('no page errors in the town/east/wagashi checks', not g.errs, g.errs[:2])
        await g.pg.close()
        await b.close()
    srv.shutdown()
    n = sum(R); print(f'RESULT {n}/{len(R)} passed'); sys.exit(0 if n == len(R) else 1)
asyncio.run(main())
