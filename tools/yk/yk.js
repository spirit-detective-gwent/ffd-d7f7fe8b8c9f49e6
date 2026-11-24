/* v6.5.60 FFF_YK: Shōwa yankii wardrobe painter. Paints the yankii looks (long tokkōfuku coats, bontan, sarashi, pompadour /
 * punch perm, hachimaki, leopard) straight onto the existing cel sheets, in-engine, once, on request. Flat 3-tone cel fills +
 * dark ink lines, same as the sheets it paints on. Nothing runs per frame; nothing is used unless FFF_YK.on() is called. */
(function (root) {
  var INK = [22, 18, 28];
  function hx(s) { return [parseInt(s.substr(1, 2), 16), parseInt(s.substr(3, 2), 16), parseInt(s.substr(5, 2), 16)]; }
  function tri(c) { var b = hx(c); return { b: b, h: b.map(function (v) { return Math.min(255, Math.round(v + (255 - v) * 0.28)); }), s: b.map(function (v) { return Math.round(v * 0.62); }) }; }
  function lum(r, g, b) { return 0.3 * r + 0.59 * g + 0.11 * b; }
  /* ---- base classifiers: 0 none, 1 ink, 2 skin, 3 hair, 4 top, 5 shirt, 6 pants, 7 shoes, 8 other ---- */
  var CL = {
    punk: function (r, g, b, yr) { var L = lum(r, g, b);
      if (L < 52) return 1;
      if (yr < 0.22 && r > 150 && g > 110 && b < 118 && r - b > 70) return 3;
      if (r > 140 && r > g + 25 && g > b - 6 && g < b + 50 && b > 88 && r - b > 30 && r - b < 115) return 2;
      if (g > r + 35 && g > 70 && g >= b - 25) return 4;
      if (yr > 0.15 && yr < 0.6 && r > 150 && g > 150 && b > 130 && Math.abs(r - b) < 50) return 5;
      if (b > r + 18 && b > 60) return 6;
      if (yr > 0.86 && L > 150) return 7;
      if (yr > 0.25 && yr < 0.6 && r > 170 && b < 120) return 4; /* gold zigzag / back emblem sit on the jacket */
      return 8; },
    ryo: function (r, g, b, yr) { var L = lum(r, g, b);
      if (r > 140 && r > g + 12 && g > b - 5 && b > 70 && r - b > 35 && g > 80) return 2;
      if (r > 95 && r > g + 50 && r > b + 40) return 5;
      if (yr > 0.86 && L > 150) return 7;
      if (L < 24) return 1;
      if (yr < 0.2) return 3;
      if (r > 120 && g > 90 && b < 110 && yr > 0.25 && yr < 0.62) return 4; /* gold buttons */
      if (L < 80) return L >= 35 ? 4 : 6;
      return 8; },
    aoi: function (r, g, b, yr) { var L = lum(r, g, b);
      if (r > 140 && r > g + 12 && g > b - 5 && b > 70 && r - b > 30) return 2;
      if (L < 22) return 1;
      if (yr < 0.2 && L < 60) return 3;
      if (yr > 0.84 && L < 110 && Math.abs(r - b) < 16) return 7;
      if (b > r + 12 && L < 120) return 4;
      if (yr > 0.2 && yr < 0.6 && L > 140 && b >= r) return 4; /* sailor collar stripes */
      return 8; },
    /* painted battle stands (Ryo / Aoi): softer gradients, same idea */
    ryoP: function (r, g, b, yr) { var L = lum(r, g, b);
      if (r > 130 && r > g + 18 && g > b - 8 && b > 50 && r - b > 30 && g > 70) return 2;
      if (r > 80 && r > g * 1.7 && r > b * 1.5) return 5;
      if (yr > 0.84 && L > 120) return 7;
      if (yr < 0.2 && L < 70) return 3;
      if (L < 14) return 1;
      if (yr < 0.5 && L < 95 && b >= r - 8) return 4;
      if (L < 70) return 6;
      return 8; },
    aoiP: function (r, g, b, yr) { var L = lum(r, g, b);
      if (r > 130 && r > g + 15 && g > b - 8 && b > 60 && r - b > 25) return 2;
      if (yr < 0.24 && L < 70) return 3;
      if (L < 14) return 1;
      if (g > r + 8 && g >= b - 6 && L < 120 && yr < 0.62) return 4; /* green sailor top / skirt */
      if (yr > 0.15 && yr < 0.45 && L > 150 && Math.abs(r - b) < 30) return 4;
      if (yr > 0.82 && L < 80) return 7;
      return 8; }
  };
  /* ---- glyphs for the back embroidery: 天 上 天 下 (tenjō tenge), strokes in a 10x10 box ---- */
  var GLY = { ten: [[2.5, 1.6, 7.5, 1.6], [1, 4.4, 9, 4.4], [5, 1.6, 5, 4.4, 1.4, 9.2], [5, 4.4, 8.8, 9.2]],
    jo: [[5, 0.8, 5, 8.6], [5, 4.6, 8.2, 4.6], [1, 8.8, 9, 8.8]],
    ge: [[1, 1.4, 9, 1.4], [5, 1.4, 5, 9.2], [5.6, 4.2, 7.8, 6]],
    /* 湯 (yu, hot water): the bathhouse crest Gōda's crew wear */
    yu: [[1.1, 1.2, 2.1, 2.0], [0.7, 4.0, 1.7, 4.8], [0.8, 9.0, 2.2, 6.4], [4.2, 0.8, 4.2, 3.6], [4.2, 0.8, 8.6, 0.8, 8.6, 3.6], [4.2, 2.2, 8.6, 2.2], [4.2, 3.6, 8.6, 3.6],
      [3.2, 4.9, 9.2, 4.9], [4.6, 6.2, 9.0, 6.2, 8.5, 9.3, 7.5, 8.8], [6.0, 6.2, 4.0, 9.3], [7.5, 6.2, 5.7, 9.3]] };
  function glyph(x, k, cx, cy, s, col, w) { var G = GLY[k]; x.lineCap = 'round'; x.lineJoin = 'round';
    [[INK, w + 1.6], [col, w]].forEach(function (p) { x.strokeStyle = 'rgb(' + p[0].join(',') + ')'; x.lineWidth = p[1];
      G.forEach(function (st) { x.beginPath(); for (var i = 0; i < st.length; i += 2) { var px = cx + (st[i] - 5) * s / 10, py = cy + (st[i + 1] - 5) * s / 10; if (i) x.lineTo(px, py); else x.moveTo(px, py); } x.stroke(); }); }); }
  function rgb(c) { return 'rgb(' + c.join(',') + ')'; }
  function hash(a, b) { var h = (a * 374761393 + b * 668265263) | 0; h = (h ^ (h >>> 13)) * 1274126177; return ((h ^ (h >>> 16)) >>> 0) / 4294967296; }
  /* leopard: tan ground, broken dark rosettes on a jittered 7px grid */
  function leo(x, y, sc) { var g = 7 * sc, cx = Math.floor(x / g), cy = Math.floor(y / g), best = 9, bi = 0;
    for (var dy = -1; dy <= 1; dy++) for (var dx = -1; dx <= 1; dx++) { var gx = cx + dx, gy = cy + dy, px = (gx + 0.2 + 0.6 * hash(gx, gy)) * g, py = (gy + 0.2 + 0.6 * hash(gy + 7, gx)) * g, d = Math.hypot(x - px, y - py) / g; if (d < best) { best = d; bi = hash(gx * 3, gy); } }
    var r = 0.24 + 0.1 * bi; if (best < r * 0.55) return 1; if (best < r) return bi > 0.35 ? 2 : 1; return 0; }
  var LEO = [[214, 160, 70], [122, 74, 30], [40, 24, 16]];
  /* irezumi: indigo seigaiha waves with red peony blots, inked on the chest the open happi shows */
  function irez(x, y, sc, face) { var g = 6 * sc, r = g, gy = Math.floor(y / (g * 0.5)), off = (gy % 2) * g, gx = Math.floor((x + off) / (g * 2)), cx = gx * g * 2 - off + g, cy = gy * g * 0.5 + g * 0.5, dd = Math.hypot(x - cx, y - cy);
    var pb = hash(Math.floor(x / (g * 3)), Math.floor(y / (g * 3))); if (pb > 0.8) { var px = (Math.floor(x / (g * 3)) + 0.5) * g * 3, py = (Math.floor(y / (g * 3)) + 0.5) * g * 3, pd = Math.hypot(x - px, y - py) / (g * 1.3); if (pd < 1) return pd < 0.35 ? 3 : 2; }
    if (y > cy) return 0; if (Math.abs(dd - r * 0.95) < 0.9 || Math.abs(dd - r * 0.55) < 0.8) return 1; return 0; }
  var IREZ = [null, [36, 52, 110], [176, 44, 38], [226, 120, 70]];

  function paintCell(src, sx, sy, w, h, spec, face) {
    var cv = document.createElement('canvas'); cv.width = w; cv.height = h; var x = cv.getContext('2d', { willReadFrequently: true });
    var sideF = face === 'left' || face === 'right', hk = sideF ? (spec.headSide || 1.16) : (spec.headFront || 1);
    if (hk !== 1 && !spec.painted) { /* side views: the head up to the neck drawn a little bigger (it read small next to the coat), pinned at the neck */
      var hs = document.createElement('canvas'); hs.width = w; hs.height = h; var hsx = hs.getContext('2d', { willReadFrequently: true }); hsx.drawImage(src, sx, sy, w, h, 0, 0, w, h);
      var hd0 = hsx.getImageData(0, 0, w, h).data, hya = -1, hyb = 0; for (var hy = 0; hy < h; hy++) { var hn = 0; for (var hxx = 0; hxx < w; hxx++) if (hd0[(hy * w + hxx) * 4 + 3] > 150) hn++; if (hn >= 2) { if (hya < 0) hya = hy; hyb = hy; } }
      if (hya >= 0) { var yN = Math.round(hya + (hyb - hya) * (spec.neckQ || 0.165)), ha = w, hb = 0; for (var hy2 = hya; hy2 < yN; hy2++) for (var hx2 = 0; hx2 < w; hx2++) if (hd0[(hy2 * w + hx2) * 4 + 3] > 150) { if (hx2 < ha) ha = hx2; if (hx2 > hb) hb = hx2; }
        var hcxN = (ha + hb) / 2, hc2 = document.createElement('canvas'); hc2.width = w; hc2.height = h; var hcx3 = hc2.getContext('2d'); hcx3.drawImage(hs, 0, yN, w, h - yN, 0, yN, w, h - yN);
        hcx3.imageSmoothingEnabled = true; hcx3.drawImage(hs, 0, 0, w, yN + 2, hcxN - hcxN * hk, yN + 2 - (yN + 2) * hk, w * hk, (yN + 2) * hk);
        src = hc2; sx = 0; sy = 0; } }
    if (spec.bulk) { /* widen the body row by row around its centre: big shoulders, thick arms, a head that stays put */
      var t0 = document.createElement('canvas'); t0.width = w; t0.height = h; var tx = t0.getContext('2d', { willReadFrequently: true }); tx.drawImage(src, sx, sy, w, h, 0, 0, w, h);
      var d0 = tx.getImageData(0, 0, w, h).data, ya = h, yb = 0, xa = w, xb = 0;
      for (var yy = 0; yy < h; yy++) for (var xx = 0; xx < w; xx++) if (d0[(yy * w + xx) * 4 + 3] > 60) { if (yy < ya) ya = yy; if (yy > yb) yb = yy; if (xx < xa) xa = xx; if (xx > xb) xb = xx; }
      var cxm = (xa + xb) / 2, HH = Math.max(1, yb - ya); x.imageSmoothingEnabled = true;
      for (var ry = 0; ry < h; ry++) { var q = (ry - ya) / HH, p = spec.sumo ? (q < 0.16 ? 0.1 : q < 0.26 ? 0.1 + (q - 0.16) / 0.1 * 0.7 : q < 0.66 ? 0.8 + 0.42 * Math.sin(Math.PI * (q - 0.26) / 0.4) : sideF ? Math.max(0.1, 0.8 - (q - 0.66) * 2.4) : Math.max(0.42, 0.8 - (q - 0.66) * 1.1)) : q < 0.17 ? 0.12 : q < 0.24 ? 0.12 + (q - 0.17) / 0.07 * 0.88 : q < 0.5 ? 1 - (q - 0.24) * 0.6 : sideF ? Math.max(0.1, 0.84 - (q - 0.5) * 3.2) : q < 0.9 ? 0.84 - (q - 0.5) * 0.9 : 0.48;
        var s = 1 + spec.bulk * p, nw = w * s; x.drawImage(t0, 0, ry, w, 1, cxm - cxm * s, ry, nw, 1); }
      src = cv; sx = 0; sy = 0; cv = document.createElement('canvas'); cv.width = w; cv.height = h; x = cv.getContext('2d', { willReadFrequently: true }); }
    x.drawImage(src, sx, sy, w, h, 0, 0, w, h);
    var id = x.getImageData(0, 0, w, h), d = id.data, N = w * h, C = new Uint8Array(N), L = new Float32Array(N);
    var y0 = h, y1 = 0, x0 = w, x1 = 0, i, X, Y;
    var RC = new Uint16Array(h), CC = new Uint16Array(w); for (i = 0; i < N; i++) if (d[i * 4 + 3] > 150) { RC[(i / w) | 0]++; CC[i % w]++; }
    for (Y = 0; Y < h; Y++) if (RC[Y] >= 2) { if (Y < y0) y0 = Y; y1 = Y; } for (X = 0; X < w; X++) if (CC[X] >= 3) { if (X < x0) x0 = X; x1 = X; }
    if (y1 <= y0) return cv;
    var H = y1 - y0, fn = CL[spec.base];
    for (i = 0; i < N; i++) { var a = d[i * 4 + 3]; if (a < 40) continue; var r = d[i * 4], g = d[i * 4 + 1], b = d[i * 4 + 2]; L[i] = lum(r, g, b); C[i] = fn(r, g, b, ((i / w | 0) - y0) / H); }
    /* landmarks */
    function rowCount(Y, k) { var n = 0; for (var X = 0; X < w; X++) if (C[Y * w + X] === k) n++; return n; }
    function rowExt(Y, k) { var a = -1, b = -1; for (var X = 0; X < w; X++) if (C[Y * w + X] === k) { if (a < 0) a = X; b = X; } return a < 0 ? null : [a, b]; }
    var hem = -1, topK = 4, minTop = spec.base === 'ryo' || spec.base === 'ryoP' ? 8 : 4;
    for (Y = Math.round(y0 + H * 0.3); Y < y0 + H * (spec.hemMax || 0.66); Y++) if (rowCount(Y, topK) >= minTop) hem = Y;
    if (hem < 0) hem = Math.round(y0 + H * 0.5);
    if (spec.base === 'ryo' || spec.base === 'ryoP') for (i = 0; i < N; i++) { Y = i / w | 0; if (C[i] === 4 && Y > hem) C[i] = 6; else if (C[i] === 6 && Y <= hem) C[i] = 4; }
    if (spec.base === 'aoi' || spec.base === 'aoiP') { /* navy below the belt is the skirt */
      for (i = 0; i < N; i++) { Y = i / w | 0; if (C[i] === 4 && Y > hem) C[i] = 6; } }
    if (spec.base === 'punk' && face === 'back') { var ex0 = w, ex1 = 0, ey0 = h, ey1 = 0; for (Y = Math.round(y0 + H * 0.2); Y < hem; Y++) for (X = 0; X < w; X++) { i = Y * w + X; if (C[i] === 8 || (C[i] === 4 && d[i * 4] > 150)) { if (X < ex0) ex0 = X; if (X > ex1) ex1 = X; if (Y < ey0) ey0 = Y; if (Y > ey1) ey1 = Y; } }
      if (ex1 > ex0 && ex1 - ex0 < w * 0.2) for (Y = ey0 - 2; Y <= ey1 + 2; Y++) for (X = ex0 - 2; X <= ex1 + 2; X++) { i = Y * w + X; if (C[i]) { C[i] = 4; L[i] = 120; d[i * 4] = 32; d[i * 4 + 1] = 144; d[i * 4 + 2] = 128; } } }
    if (spec.base === 'punk') { var C2 = C.slice(); for (Y = Math.round(y0 + H * 0.2); Y < hem; Y++) for (X = 2; X < w - 2; X++) { i = Y * w + X; if (C[i] !== 8) continue; var n4 = 0; for (var dy4 = -2; dy4 <= 2; dy4++) for (var dx4 = -2; dx4 <= 2; dx4++) if (C[i + dy4 * w + dx4] === 4) n4++; if (n4 >= 10) { C2[i] = 4; L[i] = Math.max(L[i], 110); } } C = C2; }
    var faceTop = -1, chin = -1, FCX = -1;
    for (Y = y0; Y < y0 + H * 0.34; Y++) if (rowCount(Y, 2) >= 3) { if (faceTop < 0) faceTop = Y; chin = Y; }
    var hx0 = w, hx1 = 0, hy1 = y0;
    for (Y = y0; Y < (faceTop > 0 ? faceTop + (chin - faceTop) * 0.6 : y0 + H * 0.16); Y++) for (X = 0; X < w; X++) { var c = C[Y * w + X]; if (c === 3 || (c === 1 && Y < faceTop)) { if (X < hx0) hx0 = X; if (X > hx1) hx1 = X; hy1 = Y; } }
    if (faceTop > 0) { var fcx = 0, fcn = 0; for (Y = faceTop; Y <= chin; Y++) for (X = 0; X < w; X++) if (C[Y * w + X] === 2) { fcx += X; fcn++; } if (fcn) { fcx /= fcn; FCX = fcx; var hlim = H * 0.13; if (hx0 < fcx - hlim) hx0 = Math.round(fcx - hlim); if (hx1 > fcx + hlim) hx1 = Math.round(fcx + hlim); } } /* raised arms are not hair */
    if (faceTop < 0) faceTop = Math.round(y0 + H * 0.08);
    if (chin < 0) chin = Math.round(y0 + H * 0.16);
    var ankle = hem; for (Y = hem; Y <= y1; Y++) if (rowCount(Y, 6) >= 2) ankle = Y;
    if (spec.base === 'aoi' || spec.base === 'aoiP') { ankle = Math.round(y0 + H * 0.88); }
    (function () { var lab = new Int32Array(N), best = 0, bestN = 0, id2 = 0, st = [];
      for (var p0 = 0; p0 < N; p0++) if (C[p0] === 5 && !lab[p0]) { id2++; var n5 = 0; st.push(p0); lab[p0] = id2; while (st.length) { var q = st.pop(); n5++; [q - 1, q + 1, q - w, q + w].forEach(function (z) { if (z >= 0 && z < N && C[z] === 5 && !lab[z]) { lab[z] = id2; st.push(z); } }); } if (n5 > bestN) { bestN = n5; best = id2; } }
      for (var p1 = 0; p1 < N; p1++) if (C[p1] === 5 && lab[p1] !== best) C[p1] = 8; })();
    var shirt = null, sxa = x0 + (x1 - x0) * 0.22, sxb = x1 - (x1 - x0) * 0.22; for (Y = y0; Y < hem + 2; Y++) { var e5 = null; for (X = Math.ceil(sxa); X <= sxb; X++) if (C[Y * w + X] === 5) { if (!e5) e5 = [X, X]; e5[1] = X; } if (e5) { if (!shirt) shirt = { t: Y, b: Y, l: e5[0], r: e5[1] }; shirt.b = Y; shirt.l = Math.min(shirt.l, e5[0]); shirt.r = Math.max(shirt.r, e5[1]); } }
    /* hands on top of anything we add below the hem */
    var HAND = new Uint8Array(N), bandA = Math.round(hem - H * 0.08), bandB = Math.round(y0 + H * 0.94);
    for (Y = Math.max(1, bandA); Y < Math.min(h - 2, bandB); Y++) for (X = 2; X < w - 2; X++) { i = Y * w + X;
      if (C[i] === 2) HAND[i] = 1;
      else if (spec.glove && C[i] === 1) { var n = 0; for (var dy = -2; dy <= 2; dy++) for (var dx = -2; dx <= 2; dx++) if (C[i + dy * w + dx] === 1) n++; if (n >= 21) HAND[i] = 1; } }
    if (spec.glove) { var seen = new Uint8Array(N), stack = [];
      for (i = 0; i < N; i++) if (HAND[i] && !seen[i] && C[i] === 1) { var comp = [], bx0 = w, bx1 = 0, by0 = h, by1 = 0; stack.push(i); seen[i] = 1;
        while (stack.length) { var j = stack.pop(); comp.push(j); var jx = j % w, jy = j / w | 0; if (jx < bx0) bx0 = jx; if (jx > bx1) bx1 = jx; if (jy < by0) by0 = jy; if (jy > by1) by1 = jy;
          [j - 1, j + 1, j - w, j + w].forEach(function (q) { if (q >= 0 && q < N && HAND[q] && !seen[q] && C[q] === 1) { seen[q] = 1; stack.push(q); } }); }
        var bw3 = bx1 - bx0 + 1, bh3 = by1 - by0 + 1; if (bw3 > 26 * H / 230 || comp.length < 12 || bw3 < 6 * H / 230 || bh3 / bw3 > 2.2) comp.forEach(function (q) { HAND[q] = 0; }); } }
    if (spec.base === 'aoi' || spec.base === 'aoiP') for (Y = hem; Y < h; Y++) for (X = 0; X < w; X++) { i = Y * w + X; if (C[i] === 2) HAND[i] = 0; }
    var H2 = new Uint8Array(N); for (i = w + 1; i < N - w - 1; i++) if (HAND[i] || HAND[i - 1] || HAND[i + 1] || HAND[i - w] || HAND[i + w]) H2[i] = d[i * 4 + 3] > 40 ? 1 : 0;
    /* ---- 1. recolour ---- */
    var P = Object.assign({}, spec.pal); if (spec.hairCol && !P[3]) P[3] = tri(spec.hairCol); var med = {};
    [2, 3, 4, 5, 6, 7].forEach(function (k) { var a = []; for (var j = 0; j < N; j += 2) if (C[j] === k) a.push(L[j]); a.sort(function (p, q) { return p - q; }); med[k] = a.length ? a[a.length >> 1] : 128; });
    function put(j, t, rl) { if (spec.painted) { var f = Math.max(0.4, Math.min(1.45, rl)), up = f > 1 ? (f - 1) / 0.45 : 0; for (var q2 = 0; q2 < 3; q2++) d[j * 4 + q2] = Math.min(255, f <= 1 ? t.s[q2] + (t.b[q2] - t.s[q2]) * (f - 0.4) / 0.6 : t.b[q2] + (t.h[q2] - t.b[q2]) * up); return; }
      var c = rl > 1.12 ? t.h : rl > 0.8 ? t.b : t.s; d[j * 4] = c[0]; d[j * 4 + 1] = c[1]; d[j * 4 + 2] = c[2]; }
    var sar = tri('#f1ece0'), skin = tri(spec.skin || '#f2c9a0'), HARA = tri(spec.haraCol || '#d8c9a4'), sc0 = H / 230, dir2 = face === 'left' ? -1 : face === 'right' ? 1 : 0;
    var shoeT = h; if (spec.geta) for (i = 0; i < N; i++) if (C[i] === 7 && (i / w | 0) > y0 + H * 0.8 && (i / w | 0) < shoeT) shoeT = i / w | 0;
    for (i = 0; i < N; i++) { var k = C[i]; if (!k || k === 1 || k === 8) continue; Y = i / w | 0; X = i % w; var rl = L[i] / med[k];
      if (k === 5 && spec.hara && shirt && (Y - shirt.t) / Math.max(1, shirt.b - shirt.t) > spec.hara) { put(i, HARA, (X % 3 === 0) ? 0.72 : 1); continue; } /* haramaki: a ribbed belly band */
      if (k === 5 && spec.shirt === 'irezumi' && shirt) { var qz = (Y - shirt.t) / Math.max(1, shirt.b - shirt.t); var iz = irez(X, Y, sc0, face); if (qz < 0.12 || !iz) put(i, skin, rl); else { var zc = IREZ[iz]; d[i * 4] = zc[0]; d[i * 4 + 1] = zc[1]; d[i * 4 + 2] = zc[2]; } continue; }
      if (k === 7 && spec.geta && Y > shoeT) { var gq = (Y - shoeT) / Math.max(1, y1 - shoeT); if (gq < 0.3) put(i, tri(spec.geta.strap), rl); else if (gq > 0.82) put(i, tri('#3a2a1e'), 1); else put(i, tri(spec.geta.wood), (Y % 3 === 0) ? 0.86 : rl); continue; }
      if (k === 4 && spec.happi && Y <= hem && Y > hem - H * 0.045) { put(i, tri(spec.happi.hemCol), (((X >> 2) + (Y >> 1)) % 4 === 0) ? 0.55 : 1); continue; } /* the happi's banded hem */
      if (k === 4 && spec.happi && face === 'front' && shirt && Y > shirt.t - H * 0.02 && Y <= hem) { var ew = Math.max(2, (x1 - x0) * 0.075); if ((X < shirt.l && X >= shirt.l - ew) || (X > shirt.r && X <= shirt.r + ew)) { put(i, tri(spec.happi.eri), rl); continue; } } /* the white collar band (eri) */
      if (k === 4 && spec.happi && sideF && Y > y0 + H * 0.2 && Y <= hem) { var ex4 = rowExt(Y, 4); if (ex4) { var fr4 = dir2 > 0 ? ex4[1] : ex4[0], ew2 = Math.max(2, (x1 - x0) * 0.09); if (Math.abs(X - fr4) < ew2) { put(i, tri(spec.happi.eri), rl); continue; } } }
      if (k === 5 && spec.shirt === 'sarashi' && shirt) { var q = (Y - shirt.t) / Math.max(1, shirt.b - shirt.t); if (q < 0.3) put(i, skin, rl); else put(i, sar, ((Y - shirt.t) % 4 === 0) ? 0.7 : 1); continue; }
      if (k === 5 && spec.shirt === 'leopard') { var lp = leo(X, Y, spec.leoSc || 1); if (lp) { var cc = LEO[lp]; d[i * 4] = cc[0]; d[i * 4 + 1] = cc[1]; d[i * 4 + 2] = cc[2]; } else put(i, tri('#d6a046'), rl); continue; }
      var t = P[k]; if (t) put(i, t, rl); }
    if (spec.base === 'punk') for (i = 0; i < N; i++) if (C[i] === 1 || C[i] === 8) { var rr = d[i * 4], gg = d[i * 4 + 1], bb = d[i * 4 + 2]; if ((gg - rr > 10 || bb - rr > 18) && L[i] < 90) { var kk = Math.min(1.4, L[i] / 30); d[i * 4] = INK[0] * kk; d[i * 4 + 1] = INK[1] * kk; d[i * 4 + 2] = INK[2] * kk; } }
    /* Aoi's open front: a sarashi strip down the middle of her coat */
    if (spec.openFront && face !== 'back' && face !== 'left' && face !== 'right') { var cxm2 = (x0 + x1) / 2, sw = (x1 - x0) * 0.09, t1 = chin + (hem - chin) * 0.25;
      for (Y = Math.round(t1); Y < hem - 1; Y++) for (X = Math.round(cxm2 - sw); X <= Math.round(cxm2 + sw); X++) { i = Y * w + X; if (C[i] === 4) { var qq = (Y - t1) / (hem - t1); if (qq < 0.22) put(i, skin, 1); else put(i, sar, ((Y - Math.round(t1)) % 4 === 0) ? 0.7 : 1); } } }
    /* ---- 2. bontan: balloon the legs out past the knee, pinch at the ankle (edges smoothed row to row) ---- */
    if (spec.bag && ankle > hem + 8) { var pt = P[6], bg = spec.bag * (sideF && spec.bagSide ? spec.bagSide : 1) * H / 230, EL = [], ER = [];
      for (Y = hem + 1; Y <= ankle; Y++) { var ex = rowExt(Y, 6); if (!ex) { EL[Y] = ER[Y] = null; continue; } var a1 = ex[0], b1 = ex[1];
        while (a1 > 0 && C[Y * w + a1 - 1] === 1) a1--; while (b1 < w - 1 && C[Y * w + b1 + 1] === 1) b1++; EL[Y] = a1; ER[Y] = b1; }
      function sm(A, Y) { var s = 0, n = 0; for (var k = -4; k <= 4; k++) if (A[Y + k] != null) { s += A[Y + k]; n++; } return n ? s / n : null; }
      for (Y = hem + 1; Y <= ankle; Y++) { if (EL[Y] == null) continue; var tt = (Y - hem) / (ankle - hem); if (tt > 0.94) continue; var e = bg * Math.pow(Math.sin(Math.PI * Math.min(1, tt / 0.94)), 0.7);
        [[EL, -1], [ER, 1]].forEach(function (S) { var A = S[0], sd = S[1], base = sm(A, Y), tgt = Math.round(base + sd * e), xe = A[Y];
          if ((tgt - xe) * sd < 1) return;
          for (var xx2 = xe; xx2 !== tgt + sd; xx2 += sd) { if (xx2 < 1 || xx2 >= w - 1) break; var j = Y * w + xx2; if (xx2 !== xe && d[j * 4 + 3] > 120 && C[j] !== 1 && C[j] !== 6) break;
            var dist = (tgt - xx2) * sd, cc2 = dist < 2 ? INK : dist < 4 ? pt.s : pt.b; d[j * 4] = cc2[0]; d[j * 4 + 1] = cc2[1]; d[j * 4 + 2] = cc2[2]; d[j * 4 + 3] = 255; } }); } }
    x.putImageData(id, 0, 0);
    /* ---- 4. hair: pompadour or punch perm ---- */
    var capTop = 0, capBot = 0, hw = Math.max(8, hx1 - hx0), hcx = (hx0 + hx1) / 2, hh = Math.max(8, chin - y0), sc = H / 230, dir = face === 'left' ? -1 : face === 'right' ? 1 : 0;
    var ht = tri(spec.hairCol || '#1e1a22');
    if (spec.hair) { /* clear the old hair, lay a slick cap, put the face back, then the quiff / the perm on top */
      var hairBot = y0 + hh * 0.5; for (Y = y0; Y < y0 + H * 0.3; Y++) if (rowCount(Y, 3) >= 3) hairBot = Y;
      var chinH = Math.min(chin, Math.round(y0 + H * 0.2)), ft = face === 'back' ? hairBot : faceTop, cut = face === 'back' ? hairBot + 2 : ft + (chinH - ft) * 0.42, fext = [], fwM = 0;
      if (face !== 'back') for (Y = faceTop; Y <= chinH; Y++) { var fe = rowExt(Y, 2); if (fe && FCX >= 0) { var flim = H * 0.075; fe = [Math.max(fe[0], Math.round(FCX - flim)), Math.min(fe[1], Math.round(FCX + flim))]; if (fe[1] < fe[0]) fe = null; } fext[Y] = fe; if (fe && fe[1] - fe[0] > fwM) fwM = fe[1] - fe[0]; }
      var cur = x.getImageData(0, 0, w, h), cd = cur.data, keep = x.getImageData(0, 0, w, h);
      for (Y = Math.max(0, y0 - 2); Y < hairBot + 4; Y++) { var fe2 = face !== 'back' && Y >= faceTop ? fext[Y] : null; for (X = Math.max(0, hx0 - 10); X <= Math.min(w - 1, hx1 + 10); X++) { i = Y * w + X; var cl = C[i];
        var inFace = fe2 && X >= fe2[0] - 1 && X <= fe2[1] + 1;
        var nearF = fe2 && X >= fe2[0] - 2 && X <= fe2[1] + 2; if (cl === 3 || (Y < cut && ((cl === 1 && !inFace) || (cl === 8 && !inFace))) || (Y >= cut && Y < Math.max(hairBot + 3, chin - 2) && (cl === 8 || cl === 1) && !nearF && face !== 'back')) cd[i * 4 + 3] = 0; } }
      x.putImageData(cur, 0, 0);
      var fL, fR, skW = face === 'front' ? Math.max(fwM * 0.62 + 3 * sc, hw * 0.44) : face === 'back' ? hw * 0.38 : Math.max(hw * 0.46, fwM * 0.72), fL = w, fR = 0; fext.forEach(function (fe) { if (fe) { fL = Math.min(fL, fe[0]); fR = Math.max(fR, fe[1]); } }); var capCx = face === 'front' || face === 'back' ? hcx : fR > fL ? (dir > 0 ? fR : fL) - dir * skW * 0.88 : hcx - dir * skW * 0.2,
        capTop = y0 + (ft - y0) * 0.1; capBot = face === 'front' ? ft + (chinH - ft) * 0.2 : face === 'back' ? hairBot + 2 : Math.max(Math.min(hairBot, ft + (chinH - ft) * 0.5), ft + (chinH - ft) * 0.36); var capCy = (capTop + capBot) / 2 + (face === 'front' ? (capBot - capTop) * 0.12 : 0), capRy = capCy - capTop;
      var capRx = skW;
      var HP = null;
      if (sideF && fR > fL) { /* side views: a full-size head in profile drawn under the hair (the old bangs hid most of the face) */
        var fEdge = dir > 0 ? fR : fL, sHT = capTop, sCH = chinH + 3, sHH = sCH - sHT, hrx = sHH * 0.45, hcxS = fEdge - dir * sHH * 0.4, hcy = sHT + sHH * 0.5;
        HP = function (k) { function f(u, v) { return [hcxS + (fEdge + dir * u * sHH - hcxS) * k, hcy + (sHT + v * sHH - hcy) * k]; } var P = [['m', -0.3, 0], ['q', -0.02, 0, -0.03, 0.3], ['l', 0.01, 0.46], ['l', -0.01, 0.53], ['l', 0.08, 0.66], ['l', 0, 0.7], ['l', 0.02, 0.79], ['l', -0.01, 0.84], ['q', 0, 0.97, -0.14, 0.98], ['l', -0.42, 0.9], ['l', -0.5, 0.8], ['q', -0.9, 0.72, -0.86, 0.4], ['q', -0.8, 0, -0.3, 0]];
          x.beginPath(); P.forEach(function (p) { var a1 = f(p[1], p[2]); if (p[0] === 'm') x.moveTo(a1[0], a1[1]); else if (p[0] === 'l') x.lineTo(a1[0], a1[1]); else { var a2 = f(p[3], p[4]); x.quadraticCurveTo(a1[0], a1[1], a2[0], a2[1]); } }); x.closePath(); };
        HP(1); x.fillStyle = rgb(skin.b); x.fill(); x.save(); x.clip(); x.fillStyle = rgb(skin.s); x.beginPath(); x.moveTo(fEdge - dir * sHH * 0.5, sHT + sHH * 0.62); x.lineTo(fEdge - dir * sHH * 0.2, sHT + sHH * 0.95); x.lineTo(fEdge - dir * sHH * 0.9, sHT + sHH * 1.1); x.lineTo(fEdge - dir * sHH * 0.9, sHT + sHH * 0.6); x.fill(); x.restore();
        HP(1); x.lineWidth = 2 * sc; x.lineJoin = 'round'; x.strokeStyle = rgb(INK); x.stroke();
        capCx = hcxS - dir * sHH * 0.06; capRx = sHH * 0.47; capCy = hcy - sHH * 0.02; capRy = sHH * 0.53; capBot = capCy + capRy; ft = sHT; chinH = sCH; skW = sHH * 0.4; }
      x.save(); x.beginPath(); if (sideF) { var fYh = ft + (chinH - ft) * 0.3, bYh = ft + (chinH - ft) * 0.8; x.moveTo(0, 0); x.lineTo(w, 0); x.lineTo(w, dir > 0 ? fYh : bYh); x.lineTo(0, dir > 0 ? bYh : fYh); x.closePath(); } else x.rect(0, 0, w, capBot); x.clip();
      if (HP) HP(1.07); else { x.beginPath(); x.ellipse(capCx, capCy, capRx, capRy, 0, 0, Math.PI * 2); }
      x.fillStyle = rgb(ht.b); x.fill(); x.lineWidth = 2.2 * sc; x.strokeStyle = rgb(INK); x.stroke();
      x.lineWidth = 1.3 * sc; x.strokeStyle = rgb(ht.s); for (var gl = -2; gl <= 2; gl++) { x.beginPath(); x.ellipse(capCx + gl * skW * 0.22, capCy + capRy * 0.2, skW * 0.3, capRy * 0.95, 0, Math.PI * 1.1, Math.PI * 1.9); x.stroke(); }
      x.restore();
      /* the face back on top of the cap */
      var fc = document.createElement('canvas'); fc.width = w; fc.height = h; var fx3 = fc.getContext('2d'), fid = fx3.createImageData(w, h), kd = keep.data;
      if (face !== 'back') for (Y = faceTop; Y <= chinH + 6; Y++) { var fe3 = fext[Math.min(Y, chinH)]; if (!fe3) continue; for (X = fe3[0] - 1; X <= fe3[1] + 1; X++) { i = Y * w + X; if (C[i] === 3 || (C[i] === 8 && Y < hairBot + 3)) continue; if (Y < faceTop + (chinH - faceTop) * 0.14 && C[i] !== 2) continue; if (Y > chinH && C[i] !== 2 && C[i] !== 1) continue; fid.data[i * 4] = kd[i * 4]; fid.data[i * 4 + 1] = kd[i * 4 + 1]; fid.data[i * 4 + 2] = kd[i * 4 + 2]; fid.data[i * 4 + 3] = kd[i * 4 + 3]; } }
      fx3.putImageData(fid, 0, 0); var PROF = null; if (!(sideF && fR > fL)) x.drawImage(fc, 0, 0);
      else { /* a drawn profile, in the sheet's own line weight: brow, eye, nose, mouth, ear */
        var fh = sHH, ex2 = fEdge - dir * sHH * 0.13, ey2 = sHT + sHH * 0.53; PROF = { ex: ex2, ey: ey2, fh: fh };
        x.lineCap = 'round'; x.strokeStyle = rgb(INK); x.fillStyle = rgb(INK);
        x.lineWidth = 1.9 * sc; x.beginPath(); x.moveTo(fEdge - dir * sHH * 0.22, sHT + sHH * 0.43); x.lineTo(fEdge - dir * sHH * 0.02, sHT + sHH * 0.45); x.stroke();
        x.beginPath(); x.ellipse(ex2, ey2, 1.4 * sc, 2.3 * sc, 0, 0, 7); x.fill();
        x.lineWidth = 1.4 * sc; x.beginPath(); x.moveTo(fEdge - dir * sHH * 0.02, sHT + sHH * 0.8); x.lineTo(fEdge - dir * sHH * 0.12, sHT + sHH * 0.79); x.stroke();
        var erx = fEdge - dir * sHH * 0.47, ery = sHT + sHH * 0.58; x.beginPath(); x.ellipse(erx, ery, 2.4 * sc, 3.8 * sc, 0, 0, 7); x.fillStyle = rgb(skin.s); x.fill(); x.lineWidth = 1.4 * sc; x.stroke(); }
      chin = chinH;
      if (spec.hair === 'pomp') { var side = face === 'left' || face === 'right', rise = hh * 0.34, qx = side ? capCx + dir * skW * 0.5 : capCx, qy = capTop + (side ? rise * 0.12 : capRy * 0.12), qrx = side ? skW * 0.66 : skW * 0.84, qry = rise * (side ? 0.56 : 0.85);
        x.save(); x.translate(qx, qy); x.rotate(dir * -0.42);
        x.beginPath(); x.ellipse(0, 0, qrx, qry, 0, Math.PI * 0.92, Math.PI * 2.08); x.fillStyle = rgb(ht.b); x.lineWidth = 2.2 * sc; x.strokeStyle = rgb(INK); x.stroke(); x.fill();
        x.beginPath(); x.ellipse(0, qry * 0.3, qrx * 0.9, qry * 0.45, 0, Math.PI * 0.05, Math.PI * 0.95); x.fillStyle = rgb(ht.s); x.fill();
        x.lineCap = 'round'; x.lineWidth = 1.5 * sc; x.strokeStyle = rgb(ht.h); [-0.5, -0.12, 0.28].forEach(function (o) { x.beginPath(); x.ellipse(o * qrx * 0.7 + dir * qrx * 0.12, qry * 0.15, qrx * 0.42, qry * 0.62, 0, Math.PI * 1.15, Math.PI * 1.72); x.stroke(); });
        x.restore(); }
      if (spec.hair === 'perm') { /* punch perm: a tight, squared-off helmet of small curls hugging the skull, flat on top, straight hairline */
        var pr = 2.7 * sc, pw = (sideF ? capRx : skW) * 0.94, pL = capCx - pw, pR = capCx + pw, pT = capTop - capRy * 0.04, pB = capBot + (sideF ? 0 : 1), rad = Math.min(pw * 0.86, (pB - pT) * 0.9);
        var permPath = function () { x.beginPath(); x.moveTo(pL, pB); x.lineTo(pL, pT + rad); x.quadraticCurveTo(pL, pT, pL + rad, pT); x.lineTo(pR - rad, pT); x.quadraticCurveTo(pR, pT, pR, pT + rad); x.lineTo(pR, pB); x.closePath(); };
        if (HP) permPath = function () { HP(1.1); };
        x.save(); x.beginPath(); if (HP) { var fY2 = ft + (chinH - ft) * 0.28, bY2 = ft + (chinH - ft) * 0.76; x.moveTo(0, 0); x.lineTo(w, 0); x.lineTo(w, dir > 0 ? fY2 : bY2); x.lineTo(0, dir > 0 ? bY2 : fY2); x.closePath(); } else x.rect(0, 0, w, capBot + 1); x.clip(); permPath(); x.fillStyle = rgb(ht.s); x.fill(); x.save(); x.clip();
        for (var py = pT + pr * 0.6, rw = 0; py < pB + pr; py += pr * 1.3, rw++) for (var px = pL - pr; px <= pR + pr; px += pr * 1.5) { var cx2 = px + (rw % 2 ? pr * 0.75 : 0), jx = cx2 + (hash(py | 0, cx2 | 0) - 0.5) * pr * 0.4, jr = pr * (0.78 + 0.2 * hash(cx2 | 0, py | 0));
          x.beginPath(); x.arc(jx, py, jr, Math.PI * 0.9, Math.PI * 2.25); x.lineWidth = 1.05 * sc; x.strokeStyle = rgb(ht.b); x.stroke(); x.beginPath(); x.arc(jx - jr * 0.2, py - jr * 0.35, jr * 0.28, 0, 7); x.fillStyle = rgb(ht.h); x.fill(); }
        x.restore(); permPath(); x.lineWidth = 2.2 * sc; x.strokeStyle = rgb(INK); x.stroke(); x.restore();
        if (!PROF) x.drawImage(fc, 0, 0); } }
    /* ---- 3a. the top-knot: an ōichō ginkgo-leaf mage for an ōzeki, a plain chonmage otherwise ---- */
    if (spec.mage && spec.hair && capTop) { var mk = sc * (spec.mage === 'oicho' ? 1.55 : 0.9), mx = capCx + (sideF ? -dir * skW * 0.1 : 0), my = capTop + 1 * sc;
      x.save(); x.lineJoin = 'round'; x.lineWidth = 2 * sc; x.strokeStyle = rgb(INK);
      if (sideF) { x.beginPath(); x.moveTo(mx - dir * 6 * mk, my + 3 * mk); x.quadraticCurveTo(mx - dir * 3 * mk, my - 8 * mk, mx + dir * 9 * mk, my - 4 * mk); x.quadraticCurveTo(mx + dir * 13 * mk, my - 1 * mk, mx + dir * 10 * mk, my + 2 * mk); x.quadraticCurveTo(mx + dir * 2 * mk, my - 2 * mk, mx - dir * 1 * mk, my + 4 * mk); x.closePath(); x.fillStyle = rgb(ht.b); x.fill(); x.stroke(); }
      else { var fw2 = (face === 'back' ? 7 : 8) * mk, fh2 = 9 * mk; x.beginPath(); x.moveTo(mx, my + 2 * mk); x.quadraticCurveTo(mx - fw2 * 1.3, my - fh2 * 0.4, mx - fw2, my - fh2); x.quadraticCurveTo(mx, my - fh2 * 1.25, mx + fw2, my - fh2); x.quadraticCurveTo(mx + fw2 * 1.3, my - fh2 * 0.4, mx, my + 2 * mk); x.closePath(); x.fillStyle = rgb(ht.b); x.fill(); x.stroke();
        x.lineWidth = 1.2 * sc; x.strokeStyle = rgb(ht.h); [-0.45, 0, 0.45].forEach(function (o) { x.beginPath(); x.moveTo(mx, my); x.lineTo(mx + o * fw2, my - fh2 * 0.9); x.stroke(); }); }
      x.fillStyle = rgb(spec.mageTie || [240, 236, 226]); x.fillRect(mx - 2.5 * mk, my - 1 * mk, 5 * mk, 2.6 * mk); x.restore(); }
    /* ---- 3b. a sento towel over one shoulder ---- */
    if (spec.towel && face !== 'back') { var tY = chin + (hem - chin) * 0.0, tex = rowExt(Math.round(tY + 6 * sc), 4) || [x0, x1], tw = Math.max(4, (x1 - x0) * 0.1), tX = face === 'front' ? tex[0] + (tex[1] - tex[0]) * 0.2 : (dir > 0 ? tex[0] + tw * 0.4 : tex[1] - tw * 1.4), tL = (hem - tY) * (face === 'front' ? 0.82 : 0.6);
      x.save(); x.beginPath(); x.moveTo(tX, tY); x.lineTo(tX + tw, tY - 1 * sc); x.lineTo(tX + tw * 1.05, tY + tL); x.lineTo(tX + tw * 0.1, tY + tL + 2 * sc); x.closePath(); x.fillStyle = rgb(hx(spec.towel)); x.fill(); x.lineWidth = 1.8 * sc; x.strokeStyle = rgb(INK); x.stroke();
      x.strokeStyle = 'rgba(40,60,120,.55)'; x.lineWidth = 1.2 * sc; [0.78, 0.88].forEach(function (q) { x.beginPath(); x.moveTo(tX + tw * 0.08, tY + tL * q); x.lineTo(tX + tw * 1.02, tY + tL * q - 0.5); x.stroke(); }); x.restore(); }
    /* ---- 3c. a crest on the back of a short happi (no coat tails to carry it) ---- */
    if (spec.crest && face === 'back') { var cT = y0 + H * 0.24, cB = hem - H * 0.05, cG = Math.min((x1 - x0) * 0.42, (cB - cT) * 0.8), cCy = (cT + cB) / 2, cCx = (x0 + x1) / 2, ce = hx(spec.crest.col);
      x.save(); x.beginPath(); x.arc(cCx, cCy, cG * 0.7, 0, 7); x.fillStyle = rgb(ce); x.fill(); x.lineWidth = Math.max(1.4, 1.6 * sc); x.strokeStyle = rgb(INK); x.stroke(); glyph(x, spec.crest.k, cCx, cCy, cG * 0.95, hx(spec.crest.ink || '#22345e'), Math.max(1.3, 1.8 * sc)); x.restore(); }
    /* ---- 3. headband (painted on the head pixels, so it wraps) ---- */
    if (spec.band) { var by = Math.round(spec.hair && capBot ? (face === 'front' ? faceTop - Math.max(3, Math.round(5 * sc)) + 1 : sideF && PROF ? ft + (chinH - ft) * 0.27 : capTop + (capBot - capTop) * 0.62) : face === 'back' ? y0 + 0.4 * hh : faceTop - (face === 'front' ? 0.02 : 0.14) * hh), bh = Math.max(3, Math.round(5 * sc)), bt = tri(spec.band);
      id = x.getImageData(0, 0, w, h); d = id.data;
      for (Y = by; Y < by + bh; Y++) for (X = hx0 - 2; X <= hx1 + 2; X++) { i = Y * w + X; if (d[i * 4 + 3] < 120 || C[i] === 5 || C[i] === 4) continue; var cb = (Y === by || Y === by + bh - 1) ? INK : Y === by + 1 ? bt.h : bt.b; if (spec.bandLeo && cb !== INK) { var lq = leo(X * 1.6, Y * 1.6, 0.55); if (lq) cb = LEO[lq]; } d[i * 4] = cb[0]; d[i * 4 + 1] = cb[1]; d[i * 4 + 2] = cb[2]; }
      x.putImageData(id, 0, 0);
      if (face !== 'front') { var kx = face === 'back' ? hcx + hw * 0.18 : (dir < 0 ? hx1 : hx0), ky = by + bh / 2, sd = face === 'back' ? 1 : -dir; /* knot tails */
        x.lineJoin = 'round'; [0, 1].forEach(function (n2) { x.beginPath(); x.moveTo(kx, ky - 1.5 * sc); x.quadraticCurveTo(kx + sd * (7 + n2 * 3) * sc, ky + (2 + n2 * 4) * sc, kx + sd * (13 + n2 * 2) * sc, ky + (6 + n2 * 7) * sc); x.lineTo(kx + sd * (10 + n2 * 2) * sc, ky + (8 + n2 * 7) * sc); x.quadraticCurveTo(kx + sd * 5 * sc, ky + (4 + n2 * 3) * sc, kx, ky + 1.5 * sc); x.closePath(); x.fillStyle = rgb(n2 ? bt.s : bt.b); x.fill(); x.strokeStyle = rgb(INK); x.lineWidth = 1.6 * sc; x.stroke(); }); }
      if (spec.bandDot && face === 'front') { x.beginPath(); x.arc(hcx, by + bh / 2, bh * 0.42, 0, 7); x.fillStyle = spec.bandDot; x.fill(); } }
    /* ---- 5. sunglasses ---- */
    if (spec.shades && face !== 'back') { var fy = faceTop + (chin - faceTop) * (spec.shadeQ != null ? spec.shadeQ : 0.3), fw = hw * 0.62, lw2 = fw * 0.4, lh = Math.max(3, (chin - faceTop) * 0.2);
      var lens = face === 'front' ? [hcx - fw * 0.27, hcx + fw * 0.27] : [typeof PROF === 'object' && PROF ? PROF.ex + dir * lw2 * 0.15 : hcx + dir * hw * 0.3]; if (face !== 'front' && PROF) fy = PROF.ey - PROF.fh * 0.02;
      lens.forEach(function (lx) { x.beginPath(); x.ellipse(lx, fy, lw2 / 2, lh / 2, 0, 0, 7); x.fillStyle = 'rgb(20,18,26)'; x.fill(); x.fillStyle = 'rgba(160,220,255,0.8)'; x.fillRect(lx - lw2 * 0.25, fy - lh * 0.25, lw2 * 0.22, Math.max(1, lh * 0.18)); });
      x.strokeStyle = 'rgb(20,18,26)'; x.lineWidth = 1.6 * sc; x.beginPath(); if (face === 'front') { x.moveTo(lens[0] + lw2 / 2, fy); x.lineTo(lens[1] - lw2 / 2, fy); } else { x.moveTo(lens[0] - dir * lw2 / 2, fy); x.lineTo(PROF ? PROF.ex - dir * PROF.fh * 0.55 : hcx - dir * hw * 0.15, fy - 1); } x.stroke(); }
    /* ---- 6. the long coat (tokkōfuku) or the long sukeban skirt ---- */
    var ext = null; for (Y = hem + 2; Y < Math.min(ankle, hem + 14); Y++) { var e6 = rowExt(Y, 6); if (e6) ext = ext ? [Math.min(ext[0], e6[0]), Math.max(ext[1], e6[1])] : e6; }
    if (spec.skirt) { ext = null; for (Y = hem + 2; Y < hem + 16; Y++) { var a2 = -1, b2 = -1; for (X = 0; X < w; X++) if (d[(Y * w + X) * 4 + 3] > 100 && C[Y * w + X] === 2) { if (a2 < 0) a2 = X; b2 = X; } if (a2 >= 0) ext = ext ? [Math.min(ext[0], a2 - 2), Math.max(ext[1], b2 + 2)] : [a2 - 2, b2 + 2]; } }
    if (!ext || ext[1] - ext[0] < 8) ext = rowExt(hem, 4) || [x0 + 10, x1 - 10];
    if (spec.painted && !spec.skirt) { var jx = null; for (Y = hem - 4; Y <= hem; Y++) { var e4 = rowExt(Y, 4); if (e4) jx = jx ? [Math.min(jx[0], e4[0]), Math.max(jx[1], e4[1])] : e4; } if (jx) ext = [jx[0] + 2, jx[1] - 2]; }
    if (spec.painted && spec.skirt) { var sx2 = null; for (Y = hem - 3; Y <= hem; Y++) { var e7 = rowExt(Y, 6) || rowExt(Y, 4); if (e7) sx2 = sx2 ? [Math.min(sx2[0], e7[0]), Math.max(sx2[1], e7[1])] : e7; } if (sx2) ext = sx2; }
    var tor = null; for (Y = hem - 6; Y <= hem; Y++) { var e8 = rowExt(Y, 4); if (e8) tor = tor ? [Math.min(tor[0], e8[0]), Math.max(tor[1], e8[1])] : e8; }
    if (tor && !spec.skirt) { var tw = tor[1] - tor[0], tc = (tor[0] + tor[1]) / 2, mx = Math.min(spec.coatMaxW || 1e9, Math.max(tw * 1.25, 20 * H / 230)); if (ext[1] - ext[0] > mx) ext = [Math.max(ext[0], tc - mx / 2), Math.min(ext[1], tc + mx / 2)]; } /* a lunge's back leg must not drag the coat out sideways */
    var pl = ext[0] - 2, prr = ext[1] + 2, cx = (pl + prr) / 2, tail = hem + (ankle - hem) * (spec.coatLen || 0);
    var co = spec.coat ? tri(spec.coat) : null, lin = spec.lining ? tri(spec.lining) : null, emb = spec.emb ? hx(spec.emb) : null;
    function panel(pts, fill, shadeSide) { x.beginPath(); pts.forEach(function (p, n) { if (n) x.lineTo(p[0], p[1]); else x.moveTo(p[0], p[1]); }); x.closePath(); x.fillStyle = rgb(fill.b); x.fill();
      if (shadeSide) { x.save(); x.clip(); x.fillStyle = rgb(fill.s); var sx0 = shadeSide < 0 ? Math.min.apply(null, pts.map(function (p) { return p[0]; })) : Math.max.apply(null, pts.map(function (p) { return p[0]; })) - 4 * sc; x.fillRect(sx0, 0, 4 * sc, h); x.restore(); }
      x.lineWidth = 2.2 * sc; x.lineJoin = 'round'; x.strokeStyle = rgb(INK); x.stroke(); }
    if (spec.skirt) { var sk = tri(spec.skirt), fl = 5 * sc; var sl = ext[0] - 1, sr = ext[1] + 1;
      var bl = sl - fl - (face === 'right' ? 3 * sc : 0), br = sr + fl + (face === 'left' ? 3 * sc : 0);
      if (spec.painted) { var lg = null, ly = Math.round(hem + (ankle - hem) * 0.7); for (X = 0; X < w; X++) if (d[(ly * w + X) * 4 + 3] > 100) { if (!lg) lg = [X, X]; lg[1] = X; } if (lg) { bl = Math.min(bl, lg[0] + 4 * sc); br = Math.max(br, lg[1] - 4 * sc); } }
      panel([[sl, hem], [sr, hem], [br, ankle], [bl, ankle]], sk, 1);
      x.strokeStyle = rgb(sk.s); x.lineWidth = 1.2 * sc; for (var pk = 1; pk < 5; pk++) { var fx = sl + (sr - sl) * pk / 5; x.beginPath(); x.moveTo(fx, hem + 3); x.lineTo(bl + (br - bl) * pk / 5, ankle - 2); x.stroke(); } }
    if (co && spec.coatLen) { var fl2 = (5 + (spec.bag || 0) * 0.7) * sc, gap = shirt && face === 'front' ? Math.max(3 * sc, (shirt.r - shirt.l) * 0.5) : 4 * sc;
      if (face === 'front') { var bL = pl - fl2, bR = prr + fl2, iL = cx - gap - 1, iR = cx + gap + 1;
        if (spec.painted) { var lg2 = null, ty = Math.round(tail); for (X = 0; X < w; X++) if (d[(ty * w + X) * 4 + 3] > 100) { if (!lg2) lg2 = [X, X]; lg2[1] = X; } if (lg2) { bL = Math.min(bL, lg2[0] + (pl - lg2[0]) * 0.3); bR = Math.max(bR, lg2[1] - (lg2[1] - prr) * 0.3); iL = cx - gap - (cx - gap - bL) * 0.35; iR = cx + gap + (bR - cx - gap) * 0.35; } }
        panel([[pl, hem - 1], [cx - gap, hem - 1], [iL, tail], [bL, tail + 2 * sc]], co, -1); panel([[cx + gap, hem - 1], [prr, hem - 1], [bR, tail + 2 * sc], [iR, tail]], co, 1);
        if (lin) { [[cx - gap, -1], [cx + gap, 1]].forEach(function (s) { x.beginPath(); x.moveTo(s[0], hem); x.lineTo(s[0] - s[1] * 2.2 * sc, hem); x.lineTo((s[1] < 0 ? iL : iR) - s[1] * 2.6 * sc, tail - 1); x.lineTo((s[1] < 0 ? iL : iR), tail - 1); x.closePath(); x.fillStyle = rgb(lin.b); x.fill(); }); }
        if (emb) { x.strokeStyle = rgb(emb); x.lineWidth = 1.3 * sc; [[pl + 3 * sc, -1], [prr - 3 * sc, 1]].forEach(function (s) { x.beginPath(); x.moveTo(s[0], tail - 3 * sc); x.lineTo(s[0] + s[1] * fl2 * 0.6, tail - 3 * sc); x.stroke(); });
          var gs = Math.min(9 * sc, (tail - hem) / 2.6); if (gs > 4) { var KF = (spec.kanji && spec.kanji.front) || ['ten', 'ge']; if (KF[0]) glyph(x, KF[0], pl + (cx - gap - pl) * 0.45 - fl2 * 0.3, hem + gs * 0.9, gs, emb, 1.1 * sc); if (KF[1]) glyph(x, KF[1], prr - (prr - cx - gap) * 0.45 + fl2 * 0.3, hem + gs * 0.9, gs, emb, 1.1 * sc); } } }
      else if (face === 'back') { panel([[pl - 1, hem - 1], [prr + 1, hem - 1], [prr + fl2, tail + 2 * sc], [cx + 1, tail + 1 * sc], [cx - 1, tail + 1 * sc], [pl - fl2, tail + 2 * sc]], co, 1);
        x.strokeStyle = rgb(INK); x.lineWidth = 1.4 * sc; x.beginPath(); x.moveTo(cx, hem + (tail - hem) * 0.45); x.lineTo(cx, tail); x.stroke(); }
      else { var back = face === 'left' ? 1 : -1, bx = back > 0 ? prr : pl, fx2 = back > 0 ? pl : prr;
        panel([[fx2 - back * 1, hem - 1], [bx + back * 2 * sc, hem - 1], [bx + back * (fl2 + 4 * sc), tail + 1 * sc], [fx2 - back * 3 * sc, tail + 2 * sc]], co, back);
        if (lin) { x.beginPath(); x.moveTo(fx2 - back, hem); x.lineTo(fx2 + back * 2.6 * sc, hem); x.lineTo(fx2 - back * 0.4 * sc, tail); x.lineTo(fx2 - back * 3 * sc, tail + 1); x.closePath(); x.fillStyle = rgb(lin.b); x.fill(); x.strokeStyle = rgb(INK); x.lineWidth = 1.2 * sc; x.stroke(); }
        if (emb) { var gs2 = Math.min(9 * sc, (tail - hem) / 2.4); if (gs2 > 4) glyph(x, (spec.kanji && spec.kanji.side) || 'jo', (pl + prr) / 2 + back * 3 * sc, hem + (tail - hem) * 0.5, gs2, emb, 1.1 * sc); } } }
    /* ---- 7. back embroidery 天上天下 ---- */
    if (emb && face === 'back' && spec.coatLen) { var top = y0 + H * 0.26, bot = Math.max(hem + 4, tail - (tail - hem) * 0.3), gs3 = Math.min((x1 - x0) * 0.3, (bot - top) / 4.3);
      var KB = (spec.kanji && spec.kanji.back) || ['ten', 'jo', 'ten', 'ge'];
      if (KB.length === 1) { /* one big crest in a circle, the sento way */ var gb = Math.min((x1 - x0) * 0.38, (bot - top) * 0.52), cyb = top + (bot - top) * 0.42;
        x.lineWidth = Math.max(1.6, 2 * sc); x.strokeStyle = rgb(emb); x.beginPath(); x.arc(cx, cyb, gb * 0.72, 0, 7); x.stroke(); glyph(x, KB[0], cx, cyb, gb, emb, Math.max(1.3, 1.7 * sc)); }
      else KB.forEach(function (g, n3) { glyph(x, g, cx, top + gs3 * 0.6 + n3 * gs3 * 1.08, gs3, emb, Math.max(1.2, 1.5 * sc)); }); }
    if (emb && face === 'front' && spec.coatLen && shirt) { x.strokeStyle = rgb(emb); x.lineWidth = 1.1 * sc; [[shirt.l - 2, -1], [shirt.r + 2, 1]].forEach(function (s) { x.beginPath(); x.moveTo(s[0], shirt.t + 2); x.lineTo(s[0] + s[1] * 1, hem - 2); x.stroke(); }); }
    /* hands back on top */
    var hc = document.createElement('canvas'); hc.width = w; hc.height = h; var hcx2 = hc.getContext('2d', { willReadFrequently: true }), hid = hcx2.createImageData(w, h), hd = hid.data, od = id.data;
    var base = x.getImageData(0, 0, w, h); /* the recoloured hands live in id (before vector add-ons) */
    for (i = 0; i < N; i++) if (H2[i]) { hd[i * 4] = od[i * 4]; hd[i * 4 + 1] = od[i * 4 + 1]; hd[i * 4 + 2] = od[i * 4 + 2]; hd[i * 4 + 3] = od[i * 4 + 3]; }
    hcx2.putImageData(hid, 0, 0); x.drawImage(hc, 0, 0); base = null;
    if (spec.debug) { var dd = x.getImageData(0, 0, w, h); var PAL = [[0, 0, 0], [0, 0, 0], [255, 180, 140], [255, 230, 0], [0, 200, 120], [255, 255, 255], [40, 80, 255], [200, 0, 200], [255, 0, 0]];
      for (i = 0; i < N; i++) if (C[i]) { var pc = PAL[C[i]]; dd.data[i * 4] = pc[0]; dd.data[i * 4 + 1] = pc[1]; dd.data[i * 4 + 2] = pc[2]; dd.data[i * 4 + 3] = 255; }
      [hem, ankle, faceTop, chin].forEach(function (yy, n4) { for (X = 0; X < w; X++) { i = yy * w + X; dd.data[i * 4] = n4 === 0 ? 255 : 0; dd.data[i * 4 + 1] = n4 === 1 ? 255 : 0; dd.data[i * 4 + 2] = n4 > 1 ? 255 : 0; dd.data[i * 4 + 3] = 255; } });
      x.putImageData(dd, 0, 0); }
    return cv;
  }
  var FACE4 = ['front', 'left', 'right', 'back'];
  /* a whole sheet: cols x rows cells of cw x ch, row r faces FACE4[r] (single figures face front) */
  function paintSheet(img, spec, cols, rows, cw, chh, faces) {
    var W = img.naturalWidth || img.width, Hh = img.naturalHeight || img.height; cw = cw || W / cols; chh = chh || Hh / rows;
    var out = document.createElement('canvas'); out.width = W; out.height = Hh; var o = out.getContext('2d', { willReadFrequently: true });
    for (var r = 0; r < rows; r++) for (var c = 0; c < cols; c++) { var f = (faces || FACE4)[r] || 'front'; o.drawImage(paintCell(img, c * cw, r * chh, cw, chh, spec, f), c * cw, r * chh); }
    return out;
  }
  /* ---- the looks ---- */
  var SPEC = {
    /* Punk A "Murasaki": purple tokkōfuku with gold 天上天下, sarashi, black regent pompadour, white bontan */
    punkA: { base: 'punk', glove: 1, pal: { 4: tri('#5b2a86'), 6: tri('#e6e1d3'), 7: tri('#2a2430') }, coat: '#5b2a86', coatLen: 0.7, emb: '#f0c040', lining: '#d63a3a', bag: 9, shirt: 'sarashi', hair: 'pomp', hairCol: '#1e1a24' },
    /* Punk B "Leopard": Nails' crew. Short black tanran jacket, leopard shirt, purple bontan, brown punch perm, shades */
    punkB: { base: 'punk', glove: 1, pal: { 3: tri('#5a3a26'), 4: tri('#23202a'), 6: tri('#4b2f6e'), 7: tri('#c9b48a') }, bag: 10, shirt: 'leopard', hair: 'perm', hairCol: '#5a3a26', shades: 1 },
    /* Punk C "Hachimaki": indigo long coat, red headband, sarashi, khaki bontan, bleached pompadour */
    punkC: { base: 'punk', glove: 1, pal: { 3: tri('#e8cf7a'), 4: tri('#2b3a6e'), 6: tri('#b9a27a'), 7: tri('#efe9dc') }, coat: '#2b3a6e', coatLen: 0.6, emb: '#e8e2d0', lining: '#c8a040', bag: 8, shirt: 'sarashi', hair: 'pomp', hairCol: '#e8cf7a', band: '#d8382e' },
    /* Flip, Nails' lieutenant: built big. White long coat, leopard lining, gold kanji, blond pompadour, shades, black bontan */
    flip: { base: 'punk', glove: 1, bulk: 0.72, bagSide: 0.5, pal: { 3: tri('#f0d060'), 4: tri('#efece4'), 6: tri('#302b3a'), 7: tri('#f2efe6') }, coat: '#efece4', coatLen: 0.76, emb: '#d9a520', lining: '#d6a046', bag: 12, shirt: 'leopard', leoSc: 1.1, hair: 'pomp', hairCol: '#f0d060', shades: 1 },
    /* Ryo: black tokkōfuku with fire-orange 天上天下, orange lining, sarashi, white hachimaki with a red sun, charcoal bontan */
    ryo: { base: 'ryo', pal: { 4: tri('#1c1a22'), 6: tri('#2e2c36') }, coat: '#1c1a22', coatLen: 0.72, emb: '#ff8a26', lining: '#e0541e', bag: 9, shirt: 'sarashi', band: '#f1ece0', bandDot: '#d22a2a', hemMax: 0.62 },
    /* Aoi: sukeban. White long coat with cyan 天上天下 over sarashi, ankle-length navy pleated skirt */
    aoi: { base: 'aoi', pal: { 4: tri('#e9ecef'), 6: tri('#1d2540') }, coat: '#e9ecef', coatLen: 0.55, emb: '#2fc8e0', lining: '#2fc8e0', skirt: '#1d2540', hemMax: 0.66 }
  };
  /* the gray-coat men by the Lantern Alley informant: long charcoal-gray coat, dark slacks, slicked black hair, tinted shades. No kanji. */
  SPEC.gray = { base: 'punk', glove: 1, pal: { 4: tri('#55585f'), 6: tri('#2a2b31'), 7: tri('#3b3c43') }, coat: '#6c6f76', coatLen: 0.8, emb: null, lining: '#3f4148', bag: 2, hair: 'pomp', hairCol: '#16161a', shades: 1 };
  /* Kaneda, Gōda's door man at Kitsune-no-Yu: built heavy (less than Flip), an indigo sento long coat with the white 湯 crest in a ring on the back
   * and 湯 on both front panels, a white towel tied as a hachimaki, black punch perm, sarashi, charcoal bontan. No shades: he wants you to see him look. */
  /* ---- Gōda's crew, the Kitsune-no-Yu bath boys: nothing like the Punks' long coats. Short indigo happi with a white collar band and a banded hem,
   * the white 湯 crest on the back, the chest open on an irezumi of waves and peonies, a ribbed haramaki, dark momohiki, geta. Slicked-back hair. ---- */
  SPEC.yuH = { base: 'punk', glove: 1, pal: { 3: tri('#16141a'), 4: tri('#2a3f7a'), 6: tri('#2a2830') }, happi: { eri: '#efe9dc', hemCol: '#efe9dc' }, crest: { k: 'yu', col: '#efe9dc', ink: '#2a3f7a' },
    shirt: 'irezumi', hara: 0.62, haraCol: '#d8c9a4', bag: 2, geta: { wood: '#b98a52', strap: '#b8322a' }, hair: 'slick', hairCol: '#16141a', towel: null };
  /* Kaneda, the door man: the same cut in black with a red collar band, a white towel tied round the head, built heavy */
  SPEC.kaneda = { base: 'punk', glove: 1, bulk: 0.5, bagSide: 0.4, pal: { 3: tri('#1a1714'), 4: tri('#1d1b22'), 6: tri('#33302e') }, happi: { eri: '#b8322a', hemCol: '#b8322a' }, crest: { k: 'yu', col: '#efe9dc', ink: '#1d1b22' },
    shirt: 'irezumi', hara: 0.6, haraCol: '#efe9dc', bag: 3, geta: { wood: '#a87a46', strap: '#1d1b22' }, hair: 'slick', hairCol: '#1a1714', band: '#f2ede0' };
  /* Gōda Daizō: the old ōzeki. Built like a wall, an ōichō top-knot, a boiler-keeper's brown hanten over a bare chest, a black haramaki where the mawashi was,
   * a blue-striped tenugui over one shoulder, big geta */
  SPEC.goda = { base: 'punk', glove: 1, bulk: 1.5, sumo: 1, bagSide: 0.5, pal: { 3: tri('#141216'), 4: tri('#6b3b22'), 5: tri('#e9b98c'), 6: tri('#3a3530') }, happi: { eri: '#2a211c', hemCol: '#2a211c' }, crest: { k: 'yu', col: '#e9dcc0', ink: '#6b3b22' },
    shirt: 'bare', hara: 0.55, haraCol: '#22202a', bag: 6, geta: { wood: '#9a6a3a', strap: '#efe9dc' }, hair: 'slick', hairCol: '#141216', mage: 'oicho', towel: '#f4f1ea' };
  /* the West Street stall's two accessories, worn over the yankii look: tinted shades / a leopard hachimaki with leopard coat lining */
  SPEC.ryoS = Object.assign({}, SPEC.ryo, { shades: 1, shadeQ: 0.0 }); SPEC.aoiS = Object.assign({}, SPEC.aoi, { shades: 1 });
  SPEC.ryoL = Object.assign({}, SPEC.ryo, { band: '#d6a046', bandDot: null, bandLeo: 1, lining: '#d6a046' }); SPEC.aoiL = Object.assign({}, SPEC.aoi, { band: '#d6a046', bandLeo: 1, lining: '#d6a046' });
  SPEC.ryoFig = Object.assign({}, SPEC.ryo, { base: 'ryoP', painted: 1, bag: 0, coatLen: 0.6, hemMax: 0.6 }); SPEC.aoiFig = Object.assign({}, SPEC.aoi, { base: 'aoiP', painted: 1, coatLen: 0.5, hemMax: 0.62 });
  root.FFF_YK = { SPEC: SPEC, paintCell: paintCell, paintSheet: paintSheet, tri: tri };
})(window);
