import asyncio, sys, json
sys.path.insert(0, '/workspace/alleycat/tools'); from h import *
async def main():
  async with async_playwright() as p:
    errs=[]; b,ctx,pg = await newpage(p, 8801, '/workspace/alleycat/wt', errs)
    r = await pg.evaluate("""(()=>{var E=window.ENGINE||window.FFF_ENGINE; var CHs=(window.ENGINE&&ENGINE.chars&&ENGINE.chars())||{}; var IMG=window.__ev('IMG'); var out={has:[],no:[]};
      Object.keys(CHs).forEach(function(id){var c=CHs[id]; if(!c||!c.fig)return; (IMG[c.fig+'_down']?out.has:out.no).push(id+':'+c.fig)}); out.n=Object.keys(CHs).length; out.img=Object.keys(IMG).length; return JSON.stringify(out)})()""")
    print(r[:4000]); await b.close()
asyncio.run(main())
