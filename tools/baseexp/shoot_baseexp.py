#!/workspace/pwenv/bin/python3
"""Contact strips for Erik: every new room, a guard-and-cover sequence, the lane-fee kick + lever. usage: shoot_baseexp.py <tree> [port] OUTDIR"""
import asyncio, sys, json, os
OUTD = sys.argv.pop()
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_baseexp.py')).read().split('async def main():')[0])
from PIL import Image, ImageDraw, ImageFont
def font(n):
    for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',):
        if os.path.exists(f): return ImageFont.truetype(f, n)
    return ImageFont.load_default()
def strip(frames, out, title):
    W, H = 390, 844; pad = 12; cap = 54; n = len(frames)
    im = Image.new('RGB', (pad + n * (W + pad), 60 + H + cap + pad), (24, 22, 30)); d = ImageDraw.Draw(im)
    d.text((pad, 16), title, fill=(240, 232, 210), font=font(26))
    for i, (path, label) in enumerate(frames):
        x = pad + i * (W + pad); im.paste(Image.open(path).convert('RGB'), (x, 60))
        y = 60 + H + 8
        for j, ln in enumerate(label.split('\n')[:2]): d.text((x + 4, y + j * 22), ln, fill=(230, 226, 214), font=font(17))
    im.save(out); print('strip', out, im.size)
async def snap(pg, name, hide_ui=False):
    p = os.path.join(OUTD, 'raw', name + '.png'); await pg.screenshot(path=p); return p
async def cam(pg, x, y):
    await ev(pg, "(function(){ var c=camAt(%d,%d); W.pan={scr:1, run:function(){ W.cam.x=c[0]; W.cam.y=c[1]; }}; })(); 1" % (x, y))
async def main():
    os.makedirs(os.path.join(OUTD, 'raw'), exist_ok=True)
    h = serve(root, PORT)
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p); await ev(pg, STUB); await enter(pg, 'caf')
        await ev(pg, "var C=cafS(); ['line','kitchen','staff','cooler','dock','dish','bakery'].forEach(function(k){C.e[k]=1;}); save(); 1")
        rooms = []
        for k, at, cm, lab in [('cooler', [560, 520], [330, 470], 'Walk-in Cooler: guard + crate\nbetween the shelves'), ('dock', [560, 520], [330, 400], 'Loading Dock: guard, crate by\nthe van, pallets + sacks as cover'),
                           ('dish', [700, 640], None, 'Dish Room: quiet link\nDock <-> Kitchen (no foes)'), ('bakery', [930, 560], [860, 450], 'Bakery: guard, crate\neast of the bread counter')]:
            await go(pg, 'caf', k); await put(pg, *at); await ev(pg, "var f=(W.dgF||[]).find(q=>q.grd); if(f){f.gT=99;} 1")
            if cm: await cam(pg, *cm)
            await pg.wait_for_timeout(900)
            rooms.append((await snap(pg, 'room_' + k), lab)); await ev(pg, "W.pan=null; 1")
        await enter(pg, 'fld'); await ev(pg, "var S=fldS(); ['cage','showers','trainer','booth','track','lockers','coach'].forEach(function(k){S.e[k]=1;}); save(); 1")
        for k, at, lab in [('cage', [420, 470], 'Equipment Cage: own hurdle;\nkicked hurdles land here'), ('showers', [760, 640], 'Showers: hurdle by\nthe stall divider'),
                           ('trainer', [700, 600], 'Trainer\u2019s Room: hurdle;\ndoor down to the Coach\u2019s Office'), ('booth', [900, 330], 'Timing Booth: one-use lever\nunder the lap clock')]:
            await go(pg, 'fld', k); await put(pg, *at); await pg.wait_for_timeout(900)
            rooms.append((await snap(pg, 'room_' + k), lab))
        strip(rooms[:4], os.path.join(OUTD, 'strip_cafe_rooms.png'), 'Cafeteria: 4 new rooms (handmade cel, existing style)')
        strip(rooms[4:], os.path.join(OUTD, 'strip_storehouse_rooms.png'), 'Storehouse: 4 new rooms')
        # ---- guard + cover (Dock): beat, cover, lift, spotted
        await enter(pg, 'caf'); await go(pg, 'caf', 'dock'); seq = []
        await ev(pg, "var f=W.dgF.find(q=>q.grd); grdHome(f); f.gT=99; 1"); await put(pg, 300, 600); await cam(pg, 265, 440); await pg.wait_for_timeout(700)
        seq.append((await snap(pg, 'g1'), '1. Guard faces the crate side (west).\nCone = his view.'))
        await put(pg, 100, 490); await pg.wait_for_timeout(1200)
        seq.append((await snap(pg, 'g2'), '2. Behind the sacks inside his cone:\nprops block sight, no "?"'))
        await ev(pg, "var f=W.dgF.find(q=>q.grd); f.gT=0.01; 1"); await pg.wait_for_timeout(330)
        seq.append((await snap(pg, 'g3'), '3. He turns through the back wall\n(0.7 s, readable).'))
        await pg.wait_for_timeout(900); await ev(pg, "var f=W.dgF.find(q=>q.grd); f.gT=99; 1"); await put(pg, 190, 360); await pg.wait_for_timeout(400)
        seq.append((await snap(pg, 'g4'), '4. Facing east: walk up\nto the crate behind him.'))
        await ev(pg, "cafLift('dock'); 1"); await pg.wait_for_timeout(500); await skipall(pg, 4); await free(pg); await cam(pg, 265, 440); await pg.wait_for_timeout(800)
        seq.append((await snap(pg, 'g5'), '5. Crate up: his cone grows (x1.25),\nnotice time halves.'))
        await ev(pg, "var f=W.dgF.find(q=>q.grd); f.gT=0.01; 1"); await pg.wait_for_timeout(900); await ev(pg, "var f=W.dgF.find(q=>q.grd); f.gT=99; 1"); await put(pg, 230, 420); await pg.wait_for_timeout(1100)
        seq.append((await snap(pg, 'g6'), '6. Caught in the open with the crate:\n"!" then chase -> fight, crate goes home'))
        strip(seq, os.path.join(OUTD, 'strip_guard_cover.png'), 'Lunch Duty: room guard, cover, carry (Loading Dock)')
        await ev(pg, "cafDrop('test'); W.dgFight=null; W.__fights=[]; 1"); await free(pg)
        # ---- lane fee
        await enter(pg, 'fld'); await go(pg, 'fld', 'showers'); await ev(pg, "fldLift('showers'); 1"); await pg.wait_for_timeout(400); await skipall(pg, 4); await free(pg)
        await go(pg, 'fld', 'track'); await pg.wait_for_timeout(500); await free(pg); lf = []
        await ev(pg, "var R=FLDG.track, sp=R.spots.find(q=>q.id==='slot0'), a=lw(R,[280,440]); W.ryo.x=a[0]; W.ryo.y=a[1]+20; place(W.ryo,0); var g=fldSlotAng('slot0'); W.fldLap.t=Math.floor(W.fldLap.t)+(g/(2*Math.PI)-0.1+1)%1; 1")
        await pg.wait_for_timeout(250)
        lf.append((await snap(pg, 'k1'), '1. Carrying a hurdle: the mark ring is RED\nwhile Bando is on this side.'))
        await ev(pg, "fldPlace('slot0'); 1"); await pg.wait_for_timeout(260)
        lf.append((await snap(pg, 'k2'), '2. Set it anyway: he kicks it\n(one-shot CSS flight).'))
        await pg.wait_for_timeout(900)
        lf.append((await snap(pg, 'k3'), '3. "Not in my lane, rookie."\nIt goes back to the Equipment Cage.'))
        await skipall(pg, 6); await free(pg)
        await go(pg, 'fld', 'cage'); await put(pg, 520, 700); await pg.wait_for_timeout(600)
        lf.append((await snap(pg, 'k4'), '4. The kicked hurdle waits in the Cage\n(Lift tag).'))
        await ev(pg, "fldAct('hk_showers'); 1"); await pg.wait_for_timeout(300); await skipall(pg, 4); await free(pg)
        await go(pg, 'fld', 'booth'); await put(pg, 960, 260); await pg.wait_for_timeout(400)
        lf.append((await snap(pg, 'k5'), '5. Timing Booth lever (one use):\nslows his next lap.'))
        await ev(pg, "fldAct('lever'); 1"); await pg.wait_for_timeout(400); await skipall(pg, 6); await free(pg)
        await go(pg, 'fld', 'track'); await free(pg)
        await ev(pg, "var R=FLDG.track, a=lw(R,[280,440]); W.ryo.x=a[0]; W.ryo.y=a[1]+20; place(W.ryo,0); var g=fldSlotAng('slot0'); W.fldLap.t=Math.floor(W.fldLap.t)+(g/(2*Math.PI)+0.45+1)%1; 1")
        await pg.wait_for_timeout(400)
        lf.append((await snap(pg, 'k6'), '6. Slowed lap, far side:\nring GREEN, set it.'))
        await ev(pg, "fldPlace('slot0'); 1"); await pg.wait_for_timeout(700)
        lf.append((await snap(pg, 'k7'), '7. Hurdle stands on the mark (1/3).'))
        strip(lf, os.path.join(OUTD, 'strip_lane_fee.png'), "Lane fee's due: far side only, kick to the Cage, Timing Booth lever")
        print('errs', errs); await b.close()
asyncio.run(main())
