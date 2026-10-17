/* JomaPaint · landing (propuesta). Sin dependencias.
   1. Partículas de polvo en el hero   2. Estaciones del proceso
   3. Explorador RAL                   4. Cotizador guiado
   5. Carrusel de proveedores          6. Ajuste de acento (?acento=rojo|neutro) */
(function () {
  'use strict';
  var JP = window.JP || {};
  var T = JP.t || {};
  var ROOT = JP.root || '';
  var reduce = false;
  try { reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}

  /* ---------- utilidades ---------- */
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var esc = function (v) { return String(v == null ? '' : v).replace(/[&<>"']/g, function (ch) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]; }); };
  var fmt = function (s, o) { return String(s).replace(/\{(\w+)\}/g, function (m, k) { return o[k] != null ? o[k] : m; }); };
  var hx = function (h) { var n = parseInt(String(h).replace('#', ''), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
  var mix = function (a, b, t) { var x = hx(a), y = hx(b); return '#' + x.map(function (v, i) { return ('0' + Math.round(v + (y[i] - v) * t).toString(16)).slice(-2); }).join(''); };
  var rgba = function (h, a) { var c = hx(h); return 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + a + ')'; };
  var lum = function (h) { var c = hx(h).map(function (v) { v = v / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; };
  /* Texto sobre un color: negro o blanco, el que dé más contraste (WCAG). */
  var ink = function (h) { var L = lum(h); return (L + 0.05) / 0.05 >= 1.05 / (L + 0.05) ? '#000000' : '#FFFFFF'; };
  var norm = function (t) { return String(t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
  var scrollToId = function (id) { var el = document.getElementById(id); if (el) el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); };

  /* Color compartido entre explorador, proceso, cotizador y seguimiento */
  var listeners = [];
  var state = { ral: { c: '1023', n: '', h: '#F7B500' }, tex: 'lisa', gloss: 'satinado' };
  var setRal = function (r) { state.ral = r; listeners.forEach(function (fn) { fn(r); }); };
  var onRal = function (fn) { listeners.push(fn); };

  /* ---------- 6. acento ---------- */
  try {
    var acc = new URLSearchParams(location.search).get('acento');
    if (acc === 'rojo' || acc === 'neutro') document.documentElement.setAttribute('data-acento', acc);
  } catch (e) {}

  /* ---------- 1. partículas ---------- */
  (function particles() {
    var cv = $('#powder'), root = $('.hero');
    if (!cv || !root || !cv.getContext) return;
    var ctx = cv.getContext('2d');
    var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    var n0 = 0, W = 1, H = 1, P = [], t = 0, visible = true, mouse = null, sprite = null, color = '#F7B500';
    var rnd = Math.random;
    var target = function () { return W < 760 ? { x: W * 0.78, y: H * 0.34 } : { x: W * 0.71, y: H * 0.46 }; };
    var spawn = function (p, first) {
      p.amb = rnd() < 0.26; p.life = 0; p.fade = 0; p.spin = rnd() < 0.5 ? -1 : 1; p.dep = 26 + rnd() * 90;
      if (p.amb) { p.x = rnd() * W; p.y = rnd() * H; p.vx = (rnd() - 0.5) * 0.18; p.vy = -0.04 - rnd() * 0.14; p.r = 0.9 + rnd() * 2.6; p.a = 0.05 + rnd() * 0.14; p.max = 600 + rnd() * 900; }
      else { p.x = W * (first ? 0.28 + rnd() * 0.66 : 0.26 + rnd() * 0.12); p.y = H * (0.2 + rnd() * 0.56); p.vx = 0.5 + rnd() * 1.6; p.vy = (rnd() - 0.5) * 1.0; p.r = 0.45 + rnd() * 1.3; p.a = 0.32 + rnd() * 0.58; p.max = 260 + rnd() * 520; }
      if (first) p.life = Math.floor(rnd() * 120);
      return p;
    };
    var resize = function () {
      W = Math.max(1, root.clientWidth); H = Math.max(1, root.clientHeight);
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var small = W < 760;
      var n = Math.round(Math.min(small ? 360 : 900, Math.max(small ? 160 : 240, (W * H) / (small ? 1700 : 1400))));
      if (n0 && P.length < n) n = Math.min(n, P.length);
      while (P.length < n) P.push(spawn({}, true));
      P.length = n; n0 = n0 || n;
    };
    var getSprite = function () {
      if (sprite) return sprite;
      var c = hx(color), s = document.createElement('canvas'); s.width = 32; s.height = 32;
      var g = s.getContext('2d'), gr = g.createRadialGradient(16, 16, 0, 16, 16, 16);
      gr.addColorStop(0, 'rgba(255,255,255,1)');
      gr.addColorStop(0.18, 'rgba(' + c.join(',') + ',1)');
      gr.addColorStop(0.45, 'rgba(' + c.join(',') + ',0.3)');
      gr.addColorStop(1, 'rgba(' + c.join(',') + ',0)');
      g.fillStyle = gr; g.fillRect(0, 0, 32, 32); sprite = s; return s;
    };
    var step = function () {
      var T0 = target();
      for (var i = 0; i < P.length; i++) {
        var p = P[i]; p.life++;
        if (p.amb) {
          var a0 = Math.sin(p.x * 0.003 + t * 0.0005) + Math.cos(p.y * 0.004 - t * 0.0004);
          p.vx += Math.cos(a0 * 2.2) * 0.006; p.vy += Math.sin(a0 * 2.2) * 0.006; p.vx *= 0.99; p.vy *= 0.99;
        } else {
          var ts = mouse ? [[T0.x, T0.y, 1], [mouse.x, mouse.y, 1.7]] : [[T0.x, T0.y, 1]];
          for (var k = 0; k < ts.length; k++) {
            var dx = ts[k][0] - p.x, dy = ts[k][1] - p.y, d2 = dx * dx + dy * dy, d = Math.sqrt(d2) + 0.001;
            var f = ts[k][2] * 900 / (d2 + 9000);
            p.vx += (dx / d) * f - (dy / d) * f * 0.95 * p.spin;
            p.vy += (dy / d) * f + (dx / d) * f * 0.95 * p.spin;
            if (k === 0 && d < p.dep && !p.fade) p.fade = 1;
          }
          var a1 = Math.sin(p.x * 0.0042 + t * 0.0007) + Math.cos(p.y * 0.0051 - t * 0.0006);
          p.vx += Math.cos(a1 * 2.4) * 0.03; p.vy += Math.sin(a1 * 2.4) * 0.03; p.vx *= 0.975; p.vy *= 0.975;
        }
        p.x += p.vx; p.y += p.vy;
        if (p.fade) { p.fade -= 0.035; if (p.fade <= 0) spawn(p, false); }
        if (p.life > p.max || p.x < -40 || p.x > W + 40 || p.y < -40 || p.y > H + 40) spawn(p, false);
      }
      t += 16;
    };
    var draw = function (trail) {
      if (trail) { ctx.globalCompositeOperation = 'destination-out'; ctx.fillStyle = 'rgba(0,0,0,0.2)'; ctx.fillRect(0, 0, W, H); }
      else ctx.clearRect(0, 0, W, H);
      ctx.globalCompositeOperation = 'lighter';
      var sp = getSprite();
      for (var i = 0; i < P.length; i++) {
        var p = P[i], a = p.a * Math.min(1, p.life / 40);
        if (p.life > p.max - 60) a *= Math.max(0, (p.max - p.life) / 60);
        if (p.fade) a *= p.fade;
        if (a <= 0.003) continue;
        var s = p.r * 6; ctx.globalAlpha = a; ctx.drawImage(sp, p.x - s / 2, p.y - s / 2, s, s);
      }
      ctx.globalAlpha = 1;
    };
    /* Arranca cuando la página ya ha cargado y el navegador está libre: no compite con el primer pintado. */
    var start = function () {
      resize();
      if (window.ResizeObserver) new ResizeObserver(resize).observe(root); else window.addEventListener('resize', resize);
      if (window.IntersectionObserver) new IntersectionObserver(function (es) { visible = es[0] ? es[0].isIntersecting : true; }).observe(root);
      root.addEventListener('pointermove', function (e) { var r = root.getBoundingClientRect(); mouse = { x: e.clientX - r.left, y: e.clientY - r.top }; });
      root.addEventListener('pointerleave', function () { mouse = null; });
      if (reduce) { for (var n = 0; n < 220; n++) step(); draw(false); return; }
      /* Presupuesto por fotograma: si el equipo no llega a ~30 fps (pintado incluido),
         se reducen las partículas, luego se pinta uno de cada dos fotogramas y, en último caso,
         la animación se queda quieta. */
      var ema = 0, frames = 0, skip = false, odd = false, last = 0, stopped = false;
      (function loop(now) {
        if (stopped) return;
        if (visible && !document.hidden) {
          if (last) { var dt = now - last; ema = frames++ ? ema * 0.85 + dt * 0.15 : dt; }
          last = now;
          if (frames > 15 && ema > 34) {
            var min = Math.round(n0 * 0.35);
            if (P.length > min) P.length = Math.max(min, Math.round(P.length * 0.6));
            else if (!skip) skip = true;
            else if (ema > 60) stopped = true;
            frames = 0;
          }
          if (!(skip && (odd = !odd))) { step(); draw(true); }
        } else last = 0;
        requestAnimationFrame(loop);
      })(performance.now());
    };
    var idle = function () { if (window.requestIdleCallback) window.requestIdleCallback(start, { timeout: 2000 }); else setTimeout(start, 300); };
    if (document.readyState === 'complete') idle(); else window.addEventListener('load', idle);
  })();

  /* ---------- 2. estaciones del proceso ---------- */
  (function process() {
    var tabs = $$('#stations [role="tab"]'), panels = $$('.st-panel'), zones = $$('#zones > div');
    var photos = $$('#st-photos img'), cap = $('#st-cap'), carriage = $('#carriage'), fx = $('#fx');
    if (!tabs.length) return;
    var st = 0, manual = false;
    var front = $('#pc-front'), top = $('#pc-top'), side = $('#pc-side'), speck = $('#pc-speck'), gloss = $('#pc-gloss'), brush = $('#pc-brush');
    var zoneBg = function (i) {
      return [
        'radial-gradient(80% 70% at 50% 45%, rgba(120,170,220,0.22), transparent 72%)',
        'radial-gradient(80% 80% at 50% 58%, rgba(242,169,0,0.24), transparent 72%)',
        'radial-gradient(80% 70% at 50% 50%, ' + rgba(state.ral.h, 0.3) + ', transparent 72%)',
        'radial-gradient(80% 80% at 50% 58%, rgba(232,95,30,0.28), transparent 72%)',
        'radial-gradient(80% 70% at 50% 50%, rgba(250,249,246,0.1), transparent 72%)'
      ][i];
    };
    var render = function (focus) {
      var h = state.ral.h;
      tabs.forEach(function (b, i) { var on = i === st; b.setAttribute('aria-selected', on ? 'true' : 'false'); b.tabIndex = on ? 0 : -1; });
      panels.forEach(function (p, i) { p.hidden = i !== st; });
      zones.forEach(function (z, i) { z.classList.toggle('on', i === st); z.classList.toggle('glow', i === st && (i === 1 || i === 3)); z.style.background = i === st ? zoneBg(i) : 'transparent'; });
      photos.forEach(function (im, i) { im.classList.toggle('on', i === st); });
      if (cap && T.stCaps) cap.textContent = T.stCaps[st];
      if (carriage) carriage.style.left = (st * 20 + 10) + '%';
      var f, tp, sd, sO = 0, gO = 0, bO = 0;
      if (st <= 1) { f = '#8C9096'; tp = '#B7BBC0'; sd = '#5D6167'; bO = st === 0 ? 0.24 : 0.14; }
      else if (st === 2) { var chalk = mix(h, '#FFFFFF', 0.26); f = chalk; tp = mix(chalk, '#FFFFFF', 0.25); sd = mix(chalk, '#000000', 0.3); sO = 0.6; }
      else { f = h; tp = mix(h, '#FFFFFF', 0.24); sd = mix(h, '#000000', 0.34); gO = 0.55; }
      if (front) { front.setAttribute('fill', f); top.setAttribute('fill', tp); side.setAttribute('fill', sd); speck.setAttribute('opacity', sO); gloss.setAttribute('opacity', gO); brush.setAttribute('opacity', bO); }
      if (fx) {
        var html = '';
        if (st === 2 && !reduce) for (var k = 0; k < 14; k++) { var t0 = 64 + ((k * 23) % 90); html += '<span style="position:absolute;left:' + (-150 + ((k * 37) % 70)) + 'px;top:' + t0 + 'px;width:' + (2 + (k % 3)) + 'px;height:' + (2 + (k % 3)) + 'px;border-radius:50%;background:' + h + ';box-shadow:0 0 8px ' + h + ';--dx:' + (170 + ((k * 19) % 40)) + 'px;--dy:' + ((112 - t0) * 0.35) + 'px;animation:jpSpray 1.25s linear ' + ((k * 0.17) % 1.25).toFixed(2) + 's infinite;"></span>'; }
        if (st === 0 && !reduce) for (var j = 0; j < 9; j++) html += '<span style="position:absolute;left:' + (44 + j * 10) + 'px;top:46px;width:2px;height:7px;background:#9CC6EA;animation:jpDrip 1.5s ease-in ' + ((j * 0.37) % 1.5).toFixed(2) + 's infinite;"></span>';
        if (st === 4 && !reduce) html += '<div style="position:absolute;left:34px;top:60px;width:104px;height:1px;background:#FAF9F6;box-shadow:0 0 12px 1px rgba(250,249,246,.8);animation:jpScan 1.6s ease-in-out infinite alternate;"></div>';
        fx.innerHTML = html;
      }
      if (focus) tabs[st].focus();
    };
    tabs.forEach(function (b, i) {
      b.addEventListener('click', function () { st = i; manual = true; render(false); });
      b.addEventListener('keydown', function (e) {
        var k = e.key, n = null;
        if (k === 'ArrowRight') n = (st + 1) % tabs.length; else if (k === 'ArrowLeft') n = (st + tabs.length - 1) % tabs.length; else if (k === 'Home') n = 0; else if (k === 'End') n = tabs.length - 1;
        if (n != null) { e.preventDefault(); st = n; manual = true; render(true); }
      });
    });
    onRal(function () { render(false); });
    var sec = $('#proceso'), inView = true;
    if (window.IntersectionObserver && sec) new IntersectionObserver(function (es) { inView = es[0].isIntersecting; }, { threshold: 0.25 }).observe(sec);
    if (!reduce) setInterval(function () { if (!manual && inView && !document.hidden) { st = (st + 1) % tabs.length; render(false); } }, 4200);
    render(false);
  })();

  /* ---------- 3. explorador RAL ---------- */
  var RAL = (window.JP_RAL || []).map(function (r) { return { c: r[0], es: r[1], fr: r[2], h: '#' + r[3], f: r[0].charAt(0), p: r[4] === 'p', l: r[4] === 'l' }; });
  var ralName = function (x) { return T.ralName === 2 ? x.fr : x.es; };
  (function explorer() {
    var grid = $('#ral-grid'); if (!grid || !RAL.length) return;
    var fam = 'all', q = '';
    var DOT = { '1': '#F7B500', '2': '#E75B12', '3': '#C1121C', '4': '#904684', '5': '#13447C', '6': '#3E753B', '7': '#8F999F', '8': '#6F4A2F', '9': '#F7F9EF' };
    var famsEl = $('#ral-fams'), empty = $('#ral-empty'), count = $('#ral-count');
    var famNames = T.fams || [];
    famsEl.innerHTML = ['all', '1', '2', '3', '4', '5', '6', '7', '8', '9'].map(function (id, i) {
      return '<button type="button" data-fam="' + id + '" aria-pressed="' + (id === 'all') + '">' + (id === 'all' ? '' : '<span class="dot" style="background:' + DOT[id] + '"></span>') + esc(famNames[i] || id) + '</button>';
    }).join('');
    var sheen = 'linear-gradient(135deg, rgba(255,255,255,0.42) 0%, rgba(255,255,255,0) 48%, rgba(255,255,255,0.28) 74%, rgba(255,255,255,0) 100%), ';
    var paintGrid = function () {
      var nq = norm(q).replace(/^ral\s*/, '').trim();
      var list = RAL.filter(function (x) {
        if (fam !== 'all' && x.f !== fam) return false;
        if (!nq) return true;
        return x.c.indexOf(nq) === 0 || norm(x.es).indexOf(nq) >= 0 || norm(x.fr).indexOf(nq) >= 0;
      });
      grid.innerHTML = list.map(function (x) {
        var on = x.c === state.ral.c;
        var lbl = 'RAL ' + x.c + ' ' + ralName(x) + (x.p ? ' (' + T.pearl + ')' : '') + (x.l ? ' (' + T.lum + ')' : '');
        return '<button type="button" class="sw tnum" data-c="' + x.c + '" aria-pressed="' + on + '" aria-label="' + esc(lbl) + '" title="' + esc(lbl) + '" style="background:' + (x.p ? sheen : '') + x.h + ';color:' + ink(x.h) + '">' + x.c + (x.l ? '<span class="lum"></span>' : '') + '</button>';
      }).join('');
      empty.hidden = list.length > 0;
      if (!list.length) empty.textContent = fmt(T.empty, { q: q });
      count.textContent = fmt(T.count, { n: list.length });
    };
    /* Acabados: mate sin brillo; satinado con un brillo ancho y suave; brillante con el reflejo de una ventana.
       w/k: luz y sombra de la cara · sheen: brillo difuso · refl: reflejo · edge: canto superior */
    var G = { mate: { w: 0.05, k: 0.12, sheen: 0, refl: 0, edge: 0.22 }, satinado: { w: 0.1, k: 0.24, sheen: 0.2, refl: 0, edge: 0.38 }, brillante: { w: 0.14, k: 0.4, sheen: 0.06, refl: 1, edge: 0.65 } };
    var FAMIDX = { '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9 };
    var paintPlate = function () {
      var sel = RAL.filter(function (x) { return x.c === state.ral.c; })[0] || RAL[0];
      var base = sel.h, L0 = lum(base), light = L0 < 0.05;
      var solid = light ? mix(base, '#FAF9F6', 0.86) : mix(base, '#141414', 0.64);
      var field = $('#ral-field');
      field.style.background = 'radial-gradient(70% 55% at 50% 38%, rgba(255,255,255,' + (light ? '0.5' : '0.10') + '), rgba(255,255,255,0) 70%), ' + solid;
      field.style.color = light ? '#1A1A1A' : '#FAF9F6';
      var g = G[state.gloss], tx = state.tex === 'texturada', pale = L0 > 0.6;
      $('#f0').setAttribute('stop-color', mix(base, '#FFFFFF', g.w));
      $('#f1').setAttribute('stop-color', base);
      $('#f2').setAttribute('stop-color', mix(base, '#000000', g.k));
      $('#r-top').setAttribute('fill', mix(base, '#FFFFFF', 0.3));
      $('#r-side').setAttribute('fill', mix(base, '#000000', 0.42));
      $('#r-hole').setAttribute('fill', solid);
      var sheen = g.sheen * (tx ? 0.5 : 1) * (pale ? 0.6 : 1), refl = g.refl * (tx ? 0.3 : 1);
      $('#sh0').setAttribute('stop-opacity', sheen.toFixed(3));
      $('#sh1').setAttribute('stop-opacity', (sheen * 0.35).toFixed(3));
      $('#rf1').setAttribute('stop-opacity', (0.48 * refl).toFixed(3));
      $('#rf2').setAttribute('stop-opacity', (0.26 * refl).toFixed(3));
      $('#rm1').setAttribute('stop-opacity', (0.14 * refl).toFixed(3));
      $('#r-edge').setAttribute('stroke-opacity', g.edge);
      $('#r-tex-d').setAttribute('opacity', tx ? 0.5 : 0);
      $('#r-tex-l').setAttribute('opacity', tx ? (pale ? 0.3 : 0.35) : 0);
      $('#r-pearl').setAttribute('opacity', sel.p ? 0.5 : 0);
      $('#ral-code').textContent = sel.c;
      $('#ral-name').textContent = ralName(sel);
      $('#ral-hex').textContent = sel.h.toUpperCase();
      $('#ral-fam').textContent = (famNames[FAMIDX[sel.f]] || '') + (sel.p ? ' · ' + T.pearl : '') + (sel.l ? ' · ' + T.lum : '');
      $('#ral-sticker').textContent = 'RAL ' + sel.c + ' · ' + T.texSticker[state.tex] + ' · ' + T.glossSticker[state.gloss];
      $('#ral-svg').setAttribute('aria-label', fmt(T.svg, { c: sel.c, n: ralName(sel), tex: T.tex[state.tex], gloss: T.gloss[state.gloss] }));
      $$('.ral-current').forEach(function (e) { e.textContent = sel.c; });
      if (plate3d) plate3d.update({ hex: sel.h, tex: state.tex, gloss: state.gloss, pearl: sel.p, lum: sel.l, sticker: $('#ral-sticker').textContent, label: $('#ral-svg').getAttribute('aria-label') });
    };
    /* Placa en 3D (three.js, assets/ral3d.js): se carga al acercarse a la sección. Sin WebGL, se queda la placa SVG. */
    var plate3d = null;
    (function load3d() {
      var host = $('.ral-plate'); if (!host || !window.IntersectionObserver) return;
      try { if (navigator.connection && navigator.connection.saveData) return; } catch (e) {}
      var io = new IntersectionObserver(function (es) {
        if (!es.some(function (e) { return e.isIntersecting; })) return;
        io.disconnect();
        if (!window.WebGLRenderingContext) return;
        import(new URL(ROOT + 'assets/ral3d.js', location.href).href).then(function (m) {
          plate3d = m.init(host, { reduce: reduce });
          paintPlate();
          requestAnimationFrame(function () { host.classList.add('is-3d'); });
        }).catch(function () {});
      }, { rootMargin: '600px 0px' });
      io.observe(host);
    })();
    famsEl.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-fam]'); if (!b) return;
      fam = b.getAttribute('data-fam');
      $$('button', famsEl).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      paintGrid();
    });
    $('#ral-q').addEventListener('input', function (e) { q = e.target.value; paintGrid(); });
    grid.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-c]'); if (!b) return;
      var x = RAL.filter(function (r) { return r.c === b.getAttribute('data-c'); })[0];
      $$('.sw', grid).forEach(function (s) { s.setAttribute('aria-pressed', s === b ? 'true' : 'false'); });
      setRal({ c: x.c, n: ralName(x), h: x.h });
    });
    var segs = function (sel, key) {
      $$(sel + ' button').forEach(function (b) {
        b.addEventListener('click', function () {
          state[key] = b.getAttribute('data-' + key);
          $$(sel + ' button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
          paintPlate(); if (window.JPQ) window.JPQ.sync();
        });
      });
    };
    segs('#seg-tex', 'tex'); segs('#seg-gloss', 'gloss');
    $('#ral-use').addEventListener('click', function () { if (window.JPQ) window.JPQ.goStep(2); scrollToId('presupuesto'); });
    onRal(function () { paintPlate(); });
    window.JPR = { paint: paintPlate };
    var first = RAL.filter(function (x) { return x.c === state.ral.c; })[0];
    if (first) state.ral = { c: first.c, n: ralName(first), h: first.h };
    paintPlate();
    /* La rejilla de 213 colores se pinta al acercarse a la sección. */
    if (window.IntersectionObserver) {
      var io = new IntersectionObserver(function (es) { if (es.some(function (e) { return e.isIntersecting; })) { io.disconnect(); paintGrid(); } }, { rootMargin: '800px 0px' });
      io.observe(grid);
    } else paintGrid();
  })();

  /* ---------- 4. cotizador ---------- */
  (function quote() {
    var main = $('#q-main'), aside = $('#q-aside'), stepsEl = $('#q-steps');
    if (!main) return;
    /* Arranca con una referencia vacía: el cliente no tiene que borrar nada. */
    var blank = function (id) { return { id: id, ref: '', qty: '', mat: 0, kg: '', L: '', A: '', H: '', hang: -1, faces: '', file: '', size: '' }; };
    var q = { step: 1, env: 1, del: 0, rgpd: false, extras: {}, nextId: 2, lines: [blank(1)], form: {}, code: '', heroFiles: [], err: '' };
    var val = function (k) { return esc(q.form[k] || ''); };
    q.extras[T.extras.length - 1] = true;
    /* Plazo: un día laborable desde que entra la solicitud, en horario de oficina
       (lunes a viernes, 7:00–17:00, hora de Madrid). Fuera de horario, el reloj
       empieza a las 7:00 del siguiente día laborable. Se redondea a la hora siguiente. */
    var deadline = (function () {
      var OPEN = 7, CLOSE = 17, H = 3600000, p = {}, now = new Date(), w;
      try { new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Madrid', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(now).forEach(function (x) { p[x.type] = x.value; }); } catch (e) {}
      /* hora de pared de Madrid guardada en campos UTC: sin saltos por cambio de hora */
      w = p.year ? new Date(Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour % 24, +p.minute)) : new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours(), now.getMinutes()));
      var at = function (d, h) { return new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate(), h)); };
      var work = function (d) { var x = d.getUTCDay(); return x !== 0 && x !== 6; };
      if (w.getUTCMinutes()) w = new Date(at(w, w.getUTCHours()).getTime() + H);
      if (w.getUTCHours() >= CLOSE) w = at(new Date(w.getTime() + 24 * H), OPEN);
      else if (w.getUTCHours() < OPEN) w = at(w, OPEN);
      while (!work(w)) w = at(new Date(w.getTime() + 24 * H), OPEN);
      var d = new Date(w.getTime() + 24 * H);
      while (!work(d)) d = new Date(d.getTime() + 24 * H);
      /* las 7:00 de un día equivalen al cierre (17:00) del día laborable anterior */
      if (d.getUTCHours() === OPEN) { d = at(new Date(d.getTime() - 24 * H), CLOSE); while (!work(d)) d = at(new Date(d.getTime() - 24 * H), CLOSE); }
      return fmt(T.dl || '{wd} {d} {m} {h}:00', { wd: (T.wd || [])[d.getUTCDay()] || '', d: d.getUTCDate(), m: (T.mo || [])[d.getUTCMonth()] || (d.getUTCMonth() + 1), h: d.getUTCHours() });
    })();
    $$('.q-deadline').forEach(function (e) { e.textContent = deadline; });
    var ico = {
      file: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1A1A1A" stroke-width="1.5" aria-hidden="true"><path d="M6 3 H14 L19 8 V21 H6 Z M14 3 V8 H19"></path></svg>',
      up: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1A1A1A" stroke-width="1.5" aria-hidden="true"><path d="M12 15.5 V3.5 M7 8.5 L12 3.5 L17 8.5 M4 14 V20 H20 V14"></path></svg>',
      x: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1A1A1A" stroke-width="1.5" aria-hidden="true"><path d="M6 6 L18 18 M18 6 L6 18"></path></svg>',
      plus: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1A1A1A" stroke-width="1.5" aria-hidden="true"><path d="M12 5 V19 M5 12 H19"></path></svg>',
      warn: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1A1A1A" stroke-width="1.5" aria-hidden="true" style="flex:none; margin-top:1px;"><path d="M12 3 L22 20 H2 Z M12 9.5 V14 M12 16.5 V17.5"></path></svg>',
      ok: '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="1.75" aria-hidden="true"><path d="M4.5 12.5 L9.5 17.5 L19.5 6.5"></path></svg>'
    };
    var seg = function (name, opts, cur, extra) {
      return '<div class="seg">' + opts.map(function (o, i) { return '<button type="button" data-act="' + name + '" data-v="' + i + '"' + (extra || '') + ' aria-pressed="' + (i === cur) + '">' + esc(o) + '</button>'; }).join('') + '</div>';
    };
    var texIdx = function () { return state.tex === 'texturada' ? 1 : 0; };
    var glossIdx = function () { return ['mate', 'satinado', 'brillante'].indexOf(state.gloss); };
    var lineHTML = function (l, i) {
      var n = i + 1;
      var top = l.file
        ? '<span class="q-file">' + ico.file + '<span style="min-width:0;"><span class="q-file-n">' + esc(l.file) + '</span><span class="q-file-s">' + esc(l.size) + '</span></span><button type="button" class="q-unfile link-ink" data-act="unfile" data-id="' + l.id + '">' + esc(T.unfile) + '</button></span>'
        : '<label class="q-drop">' + ico.up + '<span>' + esc(T.addFile) + '</span><input type="file" class="sr-file" data-act="file" data-id="' + l.id + '"></label>';
      return '<fieldset class="q-line"><legend>' + esc(fmt(T.ref, { n: n })) + '</legend>' +
        '<div class="q-line-top">' + top + '<button type="button" class="q-x" data-act="rm" data-id="' + l.id + '" aria-label="' + esc(fmt(T.remove, { n: n })) + '">' + ico.x + '</button></div>' +
        '<div class="g4">' +
          '<label class="field">' + esc(T.fRef) + '<input class="input" type="text" data-f="ref" data-id="' + l.id + '" value="' + esc(l.ref) + '" placeholder="' + esc(T.fRefPh) + '"></label>' +
          '<label class="field">' + esc(T.fQty) + '<input class="input tnum" type="number" min="1" inputmode="numeric" data-f="qty" data-id="' + l.id + '" value="' + esc(l.qty) + '"></label>' +
          '<label class="field">' + esc(T.fMat) + '<select class="input" data-f="mat" data-id="' + l.id + '">' + T.mats.map(function (m, k) { return '<option value="' + k + '"' + (k === l.mat ? ' selected' : '') + '>' + esc(m) + '</option>'; }).join('') + '</select></label>' +
          '<label class="field">' + esc(T.fKg) + '<input class="input tnum" type="text" inputmode="decimal" data-f="kg" data-id="' + l.id + '" value="' + esc(l.kg) + '" placeholder="' + esc(T.fKgPh) + '"></label>' +
        '</div>' +
        '<div role="group" aria-label="' + esc(fmt(T.dimsLabel, { n: n })) + '" class="field" style="gap:6px;"><span>' + esc(T.dims) + '</span><div class="dims">' +
          ['L', 'A', 'H'].map(function (k, j) { return '<input class="input tnum" type="text" inputmode="numeric" aria-label="' + esc(T.dimNames[j]) + '" placeholder="' + esc(T.dimNames[j]) + '" data-f="' + k + '" data-id="' + l.id + '" value="' + esc(l[k]) + '">'; }).join('') +
        '</div></div>' +
        '<div class="g2"><div role="group" aria-label="' + esc(T.hangLabel) + '" class="field"><span>' + esc(T.hangQ) + '</span>' + seg('hang', T.hang, l.hang, ' data-id="' + l.id + '"') + '</div>' +
          '<label class="field">' + esc(T.faces) + '<input class="input" type="text" data-f="faces" data-id="' + l.id + '" value="' + esc(l.faces) + '" placeholder="' + esc(T.facesPh) + '"></label></div>' +
        (l.hang > 0 ? '<p role="note" class="warn">' + ico.warn + esc(T.warn) + '</p>' : '') +
      '</fieldset>';
    };
    var renderSteps = function () {
      stepsEl.innerHTML = T.steps.map(function (lb, i) {
        var n = i + 1, cur = n === q.step, done = n < q.step || q.step === 4, locked = (n > q.step && q.step !== 4) || q.step === 4;
        return '<li><button type="button" data-act="go" data-v="' + n + '"' + (cur ? ' aria-current="step"' : '') + (locked ? ' disabled' : '') + '><span class="q-mark tnum">' + (done && !cur ? '✓' : n) + '</span><span class="q-step-l">' + esc(lb) + '</span></button></li>';
      }).join('');
    };
    var renderMain = function () {
      var h = '';
      if (q.step === 1) {
        h = q.lines.map(lineHTML).join('') + '<button type="button" class="btn btn-line btn-add" data-act="add">' + ico.plus + esc(T.addLine) + '</button>';
      } else if (q.step === 2) {
        var r = state.ral;
        h = '<div class="q-color"><span class="q-color-sw" style="background:' + r.h + '"></span><div class="q-color-t"><span class="small-muted">' + esc(T.color) + '</span><span class="q-color-c tnum">RAL ' + esc(r.c) + '</span><span>' + esc(r.n) + '</span></div><a href="#colores" class="link-ink">' + esc(T.change) + '</a></div>' +
          '<label class="field" style="max-width:520px;">' + esc(T.otherColor) + '<input class="input" type="text" data-q="otherColor" value="' + val('otherColor') + '" placeholder="' + esc(T.otherColorPh) + '"></label>' +
          '<div class="g2"><div role="group" aria-label="' + esc(T.texL) + '" class="field"><span>' + esc(T.texL) + '</span>' + seg('tex', T.texOpts, texIdx()) + '</div>' +
          '<div role="group" aria-label="' + esc(T.glossL) + '" class="field"><span>' + esc(T.glossL) + '</span>' + seg('gloss', T.glossOpts, glossIdx()) + '</div></div>' +
          '<fieldset class="fs"><legend>' + esc(T.envQ) + '</legend><div class="envs">' + T.envs.map(function (e, i) {
            return '<button type="button" class="env" data-act="env" data-v="' + i + '" aria-pressed="' + (i === q.env) + '"><span class="env-h"><span>' + esc(e[0]) + '</span><span class="env-c tnum">' + esc(e[1]) + '</span></span><span class="env-d">' + esc(e[2]) + '</span></button>';
          }).join('') + '</div></fieldset>' +
          '<fieldset class="fs"><legend>' + esc(T.extrasL) + '</legend><div class="checks">' + T.extras.map(function (x, i) {
            var on = !!q.extras[i];
            return '<label class="check' + (on ? ' on' : '') + '"><input type="checkbox" data-act="extra" data-v="' + i + '"' + (on ? ' checked' : '') + '>' + esc(x) + '</label>';
          }).join('') + '</div></fieldset>';
      } else if (q.step === 3) {
        h = '<div class="g2"><label class="field">' + esc(T.when) + '<input class="input" type="date" data-q="when" value="' + val('when') + '"></label>' +
          '<div role="group" aria-label="' + esc(T.delL) + '" class="field"><span>' + esc(T.delL) + '</span>' + seg('del', T.del, q.del) + '</div></div>' +
          (q.del === 1 ? '<p style="margin-top:-8px; font-size:14px;"><mark class="note">' + esc(T.pickup) + '</mark></p>' : '') +
          '<div class="g2">' + T.contact.map(function (c, k) { return '<label class="field">' + esc(c[0]) + '<input class="input" type="' + c[1] + '" autocomplete="' + c[2] + '" data-q="c' + k + '" value="' + val('c' + k) + '"' + (c[1] === 'email' ? ' required' : '') + ' placeholder="' + esc(c[3]) + '"></label>'; }).join('') + '</div>' +
          '<label class="field">' + esc(T.notes) + '<textarea class="input" rows="4" data-q="notes" placeholder="' + esc(T.notesPh) + '">' + val('notes') + '</textarea></label>' + (q.err ? '<p role="alert" class="warn">' + ico.warn + esc(q.err) + '</p>' : '') +
          '<label class="rgpd"><input type="checkbox" data-act="rgpd"' + (q.rgpd ? ' checked' : '') + '><span>' + T.rgpd + '</span></label>';
      } else {
        h = '<div class="q-done" tabindex="-1" id="q-done"><span class="q-done-ico">' + ico.ok + '</span><div style="display:flex; flex-direction:column; gap:10px;"><h3>' + esc(fmt(T.doneTitle, { code: q.code || 'JP' })) + '</h3><p class="lead" style="max-width:none;">' + esc(fmt(T.doneLead, { d: deadline })) + '</p></div>' +
          '<ol>' + T.doneSteps.map(function (s, i) { return '<li><span class="tnum" style="font-weight:600;">' + (i + 1) + '</span><span>' + esc(s) + '</span></li>'; }).join('') + '</ol>' +
          '<div class="row-btns"><a href="' + ROOT + 'seguimiento.html" class="btn btn-ink">' + esc(T.doneTrack) + '</a><button type="button" class="btn btn-line" data-act="restart">' + esc(T.doneNew) + '</button></div></div>';
      }
      main.innerHTML = h;
    };
    var renderAside = function () {
      var tot = q.lines.reduce(function (a, l) { return a + (parseInt(l.qty, 10) || 0); }, 0);
      var exOn = T.extras.filter(function (x, i) { return q.extras[i]; });
      var env = T.envs[q.env], r = state.ral;
      var finish = T.texOpts[texIdx()] + ', ' + T.glossOpts[glossIdx()].toLowerCase();
      var nextDisabled = q.step === 3 && !q.rgpd;
      aside.innerHTML = '<h3 class="aside-h">' + esc(T.asideTitle) + '</h3>' +
        '<ul class="aside-lines">' + q.lines.map(function (l, i) { return '<li><span>' + esc(l.ref || fmt(T.ref, { n: i + 1 })) + '</span><span class="aside-dim tnum">' + esc(l.qty || '—') + ' · ' + esc(T.mats[l.mat]) + '</span></li>'; }).join('') + '</ul>' +
        '<p class="aside-tot"><span>' + esc(fmt(T.nRefs, { n: q.lines.length })) + '</span><span class="tnum">' + esc(fmt(T.nPcs, { n: tot })) + '</span></p>' +
        '<div class="aside-col"><span style="background:' + r.h + '"></span><span><span class="tnum" style="font-weight:600;">RAL ' + esc(r.c) + ' · ' + esc(r.n) + '</span><span class="aside-dim">' + esc(finish) + '</span></span></div>' +
        '<p class="aside-dim" style="font-size:15px;">' + esc(env[0]) + ' · ' + esc(env[1]) + '<span style="display:block; margin-top:4px;">' + esc(exOn.length ? T.extrasPre + exOn.join(', ').toLowerCase() : T.extrasNone) + '</span></p>' +
        '<div class="aside-dl"><span class="t">' + esc(T.deadlineL) + '</span><span class="v tnum">' + esc(deadline) + '</span><span class="t">' + T.cutoff + '</span></div>' +
        (q.step !== 4 ? '<div class="aside-nav"><button type="button" class="btn btn-acc" data-act="next"' + (nextDisabled ? ' disabled' : '') + '>' + esc(T.next[q.step - 1]) + '</button>' +
          (q.step > 1 ? '<button type="button" class="aside-back" data-act="back">' + esc(T.back) + '</button>' : '') +
          (nextDisabled ? '<span class="aside-need">' + esc(T.needRgpd) + '</span>' : '') + '</div>' : '');
    };
    var render = function () { renderSteps(); renderMain(); renderAside(); };
    var goStep = function (n) { q.step = n; render(); };
    var handle = function (e) {
      var b = e.target.closest('[data-act]'); if (!b) return;
      var act = b.getAttribute('data-act'), v = parseInt(b.getAttribute('data-v'), 10), id = parseInt(b.getAttribute('data-id'), 10);
      var line = q.lines.filter(function (l) { return l.id === id; })[0];
      if (act === 'go') goStep(v);
      else if (act === 'next' && q.step === 3) { send(); }
      else if (act === 'next') { goStep(q.step + 1); scrollToId('presupuesto'); if (q.step === 4) { var d = $('#q-done'); if (d) d.focus({ preventScroll: true }); } }
      else if (act === 'back') goStep(Math.max(1, q.step - 1));
      else if (act === 'restart') { q.rgpd = false; goStep(1); }
      else if (act === 'add') { q.lines.push(blank(q.nextId++)); render(); }
      else if (act === 'rm') { q.lines = q.lines.filter(function (l) { return l.id !== id; }); if (!q.lines.length) q.lines = [blank(q.nextId++)]; render(); }
      else if (act === 'unfile' && line) { line.file = ''; line.size = ''; line.fileObj = null; renderMain(); }
      else if (act === 'hang' && line) { line.hang = v; renderMain(); }
      else if (act === 'tex') { state.tex = v === 1 ? 'texturada' : 'lisa'; syncExplorer('#seg-tex', 'tex'); render(); }
      else if (act === 'gloss') { state.gloss = ['mate', 'satinado', 'brillante'][v]; syncExplorer('#seg-gloss', 'gloss'); render(); }
      else if (act === 'env') { q.env = v; render(); }
      else if (act === 'del') { q.del = v; renderMain(); }
    };
    var syncExplorer = function (sel, key) {
      $$(sel + ' button').forEach(function (x) { x.setAttribute('aria-pressed', x.getAttribute('data-' + key) === state[key] ? 'true' : 'false'); });
      if (window.JPR) window.JPR.paint();
    };

    /* Envío: formulario real a FormSubmit (formsubmit.co), con los planos adjuntos (máx. 10 MB en total).
       Vuelve a esta página con ?enviado=CÓDIGO y muestra el paso 4. */
    var MAXB = 10 * 1024 * 1024;
    var send = function () {
      var mail = (q.form.c3 || '').trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(mail)) { q.err = T.needEmail; renderMain(); var m = $('[data-q="c3"]'); if (m) m.focus(); return; }
      if (!q.rgpd) return;
      q.err = '';
      var d = new Date(), pad = function (n) { return ('0' + n).slice(-2); };
      q.code = 'JP-' + String(d.getFullYear()).slice(-2) + pad(d.getMonth() + 1) + pad(d.getDate()) + '-' + Math.floor(1000 + Math.random() * 9000);
      var files = q.lines.map(function (l) { return l.fileObj; }).filter(Boolean).concat(q.heroFiles || []);
      var total = files.reduce(function (a, f) { return a + f.size; }, 0), attach = total <= MAXB;
      var r = state.ral, env = T.envs[q.env];
      var lines = q.lines.map(function (l, i) {
        return (i + 1) + '. ' + (l.ref || '—') + ' · cant. ' + (l.qty || '—') + ' · ' + T.mats[l.mat] + (l.kg ? ' · ' + l.kg + ' kg' : '') +
          ((l.L || l.A || l.H) ? ' · ' + [l.L, l.A, l.H].map(function (x) { return x || '?'; }).join('×') + ' mm' : '') +
          ' · cuelgue: ' + (l.hang >= 0 ? T.hang[l.hang] : '—') + (l.faces ? ' · caras vistas: ' + l.faces : '') + (l.file ? ' · archivo: ' + l.file : '');
      }).join('\n');
      var fields = {
        '_subject': 'Solicitud de presupuesto ' + q.code + ' · ' + (q.form.c0 || mail),
        '_template': 'table', '_captcha': 'false',
        '_next': location.origin + location.pathname + '?enviado=' + q.code + '#presupuesto',
        'Código': q.code, 'Idioma de la web': JP.lang || '',
        'Empresa': q.form.c0 || '', 'CIF': q.form.c1 || '', 'Nombre': q.form.c2 || '', 'email': mail, 'Teléfono': q.form.c4 || '',
        'Referencias': lines,
        'Color': 'RAL ' + r.c + ' ' + (r.n || '') + (q.form.otherColor ? ' · otro: ' + q.form.otherColor : ''),
        'Acabado': T.texOpts[texIdx()] + ', ' + T.glossOpts[glossIdx()],
        'Ambiente': env[0] + ' (' + env[1] + ')',
        'Extras': T.extras.filter(function (x, i) { return q.extras[i]; }).join(', ') || '—',
        'Fecha deseada': q.form.when || '—', 'Entrega': T.del[q.del],
        'Notas': q.form.notes || '',
        'Plazo mostrado al cliente': deadline,
        'Adjuntos': attach ? (files.length ? files.length + ' archivo(s)' : 'ninguno') : 'NO adjuntados (superan 10 MB): ' + files.map(function (f) { return f.name; }).join(', ')
      };
      var f = document.createElement('form');
      f.method = 'POST'; f.action = 'https://formsubmit.co/' + (JP.form || ''); f.enctype = 'multipart/form-data'; f.style.display = 'none';
      Object.keys(fields).forEach(function (k) { var i = document.createElement(k === 'Referencias' || k === 'Notas' ? 'textarea' : 'input'); i.name = k; i.value = fields[k]; f.appendChild(i); });
      var hp = document.createElement('input'); hp.name = '_honey'; hp.value = ''; f.appendChild(hp);
      if (attach && files.length && window.DataTransfer) {
        files.forEach(function (file, n) { try { var dt = new DataTransfer(); dt.items.add(file); var fi = document.createElement('input'); fi.type = 'file'; fi.name = 'attachment' + (n ? n + 1 : ''); fi.files = dt.files; f.appendChild(fi); } catch (e) {} });
      }
      document.body.appendChild(f);
      var btn = $('[data-act="next"]', aside); if (btn) { btn.disabled = true; btn.textContent = T.sending; }
      f.submit();
    };
    try {
      var sent = new URLSearchParams(location.search).get('enviado');
      if (sent && /^JP-[\d-]+$/.test(sent)) { q.code = sent; q.step = 4; history.replaceState(null, '', location.pathname + '#presupuesto'); setTimeout(function () { scrollToId('presupuesto'); }, 60); }
    } catch (e) {}
    main.addEventListener('click', handle); aside.addEventListener('click', handle); stepsEl.addEventListener('click', handle);
    main.addEventListener('change', function (e) {
      var el = e.target, act = el.getAttribute('data-act');
      if (act === 'extra') { var i = parseInt(el.getAttribute('data-v'), 10); q.extras[i] = el.checked; el.parentNode.classList.toggle('on', el.checked); renderAside(); }
      else if (act === 'rgpd') { q.rgpd = el.checked; renderAside(); }
      else if (act === 'file') {
        var id = parseInt(el.getAttribute('data-id'), 10), l = q.lines.filter(function (x) { return x.id === id; })[0], f = el.files && el.files[0];
        if (l && f) { l.fileObj = f; l.file = f.name; l.size = f.size > 1048576 ? (f.size / 1048576).toFixed(1).replace('.', ',') + ' MB' : Math.max(1, Math.round(f.size / 1024)) + ' KB'; renderMain(); }
      }
      var fld = el.getAttribute('data-f');
      if (fld && fld === 'mat') { var ln = q.lines.filter(function (x) { return x.id === parseInt(el.getAttribute('data-id'), 10); })[0]; if (ln) { ln.mat = parseInt(el.value, 10); renderAside(); } }
    });
    main.addEventListener('input', function (e) {
      var qk = e.target.getAttribute('data-q'); if (qk) { q.form[qk] = e.target.value; return; }
      var el = e.target, fld = el.getAttribute('data-f'); if (!fld || fld === 'mat') return;
      var ln = q.lines.filter(function (x) { return x.id === parseInt(el.getAttribute('data-id'), 10); })[0];
      if (ln) { ln[fld] = el.value; if (fld === 'ref' || fld === 'qty') renderAside(); }
    });
    onRal(function () { if (q.step === 2) renderMain(); renderAside(); });
    window.JPQ = { goStep: goStep, sync: function () { if (q.step === 2) renderMain(); renderAside(); } };

    /* archivo del hero: va a la primera referencia */
    var hf = $('#hero-file'), hl = $('#hero-file-label'), drop = $('.upload-drop');
    var takeFiles = function (files) {
      if (!files || !files.length) return;
      var f = files[0];
      hl.textContent = files.length > 1 ? fmt(T.fileSel, { n: files.length }) : f.name;
      q.lines[0].file = f.name; q.lines[0].fileObj = f; q.heroFiles = Array.prototype.slice.call(files, 1);
      q.lines[0].size = f.size > 1048576 ? (f.size / 1048576).toFixed(1).replace('.', ',') + ' MB' : Math.max(1, Math.round(f.size / 1024)) + ' KB';
      q.step = 1; render();
    };
    if (hf) hf.addEventListener('change', function () { takeFiles(hf.files); });
    if (drop) {
      ['dragenter', 'dragover'].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add('drag'); }); });
      ['dragleave', 'drop'].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.remove('drag'); }); });
      drop.addEventListener('drop', function (e) { takeFiles(e.dataTransfer && e.dataTransfer.files); });
    }
    render();
  })();

  /* ---------- 5. carrusel de proveedores ---------- */
  (function marquee() {
    var track = $('#logo-track'), set = track && $('.logo-set', track);
    if (!set) return;
    var clone = set.cloneNode(true);
    clone.setAttribute('aria-hidden', 'true');
    $$('img', clone).forEach(function (im) { im.alt = ''; });
    track.appendChild(clone);
  })();
})();
