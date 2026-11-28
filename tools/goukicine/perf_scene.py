#!/workspace/pwenv/bin/python3
"""Perf of the Gouki Main Court entry, live vs branch, interleaved (L,B,L,B,...), waiting while the 1-min load > 6.
usage: perf_scene.py LIVE_DIR BRANCH_DIR [--runs 3] [--throttle 4] [--secs 16]
Window: from entering the court through the walk-in / arrival push / name card / first lines (live: the player walks up by hand).
fps, 1% low, p95 frame time, cpu_busy_pct (heat proxy), heap. iPhone size, dpr 3."""
import asyncio, sys, json, os, time, statistics, functools, http.server, socketserver, threading, argparse
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument("live"); ap.add_argument("br"); ap.add_argument("--runs", type=int, default=3); ap.add_argument("--throttle", type=float, default=4); ap.add_argument("--secs", type=float, default=16); ap.add_argument("--out", default="/workspace/goukicine/logs/perf_scene.json"); A = ap.parse_args()
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True; daemon_threads = True
def serve(root, port):
    raw = (Path(root) / "index.html").read_bytes(); n = b"root.WORLD_API = {"
    raw = raw.replace(n, b"root.__ev=function(s){return eval(s)};" + n, 1)
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_GET(self):
            if self.path.split("?", 1)[0] in ("/", "/index.html"):
                self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(raw))); self.end_headers(); self.wfile.write(raw); return
            return super().do_GET()
    h = TS(("127.0.0.1", port), functools.partial(Q, directory=str(root))); threading.Thread(target=h.serve_forever, daemon=True).start()
SAMPLER = """()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);}"""
def stats(ft):
    ft = ft[2:]; tot = sum(ft); s = sorted(ft, reverse=True); n = max(1, len(ft) // 100)
    return dict(fps=round(1000 * len(ft) / tot, 1), low1=round(1000 / (sum(s[:n]) / n), 1), p95=round(sorted(ft)[int(len(ft) * 0.95)], 2), worst=round(s[0]), frames=len(ft))
async def metrics(cdp):
    m = await cdp.send("Performance.getMetrics"); return {x["name"]: x["value"] for x in m["metrics"]}
async def ev(pg, code):
    return await pg.evaluate("(c)=>{try{var r=__ev(c);return (r===undefined)?null:JSON.parse(JSON.stringify(r))}catch(e){return {__err:String(e&&e.message||e)}}}", code)
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
HUSH = """(function(){try{close()}catch(e){}W.scGen=(W.scGen|0)+1;W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];W.runUp=false;try{while((W.scr|0)>0)sLock(0)}catch(e5){}var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML='';}var w=document.getElementById('wintro');if(w)w.remove();try{if(typeof FFF_SCAM!=='undefined'&&FFF_SCAM.clear)FFF_SCAM.clear()}catch(e7){}W.pan=null;W.scrCam=null;return 1})()"""
SETUP = "(function(){SAVE.intro=1;SAVE.chapter=1;SAVE.gouki=0;SAVE.ch1=0;SAVE.ngp=0;SAVE.bent={};SAVE.icard={ryo:1,aoi:1};var S=gymS();S.sl={lockers:1,weight:1,side:1};S.e.press=1;S.e.arena=1;gymGo('arena');return 1})()"
NEXT = """(function(){var d=document.getElementById('wdlg');if(!d||!d.classList.contains('on'))return 0;var b=[...d.querySelectorAll('button')].find(e=>/Next/.test(e.textContent)&&e.offsetParent);if(b){b.click();return 1}return 0})()"""
async def one(p, url, tag):
    b = await p.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
    ctx = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=3, is_mobile=True, has_touch=True,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
    cdp = await ctx.new_cdp_session(pg); await cdp.send("Performance.enable")
    await pg.goto(url, wait_until="domcontentloaded", timeout=120000); await pg.wait_for_timeout(3500); await pg.touchscreen.tap(195, 422); await pg.wait_for_timeout(200)
    await ev(pg, "(function(){try{root.FFF_CRAWL_MS=1;root.FFF_CIN_K=1;ST.set.cam='on';ST.set.tips=false;ST.set.txt='fast';ST.set.rm=false;}catch(e){}return 1})()")
    await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(2500)
    for i in range(14):
        c = await pg.evaluate(SK)
        if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(250)
    await ev(pg, HUSH); await pg.wait_for_timeout(1500)
    if A.throttle > 1: await cdp.send("Emulation.setCPUThrottlingRate", {"rate": A.throttle})
    await pg.evaluate(SAMPLER); m0 = await metrics(cdp); t0 = time.time()
    await ev(pg, SETUP); walked = False; last = 0
    while time.time() - t0 < A.secs:
        if not walked and time.time() - t0 > 1.8:
            walked = True; await ev(pg, "(function(){if(W.gymBossBusy||W.gkCine)return 0;var g=W.gymGouki;walkTo(g.x,g.y+70,true,true);return 1})()")
        if time.time() - last > 2.0 and time.time() - t0 > 12:
            if await ev(pg, NEXT): last = time.time()
        await pg.wait_for_timeout(250)
    m1 = await metrics(cdp); await pg.evaluate("window.__run=false"); ft = await pg.evaluate("window.__ft")
    wall = m1["Timestamp"] - m0["Timestamp"]; r = stats(ft)
    r["cpu_busy_pct"] = round(100 * (m1["TaskDuration"] - m0["TaskDuration"]) / wall, 1); r["heap_mb"] = round(m1["JSHeapUsedSize"] / 1e6, 1); r["errs"] = errs; r["tag"] = tag
    r["load"] = round(os.getloadavg()[0], 2)
    await ctx.close(); await b.close(); return r
async def main():
    from playwright.async_api import async_playwright
    serve(A.live, 53301); serve(A.br, 53302); out = []
    async with async_playwright() as p:
        for i in range(A.runs):
            for tag, port in (("live", 53301), ("branch", 53302)):
                while os.getloadavg()[0] > 6: print("load", os.getloadavg()[0], "waiting", flush=True); await asyncio.sleep(20)
                r = await one(p, f"http://127.0.0.1:{port}/index.html", tag); r["i"] = i; out.append(r); print(json.dumps(r), flush=True)
                Path(A.out).write_text(json.dumps(out, indent=1))
    for tag in ("live", "branch"):
        R = [x for x in out if x["tag"] == tag]
        print(tag, "fps med", statistics.median(x["fps"] for x in R), "low1 med", statistics.median(x["low1"] for x in R), "p95 med", statistics.median(x["p95"] for x in R), "cpu med", statistics.median(x["cpu_busy_pct"] for x in R), "heap", [x["heap_mb"] for x in R], flush=True)
asyncio.run(main())
