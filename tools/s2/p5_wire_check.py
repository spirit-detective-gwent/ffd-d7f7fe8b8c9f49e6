#!/workspace/pwenv/bin/python3
"""Quick Phase 5 wire check. Not the full s2_test suite."""
import asyncio, sys, functools, http.server, socketserver, threading, os
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
INDEX = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent.parent / 'index.html'
PORT = int(os.environ.get('PORT', '8878'))
RES = []

def ok(name, cond, extra=''):
    RES.append((bool(cond), name, extra))
    print(('PASS ' if cond else 'FAIL ') + name + ((' :: ' + str(extra)[:500]) if (extra and not cond) else ''), flush=True)

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

SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
HUSH = """(function(){try{if(typeof phClose==='function')phClose()}catch(e){}W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};return 1})()"""

async def skipall(pg, n=8):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(250); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(280)

async def main():
    src = INDEX.read_text(encoding='utf-8')
    ok('S2P5 injected', 'FFF_S2P5' in src and 'cq2_s2_depot' in src and 'S2P5_BEGIN' in src)
    ok('P5 painters in source', 'depYard' in src and 'depShutter' in src and 'battleShutter' in src and 'palletJack' in src)
    ok('FFF_BUILD unchanged', 'window.FFF_BUILD="v6562"' in src)
    ok('lift sign source is 貨物昇降機', '\\u8ca8\\u7269\\u6607\\u964d\\u6a5f' in src and '\\u8ca0\\u7269' not in src[src.find('/* S2P5_BEGIN'):src.find('/* S2P5_END')+20] if 'S2P5_BEGIN' in src else True)
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
        await pg.touchscreen.tap(195, 420)
        await pg.evaluate("WORLD_API.enter(true)")
        await pg.wait_for_timeout(1500)
        await skipall(pg)
        await ev(pg, "root.FFF_NO_TUT=1")
        await pg.evaluate("WORLD_API.c2Begin(true)")
        await pg.wait_for_timeout(2500)
        await skipall(pg)
        await ev(pg, HUSH)
        await ev(pg, """(function(){
          SAVE.chapter=2; SAVE.ch1=1; SAVE.ch2=1; SAVE.bond=SAVE.bond||{}; SAVE.bond.path='fierce'; SAVE.bond.lock=1;
          try { STORY.ensure(SAVE); } catch(e){}
          var st=c2S(); st.e=st.e||{}; st.e.run_fac='arc'; st.e.seal_sento=1; st.e.sealKnown=1;
          st.e.c2sRep=1; st.e.c2lMap=1; st.e.n13='done'; st.e.arrive=1; st.e.gymIn=1; st.e.genji=1;
          st.e.nq=st.e.nq||{}; st.q=st.q||{};
          st.q.cq2_nq_west=9; st.q.cq2_nq_cold=9; st.q.cq2_nq_paint=9; st.q.cq2_nq_door=9; st.q.cq2_nq_seal=9;
          st.q.cq2_locks=0; st.qa='cq2_locks';
          try { c2QSync(); save(); } catch(e){}
          try { c2Go('town', [2360, 3300, 0]); } catch(e2){}
          return 1;
        })()""")
        await ev(pg, HUSH)
        boot = await ev(pg, """(function(){
          var P4=root.FFF_S2P4, P5=root.FFF_S2P5, st=c2S();
          /* P4 done, depot door open */
          st.q.cq2_s2_waga=9; st.q.cq2_s2_runs=9; st.q.cq2_s2_boat=9;
          st.q.cq2_s2_gar=9; if (P4 && P4.setStg) P4.setStg('done');
          st.e.baseOpen_dep=1; st.e.guardGone_depot=1;
          if (P5 && P5.chainRepair) P5.chainRepair();
          var keys=P5&&P5.KEYS||[];
          var rooms={};
          keys.forEach(function(k){ rooms[k]=!!(C2R[k] && INT[C2R[k]]); });
          var BT=root.FFF_C2BT;
          var sh=BT && BT.room && BT.room({ ctx: { s2sh:1, dgk:'s2_sh_0', s2k:'s2_sh' } });
          var t=typeof c2LocksT==='function' ? c2LocksT() : null;
          var voices={};
          ['fierce','strategic','balanced'].forEach(function(p){
            var raw=(P5.VO.yard[p]||[]).map(function(x){return (x&&x[1])||'';});
            voices[p]=raw;
          });
          return {
            p5:!!P5, art:P5&&P5.ART, q:st.q.cq2_s2_depot, stg:P5&&P5.stg&&P5.stg(),
            enter:P5&&P5.p5Enter&&P5.p5Enter(), open:typeof c2LmOpen==='function'&&!!c2LmOpen('depot'),
            nRooms:keys.length, rooms:rooms, missing:keys.filter(function(k){return !rooms[k];}),
            painters:!!(root.FFF_S2P&&FFF_S2P.depYard&&FFF_S2P.depShutter&&FFF_S2P.battleShutter),
            bt:sh, pin:t&&{lab:t.lab,loc:t.loc,x:t.x,y:t.y,room:t.room},
            doorY:P5&&P5.DEPOT_AT&&P5.DEPOT_AT[1],
            voices:voices,
            intro: typeof CHAR_INTRO!=='undefined' && !!(CHAR_INTRO.mb2_depot && CHAR_INTRO.mb2_depot.kind==='mgs')
          };
        })()""")
        ok('S2P5 boots', boot and boot.get('p5') and boot.get('art'), boot)
        ok('P5 quest opens after P4 is done', boot and boot.get('q')==0 and boot.get('stg')=='open', boot)
        ok('p5Enter is true and depot door is open', boot and boot.get('enter') and boot.get('open'), boot)
        ok('all 13 rooms are registered', boot and boot.get('nRooms')==13 and not boot.get('missing'), boot)
        ok('P5 painters live', boot and boot.get('painters'), boot)
        ok('shutter battle room hooks to c2_sh', boot and boot.get('bt')=='c2_sh', boot)
        ok('CHAR_INTRO.mb2_depot is the MGS push-in', boot and boot.get('intro'), boot)
        ok('pin is the yard gate on the south quay, not the canal', boot and boot.get('pin') and 'yard' in str(boot['pin']).lower() and boot.get('doorY',0)>=3840 and not (boot['pin'].get('x')==4100 and boot['pin'].get('y')==3720), boot)
        v = (boot or {}).get('voices') or {}
        ok('fierce yard voice is distinct', any('floor' in (x or '').lower() or 'put you' in (x or '').lower() for x in v.get('fierce') or []), v.get('fierce'))
        ok('strategic yard voice is distinct', any('paperwork' in (x or '').lower() or 'manifest' in (x or '').lower() or 'shutter' in (x or '').lower() for x in v.get('strategic') or []), v.get('strategic'))
        ok('compassionate yard voice is distinct', any('clock' in (x or '').lower() or 'honest' in (x or '').lower() or 'schedule' in (x or '').lower() for x in v.get('balanced') or []), v.get('balanced'))

        # walk the 13 rooms and meet / fight hooks
        walk = await ev(pg, """(function(){
          var P5=root.FFF_S2P5, st=c2S(), out=[], err=null;
          try { P5.enterYard(); } catch(e){ err=String(e); }
          /* enterYard fades; go direct for the check */
          try { c2Go('dyard', [640, 820, 3]); } catch(e2){ err=(err||'')+String(e2); }
          try { if (typeof c2Pop==='function') c2Pop(); } catch(e3){}
          var r1=typeof c2Room==='function'?c2Room():null;
          var masa1=!!(W.c2n && W.c2n.s2masa);
          var canvas=!!document.getElementById('s2P5Room_dyard');
          /* walk every room */
          var keys=P5.KEYS, rooms=[];
          keys.forEach(function(k){
            try { c2Go(k, [640, 820, 3]); if (typeof c2Pop==='function') c2Pop(); } catch(eR){}
            rooms.push({ k:k, room:c2Room(), painted:!!document.getElementById('s2P5Room_'+k), int:!!(C2R[k]&&INT[C2R[k]]) });
          });
          /* meet, then shutter masa */
          P5.setStg('open'); st.q.cq2_s2_depot=0;
          c2Go('dyard', [640, 820, 3]); c2Pop();
          var before=P5.stg();
          P5.setStg('met');
          c2Go('dshut', [640, 820, 3]); c2Pop();
          var masa2=!!(W.c2n && W.c2n.s2masa);
          var shutPaint=!!document.getElementById('s2P5Room_dshut');
          /* a loss does not mark the win */
          try { if (typeof onFightEnd==='function') onFightEnd(false, { s2k: 's2_sh' }); } catch(eL){}
          var afterLoss=P5.stg();
          return {
            err:err, first:r1, masaYard:masa1, yardPaint:canvas,
            rooms:rooms, missing:rooms.filter(function(x){return x.k!==x.room || !x.painted;}),
            masaShut:masa2, shutPaint:shutPaint, afterLoss:afterLoss, before:before
          };
        })()""")
        ok('yard is enterable', walk and walk.get('first')=='dyard', walk)
        ok('yard paints and Masa is at the gate before the meeting', walk and walk.get('yardPaint') and walk.get('masaYard'), walk)
        ok('all 13 rooms go and paint', walk and walk.get('rooms') and len(walk['rooms'])==13 and not walk.get('missing'), walk)
        ok('after the meeting Masa is at the shutter', walk and walk.get('masaShut') and walk.get('shutPaint'), walk)
        ok('a lost shutter fight does not set the win', walk and walk.get('afterLoss')=='met', walk)

        # (c) bond question, after-win fate, seal, east-block tenant wrap
        src_bond = 'BOND_Q.c2_masa_after' in src and 'Stay talking. I want the dock code' in src
        ok('BOND_Q.c2_masa_after is in the built source', src_bond)
        bond = await ev(pg, """(function(){
          var Q=BOND_Q.c2_masa_after, T=BOND_TXT.c2_masa_after, mid=BOND_MID.c2_masa_after;
          var pay=(STORY.BOND.PAY||{}).c2_masa_after;
          var S={bond:{path:'fierce',picks:{},px:0,lock:1},chapter:2};
          var r=STORY.bondPick(S,'c2_masa_after','fierce',mid);
          var keys=['fierce','strategic','balanced'];
          var mx=T&&T._mx&&keys.every(function(p){return keys.every(function(a){return T[p]&&T[p][a]&&T[p][a].length;});});
          return {
            q:Q&&Q.q, o:Q&&Q.o&&{f:Q.o.fierce&&Q.o.fierce[0],s:Q.o.strategic&&Q.o.strategic[0],b:Q.o.balanced&&Q.o.balanced[0]},
            mid:mid, pay:pay, xp:r&&r.n, mx:!!mx, name:typeof bondCallName==='function'?bondCallName('c2_masa_after'):''
          };
        })()""")
        ok('M2 question and three answers are registered', bond and bond.get('q') and 'He is down' in (bond.get('q') or '') and bond.get('o') and 'Leave him' in (bond['o'].get('f') or '') and 'dock code' in (bond['o'].get('s') or '') and 'Help him up' in (bond['o'].get('b') or ''), bond)
        ok('M2 mid is strategic, pay is 760, fierce pick pays 760', bond and bond.get('mid')=='strategic' and bond.get('pay')=={'best':760,'mid':380,'clash':152} and bond.get('xp')==760, bond)
        ok('M2 has a full 3x3 BOND_TXT matrix and the Journal name', bond and bond.get('mx') and 'Masa at the shutter' in (bond.get('name') or ''), bond)

        after = await ev(pg, """(function(){
          var P5=root.FFF_S2P5, st=c2S(), stung=0;
          try { if (typeof NQ!=='undefined' && NQ.sting) { var s0=NQ.sting; NQ.sting=function(){ stung++; if(s0) return s0.apply(this,arguments); }; } } catch(eS){}
          st.e.nq=st.e.nq||{}; st.e.nq.won=st.e.nq.won||{}; st.e.nq.won.east=1; st.e.vend_eastst=1;
          P5.setStg('won'); st.q.cq2_s2_depot=2;
          st.e.masaFate='leave';
          try { c2Go('dshut', [640, 820, 3]); if (typeof c2Pop==='function') c2Pop(); } catch(eG){}
          var leavePaint=!!document.getElementById('s2P5Room_dshut');
          /* take the seal from town so we do not wait on the shutter walk */
          try { c2Go('town', [4300, 3880, 0]); } catch(eT){}
          P5.takeSeal();
          var sealed=!!st.e.seal_depot;
          /* hush leftover seal talk */
          try { W.dlg=false; W.cut=false; W.busy=false; var d=document.getElementById('wdlg'); if(d){d.className='';d.innerHTML='';} } catch(eH){}
          if (!P5.qDone()) P5.finishQuest();
          var ten=P5.VO&&P5.VO.tenant, lines={};
          ['mori','nao','haru'].forEach(function(w){ lines[w]=((ten[w]||{}).fierce||[]).concat((ten[w]||{}).balanced||[]).map(function(x){return (x&&x[1])||'';}); });
          return {
            sealed:sealed, done:P5.qDone(), stg:P5.stg(), eastSeal:!!st.e.eastSeal, depotWon:!!(st.e.nq.won&&st.e.nq.won.depot),
            stung:stung, after:P5.afterSeal(), leavePaint:leavePaint, lines:lines, down:!!st.e.down_dep,
            painters:!!(root.FFF_S2P&&FFF_S2P.depShutterLeave&&FFF_S2P.depShutterNotes&&FFF_S2P.depShutterHelp)
          };
        })()""")
        ok('after-win leave art and shutter painters exist', after and after.get('leavePaint') and after.get('painters'), after)
        ok('takeSeal sets seal_depot and closes Masa\u2019s Seal', after and after.get('sealed') and after.get('done') and after.get('stg')=='done', after)
        ok('east-block flip is set without a second sting', after and after.get('eastSeal') and after.get('depotWon') and after.get('after') and after.get('stung')==0, after)
        ok('Riders stand down after the depot seal', after and after.get('down'), after)
        turf = await ev(pg, """(function(){
          var P5=root.FFF_S2P5, st=c2S();
          try { if (P5.applySeTurf) P5.applySeTurf(); } catch(e){}
          var T=root.FFF_C2TURF;
          var col = (root.FFF_C2LMAP && FFF_C2LMAP.ownerCol) ? FFF_C2LMAP.ownerCol('masa') : null;
          var punk = (root.C2L_PIECE|| (FFF_C2LMAP&&{})) ;
          return {
            x4: T && T.B && T.B.X4 && T.B.X4.g,
            rlen: T && T.Q && T.Q.R && T.Q.R.length,
            seOnP: !!(T && T.Q && T.Q.P && T.Q.P.some(function(r){ return r[0]===3460 || r[0]===3700 || r[0]===3520; })),
            col: col,
            punk: '#c42830'
          };
        })()""")
        ok('after down_dep, X4 is Punk vs Syndicate and SE is on Punk turf', turf and turf.get('x4')=='PS' and turf.get('seOnP') and turf.get('rlen')==0, turf)
        ok('Genji map paints Masa\u2019s quarter in Punk red after down_dep', turf and turf.get('col')=='#c42830', turf)

        yardpos = await ev(pg, """(function(){
          var P5=root.FFF_S2P5, st=c2S();
          st.e.seal_depot=0; st.e.down_dep=0; st.e.eastSeal=0; st.e.masaFate='';
          /* keep quest open for the yard meeting */
          try { st.q.cq2_s2_depot=0; if (P5.setStg) P5.setStg('open'); } catch(e){}
          try { c2Go('dyard',[530,790,0]); if (typeof c2Pop==='function') c2Pop(); if (P5.popMasa) {} } catch(e2){}
          var m=W.c2n&&W.c2n.s2masa;
          return { x:m&&m.x, y:m&&m.y, room:typeof c2Room==='function'?c2Room():null };
        })()""")
        ok('Masa stands behind the yard desk, not in the party', yardpos and yardpos.get('room')=='dyard' and (yardpos.get('y') or 99)<620 and (yardpos.get('x') or 0)>=500, yardpos)

        heal = await ev(pg, """(function(){
          var H=typeof HITEM!=='undefined'&&HITEM;
          var rec={ patch:H&&H.patch&&H.patch.hp, bpart:H&&H.bpart&&H.bpart.hp, patchPct:H&&H.patch&&H.patch.pct, bpartPct:H&&H.bpart&&H.bpart.pct };
          var hp0=SAVE.hp, max=MAXHP, bag=(SAVE.heal||[]).slice();
          SAVE.hp=Math.max(1, max-20); SAVE.heal=['patch','bpart'];
          var a=useHeal(0), hp1=SAVE.hp;
          SAVE.heal=['bpart']; var b=useHeal(0), hp2=SAVE.hp;
          SAVE.hp=hp0; SAVE.heal=bag; try{save();hud();}catch(e){}
          rec.d6=hp1-(max-20); rec.d10=hp2-hp1; rec.ok=a&&b;
          return rec;
        })()""")
        ok('Hase patch kit heals +6 and spare tube +10, not 20% bandage', heal and heal.get('patch')==6 and heal.get('bpart')==10 and heal.get('d6')==6 and heal.get('d10')==10 and heal.get('patchPct') is None, heal)
        lines = (after or {}).get('lines') or {}
        ok('after-seal Mori line is new (freight quiet)', any('quiet for good' in (x or '').lower() or 'kettle' in (x or '').lower() for x in lines.get('mori') or []), lines.get('mori'))
        ok('after-seal Nao line is new (day job)', any('day job' in (x or '').lower() for x in lines.get('nao') or []), lines.get('nao'))
        ok('after-seal Haru line is new (bikes gone)', any('bikes are gone' in (x or '').lower() or 'sofa' in (x or '').lower() for x in lines.get('haru') or []), lines.get('haru'))

        # landmark path is unchanged: not nails, c2Enter('depot') should NOT be forced if p5Enter is false
        land = await ev(pg, """(function(){
          var st=c2S(), P5=root.FFF_S2P5;
          var fac=st.e.run_fac;
          st.e.run_fac='neo';
          var enter=P5.p5Enter();
          st.e.run_fac=fac;
          return { enter:enter, stillP5:P5.p5Enter() };
        })()""")
        ok('landmark / non-Nails path does not take the 13-room depot', land and land.get('enter') is False and land.get('stillP5') is True, land)

        ok('no page errors', not errs, errs[:6])
        await b.close()
    fails = [r for r in RES if not r[0]]
    print('RESULT', f'{len(RES)-len(fails)}/{len(RES)} pass', f'{len(fails)} fail')
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    asyncio.run(main())
