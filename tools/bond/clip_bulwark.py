#!/workspace/pwenv/bin/python3
"""Record a Masa fight at Compassionate Lv10: special starts Bulwark, a hit stores Rebound, the next attack releases it.
60 fps virtual time. Review-only; does not publish.
usage: FFD=/workspace/ffd-comp clip_bulwark.py
"""
import os, sys, asyncio, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import bh
from playwright.async_api import async_playwright

OUT = Path('/workspace/v6560-review/comp'); OUT.mkdir(exist_ok=True)
PORT = 9015
FFD = os.environ.get('FFD', '/workspace/ffd-comp')
bh.FFD = FFD
SETUP = r"""
(function(){
  SAVE.intro=1; SAVE.ch1=1; SAVE.dbl=1; SAVE.hp=55; SAVE.sp=40; SAVE.maxHp=55;
  SAVE.c2les={assist:1,sneak:1,cover:1};
  SAVE.chars=SAVE.chars||{}; SAVE.chars.aoi=SAVE.chars.aoi||{}; SAVE.chars.aoi.sp=40;
  var B=STORY.bond(SAVE); B.path='balanced'; B.lock=1; B.px=6000; // Lv 10 (bondTot(10)=5723, bondTot(11)=8145)
  ST.set.txt='normal'; ST.set.tips=false; ST.set.flash='normal';
  return {lv:STORY.bondLv(SAVE), path:B.path};
})()
"""
START = r"""
(function(){
  var lo=STORY.loadout(SAVE);
  var pst=gearPst({combo:true,hp:SAVE.hp,max:55,spirit:40,deck:lo.deck,sig:lo.sig,sig2:lo.sig2,disc:1,cmax:lo.cmax,ctrPlus:lo.ctrPlus|0,dgPlus:0,rebCap:lo.rebCap|0});
  var bench=benchOf(null,{mini:'mb2_depot',dg:'c2'});
  FFF_UI.startMatch('ryo',{foes:['mb2_depot'],mini:'mb2_depot',drop:0,partner:'Aoi',assist:1,bench:bench,pst:pst,ctx:{dg:'c2',mini:'mb2_depot'},esc:null});
  var b=FFF_UI.ST&&FFF_UI.ST.b;
  return {ok:!!b, sig:b&&b.s[0].sig&&b.s[0].sig.n, bulw:b&&b.s[0].sig&&b.s[0].sig.bulw, cap:b&&b.s[0].sig&&b.s[0].sig.bulwCap, rebCap:b&&b.rebCap, path:STORY.bond(SAVE).path, lv:STORY.bondLv(SAVE)};
})()
"""
ARM = r"""
(function(){
  var ST=FFF_UI.ST, b=ST.b, E=ENGINE;
  if(!b) return {ok:0,why:'nobattle'};
  ST.swapOpen=false; ST.mark=[]; ST.busy=false; ST.anim=false;
  b.s[0].spirit=40;
  if(b.bench) b.bench.spirit=40;
  b.turn=0;
  function onlyAtk(arr){
    var o=(arr||[]).filter(function(c){return c.t==='atk'&&!c.pierce;});
    if(!o.length){ o=[{t:'atk',v:6,hits:1,n:'Crate Toss',id:'dep_crate',u:'crate1',ch:'mb2_depot'}]; }
    return o;
  }
  b.s[1].hand=onlyAtk(b.s[1].hand);
  b.s[1].deck=onlyAtk(b.s[1].deck);
  FFF_UI.render(false);
  return {ok:1,lv:STORY.bondLv(SAVE),bulw:!!(b.s[0].sig&&b.s[0].sig.bulw),g:b.s[0].sig&&b.s[0].sig.bulwG,cap:b.s[0].sig&&b.s[0].sig.bulwCap,sp:b.s[0].spirit,foe:(b.s[1].hand[0]&&b.s[1].hand[0].n)||'',sig:b.s[0].sig&&b.s[0].sig.n};
})()
"""
POLL = r"""
(function(){
  var ST=FFF_UI.ST,b=ST&&ST.b,g=document.getElementById('game');
  var chip=document.querySelector('.bulwb');
  var floats=[...document.querySelectorAll('.float')].map(function(e){return e.textContent;});
  var log=document.getElementById('logBox');
  return {
    on:!!(g&&g.classList.contains('on')),
    busy:!!(ST&&ST.busy), turn:b&&b.turn, over:!!(b&&b.over),
    guard:b&&b.s[0]&&b.s[0].guard,
    bulw:b&&b.bulw?{t:b.bulw.t,g:b.bulw.g}:null,
    reb:b&&(b.reb|0),
    chipOn:!!(chip&&chip.classList.contains('on')),
    chip:(chip&&chip.textContent)||'',
    fp:!!document.querySelector('#fP.bulwOn'),
    floats:floats,
    log:(log&&log.textContent||'').slice(-400)
  };
})()
"""

async def main():
    os.environ['FFD']=FFD
    bh.serve(PORT, FFD)
    body=bh.inject(FFD+'/index.html')
    errs=[]
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-gl=swiftshader','--enable-unsafe-swiftshader'])
        ctx=await b.new_context(viewport={'width':390,'height':844}, device_scale_factor=1, is_mobile=True, has_touch=True)
        pg=await ctx.new_page(); await pg.add_init_script(bh.SHIM)
        pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
        await bh.boot(pg, PORT, body); await bh.ch2(pg); await bh.ev(pg, bh.HUSH)
        info=await bh.ev(pg, SETUP)
        print('setup', info)
        ok=await bh.ev(pg, START)
        print('start', ok)
        # wait for the battle screen
        for _ in range(80):
            st=await bh.ev(pg, POLL)
            if st and st.get('on'): break
            await pg.wait_for_timeout(100)
        arm=await bh.ev(pg, ARM)
        print('arm', arm)
        d='/tmp/compclip/bulwark'
        v=bh.VT(pg, ctx, d); await v.start()
        await v.run(0.8)
        # arm and play the special
        picked=await bh.ev(pg, "FFF_UI.sigPick()")
        print('sigPick', picked)
        await v.run(0.5)
        st1=await bh.ev(pg, POLL)
        print('after arm', {k:st1.get(k) for k in ('on','busy','chip','fp') if isinstance(st1,dict)})
        committed=await bh.ev(pg, "FFF_UI.playCommit()")
        if not committed:
            committed=await pg.evaluate("""()=>{var pv=document.querySelector('#preview, #preview.live, #btnAct'); if(pv){pv.click(); return 'clicked '+(pv.id||pv.className);} return 'no preview';}""")
        print('playCommit', committed)
        await v.run(0.4)
        skipped = await pg.evaluate("""()=>{
          var c=document.getElementById('cut');
          if(c && c.onpointerdown){
            try{ c.onpointerdown({preventDefault:function(){}}); return 1; }
            catch(e){ return 'ERR:'+e.message; }
          }
          return 0;
        }""")
        print('skipcut', skipped)
        # let the special resolve and Masa take his (attack-only) turn
        await v.run(2.0)
        # wait through the special and the enemy reply
        seen={'bulw':False,'store':False,'rel':False}
        still=0; last=None; maxf=60*18
        evlog=[]
        while v.n<maxf:
            await v.run(0.1)
            st=await bh.ev(pg, POLL)
            if not isinstance(st, dict):
                evlog.append(('bad',st)); continue
            evlog.append((v.n, st.get('bulw'), st.get('reb'), st.get('chip'), st.get('floats'), st.get('turn'), st.get('busy')))
            if st.get('fp') or st.get('chipOn') or (st.get('bulw') and st['bulw'].get('t',0)>0):
                seen['bulw']=True
            if (st.get('reb') or 0)>0 or any('REBOUND' in (f or '') and '+' in (f or '') for f in (st.get('floats') or [])):
                if not seen['rel'] and (st.get('reb') or 0)>0: seen['store']=True
                if any('REBOUND' in (f or '') for f in (st.get('floats') or [])) and seen['store'] and st.get('reb')==0:
                    seen['rel']=True
            if seen['rel'] and not st.get('busy'):
                still+=1
                if still>=36: break
            else:
                still=0
            cut_up = await pg.evaluate("()=>!!(document.getElementById('cut')&&document.getElementById('cut').onpointerdown)")
            if cut_up:
                await pg.evaluate("()=>{var c=document.getElementById('cut');if(c&&c.onpointerdown)c.onpointerdown({preventDefault:function(){}})}")
                await v.run(0.4)
                continue
            if st.get('turn') == 0 and not st.get('busy') and seen['bulw'] and not seen['rel']:
                want_atk = bool(seen['store'])
                play = await pg.evaluate(
                    """(want)=>{
                      var cards=[...document.querySelectorAll('#hand .card')];
                      var pick;
                      if(want) pick=cards.find(c=>/Street Jab|Guard Crack|Clean Slash|Kata/i.test(c.textContent||''))||cards.find(c=>/ATTACK/i.test(c.textContent||''));
                      else pick=cards.find(c=>/Ouendan|CHARGE|Tape Up/i.test(c.textContent||''))||cards[1];
                      if(!pick) return 'nocard';
                      pick.click();
                      var a=document.getElementById('btnAct'); if(a) a.click();
                      var pv=document.querySelector('#preview.live'); if(pv) pv.click();
                      try{ if(window.FFF_UI&&FFF_UI.playCommit) FFF_UI.playCommit(); }catch(e){}
                      return (pick.textContent||'').slice(0,50);
                    }""",
                    want_atk,
                )
                print('play', 'atk' if want_atk else 'yield', play, 'frame', v.n, 'reb', st.get('reb'))
                evlog.append(('play', play, v.n, want_atk))
                await v.run(0.3)
        await v.run(0.8)
        final=await bh.ev(pg, POLL)
        print('final', {k:final.get(k) for k in ('bulw','reb','chip','fp','floats','log') if isinstance(final,dict)})
        print('seen', seen, 'frames', v.n, 'errs', errs[:6])
        mp4=OUT/'bulwark_rebound.mp4'
        bh.encode(d, mp4)
        print('wrote', mp4, 'bytes', mp4.stat().st_size)
        # key stills: first frame with chip, first REBOUND float
        open(OUT/'clip_log.json','w').write(json.dumps({'seen':seen,'final':final if isinstance(final,dict) else str(final),'errs':errs,'frames':v.n}, indent=2)[:8000])
        await b.close()
        if not seen['bulw']:
            sys.exit(2)

asyncio.run(main())
