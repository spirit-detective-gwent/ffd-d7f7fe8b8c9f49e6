#!/workspace/pwenv/bin/python3
"""Quick fps/heat gate: Ch2 town near the gym, 1x and 4x throttle, ~8s walk each."""
import asyncio, json, http.server, socketserver, threading, functools, statistics
from pathlib import Path
from playwright.async_api import async_playwright

FFD = '/workspace/ffd-qsnd'
PORT = 8973
OUT = Path('/tmp/qsnd')
SAMPLER = """()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);}"""

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def serve(port, directory=FFD):
    s = TS(('127.0.0.1', port), functools.partial(Q, directory=directory))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s

def stats(ft):
    ft = [x for x in ft[2:]]
    if not ft: return {}
    tot = sum(ft); s = sorted(ft, reverse=True); n = max(1, len(ft)//100)
    return dict(fps=round(1000*len(ft)/tot,1), low1=round(1000/(sum(s[:n])/n),1),
                over20=sum(1 for x in ft if x>20), over33=sum(1 for x in ft if x>33.4),
                frames=len(ft), worst=round(s[0],1))

async def ev(pg, code):
    return await pg.evaluate(
        """(c)=>{var r=window.__ev(c);try{return JSON.parse(JSON.stringify(r===undefined?null:r))}catch(e){return String(r)}}""",
        code,
    )

async def window(pg, cdp, secs):
    await pg.evaluate(SAMPLER)
    m0 = await cdp.send('Performance.getMetrics')
    m0 = {x['name']: x['value'] for x in m0['metrics']}
    await pg.wait_for_timeout(secs * 1000)
    m1 = await cdp.send('Performance.getMetrics')
    m1 = {x['name']: x['value'] for x in m1['metrics']}
    await pg.evaluate("window.__run=false")
    ft = await pg.evaluate("window.__ft")
    wall = m1['Timestamp'] - m0['Timestamp']
    r = stats(ft)
    r['cpu_busy_pct'] = round(100*(m1['TaskDuration']-m0['TaskDuration'])/wall, 1)
    r['script_pct'] = round(100*(m1['ScriptDuration']-m0['ScriptDuration'])/wall, 1)
    r['heap_mb'] = round(m1['JSHeapUsedSize']/1e6, 1)
    return r

SEED = r"""
(function(){
  window.FFF_SKIP_C2_CINE=1;W._c2SkipCine=1;
  var S=c2S();S.e=S.e||{};S.q=S.q||{};
  ['arrive','gymIn','genji','herbBrief','sumire','informant','infPunk','c2sRep','roam','called','c2lMap','fc51Hear','fc13sOut'].forEach(function(k){S.e[k]=1;});
  S.e.fc51Brawls=['X1','X3']; S.q.cq2_arrive=9;S.q.cq2_hq=9;S.q.cq2_scout=9;S.q.cq2_word=0;S.q.cq2_locks=0;S.qa='cq2_locks';
  SAVE.chapter=2;SAVE.qa='cq2_locks';SAVE.qs=Object.assign(SAVE.qs||{},{cq2_arrive:9,cq2_hq:9,cq2_scout:9,cq2_word:0,cq2_locks:0});
  save(); if(typeof c2Go==='function'){c2Go('town',[1100,2670,2]);}
  W.dlg=false;W.cut=false;W.busy=false;1;
})()
"""

async def boot(p, thr):
    html = Path('/tmp/qsnd/index_hooked.html').read_text(encoding='utf-8')
    b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
    ctx = await b.new_context(viewport={'width':390,'height':844}, device_scale_factor=3, is_mobile=True, has_touch=True,
        user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
    pg = await ctx.new_page()
    async def rt(route):
        await route.fulfill(body=html, content_type='text/html')
    await pg.route('**/index.html', rt)
    await pg.goto('http://127.0.0.1:%d/index.html' % PORT)
    await pg.wait_for_function("()=>!!(window.WORLD_API && window.__ev)", timeout=90000)
    cdp = await ctx.new_cdp_session(pg)
    await cdp.send('Performance.enable')
    if thr > 1:
        await cdp.send('Emulation.setCPUThrottlingRate', {'rate': thr})
    await pg.wait_for_timeout(500)
    await pg.touchscreen.tap(195, 420)
    await pg.evaluate("WORLD_API.enter(true)")
    await pg.wait_for_timeout(1000)
    await ev(pg, "window.FFF_SKIP_C2_CINE=1;W._c2SkipCine=1;1")
    await pg.evaluate("WORLD_API.c2Begin(true)")
    await pg.wait_for_timeout(2000)
    await ev(pg, "try{if(typeof phClose==='function')phClose()}catch(e){}W.dlg=false;W.cut=false;W.busy=false;W.paused=false;1")
    await ev(pg, SEED)
    await pg.wait_for_timeout(800)
    return b, ctx, pg, cdp

async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t = Path(FFD+'/index.html').read_text(encoding='utf-8')
    t = t.replace('var W = { guards: [], paused: false', 'root.__ev=function(s){return eval(s)};var W = { guards: [], paused: false', 1)
    Path('/tmp/qsnd/index_hooked.html').write_text(t, encoding='utf-8')
    serve(PORT)
    out = {}
    async with async_playwright() as p:
        for label, thr, secs in (('town_1x', 1, 8), ('town_4x', 4, 8)):
            b, ctx, pg, cdp = await boot(p, thr)
            await ev(pg, "if(WORLD_API.walkToX)WORLD_API.walkToX(2000,2670);1")
            r = await window(pg, cdp, secs)
            out[label] = r
            print(label, json.dumps(r))
            await b.close()
    Path(OUT/'perf.json').write_text(json.dumps(out, indent=2))
    print('PERF', json.dumps(out, indent=2))

if __name__ == '__main__':
    asyncio.run(main())
