#!/workspace/pwenv/bin/python3
"""v6565-nursecab: Ch1 nurse white cabinet restocks once per Ch1 MAIN quest (1 gauze + 1 tape, no timer, no stacking).
usage: test_cab.py <worktree> [port] [--shots DIR] [--live]   (--live: only the 'before' shot, on a tree without cabQuestDone)
Real game functions in a headless 390x844 page."""
import asyncio, sys, functools, http.server, socketserver, threading, json
from pathlib import Path
from playwright.async_api import async_playwright
args = sys.argv[1:]
def opt(name, flag=False):
    if name in args:
        i = args.index(name)
        if flag: del args[i]; return True
        v = args[i + 1]; del args[i:i + 2]; return v
shots = opt('--shots'); live = opt('--live', True)
root = Path(args[0]); PORT = int(args[1]) if len(args) > 1 else 52671
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
    RES.append((bool(cond), name)); print(('PASS ' if cond else 'FAIL ') + name + ((' :: ' + str(extra)[:300]) if extra else ''), flush=True)
async def boot(p, init=None):
    b = await p.chromium.launch(headless=True, args=['--disable-dev-shm-usage'])
    ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True,
      user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mobile/15E148 Safari/604.1')
    if init: await ctx.add_init_script(init)
    pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(3500)
    await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(2500); await skipall(pg, 12)
    return b, ctx, pg, errs
CLR = "(function(){ W.scGen=(W.scGen|0)+1; try{sLock(0,'x')}catch(e){} try{close()}catch(e){} W.cut=false; W.dlg=false; W.scr=false; W.busy=false; W.qBusy=0; document.body.classList.remove('fff-dlg-on'); var o=document.getElementById('wquest'); if(o) o.remove(); })()"
DLG = "(function(){ var d=document.getElementById('wdlg'); return d&&d.offsetParent!==null? d.innerText : ''; })()"
CLOSE = "(()=>{var b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Close'&&e.offsetParent);if(b)b.click()})()"
# a mid-Ch1 save: nurse met, lesson learnt, library quest on its hand-in step
SETUP = """(function(){ SAVE.chapter=1; SAVE.ch1=0; SAVE.sc=SAVE.sc||{}; SAVE.craft=SAVE.craft||{}; SAVE.craft.dress=1; SAVE.sc.dress='done';
  SAVE.herbs={gauze:0,tape:0,leaf:0,ginger:0}; delete SAVE.cabR; SAVE.cabT=Date.now()-5000; SAVE.qs={}; SAVE.saved=[]; qStart('q_mb_lib'); SAVE.qs.q_mb_lib=2; save(); return 1; })()"""
MATS = "[phMatN('gauze'), phMatN('tape')]"
async def go_nurse(pg):
    r = await ev(pg, "(function(){ try { intGo('room'); return 'intGo'; } catch(e){ return String(e); } return 'none'; })()")
    await pg.wait_for_timeout(1800); await ev(pg, CLR); await pg.wait_for_timeout(600)
    return r
async def open_cab(pg):
    await ev(pg, "(function(){ root.FFF_FAST_KIT=1; n9Cabinet(); root.FFF_FAST_KIT=0; })()"); await pg.wait_for_timeout(700)
async def main():
    h = serve(root, PORT)
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p)
        await ev(pg, CLR); await ev(pg, SETUP)
        where = await go_nurse(pg); inside = await ev(pg, "W.inside && W.inside.id")
        print('nurse room:', where, inside)
        # complete the library main quest the real way (qDoneNow is what the @quest done scene step calls)
        await ev(pg, "qDoneNow()"); await pg.wait_for_timeout(300); await ev(pg, CLR)
        if live:
            await open_cab(pg); t = await ev(pg, DLG)
            ok('live: no restock after a main quest (cabinet text)', 'Take gauze' not in t, t)
            if shots: await pg.screenshot(path=str(Path(shots) / 'before_live_cabinet_after_quest.png'))
            ok('no page errors', not errs, errs); await b.close(); h.shutdown(); return
        ok('main quest done -> one restock waiting', await ev(pg, "SAVE.cabR") == 1)
        r2 = await ev(pg, "(function(){ qStart('q_mb_art'); SAVE.qs.q_mb_art=3; qDoneNow(); return [SAVE.qs.q_mb_art, SAVE.cabR]; })()"); await ev(pg, CLR)
        ok('second main quest before a visit does not stack', r2 == [9, 1], r2)
        await pg.wait_for_timeout(3800)
        await open_cab(pg); t = await ev(pg, DLG)
        ok('stocked text names the amount', 'Fresh supplies are in' in t and '1 Clean Gauze + 1 Medical Tape' in t and 'Restocks after you finish a main quest' in t, t)
        if shots: await pg.screenshot(path=str(Path(shots) / 'after_branch_cabinet_restocked.png'))
        m0 = await ev(pg, MATS)
        await pg.evaluate("(()=>{var b=[...document.querySelectorAll('button')].find(e=>/Take gauze and tape/.test(e.textContent)&&e.offsetParent);if(b)b.click()})()"); await pg.wait_for_timeout(900)
        m1 = await ev(pg, MATS)
        ok('take gives exactly 1 gauze + 1 tape (one dressing recipe)', m1[0] - m0[0] == 1 and m1[1] - m0[1] == 1, (m0, m1))
        ok('restock used up', not await ev(pg, "SAVE.cabR"))
        await ev(pg, CLR); await open_cab(pg); t = await ev(pg, DLG)
        ok('empty text explains the restock + amount, no take button', 'Restocks after you finish a main quest: 1 Clean Gauze + 1 Medical Tape' in t and 'Take gauze' not in t, t)
        if shots: await pg.screenshot(path=str(Path(shots) / 'after_branch_cabinet_empty.png'))
        await pg.evaluate(CLOSE); await ev(pg, CLR)
        await ev(pg, "n9Cabinet()"); await pg.wait_for_timeout(400)
        ok('empty open does not play the reach (no kit anim)', not await ev(pg, "!!(W.kit&&W.kit.phase)"))
        await ev(pg, "cabTake()"); ok('no timer refill: cabTake on empty gives nothing', await ev(pg, MATS) == m1)
        await ev(pg, CLR)
        # side quest / Ch2 main ids do not restock
        await ev(pg, "cabQuestDone('sq_lost_bag'); cabQuestDone('cq2_dig'); cabQuestDone('cq3_tide')")
        ok('side / Ch2 / Ch3 quest ids do not restock', not await ev(pg, "SAVE.cabR"))
        r = await ev(pg, "(function(){ var k=Object.keys(SQDEF||{})[0]; if(!k) return 'nosq'; var s=sqState(k); s.st=3; W.dlg=false; sqTurnIn(k); return k; })()")
        await pg.wait_for_timeout(600); await skipall(pg, 10); await ev(pg, CLR)
        ok('real Ch1 side-quest turn-in does not restock', not await ev(pg, "SAVE.cabR"), r)
        # c2QDone path (calls qDoneNow with a cq2_ id)
        await ev(pg, "(function(){ try{ var S=c2S(); S.qa='cq2_x'; S.q=S.q||{}; S.q.cq2_x=0; c2QDone('cq2_x'); }catch(e){} })()"); await ev(pg, CLR)
        ok('Ch2 main quest via c2QDone does not restock', not await ev(pg, "SAVE.cabR"))
        await ev(pg, SETUP.replace("SAVE.chapter=1", "SAVE.chapter=1").replace("qStart('q_mb_lib'); SAVE.qs.q_mb_lib=2;", "SAVE.qs.q_mb_lib=9;SAVE.qs.q_mb_art=9;SAVE.qs.q_mb_cafe=9;SAVE.qs.q_mb_field=9;qStart('q_gouki');"))
        await ev(pg, "(function(){ var q=qCur(); if(q&&q.d.steps.length===1){ SAVE.qs[q.id]=9; } })()")
        # Gouki single-step completion goes through qBeat's else-branch
        await ev(pg, "(function(){ SAVE.qs.q_gouki=0; SAVE.qa='q_gouki'; delete SAVE.cabR; try{ qBeat('gouki'); }catch(e){ return String(e); } })()"); await ev(pg, CLR)
        ok('Gouki (single-step main quest) restocks', await ev(pg, "SAVE.cabR") == 1)
        # reach animation plays when stocked
        await ev(pg, CLR); await ev(pg, "n9Cabinet()"); await pg.wait_for_timeout(250)
        anim = await ev(pg, "!!(W.kit&&W.kit.phase)") if await ev(pg, "W.inside&&W.inside.id") == 'room' else 'not-in-room'
        ok('stocked open plays the reach animation in the office', anim is True or anim == 'not-in-room', anim)
        for _ in range(24):
            t = await ev(pg, DLG)
            if 'Fresh supplies' in t: break
            await pg.wait_for_timeout(500)
        ok('after the reach the stocked dialog opens', 'Fresh supplies are in' in t, t)
        await pg.evaluate(CLOSE); await ev(pg, CLR)
        # lesson untouched
        l = await ev(pg, "(function(){ SAVE.herbs={gauze:0,tape:0}; SAVE.sc.dress='fetch'; root.FFF_FAST_KIT=1; n9Cabinet(); root.FFF_FAST_KIT=0; return ["+MATS+", SAVE.cabR]; })()")
        await skipall(pg, 6); await ev(pg, "(function(){ try{ W.v630Lesson=''; resume&&resume(); }catch(e){} })()"); await ev(pg, CLR)
        ok('lesson fetch still 1+1 and leaves the waiting restock alone', l[0] == [1, 1] and l[1] == 1, l)
        ok('free heal unchanged (HEAL.freePct, 90 s)', await ev(pg, "[Math.round(MAXHP*HEAL.freePct)]") == [12], await ev(pg, "[MAXHP, HEAL.freePct]"))
        # NG+ starts fresh
        ng = await ev(pg, "(function(){ SAVE.cabR=1; var o=FFF_NG.base(); var n=FFF_NG.build(SAVE,o); return [n.cabR===undefined||!n.cabR, n.chapter]; })()")
        ok('NG+ build starts the cabinet fresh (no carried restock)', ng and ng[0] is True, ng)
        # take right after a hand-in banner: pills wait until the banner is gone
        await ev(pg, "(function(){ document.querySelectorAll('#wmatpop i').forEach(function(e){e.remove()}); SAVE.cabR=1; qBanner('QUEST COMPLETE','Test',''); cabTake(); })()")
        await pg.wait_for_timeout(1000); early = await ev(pg, "document.querySelectorAll('#wmatpop i').length")
        if shots: await pg.screenshot(path=str(Path(shots) / 'after_branch_take_during_banner_1s.png'))
        late = 0
        for _ in range(40):
            await pg.wait_for_timeout(250); late = await ev(pg, "document.querySelectorAll('#wmatpop i').length")
            if late: break
        if shots: await pg.screenshot(path=str(Path(shots) / 'after_branch_take_after_banner.png'))
        ok('pills held while the QUEST COMPLETE banner is up, shown after', early == 0 and late == 2, (early, late))
        ok('no page errors', not errs, errs)
        await b.close()
        # old save (live v6.5.64 shape: cabT set, no cabR) loads clean
        old = "localStorage.setItem('fff_world', JSON.stringify(Object.assign(JSON.parse(localStorage.getItem('fff_world')||'{}'), {cabT: Date.now()-1000})));"
        b, ctx, pg, errs = await boot(p)
        await ev(pg, "(function(){ var s=JSON.parse(localStorage.getItem('fff_world')||'{}'); s.cabT=Date.now()-1000; delete s.cabR; localStorage.setItem('fff_world', JSON.stringify(s)); })()")
        await pg.reload(); await pg.wait_for_timeout(3500); await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(2500); await skipall(pg, 12); await ev(pg, CLR)
        await ev(pg, "(function(){ SAVE.sc=SAVE.sc||{}; SAVE.sc.dress='done'; })()"); await open_cab(pg); t = await ev(pg, DLG)
        ok('old save (cabT, no cabR) loads and shows the empty cabinet', 'Restocks after you finish a main quest' in t and not errs, (t, errs))
        await b.close()
    h.shutdown()
    bad = [n for c, n in RES if not c]
    print(f'{len(RES) - len(bad)}/{len(RES)} PASS'); sys.exit(1 if bad else 0)
asyncio.run(main())
