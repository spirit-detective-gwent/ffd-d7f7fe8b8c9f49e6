#!/usr/bin/env python3
"""New Game Plus tests (headless Chromium via Playwright).
Run:  /workspace/pwenv/bin/python tools/ngp/ngp_test.py [index.html]   -> prints PASS/FAIL lines, exit 1 on any FAIL.
  T1 key coverage: every SAVE key the source mentions is either carried by NG+ or declared fresh below (new keys fail until someone decides)
  T2 all 12 options x every choice on a fixture save (pure ngBuild)
  T3 Gang skills 'Learn again': scenes replay, skills grant again; Keep keeps them
  T4 Ch1 -> Ch2 in NG+ (crew rep, snapshots, no stale state), and NG+ started from Ch2 / Ch3
  T5 packs spawn in NG+ like a normal start
  T6 no stray mood object in id arrays / gear.eq
  T7 options screen lists every option (shots in tools/ngp/shots)"""
import asyncio, sys, re, json, functools, http.server, socketserver, threading, os
from pathlib import Path
from playwright.async_api import async_playwright
HERE = Path(__file__).resolve().parent
INDEX = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent.parent / 'index.html'
SHOTS = HERE / 'shots'; SHOTS.mkdir(exist_ok=True)
PORT = 8977
RES = []
def ok(name, cond, extra=''):
    RES.append((bool(cond), name, extra)); print(('PASS ' if cond else 'FAIL ') + name + ((' :: ' + str(extra)[:300]) if (extra and not cond) else ''), flush=True)

# SAVE keys that start FRESH in NG+ on purpose (everything not carried). A key the game starts mentioning that is in neither list fails T1.
FRESH_OK = set('''x y hp sp int deck_ intro mb sc chapter ch1 ch2 ch3 gouki dbl gkPh gkRevives gkPhp gkPsp gkTalk hint freeT patchT patchMig vm dg sq qs qa qOff qTrack qTrackPick stuT
dgRf crewDown splVs bent bx sit wkit find findHi shops carry saved cur svI svW svT act eMoved cabT c2pre c3pre c2entry c3entry c2acc c2own itemScarce_ fights stuT cxSeen_ ds_ ngp
gkTalk cx_ journalLog_ chars_ xp phMig_ itemSeed foeStr_ sodaSeen_ icard_ tips_ svV crewRep_ lpv c2 mealEdge itemScarce cabR supLay'''.split())  # itemScarce: retired by v6564-craft (old saves drop it on load); cabR: v6565-nursecab pending cabinet restock, NG+ starts fresh; supLay: v6565-supplyrooms Ch1 cabinet layout, NG+ rolls a fresh one (kits refill)

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True; daemon_threads = True
def serve(port, directory):
    s = TS(('127.0.0.1', port), functools.partial(Q, directory=str(directory))); threading.Thread(target=s.serve_forever, daemon=True).start(); return s
def body():
    t = INDEX.read_text(encoding='utf-8')
    assert 'root.FFF_13U = { CONTEST' in t
    t = t.replace('root.FFF_13U = { CONTEST', 'root.__ev=function(s){return eval(s)};root.FFF_13U = { CONTEST', 1)
    return t
async def ev(pg, code):
    return await pg.evaluate("(c)=>{var r=window.__ev(c);try{return (typeof r==='string')?r:JSON.parse(JSON.stringify(r===undefined?null:r))}catch(e){return String(r)}}", code)
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
async def skipall(pg, n=6):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(250); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(300)
HUSH = """(function(){try{if(typeof phClose==='function')phClose()}catch(e){}W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};return 1})()"""
async def newpage(p, errs, save=None):
    b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
    ctx = await b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
    pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
    html = body()
    async def rt(route): await route.fulfill(body=html, content_type='text/html')
    await pg.route('**/index.html', rt)
    await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(2500)
    if save is not None: await pg.evaluate("(c)=>localStorage.setItem('fff_world',c)", json.dumps(save))
    return b, pg
async def boot(pg):
    await pg.touchscreen.tap(195, 420)
    await pg.evaluate("WORLD_API.enter(false)"); await pg.wait_for_timeout(1500); await skipall(pg); await ev(pg, HUSH)
    await ev(pg, "root.FFF_NO_TUT=1")

FIXTURE_JS = r"""(function(){
  var S=SAVE; STORY.ensure(S);
  S.items=777; S.ess=55; S.seal=3; S.books={common:2,uncommon:1}; S.heal=['potion','bandage']; S.soda={ramune:3}; S.sodaOn=2; S.sodaK='ramune';
  S.herbs={leaf:4,ginger:3,gauze:2,tape:1,kelp:2,bonito:1,pearl:1}; S.bagUp=2; S.c2hp=6; S.foeStr='strong'; S.wins=9; S.losses=2;
  var ids=Object.keys(GEAR), hd=ids.filter(function(i){return GEAR[i].slot==='head'})[0], ac=ids.filter(function(i){return GEAR[i].slot==='acc'})[0];
  S.gear={own:{},eq:{ryo:{head:hd,acc:ac,tm:'sukajan'},aoi:{head:null,acc:null,tm:null}},later:{},hide:{ryo:{},aoi:{}},v:418,of:{sukajan:1},ofNew:{sukajan:1}}; S.gear.own[hd]=1; S.gear.own[ac]=1;
  S.c2les={assist:1,cover:1,sneak:1}; S.c2lesReady='cover'; S.c2kos=5; S.evoLesson=1;
  S.gsk={hanabi:1,finale:1,alley:1,cheap:1}; S.cxNew={gsk_hanabi:1,gsk_alley:1,mat_x:1}; S.cx={tip_howto:1}; S.tips={howto:1}; S.craft={dress:1,potion:1}; S.journalLog=['Take Down Gouki'];
  S.bond={path:'strategic',px:500,lock:1,ask:1,picks:{first:'fierce'},lq:[]};
  S.dg={c2:{stand:{arc:3,neo:2,bat:1,dep:4},e:{n13alley:1,run_fac:'arc'}}};
  var c=S.cards[0]; c.lp={atk:2}; c.enh=['x']; S.lp={atk:1}; S.sigLv=2; S.lv={a:1};
  var A=freshChar(); STORY.ensure(A); A.cards[0].lp={atk:3}; A.sigLv=1; S.chars={aoi:A};
  S.crewDown={P1:1}; S.splVs={gouki:1}; S.wkit={a:1}; S.find={a:1}; S.bx={a:1}; S.sit={a:1}; S.ch1=1; S.gouki=1; S.ch2=1; S.ch3=1; S.dbl=1; S.mb={gouki:1}; S.sc={ending:1,intro:1}; S.intro=1; S.chapter=2;
  S.c2entry={x:1}; S.c3entry={x:1}; S.c2pre=1; S.c3pre=1; S.carry='crate'; S.qs={sq_x:1}; S.sq={sq_kenta:{st:9}}; S.qa='q'; S.ngp=1;
  return Object.keys(S).length})()"""

def keys_in_source():
    t = INDEX.read_text(encoding='utf-8')
    t = re.sub(r'^[A-Za-z0-9+/=]{200,}$', '', t, flags=re.M)
    return sorted(set(re.findall(r'\bSAVE\.([A-Za-z_][A-Za-z0-9_]*)', t)))

async def t1(pg):
    carried = set(await ev(pg, "Object.keys(FFF_NG.keep).concat(FFF_NG.settings)"))
    fk = set(await ev(pg, "Object.keys(fresh())"))
    # the check ignores method names (SAVE.hasOwnProperty etc.)
    srcs = [k for k in keys_in_source() if k not in ('hasOwnProperty',)]
    unknown = [k for k in srcs if k not in carried and k not in FRESH_OK and k not in fk]
    ok('T1 every SAVE key in the source is carried or declared fresh', not unknown, unknown)
    ok('T1 every fresh() key is carried or declared fresh (or a setting-like key)', not [k for k in fk if k not in carried and k not in FRESH_OK and k not in
       ('binds','padBinds','padRev','pcScale','rumble','autoRun','audioMode','txtSize','musVol','sfxVol','shake','flash','deadz','crewDown','ambRate','itemScarce','xpMode','autoAdv','sort','foeStr','lv','lp','sigLv','ds','nk','deck','own','cards','sodaSeen','gseen','cxItem','cxFood','cxNew','cx','c2pre','crewRep','journalLog','tips','qTrack')], 'see list')
    ok('T1 option registry has 12 options incl. gang', await ev(pg, "FFF_NG.opts.map(function(d){return d.k}).join()") == 'diff,bond,cards,enh,ess,acc,items,yen,level,tech,gang,rep')

def eq(a, b): return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
async def build(pg, **kw):
    js = "(function(){var o=FFF_NG.base();" + ''.join(f"o['{k}']='{v}';" for k, v in kw.items()) + "return JSON.parse(JSON.stringify(FFF_NG.build(SAVE,o)))})()"
    return await ev(pg, js)

async def t2(pg):
    fx = await ev(pg, "JSON.parse(JSON.stringify(SAVE))")
    base = await build(pg)
    # classic: everything carried, everything else fresh
    ok('T2 classic: ngp +1, chapter 1, intro 0, ch1/gouki clear', base['ngp'] == 2 and base['chapter'] == 1 and base['intro'] == 0 and base['ch1'] == 0 and base['gouki'] == 0)
    for k in ['items', 'ess', 'seal', 'heal', 'soda', 'herbs', 'bagUp', 'c2hp', 'gsk', 'c2les', 'c2lesReady', 'c2kos', 'evoLesson', 'cx', 'tips', 'craft', 'journalLog', 'wins']:
        ok(f'T2 classic keeps {k}', eq(base[k], fx[k]), (base[k], fx[k]))
    ok('T2 classic keeps cards+enhancements', eq(base['cards'], fx['cards']) and eq(base['deck'], fx['deck']) and eq(base['lp'], fx['lp']) and base['sigLv'] == 2 and base['cards'][0]['lp'] == {'atk': 2} and base['cards'][0]['enh'] == ['x'])
    ok('T2 classic keeps Aoi (parked char) cards', base['chars']['aoi']['cards'][0]['lp'] == {'atk': 3})
    ok('T2 classic keeps gear incl. outfits', eq(base['gear']['of'], {'sukajan': 1}) and base['gear']['eq']['ryo']['tm'] == 'sukajan')
    ok('T2 classic keeps bond path/px, clears picks and ask', base['bond']['path'] == 'strategic' and base['bond']['px'] == 500 and base['bond']['picks'] == {} and 'ask' not in base['bond'])
    ok('T2 classic crewRep from Ch2 standing', base['crewRep'] == {'arc': 3, 'neo': 2, 'bat': 1, 'dep': 4})
    ok('T2 classic foeStr = difficulty setting', base['foeStr'] in ('normal', 'weak', 'strong', 'max'))
    fresh_fields = {'crewDown': {}, 'splVs': None, 'wkit': {}, 'find': {}, 'bx': {}, 'sit': {}, 'ch2': 0, 'dbl': 0, 'carry': '', 'qs': None, 'qa': None, 'c2pre': 0, 'dg': {}, 'sq': None}
    for k, v in fresh_fields.items():
        got = base.get(k)
        ok(f'T2 classic starts {k} fresh', got in (v, None, {}, 0, '') and not (isinstance(got, dict) and got), got)
    ok('T2 classic: c2entry/c3entry snapshots and ch3 are gone', not base.get('c2entry') and not base.get('c3entry') and not base.get('ch3'))
    ok('T2 classic: mb/sc fresh', base['mb'] == {} and base['sc'] == {})
    # each option, each non-base choice
    dres = [(v, (await build(pg, diff=v))['foeStr']) for v in ['weak', 'normal', 'strong', 'max']]
    ok('T2 diff weak/strong/max/normal', all(a == b for a, b in dres), dres)
    baseB = await ev(pg, "FFF_NG.base().bond"); freshB = await ev(pg, "FFF_NG.fresh().bond")
    ok('T2 Classic preset preselects the current Bond path (not a Keep button)', baseB=='strategic' and freshB=='reset', (baseB, freshB))
    for v in ['fierce', 'strategic', 'balanced']:
        b = await build(pg, bond=v); ok(f'T2 bond {v}', b['bond']['path'] == v and b['bond']['px'] == 500)
    b = await build(pg, bond='reset'); ok('T2 bond Reset: path and points cleared, so Ch1 can choose again', (b['bond'] or {}).get('path') in (None, '') and (b['bond'] or {}).get('px', 0) == 0 and (b['bond'] or {}).get('picks') in (None, {}) and not (b['bond'] or {}).get('lock'), b['bond'])
    b = await build(pg, cards='fresh'); ok('T2 cards fresh: starter deck (no upgrades), Aoi reset too', b['cards'][0]['lp'] == {} and b['cards'][0]['enh'] == [] and len(b['cards']) > 0 and not (b['chars'].get('aoi') or {}).get('cards'), (b['cards'][0], b['chars'].get('aoi')))
    ok('T2 cards fresh keeps essence/yen/gear', b['ess'] == 55 and b['items'] == 777 and b['gear']['of'] == {'sukajan': 1})
    b = await build(pg, enh='fresh'); ok('T2 enhancements fresh: upgrades off everywhere, essence refunded', all(c['lp'] == {} and c['enh'] == [] for c in b['cards']) and b['sigLv'] == 0 and b['lp'] == {} and b['chars']['aoi']['sigLv'] == 0 and b['ess'] > 55, (b['ess'], b['sigLv']))
    ok('T2 enhancements fresh keeps the cards', len(b['cards']) == len(fx['cards']))
    b = await build(pg, enh='fresh', ess='reset'); ok('T2 enh fresh + essence reset: essence 0 (no refund kept)', b['ess'] == 0)
    b = await build(pg, ess='reset'); ok('T2 essence reset: ess, seals, books all 0', b['ess'] == 0 and b['seal'] == 0 and b['books'] == {'common': 0, 'uncommon': 0})
    b = await build(pg, acc='hide'); ok('T2 accessories hide: owned gear, outfits and equipped slots cleared', b['gear']['own'] == {} and b['gear']['of'] == {} and b['gear']['eq']['ryo']['head'] is None and b['gear']['eq']['ryo']['acc'] is None and b['gear']['eq']['ryo']['tm'] is None)
    b = await build(pg, items='reset'); ok('T2 items reset: potions, sodas, herbs cleared; yen/ess stay', b['heal'] == [] and b['soda'] == {} and b['sodaOn'] == 0 and b['sodaK'] == '' and all(v == 0 for v in b['herbs'].values()) and b['items'] == 777 and b['ess'] == 55)
    b = await build(pg, yen='reset'); ok('T2 yen reset: 0, items stay', b['items'] == 0 and b['heal'] == fx['heal'])
    b = await build(pg, level='reset'); ok('T2 level reset: bond xp 0, conditioning hp 0, path stays', b['bond']['px'] == 0 and b['c2hp'] == 0 and b['bond']['path'] == 'strategic')
    b = await build(pg, tech='reset'); ok("T2 Genji's techniques reset: c2les, ready flag, kos, evo lesson", b['c2les'] in (None, {}) and b['c2lesReady'] == '' and b['c2kos'] == 0 and b['evoLesson'] == 0)
    ok('T2 tech reset leaves gang skills alone', eq(b['gsk'], fx['gsk']) and eq(b['cxNew'], fx['cxNew']))
    b = await build(pg, gang='reset'); ok('T2 Gang skills reset: gsk empty, gsk_ Codex badges gone, other badges stay', (b['gsk'] in (None, {})) and 'gsk_hanabi' not in b['cxNew'] and 'gsk_alley' not in b['cxNew'] and b['cxNew'].get('mat_x') == 1, (b['gsk'], b['cxNew']))
    ok('T2 gang reset leaves Genji techniques alone', eq(b['c2les'], fx['c2les']))
    b = await build(pg, rep='reset'); ok('T2 crew rep reset: neutral', b['crewRep'] == {'arc': 0, 'neo': 0, 'bat': 0, 'dep': 0})
    b = await ev(pg, "JSON.parse(JSON.stringify(FFF_NG.build(SAVE,FFF_NG.fresh())))")
    ok('T2 Fresh Start preset: everything reset, Codex stays', b['items'] == 0 and b['ess'] == 0 and b['gsk'] in (None, {}) and b['c2les'] in (None, {}) and not (b['bond'] or {}).get('path') and (b['bond'] or {}).get('px', 0) == 0 and b['cx'] == fx['cx'] and b['tips'] == fx['tips'] and b['gear']['of'] == {} and b['crewRep'] == {'arc': 0, 'neo': 0, 'bat': 0, 'dep': 0} and b['heal'] == [], b['gsk'])
    ok('T2 settings survive (binds, text size, ...)', eq(b['binds'], fx['binds']) and b['txtSize'] == fx['txtSize'])
    ok('T2 ngBuild does not touch the live save', await ev(pg, "SAVE.items===777&&SAVE.ngp===1&&SAVE.gsk.alley===1"))

async def t3(pg, errs):
    # live NG+ start with Gang skills = Learn again; then the Nails/gang grants work again
    await ev(pg, "(function(){var o=FFF_NG.base();o.gang='reset';FFF_NG.start(o);return 1})()")
    await pg.wait_for_timeout(2500)
    st = await ev(pg, "JSON.stringify({gsk:SAVE.gsk,has:FFF_OPN.has('alley'),ngp:SAVE.ngp,dg:Object.keys(SAVE.dg||{}),cxn:Object.keys(SAVE.cxNew||{})})")
    st = json.loads(st)
    ok('T3 Learn again: no gang skill owned after the NG+ start', not st['has'] and not (st['gsk'] or {}), st)
    ok('T3 Learn again: scene state replays (dg wiped, so Nails / lock scenes run again)', st['dg'] == [] and True)
    g = await ev(pg, "(function(){var h=FFF_OPN.grant('hanabi'),a=FFF_OPN.grant('alley',true),k=FFF_OPN.has('alley'),c=!!(SAVE.cxNew&&SAVE.cxNew.gsk_alley);return {a:a,h:h,k:k,c:c,hh:FFF_OPN.has('hanabi')}})()")
    ok('T3 Learn again: a gang skill (a different gang than the old run) and Alley Cat grant again, with their Codex badges', g['a'] and g['h'] and g['k'] and g['c'] and g['hh'], g)
    # Keep: grants refused for the other gang (one gang per run), skills stay
    await ev(pg, "(function(){FFF_OPN.revoke();SAVE.gsk={kamikaze:1,redline:1,alley:1,cheap:1};SAVE.cxNew={gsk_alley:1};SAVE.intro=1;SAVE.ch1=1;SAVE.gouki=1;save();var o=FFF_NG.base();FFF_NG.start(o);return 1})()")
    await pg.wait_for_timeout(2500)
    k = await ev(pg, "JSON.stringify({gsk:SAVE.gsk,r:FFF_OPN.grant('hanabi'),has:FFF_OPN.has('kamikaze'),cx:SAVE.cxNew})")
    k = json.loads(k)
    ok('T3 Keep: gang skills stay and the one-gang-per-run rule still applies', k['has'] and k['gsk'].get('alley') == 1 and k['r'] is False, k)
    ok('T3 no page errors', not errs, errs[:3])

async def t4(p, cleared_ready):
    # Ch1 -> Ch2 inside an NG+ run
    errs = []; b, pg = await newpage(p, errs); await boot(pg); await ev(pg, FIXTURE_JS)
    await ev(pg, "(function(){var o=FFF_NG.base();FFF_NG.start(o);return 1})()"); await pg.wait_for_timeout(2500)
    await ev(pg, "(function(){unstage&&unstage();W.scGen=(W.scGen|0)+1;SAVE.intro=1;SAVE.sc=SAVE.sc||{};SAVE.sc.nurse=1;SAVE.sc.after=1;W.dlg=false;W.busy=false;var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};return 1})()")
    await pg.evaluate("WORLD_API.c2Begin(false)"); await pg.wait_for_timeout(3000); await skipall(pg, 10); await pg.wait_for_timeout(1500); await skipall(pg, 10); await ev(pg, HUSH)
    s = json.loads(await ev(pg, "JSON.stringify({ch:SAVE.chapter,ngp:SAVE.ngp,c2:c2On(),room:W.inside&&W.inside.id,cls:document.getElementById('world').className,stand:c2S().stand||{},e:Object.keys(c2S().e||{}),gsk:SAVE.gsk,snap:!!SAVE.c2entry,snapNgp:SAVE.c2entry&&SAVE.c2entry.ngp,crew:Object.keys(SAVE.crewDown||{}),hp:SAVE.hp,max:MAXHP})"))
    ok('T4 Ch1 -> Ch2 in NG+: chapter 2, in the Ch2 town, c2 class', s['ch'] == 2 and s['c2'] and s['room'] == 'c2_town' and 'c2' in s['cls'], s)
    ok('T4 Ch2 run starts clean (no stale arrive/lock flags) and keeps crew rep from the last run', 'n13alley' not in s['e'] and 'run_fac' not in s['e'] and s['stand'].get('arc') == 3 and s['stand'].get('dep') == 4 and s['stand'].get('neo') == 2, s)
    ok('T4 NG+ Ch2 takes its own entry snapshot (not the old run\'s)', s['snap'] and s['snapNgp'] == 2, s)
    ok('T4 gang skills kept through Ch1 -> Ch2', s['gsk'].get('alley') == 1)
    ok('T4 no stale beaten crews in NG+ Ch2', s['crew'] == [], s['crew'])
    ok('T4 no page errors (Ch1 -> Ch2)', not errs, errs[:3])
    await b.close()
    # NG+ started from Ch2 and from Ch3
    for ch in (2, 3):
        errs = []; b, pg = await newpage(p, errs); await boot(pg); await ev(pg, FIXTURE_JS)
        await ev(pg, "(function(){c3Preset();SAVE.ch1=1;SAVE.gouki=1;SAVE.ch2=1;SAVE.intro=1;SAVE.crewDown={P1:1};save();return 1})()")
        if ch == 2: await pg.evaluate("WORLD_API.c2Begin(false)")
        else: await ev(pg, "c3Begin(false)")
        await pg.wait_for_timeout(2500); await skipall(pg); await ev(pg, HUSH)
        pre = await ev(pg, "SAVE.chapter")
        await ev(pg, "(function(){FFF_NG.start(FFF_NG.base());return 1})()"); await pg.wait_for_timeout(2500)
        s = json.loads(await ev(pg, "JSON.stringify({ch:SAVE.chapter,chN:chN(),c2:c2On(),room:W.inside&&W.inside.id,cls:document.getElementById('world').className,ngp:SAVE.ngp,crew:Object.keys(SAVE.crewDown||{}),ry:[Math.round(W.ryo.x),Math.round(W.ryo.y)],start:[WD.start[0],WD.start[1]]})"))
        ok(f'T4 NG+ started from Ch{ch} (was chapter {pre}): back in Ch1, no c2/c3/inside class, not inside a room', s['ch'] == 1 and s['chN'] == 1 and not s['c2'] and s['room'] is None and not re.search(r'\b(c2|c2town|c3|inside|inroom)\b', s['cls']), s)
        ok(f'T4 NG+ from Ch{ch}: beaten crews cleared, Ryo at the Ch1 start', s['crew'] == [] and s['ry'][0] == s['start'][0] and abs(s['ry'][1] - s['start'][1]) <= 80, s)
        ok(f'T4 no page errors (NG+ from Ch{ch})', not errs, errs[:3]); await b.close()

async def t5(p):
    out = {}
    for mode in ('normal', 'ngp'):
        errs = []; b, pg = await newpage(p, errs); await boot(pg)
        if mode == 'ngp':
            await ev(pg, FIXTURE_JS); await ev(pg, "(function(){FFF_NG.start(FFF_NG.base());return 1})()")
        else:
            await pg.evaluate("WORLD_API.freshEnter()")
        await pg.wait_for_timeout(2500)
        await ev(pg, "root.FFF_NO_TUT=1")
        await ev(pg, """(function(){try{unstage&&unstage()}catch(e){};W.scGen=(W.scGen|0)+1;SAVE.intro=1;SAVE.sc=SAVE.sc||{};SAVE.sc.nurse=1;SAVE.sc.after=1;W.dlg=false;W.busy=false;W.scr=0;W.cut=false;W.path=[];var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};W.ryo.x=1800;W.ryo.y=2900;W.aoi.x=1800;W.aoi.y=2960;resetTrail(1800,2900,3);camera(true);return 1})()""")
        await pg.wait_for_timeout(12000)
        out[mode] = json.loads(await ev(pg, "JSON.stringify({packs:packsLive(),path:packBodies('path').length,roam:W.roam.length,crew:Object.keys(SAVE.crewDown||{}).length})"))
        await pg.screenshot(path=str(SHOTS / f'packs_{mode}.png')); ok(f'T5 no page errors ({mode})', not errs, errs[:3]); await b.close()
    ok('T5 NG+: packsLive() is true after the intro', out['ngp']['packs'], out)
    ok('T5 NG+ spawns path packs like a normal start', out['ngp']['path'] > 0 and out['normal']['path'] > 0, out)

async def t6(pg):
    t = INDEX.read_text(encoding='utf-8')
    ok("T6 no stray { mood } object inside id arrays", not re.search(r"\[(?:'[A-Za-z0-9_\-]{1,24}', ){1,}\{ mood: '[a-z]+' \}\]", t))
    ok("T6 gear.eq has no '[object Object]' key", await ev(pg, "(function(){gearS();return Object.keys(SAVE.gear.eq).join()})()") == 'ryo,aoi')
    ok('T6 dead NG+ code is gone', not re.search(r'function (ngPlus|ngCarry|ngDesc|ngBondAsk)\b', t))
    ok("T6 packsLive has no NG+ exclusion", 'function packsLive() { return !!(' in t and '!SAVE.ngp && SAVE.intro' not in t)

async def t7(p):
    errs = []; b, pg = await newpage(p, errs); await boot(pg); await ev(pg, FIXTURE_JS)
    await ev(pg, "(function(){SAVE.ch1=1;SAVE.gouki=1;save();FFF_NG_OPEN();return 1})()"); await pg.wait_for_timeout(800)
    rows = json.loads(await ev(pg, "JSON.stringify([].slice.call(document.querySelectorAll('#ngplus .ngrow > b')).map(function(e){return e.textContent}))"))
    ok('T7 options screen lists all 12 options', rows == ['Difficulty', 'Bond path', 'Cards', 'Enhancements', 'Spirit essences', 'Accessories', 'Items & ingredients', 'Yen', 'Ryo & Aoi’s level', 'Genji’s techniques', 'Gang skills', 'Crew rep'], rows)
    txt = await ev(pg, "document.getElementById('ngplus').innerText")
    ok("T7 label says Compassionate, not Balanced", 'Compassionate' in txt and 'Balanced' not in txt)
    bondBtns = json.loads(await ev(pg, "JSON.stringify([].slice.call(document.querySelectorAll('#ngplus .ngrow.ng2x2 button')).map(function(e){return [e.textContent,e.classList.contains('on'),e.getAttribute('data-v')]}))"))
    ok('T7 Bond path is Reset / Fierce / Strategic / Compassionate, Classic preselects the current path', [b[0] for b in bondBtns]==['Reset','Fierce','Strategic','Compassionate'] and [b[2] for b in bondBtns if b[1]]==['strategic'], bondBtns)
    await ev(pg, "document.querySelector('#ngplus [data-pre=fresh]').click()"); await pg.wait_for_timeout(200)
    onFresh = await ev(pg, "document.querySelector('#ngplus .ngrow.ng2x2 button.on').getAttribute('data-v')")
    modeF = await ev(pg, "v640NgMode()")
    ok('T7 Fresh Start selects Bond Reset', onFresh=='reset' and modeF=='fresh', (onFresh, modeF))
    await ev(pg, "document.querySelector('#ngplus [data-pre=classic]').click()"); await pg.wait_for_timeout(200)
    await ev(pg, "document.querySelector('#ngplus .ngrow.ng2x2 [data-v=reset]').click()"); await pg.wait_for_timeout(200)
    modeC = await ev(pg, "v640NgMode()")
    onR = await ev(pg, "document.querySelector('#ngplus .ngrow.ng2x2 button.on').getAttribute('data-v')")
    ok('T7 changing Bond to Reset switches Classic to Custom', modeC=='custom' and onR=='reset', (modeC, onR))
    await ev(pg, "document.querySelector('#ngplus [data-pre=classic]').click()"); await pg.wait_for_timeout(200)
    box = '#ngplus'
    for i, y in enumerate([0, 700, 1400, 2100]):
        await ev(pg, f"document.getElementById('ngplus').scrollTop={y}"); await pg.wait_for_timeout(200)
        await pg.screenshot(path=str(SHOTS / f'options_{i}.png'))
    await ev(pg, "document.querySelector('#ngplus [data-pre=fresh]').click()"); await pg.wait_for_timeout(300)
    await ev(pg, "document.querySelector('#ngplus [data-a=review]').click()"); await pg.wait_for_timeout(500)
    await ev(pg, "document.getElementById('ngplus').scrollTop=0"); await pg.screenshot(path=str(SHOTS / 'review_fresh.png'))
    ok('T7 no page errors (options screen)', not errs, errs[:3]); await b.close()


async def t8(p):
    """NG+ from the title screen (cold: world not built yet), Fresh Start preset, through the real buttons"""
    errs = []; b, pg = await newpage(p, errs)
    await boot(pg); await ev(pg, FIXTURE_JS)
    await ev(pg, "(function(){SAVE.ch1=1;SAVE.gouki=1;SAVE.chapter=1;SAVE.intro=1;save();return 1})()")
    await pg.reload(); await pg.wait_for_timeout(3500)
    await pg.evaluate("[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&/New Game ?\\+|Plus/i.test(e.textContent))[0].click()"); await pg.wait_for_timeout(1500)
    await ev(pg, "root.FFF_NO_TUT=1")
    await pg.evaluate("document.querySelector('#ngplus [data-pre=fresh]').click()"); await pg.wait_for_timeout(300)
    await pg.evaluate("document.querySelector('#ngplus [data-a=review]').click()"); await pg.wait_for_timeout(300)
    await pg.evaluate("document.querySelector('#ngplus [data-a=start]').click()"); await pg.wait_for_timeout(4000)
    s = json.loads(await ev(pg, "JSON.stringify({ngp:SAVE.ngp,on:W.on,ch:SAVE.chapter,items:SAVE.items,gsk:SAVE.gsk,bond:SAVE.bond&&SAVE.bond.path,ess:SAVE.ess,cx:SAVE.cx,intro:SAVE.intro,scr:W.scr})"))
    ok('T8 title -> New Game+ -> Fresh Start: world entered, run reset, Codex kept', s['ngp'] == 2 and s['on'] and s['ch'] == 1 and s['items'] == 0 and not s['gsk'] and not s['bond'] and s['ess'] == 0 and s['cx'].get('tip_howto') == 1, s)  # intro may add more tip_* entries after the start
    await pg.screenshot(path=str(SHOTS / 'title_ngp_start.png'))
    ok('T8 no page errors (title start)', not errs, errs[:3]); await b.close()

async def t9(p):
    """A Bond Reset NG+ run gets a path assigned the usual way in Chapter One (the courtyard first pick)."""
    errs = []; b, pg = await newpage(p, errs); await boot(pg); await ev(pg, FIXTURE_JS)
    await ev(pg, "(function(){var o=FFF_NG.base();o.bond='reset';FFF_NG.start(o);return 1})()")
    await pg.wait_for_timeout(2500)
    pre = json.loads(await ev(pg, "JSON.stringify({path:SAVE.bond&&SAVE.bond.path,px:SAVE.bond&&SAVE.bond.px,lock:!!(SAVE.bond&&SAVE.bond.lock),ngp:SAVE.ngp})"))
    ok('T9 after Reset start: no path, no points, unlocked', not pre['path'] and pre['px']==0 and not pre['lock'] and pre['ngp']==2, pre)
    # the intro's first Bond pick: FFF_BOND auto-answers, same hook the tests use
    got = json.loads(await ev(pg, """(function(){
      root.FFF_BOND='fierce';
      var out={};
      try {
        bondAsk('first', function(L){ out.lines=L&&L.length; });
      } catch (e) { out.err=String(e&&e.message||e); }
      var B=STORY.bond(SAVE);
      out.path=B.path; out.px=B.px|0; out.lock=!!B.lock; out.first=B.picks&&B.picks.first; out.askOpen=!!(document.getElementById('wdlg')&&document.getElementById('wdlg').classList.contains('on'));
      return JSON.stringify(out);
    })()"""))
    ok('T9 Reset run: the Ch1 first pick assigns Fierce and locks it, the same as a new game', got.get('path')=='fierce' and got.get('first')=='fierce' and got.get('lock') and got.get('px',0)>=0 and not got.get('err'), got)
    ok('T9 no page errors (Reset path assign)', not errs, errs[:3]); await b.close()

async def main():
    serve(PORT, INDEX.parent)
    async with async_playwright() as p:
        errs = []; b, pg = await newpage(p, errs); await boot(pg); await ev(pg, FIXTURE_JS)
        await t1(pg); await t2(pg); await t6(pg); await t3(pg, errs); await b.close()
        await t4(p, None); await t5(p); await t7(p); await t8(p); await t9(p)
    bad = [r for r in RES if not r[0]]
    print(f'\n{len(RES) - len(bad)}/{len(RES)} passed'); sys.exit(1 if bad else 0)
asyncio.run(main())
