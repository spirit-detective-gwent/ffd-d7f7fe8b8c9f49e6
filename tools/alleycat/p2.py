import asyncio, sys
sys.path.insert(0, '/workspace/alleycat/tools'); from h import *
async def main():
  async with async_playwright() as p:
    errs=[]; b,ctx,pg = await newpage(p, 8801, '/workspace/alleycat/wt', errs)
    await boot(pg)
    await ev(pg, "SAVE.intro=1;SAVE.ngp=1;SAVE.gsk={alley:1};W.tut=false;1")
    for room in ['dl_hall','dl_stacks','dl_foyer']:
      await ev(pg, "intGo('%s');1"%room); await pg.wait_for_timeout(2500); await ev(pg, HUSH)
      print(room, await ev(pg, "JSON.stringify({inside:W.inside&&W.inside.id,dgF:(W.dgF||[]).map(q=>[q.id,q.s.x|0,q.s.y|0,q.st,(q.fa||0).toFixed(2)]),ryo:[W.ryo.x|0,W.ryo.y|0],gsk:gskLive(),ctx:ambCtxOk()})"))
      await pg.screenshot(path='/tmp/p2_%s.png'%room)
    print(errs[:5]); await b.close()
asyncio.run(main())
