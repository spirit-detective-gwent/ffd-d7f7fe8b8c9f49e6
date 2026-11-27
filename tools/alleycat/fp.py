import asyncio, sys, base64
sys.path.insert(0, '/workspace/alleycat/tools'); from h import *
async def main():
  async with async_playwright() as p:
    errs=[]; b,ctx,pg = await newpage(p, 8801, '/workspace/alleycat/wt', errs)
    ids=sys.argv[1].split(',')
    for id in ids:
      for k,r in [('fold',1),('kneel',1),('foldv',0),('foldv',3),('kneelv',0),('kneelv',3)]:
        await ev(pg, "opnFoePose('%s','%s',%d);1"%(id,k,r))
      await pg.wait_for_timeout(1500)
      for k,r in [('fold',1),('kneel',1),('foldv',0),('foldv',3),('kneelv',0),('kneelv',3)]:
        u = await ev(pg, "(OPN_FP['%s:%s:%d']||{}).u||''"%(id,k,r))
        if u: open('/tmp/fp_%s_%s_%d.png'%(id,k,r),'wb').write(base64.b64decode(u.split(',')[1]))
        else: print('missing',id,k,r)
      src = await ev(pg, "IMG['%s_hurt']||''"%id); print(id, src[:60])
    print(errs[:3]); await b.close()
asyncio.run(main())
