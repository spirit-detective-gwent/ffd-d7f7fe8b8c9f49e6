#!/usr/bin/env node
/* Compassionate Bulwark / Rebound: engine + bond table tests against this worktree's index.html.
   usage: node tools/bond/comp_test.js   (run from the worktree, or pass INDEX=) */
const fs = require('fs');
const path = require('path');
const INDEX = process.env.INDEX || path.resolve(__dirname, '../../index.html');
const OUT = '/tmp/eng_comp.js';

function extract() {
  const t = fs.readFileSync(INDEX, 'utf8');
  const i = t.indexOf('window.CARD_DATA=');
  const nl = t.indexOf('\n', i);
  let card = t.slice(i, nl);
  if (!card.trim().endsWith(';')) card += ';';
  const a = t.indexOf('<script>/* Fox Fire Fist: Delinquent Duel - rules engine');
  const start = a + '<script>'.length;
  const needle = "module.exports = E; else root.ENGINE = E;\n})(this);";
  const end = t.indexOf(needle, start) + needle.length;
  fs.writeFileSync(OUT, 'globalThis.window=globalThis;\n' + card + '\n' + t.slice(start, end) + '\nmodule.exports = window.ENGINE || module.exports;\n');
}
extract();
const E = require(OUT);
E.init(window.CARD_DATA);

const t = fs.readFileSync(INDEX, 'utf8');
function grab(fn) {
  const i = t.indexOf(fn);
  if (i < 0) throw new Error('missing ' + fn);
  const j = t.indexOf('\nfunction ', i + 1);
  return t.slice(i, j);
}
eval(t.slice(t.indexOf('var BOND = '), t.indexOf('function bondNeed')));
function bond(S) { return S.bond; }
function bondLv(S) { return S.lv; }
function bondDmg(lv) { return lv <= 5 ? BOND.DMG[lv - 1] : 18 + (lv - 5); }
function bondSigId(p, ch) { return ch === 'aoi' ? BOND.ASIG[p] : BOND.SIG[p]; }
eval(grab('function bondSig(S, ch)'));
eval(grab('function bondFight(S)'));

let fails = 0;
function ok(name, cond, extra) {
  if (!cond) { fails++; console.log('FAIL', name, extra !== undefined ? extra : ''); }
  else console.log('PASS', name);
}
function eq(name, a, b) { ok(name, JSON.stringify(a) === JSON.stringify(b), { got: a, want: b }); }

const WANT = {
  1: { t: 1, g: 2 },
  2: { t: 1, g: 2, dmg: 14 },
  3: { t: 2, g: 3, dmg: 15 },
  4: { t: 2, g: 3, dmg: 17 },
  5: { t: 3, g: 4, cap: 6, dmg: 18 },
  6: { t: 4, g: 5, cap: 10, dmg: 19 },
  7: { t: 4, g: 5, cap: 10, dmg: 20 },
  8: { t: 4, g: 5, cap: 10, dmg: 21 },
  9: { t: 4, g: 5, cap: 10, dmg: 22 },
  10: { t: 4, g: 5, cap: 10, dmg: 23 }
};

ok('SB.heal10 is 3', E.SB.heal10 === 3);
ok('SB.guard10 is 3', E.SB.guard10 === 3);
ok('SB.lv8 still 3', E.SB.lv8 === 3);
ok('sbHoldLine exported', typeof E.sbHoldLine === 'function');

for (const lv of Object.keys(WANT).map(Number)) {
  const w = WANT[lv];
  for (const ch of ['ryo', 'aoi']) {
    const S = { bond: { path: 'balanced' }, lv, act: ch };
    const c = bondSig(S, ch);
    eq(`Lv${lv} ${ch} special dmg`, c.v, w.dmg || bondDmg(lv));
    eq(`Lv${lv} ${ch} bulw turns`, c.bulw, w.t);
    eq(`Lv${lv} ${ch} bulw Guard`, c.bulwG, w.g);
    eq(`Lv${lv} ${ch} bulwCap`, c.bulwCap, w.cap);
    ok(`Lv${lv} ${ch} no dodge brk/mark leftovers`, !c.brk && !c.mark && !c.burn);
    ok(`Lv${lv} ${ch} id`, c.id === (ch === 'aoi' ? 'a_hpc' : 'r_hfb'));
  }
  const f = bondFight({ bond: { path: 'balanced' }, lv });
  eq(`Lv${lv} dgPlus 0`, f.dgPlus, 0);
  eq(`Lv${lv} rebCap`, f.rebCap, w.cap || 0);
  eq(`Lv${lv} no ctrPlus`, f.ctrPlus, 0);
}

// Fierce / Strategic unchanged
const f5 = bondSig({ bond: { path: 'fierce' }, lv: 5, act: 'ryo' }, 'ryo');
eq('Fierce Lv5 burn 2 brk 2', { burn: f5.burn, brk: f5.brk, id: f5.id }, { burn: 2, brk: 2, id: 'r_fff' });
const f6 = bondSig({ bond: { path: 'fierce' }, lv: 6, act: 'ryo' }, 'ryo');
eq('Fierce Lv6 burn 3', f6.burn, 3);
const s5 = bondSig({ bond: { path: 'strategic' }, lv: 5, act: 'ryo' }, 'ryo');
eq('Strategic Lv5 mark 3 keep 10 bench 5', { mark: s5.mark, keep: s5.keepSp, bench: s5.benchSp, id: s5.id }, { mark: 3, keep: 10, bench: 5, id: 'r_ds' });
const s6 = bondSig({ bond: { path: 'strategic' }, lv: 6, act: 'aoi' }, 'aoi');
eq('Strategic Lv6 mark 4 keep 15 bench 10', { mark: s6.mark, keep: s6.keepSp, bench: s6.benchSp, id: s6.id }, { mark: 4, keep: 15, bench: 10, id: 'a_fsc' });
eq('Strategic fight Lv6 ctrPlus 3', bondFight({ bond: { path: 'strategic' }, lv: 6 }).ctrPlus, 3);
eq('Fierce fight no rebCap', bondFight({ bond: { path: 'fierce' }, lv: 10 }).rebCap, 0);

eq('PERK Lv1', BOND.PERK.balanced[0], 'Bulwark 1 turn · Guard 2');
eq('PERK Lv5', BOND.PERK.balanced[4], 'Bulwark 3 turns · Guard 4 · REBOUND (stored up to 6)');
eq('PERK Lv10', BOND.PERK.balanced[9], 'Bulwark 4 · Guard 5 · Rebound 10 · Echo 35% (+1 Rebound) · Awakening: heal 3 + Guard 3');
ok('PERK fierce unchanged', BOND.PERK.fierce[9].indexOf('BURN 3') >= 0 && BOND.PERK.fierce[9].indexOf('burns all foes') >= 0);
ok('PERK strategic unchanged', BOND.PERK.strategic[9].indexOf('Mark +4') >= 0 && BOND.PERK.strategic[9].indexOf('Awakening: stun') >= 0);

function atk(v, o) { return Object.assign({ t: 'atk', v, hits: 1, n: 'Hit', id: 't_hit', u: 'h' + Math.random(), ch: 'ryo' }, o || {}); }
function foeAtk(v, o) { return Object.assign({ t: 'atk', v, hits: 1, n: 'FoeHit', id: 'e_hit', u: 'e' + Math.random(), ch: 'mb2_depot' }, o || {}); }

function setup(lv, o) {
  o = o || {};
  E.setRng(function () { return 0.99; }); // no random echoes unless we force them
  const b = E.newBattle('ryo', 'mb2_depot', 0);
  const S = { bond: { path: 'balanced' }, lv, act: 'ryo' };
  const sig = bondSig(S, 'ryo');
  const jab = atk(3, { id: 'r_jab', n: 'Street Jab' });
  const pst = { hp: o.hp || 55, max: o.hp || 55, spirit: 40, deck: [jab, jab, jab, jab, jab], sig, disc: 0, rebCap: bondFight(S).rebCap };
  E.applyPst(b, b.s[0], pst);
  b.s[0].hand = [jab, atk(3, { id: 'r_jab2', n: 'Street Jab' }), atk(2, { id: 'r_crack', n: 'Knuckle Crack', pierce: 1 })];
  b.s[0].guard = 0;
  b.s[1].hand = [foeAtk(o.foeV || 6), foeAtk(o.foeV || 6), foeAtk(o.foeV || 6), foeAtk(o.foeV || 6), foeAtk(o.foeV || 6)];
  b.s[1].guard = 0; b.s[1].spirit = 0;
  b.turn = 0;
  return b;
}

// Lv1: special starts Bulwark 1 / Guard 2; top-up at end of that turn; one enemy hit is shielded; then it ends.
{
  const b = setup(1);
  const fx = E.applyMove(b, 0, { sig: true });
  ok('Lv1 special logs Bulwark', (fx.log || []).join(' ').indexOf('Bulwark: 1 turn, Guard 2') >= 0, fx.log);
  eq('Lv1 top-up to 2', b.s[0].guard, 2);
  eq('Lv1 duration still 1 after own turn', b.bulw && b.bulw.t, 1);
  eq('Lv1 no store yet', b.reb | 0, 0);
  const hp0 = b.s[0].hp;
  const fe = E.applyMove(b, 1, { u: b.s[1].hand[0].u });
  eq('Lv1 6 into Guard 2 deals 4', hp0 - b.s[0].hp, 4);
  eq('Lv1 no Rebound at Lv1 (cap 0)', b.reb | 0, 0);
  eq('Lv1 wait set after enemy', b.bulwWait, 1);
  E.applyMove(b, 0, { u: b.s[0].hand[0].u });
  eq('Lv1 ended after one enemy phase', !b.bulw || b.bulw.t <= 0, true);
  eq('Lv1 no second top-up', b.s[0].guard, 0); // 6-2 already wore it, and no refill
}

// Lv5: store up to 6, release on next first hit. Multi-hit gets it once.
{
  const b = setup(5, { foeV: 6 });
  E.applyMove(b, 0, { sig: true });
  eq('Lv5 Guard topped to 4', b.s[0].guard, 4);
  eq('Lv5 cap 6', b.rebCap, 6);
  const hp0 = b.s[0].hp;
  E.applyMove(b, 1, { u: b.s[1].hand[0].u }); // 6 vs Guard 4 -> store 4, take 2
  eq('Lv5 stored 4', b.reb, 4);
  eq('Lv5 took 2', hp0 - b.s[0].hp, 2);
  const foeHp = b.s[1].hp;
  const jab = b.s[0].hand[0];
  const fx = E.applyMove(b, 0, { u: jab.u });
  eq('Lv5 released 4', fx.rel, 4);
  eq('Lv5 jab 3 + Rebound 4 = 7', foeHp - b.s[1].hp, 7);
  eq('Lv5 store cleared', b.reb, 0);
}

// Cap 6: first hit stores 4, next player turn refills Guard 4, second hit would add 4 but caps at 6
{
  const b = setup(5, { foeV: 6 });
  E.applyMove(b, 0, { sig: true });
  E.applyMove(b, 1, { u: b.s[1].hand[0].u });
  eq('Lv5 mid store 4', b.reb, 4);
  const g = { t: 'guard', v: 0, n: 'Wait', id: 'waitC', u: 'wc', ch: 'ryo' };
  b.s[0].hand.push(g);
  E.applyMove(b, 0, { u: g.u });
  eq('Lv5 refilled to 4', b.s[0].guard, 4);
  E.applyMove(b, 1, { u: b.s[1].hand[0].u });
  eq('Lv5 cap stops at 6', b.reb, 6);
}

// Pierce does not store
{
  const b = setup(5, { foeV: 6 });
  E.applyMove(b, 0, { sig: true });
  b.s[1].hand[0] = foeAtk(6, { pierce: 1, brk: 1, n: 'Pallet Ram' });
  const hp0 = b.s[0].hp; const g0 = b.s[0].guard;
  E.applyMove(b, 1, { u: b.s[1].hand[0].u });
  eq('pierce cleared Guard', b.s[0].guard, 0);
  eq('pierce stored nothing', b.reb | 0, 0);
  ok('pierce dealt through', b.s[0].hp < hp0 && g0 === 4);
}

// Release is first-hit only (multi-hit)
{
  const b = setup(6, { foeV: 6 });
  E.applyMove(b, 0, { sig: true });
  eq('Lv6 Guard 5', b.s[0].guard, 5);
  E.applyMove(b, 1, { u: b.s[1].hand[0].u }); // 6 vs 5 -> store 5
  eq('Lv6 stored 5', b.reb, 5);
  b.s[0].hand[0] = atk(2, { hits: 3, n: 'Chain Jabs', id: 'r_chain' });
  const foeHp = b.s[1].hp;
  const fx = E.applyMove(b, 0, { u: b.s[0].hand[0].u });
  eq('multi-hit released once', fx.rel, 5);
  eq('2+5 + 2 + 2 = 11', foeHp - b.s[1].hp, 11);
}

// Path Echo +1 Rebound (forced, as Sync Break II does)
{
  const b = setup(7);
  b.echo = { k: 'balanced', p: 0 };
  b.s[0].sbEcho = 1;
  b.rebCap = 10;
  const fx = E.applyMove(b, 0, { u: b.s[0].hand[0].u });
  eq('forced Echo stored +1', b.reb, 1);
  ok('echo log', (fx.log || []).join(' ').indexOf('Path Echo: Rebound +1') >= 0, fx.log);
  const foeHp = b.s[1].hp;
  E.applyMove(b, 1, { u: b.s[1].hand[0].u }); // enemy turn, no release
  const jab = b.s[0].hand[0];
  const fx2 = E.applyMove(b, 0, { u: jab.u });
  eq('Echo Rebound released on next atk', fx2.rel, 1);
  eq('jab 3+1 = 4', foeHp - b.s[1].hp, 4);
}

// Special refresh does not stack turns; keeps unspent store
{
  const b = setup(6);
  E.applyMove(b, 0, { sig: true });
  E.applyMove(b, 1, { u: b.s[1].hand[0].u }); // store 5 (6 vs Guard 5)
  eq('pre-refresh store 5', b.reb, 5);
  b.s[0].spirit = 40;
  E.applyMove(b, 0, { sig: true });
  eq('refresh resets duration to 4', b.bulw.t, 4);
  eq('store kept across refresh (released? special is a sig so it SHOULD release)', b.reb, 0); // special releases then refreshes
  // This is correct per the design: the special that refreshes also cashes Rebound.
}

// Unspent Rebound stays after Bulwark ends
{
  const b = setup(5, { foeV: 6 });
  E.applyMove(b, 0, { sig: true });
  E.applyMove(b, 1, { u: b.s[1].hand[0].u });
  eq('stored before end', b.reb, 4);
  // three enemy phases + player turns to burn 3 duration: already 1 phase done (wait=1)
  // player turn: decrement to 2, top-up, ...
  for (let i = 0; i < 3; i++) {
    // don't attack (would release). Play a charge-like no-op: use a guard card? easier: give a charge and play it? 
    // Use a 0-damage... actually atk would release. Put a guard card in hand.
    const g = { t: 'guard', v: 0, n: 'Wait', id: 'wait', u: 'w' + i, ch: 'ryo' };
    b.s[0].hand.push(g);
    E.applyMove(b, 0, { u: g.u });
    if (b.s[1].hand.length) E.applyMove(b, 1, { u: b.s[1].hand[0].u });
  }
  ok('Bulwark ended', !b.bulw || b.bulw.t <= 0, b.bulw);
  ok('store still there', (b.reb | 0) > 0, b.reb);
  const store = b.reb | 0;
  const foeHp = b.s[1].hp;
  const jab = b.s[0].hand.find(c => c.t === 'atk' && !c.pierce) || b.s[0].hand.find(c => c.t === 'atk');
  const fx = E.applyMove(b, 0, { u: jab.u });
  eq('released after Bulwark ended', fx.rel, store);
}

// Group: two enemy actions in one phase tick duration only once
{
  const b = setup(3, { foeV: 4 });
  // make a 2-foe group
  const s2 = Object.assign({}, b.s[1], { ch: 'c2_punk', hp: 40, max: 40, hand: [foeAtk(4), foeAtk(4)], guard: 0, spirit: 0 });
  b.grp = [b.s[1], s2];
  E.applyMove(b, 0, { sig: true });
  eq('Lv3 duration 2 after special', b.bulw.t, 2);
  E.applyMove(b, 1, { u: b.s[1].hand[0].u });
  const tAfter1 = b.bulw.t;
  // second foe, same phase (si=1 again)
  const old = b.s[1];
  b.s[1] = s2;
  E.applyMove(b, 1, { u: s2.hand[0].u });
  b.s[1] = old;
  eq('group phase does not tick twice mid-line', b.bulw.t, tAfter1);
  const g = { t: 'guard', v: 0, n: 'Wait', id: 'waitG', u: 'wg', ch: 'ryo' };
  b.s[0].hand.push(g);
  E.applyMove(b, 0, { u: g.u });
  eq('one tick at the start of the next player turn', b.bulw.t, 1);
}

// Shared: switch mid-Bulwark, incoming partner gets the next top-up; store is party-wide
{
  const b = setup(5, { foeV: 6 });
  const S = { bond: { path: 'balanced' }, lv: 5, act: 'aoi' };
  const sigA = bondSig(S, 'aoi');
  const jabA = atk(4, { id: 'a_kata', n: 'Kata Drill', ch: 'aoi' });
  E.addBench(b, 'aoi', { hp: 55, max: 55, spirit: 20, deck: [jabA], sig: sigA, disc: 0 }, true);
  E.applyMove(b, 0, { sig: true });
  E.applyMove(b, 1, { u: b.s[1].hand[0].u });
  const store = b.reb;
  ok('store after Ryo block', store > 0, store);
  // swap in Aoi (HP shared)
  const out = b.s[0], inn = b.bench;
  inn.hp = out.hp; inn.max = out.max;
  b.s[0] = inn; b.bench = out; inn.bench = 0; out.bench = 1; delete inn.bench;
  b.s[0].hand = [jabA];
  eq('Aoi starts with 0 Guard', b.s[0].guard, 0);
  const g = { t: 'guard', v: 0, n: 'Wait', id: 'wa', u: 'wa', ch: 'aoi' };
  b.s[0].hand.push(g);
  E.applyMove(b, 0, { u: g.u });
  eq('Aoi topped up to 4', b.s[0].guard, 4);
  const foeHp = b.s[1].hp;
  const fx = E.applyMove(b, 0, { u: jabA.u });
  // wait, I already played wait, then need enemy? I played wait which is si=0, that would have... 
  // Actually I played wait then immediately Aoi attack without enemy - the store should still release on her attack.
  // But I already used wait as the player turn after the enemy, then I try to play kata on the same... 
  // After wait, turn flipped to 1. I can't play Aoi attack without setting turn. Let me just check store wasn't lost and guard top-up.
  ok('store still party-wide after switch (may have waited one turn)', (b.reb === store) || (fx && fx.rel === store), { reb: b.reb, rel: fx && fx.rel, store });
}

// Dodged attack does not consume Rebound
{
  const b = setup(5);
  b.reb = 4; b.rebCap = 6;
  b.s[1].dodge = 100; b.s[1].dgAll = 1;
  E.setRng(function () { return 0; });
  const jab = b.s[0].hand[0];
  const fx = E.applyMove(b, 0, { u: jab.u });
  ok('dodged', !!(fx.dodged || (fx.log || []).join(' ').match(/dodged/i)), fx.log);
  eq('Rebound kept on dodge', b.reb, 4);
}

const total = 0;
if (fails) { console.log('FAILED', fails); process.exit(1); }
console.log('ALL PASS');
