#!/workspace/pwenv/bin/python3
"""No-old-art check for the Ch2 gangs (ch2-gangs): Jin (mb2_game), Masa (mb2_depot), the Bouncer, Sabu (n13sb), Club Kitsune Suits /
Runners (c2_suit), Depot Riders / Dock Hands (c2_boso). Modeled on tools/yk/test_no_old_art.py (ch2-idle).
 1. IMG audit: every sheet key for these men (and the street-act sheets) points at the new world/<pre>_*.webp files; PT / card figs too.
 2. Sampler (every 50 ms): street events of the Suits / Riders, the border gang-fights with them, stand-ins (stand / act / hit / kneel /
    lie / walk). Fails when a sprite's background ever resolves to an embedded data: sheet, an old world/ name, nothing, or when one man
    flips between his crew's two looks.
usage: test_no_old_art_gangs.py <worktree dir> [port] [quick]   (exit 1 on failure)"""
import asyncio, sys, json, re, http.server, socketserver, threading, functools
from pathlib import Path
from playwright.async_api import async_playwright
root = Path(sys.argv[1]); PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 52310; QUICK = len(sys.argv) > 3
NEWBASE = r'(c2_suitK[12]|c2_bosoK[12]|mb2_gameK|mb2_depotK|bouncerK|n13sbK)'
WHO = {'c2_suit', 'c2_boso', 'bouncer', 'mb2_game', 'mb2_depot', 'n13sb'}
NEWLOOP = re.compile(r'^c2x_act_(suit|boso)(K2)?$')
SHEETS = '(walk|run|hurt|kn|lie|map|fig|idle|fig_hurt|fig_down)'
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
 S.iv=setInterval(function(){ document.querySelectorAll('#world .wsp, .c2lie, #world [class*=lie]').forEach(function(e){ var r=S.els.get(e); if(!r){r={id:++S.n,who:e.dataset.who||'',cls:String(e.className),seen:{}};S.els.set(e,r);}
   var bi=e.style.backgroundImage||''; var m=bi.match(/world\/([^?")]+)/); var u=m?m[1]:(bi.indexOf('data:')>=0?'DATA':(bi.indexOf('blob:')>=0?'BLOB':(bi?bi.slice(0,30):'NONE')));
   var k=u+'|'+(e.dataset.loop||''); r.seen[k]=(r.seen[k]||0)+1; if(e.dataset.who)r.who=e.dataset.who; }); },50); })()"""
BAD = []; COUNT = {}
def analyse(tag, els):
    nb = 0
    for r in els:
        keys = list(r['seen'].keys()); tracked = r['who'] in WHO
        for k in keys:
            u, lp = k.split('|', 1); b = re.match(r'(.+?)_' + SHEETS + r'\.webp$', u)
            if (b and re.fullmatch(NEWBASE, b.group(1))) or NEWLOOP.match(lp) or re.match(r'c2x_act_(suit|boso)K', u): tracked = True
        if not tracked: continue
        nb += 1; why = []
        for k in keys:
            u, lp = k.split('|', 1)
            if u in ('DATA', 'BLOB'): why.append('embedded sheet ' + u + ' loop=' + lp)
            if u == 'NONE' and r['who'] in WHO: why.append('no sheet')
            bm = re.match(r'(.+?)_' + SHEETS + r'\.webp$', u)
            if bm and not re.fullmatch(NEWBASE, bm.group(1)): why.append('unexpected sheet ' + u)
            if not bm and u not in ('NONE', 'DATA', 'BLOB') and not re.fullmatch(r'c2x_act_(suit|boso)K[12]\.webp', u): why.append('unexpected sheet ' + u)
            if bm: COUNT[bm.group(2)] = COUNT.get(bm.group(2), 0) + 1
            if re.match(r'c2x_act_', u): COUNT['act'] = COUNT.get('act', 0) + 1
        for g in ('suit', 'boso'):
            if len(set(re.findall(r'(?:c2_%sK|c2x_act_%sK)([12])' % (g, g), ' '.join(keys)))) > 1: why.append(g + ' look flips between A and B')
        if why: BAD.append((tag, r['who'] or r['cls'], sorted(set(why)), r['seen']))
    return nb
async def collect(pg, tag):
    els = await pg.evaluate("(()=>{var o=[];window.__S.els.forEach(function(r){o.push(r)});return o})()"); n = analyse(tag, els); print(f'  {tag}: {n} tracked, bad so far {len(BAD)}', flush=True); return n
AUDIT = r"""(function(){ var bad=[], n=0, re=/^(bouncer|jin|masa|mb2_game|mb2_depot|c2_suit|c2_suitR|c2_suitg|c2_boso|c2_bosoD|c2_bosog|n13sb)_/;
  Object.keys(IMG).forEach(function(k){ if(!re.test(k)&&!/^c2x_act_(suit|boso)/.test(k)) return; n++; var v=String(IMG[k]);
    if(!/^world\/(c2_suitK[12]|c2_bosoK[12]|mb2_gameK|mb2_depotK|bouncerK|n13sbK)_[a-z_]+\.webp|^world\/c2x_act_(suit|boso)K[12]\.webp/.test(v)) bad.push(k+' -> '+v.slice(0,60)); });
  ['mb2_game','mb2_depot','bouncer','n13sb','c2_suit','c2_boso','c2_suitR','c2_bosoD'].forEach(function(id){ var p=PT[id]; if(!p||!IMG[p]||!/^world\/[a-z0-9_]+K[12]?_fig\.webp/.test(IMG[p])) bad.push('PT.'+id+' -> '+p+' '+String(IMG[p]).slice(0,40)); });
  var C=(window.CARD_DATA||{}).chars||{}; ['mb2_game','mb2_depot','bouncer','c2_suit','c2_suitg','c2_boso','c2_bosog'].forEach(function(id){ var c=C[id]; if(!c) return; var f=c.fig; if(!f||!IMG[f]||!/^world\//.test(IMG[f])) bad.push('card '+id+' fig '+f+' '+String(IMG[f]).slice(0,40)); ['_hurt','_down'].forEach(function(x){ if(IMG[f+x]&&!/^world\//.test(IMG[f+x])) bad.push('card '+id+' '+f+x); }); });
  if(typeof PC_FIG!=='undefined') PC_FIG.forEach(function(k){ if(/^(bouncer|c2_suit|c2_boso|mb2_game|mb2_depot)_fig$/.test(k)) bad.push('PC_FIG '+k); });
  ['c2x_act_suit-src','c2x_act_boso-src'].forEach(function(i){ if(document.getElementById(i)) bad.push('embedded '+i); });
  return {n:n,bad:bad}; })()"""
async def main():
    h = serve()
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True, args=['--disable-dev-shm-usage'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True,
          user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
        pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        await pg.goto(f'http://127.0.0.1:{PORT}/index.html'); await pg.wait_for_timeout(3500)
        a = await ev(pg, AUDIT); print('IMG audit:', a['n'], 'keys;', len(a['bad']), 'bad', a['bad'][:12], flush=True)
        for x in a['bad']: BAD.append(('audit', x, ['old/unexpected IMG'], {}))
        await pg.evaluate("WORLD_API.enter(true)"); await pg.wait_for_timeout(2500); await skipall(pg, 12)
        await pg.evaluate("WORLD_API.c2Begin(true)"); await pg.wait_for_timeout(3000); await skipall(pg, 12); await pg.wait_for_timeout(1500)
        a = await ev(pg, AUDIT); print('IMG audit (in Ch2):', a['n'], 'keys;', len(a['bad']), 'bad', a['bad'][:12], flush=True)
        for x in a['bad']: BAD.append(('audit ch2', x, ['old/unexpected IMG'], {}))
        await ev(pg, "(function(){var S=c2S();S.e.genji=1;S.e.roam=1;S.e.arrive=1;S.e.gymIn=1;})()")
        evs = await ev(pg, "FFF_C2EV.EVENTS.filter(function(e){return e.g==='S'||e.g==='R'}).map(function(e){return [e.id,Math.round(e.x),Math.round(e.y)]})")
        if QUICK: evs = evs[::3]
        for (id, x, y) in evs:
            await ev(pg, "FFF_C2EV.clear()"); await tele(pg, x, y + 150, 500)
            await ev(pg, "FFF_C2EV.force('%s')" % id); await pg.evaluate(SAMPLER); await pg.wait_for_timeout(5200)
            await collect(pg, 'event ' + id)
        await ev(pg, "FFF_C2EV.clear()")
        for bd in ('X1', 'X3', 'X4'):
            at = await ev(pg, "G38T.BORDER['%s'].at" % bd); await tele(pg, at[0], at[1] + 140, 4500)
            ok = await ev(pg, "g38tStart('%s','test')" % bd); await pg.evaluate(SAMPLER); await pg.wait_for_timeout(9000 if QUICK else 20000)
            await collect(pg, 'gang-fight %s started=%s' % (bd, ok))
        ids = ['c2_suit'] * 4 + ['c2_boso'] * 4 + ['bouncer', 'mb2_game', 'mb2_depot', 'n13sb']
        await tele(pg, 2180, 2000, 1500)
        await ev(pg, "(function(){var r=WORLD_API.W.ryo;window.__T=[];%s.forEach(function(id,i){var s=c2Npc(id,r.x-190+i*32,r.y-80,Math.PI/2);window.__T.push([id,s])})})()" % json.dumps(ids))
        await pg.evaluate(SAMPLER)
        for t in range(7):
            await pg.wait_for_timeout(1000)
            await ev(pg, """window.__T.forEach(function(q,i){var s=q[1],id=q[0];try{
              if(%d===1)hurtPlay(s,id);
              if(%d===2&&/^c2_(suit|boso)$/.test(id))celLoop(s,'c2x_act_'+id.slice(3),i%%5,{ms:200});
              if(%d===3)celLoop(s,id+'_kn',i%%4,{ms:200});
              if(%d===4){celLoopOff(s);var le=lieEl(id,s.x,s.y,C2K[id]||1.15,false);if(le){le.classList.add('c2lie');layer.appendChild(le);setTimeout(function(){le.remove()},900)}}
              if(%d===5)waddle(s,3,Math.random()*6.28);
              if(%d===6)waddle(s,0,Math.PI/2);}catch(e){}})""" % ((t,) * 6))
        await collect(pg, 'stand-ins (stand/act/hit/kneel/lie/walk/idle)')
        print('sheet kinds seen:', COUNT)
        print('page errors:', errs[:3])
        await b.close()
    h.shutdown()
    if BAD:
        print('FAIL: %d problem(s)' % len(BAD))
        for tag, who, why, seen in BAD[:40]: print(' ', tag, who, why, dict(list(seen.items())[:6]))
        sys.exit(1)
    print('PASS: every gang sprite resolved to the new sheets, no look flips')
asyncio.run(main())
