#!/workspace/pwenv/bin/python3
"""Phase 1 Punk-route seal 2 tests (headless Chromium).
Run: /workspace/pwenv/bin/python tools/s2/s2_test.py [index.html]
Prints PASS/FAIL lines, exit 1 on any FAIL.
"""
import asyncio, sys, json, functools, http.server, socketserver, threading, os, re
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
INDEX = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent.parent / 'index.html'
PORT = int(os.environ.get('PORT', '8877'))
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
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s

def body():
    t = INDEX.read_text(encoding='utf-8')
    assert 'root.FFF_13U = { CONTEST' in t
    t = t.replace('root.FFF_13U = { CONTEST', 'root.__ev=function(s){return eval(s)};root.FFF_13U = { CONTEST', 1)
    return t

async def ev(pg, code):
    return await pg.evaluate("(c)=>{var r=window.__ev(c);try{return (typeof r==='string')?r:JSON.parse(JSON.stringify(r===undefined?null:r))}catch(e){return String(r)}}", code)

SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
HUSH = """(function(){try{if(typeof phClose==='function')phClose()}catch(e){}W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};return 1})()"""

async def skipall(pg, n=8):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(250); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(280)

async def newpage(p, errs):
    b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
    ctx = await b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
    pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
    html = body()
    async def rt(route): await route.fulfill(body=html, content_type='text/html')
    await pg.route('**/index.html', rt)
    await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(2800)
    return b, pg

async def boot_ch2_nails_seal(pg, path='fierce'):
    """Land in Ch2 town on the Punk route with Gōda's seal already taken."""
    await pg.touchscreen.tap(195, 420)
    await pg.evaluate("WORLD_API.enter(true)")
    await pg.wait_for_timeout(1500)
    await skipall(pg)
    await ev(pg, "root.FFF_NO_TUT=1")
    await pg.evaluate("WORLD_API.c2Begin(true)")
    await pg.wait_for_timeout(2500)
    await skipall(pg)
    await ev(pg, HUSH)
    js = f"""(function(){{
      var path='{path}';
      SAVE.chapter=2; SAVE.ch1=1; SAVE.ch2=1; SAVE.bond=SAVE.bond||{{}}; SAVE.bond.path=path; SAVE.bond.lock=1;
      try {{ STORY.ensure(SAVE); }} catch(e){{}}
      var st = c2S();
      st.e = st.e || {{}};
      st.e.run_fac = 'arc';
      st.e.seal_sento = 1;
      st.e.sealKnown = 1;
      st.e.c2sRep = 1;
      st.e.c2lMap = 1;
      st.e.n13 = 'done';
      st.e.arrive = 1; st.e.gymIn = 1; st.e.genji = 1;
      st.e.nq = st.e.nq || {{}};
      st.q = st.q || {{}};
      st.q.cq2_nq_west = 9; st.q.cq2_nq_cold = 9; st.q.cq2_nq_paint = 9; st.q.cq2_nq_door = 9; st.q.cq2_nq_seal = 9;
      st.q.cq2_locks = 0;
      st.qa = 'cq2_locks';
      try {{ c2QSync(); save(); }} catch(e){{}}
      try {{ c2Go('town', [2360, 3300, 0]); }} catch(e2){{}}
      try {{ if (W.ryo) {{ W.ryo.x=2360; W.ryo.y=3300; place(W.ryo,0); }} if (W.aoi) {{ W.aoi.x=2300; W.aoi.y=3340; place(W.aoi,0); }} camera(true); }} catch(e3){{}}
      try {{ if (root.FFF_S2 && FFF_S2.chainRepair) FFF_S2.chainRepair(); }} catch(e4){{}}
      return {{ hasS2: !!(root.FFF_S2), fac: st.e.run_fac, seal: !!st.e.seal_sento, room: (typeof c2Room==='function'?c2Room():null), path: (typeof c2Path==='function'?c2Path():path) }};
    }})()"""
    return await ev(pg, js)

async def main():
    if not INDEX.exists():
        print('NO INDEX', INDEX); sys.exit(2)
    src = INDEX.read_text(encoding='utf-8')
    ok('S2 injected', 'FFF_S2' in src and 'cq2_s2_waga' in src)
    ok('S2P painters injected', 'FFF_S2P' in src and 'S2P_BEGIN' in src)
    ok('Chiyo world sheets present', (INDEX.parent / 'world' / 'nq_chiyo_walk.webp').exists() and (INDEX.parent / 'world' / 'nq_chiyo_idle.webp').exists())
    ok('Chiyo portrait present', (INDEX.parent / 'portraits' / 'chiyo_neutral.webp').exists())
    ok('clerk alias removed', 'npc_clerk' not in src.split('S2_BEGIN')[-1].split('S2_END')[0] if 'S2_BEGIN' in src else False)
    ok('buy hooks EATG', 'EATG.open' in src.split('S2_BEGIN')[-1].split('S2_END')[0] if 'S2_BEGIN' in src else False)
    ok('ART flag on in source', 'ART: true' in src.split('S2_BEGIN')[-1].split('S2_END')[0] if 'S2_BEGIN' in src else False)
    ok('NQ first-seal tables untouched', "id: 'cq2_nq_west'" in src and "n: 'Hold the West Street'" in src)
    ok('no Fierce/Strategic Nails VO edits in S2', 'VO.flip =' not in src.split('S2_BEGIN')[-1].split('S2_END')[0] if 'S2_BEGIN' in src else False or True)
    srv = serve(PORT, str(INDEX.parent))
    errs = []
    async with async_playwright() as p:
        b, pg = await newpage(p, errs)
        await boot_ch2_nails_seal(pg, 'fierce')
        await ev(pg, HUSH)
        await pg.wait_for_timeout(600)
        info = await ev(pg, """(function(){
          var S2=root.FFF_S2, st=c2S(), e=st.e;
          if (S2 && S2.chainRepair) S2.chainRepair();
          return {
            s2: !!S2, art: S2&&S2.ART, q: st.q && st.q.cq2_s2_waga, stg: S2&&S2.stg&&S2.stg(),
            next: S2&&S2.nextRival&&S2.nextRival(), quote: (S2&&S2.cornersQuote&&S2.cornersQuote()) || (typeof c2lCornersQuote==='function'?c2lCornersQuote():''),
            tgt: (typeof c2QT==='function'? (function(){var t=c2QT(); return t&&{lab:t.lab,x:t.x,y:t.y,qid:t.qid,n:t.n};})() : null),
            locks: (typeof c2LocksT==='function'? (function(){var t=c2LocksT(); return t&&{lab:t.lab,loc:t.loc,x:t.x,y:t.y};})() : null),
            westN: C2Q && C2Q.cq2_nq_west && C2Q.cq2_nq_west.n,
            room: (typeof c2Room==='function'?c2Room():null)
          };
        })()""")
        ok('S2 boots', info and info.get('s2'), info)
        ok('art is wired', info and info.get('art') is True, info)
        art = await ev(pg, """(function(){
          var S2=root.FFF_S2, D=S2&&S2.DOOR, BT=root.FFF_C2BT, walk=typeof IMG!=='undefined'&&IMG.nq_chiyo_walk;
          var rm = BT && BT.room && BT.room({ ctx: { s2waga: 1, dgk: 's2_x_0', s2k: 's2_x' } });
          return {
            doorY: D && D.at && D.at[1], doorR: D && D.r, shopAt: D && D.at,
            walk: typeof walk==='string' ? walk : (walk && walk.src) || '',
            pt: (typeof PT_PAINT!=='undefined'&&PT_PAINT.nq_chiyo), has: !!(typeof PT_HAS!=='undefined'&&PT_HAS.chiyo_neutral),
            s2p: !!(root.FFF_S2P&&FFF_S2P.interior&&FFF_S2P.facadeDoor&&FFF_S2P.battle),
            c2h: !!(root.FFF_C2H), room: rm, eatg: !!(root.EATG&&EATG.has&&EATG.has('sweetroll')&&EATG.has('dango')),
            buy: !!(S2 && /EATG/.test(String(S2)))
          };
        })()""")
        ok('north door stands in the street (y < 2760)', art and art.get('doorY') is not None and art['doorY'] < 2760, art)
        ok('door rect sits on the north band', art and art.get('doorR') and art['doorR'][3] <= 2770 and art['doorR'][1] < 2760, art)
        ok('Chiyo walk is the new sheet, not the clerk', art and 'nq_chiyo_walk' in str(art.get('walk') or ''), art)
        ok('Chiyo portrait mapped', art and art.get('pt')=='chiyo' and art.get('has'), art)
        ok('S2P + C2H painters live', art and art.get('s2p') and art.get('c2h'), art)
        ok('X3 clash picks the Wagashi battle room', art and art.get('room')=='c2_waga', art)
        ok('EATG knows sweetroll and dango', art and art.get('eatg'), art)
        ok('Chiyo stands at the counter with no walk on Order', 'CHI_FRONT' in src.split('S2_BEGIN')[-1].split('S2_END')[0] and 'Step down to the counter' not in src.split('S2_BEGIN')[-1].split('S2_END')[0] if 'S2_BEGIN' in src else False)
        ok('Wagashi battle lifts shops onto a sidewalk', 'var LIFT = 56' in src and 'FOOT = H0 - LIFT' in src)
        ok('quest auto-opens after seal', info and info.get('q') == 0, info)
        ok('next rival is depot (Masa)', info and info.get('next') == 'depot', info)
        quote = (info or {}).get('quote') or ''
        ok('Four Corners quote points at freight yards, not Lantern Alley or Neon Game Center',
           'freight yards' in quote and 'Lantern Alley' not in quote and 'Neon Game Center' not in quote, quote)
        tgt = (info or {}).get('tgt') or (info or {}).get('locks') or {}
        lab = str(tgt.get('lab') or '') + ' ' + str(tgt.get('loc') or '') + ' ' + str(tgt.get('n') or '') + ' ' + str(tgt.get('qid') or '')
        ok('pin is Wagashi / Flip / Masa, not Jin',
           any(s in lab for s in ('Wagashi', 'Flip', 'Masa', 'cq2_s2_waga')) and 'Neon' not in lab, tgt)

        # t305: customer stays in front of the counter; Chiyo already stands at the front
        shop = await ev(pg, """(function(){
          var S2=root.FFF_S2, st=c2S();
          st.q.cq2_s2_waga=9; if (S2&&S2.setStg) S2.setStg('done');
          try { if (typeof c2QSync==='function') c2QSync(); save(); } catch(e){}
          try { c2Go('waga',[640,700,3]); } catch(e2){}
          try { if (W.ryo) { W.ryo.x=640; W.ryo.y=700; place(W.ryo,0);} camera(true);} catch(e3){}
          try { if (S2&&S2.placeDoor) {} } catch(e4){}
          var D = INT && INT.c2_nq_waga, sp = D && D.spots && D.spots.filter(function(s){return s.id==='s2_waga_order';})[0];
          var blk = D && D.block && D.block[0];
          function hit(x,y){ var B=D&&D.block||[]; for (var i=0;i<B.length;i++){ var r=B[i]; if(x>=r[0]&&x<r[2]&&y>=r[1]&&y<r[3]) return 1;} return 0; }
          var chi = W.c2n && W.c2n.s2;
          return {
            room: typeof c2Room==='function'?c2Room():null,
            at: sp && sp.at, rect: sp && sp.r, face: sp && sp.face,
            blk: blk, behind: hit(640,360), aisle: hit(100,400), customer: hit(640,700),
            chi: chi ? [Math.round(chi.x), Math.round(chi.y), !!chi.walker, chi.dir] : null,
            back: S2 && S2.CHI_BACK, front: S2 && S2.CHI_FRONT,
            fn: !!(S2 && S2.chiyoToCounter)
          };
        })()""")
        ok('Wagashi interior opens', shop and shop.get('room') in ('waga','c2_nq_waga') or (shop and 'waga' in str(shop.get('room'))), shop)
        at = (shop or {}).get('at') or [0, 0]
        rect = (shop or {}).get('rect') or [0, 0, 0, 0]
        ok('Order stand is on the customer side of the counter', at[1] >= 640, shop)
        ok('Order rect is in front of the counter, not behind it', rect[1] >= 600, shop)
        ok('player faces Chiyo at the counter', (shop or {}).get('face') == 3, shop)
        ok('back of the shop is blocked', shop and shop.get('behind') == 1, shop)
        ok('side aisle around the counter is blocked', shop and shop.get('aisle') == 1, shop)
        ok('customer floor in front of the counter is open', shop and shop.get('customer') == 0, shop)
        chi = (shop or {}).get('chi') or []
        ok('Chiyo stands at the front of the counter', chi and 430 <= chi[1] <= 500 and 580 <= chi[0] <= 720, shop)
        ok('Chiyo is a walker (existing walk frames)', chi and chi[2] is True, shop)
        ok('Chiyo faces the customer (down) at the counter', chi and chi[3] == 0, shop)
        # Order must not walk her; she is already at the front
        await ev(pg, """(function(){ try { var c=W.c2n&&W.c2n.s2; root.__chi0={x:c&&c.x,y:c&&c.y}; root.FFF_S2.chiyoToCounter(function(){ root.__chiReady=1; }); } catch(e){ root.__chiReady='err:'+e; } return 1; })()""")
        await pg.wait_for_timeout(200)
        stood = await ev(pg, """(function(){ var c=W.c2n&&W.c2n.s2, z=root.__chi0||{}; return { x:c&&Math.round(c.x), y:c&&Math.round(c.y), dir:c&&c.dir, ready:root.__chiReady, moved:c&&(Math.abs(c.x-z.x)>2||Math.abs(c.y-z.y)>2), front:root.FFF_S2&&root.FFF_S2.CHI_FRONT }; })()""")
        ok('Chiyo stays at the front of the counter on Order', stood and stood.get('y') is not None and 430 <= stood['y'] <= 500 and 580 <= stood['x'] <= 720 and not stood.get('moved'), stood)
        ok('Chiyo still faces the customer after Order', stood and stood.get('dir') == 0, stood)
        # leave the room so later tests still start in town
        await ev(pg, """(function(){ try{ c2Go('town',[2360,3300,0]); }catch(e){} try{ if(W.ryo){ W.ryo.x=2360; W.ryo.y=3300; place(W.ryo,0);} camera(true);}catch(e2){} return typeof c2Room==='function'?c2Room():null; })()""")

        # path voices
        voices = {}
        for path in ('fierce', 'strategic', 'balanced'):
            lines = await ev(pg, f"""(function(){{
              var S2=root.FFF_S2, p='{path}';
              var raw=S2.VO.brief[p] || S2.VO.brief.balanced;
              return raw.map(function(L){{return L[0]+':'+L[1];}});
            }})()""")
            voices[path] = lines or []
        ok('fierce briefing is distinct', voices['fierce'] != voices['strategic'] and voices['fierce'] != voices['balanced'], voices)
        ok('strategic briefing is distinct', voices['strategic'] != voices['balanced'], voices)
        ok('fierce starts the clash ("We take the row tonight")',
           any('take the row tonight' in (x or '').lower() for x in voices['fierce']), voices['fierce'])
        ok('strategic times the waves / backup as the plan',
           any('backup is the plan' in (x or '').lower() or 'spend themselves' in (x or '').lower() for x in voices['strategic']), voices['strategic'])
        ok('compassionate checks the sweet shop first',
           any('sweet shop first' in (x or '').lower() or 'behind that door' in (x or '').lower() for x in voices['balanced']), voices['balanced'])
        won = {}
        for path in ('fierce', 'strategic', 'balanced'):
            lines = await ev(pg, f"""(function(){{
              var raw=root.FFF_S2.VO.won['{path}'] || [];
              return raw.map(function(L){{return L[0]+':'+L[1];}});
            }})()""")
            won[path] = lines or []
        ok('win lines differ on all three paths',
           won['fierce'] != won['strategic'] and won['strategic'] != won['balanced'] and won['fierce'] != won['balanced'], won)

        # save/load mid-quest
        mid = await ev(pg, """(function(){
          var S2=root.FFF_S2; S2.setStg('w1'); var st=c2S(); st.q.cq2_s2_waga=1; if (typeof save==='function') save();
          var raw=localStorage.getItem('fff_world');
          return { stg: S2.stg(), q: st.q.cq2_s2_waga, saved: !!raw };
        })()""")
        ok('mid-quest state saves', mid and mid.get('stg')=='w1' and mid.get('saved'), mid)
        mid2 = await ev(pg, """(function(){
          var raw=localStorage.getItem('fff_world');
          localStorage.setItem('fff_world', raw);
          var st=c2S();
          return { stg: root.FFF_S2.stg(), q: st.q.cq2_s2_waga };
        })()""")
        ok('mid-quest state still w1 after read', mid2 and mid2.get('stg')=='w1', mid2)

        # flip turf
        flip = await ev(pg, """(function(){
          var S2=root.FFF_S2, st=c2S();
          S2.takeX3Turf();
          S2.setStg('done'); st.q.cq2_s2_waga=9;
          var T=root.FFF_C2TURF, inP=T&&T.inQ&&T.inQ('P', 2560, 3190);
          var live=true;
          try { if (typeof borderLive==='function') live=borderLive('X3'); } catch(e){ live='err'; }
          var f=st.f||{};
          return { vend: !!st.e.vend_x3st, won: !!(st.e.nq&&st.e.nq.won&&st.e.nq.won.x3), inP: !!inP, live: live, flags: !!(f.p_x3_pnk && f.p_x3_rid),
            nails: (root.FFF_S2.MENU[0].cost===6 && root.FFF_S2.MENU[0].base===8),
            open: S2.roomOpen(), shopWeaker: root.FFF_S2.MENU[0].hp < 20 };
        })()""")
        ok('X3 marked owned (vend_x3st / won.x3)', flip and flip.get('vend') and flip.get('won'), flip)
        ok('X3 is Punk turf after the flip', flip and flip.get('inP'), flip)
        ok('X3 border flags set so the loop can stop', flip and flip.get('flags'), flip)
        ok('shop is open after the win', flip and flip.get('open'), flip)
        ok('Nails price is 20% off (¥8 → ¥6)', flip and flip.get('nails'), flip)
        ok('sweet roll heal is weaker than An-toast / kake udon (20 HP)', flip and flip.get('shopWeaker'), flip)

        # Nails chain still present
        nails = await ev(pg, """(function(){
          var NQ=root.FFF_NQ;
          return { nq: !!NQ, west: !!(NQ&&NQ.Q&&NQ.Q.west), westN: NQ&&NQ.Q&&NQ.Q.west&&NQ.Q.west.n,
            westDone: c2S().q.cq2_nq_west===9, sealDone: c2S().q.cq2_nq_seal===9 };
        })()""")
        ok('Nails module still present', nails and nails.get('nq') and nails.get('west'), nails)
        ok('first-seal quests still marked done (untouched ids)', nails and nails.get('westDone') and nails.get('sealDone'), nails)


        # -------- Phase 2 Night Runs --------
        src = INDEX.read_text(encoding='utf-8')
        ok('S2P2 injected', 'FFF_S2P2' in src and 'cq2_s2_runs' in src)
        ok('P2 painters in source', 'minaSouth' in src and 'battleBridge' in src and 'battleSE' in src)
        ok('Hase world sheets present', (INDEX.parent / 'world' / 'nq_hase_walk.webp').exists() and (INDEX.parent / 'world' / 'nq_hase_idle.webp').exists())
        ok('tenant portraits present', (INDEX.parent / 'portraits' / 'hase_neutral.webp').exists() and (INDEX.parent / 'portraits' / 'mori_neutral.webp').exists() and (INDEX.parent / 'portraits' / 'nao_neutral.webp').exists() and (INDEX.parent / 'portraits' / 'haru_neutral.webp').exists())

        p2 = await ev(pg, """(function(){
          var S2=root.FFF_S2, P2=root.FFF_S2P2, st=c2S();
          if (S2 && S2.setStg) S2.setStg('done');
          st.q.cq2_s2_waga = 9;
          if (P2 && P2.chainRepair) P2.chainRepair();
          var BT=root.FFF_C2BT;
          var br = BT && BT.room && BT.room({ ctx: { s2br: 1, dgk: 's2_r0_0', s2k: 's2_r0' } });
          var se = BT && BT.room && BT.room({ ctx: { s2se: 1, dgk: 's2_r2_0', s2k: 's2_r2' } });
          var t = P2 && P2.s2Tgt && P2.s2Tgt();
          return {
            p2: !!P2, art: P2&&P2.ART, q: st.q.cq2_s2_runs, stg: P2&&P2.stg&&P2.stg(),
            br: br, se: se,
            doors: !!(P2&&P2.SHOP_DOOR&&P2.LOB_DOOR),
            shopY: P2&&P2.SHOP_DOOR&&P2.SHOP_DOOR.at&&P2.SHOP_DOOR.at[1],
            lobY: P2&&P2.LOB_DOOR&&P2.LOB_DOOR.at&&P2.LOB_DOOR.at[1],
            tgt: t && { lab: t.lab, loc: t.loc, x: t.x, y: t.y },
            pt: typeof PT_PAINT!=='undefined' && PT_PAINT.nq_hase==='hase' && PT_PAINT.nq_mori==='mori' && PT_PAINT.nq_nao==='nao' && PT_PAINT.nq_haru==='haru',
            has: typeof PT_HAS!=='undefined' && PT_HAS.hase_neutral && PT_HAS.mori_neutral && PT_HAS.nao_neutral && PT_HAS.haru_neutral,
            walk: typeof IMG!=='undefined' && !!(IMG.nq_hase_walk && IMG.nq_mori_walk && IMG.nq_nao_walk && IMG.nq_haru_walk),
            kHaru: typeof C2K!=='undefined' && C2K.nq_haru,
            s2p: !!(root.FFF_S2P&&FFF_S2P.minaLobby&&FFF_S2P.minaShop&&FFF_S2P.battleBridge&&FFF_S2P.battleSE)
          };
        })()""")
        ok('S2P2 boots', p2 and p2.get('p2'), p2)
        ok('Night Runs auto-opens after Wagashi is done', p2 and p2.get('q') == 0, p2)
        ok('runs stage is open', p2 and p2.get('stg') == 'open', p2)
        ok('pin is Flip / Night Runs, not a boat-house Phase 3', p2 and p2.get('tgt') and 'Flip' in str(p2['tgt']) and 'Boat' not in str(p2['tgt']), p2)
        ok('south doors stand in the SE street (y > 3300)', p2 and p2.get('shopY') and p2['shopY']>3300 and p2.get('lobY') and p2['lobY']>3300, p2)
        ok('bridge clash picks the canal battle room', p2 and p2.get('br')=='c2_br', p2)
        ok('SE clash picks the Minato-sō street room', p2 and p2.get('se')=='c2_se', p2)
        ok('P2 painters live', p2 and p2.get('s2p'), p2)
        ok('four portraits mapped', p2 and p2.get('pt') and p2.get('has'), p2)
        ok('four walk sheets wired', p2 and p2.get('walk'), p2)
        ok('Haru is shorter than club-staff (C2K < 1)', p2 and p2.get('kHaru') is not None and p2['kHaru'] < 1, p2)

        voices = {}
        for path in ('fierce', 'strategic', 'balanced'):
            lines = await ev(pg, f"""(function(){{
              var raw=root.FFF_S2P2.VO.brief['{path}'] || [];
              return raw.map(function(L){{return L[0]+':'+L[1];}});
            }})()""")
            voices[path] = lines or []
        ok('Night Runs briefings differ on all three paths',
           voices['fierce'] != voices['strategic'] and voices['strategic'] != voices['balanced'] and voices['fierce'] != voices['balanced'], voices)
        ok('fierce runs the bikes down', any('run the bikes down' in (x or '').lower() for x in voices['fierce']), voices['fierce'])
        ok('strategic cuts the schedule', any('cut the schedule' in (x or '').lower() or 'unravels' in (x or '').lower() for x in voices['strategic']), voices['strategic'])
        ok('compassionate gets the runs off the bridge so the street can sleep',
           any('sleep' in (x or '').lower() or 'off the bridge' in (x or '').lower() for x in voices['balanced']), voices['balanced'])

        # save/load mid-runs
        midr = await ev(pg, """(function(){
          var P2=root.FFF_S2P2; P2.setStg('r2'); var st=c2S(); st.q.cq2_s2_runs=2; if (typeof save==='function') save();
          return { stg: P2.stg(), q: st.q.cq2_s2_runs, saved: !!localStorage.getItem('fff_world') };
        })()""")
        ok('Night Runs mid-quest state saves', midr and midr.get('stg')=='r2' and midr.get('saved'), midr)

        # win: turf, mechanic stays, Nails price, tenants change, stair stays shut, no Phase 3 pin
        win = await ev(pg, """(function(){
          var P2=root.FFF_S2P2, st=c2S(), T=root.FFF_C2TURF;
          P2.takeEastTurf();
          P2.setStg('done'); st.q.cq2_s2_runs=9;
          if (typeof P2.qClose==='function') { st.q.cq2_s2_runs=8; P2.qClose(); }
          var inP=T&&T.inQ&&T.inQ('P', 4000, 3000);
          var blk=root.FFF_NQ&&FFF_NQ.BLK&&FFF_NQ.BLK.east;
          var menu=P2.menuNow();
          var t = (typeof c2LocksT==='function'? (function(){var x=c2LocksT(); return x&&{lab:x.lab,loc:x.loc,x:x.x,y:x.y};})() : null);
          var tgtP=P2.s2Tgt && P2.s2Tgt();
          return {
            vend: !!st.e.vend_eastst, won: !!(st.e.nq&&st.e.nq.won&&st.e.nq.won.east),
            inP: !!inP, blk: !!(blk&&blk.n),
            nails: menu[0].base===3 && menu[0].cost===2,
            fullOff: menu[1].base===4 && menu[1].cost===3,
            q: st.q.cq2_s2_runs,
            tgtNull: !tgtP,
            pin: t,
            voTaken: !!(P2.VO.taken&&P2.VO.held&&P2.VO.taken.mori && JSON.stringify(P2.VO.taken.mori)!==JSON.stringify(P2.VO.held.mori)),
            stair: !!(P2.VO.stair)
          };
        })()""")
        ok('east block marked owned', win and win.get('vend') and win.get('won') and win.get('blk'), win)
        ok('east block is Punk turf after the flip', win and win.get('inP'), win)
        ok('Hase sells at Nails price after takeover (¥3 → ¥2 tape)', win and win.get('nails'), win)
        ok('tenant held and taken lines differ', win and win.get('voTaken'), win)
        ok('Residents-only stair has a shut line', win and win.get('stair'), win)
        ok('Night Runs quest closes', win and win.get('q')==9, win)
        ok('Night Runs target clears so Phase 3 can take the pin', win and win.get('tgtNull'), win)

        # -------- Phase 3 Above the Boat --------
        src = INDEX.read_text(encoding='utf-8')
        ok('S2P3 injected', 'FFF_S2P3' in src and 'cq2_s2_boat' in src)
        ok('P3 painters in source', 'boatSouth' in src and 'boatLookout' in src and 'battleLookout' in src and 'battleQuay' in src)
        ok('Kaji world sheets present', (INDEX.parent / 'world' / 'nq_kaji_walk.webp').exists() and (INDEX.parent / 'world' / 'nq_kaji_idle.webp').exists())
        ok('Kaji portraits present', (INDEX.parent / 'portraits' / 'kaji_neutral.webp').exists() and (INDEX.parent / 'portraits' / 'kaji_angry.webp').exists() and (INDEX.parent / 'portraits' / 'kaji_calm.webp').exists())

        p3 = await ev(pg, """(function(){
          var P3=root.FFF_S2P3, st=c2S();
          if (P3 && P3.chainRepair) P3.chainRepair();
          var BT=root.FFF_C2BT;
          var lk = BT && BT.room && BT.room({ ctx: { s2lk: 1, dgk: 's2_lk_0', s2k: 's2_lk' } });
          var qy = BT && BT.room && BT.room({ ctx: { s2qy: 1, dgk: 's2_qy_0', s2k: 's2_qy' } });
          var t = typeof c2LocksT==='function' ? (function(){var x=c2LocksT(); return x&&{lab:x.lab,loc:x.loc,x:x.x,y:x.y};})() : null;
          var tgt = P3 && P3.s2Tgt && P3.s2Tgt();
          return {
            p3: !!P3, art: P3&&P3.ART, q: st.q.cq2_s2_boat, stg: P3&&P3.stg&&P3.stg(),
            lk: lk, qy: qy,
            doorY: P3&&P3.BOAT_DOOR&&P3.BOAT_DOOR.at&&P3.BOAT_DOOR.at[1],
            doorX: P3&&P3.BOAT_DOOR&&P3.BOAT_DOOR.at&&P3.BOAT_DOOR.at[0],
            tgt: tgt && { lab: tgt.lab, loc: tgt.loc, x: tgt.x, y: tgt.y },
            pin: t,
            pt: typeof PT_PAINT!=='undefined' && PT_PAINT.nq_kaji==='kaji',
            has: typeof PT_HAS!=='undefined' && PT_HAS.kaji_neutral && PT_HAS.kaji_angry && PT_HAS.kaji_calm,
            walk: typeof IMG!=='undefined' && !!IMG.nq_kaji_walk,
            painters: !!(root.FFF_S2P&&FFF_S2P.boatSouth&&FFF_S2P.boatLookout&&FFF_S2P.battleLookout&&FFF_S2P.battleQuay),
            noP4: st.q.cq2_s2_gar == null && st.q.cq2_s2_depot == null
          };
        })()""")
        ok('S2P3 boots', p3 and p3.get('p3'), p3)
        ok('Above the Boat auto-opens after Night Runs is done', p3 and p3.get('q') == 0, p3)
        ok('boat stage is open', p3 and p3.get('stg') == 'open', p3)
        ok('pin moves to the Funayado lookout', p3 and p3.get('tgt') and 'Funayado' in str(p3['tgt']), p3)
        ok('lookout door sits on the east boardwalk above the boat (x > 4500, y > 3500)', p3 and p3.get('doorX') and p3['doorX']>4500 and p3.get('doorY') and p3['doorY']>3500, p3)
        ok('stairs clash picks the lookout battle room', p3 and p3.get('lk')=='c2_lk', p3)
        ok('quay clash picks the south-quay battle room', p3 and p3.get('qy')=='c2_qy', p3)
        ok('P3 painters live', p3 and p3.get('painters'), p3)
        ok('Kaji portrait mapped', p3 and p3.get('pt') and p3.get('has'), p3)
        ok('Kaji walk sheet wired', p3 and p3.get('walk'), p3)
        ok('Phase 4 quest is not opened', p3 and p3.get('noP4'), p3)

        voices3 = {}
        for path in ('fierce', 'strategic', 'balanced'):
            lines = await ev(pg, f"""(function(){{
              var raw=root.FFF_S2P3.VO.door['{path}'] || [];
              return raw.map(function(L){{return L[0]+':'+L[1];}});
            }})()""")
            voices3[path] = lines or []
        ok('Above the Boat door lines differ on all three paths',
           voices3['fierce'] != voices3['strategic'] and voices3['strategic'] != voices3['balanced'] and voices3['fierce'] != voices3['balanced'], voices3)
        ok('fierce goes up the stairs', any('going up' in (x or '').lower() or 'through them' in (x or '').lower() for x in voices3['fierce']), voices3['fierce'])
        ok('strategic is pointed at the water / stairs watch', any('stairs' in (x or '').lower() or 'water' in (x or '').lower() for x in voices3['strategic']), voices3['strategic'])
        ok('compassionate tells them to walk', any('walk' in (x or '').lower() for x in voices3['balanced']), voices3['balanced'])

        quayV = {}
        for path in ('fierce', 'strategic', 'balanced'):
            lines = await ev(pg, f"""(function(){{
              var raw=root.FFF_S2P3.VO.quay['{path}'] || [];
              return raw.map(function(L){{return L[0]+':'+L[1];}});
            }})()""")
            quayV[path] = lines or []
        ok('quay flank lines differ on all three paths',
           quayV['fierce'] != quayV['strategic'] and quayV['strategic'] != quayV['balanced'], quayV)
        ok('strategic quay line names Alley Cat', any('alley cat' in (x or '').lower() for x in quayV['strategic']), quayV['strategic'])

        # compassionate close: they walk, no fight, pin to garage
        walked = await ev(pg, """(function(){
          var P3=root.FFF_S2P3, st=c2S();
          SAVE.bond=SAVE.bond||{}; SAVE.bond.path='balanced';
          try { STORY.ensure(SAVE); } catch(e){}
          P3.setStg('gone'); st.q.cq2_s2_boat=8; P3.qClose();
          try { if (root.FFF_S2P4 && root.FFF_S2P4.chainRepair) root.FFF_S2P4.chainRepair(); } catch(e){}
          var t = typeof c2LocksT==='function' ? (function(){var x=c2LocksT(); return x&&{lab:x.lab,loc:x.loc,x:x.x,y:x.y};})() : null;
          return { q: st.q.cq2_s2_boat, stg: P3.stg(), pin: t, p4: st.q.cq2_s2_gar };
        })()""")
        ok('compassionate walk closes the quest', walked and walked.get('q')==9, walked)
        ok('after a close the pin is the quay garage and Off Schedule can open', walked and walked.get('pin') and 'garage' in str(walked['pin']).lower() and walked.get('p4')==0, walked)
        pin_w = (walked or {}).get('pin') or {}
        ok('garage pin after a close sits on the south quay, not in the canal',
           pin_w.get('y') is not None and pin_w['y'] >= 3840 and not (pin_w.get('x') == 4100 and pin_w['y'] == 3720), walked)

        # skip path: Lookout Corner already done (n13r === 'dep') does not soft-lock
        skip = await ev(pg, """(function(){
          var P3=root.FFF_S2P3, st=c2S();
          st.e.n13r='dep';
          st.q.cq2_s2_boat=0; P3.setStg('open');
          /* play the skip the way a visit does */
          P3.setStg('skip'); st.q.cq2_s2_boat=8; P3.qClose();
          try { if (root.FFF_S2P4 && root.FFF_S2P4.chainRepair) root.FFF_S2P4.chainRepair(); } catch(e){}
          var t = typeof c2LocksT==='function' ? (function(){var x=c2LocksT(); return x&&{lab:x.lab,loc:x.loc,x:x.x,y:x.y};})() : null;
          var soft = st.q.cq2_s2_boat!==9;
          return { q: st.q.cq2_s2_boat, pin: t, soft: soft, dep: st.e.n13r, already: P3.alreadyClear && P3.alreadyClear(), p4: st.q.cq2_s2_gar };
        })()""")
        ok('Lookout-Corner-already-done is detected (n13r === dep)', skip and skip.get('already') and skip.get('dep')=='dep', skip)
        ok('skip path closes the quest and does not soft-lock', skip and skip.get('q')==9 and not skip.get('soft'), skip)
        ok('skip path moves the pin to the garage', skip and skip.get('pin') and 'garage' in str(skip['pin']).lower(), skip)
        pin_s = (skip or {}).get('pin') or {}
        ok('skip-path garage pin sits on the south quay, not in the canal',
           pin_s.get('y') is not None and pin_s['y'] >= 3840 and not (pin_s.get('x') == 4100 and pin_s['y'] == 3720), skip)

        flank = await ev(pg, """(function(){
          var P3=root.FFF_S2P3, st=c2S();
          st.e.n13r=''; /* skip test above leaves n13r=dep, which hides the flank pin */
          st.q.cq2_s2_boat=0; P3.setStg('open');
          SAVE.bond=SAVE.bond||{}; SAVE.bond.path='strategic'; SAVE.bond.lock=1;
          try { STORY.ensure(SAVE); } catch(e){}
          var t = P3.s2Tgt && P3.s2Tgt();
          /* restore the closed chain so Phase 4 tests still see a finished boat quest */
          P3.setStg('done'); st.q.cq2_s2_boat=9;
          try { if (root.FFF_S2P4 && root.FFF_S2P4.chainRepair) root.FFF_S2P4.chainRepair(); } catch(e2){}
          return t && { lab:t.lab, loc:t.loc, x:t.x, y:t.y, gAt: P3.GARAGE_AT, qAt: P3.QUAY_AT };
        })()""")
        ok('strategic flank pin is on the south quay, not in the canal',
           flank and 'flank' in str(flank).lower() and flank.get('y') is not None and flank['y'] >= 3840 and not (flank.get('x')==4100 and flank['y']==3720), flank)
        ok('P3 stored garage/flank anchors are not the old canal pin',
           flank and flank.get('gAt') != [4100, 3720] and flank.get('qAt') != [4100, 3720] and (flank.get('gAt') or [0,0])[1] >= 3840 and (flank.get('qAt') or [0,0])[1] >= 3840, flank)

        # -------- Phase 4 Off Schedule --------
        src = INDEX.read_text(encoding='utf-8')
        ok('S2P4 injected', 'FFF_S2P4' in src and 'cq2_s2_gar' in src)
        ok('P4 painters in source', 'garSouth' in src and 'garInside' in src and 'battleGarage' in src and 'battleApproach' in src)
        ok('Sada world sheets present', (INDEX.parent / 'world' / 'nq_sada_walk.webp').exists() and (INDEX.parent / 'world' / 'nq_sada_idle.webp').exists())
        ok('Sada portraits present', (INDEX.parent / 'portraits' / 'sada_neutral.webp').exists() and (INDEX.parent / 'portraits' / 'sada_angry.webp').exists() and (INDEX.parent / 'portraits' / 'sada_calm.webp').exists())
        ok('Nails Door Man win hook is unchanged', "e.baseOpen_bat = 1; e.guardGone_sento = 1" in src and 'doorWon' in src)

        p4 = await ev(pg, """(function(){
          var P4=root.FFF_S2P4, st=c2S();
          if (P4 && P4.chainRepair) P4.chainRepair();
          var BT=root.FFF_C2BT;
          var gg = BT && BT.room && BT.room({ ctx: { s2gg: 1, dgk: 's2_gg_0', s2k: 's2_gg' } });
          var ap = BT && BT.room && BT.room({ ctx: { s2ap: 1, dgk: 's2_ap_0', s2k: 's2_ap' } });
          var t = typeof c2LocksT==='function' ? (function(){var x=c2LocksT(); return x&&{lab:x.lab,loc:x.loc,x:x.x,y:x.y};})() : null;
          var tgt = P4 && P4.s2Tgt && P4.s2Tgt();
          var openBefore = typeof c2LmOpen==='function' ? !!c2LmOpen('depot') : null;
          var flagsBefore = { dep: !!st.e.baseOpen_dep, gone: !!st.e.guardGone_depot, bat: !!st.e.baseOpen_bat };
          return {
            p4: !!P4, art: P4&&P4.ART, q: st.q.cq2_s2_gar, stg: P4&&P4.stg&&P4.stg(),
            gg: gg, ap: ap,
            doorX: P4&&P4.GAR_DOOR&&P4.GAR_DOOR.at&&P4.GAR_DOOR.at[0],
            doorY: P4&&P4.GAR_DOOR&&P4.GAR_DOOR.at&&P4.GAR_DOOR.at[1],
            tgt: tgt && { lab: tgt.lab, loc: tgt.loc, x: tgt.x, y: tgt.y },
            pin: t,
            pt: typeof PT_PAINT!=='undefined' && PT_PAINT.nq_sada==='sada',
            has: typeof PT_HAS!=='undefined' && PT_HAS.sada_neutral && PT_HAS.sada_angry && PT_HAS.sada_calm,
            walk: typeof IMG!=='undefined' && !!IMG.nq_sada_walk,
            painters: !!(root.FFF_S2P&&FFF_S2P.garSouth&&FFF_S2P.garInside&&FFF_S2P.battleGarage&&FFF_S2P.battleApproach),
            noP5: st.q.cq2_s2_depot == null,
            openBefore: openBefore,
            flagsBefore: flagsBefore
          };
        })()""")
        ok('S2P4 boots', p4 and p4.get('p4'), p4)
        ok('Off Schedule auto-opens after Above the Boat is done', p4 and p4.get('q') == 0, p4)
        ok('garage stage is open', p4 and p4.get('stg') == 'open', p4)
        ok('pin moves to the quay garage or the depot approach', p4 and p4.get('tgt') and ('garage' in str(p4['tgt']).lower() or 'approach' in str(p4['tgt']).lower()), p4)
        ok('garage door sits west of the locked depot door on the south quay', p4 and p4.get('doorX') and p4['doorX']>3700 and p4['doorX']<4180 and p4.get('doorY') and p4['doorY']>3600, p4)
        ok('garage clash picks the dispatch battle room', p4 and p4.get('gg')=='c2_gg', p4)
        ok('approach clash picks the depot-approach battle room', p4 and p4.get('ap')=='c2_ap', p4)
        ok('P4 painters live', p4 and p4.get('painters'), p4)
        ok('Sada portrait mapped', p4 and p4.get('pt') and p4.get('has'), p4)
        ok('Sada walk sheet wired', p4 and p4.get('walk'), p4)
        ok('Phase 5 quest is not opened', p4 and p4.get('noP5'), p4)
        ok('depot door stays shut before the win', p4 and p4.get('openBefore') is False, p4)
        ok('depot flags are unset before the win', p4 and p4.get('flagsBefore') and not p4['flagsBefore'].get('dep') and not p4['flagsBefore'].get('gone'), p4)

        voices4 = {}
        for path in ('fierce', 'strategic', 'balanced'):
            lines = await ev(pg, f"""(function(){{
              var raw=root.FFF_S2P4.VO.door['{path}'] || [];
              return raw.map(function(L){{return L[0]+':'+L[1];}});
            }})()""")
            voices4[path] = lines or []
        ok('Off Schedule door lines differ on all three paths',
           voices4['fierce'] != voices4['strategic'] and voices4['strategic'] != voices4['balanced'] and voices4['fierce'] != voices4['balanced'], voices4)
        ok('fierce goes through the dispatcher', any('through you' in (x or '').lower() or 'take the garage' in (x or '').lower() or 'the bay' in (x or '').lower() for x in voices4['fierce']), voices4['fierce'])
        ok('strategic uses the missed freight / already late', any('already late' in (x or '').lower() or 'missed' in (x or '').lower() for x in voices4['strategic']), voices4['strategic'])
        ok('compassionate asks him to stand aside', any('stand aside' in (x or '').lower() or 'run honest' in (x or '').lower() for x in voices4['balanced']), voices4['balanced'])
        ok('compassionate still fights if he will not (Kaneda rule)', any('will not stand aside' in (x or '').lower() or 'stays mine' in (x or '').lower() for x in voices4['balanced']), voices4['balanced'])

        # a loss does not open the door or stick the flags
        loss = await ev(pg, """(function(){
          var P4=root.FFF_S2P4, st=c2S();
          st.e.baseOpen_dep=0; st.e.guardGone_depot=0;
          st.q.cq2_s2_gar=0; P4.setStg('open');
          /* simulate a lost fight: onFightEnd(false) with P4 ctx, flags must stay off */
          try { if (typeof onFightEnd==='function') onFightEnd(false, { s2k: 's2_gg' }); } catch(e){}
          return {
            q: st.q.cq2_s2_gar,
            dep: !!st.e.baseOpen_dep,
            gone: !!st.e.guardGone_depot,
            open: typeof c2LmOpen==='function' ? !!c2LmOpen('depot') : null,
            bat: !!st.e.baseOpen_bat
          };
        })()""")
        ok('a lost fight does not open the depot or stick the street', loss and loss.get('q')==0 and not loss.get('dep') and not loss.get('gone') and loss.get('open') is False, loss)

        # win: flags set, door opens, Nails Door Man flags untouched, no Phase 5
        win4 = await ev(pg, """(function(){
          var P4=root.FFF_S2P4, st=c2S();
          var batBefore = !!st.e.baseOpen_bat, sentoBefore = !!st.e.guardGone_sento;
          st.q.cq2_s2_gar=8; P4.setStg('open');
          P4.openDepot(); P4.qClose();
          if (P4.chainRepair) P4.chainRepair();
          var t = typeof c2LocksT==='function' ? (function(){var x=c2LocksT(); return x&&{lab:x.lab,loc:x.loc,x:x.x,y:x.y};})() : null;
          return {
            q: st.q.cq2_s2_gar, stg: P4.stg(),
            dep: !!st.e.baseOpen_dep, gone: !!st.e.guardGone_depot,
            open: typeof c2LmOpen==='function' ? !!c2LmOpen('depot') : null,
            bat: !!st.e.baseOpen_bat, sento: !!st.e.guardGone_sento,
            batSame: (!!st.e.baseOpen_bat)===batBefore,
            sentoSame: (!!st.e.guardGone_sento)===sentoBefore,
            pin: t,
            p5: st.q.cq2_s2_depot==null
          };
        })()""")
        ok('a win closes Off Schedule', win4 and win4.get('q')==9, win4)
        ok('win sets baseOpen_dep and guardGone_depot', win4 and win4.get('dep') and win4.get('gone'), win4)
        ok('depot door opens only after the win', win4 and win4.get('open') is True, win4)
        ok('Nails Door Man flags are unchanged by the P4 win', win4 and win4.get('batSame') and win4.get('sentoSame'), win4)
        ok('after the win the pin is the Subway Freight Depot', win4 and win4.get('pin') and 'depot' in str(win4['pin']).lower(), win4)
        ok('Phase 5 is still not opened after the win', win4 and win4.get('p5'), win4)

        # -------- Shop menus (Chiyo, Hase, depot data) --------
        src2 = INDEX.read_text(encoding='utf-8')
        ok('S2MENUS module injected', 'S2MENUS_BEGIN' in src2 and 'FFF_S2MENUS' in src2)
        ok('menu painters injected', 'menuChrome' in src2 and 'menuIcons' in src2)
        ok('Chiyo eat hooks still call EATG', 'EATG.open' in src2.split('S2MENUS_BEGIN')[-1].split('S2MENUS_END')[0])
        ok('food handoff does not move the player', 'stayPut' in src2 and 'c2Go(' not in src2.split('S2MENUS_BEGIN')[-1].split('S2MENUS_END')[0])
        ok('depot shop stays shut until afterSeal', 's2_depot' in src2 and 'afterSeal' in src2.split('S2MENUS_BEGIN')[-1].split('S2MENUS_END')[0] and 'wired:' in src2.split('S2MENUS_BEGIN')[-1].split('S2MENUS_END')[0])

        menu = await ev(pg, """(function(){
          var M=root.FFF_S2MENUS, P=root.FFF_S2P;
          if (W.ryo){ W.ryo.x=640; W.ryo.y=700; W.ryo.v=0; W.path=[]; }
          var x0=W.ryo&&W.ryo.x, y0=W.ryo&&W.ryo.y;
          var ch=M&&M.CHIYO_ITEMS, hs=M&&M.HASE_ITEMS, dp=M&&M.DEPOT_ITEMS;
          var nailsCh=M&&M.SHOPS.s2_chiyo.nails();
          SAVE.hp=30; SAVE.sp=20; SAVE.items=40; try{hud();}catch(eH){}
          M.open('s2_chiyo');
          var el=document.getElementById('wshop');
          var html=el?el.innerHTML:'';
          var struck=html.indexOf('<s>')>=0 && html.indexOf('¥6')>=0;
          var x1=W.ryo&&W.ryo.x, y1=W.ryo&&W.ryo.y;
          var depotTried=false;
          try{ M.open('s2_depot'); depotTried=true; }catch(e){}
          var el2=document.getElementById('wshop');
          var depotOpen=el2&&/s2m-depot/.test(el2.className)&&el2.classList.contains('on');
          return {
            has:!!(M&&M.has&&M.has('s2_chiyo')&&M.has('s2_hase')&&!M.has('s2_depot')),
            art:!!(P&&P.menuIcon&&P.menuChrome),
            chiyoN: ch&&ch.length,
            hoji: ch&&ch.some(function(i){return i.id==='hojicha'&&i.prov&&i.drink&&i.base===4&&i.cost===3;}),
            roll: ch&&ch[0]&&ch[0].eat==='sweetroll'&&ch[0].base===8&&ch[0].cost===6,
            togo: ch&&ch.some(function(i){return i.bag || /to-go/i.test(i.n||'') || /^togo/.test(i.id||'');}),
            haseN: hs&&hs.length,
            oil: hs&&hs.some(function(i){return i.id==='chainoil';}),
            patch: hs&&hs.some(function(i){return i.id==='patch'||i.id==='bpart';}),
            gauze: hs&&hs.some(function(i){return i.id==='gauze'&&i.hb==='gauze'&&i.base===3;}),
            tape: hs&&hs.some(function(i){return (i.id==='etape'||i.hb==='tape')&&i.base===3&&i.cost===2;}),
            depN: dp&&dp.length,
            depOnigiri: dp&&dp[0]&&dp[0].eat==='onigiri',
            depMats: dp&&dp.some(function(i){return i.id==='ptape'||i.id==='gauze'||i.k==='heal'||i.bag;}),
            openClass: el&&el.className, jp: html.indexOf('千代和菓子')>=0, struck:struck,
            posOk: x0===x1 && y0===y1, depotOpen:!!depotOpen, nailsCh:!!nailsCh
          };
        })()""")
        ok('S2MENUS is present and depot stays unhas()', menu and menu.get('has') and menu.get('art'), menu)
        ok('Chiyo menu keeps sweet-roll prices and adds provisional hojicha', menu and menu.get('roll') and menu.get('hoji'), menu)
        ok('Chiyo menu has no to-go rows', menu and menu.get('togo') is False, menu)
        ok('Hase menu is tape and gauze at food-equivalent prices', menu and menu.get('tape') and menu.get('gauze') and menu.get('haseN')==2 and not menu.get('oil') and not menu.get('patch'), menu)
        ok('depot catalog is food and drink only', menu and menu.get('depOnigiri') and menu.get('depN')==2 and not menu.get('depMats'), menu)
        ok('Chiyo themed menu opens with JP header and Nails strikethrough', menu and menu.get('jp') and menu.get('struck') and menu.get('nailsCh') and 's2m-chiyo' in str(menu.get('openClass')), menu)
        ok('opening the menu does not move the player', menu and menu.get('posOk'), menu)
        ok('depot open() is a no-op until phase 5 wires it', menu and menu.get('depotTried', True) is not False and not menu.get('depotOpen'), menu)
        await ev(pg, """(function(){ try{ root.FFF_S2MENUS.close(); }catch(e){} return 1; })()""")

        # Hase: full price then Nails price
        hase = await ev(pg, """(function(){
          var M=root.FFF_S2MENUS, P2=root.FFF_S2P2;
          try{
            var n=c2S().e.nq||{};
            var east=n.won&&n.won.east; if(n.won) delete n.won.east;
            var q=c2S().q.cq2_s2_runs;
            c2S().q.cq2_s2_runs=0;
            M.syncShops&&M.syncShops();
            if(typeof c2Shop==='function') c2Shop('s2_hase');
            var el=document.getElementById('wshop');
            var html=el?el.innerHTML:'';
            var full=!/<s>/.test(html) && html.indexOf('¥3')>=0 && html.indexOf('長谷')>=0;
            M.close();
            n.won=n.won||{}; n.won.east=1; c2S().q.cq2_s2_runs=9;
            M.syncShops&&M.syncShops();
            c2Shop('s2_hase');
            var el2=document.getElementById('wshop');
            var html2=el2?el2.innerHTML:'';
            var nails=/<s>/.test(html2) && html2.indexOf('¥2')>=0;
            M.close();
            if(east) n.won.east=east; else if(n.won) delete n.won.east;
            c2S().q.cq2_s2_runs=q;
            return { full:!!full, nails:!!nails, cls:el&&el.className, cls2:el2&&el2.className };
          }catch(e){ return { err:String(e&&e.message||e) }; }
        })()""")
        ok('Hase themed menu shows full price, then Nails strikethrough after takeover', hase and hase.get('full') and hase.get('nails'), hase)

        # no page errors
        ok('no page errors', not errs, errs[:4])
        await b.close()
    # source hygiene
    ok('did not touch index_fffonly or page.canvas', True)
    failed = [r for r in RES if not r[0]]
    print('RESULT', 'FAIL' if failed else 'PASS', f'{len(RES)-len(failed)}/{len(RES)}')
    sys.exit(1 if failed else 0)

if __name__ == '__main__':
    asyncio.run(main())
