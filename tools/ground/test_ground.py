#!/workspace/pwenv/bin/python3
"""v6564-ground regression: every battle stage has a ground value, and each foe's feet fall inside that stage's floor band.
Run: /workspace/pwenv/bin/python3 tools/ground/test_ground.py [index.html]
Geometry is measured in a real 390x844 battle: the lowest opaque row of the foe canvas (#eFig) in screen px.
FLOOR = screen y (390x844) where the stage's floor starts, read off the painting (painted Ch2 rooms: H0 330/1280 * 0.659 = 217; others by eye).
A foot is ok when FLOOR - TOL <= foot <= FLOOR + DEPTH. A stage with no FLOOR entry fails: add it when you add a backdrop.
"""
import asyncio, functools, http.server, os, socketserver, sys, threading, json
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
INDEX = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent.parent / 'index.html'
PORT = int(os.environ.get('PORT', '8957'))
TOL, DEPTH = 3, 90
H = 'c2_hustler'; P = 'c2_punk'; S = 'c2_suit'; B = 'c2_boso'
# stage -> (floor top, [foe groups that really fight there])
FLOOR = {
  # Ch1 photo rooms (unchanged since v6.5.20; default foot or bt-feet-lo)
  '1': (125, [['bully1']]), 'lib_hall': (135, [['bully1'], ['bully2']]), 'lib_archive': (125, [['mb_lib']]), 'art_studio': (140, [['paint']]),
  'art_stage': (135, [['mb_art'], ['drum']]), 'cafe_line': (150, [['bully3']]), 'cafe_dining': (150, [['mb_cafe']]), 'store_bay': (150, [['bully4']]),
  'store_track': (120, [['mb_field']]), 'gym_side': (165, [['bully2']]), 'gym_arena': (150, [['gouki']]), 'gekko_cafe': (150, [[H, H, H]]),
  # Ch2 painted rooms (c2_gym = ch2-fixes GGD-25 boxing ring: its canvas starts just inside the far ropes, ~140)
  'c2_sento_hall': (217, [[S], [B], [P], [H], [P, S, B]]), 'c2_sento_boiler': (217, [['mb2_sento']]), 'c2_sento_kitchen': (217, [[H, H]]),
  'c2_sento_trophy': (217, [[H, 'c2_doorman']]), 'c2_hotel_door': (217, [[H, H, S], [S, S]]), 'c2_west_wall': (217, [[P, P, P], [P, P]]),
  'c2_udon': (217, [['chinpira1'], [P, P]]), 'c2_lantern_alley': (217, [['enforcer'], [H, H], ['c2_boss']]),
  'c2_street': (213, [[P, P, P], [S, S], [B, B], [H, H, H], ['c2_doorman', H, H]]), 'c2_club': (217, [['bouncer'], ['chinpira1'], [S, S]]),
  'c2_gym': (140, [['aoi'], ['ryo']]), 'c2_depot': (217, [['mb2_depot']]), 'c2_arcade': (217, [['mb2_arcade'], ['mb2_game']]),
  'c2_waga': (217, [[B, B, B]]), 'c2_br': (214, [[B, B]]), 'c2_se': (214, [[B, B]]), 'c2_lk': (195, [['nq_kaji', B]]), 'c2_qy': (203, [['nq_kaji', B]]),
  'c2_gg': (210, [['nq_sada', B, B]]), 'c2_ap': (212, [['nq_sada', B, B]]), 'c2_sh': (212, [['mb2_depot', B, B]]),
  # Jin's turf rooms (v6564-jin, registered by FFF_S2P6.hookBattle when that branch is merged)
  'c2_j6ramen': (217, [[S, S]]), 'c2_j6karaV': (217, [[S]]), 'c2_j6hhall': (217, [[S, S]]), 'c2_j6hdeal': (217, [[S]]),
  'c2_j6ckoff': (217, [['chinpira1']]), 'c2_j6gcback': (217, [['mb2_game']]),
}
RES = []
def ok(name, cond, extra=''):
    RES.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + ((' :: ' + str(extra)[:300]) if (extra and not cond) else ''), flush=True)

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True; daemon_threads = True

REG = """()=>{var C=ENGINE.chars();
 C.enforcer=Object.assign({},C.c2_hustler,{name:'Ban Shigure',story:1,art:'enforcer_fig',fig:'enforcer_fig',dbl:2,dblSp:40});
 ['nq_kaji','nq_sada'].forEach(function(id){ if(!C[id]) C[id]=Object.assign({},C.c2_boso,{name:id,story:1,fig:id+'_fig',art:id+'_fig',alt:id+'_fig'}); if(!C[id+'g']) C[id+'g']=C[id]; });
 try{ if(window.FFF_S2P6&&FFF_S2P6.hookBattle) FFF_S2P6.hookBattle(); }catch(e){} return 1}"""
START = """([foes,room,ctx])=>{window.FFF_BTROOM=function(){return room};
 FFF_UI.startMatch('ryo',{foes:foes,hp:0,boss:false,drop:0,partner:'Aoi',esc:null,ctx:ctx||{dg:'c2'},bench:{ch:'aoi',pst:{hp:46,spirit:40,sig2:null,disc:0,cmax:3,combo:true},path:'balanced'},pst:{combo:true,hp:46,spirit:40,sig2:null,disc:0,cmax:3}})}"""
FOOT = """()=>{var cv=document.getElementById('eFig'),r=cv.getBoundingClientRect(),g=cv.getContext('2d'),w=cv.width,h=cv.height,d=g.getImageData(0,0,w,h).data,lo=-1,hi=-1;
 for(var y=0;y<h;y++){for(var x=0;x<w;x++){if(d[(y*w+x)*4+3]>40){if(hi<0)hi=y;lo=y;break}}}
 var cx=r.left+r.width/2;return {top:r.top+hi*r.height/h,foot:r.top+(lo+1)*r.height/h,cx:cx}}"""

async def main():
    srv = TS(('127.0.0.1', PORT), functools.partial(Q, directory=str(INDEX.parent)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    src = INDEX.read_text(encoding='utf-8')
    ok('feetPx has a default ground line for painted rooms', 'var GROUND_DEF' in src and 'GROUND[id] != null ? GROUND[id] : GROUND_DEF' in src)
    errs = []
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--disable-dev-shm-usage'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(3500)
        await pg.touchscreen.tap(195, 420); await pg.wait_for_timeout(700)
        await pg.evaluate(REG)
        keys = await pg.evaluate("Object.keys(FFF_C2BT.KEY)")
        for k in keys:   # every registered painted stage must have a ground value and a floor band
            f = await pg.evaluate("(k)=>FFF_C2BT.feetPx(k)", k)
            ok(f'stage {k} has a ground value > 0', f and f > 0, f)
            ok(f'stage {k} has a floor band in this test (add it with the backdrop)', k in FLOOR)
        for k, (top, groups) in FLOOR.items():
            if k.startswith('c2_') and k not in keys: print('skip (not registered here):', k); continue
            for g in groups:
                try:
                    await pg.evaluate("window.FFF_NO_TUT=1")
                    await pg.evaluate(START, [g, k, ({'dg': 'c2'} if k.startswith('c2_') or k == 'gekko_cafe' else None)]); await pg.wait_for_timeout(2600)
                    m = await pg.evaluate(FOOT)
                    nm = f'{k} foes={"+".join(g)} foot={m["foot"]:.0f} floor>={top}'
                    ok(nm + ' inside band', top - TOL <= m['foot'] <= top + DEPTH, m)
                    ok(f'{k} foes={"+".join(g)} centred', abs(m['cx'] - 195) < 6, m)
                except Exception as e:
                    ok(f'{k} foes={"+".join(g)} ran', False, str(e)[:200])
                await pg.evaluate("()=>{try{FFF_UI.quit&&FFF_UI.quit()}catch(e){}}")
        ok('no page errors', not errs, errs)
        await b.close()
    n = len(RES); f = RES.count(False)
    print(f'\n{n - f}/{n} passed'); sys.exit(1 if f else 0)

asyncio.run(main())
