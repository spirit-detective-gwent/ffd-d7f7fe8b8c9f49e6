"""test_shonen: Shonen Showdown (fighter cabinet) v6566-shonen. Usage: test_shonen.py [index.html]"""
import asyncio, sys, json; sys.path.insert(0,'/workspace/shonen'); import h
from pathlib import Path
if len(sys.argv) > 1: h.INDEX = Path(sys.argv[1])
R = []
def ok(name, cond, info=''):
    R.append((name, bool(cond))); print(('PASS ' if cond else 'FAIL ') + name + ('  ' + str(info) if info != '' else ''), flush=True)
G = "FFF_S2ARC.cabG()"
async def main():
    async with h.Game(out='/workspace/shonen/shots/test') as g:
        await g.boot(); await g.ev("FFF_S2P6.setStg('done'); SAVE.items=999; save(); 1")
        await g.ev("FFF_S2P6.enterRoom('gc'); 1"); await g.wait(2500); await g.adv(6); await g.hush()
        cab = await g.ev("JSON.stringify({n:FFF_S2ARC.CABS.fighter.n, jp:FFF_S2ARC.CABS.fighter.jp, names:Object.keys(FFF_S2ARC.FIGHT_CAST).map(function(k){return FFF_S2ARC.FIGHT_CAST[k].n})})")
        cab = json.loads(cab)
        ok('cabinet named Shonen Showdown', cab['n'] == 'Sh\u014dnen Showdown', cab['n'])
        ok('fighter names', cab['names'] == ['KAZE TENMA','BLUE LOTUS','IRON DAIMYO','RAZOR REI','THE RONIN','BLACK COMET'], cab['names'])
        sty = json.loads(await g.ev("JSON.stringify(['ryo','aoi','masa'].reduce(function(o,k){var c=FFF_S2ARC.FIGHT_CAST[k];o[k]={style:c.style,hd:c.hd,top:c.top};return o},{}) )"))
        ok('Kaze Tenma open jacket + tall spikes (not gakuran)', sty['ryo']['style']=='openjack' and sty['ryo']['hd']=='tallspike' and sty['ryo']['top']!='#1c2244', sty['ryo'])
        ok('Blue Lotus light-blue sailor (not green)', sty['aoi']['style']=='sailor' and sty['aoi']['top']=='#7ec8e8', sty['aoi'])
        ok('The Ronin kimono + kasa (not vest/hardhat)', sty['masa']['style']=='kimono' and sty['masa']['hd']=='kasa', sty['masa'])
        html = h.INDEX.read_text(encoding='utf8')
        i = html.index('/* S2ARCFIGHT_BEGIN'); j = html.index('/* S2ARCFIGHT_END */')
        import re as _re
        blk = _re.sub(r'/\*.*?\*/', '', html[i:j], flags=_re.S)
        ok('no old title text in fighter block (code, not comments)', 'FOX FIRE' not in blk and "'FIST II'" not in blk and 'Fox Fire Fist II' not in blk and '\\u72d0\\u706b\\u62f3' not in blk)
        ok('no old cast display names', not any(("n: '%s'" % n) in blk for n in ['RYO','AOI','G\\u014cDA','NAILS','MASA','JIN']))
        ok('room cabinet label renamed', "fighter: 'SH\\u014cNEN SHOWDOWN'" in html and "'FOX FIST II'" not in html)
        print('cab', await g.ev("FFF_S2P6.cab('fighter')")); await g.wait(1600)
        print('start', await g.ev("FFF_S2ARC.cabStart()")); await g.wait(500)
        hs = await g.ev("JSON.stringify(%s.how)" % G); ok('how-to text updated', 'auto' not in hs and 'swipe up' in hs and 'SPECIAL' in hs and 'AWAY' not in hs, hs)
        panel = json.loads(await g.ev("JSON.stringify(%s.panel.btns.map(function(b){return [b.k,b.l,b.r]}))" % G))
        ok('two buttons only (ATTACK, SPECIAL), big', [p[0] for p in panel] == ['a','sp'] and all(p[2] >= 40 for p in panel), panel)
        ok('D-pad left/right', await g.ev("!!%s.panel.stick.dpad" % G))
        # pick a fighter via real taps (select uses screen taps)
        await g.tap(14+34+46, 92+280+40); await g.wait(400); await g.tap(14+34+46, 92+280+40); await g.wait(800)
        st = await g.ev("JSON.stringify(%s.dbg())" % G); print('after select', st)
        await g.wait(3600)
        ph = await g.ev("%s.phase()" % G); ok('match reaches fight', ph == 'fight', ph)
        # helpers
        RESET = """(function(o){var G=FFF_S2ARC.cabG(), pe=G._pe(), P=pe[0], E=pe[1]; P.max=P.hp=9999; E.max=E.hp=9999; P.x=150; E.x=150+(o.d||70); P.face=1; E.face=-1;
          [P,E].forEach(function(F){F.st='idle';F.mv=null;F.stT=0;F.vx=0;F.vy=0;F.air=false;F.y=430;F.lockT=0;F.inv=0;F.meter=o.m||0}); E.aiT=99; E.want={}; G.in.l=G.in.r=false; return 1})"""
        FOE_HIT = """(function(k){var G=FFF_S2ARC.cabG(), pe=G._pe(), P=pe[0], E=pe[1]; E.aiT=99; E.want={act:null}; var h0=P.hp, b0=G._in().blocks;
          return JSON.stringify({h0:h0,b0:b0})})"""
        async def foe_attack(k='p', d=46, setup=None, frames=40):
            await g.ev(RESET + "({d:%d})" % d)
            if setup: await g.ev(setup)
            b0 = await g.ev("%s._in().blocks" % G); h0 = await g.ev("%s._pe()[0].hp" % G)
            await g.ev("(function(){var E=%s._pe()[1]; E.want={act:'%s'}; E.aiT=99; return 1})()" % (G, k))
            await g.wait(700)
            b1 = await g.ev("%s._in().blocks" % G); h1 = await g.ev("%s._pe()[0].hp" % G); pst = await g.ev("%s._pe()[0].st" % G)
            await g.ev("(function(){var E=%s._pe()[1]; E.want={}; return 1})()" % G)
            return b1 - b0, h0 - h1, pst
        b, dmg, pst = await foe_attack('k'); ok('auto-block when idle', b >= 1 and dmg <= 2, (b, dmg, pst))
        b, dmg, pst = await foe_attack('k', setup="(G=>{G.in.r=true;return 1})(%s)" % G); ok('auto-block while walking forward', b >= 1 and dmg <= 2, (b, dmg, pst))
        b, dmg, pst = await foe_attack('k', setup="(G=>{G.in.l=true;return 1})(%s)" % G); ok('auto-block while walking back', b >= 1 and dmg <= 2, (b, dmg, pst))
        await g.ev("(G=>{G.in.l=G.in.r=false;return 1})(%s)" % G)
        # low / sweep: no high-low distinction for the player
        b, dmg, pst = await foe_attack('sp', d=160)
        ok('special blocked, chip damage stays', b >= 1 and dmg >= 1, (b, dmg, pst))
        # blocked during attack startup: player presses ATTACK, foe hits during the startup
        await g.ev(RESET + "({d:46})")
        r = await g.ev("""(function(){var G=FFF_S2ARC.cabG(), pe=G._pe(), P=pe[0], E=pe[1]; G.press('a'); G.step(1/60); var s=P.st, mvk=P.mv&&P.mv.k; P.stT=0.01;
           var m={k:'k',dmg:9,lvl:'mid',bs:0.2,hs:0.3,kb:60}; var h0=P.hp; /* land() is internal: emulate via the foe's move hitting now */
           E.st='atk'; E.mv=Object.assign({},m,{pose:'k',s:0,a:0.2,r:0.1,reach:80}); E.stT=0; E.hitDone=false; G.step(1/60); G.step(1/60);
           return JSON.stringify({s:s,mvk:mvk,pst:P.st,dmg:h0-P.hp})})()""")
        r = json.loads(r); ok('no block during attack startup (gets hit)', r['s'] == 'atk' and r['mvk'] == 'p' and r['dmg'] >= 5, r)
        # ATTACK chain P > P > K
        await g.ev(RESET + "({d:60})")
        seq = await g.ev("""(function(){var G=FFF_S2ARC.cabG(), P=G._pe()[0], E=G._pe()[1], seq=[], last=null; E.blockW=false;
            for (var f=0; f<90; f++){ if (f%6===0) G.press('a'); G.step(1/60); var k=P.st==='atk'&&P.mv?P.mv.k+P.chainN:null; if(k&&k!==last){seq.push(k);} last=k; } return seq.join(',')})()""")
        ok('ATTACK taps chain P > P > K', seq.startswith('p1,p2,k3'), seq)
        # SPECIAL tap vs hold
        await g.ev(RESET + "({d:200})")
        tap = await g.ev("""(function(){var G=FFF_S2ARC.cabG(), P=G._pe()[0]; G.press('sp'); for(var i=0;i<6;i++)G.step(1/60); G.release('sp'); G.step(1/60); G.step(1/60); return P.st==='atk'?P.mv.k+':'+P.mv.n:P.st})()""")
        ok('SPECIAL tap = special', tap.startswith('sp:'), tap)
        await g.wait(900); await g.ev(RESET + "({d:200})")
        hold = await g.ev("""(function(){var G=FFF_S2ARC.cabG(), P=G._pe()[0]; G.press('sp'); for(var i=0;i<30;i++)G.step(1/60); var ring=G.panel.btns[1].ring(); G.release('sp'); G.step(1/60); G.step(1/60); return (P.st==='atk'?P.mv.k+':'+P.mv.n:P.st)+'|'+ring.toFixed(2)})()""")
        ok('SPECIAL hold 0.5s = charged move (ring full)', hold.startswith('spf:') and hold.endswith('|1.00'), hold)
        await g.wait(900)
        # super: full bar -> glow -> one tap
        await g.ev(RESET + "({d:60,m:100})")
        gl = await g.ev("%s.panel.btns[1].glow()+'|'+%s.panel.btns[1].lf()" % (G, G)); ok('SPECIAL glows + reads SUPER when bar full', gl == 'true|SUPER', gl)
        await g.wait(250); await g.shot('test_super_glow', hush=False)
        su = await g.ev("""(function(){var G=FFF_S2ARC.cabG(), P=G._pe()[0]; G.press('sp'); G.step(1/60); return (P.mv&&P.mv.k)+'|'+P.meter})()""")
        ok('one SPECIAL tap fires SUPER when full', su == 'su|0', su)
        await g.wait(1500)
        gl2 = await g.ev("%s.panel.btns[1].glow()" % G); ok('glow off after super', gl2 is False or gl2 == 'false', gl2)
        # swipe up jump via real touch on the screen
        await g.ev(RESET + "({d:150})")
        await g.pg.evaluate("""()=>{const c=document.querySelector('#j6arc canvas'); const r=c.getBoundingClientRect();
            const mk=(t,y)=>new PointerEvent(t,{pointerId:7,clientX:r.left+200,clientY:r.top+y,bubbles:true,pointerType:'touch'});
            c.dispatchEvent(mk('pointerdown',420)); c.dispatchEvent(mk('pointermove',400)); c.dispatchEvent(mk('pointermove',360)); c.dispatchEvent(mk('pointerup',360));}""")
        await g.wait(120); air = await g.ev("%s._pe()[0].air+'|'+%s._pe()[0].st" % (G, G)); ok('swipe up on screen = jump', air.startswith('true'), air)
        await g.wait(900); await g.ev(RESET + "({d:150})")
        await g.pg.evaluate("""()=>{const c=document.querySelector('#j6arc canvas'); const r=c.getBoundingClientRect(), s=r.width/390;
            const mk=(t,x,y)=>new PointerEvent(t,{pointerId:8,clientX:r.left+x*s,clientY:r.top+y*s,bubbles:true,pointerType:'touch'});
            c.dispatchEvent(mk('pointerdown',120,740)); c.dispatchEvent(mk('pointermove',122,715)); c.dispatchEvent(mk('pointermove',124,690)); c.dispatchEvent(mk('pointerup',124,690));}""")
        await g.wait(120); air = await g.ev("%s._pe()[0].air" % G); ok('swipe up from the D-pad = jump', air is True or air == 'true', air)
        await g.wait(900)
        # D-pad touch walks; no crouch
        await g.ev(RESET + "({d:200})")
        x0 = await g.ev("%s._pe()[0].x" % G)
        await g.pg.evaluate("""()=>{const c=document.querySelector('#j6arc canvas'); const r=c.getBoundingClientRect(), s=r.width/390;
            c.dispatchEvent(new PointerEvent('pointerdown',{pointerId:9,clientX:r.left+150*s,clientY:r.top+760*s,bubbles:true,pointerType:'touch'}));}""")
        await g.wait(400); x1 = await g.ev("%s._pe()[0].x" % G); dn = await g.ev("%s.in.d+'|'+%s._pe()[0].crouch" % (G, G))
        await g.pg.evaluate("""()=>{const c=document.querySelector('#j6arc canvas'); const r=c.getBoundingClientRect(), s=r.width/390;
            c.dispatchEvent(new PointerEvent('pointerup',{pointerId:9,clientX:r.left+150*s,clientY:r.top+760*s,bubbles:true,pointerType:'touch'}));}""")
        ok('D-pad right walks, down-right never crouches', x1 > x0 + 15 and dn == 'false|false', (x0, x1, dn))
        # real ATTACK button tap
        await g.ev(RESET + "({d:200})")
        await g.pg.evaluate("""()=>{const c=document.querySelector('#j6arc canvas'); const r=c.getBoundingClientRect(), s=r.width/390;
            const e=(t)=>new PointerEvent(t,{pointerId:10,clientX:r.left+240*s,clientY:r.top+728*s,bubbles:true,pointerType:'touch'}); c.dispatchEvent(e('pointerdown')); c.dispatchEvent(e('pointerup'));}""")
        await g.wait(60); at = await g.ev("%s._pe()[0].st+'|'+(%s._pe()[0].mv&&%s._pe()[0].mv.k)" % (G, G, G)); ok('ATTACK button tap attacks', at.startswith('atk|p'), at)

        # v6566-shonen t606u: hitstop on landed hits; bufT holds during freeze
        await g.ev(RESET + "({d:48})")
        # Pause the cabinet rAF stepper so only these scripted steps run; two 1/60 steps stay inside the 0.045s jab freeze.
        hs = await g.ev("(function(){var G=FFF_S2ARC.cabG(),P=G._pe()[0],E=G._pe()[1]; if(!G._rawStep) G._rawStep=G.step; G.step=function(){}; E.aiT=99;E.want={}; G._rawStep(0); G.press('a'); var seen=0,f0=0,kind='',x0=0,x1=0,bufKept=0,b1=0,b2=0; for(var i=0;i<40;i++){ G._rawStep(1/60); if(P.st==='atk'&&P.mv&&P.mv.hit&&!seen){ seen=1; f0=G._in().freeze; kind=P.mv.k; x0=E.x; G.press('a'); b1=G._in().bufT; G._rawStep(1/60); G._rawStep(1/60); b2=G._in().bufT; bufKept=(b2>=b1-1e-9 && b2>0)?1:0; x1=E.x; break; } } G.step=G._rawStep; return {seen:seen,f0:+f0.toFixed(4),kind:kind,bufKept:bufKept,b1:+b1.toFixed(4),b2:+b2.toFixed(4),moved:+Math.abs(x1-x0).toFixed(4),fr:+G._in().freeze.toFixed(4)}; })()")
        ok('jab hitstop ~0.045s', hs.get('seen') and hs['kind']=='p' and 0.03 <= hs['f0'] <= 0.055, hs)
        ok('hitstop does not eat a buffered ATTACK (bufT holds, foe does not slide)', hs.get('bufKept')==1 and hs.get('moved',99)<0.02, hs)
        await g.wait(400); await g.ev(RESET + "({d:48})")
        hk = await g.ev("(function(){var G=FFF_S2ARC.cabG(),P=G._pe()[0]; G._pe()[1].aiT=99; G._pe()[1].want={}; var fK=0; for(var i=0;i<90;i++){ if(i%6===0) G.press('a'); G.step(1/60); if(P.st==='atk'&&P.mv&&P.mv.k==='k'&&P.mv.hit){ fK=G._in().freeze; break; } } return {fK:+fK.toFixed(4),chain:P.chainN}; })()")
        ok('kick/finisher hitstop ~0.06-0.09s', 0.05 <= hk['fK'] <= 0.09, hk)
        await g.wait(400); await g.ev(RESET + "({d:46})")
        hb = await g.ev("(function(){var G=FFF_S2ARC.cabG(),E=G._pe()[1]; var b0=G._in().blocks,f=0; E.aiT=99; E.want={act:'k'}; for(var i=0;i<50;i++){ G.step(1/60); if(G._in().blocks>b0){ f=G._in().freeze; break; } } return {f:+f.toFixed(4),blocks:G._in().blocks-b0}; })()")
        ok('blocked hit gets ~0.03s hitstop', hb.get('blocks',0)>=1 and 0.02 <= hb['f'] <= 0.04, hb)
        e1 = [e for e in g.errs if '404' not in e]; ok('no console errors (controls session)', not e1, e1[:5])
    # full ladder by a bot in node (all 6 fighters, continues allowed)
    import subprocess
    src = str(h.INDEX.parent)
    out = subprocess.run(['node', '/workspace/shonen/wt/tools/s2/test_shonen_sim.js', '18', 'smart', '30'], capture_output=True, text=True, env={'SRC': src, 'PATH': '/usr/bin:/bin:/usr/local/bin'}).stdout.strip()
    print(out); fc = int(out.split('full clears ')[1].split()[0]); ok('full 5-match ladder playable by a bot (with continues)', fc >= 12, out)
    out2 = subprocess.run(['node', '/workspace/shonen/wt/tools/s2/test_shonen_sim.js', '18', 'idle'], capture_output=True, text=True, env={'SRC': src, 'PATH': '/usr/bin:/bin:/usr/local/bin'}).stdout.strip()
    ok('not trivial: an idle (auto-block only) player loses match 1', ' 0 0 0 0 0 ' in out2, out2)
    await ladder_live()
async def ladder_live():
    # a real in-page full ladder run with the bot driving G (no lives cheat), continues allowed
    async with h.Game(out='/workspace/shonen/shots/test') as g:
        await g.boot(); await g.ev("FFF_S2P6.setStg('done'); SAVE.items=999; save(); 1")
        await g.ev("FFF_S2P6.enterRoom('gc'); 1"); await g.wait(2500); await g.adv(6); await g.hush()
        await g.ev("FFF_S2P6.cab('fighter')"); await g.wait(1500); await g.ev("FFF_S2ARC.cabStart()"); await g.wait(400)
        await g.ev("%s.dbg({sel:0})" % G)
        BOT = """(function(){ if (window.__bot) return 1; window.__bot = setInterval(function(){ var G=FFF_S2ARC.cabG(); if(!G||G.phase()!=='fight') return; var pe=G._pe(),P=pe[0],E=pe[1],W=G.in; W.l=W.r=false;
          var d=Math.abs(E.x-P.x), fw=P.face>0?'r':'l', bk=P.face>0?'l':'r';
          if (P.meter>=100&&d<120) G.press('sp'); else if (d>150){ if(Math.random()<0.05){G.press('sp');G.release('sp');} else W[fw]=true; }
          else if (d>58) W[fw]=true; else if (E.st==='block'&&Math.random()<0.5) W[bk]=true;
          else if ((E.st==='atk'&&E.stT>E.mv.s+E.mv.a)||Math.random()<0.25) G.press('a'); }, 33); return 1 })()"""
        await g.ev(BOT)
        seen = set(); stt = None
        for i in range(900):
            await g.wait(1000)
            stt = await g.ev("FFF_S2ARC.cabSt()")
            stg = await g.ev("%s ? %s.stage : -1" % (G, G)); seen.add(stg)
            if stt == 'cont': await g.ev("FFF_S2ARC._cab.contYes()")
            if stt in ('win', 'board', 'name', None): break
        print('ladder end state', stt, 'stages seen', sorted(seen))
        ok('in-page bot plays the full ladder to ALL CLEAR', stt in ('win', 'board', 'name') and 4 in seen, (stt, sorted(seen)))
        errs = [e for e in g.errs if '404' not in e]; ok('no console errors', not errs, errs[:5])
asyncio.run(main())
print('SUMMARY', sum(1 for r in R if r[1]), '/', len(R), 'PASS'); sys.exit(0 if all(r[1] for r in R) else 1)
