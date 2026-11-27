#!/usr/bin/env python3
"""Sync Break in Ch1. usage: t_sb.py INDEX PORT MODE(ngp|first|noNgpAssist) FOES(comma; 'gouki' = boss finale) SHOT [brk]"""
import asyncio, sys, json, functools, http.server, socketserver, threading
from pathlib import Path
from playwright.async_api import async_playwright
INDEX=Path(sys.argv[1]).resolve(); PORT=int(sys.argv[2]); MODE=sys.argv[3]; FOES=sys.argv[4].split(','); SHOT=sys.argv[5]; BRK=len(sys.argv)>6 and sys.argv[6]
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address=True; daemon_threads=True
s=TS(('127.0.0.1',PORT),functools.partial(Q,directory=str(INDEX.parent))); threading.Thread(target=s.serve_forever,daemon=True).start()
html=INDEX.read_text(encoding='utf-8').replace('root.FFF_13U = { CONTEST','root.__ev=function(s){return eval(s)};root.FFF_13U = { CONTEST',1)
async def ev(pg,c): return await pg.evaluate("(c)=>{var r=window.__ev(c);try{return JSON.parse(JSON.stringify(r===undefined?null:r))}catch(e){return String(r)}}",c)
SK="""()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
HUSH="""(function(){try{if(typeof phClose==='function')phClose()}catch(e){}W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};return 1})()"""
SETUP={'ngp':"S.ngp=1;S.c2les={assist:1,sneak:1,cover:1};",'first':"S.ngp=0;delete S.c2les;",'noNgpAssist':"S.ngp=0;S.c2les={assist:1,sneak:1,cover:1};",'ch2':"S.ngp=0;S.c2les={assist:1,sneak:1,cover:1};S.chapter=2;"}[MODE]
async def main():
    errs=[]
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-gl=swiftshader','--enable-unsafe-swiftshader'])
        ctx=await b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=2)
        pg=await ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        async def rt(route): await route.fulfill(body=html,content_type='text/html')
        await pg.route('**/index.html',rt)
        await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(2500)
        await pg.touchscreen.tap(195,420); await pg.evaluate("WORLD_API.enter(false)"); await pg.wait_for_timeout(1500)
        for i in range(6):
            c=await pg.evaluate(SK)
            if not c: break
            await pg.touchscreen.tap(*c); await pg.wait_for_timeout(300)
        await ev(pg,HUSH); await ev(pg,"root.FFF_NO_TUT=1")
        await ev(pg,"(function(){var S=SAVE;S.intro=1;S.chapter=1;W.tut=0;S.bond=S.bond||{};S.bond.path='fierce';S.bond.px=600;S.bond.lock=1;S.bond.ask=1;"+SETUP+"save();return 1})()")
        boss=FOES==['gouki']
        await ev(pg,"fight(%s,%s,{_ru:1})"%(json.dumps(FOES),'true' if boss else 'false'))
        for i in range(40):
            await pg.wait_for_timeout(500)
            ph=await pg.evaluate("()=>{var S=FFF_UI.ST;return S.b&&S.phase}")
            if ph=='mull': break
        await pg.wait_for_timeout(600)
        await pg.evaluate("()=>document.getElementById('btnAct').click()")
        await pg.wait_for_timeout(2500)
        info=await pg.evaluate("""()=>{var S=FFF_UI.ST,b=S.b,E=ENGINE;return {phase:S.phase,turn:b.turn,sync:!!b.sync,sbC1:!!b.sbC1,bench:b.bench&&b.bench.ch,me:b.s[0].ch,
          foes:(b.grp||[b.s[1]]).map(s=>[s.ch,E.sbType(b,s),E.sbBoss?E.sbBoss(b,s.ch):!!E.SB_BOSS[s.ch]]),
          icons:[...document.querySelectorAll('#fE .sbico, #foeRow .sbico')].map(e=>e.dataset.t)}}""")
        print('INFO',json.dumps(info))
        import os
        if os.environ.get('PROBE'): print('PROBE',json.dumps(await pg.evaluate(os.environ['PROBE'])))
        if os.environ.get('CSS'): await pg.add_style_tag(content=os.environ['CSS']); await pg.wait_for_timeout(300)
        if BRK:
            # wait for player's turn, then Ryo guard-breaks a guarding G foe
            for i in range(30):
                t=await pg.evaluate("()=>{var S=FFF_UI.ST;return S.b.turn===0&&!S.busy}")
                if t: break
                await pg.wait_for_timeout(500)
            r=await pg.evaluate("""()=>{var S=FFF_UI.ST,b=S.b;if(b.s[0].ch!=='ryo')return 'not ryo';var op=b.s[1];op.guard=4;
              var c=b.s[0].hand[0];c.id='r_guard';c.t='atk';c.v=3;c.pierce=1;c.brk=4;c.n='Guard Breaker';delete c.hits;S.sel=c.u;S.combo=[];FFF_UI.render(false);return FFF_UI.playCommit()}""")
            print('PLAY',r)
            for i in range(20):
                await pg.wait_for_timeout(500)
                w=await pg.evaluate("()=>{var b=FFF_UI.ST.b;return b.sbWin?JSON.parse(JSON.stringify(b.sbWin)):null}")
                if w and w.get('shown'): break
            await pg.wait_for_timeout(400)
            print('SBWIN',json.dumps(w), 'sbN',await pg.evaluate("()=>FFF_UI.ST.b.sbN|0"), 'btnSw',await pg.evaluate("()=>document.getElementById('btnSw').innerText"))
        await pg.screenshot(path=SHOT)
        print('ERRS',errs[:5])
        await b.close()
asyncio.run(main())
