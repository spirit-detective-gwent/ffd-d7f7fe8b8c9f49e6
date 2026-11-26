#!/workspace/pwenv/bin/python3
"""Mizuno / Ch1 mini-boss camera checks and 390x844 + 430x932 shots.
usage: test_cam.py [worktree] [port] [--index PATH] [--tag TAG] [--shots] [--perf]
"""
import asyncio, json, sys, functools, http.server, socketserver, threading, re, time
from pathlib import Path

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
FLAGS = set(a for a in sys.argv[1:] if a.startswith("--"))
ROOT = Path(ARGS[0] if len(ARGS) > 0 else "/workspace/mizuno-cam/wt")
PORT = int(ARGS[1] if len(ARGS) > 1 else 52741)
INDEX = None
TAG = "after"
PERF = "--perf" in FLAGS or "--shots" in FLAGS
for a in sys.argv[1:]:
    if a.startswith("--index="):
        INDEX = Path(a.split("=", 1)[1])
    elif a.startswith("--tag="):
        TAG = a.split("=", 1)[1]
if INDEX is None and "--before" in FLAGS:
    INDEX = Path("/workspace/mizuno-cam/index_before.html")
    TAG = "before"
SHOTS = Path("/workspace/mizuno-cam/shots")
SHOTS.mkdir(parents=True, exist_ok=True)

class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def serve():
    index_bytes = (INDEX or (ROOT / "index.html")).read_bytes()
    n = b"root.WORLD_API = {"
    index_bytes = index_bytes.replace(n, b"root.__ev=function(s){return eval(s)};" + n, 1)
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
        def do_GET(self):
            path = self.path.split("?", 1)[0]
            if path in ("/", "/index.html"):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(index_bytes)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(index_bytes)
                return
            return super().do_GET()
    h = TS(("127.0.0.1", PORT), functools.partial(Q, directory=str(ROOT)))
    threading.Thread(target=h.serve_forever, daemon=True).start()
    return h

HUSH = """(function(){try{if(typeof phClose==='function')phClose()}catch(e){}try{if(typeof autoSet==='function')autoSet(false)}catch(eA){}try{clearTimeout(W.autoT)}catch(eT){}W.autoTok=(W.autoTok|0)+1;try{close()}catch(e2){}W.scGen=(W.scGen|0)+1;W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];try{while((W.scr|0)>0)sLock(0)}catch(e5){}var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML='';d.style.opacity='';d.style.transform=''}try{if(typeof commentHide==='function')commentHide()}catch(e3){}var w=document.getElementById('wintro');if(w)w.remove();try{if(typeof FFF_SCAM!=='undefined'&&FFF_SCAM.clear)FFF_SCAM.clear()}catch(e7){}W.pan=null;W.scrCam=null;W.libCamHold=0;W.bossCamHold=0;W._bossCamOff=0;return 1})()"""

READ = """(function(){
  var d=document.getElementById('wdlg');
  var intro=document.getElementById('wintro');
  var q=d&&d.querySelector('.q, .d2-q, .tw, .body, p');
  var snm=d&&d.querySelector('.snm, .d2-nm, b.snm');
  var line=(q&&(q.innerText||q.textContent)||(d&&d.innerText)||'').replace(/\\s+/g,' ').trim();
  function box(s){
    if(!s||!s.el) return null;
    var b=s.el.getBoundingClientRect(), vw=innerWidth, vh=innerHeight;
    return {x:+b.x.toFixed(1), y:+b.y.toFixed(1), w:+b.width.toFixed(1), h:+b.height.toFixed(1),
      cx:+(b.x+b.width/2).toFixed(1), cy:+(b.y+b.height/2).toFixed(1),
      left:+b.left.toFixed(1), right:+b.right.toFixed(1),
      vis: b.width>2 && b.right>8 && b.left<vw-8 && b.bottom>8 && b.top<vh-8};
  }
  var mz=W.libN&&W.libN.mizuno, r=W.ryo, a=W.aoi;
  var scam= (typeof FFF_SCAM!=='undefined' && FFF_SCAM && FFF_SCAM.st) ? {on:!!FFF_SCAM.st.on,ease:!!FFF_SCAM.st.ease,boss:!!FFF_SCAM.st.boss,bridge:!!FFF_SCAM.st.bridge,z:(function(){try{var v=document.getElementById('wv');var cs=getComputedStyle(v);return parseFloat(cs.scale)||1;}catch(e){return 1;}})()} : null;
  return {
    dlg:!!(d&&(d.classList.contains('on')||d.offsetParent)),
    intro:!!intro,
    name:(snm&&snm.textContent)||'',
    line:line,
    vw:innerWidth, vh:innerHeight,
    mz:box(mz), ryo:box(r), aoi:box(a),
    ryoPos: r? [Math.round(r.x), Math.round(r.y)] : null,
    mzPos: mz? [Math.round(mz.x), Math.round(mz.y)] : null,
    S: W.S, hold:!!(W.bossCamHold||W.libCamHold), mode:W.bossCamMode||null,
    room: (typeof libRoom==='function'&&libRoom())|| (W.inside&&W.inside.id)||'',
    scam: scam
  };
})()"""

RES = []
def ok(name, cond, extra=""):
    RES.append((bool(cond), name, extra))
    print(("PASS " if cond else "FAIL ") + name + ((" :: " + str(extra)[:400]) if extra and not cond else ""), flush=True)

async def ev(pg, code):
    return await pg.evaluate(
        "(c)=>{try{var r=__ev(c);return (r===undefined)?null:JSON.parse(JSON.stringify(r))}catch(e){return {__err:String(e&&e.message||e)}}}",
        code,
    )

async def skipall(pg, n=12):
    SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(200)
            c = await pg.evaluate(SK)
            if not c:
                break
        await pg.touchscreen.tap(*c)
        await pg.wait_for_timeout(200)
    await pg.evaluate("(()=>{var b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Close'&&e.offsetParent);if(b)b.click()})()")

async def shot(pg, name):
    path = SHOTS / f"{TAG}_{name}.png"
    await pg.screenshot(path=str(path), type="png")
    print(f"SHOT {path}", flush=True)
    return path

async def st(pg):
    s = await ev(pg, READ)
    if isinstance(s, dict) and s.get("line"):
        s["line"] = s["line"].replace("\u2060", "").replace("⁠", "")
    return s

async def next_line(pg, times=1):
    for _ in range(times):
        await ev(pg, """(function(){
          var d=document.getElementById('wdlg');
          var b=d&&d.querySelector('.bt button, button.hot, .d2-list button, .next, .ok');
          if(b){ b.click(); return 1; }
          if(d){ try{ d.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,cancelable:true})); }catch(e){ d.click(); } }
          return 1;
        })()""")
        await pg.wait_for_timeout(200)
    return await st(pg)

async def skip_intro_card(pg):
    for i in range(40):
        s = await ev(pg, """(function(){
          var e=document.getElementById('wintro');
          if(!e) return 0;
          var b=e.querySelector('.iskip');
          if(b){ b.click(); return 2; }
          try{ e.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,cancelable:true})); }catch(err){ e.click(); }
          return 1;
        })()""")
        if s == 0:
            await pg.wait_for_timeout(350)
            break
        await pg.wait_for_timeout(80)
    for i in range(20):
        s = await st(pg)
        if not s.get("intro"):
            return s
        await pg.wait_for_timeout(80)
    return await st(pg)

async def boot(p, w=390, h=844):
    from playwright.async_api import async_playwright
    b = await p.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
    ctx = await b.new_context(
        viewport={"width": w, "height": h},
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
    await pg.touchscreen.tap(w // 2, h // 2)
    await pg.wait_for_timeout(200)
    await ev(pg, "(function(){try{root.FFF_CRAWL_MS=1;ST.set.cam='on';ST.set.tips=false;if(ST.set.txt!=null)ST.set.txt='fast';ST.set.rm=false;}catch(e){}return 1})()")
    await pg.evaluate("WORLD_API.enter(true)")
    await pg.wait_for_timeout(2000)
    await skipall(pg, 14)
    await ev(pg, HUSH)
    return b, ctx, pg, errs

async def setup_archive(pg, path="balanced", ngp=False):
    code = f"""(function(){{
      SAVE.intro=1; SAVE.ch1=0; SAVE.chapter=1; SAVE.gouki=0;
      SAVE.ngp={1 if ngp else 0};
      SAVE.sc={{}}; SAVE.mb=SAVE.mb||{{}}; delete SAVE.mb.mb_lib;
      SAVE.bond=SAVE.bond||{{}}; SAVE.bond.path='{path}'; SAVE.bond.lock='{path}';
      SAVE.icard={{ryo:1,aoi:1}};
      SAVE.bent={{}}; /* first-visit arrival */
      var L=dgS('lib');
      L.e={{foyer:1,hall:1,stacks:1,carrels:1,ante:1}}; /* archive not yet visited */
      L.unp={{s_pony:1,s_mio:1,s_boy:1}};
      L.akey=1; L.okey=1;
      try{{ ST.set.cam='on'; ST.set.rm=false; ST.set.txt='fast'; }}catch(e){{}}
      try{{ delete root.FFF_SKIP_INTRO; root.FFF_SCAM_OFF=false; }}catch(e2){{}}
      libGo('archive');
      return {{room:libRoom(), mz:!!(W.libN&&W.libN.mizuno), ryo:W.ryo&&[Math.round(W.ryo.x),Math.round(W.ryo.y)], path:SAVE.bond.path, ngp:SAVE.ngp|0}};
    }})()"""
    return await ev(pg, code)

async def wait_pred(pg, pred, timeout=20000, settle=0):
    t0 = time.time()
    s = None
    while (time.time() - t0) * 1000 < timeout:
        s = await st(pg)
        if s and pred(s):
            if settle:
                await pg.wait_for_timeout(settle)
                s = await st(pg)
            return s
        if s and s.get("intro"):
            s = await skip_intro_card(pg)
            continue
        await pg.wait_for_timeout(120)
    return s or await st(pg)

def has(s, *needles):
    line = (s.get("line") or "")
    return all(n.lower() in line.lower() for n in needles)

def mizuno_ok(s, vw=390, label=""):
    """Mizuno should be horizontally centered-ish and fully (or almost) in frame, not clipped at x=0-35."""
    mz = s.get("mz") or {}
    if not mz:
        return False, "no mizuno box"
    cx, left, right, w = mz.get("cx", 0), mz.get("left", 0), mz.get("right", 0), mz.get("w", 0)
    # centre within 28%-72% of viewport; left edge not hard-clipped (allow 8px), most of the body visible
    mid = 0.28 * vw <= cx <= 0.72 * vw
    not_edge = left >= -12 or (w > 0 and (min(right, vw) - max(left, 0)) > 0.7 * w)
    vis = mz.get("vis")
    return bool(mid and not_edge and vis), {"cx": cx, "left": left, "right": right, "w": w, "vw": vw, "vis": vis, "label": label}

async def run_mizuno(pg, path="balanced", ngp=False, do_shots=False, vw=390, vh=844, perf=False):
    tag = f"{path}{'_ngp' if ngp else ''}_{vw}x{vh}"
    await ev(pg, HUSH)
    await pg.wait_for_timeout(200)
    info = await setup_archive(pg, path, ngp=ngp)
    ok(f"{tag} entered archive with Mizuno", info and not info.get("__err") and info.get("mz") and info.get("room") == "archive", info)
    # wait for walk-in + reveal + first dialogue (or intro card)
    s = await wait_pred(pg, lambda x: x.get("intro") or x.get("dlg"), timeout=18000)
    if s and s.get("intro"):
        if do_shots:
            await shot(pg, f"{tag}_intro")
        s = await skip_intro_card(pg)
    # step to the "Nobody listened" line (the zoomed dialogue Erik screenshotted)
    s = await wait_pred(pg, lambda x: x.get("dlg"), timeout=8000)
    for i in range(14):
        if has(s, "Nobody listened") or has(s, "Isn't it nice") or has(s, "Isn’t it nice"):
            break
        s = await next_line(pg)
        if s.get("intro"):
            s = await skip_intro_card(pg)
        await pg.wait_for_timeout(80)
    nobody = has(s, "Nobody listened") or has(s, "nice")
    ok(f"{tag} reached Nobody listened (or nearby Mizuno line)", nobody or ("library" in (s.get("line") or "").lower()) or s.get("name") in ("Mizuno", "Mizuno Sho"), s)
    if do_shots:
        await shot(pg, f"{tag}_nobody")
    good, detail = mizuno_ok(s, vw, "nobody")
    ok(f"{tag} Mizuno centred in frame at Nobody listened", good, detail if not good else s.get("mz"))
    # He should not be a sliver at the left edge
    mz = s.get("mz") or {}
    ok(f"{tag} Mizuno not clipped as a left-edge sliver",
       not (mz and mz.get("right") is not None and mz.get("right") < vw * 0.25 and mz.get("left", 0) < 20),
       mz)

    if perf:
        # 5s idle on the held reveal
        await ev(pg, "()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);}()")
        cdp = await pg.context.new_cdp_session(pg)
        await cdp.send("Performance.enable")
        m0 = await cdp.send("Performance.getMetrics")
        await pg.wait_for_timeout(5000)
        m1 = await cdp.send("Performance.getMetrics")
        await ev(pg, "window.__run=false")
        ft = await pg.evaluate("window.__ft") or []
        def met(ms):
            return {x["name"]: x["value"] for x in ms["metrics"]}
        a, b = met(m0), met(m1)
        wall = b["Timestamp"] - a["Timestamp"]
        tot = sum(ft[2:]) or 1
        fps = round(1000 * max(1, len(ft) - 2) / tot, 1)
        heat = round(100 * (b["TaskDuration"] - a["TaskDuration"]) / wall, 1) if wall else 0
        heap = round(b["JSHeapUsedSize"] / 1e6, 1)
        print(f"PERF {tag} fps={fps} heat={heat} frames={len(ft)} heap={heap}MB", flush=True)
        ok(f"{tag} reveal stays at 50+ fps", fps >= 50, {"fps": fps, "heat": heat})
        await cdp.detach()

    # Advance to the chal line / fight-ask ("library archive is closed" / "Overdue fines")
    for i in range(16):
        line = s.get("line") or ""
        if "archive is closed" in line.lower() or "Overdue fines" in line or "paid in pain" in line.lower() or "never returned a book" in line.lower():
            break
        # maybe the Fight / Walk away prompt already
        ask = await ev(pg, """(function(){var bs=[...document.querySelectorAll('button')].map(b=>b.textContent.trim());return {fight:bs.indexOf('Fight')>=0, away:bs.some(t=>/Walk away/.test(t)), bs:bs.slice(0,8)};})()""")
        if isinstance(ask, dict) and ask.get("fight"):
            break
        s = await next_line(pg)
        if s.get("intro"):
            s = await skip_intro_card(pg)
        await pg.wait_for_timeout(80)
    s = await st(pg)
    if do_shots:
        await shot(pg, f"{tag}_chal")
    good2, detail2 = mizuno_ok(s, vw, "chal")
    # At chal / fines, camera must not have snapped back to the door: Mizuno still in frame, not a left sliver
    mz2 = s.get("mz") or {}
    snapped = mz2 and mz2.get("right") is not None and mz2.get("right") < vw * 0.22 and (s.get("ryo") or {}).get("cx", 0) > vw * 0.55
    ok(f"{tag} no snap back to the door at chal/fines", not snapped and (mz2.get("vis") if mz2 else False),
       {"mz": mz2, "ryo": s.get("ryo"), "aoi": s.get("aoi"), "line": (s.get("line") or "")[:160]})
    # Prefer still reasonably centred; if a two-shot, cx can sit a bit off-centre — still must be on screen
    ok(f"{tag} Mizuno still on screen at chal/fines",
       bool(mz2 and mz2.get("vis") and mz2.get("right", 0) - max(mz2.get("left", 0), 0) > 40),
       detail2 if not good2 else mz2)

    # If Fight is up, press it and capture the run-up (all three in frame)
    ask = await ev(pg, """(function(){var b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Fight'&&e.offsetParent);if(!b)return 0;b.click();return 1;})()""")
    ran = False
    if ask:
        # poll during run-up
        t0 = time.time()
        mid = None
        while time.time() - t0 < 6:
            ru = await ev(pg, "(function(){return {ru:!!W.runUp, mode:W.bossCamMode||null, hold:!!(W.bossCamHold||W.libCamHold)};})()")
            cur = await st(pg)
            if ru and ru.get("ru"):
                mid = cur
                if do_shots and not ran:
                    await shot(pg, f"{tag}_runup")
                    ran = True
                # all three visible?
                vis3 = sum(1 for k in ("mz", "ryo", "aoi") if (cur.get(k) or {}).get("vis"))
                if vis3 >= 2:
                    break
            # swirl / fight started
            if await ev(pg, "(function(){return !!(document.getElementById('wswirl')||(root.FFF&&FFF.b));})()"):
                break
            await pg.wait_for_timeout(80)
        if mid is None:
            mid = await st(pg)
        if do_shots and not ran:
            await shot(pg, f"{tag}_runup")
        vis3 = sum(1 for k in ("mz", "ryo", "aoi") if (mid.get(k) or {}).get("vis"))
        ok(f"{tag} run-up keeps Mizuno in frame", bool((mid.get("mz") or {}).get("vis")), mid)
        # After the walk-in they start close, so 2-3 visible is the goal
        ok(f"{tag} run-up shows at least two of the trio", vis3 >= 2, {"vis3": vis3, "mz": mid.get("mz"), "ryo": mid.get("ryo"), "aoi": mid.get("aoi")})
    return s

def static_checks():
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    # only meaningful on the patched tree
    if "BENT_EASE" not in src:
        print("STATIC skipped (before / unpatched index)", flush=True)
        return
    ok("BENT_EASE covers the four Ch1 minis", all(k in src for k in ("mb_lib: 1", "mb_art: 1", "mb_cafe: 1", "mb_field: 1")))
    ok("libBoss walks Ryo and Aoi in before bossEnt", "libBossApproach" in src and "bossEnt('mb_lib'" in src)
    ok("end() holds the frame while bridged", "S.ease && S.bridge" in src)
    ok("no instant CSS cut when S.ease", "if (S.boss && !S.ease)" in src)
    ok("cutPush eases from the current frame for Ch1 minis", "Ch1 minis ease from the current frame" in src)
    ok("cafe/field/art hold the camera through miniDialog", src.count("W.bossCamHold = 1") >= 4)
    ok("run-up widens, then a clash push-in", "runUpClash" in src and "W.bossCamMode = 'wide'" in src)
    ok("swirl releases the hold (no snap at fight())", "W._bossCamUntilSwirl" in src and "libBossCamOff(true)" in src)
    # other Ch1 minis share bossEnt
    ok("Mai, Kurata and Bando still go through bossEnt",
       "bossEnt('mb_art'" in src and "bossEnt('mb_cafe'" in src and "bossEnt('mb_field'" in src)

async def main():
    from playwright.async_api import async_playwright
    static_checks()
    serve()
    print(f"Serving {ROOT} index={INDEX or ROOT/'index.html'} tag={TAG} port={PORT}", flush=True)
    do_shots = "--shots" in FLAGS or "--before" in FLAGS or TAG in ("before", "after")
    # default to shots on
    do_shots = True
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p, 390, 844)
        ok("boot clean", not errs, errs)
        # Compassionate (balanced) with shots + perf, then other paths / NG+ without extra shots
        await run_mizuno(pg, "balanced", ngp=False, do_shots=do_shots, vw=390, vh=844, perf=("--perf" in FLAGS or TAG == "after"))
        if TAG != "before":
            await run_mizuno(pg, "fierce", ngp=False, do_shots=False, vw=390, vh=844)
            await run_mizuno(pg, "strategic", ngp=False, do_shots=False, vw=390, vh=844)
            await run_mizuno(pg, "balanced", ngp=True, do_shots=False, vw=390, vh=844)
        await ctx.close(); await b.close()
        # taller iPhone
        b, ctx, pg, errs = await boot(p, 430, 932)
        ok("boot 430x932 clean", not errs, errs)
        await run_mizuno(pg, "balanced", ngp=False, do_shots=do_shots, vw=430, vh=932, perf=False)
        await ctx.close(); await b.close()
    passed = sum(1 for r in RES if r[0])
    failed = sum(1 for r in RES if not r[0])
    print(f"\nRESULT {passed} passed, {failed} failed, tag={TAG}", flush=True)
    (SHOTS / f"{TAG}_results.json").write_text(json.dumps(
        [{"ok": a, "name": b, "extra": str(c)[:400]} for a, b, c in RES], indent=2))
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    asyncio.run(main())
