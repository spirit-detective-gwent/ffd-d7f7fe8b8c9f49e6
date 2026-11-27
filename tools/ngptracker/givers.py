#!/workspace/pwenv/bin/python3
"""Are the Ch1 side-quest givers there and offering (!) in NG+? intGo each giver room, list npc sprites + mark, run the offer and Accept."""
import asyncio, sys, json; sys.path.insert(0, '/workspace/ngptracker/tools'); import h, repro_lib as R
INDEX, MODE = sys.argv[1], sys.argv[2]
async def main():
    async with h.Game(INDEX) as g:
        await R.setup(g, MODE)
        for room, npc, sq in [('hall', 'kenta', 'sq_kenta'), ('hall', 'yuto', 'sq_yuto'), ('cmus', 'ayaf', 'sq_aya'), ('c1a', 'rikuf', 'sq_riku')]:
            await g.ev("try{ if(W.inside) intExit(true) }catch(e){}; 1"); await g.wait(600)
            r = await g.ev("(function(){ try{ intGo('%s') }catch(e){ return 'err '+e.message } return W.inside&&W.inside.id })()" % room); await g.wait(1500); await g.hush()
            npcs = await g.ev("[...document.querySelectorAll('[data-npc]')].map(function(e){return e.dataset.npc})")
            mk = await g.ev("sqMarkKind('%s'.replace(/f$/,''))" % npc)
            # run the talk on that sprite and press Accept
            t = await g.ev("(function(){ var e=[...document.querySelectorAll('[data-npc]')].filter(function(x){return x.dataset.npc==='%s'||x.dataset.npc==='%s'.replace(/f$/,'')})[0]; if(!e) return 'nosprite'; var s={el:e}; return String(sqTalk(e.dataset.npc, s)) })()" % (npc, npc))
            for _ in range(14):
                await g.wait(300)
                c = await g.pg.evaluate("""()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^(Accept|Next|Skip)/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var a=b.find(e=>/^Accept/.test(e.textContent.trim()))||b[0];var r=a.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}""")
                if c: await g.pg.touchscreen.tap(*c)
            print(room, r, npc, 'sprites', npcs, 'mark', mk, 'talk', t, 'st', await g.ev("sqState('%s').st" % sq), flush=True)
            await g.hush()
        print('errs', g.errs[:5])
asyncio.run(main())
