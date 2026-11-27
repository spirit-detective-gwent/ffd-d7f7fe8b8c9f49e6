#!/workspace/pwenv/bin/python3
"""Gouki Main Court entry cinematic (Erik t535).
usage: test_goukicine.py <worktree> [port] [--only=mode,...] [--shots]
Modes: fierce (first visit, south door), strategic (first visit), repeat (entrance already seen), west (Trophy Hall door),
       ngp (NG+), near (re-entered without a room change: the walk-up trigger still plays the cinematic), aoi (Aoi leading).
Checks per mode:
  - the cinematic starts on its own after entering the court, input locked while they walk (W.scr > 0)
  - Ryo's position moves toward Gouki and stops at the set distance (Aoi too)
  - while stopped (dialogue / arrival), nobody runs in place: whenever a walker's position does not change between samples,
    its walk frame does not change, run is off, moving is off, and the frame is a standing frame (2 / 6 of the 8-frame cycle)
  - the fight starts (W.on false, battle board up) and no page errors
"""
import asyncio, json, sys, functools, http.server, socketserver, threading, time
from pathlib import Path
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
ROOT = Path(ARGS[0] if ARGS else "/workspace/goukicine/wt"); PORT = int(ARGS[1]) if len(ARGS) > 1 else 53201
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--only=")), None); SHOTS = "--shots" in sys.argv
SD = Path("/workspace/goukicine/shots"); SD.mkdir(parents=True, exist_ok=True)
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True; daemon_threads = True
def serve():
    raw = (ROOT / "index.html").read_bytes(); n = b"root.WORLD_API = {"
    raw = raw.replace(n, b"root.__ev=function(s){return eval(s)};" + n, 1)
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_GET(self):
            if self.path.split("?", 1)[0] in ("/", "/index.html"):
                self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(raw))); self.end_headers(); self.wfile.write(raw); return
            return super().do_GET()
    h = TS(("127.0.0.1", PORT), functools.partial(Q, directory=str(ROOT))); threading.Thread(target=h.serve_forever, daemon=True).start()
RES = []
def ok(name, cond, extra=""):
    RES.append((bool(cond), name, str(extra)[:400])); print(("PASS " if cond else "FAIL ") + name + (" :: " + str(extra)[:400] if extra else ""), flush=True)
async def ev(pg, code):
    return await pg.evaluate("(c)=>{try{var r=__ev(c);return (r===undefined)?null:JSON.parse(JSON.stringify(r))}catch(e){return {__err:String(e&&e.message||e)}}}", code)
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
HUSH = """(function(){try{close()}catch(e){}W.scGen=(W.scGen|0)+1;W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];W.runUp=false;try{while((W.scr|0)>0)sLock(0)}catch(e5){}var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML='';}var w=document.getElementById('wintro');if(w)w.remove();try{if(typeof FFF_SCAM!=='undefined'&&FFF_SCAM.clear)FFF_SCAM.clear()}catch(e7){}W.pan=null;W.scrCam=null;W.libCamHold=0;W.bossCamHold=0;return 1})()"""
STATE = """(function(){var d=document.getElementById('wdlg'),r=W.ryo,a=W.aoi,g=W.gymGouki;
 function w(s){return s?[Math.round(s.x*10)/10,Math.round(s.y*10)/10,s.fr,!!s.moving,!!s.run,s.nc|0]:null}
 return {r:w(r),a:(a&&a.el&&a.el.style.visibility!=='hidden')?w(a):null,g:g?[g.x,g.y]:null,dlg:!!(d&&d.classList.contains('on')),boss:!!(root.FFF_SCAM&&FFF_SCAM.st.boss),
 ru:!!W.runUp,cine:W.gkCine|0,at:W.gkCineAt||null,scr:W.scr|0,on:!!W.on,busy:W.gymBossBusy|0,fight:!!W.__gkFight,room:W.inside&&W.inside.id};})()"""
HOOK = """(function(){if(W.__gkHook)return 1;W.__gkHook=1;var _f=fight;fight=function(grp,boss,ctx){if(boss&&ctx&&ctx._ru)W.__gkFight={t:performance.now(),r:[W.ryo.x,W.ryo.y]};return _f.apply(this,arguments)};
 var _g=fight;return 2})()"""
def setup(mode):
    path = "strategic" if mode == "strategic" else "fierce"
    bent = "SAVE.bent={gouki:1};" if mode in ("repeat", "near") else "SAVE.bent={};"
    ngp = "SAVE.ngp=1;" if mode == "ngp" else "SAVE.ngp=0;"
    act = "SAVE.act='aoi';" if mode == "aoi" else "SAVE.act='ryo';"
    land = "libLand(GYMG.arena,'gW')" if mode == "west" else "null"
    pre = "W.__near=1;" if mode == "near" else ""
    return ("(function(){SAVE.intro=1;SAVE.chapter=1;SAVE.gouki=0;SAVE.ch1=0;SAVE.dbl=0;SAVE.gkPh=0;SAVE.gkRevives=0;" + ngp + bent + act + pre +
            "SAVE.bond=Object.assign(SAVE.bond||{},{path:'" + path + "',lock:1});SAVE.icard={ryo:1,aoi:1};var S=gymS();S.sl={lockers:1,weight:1,side:1};S.e.press=1;S.e.arena=1;"
            "try{if(typeof swapTo==='function'&&SAVE.act==='aoi'){}}catch(e){}"
            "gymGo('arena'," + land + ");if(W.__near){W.gkCineArm=0;}return {r:[W.ryo.x,W.ryo.y],g:W.gymGouki&&[W.gymGouki.x,W.gymGouki.y],act:SAVE.act,who:W.ryo.el.dataset.who};})()")
NEXT = """(function(){var d=document.getElementById('wdlg');if(!d||!d.classList.contains('on'))return 0;var b=[...d.querySelectorAll('button')].find(e=>/Next|Fight|Continue|OK/.test(e.textContent)&&e.offsetParent);if(b){b.click();return 1}return 0})()"""
async def run_mode(p, mode):
    b = await p.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
    ctx = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
    pg = await ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    await pg.goto(f"http://127.0.0.1:{PORT}/index.html", wait_until="domcontentloaded", timeout=90000)
    await pg.wait_for_timeout(3000); await pg.touchscreen.tap(195, 422); await pg.wait_for_timeout(200)
    await ev(pg, "(function(){try{root.FFF_CRAWL_MS=1;root.FFF_CIN_K=1;ST.set.cam='on';ST.set.tips=false;ST.set.txt='fast';ST.set.rm=false;}catch(e){}return 1})()")
    await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(2000)
    for i in range(14):
        c = await pg.evaluate(SK)
        if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(200)
    await ev(pg, HUSH); await ev(pg, HOOK)
    info = await ev(pg, setup(mode)); print("SETUP", mode, info, flush=True)
    log = []; t0 = time.time(); last_next = 0; nshot = 0; walked = False
    while time.time() - t0 < 60:
        s = await ev(pg, STATE); s["T"] = round(time.time() - t0, 2); log.append(s)
        if mode == "near" and not walked and s["T"] > 1.6:
            walked = True  # player walks toward him by hand (no room change): the proximity trigger must play the same cinematic
            await ev(pg, "(function(){var g=W.gymGouki;walkTo(g.x-20,g.y+120,true,false);return 1})()")
        if SHOTS and nshot < 60 and s["T"] > nshot * 0.5:
            await pg.screenshot(path=str(SD / f"test_{mode}_{nshot:02d}.png")); nshot += 1
        if s["dlg"] and time.time() - last_next > 0.9:
            if await ev(pg, NEXT): last_next = time.time()
        if s["fight"] and not s["on"]:
            await pg.wait_for_timeout(1200); s2 = await ev(pg, "(function(){return {on:!!W.on,bt:!!document.querySelector('#hand .card, #hand, .hand')}})()"); log.append({"post": s2}); break
        await pg.wait_for_timeout(70)
    await ctx.close(); await b.close()
    L = [x for x in log if "r" in x]
    (SD / f"test_{mode}.json").write_text(json.dumps(log))
    cine = [x for x in L if x["cine"]]
    ok(f"{mode}: cinematic starts on its own after entering the court", bool(cine), info)
    if not cine: return
    walk = [x for x in cine if not x["at"]]
    ok(f"{mode}: input locked while they walk in", walk and all(x["scr"] > 0 for x in walk), [x["scr"] for x in walk][:20])
    g = L[0]["g"]; d0 = ((cine[0]["r"][0] - g[0]) ** 2 + (cine[0]["r"][1] - g[1]) ** 2) ** 0.5
    stop = [x for x in cine if x["at"] and not x["ru"]]
    ok(f"{mode}: a stopped phase is reached", bool(stop))
    if stop:
        ds = ((stop[0]["r"][0] - g[0]) ** 2 + (stop[0]["r"][1] - g[1]) ** 2) ** 0.5
        mv = ((stop[0]["r"][0] - cine[0]["r"][0]) ** 2 + (stop[0]["r"][1] - cine[0]["r"][1]) ** 2) ** 0.5
        ok(f"{mode}: Ryo's position moves in and stops at the set distance", (mv > 30 or d0 < 190) and 120 <= ds <= 180, {"d0": round(d0), "dStop": round(ds), "moved": round(mv)})
        if stop[0]["a"]:
            da = ((stop[-1]["a"][0] - g[0]) ** 2 + (stop[-1]["a"][1] - g[1]) ** 2) ** 0.5
            ok(f"{mode}: Aoi comes in and stops beside him", da < 220, round(da))
    bad = []
    for who in ("r", "a"):
        for i in range(1, len(L)):
            p, c = L[i - 1], L[i]
            if not (p.get(who) and c.get(who)) or c["ru"] or not c["on"]: continue
            if not (c["cine"] or c["busy"]): continue
            if p[who][0] == c[who][0] and p[who][1] == c[who][1]:
                f = c[who]; standing = f[2] in (2, 6) if f[5] == 8 else True
                if f[2] != p[who][2] or f[3] or f[4] or not standing: bad.append((who, c["T"], p[who], f))
    held = sum(1 for x in stop)
    ok(f"{mode}: nobody runs in place while stopped (run anim off when velocity is 0)", not bad and held > 5, {"bad": bad[:6], "held_samples": held})
    fs = [x for x in L if x["fight"]]
    post = next((x["post"] for x in log if "post" in x), None)
    ok(f"{mode}: the fight starts", bool(fs) and post and not post["on"], post)
    ok(f"{mode}: no page errors", not errs, errs)
async def main():
    from playwright.async_api import async_playwright
    serve()
    modes = ["fierce", "strategic", "repeat", "west", "ngp", "near", "aoi"]
    if ONLY: modes = [m for m in modes if m in ONLY]
    async with async_playwright() as p:
        for m in modes:
            try: await run_mode(p, m)
            except Exception as e: ok(f"{m}: ran", False, repr(e))
    P = sum(1 for r in RES if r[0]); F = len(RES) - P
    print(f"\nRESULT {P} passed, {F} failed", flush=True); sys.exit(1 if F else 0)
asyncio.run(main())
