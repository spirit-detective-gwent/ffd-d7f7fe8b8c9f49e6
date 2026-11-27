# battle opening with the downed man: bt.py port root tag
import asyncio, sys, json, os
sys.path.insert(0, '/workspace/alleycat/tools'); from h import *
port, root, tag = int(sys.argv[1]), sys.argv[2], sys.argv[3]
OUT='/workspace/alleycat/shots/raw'
CASES = [('ch1lib', "['bully1']", "{dg:'lib',dgk:'lib_t0',dgks:['lib_t0'],dgm:'dl_hall',amb:{k:0.62,side:'back'},acDown:1,opnAc:1}"),
         ('ch1yard', "['bully3','bully2']", "{amb:{k:0.62,side:'back'},acDown:1,opnAc:1,place:'yard'}"),
         ('ch2udon', "['c2_punk']", "{dg:'c2',dgk:'punk1',dgks:['punk1'],amb:{k:0.62,side:'back'},acDown:1,opnAc:1}"),
         ('ch2street', "['c2_suit','c2_suit']", "{dg:'c2',dgk:'sq_x',dgks:['sq_x'],amb:{k:0.62,side:'back'},acDown:1,opnAc:1}")]
async def main():
  async with async_playwright() as p:
    for name, foes, cx in [c for c in CASES if c[0] in os.environ.get('BTC','ch1lib,ch1yard,ch2udon,ch2street').split(',')]:
      errs=[]; b,ctx,pg = await newpage(p, port, root, errs, save=json.load(open('/workspace/alleycat/tools/save_c1.json')))
      await pg.reload(); await pg.wait_for_timeout(2500); await boot(pg, cont=True); await ev(pg, "clearRoam();W.spawnT=1e12;1")
      await ev(pg, "fight(%s, false, %s);1" % (foes, cx)); await pg.wait_for_timeout(2600)
      info = await pg.evaluate("(()=>{var k=document.querySelector('.kopose.acdown'),fe=document.querySelector('#fE'),fb=document.querySelector('#fE .fbody');var kb=k&&k.getBoundingClientRect(),rb=fe.getBoundingClientRect();return JSON.stringify({bfx:document.getElementById('game').getAttribute('data-bfx'),feet:getComputedStyle(fe).getPropertyValue('--bt-feet'),pose:kb?[Math.round(kb.left),Math.round(kb.top),Math.round(kb.width),Math.round(kb.height),Math.round(kb.bottom)]:null,row:[Math.round(rb.top),Math.round(rb.bottom)],fbOp:fb&&fb.style.opacity})})()")
      print(name, info)
      await pg.screenshot(path='%s/%s_%s_open.png'%(OUT,tag,name))
      c = await pg.evaluate("(()=>{var c=[...document.querySelectorAll('#hand .card')].filter(e=>e.offsetParent);if(!c.length)return null;var r=c[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
      if c:
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(500)
        t = await pg.evaluate("(()=>{var e=[...document.querySelectorAll('*')].filter(e=>e.offsetParent&&/^TAP TO PLAY$/i.test((e.textContent||'').trim()));if(!e.length)return null;var r=e[e.length-1].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
        print(name,'ttp',t); await pg.touchscreen.tap(*(t or c))
        prev=0
        for ms in (120, 260, 450, 1400):
          await pg.wait_for_timeout(ms - prev)
          await pg.screenshot(path='%s/%s_%s_rise%04d.png'%(OUT,tag,name,ms))
          prev=ms
        print(name, 'after', await pg.evaluate("(()=>{var k=document.querySelector('.kopose.acdown');var fb=document.querySelector('#fE .fbody');return JSON.stringify({pose:!!k,fbOp:fb&&fb.style.opacity,down:fb&&fb.closest('.fighter').dataset.down||''})})()"))
      print('ERR', errs[:3]); await ctx.close(); await b.close()
asyncio.run(main())
