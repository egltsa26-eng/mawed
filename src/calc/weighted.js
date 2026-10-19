window.MawedPage = function (M) {
  var root = document.querySelector('[data-calc="weighted"]');
  var form = root.querySelector('form');
  var out = root.querySelector('.result-body');
  var $ = function (id) { return form.querySelector('#' + id); };
  var preset = $('w-preset');
  var custom = form.querySelector('[data-custom]');
  var stepField = form.querySelector('[data-step]');
  var NAMES = ['الثانوي', 'القدرات', 'التحصيلي', 'STEP'];

  function val(el) { var v = parseFloat(String(el.value).replace(/,/g, '')); return isFinite(v) ? v : NaN; }
  function weights() {
    if (preset.value === 'custom') return [$('w-wg'), $('w-wq'), $('w-wt'), $('w-ws')].map(function (el) { var x = val(el); return isFinite(x) ? x : 0; });
    return preset.value.split('-').map(Number);
  }
  function row(k, v) { return '<li><span>' + k + '</span><b>' + v + '</b></li>'; }
  function calc() {
    custom.hidden = preset.value !== 'custom';
    var w = weights();
    stepField.hidden = !(w[3] > 0);
    var scores = [val($('w-gpa')), val($('w-q')), val($('w-t')), val($('w-s'))];
    var sum = w[0] + w[1] + w[2] + w[3];
    for (var i = 0; i < 4; i++) {
      if (w[i] > 0 && !isFinite(scores[i])) { out.innerHTML = '<p class="muted">اكتب درجة ' + NAMES[i] + ' من 100.</p>'; return; }
      if (w[i] > 0 && (scores[i] < 0 || scores[i] > 100)) { out.innerHTML = '<p class="warn">درجة ' + NAMES[i] + ' لازم تكون بين 0 و100.</p>'; return; }
    }
    if (Math.abs(sum - 100) > 0.001) { out.innerHTML = '<p class="warn">مجموع الأوزان ' + sum + '%، ولازم يكون 100%.</p>'; return; }
    var total = 0, lines = '';
    for (var j = 0; j < 4; j++) {
      if (!(w[j] > 0)) continue;
      var part = scores[j] * w[j] / 100;
      total += part;
      lines += row(NAMES[j] + ' × ' + w[j] + '%', part.toFixed(2));
    }
    out.innerHTML = '<div class="result-big">' + total.toFixed(2) + '<small>%</small></div><ul class="breakdown">' + lines + '</ul>';
  }
  form.addEventListener('input', calc);
  form.addEventListener('change', calc);
  calc();
};
