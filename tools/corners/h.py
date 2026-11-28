#!/workspace/pwenv/bin/python3
"""Harness for Nails alley / Four Corners gym-exit tests."""
import asyncio, functools, http.server, os, socket, socketserver, threading
from pathlib import Path
from playwright.async_api import async_playwright

INDEX = Path(os.environ.get('FFD_INDEX', '/workspace/nailsalley/wt/index.html'))
ROOT = INDEX.parent

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""

HUSH = """(function(){
  try { if (typeof phClose==='function') phClose(); } catch(e){}
  W.paused=false; if(!arguments[0]){ W.dlg=false; W.cut=false; W.busy=false; }
  W.path=[]; W.fading=0;
  var d=document.getElementById('wdlg'); if(d && !arguments[0]){ d.className=''; d.innerHTML=''; }
  var q=document.getElementById('wquest'); if(q) q.style.display='none';
  return 1;
})()"""

SEED = r"""
(function(){
  try { window.FFF_SKIP_C2_CINE=1; W._c2SkipCine=1; } catch(e){}
  var S=c2S(); S.e=S.e||{}; S.q=S.q||{};
  ['arrive','gymIn','genji','herbBrief','sumire','informant','infPunk','c2sRep','roam','called','c2lMap'].forEach(function(k){ S.e[k]=1; });
  delete S.e.run_fac; delete S.e.solo;
  delete S.e.fc51Hear; delete S.e.fc13sOut; delete S.e.fc13sTrk; delete S.e.ask44Beat;
  delete S.e.fc51Brawls; delete S.e.fc51Seen; delete S.e.lockAsk;
  ['X1','X2','X3','X4'].forEach(function(b){ delete S.e['g38win_'+b]; delete S.e['clash_'+b]; });
  S.f=S.f||{};
  ['p_x1_hus','p_x1_syn','p_x2_hus','p_x2_pnk','p_x3_pnk','p_x3_rid','p_x4_syn','p_x4_rid'].forEach(function(k){
    delete S.f[k]; delete S.f[k+'_0']; delete S.f[k+'_1'];
  });
  S.q.cq2_arrive=9; S.q.cq2_hq=9; S.q.cq2_scout=9;
  S.q.cq2_word=0; S.q.cq2_locks=0; S.qa='cq2_locks';
  SAVE.chapter=2; SAVE.bond=SAVE.bond||{}; SAVE.bond.path='balanced'; SAVE.bond.lock=1;
  SAVE.qa='cq2_locks'; SAVE.qs=SAVE.qs||{};
  SAVE.qs.cq2_arrive=9; SAVE.qs.cq2_hq=9; SAVE.qs.cq2_scout=9;
  SAVE.qs.cq2_word=0; SAVE.qs.cq2_locks=0;
  try { if (typeof c2QSync==='function') c2QSync(); } catch(e){}
  try { save(); } catch(e2){}
  return { qa:S.qa, c2lMap:!!S.e.c2lMap, roam:!!S.e.roam, hear:!!S.e.fc51Hear, run:S.e.run_fac||null };
})()
"""

HOOK = r"""
(function(){
  if (window.__hk) return 1;
  window.__hk=1; window.__ctxs=[]; window.__evs=[];
  var f0=fight;
  fight=function(grp,boss,ctx){ try{ window.__ctxs.push({grp:grp,ctx:ctx||{}}); }catch(e){} return f0.apply(this,arguments); };
  var e0=ev;
  ev=function(k){ try{ var s=String(k||''); if(/world:(qs|c2v2|13u|nq|s2|nalley|g38t|fc13s|c2:lock|v6551|v6552|13t)/.test(s)) window.__evs.push(Math.round(performance.now())+' '+s); }catch(e){} return e0.apply(this,arguments); };
  return 1;
})()
"""

class Game:
    def __init__(self, port=None, out='/workspace/nailsalley/shots', throttle=None, index=None):
        self.throttle = throttle
        self.index = Path(index or INDEX)
        self.root = self.index.parent
        k = socket.socket(); k.bind(('127.0.0.1', 0)); self.port = port or k.getsockname()[1]; k.close()
        self.out = Path(out); self.out.mkdir(parents=True, exist_ok=True)
        self.errs = []

    async def __aenter__(self):
        self.srv = TS(('127.0.0.1', self.port), functools.partial(Q, directory=str(self.root)))
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.p = await async_playwright().start()
        self.b = await self.p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required'])
        self.ctx = await self.b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=1)
        self.pg = await self.ctx.new_page()
        self.pg.on('pageerror', lambda e: self.errs.append(str(e)))
        if self.throttle:
            self.cdp = await self.ctx.new_cdp_session(self.pg)
            await self.cdp.send('Emulation.setCPUThrottlingRate', {'rate': self.throttle})
        html = self.index.read_text(encoding='utf-8')
        needle = 'var W = { guards: [], paused: false'
        if needle in html:
            html = html.replace(needle, 'root.__ev=function(s){return eval(s)};' + needle, 1)
        else:
            html = html.replace('root.FFF_13U = { CONTEST', 'root.__ev=function(s){return eval(s)};root.FFF_13U = { CONTEST', 1)
        async def rt(route):
            await route.fulfill(body=html, content_type='text/html')
        await self.pg.route('**/index.html', rt)
        await self.pg.goto(f'http://127.0.0.1:{self.port}/index.html', timeout=120000)
        await self.pg.wait_for_function('()=>!!(window.WORLD_API)', timeout=90000)
        await self.wait(600)
        return self

    async def __aexit__(self, *a):
        try:
            await self.b.close(); await self.p.stop()
        finally:
            self.srv.shutdown(); self.srv.server_close()

    async def ev(self, code):
        return await self.pg.evaluate(
            "(c)=>{var r=window.__ev(c);try{return (typeof r==='string')?r:JSON.parse(JSON.stringify(r===undefined?null:r))}catch(e){return String(r)}}",
            code,
        )

    async def wait(self, ms):
        await self.pg.wait_for_timeout(ms)

    async def skipall(self, n=10):
        for i in range(n):
            c = await self.pg.evaluate(SK)
            if not c:
                await self.wait(200)
                c = await self.pg.evaluate(SK)
                if not c:
                    break
            await self.pg.touchscreen.tap(*c)
            await self.wait(200)

    async def hush(self, keep=False):
        await self.ev(('(function(){ try{if(typeof phClose===\'function\')phClose()}catch(e){} W.paused=false;'
                       + ('' if keep else 'W.dlg=false;W.cut=false;W.busy=false;')
                       + 'W.path=[];W.fading=0; var d=document.getElementById(\'wdlg\'); if(d && !%s){d.className=\'\';d.innerHTML=\'\';} return 1})()' % ('true' if keep else 'false')))

    async def boot(self):
        await self.pg.touchscreen.tap(195, 420)
        await self.pg.evaluate('WORLD_API.enter(true)')
        await self.wait(1500)
        await self.skipall()
        await self.ev('root.FFF_NO_TUT=1;window.FFF_SKIP_C2_CINE=1;1')
        await self.pg.evaluate('WORLD_API.c2Begin(true)')
        await self.wait(2500)
        await self.skipall(14)
        await self.hush()
        hook = await self.ev(HOOK)
        seed = await self.ev(SEED)
        return {'hook': hook, 'seed': seed}

    async def gym_exit(self):
        await self.ev("c2Go('gym');1")
        await self.wait(900)
        await self.skipall(6)
        await self.hush()
        await self.ev("if(typeof c2Out==='function')c2Out('gym'); else if(typeof c2Go==='function')c2Go('town');1")
        await self.wait(1400)
        # dismiss the step-outside beat
        for i in range(20):
            st = await self.ev("({dlg:!!W.dlg,cut:!!W.cut,hear:!!(c2S()&&c2S().e&&c2S().e.fc51Hear),room:typeof c2Room==='function'&&c2Room(),xy:W.ryo&&[Math.round(W.ryo.x),Math.round(W.ryo.y)]})")
            if st and st.get('dlg'):
                await self.pg.touchscreen.tap(195, 700)
                await self.skipall(3)
            await self.wait(250)
            if st and st.get('hear') and st.get('room') == 'town' and not st.get('dlg') and i > 2:
                break
        await self.hush()
        return await self.ev("({room:c2Room(),hear:!!c2S().e.fc51Hear,xy:W.ryo&&[Math.round(W.ryo.x),Math.round(W.ryo.y)],g38:W.g38c&&W.g38c.b,nalley:!!root.FFF_NALLEY})")

    async def go_xy(self, x, y):
        await self.ev(f"""(function(){{
          W.dlg=false; W.busy=false; W.cut=false; W.path=[];
          if(W.ryo){{ W.ryo.x={x}; W.ryo.y={y}; W.ryo.v=0; if(typeof place==='function') place(W.ryo,0); if(typeof resetTrail==='function') resetTrail({x},{y},W.ryo.dir||0); }}
          if(W.aoi){{ W.aoi.x={x}+30; W.aoi.y={y}+16; if(typeof place==='function') place(W.aoi,0); }}
          try{{ if(typeof camera==='function') camera(true); }}catch(e){{}}
          try{{ if(typeof c2Pop==='function') c2Pop(); }}catch(e2){{}}
          return 1;
        }})()""")
        await self.wait(400)

    async def snapshot(self, b=None):
        return await self.ev(f"""(function(){{
          var B=(typeof G38T!=='undefined'&&G38T.BORDER)||{{}};
          var want={('["'+b+'"]') if b else 'Object.keys(B)'};
          var r=W.ryo||{{}}, e=(c2S()&&c2S().e)||{{}}, f=(c2S()&&c2S().f)||{{}};
          function men(k){{ return (W.dgF||[]).filter(function(o){{ return o&&o.crew===k&&o.s&&o.s.el&&o.s.el.parentNode; }}).map(function(o){{ return {{key:o.key,id:o.id,st:o.st,keep:!!o.nalleyKeep,x:Math.round(o.s.x),y:Math.round(o.s.y)}}; }}); }}
          var borders={{}};
          want.forEach(function(id){{
            var X=B[id]; if(!X) return;
            borders[id]={{ at:X.at, a:X.a, b:X.b, win:!!e['g38win_'+id], downA:!!(f[X.a]||f[X.a+'_0']), downB:!!(f[X.b]||f[X.b+'_0']), A:men(X.a), Z:men(X.b) }};
          }});
          return {{
            xy:r&&[Math.round(r.x),Math.round(r.y)],
            room:typeof c2Room==='function'&&c2Room(),
            hear:!!e.fc51Hear, run:e.run_fac||null, n13:e.n13||null, lockAsk:e.lockAsk||null,
            clash:W.g38c&&{{b:W.g38c.b,ph:W.g38c.ph}},
            keep:(W.dgF||[]).filter(function(o){{return o&&o.nalleyKeep;}}).map(function(o){{return o.id||o.crew;}}),
            flip: (function(){{ var el=document.querySelector('.n13'); if(!el) return null;
              var s=null; try{{ s=(W.c2n&&W.c2n.n13flip)||null; }}catch(e){{}}
              var x=null,y=null; if(s){{x=s.x;y=s.y;}}
              return {{x:x,y:y,cam:W.cam&&{{x:W.cam.x,y:W.cam.y,S:(WORLD_API&&WORLD_API.W&&WORLD_API.W.S)||1}}}};
            }})(),
            hs:!!document.getElementById('nalleyhs'),
            evs:(window.__evs||[]).slice(-30),
            borders:borders
          }};
        }})()""")

    async def shot(self, name, hush=True):
        if hush:
            await self.hush()
        path = self.out / (name + '.png')
        await self.pg.screenshot(path=str(path), type='png')
        return str(path)

    async def win_fight(self, ok=True):
        v = 'true' if ok else 'false'
        return await self.ev(f"""(function(){{
          var L=window.__ctxs[window.__ctxs.length-1]; if(!L) return 'nofight';
          var st={{ctx:L.ctx,endHp:40,endSpirit:0,win:{v},switches:0,foes:L.grp}};
          try{{ var g=document.getElementById('game'); if(g) g.classList.remove('on'); var r=document.getElementById('result'); if(r) r.classList.remove('on'); }}catch(e){{}}
          try{{ back({v}, st); }}catch(e){{ return 'err '+e.message; }}
          W.dgFight=null; W.busy=false;
          return 'back '+(L.ctx&&L.ctx.g38clash&&L.ctx.g38clash.b);
        }})()""")
