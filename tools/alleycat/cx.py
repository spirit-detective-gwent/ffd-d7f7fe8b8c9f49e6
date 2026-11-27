# codex Alley Cat entry + New Move card: cx.py port root tag
import asyncio, sys, json
sys.path.insert(0, '/workspace/alleycat/tools'); from h import *
port, root, tag = int(sys.argv[1]), sys.argv[2], sys.argv[3]
OUT='/workspace/alleycat/shots'
async def main():
  async with async_playwright() as p:
    errs=[]; b,ctx,pg = await newpage(p, port, root, errs, save=json.load(open('/workspace/alleycat/tools/save_c1.json')))
    await pg.reload(); await pg.wait_for_timeout(2500); await boot(pg, cont=True); await ev(pg, "clearRoam();W.spawnT=1e12;SAVE.gsk=SAVE.gsk||{};SAVE.gsk.alley=1;1"); await pg.wait_for_timeout(800); await ev(pg, HUSH)
    await ev(pg, "W.cxCat='tech';W.cxDrill=1;W.cxKeep=1;pause('codex');1"); await pg.wait_for_timeout(1200)
    y = await pg.evaluate("(()=>{var a=document.querySelector('article[data-k=\"alley\"]');if(!a)return null;a.scrollIntoView({block:'start'});return a.innerText})()")
    print('CODEX', y); await pg.wait_for_timeout(500)
    await pg.screenshot(path='%s/codex_alley_%s.png'%(OUT,tag))
    cb = await pg.evaluate("(()=>{var b=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&/^Close$/.test((e.textContent||'').trim()));if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
    for i in range(3):
      cb = await pg.evaluate("(()=>{var b=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&/^Close$/.test((e.textContent||'').trim()));if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
      if not cb: break
      await pg.touchscreen.tap(*cb); await pg.wait_for_timeout(500)
    await ev(pg, HUSH); await pg.wait_for_timeout(400)
    await ev(pg, "delete SAVE.gsk.alley;W.dlg=false;root.__alleyCard(function(){});1"); await pg.wait_for_timeout(1500)
    print('CARD', await pg.evaluate("(()=>{var e=document.getElementById('wnmove');return e&&e.innerText})()"))
    await pg.screenshot(path='%s/card_alley_%s.png'%(OUT,tag))
    print('ERR', errs[:3]); await b.close()
asyncio.run(main())
