#!/workspace/pwenv/bin/python3
"""v6566-prices (Erik t572u / t575u): Ch1 soda Y3, machine food Y7 (shared with the Ch2 harbor machines), cafeteria hot lunch Y12
ONCE per playthrough (50% HP; full HP on an eating-game win; no bad-run halving), potion stays Y6. Every visible price text matches.
usage: test_prices.py <worktree> [port] [--shots DIR] [--live]   (--live: only the 'before' shots on the live tree)"""
import asyncio, os, re
exec(open(__file__.rsplit('/', 1)[0] + '/lib.py').read())
BTNS = "[...document.querySelectorAll('#wdlg button')].filter(e=>e.offsetParent!==null).map(e=>[e.textContent.trim(), !!e.disabled])"
def click_js(rx): return "(function(){ var b=[...document.querySelectorAll('#wdlg button')].find(e=>e.offsetParent!==null&&/%s/.test(e.textContent)); if(!b) return 'none'; if(b.disabled) return 'disabled'; b.click(); return 'ok'; })()" % rx
EATSTUB = "(function(){ var G=root.EATG; if(!G.__o0) G.__o0=G.open; W.__eo=null; G.open=function(o){ W.__eo={item:o.item, rows:o.rows}; setTimeout(function(){ o.onEnd(W.__eres||'close'); }, 30); return true; }; return 1; })()"
async def dlg(pg): return await ev(pg, DLG)
async def shut(pg): await ev(pg, CLR); await pg.wait_for_timeout(150)
async def buy(pg, opener, rx, items, hp=None):
    await shut(pg); await ev(pg, "SAVE.items=%d; %s save(); %s; 1" % (items, ('SAVE.hp=%d;' % hp) if hp is not None else '', opener)); await pg.wait_for_timeout(250)
    t = await dlg(pg); b = await ev(pg, BTNS); r = await ev(pg, click_js(rx)); await pg.wait_for_timeout(500)
    return t, b, r
async def shoot(pg, name):
    if shots: os.makedirs(shots, exist_ok=True); await pg.screenshot(path=os.path.join(shots, name)); print('shot', os.path.join(shots, name))

async def main():
    h = serve(root, PORT)
    async with async_playwright() as p:
        b, ctx, pg, errs = await boot(p)
        if shots:
            await ev(pg, "cafEnter(); 1"); await pg.wait_for_timeout(1500); await skipall(pg, 8); await shut(pg)
            await ev(pg, "W.fading=false; cafGo('staff'); 1"); await pg.wait_for_timeout(900); await skipall(pg, 6); await shut(pg)
            tag = 'before' if live else 'after'
            await ev(pg, "SAVE.items=20; SAVE.hp=20; save(); hud(); cafVend('c2'); 1"); await pg.wait_for_timeout(500); await shoot(pg, tag + '_food_machine.png'); await shut(pg)
            await ev(pg, "SAVE.items=20; save(); hud(); cafVend('c1'); 1"); await pg.wait_for_timeout(500); await shoot(pg, tag + '_soda_machine.png'); await shut(pg)
            await ev(pg, "SAVE.items=20; SAVE.hp=20; save(); hud(); cafGo('line'); 1"); await pg.wait_for_timeout(900); await skipall(pg, 4); await shut(pg)
            await ev(pg, "cafLunch(); 1"); await pg.wait_for_timeout(500); await shoot(pg, tag + '_lunch_counter.png'); await shut(pg)
            await ev(pg, "W.ryo.x=520; W.ryo.y=560; place(W.ryo,0); 1"); await pg.wait_for_timeout(1500); await shoot(pg, tag + '_lunch_line_sign.png')
            await ev(pg, "SAVE.items=2; save(); hud(); fldVend('f1'); 1"); await pg.wait_for_timeout(500); await shoot(pg, tag + '_greyed_soda_button.png'); await shut(pg)
            await ev(pg, "SAVE.items=10; SAVE.shops=SAVE.shops||{}; delete SAVE.shops.nq_gk1; save(); hud(); c2Shop('nq_gk1'); 1"); await pg.wait_for_timeout(600); await shoot(pg, tag + '_ch2_dagashi_fumi.png')
            await ev(pg, "try{ var m=document.getElementById('wshop'); if(m) m.className=''; }catch(e){} W.dlg=false; if(!SHOPS.shop_surplus) SHOPS.shop_surplus=C3SHOPS.shop_surplus; delete SAVE.shops.shop_surplus; save(); c2Shop('shop_surplus'); 1"); await pg.wait_for_timeout(600); await shoot(pg, tag + '_ch2_harbor_surplus.png')
            await ev(pg, "try{ var m=document.getElementById('wshop'); if(m) m.className=''; }catch(e){} W.dlg=false; 1")
            if live: await b.close(); h.shutdown(); return
        # ---------- P: constants
        k = await ev(pg, "[SODA.cost, FOOD.cost, FOOD.pct, CAF_LUNCH, CAF_LUNCH_PCT, STORY.POTION.cost, AID.cost, MAXHP]")
        ok('P1 soda 3, food 7 (30%), lunch 12 (50%), potion 6, bandage machine 4', k[:7] == [3, 7, 0.3, 12, 0.5, 6, 4], k)
        mx = k[7]; fh = -(-mx * 3 // 10); lh = -(-mx // 2)
        await ev(pg, EATSTUB)
        # ---------- V: every Ch1 machine family + the Ch2 harbor machine charge the new price, refuse when short
        fams = [('library', "libVend('a1')", "libVend('a2')"), ('art kiln', "artVend('k1')", "artVend('k2')"), ('cafeteria', "cafVend('c1')", "cafVend('c2')"),
                ('storehouse', "fldVend('f1')", "fldVend('f2')"), ('gym annex', "gymVend('g1')", "gymVend('g2')"), ('nurse/training', "trainVendAct('tsoda')", "trainVendAct('tfood')"),
                ('Ch2 harbor', "c2VendAct('v1')", "c2VendAct('v2')")]
        for nm, so, fo in fams:
            if nm == 'Ch2 harbor': await ev(pg, "W.__c2w=C2W; C2W=Object.assign({}, C2W||{}, {vend:[['v1','soda',1240,760],['v2','food',1310,760]]}); 1")
            s0 = await ev(pg, "sodaN()")
            t, bt, r = await buy(pg, so, 'Buy', 10)
            s1 = await ev(pg, "[SAVE.items, sodaN()]")
            ok('V %s soda: prompt says Y3, buying charges 3 (10 -> 7) and bags a soda' % nm, ('\u00a53' in t) and r == 'ok' and s1 == [7, s0 + 1], [t[:120], bt, r, s1])
            t, bt, r = await buy(pg, so, 'Buy', 2)
            ok('V %s soda: with Y2 the button says need Y3, is greyed out, nothing charged' % nm, any('need \u00a53' in x[0] and x[1] for x in bt) and r == 'disabled' and await ev(pg, "SAVE.items") == 2, [bt, r])
            t, bt, r = await buy(pg, fo, 'Onigiri', 10, 10); await pg.wait_for_timeout(300)
            s2 = await ev(pg, "[SAVE.items, SAVE.hp]")
            ok('V %s food: prompt says Y7, buying charges 7 and heals 30%% (+%d)' % (nm, fh), ('\u00a57' in t) and r == 'ok' and s2 == [3, min(mx, 10 + fh)], [t[:140], bt, r, s2])
            t, bt, r = await buy(pg, fo, 'Onigiri', 6, 10)
            ok('V %s food: with Y6 every food button is greyed out, nothing charged or healed' % nm, r == 'disabled' and all(x[1] for x in bt if x[0] != 'Not now') and await ev(pg, "[SAVE.items, SAVE.hp]") == [6, 10], [bt, r])
        await ev(pg, "C2W=W.__c2w; 1")
        # map corner machine (world vend) prompt
        await shut(pg); await ev(pg, "SAVE.items=10; save(); try{ vend('vm_lib'); }catch(e){} 1"); await pg.wait_for_timeout(400)
        t = await dlg(pg); ok('V map corner machine prompt shows Y3 (not Y2) and the current effect (+5 Spirit, no Fizz/Cola next-fight text)', ('\u00a53' in t) and ('\u00a52' not in t) and '+5 Spirit' in t and 'Fizz' not in t, t[:300]); await shut(pg)
        # ---------- L: hot lunch, once, 50% / full on a win
        await ev(pg, "delete cafS().e.lunch; save(); W.__eres='close'; 1")
        t, bt, r = await buy(pg, "cafLunch()", 'Buy', 11, 10)
        ok('L1 lunch prompt: Y12, half your HP, one per student; with Y11 the button is disabled (need Y12), nothing charged',
           '\u00a512' in t and 'half your HP' in t and 'One per student' in t and r == 'disabled' and await ev(pg, "[SAVE.items, SAVE.hp, !!cafS().e.lunch]") == [11, 10, False], [t[:200], bt, r])
        t, bt, r = await buy(pg, "cafLunch()", 'Buy', 20, 10); await pg.wait_for_timeout(500)
        s = await ev(pg, "[SAVE.items, SAVE.hp, cafS().e.lunch|0, W.__eo&&W.__eo.item, W.__eo&&W.__eo.rows.bad]")
        ok('L2 buy with Y20 at 10 HP, close miss: charged 12, +50%% (+%d), flag saved, eating game opened (lunch)' % lh, s[:4] == [8, min(mx, 10 + lh), 1, 'lunch'], s)
        ok('L3 lunch bad-run row is not halved (still half your HP)', s[4] and s[4][1] == '+%d HP' % lh, s[4])
        t, bt, r = await buy(pg, "cafLunch()", 'Buy|Already', 50, 5)
        ok('L4 second visit: "already had", button disabled, no charge, no heal', 'already had' in t and r == 'disabled' and await ev(pg, "[SAVE.items, SAVE.hp]") == [50, 5], [t[:160], bt, r])
        await ev(pg, "cafS().e.lunch=1; save(); 1"); await pg.reload(); await pg.wait_for_timeout(3500); await ev(pg, "WORLD_API.enter(true)"); await pg.wait_for_timeout(2500); await skipall(pg, 12)
        ok('L5 the one-lunch flag survives a reload (persisted in the save)', await ev(pg, "cafS().e.lunch|0") == 1)
        await ev(pg, EATSTUB)
        for res, want in (('win', mx), ('close', min(mx, 10 + lh)), ('bad', min(mx, 10 + lh))):
            await ev(pg, "delete cafS().e.lunch; W.__eres='%s'; save(); 1" % res)
            t, bt, r = await buy(pg, "cafLunch()", 'Buy', 20, 10); await pg.wait_for_timeout(600)
            ok('L6 eating-game %s -> HP %d' % (res, want), await ev(pg, "[SAVE.hp, SAVE.items]") == [want, 8], await ev(pg, "[SAVE.hp, SAVE.items]"))
        await ev(pg, "delete cafS().e.lunch; root.FFF_EATG_OFF=1; save(); 1")
        t, bt, r = await buy(pg, "cafLunch()", 'Buy', 12, 10); await pg.wait_for_timeout(600)
        ok('L7 eating game off: exactly Y12 buys it, +50%', await ev(pg, "[SAVE.hp, SAVE.items]") == [min(mx, 10 + lh), 0], await ev(pg, "[SAVE.hp, SAVE.items]"))
        await ev(pg, "delete cafS().e.lunch; root.FFF_EATG_OFF=0; save(); 1")
        t, bt, r = await buy(pg, "cafLunch()", 'Buy|full', 20, mx)
        ok('L8 at full HP: button says you are full, nothing charged, flag not used', r == 'disabled' and await ev(pg, "[SAVE.items, cafS().e.lunch|0]") == [20, 0], [bt, r])
        # ---------- S: Chapter 2 shop sodas (Erik: harbor cold box + Dagashi Fumi Y3; Machi Motors Y3, Nails' price Y2 kept)
        sh = await ev(pg, "(function(){ if(!SHOPS.shop_surplus) SHOPS.shop_surplus=C3SHOPS.shop_surplus; var f=function(id,i){ return SHOPS[id].items.find(q=>q.id===i); }; return [f('shop_surplus','s3_soda').cost, f('nq_gk1','ram').cost, f('nq_motors','can').base, f('nq_motors','can').cost]; })()")
        ok('S1 shop soda prices: cold box 3, Dagashi Fumi 3, Machi Motors 3 (Nails 2)', sh == [3, 3, 3, 2], sh)
        for sid, iid, nm, pay in (('shop_surplus', 's3_soda', 'harbor cold box', 3), ('nq_gk1', 'ram', 'Dagashi Fumi', 3), ('nq_motors', 'can', 'Machi Motors (Nails price)', 2)):
            await shut(pg); await ev(pg, "SAVE.items=10; SAVE.shops=SAVE.shops||{}; delete SAVE.shops['%s']; save(); c2Shop('%s'); 1" % (sid, sid)); await pg.wait_for_timeout(300)
            bt = await ev(pg, "(function(){ var b=document.querySelector('#wshop button[data-i=\"%s\"]'); return b?[b.textContent.trim(), b.disabled]:null; })()" % iid)
            s0 = await ev(pg, "sodaN()"); r = await ev(pg, "shopBuy('%s','%s')" % (sid, iid)); s1 = await ev(pg, "[SAVE.items, sodaN()]")
            ok('S %s: button shows Y%d, buying charges %d and bags a soda' % (nm, pay, pay), bt and ('\u00a5%d' % pay) in bt[0] and not bt[1] and r and s1 == [10 - pay, s0 + 1], [bt, r, s1])
            await ev(pg, "try{ var m=document.getElementById('wshop'); if(m) m.className=''; }catch(e){} SAVE.items=%d; save(); c2Shop('%s'); 1" % (pay - 1, sid)); await pg.wait_for_timeout(300)
            bt = await ev(pg, "(function(){ var b=document.querySelector('#wshop button[data-i=\"%s\"]'); return b?[b.textContent.trim(), b.disabled]:null; })()" % iid)
            r = await ev(pg, "shopBuy('%s','%s')" % (sid, iid))
            ok('S %s: with Y%d the button is greyed and buying refuses' % (nm, pay - 1), bt and bt[1] and not r and await ev(pg, "SAVE.items") == pay - 1, [bt, r])
        await ev(pg, "try{ var m=document.getElementById('wshop'); if(m) m.className=''; }catch(e){} W.dlg=false; 1")
        # ---------- T: texts
        src = (root / 'index.html').read_text(encoding='utf-8')
        kl = re.search(r"talk_eat2: \[\['kenta', '([^']*)'", src).group(1)
        ok('T1 Kenta line: twelve yen, no "two yen", no deal/cheap wording', 'Twelve yen' in kl and 'two yen' not in kl.lower() and not re.search(r'deal|cheap|best', kl, re.I), kl)
        ok('T2 no "Two yen" soda banter left', "Two yen. We'll grab some." not in src and src.count("Three yen. We'll grab some.") == 2)
        sodas = [m.group(0) for m in re.finditer(r"[^\n]{0,80}\\u00a52[^\n]{0,60}", src) if re.search(r'(?i)soda|flavour|machine', m.group(0)) and 'Nails' not in m.group(0)]
        ok('T3 no soda/machine text still says Y2', not sodas, sodas[:3])
        ok('T4 harbor Ramune description matches what it does (+5 Spirit), no "more yen"', 'more yen from your next fights' not in src and "n: 'Ramune (cold box)', cost: 3, stock: 3, d: 'A soda: +5 Spirit on the map, full Spirit on a chug win.'" in src)
        import base64, io
        from PIL import Image as PI
        bim = PI.open(io.BytesIO(base64.b64decode(re.search(r"IMG\['wkitbg_cf_line'\] = 'data:image/webp;base64,([^']+)'", src).group(1)))).convert('RGB')
        px = bim.load(); lit = [sum(px[x, y]) > 480 for x in range(227, 406) for y in range(29, 96)]
        rows = [y for y in range(29, 96) if any(sum(px[x, y]) > 480 for x in range(227, 406))]
        bands = sum(1 for a, b in zip([28] + rows, rows) if b - a > 1)
        purple = sum(1 for x in range(290, 340) for y in range(78, 92) if px[x, y][2] > 170 and px[x, y][0] < 195)
        ok('T7 Lunch Line board repainted: 1152x864 room image, 4 chalk lines (today / melon bread / hot lunch / purple EAT.)', bim.size == (1152, 864) and bands == 4 and purple > 15, [bim.size, bands, purple, sum(lit)])
        pp = await ev(pg, "PHONE.prices()")
        ok('T5 phone price notes: soda 3, food 7, potion 6, effect text current', pp['soda']['yen'] == 3 and pp['food']['yen'] == 7 and pp['potionShop']['yen'] == 6 and 'Fizz' not in pp['soda']['effect'] and '\u00a512' in pp['recommendation'] and 'shop sodas are \u00a53' in pp['recommendation'], pp)
        ok('T6 no page errors', not errs, errs); await b.close()
    h.shutdown()
    print('RESULT %d/%d pass' % (sum(1 for r in RES if r[0]), len(RES)))
asyncio.run(main())
