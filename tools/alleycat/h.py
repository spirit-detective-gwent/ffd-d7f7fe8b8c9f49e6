import asyncio, sys, json, os
from playwright.async_api import async_playwright
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
HUSH = """(function(){try{if(typeof phClose==='function')phClose()}catch(e){}W.paused=false;W.dlg=false;W.cut=false;W.busy=false;W.path=[];var d=document.getElementById('wdlg');if(d){d.className='';d.innerHTML=''};return 1})()"""
SLOW = r'''(()=>{const P=performance.now.bind(performance), st=window.setTimeout.bind(window), si=window.setInterval.bind(window); let k=1, base=P(), vb=base;
 function vnow(){return vb+(P()-base)/k}
 window.__setSlow=function(f){const n=P(); vb=vnow(); base=n; k=f; return k};
 performance.now=vnow; window.setTimeout=function(fn,ms){var a=[].slice.call(arguments,2);return st(function(){fn.apply(null,a)},(+ms||0)*k)};
 window.setInterval=function(fn,ms){var a=[].slice.call(arguments,2);return si(function(){fn.apply(null,a)},(+ms||0)*k)};
 const raf=window.requestAnimationFrame.bind(window); window.requestAnimationFrame=function(cb){return raf(function(){cb(vnow())})};})()'''
def body(path):
    t = open(path, encoding='utf-8').read()
    assert 'root.FFF_13U = { CONTEST' in t
    t = t.replace('  function alleyCard(done) {', '  root.__alleyCard = function (d) { return alleyCard(d); }; function alleyCard(done) {', 1)  # harness-only hook
    return t.replace('root.FFF_13U = { CONTEST', 'root.__ev=function(s){return eval(s)};root.FFF_13U = { CONTEST', 1)
async def ev(pg, code):
    return await pg.evaluate("(c)=>{var r=window.__ev(c);try{return (typeof r==='string')?r:JSON.parse(JSON.stringify(r===undefined?null:r))}catch(e){return String(r)}}", code)
async def skipall(pg, n=6):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(250); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(300)
async def newpage(p, port, root, errs, save=None, video=None, gl=True, clock=False):
    args = ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required']
    b = await p.chromium.launch(args=args)
    kw = dict(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
    if video: kw['record_video_dir'] = video; kw['record_video_size'] = {'width': 390, 'height': 844}
    ctx = await b.new_context(**kw)
    pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
    if clock: await pg.add_init_script(SLOW)
    html = body(os.path.join(root, 'index.html'))
    async def rt(route): await route.fulfill(body=html, content_type='text/html')
    await pg.route('**/index.html', rt)
    await pg.goto(f'http://127.0.0.1:{port}/index.html'); await pg.wait_for_timeout(2500)
    if save is not None: await pg.evaluate("(c)=>localStorage.setItem('fff_world',c)", json.dumps(save))
    return b, ctx, pg
async def boot(pg, cont=False):
    await pg.touchscreen.tap(195, 420)
    await pg.evaluate("WORLD_API.enter(%s)" % ('true' if cont else 'false')); await pg.wait_for_timeout(1500); await skipall(pg); await ev(pg, HUSH)
    await ev(pg, "root.FFF_NO_TUT=1")
