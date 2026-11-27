#!/workspace/pwenv/bin/python3
"""Usage: perf_check.py OLD_REF NEW_REF [--runs 2] [--soak 10] [--throttle 4] [--quick]
Creates temp git worktrees, serves each, measures idle/overworld/battle/soak at iPhone size. Writes results.json + report.md here."""
import asyncio,sys,json,subprocess,os,statistics,threading,http.server,socketserver,functools,tempfile,argparse,shutil
from playwright.async_api import async_playwright
ap=argparse.ArgumentParser();ap.add_argument('old');ap.add_argument('new');ap.add_argument('--runs',type=int,default=2)
ap.add_argument('--soak',type=int,default=10);ap.add_argument('--throttle',type=float,default=4);ap.add_argument('--quick',action='store_true')
ap.add_argument('--only',default='');ap.add_argument('--walk',type=int,default=60);ap.add_argument('--repo',default='/workspace/ffd');A=ap.parse_args()
OUT=os.path.dirname(os.path.abspath(__file__))
T_TITLE,T_OVER,T_BATTLE=(6,8,25) if A.quick else (20,30,75)
SAMPLER="""()=>{window.__ft=[];var l=performance.now();window.__run=true;(function f(t){if(!window.__run)return;window.__ft.push(t-l);l=t;requestAnimationFrame(f)})(l);}"""
def stats(ft):
  ft=[x for x in ft[2:]]
  if not ft: return {}
  tot=sum(ft);s=sorted(ft,reverse=True);n=max(1,len(ft)//100)
  return dict(fps=round(1000*len(ft)/tot,1),low1=round(1000/(sum(s[:n])/n),1),over20=sum(1 for x in ft if x>20),over33=sum(1 for x in ft if x>33.4),frames=len(ft),worst=round(s[0],0),ft_med=round(sorted(ft)[len(ft)//2],2),ft_p95=round(sorted(ft)[int(len(ft)*0.95)],2))
async def metrics(cdp):
  m=await cdp.send('Performance.getMetrics');return {x['name']:x['value'] for x in m['metrics']}
async def window(pg,cdp,secs,act=None):
  await pg.evaluate(SAMPLER);m0=await metrics(cdp)
  if act: await act()
  else: await pg.wait_for_timeout(secs*1000)
  m1=await metrics(cdp);await pg.evaluate("window.__run=false");ft=await pg.evaluate("window.__ft")
  wall=m1['Timestamp']-m0['Timestamp'];r=stats(ft)
  r['cpu_busy_pct']=round(100*(m1['TaskDuration']-m0['TaskDuration'])/wall,1)
  r['script_pct']=round(100*(m1['ScriptDuration']-m0['ScriptDuration'])/wall,1)
  r['heap_mb']=round(m1['JSHeapUsedSize']/1e6,1);return r
async def newpage(b,url,thr):
  ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,is_mobile=True,has_touch=True,
    user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
  pg=await ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:150]))
  cdp=await ctx.new_cdp_session(pg);await cdp.send('Performance.enable')
  if thr>1: await cdp.send('Emulation.setCPUThrottlingRate',{'rate':thr})
  await pg.goto(url);await pg.wait_for_timeout(3500);return ctx,pg,cdp,errs
async def tap(pg,x,y): await pg.touchscreen.tap(x,y)
async def center(pg,sel):
  return await pg.evaluate("(s)=>{var e=document.querySelector(s);if(!e)return null;var r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}",sel)
async def start_battle(pg,path='balanced'):
  await pg.evaluate("(p)=>FFF_UI.startMatch('ryo',{foes:['tut1'],hp:0,boss:false,drop:0,partner:'Aoi',esc:null,bench:{ch:'aoi',pst:{hp:46,spirit:40,sig2:null,disc:0,cmax:3,combo:true},path:p},pst:{combo:true,hp:46,spirit:40,sig2:null,disc:0,cmax:3}})",path)
  await pg.wait_for_timeout(5500)
READY="FFF.b&&!FFF.b.over&&FFF.b.turn===0&&!FFF.busy&&FFF.phase==='play'"
async def reset(pg):
  await pg.evaluate("""()=>{var b=FFF.b;b.turn=0;FFF.busy=false;FFF.phase='play';var s=b.s[0];s.hp=s.max=9999;s.spirit=40;b.bench.spirit=40;s.combo=true;s.cmax=3;b.s[1].hp=b.s[1].max=99999;b.s[1].guard=0;FFF.sel=null;FFF.combo=[];FFF.render()}""")
  await pg.wait_for_timeout(500)
async def wait_ready(pg,t=30000):
  try: await pg.wait_for_function(READY,timeout=t);return True
  except Exception: return False
async def do_combo(pg,n):
  await reset(pg)
  await pg.evaluate("""(n)=>{var s=FFF.b.s[0],CD=window.CARD_DATA.cards;var base=s.hand.find(c=>c.t==='atk')||s.hand[0];
   s.hand=[0,1,2].map(i=>Object.assign({},base,{u:900+i}));FFF.sel=900;FFF.combo=n===3?[901,902]:[901];FFF.render()}""",n)
  await pg.wait_for_timeout(600);c=await center(pg,'#preview .card, #preview')
  if c: await tap(pg,*c)
  await pg.wait_for_timeout(1500);await pg.mouse.click(1,1) if False else None
async def do_sig(pg):
  await reset(pg);c=await center(pg,'#btnAct')
  if c: await tap(pg,*c)
  await pg.wait_for_timeout(1200);c=await center(pg,'#preview .card, #preview')
  if c: await tap(pg,*c)
async def do_dbl(pg):
  await reset(pg);await pg.wait_for_timeout(500);c=await center(pg,'#btnDbl')
  if c: await tap(pg,*c)
BYSTEP={}
async def battle_loop(pg,secs,log):
  import time;t0=time.time();k=0
  seq=[('dbl2',lambda:do_combo(pg,2)),('tri',lambda:do_combo(pg,3)),('sig',lambda:do_sig(pg)),('partner',lambda:do_dbl(pg))]
  while time.time()-t0<secs:
    nm,f=seq[k%4];k+=1;i0=await pg.evaluate("window.__ft.length");await f();ok=await wait_ready(pg,25000)
    seg=await pg.evaluate("(i)=>window.__ft.slice(i)",i0);seg=seg[2:] or [16.7]
    BYSTEP.setdefault(nm,[]).append((sum(1 for x in seg if x>20),len(seg),round(max(seg)),round(sum(seg)/len(seg),2)))
    log.append((nm,ok))
    if not ok: # recover (e.g. stuck cutscene): tap to skip
      await tap(pg,195,300);await wait_ready(pg,5000)

SK="""()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""
async def skipall(pg,n=6):
  for i in range(n):
    c=await pg.evaluate(SK)
    if not c:
      await pg.wait_for_timeout(700);c=await pg.evaluate(SK)
      if not c: break
    await pg.touchscreen.tap(*c);await pg.wait_for_timeout(700)
  await pg.evaluate("(()=>{var b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Close'&&e.offsetParent);if(b)b.click()})()")
# Spots (world px). Ch1 map = school (start 1440,3820; gym door 1470,930; main bldg 1440,2460). Ch2 map = Kitsune-Chuo
# town (start 1080,900): gym door [910,2640], Chuo-dori border X1 [1900,1800], Lantern Alley [4060,2720], town centre [2560,2300].
SPOTS=[('ch1_grounds',1,(1440,1700)),('ch2_genji_gym',2,(910,2700)),('ch2_chuo_border',2,(1900,1800)),('ch2_lantern_alley',2,(4060,2720)),('ch2_town_centre',2,(2560,2300))]
if os.environ.get('PERF_SPOTS'): SPOTS=[x for x in SPOTS if x[0] in os.environ['PERF_SPOTS'].split(',')]
async def world_dom(pg): return await pg.evaluate("document.getElementById('world').getElementsByTagName('*').length")
async def tele(pg,x,y):
  await pg.evaluate("(a)=>{var A=WORLD_API,W=A.W;var c=A.walkableAt(a[0],a[1]);W.ryo.x=a[0];W.ryo.y=a[1];W.aoi.x=a[0];W.aoi.y=a[1]+60;A.camera(true)}",[x,y]);await pg.wait_for_timeout(2500)
async def walk_window(pg,cdp,x,y,secs):
  import time
  async def walk():
    t0=time.time();k=0
    while time.time()-t0<secs:
      dx,dy=[(300,0),(-300,0),(0,250),(0,-250)][k%4];k+=1
      await pg.evaluate("(a)=>{var A=WORLD_API,W=A.W;var tx=W.ryo.x+a[0],ty=W.ryo.y+a[1];if(!A.walkableAt(tx,ty)){tx=a[2];ty=a[3]}A.walkTo(tx,ty,false,false)}",[dx,dy,x,y]);await pg.wait_for_timeout(2500)
  return await window(pg,cdp,0,walk)
async def world_run(pg,cdp,thr):
  res={'spots':{}};secs=5 if A.quick else 8
  await pg.evaluate("WORLD_API.enter(true)");await pg.wait_for_timeout(1500);await skipall(pg)
  for nm,ch,(x,y) in SPOTS:
    if ch==2 and 'ch2_started' not in res:
      res['ch2_started']=1;await pg.evaluate("WORLD_API.c2Begin(true)");await pg.wait_for_timeout(2500);await skipall(pg);await pg.wait_for_timeout(1500)
    await tele(pg,x,y)
    if nm=='ch1_grounds':
      await gc(cdp);res['ch1_heap_after_gc_mb']=round((await metrics(cdp))['JSHeapUsedSize']/1e6,1)
    r=await window(pg,cdp,secs);r['draw_items']=await world_dom(pg);res['spots'][nm]=r
    if nm in ('ch1_grounds','ch2_town_centre') and thr<=1:
      res['walk_'+nm.split('_')[0]]=await walk_window(pg,cdp,x,y,10 if A.quick else A.walk)
  return res
async def counts(pg):
  return await pg.evaluate("({dom:document.getElementsByTagName('*').length,canv:document.getElementsByTagName('canvas').length,jsmem:performance.memory?performance.memory.usedJSHeapSize:0})")
async def gc(cdp):
  for _ in range(3): await cdp.send('HeapProfiler.collectGarbage')
async def scenario(b,url,thr,which):
  ctx,pg,cdp,errs=await newpage(b,url,thr);res={}
  try:
    if which=='title':
      res=await window(pg,cdp,T_TITLE)
    elif which=='world':
      res=await world_run(pg,cdp,thr)
    elif which=='battle':
      await tap(pg,195,420);await start_battle(pg);log=[]
      async def act(): await battle_loop(pg,T_BATTLE,log)
      res=await window(pg,cdp,0,act);res['turns']=len(log);res['by_step']={k:dict(n=len(v),over20_per_step=round(sum(q[0] for q in v)/len(v),1),frames_per_step=round(sum(q[1] for q in v)/len(v)),avg_ft=round(sum(q[3] for q in v)/len(v),2),worst=max(q[2] for q in v)) for k,v in BYSTEP.items()};BYSTEP.clear();res['stuck']=sum(1 for _,o in log if not o)
    elif which=='pick':
      await tap(pg,195,420);await start_battle(pg);await reset(pg);res=await window(pg,cdp,T_OVER if not A.quick else 6)
    elif which=='soak':
      await tap(pg,195,420);series=[]
      for i in range(A.soak):
        await start_battle(pg);await reset(pg)
        await do_combo(pg,2);await wait_ready(pg,25000)
        await do_sig(pg);await wait_ready(pg,25000)
        await pg.evaluate("FFF.b.s[1].hp=1;FFF.b.s[1].max=99999");await do_combo(pg,2);await pg.wait_for_timeout(9000)
        await pg.evaluate("(()=>{try{FFF_UI.leave&&FFF_UI.leave()}catch(e){}})()")
        await pg.goto(url) if False else None
        await gc(cdp);m=await metrics(cdp);c=await counts(pg)
        series.append(dict(i=i+1,heap_mb=round(m['JSHeapUsedSize']/1e6,2),dom=c['dom'],canv=c['canv'],listeners=int(m.get('JSEventListeners',0)),nodes=int(m.get('Nodes',0))))
      res=dict(series=series)
      h=[s['heap_mb'] for s in series];n=len(h)
      if n>=3:
        xs=list(range(n));mx=sum(xs)/n;my=sum(h)/n;res['heap_slope_mb_per_battle']=round(sum((x-mx)*(y-my) for x,y in zip(xs,h))/sum((x-mx)**2 for x in xs),3)
        res['dom_slope']=round(sum((x-mx)*(s['dom']-sum(q['dom'] for q in series)/n) for x,s in zip(xs,series))/sum((x-mx)**2 for x in xs),2)
        res['listener_delta']=series[-1]['listeners']-series[0]['listeners']
  except Exception as e: res['error']=repr(e)[:200]
  res['errs']=errs[:3];await ctx.close();return res
def serve(d):
  h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=d)
  class Q(h.func):
    def log_message(s,*a):pass
  s=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(Q,directory=d));s.daemon_threads=True
  threading.Thread(target=s.serve_forever,daemon=True).start();return s
async def main():
  tmp=tempfile.mkdtemp(prefix='perf_');wts={};srv={}
  for lab,ref in (('old',A.old),('new',A.new)):
    d=os.path.join(tmp,lab);subprocess.check_call(['git','-C',A.repo,'worktree','add','--detach',d,ref],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    wts[lab]=d;srv[lab]=serve(d)
  R={'old':{},'new':{}}
  try:
    async with async_playwright() as p:
      b=await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required','--enable-precise-memory-info','--js-flags=--expose-gc'])
      plan=[('native',1,w) for w in ['title','world','pick','battle']]+[('thr',A.throttle,w) for w in ['world','battle']]+[('native',1,'soak')]
      if A.only: plan=[p for p in plan if p[2] in A.only.split(',')]
      for mode,thr,which in plan:
        key=mode+':'+which
        for run in range(1 if which=='soak' else A.runs):
          for lab in (('old','new') if run%2==0 else ('new','old')):
            url=f"http://127.0.0.1:{srv[lab].server_address[1]}/index.html"
            r=await scenario(b,url,thr,which);R[lab].setdefault(key,[]).append(r);print(lab,key,json.dumps(r)[:260],flush=True)
      await b.close()
  finally:
    for lab,d in wts.items():
      srv[lab].shutdown();subprocess.call(['git','-C',A.repo,'worktree','remove','--force',d],stderr=subprocess.DEVNULL)
    shutil.rmtree(tmp,ignore_errors=True)
  json.dump(R,open(os.path.join(OUT,'results_'+(A.only.replace(',','_') or 'full')+'.json'),'w'),indent=1)
  def M(v): return round(statistics.median(v),2) if v else None
  def get(lab,key,path):
    out=[]
    for r in R[lab].get(key,[]):
      x=r
      try:
        for p in path: x=x[p]
        out.append(x)
      except Exception: pass
    return M(out)
  G=[];P=lambda ok:'PASS' if ok else 'FAIL'
  L=[f"# perf_check {A.old} (OLD) vs {A.new} (NEW)  390x844 DPR3 mobile; throttled runs x{A.throttle}; medians of {A.runs}\n"]
  def row(name,key,path,unit=''):
    o,n=get('old',key,path),get('new',key,path);L.append(f"| {name} | {o} | {n} |");return o,n
  L+=["| metric | OLD | NEW |","|--|--|--|"]
  for k in ['fps','low1','over20','over33','cpu_busy_pct','script_pct']:
    for w in ['title','pick','battle']: row(f"native {w} {k}",'native:'+w,[k])
  for nm,ch,_ in SPOTS:
    for k in ['fps','low1','cpu_busy_pct','draw_items']: row(f"native {nm} {k}",'native:world',['spots',nm,k])
  for ch in ('ch1','ch2'):
    for k in ['fps','low1','over20','cpu_busy_pct']: row(f'native long walk {ch} {k}','native:world',['walk_'+ch,k])
  row('Ch1 heap after GC MB','native:world',['ch1_heap_after_gc_mb'])
  for nm,ch,_ in SPOTS:
    for k in ['fps','cpu_busy_pct','ft_med','ft_p95']: row(f"x{A.throttle:g} {nm} {k}",'thr:world',['spots',nm,k])
  for k in ['fps','low1','over20','cpu_busy_pct']: row(f"x{A.throttle:g} battle {k}",'thr:battle',[k])
  # gates
  L.append("\n## Gates (NEW vs OLD)")
  def g(name,ok,detail):
    if 'None' in detail.split(';')[0]: L.append(f"- SKIP {name}: no data (scenario not run)");return
    L.append(f"- {P(ok)} {name}: {detail}");G.append(ok)
  for nm,ch,_ in SPOTS:
    n=get('new','native:world',['spots',nm,'fps']);o=get('old','native:world',['spots',nm,'fps']);g(f"{nm} fps>=58",n is not None and n>=58,f"new {n} old {o}")
  n=get('new','native:pick',['fps']);g("card-pick fps>=55",n is not None and n>=55,f"new {n} old {get('old','native:pick',['fps'])}")
  n=get('new','native:battle',['fps']);g("battle fps>=55",n is not None and n>=55,f"new {n} old {get('old','native:battle',['fps'])}")
  for ch in ('ch1','ch2'):
    n=get('new','native:world',['walk_'+ch,'fps']);g(f"long walk {ch} fps>=50 (60s)",n is not None and n>=50,f"new {n} old {get('old','native:world',['walk_'+ch,'fps'])}; 1% low new {get('new','native:world',['walk_'+ch,'low1'])} old {get('old','native:world',['walk_'+ch,'low1'])}")
  for nm,ch,_ in SPOTS:
    for k in ['ft_med','ft_p95']:
      n=get('new','thr:world',['spots',nm,k]);o=get('old','thr:world',['spots',nm,k]);g(f"x{A.throttle:g} {nm} {k} not heavier (<=+10%)",n is not None and o is not None and n<=o*1.10+0.5,f"new {n} old {o} ms")
  n=get('new','thr:battle',['fps']);o=get('old','thr:battle',['fps']);g(f"x{A.throttle:g} battle fps>=55 and within 3% of OLD",n is not None and n>=55 and o is not None and n>=o*0.97,f"new {n} old {o}")
  n=get('new','native:world',['spots','ch1_grounds','draw_items']);g("Ch1 draw items<=233",n is not None and n<=233,f"new {n} old {get('old','native:world',['spots','ch1_grounds','draw_items'])}")
  for nm,ch,_ in SPOTS[1:]:
    n=get('new','native:world',['spots',nm,'draw_items']);o=get('old','native:world',['spots',nm,'draw_items']);g(f"{nm} draw items growth<=40",n is not None and o is not None and n-o<=40,f"new {n} old {o}")
  n=get('new','native:world',['ch1_heap_after_gc_mb']);g("Ch1 JS memory<=116MB (after GC)",n is not None and n<=116,f"new {n} old {get('old','native:world',['ch1_heap_after_gc_mb'])}")
  for lab in ('old','new'):
    for r in R[lab].get('native:soak',[]):
      L.append(f"\nSoak {lab}: heap slope MB/battle={r.get('heap_slope_mb_per_battle')} domSlope={r.get('dom_slope')} listenerDelta={r.get('listener_delta')}")
      L.append("heap after GC: "+", ".join(str(q['heap_mb']) for q in r.get('series',[]))+" | dom: "+", ".join(str(q['dom']) for q in r.get('series',[]))+" | canvases: "+", ".join(str(q['canv']) for q in r.get('series',[])))
  sl=[r.get('heap_slope_mb_per_battle') for r in R['new'].get('native:soak',[])]
  g("soak heap not trending up (slope<=0.3MB/battle)",bool(sl) and sl[0] is not None and sl[0]<=0.3,f"new slope {sl}")
  for mode in ('native:battle','thr:battle'):
    for lab in ('old','new'):
      for r in R[lab].get(mode,[])[:1]: L.append(f"\nper-step {mode} {lab}: "+json.dumps(r.get('by_step')))
  L.append("\nSee battle_bench.py (per-step throttled breakdown): run `battle_bench.py URL_OLD URL_NEW --thr 4`")
  L.append("\nOVERALL: "+P(all(G)))
  open(os.path.join(OUT,'report_'+(A.only.replace(',','_') or 'full')+'.md'),'w').write("\n".join(L));print("\n".join(L))
asyncio.run(main())
