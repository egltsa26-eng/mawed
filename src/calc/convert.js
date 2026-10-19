window.MawedPage = function (M) {
  var form = document.querySelector('[data-calc="convert"] form');
  var out = document.querySelector('[data-calc="convert"] .result-body');
  var dir = form.querySelector('#cv-dir');
  var d = form.querySelector('#cv-d'), m = form.querySelector('#cv-m'), y = form.querySelector('#cv-y');
  var yHint = form.querySelector('#cv-y-hint');

  function fillMonths() {
    var names = dir.value === 'h2g' ? M.HM : M.GM;
    var keep = m.value;
    m.innerHTML = '';
    names.forEach(function (n, i) { var o = document.createElement('option'); o.value = i + 1; o.textContent = (i + 1) + ' - ' + n; m.appendChild(o); });
    m.value = keep || '1';
    yHint.textContent = dir.value === 'h2g' ? 'من 1343 إلى 1500 هـ' : 'من 1925 إلى 2077 م';
  }
  function row(k, v) { return '<li><span>' + k + '</span><b>' + v + '</b></li>'; }
  function calc() {
    var dd = parseInt(d.value, 10), mm = parseInt(m.value, 10), yy = parseInt(y.value, 10);
    if (!dd || !mm || !yy) { out.innerHTML = '<p class="muted">اكتب اليوم والشهر والسنة.</p>'; return; }
    var g, h;
    if (dir.value === 'h2g') {
      h = [yy, mm, dd];
      g = M.fromHijri(yy, mm, dd);
      if (!g) {
        var len = M.hMonthLen(yy, mm);
        out.innerHTML = '<p class="warn">' + (len ? 'شهر ' + M.HM[mm - 1] + ' ' + yy + ' في تقويم أم القرى ' + len + ' يومًا فقط.' : 'السنة خارج المدى المتاح (1343 إلى 1500 هـ).') + '</p>';
        return;
      }
      out.innerHTML = '<div class="result-big" style="font-size:clamp(1.6rem,1.2rem + 2vw,2.2rem)">' + M.gText(g) + '<small>م</small></div>' +
        '<ul class="breakdown">' + row('اليوم', M.weekday(g)) + row('التاريخ الهجري', M.hText(h)) +
        row('بالأرقام', g[2] + '/' + g[1] + '/' + g[0]) + '</ul>';
    } else {
      var t = new Date(Date.UTC(yy, mm - 1, dd));
      if (t.getUTCMonth() !== mm - 1 || t.getUTCDate() !== dd) { out.innerHTML = '<p class="warn">هذا اليوم غير موجود في ' + M.GM[mm - 1] + ' ' + yy + '.</p>'; return; }
      g = [yy, mm, dd];
      h = M.toHijri(yy, mm, dd);
      if (!h) { out.innerHTML = '<p class="warn">السنة خارج المدى المتاح (1925 إلى 2077 م).</p>'; return; }
      out.innerHTML = '<div class="result-big" style="font-size:clamp(1.6rem,1.2rem + 2vw,2.2rem)">' + M.hText(h) + '</div>' +
        '<ul class="breakdown">' + row('اليوم', M.weekday(g)) + row('التاريخ الميلادي', M.gText(g)) +
        row('بالأرقام', h[2] + '/' + h[1] + '/' + h[0] + 'هـ') + '</ul>';
    }
  }
  dir.addEventListener('change', function () {
    // carry the shown date over to the other calendar so switching feels natural
    var dd = parseInt(d.value, 10), mm = parseInt(m.value, 10), yy = parseInt(y.value, 10);
    var conv = null;
    if (dd && mm && yy) conv = dir.value === 'h2g' ? M.toHijri(yy, mm, dd) : M.fromHijri(yy, mm, dd);
    fillMonths();
    if (conv) { y.value = conv[0]; m.value = conv[1]; d.value = conv[2]; }
    calc();
  });
  [d, m, y].forEach(function (el) { el.addEventListener('input', calc); el.addEventListener('change', calc); });
  var t = M.todayRiyadh();
  fillMonths();
  y.value = t[0]; m.value = t[1]; d.value = t[2];
  calc();
};
