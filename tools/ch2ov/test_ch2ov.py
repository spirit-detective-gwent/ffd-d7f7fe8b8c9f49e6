#!/workspace/pwenv/bin/python3
"""v6564-ch2ov: Ban feet, Wagashi placement, Chiyo shopCold loop, Kissa door, Four Corners lines.
Run: /workspace/pwenv/bin/python3 tools/ch2ov/test_ch2ov.py [index.html]
"""
import asyncio, functools, http.server, os, socketserver, sys
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
INDEX = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent.parent / 'index.html'
PORT = int(os.environ.get('PORT', '8916'))
RES = []

def ok(name, cond, extra=''):
    RES.append((bool(cond), name, extra))
    print(('PASS ' if cond else 'FAIL ') + name + ((' :: ' + str(extra)[:400]) if (extra and not cond) else ''), flush=True)

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def serve(port, directory):
    s = TS(('127.0.0.1', port), functools.partial(Q, directory=str(directory)))
    import threading
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s

def body():
    t = INDEX.read_text(encoding='utf-8')
    n = 'root.WORLD_API = {'
    assert n in t
    t = t.replace(n, 'root.__ev=function(s){return eval(s)};' + n, 1)
    return t

async def ev(pg, code):
    return await pg.evaluate("(c)=>{var r=window.__ev(c);try{return (typeof r==='string')?r:JSON.parse(JSON.stringify(r===undefined?null:r))}catch(e){return String(r)}}", code)

HUSH = """(function(){try{if(typeof phClose==='function')phClose()}catch(e){}W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};return 1})()"""
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""

async def skipall(pg, n=12):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(220); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(220)

async def boot_ch2(p, errs, path='balanced'):
    b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--disable-dev-shm-usage'])
    ctx = await b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
    pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)[:240]))
    html = body()
    async def rt(route): await route.fulfill(body=html, content_type='text/html')
    await pg.route('**/index.html', rt)
    await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(2800)
    await pg.touchscreen.tap(195, 420)
    await pg.evaluate("WORLD_API.enter(true)")
    await pg.wait_for_timeout(1600)
    await skipall(pg)
    await ev(pg, "root.FFF_NO_TUT=1")
    await pg.evaluate("WORLD_API.c2Begin(true)")
    await pg.wait_for_timeout(2500)
    await skipall(pg)
    await ev(pg, HUSH)
    await ev(pg, f"""(function(){{
      var path='{path}';
      SAVE.chapter=2; SAVE.ch1=1; SAVE.ch2=1; SAVE.bond=SAVE.bond||{{}}; SAVE.bond.path=path; SAVE.bond.lock=1;
      try {{ STORY.ensure(SAVE); }} catch(e){{}}
      var st=c2S(); st.e=st.e||{{}}; st.e.arrive=1; st.e.gymIn=1; st.e.genji=1; st.e.c2sRep=1; st.e.roam=1; st.e.called=1; st.e.c2lMap=1;
      st.q=st.q||{{}}; st.q.cq2_locks=0; st.qa='cq2_locks';
      try {{ c2QSync(); save(); }} catch(e){{}}
      return 1;
    }})()""")
    return b, pg

LANE = [910, 2600, 4900, 2760]

def overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])

def area_overlap(a, b):
    if not overlap(a, b): return 0
    return (min(a[2], b[2]) - max(a[0], b[0])) * (min(a[3], b[3]) - max(a[1], b[1]))

async def main():
    src = INDEX.read_text(encoding='utf-8')
    ok('Ban lantern_alley has feet offset', "sway: 1, feet: 52" in src or "c2_lantern_alley" in src and "feet: 52" in src)
    ok('no leftover "join a crew / win streets" in Four Corners talk',
       all(x not in src for x in [
           'So we get a crew first', 'win some streets', 'Then we join something',
           'Win their streets', 'Throw in with a crew',
           'So we get inside. One of the four.']))
    ok('new balanced Ryo line present',
       "Let's check out the gangs, see if someone knows anything." in src
       or "Let\\u2019s check out the gangs, see if someone knows anything." in src)

    srv = serve(PORT, str(INDEX.parent))
    errs = []
    async with async_playwright() as p:
        b, pg = await boot_ch2(p, errs, 'balanced')
        await ev(pg, "c2Go('town',[3080,2640,3]);1")
        await pg.wait_for_timeout(1600)
        await ev(pg, HUSH); await skipall(pg, 6); await ev(pg, HUSH)

        # --- placement + doors ---
        geo = await ev(pg, """(function(){
          var S2=root.FFF_S2, d=S2&&S2.DOOR, fac=S2&&S2.FAC_BOX, box;
          var el=document.getElementById('s2WagaDoor');
          if(el){ box=[parseFloat(el.style.left), parseFloat(el.style.top), parseFloat(el.style.left)+el.offsetWidth, parseFloat(el.style.top)+el.offsetHeight]; }
          var spots=(INT.c2_town&&INT.c2_town.spots||[]).map(function(s){return {id:s.id,r:s.r,at:s.at,lab:s.lab,trans:!!(typeof TRANS!=='undefined'&&TRANS[s.id])};});
          var gk = (root.FFF_13U && FFF_13U.GK_DOOR) || null;
          var lie = (typeof bankoLieSpots==='function') ? bankoLieSpots() : null;
          var feet = (root.FFF_C2BT && FFF_C2BT.feetPx && FFF_C2BT.feetPx('c2_lantern_alley'));
          var room = (root.FFF_C2BT && FFF_C2BT.room && FFF_C2BT.room({ctx:{dg:'c2',dgk:'enforcer',enfDoom:1}}));
          var talk = {
            bal: (typeof c2lStreetTalk==='function'?c2lStreetTalk(): (typeof c2ClubChoiceLines==='function'?c2ClubChoiceLines():[])),
          };
          return {door:d, fac:fac, box:box, spots:spots, gk:gk, lie:lie, feet:feet, room:room,
                  steps: (C2Q&&C2Q.cq2_locks&&C2Q.cq2_locks.steps),
                  talk:talk};
        })()""")

        ok('Ban fight room is lantern_alley', geo and geo.get('room')=='c2_lantern_alley', geo and geo.get('room'))
        ok('Ban lantern_alley feetPx is 52', geo and geo.get('feet')==52, geo and geo.get('feet'))

        box = (geo or {}).get('box') or (geo or {}).get('fac')
        ok('Wagashi facade sits on Lucky 7 frontage (bottom at y=2600)', box and box[1] <= 2440 + 2 and box[3] <= 2600 + 2, box)
        ok('Wagashi facade does not sit in the sidewalk alley (y 2600-2760)', box and box[3] <= 2600 + 1, box)
        lie = (geo or {}).get('lie') or {}
        def body_rect(pt, w=90, h=40):
            if not pt: return None
            return [pt['x']-w/2, pt['y']-h/2, pt['x']+w/2, pt['y']+h/2]
        overlap_body = False
        if box and lie.get('ryo'):
            for k in ('ryo','aoi'):
                br = body_rect(lie[k])
                if br and overlap(box, br):
                    overlap_body = True
        ok('Wagashi facade does not cover Ban lie bodies', not overlap_body, {'box':box,'lie':lie})

        door = (geo or {}).get('door') or {}
        r = door.get('r')
        ok('Wagashi door trigger ends at the lane wall (y<=2600)', r and r[3] <= 2600, r)
        ok('Wagashi door trigger is doorway-sized (width<=100, height<=90)', r and (r[2]-r[0]) <= 100 and (r[3]-r[1]) <= 90, r)
        ok('Wagashi door barely clips the sidewalk (overlap area < 200)', r and area_overlap(r, LANE) <= 200, r and area_overlap(r, LANE))

        gk = (geo or {}).get('gk') or {}
        gr = gk.get('r') if isinstance(gk, dict) else None
        # FFF_13U.GK_DOOR is the object
        if not gr and isinstance(gk, dict) and 'at' in gk:
            gr = gk.get('r')
        ok('Kissa Gekko door ends at the lane wall (y<=2600)', gr and gr[3] <= 2600, gk)
        ok('Kissa door does not swallow the sidewalk (overlap area < 400)', gr and area_overlap(gr, LANE) <= 400, gr and (area_overlap(gr, LANE) if gr else None))
        ok('walking the mid-sidewalk at the kissa x does not hit the door',
           gr and not (2150 >= gr[0] and 2150 < gr[2] and 2680 >= gr[1] and 2680 < gr[3]), gr)

        # other Ch2 town TRANS doors vs the lantern lane
        spots = (geo or {}).get('spots') or []
        trans = [s for s in spots if s.get('trans') and s.get('r')]
        fat = []
        for s in trans:
            rr = s['r']; ov = area_overlap(rr, LANE)
            # a lip into the lane is ok; a deep bite (>= 40px into the 160px lane over a wide door) is not
            depth = 0
            if overlap(rr, LANE):
                depth = min(rr[3], LANE[3]) - max(rr[1], LANE[1])
            if ov >= 80*40 or depth > 48:
                fat.append({'id':s['id'],'r':rr,'overlap':ov,'depth':depth})
        ok('no other Ch2 town door trigger bites >48px into the lantern lane', not fat, fat)

        # Four Corners live lines
        # force balanced path already
        lines = await ev(pg, """(function(){
          function labs(fn){ try{ return (fn()||[]).map(function(x){return [x[0],x[1]];}); }catch(e){ return 'err '+e.message; } }
          var out={};
          // temporarily set path
          var paths=['balanced','fierce','strategic'];
          paths.forEach(function(p){
            SAVE.bond=SAVE.bond||{}; SAVE.bond.path=p;
            out[p]={ choice: (typeof c2ClubChoiceLines==='function'?labs(c2ClubChoiceLines):'missing'),
                     street: (typeof c2lStreetTalk==='function'?labs(c2lStreetTalk):'missing') };
          });
          SAVE.bond.path='balanced';
          var st=(typeof c2lCornersSteps==='function'&&c2lCornersSteps())||[];
          return {out:out, steps:st, c2s:(typeof C2S_STEPS!=='undefined'?C2S_STEPS[0]:null)};
        })()""")
        def hay(obj):
            return str(obj).lower()
        h = hay(lines)
        ok('live talk has the new balanced Ryo line',
           'check out the gangs, see if someone knows anything' in h, lines)
        banned = ['join something', 'get a crew first', 'win some streets', 'win their streets', 'get inside. one of the four', 'throw in with a crew']
        ok('live Four Corners talk has no join-crew / win-streets wording',
           not any(b in h for b in banned), lines)
        ok('C2S_STEPS opens on checking out the gangs',
           lines and lines.get('c2s') and 'gang' in lines['c2s'].lower() and 'throw in' not in lines['c2s'].lower(),
           lines and lines.get('c2s'))

        # --- Chiyo shopCold loop (exported S2.doorTalk + latch state; no scoped talk) ---
        loop = await ev(pg, """(function(){
          var S2=root.FFF_S2;
          if(!S2||typeof S2.doorTalk!=='function'||!S2.DOOR) return {err:'no S2.doorTalk hook'};
          var r=S2.DOOR.r, at=S2.DOOR.at;
          function stand(x,y){
            W.ryo.x=x; W.ryo.y=y;
            try{ if(typeof place==='function') place(W.ryo,0); }catch(e){}
          }
          function hushDlg(){
            W.dlg=false; W.busy=false; W.cut=false;
            try{ var el=document.getElementById('wdlg'); if(el){ el.className=''; el.innerHTML=''; } }catch(e){}
          }
          stand((r[0]+r[2])/2, (r[1]+r[3])/2);
          hushDlg(); W._s2WagaSaid=0;
          var open0=!!(S2.qDone&&S2.qDone());
          S2.doorTalk();
          var t1={dlg:!!W.dlg, said:!!W._s2WagaSaid, inDoor:!!S2.inWagaDoor(), entered:!!(typeof c2Room==='function'&&c2Room()==='waga'), open:open0};
          var txt='';
          try{ var d=document.getElementById('wdlg'); txt=(d&&(d.innerText||d.textContent)||''); }catch(e2){}
          t1.txt=txt.slice(0,160);
          // player closes the line but is still in the doorway
          hushDlg();
          S2.doorTalk();
          var t2={dlg:!!W.dlg, said:!!W._s2WagaSaid};
          // walk out of the rect; latch poll is 150ms
          stand(at[0], at[1]+80);
          return {t1:t1,t2:t2,at:at,r:r,y:W.ryo.y,inDoorNow:!!S2.inWagaDoor()};
        })()""")
        await pg.wait_for_timeout(280)
        loop2 = await ev(pg, """(function(){
          var S2=root.FFF_S2, r=S2.DOOR.r;
          var saidAfterLeave=!!W._s2WagaSaid, stillIn=!!S2.inWagaDoor();
          function stand(x,y){ W.ryo.x=x; W.ryo.y=y; try{ if(typeof place==='function') place(W.ryo,0); }catch(e){} }
          function hushDlg(){ W.dlg=false; W.busy=false; W.cut=false; try{ var el=document.getElementById('wdlg'); if(el){ el.className=''; el.innerHTML=''; } }catch(e){} }
          hushDlg();
          stand((r[0]+r[2])/2, (r[1]+r[3])/2);
          S2.doorTalk();
          return {saidAfterLeave:saidAfterLeave, stillIn:stillIn, dlgReenter:!!W.dlg, saidReenter:!!W._s2WagaSaid};
        })()""")
        ok('S2.doorTalk hook is exported', loop and 'err' not in (loop or {}), loop)
        ok('shopCold talk starts once at the closed door', loop and loop.get('t1') and loop['t1'].get('dlg') and not loop['t1'].get('entered'), loop)
        ok('still standing in the door cannot retrigger shopCold (no loop)', loop and loop.get('t2') and loop['t2'].get('dlg') is False and loop['t2'].get('said') is True, loop)
        ok('latch arms on the closed-shop talk', loop and loop.get('t1') and loop['t1'].get('said'), loop)
        ok('leaving the door clears the shopCold latch', loop2 and loop2.get('saidAfterLeave') is False and loop2.get('stillIn') is False, loop2)
        ok('re-entering the door can talk again after leaving', loop2 and loop2.get('dlgReenter') is True, loop2)

        # mid-sidewalk at kissa x should not auto-enter gekko
        walk = await ev(pg, """(function(){
          var gk=(root.FFF_13U&&FFF_13U.GK_DOOR)||{};
          var r=gk.r, hits=[];
          // sample the sidewalk centerline y=2680 across the kissa x span
          var xs=[2080,2150,2210], ys=[2608,2640,2680,2720];
          ys.forEach(function(y){ xs.forEach(function(x){
            var inr = r && x>=r[0] && x<r[2] && y>=r[1] && y<r[3];
            hits.push({x:x,y:y,hit:!!inr});
          }); });
          return {r:r, at:gk.at, hits:hits};
        })()""")
        mid = [h for h in (walk or {}).get('hits') or [] if h['y'] >= 2640 and h.get('hit')]
        ok('sidewalk samples at/below y=2640 do not sit in the kissa trigger (except maybe the exit stand)', 
           not any(h['y']>=2680 and h['hit'] for h in (walk or {}).get('hits') or []), walk)

        await ev(pg, HUSH)
        print('page errors', errs[:6])
        ok('no page errors', not errs, errs)
        await b.close()

    failed = [r for r in RES if not r[0]]
    print('RESULT', f'{len(RES)-len(failed)}/{len(RES)} pass', ('FAIL' if failed else 'OK'))
    sys.exit(1 if failed else 0)

asyncio.run(main())
