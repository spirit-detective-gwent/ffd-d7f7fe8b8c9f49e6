#!/workspace/pwenv/bin/python3
# bake.py jobs.json outdir : paints every job in headless Chromium with yk.js and writes <key>.webp
import asyncio,sys,json,base64,os,time
from playwright.async_api import async_playwright
async def main():
  jobs=json.load(open(sys.argv[1])); out=sys.argv[2]; only=sys.argv[3].split(',') if len(sys.argv)>3 else None
  os.makedirs(out,exist_ok=True)
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('http://127.0.0.1:8881/bake.html'); await pg.wait_for_function('window.READY')
    for k,j in jobs.items():
      if only and k not in only: continue
      t=time.time(); d=await pg.evaluate('j=>paintJob(j)',j); open(os.path.join(out,k+'.webp'),'wb').write(base64.b64decode(d.split(',')[1])); print(k,round(time.time()-t,2),'s',errs[-1:] if errs else '')
    await b.close()
asyncio.run(main())
