#!/usr/bin/env python3
"""perf (alley cat): grounds, plain battle, Alley-Cat downed-opening battle, a takedown window. usage: perf_sb.py INDEX LABEL OUTJSON. spots: grounds walk (key spot), single battle, 3v battle, Gouki finale. 1x fps + 4x fps/heat, heap after GC."""
import asyncio, sys, json, functools, http.server, socketserver, threading
from pathlib import Path
from playwright.async_api import async_playwright
INDEX=Path(sys.argv[1]).resolve(); LABEL=sys.argv[2]; OUT=sys.argv[3]
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
s=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(Q,directory=str(INDEX.parent))); s.daemon_threads=True
threading.Thread(target=s.serve_forever,daemon=True).start(); PORT=s.server_address[1]
html=INDEX.read_text(encoding='utf-8').replace('root.FFF_13U = { CONTEST','root.__ev=function(s){return eval(s)};root.FFF_13U = { CONTEST',1)
SAMP="()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);}"
async def ev(pg,c): return await pg.evaluate("(c)=>{var r=window.__ev(c);try{return JSON.parse(JSON.stringify(r===undefined?null:r))}catch(e){return String(r)}}",c)
async def met(cdp): m=await cdp.send('Performance.getMetrics'); return {x['name']:x['value'] for x in m['metrics']}
async def win(pg,cdp,secs):
    await pg.evaluate(SAMP); m0=await met(cdp); await pg.wait_for_timeout(int(secs*1000)); m1=await met(cdp)
    await pg.evaluate("window.__run=false"); ft=(await pg.evaluate("window.__ft"))[2:]
    wall=m1['Timestamp']-m0['Timestamp']
    return dict(fps=round(1000*len(ft)/sum(ft),1) if ft else 0, heat=round(100*(m1['TaskDuration']-m0['TaskDuration'])/wall,1))
SK="""()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
HUSH="""(function(){try{if(typeof phClose==='function')phClose()}catch(e){}W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};return 1})()"""
async def spot(pg,cdp,res,name):
    await cdp.send('Emulation.setCPUThrottlingRate',{'rate':1}); a=await win(pg,cdp,5)
    await cdp.send('Emulation.setCPUThrottlingRate',{'rate':4}); b=await win(pg,cdp,6)
    await cdp.send('Emulation.setCPUThrottlingRate',{'rate':1})
    res[name]=dict(fps1=a['fps'],fps4=b['fps'],heat4=b['heat']); print(name,res[name],flush=True)
async def battle(pg,foes,boss,cx='{_ru:1}'):
    await ev(pg,"(function(){W.fightT=0;fight(%s,%s,%s);return 1})()"%(json.dumps(foes),'true' if boss else 'false',cx))
    for i in range(40):
        await pg.wait_for_timeout(500)
        if await pg.evaluate("()=>{var S=FFF_UI.ST;return !!(S.b&&S.phase==='mull')}"): break
    await pg.wait_for_timeout(500)
    if 'acDown' not in cx: await pg.evaluate("()=>document.getElementById('btnAct').click()")
    await pg.wait_for_timeout(3000)
    return await pg.evaluate("()=>document.querySelectorAll('#fE .sbico, #foeRow .sbico').length")
async def leave(pg):
    await ev(pg,"(function(){try{var S=FFF_UI.ST;S.b.over=1;}catch(e){}return 1})()")
async def main():
    res={'label':LABEL}
    async with async_playwright() as p:
        br=await p.chromium.launch(args=['--use-gl=swiftshader','--enable-unsafe-swiftshader'])
        ctx=await br.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=int(__import__('os').environ.get('DPR','3')))
        pg=await ctx.new_page(); cdp=await ctx.new_cdp_session(pg); await cdp.send('Performance.enable')
        async def rt(route): await route.fulfill(body=html,content_type='text/html')
        await pg.route('**/index.html',rt)
        await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(2500)
        await pg.touchscreen.tap(195,420); await pg.evaluate("WORLD_API.enter(false)"); await pg.wait_for_timeout(1500)
        for i in range(6):
            c=await pg.evaluate(SK)
            if not c: break
            await pg.touchscreen.tap(*c); await pg.wait_for_timeout(300)
        await ev(pg,HUSH); await ev(pg,"root.FFF_NO_TUT=1")
        await ev(pg,"(function(){var S=SAVE;S.intro=1;S.chapter=1;W.tut=0;S.bond=S.bond||{};S.bond.path='fierce';S.bond.px=600;S.bond.lock=1;S.bond.ask=1;S.ngp=1;S.c2les={assist:1,sneak:1,cover:1};save();return 1})()")
        await pg.wait_for_timeout(1500)
        await spot(pg,cdp,res,'grounds')
        await cdp.send('HeapProfiler.collectGarbage'); res['heap0']=round((await met(cdp))['JSHeapUsedSize']/1e6,2)
        # one page per battle kind to keep it simple: reload between
        for nm,foes,boss,cx in [('battle1',['bully2'],False,'{_ru:1}'),('acbattle',['bully1'],False,"{_ru:1,amb:{k:0.62,side:'back'},acDown:1,opnAc:1}")]:
            await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(2500)
            await pg.touchscreen.tap(195,420); await pg.evaluate("WORLD_API.enter(false)"); await pg.wait_for_timeout(1500)
            for i in range(6):
                c=await pg.evaluate(SK)
                if not c: break
                await pg.touchscreen.tap(*c); await pg.wait_for_timeout(300)
            await ev(pg,HUSH); await ev(pg,"root.FFF_NO_TUT=1")
            res[nm+'_icons']=await battle(pg,foes,boss,cx)
            res[nm+'_pose']=await pg.evaluate("()=>!!document.querySelector('.kopose.acdown, #eFig.ac-down')")
            await spot(pg,cdp,res,nm)
            await cdp.send('HeapProfiler.collectGarbage'); res[nm+'_heap']=round((await met(cdp))['JSHeapUsedSize']/1e6,2)
        await br.close()
    json.dump(res,open(OUT,'w')); print('RES',json.dumps(res))
asyncio.run(main())
