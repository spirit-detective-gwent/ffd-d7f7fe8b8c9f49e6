#!/workspace/pwenv/bin/python3
"""Ch1 crafting-supply test (v6564-craft).
usage: test_supply.py <worktree> [port] [--shot PATH] [--base <old worktree>]
Runs the REAL game functions in a headless 390x844 page:
  - simulates a thorough Ch1 (lesson + safe kits + wall kits + 4 minis + N street foes) and reports total mats / dressings (target 15-18)
  - checks 8% street drops (Ch1) / 4% (Ch2), bosses drop nothing, mini first-win = 1 (Ch1) / 2 (Ch2)
  - checks quest hand-ins give no mats in Ch1, the nurse (no restock, no post-KO mats, lesson still 1+1)
  - checks the dressing cap (5), the '+1 Gauze' popup (queued until the world is back), and scarcity removal incl. loading an old scarce save
  - with --base: measures the same street/mini/quest numbers on the old tree for the before/after table"""
import asyncio, sys, functools, http.server, socketserver, threading, re, json
from pathlib import Path
from playwright.async_api import async_playwright
args = [a for a in sys.argv[1:]]
def opt(name):
    if name in args:
        i = args.index(name); v = args[i + 1]; del args[i:i + 2]; return v
shot = opt('--shot'); base = opt('--base')
root = Path(args[0]); PORT = int(args[1]) if len(args) > 1 else 52611
FOES = 48   # street foes a thorough Ch1 fights (every roaming/lane/dungeon bully)
RUNS = 600
class TS(socketserver.ThreadingTCPServer): allow_reuse_address = True; daemon_threads = True
def serve(rt, port):
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_GET(self):
            if self.path.split('?', 1)[0] in ('/', '/index.html'):
                raw = (rt / 'index.html').read_bytes(); n = b'root.WORLD_API = {'
                raw = raw.replace(n, b'root.__ev=function(s){return eval(s)};' + n, 1)
                self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(raw))); self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(raw); return
            return super().do_GET()
    h = TS(('127.0.0.1', port), functools.partial(Q, directory=str(rt))); threading.Thread(target=h.serve_forever, daemon=True).start(); return h
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
async def ev(pg, code):
    return await pg.evaluate("(c)=>{try{var r=__ev(c);return (r===undefined)?null:JSON.parse(JSON.stringify(r))}catch(e){return {__err:String(e&&e.message||e)}}}", code)
async def skipall(pg, n=12):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(300); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(280)
    await pg.evaluate("(()=>{var b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Close'&&e.offsetParent);if(b)b.click()})()")
RES = []
def ok(name, cond, extra=''):
    RES.append((bool(cond), name, extra)); print(('PASS ' if cond else 'FAIL ') + name + ((' :: ' + str(extra)[:300]) if extra else ''), flush=True)
async def boot(p, port, init=None):
    b = await p.chromium.launch(headless=True, args=['--disable-dev-shm-usage'])
    ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True,
      user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mobile/15E148 Safari/604.1')
    if init: await ctx.add_init_script(init)
    pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    await pg.goto(f'http://127.0.0.1:{port}/index.html'); await pg.wait_for_timeout(3500)
    await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(2500); await skipall(pg, 12)
    return b, ctx, pg, errs
# in-page helpers (silence save during Monte Carlo; reset mats)
HELP = """
window.__T = {
  quiet: function(f){ var s0 = save; save = function(){}; try { return f(); } finally { save = s0; } },
  reset: function(){ SAVE.herbs = {gauze:0,tape:0,leaf:0,ginger:0}; SAVE.heal = []; },
  mats: function(){ return phMatN('gauze') + phMatN('tape'); }
};
"""
# measured sources, ONE run, real code. Returns per-source counts.
ONE = """(function(a){ var FOES=a.foes, o={}, T=window.__T; return T.quiet(function(){
  var ch0 = SAVE.chapter; SAVE.chapter = 1; SAVE.craft = SAVE.craft || {}; SAVE.mb = SAVE.mb || {};
  T.reset(); var tot = {};
  function mark(k, f){ var b = T.mats(); f(); tot[k] = T.mats() - b; }
  mark('lesson', function(){ SAVE.sc = SAVE.sc || {}; SAVE.sc.dress = 'fetch'; v630DressFetch(); });
  mark('safe_kits', function(){ (a.safe||[]).forEach(function(k){ phMatAdd(k, 1); }); });
  mark('wall_kits', function(){ (WKIT_TABLE.wall||[]).forEach(function(w){ (wkitGive(w.id)||[]).forEach(function(k){ phMatAdd(k,1); }); }); });
  mark('minis', function(){ ['mb_lib','mb_art','mb_cafe','mb_field'].forEach(function(m){ healDrops({mini:m, foes:[1]}, {firstMini:true}); }); });
  mark('quests', function(){ for (var i=0;i<(a.relays||4);i++) qReward(); });
  mark('street', function(){ for (var i=0;i<FOES;i++) healDrops({foes:[1]}, {}); });
  var g = phMatN('gauze'), t = phMatN('tape'); SAVE.chapter = ch0;
  return {tot: tot, g: g, t: t, mats: g + t, dress: Math.min(g, t)};
}); })"""
async def free_world(pg):
    """Clear the opening scene so the screenshot shows the plain world."""
    await ev(pg, "(function(){ W.scGen=(W.scGen|0)+1; try{sLock(0,'x')}catch(e){} try{close()}catch(e){} W.cut=false; W.dlg=false; W.scr=false; W.busy=false; document.body.classList.remove('fff-dlg-on'); })()")
    for _ in range(40):
        d = await ev(pg, "({dlg:W.dlg,cut:!!W.cut,cls:document.body.className})")
        if not d['dlg'] and not d['cut'] and 'fff-dlg-on' not in d['cls']: break
        await pg.evaluate("(()=>{var b=[...document.querySelectorAll('button')].find(e=>/^(OK|Next|Skip|Close)/.test(e.textContent.trim())&&e.offsetParent);if(b)b.click()})()"); await pg.wait_for_timeout(500)
    await pg.wait_for_timeout(800)
async def main():
    h = serve(root, PORT)
    html = (root / 'index.html').read_text(encoding='utf-8')
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p, PORT)
        await ev(pg, HELP)
        # ---------- scarcity removed ----------
        ok('source: no koDropScarce / gpItem / SAVE.itemScarce branches', not re.search(r'koDropScarce|gpItem|wkitScarceOn|wkitSeed|scarceStocked', html) and len(re.findall(r'itemScarce', html)) <= 2, re.findall(r'.{30}itemScarce.{30}', html)[:3])
        await ev(pg, "phOpenSettings('world')"); await pg.wait_for_timeout(600)
        txt = await pg.evaluate("document.body.innerText")
        ok('Settings has no Item scarcity row', 'scarcity' not in txt.lower(), [l for l in txt.split('\n') if 'scar' in l.lower()])
        ok('SAVE has no itemScarce/itemSeed', await ev(pg, "!('itemScarce' in SAVE) && !('itemSeed' in SAVE)"))
        await ev(pg, "(function(){var b=document.querySelector('#settings .back'); if(b) b.click();})()")
        await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(800); await skipall(pg, 4)
        # ---------- street / mini / boss rates ----------
        r = await ev(pg, """(function(){ return __T.quiet(function(){ var out={}; SAVE.chapter=1; SAVE.mb=SAVE.mb||{};
          function rate(ch, st, res, N){ SAVE.chapter=ch; var hits=0, kinds={gauze:0,tape:0}; for (var i=0;i<N;i++){ __T.reset(); healDrops(st,res); var m=__T.mats(); hits+=m; } return hits/N; }
          out.ch1=rate(1,{foes:[1]},{},6000); out.ch2=rate(2,{foes:[1]},{},6000);
          out.boss=rate(1,{boss:1,foes:[1]},{},300); out.mini1=rate(1,{mini:'mb_lib',foes:[1]},{firstMini:true},50); out.mini1rep=rate(1,{mini:'mb_lib',foes:[1]},{firstMini:false},50);
          out.mini2=rate(2,{mini:'mb2_x',foes:[1]},{firstMini:true},50); out.c2boss=rate(2,{ctx:{c2boss:1},foes:[1]},{},300);
          SAVE.chapter=1; return out; }); })()""")
        print('rates', r)
        ok('Ch1 street drop = 8% per foe', 0.065 <= r['ch1'] <= 0.095, r['ch1'])
        ok('Ch2 street drop stays 4%', 0.03 <= r['ch2'] <= 0.052, r['ch2'])
        ok('Boss / Ch2 boss drop nothing', r['boss'] == 0 and r['c2boss'] == 0, (r['boss'], r['c2boss']))
        ok('Ch1 mini first win = 1 material; repeat = 0; Ch2 mini = 2', r['mini1'] == 1 and r['mini1rep'] == 0 and r['mini2'] == 2, (r['mini1'], r['mini1rep'], r['mini2']))
        # balanced kind: 1 foe at a time never lets one kind run away
        bal = await ev(pg, """(function(){ return __T.quiet(function(){ SAVE.chapter=1; __T.reset(); root.FFF_MAT_ROLL=0; for (var i=0;i<20;i++) healDrops({foes:[1]},{}); root.FFF_MAT_ROLL=null; return [phMatN('gauze'),phMatN('tape')]; }); })()""")
        ok('forced drops balance gauze/tape', bal and abs(bal[0] - bal[1]) <= 1, bal)
        # ---------- quest rewards ----------
        q = await ev(pg, """(function(){ return __T.quiet(function(){ SAVE.chapter=1; __T.reset(); var s=qReward(); var a=__T.mats(); var rm=rewardMain('q_relay1')||''; SAVE.chapter=2; __T.reset(); var s2=qReward(); var b=__T.mats(); SAVE.chapter=1; return {ch1:a, s:s, rm:rm, ch2:b}; }); })()""")
        ok('Ch1 quest hand-in gives no gauze/tape/bandage; text matches', q['ch1'] == 0 and not re.search(r'gauze|tape|bandage', q['s'] + q['rm'], re.I), q)
        ok('Ch2 quest hand-in unchanged (+band mats)', q['ch2'] >= 2, q)
        # ---------- nurse ----------
        n = await ev(pg, """(function(){ return __T.quiet(function(){ SAVE.chapter=1; SAVE.sc=SAVE.sc||{}; SAVE.sc.dress='x'; __T.reset(); delete SAVE.cabT; n9Cabinet(); var a=__T.mats(); var cab=SAVE.cabT; var d=document.getElementById('wdlg'); var t=d?d.innerText:''; if (typeof dlgClose==='function') try{dlgClose()}catch(e){}; W.dlg=false; return {mats:a, cabT:cab||null, txt:t}; }); })()""")
        ok('Nurse cabinet no longer restocks', n['mats'] == 0 and not n['cabT'], n)
        ok('source: no post-KO nurse mats text / grant', 'She sets out 1 gauze' not in html and "koGrantMat('gauze', 1)" not in html)
        les = await ev(pg, """(function(){ return __T.quiet(function(){ SAVE.chapter=1; __T.reset(); SAVE.sc={dress:'fetch'}; n9Cabinet(); var m=[phMatN('gauze'),phMatN('tape')]; try{ if(typeof sceneEnd==='function') sceneEnd(); }catch(e){} W.dlg=false; W.paused=false; return m; }); })()""")
        ok('Dressing lesson still gives 1 gauze + 1 tape', les == [1, 1], les)
        # ---------- kits ----------
        safe = re.findall(r"kit: \{ id: 'kit[A-Z]', r: \[[^\]]*\], at: \[[^\]]*\], give: \[([^\]]*)\]", html)
        sk = [re.findall(r"'(\w+)'", s)[0] for s in safe]
        ok('six safe-room kits hold 1 piece each (3 gauze + 3 tape)', len(safe) == 6 and all(len(re.findall(r"'", s)) == 2 for s in safe) and sk.count('gauze') == 3 and sk.count('tape') == 3, sk)
        wall = await ev(pg, "(WKIT_TABLE.wall||[]).map(function(w){return [w.id, wkitGive(w.id)]}).filter(function(x){return x[1].length})")
        ntab = await ev(pg, "(WKIT_TABLE.wall||[]).length")
        ok('wall kits: only %d of %d hold a piece (1 each)' % (len(wall), ntab), 1 <= len(wall) <= 3, wall)
        # an unstocked wall kit takes the existing empty path
        e = await ev(pg, "(function(){var w=(WKIT_TABLE.wall||[]).filter(function(w){return !wkitGive(w.id).length})[0]; return w? {id:w.id, give:wkitGive(w.id), stocked:wkitIsStocked(w.id)}:null})()")
        ok('unstocked wall kit reads as empty (existing open_empty path)', e and e['give'] == [] and not e['stocked'], e)
        # ---------- cap ----------
        c = await ev(pg, """(function(){ return __T.quiet(function(){ SAVE.chapter=1; SAVE.craft={dress:1,potion:1}; var o={}; __T.reset(); SAVE.herbs={gauze:20,tape:20,leaf:3,ginger:3};
          var need=craftNeedOf('dress'); o.max0=phCraftMax(need);
          SAVE.heal=['dress','dress','dress','dress','dress']; o.max5=phCraftMax(need); var before=SAVE.heal.length; W.phQty={dress:1,potion:1}; phDoCraft('dress'); o.after=SAVE.heal.length; o.mats=[phMatN('gauze'),phMatN('tape')];
          o.potion=phCraftMax(craftNeedOf('potion')); o.html=phCraft().indexOf('Dressing bag is full')>=0;
          SAVE.heal=['dress','dress','dress','dress','dress','dress','dress']; o.max7=phCraftMax(need); o.keep7=SAVE.heal.length;
          SAVE.heal=['dress','dress','dress','dress']; o.max4=phCraftMax(need);
          SAVE.heal=[]; o.maxEmpty=phCraftMax(need); return o; }); })()""")
        ok('cap: empty bag crafts up to 5; at 5 crafts none; 4 -> 1', c['max0'] == 5 and c['max5'] == 0 and c['max4'] == 1 and c['maxEmpty'] == 5, c)
        ok('cap: craft blocked at 5, materials stay, message shown, potions unaffected', c['after'] == 5 and c['mats'] == [20, 20] and c['html'] and c['potion'] == 3, c)
        ok('cap: a save with 7 keeps all 7 but cannot craft', c['max7'] == 0 and c['keep7'] == 7, c)
        # ---------- thorough Ch1 sim ----------
        safe_list = sk
        tot = []; per = {}
        for k in range(RUNS):
            pass
        res = await ev(pg, "(function(){var a=%s; var N=%d, sum=0, mn=1e9, mx=0, ds=0, per={}, hist={}; for (var i=0;i<N;i++){ var r=(%s)(a); sum+=r.mats; ds+=r.dress; mn=Math.min(mn,r.mats); mx=Math.max(mx,r.mats); hist[r.mats]=(hist[r.mats]||0)+1; for (var k in r.tot) per[k]=(per[k]||0)+r.tot[k]; } for (var k in per) per[k]=+(per[k]/N).toFixed(2); return {mean:+(sum/N).toFixed(2), dress:+(ds/N).toFixed(2), min:mn, max:mx, per:per, hist:hist}; })()" % (json.dumps({'foes': FOES, 'safe': safe_list, 'relays': 4}), RUNS, ONE))
        print('THOROUGH CH1 (%d street foes, %d runs):' % (FOES, RUNS), json.dumps(res))
        ok('thorough Ch1: mean total materials 15-18', 15 <= res['mean'] <= 18.5, res)
        ok('thorough Ch1: mean dressings craftable 7-9 (= min(gauze,tape))', 6.5 <= res['dress'] <= 9.5, res['dress'])
        # ---------- popup ----------
        await free_world(pg)
        pop = await ev(pg, """(function(){ SAVE.chapter=1; __T.reset(); var f=document.getElementById('wmatpop'); if(f) f.remove(); W.matPopQ=[]; W.on=false; root.FFF_MAT_ROLL=0; root.FFF_MAT_KIND='gauze'; healDrops({foes:[1]},{}); root.FFF_MAT_ROLL=null; root.FFF_MAT_KIND=null; return {queued:(W.matPopQ||[]).length, shown:!!document.getElementById('wmatpop')&&document.querySelectorAll('#wmatpop .mp').length}; })()""")
        ok('popup waits (queued) while the result screen covers the world', pop['queued'] == 1 and not pop['shown'], pop)
        await ev(pg, "W.on=true"); await pg.wait_for_timeout(1300)
        pp = await pg.evaluate("""()=>{var e=document.querySelector('#wmatpop .mp'); if(!e) return null; var r=e.getBoundingClientRect(), s=getComputedStyle(e.parentNode), c=getComputedStyle(e); var top=document.elementFromPoint(r.x+r.width/2, r.y+r.height/2); return {t:e.textContent, x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height), pe:s.pointerEvents, op:c.opacity, hit:top&&top.closest('#wmatpop')?'blocks':'passes'}}""")
        ok("popup reads '+1 Gauze' and never blocks a tap", pp and pp['t'] == '+1 Gauze' and pp['pe'] == 'none', pp)
        if shot:
            await pg.screenshot(path=shot); print('screenshot', shot)
        await pg.wait_for_timeout(2600)
        gone = await pg.evaluate("document.querySelectorAll('#wmatpop .mp').length")
        ok('popup clears itself (no stuck element)', gone == 0, gone)
        # a Tape one for the label
        await ev(pg, "(function(){ root.FFF_MAT_KIND='tape'; root.FFF_MAT_ROLL=0; healDrops({foes:[1]},{}); root.FFF_MAT_ROLL=null; root.FFF_MAT_KIND=null; })()"); await pg.wait_for_timeout(700)
        ok("popup reads '+1 Tape'", await pg.evaluate("[...document.querySelectorAll('#wmatpop .mp')].some(e=>e.textContent==='+1 Tape')"))
        ok('no page errors in the run', not errs, errs[:3])
        await b.close()
        # ---------- old save with scarcity set loads clean ----------
        init = """(function(){ try{ var w=JSON.parse(localStorage.getItem('fff_world')||'null'); }catch(e){} })();"""
        b, ctx, pg, errs = await boot(p, PORT)
        await ev(pg, "(function(){ SAVE.itemScarce='scarce'; SAVE.itemSeed=777; ST.set.itemScarce='scarce'; SAVE.herbs={gauze:2,tape:1}; save(); try{localStorage.setItem('fff_set', JSON.stringify(ST.set))}catch(e){} })()")
        raw = await pg.evaluate("localStorage.getItem('fff_world')")
        ok('old save really carries itemScarce before reload', raw and 'scarce' in raw)
        await pg.reload(); await pg.wait_for_timeout(3500); await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(2500); await skipall(pg, 6)
        o = await ev(pg, "({sc:SAVE.itemScarce||null, seed:SAVE.itemSeed||null, setsc:(ST.set&&ST.set.itemScarce)||null, g:phMatN('gauze'), t:phMatN('tape')})")
        ok('old scarce save loads as normal (keys dropped, mats kept)', o['sc'] is None and o['seed'] is None and o['setsc'] is None and o['g'] == 2 and o['t'] == 1, o)
        await ev(pg, HELP)
        rr = await ev(pg, """(function(){ return __T.quiet(function(){ SAVE.chapter=1; var h=0; for (var i=0;i<4000;i++){ __T.reset(); healDrops({foes:[1]},{}); h+=__T.mats(); } return h/4000; }); })()""")
        ok('old scarce save: street drop is the normal 8%', 0.065 <= rr <= 0.095, rr)
        ok('old-save run: no page errors', not errs, errs[:3])
        await b.close()
        # ---------- before numbers from the old tree ----------
        if base:
            bp = Path(base); h2 = serve(bp, PORT + 1)
            b, ctx, pg, errs = await boot(p, PORT + 1); await ev(pg, HELP)
            ob = await ev(pg, """(function(){ return __T.quiet(function(){ var o={}; SAVE.chapter=1; SAVE.mb=SAVE.mb||{}; var N=4000, h=0; for (var i=0;i<N;i++){ __T.reset(); healDrops({foes:[1]},{}); h+=__T.mats(); } o.street_rate=h/N; __T.reset(); healDrops({mini:'mb_lib',foes:[1]},{firstMini:true}); o.mini_healDrops=__T.mats(); __T.reset(); for (var i=0;i<4;i++) qReward(); o.quest4=__T.mats();
              o.kitsWall=(WKIT_TABLE.wall||[]).reduce(function(a,w){return a+(w.normal&&w.normal.gauze||0)+(w.normal&&w.normal.tape||0)},0); return o; }); })()""")
            print('BEFORE (old tree measured):', json.dumps(ob)); await b.close()
    bad = [r for r in RES if not r[0]]
    print('\n%d/%d passed' % (len(RES) - len(bad), len(RES)))
    sys.exit(1 if bad else 0)
asyncio.run(main())
