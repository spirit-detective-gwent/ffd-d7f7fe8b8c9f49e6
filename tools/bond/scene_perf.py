"""Scene perf: sento win -> bond scene -> seal. old (b15775f: c2lm_sento ask) vs new (c2_goda). native + CPU x4. fps / low1 / cpu_busy% / heap."""
import sys, asyncio, json, statistics
sys.path.insert(0, '/workspace/ffd-bond/tools/bond')
import bh
from playwright.async_api import async_playwright
SAMPLER = "()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l)}"
CLICK = """(i)=>{var b=[...document.querySelectorAll('#wdlg.on button')].filter(e=>e.offsetParent&&!e.disabled&&!/Auto/.test(e.textContent));if(!b.length)return null;var bo=document.querySelector('#wdlg.on button.bondopt');(bo?b.filter(e=>e.classList.contains('bondopt')):b)[bo?i:0].click();return 1}"""
POLL = "(function(){var d=document.getElementById('wdlg');return {on:!!(d&&d.classList.contains('on')),bond:!!document.querySelector('#wdlg.on button.bondopt'),seal:!!c2S().e.seal_sento}})()"
async def metrics(c):
    m = await c.send('Performance.getMetrics'); return {x['name']: x['value'] for x in m['metrics']}
async def run(b, port, body, thr, ans):
    ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, is_mobile=True, has_touch=True)
    pg = await ctx.new_page(); cdp = await ctx.new_cdp_session(pg); await cdp.send('Performance.enable')
    await bh.boot(pg, port, body); await bh.ch2(pg)
    await bh.ev(pg, "(function(){var E=c2S().e;E.run_fac='arc';E.baseOpen_bat=1;E.guardGone_sento=1;E.arrive=1;STORY.bond(SAVE).path='strategic';return 1})()")
    await bh.ev(pg, "c2Go('sento')"); await pg.wait_for_timeout(2500); await bh.ev(pg, bh.HUSH)
    if thr > 1: await cdp.send('Emulation.setCPUThrottlingRate', {'rate': thr})
    await pg.wait_for_timeout(500)
    await bh.ev(pg, "(function(){var b=W.c2n.boss;W.ryo.x=b.x-90;W.ryo.y=b.y+60;place(W.ryo,0);if(W.aoi){W.aoi.x=b.x-130;W.aoi.y=b.y+90;place(W.aoi,0)}camera(true);window.__h0=performance.memory.usedJSHeapSize;return 1})()")
    await pg.evaluate(SAMPLER); m0 = await metrics(cdp)
    await bh.ev(pg, "c2LmBack(true,{ctx:{c2lm:'sento',dg:'c2'}});1")
    for i in range(600):
        await pg.wait_for_timeout(450); st = await bh.ev(pg, POLL)
        if st['seal']: break
        if st['on']: await pg.evaluate(CLICK, ans)
    await pg.wait_for_timeout(2500)
    m1 = await metrics(cdp); await pg.evaluate("window.__run=false"); ft = (await pg.evaluate("window.__ft"))[2:]
    wall = m1['Timestamp'] - m0['Timestamp']; s = sorted(ft, reverse=True); n = max(1, len(ft) // 100)
    r = dict(fps=round(1000 * len(ft) / sum(ft), 1), low1=round(1000 / (sum(s[:n]) / n), 1), cpu_busy_pct=round(100 * (m1['TaskDuration'] - m0['TaskDuration']) / wall, 1), script_pct=round(100 * (m1['ScriptDuration'] - m0['ScriptDuration']) / wall, 1), secs=round(wall), over33=sum(1 for x in ft if x > 33.4), heap_delta_mb=round(((await bh.ev(pg, "performance.memory.usedJSHeapSize")) - (await bh.ev(pg, "window.__h0"))) / 1e6, 1), seal=st['seal'])
    await ctx.close(); return r
async def main():
    bh.serve(8961, '/tmp/sp_old'); bh.serve(8962, '/tmp/sp_new')
    bo = bh.inject('/tmp/sp_old/index.html'); bn = bh.inject('/tmp/sp_new/index.html'); out = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for thr in (1, 4):
            for lab, port, body in (('old', 8961, bo), ('new', 8962, bn)):
                for k in range(2):
                    r = await run(b, port, body, thr, 1); out.setdefault(f'{lab} x{thr}', []).append(r); print(lab, 'x%d' % thr, r, flush=True)
        await b.close()
    json.dump(out, open('/workspace/perf-check/results_scene_goda.json', 'w'), indent=1)
asyncio.run(main())
