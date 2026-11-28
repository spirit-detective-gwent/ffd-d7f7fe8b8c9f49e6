#!/workspace/pwenv/bin/python3
"""MODE=video: record the lesson from 'Teach me' to the compare card (pour, carry, hand-off) as a 390x844 webm in $VID.
   MODE=shots: phone-size (DSF 1 and 3) key frames: pour (stream), carry mid-walk, hand-off.  OUT=dir. FFD_INDEX picks the build."""
import asyncio, sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import h
MODE = os.environ.get('MODE', 'shots'); OUT = os.environ.get('OUT', '/workspace/herbcine/shots/v2media'); os.makedirs(OUT, exist_ok=True)
STATE = """(function(){ var st=c2S(); st.e.sumire=1; st.e.herbBrief=1; SAVE.craft={}; SAVE.sc=SAVE.sc||{};
 SAVE.sc.pot='gather'; SAVE.sc.potGift=1; SAVE.sc.potLeaf=1; delete SAVE.sc.potHand; delete SAVE.sc.potGinger; delete SAVE.sc.potGranted;
 var hb=herbS(); hb.leaf=1; hb.ginger=1; save(); return 1; })()"""
PROBE = """(function(){ function r(e){ if(!e) return null; var b=e.getBoundingClientRect(); return [b.x,b.y,b.width,b.height]; }
 var su=W.c2n.sumire, bt=document.getElementById('hsbot'), sm=document.getElementById('hsstream');
 return {su:r(su.el), sy:su.y, bot:r(bt), par:bt?(bt.parentNode===su.el?'su':bt.parentNode===W.ryo.el?'ryo':'o'):null, smop:sm?+getComputedStyle(sm).opacity:0, smh:sm&&sm.getAnimations().some(function(a){return a.playState==='running'&&a.currentTime>40})?sm.getBoundingClientRect().height:0, dp:r(document.getElementById('hsladle')), cmp:!!document.getElementById('hscmp'), live:!!document.getElementById('hspour')}})()"""
async def main():
    async with h.Game(path='compassionate', out=OUT) as g:
        await g.boot(); await g.enter('clinic', 560, 640)
        await g.ev("W.scr=0;W.cut=0;1"); await g.hush(); await g.ev(STATE); await g.ev("c2SumireD()"); await g.wait(900)
        if MODE == 'video': await g.wait(600)
        await g.ev("(function(){var b=[...document.querySelectorAll('#wdlg button')].find(function(x){return /Teach me$/.test(x.textContent.trim())}); b.click(); return 1})()")
        got = {}; n = 0
        for k in range(900):
            p = await g.ev(PROBE)
            if MODE == 'shots':
                if p['smop'] > 0.5 and p['smh'] > 5 and 'pour' not in got: got['pour'] = 1; await g.wait(120); await g.pg.screenshot(path=f'{OUT}/pour_phone.png'); await g.ev('1')
                if p['par'] == 'su' and p['sy'] > 500 and p['sy'] < 560 and 'carry' not in got: got['carry'] = 1; await g.pg.screenshot(path=f'{OUT}/carry_phone.png')
                if p['par'] == 'su' and p['sy'] > 598 and 'offer' not in got and k > 0: got['offer'] = 1; await g.pg.screenshot(path=f'{OUT}/offer_phone.png')
                if p['par'] == 'ryo' and 'take' not in got: got['take'] = 1; await g.wait(150); await g.pg.screenshot(path=f'{OUT}/take_phone.png')
            c = await g.pg.evaluate(h.NX)
            if c and k % 3 == 0 and not p['cmp'] and 'take' in got | ({'take': 1} if MODE == 'video' else {}): pass
            if c and k % 4 == 0: await g.pg.touchscreen.tap(*c)
            if p['cmp']:
                n += 1
                if n > (12 if MODE == 'video' else 3): break
            await g.wait(60 if MODE == 'video' else 40)
        print(MODE, got, g.errs[:3])
        if MODE == 'video':
            await g.pg.close(); print('video', await g.pg.video.path())
asyncio.run(main())
