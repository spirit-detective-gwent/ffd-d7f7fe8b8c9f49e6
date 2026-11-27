import asyncio, sys
sys.path.insert(0, '/workspace/alleycat/tools'); from h import *
async def main():
  async with async_playwright() as p:
    errs=[]; b,ctx,pg = await newpage(p, 8801, '/workspace/alleycat/wt', errs)
    await boot(pg)
    await pg.wait_for_timeout(2000)
    print(await ev(pg, "JSON.stringify({ch:SAVE.chapter,intro:SAVE.intro,roam:W.roam.length,inside:W.inside&&W.inside.id,ryo:[W.ryo.x|0,W.ryo.y|0],gsk:typeof gskLive==='function'?gskLive():'nf',ints:Object.keys(INT).slice(0,40)})"))
    await pg.screenshot(path='/tmp/p1.png'); print(errs[:5]); await b.close()
asyncio.run(main())
