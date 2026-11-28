#!/workspace/pwenv/bin/python3
"""Timeline of camera + actor positions through the clash (finds snaps / teleports). Prints a jump report."""
import asyncio, json, math, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import h, t13_clash as T
SMP = r"""(function(){
  function c(e){var r=e.getBoundingClientRect();return [Math.round(r.left+r.width/2),Math.round(r.bottom)];}
  var hs=[].slice.call(document.querySelectorAll('.nq[data-npc="c2_hustler"]')).filter(function(e){return e.isConnected}), ps=[].slice.call(document.querySelectorAll('.nq[data-npc="c2_punk"]')).filter(function(e){return e.isConnected}), fl=document.querySelector('.nq[data-npc="n13flip"]');
  var st=root.FFF_UI&&FFF_UI.ST;
  return {t:performance.now()|0, xc:(root.FFF_NQ&&FFF_NQ.xc)?FFF_NQ.xc.st():'', ig:!!(st&&st.inGame), wd:!!(document.getElementById('world')&&document.getElementById('world').classList.contains('on')),
   cam:[Math.round(W.cam.x),Math.round(W.cam.y)], ryo:[Math.round(W.ryo.x),Math.round(W.ryo.y)], rs:(function(){var e=W.ryo.el; if(!e) return null; return c(e)})(),
   hs:hs.map(c), ps:ps.map(c), fl:fl?c(fl):null, pan:!!W.pan};})()"""
async def main():
    async with h.Game(out='/tmp') as g:
        await g.boot(); await T.seed(g)
        log = []; run = True
        async def samp():
            while run:
                try: log.append(await g.ev(SMP))
                except Exception as e: log.append(None); print('err', str(e)[:200]) if len(log)<3 else None
                await asyncio.sleep(0.05)
        task = asyncio.create_task(samp())
        await T.walkin(g); await T.through_clash_line(g); await T.to_battle(g); await g.wait(600)
        await T.win(g); p = await T.to_post(g); await g.wait(5000)
        for _ in range(8):
            if not await T.tap_btn(g, '^(Next|OK)'): break
            await g.wait(400)
        run = False; await task
    prev = None; out = []
    for s in log:
        if prev:
            jc = math.hypot(s['cam'][0]-prev['cam'][0], s['cam'][1]-prev['cam'][1])
            jr = math.hypot(s['ryo'][0]-prev['ryo'][0], s['ryo'][1]-prev['ryo'][1])
            jp = max([math.hypot(a[0]-b[0], a[1]-b[1]) for a, b in zip(s['ps'], prev['ps'])] + [0])
            jh = max([math.hypot(a[0]-b[0], a[1]-b[1]) for a, b in zip(s['hs'], prev['hs'])] + [0])
            if max(jc, jr, jp, jh) > 40 or s['ig'] != prev['ig'] or s['xc'] != prev['xc'] or len(s['ps']) != len(prev['ps']) or len(s['hs']) != len(prev['hs']):
                out.append((s['t'] - log[0]['t'], 'xc=' + s['xc'], 'ig' if s['ig'] else '--', 'cam', jc and round(jc), 'ryo', round(jr), 'pk', round(jp), 'hu', round(jh), 'n', len(s['ps']), len(s['hs']), s['cam'], s['ryo'], s['ps'], s['hs']))
        prev = s
    for o in out: print(*o)
    Path('/tmp/trace.json').write_text(json.dumps(log))
asyncio.run(main())
