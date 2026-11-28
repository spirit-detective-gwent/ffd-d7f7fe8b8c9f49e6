global.window = global; global.performance = { now: () => Date.now() };
global.document = { createElement: () => ({ getContext: () => new Proxy({}, { get: () => () => ({ addColorStop() {} }) }) }) };
const fs = require('fs'); const D = (process.env.SRC || '/workspace/shonen/wt') + '/tools/s2/';
eval(fs.readFileSync(D + 's2arc_cab.js', 'utf8')); eval(fs.readFileSync(D + 's2arc_fight.js', 'utf8'));
const A = window.FFF_S2ARC, K = A.K; K.tone = () => {}; K.drum = () => {};
const runs = +process.argv[2] || 30, mode = process.argv[3] || 'smart', cont = +(process.argv[4] || 0);
let perStage = [0,0,0,0,0], rounds = [0,0], hpLeft = [], conts = 0, fullClears = 0, scores = [];
for (let r = 0; r < runs; r++) {
  const G = A.GAMES.fighter(K, A.CABS.fighter); G.in = {};
  G.start(); G.dbg({ sel: r % 6 }); let res, sp = 0, used = 0;
  for (let f = 0; f < 60 * 60 * 60; f++) {
    const [P, E] = G._pe(); const W = G.in; W.l = W.r = false;
    if (G.phase() === 'fight' && mode !== 'idle') {
      const dist = Math.abs(E.x - P.x), fw = P.face > 0 ? 'r' : 'l', bk = P.face > 0 ? 'l' : 'r';
      if (sp > 0) { sp--; if (sp === 0) G.release('sp'); }
      else if (mode === 'mash') { if (dist > 60) W[fw] = true; if (Math.random() < 0.2) G.press('a'); }
      else {
        const eRec = E.st === 'atk' && E.stT > E.mv.s + E.mv.a;
        if (P.meter >= 100 && dist < 120) { G.press('sp'); }
        else if (dist > 150) { if (Math.random() < 0.03) { G.press('sp'); sp = Math.random() < 0.4 ? 30 : 2; } else W[fw] = true; }
        else if (dist > 58) { if (Math.random() < 0.01) G.swipeUp(fw === 'r' ? 30 : -30); else W[fw] = true; }
        else if (E.st === 'block' && Math.random() < 0.5) W[bk] = true;  /* back off a blocker */
        else if (eRec || Math.random() < 0.14) G.press('a');
      }
    }
    res = G.step(1 / 60);
    if (res === 'clear') { perStage[G.stage]++; G.next(); }
    if (res === 'dead' && cont && used < cont) { used++; conts++; G.cont(); continue; }
    if (res === 'dead' || res === 'win') { if (res === 'win') { perStage[4]++; fullClears++; } break; }
  }
  scores.push(G.score);
}
console.log(mode, 'runs', runs, 'clears per match', perStage.join(' '), 'full clears', fullClears, 'continues used', conts, 'median score', scores.sort((a,b)=>a-b)[runs>>1]);
