#!/workspace/pwenv/bin/python3
"""Hook AU.play / qBanner / ev, seed Four Corners pickup, exit gym, walk the street, log SFX."""
import asyncio, json, http.server, socketserver, threading, functools
from pathlib import Path
from playwright.async_api import async_playwright

FFD = '/workspace/ffd-qsnd'
PORT = 8971
OUT = Path('/tmp/qsnd')
SK = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^Skip/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return null;var r=b[0].getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}"""

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def serve(port, directory=FFD):
    s = TS(('127.0.0.1', port), functools.partial(Q, directory=directory))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s

def body():
    t = Path(FFD + '/index.html').read_text(encoding='utf-8')
    needle = 'var W = { guards: [], paused: false'
    assert needle in t, 'W decl missing'
    t = t.replace(needle, 'root.__ev=function(s){return eval(s)};' + needle, 1)
    return t

async def ev(pg, code):
    return await pg.evaluate(
        """(c)=>{var r=window.__ev(c);try{return (r&&typeof r.then==='function')?'THEN':(typeof r==='string'?r:JSON.parse(JSON.stringify(r===undefined?null:r)))}catch(e){return String(r)}}""",
        code,
    )

HOOK = r"""
if (window.__sfxhook) 'already';
else (function(){
  window.__sfxhook = 1;
  window.__sfxlog = [];
  function rec(src, name, extra) {
    var st = '';
    try { st = (new Error()).stack || ''; } catch (e) {}
    var lines = st.split('\n').map(function (s) { return s.trim(); }).filter(Boolean).slice(2, 10);
    var S = null, e = {}, qa = '', qs = null;
    try { S = typeof c2S === 'function' ? c2S() : null; e = (S && S.e) || {}; } catch (err) {}
    try { qa = (S && S.qa) || (SAVE && SAVE.qa) || ''; qs = (S && S.q) || (SAVE && SAVE.qs) || null; } catch (err2) {}
    window.__sfxlog.push({
      t: Math.round(performance.now()),
      src: src,
      name: name,
      extra: extra || null,
      x: (W.ryo && Math.round(W.ryo.x)) || 0,
      y: (W.ryo && Math.round(W.ryo.y)) || 0,
      room: (typeof c2Room === 'function' && c2Room()) || (W.inside && W.inside.id) || '',
      loc: W.loc || '',
      dlg: !!W.dlg,
      cut: !!W.cut,
      busy: !!W.busy,
      qa: qa,
      qs: qs ? JSON.parse(JSON.stringify(qs)) : null,
      hear: !!(e.fc51Hear),
      out: !!(e.fc13sOut),
      banner: (function () {
        var o = document.getElementById('wquest');
        return o && (o.classList.contains('go') || o.innerText) ? (o.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 160) : '';
      })(),
      stack: lines
    });
  }
  window.__sfxrec = rec;
  if (typeof AU !== 'undefined' && AU.play) {
    var p0 = AU.play;
    AU.play = function (n, o) {
      rec('AU.play', String(n), { gain: o && o.gain, pan: o && o.pan });
      return p0.apply(this, arguments);
    };
  }
  if (typeof qBanner === 'function') {
    var qb = qBanner;
    qBanner = function (k, t, s) {
      rec('qBanner', String(k), { title: t, sub: s });
      return qb.apply(this, arguments);
    };
  }
  if (typeof ev === 'function') {
    var ev0 = ev;
    ev = function (k) {
      var s = String(k || '');
      if (/quest|banner|beacon|qdone|qready|codex|outside|fc13s|13t:|sfx|roundwin|complete/i.test(s)) rec('ev', s);
      return ev0.apply(this, arguments);
    };
  }
  'hooked';
})()
"""

SEED = r"""
(function(){
  try { window.FFF_SKIP_C2_CINE = 1; W._c2SkipCine = 1; } catch (e) {}
  var S = c2S();
  S.e = S.e || {};
  S.q = S.q || {};
  ['arrive','gymIn','genji','herbBrief','sumire','informant','infPunk','c2sRep','roam','called','c2lMap'].forEach(function (k) { S.e[k] = 1; });
  delete S.e.fc51Hear; delete S.e.fc13sOut; delete S.e.fc13sTrk; delete S.e.ask44Beat; delete S.e.fc51Brawls; delete S.e.fc51Seen;
  S.q.cq2_arrive = 9; S.q.cq2_hq = 9; S.q.cq2_scout = 9;
  S.q.cq2_word = 0; S.q.cq2_locks = 0;
  S.qa = 'cq2_locks';
  SAVE.chapter = 2;
  SAVE.qa = 'cq2_locks';
  SAVE.qs = SAVE.qs || {};
  SAVE.qs.cq2_arrive = 9; SAVE.qs.cq2_hq = 9; SAVE.qs.cq2_scout = 9;
  SAVE.qs.cq2_word = 0; SAVE.qs.cq2_locks = 0;
  if (typeof save === 'function') save();
  if (typeof c2QSync === 'function') c2QSync();
  return { eKeys: Object.keys(S.e).filter(function (k) { return S.e[k]; }), q: S.q, qa: S.qa, room: (typeof c2Room === 'function' && c2Room()) };
})()
"""

DUMP = r"""
(function(){
  var d = (C2W && C2W.doors && C2W.doors.gym) || null;
  var B = (typeof G38T !== 'undefined' && G38T.BORDER) || {};
  var borders = {};
  Object.keys(B).forEach(function (k) { borders[k] = { at: B[k].at, n: B[k].n, a: B[k].a, b: B[k].b }; });
  var r = W.ryo || {};
  var e = (c2S() && c2S().e) || {};
  return {
    gymDoor: d,
    ryo: { x: r.x, y: r.y, room: (typeof c2Room === 'function' && c2Room()), inside: W.inside && W.inside.id, loc: W.loc },
    borders: borders,
    qa: SAVE.qa,
    qs: SAVE.qs,
    cq: c2S().q,
    flags: { c2lMap: !!e.c2lMap, fc51Hear: !!e.fc51Hear, fc13sOut: !!e.fc13sOut, genji: !!e.genji, phase: (window.FFF_13T && FFF_13T.phase && FFF_13T.phase()) }
  };
})()
"""

HUSH = r"""
(function(){
  try { if (typeof phClose === 'function') phClose(); } catch (e) {}
  W.paused = false; W.dlg = false; W.cut = false; W.busy = false; W.path = []; W.fading = 0;
  var d = document.getElementById('wdlg'); if (d) { d.className = ''; d.innerHTML = ''; }
  1;
})()
"""

async def skipall(pg, n=10):
    for i in range(n):
        c = await pg.evaluate(SK)
        if not c:
            await pg.wait_for_timeout(250)
            c = await pg.evaluate(SK)
            if not c:
                break
        await pg.touchscreen.tap(*c)
        await pg.wait_for_timeout(280)

async def slog(pg, label=''):
    log = await ev(pg, "window.__sfxlog||[]") or []
    interesting = []
    for x in log:
        name = str(x.get('name') or '')
        src = x.get('src') or ''
        extra = x.get('extra') or {}
        if name in ('roundwin', 'quest_ready', 'katana_unsheathe', 'select') or src in ('qBanner', 'ev') or 'complete' in name.lower() or 'QUEST' in str(extra):
            interesting.append(x)
    print(f'--- log {label}: {len(log)} total, {len(interesting)} interesting ---')
    for x in interesting:
        print(json.dumps({
            't': x.get('t'), 'src': x.get('src'), 'name': x.get('name'), 'extra': x.get('extra'),
            'xy': [x.get('x'), x.get('y')], 'room': x.get('room'), 'loc': x.get('loc'),
            'dlg': x.get('dlg'), 'qa': x.get('qa'), 'hear': x.get('hear'), 'out': x.get('out'),
            'banner': x.get('banner'),
            'stack0': ((x.get('stack') or [''])[0] or '')[:200]
        }, ensure_ascii=False))
    return log

async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    s = serve(PORT)
    print('loading html...')
    html = body()
    print('html bytes', len(html))
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:240]))
        async def rt(route):
            await route.fulfill(body=html, content_type='text/html')
        await pg.route('**/index.html', rt)
        await pg.goto(f'http://127.0.0.1:{PORT}/index.html')
        await pg.wait_for_function("()=>!!(window.WORLD_API && window.__ev)", timeout=90000)
        await pg.wait_for_timeout(800)
        await pg.touchscreen.tap(195, 420)
        await pg.evaluate("WORLD_API.enter(true)")
        await pg.wait_for_timeout(1500)
        await skipall(pg)
        await ev(pg, "window.FFF_SKIP_C2_CINE=1;W._c2SkipCine=1;1")
        await pg.evaluate("WORLD_API.c2Begin(true)")
        await pg.wait_for_timeout(3000)
        await skipall(pg, 14)
        await ev(pg, HUSH)
        seed = await ev(pg, SEED)
        print('SEED', json.dumps(seed, default=str))
        await ev(pg, "c2Go('gym');1")
        await pg.wait_for_timeout(1000)
        await skipall(pg, 6)
        await ev(pg, HUSH)
        hook = await ev(pg, HOOK)
        print('HOOK', hook)
        dump = await ev(pg, DUMP)
        print('IN GYM', json.dumps(dump, default=str)[:2200])
        Path(OUT / 'pre.json').write_text(json.dumps({'seed': seed, 'dump': dump}, default=str, indent=2))

        await ev(pg, "window.__sfxlog=[];1")
        print('LEAVING GYM')
        await ev(pg, "if(typeof c2Out==='function')c2Out('gym'); else if(typeof c2Leave==='function')c2Leave();1")
        await pg.wait_for_timeout(1600)
        await slog(pg, 'after c2Out 1.6s')
        dump2 = await ev(pg, DUMP)
        print('AFTER OUT', json.dumps(dump2, default=str)[:1800])

        for i in range(24):
            st = await ev(pg, """({
              dlg:!!W.dlg, cut:!!W.cut,
              hear:!!(c2S()&&c2S().e&&c2S().e.fc51Hear),
              txt:(document.getElementById('wdlg')&&document.getElementById('wdlg').innerText||'').slice(0,140),
              banner:(document.getElementById('wquest')&&document.getElementById('wquest').innerText||'').replace(/\\s+/g,' ').trim().slice(0,160),
              xy:W.ryo&&[Math.round(W.ryo.x),Math.round(W.ryo.y)],
              room:typeof c2Room==='function'&&c2Room(),
              loc:W.loc
            })""")
            print('TICK', i, json.dumps(st, ensure_ascii=False))
            if st and (st.get('dlg') or st.get('txt')):
                await pg.touchscreen.tap(195, 700)
            await pg.wait_for_timeout(400)
            if st and st.get('hear') and not st.get('dlg') and i > 4:
                break

        await slog(pg, 'after hear-wait')
        pos = await ev(pg, "W.ryo&&[W.ryo.x,W.ryo.y]")
        print('POS after leave', pos)
        ox, oy = pos if pos and len(pos) == 2 else (910, 2700)
        targets = [
            (ox + 220, oy, 'east-short'),
            (ox + 500, oy, 'east-mid'),
            (ox + 220, oy - 220, 'ne'),
            (ox, oy - 280, 'north'),
            (ox + 800, oy, 'east-far'),
        ]
        for x, y, lab in targets:
            print('WALK', lab, x, y)
            await ev(pg, f"""
              W.dlg=false; W.busy=false; W.cut=false; W.path=[];
              if (window.WORLD_API && WORLD_API.walkToX) WORLD_API.walkToX({x},{y});
              else if (typeof walkTo==='function') walkTo({x},{y},true,true);
              else {{ W.ryo.x={x}; W.ryo.y={y}; if(typeof place==='function') place(W.ryo); }}
              1;
            """)
            await pg.wait_for_timeout(2000)
            st = await ev(pg, """({
              dlg:!!W.dlg,
              txt:(document.getElementById('wdlg')&&document.getElementById('wdlg').innerText||'').slice(0,80),
              banner:(document.getElementById('wquest')&&document.getElementById('wquest').innerText||'').replace(/\\s+/g,' ').trim().slice(0,160),
              xy:W.ryo&&[Math.round(W.ryo.x),Math.round(W.ryo.y)],
              loc:W.loc,
              hear:!!(c2S()&&c2S().e&&c2S().e.fc51Hear)
            })""")
            print('  at', json.dumps(st, ensure_ascii=False))
            if st and st.get('dlg'):
                for _ in range(8):
                    await pg.touchscreen.tap(195, 700)
                    await pg.wait_for_timeout(250)
            await slog(pg, 'after ' + lab)

        full = await ev(pg, "window.__sfxlog||[]") or []
        Path(OUT / 'sfxlog.json').write_text(json.dumps(full, indent=2, default=str))
        print('ERRS', errs)
        names = {}
        for x in full:
            k = str(x.get('src')) + ':' + str(x.get('name'))
            names[k] = names.get(k, 0) + 1
        print('COUNTS', json.dumps(names, indent=2))
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
