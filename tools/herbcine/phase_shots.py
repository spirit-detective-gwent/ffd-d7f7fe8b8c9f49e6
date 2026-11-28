#!/workspace/pwenv/bin/python3
"""Drive one cinematic phase directly (no dialogue) and shoot a clip of the pot area every step. PHASE=brew|hand|back  OUT=dir"""
import asyncio, sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import h
PHASE = os.environ.get('PHASE', 'brew'); OUT = os.environ.get('OUT', '/workspace/herbcine/shots/ph_' + PHASE)
async def clip_of(g):
    # screen rect around world box (x0,y0,x1,y1) given by env
    x0, y0, x1, y1 = [float(v) for v in os.environ.get('BOX', '560,380,730,500').split(',')]
    r = await g.ev("""(function(){ var L=document.getElementById('wisp')||layer; function p(x,y){var e=document.createElement('i'); e.style.cssText='position:absolute;width:1px;height:1px;left:'+x+'px;top:'+y+'px'; L.appendChild(e); var b=e.getBoundingClientRect(); e.remove(); return [b.x,b.y]} return [p(%s,%s), p(%s,%s)] })()""" % (x0, y0, x1, y1))
    return {'x': max(0, r[0][0]), 'y': max(0, r[0][1]), 'width': r[1][0] - r[0][0], 'height': r[1][1] - r[0][1]}
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with h.Game(path='compassionate', out=OUT) as g:
        await g.boot(); await g.enter('clinic', 560, 640)
        await g.ev("(function(){var st=c2S(); st.e.sumire=1; SAVE.craft={}; return 1})()")
        await g.ev("hsCineSetup(function(){ window.__s1=1 }); 1")
        for i in range(200):
            if await g.ev("!!window.__s1"): break
            await g.wait(200)
        await g.hush()
        if PHASE == 'brew':
            await g.ev("hsCineBrew(function(){ window.__s2=1 }); 1")
            flag = '__s2'
        else:
            await g.ev("hsCineBrew(function(){ window.__s2=1 }); 1")
            for i in range(400):
                if await g.ev("!!window.__s2"): break
                await g.wait(200)
            await g.wait(300)
            if PHASE == 'hand':
                await g.ev("hsCineHand(function(){ window.__s3=1 }); 1"); flag = '__s3'
            else:
                await g.ev("hsCineHand(function(){ window.__s3=1 }); 1")
                for i in range(400):
                    if await g.ev("!!window.__s3"): break
                    await g.wait(200)
                await g.ev("hsCineBack(function(){ window.__s4=1 }); 1"); flag = '__s4'
        log = []
        for i in range(400):
            clip = await clip_of(g)
            await g.pg.screenshot(path=f'{OUT}/p{i:03d}.png', clip=clip)
            if await g.ev(f"!!window.{flag}"): break
            await g.wait(int(os.environ.get('STEP', '120')))
        print('frames', i, 'errs', g.errs[:5])
asyncio.run(main())
