import asyncio, sys, json
sys.path.insert(0, '/workspace/alleycat/tools'); from h import *
async def main():
  async with async_playwright() as p:
    errs=[]; b,ctx,pg = await newpage(p, 8801, '/workspace/alleycat/wt', errs, save=json.load(open('/workspace/alleycat/tools/save_c1.json')))
    await pg.reload(); await pg.wait_for_timeout(2500)
    pg.on('console', lambda m: print('CON', m.text[:200]) if 'alley' in m.text else None)
    await boot(pg, cont=True)
    await ev(pg, "clearRoam();1")
    await ev(pg, "fight(['bully1'], false, {amb:{k:0.62,side:'back'}, acDown:1, opnAc:1, place:'x'});1")
    await pg.wait_for_timeout(3000)
    print(await pg.evaluate("(()=>{var k=[...document.querySelectorAll('.kopose,.koshadow')].map(e=>[e.className,e.style.left,e.style.top,e.style.width,e.style.height,(e.src||'').slice(-40)]);var fb=document.querySelector('#fE .fbody');return JSON.stringify({k:k,fb:fb&&[fb.style.opacity,fb.getBoundingClientRect().top],down:fb&&fb.closest('.fighter').dataset.down})})()"))
    await pg.screenshot(path='/tmp/p3.png'); print(errs[:5]); await b.close()
asyncio.run(main())
