#!/workspace/pwenv/bin/python3
# bake2.py specs(comma) [kinds(comma)] : paints walk/fig/map (+more) for the given yk specs -> baked/<spec>_<kind>.webp
import asyncio,sys,json,base64,os,time
from playwright.async_api import async_playwright
K={'walk':dict(src='ext/c2_punk_walk.webp',cols=8,rows=4,cw=208,ch=272),
   'run':dict(src='ext/c2_punk_run.webp',cols=8,rows=4,cw=208,ch=272),
   'hurt':dict(src='ext/c2_punk_hurt.webp',cols=4,rows=4,cw=208,ch=272),
   'kn':dict(src='ext/c2_punk_kn.webp',cols=4,rows=4,cw=208,ch=272),
   'map':dict(src='ext/c2_punk_map.webp',cols=1,rows=1,faces=['front']),
   'fig':dict(src='ext/c2_punk_fig.webp',cols=1,rows=1,faces=['front']),
   'fig_hurt':dict(src='ext/c2_punk_fig_hurt.webp',cols=1,rows=1,faces=['front']),
   'lie':dict(src='ext/c2_punk_lie.webp',cols=2,rows=1,faces=['left'],rot=-1),
   'fig_down':dict(src='ext/c2_punk_fig_down.webp',cols=1,rows=1,faces=['right'],rot=1)}
async def main():
  specs=sys.argv[1].split(','); kinds=sys.argv[2].split(',') if len(sys.argv)>2 else ['walk','fig','map']
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('http://127.0.0.1:8891/bake.html'); await pg.wait_for_function('window.READY')
    for s in specs:
      for k in kinds:
        j=dict(K[k]); j['spec']=s.split('+')[0]; j['opts']={'debug':1} if '+dbg' in s else {}; j['q']=0.95; t=time.time()
        d=await pg.evaluate('j=>paintJob(j)',j); open(f'baked/{s}_{k}.webp','wb').write(base64.b64decode(d.split(',')[1])); print(s,k,round(time.time()-t,2),'s',errs[-1:] if errs else '',flush=True)
    await b.close()
asyncio.run(main())
