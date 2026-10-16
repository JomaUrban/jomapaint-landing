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
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var W = 1, H = 1, P = [], t = 0, visible = true, mouse = null, sprite = null, color = '#F7B500';
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
      var n = Math.round(Math.min(1150, Math.max(240, (W * H) / 1250)));
      while (P.length < n) P.push(spawn({}, true));
      P.length = n;
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
    resize();
    if (window.ResizeObserver) new ResizeObserver(resize).observe(root); else window.addEventListener('resize', resize);
    if (window.IntersectionObserver) new IntersectionObserver(function (es) { visible = es[0] ? es[0].isIntersecting : true; }).observe(root);
    root.addEventListener('pointermove', function (e) { var r = root.getBoundingClientRect(); mouse = { x: e.clientX - r.left, y: e.clientY - r.top }; });
    root.addEventListener('pointerleave', function () { mouse = null; });
    if (reduce) { for (var n = 0; n < 220; n++) step(); draw(false); return; }
    (function loop() { if (visible && !document.hidden) { step(); draw(true); } requestAnimationFrame(loop); })();
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
        return '<button type="button" class="sw tnum" data-c="' + x.c + '" aria-pressed="' + on + '" aria-label="' + esc(lbl) + '" title="' + esc(lbl) + '" style="background:' + (x.p ? sheen : '') + x.h + ';color:' + (lum(x.h) > 0.36 ? 'rgba(26,26,26,0.82)' : 'rgba(255,255,255,0.9)') + '">' + x.c + (x.l ? '<span class="lum"></span>' : '') + '</button>';
      }).join('');
      empty.hidden = list.length > 0;
      if (!list.length) empty.textContent = fmt(T.empty, { q: q });
      count.textContent = fmt(T.count, { n: list.length });
    };
    var G = { mate: { sp: [0.04, 0.42, 0.86], peak: 0.05, glint: 0 }, satinado: { sp: [0.18, 0.38, 0.6], peak: 0.17, glint: 0.06 }, brillante: { sp: [0.3, 0.355, 0.41], peak: 0.62, glint: 0.42 } };
    var FAMIDX = { '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9 };
    var paintPlate = function () {
      var sel = RAL.filter(function (x) { return x.c === state.ral.c; })[0] || RAL[0];
      var base = sel.h, L0 = lum(base), light = L0 < 0.05;
      var solid = light ? mix(base, '#FAF9F6', 0.86) : mix(base, '#141414', 0.64);
      var field = $('#ral-field');
      field.style.background = 'radial-gradient(70% 55% at 50% 38%, rgba(255,255,255,' + (light ? '0.5' : '0.10') + '), rgba(255,255,255,0) 70%), ' + solid;
      field.style.color = light ? '#1A1A1A' : '#FAF9F6';
      $('#f0').setAttribute('stop-color', mix(base, '#FFFFFF', 0.1));
      $('#f1').setAttribute('stop-color', base);
      $('#f2').setAttribute('stop-color', mix(base, '#000000', 0.22));
      $('#r-top').setAttribute('fill', mix(base, '#FFFFFF', 0.34));
      $('#r-side').setAttribute('fill', mix(base, '#000000', 0.42));
      $('#r-hole').setAttribute('fill', solid);
      var g = G[state.gloss], k = state.tex === 'texturada' ? 0.55 : 1;
      $('#s1').setAttribute('offset', g.sp[0]); $('#s2').setAttribute('offset', g.sp[1]); $('#s3').setAttribute('offset', g.sp[2]);
      $('#s2').setAttribute('stop-opacity', (g.peak * k).toFixed(3));
      $('#r-glint').setAttribute('opacity', (g.glint * k).toFixed(3));
      $('#r-peel').setAttribute('opacity', state.tex === 'lisa' ? 0.16 : 0);
      $('#r-grain').setAttribute('opacity', state.tex === 'texturada' ? 0.6 : 0);
      $('#r-pearl').setAttribute('opacity', sel.p ? 0.5 : 0);
      $('#ral-code').textContent = sel.c;
      $('#ral-name').textContent = ralName(sel);
      $('#ral-hex').textContent = sel.h.toUpperCase();
      $('#ral-fam').textContent = (famNames[FAMIDX[sel.f]] || '') + (sel.p ? ' · ' + T.pearl : '') + (sel.l ? ' · ' + T.lum : '');
      $('#ral-sticker').textContent = 'RAL ' + sel.c + ' · ' + T.texSticker[state.tex] + ' · ' + T.glossSticker[state.gloss];
      $('#ral-svg').setAttribute('aria-label', fmt(T.svg, { c: sel.c, n: ralName(sel), tex: T.tex[state.tex], gloss: T.gloss[state.gloss] }));
      $$('.ral-current').forEach(function (e) { e.textContent = sel.c; });
    };
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
    paintGrid(); paintPlate();
  })();

  /* ---------- 4. cotizador ---------- */
  (function quote() {
    var main = $('#q-main'), aside = $('#q-aside'), stepsEl = $('#q-steps');
    if (!main) return;
    var S = T.sample || [];
    var q = {
      step: 1, env: 1, del: 0, rgpd: false, extras: {}, nextId: 3,
      lines: [
        { id: 1, ref: S[0] ? S[0][0] : 'A', qty: 120, mat: 0, kg: '0,35', L: '120', A: '80', H: '60', hang: 0, faces: S[0] ? S[0][3] : '', file: S[0] ? S[0][1] : '', size: S[0] ? S[0][2] : '' },
        { id: 2, ref: S[1] ? S[1][0] : 'B', qty: 6, mat: 1, kg: '38', L: '2400', A: '1200', H: '80', hang: 2, faces: '', file: S[1] ? S[1][1] : '', size: S[1] ? S[1][2] : '' }
      ]
    };
    q.extras[T.extras.length - 1] = true;
    var deadline = (function () {
      var d = new Date(Date.now() + 24 * 3600 * 1000);
      var dow = function (x) { try { return new Intl.DateTimeFormat('en-GB', { weekday: 'short', timeZone: 'Europe/Madrid' }).format(x); } catch (e) { return ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][x.getDay()]; } };
      while (dow(d) === 'Sat' || dow(d) === 'Sun') d = new Date(d.getTime() + 24 * 3600 * 1000);
      try {
        var pp = {};
        new Intl.DateTimeFormat(T.locale || 'es-ES', { weekday: 'short', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Europe/Madrid' }).formatToParts(d).forEach(function (x) { pp[x.type] = x.value; });
        return (pp.weekday || '').replace('.', '') + ' ' + pp.day + ' ' + (pp.month || '').replace('.', '') + ' · ' + pp.hour + ':' + pp.minute;
      } catch (e) { return d.toLocaleString(); }
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
        ? '<span class="q-file">' + ico.file + '<span style="min-width:0;"><span class="q-file-n">' + esc(l.file) + '</span><span class="q-file-s">' + esc(l.size) + '</span></span></span>'
        : '<label class="q-drop">' + ico.up + '<span>' + esc(T.addFile) + '</span><input type="file" class="sr-file" data-act="file" data-id="' + l.id + '"></label>';
      return '<fieldset class="q-line"><legend>' + esc(fmt(T.ref, { n: n })) + '</legend>' +
        '<div class="q-line-top">' + top + '<button type="button" class="q-x" data-act="rm" data-id="' + l.id + '" aria-label="' + esc(fmt(T.remove, { n: n })) + '">' + ico.x + '</button></div>' +
        '<div class="g4">' +
          '<label class="field">' + esc(T.fRef) + '<input class="input" type="text" data-f="ref" data-id="' + l.id + '" value="' + esc(l.ref) + '"></label>' +
          '<label class="field">' + esc(T.fQty) + '<input class="input tnum" type="number" min="1" inputmode="numeric" data-f="qty" data-id="' + l.id + '" value="' + esc(l.qty) + '"></label>' +
          '<label class="field">' + esc(T.fMat) + '<select class="input" data-f="mat" data-id="' + l.id + '">' + T.mats.map(function (m, k) { return '<option value="' + k + '"' + (k === l.mat ? ' selected' : '') + '>' + esc(m) + '</option>'; }).join('') + '</select></label>' +
          '<label class="field">' + esc(T.fKg) + '<input class="input tnum" type="text" inputmode="decimal" data-f="kg" data-id="' + l.id + '" value="' + esc(l.kg) + '" placeholder="' + esc(T.fKgPh) + '"></label>' +
        '</div>' +
        '<div role="group" aria-label="' + esc(fmt(T.dimsLabel, { n: n })) + '" class="field" style="gap:6px;"><span>' + esc(T.dims) + '</span><div class="dims">' +
          ['L', 'A', 'H'].map(function (k, j) { return '<input class="input tnum" type="text" inputmode="numeric" aria-label="' + esc(T.dimNames[j]) + '" placeholder="' + esc(T.dimNames[j]) + '" data-f="' + k + '" data-id="' + l.id + '" value="' + esc(l[k]) + '">'; }).join('') +
        '</div></div>' +
        '<div class="g2"><div role="group" aria-label="' + esc(T.hangLabel) + '" class="field"><span>' + esc(T.hangQ) + '</span>' + seg('hang', T.hang, l.hang, ' data-id="' + l.id + '"') + '</div>' +
          '<label class="field">' + esc(T.faces) + '<input class="input" type="text" data-f="faces" data-id="' + l.id + '" value="' + esc(l.faces) + '" placeholder="' + esc(T.facesPh) + '"></label></div>' +
        (l.hang !== 0 ? '<p role="note" class="warn">' + ico.warn + esc(T.warn) + '</p>' : '') +
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
          '<label class="field" style="max-width:520px;">' + esc(T.otherColor) + '<input class="input" type="text" placeholder="' + esc(T.otherColorPh) + '"></label>' +
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
        h = '<div class="g2"><label class="field">' + esc(T.when) + '<input class="input" type="date"></label>' +
          '<div role="group" aria-label="' + esc(T.delL) + '" class="field"><span>' + esc(T.delL) + '</span>' + seg('del', T.del, q.del) + '</div></div>' +
          (q.del === 1 ? '<p style="margin-top:-8px; font-size:14px;"><mark class="note">' + esc(T.pickup) + '</mark></p>' : '') +
          '<div class="g2">' + T.contact.map(function (c) { return '<label class="field">' + esc(c[0]) + '<input class="input" type="' + c[1] + '" autocomplete="' + c[2] + '" placeholder="' + esc(c[3]) + '"></label>'; }).join('') + '</div>' +
          '<label class="field">' + esc(T.notes) + '<textarea class="input" rows="4" placeholder="' + esc(T.notesPh) + '"></textarea></label>' +
          '<label class="rgpd"><input type="checkbox" data-act="rgpd"' + (q.rgpd ? ' checked' : '') + '><span>' + T.rgpd + '</span></label>';
      } else {
        h = '<div class="q-done" tabindex="-1" id="q-done"><span class="q-done-ico">' + ico.ok + '</span><div style="display:flex; flex-direction:column; gap:10px;"><h3>' + esc(fmt(T.doneTitle, { code: 'JP-26-0001' })) + '</h3><p class="lead" style="max-width:none;">' + esc(fmt(T.doneLead, { d: deadline })) + '</p></div>' +
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
        '<ul class="aside-lines">' + q.lines.map(function (l) { return '<li><span>' + esc(l.ref) + '</span><span class="aside-dim tnum">' + esc(l.qty) + ' · ' + esc(T.mats[l.mat]) + '</span></li>'; }).join('') + '</ul>' +
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
      else if (act === 'next') { if (q.step === 3 && !q.rgpd) return; goStep(q.step + 1); scrollToId('presupuesto'); if (q.step === 4) { var d = $('#q-done'); if (d) d.focus({ preventScroll: true }); } }
      else if (act === 'back') goStep(Math.max(1, q.step - 1));
      else if (act === 'restart') { q.rgpd = false; goStep(1); }
      else if (act === 'add') { q.lines.push({ id: q.nextId++, ref: fmt(T.ref, { n: q.lines.length + 1 }), qty: 1, mat: 0, kg: '', L: '', A: '', H: '', hang: 2, faces: '', file: '', size: '' }); render(); }
      else if (act === 'rm') { if (q.lines.length > 1) { q.lines = q.lines.filter(function (l) { return l.id !== id; }); render(); } }
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
    main.addEventListener('click', handle); aside.addEventListener('click', handle); stepsEl.addEventListener('click', handle);
    main.addEventListener('change', function (e) {
      var el = e.target, act = el.getAttribute('data-act');
      if (act === 'extra') { var i = parseInt(el.getAttribute('data-v'), 10); q.extras[i] = el.checked; el.parentNode.classList.toggle('on', el.checked); renderAside(); }
      else if (act === 'rgpd') { q.rgpd = el.checked; renderAside(); }
      else if (act === 'file') {
        var id = parseInt(el.getAttribute('data-id'), 10), l = q.lines.filter(function (x) { return x.id === id; })[0], f = el.files && el.files[0];
        if (l && f) { l.file = f.name; l.size = f.size > 1048576 ? (f.size / 1048576).toFixed(1).replace('.', ',') + ' MB' : Math.max(1, Math.round(f.size / 1024)) + ' KB'; renderMain(); }
      }
      var fld = el.getAttribute('data-f');
      if (fld && fld === 'mat') { var ln = q.lines.filter(function (x) { return x.id === parseInt(el.getAttribute('data-id'), 10); })[0]; if (ln) { ln.mat = parseInt(el.value, 10); renderAside(); } }
    });
    main.addEventListener('input', function (e) {
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
      q.lines[0].file = f.name;
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
