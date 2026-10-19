window.MawedPage = function (M) {
  var root = document.querySelector('[data-calc="eosb"]');
  var form = root.querySelector('form');
  var out = root.querySelector('.result-body');
  var $ = function (id) { return form.querySelector('#' + id); };

  function num(el) { var v = parseFloat(String(el.value).replace(/,/g, '')); return isFinite(v) && v > 0 ? v : 0; }
  function parseDate(s) { var p = String(s || '').split('-'); return p.length === 3 ? [+p[0], +p[1], +p[2]] : null; }
  function diff(a, b) { // Gregorian [y,m,d], a <= b
    var y = b[0] - a[0], m = b[1] - a[1], d = b[2] - a[2];
    if (d < 0) { m -= 1; d += new Date(Date.UTC(b[0], b[1] - 1, 0)).getUTCDate(); }
    if (m < 0) { y -= 1; m += 12; }
    return [y, m, d];
  }
  function reason() { var c = form.querySelector('input[name="eos-reason"]:checked'); return c ? c.value : 'employer'; }
  function row(k, v) { return '<li><span>' + k + '</span><b>' + v + '</b></li>'; }
  function plural(n, one, two, few, many) { return n === 1 ? one : n === 2 ? two : n <= 10 ? n + ' ' + few : n + ' ' + many; }

  function calc() {
    var s = parseDate($('eos-start').value), e = parseDate($('eos-end').value);
    var wage = num($('eos-basic')) + num($('eos-housing')) + num($('eos-transport')) + num($('eos-other'));
    if (!s || !e) { out.innerHTML = '<p class="muted">اكتب تاريخ بداية العمل وتاريخ نهايته.</p>'; return; }
    if (M.mjd(e[0], e[1], e[2]) <= M.mjd(s[0], s[1], s[2])) { out.innerHTML = '<p class="warn">تاريخ النهاية لازم يكون بعد تاريخ البداية.</p>'; return; }
    if (!wage) { out.innerHTML = '<p class="muted">اكتب آخر أجر شهري: الأساسي والبدلات الثابتة.</p>'; return; }
    var t = diff(s, e);
    var years = t[0] + t[1] / 12 + t[2] / 365;
    var first = Math.min(years, 5), rest = Math.max(years - 5, 0);
    var full = first * wage / 2 + rest * wage;
    var r = reason(), factor = 1, why = '';
    if (r === 'resign') {
      if (years < 2) { factor = 0; why = 'الاستقالة قبل إكمال سنتين لا يستحق معها العامل مكافأة (المادة 85).'; }
      else if (years <= 5) { factor = 1 / 3; why = 'استقالة بعد سنتين وحتى خمس سنوات: ثلث المكافأة (المادة 85).'; }
      else if (years < 10) { factor = 2 / 3; why = 'استقالة بعد أكثر من خمس سنوات وقبل عشر: ثلثا المكافأة (المادة 85).'; }
      else { factor = 1; why = 'استقالة بعد عشر سنوات أو أكثر: المكافأة كاملة (المادة 85).'; }
    } else if (r === 'art80') {
      factor = 0; why = 'الفصل لأحد أسباب المادة 80 يُسقط المكافأة.';
    } else if (r === 'art87') {
      why = 'الحالات المذكورة في المادة 87 تستحق المكافأة كاملة حتى لو ترك العامل العمل.';
    } else {
      why = 'انتهاء العقد أو إنهاؤه من صاحب العمل لغير أسباب المادة 80: المكافأة كاملة (المادة 84).';
    }
    var award = full * factor;
    var leaveDays = num($('eos-leave'));
    var leavePay = leaveDays * wage / 30;
    var contract = form.querySelector('input[name="eos-contract"]:checked');
    var openEnded = contract && contract.value === 'open';
    var caution = (r === 'resign' && openEnded && factor < 1)
      ? '<p class="warn">عقدك غير محدد المدة: بعد تعديلات نظام العمل في فبراير 2025 صار تعريف الاستقالة مرتبطًا بالعقد محدد المدة، وبعض التقارير تذكر أن إنهاء العقد غير محدد المدة بإشعار وفق المادة 75 يستحق المكافأة كاملة (' + M.money(full) + ' ريال). هذه النقطة غير محسومة في المصادر الرسمية، فتأكد من حاسبة الوزارة أو مكتب العمل.</p>'
      : '';
    var dur = [t[0] ? plural(t[0], 'سنة', 'سنتان', 'سنوات', 'سنة') : '', t[1] ? plural(t[1], 'شهر', 'شهران', 'أشهر', 'شهرًا') : '', t[2] ? plural(t[2], 'يوم', 'يومان', 'أيام', 'يومًا') : ''].filter(Boolean).join(' و');
    out.innerHTML =
      '<div class="result-big">' + M.money(award) + '<small>ريال</small></div>' +
      '<p>' + why + '</p>' + caution +
      '<ul class="breakdown">' +
      row('مدة الخدمة', dur || 'أقل من يوم') +
      row('الأجر المعتمد للحساب', M.money(wage) + ' ريال') +
      row('عن أول 5 سنوات (نصف شهر لكل سنة)', M.money(first * wage / 2) + ' ريال') +
      row('عن ما بعد 5 سنوات (شهر لكل سنة)', M.money(rest * wage) + ' ريال') +
      row('المكافأة الكاملة', M.money(full) + ' ريال') +
      (factor !== 1 ? row('نسبة الاستحقاق', factor === 0 ? 'لا شيء' : factor < .5 ? 'الثلث' : 'الثلثان') : '') +
      (leaveDays ? row('بدل الإجازات المتبقية: ' + (leaveDays === 1 ? 'يوم واحد' : leaveDays === 2 ? 'يومان' : leaveDays + ' ' + (leaveDays <= 10 ? 'أيام' : 'يومًا')) + ' (المادة 111)', M.money(leavePay) + ' ريال') + row('المجموع مع بدل الإجازات', M.money(award + leavePay) + ' ريال') : '') +
      '</ul>';
  }
  form.addEventListener('input', calc);
  form.addEventListener('change', calc);
  calc();
};
