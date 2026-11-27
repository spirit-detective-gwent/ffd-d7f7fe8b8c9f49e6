#!/workspace/pwenv/bin/python3
"""After an escape, stand still / walk for a while and sample the input-lock flags. usage: soak.py <worktree> <port> <scenario> [secs]"""
import sys, json, asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import harness as H
import scen
ROOT=sys.argv[1]; PORT=int(sys.argv[2]); NAME=sys.argv[3]; SECS=int(sys.argv[4]) if len(sys.argv)>4 else 25
SAMPLE = """(function(){var f=W.forced;return {t:Math.round(W.t||0),forced:f?{id:f.id,st:f.st,ft:+(f.ft||0).toFixed(1),inRoam:W.roam.indexOf(f)>=0}:null,busy:W.busy,dlg:W.dlg,cut:W.cut,runUp:W.runUp,fading:W.fading,ambOn:!!W.ambOn,live:tagsLive(),ig:FFF_UI.ST.inGame,roam:W.roam.map(function(q){return q.st}).join(',')}})()"""
async def main():
    H.serve(ROOT, PORT)
    async with H.async_playwright() as p:
        b, ctx, pg, errs = await H.boot(p, PORT)
        await H.ch1_ready(pg, 1800, 3000); await H.ev(pg, scen.MK); await H.ev(pg, "window.FFF_ESC_ROLL=0")
        await H.ev(pg, scen.SCEN[NAME])
        for i in range(80):
            await pg.wait_for_timeout(250)
            s = await H.ev(pg, "(function(){var r=document.getElementById('btnRun');return {ig:FFF_UI.ST.inGame,busy:FFF_UI.ST.busy,ph:FFF_UI.ST.phase,hid:r&&r.hidden,dis:r&&r.disabled}})()")
            if s.get('ig') and not s.get('hid') and not s.get('dis') and s.get('ph')=='play' and not s.get('busy'): break
            await H.ev(pg, "if(window.FFF_WAVE&&document.getElementById('fwvB'))FFF_WAVE.stop()")
        await pg.wait_for_timeout(1200)
        c = await pg.evaluate("()=>{var r=document.getElementById('btnRun').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}")
        await pg.touchscreen.tap(*c)
        for i in range(SECS*2):
            await pg.wait_for_timeout(500)
            print(json.dumps(await H.ev(pg, SAMPLE)), flush=True)
        print('errs', errs[:3]); await b.close()
asyncio.run(main())
