#!/workspace/pwenv/bin/python3
"""t12: after backing the Punks at X2, the spokesman stays, the handshake
cine runs, Flip walks in from off-screen, skip and Walk away stay safe,
and a mid-scene reload resumes the offer."""
import asyncio, json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import h

async def ok(name, cond, detail=None):
    print(('PASS' if cond else 'FAIL'), name, '' if detail is None else json.dumps(detail, default=str)[:400])
    if not cond:
        raise AssertionError(name)

async def dismiss(g, n=8):
    for _ in range(n):
        st = await g.ev("({dlg:!!W.dlg,txt:(document.getElementById('wdlg')&&document.getElementById('wdlg').innerText||'').slice(0,80)})")
        if not st or not st.get('dlg'):
            break
        await g.pg.touchscreen.tap(195, 700)
        await g.skipall(2)
        await g.wait(200)

async def setup_at_x2(g):
    boot = await g.boot()
    left = await g.gym_exit()
    await g.go_xy(1790, 2165)
    for i in range(14):
        await g.ev("if(typeof g38tClashCheck==='function')g38tClashCheck(); if(root.FFF_NALLEY&&FFF_NALLEY.retrigger)FFF_NALLEY.retrigger();1")
        s = await g.snapshot('X2')
        if (s.get('clash') or {}).get('b') == 'X2':
            return s
        await g.wait(350)
    return await g.snapshot('X2')

async def join_punks(g):
    # Back the Punks (arc) in the active clash
    r = await g.ev("""(function(){
      var C=W.g38c; if(!C) return 'no-clash';
      var side = (G38T.FAC[C.A.id]==='arc') ? 'A' : ((G38T.FAC[C.Z.id]==='arc') ? 'Z' : null);
      if(!side) return 'no-punk-side:'+C.A.id+','+C.Z.id;
      try {
        if (typeof g38tBack==='function') g38tBack(side);
      } catch(e){ return 'err '+e.message; }
      return 'asked '+side+' '+C.b;
    })()""")
    print('JOIN prompt', r)
    await g.wait(400)
    # click "Back the Punks" if a dialog is up
    clicked = await g.ev("""(function(){
      var btns=[...document.querySelectorAll('#wdlg button, button')].filter(function(b){return /Back the Punks/i.test(b.textContent||'');});
      if(!btns.length) return 'no-btn:'+([...document.querySelectorAll('#wdlg button,button')].map(function(b){return b.textContent;}).slice(0,8));
      btns[0].click(); return 'clicked';
    })()""")
    print('CLICK', clicked)
    await g.wait(600)
    return await g.ev("({fight:!!W.dgFight,ctxs:window.__ctxs.length,last:window.__ctxs[window.__ctxs.length-1]})")

async def run():
    out = Path(os.environ.get('SHOTDIR', '/workspace/nailsalley/shots'))
    async with h.Game(out=str(out), index=os.environ.get('FFD_INDEX')) as g:
        s0 = await setup_at_x2(g)
        print('AT X2', {k: s0[k] for k in ('clash','keep','hear','xy') if k in s0})
        await ok('clash on at X2', (s0.get('clash') or {}).get('b') == 'X2', s0.get('clash'))
        joined = await join_punks(g)
        print('JOINED', json.dumps(joined, default=str)[:400])
        await ok('fight opened', bool(joined and (joined.get('fight') or joined.get('ctxs'))), joined)
        w = await g.win_fight(True)
        print('WIN', w)
        await ok('won clash returned', isinstance(w, str) and w.startswith('back'), w)
        await g.wait(500)
        snap = await g.snapshot('X2')
        print('AFTER WIN keep', snap.get('keep'), 'lockAsk', snap.get('lockAsk'), 'evs', (snap.get('evs') or [])[-8:])
        await ok('backed Punk kept or cine armed', bool(snap.get('keep') or snap.get('lockAsk') or any('nalley' in str(e) for e in (snap.get('evs') or []))), snap)
        await g.shot('t12_after_win_punk')

        # wait for cine to start (1.8s lock-ask delay)
        seen = None
        for i in range(20):
            evs = await g.ev("window.__evs||[]") or []
            if any('nalley:cine:start' in str(e) or 'nalley:offer' in str(e) or 'lock:ask' in str(e) for e in evs):
                seen = evs
                break
            await g.wait(250)
        print('CINE EVS', (seen or evs)[-12:])
        await ok('handshake cine started', bool(seen), seen)
        # skip the walk if it's still going, then wait for the offer / Shake button
        await g.ev("if(W.nalleyCine&&W.nalleyCine.st==='walk'){W.nalleySkipWalk=1;}1")
        clicked = 'no-shake'
        txt = ''
        CLICK = """(function(){
          var labs=['Shake on it','OK','Next'];
          var btns=[...document.querySelectorAll('#wdlg button, #wdlg.on button, button')];
          var names=btns.map(function(b){return (b.textContent||'').trim();});
          for (var i=0;i<labs.length;i++){
            var b=btns.filter(function(x){return x.textContent&&x.textContent.indexOf(labs[i])>=0 && x.offsetParent!==null;})[0];
            if(b){ b.click(); return 'click:'+labs[i]; }
          }
          return 'none:'+names.slice(0,8).join('|');
        })()"""
        for i in range(16):
            st = await g.ev("""({st:W.nalleyCine&&W.nalleyCine.st,dlg:!!W.dlg,cut:!!W.cut,on:!!(document.getElementById('wdlg')&&document.getElementById('wdlg').classList.contains('on')),
              txt:(document.getElementById('wdlg')&&document.getElementById('wdlg').innerText||'').replace(/\s+/g,' ').trim().slice(0,180),
              shake:[...document.querySelectorAll('button')].some(function(x){return /Shake on it/i.test(x.textContent||'');}),
              btns:[...document.querySelectorAll('#wdlg button, button')].filter(function(b){return b.offsetParent!==null;}).map(function(b){return (b.textContent||'').trim();}).slice(0,8)})""")
            print('WAIT', i, st)
            txt = (st or {}).get('txt') or ''
            if st and st.get('shake'):
                break
            if st and (st.get('dlg') or st.get('on')) and not st.get('shake'):
                print('  ADV', await g.ev(CLICK))
            await g.wait(700)
        print('DLG', (txt or '')[:200])
        clicked = await g.ev("""(function(){
          var b=[...document.querySelectorAll('button')].filter(function(x){return /Shake on it/i.test(x.textContent||'');})[0];
          if(!b) return 'no-shake'; b.click(); return 'shook';
        })()""")
        print('SHAKE', clicked)
        await ok('Shake on it is on screen', clicked == 'shook', clicked)
        if clicked == 'shook':
            await g.wait(200)
            hs = await g.ev("!!document.getElementById('nalleyhs')")
            print('HS canvas', hs)
            await g.shot('t12_handshake_pose', hush=False)
            # canvas may last 900ms; either we caught it or ev recorded the draw
            evs = await g.ev("window.__evs||[]") or []
            await ok('handshake pose drawn or shake ev fired', bool(hs) or any('nalley:hs' in str(e) or 'nalley:shake' in str(e) for e in evs), evs[-10:])
        await g.wait(1600)
        locked = await g.ev("({run:c2S().e.run_fac,n13:c2S().e.n13,lockAsk:c2S().e.lockAsk||null})")
        print('LOCKED', locked)
        await ok('run_fac is arc after shake', locked and locked.get('run') == 'arc', locked)

        # Flip should walk in from off-screen
        await g.wait(800)
        # force cutStart if the 2.6s timer is still pending
        await g.ev("try{ if(c2S().e.n13==='cut' && !W.n13cutGo){ /* wait */ } }catch(e){} 1")
        flip_off = None
        for i in range(24):
            evs = await g.ev("window.__evs||[]") or []
            off = [e for e in evs if 'nalley:flip:off' in str(e) or 'nalley:flip:walk' in str(e)]
            if off:
                flip_off = off
                break
            await g.wait(250)
        print('FLIP EVS', flip_off or (await g.ev("window.__evs||[]"))[-10:])
        await ok('Flip walk-in started from off-camera ev', bool(flip_off), flip_off)
        # skip Flip walk
        await g.ev("W.nalleySkipFlip=1;1")
        await g.wait(600)
        await g.shot('t12_flip_after', hush=False)
        evs = await g.ev("window.__evs||[]") or []
        print('SKIP EV', [e for e in evs if 'skip:flip' in str(e) or 'flip:skipped' in str(e)])
        print('ERRS', g.errs[:8])
        await ok('no page errors on happy path', not g.errs, g.errs[:4])

    # Walk away + reload mid-offer, fresh page
    async with h.Game(out=str(out), index=os.environ.get('FFD_INDEX')) as g:
        s0 = await setup_at_x2(g)
        await join_punks(g)
        await g.win_fight(True)
        for i in range(20):
            evs = await g.ev("window.__evs||[]") or []
            if any('nalley:cine:start' in str(e) or 'nalley:offer' in str(e) for e in evs):
                break
            await g.wait(250)
        await g.ev("if(W.nalleyCine&&W.nalleyCine.st==='walk'){W.nalleySkipWalk=1;}1")
        await g.wait(700)
        await dismiss(g, 8)
        # Walk away
        away = await g.ev("""(function(){
          var b=[...document.querySelectorAll('button')].filter(function(x){return /Walk away/i.test(x.textContent||'');})[0];
          if(!b) return 'no-away'; b.click(); return 'away';
        })()""")
        print('AWAY', away)
        await g.wait(1500)
        st = await g.ev("({run:c2S().e.run_fac||null,cut:!!W.cut,dlg:!!W.dlg,lockAsk:c2S().e.lockAsk||null,cine:W.nalleyCine})")
        print('AFTER AWAY', st)
        await ok('Walk away does not lock a side', not (st and st.get('run')), st)
        await ok('Walk away does not leave W.cut stuck', not (st and st.get('cut')), st)
        print('ERRS2', g.errs[:6])
        await ok('no page errors on walk-away', not g.errs, g.errs[:4])

    # Reload mid-offer: seed lockAsk and resume
    async with h.Game(out=str(out), index=os.environ.get('FFD_INDEX')) as g:
        await g.boot()
        left = await g.gym_exit()
        await g.go_xy(1790, 2165)
        await g.ev("""(function(){
          var S=c2S(); S.e.lockAsk={fac:'arc',b:'X2'}; S.e.g38win_X2=1;
          if(typeof save==='function') save();
          try{ if(typeof c2Pop==='function') c2Pop(); }catch(e){}
          return 1;
        })()""")
        await g.wait(800)
        evs = await g.ev("window.__evs||[]") or []
        cine = await g.ev("({cine:W.nalleyCine,cut:!!W.cut,ask:c2S().e.lockAsk})")
        print('RESUME', cine, evs[-8:])
        await ok('mid-scene reload resumes offer or starts cine',
                 bool((cine and cine.get('cine')) or any('nalley:resume' in str(e) or 'nalley:cine:start' in str(e) for e in evs)),
                 cine)
        print('ERRS3', g.errs[:6])
        await ok('no page errors on resume', not g.errs, g.errs[:4])

    print('t12 ALL PASS')

if __name__ == '__main__':
    asyncio.run(run())
