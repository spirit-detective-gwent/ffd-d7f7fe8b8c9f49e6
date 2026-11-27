#!/workspace/pwenv/bin/python3
"""probe: Gouki first-KO flow on Fierce, fresh vs NG+. usage: probe.py <tree> <port> [ngp]"""
import sys, asyncio, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'escint')); import harness as H
ROOT, PORT = sys.argv[1], int(sys.argv[2]); NGP = len(sys.argv) > 3 and sys.argv[3] == 'ngp'
SET = """(function(){var B=STORY.bond(SAVE);B.path='fierce';B.picks=B.picks||{};B.picks.dg_gouki='fierce';B.px=Math.max(B.px|0,STORY.bondTot?0:0);
var l=1;while(STORY.bondLv(SAVE)<5&&l<200){B.px=(B.px|0)+50;l++}
SAVE.gouki=0;SAVE.ch1=0;SAVE.gkPh=0;SAVE.gkRevives=0;SAVE.dbl=0;SAVE.ngp=NGP;delete gearS().own.ofuda;save();return {lv:STORY.bondLv(SAVE),gate:gearGate('ofuda')}})()"""
WIN = "(function(){var b=FFF_UI.ST.b;(b.grp||[]).forEach(function(s){s.hp=0});if(b.s[1])b.s[1].hp=0;b.over=true;b.winner=0;FFF_UI.endMatch();return 1})()"
async def main():
    H.serve(ROOT, PORT)
    async with H.async_playwright() as p:
        b, ctx, pg, errs = await H.boot(p, PORT)
        await H.ch1_ready(pg, 1440, 3300)
        print('set', await H.ev(pg, SET.replace('NGP', '1' if NGP else '0')))
        await H.ev(pg, "FFF_UI.ST.events.length=0; gkFight(); 1")
        for i in range(40):
            await pg.wait_for_timeout(500)
            if await H.ev(pg, "!!(FFF_UI.ST.inGame&&FFF_UI.ST.b&&FFF_UI.ST.phase==='play')"): break
        print('ctx', await H.ev(pg, "JSON.stringify(FFF_UI.ST.story&&FFF_UI.ST.story.ctx)"))
        await H.ev(pg, WIN)
        for i in range(30):
            await pg.wait_for_timeout(500)
            gf = await H.ev(pg, "!!document.querySelector('#gfind.on')")
            if gf: print('GFIND popup at', i); break
        await pg.wait_for_timeout(1500)
        print('events', [e for e in (await H.ev(pg, "FFF_UI.ST.events.slice()")) if any(k in e for k in ('gouki', 'gear', 'gk', 'story:end', 'chapter', 'ending'))])
        print('save', await H.ev(pg, "({gouki:SAVE.gouki,gkPh:SAVE.gkPh,rev:SAVE.gkRevives,ofuda:!!gearS().own.ofuda,ig:FFF_UI.ST.inGame,ctx:JSON.stringify(FFF_UI.ST.story&&FFF_UI.ST.story.ctx)})"))
        await pg.screenshot(path=f'/workspace/ofuda/probe_{"ngp" if NGP else "fresh"}.png')
        print('errs', errs[:3]); await b.close()
asyncio.run(main())
