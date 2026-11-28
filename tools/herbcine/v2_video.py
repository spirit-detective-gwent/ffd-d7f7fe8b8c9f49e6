#!/workspace/pwenv/bin/python3
"""Record a 390x844 clip: tap a pot (Ryo walks over and plants), then the ladle pour and the low-waist carry. VID=dir for the webm."""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import h
VID = os.environ.get('VID', '/workspace/herbcine/shots/v2vid')
os.makedirs(VID, exist_ok=True); os.environ['VID'] = VID
STATE = """(function(){ var st=c2S(); st.e.sumire=1; st.e.herbBrief=1; st.e.gardenIntro=1; st.e.gingerIntro=1;
 SAVE.craft={potion:1}; SAVE.sc=SAVE.sc||{}; SAVE.sc.pot='gather'; SAVE.sc.potGift=1; SAVE.sc.potLeaf=1;
 delete SAVE.sc.potHand; delete SAVE.sc.potGinger; delete SAVE.sc.potGranted;
 var hb=herbS(); hb.leaf=1; hb.ginger=1; herbAdd('seed', 9); save(); return 1; })()"""
LESSON = """(function(){ var st=c2S(); st.e.sumire=1; st.e.herbBrief=1; SAVE.craft={}; SAVE.sc=SAVE.sc||{};
 SAVE.sc.pot='gather'; SAVE.sc.potGift=1; SAVE.sc.potLeaf=1; delete SAVE.sc.potHand; delete SAVE.sc.potGinger; delete SAVE.sc.potGranted;
 var hb=herbS(); hb.leaf=1; hb.ginger=1; save(); return 1; })()"""
async def w2s(g, x, y):
    return await g.ev(f"(function(){{var e=document.createElement('i'); e.style.cssText='position:absolute;width:1px;height:1px;left:{x}px;top:{y}px'; (document.getElementById('wisp')||layer).appendChild(e); var b=e.getBoundingClientRect(); e.remove(); return [b.x,b.y]}})()")
async def main():
    async with h.Game(path='compassionate', out=VID) as g:
        await g.boot(); await g.enter('clinic', 560, 640)
        await g.ev("W.scr=0;W.cut=0;1"); await g.hush(); await g.ev(STATE)
        # stand off to the south-west of gp5, camera on the garden
        px, py = 298, 296
        await g.ev(f"(function(){{c2Cyc().pots.gp5.st='empty'; W.busy=false; W.dlg=false; W.path=[]; W.arrive=null; W.ryo.x={px-80}; W.ryo.y={py+80}; W.ryo.v=0; place(W.ryo,0); if(W.aoi){{W.aoi.x={px-140}; W.aoi.y={py+90}; place(W.aoi,0)}} camera(true); return 1}})()")
        await g.wait(900)
        sx, sy = await w2s(g, px, py - 20)
        await g.pg.touchscreen.tap(sx, sy)
        # wait for the walk + plant to finish
        for i in range(80):
            st = await g.ev("[c2Cyc().pots.gp5.st, !!W.busy, W.ryo.x|0, W.ryo.y|0]")
            if st[0] == 'planted' and not st[1]: break
            await g.wait(200)
        await g.wait(700)
        # now the lesson: pour + low carry. Reset craft so Teach me is offered.
        await g.hush(); await g.ev(LESSON); await g.ev("c2Go('clinic',[560,640,0]); W.scr=0;W.cut=0;1")
        # natural enter standing
        await g.ev("(function(){W.ryo.x=560; W.ryo.y=640; place(W.ryo,0); if(W.aoi){W.aoi.x=490; W.aoi.y=670; place(W.aoi,0)} camera(true); return 1})()")
        await g.wait(600)
        await g.ev("c2SumireD()"); await g.wait(900)
        await g.ev("(function(){var b=[...document.querySelectorAll('#wdlg button')].find(function(x){return /Teach me$/.test(x.textContent.trim())}); if(b)b.click(); return 1})()")
        for k in range(900):
            c = await g.pg.evaluate(h.NX)
            if c and k % 4 == 0: await g.pg.touchscreen.tap(*c)
            # stop a beat after the hand-off (Ryo holds the bottle) once the compare card is up, or when she has walked back
            done = await g.ev("!!(SAVE.craft&&SAVE.craft.potion)&&!W.dlg&&!(window.HS&&HS.on)")
            mid = await g.ev("(function(){var b=document.getElementById('hsbot'); return !!(b && b.parentNode===W.ryo.el && document.getElementById('hscmp'))})()")
            if mid:
                await g.wait(800); break
            if done: break
            await g.wait(80)
        await g.wait(400)
        path = await g.pg.video.path()
        await g.pg.close()
        print('webm', path, flush=True)
        open(os.path.join(VID, 'webm.path'), 'w').write(str(path))
asyncio.run(main())
