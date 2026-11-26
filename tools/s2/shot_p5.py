#!/workspace/pwenv/bin/python3
"""Capture in-game Masa's Seal stills to phase5/wired/."""
import asyncio, functools, http.server, socketserver, threading, os, sys
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
INDEX = HERE.parent.parent / 'index.html'
OUT = Path('/workspace/v6560-review/seal2/phase5/wired')
OUT.mkdir(parents=True, exist_ok=True)
PORT = int(os.environ.get('PORT', '8895'))
SUFFIX = os.environ.get('SHOT_SUFFIX', '')
ONLY = set(filter(None, os.environ.get('SHOTS', '').split(',')))

ROOMS = [
    ('dyard', '01_yard_gate'),
    ('dclock', '02_time_clock'),
    ('dbay', '03_loading_bay'),
    ('dcrate', '04_crate_stacks'),
    ('dcold', '05_cold_store'),
    ('dcage', '06_parts_cage'),
    ('dbike', '07_bike_bay'),
    ('dloft', '08_dispatch_loft'),
    ('dbreak', '09_break_room'),
    ('dtun', '10_tunnel_spur'),
    ('dman', '11_manifest_office'),
    ('dant', '12_lift_anteroom'),
    ('dshut', '13_lift_shutter'),
]

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def body():
    t = INDEX.read_text(encoding='utf-8')
    t = t.replace('root.FFF_13U = { CONTEST', 'root.__ev=function(s){return eval(s)};root.FFF_13U = { CONTEST', 1)
    return t

async def ev(pg, code):
    return await pg.evaluate("(c)=>{var r=window.__ev(c);try{return (typeof r==='string')?r:JSON.parse(JSON.stringify(r===undefined?null:r))}catch(e){return String(r)}}", code)

HUSH = """(function(){try{if(typeof phClose==='function')phClose()}catch(e){}
W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];
var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};
var q=document.getElementById('wquest'); if(q) q.style.display='none';
return 1})()"""

async def skipall(pg, n=8):
    SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(200); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(200)

async def shot(pg, name, hush=True):
    if hush:
        await ev(pg, HUSH)
        await pg.wait_for_timeout(200)
    if ONLY and name not in ONLY and (name + SUFFIX) not in ONLY:
        print('skip', name, flush=True)
        return None
    path = OUT / f'{name}{SUFFIX}.png'
    await pg.screenshot(path=str(path), type='png')
    print('shot', path, flush=True)
    return path

async def boot(pg):
    await pg.touchscreen.tap(195, 420)
    await pg.evaluate("WORLD_API.enter(true)")
    await pg.wait_for_timeout(1500)
    await skipall(pg)
    await ev(pg, "root.FFF_NO_TUT=1")
    await pg.evaluate("WORLD_API.c2Begin(true)")
    await pg.wait_for_timeout(2500)
    await skipall(pg)
    await ev(pg, HUSH)
    return await ev(pg, """(function(){
      SAVE.chapter=2; SAVE.ch1=1; SAVE.ch2=1; SAVE.bond=SAVE.bond||{}; SAVE.bond.path='fierce'; SAVE.bond.lock=1;
      try { STORY.ensure(SAVE); } catch(e){}
      var st=c2S(); st.e=st.e||{}; st.e.run_fac='arc'; st.e.seal_sento=1; st.e.sealKnown=1; st.e.c2sRep=1; st.e.c2lMap=1;
      st.e.n13='done'; st.e.arrive=1; st.e.gymIn=1; st.e.genji=1; st.e.nq=st.e.nq||{};
      st.q.cq2_arrive=9; st.q.cq2_hq=9; st.q.cq2_scout=9;
      st.q=st.q||{}; st.q.cq2_nq_west=9; st.q.cq2_nq_cold=9; st.q.cq2_nq_paint=9; st.q.cq2_nq_door=9; st.q.cq2_nq_seal=9;
      st.q.cq2_locks=0; st.qa='cq2_locks';
      st.q.cq2_s2_waga=9; if (root.FFF_S2&&root.FFF_S2.setStg) root.FFF_S2.setStg('done');
      st.q.cq2_s2_runs=9; if (root.FFF_S2P2&&root.FFF_S2P2.setStg) root.FFF_S2P2.setStg('done');
      st.q.cq2_s2_boat=9; if (root.FFF_S2P3&&root.FFF_S2P3.setStg) root.FFF_S2P3.setStg('done');
      st.q.cq2_s2_gar=9; if (root.FFF_S2P4&&root.FFF_S2P4.setStg) root.FFF_S2P4.setStg('done');
      st.e.baseOpen_dep=1; st.e.guardGone_depot=1;
      try { c2QSync(); save(); } catch(e){}
      try { if (root.FFF_S2P5&&root.FFF_S2P5.chainRepair) root.FFF_S2P5.chainRepair(); } catch(e5){}
      return { p5:!!root.FFF_S2P5, q:st.q.cq2_s2_depot, stg:root.FFF_S2P5&&root.FFF_S2P5.stg&&root.FFF_S2P5.stg() };
    })()""")

async def go_room(pg, k, x=640, y=720, face=0):
    return await ev(pg, f"""(function(){{
      var P5=root.FFF_S2P5;
      try {{ c2Go('{k}', [{x}, {y}, {face}]); }} catch(e){{}}
      try {{ if (typeof c2Pop==='function') c2Pop(); }} catch(e2){{}}
      try {{ if (W.ryo) {{ W.ryo.x={x}; W.ryo.y={y}; place(W.ryo,0); }} if (W.aoi) {{ W.aoi.x={x}-80; W.aoi.y={y}+40; place(W.aoi,0); }} camera(true); }} catch(e3){{}}
      try {{ if (P5 && P5.paintRoom) P5.paintRoom(); }} catch(e4){{}}
      return {{ room: typeof c2Room==='function'?c2Room():null, canvas:!!document.getElementById('s2P5Room_{k}'), masa:!!(W.c2n&&W.c2n.s2masa) }};
    }})()""")

async def go_town(pg, x, y):
    await ev(pg, f"""(function(){{
      try {{ c2Go('town', [{x}, {y}, 0]); }} catch(e){{}}
      try {{ if (W.ryo) {{ W.ryo.x={x}; W.ryo.y={y}; place(W.ryo,0); }} if (W.aoi) {{ W.aoi.x={x}-60; W.aoi.y={y}+40; place(W.aoi,0); }} camera(true); }} catch(e3){{}}
      return typeof c2Room==='function'?c2Room():null;
    }})()""")
    await ev(pg, HUSH)
    await pg.wait_for_timeout(400)

async def main():
    s = TS(('127.0.0.1', PORT), functools.partial(Q, directory=str(INDEX.parent)))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    errs = []
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        html = body()
        async def rt(route): await route.fulfill(body=html, content_type='text/html')
        await pg.route('**/index.html', rt)
        await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(2200)
        info = await boot(pg)
        print('boot', info, flush=True)

        await go_town(pg, 4300, 3880)
        await shot(pg, '00_depot_approach')

        # 13 rooms, Masa at the yard then at the shutter
        for k, name in ROOMS:
            stg = 'open' if k == 'dyard' else 'met'
            qn = 1 if stg == 'met' else 0
            await ev(pg, f"""(function(){{
              var P5=root.FFF_S2P5, st=c2S();
              st.e.masaFate=''; st.e.seal_depot=0;
              P5.setStg('{stg}'); st.q.cq2_s2_depot={qn};
              return P5.stg();
            }})()""")
            xy = (500, 760) if k == 'dyard' else ((640, 760) if k == 'dshut' else (640, 720))
            info = await go_room(pg, k, xy[0], xy[1])
            print(name, info, flush=True)
            await pg.wait_for_timeout(500)
            await ev(pg, HUSH)
            await shot(pg, name)

        # battle shutter (paint the hook room onto a live canvas if the fight UI is not up)
        battle = await ev(pg, """(function(){
          var P5=root.FFF_S2P5, BT=root.FFF_C2BT;
          try { if (P5 && P5.hookBattle) P5.hookBattle(); } catch(e){}
          var m=document.getElementById('wimap')||document.getElementById('world');
          var c=document.getElementById('s2P5Battle');
          if (c && c.parentNode) c.parentNode.removeChild(c);
          c=document.createElement('canvas'); c.id='s2P5Battle'; c.width=1280; c.height=900;
          c.className='nqprop';
          c.style.cssText='position:absolute;left:0;top:0;width:1280px;height:900px;z-index:1;pointer-events:none';
          if (m) m.insertBefore(c, m.firstChild);
          try { if (root.FFF_S2P && FFF_S2P.battleShutter) FFF_S2P.battleShutter(c.getContext('2d')); } catch(e2){ return {err:String(e2)}; }
          try { c2Go('dshut',[640,720,0]); if (typeof c2Pop==='function') c2Pop(); } catch(e3){}
          try { if (W.ryo) { W.ryo.x=560; W.ryo.y=700; place(W.ryo,0);} if (W.aoi) { W.aoi.x=480; W.aoi.y=740; place(W.aoi,0);} camera(true);} catch(e4){}
          return { room: typeof c2Room==='function'?c2Room():null, painted:!!c, hook:!!(BT&&BT.ROOMS&&BT.ROOMS.sh) };
        })()""")
        print('battle', battle, flush=True)
        await pg.wait_for_timeout(400)
        await ev(pg, HUSH)
        await shot(pg, '14_battle_shutter')
        await ev(pg, """(function(){ var c=document.getElementById('s2P5Battle'); if(c&&c.parentNode)c.parentNode.removeChild(c); return 1; })()""")

        # after-win shutter fates
        for fate, name in [('leave', '15_after_leave'), ('notes', '16_after_notes'), ('help', '17_after_help')]:
            info = await ev(pg, f"""(function(){{
              var P5=root.FFF_S2P5, st=c2S();
              P5.setStg('won'); st.q.cq2_s2_depot=2; st.e.masaFate='{fate}'; st.e.seal_depot=0;
              try {{ c2Go('dshut',[640,720,0]); if (typeof c2Pop==='function') c2Pop(); }} catch(e){{}}
              try {{ if (W.ryo) {{ W.ryo.x=560; W.ryo.y=740; place(W.ryo,0); }} if (W.aoi) {{ W.aoi.x=480; W.aoi.y=780; place(W.aoi,0); }} camera(true); }} catch(e2){{}}
              /* drop cache so the fate painter is used */
              try {{
                var el=document.getElementById('s2P5Room_dshut');
                if (el && el.parentNode) el.parentNode.removeChild(el);
                if (P5.paintRoom) P5.paintRoom();
              }} catch(e3){{}}
              return {{ room:c2Room(), fate:st.e.masaFate, canvas:!!document.getElementById('s2P5Room_dshut') }};
            }})()""")
            print(name, info, flush=True)
            await pg.wait_for_timeout(400)
            await ev(pg, HUSH)
            await shot(pg, name)

        # bond question dialog (do not hush)
        bond = await ev(pg, """(function(){
          var P5=root.FFF_S2P5, st=c2S();
          P5.setStg('won'); st.q.cq2_s2_depot=2; st.e.masaFate=''; st.e.seal_depot=0;
          try { var B=STORY.bond(SAVE); if (B && B.picks) delete B.picks.c2_masa_after; } catch(e){}
          try { c2Go('dshut',[640,720,0]); if (typeof c2Pop==='function') c2Pop(); } catch(e2){}
          try { if (W.ryo) { W.ryo.x=560; W.ryo.y=740; place(W.ryo,0); } if (W.aoi) { W.aoi.x=480; W.aoi.y=780; place(W.aoi,0); } camera(true); } catch(e3){}
          try { W.dlg=false; W.cut=false; W.busy=false; } catch(e4){}
          P5.askBond();
          return 1;
        })()""")
        # wait for bond options
        shown = False
        for i in range(20):
            await pg.wait_for_timeout(250)
            st = await ev(pg, """(function(){var n=document.querySelectorAll('#wdlg.on button.bondopt').length; var t=((document.querySelector('#wdlg.on .bqq,#wdlg.on .tw')||{}).textContent)||''; return {n:n,t:t.slice(0,80)};})()""")
            print('bond wait', st, flush=True)
            if isinstance(st, dict) and st.get('n', 0) >= 3:
                shown = True
                break
        print('bond shown', shown, bond, flush=True)
        await shot(pg, '18_bond_question', hush=False)

        # after-seal tenants in the Minato-so lobby
        ten = await ev(pg, """(function(){
          var P5=root.FFF_S2P5, P2=root.FFF_S2P2, st=c2S();
          st.e.seal_depot=1; st.e.eastSeal=1; st.e.masaFate='help';
          P5.setStg('done'); st.q.cq2_s2_depot=9;
          try { c2Go('mina',[640,700,0]); if (typeof c2Pop==='function') c2Pop(); } catch(e){}
          try { if (W.ryo) { W.ryo.x=640; W.ryo.y=700; place(W.ryo,0); } if (W.aoi) { W.aoi.x=560; W.aoi.y=740; place(W.aoi,0); } camera(true); } catch(e2){}
          return { room: typeof c2Room==='function'?c2Room():null, after:P5.afterSeal&&P5.afterSeal(), mori:!!(W.c2n&&(W.c2n.s2mori||true)) };
        })()""")
        print('tenants', ten, flush=True)
        await pg.wait_for_timeout(500)
        await ev(pg, HUSH)
        await shot(pg, '19_tenants_after_seal')

        # sealed shutter
        sealed = await ev(pg, """(function(){
          var P5=root.FFF_S2P5, st=c2S();
          st.e.seal_depot=1; st.e.masaFate='help'; P5.setStg('done'); st.q.cq2_s2_depot=9;
          try { c2Go('dshut',[640,720,0]); if (typeof c2Pop==='function') c2Pop(); } catch(e){}
          try { if (W.ryo) { W.ryo.x=560; W.ryo.y=740; place(W.ryo,0); } camera(true); } catch(e2){}
          try { var el=document.getElementById('s2P5Room_dshut'); if(el&&el.parentNode)el.parentNode.removeChild(el); if(P5.paintRoom)P5.paintRoom(); } catch(e3){}
          return { room:c2Room(), canvas:!!document.getElementById('s2P5Room_dshut') };
        })()""")
        print('sealed', sealed, flush=True)
        await pg.wait_for_timeout(400)
        await ev(pg, HUSH)
        await shot(pg, '20_shutter_sealed')

        # Genji / city map after down_dep: SE quarter Punk red, X4 Punk vs Syndicate,
        # Masa/Riders (and already-beaten Gōda/Hustlers) stood down. Hide leftover Ch2-start banners
        # (Downtown Arrival is a c2Begin harness leftover, z-index 60 over the map).
        mmap = await ev(pg, """(function(){
          var P5=root.FFF_S2P5, st=c2S();
          st.e.run_fac='arc'; st.e.down_dep=1; st.e.seal_depot=1; st.e.eastSeal=1;
          st.e.down_bat=1; st.e.seal_sento=1;
          st.e.masaFate='help'; P5.setStg('done'); st.q.cq2_s2_depot=9;
          st.q.cq2_arrive=9; st.q.cq2_hq=9; st.q.cq2_scout=9;
          try { if (P5.applySeTurf) P5.applySeTurf(); else if (P5.flipEast) P5.flipEast(); } catch(e){}
          try {
            var o=document.getElementById('wquest');
            if (o) { o._qgen=(o._qgen|0)+1; o.className=''; o.style.visibility='hidden'; o.dataset.k=''; o.dataset.done='1'; }
          } catch(eQ){}
          try { if (root.FFF_C2LMAP && FFF_C2LMAP.openAll) FFF_C2LMAP.openAll({ focus:'masa' }); } catch(e2){ return {err:String(e2)}; }
          var T=root.FFF_C2TURF, M=root.FFF_C2LMAP;
          return {
            col: M&&M.ownerCol&&M.ownerCol('masa'),
            x4: T&&T.B&&T.B.X4&&T.B.X4.g,
            map: !!document.getElementById('c2citymap'),
            rlen: T&&T.Q&&T.Q.R&&T.Q.R.length,
            pin: M&&M.pinLab&&M.pinLab('masa'),
            chip: M&&M.chipLab&&M.chipLab('masa'),
            gChip: M&&M.chipLab&&M.chipLab('goda'),
            banner: (function(){ var q=document.getElementById('wquest'); return q&&q.style.visibility!=='hidden'?q.textContent.slice(0,80):''; })()
          };
        })()""")
        print('map', mmap, flush=True)
        await pg.wait_for_timeout(800)
        try:
            await pg.wait_for_function("() => { var b=document.querySelector('#c2citymap.on .c2cm-board img'); return b && b.complete && b.naturalWidth>0; }", timeout=4000)
        except Exception as e:
            print('map wait', e, flush=True)
        await pg.wait_for_timeout(400)
        await shot(pg, '21_map_after_masa', hush=False)
        await ev(pg, """(function(){ try { if (root.FFF_C2LMAP && FFF_C2LMAP.hide) FFF_C2LMAP.hide(); } catch(e){} var box=document.getElementById('c2citymap'); if(box&&box.parentNode)box.parentNode.removeChild(box); return 1; })()""")

        # yard meeting during the talk, Masa behind the desk
        await ev(pg, """(function(){
          var P5=root.FFF_S2P5, st=c2S();
          st.e.seal_depot=0; st.e.masaFate=''; st.e.down_dep=0; st.e.eastSeal=0;
          P5.setStg('open'); st.q.cq2_s2_depot=0;
          return P5.stg();
        })()""")
        info = await go_room(pg, 'dyard', 530, 790)
        print('yard talk setup', info, flush=True)
        await ev(pg, """(function(){
          try { if (W.ryo) { W.ryo.x=500; W.ryo.y=800; place(W.ryo,0); } if (W.aoi) { W.aoi.x=600; W.aoi.y=810; place(W.aoi,0); } camera(true); } catch(e){}
          try { W.dlg=false; W.cut=false; W.busy=false; if (root.FFF_S2P5 && FFF_S2P5.yardTalk) FFF_S2P5.yardTalk(); } catch(e2){}
          var m=W.c2n&&W.c2n.s2masa;
          return { masa:m&&[m.x,m.y], dlg:!!W.dlg };
        })()""")
        await pg.wait_for_timeout(500)
        await shot(pg, '01_yard_gate_talk', hush=False)

        print('ERRS', errs[:8], flush=True)
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
