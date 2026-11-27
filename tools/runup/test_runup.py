#!/workspace/pwenv/bin/python3
"""Ch1 sub-boss run-up checks (Erik t534): Ryo must actually run up to every Ch1 mini
(Mizuno, Mai, Kurata, Bando) and the fight must start on arrival, no stall.
usage: test_runup.py <worktree> [port] [--index=PATH] [--tag=TAG] [--shot]
Checks per boss, first visit (boss entrance plays) and repeat visit:
  - Fight pressed -> fight() entered (run-up done) in < 2.0 s
  - Ryo's distance to the foe shrinks during the run-up when he starts > 62 px away
"""
import asyncio, json, sys, functools, http.server, socketserver, threading, time
from pathlib import Path
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
ROOT = Path(ARGS[0] if ARGS else "/workspace/runup/wt")
PORT = int(ARGS[1]) if len(ARGS) > 1 else 52811
INDEX = None; TAG = "after"; SHOT = "--shot" in sys.argv
for a in sys.argv[1:]:
    if a.startswith("--index="): INDEX = Path(a.split("=", 1)[1])
    if a.startswith("--tag="): TAG = a.split("=", 1)[1]
SHOTS = Path("/workspace/runup/shots"); SHOTS.mkdir(parents=True, exist_ok=True)
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True; daemon_threads = True
def serve():
    raw = (INDEX or ROOT / "index.html").read_bytes(); n = b"root.WORLD_API = {"
    raw = raw.replace(n, b"root.__ev=function(s){return eval(s)};" + n, 1)
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_GET(self):
            if self.path.split("?", 1)[0] in ("/", "/index.html"):
                self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(raw))); self.send_header("Cache-Control", "no-store"); self.end_headers(); self.wfile.write(raw); return
            return super().do_GET()
    h = TS(("127.0.0.1", PORT), functools.partial(Q, directory=str(ROOT))); threading.Thread(target=h.serve_forever, daemon=True).start(); return h
RES = []
def ok(name, cond, extra=""):
    RES.append((bool(cond), name, str(extra)[:400]))
    print(("PASS " if cond else "FAIL ") + name + (" :: " + str(extra)[:400] if extra else ""), flush=True)
async def ev(pg, code):
    return await pg.evaluate("(c)=>{try{var r=__ev(c);return (r===undefined)?null:JSON.parse(JSON.stringify(r))}catch(e){return {__err:String(e&&e.message||e)}}}", code)
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
async def skipall(pg, n=14):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(200); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(200)
    await pg.evaluate("(()=>{var b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Close'&&e.offsetParent);if(b)b.click()})()")
HUSH = """(function(){try{close()}catch(e){}W.scGen=(W.scGen|0)+1;W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];W.runUp=false;try{while((W.scr|0)>0)sLock(0)}catch(e5){}var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML='';}var w=document.getElementById('wintro');if(w)w.remove();try{if(typeof FFF_SCAM!=='undefined'&&FFF_SCAM.clear)FFF_SCAM.clear()}catch(e7){}W.pan=null;W.scrCam=null;W.libCamHold=0;W.bossCamHold=0;W._bossCamOff=0;W._bossCamUntilSwirl=0;W.fldBossT=0;return 1})()"""
HOOK = """(function(){ if(W.__ruHook) return 1; W.__ruHook=1;
  var _f=fight; fight=function(grp,boss,ctx){ if(ctx&&ctx.mini&&!W.__ru1){ var r=W.ryo; if(!ctx._ru){ var t=runUpTarget(grp,boss); W.__ru0={t:performance.now(),r:[r.x,r.y],a:W.aoi?[W.aoi.x,W.aoi.y]:null,tg:t?[t.x,t.y]:null,id:ctx.mini}; }
      else W.__ru1={t:performance.now(),r:[r.x,r.y],a:W.aoi?[W.aoi.x,W.aoi.y]:null}; }
    if(ctx&&ctx.mini&&W.__ru0&&!W.__ru1&&!W.__ruNoFight&&false){}
    return _f.apply(this,arguments); };
  return 2; })()"""
# Enter the boss room fresh. first=True -> entrance never seen (bossEnt plays, FFF_SCAM boss + bridge).
def setup(boss, first):
    bent = "SAVE.bent={};" if first else f"SAVE.bent=SAVE.bent||{{}};SAVE.bent['{boss}']=1;"
    common = f"""SAVE.intro=1;SAVE.chapter=1;SAVE.gouki=0;SAVE.ngp=0;SAVE.mb=SAVE.mb||{{}};delete SAVE.mb['{boss}'];SAVE.icard={{ryo:1,aoi:1}};
      SAVE.ic=SAVE.ic||{{}};{bent}try{{ST.set.cam='on';ST.set.rm=false;ST.set.txt='fast';delete root.FFF_SKIP_INTRO;root.FFF_SCAM_OFF=false;}}catch(e){{}}
      W.__ru0=null;W.__ru1=null;"""
    if boss == "mb_lib":
        body = "var L=dgS('lib');L.e={foyer:1,hall:1,stacks:1,carrels:1,ante:1};L.unp={s_pony:1,s_mio:1,s_boy:1};L.akey=1;L.okey=1;libGo('archive');"
    elif boss == "mb_art":
        body = "var S=artS();delete S.e.stage;artGo('stage');setTimeout(function(){if(!W.dlg&&!W.__ru0&&!(FFF_SCAM&&FFF_SCAM.st.boss))artBoss();},1500);"
    elif boss == "mb_cafe":
        body = "var S=cafS();delete S.e.dining;cafGo('dining');setTimeout(function(){if(!W.dlg&&!W.__ru0&&!(FFF_SCAM&&FFF_SCAM.st.boss))cafBoss();},1500);"
    else:
        body = "var S=fldS();delete S.e.boss;fldGo('track');setTimeout(function(){W.fldBossT=0;fldBoss({direct:1});},1200);"
    return "(function(){" + common + body + "return {room:W.inside&&W.inside.id};})()"
STATE = """(function(){var d=document.getElementById('wdlg'),bs=[...document.querySelectorAll('button')].filter(b=>b.offsetParent);
 return {intro:!!document.getElementById('wintro'),dlg:!!(d&&d.classList.contains('on')),fight:bs.some(b=>b.textContent.trim()==='Fight'),
 ru:!!W.runUp,on:!!W.on,ru0:W.__ru0,ru1:W.__ru1,boss:!!(root.FFF_SCAM&&FFF_SCAM.st&&FFF_SCAM.st.boss),room:W.inside&&W.inside.id,
 r:W.ryo?[W.ryo.x,W.ryo.y]:null};})()"""
ADV = """(function(){var e=document.getElementById('wintro');if(e){var b=e.querySelector('.iskip');if(b)b.click();else e.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,cancelable:true}));return 'intro';}
 var d=document.getElementById('wdlg');if(d&&d.classList.contains('on')){var b2=d.querySelector('.bt button, button.hot, .next, .ok');if(b2&&!/Walk away/.test(b2.textContent)){b2.click();return 'btn';}
 d.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,cancelable:true}));return 'dlg';}
 document.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,cancelable:true}));return 'tap';})()"""
async def run_boss(pg, boss, first):
    tag = f"{boss}_{'first' if first else 'repeat'}"
    await ev(pg, HUSH); await ev(pg, "(function(){if(!W.inside)return 1;try{intOut&&intOut()}catch(e){}return 1})()")
    await pg.wait_for_timeout(300)
    info = await ev(pg, setup(boss, first))
    print("SETUP", tag, info, flush=True)
    t0 = time.time(); clicked = None; s = None
    while time.time() - t0 < 60:
        s = await ev(pg, STATE)
        if s.get("ru0"):
            clicked = time.time(); break
        if s.get("fight"):
            await ev(pg, "(function(){var b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Fight'&&e.offsetParent);b.click();return 1})()")
            clicked = time.time(); break
        await ev(pg, ADV); await pg.wait_for_timeout(180 if not s.get("ru") else 60)
    ok(f"{tag} reached the Fight prompt", clicked is not None, s)
    if not clicked: return
    shot_done = False; mid = None
    while time.time() - clicked < 8:
        s = await ev(pg, STATE)
        if SHOT and not shot_done and s.get("ru") and time.time() - clicked > 0.45:
            await pg.screenshot(path=str(SHOTS / f"{TAG}_{tag}_runup.png")); shot_done = True; mid = s
        if s.get("ru1"): break
        await pg.wait_for_timeout(40)
    ru0, ru1 = s.get("ru0"), s.get("ru1")
    ok(f"{tag} run-up hooked", bool(ru0 and ru1), s)
    if not (ru0 and ru1): return
    dt = (ru1["t"] - ru0["t"]) / 1000.0
    tg = ru0.get("tg")
    d0 = ((ru0["r"][0] - tg[0]) ** 2 + (ru0["r"][1] - tg[1]) ** 2) ** 0.5 if tg else 0
    d1 = ((ru1["r"][0] - tg[0]) ** 2 + (ru1["r"][1] - tg[1]) ** 2) ** 0.5 if tg else 0
    moved = ((ru1["r"][0] - ru0["r"][0]) ** 2 + (ru1["r"][1] - ru0["r"][1]) ** 2) ** 0.5
    am = ((ru1["a"][0] - ru0["a"][0]) ** 2 + (ru1["a"][1] - ru0["a"][1]) ** 2) ** 0.5 if ru0.get("a") and ru1.get("a") else 0
    det = {"t": round(dt, 2), "d0": round(d0), "d1": round(d1), "ryoMoved": round(moved), "aoiMoved": round(am)}
    print("RUNUP", tag, json.dumps(det), flush=True)
    ok(f"{tag} fight starts under 2.0 s after Fight", dt < 2.0, det)
    if d0 > 62:
        ok(f"{tag} Ryo runs toward the foe (gap closes to <= 75 px)", d1 < d0 - 20 and d1 <= 75, det)
        ok(f"{tag} Aoi follows", am > 10, det)
    else:
        ok(f"{tag} already at the foe (no run needed)", d1 <= 75, det)
    if SHOT and shot_done:
        await pg.screenshot(path=str(SHOTS / f"{TAG}_{tag}_arrive.png"))
    # let the swirl / fight come up, then leave the battle
    await pg.wait_for_timeout(2600)
    await ev(pg, "(function(){try{if(root.FFF&&FFF.b&&FFF.end)FFF.end()}catch(e){}return 1})()")
async def main():
    from playwright.async_api import async_playwright
    serve()
    bosses = [b for b in ["mb_lib", "mb_art", "mb_cafe", "mb_field"] if not any(a.startswith("--only=") for a in sys.argv) or b in [x.split("=",1)[1] for x in sys.argv if x.startswith("--only=")][0].split(",")]
    async with async_playwright() as p:
        for boss in bosses:
            for first in (True, False):
                b = await p.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
                ctx = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
                pg = await ctx.new_page(); errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
                await pg.goto(f"http://127.0.0.1:{PORT}/index.html", wait_until="domcontentloaded", timeout=90000)
                await pg.wait_for_timeout(3000); await pg.touchscreen.tap(195, 422); await pg.wait_for_timeout(200)
                await ev(pg, "(function(){try{root.FFF_CRAWL_MS=1;ST.set.cam='on';ST.set.tips=false;ST.set.txt='fast';ST.set.rm=false;}catch(e){}return 1})()")
                await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(2000); await skipall(pg)
                await ev(pg, HUSH); await ev(pg, HOOK)
                await run_boss(pg, boss, first)
                ok(f"{boss} {'first' if first else 'repeat'} no page errors", not errs, errs)
                await ctx.close(); await b.close()
    P = sum(1 for r in RES if r[0]); F = len(RES) - P
    print(f"\nRESULT {P} passed, {F} failed, tag={TAG}", flush=True)
    (SHOTS / f"{TAG}_results.json").write_text(json.dumps([{"ok": a, "name": n, "extra": e} for a, n, e in RES], indent=2))
    sys.exit(1 if F else 0)
asyncio.run(main())
