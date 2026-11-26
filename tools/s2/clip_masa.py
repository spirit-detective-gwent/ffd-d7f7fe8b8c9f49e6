#!/workspace/pwenv/bin/python3
"""Clip of the Masa intro push-in, the start of the shutter fight, and the bond question.
Review-only; never publishes.
"""
import asyncio, os, sys, shutil, subprocess
from pathlib import Path
sys.path.insert(0, str(Path('/workspace/ffd-seal2-p5/tools/bond')))
import bh
from playwright.async_api import async_playwright

OUT = Path('/workspace/v6560-review/seal2/phase5/wired')
OUT.mkdir(parents=True, exist_ok=True)
PORT = int(os.environ.get('PORT', '8995'))
FFD = '/workspace/ffd-seal2-p5'
POLL = """(function(){
  var d=document.getElementById('wdlg');
  var on=!!(d&&d.classList.contains('on'));
  var fight=!!(document.getElementById('battle')&&document.getElementById('battle').classList.contains('on'))
    || !!(document.querySelector('.screen.fight.on, #fight.on, #board.fight'));
  return {
    on:on,
    len:on?(((d.querySelector('.d2-q,.tw,.d2-body,.bqq')||{}).textContent)||'').length:0,
    bond:!!document.querySelector('#wdlg.on button.bondopt'),
    intro:!!(document.querySelector('.bent, #wdlg.on .sh, .cintro, [data-bent]')),
    fight:fight || !!(typeof ST!=='undefined' && ST.inGame),
    stg:(root.FFF_S2P5&&FFF_S2P5.stg&&FFF_S2P5.stg())||'',
    cut:!!W.cut, dlg:!!W.dlg
  };
})()"""
CLICK = """(i)=>{var b=[...document.querySelectorAll('#wdlg.on button')].filter(e=>e.offsetParent&&!e.disabled&&!/Auto/.test(e.textContent));if(!b.length)return null;var x=b[i||0]||b[0];x.click();return x.textContent.trim()}"""

SETUP = """(function(){
  SAVE.chapter=2; SAVE.ch1=1; SAVE.ch2=1; SAVE.bond=SAVE.bond||{}; SAVE.bond.path='fierce'; SAVE.bond.lock=1;
  try { STORY.ensure(SAVE); } catch(e){}
  var st=c2S(); st.e=st.e||{}; st.e.run_fac='arc'; st.e.seal_sento=1; st.e.sealKnown=1; st.e.c2sRep=1; st.e.c2lMap=1;
  st.e.n13='done'; st.e.arrive=1; st.e.gymIn=1; st.e.genji=1; st.e.nq=st.e.nq||{};
  st.q=st.q||{}; st.q.cq2_nq_west=9; st.q.cq2_nq_cold=9; st.q.cq2_nq_paint=9; st.q.cq2_nq_door=9; st.q.cq2_nq_seal=9;
  st.q.cq2_locks=0; st.qa='cq2_locks';
  st.q.cq2_s2_waga=9; st.q.cq2_s2_runs=9; st.q.cq2_s2_boat=9; st.q.cq2_s2_gar=9;
  st.e.baseOpen_dep=1; st.e.guardGone_depot=1;
  try { if (root.FFF_S2&&FFF_S2.setStg) FFF_S2.setStg('done'); } catch(e1){}
  try { if (root.FFF_S2P2&&FFF_S2P2.setStg) FFF_S2P2.setStg('done'); } catch(e2){}
  try { if (root.FFF_S2P3&&FFF_S2P3.setStg) FFF_S2P3.setStg('done'); } catch(e3){}
  try { if (root.FFF_S2P4&&FFF_S2P4.setStg) FFF_S2P4.setStg('done'); } catch(e4){}
  try { c2QSync(); save(); } catch(e){}
  try { if (root.FFF_S2P5&&FFF_S2P5.chainRepair) FFF_S2P5.chainRepair(); } catch(e5){}
  var P5=root.FFF_S2P5;
  P5.setStg('met'); st.q.cq2_s2_depot=1;
  st.e.masaFate=''; st.e.seal_depot=0;
  try { var B=STORY.bond(SAVE); if (B && B.picks) delete B.picks.c2_masa_after; } catch(e6){}
  return { q:st.q.cq2_s2_depot, stg:P5.stg() };
})()"""

async def boot_p5(pg, port, body):
    await bh.boot(pg, port, body)
    await bh.ch2(pg)
    info = await bh.ev(pg, SETUP)
    print('setup', info, flush=True)
    await bh.ev(pg, """(function(){
      try { c2Go('dshut',[640,760,3]); if (typeof c2Pop==='function') c2Pop(); } catch(e){}
      try { if (W.ryo) { W.ryo.x=560; W.ryo.y=760; place(W.ryo,0); } if (W.aoi) { W.aoi.x=480; W.aoi.y=800; place(W.aoi,0); } camera(true); } catch(e2){}
      return typeof c2Room==='function'?c2Room():null;
    })()""")
    await pg.wait_for_timeout(800)
    await bh.ev(pg, bh.HUSH)

async def record_all(body, errs):
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
        pg = await ctx.new_page(); await pg.add_init_script(bh.SHIM)
        pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
        await boot_p5(pg, PORT, body)
        d = '/tmp/p5clip/masa'
        v = bh.VT(pg, ctx, d)
        await v.start()
        await v.run(0.6)

        # Masa intro push-in at the shutter
        started = await bh.ev(pg, """(function(){
          var P5=root.FFF_S2P5;
          try { W.dlg=false; W.cut=false; W.busy=false; } catch(e){}
          try { if (typeof c2ActC==='function') return !!c2ActC('dshut','s2_talk_masa'); } catch(e2){}
          return 0;
        })()""")
        print('intro start', started, flush=True)

        saw_intro = False
        saw_fight = False
        still = 0
        lastlen = -1
        clicks = 0
        # drive the intro lines, linger, then let the fight start
        maxf = 60 * 40
        while v.n < maxf and not saw_fight:
            await v.run(0.1)
            st = await bh.ev(pg, POLL)
            if not isinstance(st, dict):
                continue
            if st.get('fight'):
                saw_fight = True
                break
            if st.get('intro') or st.get('on'):
                saw_intro = True
            if not st.get('on'):
                lastlen = -1
                still = 0
                continue
            if st['len'] == lastlen:
                still += 1
            else:
                lastlen = st['len']
                still = 0
            # linger on each line, especially any intro card
            need = 14 if st.get('intro') else 8 + int(min(24, lastlen / 8))
            if still >= need and not st.get('bond'):
                await pg.evaluate(CLICK, 0)
                clicks += 1
                lastlen = -1
                still = 0

        print('intro done', 'frames', v.n, 'intro', saw_intro, 'fight', saw_fight, 'clicks', clicks, flush=True)
        # start of the fight: hold a couple of seconds on the battle
        if saw_fight:
            await v.run(2.4)
        else:
            # force a painted beat if the fight UI did not come up
            await v.run(0.8)

        # jump to the after-win bond (skip the long victory cine)
        await bh.ev(pg, """(function(){
          try { if (typeof backToMap==='function') backToMap(); } catch(e){}
          try { ST.inGame=false; W.dgFight=null; W.busy=false; W.dlg=false; W.cut=false; } catch(e2){}
          var d=document.getElementById('wdlg'); if(d){d.className='';d.innerHTML='';}
          var r=document.getElementById('result'); if(r) r.className='screen';
          var bat=document.getElementById('battle'); if(bat) bat.className=bat.className.replace(/\\bon\\b/g,'');
          try { show && show('world'); } catch(e3){}
          var P5=root.FFF_S2P5, st=c2S();
          P5.setStg('won'); st.q.cq2_s2_depot=2; st.e.masaFate=''; st.e.seal_depot=0;
          try { var B=STORY.bond(SAVE); if (B && B.picks) delete B.picks.c2_masa_after; } catch(e4){}
          try { c2Go('dshut',[640,720,0]); if (typeof c2Pop==='function') c2Pop(); } catch(e5){}
          try { if (W.ryo) { W.ryo.x=560; W.ryo.y=740; place(W.ryo,0); } if (W.aoi) { W.aoi.x=480; W.aoi.y=780; place(W.aoi,0); } camera(true); } catch(e6){}
          return 1;
        })()""")
        await v.run(0.5)
        await bh.ev(pg, """(function(){
          var P5=root.FFF_S2P5;
          try { W.dlg=false; W.cut=false; W.busy=false; } catch(e){}
          P5.askBond();
          return 1;
        })()""")

        saw_bond = False
        still = 0
        lastlen = -1
        maxf2 = v.n + 60 * 25
        while v.n < maxf2:
            await v.run(0.1)
            st = await bh.ev(pg, POLL)
            if not isinstance(st, dict):
                continue
            if st.get('bond'):
                if not saw_bond:
                    saw_bond = True
                    print('bond up at', v.n, flush=True)
                still += 1
                # linger on the question, then pick Fierce (leave him) and hold a beat
                if still >= 24:
                    await pg.evaluate(CLICK, 0)
                    still = 0
                    # record the pick and a little of the payoff, then stop
                    await v.run(2.0)
                    break
            elif st.get('on'):
                if st['len'] == lastlen:
                    still += 1
                else:
                    lastlen = st['len']
                    still = 0
                if still >= 8:
                    await pg.evaluate(CLICK, 0)
                    lastlen = -1
                    still = 0
            else:
                still = 0
                lastlen = -1
                if saw_bond:
                    await v.run(1.0)
                    break

        await v.run(0.6)
        print('done frames', v.n, 'bond', saw_bond, flush=True)
        await b.close()
        return d, saw_intro, saw_fight, saw_bond

async def main():
    os.environ['FFD'] = FFD
    bh.FFD = FFD
    bh.serve(PORT, FFD)
    body = bh.inject(FFD + '/index.html')
    errs = []
    d, intro, fight, bond = await record_all(body, errs)
    mp4 = OUT / 'clip_masa_intro_fight_bond.mp4'
    bh.encode(d, mp4)
    print('WROTE', mp4, 'size', mp4.stat().st_size, 'intro', intro, 'fight', fight, 'bond', bond, flush=True)
    print('ERRS', errs[:8], flush=True)
    if not (intro or fight or bond):
        sys.exit(1)

asyncio.run(main())
