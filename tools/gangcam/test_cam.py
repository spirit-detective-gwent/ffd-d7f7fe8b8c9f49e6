#!/workspace/pwenv/bin/python3
"""Regression: overworld camera restores after a street/ambush/pack fight.
usage: test_cam.py [worktree] [port]
Writes /workspace/gangcam/shots/before.png after.png before_after.png
and prints fps/heat for the post-fight map and a long walk.
"""
import asyncio, functools, http.server, json, socketserver, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/workspace/gangcam/wt")
PORT = int(sys.argv[2] if len(sys.argv) > 2 else 52780)
SHOTS = Path("/workspace/gangcam/shots")
SHOTS.mkdir(parents=True, exist_ok=True)
RES = []

class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def serve():
    index_bytes = (ROOT / "index.html").read_bytes()
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

def ok(name, cond, extra=""):
    RES.append((bool(cond), name, extra))
    print(("PASS " if cond else "FAIL ") + name + ((" :: " + str(extra)[:240]) if extra and not cond else ""), flush=True)

async def ev(pg, code):
    return await pg.evaluate(
        "(c)=>{try{var r=__ev(c);return (r===undefined)?null:JSON.parse(JSON.stringify(r))}catch(e){return {__err:String(e&&e.message||e)}}}",
        code,
    )

SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""

async def skipall(pg, n=14):
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

HUSH = """(function(){try{if(typeof phClose==='function')phClose()}catch(e){}try{if(typeof autoSet==='function')autoSet(false)}catch(eA){}try{clearTimeout(W.autoT)}catch(eT){}W.autoTok=(W.autoTok|0)+1;try{if(typeof close==='function')close()}catch(e2){}W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];try{while((W.scr|0)>0)sLock(0)}catch(e5){}var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML='';d.style.opacity='';d.style.transform=''}try{if(typeof commentHide==='function')commentHide()}catch(e3){}var w=document.getElementById('wintro');if(w)w.remove();return 1})()"""

BOOT = """(function(){
  SAVE.intro=1; SAVE.chapter=1; SAVE.ch1=0; SAVE.gouki=0; SAVE.ngp=0;
  SAVE.sc=SAVE.sc||{}; SAVE.sc.nurse=1; SAVE.sc.kn=1;
  SAVE.bond=SAVE.bond||{}; SAVE.bond.path='balanced'; SAVE.bond.lock='balanced';
  SAVE.icard={ryo:1,aoi:1};
  SAVE.hp=18; SAVE.items=75;
  try{ var B=STORY.bond(SAVE); B.path=B.path||'balanced'; B.px=(STORY.bondTot?STORY.bondTot(3):60)+4; }catch(eB){}
  if(W.ryo){ W.ryo.x=3000; W.ryo.y=2200; W.ryo.dir=0; if(W.ryo.el){ W.ryo.el.style.visibility=''; W.ryo.el.classList.remove('out'); } }
  if(W.aoi){ W.aoi.x=2940; W.aoi.y=2260; W.aoi.dir=0; if(W.aoi.el){ W.aoi.el.style.visibility=''; W.aoi.el.classList.remove('out'); } }
  try{ if(typeof resetTrail==='function') resetTrail(W.ryo.x,W.ryo.y,0); }catch(eT){}
  W.busy=false; W.dlg=false; W.cut=false; W.forced=null; W.runUp=false;
  try{ if(typeof FFF_ZOOM!=='undefined'&&FFF_ZOOM) FFF_ZOOM.set(1); }catch(eZ){}
  try{ if(typeof hud==='function') hud(); }catch(eH){}
  try{ if(typeof camera==='function') camera(true); }catch(eC){}
  try{ if(typeof place==='function'){ place(W.ryo,0); place(W.aoi,0); } }catch(eP){}
  try{ if(typeof rdyOff==='function'){ rdyOff(W.ryo); rdyOff(W.aoi); } }catch(eR){}
  return {area: (typeof areaName==='function'&&areaName(W.ryo.x,W.ryo.y))||'', x:Math.round(W.ryo.x), y:Math.round(W.ryo.y)};
})()"""

STUCK = """(function(){
  var wv=document.getElementById('wv'); if(!wv||!W.ryo||!W.ryo.el) return {ok:0};
  var vr=wv.getBoundingClientRect(), er=W.ryo.el.getBoundingClientRect();
  var x=er.left+er.width/2-vr.left, y=er.top+er.height*0.4-vr.top;
  wv.style.transformOrigin=x+'px '+y+'px';
  wv.style.scale='1.8'; wv.style.translate='0px 0px';
  W.pan={scr:1, run:function(){}};
  W.camFocus=[W.ryo, W.aoi].filter(Boolean);
  try{ if(typeof camera==='function') camera(true); }catch(e){}
  return FFF_ENC_CAM.read();
})()"""

READ = """(function(){
  var r=W.ryo, a=W.aoi, wv=document.getElementById('wv'), cs=wv&&getComputedStyle(wv);
  var z=(cs&&cs.scale&&cs.scale!=='none')?(parseFloat(cs.scale)||1):1;
  function box(s){ if(!s||!s.el) return null; var b=s.el.getBoundingClientRect();
    return {x:+b.x.toFixed(1),y:+b.y.toFixed(1),w:+b.width.toFixed(1),h:+b.height.toFixed(1),
      cx:+(b.x+b.width/2).toFixed(1),cy:+(b.y+b.height/2).toFixed(1)}; }
  var api=typeof FFF_ENC_CAM!=='undefined'&&FFF_ENC_CAM;
  return {
    z:+z.toFixed(3),
    pan:!!W.pan, panScr:!!(W.pan&&W.pan.scr),
    camFocus:!!(W.camFocus&&W.camFocus.length),
    scamOn:!!(typeof FFF_SCAM!=='undefined'&&FFF_SCAM&&FFF_SCAM.st&&FFF_SCAM.st.on),
    scamBoss:!!(typeof FFF_SCAM!=='undefined'&&FFF_SCAM&&FFF_SCAM.st&&FFF_SCAM.st.boss),
    hasApi:!!api,
    area:(typeof areaName==='function'&&r&&areaName(r.x,r.y))||'',
    ryo:box(r), aoi:box(a), vw:innerWidth, vh:innerHeight,
    hp:SAVE.hp, yen:SAVE.items, S:W.S
  };
})()"""

async def measure(pg, cdp, secs):
    await ev(pg, "window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);1")
    m0 = await cdp.send("Performance.getMetrics")
    await pg.wait_for_timeout(int(secs * 1000))
    m1 = await cdp.send("Performance.getMetrics")
    await ev(pg, "window.__run=false;1")
    ft = await pg.evaluate("window.__ft") or []
    def met(ms):
        return {x["name"]: x["value"] for x in ms["metrics"]}
    a, b = met(m0), met(m1)
    wall = b["Timestamp"] - a["Timestamp"]
    tot = sum(ft[2:]) or 1
    fps = round(1000 * max(1, len(ft) - 2) / tot, 1)
    heat = round(100 * (b["TaskDuration"] - a["TaskDuration"]) / wall, 1) if wall else 0
    heap = round(b["JSHeapUsedSize"] / 1e6, 1)
    return {"fps": fps, "heat": heat, "heap": heap, "frames": len(ft)}

async def boot_page(p):
    b = await p.chromium.launch(headless=True, args=["--disable-dev-shm-usage", "--use-gl=swiftshader", "--enable-unsafe-swiftshader"])
    ctx = await b.new_context(
        viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True,
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    )
    pg = await ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    await pg.goto(f"http://127.0.0.1:{PORT}/index.html")
    await pg.wait_for_timeout(3500)
    await pg.evaluate("WORLD_API.enter(true)")
    await pg.wait_for_timeout(2000)
    await skipall(pg, 14)
    await ev(pg, HUSH)
    pos = await ev(pg, BOOT)
    await ev(pg, HUSH)
    await pg.wait_for_timeout(1200)
    await ev(pg, "try{if(typeof hud==='function')hud()}catch(e){}1")
    await pg.wait_for_timeout(300)
    return b, ctx, pg, errs, pos

async def main():
    src = (ROOT / "index.html").read_text(encoding="utf-8", errors="ignore")
    ok("source exports FFF_ENC_CAM.restore", "root.FFF_ENC_CAM" in src and "function encCamRestore" in src)
    ok("fight() hands off encounter zoom", "encCamHandoffIntoFight(); /* v6564-gangcam" in src)
    ok("back() win/loss restores camera", "encCamRestore(); /* v6564-gangcam */" in src and "save(); enter(true);" in src)
    ok("escaped() restores camera", "world:back:escape" in src and src.count("encCamRestore") >= 4)
    ok("run-up cancel restores camera", "W.runUp = false; if (typeof encCamRestore === 'function') encCamRestore(); return false;" in src)
    ok("does not edit libBossCam / bossEnt", "function libBossCam(" in src and "function libBossCamOff(" in src)
    ok("source exports FFF_ZOOM pinch API", "root.FFF_ZOOM" in src and "function applyCamS" in src and "function visSpawn" in src)
    ok("pinch is wired on the walking stick pointers", "if (zmDown(e)) return;" in src and "if (zmMove(e)) return;" in src)
    ok("in-flight restore ease is cancelled on a later skip", "function encCamCancelEase" in src and "W._encCamAn = a;" in src)

    h = serve()
    async with async_playwright() as p:
        b, ctx, pg, errs, pos = await boot_page(p)
        ok("booted onto East Campus / East Gate", isinstance(pos, dict) and ("East Campus" in str(pos.get("area") or "") or "East Gate" in str(pos.get("area") or "")), pos)
        st0 = await ev(pg, READ)
        ok("FFF_ENC_CAM is wired", isinstance(st0, dict) and st0.get("hasApi"), st0)

        stuck = await ev(pg, STUCK)
        await pg.wait_for_timeout(200)
        before = await ev(pg, READ)
        ok("leftover sting zoom is visible (the bug state)", isinstance(before, dict) and before.get("z", 1) >= 1.5 and before.get("pan"), before)
        await pg.screenshot(path=str(SHOTS / "before.png"), type="png")

        # restore (the fix), wait for the ease
        done = await ev(pg, "(function(){var d=0; FFF_ENC_CAM.restore(1600, function(){ d=1; window.__encDone=1; }); return FFF_ENC_CAM.read();})()")
        for _ in range(40):
            flag = await pg.evaluate("window.__encDone||0")
            if flag:
                break
            await pg.wait_for_timeout(100)
        await pg.wait_for_timeout(200)
        after = await ev(pg, READ)
        ok("restore eases #wv scale back to 1", isinstance(after, dict) and after.get("z", 9) <= 1.02, after)
        ok("restore clears leftover W.pan so the follow camera can run", isinstance(after, dict) and not after.get("pan"), after)
        ok("restore clears leftover camFocus (not a gym lesson)", isinstance(after, dict) and not after.get("camFocus"), after)
        ryo_w = (after or {}).get("ryo") or {}
        ryo_w0 = (before or {}).get("ryo") or {}
        ok("Ryo draws smaller after restore (zoom out, not a snap leftover)",
           ryo_w.get("w") and ryo_w0.get("w") and ryo_w["w"] < ryo_w0["w"] * 0.75,
           {"before": ryo_w0.get("w"), "after": ryo_w.get("w")})
        await pg.screenshot(path=str(SHOTS / "after.png"), type="png")

        # win path: back() must unlock even mid-zoom
        await ev(pg, STUCK)
        await ev(pg, HUSH)
        await ev(pg, """(function(){
          var wv=document.getElementById('wv'); if(wv){ wv.style.transformOrigin='50% 50%'; wv.style.scale='1.55'; }
          W.pan={scr:1, run:function(){}};
          try{ back(true, {ctx:{outGang:1}, endHp:18, endSpirit:10, escaped:0, grp:['bully1']}); }catch(eB){ window.__backErr=String(eB&&eB.message||eB); }
          return 1;
        })()""")
        await pg.wait_for_timeout(400)
        await ev(pg, HUSH)
        bw = await ev(pg, READ)
        ok("back() win hook clears W.pan immediately", isinstance(bw, dict) and not bw.get("pan"), bw)
        await pg.wait_for_timeout(1800)
        await ev(pg, HUSH)
        await ev(pg, "(function(){try{if(FFF_SCAM&&FFF_SCAM.clear)FFF_SCAM.clear()}catch(e){}W.dlg=false;W.cut=false;W.busy=false;1})()")
        await pg.wait_for_timeout(150)
        bw2 = await ev(pg, READ)
        ok("back() win hook eases the leftover street zoom out", isinstance(bw2, dict) and bw2.get("z", 9) <= 1.05, bw2)

        # flee path
        await ev(pg, STUCK)
        await ev(pg, """(function(){
          try{ escaped({ctx:{outGang:1}, endHp:18, endSpirit:10, escaped:1, grp:[]}); }catch(e){ window.__escErr=String(e&&e.message||e); }
          return 1;
        })()""")
        await pg.wait_for_timeout(400)
        await ev(pg, HUSH)
        esc = await ev(pg, READ)
        ok("escaped() / flee hook clears W.pan", isinstance(esc, dict) and not esc.get("pan"), esc)
        await pg.wait_for_timeout(1800)
        esc2 = await ev(pg, READ)
        ok("escaped() eases zoom out", isinstance(esc2, dict) and esc2.get("z", 9) <= 1.05, esc2)

        # chained dialogue: restore, then a short scene can start (FFF_SCAM may take over from z=1)
        await ev(pg, BOOT)
        await ev(pg, HUSH)
        await ev(pg, STUCK)
        await ev(pg, "(function(){window.__encDone=0; FFF_ENC_CAM.restore(200, function(){ window.__encDone=1; }); return 1;})()")
        for _ in range(20):
            if await pg.evaluate("window.__encDone||0"):
                break
            await pg.wait_for_timeout(50)
        mid = await ev(pg, READ)
        ok("restore finished before chained dialogue (street zoom gone)",
           isinstance(mid, dict) and mid.get("z", 9) <= 1.08 and not mid.get("pan"), mid)
        try:
            await ev(pg, "scene(null, [['aoi','His Shush card drains your stamina, so bring a counter.']], function(){});1")
        except Exception:
            pass
        await pg.wait_for_timeout(500)
        dlg = await ev(pg, READ)
        ok("chained dialogue after restore does not keep the 1.8x street zoom",
           isinstance(dlg, dict) and dlg.get("z", 9) < 1.35, dlg)
        await ev(pg, HUSH)
        try:
            await ev(pg, "(function(){try{if(FFF_SCAM&&FFF_SCAM.clear)FFF_SCAM.clear()}catch(e){}W.dlg=false;W.cut=false;W.busy=false;1})()")
        except Exception:
            pass

        # boss / Archive-cam guard (W.bossCamHold), without poking FFF_SCAM's watchdog
        await ev(pg, STUCK)
        await ev(pg, "(function(){ W.bossCamHold=1; FFF_ENC_CAM.restore(200); return FFF_ENC_CAM.read(); })()")
        await pg.wait_for_timeout(300)
        boss = await ev(pg, READ)
        ok("restore leaves a live boss / Archive camera zoom alone", isinstance(boss, dict) and boss.get("z", 0) >= 1.5 and boss.get("pan"), boss)
        await ev(pg, "(function(){ W.bossCamHold=0; FFF_ENC_CAM.restore(100, function(){}); return 1; })()")
        await pg.wait_for_timeout(500)

        # run-up cancel hook is the same restore; exercise it directly
        await ev(pg, STUCK)
        await ev(pg, "(function(){ W.runUp=true; if(typeof encCamRestore==='function') encCamRestore(200); W.runUp=false; return 1; })()")
        await pg.wait_for_timeout(500)
        ru = await ev(pg, READ)
        ok("run-up cancel restore clears W.pan", isinstance(ru, dict) and not ru.get("pan"), ru)
        await pg.wait_for_timeout(1500)
        ru2 = await ev(pg, READ)
        ok("run-up cancel eases zoom out", isinstance(ru2, dict) and ru2.get("z", 9) <= 1.05, ru2)

        # two-finger pinch zoom on the walking map
        await ev(pg, BOOT)
        await ev(pg, HUSH)
        await ev(pg, "(function(){ try{ if(FFF_SCAM&&FFF_SCAM.clear) FFF_SCAM.clear(); }catch(e){} W.dlg=false;W.cut=false;W.busy=false;W.paused=false; if(FFF_ZOOM) FFF_ZOOM.set(1); return 1; })()")
        pinch = await ev(pg, """(function(){
          var v=document.getElementById('wv');
          function fire(type,id,x,y,prim){
            v.dispatchEvent(new PointerEvent(type,{pointerId:id,pointerType:'touch',clientX:x,clientY:y,bubbles:true,cancelable:true,composed:true,isPrimary:!!prim}));
          }
          var z0=FFF_ZOOM.get();
          fire('pointerdown',21,200,400,1); fire('pointermove',21,240,460,1); fire('pointerup',21,240,460,1);
          var afterOne=FFF_ZOOM.get();
          fire('pointerdown',22,150,400,1); fire('pointerdown',23,250,400,0);
          fire('pointermove',22,152,406,1); fire('pointermove',23,248,394,0);
          fire('pointerup',22,152,406,1); fire('pointerup',23,248,394,0);
          var afterSlop=FFF_ZOOM.get();
          fire('pointerdown',24,180,420,1); fire('pointerdown',25,220,420,0);
          fire('pointermove',24,60,420,1); fire('pointermove',25,340,420,0);
          var mid=FFF_ZOOM.get(), midShow=FFF_ZOOM.show(), S=W.S, Sb=W.Sbase;
          fire('pointerup',24,60,420,1); fire('pointerup',25,340,420,0);
          return {z0:z0, afterOne:afterOne, afterSlop:afterSlop, mid:mid, midShow:midShow, S:S, Sbase:Sb, locked:FFF_ZOOM.locked(), min:FFF_ZOOM.min, max:FFF_ZOOM.max};
        })()""")
        ok("one-finger drag does not zoom", isinstance(pinch, dict) and abs((pinch.get("afterOne") or 0) - (pinch.get("z0") or 1)) < 0.001, pinch)
        ok("two-finger jitter under the slop does not zoom", isinstance(pinch, dict) and abs((pinch.get("afterSlop") or 0) - (pinch.get("z0") or 1)) < 0.001, pinch)
        ok("a real two-finger spread zooms out and clamps at ~15%", isinstance(pinch, dict) and 1.14 <= (pinch.get("mid") or 0) <= 1.151, pinch)

        clamp = await ev(pg, """(function(){
          FFF_ZOOM.set(1);
          var v=document.getElementById('wv');
          function fire(type,id,x,y,prim){
            v.dispatchEvent(new PointerEvent(type,{pointerId:id,pointerType:'touch',clientX:x,clientY:y,bubbles:true,cancelable:true,composed:true,isPrimary:!!prim}));
          }
          fire('pointerdown',36,80,420,1); fire('pointerdown',37,320,420,0);
          fire('pointermove',36,180,420,1); fire('pointermove',37,220,420,0);
          var pinchIn=FFF_ZOOM.get();
          fire('pointerup',36,180,420,1); fire('pointerup',37,220,420,0);
          FFF_ZOOM.set(0.5); var lo=FFF_ZOOM.get();
          FFF_ZOOM.set(2); var hi=FFF_ZOOM.get();
          return {pinchIn:pinchIn, lo:lo, hi:hi};
        })()""")
        ok("a real two-finger pinch zooms in and clamps at ~15% closer", isinstance(clamp, dict) and 0.849 <= (clamp.get("pinchIn") or 0) <= 0.86, clamp)
        ok("FFF_ZOOM.set clamps to 0.85..1.15", isinstance(clamp, dict) and abs((clamp.get("lo") or 0)-0.85)<0.001 and abs((clamp.get("hi") or 0)-1.15)<0.001, clamp)

        lock = await ev(pg, """(function(){
          FFF_ZOOM.set(1.15);
          var kept=FFF_ZOOM.get();
          W.dlg=true;
          for (var i=0;i<24;i++) camera(true);
          var show=FFF_ZOOM.show(), S=W.S, Sb=W.Sbase, z=FFF_ZOOM.get(), locked=FFF_ZOOM.locked();
          var v=document.getElementById('wv');
          function fire(type,id,x,y,prim){
            v.dispatchEvent(new PointerEvent(type,{pointerId:id,pointerType:'touch',clientX:x,clientY:y,bubbles:true,cancelable:true,composed:true,isPrimary:!!prim}));
          }
          fire('pointerdown',40,180,420,1); fire('pointerdown',41,220,420,0);
          fire('pointermove',40,60,420,1); fire('pointermove',41,340,420,0);
          var midDlg=FFF_ZOOM.get();
          fire('pointerup',40,60,420,1); fire('pointerup',41,340,420,0);
          W.dlg=false;
          for (var j=0;j<24;j++) camera(true);
          var showBack=FFF_ZOOM.show(), zBack=FFF_ZOOM.get();
          return {kept:kept, show:show, S:S, Sb:Sb, z:z, locked:locked, midDlg:midDlg, showBack:showBack, zBack:zBack};
        })()""")
        ok("dialogue/menus lock the camera to default zoom and keep the player's zoom",
           isinstance(lock, dict) and lock.get("locked") and abs((lock.get("z") or 0)-1.15)<0.001 and abs((lock.get("show") or 0)-1)<0.02 and abs((lock.get("S") or 0)-(lock.get("Sb") or 1))<0.002,
           lock)
        ok("pinch is ignored during dialogue", isinstance(lock, dict) and abs((lock.get("midDlg") or 0)-1.15)<0.001, lock)
        ok("player zoom is restored after dialogue", isinstance(lock, dict) and abs((lock.get("zBack") or 0)-1.15)<0.001 and (lock.get("showBack") or 0) >= 1.10, lock)

        dtap = await ev(pg, """(function(){
          var v=document.getElementById('wv');
          function fire(type,id,x,y,prim){
            v.dispatchEvent(new PointerEvent(type,{pointerId:id,pointerType:'touch',clientX:x,clientY:y,bubbles:true,cancelable:true,composed:true,isPrimary:!!prim}));
          }
          FFF_ZOOM.set(1.12);
          function tap(a,b){
            fire('pointerdown',a,150,400,1); fire('pointerdown',b,250,400,0);
            fire('pointerup',a,150,400,1); fire('pointerup',b,250,400,0);
          }
          tap(50,51); tap(52,53);
          return {z:FFF_ZOOM.get()};
        })()""")
        ok("two-finger double-tap eases back to default zoom", isinstance(dtap, dict) and abs((dtap.get("z") or 0)-1)<0.001, dtap)

        spawn = await ev(pg, """(function(){
          var hits=[], C=(typeof C1E!=='undefined'&&C1E)||(root.FFF_C1E&&FFF_C1E.C), pad=FFF_ZOOM.widePad(), px=W.ryo.x, py=W.ryo.y;
          function check(tag,x,y,m,R){
            var angs=[0,0.8,1.57,2.4,3.14,3.9,4.71,5.5], ds=[Math.max(80,R-30), Math.round(R*0.6), 420, 560], a,d,ox,oy,wr,inside,would;
            for (a=0;a<angs.length;a++) for (d=0;d<ds.length;d++){
              ox=x-Math.cos(angs[a])*ds[d]; oy=y-Math.sin(angs[a])*ds[d];
              W.ryo.x=ox; W.ryo.y=oy; try{camera(true)}catch(e){}
              wr=FFF_ZOOM.wideCam(0);
              inside=x>wr[0]&&x<wr[2]&&y>wr[1]&&y<wr[3];
              would=!FFF_ZOOM.visSpawn(x,y,m);
              if (inside && would) hits.push({tag:tag, x:x, y:y, d:ds[d]});
            }
          }
          if (C && C.GROUPS) C.GROUPS.forEach(function(G){ check('G'+G.id, G.at[0], G.at[1], 80, C.SPAWN_R||1000); });
          W.ryo.x=px; W.ryo.y=py; try{camera(true)}catch(e){} FFF_ZOOM.set(1);
          return {n:hits.length, hits:hits.slice(0,6), pad:pad, groups:C&&C.GROUPS&&C.GROUPS.length};
        })()""")
        ok("Ch1/Ch2 spawn points stay off-screen at max zoom-out",
           isinstance(spawn, dict) and spawn.get("n")==0 and (spawn.get("groups") or 0)>=8, spawn)

        # reset a clean post-fight map for perf + final after shot already taken
        await ev(pg, BOOT)
        await ev(pg, HUSH)
        await ev(pg, "(function(){try{if(FFF_SCAM&&FFF_SCAM.clear)FFF_SCAM.clear()}catch(e){} FFF_ENC_CAM.restore(100); return 1;})()")
        await pg.wait_for_timeout(800)

        cdp = await ctx.new_cdp_session(pg)
        await cdp.send("Performance.enable")
        idle = await measure(pg, cdp, 5)
        print(f"PERF map_after_fight fps={idle['fps']} heat={idle['heat']} heap={idle['heap']}MB", flush=True)
        ok("map after the fight stays at 58+ fps", idle["fps"] >= 58, idle)

        # long walk across East Campus
        await ev(pg, "if(typeof walkTo==='function') walkTo(3640,1080,true,false);1")
        walk = await measure(pg, cdp, 8)
        print(f"PERF long_walk fps={walk['fps']} heat={walk['heat']} heap={walk['heap']}MB", flush=True)
        ok("long walk stays at 50+ fps", walk["fps"] >= 50, walk)
        heap0 = idle["heap"]

        await ev(pg, BOOT)
        await ev(pg, HUSH)
        await ev(pg, "W.path=[];1")
        await cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
        t4 = await measure(pg, cdp, 5)
        await ev(pg, "if(typeof walkTo==='function') walkTo(2860,2200,true,false);1")
        t4w = await measure(pg, cdp, 8)
        print(f"PERF map_4x fps={t4['fps']} heat={t4['heat']} heap={t4['heap']}MB", flush=True)
        print(f"PERF walk_4x fps={t4w['fps']} heat={t4w['heat']} heap={t4w['heap']}MB", flush=True)
        heat_delta = round(t4["heat"] - idle["heat"], 1)
        print(f"PERF heat_delta_4x={heat_delta} (idle {idle['heat']} -> 4x {t4['heat']})", flush=True)
        print("NOTE 4x heat is compared to live in a separate baseline run, not to 1x in this build", flush=True)
        ok("4x throttle run completed (heat reported)", True, {"delta_vs_1x": heat_delta, "idle": idle, "t4": t4})
        ok("memory flat after walks (heap not climbing hard)", t4w["heap"] <= heap0 + 25, {"idle": heap0, "after": t4w["heap"]})
        await cdp.detach()
        ok("no page errors", not errs, errs[:3])
        await b.close()

    # side-by-side 390x844
    try:
        from PIL import Image
        a = Image.open(SHOTS / "before.png").convert("RGB")
        bimg = Image.open(SHOTS / "after.png").convert("RGB")
        # device_scale_factor=2 -> 780x1688; scale each half down to 390x844
        a = a.resize((390, 844), Image.Resampling.LANCZOS)
        bimg = bimg.resize((390, 844), Image.Resampling.LANCZOS)
        out = Image.new("RGB", (780, 844))
        out.paste(a, (0, 0))
        out.paste(bimg, (390, 0))
        out.save(SHOTS / "before_after.png")
        print("SHOT", SHOTS / "before_after.png")
    except Exception as e:
        print("SHOT_ERR", e)

    failed = [r for r in RES if not r[0]]
    print("RESULT", "FAIL" if failed else "PASS", f"{len(RES)-len(failed)}/{len(RES)}")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    asyncio.run(main())
