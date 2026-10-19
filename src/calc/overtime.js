window.MawedPage = function (M) {
  var root = document.querySelector('[data-calc="overtime"]');
  var form = root.querySelector('form');
  var out = root.querySelector('.result-body');
  var $ = function (id) { return form.querySelector('#' + id); };
  function num(el) { var v = parseFloat(String(el.value).replace(/,/g, '')); return isFinite(v) && v > 0 ? v : 0; }
  function row(k, v) { return '<li><span>' + k + '</span><b>' + v + '</b></li>'; }
  function calc() {
    var basic = num($('ot-basic')), allow = num($('ot-allow')), hours = num($('ot-hours')), daily = num($('ot-daily')) || 8;
    if (!basic) { out.innerHTML = '<p class="muted">اكتب الراتب الأساسي الشهري.</p>'; return; }
    if (!hours) { out.innerHTML = '<p class="muted">اكتب عدد ساعات العمل الإضافي.</p>'; return; }
    var monthHours = 30 * daily;
    var hourActual = (basic + allow) / monthHours;
    var hourBasic = basic / monthHours;
    var perHour = hourActual + hourBasic * 0.5;
    out.innerHTML = '<div class="result-big">' + M.money(perHour * hours) + '<small>ريال</small></div>' +
      '<ul class="breakdown">' +
      row('أجر الساعة الفعلي', M.money(hourActual) + ' ريال') +
      row('50% من أجر الساعة الأساسي', M.money(hourBasic * 0.5) + ' ريال') +
      row('أجر الساعة الإضافية', M.money(perHour) + ' ريال') +
      row('عدد الساعات', hours.toLocaleString('en-US')) +
      '</ul>';
  }
  form.addEventListener('input', calc);
  form.addEventListener('change', calc);
  calc();
};
