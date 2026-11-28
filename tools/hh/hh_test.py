"""hh_test: the Kitsune BOY handheld (v6566-handheld, GGD-93). Usage: hh_test.py [ROOT] [SHOTS]
Boots a Chapter One save with every base cleared, then plays the side quest, the six challengers, the menu tab, the cheat pocket,
persistence and a reload in the middle of a match. Uses the box harness in /workspace/handheld/hhtools (playwright)."""
import asyncio, sys, json, re
sys.path.insert(0, '/workspace/handheld/hhtools')
from h import *; from srv import serve; from adv import adv
from pathlib import Path
ROOT = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parents[2])
SHOTS = sys.argv[2] if len(sys.argv) > 2 else '/workspace/handheld/shots'
Path(SHOTS).mkdir(parents=True, exist_ok=True)
SAVE0 = json.load(open('/workspace/handheld/hhtools/save_c1.json'))
R = []
def ok(name, cond, info=''):
    R.append((name, bool(cond))); print(('PASS ' if cond else 'FAIL ') + name + ('  ' + str(info)[:300] if info != '' else ''), flush=True)
async def J(pg, c):
    r = await ev(pg, c)
    try: return json.loads(r) if isinstance(r, str) and r[:1] in '[{' else r
    except Exception: return r
async def tap_btn(pg, sel, rx):
    c = await pg.evaluate("([s,r])=>{var b=[...document.querySelectorAll(s)].find(e=>new RegExp(r).test(e.textContent)&&e.offsetParent!==null);if(!b)return null;var q=b.getBoundingClientRect();return [q.x+q.width/2,q.y+q.height/2]}", [sel, rx])
    if c: await pg.touchscreen.tap(*c)
    return c
async def setup(pg):
    await pg.reload(); await pg.wait_for_timeout(2500); await boot(pg, cont=True)
    await J(pg, "clearRoam();W.spawnT=1e12;1"); await pg.wait_for_timeout(500); await J(pg, HUSH)
async def to_talk(pg, id):
    await J(pg, "var q=W.hhS.filter(function(r){return r.id==='%s'})[0]; W.ryo.x=q.talk[0]; W.ryo.y=q.talk[1]; place(W.ryo,0); camera(true); W.tagSig=''; 1" % id); await pg.wait_for_timeout(900)
async def world_ok(pg, tag):
    """menu, map, swap and movement all respond after the handheld closed"""
    st = await J(pg, "JSON.stringify({p:!!W.paused,d:!!W.dlg,hh:!!document.getElementById('j6hh'),cur:!!FFF_HH.cur()})")
    ok(tag + ': no lock flags', not st['p'] and not st['d'] and not st['hh'] and not st['cur'], st)
    x0 = await J(pg, "W.ryo.x"); y0 = await J(pg, "W.ryo.y")
    for k in ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown']:
        await pg.keyboard.down(k); await pg.wait_for_timeout(450); await pg.keyboard.up(k)
        x1 = await J(pg, "W.ryo.x"); y1 = await J(pg, "W.ryo.y")
        if abs(x1 - x0) + abs(y1 - y0) > 4: break
    ok(tag + ': Ryo moves', abs(x1 - x0) + abs(y1 - y0) > 4, [x0, y0, x1, y1])
    await J(pg, "pause('home');1"); await pg.wait_for_timeout(500); m = await J(pg, "JSON.stringify({on:/on/.test(document.getElementById('wpause').className),p:W.paused})")
    await J(pg, "phClose();1"); await pg.wait_for_timeout(300)
    ok(tag + ': menu opens', m['on'] and m['p'], m)
    await J(pg, "pause('map');1"); await pg.wait_for_timeout(600); mp = await J(pg, "JSON.stringify({on:/on/.test(document.getElementById('wpause').className)||!!document.querySelector('.pmap,.ph-map,#wpause svg'),t:W.ptab})")
    await J(pg, HUSH); await pg.wait_for_timeout(300)
    ok(tag + ': map opens', mp['on'], mp)
    a0 = await J(pg, "SAVE.act"); await J(pg, "switchChar();1"); await pg.wait_for_timeout(700); a1 = await J(pg, "SAVE.act"); await J(pg, HUSH)
    if a1 != a0: await J(pg, "switchChar();1"); await pg.wait_for_timeout(500); await J(pg, HUSH)
    ok(tag + ': swap works', a1 != a0, [a0, a1])
    st2 = await J(pg, "JSON.stringify({p:!!W.paused,d:!!W.dlg})"); ok(tag + ': still unlocked after checks', not st2['p'] and not st2['d'], st2)
async def challenge(pg, id, win=True, shot=None, mid=None):
    """walk up, Play (real taps), banter, play, result, Done, after-banter"""
    await J(pg, "FFF_HH.talk('%s');1" % id); await pg.wait_for_timeout(700)
    c = await tap_btn(pg, '#wdlg button', '^\\W*Play')
    if not c: return {'err': 'no play button'}
    await pg.wait_for_timeout(700); walk = await J(pg, "(document.querySelector('#wdlg .tx')||{}).textContent||''")
    await adv(pg); await pg.wait_for_timeout(1700)
    cur = await J(pg, "JSON.stringify(FFF_HH.cur()?{st:FFF_HH.cur().st(),cfg:FFF_HH.cur().cfg}:null)")
    if not cur: return {'err': 'handheld did not open', 'walk': walk}
    await pg.wait_for_timeout(3200)
    if mid:
        await J(pg, "(function(){var P=FFF_HH.cur().G._pe()[0]; P.hp=Math.round(P.max*0.2); return 1})()"); await pg.wait_for_timeout(500)
        mid_t = await J(pg, "(function(){var b=document.querySelector('#j6hh .hhmid');return b&&b.classList.contains('on')?b.textContent:''})()")
        await pg.wait_for_timeout(400)
        if shot: await pg.screenshot(path=shot.replace('.png', '_mid.png'))
    else: mid_t = None
    if shot: await pg.screenshot(path=shot)
    await J(pg, "FFF_HH.cur().end(%s);1" % ('true' if win else 'false')); await pg.wait_for_timeout(700)
    res = await J(pg, "JSON.stringify(FFF_HH.cur().res())")
    await tap_btn(pg, '#j6hh .hhres button', 'Done'); await pg.wait_for_timeout(700)
    after = await J(pg, "(document.querySelector('#wdlg .tx')||{}).textContent||''"); who = await J(pg, "(document.querySelector('#wdlg')||{}).className||''")
    n = await adv(pg); await pg.wait_for_timeout(400)
    return {'walk': walk, 'cfg': cur['cfg'], 'res': res, 'after': after, 'n': n, 'mid': mid_t}
async def main():
    port = serve(ROOT)
    async with async_playwright() as p:
        errs = []; b, ctx, pg = await newpage(p, port, ROOT, errs, save=SAVE0)
        await setup(pg)
        # ---------- static ----------
        html = Path(ROOT, 'index.html').read_text(encoding='utf8'); i = html.index('/* HH_BEGIN'); blk = html[i:html.index('/* HH_END */')]
        ok('no "Chapter 2" / "Chapter Two" in the handheld block', not re.search(r'Chapter (2|Two)|Ch\.? ?2\b', blk))
        BM = Path('/workspace/handheld/BANTER.md').read_text(encoding='utf8')
        md_lines = re.findall(r'^(?:Ryo|Aoi): (.+)$', BM, re.M); hb = await J(pg, "JSON.stringify(FFF_HH.banter())")
        flat = []
        def walk(o):
            if isinstance(o, list) and len(o) == 2 and o[0] in ('ryo', 'aoi') and isinstance(o[1], str): flat.append(o[1]); return
            if isinstance(o, list): [walk(x) for x in o]
            elif isinstance(o, dict): [walk(v) for v in o.values()]
        walk(hb)
        ok('BANTER.md wired word for word (every Ryo / Aoi line, nothing added)', sorted(flat) == sorted(md_lines), [len(flat), len(md_lines)])
        ok('three paths keyed fierce / balanced / strategic', sorted(hb.keys()) == ['balanced', 'fierce', 'strategic'])
        st0 = await J(pg, "JSON.stringify({hh:SAVE.hh, tile:/data-s=\"hh\"/.test(phHome())})")
        ok('fresh save: no handheld, no menu tile', not st0['hh'] and not st0['tile'], st0)
        # ---------- hallway door + Staff Room ----------
        await J(pg, "intGo('hall',{at:[1645,262,3]});1"); await pg.wait_for_timeout(1500); await J(pg, HUSH)
        d = await J(pg, "JSON.stringify({patch:!!document.querySelector('.hhsdoor'), spot:INT.hall.spots.some(function(s){return s.id==='sdoor'}), walk:walkableAt(1645,262)})")
        ok('hallway: Staff Room door patch + doorway spot', d['patch'] and d['spot'] and d['walk'], d)
        await pg.screenshot(path=SHOTS + '/01_hall_staff_room_door.png')
        # walk into the doorway for real (the walk-in door mechanic)
        await J(pg, "W.ryo.x=1645;W.ryo.y=400;place(W.ryo,0);camera(true);1"); await pg.wait_for_timeout(500)
        sc = await J(pg, "JSON.stringify(function(){var e=document.querySelector('.hhsdoor').getBoundingClientRect();return [e.x+e.width/2,e.y+e.height*0.6]}())")
        await pg.touchscreen.tap(*sc); await pg.wait_for_timeout(3500)
        inn = await J(pg, "W.inside&&W.inside.id"); ok('tapping the new door walks Ryo in (walk-in doorway, like the classrooms)', inn == 'hstaff', inn)
        if inn != 'hstaff': await J(pg, "intAct('sdoor');1"); await pg.wait_for_timeout(1800)
        await J(pg, HUSH)
        sr = await J(pg, "JSON.stringify({n:W.loc, box:!!document.querySelector('.hhboy'), tags:(W.tagL||[]).map(function(t){return t.key}), at:walkableAt(676,458)})")
        ok('Staff Room: name, box with the handheld, glowing objects', sr['n'] == 'Staff Room' and sr['box'] and 'hstaff:cbox' in sr['tags'] and sr['at'], sr)
        await J(pg, "W.ryo.x=676;W.ryo.y=470;place(W.ryo,0);waddle(W.ryo,0,-Math.PI/2);camera(true);W.tagSig='';1"); await pg.wait_for_timeout(900)
        await pg.screenshot(path=SHOTS + '/02_staff_room_desk.png')
        # ---------- Sota's tip ----------
        await J(pg, "libGo('ante');1"); await pg.wait_for_timeout(1800); await J(pg, HUSH)
        a = await J(pg, "JSON.stringify({hhS:(W.hhS||[]).map(function(q){return q.id}), tags:(W.tagL||[]).filter(function(t){return /:hh:/.test(t.key)}).map(function(t){return [t.key,t.cls||'']})})")
        ok('Silent Study: Sota sits there with a plain Talk bubble (no handheld yet)', a['hhS'] == ['sota'] and a['tags'] == [['dl_ante:hh:sota', '']], a)
        jr = await J(pg, "JSON.stringify(sideRows('active').filter(function(r){return r.id==='hh_q'}).map(function(r){return questDetail(r.id)}))")
        ok('Journal: "A Game in the Staff Room", step 1 open', jr and jr[0]['steps'][0][1] is False, jr)
        await to_talk(pg, 'sota'); await J(pg, "FFF_HH.talk('sota');1"); await pg.wait_for_timeout(700)
        t1 = await J(pg, "(document.querySelector('#wdlg .tx')||{}).textContent||''"); await adv(pg); await J(pg, HUSH)
        locs = await J(pg, "JSON.stringify(sideRows('active').map(function(r){return questDetail(r.id).loc}))")
        ok('Sota tips Ryo off about the Staff Room', any('Staff Room' in x for x in locs) and (await J(pg, "!!SAVE.hh.tip")) and 'Hey' in t1, [t1.replace('\u2060', ''), locs])
        # ---------- pickup ----------
        await J(pg, "intGo('hstaff');1"); await pg.wait_for_timeout(1500); await J(pg, HUSH)
        await J(pg, "W.ryo.x=676;W.ryo.y=458;place(W.ryo,0);waddle(W.ryo,0,-Math.PI/2);camera(true);W.tagSig='';1"); await pg.wait_for_timeout(700)
        await J(pg, "intAct('cbox');1"); await pg.wait_for_timeout(800)
        await pg.screenshot(path=SHOTS + '/03_staff_room_pickup.png')
        await adv(pg); await pg.wait_for_timeout(300); await J(pg, HUSH)
        pk = await J(pg, "JSON.stringify({own:SAVE.hh.own, box:!!document.querySelector('.hhboy'), tile:/data-s=\"hh\"/.test(phHome())})")
        ok('desk pickup: own it, box empties, Menu > More > Handheld appears', pk['own'] and not pk['box'] and pk['tile'], pk)
        await world_ok(pg, 'after pickup')
        # ---------- menu tab ----------
        await J(pg, "pause('home');1"); await pg.wait_for_timeout(500)
        await tap_btn(pg, '#wpause .ph-m', 'Handheld'); await pg.wait_for_timeout(900)
        mt = await J(pg, "JSON.stringify({t:W.ptab, cls:document.getElementById('wpause').className, tabs:[...document.querySelectorAll('#wpause .ph-tabs button')].map(function(b){return b.textContent}), f:document.querySelectorAll('#wpause .hh-f').length, cpu:!!document.querySelector('[data-hh=cpu]')})")
        ok('menu: Handheld tab with Play / Rivals / Cheats, 6 fighter cards, VS CPU', mt['t'] == 'hh' and 'hh' in mt['cls'] and len(mt['tabs']) == 3 and mt['f'] == 6 and mt['cpu'], mt)
        await pg.screenshot(path=SHOTS + '/04_menu_handheld_tab.png')
        await tap_btn(pg, '#wpause .ph-tabs button', 'Rivals'); await pg.wait_for_timeout(600); await pg.screenshot(path=SHOTS + '/04b_menu_rivals.png')
        rv = await J(pg, "document.querySelectorAll('#wpause .hh-r').length"); ok('rivals list: 6 rows', rv == 6, rv)
        # VS CPU from the menu, then back to the menu
        await tap_btn(pg, '#wpause .ph-tabs button', 'Play'); await pg.wait_for_timeout(500)
        await tap_btn(pg, '#wpause .hh-go', 'VS CPU'); await pg.wait_for_timeout(2600)
        cp = await J(pg, "JSON.stringify({cur:!!FFF_HH.cur(), st:FFF_HH.cur()&&FFF_HH.cur().st(), hid:document.getElementById('world').style.visibility})")
        ok('VS CPU opens the handheld (world layers hidden)', cp['cur'] and cp['hid'] == 'hidden', cp)
        await pg.wait_for_timeout(3600)
        FREEZE = "(function(){var pe=FFF_HH.cur().G._pe();pe[1].aiT=99;pe[1].want={};pe[1].ai=true;pe[1].hp=pe[1].max;pe[0].hp=pe[0].max;pe[0].st='idle';pe[0].mv=null;pe[0].stT=0;pe[1].x=pe[0].x+150;return FFF_HH.cur().G.phase()})()"
        ok('match reaches the fight phase', (await J(pg, FREEZE)) == 'fight')
        # controls: keyboard and touch
        await J(pg, FREEZE); x0 = await J(pg, "FFF_HH.cur().G._pe()[0].x"); await pg.keyboard.down('ArrowRight'); await pg.wait_for_timeout(500); await pg.keyboard.up('ArrowRight'); x1 = await J(pg, "FFF_HH.cur().G._pe()[0].x")
        ok('handheld: \u25b6 walks (keyboard)', x1 != x0, [x0, x1])
        vw = await pg.evaluate("[innerWidth, innerHeight]"); s = min(vw[0] / 390, vw[1] / 844); ox = (vw[0] - 390 * s) / 2; oy = (vw[1] - 844 * s) / 2
        def P(x, y): return (ox + x * s, oy + y * s)
        await J(pg, FREEZE); await J(pg, "(function(){var P=FFF_HH.cur().G._pe()[0];P.x=150;return 1})()")
        x0 = await J(pg, "FFF_HH.cur().G._pe()[0].x"); await pg.mouse.move(*P(48, 724)); await pg.mouse.down(); await pg.wait_for_timeout(500); await pg.mouse.up(); x1 = await J(pg, "FFF_HH.cur().G._pe()[0].x")
        ok('handheld: D-pad \u25c0 walks (touch)', x1 < x0, [x0, x1])
        await J(pg, FREEZE); await pg.mouse.move(*P(88, 676)); await pg.mouse.down(); await pg.wait_for_timeout(120); air = await J(pg, "FFF_HH.cur().G._pe()[0].air"); await pg.mouse.up(); await pg.wait_for_timeout(700)
        ok('handheld: D-pad \u25b2 jumps', air, air)
        await J(pg, FREEZE); await pg.mouse.move(*P(334, 696)); await pg.mouse.down(); await pg.wait_for_timeout(60); sa = await J(pg, "FFF_HH.cur().G._pe()[0].st"); await pg.mouse.up(); await pg.wait_for_timeout(500)
        ok('handheld: A attacks', sa == 'atk', sa)
        await J(pg, FREEZE); await J(pg, "(function(){var pe=FFF_HH.cur().G._pe();pe[0].x=80;pe[1].x=300;return 1})()")
        await pg.mouse.move(*P(258, 740)); await pg.mouse.down(); await pg.wait_for_timeout(60); await pg.mouse.up(); await pg.wait_for_timeout(250); sb = await J(pg, "JSON.stringify({st:FFF_HH.cur().G._pe()[0].st, pj:FFF_HH.cur().G._pj()})")
        ok('handheld: B fires a special', sb['st'] == 'atk' or sb['pj'] > 0, sb)
        await J(pg, "(function(){var P=FFF_HH.cur().G._pe()[0];P.meter=100;return 1})()"); await pg.wait_for_timeout(200)
        await pg.screenshot(path=SHOTS + '/05_handheld_fight.png')
        await J(pg, "FFF_HH.cur().end(true);1"); await pg.wait_for_timeout(600)
        pr = await J(pg, "JSON.stringify({res:FFF_HH.cur().res(), hh:SAVE.hh.qs, items:SAVE.items})")
        ok('VS CPU: no stars, no yen', pr['res']['lines'] == ['Practice \u00b7 no stars, no yen'] and not pr['hh'], pr)
        await tap_btn(pg, '#j6hh .hhres button', 'Done'); await pg.wait_for_timeout(900)
        bm = await J(pg, "JSON.stringify({t:W.ptab, on:/on/.test(document.getElementById('wpause').className), hid:document.getElementById('world').style.visibility})")
        ok('Done returns to the Handheld tab, world layers restored', bm['t'] == 'hh' and bm['on'] and bm['hid'] != 'hidden', bm)
        await J(pg, "phClose();1"); await pg.wait_for_timeout(400)
        await world_ok(pg, 'after VS CPU')
        # ---------- challengers ----------
        await J(pg, "libGo('ante');1"); await pg.wait_for_timeout(1800); await J(pg, HUSH)
        await to_talk(pg, 'sota')
        mk = await J(pg, "JSON.stringify([...document.querySelectorAll('#wtags .wtag.vs')].map(function(e){return [e.dataset.k,!!e.querySelector('.vsi')]}))")
        ok('challenger marker B: gold border + handheld badge on Sota and Rin', sorted(mk) == [['dl_ante:hh:rin', True], ['dl_ante:hh:sota', True]], mk)
        await pg.screenshot(path=SHOTS + '/06_challenger_marker.png')
        path = await J(pg, "FFF_HH.path()")
        named = await J(pg, "JSON.stringify(FFF_HH.banter()['%s'].named.sota)" % path)
        r1 = await challenge(pg, 'sota', True, SHOTS + '/07_handheld_vs_sota.png', mid=True)
        ok('walk-up: Sota\u2019s named line for this path plays first', r1.get('walk') and named[0][1].split('{')[0][:8] in r1['walk'].replace('\u2060', ''), [r1.get('walk'), named[0][1]])
        ok('handheld cfg: Blue Lotus \u26051, AI level 0, Kaze \u26051', r1.get('cfg', {}).get('foe') == 'aoi' and r1['cfg']['lv'] == 0 and r1['cfg']['me'] == 'ryo', r1.get('cfg'))
        lows = [hhStrip(x[0][1]) for x in []] if False else None
        ok('mid-match: one short overlay line on low HP', bool(r1.get('mid')), r1.get('mid'))
        ok('first win: +\u00bc\u2605 and Blue Lotus unlocked', '+\u00bc\u2605 KAZE TENMA' in r1['res']['lines'] and 'NEW FIGHTER: BLUE LOTUS' in r1['res']['lines'], r1['res'])
        hs = await J(pg, "JSON.stringify(SAVE.hh)")
        ok('save: beat sota, ryo 1 quarter, aoi unlocked, first-win pool used', hs['beat'].get('sota') and hs['qs'].get('ryo') == 1 and hs['unl'].get('aoi') and any(k.endswith(':first') for k in hs['bp']), hs)
        jd = await J(pg, "JSON.stringify(sideRows('done').map(function(r){return r.id}))"); ok('Journal: quest complete after beating Sota', 'hh_q' in jd, jd)
        await world_ok(pg, 'after a challenger match')
        # rematch + loss
        y0 = await J(pg, "SAVE.items|0"); r2 = await challenge(pg, 'sota', True)
        y1 = await J(pg, "SAVE.items|0"); ok('rematch win pays \u00a52\u20133, no star', 2 <= y1 - y0 <= 3 and (await J(pg, "SAVE.hh.qs.ryo")) == 1, [y0, y1, r2.get('res')])
        bp = await J(pg, "JSON.stringify(SAVE.hh.bp)"); ok('rematch win uses the rematch pool', any(k.endswith(':rematch') for k in bp), bp)
        r3 = await challenge(pg, 'rin', False); ok('loss: no reward, loss pool, rin still new', not (await J(pg, "!!SAVE.hh.beat.rin")) and any(k.endswith(':loss') for k in (await J(pg, "JSON.stringify(SAVE.hh.bp)"))), r3.get('res'))
        r4 = await challenge(pg, 'rin', True); ok('Rin: The Ronin unlocked, CPU \u26051\u00bc', (await J(pg, "!!SAVE.hh.unl.masa")) and abs(r4['cfg']['lv'] - 0.4) < 1e-6, r4.get('cfg'))
        # the other rooms
        for gofn, cid, shot in [("artGo('hall')", 'kaito', '08_kaito_music_hall.png'), ("cafGo('staff')", 'haru', '09_haru_cafeteria_staff.png'), ("fldGo('coach')", 'yuto', '10_yuto_coach.png')]:
            await J(pg, gofn + ";1"); await pg.wait_for_timeout(1900); await J(pg, HUSH)
            q = await J(pg, "JSON.stringify((W.hhS||[]).map(function(q){return {id:q.id,x:q.s.x,y:q.s.y,talk:q.talk,w:walkableAt(q.talk[0],q.talk[1]),ws:walkableAt(q.s.x,q.s.y)}}))")
            me = [x for x in q if x['id'] == cid]
            ok('%s spawns in his room, talk spot walkable' % cid, me and me[0]['w'], q)
            await to_talk(pg, cid); await pg.screenshot(path=SHOTS + '/' + shot)
            rr = await challenge(pg, cid, True)
            ok('%s beaten: %s' % (cid, rr.get('res', {}).get('lines')), (await J(pg, "!!SAVE.hh.beat.%s" % cid)), rr.get('after'))
            if cid == 'yuto':
                ok('the fifth win names K\u014dno (Coach\u2019s Office)', (await J(pg, "SAVE.hh.hint")) == 'yuto', rr.get('after'))
        # ---------- Glitch ----------
        await J(pg, "fldGo('coach');1"); await pg.wait_for_timeout(1900); await J(pg, HUSH)
        await to_talk(pg, 'glitch')
        gm = await J(pg, "JSON.stringify([...document.querySelectorAll('#wtags .wtag')].filter(function(e){return /hh:glitch/.test(e.dataset.k)}).map(function(e){return e.className}))")
        ok('Glitch K\u014dno: gold marker once the other five are beaten', gm and 'vs' in gm[0], gm)
        await pg.screenshot(path=SHOTS + '/11_glitch_kono.png')
        rg = await challenge(pg, 'glitch', True)
        ok('Glitch match: Black Comet, \u26052, his hidden DOUBLE SHOT', rg.get('cfg', {}).get('foe') == 'jin' and 'e' in rg['cfg']['dbl'] and abs(rg['cfg']['lv'] - 1.6) < 1e-6, rg.get('cfg'))
        gs = await J(pg, "JSON.stringify(SAVE.hh)")
        ok('Glitch win: DOUBLE SHOT in the pocket (on), Black Comet, a lead', gs['cheats'].get('dbl') and gs['cOn'] == 'dbl' and gs['unl'].get('jin') and gs['lead'], gs)
        lj = await J(pg, "JSON.stringify(sideRows('active').map(function(r){return r.id}))"); ok('Journal: arcade tournament lead', 'hh_lead' in lj, lj)
        await J(pg, "W.hhTab='cht';pause('hh');1"); await pg.wait_for_timeout(800); await pg.screenshot(path=SHOTS + '/12_cheat_pocket.png')
        cc = await J(pg, "JSON.stringify({on:!!document.querySelector('#wpause .hh-c.on'), lk:document.querySelectorAll('#wpause .hh-c.lk').length})"); ok('cheat pocket: DOUBLE SHOT card on + 3 locked', cc['on'] and cc['lk'] == 3, cc)
        await J(pg, "phClose();1"); await pg.wait_for_timeout(300)
        # DOUBLE SHOT loads on start and fires twice
        await J(pg, "FFF_HH.practice();1"); await pg.wait_for_timeout(5200)
        dq = await J(pg, "JSON.stringify({dbl:FFF_HH.cur().cfg.dbl, pd:FFF_HH.cur().G._pe()[0].dbl})")
        ok('cheat loads on start (player DOUBLE SHOT)', 'p' in dq['dbl'] and dq['pd'], dq)
        await J(pg, "(function(){var G=FFF_HH.cur().G,pe=G._pe();pe[0].x=60;pe[1].x=320;pe[1].aiT=99;pe[1].want={};pe[0].st='idle';pe[0].mv=null;return 1})()")
        await J(pg, "FFF_HH.cur().G.press('sp');FFF_HH.cur().G.release('sp');1"); await pg.wait_for_timeout(900)
        twin = await J(pg, "JSON.stringify({pj:FFF_HH.cur().G._pj(), f:FFF_HH.cur().G._pe()[0].c.mv.sp[2]})"); ok('DOUBLE SHOT: the special fires twice', twin['pj'] >= 2 or twin['f'] != 'proj', twin)
        await J(pg, "FFF_HH.cur().kill(true);1"); await pg.wait_for_timeout(500)
        # stars: four quarters on one fighter = a star, stats up
        await J(pg, "SAVE.hh.qs.ryo=4;SAVE.hh.sel='ryo';save();1"); await J(pg, "FFF_HH.practice();1"); await pg.wait_for_timeout(1500)
        sc = await J(pg, "JSON.stringify(FFF_HH.cur().cfg)"); await J(pg, "FFF_HH.cur().kill(true);1"); await pg.wait_for_timeout(400)
        ok('4 quarters = \u26052: damage, HP and speed up', sc['pk'] > 1 and sc['ph'] > 1 and sc['ps'] > 1, sc)
        # pools: no repeat until the pool cycles
        pp = await J(pg, "(function(){var B=FFF_HH.banter()[FFF_HH.path()].walk, seen=[];SAVE.hh.bp={};for(var i=0;i<B.length;i++){var ex=FFF_HH.walkUp('kaito');seen.push(B.indexOf(ex));}return JSON.stringify(seen)})()")
        ok('walk-up pool: no repeats until it cycles', len(set(pp)) == len(pp) and -1 not in pp, pp)
        # ---------- persistence + reload in the middle of a match ----------
        before = await J(pg, "JSON.stringify(SAVE.hh)")
        await J(pg, "FFF_HH.practice();1"); await pg.wait_for_timeout(4600)
        ok('a match is running before the reload', (await J(pg, "FFF_HH.cur()&&FFF_HH.cur().st()")) == 'play')
        await pg.reload(); await pg.wait_for_timeout(2500); await boot(pg, cont=True); await pg.wait_for_timeout(800); await J(pg, HUSH)
        after = await J(pg, "JSON.stringify(SAVE.hh)")
        keys = ['own', 'beat', 'unl', 'cheats', 'cOn', 'lead', 'hint', 'qs']
        ok('save survives a reload', all(before.get(k) == after.get(k) for k in keys), {k: [before.get(k), after.get(k)] for k in keys if before.get(k) != after.get(k)})
        await J(pg, "clearRoam();W.spawnT=1e12;1")
        await world_ok(pg, 'after a reload mid-match')
        ok('no page errors', not errs, errs[:5])
        await b.close()
    n = sum(1 for _, c in R if c); print('\n%d / %d passed' % (n, len(R)))
    sys.exit(0 if n == len(R) else 1)
def hhStrip(t): return re.sub(r'\{/?[a-z]+(=\d+)?\}', '', t)
asyncio.run(main())
