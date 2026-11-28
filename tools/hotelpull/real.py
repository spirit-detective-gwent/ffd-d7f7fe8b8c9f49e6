import asyncio
FORCE = "(function(){var b=FFF_UI.ST.b; if(!b) return 'nob'; (b.grp||[]).forEach(function(s){s.hp=0}); if(b.s[1]) b.s[1].hp=0; b.over=true; b.winner=0; FFF_UI.endMatch(); return 1})()"
async def real_win(g, max_ms=15000):
    """win the open battle through the real end path: endMatch, the victory cine, the result, the map button"""
    for i in range(40):
        if await g.ev("!!(FFF_UI.ST && FFF_UI.ST.inGame && FFF_UI.ST.b && !FFF_UI.ST.b.over && FFF_UI.ST.phase!=='mull')"): break
        await g.skipall(1); await g.wait(250)
    await g.wait(300)
    print('  force', await g.ev(FORCE))
    t = 0
    while t < max_ms:
        st = await g.ev("({over:!!(typeof VC!=='undefined'&&VC&&VC.over), on:document.getElementById('result').classList.contains('on'), game:document.getElementById('game').classList.contains('on'), w:!!(W&&W.on)})")
        if not st['game'] and not st['on'] and st['w']: return 'world'
        if st['on']:
            b = await g.pg.evaluate("()=>{var b=document.getElementById('rMap'); if(!b) return null; var r=b.getBoundingClientRect(); return r.width?[r.x+r.width/2,r.y+r.height/2]:null}")
            if b: await g.pg.touchscreen.tap(*b)
        await g.ev("if (typeof VC!=='undefined' && VC && VC.tap) VC.tap()")
        await g.wait(250); t += 250
    return 'timeout'
