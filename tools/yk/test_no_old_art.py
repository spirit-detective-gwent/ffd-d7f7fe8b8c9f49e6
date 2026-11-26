#!/workspace/pwenv/bin/python3
"""No-old-art regression: samples every Ch2 sprite that wears a new cel look (Punk Y1-Y3, Hustlers, Kaneda, Goda, Flip, Nails, Gray Coats, Kagero)
every 50 ms while it stands, acts, brawls, is hit, kneels and lies, in every spawn path (street-event door/pin/smoke/dice/tag crews, posts and roamers,
border gang-fights, stand-in spawns incl. hurt + lie). Fails when a sprite's background ever resolves to an old sheet (an embedded data: sheet, an old
c2x_act_punk / c2x_act_hustler loop, a missing sheet) or when one Punk flips between Y1/Y2/Y3 looks.
usage: test_no_old_art.py <worktree dir> [port] [quick]   (exit 1 on failure)"""
import asyncio, sys, json, re, os, http.server, socketserver, threading, functools
from pathlib import Path
from playwright.async_api import async_playwright
root = Path(sys.argv[1]); PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 52300; QUICK = len(sys.argv) > 3
NEWBASE = r'(c2_punkY[123]|c2_hustlerY|c2_doormanY|mb2_sentoY|n13flipY|c2_gray|c2_boss|kuroda|mb2_arcade|n13hus)'
NEWWHO = {'c2_punk','c2_hustler','n13hus','c2_gray','c2_doorman','mb2_sento','n13flip','mb2_arcade','c2_boss'}
OLDLOOP = re.compile(r'^c2x_act_(punk|hustler)$')
NEWLOOP = re.compile(r'^c2x_act_(punkY[123]|hustlerY)$')
class TS(socketserver.ThreadingTCPServer): allow_reuse_address = True; daemon_threads = True
def serve():
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_GET(self):
            if self.path.split('?', 1)[0] in ('/', '/index.html'):
                raw = (root / 'index.html').read_bytes(); n = b'root.WORLD_API = {'
                raw = raw.replace(n, b'root.__ev=function(s){return eval(s)};' + n, 1)
                self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(raw))); self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(raw); return
            return super().do_GET()
    h = TS(('127.0.0.1', PORT), functools.partial(Q, directory=str(root))); threading.Thread(target=h.serve_forever, daemon=True).start(); return h
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
async def ev(pg, code): return await pg.evaluate("(c)=>{try{var r=__ev(c);return (r===undefined)?null:JSON.parse(JSON.stringify(r))}catch(e){return {__err:String(e&&e.message||e)}}}", code)
async def skipall(pg, n=10):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(300); c = await pg.evaluate(SK)
            if not c: break
        await pg.touchscreen.tap(*c); await pg.wait_for_timeout(280)
    await pg.evaluate("(()=>{var b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Close'&&e.offsetParent);if(b)b.click()})()")
async def tele(pg, x, y, ms=2500):
    await pg.evaluate("(a)=>{var A=WORLD_API,W=A.W;W.ryo.x=a[0];W.ryo.y=a[1];W.aoi.x=a[0];W.aoi.y=a[1]+60;A.camera(true)}", [x, y]); await pg.wait_for_timeout(ms)
SAMPLER = r"""(function(){ if(window.__S){clearInterval(window.__S.iv);} var S=window.__S={els:new Map(),n:0};
 S.iv=setInterval(function(){ document.querySelectorAll('#world .wsp, .c2lie').forEach(function(e){ var r=S.els.get(e); if(!r){r={id:++S.n,who:e.dataset.who||'',cls:e.className,seen:{},first:null};S.els.set(e,r);}
   var bi=e.style.backgroundImage||''; var m=bi.match(/world\/([^?")]+)/); var u=m?m[1]:(bi.indexOf('data:')>=0?'DATA':(bi.indexOf('blob:')>=0?'BLOB':(bi?bi.slice(0,30):'NONE')));
   var k=u+'|'+(e.dataset.loop||''); r.seen[k]=(r.seen[k]||0)+1; if(!r.first)r.first=k; r.cls=e.className; if(e.dataset.who)r.who=e.dataset.who; }); },50); })()"""
BAD = []
def analyse(tag, els):
    nb = 0
    for r in els:
        keys = list(r['seen'].keys()); bases = []; loops = []; hasdata = False; tracked = r['who'] in NEWWHO
        for k in keys:
            u, lp = k.split('|', 1)
            b = re.match(r'(.+?)_(walk|run|hurt|kn|lie|map|fig|idle|fig_hurt|fig_down)\.webp$', u)
            base = b.group(1) if b else (re.sub(r'\.webp$', '', u))
            if re.fullmatch(NEWBASE, base) or NEWLOOP.match(lp) or OLDLOOP.match(lp) or lp in ('c2_gray_idle', 'c2_hustler_idle', 'c2_punkY1_idle'): tracked = True
            bases.append(base); loops.append(lp)
            if u in ('DATA', 'BLOB'): hasdata = True
        if not tracked: continue
        nb += 1; why = []
        for k in keys:
            u, lp = k.split('|', 1)
            if OLDLOOP.match(lp): why.append('old act loop ' + lp)
            if u in ('DATA', 'BLOB') and not NEWLOOP.match(lp) and r['who'] not in ('mb2_arcade',): why.append('old/embedded sheet ' + u + ' loop=' + lp)
            if u == 'NONE': why.append('no sheet')
            bm = re.match(r'(.+?)_(walk|run|hurt|kn|lie|map|fig|idle|fig_hurt|fig_down)\.webp$', u)
            if bm and not re.fullmatch(NEWBASE, bm.group(1)) and not re.match(r'(c2_boso|c2_suit)', bm.group(1)): why.append('unexpected sheet ' + u)
        pv = set(re.findall(r'punkY([123])', ' '.join(keys)))
        if len(pv) > 1: why.append('punk look flips between Y' + '/Y'.join(sorted(pv)))
        if why: BAD.append((tag, r['who'] or r['cls'], sorted(set(why)), r['seen']))
    return nb
async def sample(pg, tag, ms):
    await pg.evaluate(SAMPLER); await pg.wait_for_timeout(ms)
    els = await pg.evaluate("(()=>{var o=[];window.__S.els.forEach(function(r){o.push(r)});return o})()")
    n = analyse(tag, els); print(f'  {tag}: {n} tracked sprites, bad so far {len(BAD)}', flush=True)
async def main():
    h = serve()
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True, args=['--disable-dev-shm-usage'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True,
          user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
        pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(3500)
        await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(2500); await skipall(pg, 12)
        await pg.evaluate("WORLD_API.c2Begin(true)"); await pg.wait_for_timeout(3000); await skipall(pg, 12); await pg.wait_for_timeout(1500)
        await ev(pg, "(function(){var S=c2S();S.e.genji=1;S.e.roam=1;S.e.arrive=1;S.e.gymIn=1;})()")
        # 1. street-event crews: door / pin / vpin / smoke / dice / tag / lean (Hustlers + Punks)
        evs = await ev(pg, "FFF_C2EV.EVENTS.filter(function(e){return e.g==='H'||e.g==='P'}).map(function(e){return [e.id,Math.round(e.x),Math.round(e.y)]})")
        if QUICK: evs = evs[::4]
        for (id, x, y) in evs:
            await ev(pg, "FFF_C2EV.clear()"); await tele(pg, x, y + 150, 500)
            await ev(pg, "FFF_C2EV.force('%s')" % id); await pg.evaluate(SAMPLER); await pg.wait_for_timeout(5200)
            els = await pg.evaluate("(()=>{var o=[];window.__S.els.forEach(function(r){o.push(r)});return o})()"); n = analyse('event ' + id, els)
        print('  events done, bad', len(BAD), flush=True)
        await ev(pg, "FFF_C2EV.clear()")
        # 2. border gang-fights (call, gather, brawl, down, home) incl. the top and bottom of the Shotengai
        for bd, (bx, by) in {'X2': (1790, 2165), 'X3': (2560, 3190), 'X1': (1900, 1800)}.items():
            await tele(pg, bx, by + 140, 4500)
            ok = await ev(pg, "g38tStart('%s','test')" % bd)
            await pg.evaluate(SAMPLER); await pg.wait_for_timeout(9000 if QUICK else 22000)
            els = await pg.evaluate("(()=>{var o=[];window.__S.els.forEach(function(r){o.push(r)});return o})()"); n = analyse('gang-fight ' + bd + ' started=' + str(ok), els)
            print('  fight', bd, 'started', ok, n, 'tracked', flush=True)
            await ev(pg, "(function(){var C=W.g38c;if(C)g38tEnd(C,'test')})()") if False else None
        # 3. posts, roamers and packs standing / walking
        for k, (x, y) in {'p_hus_post': (330, 950), 'p_pnk_post': (2180, 3340), 't_alley': (260, 2690), 't_arcade': (2180, 3375), 'p_hus_street': (260, 1720)}.items():
            await tele(pg, x, y + 120, 3500); await sample(pg, 'crew ' + k, 5200)
        # 4. stand-in spawns (cutscene / quest NPC path): stand, hit, kneel-lie, in all faces
        ids = ['c2_punk', 'c2_punk', 'c2_punk', 'c2_hustler', 'n13hus', 'c2_gray', 'c2_doorman', 'mb2_sento', 'n13flip', 'mb2_arcade', 'c2_boss']
        await tele(pg, 2180, 2000, 1500)
        await ev(pg, "(function(){var r=WORLD_API.W.ryo;window.__T=[];%s.forEach(function(id,i){var s=c2Npc(id,r.x-200+i*36,r.y-80,Math.PI/2);window.__T.push([id,s])})})()" % json.dumps(ids))
        await pg.evaluate(SAMPLER)
        for t in range(5):
            await pg.wait_for_timeout(1000)
            await ev(pg, "window.__T.forEach(function(q,i){var s=q[1],id=q[0];try{if(%d===1)hurtPlay(s,id);if(%d===3){var le=lieEl(id,s.x,s.y+40,C2K[id]||1.15,false);if(le){le.classList.add('c2lie');layer.appendChild(le);setTimeout(function(){le.remove()},900)}}if(%d===4)waddle(s,3,Math.random()*6.28)}catch(e){}})" % (t, t, t))
        els = await pg.evaluate("(()=>{var o=[];window.__S.els.forEach(function(r){o.push(r)});return o})()"); n = analyse('stand-ins (stand/hit/lie/walk)', els); print('  stand-ins tracked', n)
        print('page errors:', errs[:3])
        await b.close()
    h.shutdown()
    if BAD:
        print('FAIL: %d sprite(s) resolved to old art or flipped look' % len(BAD))
        for tag, who, why, seen in BAD[:40]: print(' ', tag, who, why, dict(list(seen.items())[:6]))
        sys.exit(1)
    print('PASS: no new-art sprite ever resolved to an old sheet'); 
asyncio.run(main())
