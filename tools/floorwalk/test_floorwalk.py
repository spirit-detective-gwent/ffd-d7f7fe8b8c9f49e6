#!/workspace/pwenv/bin/python3
"""v6566-floorwalk (Erik t545): floor props in the Storehouse and the Gym are flat floor Ryo walks over.
LANE 1 chalk tile (Storehouse Locker Corridor), ORDERS mat (Gym Foyer), HOME COURT mat (Bleacher Concourse),
GRAY COAT FILE mat (Trophy Hall). For each: no grid block, keyboard walk straight across, tap-walk path across,
'Look' still offered (floor tag) and the inspect line still plays, no page errors.
usage: test_floorwalk.py <worktree> [port] [--expect-blocked]   (--expect-blocked: sanity run on live, the props block)"""
import asyncio, sys, json, os
exec(open(__file__.rsplit('/', 1)[0] + '/lib.py').read())
LIVE = '--expect-blocked' in sys.argv
NEXT = """()=>{var b=[...document.querySelectorAll('button')].filter(e=>/^(Next|Skip|Close|OK|Got it)/.test((e.textContent||'').trim())&&e.offsetParent!==null);if(!b.length)return 0;b[0].click();return 1}"""
PROPS = [  # key, go-fn, room key, pic rect, spot id, act fn, dialog text
    ('lane', 'fldGo', 'FLDG', 'lockers', [520, 480, 630, 560], 'lane', 'fldAct', 'LANE 1'),
    ('orders', 'gymGo', 'GYMG', 'foyer', [200, 520, 380, 620], 'orders', 'gymAct', 'stack of orders'),
    ('banner', 'gymGo', 'GYMG', 'concourse', [520, 200, 760, 280], 'banner', 'gymAct', 'HOME COURT'),
    ('file', 'gymGo', 'GYMG', 'trophy', [180, 480, 420, 620], 'file', 'gymAct', 'GRAY COAT FILE'),
]
PREP = "(function(){ fight=function(){ ev('test:fight'); }; (W.dgF||[]).forEach(function(f){ if(f.s&&f.s.el) f.s.el.remove(); }); W.dgF=[]; W.dlg=false; W.busy=false; W.cut=false; W.path=[]; W.arrive=null; W.cool=0; W.fading=false; return 1; })()"
async def settle(pg, ms=1500):
    t = 0
    while t < ms:
        await pg.evaluate(NEXT); await pg.wait_for_timeout(100); t += 100
async def main():
    h = serve(root, PORT)
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p)
        await ev(pg, CLR)
        for key, go, G, room, r, spot, act, txt in PROPS:
            await ev(pg, f"W.fading=false; {go}('{room}'); 1"); await settle(pg, 1800); await ev(pg, CLR); await ev(pg, PREP)
            s = await ev(pg, f"{G}.{room}.s"); R = [v * s for v in r]; cx = (R[0] + R[2]) / 2; cy = (R[1] + R[3]) / 2
            blk = await ev(pg, f"(function(){{ var c=cellOf({cx},{cy}); return !free(c[0],c[1]); }})()")
            # 1. keyboard: start left of the prop on its middle row, hold ArrowRight
            await ev(pg, f"W.ryo.x={R[0] - 45}; W.ryo.y={cy}; W.ryo.v=0; place(W.ryo,0); W.path=[]; 1"); await pg.wait_for_timeout(200)
            await ev(pg, PREP)
            xs = []; await pg.keyboard.down('ArrowRight')
            for i in range(40):
                await pg.wait_for_timeout(80); q = await ev(pg, "[Math.round(W.ryo.x),Math.round(W.ryo.y)]"); xs.append(q)
                if q[0] > R[2] + 30: break
            await pg.keyboard.up('ArrowRight')
            inside = [q for q in xs if R[0] <= q[0] <= R[2] and R[1] <= q[1] <= R[3]]
            crossed = xs and xs[-1][0] > R[2] + 30 and len(inside) > 0
            moved = len(set(map(tuple, xs))) > 3
            # 2. tap-walk: from above-left to below-right of the prop through its centre (walkTo plans on the grid)
            await ev(pg, PREP)
            await ev(pg, f"W.ryo.x={R[0] - 45}; W.ryo.y={cy}; place(W.ryo,0); W.path=[]; 1")
            okw = await ev(pg, f"walkTo({R[2] + 45},{cy},true)")
            path = await ev(pg, "(W.path||[]).map(function(n){return [Math.round(n.x!=null?n.x:n[0]),Math.round(n.y!=null?n.y:n[1])]})")
            tw = []
            for i in range(40):
                await pg.wait_for_timeout(100); q = await ev(pg, "[Math.round(W.ryo.x),Math.round(W.ryo.y)]"); tw.append(q)
                if abs(q[0] - (R[2] + 45)) < 12 and abs(q[1] - cy) < 12: break
            tin = [q for q in tw if R[0] <= q[0] <= R[2] and R[1] <= q[1] <= R[3]]
            straight = max(abs(q[1] - cy) for q in tw) if tw else 999
            # 3. Look still offered (floor tag) and the inspect line plays
            await ev(pg, f"W.ryo.x={cx}; W.ryo.y={cy}; place(W.ryo,0); 1"); await pg.wait_for_timeout(300)
            tag = await ev(pg, f"(function(){{ var t=(W.tagL||[]).find(function(q){{return q.key==='{('sf_' if G=='FLDG' else 'gy_')+room}:{spot}'}}); return t?{{lab:t.lab,floor:t.floor||0,cls:t.cls||''}}:null; }})()")
            near = await ev(pg, "(function(){ var t=tagNear(); return t?t.key:null; })()")
            await ev(pg, f"{act}('{spot}'); 1"); d = ''
            for i in range(30):  # the line types out; wait for the full text
                await pg.wait_for_timeout(150); d = await ev(pg, DLG) or ''
                if txt in d: break
            await settle(pg, 1500); await ev(pg, CLR)
            info = dict(blk=blk, kb=xs[:3] + xs[-2:], kb_in=len(inside), tw_end=tw[-1:] if tw else None, tw_in=len(tin), dev=straight, tag=tag, near=near)
            if LIVE:
                ok(f'{key} live sanity: prop blocks (grid cell blocked, keyboard walk stops before it)', blk and not crossed, info)
                continue
            ok(f'{key} {room}: prop cell is free floor (no block)', not blk, info)
            ok(f'{key} {room}: keyboard walk goes straight across the prop (positions change, passes inside, ends past it)', crossed and moved, info)
            ok(f'{key} {room}: tap-walk crosses the prop on a straight line (no detour)', okw and len(tin) > 0 and straight <= 20 and tw and abs(tw[-1][0] - (R[2] + 45)) < 12, info)
            ok(f'{key} {room}: Look tag still offered as a floor tag; standing on it selects it', tag and tag['lab'] == 'Look' and tag['floor'] == 1 and near and near.endswith(':' + spot), info)
            ok(f'{key} {room}: inspect line still plays', txt in d, d[:120])
        ok('no page errors', not errs, errs)
        await b.close()
    h.shutdown()
    n = sum(1 for r in RES if r[0]); print(f'{n}/{len(RES)} passed'); sys.exit(0 if n == len(RES) else 1)
asyncio.run(main())
