/* Cortelaser · portada. Sin dependencias.
   1. Chispas en el hero   2. Pasos del proceso   3. Explorador de materiales */
(function () {
  'use strict';
  var C = window.CL || {}, T = C.t || {};
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = false;
  try { reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}
  var nf = function (n, d) { return Number(n).toLocaleString(C.lang === 'en' ? 'en-GB' : (C.lang || 'es') + '-ES', { maximumFractionDigits: d == null ? 1 : d, minimumFractionDigits: 0 }); };

  /* ---------- 1. chispas: salen de un punto de corte y caen con gravedad ---------- */
  (function sparks() {
    var cv = $('#sparks'), root = $('.hero');
    if (!cv || !root || !cv.getContext) return;
    var ctx = cv.getContext('2d'), dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    var W = 1, H = 1, P = [], visible = true, rnd = Math.random, n = 0;
    var origin = function () { return W < 760 ? { x: W * 0.86, y: H * 0.14 } : { x: W * 0.72, y: H * 0.42 }; };
    var spawn = function (p) {
      var o = origin(), a = -Math.PI / 2 + (rnd() - 0.5) * 2.6, v = 2 + rnd() * 7;
      p.x = o.x + (rnd() - 0.5) * 8; p.y = o.y + (rnd() - 0.5) * 4;
      p.vx = Math.cos(a) * v * (rnd() < 0.5 ? 1 : 0.6); p.vy = Math.sin(a) * v * 0.6 + 1.5; p.life = 0; p.max = 40 + rnd() * 70; p.w = 0.6 + rnd() * 1.4;
      return p;
    };
    var resize = function () {
      W = Math.max(1, root.clientWidth); H = Math.max(1, root.clientHeight);
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      n = W < 760 ? 90 : 200;
      while (P.length < n) { var p = spawn({}); p.life = Math.floor(rnd() * p.max); P.push(p); }
      P.length = n;
    };
    var step = function () {
      for (var i = 0; i < P.length; i++) {
        var p = P[i]; p.life++;
        p.vy += 0.16; p.vx *= 0.99; p.px = p.x; p.py = p.y; p.x += p.vx; p.y += p.vy;
        if (p.life > p.max || p.y > H + 20 || p.x < -20 || p.x > W + 20) spawn(p);
      }
    };
    var draw = function () {
      ctx.globalCompositeOperation = 'destination-out'; ctx.fillStyle = 'rgba(0,0,0,0.35)'; ctx.fillRect(0, 0, W, H);
      ctx.globalCompositeOperation = 'lighter';
      for (var i = 0; i < P.length; i++) {
        var p = P[i], k = 1 - p.life / p.max; if (k <= 0 || p.px == null) continue;
        ctx.strokeStyle = 'rgba(255,' + Math.round(150 + 90 * k) + ',' + Math.round(60 * k) + ',' + (0.85 * k).toFixed(3) + ')';
        ctx.lineWidth = p.w; ctx.beginPath(); ctx.moveTo(p.px, p.py); ctx.lineTo(p.x, p.y); ctx.stroke();
      }
      var o = origin(), g = ctx.createRadialGradient(o.x, o.y, 0, o.x, o.y, 46);
      g.addColorStop(0, 'rgba(255,240,210,0.55)'); g.addColorStop(0.3, 'rgba(255,120,30,0.22)'); g.addColorStop(1, 'rgba(255,106,19,0)');
      ctx.fillStyle = g; ctx.fillRect(o.x - 46, o.y - 46, 92, 92);
    };
    var start = function () {
      resize();
      if (window.ResizeObserver) new ResizeObserver(resize).observe(root); else window.addEventListener('resize', resize);
      if (window.IntersectionObserver) new IntersectionObserver(function (es) { visible = es[0] ? es[0].isIntersecting : true; }).observe(root);
      if (reduce) return;
      var last = 0, slow = 0;
      (function loop(now) {
        if (visible && !document.hidden) {
          if (last && now - last > 40) slow++; else if (slow > 0) slow -= 0.5;
          last = now;
          if (slow > 40) { ctx.clearRect(0, 0, W, H); return; } /* equipo lento: se para */
          step(); draw();
        } else last = 0;
        requestAnimationFrame(loop);
      })(performance.now());
    };
    var idle = function () { if (window.requestIdleCallback) window.requestIdleCallback(start, { timeout: 2000 }); else setTimeout(start, 300); };
    if (document.readyState === 'complete') idle(); else window.addEventListener('load', idle);
  })();

  /* ---------- 2. pasos del proceso ---------- */
  (function process() {
    var tabs = $$('#stations [role="tab"]'), panels = $$('.st-panel'), zones = $$('#zones > div');
    var photos = $$('#st-photos img'), cap = $('#st-cap'), head = $('#head'), beam = $('#beam'), cut = $('#cut'), fx = $('#fx');
    if (!tabs.length) return;
    var caps = tabs.map(function (b, i) { return (panels[i] && panels[i].querySelector('h3') || b).textContent; });
    try { caps = JSON.parse(cap.getAttribute('data-caps') || 'null') || caps; } catch (e) {}
    var st = 0, manual = false;
    var render = function (focus) {
      tabs.forEach(function (b, i) { var on = i === st; b.setAttribute('aria-selected', on ? 'true' : 'false'); b.tabIndex = on ? 0 : -1; });
      panels.forEach(function (p, i) { p.hidden = i !== st; });
      zones.forEach(function (z, i) { z.classList.toggle('on', i === st); z.classList.toggle('glow', i === st && i === 2); z.style.background = i === st ? (i === 2 ? 'radial-gradient(80% 80% at 50% 60%, rgba(255,106,19,0.28), transparent 72%)' : 'radial-gradient(80% 70% at 50% 50%, rgba(250,249,246,0.08), transparent 72%)') : 'transparent'; });
      photos.forEach(function (im, i) { im.classList.toggle('on', i === st); });
      if (cap) cap.textContent = caps[st] || '';
      if (head) head.style.left = (st * 20 + 10) + '%';
      if (beam) beam.setAttribute('opacity', st === 2 ? '1' : '0');
      if (cut) cut.setAttribute('width', String(Math.min(1000, st >= 2 ? (st * 200 + 100) : 0)));
      if (fx) {
        var h = '';
        if (st === 2 && !reduce) for (var k = 0; k < 16; k++) h += '<span style="position:absolute;left:31px;top:108px;width:2px;height:2px;border-radius:50%;background:#FFB27A;box-shadow:0 0 6px #FF6A13;--dx:' + (((k * 37) % 90) - 45) + 'px;--dy:' + (20 + ((k * 23) % 50)) + 'px;animation:clSpark .7s ease-out ' + ((k * 0.09) % 0.7).toFixed(2) + 's infinite;"></span>';
        fx.innerHTML = h;
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
    var sec = $('#proceso'), inView = true;
    if (window.IntersectionObserver && sec) new IntersectionObserver(function (es) { inView = es[0].isIntersecting; }, { threshold: 0.25 }).observe(sec);
    if (!reduce) setInterval(function () { if (!manual && inView && !document.hidden) { st = (st + 1) % tabs.length; render(false); } }, 4200);
    render(false);
  })();

  /* ---------- 3. explorador de materiales ---------- */
  (function explorer() {
    var field = $('#mx-field'), range = $('#mx-range');
    if (!field || !range) return;
    var mats = $$('#mx-mats button'), face = $('#mx-face');
    var state = { mat: (C.mats || ['acero'])[0], t: parseFloat(range.value) || 2 };
    var paint = function () {
      var m = state.mat, t = state.t, d = (C.dens || {})[m] || 7.85, f = (C.holeF || {})[m] || 1;
      field.setAttribute('data-mat', m);
      mats.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-mat') === m ? 'true' : 'false'); });
      $('#mx-fam').textContent = (T.mat_short || {})[m] || m;
      $('#mx-name').textContent = (T.materials || {})[m] || m;
      $('#mx-grades').textContent = ((C.grades || {})[m] || []).join(' · ');
      $('#mx-t').textContent = nf(t, 1);
      $('#mx-t2').textContent = nf(t, 1) + ' mm';
      $('#mx-kgm2').textContent = nf(d * t, 2) + ' kg';
      $('#mx-sheet').textContent = nf(d * t * 4.5, 1) + ' kg';
      $('#mx-hole').textContent = 'Ø ' + nf(Math.max(f * t, 0.5), 1) + ' mm';
      $('#mx-dens').textContent = nf(d, 2) + ' kg/dm³';
      var more = $('#mx-more'); if (more && C.matHref && C.matHref[m]) more.setAttribute('href', C.matHref[m]);
      if (face) {
        var n = Math.max(1, Math.round(t * 2.2)), sh = [];
        for (var i = 1; i <= n; i++) sh.push('0 ' + i + 'px 0 rgba(' + (i === n ? '20,20,20' : '120,126,132') + ',1)');
        face.style.boxShadow = sh.join(',') + ', 0 ' + (n + 18) + 'px 30px rgba(0,0,0,0.45)';
      }
    };
    mats.forEach(function (b) { b.addEventListener('click', function () { state.mat = b.getAttribute('data-mat'); paint(); }); });
    range.addEventListener('input', function () { state.t = parseFloat(range.value) || 2; paint(); });
    var use = $('#mx-use');
    if (use) use.addEventListener('click', function () {
      if (window.CLQ) window.CLQ.preset(state.mat, state.t);
      var q = document.getElementById('presupuesto'); if (q) q.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    });
    window.CLX = { get: function () { return state; } };
    paint();
  })();
})();
