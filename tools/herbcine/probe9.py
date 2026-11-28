#!/workspace/pwenv/bin/python3
import asyncio, sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import h
ST = "JSON.stringify({on:FFF_SCAM.st.on,heavy:FFF_SCAM.st.heavy,soft:FFF_SCAM.st.soft,keep:FFF_SCAM.st.keep,still:FFF_SCAM.still(), tf:(document.getElementById('wv')||{}).style&&document.getElementById('wv').style.transform, sc:getComputedStyle(document.getElementById('wv')).scale, tr:getComputedStyle(document.getElementById('wv')).translate})"
async def main():
    async with h.Game(path='compassionate', out='/workspace/herbcine/shots/scratch') as g:
        await g.boot(); await g.enter('clinic', 560, 640)
        print('start', await g.ev(ST))
        await g.ev("hsCineSetup(function(){ window.__s1=1 }); 1")
        for i in range(100):
            if await g.ev("!!window.__s1"): break
            await g.wait(200)
        print('after setup', await g.ev(ST))
        await g.ev("hsCineBrew(function(){ window.__s2=1 }); 1")
        for i in range(400):
            if await g.ev("!!window.__s2"): break
            await g.wait(200)
        print('after brew', await g.ev(ST))
        await g.ev("hsCineHand(function(){ window.__s3=1 }); 1")
        for i in range(400):
            if await g.ev("!!window.__s3"): break
            await g.wait(200)
        print('after hand', await g.ev(ST))
        await g.ev("scene(null,[['ryo','It is warm.']],function(){}); 1"); await g.wait(1200)
        print('after line', await g.ev(ST))
asyncio.run(main())
