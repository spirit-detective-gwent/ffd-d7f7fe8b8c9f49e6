import asyncio, sys, json, base64
sys.path.insert(0, '/workspace/alleycat/tools'); from h import *
async def main():
  async with async_playwright() as p:
    errs=[]; b,ctx,pg = await newpage(p, 8801, '/workspace/alleycat/wt', errs, save=json.load(open('/workspace/alleycat/tools/save_c1.json')))
    await pg.reload(); await pg.wait_for_timeout(2500); await boot(pg, cont=True)
    await ev(pg, "opnRyoSheet();opnHbSheet();1"); await pg.wait_for_timeout(1500)
    for k in ('OPN_SH','OPN_HB'):
      u = await ev(pg, k+".url")
      open('/tmp/%s.png'%k,'wb').write(base64.b64decode(u.split(',',1)[1]))
    print(await ev(pg, "JSON.stringify({P:OPN.PUNCH,P3:OPN.PUNCH3,HB:OPN.HB,F:OPN.FIST})"))
    await b.close()
asyncio.run(main())
