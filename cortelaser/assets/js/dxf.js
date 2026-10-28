/* Cortelaser · análisis de DXF en el navegador (sin dependencias).
   Lee DXF ASCII (R12 a 2018): LINE, ARC, CIRCLE, LWPOLYLINE, POLYLINE/VERTEX,
   SPLINE (aproximada por sus puntos), ELLIPSE. Detecta textos, cotas y bloques.
   Devuelve contornos cerrados, longitud de corte, medidas y avisos.
   window.CLDXF.analyze(texto) -> {ok, unit, bbox, w, h, cut, loops, holes, outers, open, minHole, area, paths, notes} */
(function () {
  'use strict';
  var TAU = Math.PI * 2;

  function pairs(text) {
    var lines = text.split(/\r\n|\r|\n/), out = [];
    for (var i = 0; i + 1 < lines.length; i += 2) out.push([parseInt(lines[i].trim(), 10), lines[i + 1].trim()]);
    return out;
  }

  function arcPoints(cx, cy, r, a0, a1) {
    // a0 -> a1 en sentido antihorario (radianes)
    while (a1 <= a0) a1 += TAU;
    var n = Math.max(8, Math.ceil((a1 - a0) / (TAU / 72))), pts = [];
    for (var i = 0; i <= n; i++) {
      var a = a0 + (a1 - a0) * i / n;
      pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]);
    }
    return { pts: pts, len: r * (a1 - a0) };
  }

  function bulgeSeg(p, q, b) {
    // Segmento de polilínea con abombamiento b (tan(θ/4))
    if (!b) return { pts: [p, q], len: Math.hypot(q[0] - p[0], q[1] - p[1]) };
    var th = 4 * Math.atan(b), c = Math.hypot(q[0] - p[0], q[1] - p[1]);
    if (c === 0) return { pts: [p], len: 0 };
    var r = c / (2 * Math.sin(Math.abs(th) / 2));
    var mx = (p[0] + q[0]) / 2, my = (p[1] + q[1]) / 2;
    var d = Math.sqrt(Math.max(r * r - c * c / 4, 0));
    var ux = (q[0] - p[0]) / c, uy = (q[1] - p[1]) / c;
    var sgn = (b > 0 ? 1 : -1) * (Math.abs(th) > Math.PI ? -1 : 1);
    var cx = mx - uy * d * sgn, cy = my + ux * d * sgn;
    var a0 = Math.atan2(p[1] - cy, p[0] - cx), a1 = Math.atan2(q[1] - cy, q[0] - cx);
    var res;
    if (b > 0) res = arcPoints(cx, cy, r, a0, a1);
    else { res = arcPoints(cx, cy, r, a1, a0); res.pts.reverse(); }
    return { pts: res.pts, len: Math.abs(th) * r };
  }

  function polyPath(verts, closed) {
    var pts = [], len = 0, n = verts.length;
    if (!n) return null;
    var segs = closed ? n : n - 1;
    for (var i = 0; i < segs; i++) {
      var a = verts[i], b = verts[(i + 1) % n];
      var s = bulgeSeg([a[0], a[1]], [b[0], b[1]], a[2] || 0);
      if (pts.length) s.pts = s.pts.slice(1);
      pts = pts.concat(s.pts);
      len += s.len;
    }
    if (n === 1) pts = [[verts[0][0], verts[0][1]]];
    return { pts: pts, len: len, closed: !!closed };
  }

  function parse(text) {
    var P = pairs(text), i = 0, notes = {}, unitCode = 0, paths = [], section = null;
    var ent = null, data = [];
    function flush() {
      if (!ent) return;
      var g = function (code) { for (var k = 0; k < data.length; k++) if (data[k][0] === code) return data[k][1]; return null; };
      var f = function (code, d) { var v = g(code); return v === null ? d : parseFloat(v); };
      var all = function (code) { return data.filter(function (x) { return x[0] === code; }).map(function (x) { return parseFloat(x[1]); }); };
      if (ent === 'LINE') {
        var p = [f(10, 0), f(20, 0)], q = [f(11, 0), f(21, 0)];
        paths.push({ pts: [p, q], len: Math.hypot(q[0] - p[0], q[1] - p[1]), closed: false, kind: 'line' });
      } else if (ent === 'CIRCLE') {
        var r = f(40, 0), c = arcPoints(f(10, 0), f(20, 0), r, 0, TAU);
        paths.push({ pts: c.pts, len: TAU * r, closed: true, kind: 'circle', d: 2 * r });
      } else if (ent === 'ARC') {
        var a = arcPoints(f(10, 0), f(20, 0), f(40, 0), f(50, 0) * Math.PI / 180, f(51, 0) * Math.PI / 180);
        paths.push({ pts: a.pts, len: a.len, closed: false, kind: 'arc' });
      } else if (ent === 'LWPOLYLINE') {
        var verts = [], cur = null;
        data.forEach(function (x) {
          if (x[0] === 10) { cur = [parseFloat(x[1]), 0, 0]; verts.push(cur); }
          else if (x[0] === 20 && cur) cur[1] = parseFloat(x[1]);
          else if (x[0] === 42 && cur) cur[2] = parseFloat(x[1]);
        });
        var pl = polyPath(verts, (f(70, 0) & 1) === 1);
        if (pl) { pl.kind = 'poly'; paths.push(pl); }
      } else if (ent === 'SPLINE') {
        var fx = all(11), fy = all(21), cx = all(10), cy = all(20);
        var xs = fx.length > 1 ? fx : cx, ys = fx.length > 1 ? fy : cy, sp = [];
        for (var k = 0; k < xs.length; k++) sp.push([xs[k], ys[k], 0]);
        var spl = polyPath(sp, (f(70, 0) & 1) === 1);
        if (spl) { spl.kind = 'spline'; paths.push(spl); notes.spline = (notes.spline || 0) + 1; }
      } else if (ent === 'ELLIPSE') {
        var ex = f(10, 0), ey = f(20, 0), mx = f(11, 0), my = f(21, 0), ratio = f(40, 1), t0 = f(41, 0), t1 = f(42, TAU);
        var ma = Math.hypot(mx, my), rot = Math.atan2(my, mx), mi = ma * ratio, ep = [], el = 0;
        if (t1 <= t0) t1 += TAU;
        var n = 96;
        for (var j = 0; j <= n; j++) {
          var t = t0 + (t1 - t0) * j / n, x = ma * Math.cos(t), y = mi * Math.sin(t);
          ep.push([ex + x * Math.cos(rot) - y * Math.sin(rot), ey + x * Math.sin(rot) + y * Math.cos(rot)]);
          if (j) el += Math.hypot(ep[j][0] - ep[j - 1][0], ep[j][1] - ep[j - 1][1]);
        }
        paths.push({ pts: ep, len: el, closed: Math.abs(t1 - t0 - TAU) < 1e-6, kind: 'ellipse' });
      } else if (ent === 'TEXT' || ent === 'MTEXT') {
        notes.text = (notes.text || 0) + 1;
      } else if (ent === 'DIMENSION' || ent === 'LEADER' || ent === 'MULTILEADER') {
        notes.dim = (notes.dim || 0) + 1;
      } else if (ent === 'INSERT') {
        notes.insert = (notes.insert || 0) + 1;
      } else if (ent === 'HATCH' || ent === 'SOLID' || ent === '3DFACE' || ent === 'POINT') {
        notes.other = (notes.other || 0) + 1;
      }
      ent = null; data = [];
    }
    var poly = null;
    for (; i < P.length; i++) {
      var code = P[i][0], val = P[i][1];
      if (code === 0) {
        if (val === 'SECTION') { flush(); section = null; continue; }
        if (val === 'ENDSEC') { flush(); section = null; continue; }
        if (section === 'ENTITIES') {
          if (poly) {
            if (val === 'VERTEX') { if (ent === 'VERTEX_') pushVertex(); else flush(); ent = 'VERTEX_'; data = []; continue; }
            if (val === 'SEQEND') {
              if (ent === 'VERTEX_') { pushVertex(); }
              var pp = polyPath(poly.v, poly.closed); if (pp) { pp.kind = 'poly'; paths.push(pp); }
              poly = null; ent = null; data = []; continue;
            }
          }
          if (ent === 'VERTEX_') pushVertex();
          flush();
          if (val === 'POLYLINE') { poly = { v: [], closed: false }; ent = 'POLYLINE_'; data = []; continue; }
          ent = val; data = [];
        } else { flush(); }
        continue;
      }
      if (code === 2 && section === null && P[i - 1] && P[i - 1][1] === 'SECTION') { section = val; continue; }
      if (section === 'HEADER' && code === 9 && val === '$INSUNITS' && P[i + 1]) { unitCode = parseInt(P[i + 1][1], 10); }
      if (ent === 'POLYLINE_' && code === 70 && poly) { poly.closed = (parseInt(val, 10) & 1) === 1; continue; }
      if (ent) data.push([code, val]);
    }
    flush();
    function pushVertex() {
      var x = 0, y = 0, b = 0;
      data.forEach(function (d) { if (d[0] === 10) x = parseFloat(d[1]); else if (d[0] === 20) y = parseFloat(d[1]); else if (d[0] === 42) b = parseFloat(d[1]); });
      if (poly) poly.v.push([x, y, b]);
      ent = null; data = [];
    }
    return { paths: paths, notes: notes, unitCode: unitCode };
  }

  function chain(paths, tol) {
    // Une primitivas abiertas por sus extremos para formar contornos.
    var closed = paths.filter(function (p) { return p.closed; }).map(function (p) { return { pts: p.pts, len: p.len, d: p.d || 0 }; });
    var open = paths.filter(function (p) { return !p.closed && p.pts.length > 1; }).map(function (p) { return { pts: p.pts.slice(), len: p.len }; });
    var near = function (a, b) { return Math.abs(a[0] - b[0]) <= tol && Math.abs(a[1] - b[1]) <= tol; };
    var loops = closed, chains = [];
    while (open.length) {
      var cur = open.pop(), grown = true;
      while (grown) {
        grown = false;
        var head = cur.pts[0], tail = cur.pts[cur.pts.length - 1];
        if (near(head, tail) && cur.pts.length > 2) break;
        for (var k = 0; k < open.length; k++) {
          var o = open[k], oh = o.pts[0], ot = o.pts[o.pts.length - 1];
          if (near(tail, oh)) cur.pts = cur.pts.concat(o.pts.slice(1));
          else if (near(tail, ot)) cur.pts = cur.pts.concat(o.pts.slice().reverse().slice(1));
          else if (near(head, ot)) cur.pts = o.pts.concat(cur.pts.slice(1));
          else if (near(head, oh)) cur.pts = o.pts.slice().reverse().concat(cur.pts.slice(1));
          else continue;
          cur.len += o.len; open.splice(k, 1); grown = true; break;
        }
      }
      var h = cur.pts[0], t = cur.pts[cur.pts.length - 1];
      if (near(h, t) && cur.pts.length > 2) loops.push({ pts: cur.pts, len: cur.len, d: 0 });
      else chains.push(cur);
    }
    return { loops: loops, open: chains };
  }

  function bbox(pts) {
    var b = [Infinity, Infinity, -Infinity, -Infinity];
    pts.forEach(function (p) { if (p[0] < b[0]) b[0] = p[0]; if (p[1] < b[1]) b[1] = p[1]; if (p[0] > b[2]) b[2] = p[0]; if (p[1] > b[3]) b[3] = p[1]; });
    return b;
  }
  function area(pts) {
    var s = 0;
    for (var i = 0, n = pts.length; i < n; i++) { var a = pts[i], b = pts[(i + 1) % n]; s += a[0] * b[1] - b[0] * a[1]; }
    return Math.abs(s) / 2;
  }
  function inside(pt, pts) {
    var c = false;
    for (var i = 0, j = pts.length - 1; i < pts.length; j = i++) {
      var a = pts[i], b = pts[j];
      if ((a[1] > pt[1]) !== (b[1] > pt[1]) && pt[0] < (b[0] - a[0]) * (pt[1] - a[1]) / (b[1] - a[1]) + a[0]) c = !c;
    }
    return c;
  }

  function analyze(text) {
    if (/^AutoCAD Binary DXF/.test(text.slice(0, 22))) return { ok: false, error: 'binary' };
    var r = parse(text);
    if (!r.paths.length) return { ok: false, error: 'empty', notes: r.notes };
    var k = { 1: 25.4, 2: 304.8, 4: 1, 5: 10, 6: 1000 }[r.unitCode] || 1;
    if (k !== 1) r.paths.forEach(function (p) { p.pts = p.pts.map(function (q) { return [q[0] * k, q[1] * k]; }); p.len *= k; if (p.d) p.d *= k; });
    var allPts = []; r.paths.forEach(function (p) { allPts = allPts.concat(p.pts); });
    var bb = bbox(allPts), size = Math.max(bb[2] - bb[0], bb[3] - bb[1]);
    var ch = chain(r.paths, Math.max(size * 1e-6, 0.005));
    ch.loops.forEach(function (l) { l.bb = bbox(l.pts); l.area = area(l.pts); });
    ch.loops.sort(function (a, b) { return b.area - a.area; });
    // Profundidad de anidamiento: par = contorno exterior, impar = agujero
    ch.loops.forEach(function (l, idx) {
      var depth = 0, probe = l.pts[0];
      for (var j = 0; j < idx; j++) if (ch.loops[j].area > l.area && inside(probe, ch.loops[j].pts)) depth++;
      l.depth = depth;
    });
    var outers = ch.loops.filter(function (l) { return l.depth % 2 === 0; });
    var holes = ch.loops.filter(function (l) { return l.depth % 2 === 1; });
    var net = outers.reduce(function (s, l) { return s + l.area; }, 0) - holes.reduce(function (s, l) { return s + l.area; }, 0);
    var minHole = holes.length ? Math.min.apply(null, holes.map(function (l) { return l.d || Math.min(l.bb[2] - l.bb[0], l.bb[3] - l.bb[1]); })) : null;
    var cut = r.paths.reduce(function (s, p) { return s + p.len; }, 0);
    return {
      ok: true, unit: r.unitCode, scaled: k !== 1, bbox: bb, w: bb[2] - bb[0], h: bb[3] - bb[1], cut: cut,
      loops: ch.loops.length, outers: outers.length, holes: holes.length, open: ch.open.length, minHole: minHole,
      area: net, paths: ch.loops.map(function (l) { return { pts: l.pts, hole: l.depth % 2 === 1 }; }).concat(ch.open.map(function (o) { return { pts: o.pts, open: true }; })),
      notes: r.notes
    };
  }

  function svg(res) {
    var b = res.bbox, w = b[2] - b[0], h = b[3] - b[1], m = Math.max(w, h) * 0.04 || 1, sw = Math.max(w, h) / 220;
    var vb = [b[0] - m, -(b[3] + m), w + 2 * m, h + 2 * m].map(function (v) { return +v.toFixed(3); }).join(' ');
    var d = function (pts) { return 'M' + pts.map(function (p) { return p[0].toFixed(2) + ' ' + (-p[1]).toFixed(2); }).join('L'); };
    var body = res.paths.map(function (p) {
      var col = p.open ? '#B3261E' : (p.hole ? '#33343A' : '#111214');
      return '<path d="' + d(p.pts) + (p.open ? '' : 'Z') + '" fill="' + (p.hole || p.open ? 'none' : 'rgba(255,90,31,.10)') + '" stroke="' + col + '" stroke-width="' + sw.toFixed(3) + '"' + (p.open ? ' stroke-dasharray="' + (sw * 4).toFixed(3) + '"' : '') + '/>';
    }).join('');
    return '<svg viewBox="' + vb + '" xmlns="http://www.w3.org/2000/svg" role="img">' + body + '</svg>';
  }

  window.CLDXF = { analyze: analyze, svg: svg };
})();
