/* Cortelaser · calculadoras de peso de chapa y desarrollo de plegado. */
(function () {
  'use strict';
  var C = window.CL || {};
  var num = function (el) { return parseFloat(String(el.value).replace(',', '.')); };
  var fmt = function (n, d) { return isFinite(n) ? Number(n).toLocaleString(C.lang === 'en' ? 'en-GB' : C.lang + '-ES', { maximumFractionDigits: d, minimumFractionDigits: d }) : '—'; };

  var pw = document.getElementById('calc-peso');
  if (pw) {
    var q = function (n) { return pw.querySelector('[name=' + n + ']'); };
    var run = function () {
      var d = C.dens[q('mat').value], t = num(q('t')), a = num(q('a')), b = num(q('b')), n = Math.max(1, parseInt(q('n').value, 10) || 1);
      var m2 = a * b / 1e6, kg = m2 * t * d; // m² · mm · kg/dm³ = kg
      document.getElementById('o-m2').textContent = fmt(m2, 3) + ' m²';
      document.getElementById('o-kg').textContent = fmt(kg, kg < 10 ? 2 : 1) + ' kg';
      document.getElementById('o-kgm2').textContent = fmt(t * d, 2) + ' kg/m²';
      document.getElementById('o-tot').textContent = fmt(kg * n, kg * n < 10 ? 2 : 1) + ' kg';
    };
    pw.addEventListener('input', run); pw.addEventListener('change', run); run();
  }

  var pb = document.getElementById('calc-plegado');
  if (pb) {
    var g = function (n) { return pb.querySelector('[name=' + n + ']'); };
    var run2 = function () {
      var t = num(g('t')), r = num(g('r')), k = num(g('k')), ang = num(g('ang')), a = num(g('a')), b = num(g('b'));
      var rad = ang * Math.PI / 180;
      var ba = rad * (r + k * t);                 // margen de pliegue (longitud del arco en la fibra neutra)
      var ossb = Math.tan(rad / 2) * (r + t);     // retroceso exterior
      var bd = 2 * ossb - ba;                     // deducción de pliegue
      var flat = a + b - bd;                      // desarrollo con cotas exteriores
      document.getElementById('o-ba').textContent = fmt(ba, 2) + ' mm';
      document.getElementById('o-ossb').textContent = fmt(ossb, 2) + ' mm';
      document.getElementById('o-bd').textContent = fmt(bd, 2) + ' mm';
      document.getElementById('o-flat').textContent = fmt(flat, 2) + ' mm';
    };
    pb.addEventListener('input', run2); pb.addEventListener('change', run2); run2();
  }
})();
