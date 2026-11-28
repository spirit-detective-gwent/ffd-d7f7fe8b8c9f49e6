#!/workspace/pwenv/bin/python3
"""Run the herbalist lesson, sample bottle/Sumire/bubble/dialog every ~150ms, shot frames. FFD_INDEX picks build; TAG names shots."""
import asyncio, sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import h
TAG = os.environ.get('TAG', 'x'); OUT = os.environ.get('OUT', '/workspace/herbcine/shots/trace_' + TAG)
STATE = """(function(){ var st=c2S(); st.e.sumire=1; st.e.herbBrief=1; SAVE.craft={}; SAVE.sc=SAVE.sc||{};
 SAVE.sc.pot='gather'; SAVE.sc.potGift=1; SAVE.sc.potLeaf=1; delete SAVE.sc.potHand; delete SAVE.sc.potGinger; delete SAVE.sc.potGranted;
 var hb=herbS(); hb.leaf=1; hb.ginger=1; save(); return 1; })()"""
PROBE = """(function(){ function r(e){ if(!e) return null; var b=e.getBoundingClientRect(); return [Math.round(b.x),Math.round(b.y),Math.round(b.width),Math.round(b.height)]; }
 var su=W.c2n&&W.c2n.sumire, d=document.getElementById('wdlg'), bt=document.getElementById('hsbot'), pr=document.getElementById('hspour'), bb=document.getElementById('wbub');
 var c=document.getElementById('hscmp'), cd=document.querySelector('.hscard');
 return {su: su&&su.el?r(su.el):null, sux: su?[Math.round(su.x),Math.round(su.y)]:null, bot: r(bt), botz: bt&&bt.style.zIndex, pour: r(pr), bub: bb&&bb.offsetParent?r(bb):null, bubTxt: bb?(bb.innerText||'').slice(0,20):null,
  dlg: d&&d.className?r(d):null, dlgc: d?d.className:null, cmp: c?r(c):null, card: cd?r(cd):null, ryo: W.ryo?r(W.ryo.el):null, cine: document.body.classList.contains('hscine'), dlgflag: !!W.dlg}; })()"""
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with h.Game(path='compassionate', out=OUT) as g:
        await g.boot(); print('room', await g.enter('clinic', 560, 640))
        await g.hush(); await g.ev(STATE); await g.ev("c2SumireD()"); await g.wait(900)
        await g.ev("(function(){var b=[...document.querySelectorAll('#wdlg button')].find(function(x){return /Teach me$/.test(x.textContent.trim())}); b.click(); return 1})()")
        log = []; i = 0
        for k in range(400):
            p = await g.ev(PROBE); p['t'] = k; log.append(p)
            if k % 3 == 0: await g.pg.screenshot(path=f'{OUT}/f{i:03d}.png'); i += 1
            c = await g.pg.evaluate(h.NX)
            if c and k % 4 == 3 and not p['cine'] is None: await g.pg.touchscreen.tap(*c)
            if await g.ev("!!(SAVE.craft&&SAVE.craft.potion)&&!W.dlg"): break
            await g.wait(120)
        json.dump(log, open(OUT + '/log.json', 'w'))
        print('frames', i, 'errs', g.errs[:5])
asyncio.run(main())
