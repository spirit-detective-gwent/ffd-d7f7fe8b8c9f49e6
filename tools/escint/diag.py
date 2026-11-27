#!/workspace/pwenv/bin/python3
"""diag: dump world flags after escape vs win. usage: diag.py <worktree> [port]"""
import asyncio, sys, json
sys.argv_orig = list(sys.argv)
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import harness as tl
ROOT = sys.argv_orig[1]; PORT = int(sys.argv_orig[2]) if len(sys.argv_orig) > 2 else 53711
FLAGS = """(function(){var o={};['on','runUp','busy','dlg','pan','cut','scr','forced','paused','fading','lying','cool','safe','ambT','ambOn','opnOn','dgFight','g5busy','g38Gating','c2busy','fldCine','inside','libPend','roamT','ambNext','g38gp'].forEach(function(k){var v=W[k];o[k]=(v&&typeof v==='object')?'obj':v});
 o.tagsLive=tagsLive(); o.game=document.getElementById('game').className; o.result=document.getElementById('result').className;
 o.stInGame=FFF_UI.ST.inGame; o.stBusy=FFF_UI.ST.busy; o.stInWorld=FFF_UI.ST.inWorld; o.story=!!FFF_UI.ST.story; o.worldCls=document.getElementById('world').className;
 var e=document.elementFromPoint(195,422); o.top=e&&(e.id||e.className||e.tagName);
 return o})()"""
async def main():
    h = tl.serve(ROOT, PORT)
    async with tl.async_playwright() as p:
        b, ctx, pg, errs = await tl.boot(p, PORT)
        await tl.ch1_ready(pg)
        print('BASE', json.dumps(await tl.ev(pg, FLAGS)))
        for label, how in (('escape', 'esc'), ('win', 'win'), ('lose', 'lose')):
            await tl.ev(pg, "window.FFF_ESC_ROLL=0")
            await tl.ev(pg, "WORLD_API.fightX(['bully1'],{flv:1})")
            await pg.wait_for_timeout(4500)
            print(label, 'IN FIGHT', json.dumps(await tl.ev(pg, "({ig:FFF_UI.ST.inGame,ph:FFF_UI.ST.phase,esc:FFF_UI.ST.story&&FFF_UI.ST.story.esc,busy:FFF_UI.ST.busy})")))
            await tl.ev(pg, "FFF_UI.ST.busy=false")
            if how == 'esc':
                await tl.ev(pg, "FFF_UI.tapRun&&0")
                await pg.evaluate("document.getElementById('btnRun').click()")
                await pg.wait_for_timeout(2500)
            await pg.wait_for_timeout(500)
            print(label, json.dumps(await tl.ev(pg, FLAGS)))
            if how != 'esc': break
        print('errs', errs)
        await b.close()
asyncio.run(main())
