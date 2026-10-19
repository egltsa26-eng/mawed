window.MawedPage = function (M) {
  var form = document.querySelector('[data-calc="vat"] form');
  var out = document.querySelector('[data-calc="vat"] .result-body');
  var amt = form.querySelector('#vat-amount');
  var RATE = 0.15;
  function row(k, v) { return '<li><span>' + k + '</span><b>' + v + '</b></li>'; }
  function mode() { var c = form.querySelector('input[name="vat-mode"]:checked'); return c ? c.value : 'add'; }
  function calc() {
    var a = parseFloat(String(amt.value).replace(/,/g, ''));
    if (!(a > 0)) { out.innerHTML = '<p class="muted">اكتب المبلغ بالريال.</p>'; return; }
    var net, vat, gross;
    if (mode() === 'add') { net = a; vat = a * RATE; gross = a + vat; }
    else { gross = a; net = a / (1 + RATE); vat = gross - net; }
    out.innerHTML = '<div class="result-big">' + M.money(vat) + '<small>ريال ضريبة</small></div>' +
      '<ul class="breakdown">' + row('المبلغ قبل الضريبة', M.money(net) + ' ريال') + row('ضريبة القيمة المضافة 15%', M.money(vat) + ' ريال') +
      row('الإجمالي شامل الضريبة', M.money(gross) + ' ريال') + '</ul>';
  }
  form.addEventListener('input', calc);
  form.addEventListener('change', calc);
  calc();
};
