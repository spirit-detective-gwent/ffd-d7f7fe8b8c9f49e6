#!/workspace/pwenv/bin/python3
"""Record the Gouki Main Court entry on a build (video). usage: media.py ROOT PORT OUTDIR TAG"""
import asyncio, sys, time, functools, http.server, socketserver, threading, shutil
from pathlib import Path
ROOT, PORT, OUT, TAG = Path(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]; OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(Path(__file__).parent))
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True; daemon_threads = True
raw = (ROOT / "index.html").read_bytes().replace(b"root.WORLD_API = {", b"root.__ev=function(s){return eval(s)};root.WORLD_API = {", 1)
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
HUSH = """(function(){try{close()}catch(e){}W.scGen=(W.scGen|0)+1;W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];W.runUp=false;try{while((W.scr|0)>0)sLock(0)}catch(e5){}var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML='';}var w=document.getElementById('wintro');if(w)w.remove();try{if(typeof FFF_SCAM!=='undefined'&&FFF_SCAM.clear)FFF_SCAM.clear()}catch(e7){}W.pan=null;W.scrCam=null;return 1})()"""
NEXT = """(function(){var d=document.getElementById('wdlg');if(!d||!d.classList.contains('on'))return 0;var b=[...d.querySelectorAll('button')].find(e=>/Next|Fight/.test(e.textContent)&&e.offsetParent);if(b){b.click();return 1}return 0})()"""
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
        # warm-up page (no video) to reach the court state quickly, then a recorded page
        ctx = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, is_mobile=True, has_touch=True, record_video_dir=str(OUT / ("vid_" + TAG)), record_video_size={"width": 390, "height": 844})
        pg = await ctx.new_page(); tpage = time.time()
        await pg.goto(f"http://127.0.0.1:{PORT}/index.html", wait_until="domcontentloaded", timeout=90000)
        await pg.wait_for_timeout(3000); await pg.touchscreen.tap(195, 422); await pg.wait_for_timeout(200)
        await ev(pg, "(function(){try{root.FFF_CRAWL_MS=1;root.FFF_CIN_K=1;ST.set.cam='on';ST.set.tips=false;ST.set.txt='fast';ST.set.rm=false;}catch(e){}return 1})()")
        await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(2000)
        for i in range(14):
            c = await pg.evaluate(SK)
            if not c: break
            await pg.touchscreen.tap(*c); await pg.wait_for_timeout(200)
        await ev(pg, HUSH); await pg.wait_for_timeout(500)
        tstart = time.time(); (OUT / f"{TAG}_offset.txt").write_text(str(round(tstart - tpage, 2)))
        await ev(pg, "(function(){SAVE.intro=1;SAVE.chapter=1;SAVE.gouki=0;SAVE.ch1=0;SAVE.ngp=0;SAVE.bent={};SAVE.icard={ryo:1,aoi:1};var S=gymS();S.sl={lockers:1,weight:1,side:1};S.e.press=1;S.e.arena=1;intFade(function(){gymGo('arena');});return 1})()")
        t0 = time.time(); walked = False; last = 0; marks = []
        while time.time() - t0 < 40:
            T = time.time() - t0
            if not walked and T > 2.4:
                walked = True; r = await ev(pg, "(function(){if(W.gymBossBusy||W.gkCine)return 0;var g=W.gymGouki;walkTo(g.x,g.y+70,true,true);return 1})()")
            dl = await ev(pg, NEXT.replace("b.click();return 1", "return 2"))
            if dl and time.time() - last > 2.2:
                await ev(pg, NEXT); last = time.time(); marks.append(round(T, 2))
            on = await ev(pg, "W.on")
            if not on and T > 4: await pg.wait_for_timeout(1800); break
            await pg.wait_for_timeout(100)
        lead = t0 - (tstart - 0)  # unused
        (OUT / f"{TAG}_marks.txt").write_text(str({"skip_to_scene_s": None, "next_clicks": marks}))
        vp = pg.video; await ctx.close(); path = await vp.path(); shutil.copy(path, OUT / f"{TAG}.webm")
        await b.close()
asyncio.run(main())
