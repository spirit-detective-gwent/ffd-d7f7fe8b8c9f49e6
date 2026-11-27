/* GGD-90 eat mini-game tuning tests. node tools/eatgame/eat_test.js [index.html]
 * Runs the real EATG logic headless with simulated thumbs (seeded, +-20% wobble per tap) and checks the feel targets. */
const E = require('./load.js')(process.argv[2]);
const I = E._items, N = 100;
let pass = 0, fail = 0;
function ok(c, msg) { if (c) { pass++; console.log('PASS ' + msg); } else { fail++; console.log('FAIL ' + msg); } }
function run(it, mode) { let w = 0, c = 0, b = 0, t = 0; for (let s = 1; s <= N; s++) { const r = E._sim(it, mode, s); if (r.res === 'win') { w++; t += r.t; } else if (r.res === 'close') c++; else b++; } return { w: w / N, c: c / N, b: b / N, t: w ? t / w : 99 }; }
const fmt = r => `win ${Math.round(r.w * 100)}% close ${Math.round(r.c * 100)}% bad ${Math.round(r.b * 100)}% avg win ${r.t.toFixed(1)}s`;

/* config sanity */
const bites = Object.keys(I).filter(k => I[k].game === 'bite');
ok(bites.every(k => ['light', 'std', 'heavy'].includes(I[k].tier) && I[k].tapP > 0 && I[k].drain > 0), 'every quick bite has a tier, tapP and drain (' + bites.length + ' foods)');
ok(I.omurice.tier === 'heavy' && I.lunch.tier === 'heavy' && I.karaage.tier === 'heavy', 'hot lunch, omurice, karaage are heavy');
ok(['pudding', 'candy', 'dango', 'edamame'].every(k => I[k].tier === 'light'), 'pudding, candy bar, dango, edamame are light');
ok(['onigiri', 'melonbread', 'melon', 'yakisoba', 'antoast', 'sweetroll', 'yakitori'].every(k => I[k].tier === 'std'), 'onigiri, melon bread, yakisoba bread, an-toast, sweet roll, yakitori are standard');

/* targets per tier: [mode, check, label] */
const T = {
  light: [[3, r => r.w === 0 && r.c >= 0.9, '3/s lands on CLOSE'], [4, r => r.w >= 0.95 && r.t <= 8, '4/s reaches a perfect'],
          [5, r => r.w === 1 && r.t <= 5, '5/s perfect, seconds to spare'], [6, r => r.w === 1 && r.t <= 4, '6/s perfect'], ['lazy', r => r.w === 0 && r.c >= 0.9, 'lazy (3/s) lands on CLOSE'], ['fail', r => r.b === 1, '3 taps and stop = BAD']],
  std:   [[3, r => r.w === 0 && r.c >= 0.85, '3/s lands on CLOSE'], [4, r => r.w <= 0.02 && r.c >= 0.95, '4/s no perfect, CLOSE'],
          [5, r => r.w === 1 && r.t <= 6.5, '5/s perfect, seconds to spare'], [6, r => r.w === 1 && r.t <= 4.5, '6/s perfect'], ['lazy', r => r.w === 0 && r.c >= 0.85, 'lazy (3/s) lands on CLOSE'], ['burst', r => r.w <= 0.25 && r.c >= 0.7, 'bursty (1s at 7/s, 1s off) mostly CLOSE'], ['fail', r => r.b === 1, '3 taps and stop = BAD']],
  heavy: [[3, r => r.w === 0 && r.c >= 0.75, '3/s mostly CLOSE'], [4, r => r.w === 0 && r.c >= 0.95, '4/s no perfect, CLOSE'],
          [5, r => r.w >= 0.97 && r.t <= 7.5, '5/s perfect, a few seconds to spare'], [6, r => r.w === 1 && r.t <= 5, '6/s perfect'], ['burst', r => r.w <= 0.1 && r.c >= 0.85, 'bursty mostly CLOSE'], ['fail', r => r.b === 1, '3 taps and stop = BAD']]
};
const rep = { light: ['pudding', 'candy'], std: ['onigiri', 'melonbread', 'yakisoba', 'sweetroll'], heavy: ['lunch', 'omurice'] };
for (const tier in T) for (const it of rep[tier]) for (const [m, chk, lab] of T[tier]) { const r = run(it, m); ok(chk(r), `${tier} ${it} ${lab}: ${fmt(r)}`); }
const g = E._sim('omurice', 'good', 1); ok(g.res === 'win', 'bot good (6/s) wins omurice: ' + JSON.stringify(g));

/* ramen: same mechanic, lighter numbers. careful thumb: taps at r/s, notices heat >= hi after 0.22s, rests to lo */
function mul(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function noodle(it, r, hi, lo, seed) { const R = mul(seed * 577 + 1); const S = E._newRun(it, 'ryo', seed, null); let rest = false, see = null, nt = 0.3;
  S.script = (S) => { const t = S.pt; if (rest) { if (S.heat <= lo) rest = false; else return; } if (see === null && S.heat >= hi) see = t; if (see !== null && t - see >= 0.22) { rest = true; see = null; return; } if (t >= nt) { E._in(); E._up(); nt = t + (1 / r) * (0.8 + R() * 0.4); } };
  let k = 0; while (S.ph !== 'result' && k++ < 1300) E._step(1 / 60); return { res: S.res, cause: S.cause, t: S.pt }; }
function nrun(it, r, hi, lo) { let w = 0, oh = 0, t = 0; for (let s = 1; s <= N; s++) { const x = noodle(it, r, hi, lo, s); if (x.res === 'win') { w++; t += x.t; } if (x.cause === 'overheat') oh++; } return { w: w / N, oh: oh / N, t: w ? t / w : 99 }; }
ok(I.shoyu.tapP === 0.05 && I.shoyu.tapH === 0.075 && I.shoyu.cool === 0.42, 'shoyu numbers 20 taps / .075 / .42');
ok(I.miso.tapP === 0.048 && I.miso.tapH === 0.08 && I.miso.cool === 0.40, 'miso numbers 21 taps / .08 / .40');
ok(I.tonkotsu.tapP === 0.045 && I.tonkotsu.tapH === 0.08 && I.tonkotsu.cool === 0.40, 'tonkotsu numbers 23 taps / .08 / .40');
for (const it of ['shoyu', 'miso', 'tonkotsu']) {
  for (const [r, hi, lo] of [[5, 0.6, 0.25], [5, 0.75, 0.3], [7, 0.6, 0.25], [7, 0.75, 0.3]]) { const x = nrun(it, r, hi, lo); ok(x.w === 1 && x.t <= 8.5, `${it} careful ${r}/s stop@${hi} rest to ${lo}: win ${x.w * 100}% avg ${x.t.toFixed(1)}s`); }
  const gr = nrun(it, 7, 0.9, 0.3); ok(gr.oh >= 0.8, `${it} greedy 7/s stop@0.9: overheats ${Math.round(gr.oh * 100)}%`);
  const f = E._sim(it, 'fail', 1); ok(f.res === 'bad' && f.cause === 'overheat', `${it} non-stop tapping overheats`);
}
/* soda untouched */
ok(I.ramune.chug === 0.20 && I.ramune.fizz === 0.28 && I.ramune.rec === 0.11 && I.cola.chug === 0.22 && I.cola.fizz === 0.30, 'soda numbers unchanged');
ok(E._sim('ramune', 'good', 1).res === 'win' && E._sim('ramune', 'fail', 1).cause === 'overflow', 'soda bots unchanged (good wins, fail overflows)');
console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
