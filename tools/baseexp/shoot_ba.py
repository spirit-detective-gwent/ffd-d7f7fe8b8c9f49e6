#!/workspace/pwenv/bin/python3
"""Before (live v6.5.64) / after (branch) shots of the Cafeteria and Storehouse rooms. usage: shoot_ba.py LIVE BRANCH OUTDIR"""
import asyncio, sys, os, json
LIVE, BR, OUTD = sys.argv[1:4]
sys.argv = [sys.argv[0], BR, '52995']
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shoot_baseexp.py')).read().split('async def snap(')[0].replace("OUTD = sys.argv.pop()", ""))
CAFOK = "var C=cafS(); ['line','kitchen','staff','cooler','dock','dish','bakery','dining'].forEach(function(k){C.e[k]=1;}); save()"
FLDOK = "var S=fldS(); S.e.entry=1; S.f.fbay0=1; S.f.fbay1=1; S.e.surprise=1; ['bay','lockers','coach','track','cage','showers','trainer','booth'].forEach(function(k){S.e[k]=1;}); save()"
# key, base, live room, branch room, Ryo at (pic px), camera centre or None
SH = [('caf_crate1', 'caf', 'kitchen', 'cooler', [560, 520], [330, 470]), ('caf_crate2', 'caf', 'line', 'dock', [560, 520], [330, 400]),
      ('caf_crate3', 'caf', 'staff', 'bakery', [930, 560], [860, 450]), ('caf_kitchen', 'caf', 'kitchen', 'kitchen', [500, 420], [576, 380]),
      ('fld_bay', 'fld', 'bay', 'bay', [400, 450], [300, 470]), ('fld_lockers', 'fld', 'lockers', 'lockers', [576, 640], [576, 470]),
      ('fld_coach', 'fld', 'coach', 'coach', [600, 400], [576, 300]), ('fld_hurdle', 'fld', 'coach', 'cage', [500, 470], [400, 470]),
      ('fld_track', 'fld', 'track', 'track', [1100, 450], [1150, 450])]
async def run(p, tree, port, tag):
    global root, PORT
    root, PORT = Path(tree), port; h = serve(root, port); out = {}
    b, ctx, pg, errs = await boot(p); await ev(pg, STUB)
    for key, base, lr_, br_, at, cm in SH:
        k = lr_ if tag == 'live' else br_
        if base == 'caf' and not await ev(pg, "!!(typeof cafRoom==='function'&&cafRoom())"): await enter(pg, 'caf'); await ev(pg, CAFOK + "; 1")
        if base == 'fld' and not await ev(pg, "!!fldRoom()"): await enter(pg, 'fld'); await ev(pg, FLDOK + "; 1")
        await go(pg, base, k); await put(pg, *at); await ev(pg, "var f=(W.dgF||[]).find(q=>q.grd); if(f){f.gT=99;} 1")
        if cm: await ev(pg, "(function(){ var R=%s.%s, c0=lw(R,%s), c=camAt(c0[0],c0[1]); W.pan={scr:1, run:function(){ W.cam.x=c[0]; W.cam.y=c[1]; }}; })(); 1" % ('CAFG' if base == 'caf' else 'FLDG', k, json.dumps(cm)))
        await pg.wait_for_timeout(1000)
        pth = os.path.join(OUTD, 'raw', 'ba_%s_%s.png' % (key, tag)); await pg.screenshot(path=pth); out[key] = (pth, k); await ev(pg, "W.pan=null; 1")
    print(tag, 'errs', errs); await b.close(); h.shutdown(); return out
async def main():
    os.makedirs(os.path.join(OUTD, 'raw'), exist_ok=True)
    async with async_playwright() as p:
        L = await run(p, LIVE, 52996, 'live'); B = await run(p, BR, 52997, 'branch')
    for title, keys, fn in [('Cafeteria before (live v6.5.64) / after: crate rooms -> guarded rooms, Kitchen doors', ['caf_crate1', 'caf_crate2', 'caf_crate3', 'caf_kitchen'], 'ba_cafeteria.png'),
                            ('Storehouse before (live v6.5.64) / after: new doors, hurdles moved, track gate + rings', ['fld_bay', 'fld_lockers', 'fld_coach', 'fld_hurdle', 'fld_track'], 'ba_storehouse.png')]:
        fr = []
        for k in keys:
            fr.append((L[k][0], 'BEFORE ' + L[k][1])); fr.append((B[k][0], 'AFTER ' + B[k][1]))
        strip(fr, os.path.join(OUTD, fn), title)
asyncio.run(main())
