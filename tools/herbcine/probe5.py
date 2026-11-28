#!/workspace/pwenv/bin/python3
import asyncio, sys, json, os, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import h
async def main():
    async with h.Game(path='compassionate', out='/workspace/herbcine/shots/scratch') as g:
        await g.boot(); await g.go('clinic', 640, 520); await g.wait(1200)
        u = await g.ev("(function(){var e=W.c2n.sumire.el; return [e.style.backgroundImage.slice(0,60), IMG.tsukikage_idle? IMG.tsukikage_idle.slice(0,40):null, Object.keys(IMG).filter(function(k){return /tsukikage/.test(k)}).join(',')]})()")
        print(u)
        for k in ['tsukikage_idle']:
            d = await g.ev("IMG.%s" % k)
            if d and d.startswith('data:'):
                b = base64.b64decode(d.split(',',1)[1]); open('/workspace/herbcine/shots/scratch/%s.png'%k,'wb').write(b); print(k,len(b))
asyncio.run(main())
