#!/workspace/pwenv/bin/python3
import asyncio, sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import h
async def main():
    async with h.Game(path='compassionate', out='/workspace/herbcine/shots/scratch') as g:
        await g.boot(); await g.go('clinic', 640, 520); await g.wait(1200)
        print(await g.ev("""(function(){ var su=W.c2n.sumire, e=su.el, r=W.ryo.el; var D=INT.clinic||{}; var sp=(c2Room()==='clinic'&&typeof C2W!=='undefined')?1:0;
          var cs=getComputedStyle(e);
          var o={S:W.S,cam:[W.cam.x,W.cam.y],vw:W.vw,vh:W.vh, suXY:[su.x,su.y], off:[e.offsetWidth,e.offsetHeight,e.style.left,e.style.top,e.style.width,e.style.height], tr:e.style.transform, ryo:[W.ryo.x,W.ryo.y,r.offsetWidth,r.offsetHeight,r.style.transform], kids:[].map.call(e.children,function(c){return c.tagName+'.'+c.className}), flip:cs.scale||'', bgpos:e.style.backgroundPosition}; return JSON.stringify(o)})()"""))
        print(await g.ev("""(function(){var f=c2Room(); var s=null; try{ s=(window.__c2spots||null) }catch(e){} return JSON.stringify([f, Object.keys(W.c2n)])})()"""))
        print(await g.ev("""JSON.stringify((W.tagL||[]).filter(function(t){return /clinic/.test(t.key)}).map(function(t){return [t.key,t.lab,t.x,t.y,t.ax,t.ay,t.R,!!t.obj, !!t.silent]}))"""))
        print(await g.ev("""JSON.stringify(typeof c2Walk==='function'? c2Walk.toString().slice(0,900):null)"""))
        print(await g.ev("""JSON.stringify(typeof c2WalkAll==='function'? c2WalkAll.toString().slice(0,900):null)"""))
asyncio.run(main())
