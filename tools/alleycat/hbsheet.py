import asyncio, sys, base64
sys.path.insert(0, '/workspace/alleycat/tools'); from h import *
async def main():
  async with async_playwright() as p:
    errs=[]; b,ctx,pg = await newpage(p, 8801, '/workspace/alleycat/wt', errs)
    for L in [54, 30, 22, 16]:
      await ev(pg, "OPN.HB.lunge=%d;OPN_HB.url=null;OPN_HB.src=null;OPN_HB.busy=null;opnHbSheet();1"%L); await pg.wait_for_timeout(1500)
      u = await ev(pg, "OPN_HB.url||''")
      open('/tmp/hb_%d.png'%L,'wb').write(base64.b64decode(u.split(',')[1]))
    await b.close()
asyncio.run(main())
