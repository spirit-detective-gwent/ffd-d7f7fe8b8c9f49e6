#!/workspace/pwenv/bin/python3
"""Probe the Gouki Main Court entry: sample Ryo/Aoi position + walk frame + flags every 80 ms."""
import asyncio, json, sys, functools, http.server, socketserver, threading, time
from pathlib import Path
ROOT = Path(sys.argv[1]); PORT = int(sys.argv[2]); OUT = sys.argv[3]; MODE = sys.argv[4] if len(sys.argv) > 4 else "first"
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
async def ev(pg, code):
    return await pg.evaluate("(c)=>{try{var r=__ev(c);return (r===undefined)?null:JSON.parse(JSON.stringify(r))}catch(e){return {__err:String(e&&e.message||e)}}}", code)
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
HUSH = """(function(){try{close()}catch(e){}W.scGen=(W.scGen|0)+1;W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];W.runUp=false;try{while((W.scr|0)>0)sLock(0)}catch(e5){}var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML='';}var w=document.getElementById('wintro');if(w)w.remove();try{if(typeof FFF_SCAM!=='undefined'&&FFF_SCAM.clear)FFF_SCAM.clear()}catch(e7){}W.pan=null;W.scrCam=null;W.libCamHold=0;W.bossCamHold=0;return 1})()"""
STATE = """(function(){var d=document.getElementById('wdlg'),r=W.ryo,a=W.aoi,g=W.gymGouki;
 function bp(s){return s&&s.el?s.el.style.backgroundPosition:null}
 return {t:performance.now(),r:r?[Math.round(r.x),Math.round(r.y),r.fr,bp(r),!!r.moving,Math.round(r.v||0)]:null,a:a?[Math.round(a.x),Math.round(a.y),a.fr,bp(a),!!a.moving]:null,
 g:g?[Math.round(g.x),Math.round(g.y)]:null,dlg:!!(d&&d.classList.contains('on')),intro:!!document.getElementById('wintro'),boss:!!(root.FFF_SCAM&&FFF_SCAM.st.boss),
 ru:!!W.runUp,busy:W.gymBossBusy|0,on:!!W.on,path:(W.path||[]).length,room:W.inside&&W.inside.id,fight:!!(document.querySelector('#battle.on, .bt-on, #bt.on'))||!W.on};})()"""
async def main():
    from playwright.async_api import async_playwright
    serve()
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
        ctx = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
        pg = await ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        await pg.goto(f"http://127.0.0.1:{PORT}/index.html", wait_until="domcontentloaded", timeout=90000)
        await pg.wait_for_timeout(3000); await pg.touchscreen.tap(195, 422); await pg.wait_for_timeout(200)
        await ev(pg, "(function(){try{root.FFF_CRAWL_MS=1;ST.set.cam='on';ST.set.tips=false;ST.set.txt='fast';ST.set.rm=false;}catch(e){}return 1})()")
        await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(2000)
        for i in range(14):
            c = await pg.evaluate(SK)
            if not c: break
            await pg.touchscreen.tap(*c); await pg.wait_for_timeout(200)
        await ev(pg, HUSH)
        bent = "SAVE.bent={};" if MODE == "first" else "SAVE.bent={gouki:1};"
        ngp = "SAVE.ngp=1;" if MODE == "ngp" else "SAVE.ngp=0;"
        print(await ev(pg, "(function(){SAVE.intro=1;SAVE.chapter=1;SAVE.gouki=0;SAVE.ch1=0;" + ngp + bent + "SAVE.icard={ryo:1,aoi:1};var S=gymS();S.sl={lockers:1,weight:1,side:1};S.e.press=1;S.e.arena=1;gymGo('arena');return {r:[W.ryo.x,W.ryo.y],g:W.gymGouki&&[W.gymGouki.x,W.gymGouki.y]};})()"))
        await pg.wait_for_timeout(1800)
        await ev(pg, "(function(){var g=W.gymGouki;walkTo(g.x,g.y+70,true,true);return 1})()")
        log = []; t0 = time.time(); last_adv = 0; shots = 0
        while time.time() - t0 < 40:
            s = await ev(pg, STATE); s["T"] = round(time.time() - t0, 2); log.append(s)
            if shots < 40 and int(s["T"] * 2) > shots:
                await pg.screenshot(path=f"{OUT}_{shots:02d}.png"); shots += 1
            if s.get("dlg") and time.time() - last_adv > 1.2:
                await ev(pg, "(function(){var d=document.getElementById('wdlg');var b=[...d.querySelectorAll('button')].find(e=>/Next|Fight|Continue|OK/.test(e.textContent)&&e.offsetParent);if(b){b.click();return 'b'}d.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,cancelable:true}));return 'd'})()"); last_adv = time.time()
            if not s.get("on") and s["T"] > 3: 
                await pg.wait_for_timeout(1500); await pg.screenshot(path=f"{OUT}_fight.png"); break
            await pg.wait_for_timeout(80)
        Path(OUT + ".json").write_text(json.dumps({"log": log, "errs": errs}))
        print("errs", errs, "samples", len(log))
        await b.close()
asyncio.run(main())
