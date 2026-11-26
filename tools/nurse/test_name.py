#!/workspace/pwenv/bin/python3
"""Nurse name-reveal + painted-portrait checks and 390x844 preview shots.
usage: test_name.py [worktree] [port]
"""
import asyncio, json, sys, functools, http.server, socketserver, threading, re
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/workspace/nurse-name/wt")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 52731
SHOTS = Path("/workspace/nurse-name/shots")
SHOTS.mkdir(parents=True, exist_ok=True)

class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def serve():
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
        def do_GET(self):
            if self.path.split("?", 1)[0] in ("/", "/index.html"):
                raw = (ROOT / "index.html").read_bytes()
                n = b"root.WORLD_API = {"
                raw = raw.replace(n, b"root.__ev=function(s){return eval(s)};" + n, 1)
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(raw)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(raw)
                return
            return super().do_GET()
    h = TS(("127.0.0.1", PORT), functools.partial(Q, directory=str(ROOT)))
    threading.Thread(target=h.serve_forever, daemon=True).start()
    return h

SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
HUSH = """(function(){try{if(typeof phClose==='function')phClose()}catch(e){}try{close()}catch(e2){}W.scGen=(W.scGen|0)+1;W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];try{while((W.scr|0)>0)sLock(0)}catch(e5){}var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''}try{if(typeof commentHide==='function')commentHide()}catch(e3){}var w=document.getElementById('wintro');if(w)w.remove();try{if(typeof FFF_SCAM!=='undefined'&&FFF_SCAM.clear)FFF_SCAM.clear()}catch(e7){}return 1})()"""
READ = """(function(){
  var d=document.getElementById('wdlg');
  var intro=document.getElementById('wintro');
  var snm=d&&d.querySelector('.snm, .d2-nm, b.snm');
  var q=d&&d.querySelector('.q, .d2-q, .tw');
  var pts=[...((d&&d.querySelectorAll('.pt2, .pt, .d2-face'))||[])];
  var bgs=pts.map(function(p){return p.style.backgroundImage||''});
  var bg=bgs.join(' | ');
  return {
    dlg:!!(d&&d.classList.contains('on')),
    intro:!!intro,
    introName: intro && (intro.querySelector('.nm')||{}).textContent || '',
    introSub: intro && (intro.querySelector('.sub')||{}).textContent || '',
    name: (snm&&snm.textContent)||'',
    line: (q&&(q.innerText||q.textContent)||'').replace(/\\s+/g,' ').trim(),
    ln: d && d.dataset.ln || '',
    pt: bg.slice(0,160),
    painted: /portraits\\/nurse_/.test(bg),
    oldfig: /nurse_fig|data:image\\/webp/.test(bg) && !/portraits\\/nurse_/.test(bg),
    label: (typeof nurseLabel==='function')?nurseLabel():(NM&&NM.nurse),
    known: (typeof nurseKnown==='function')?nurseKnown():null,
    scNurse: !!(SAVE.sc&&SAVE.sc.nurse),
    scName: !!(SAVE.sc&&SAVE.sc.nurseName),
    icard: !!(SAVE.icard&&SAVE.icard.nurse)
  };
})()"""

RES = []
def ok(name, cond, extra=""):
    RES.append((bool(cond), name, extra))
    print(("PASS " if cond else "FAIL ") + name + ((" :: " + str(extra)[:300]) if extra and not cond else ""), flush=True)

async def ev(pg, code):
    return await pg.evaluate(
        "(c)=>{try{var r=__ev(c);return (r===undefined)?null:JSON.parse(JSON.stringify(r))}catch(e){return {__err:String(e&&e.message||e)}}}",
        code,
    )

async def skipall(pg, n=12):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(250)
            c = await pg.evaluate(SK)
            if not c:
                break
        await pg.touchscreen.tap(*c)
        await pg.wait_for_timeout(250)
    await pg.evaluate("(()=>{var b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Close'&&e.offsetParent);if(b)b.click()})()")

async def shot(pg, name):
    path = SHOTS / f"{name}.png"
    await pg.screenshot(path=str(path), type="png")
    print(f"SHOT {path}", flush=True)
    return path

async def st(pg):
    return await ev(pg, READ)

async def next_line(pg, times=1):
    for _ in range(times):
        # finish typewriter if busy, then advance
        busy = await ev(pg, "(function(){var b=document.querySelector('#wdlg .bt button, #wdlg button.hot'); if(!b)return 'none'; b.click(); return 'click'})()")
        await pg.wait_for_timeout(80)
        await ev(pg, "(function(){var b=document.querySelector('#wdlg .bt button, #wdlg button.hot'); if(b)b.click(); return 1})()")
        await pg.wait_for_timeout(120)
    return await st(pg)

async def skip_intro_card(pg):
    for i in range(20):
        s = await ev(pg, "(function(){var e=document.getElementById('wintro'); if(!e)return 0; var b=e.querySelector('.iskip'); if(b){b.click(); return 2} return 1})()")
        if s == 0:
            break
        if s == 2:
            await pg.wait_for_timeout(200)
            break
        await pg.wait_for_timeout(80)
    await pg.wait_for_timeout(200)
    return await st(pg)

async def boot(p):
    b = await p.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
    ctx = await b.new_context(
        viewport={"width": 390, "height": 844},
        device_scale_factor=1,
        is_mobile=True,
        has_touch=True,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    )
    pg = await ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:240]))
    await pg.goto(f"http://127.0.0.1:{PORT}/index.html", wait_until="domcontentloaded", timeout=90000)
    await pg.wait_for_timeout(3000)
    await pg.touchscreen.tap(195, 420)
    await pg.wait_for_timeout(200)
    await ev(pg, "(function(){try{root.FFF_CRAWL_MS=1;ST.set.cam='on';ST.set.tips=false;if(ST.set.txt!=null)ST.set.txt='fast'}catch(e){}return 1})()")
    await pg.evaluate("WORLD_API.enter(true)")
    await pg.wait_for_timeout(2000)
    await skipall(pg, 14)
    await ev(pg, HUSH)
    return b, ctx, pg, errs

async def setup_first_meet(pg, path="balanced", ngp=False):
    code = f"""(function(){{
      SAVE.intro=1; SAVE.ch1=0; SAVE.chapter=1; SAVE.gouki=0;
      SAVE.ngp={1 if ngp else 0};
      SAVE.sc={{}}; SAVE.bond=SAVE.bond||{{}}; SAVE.bond.path='{path}'; SAVE.bond.lock='{path}';
      SAVE.icard={{ryo:1,aoi:1{',nurse:1' if ngp else ''}}};
      try{{ root.FFF_NURSE_SKIP=0; delete root.FFF_SKIP_INTRO; }}catch(e){{}}
      if (typeof nurseSyncName==='function') nurseSyncName();
      // instant cinematics so after1 can reach the name line
      if (typeof cine==='function'){{ root._cine0=cine; cine=function(t,d){{ ev('world:cine:'+t); if(d)d(); }}; }}
      return {{label:nurseLabel(), known:nurseKnown(), path:SAVE.bond.path, ngp:SAVE.ngp|0, icard:!!(SAVE.icard&&SAVE.icard.nurse)}};
    }})()"""
    return await ev(pg, code)

async def open_post(pg):
    return await ev(pg, """(function(){
      try{ roomOpen({post:1}); }catch(e){ return {__err:String(e&&e.message||e)}; }
      return 1;
    })()""")

async def wait_dlg(pg, timeout=8000):
    t0 = asyncio.get_event_loop().time()
    while (asyncio.get_event_loop().time() - t0) * 1000 < timeout:
        s = await st(pg)
        if s and (s.get("dlg") or s.get("intro")):
            return s
        await pg.wait_for_timeout(80)
    return await st(pg)

async def step_until(pg, pred, cap=40, shots=None):
    s = await st(pg)
    for i in range(cap):
        if s.get("intro"):
            if shots:
                await shot(pg, shots)
            return s
        if pred(s):
            return s
        s = await next_line(pg)
    return s

def static_checks():
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    ok("after1 hooks nurseReveal after the name line",
       "['nurse', 'Shiraishi. School nurse. Thank you. Both of you.', { mood: 'happy' }],\n    ['@fn', function (next) { nurseReveal(next); }]" in src)
    ok("mode.post no longer plays charIntro before nurse2",
       "intro card waits until she says her name in nurse2" in src and
       "charIntro('nurse', function () { scene('nurse2'" not in src)
    ok("nurseReveal / nurseLabel helpers present",
       "function nurseReveal(done)" in src and "function nurseLabel()" in src)
    ok("n9Cabinet uses ptFace painted bust", "ptFace('nurse', 'White cabinet')" in src)
    ok("dress tutorial offer uses ptFace", "You keep coming back scraped" in src and "ptFace('nurse', nurseLabel())" in src)
    # leftover third-arg nurse_fig is only the chalk board, which goes through dlgPtUrl
    leftover = re.findall(r"dialog\([^;]{0,500}'nurse_fig'", src)
    ok("no unscoped dialog(..., 'nurse_fig') besides board (dlgPtUrl)",
       len(leftover) <= 1, leftover)


async def run_path(pg, path, ngp=False, do_shots=False):
    tag = f"{path}{'_ngp' if ngp else ''}"
    await ev(pg, HUSH)
    info = await setup_first_meet(pg, path, ngp=ngp)
    ok(f"{tag} starts unnamed", info and info.get("label") == "Nurse" and not info.get("known"), info)
    await open_post(pg)
    s = await wait_dlg(pg)
    # first spoken nurse line in after1
    s = await step_until(pg, lambda x: x.get("name") in ("Nurse", "Shiraishi-sensei") or "eyes" in (x.get("line") or "").lower())
    if "eyes" not in (s.get("line") or "").lower() and s.get("name") != "Nurse":
        # maybe still on a narrator / cine leftover; keep stepping
        s = await step_until(pg, lambda x: "eyes" in (x.get("line") or "").lower() or "never seen" in (x.get("line") or "").lower())
    ok(f"{tag} pre-name speaker is Nurse", s.get("name") == "Nurse" and s.get("label") == "Nurse", s)
    if do_shots:
        await shot(pg, "01_nurse_label_before")
    # advance to the name-saying line
    s = await step_until(pg, lambda x: "Shiraishi. School nurse" in (x.get("line") or "") or x.get("intro"))
    if s.get("intro"):
        ok(f"{tag} card must not appear before the name line", False, s)
        await skip_intro_card(pg)
        return
    ok(f"{tag} name line still labelled Nurse",
       s.get("name") == "Nurse" and "Shiraishi. School nurse" in (s.get("line") or ""), s)
    if do_shots:
        await shot(pg, "02_name_line_still_nurse")
    # next should be the intro card
    s = await next_line(pg)
    # typewriter-finish may have only completed text; ensure we advanced
    if not s.get("intro"):
        await pg.wait_for_timeout(200)
        s = await st(pg)
        if not s.get("intro"):
            s = await next_line(pg)
    ok(f"{tag} reveal card plays after the name line",
       s.get("intro") and "Shiraishi" in (s.get("introName") or ""), s)
    if do_shots:
        await shot(pg, "03_reveal_card")
    s = await skip_intro_card(pg)
    # next talk: Aoi, then later nurse should be named. Step until a nurse line.
    s = await step_until(pg, lambda x: x.get("name") in ("Shiraishi-sensei", "Nurse") and "Hayase" not in (x.get("line") or "") and x.get("name") != "Aoi Hayase" and "Aoi" not in (x.get("name") or ""))
    # more reliably: look at label() and a later nurse speaker
    found = None
    cur = s
    for i in range(16):
        if cur.get("name") == "Shiraishi-sensei":
            found = cur
            break
        if cur.get("name") == "Nurse":
            found = cur
            break
        cur = await next_line(pg)
    ok(f"{tag} later lines use Shiraishi-sensei",
       (found and found.get("name") == "Shiraishi-sensei" and found.get("label") == "Shiraishi-sensei"), found or cur)
    if do_shots and found:
        await shot(pg, "04_named_label_after")
    ok(f"{tag} nurseName flag set, icard marked",
       cur.get("scName") or (found and found.get("scName")), found or cur)

async def portraits(pg, errs):
    await ev(pg, HUSH)
    # known, so labels are Shiraishi-sensei
    await ev(pg, """(function(){
      SAVE.intro=1; SAVE.sc=SAVE.sc||{}; SAVE.sc.nurse=1; SAVE.sc.nurseName=1; SAVE.craft=SAVE.craft||{}; delete SAVE.craft.dress;
      SAVE.cabT=0; if(typeof nurseSyncName==='function') nurseSyncName();
      return nurseLabel();
    })()""")
    # --- before: hide painted bust so the old fig shows ---
    await ev(pg, """(function(){
      window._ptNurse = PT_HAS.nurse_neutral; PT_HAS.nurse_neutral=0;
      return 1;
    })()""")
    await ev(pg, "(function(){ try{ v630DressTalk(); }catch(e){ return String(e&&e.message||e);} return 1; })()")
    await pg.wait_for_timeout(250)
    s = await st(pg)
    await shot(pg, "05_bandage_tutorial_before")
    ok("bandage before uses old fig (forced)", s.get("oldfig") or not s.get("painted"), s)
    await ev(pg, HUSH)
    await ev(pg, "(function(){ try{ n9Cabinet(); }catch(e){ return String(e&&e.message||e);} return 1; })()")
    await pg.wait_for_timeout(250)
    await shot(pg, "07_cabinet_pickup_before")
    # --- after: restore painted ---
    await ev(pg, "PT_HAS.nurse_neutral = window._ptNurse || 1")
    await ev(pg, HUSH)
    await ev(pg, "(function(){ try{ v630DressTalk(); }catch(e){ return String(e&&e.message||e);} return 1; })()")
    await pg.wait_for_timeout(300)
    s = await st(pg)
    await shot(pg, "06_bandage_tutorial_after")
    ok("bandage tutorial uses painted nurse portrait", s.get("painted"), s)
    await ev(pg, HUSH)
    await ev(pg, "(function(){ try{ n9Cabinet(); }catch(e){ return String(e&&e.message||e);} return 1; })()")
    await pg.wait_for_timeout(300)
    s = await st(pg)
    await shot(pg, "08_cabinet_pickup_after")
    ok("cabinet pickup uses painted nurse portrait", s.get("painted"), s)
    # enter1 speaker during the hold-up, still unnamed
    await ev(pg, HUSH)
    await ev(pg, """(function(){
      SAVE.sc={}; SAVE.icard={ryo:1,aoi:1}; if(typeof nurseSyncName==='function') nurseSyncName();
      if (typeof cine==='function'){ cine=function(t,d){ if(d)d(); }; }
      try{ scene('nurse1'); }catch(e){ return String(e&&e.message||e); }
      return 1;
    })()""")
    s = await wait_dlg(pg)
    s = await step_until(pg, lambda x: x.get("name") == "Nurse" or "nothing in there" in (x.get("line") or ""))
    ok("enter1 (before the fight) also labels her Nurse", s.get("name") == "Nurse", s)
    if s.get("name") == "Nurse":
        await shot(pg, "00_enter1_nurse_label")

async def office_perf(pg):
    # stand in the office after first visit, idle sample
    await ev(pg, HUSH)
    await ev(pg, """(function(){
      SAVE.intro=1; SAVE.sc=SAVE.sc||{}; SAVE.sc.nurse=1; SAVE.sc.nurseName=1;
      if(typeof nurseSyncName==='function') nurseSyncName();
      try{ roomOpen({restore:1}); }catch(e){ return String(e&&e.message||e); }
      W.dlg=false; W.cut=false;
      return 1;
    })()""")
    await pg.wait_for_timeout(800)
    await ev(pg, HUSH)
    # fps sampler
    await pg.evaluate("""()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);}""")
    cdp = await pg.context.new_cdp_session(pg)
    await cdp.send("Performance.enable")
    m0 = await cdp.send("Performance.getMetrics")
    m0 = {x["name"]: x["value"] for x in m0["metrics"]}
    await pg.wait_for_timeout(5000)
    m1 = await cdp.send("Performance.getMetrics")
    m1 = {x["name"]: x["value"] for x in m1["metrics"]}
    await pg.evaluate("window.__run=false")
    ft = await pg.evaluate("window.__ft")
    ft = [x for x in (ft or [])[2:]]
    tot = sum(ft) if ft else 1
    fps = round(1000 * len(ft) / tot, 1) if ft else 0
    wall = m1.get("Timestamp", 0) - m0.get("Timestamp", 0) or 1
    heat = round(100 * (m1.get("TaskDuration", 0) - m0.get("TaskDuration", 0)) / wall, 1)
    out = dict(fps=fps, heat=heat, frames=len(ft), heap_mb=round(m1.get("JSHeapUsedSize", 0) / 1e6, 1))
    (SHOTS / "perf_office.json").write_text(json.dumps(out, indent=2))
    print("PERF nurse office", out, flush=True)
    ok("office idle fps is a number", isinstance(fps, (int, float)) and fps > 0, out)
    return out

async def main():
    static_checks()
    h = serve()
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p)
        ok("boot had no page errors", not errs, errs[:3])
        # Compassionate (balanced) with shots, then the other two paths, then NG+
        await run_path(pg, "balanced", ngp=False, do_shots=True)
        await run_path(pg, "fierce", ngp=False, do_shots=False)
        await run_path(pg, "strategic", ngp=False, do_shots=False)
        await run_path(pg, "balanced", ngp=True, do_shots=False)
        await portraits(pg, errs)
        await office_perf(pg)
        ok("no page errors after nurse scenes", not errs, errs[:4])
        await b.close()
    h.shutdown()
    failed = [n for c, n, e in RES if not c]
    print(("FAIL: " + ", ".join(failed)) if failed else "PASS: nurse name + portraits")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    asyncio.run(main())
