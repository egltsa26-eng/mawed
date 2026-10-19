window.MawedPage = function (M) {
  var form = document.querySelector('[data-calc="age"] form');
  var out = document.querySelector('[data-calc="age"] .result-body');
  var cal = form.querySelector('#age-cal');
  var d = form.querySelector('#age-d'), m = form.querySelector('#age-m'), y = form.querySelector('#age-y');

  function fillMonths() {
    var names = cal.value === 'h' ? M.HM : M.GM;
    var keep = m.value;
    m.innerHTML = '';
    names.forEach(function (n, i) { var o = document.createElement('option'); o.value = i + 1; o.textContent = (i + 1) + ' - ' + n; m.appendChild(o); });
    m.value = keep || '1';
  }
  function gDiff(a, b) { // a <= b, Gregorian [y,m,d]
    var yy = b[0] - a[0], mm = b[1] - a[1], dd = b[2] - a[2];
    if (dd < 0) { mm -= 1; dd += new Date(Date.UTC(b[0], b[1] - 1, 0)).getUTCDate(); }
    if (mm < 0) { yy -= 1; mm += 12; }
    return [yy, mm, dd];
  }
  function hDiff(a, b) { // Hijri [y,m,d]
    var yy = b[0] - a[0], mm = b[1] - a[1], dd = b[2] - a[2];
    if (dd < 0) {
      mm -= 1;
      var pm = b[1] - 1, py = b[0]; if (pm < 1) { pm = 12; py -= 1; }
      dd += M.hMonthLen(py, pm) || 30;
    }
    if (mm < 0) { yy -= 1; mm += 12; }
    return [yy, mm, dd];
  }
  function part(n, one, two, few, many) {
    if (n === 0) return '';
    if (n === 1) return one;
    if (n === 2) return two;
    if (n >= 3 && n <= 10) return n + ' ' + few;
    return n + ' ' + many;
  }
  function span(t) {
    var s = [part(t[0], 'سنة', 'سنتان', 'سنوات', 'سنة'), part(t[1], 'شهر', 'شهران', 'أشهر', 'شهرًا'), part(t[2], 'يوم', 'يومان', 'أيام', 'يومًا')].filter(Boolean);
    return s.length ? s.join(' و') : 'أقل من يوم';
  }
  function row(k, v) { return '<li><span>' + k + '</span><b>' + v + '</b></li>'; }

  function calc() {
    var dd = parseInt(d.value, 10), mm = parseInt(m.value, 10), yy = parseInt(y.value, 10);
    var today = M.todayRiyadh();
    var g, h;
    if (!dd || !mm || !yy) { out.innerHTML = '<p class="muted">اكتب تاريخ ميلادك كامل: اليوم والشهر والسنة.</p>'; return; }
    if (cal.value === 'h') {
      g = M.fromHijri(yy, mm, dd);
      if (!g) { out.innerHTML = '<p class="warn">هذا التاريخ غير موجود في تقويم أم القرى. تأكد من اليوم (بعض الأشهر 29 يومًا) ومن السنة بين 1343 و1500.</p>'; return; }
      h = [yy, mm, dd];
    } else {
      var t = new Date(Date.UTC(yy, mm - 1, dd));
      if (t.getUTCMonth() !== mm - 1 || t.getUTCDate() !== dd || yy < 1925) { out.innerHTML = '<p class="warn">تأكد من التاريخ الميلادي: اليوم غير موجود في هذا الشهر، أو السنة قبل 1925.</p>'; return; }
      g = [yy, mm, dd];
      h = M.toHijri(yy, mm, dd);
    }
    var gn = M.mjd(g[0], g[1], g[2]), tn = M.mjd(today[0], today[1], today[2]);
    if (gn > tn) { out.innerHTML = '<p class="warn">التاريخ في المستقبل. اكتب تاريخ ميلاد قبل اليوم.</p>'; return; }
    var th = M.toHijri(today[0], today[1], today[2]);
    var ga = gDiff(g, today), ha = h && th ? hDiff(h, th) : null;
    // next Gregorian birthday
    var ny = today[0], nb;
    for (;;) {
      var bd = g[2];
      var last = new Date(Date.UTC(ny, g[1], 0)).getUTCDate();
      if (bd > last) bd = last; // 29 Feb -> 28 Feb in common years
      nb = [ny, g[1], bd];
      if (M.mjd(nb[0], nb[1], nb[2]) >= tn) break;
      ny++;
    }
    var left = M.mjd(nb[0], nb[1], nb[2]) - tn;
    // next Hijri birthday (a 30th falls back to the 29th in a 29-day month)
    var hLeft = null, hNext = null;
    if (h && th) {
      for (var hy = th[0]; hy <= th[0] + 1 && hLeft === null; hy++) {
        var len = M.hMonthLen(hy, h[1]);
        if (!len) break;
        var gd = M.fromHijri(hy, h[1], Math.min(h[2], len));
        var n2 = M.mjd(gd[0], gd[1], gd[2]);
        if (n2 >= tn) { hLeft = n2 - tn; hNext = gd; }
      }
    }
    out.innerHTML =
      '<div class="result-big">' + ga[0] + '<small>سنة ميلادية</small></div>' +
      '<p>' + span(ga) + '</p>' +
      '<ul class="breakdown">' +
      (ha ? row('عمرك بالهجري', span(ha)) : '') +
      row('تاريخ الميلاد بالميلادي', M.weekday(g) + ' ' + M.gText(g)) +
      (h ? row('تاريخ الميلاد بالهجري', M.hText(h)) : '') +
      row('عدد الأيام اللي عشتها', (tn - gn).toLocaleString('en-US') + ' يوم') +
      row('عيد ميلادك الميلادي القادم', left === 0 ? 'اليوم' : 'بعد ' + left + ' ' + M.daysWord(left)) +
      (hLeft !== null ? row('عيد ميلادك الهجري القادم', hLeft === 0 ? 'اليوم' : M.weekday(hNext) + ' ' + M.gText(hNext) + '، بعد ' + hLeft + ' ' + M.daysWord(hLeft)) : '') +
      '</ul>';
  }
  cal.addEventListener('change', function () { fillMonths(); calc(); });
  [d, m, y].forEach(function (el) { el.addEventListener('input', calc); el.addEventListener('change', calc); });
  fillMonths();
  calc();
};
