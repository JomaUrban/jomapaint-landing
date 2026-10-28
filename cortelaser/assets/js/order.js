/* Cortelaser · presupuesto guiado (formato del cotizador de paint.joma.es).
   Paso 1: piezas (archivo + análisis DXF en el navegador, material, espesor, cantidad).
   Paso 2: entrega y contacto. Envío a api/solicitud (multipart) → iniciativa en Odoo. */
(function () {
  'use strict';
  var C = window.CL || {}, T = C.t || {};
  var main = document.getElementById('q-main'), aside = document.getElementById('q-aside'), stepsEl = document.getElementById('q-steps');
  if (!main) return;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var esc = function (v) { return String(v == null ? '' : v).replace(/[&<>"']/g, function (ch) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]; }); };
  var fmt = function (s, o) { return String(s == null ? '' : s).replace(/\{(\w+)\}/g, function (m, k) { return o && o[k] != null ? o[k] : m; }); };
  var nf = function (n, d) { return Number(n).toLocaleString(C.lang === 'en' ? 'en-GB' : (C.lang || 'es') + '-ES', { maximumFractionDigits: d == null ? 1 : d, minimumFractionDigits: 0 }); };
  var ext = function (n) { return (String(n).split('.').pop() || '').toLowerCase(); };
  var num = function (v) { var x = parseFloat(String(v || '').replace(',', '.')); return isFinite(x) && x > 0 ? x : 0; };
  var reduce = false;
  try { reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}
  var scrollTo = function () { var s = document.getElementById('presupuesto'); if (s) s.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); };
  var MATS = C.mats || ['acero'], MAXT = C.maxT || 6, T0 = Date.now();

  var blank = function (id) { var x = window.CLX ? window.CLX.get() : null; return { id: id, ref: '', qty: '', mat: x ? x.mat : MATS[0], t: x ? String(x.t) : '', file: null, a: null }; };
  var q = { step: 1, lines: [blank(1)], nextId: 2, del: 0, paint: false, rgpd: false, form: {}, code: '', err: '', sending: false };

  /* ---------- plazo: 24 h laborables, oficina L–V 7:00–15:00 (hora de Madrid) ---------- */
  var deadline = (function () {
    var OPEN = 7, CLOSE = 15, H = 3600000, p = {}, now = new Date(), w;
    try { new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Madrid', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(now).forEach(function (x) { p[x.type] = x.value; }); } catch (e) {}
    w = p.year ? new Date(Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour % 24, +p.minute)) : new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours(), now.getMinutes()));
    var at = function (d, h) { return new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate(), h)); };
    var work = function (d) { var x = d.getUTCDay(); return x !== 0 && x !== 6; };
    if (w.getUTCMinutes()) w = new Date(at(w, w.getUTCHours()).getTime() + H);
    if (w.getUTCHours() >= CLOSE) w = at(new Date(w.getTime() + 24 * H), OPEN);
    else if (w.getUTCHours() < OPEN) w = at(w, OPEN);
    while (!work(w)) w = at(new Date(w.getTime() + 24 * H), OPEN);
    var d = new Date(w.getTime() + 24 * H);
    while (!work(d)) d = new Date(d.getTime() + 24 * H);
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

  /* ---------- análisis de cada pieza ---------- */
  var weight = function (l) { var t = num(l.t); if (!l.a || !l.a.ok || !t || !C.dens[l.mat]) return null; return l.a.area * t * C.dens[l.mat] * 1e-6; };
  var analysis = function (l) {
    if (!l.file) return '';
    var k = ext(l.file.name), msgs = [], stats = [], prev;
    if (k !== 'dxf') {
      prev = '<span>' + esc(k.toUpperCase()) + '<br>' + esc(T.no_preview) + '</span>';
      msgs.push(['', T[k === 'step' || k === 'stp' ? 'msg_step' : (k === 'dwg' ? 'msg_dwg' : 'msg_other')]]);
    } else if (!l.a) {
      prev = '<span>' + esc(T.analyzing) + '</span>';
    } else if (!l.a.ok) {
      prev = '<span>DXF</span>';
      msgs.push(['e', T[l.a.error === 'binary' ? 'msg_binary' : 'msg_empty']]);
    } else {
      var a = l.a, t = num(l.t), w = weight(l);
      prev = window.CLDXF.svg(a).replace('<svg', '<svg role="img" aria-label="' + esc(T.preview_aria) + '"');
      stats.push([T.s_size, nf(a.w) + ' × ' + nf(a.h) + ' mm'], [T.s_cut, nf(a.cut / 1000, 2) + ' m'], [T.s_contours, a.outers + ' + ' + a.holes], [T.s_weight, w === null ? T.s_weight_need : nf(w, w < 1 ? 2 : 1) + ' kg']);
      if (a.scaled) msgs.push(['', T.msg_units]);
      if (a.open) msgs.push(['e', fmt(T.msg_open, { n: a.open })]);
      if (a.outers > 1) msgs.push(['w', fmt(T.msg_multi, { n: a.outers })]);
      if (a.notes.text) msgs.push(['w', T.msg_text]);
      if (a.notes.dim) msgs.push(['', T.msg_dim]);
      if (a.notes.insert) msgs.push(['w', T.msg_insert]);
      if (a.notes.spline) msgs.push(['', T.msg_spline]);
      if (t && a.minHole !== null && a.minHole < (C.holeF[l.mat] || 1) * t) msgs.push(['w', fmt(T.msg_hole, { d: nf(a.minHole, 2), f: nf(C.holeF[l.mat] || 1), t: nf(t) })]);
      if (!a.open && a.outers === 1 && !a.notes.text && !a.notes.insert) msgs.push(['ok', T.msg_ok]);
    }
    return '<div class="cl-part"><div class="cl-prev">' + prev + '</div><div>' +
      (stats.length ? '<dl class="cl-stats">' + stats.map(function (s) { return '<div><dt>' + esc(s[0]) + '</dt><dd class="tnum">' + esc(s[1]) + '</dd></div>'; }).join('') + '</dl>' : '') +
      (msgs.length ? '<ul class="cl-msgs">' + msgs.map(function (m) { return '<li class="' + m[0] + '">' + esc(m[1]) + '</li>'; }).join('') + '</ul>' : '') + '</div></div>';
  };
  var setFile = function (l, f) {
    l.file = f; l.a = null;
    if (!l.ref) l.ref = f.name.replace(/\.[^.]+$/, '');
    if (ext(f.name) === 'dxf' && window.CLDXF) {
      var r = new FileReader();
      r.onload = function () { try { l.a = window.CLDXF.analyze(String(r.result)); } catch (e) { l.a = { ok: false, error: 'parse' }; } refreshLine(l); renderAside(); };
      r.readAsText(f);
    }
  };
  var addFiles = function (files) {
    var list = Array.prototype.slice.call(files || []);
    if (!list.length) return;
    list.forEach(function (f) {
      var l = q.lines.filter(function (x) { return !x.file; })[0];
      if (!l) { l = blank(q.nextId++); q.lines.push(l); }
      setFile(l, f);
    });
    q.step = 1; render();
  };

  /* ---------- pintado ---------- */
  var lineHTML = function (l, i) {
    var n = i + 1, t = num(l.t);
    var top = l.file
      ? '<span class="q-file">' + ico.file + '<span style="min-width:0;"><span class="q-file-n">' + esc(l.file.name) + '</span><span class="q-file-s">' + esc(nf(l.file.size / 1024, 0)) + ' KB</span></span><label class="q-unfile link-ink">' + esc(T.unfile) + '<input type="file" class="sr-file" data-act="file" data-id="' + l.id + '" accept=".dxf,.dwg,.step,.stp,.pdf,.png,.jpg,.jpeg,.zip"></label></span>'
      : '<label class="q-drop">' + ico.up + '<span>' + esc(T.addFile) + '</span><input type="file" class="sr-file" data-act="file" data-id="' + l.id + '" accept=".dxf,.dwg,.step,.stp,.pdf,.png,.jpg,.jpeg,.zip"></label>';
    return '<fieldset class="q-line" data-line="' + l.id + '"><legend>' + esc(fmt(T.ref, { n: n })) + '</legend>' +
      '<div class="q-line-top">' + top + '<button type="button" class="q-x" data-act="rm" data-id="' + l.id + '" aria-label="' + esc(fmt(T.remove, { n: n })) + '">' + ico.x + '</button></div>' +
      '<div data-an="' + l.id + '">' + analysis(l) + '</div>' +
      '<div class="g4">' +
        '<label class="field">' + esc(T.fRef) + '<input class="input" type="text" data-f="ref" data-id="' + l.id + '" value="' + esc(l.ref) + '" placeholder="' + esc(T.fRefPh) + '"></label>' +
        '<label class="field">' + esc(T.fQty) + '<input class="input tnum" type="number" min="1" inputmode="numeric" data-f="qty" data-id="' + l.id + '" value="' + esc(l.qty) + '"></label>' +
        '<label class="field">' + esc(T.fMat) + '<select class="input" data-f="mat" data-id="' + l.id + '">' + MATS.map(function (m) { return '<option value="' + m + '"' + (m === l.mat ? ' selected' : '') + '>' + esc((T.materials || {})[m] || m) + '</option>'; }).join('') + '</select></label>' +
        '<label class="field">' + esc(T.fT) + '<input class="input tnum" type="text" inputmode="decimal" list="cl-t" data-f="t" data-id="' + l.id + '" value="' + esc(l.t) + '" placeholder="' + esc(T.fTPh) + '"></label>' +
      '</div>' +
      '<p role="note" class="warn" data-thick="' + l.id + '"' + (t > MAXT ? '' : ' hidden') + '>' + ico.warn + esc(fmt(T.msg_thick, { max: nf(MAXT) })) + '</p>' +
    '</fieldset>';
  };
  var refreshLine = function (l) { var box = $('[data-an="' + l.id + '"]', main); if (box) box.innerHTML = analysis(l); var w = $('[data-thick="' + l.id + '"]', main); if (w) w.hidden = !(num(l.t) > MAXT); };
  var renderSteps = function () {
    stepsEl.innerHTML = (T.steps || []).map(function (lb, i) {
      var n = i + 1, cur = n === q.step, done = n < q.step || q.step === 3, locked = q.step === 3;
      return '<li><button type="button" data-act="go" data-v="' + n + '"' + (cur ? ' aria-current="step"' : '') + (locked ? ' disabled' : '') + '><span class="q-mark tnum">' + (done && !cur ? '✓' : n) + '</span><span class="q-step-l">' + esc(lb) + '</span></button></li>';
    }).join('');
  };
  var val = function (k) { return esc(q.form[k] || ''); };
  var renderMain = function () {
    var h = '';
    if (q.step === 1) {
      h = q.lines.map(lineHTML).join('') + '<button type="button" class="btn btn-line btn-add" data-act="add">' + ico.plus + esc(T.addLine) + '</button>' +
        '<datalist id="cl-t">' + [0.5, 0.8, 1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6].map(function (v) { return '<option value="' + nf(v) + '"></option>'; }).join('') + '</datalist>' +
        (q.err ? '<p role="alert" class="warn">' + ico.warn + esc(q.err) + '</p>' : '');
    } else if (q.step === 2) {
      h = '<div class="g2" style="align-items:start;"><div role="group" aria-label="' + esc(T.delL) + '" class="field"><span>' + esc(T.delL) + '</span><div class="seg">' +
          (T.del || []).map(function (o, i) { return '<button type="button" data-act="del" data-v="' + i + '" aria-pressed="' + (i === q.del) + '">' + esc(o) + '</button>'; }).join('') + '</div></div>' +
          '<label class="field">' + esc(T.when) + '<input class="input" type="date" data-q="when" value="' + val('when') + '"></label></div>' +
        (q.del > 0 ? '<label class="field" style="max-width:520px;">' + esc(T.zip) + '<input class="input" type="text" autocomplete="postal-code" data-q="zip" value="' + val('zip') + '" placeholder="' + esc(T.zipPh) + '"></label>' : '') +
        '<div class="g2">' + (T.contact || []).map(function (c, k) { return '<label class="field">' + esc(c[0]) + '<input class="input" type="' + c[1] + '" autocomplete="' + c[2] + '" data-q="c' + k + '" value="' + val('c' + k) + '"' + (c[1] === 'email' ? ' required' : '') + ' placeholder="' + esc(c[3]) + '"></label>'; }).join('') + '</div>' +
        '<label class="cl-paint"><input type="checkbox" data-act="paint"' + (q.paint ? ' checked' : '') + '><span><strong>' + esc(T.paint) + '</strong><span>' + esc(T.paintD) + '</span></span></label>' +
        '<label class="field">' + esc(T.notes) + '<textarea class="input" rows="4" data-q="notes" placeholder="' + esc(T.notesPh) + '">' + val('notes') + '</textarea></label>' +
        '<label class="cl-hp" aria-hidden="true">_honey<input type="text" tabindex="-1" autocomplete="off" data-q="_honey"></label>' +
        (q.err ? '<p role="alert" class="warn">' + ico.warn + esc(q.err) + '</p>' : '') +
        '<label class="rgpd"><input type="checkbox" data-act="rgpd"' + (q.rgpd ? ' checked' : '') + '><span>' + fmt(T.rgpd, { privacy: esc(C.privacy || '#') }) + '</span></label>';
    } else {
      h = '<div class="q-done" tabindex="-1" id="q-done"><span class="q-done-ico">' + ico.ok + '</span><div style="display:flex; flex-direction:column; gap:10px;"><h3>' + esc(fmt(T.doneTitle, { code: q.code })) + '</h3><p class="lead" style="max-width:none;">' + esc(fmt(T.doneLead, { d: deadline })) + '</p></div>' +
        '<ol>' + (T.doneSteps || []).map(function (s, i) { return '<li><span class="tnum" style="font-weight:600;">' + (i + 1) + '</span><span>' + esc(s) + '</span></li>'; }).join('') + '</ol>' +
        '<div class="row-btns"><button type="button" class="btn btn-line" data-act="restart">' + esc(T.doneNew) + '</button></div></div>';
    }
    main.innerHTML = h;
  };
  var renderAside = function () {
    var pcs = 0, kg = 0, known = true;
    q.lines.forEach(function (l) { var n = parseInt(l.qty, 10) || 0; pcs += n; var w = weight(l); if (w === null) { if (l.file || n) known = false; } else kg += w * (n || 1); });
    var nextDisabled = q.step === 2 && !q.rgpd;
    aside.innerHTML = '<h3 class="aside-h">' + esc(T.asideTitle) + '</h3>' +
      '<ul class="aside-lines">' + q.lines.map(function (l, i) { return '<li><span>' + esc(l.ref || fmt(T.ref, { n: i + 1 })) + '</span><span class="aside-dim tnum">' + esc(l.qty || '—') + ' · ' + esc((T.mat_short || {})[l.mat] || l.mat) + (num(l.t) ? ' ' + esc(nf(num(l.t))) + ' mm' : '') + '</span></li>'; }).join('') + '</ul>' +
      '<p class="aside-tot"><span>' + esc(fmt(T.nRefs, { n: q.lines.length })) + '</span><span class="tnum">' + esc(fmt(T.nPcs, { n: pcs })) + '</span></p>' +
      '<p class="aside-dim" style="font-size:15px;">' + esc(T.weight) + ': <span class="tnum" style="color:var(--paper); font-weight:600;">' + (kg ? (known ? '' : '≥ ') + esc(nf(kg, kg < 10 ? 2 : 1)) + ' kg' : '—') + '</span>' +
        (q.step >= 2 ? '<span style="display:block; margin-top:4px;">' + esc((T.del || [])[q.del] || '') + (q.paint ? ' · ' + esc(T.paint) : '') + '</span>' : '') + '</p>' +
      '<div class="aside-dl"><span class="t">' + esc(T.deadlineL) + '</span><span class="v tnum">' + esc(deadline) + '</span><span class="t">' + esc(T.cutoff) + '</span></div>' +
      (q.step !== 3 ? '<div class="aside-nav"><button type="button" class="btn btn-acc" data-act="next"' + (nextDisabled || q.sending ? ' disabled' : '') + '>' + esc(q.sending ? T.sending : (T.next || [])[q.step - 1]) + '</button>' +
        (q.step > 1 ? '<button type="button" class="aside-back" data-act="back">' + esc(T.back) + '</button>' : '') +
        (nextDisabled ? '<span class="aside-need">' + esc(T.needRgpd) + '</span>' : '') + '</div>' : '');
  };
  var render = function () { renderSteps(); renderMain(); renderAside(); };
  var goStep = function (n) { q.err = ''; q.step = n; render(); };
  var line = function (id) { return q.lines.filter(function (l) { return l.id === id; })[0]; };

  /* ---------- eventos ---------- */
  var onClick = function (e) {
    var b = e.target.closest('[data-act]'); if (!b || b.tagName === 'INPUT') return;
    var act = b.getAttribute('data-act'), v = parseInt(b.getAttribute('data-v'), 10), id = parseInt(b.getAttribute('data-id'), 10);
    if (act === 'go') goStep(v);
    else if (act === 'next' && q.step === 1) { if (!q.lines.some(function (l) { return l.file; })) { q.err = T.needFile; renderMain(); return; } goStep(2); scrollTo(); }
    else if (act === 'next' && q.step === 2) send();
    else if (act === 'back') goStep(1);
    else if (act === 'restart') { q = { step: 1, lines: [blank(1)], nextId: 2, del: 0, paint: false, rgpd: false, form: {}, code: '', err: '', sending: false }; render(); }
    else if (act === 'add') { q.lines.push(blank(q.nextId++)); render(); }
    else if (act === 'rm') { q.lines = q.lines.filter(function (l) { return l.id !== id; }); if (!q.lines.length) q.lines = [blank(q.nextId++)]; render(); }
    else if (act === 'del') { q.del = v; renderMain(); renderAside(); }
  };
  main.addEventListener('click', onClick); aside.addEventListener('click', onClick); stepsEl.addEventListener('click', onClick);
  main.addEventListener('change', function (e) {
    var t = e.target, act = t.getAttribute('data-act');
    if (act === 'file' && t.files && t.files[0]) { var l = line(parseInt(t.getAttribute('data-id'), 10)); if (l) { setFile(l, t.files[0]); if (t.files.length > 1) addFiles(Array.prototype.slice.call(t.files, 1)); else render(); } }
    else if (act === 'paint') { q.paint = t.checked; renderAside(); }
    else if (act === 'rgpd') { q.rgpd = t.checked; renderAside(); }
  });
  main.addEventListener('input', function (e) {
    var t = e.target, f = t.getAttribute('data-f'), k = t.getAttribute('data-q');
    if (f) { var l = line(parseInt(t.getAttribute('data-id'), 10)); if (!l) return; l[f] = t.value; if (f === 't' || f === 'mat') refreshLine(l); renderAside(); }
    else if (k) q.form[k] = t.value;
  });
  main.addEventListener('change', function (e) { var t = e.target; if (t.getAttribute('data-f') === 'mat') { var l = line(parseInt(t.getAttribute('data-id'), 10)); if (l) { l.mat = t.value; refreshLine(l); renderAside(); } } });
  ['dragenter', 'dragover'].forEach(function (ev) { main.addEventListener(ev, function (e) { if (q.step === 1) e.preventDefault(); }); });
  main.addEventListener('drop', function (e) { if (q.step !== 1) return; e.preventDefault(); if (e.dataTransfer && e.dataTransfer.files) addFiles(e.dataTransfer.files); });

  /* Subida desde el hero: los archivos pasan al paso 1 */
  var hero = document.getElementById('hero-file'), heroDrop = document.getElementById('hero-drop'), heroLabel = document.getElementById('hero-file-label');
  var fromHero = function (files) { if (!files || !files.length) return; addFiles(files); if (heroLabel) heroLabel.textContent = fmt(T.heroFiles, { n: files.length }); scrollTo(); };
  if (hero) hero.addEventListener('change', function () { fromHero(hero.files); hero.value = ''; });
  if (heroDrop) {
    ['dragenter', 'dragover'].forEach(function (ev) { heroDrop.addEventListener(ev, function (e) { e.preventDefault(); }); });
    heroDrop.addEventListener('drop', function (e) { e.preventDefault(); if (e.dataTransfer) fromHero(e.dataTransfer.files); });
  }
  window.CLQ = { preset: function (m, t) { q.lines.forEach(function (l) { if (!l.file && !l.qty) { l.mat = m; l.t = String(t); } }); q.step = 1; render(); } };

  /* ---------- envío ---------- */
  var describe = function (l, i) {
    var a = l.a, out = [fmt(T.ref, { n: i + 1 }) + ': ' + (l.ref || '—') + (l.file ? ' (' + l.file.name + ')' : '')];
    out.push(T.fMat + ': ' + ((T.materials || {})[l.mat] || l.mat) + (l.t ? ' · ' + l.t + ' mm' : '') + ' · ' + T.fQty + ': ' + (l.qty || '—'));
    if (a && a.ok) out.push(T.s_size + ': ' + a.w.toFixed(1) + ' × ' + a.h.toFixed(1) + ' mm · ' + T.s_cut + ': ' + (a.cut / 1000).toFixed(2) + ' m · ' + T.s_contours + ': ' + a.outers + ' + ' + a.holes + (a.open ? ' · ' + fmt(T.msg_open, { n: a.open }) : ''));
    var w = weight(l); if (w !== null) out.push(T.s_weight + ': ' + w.toFixed(2) + ' kg/ud');
    return out.join('\n');
  };
  var send = function () {
    var mail = String(q.form.c3 || '').trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(mail)) { q.err = T.needEmail; renderMain(); var m = $('[data-q="c3"]', main); if (m) m.focus(); return; }
    if (!q.rgpd || q.sending) return;
    var files = q.lines.map(function (l) { return l.file; }).filter(Boolean);
    var bytes = files.reduce(function (s, f) { return s + f.size; }, 0);
    if (bytes > (C.maxMb || 10) * 1048576) { q.err = fmt(T.err_size, { mb: C.maxMb }); renderMain(); return; }
    var d = new Date(), pad = function (n) { return ('0' + n).slice(-2); };
    q.code = (C.prefix || 'CL') + '-' + String(d.getFullYear()).slice(-2) + pad(d.getMonth() + 1) + pad(d.getDate()) + '-' + Math.floor(1000 + Math.random() * 9000);
    var fd = new FormData();
    (T.contact || []).forEach(function (c, k) { fd.append(c[4], q.form['c' + k] || ''); });
    fd.set('email', mail);
    fd.append('Código', q.code);
    fd.append('Idioma', C.lang || '');
    fd.append('Piezas', q.lines.map(describe).join('\n\n'));
    fd.append('Entrega', ((T.del || [])[q.del] || '') + (q.del > 0 && q.form.zip ? ' · ' + q.form.zip : ''));
    fd.append('Fecha deseada', q.form.when || '—');
    fd.append('Pintura', q.paint ? 'SÍ: quiere también pintarlas en polvo (coordinar con pintura)' : 'no');
    fd.append('Observaciones', q.form.notes || '');
    fd.append('Plazo mostrado al cliente', deadline);
    fd.append('Privacidad', 'aceptada');
    fd.append('_subject', fmt(T.subject, { c: q.code, n: q.lines.length }) + (q.paint ? ' · + pintura' : ''));
    fd.append('_honey', q.form._honey || '');
    fd.append('_t', String(T0));
    files.forEach(function (f, i) { fd.append('archivo' + (i + 1), f, f.name); });
    q.sending = true; q.err = ''; renderAside();
    fetch(C.api, { method: 'POST', body: fd }).then(function (r) { return r.json().then(function (j) { return [r.ok, j]; }); })
      .then(function (res) {
        if (!res[0] || !res[1].ok) throw new Error(res[1].error || 'http');
        if (res[1].code) q.code = res[1].code;
        q.sending = false; q.step = 3; render(); scrollTo();
        var dn = $('#q-done'); if (dn) dn.focus({ preventScroll: true });
      })
      .catch(function () { q.sending = false; q.err = fmt(T.err_send, { email: C.email || '', phone: C.phone || '' }); render(); });
  };
  render();
})();
