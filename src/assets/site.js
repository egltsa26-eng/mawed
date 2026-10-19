/* موعد — countdowns, Umm al-Qura dates and calculators. No dependencies. */
(function () {
  'use strict';

  var GM = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر'];
  var HM = ['محرم', 'صفر', 'ربيع الأول', 'ربيع الآخر', 'جمادى الأولى', 'جمادى الآخرة', 'رجب', 'شعبان', 'رمضان', 'شوال', 'ذو القعدة', 'ذو الحجة'];
  var WD = ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت'];
  var DAY = 864e5;
  var RIYADH = 3 * 3600e3; // Saudi Arabia is UTC+3 all year

  /* ---------- Umm al-Qura calendar (month lengths from the official table) ---------- */
  var UQ = window.MAWED_UQ || null;
  var starts = null;
  function uqStarts() {
    if (starts || !UQ) return starts;
    var s = new Array(UQ.lens.length + 1), mjd = UQ.firstMJD;
    s[0] = mjd;
    for (var i = 0; i < UQ.lens.length; i++) {
      var c = UQ.lens.charAt(i);
      mjd += c === '8' ? 28 : c === '9' ? 29 : c === '0' ? 30 : 31;
      s[i + 1] = mjd;
    }
    return (starts = s);
  }
  function mjd(y, m, d) { return Math.floor(Date.UTC(y, m - 1, d) / DAY) + 40587; }
  function fromMjd(n) { var t = new Date((n - 40587) * DAY); return [t.getUTCFullYear(), t.getUTCMonth() + 1, t.getUTCDate()]; }
  function toHijri(y, m, d) {
    var s = uqStarts(); if (!s) return null;
    var n = mjd(y, m, d);
    if (n < s[0] || n >= s[s.length - 1]) return null;
    var lo = 0, hi = s.length - 2;
    while (lo < hi) { var mid = (lo + hi + 1) >> 1; if (s[mid] <= n) lo = mid; else hi = mid - 1; }
    return [UQ.firstYear + Math.floor(lo / 12), (lo % 12) + 1, n - s[lo] + 1];
  }
  function hMonthLen(hy, hm) {
    var s = uqStarts(); if (!s) return null;
    var i = (hy - UQ.firstYear) * 12 + (hm - 1);
    if (i < 0 || i >= s.length - 1) return null;
    return s[i + 1] - s[i];
  }
  function fromHijri(hy, hm, hd) {
    var s = uqStarts(); if (!s) return null;
    var i = (hy - UQ.firstYear) * 12 + (hm - 1);
    if (i < 0 || i >= s.length - 1) return null;
    if (hd < 1 || hd > s[i + 1] - s[i]) return null;
    return fromMjd(s[i] + hd - 1);
  }

  /* ---------- formatting ---------- */
  function gText(a) { return a[2] + ' ' + GM[a[1] - 1] + ' ' + a[0]; }
  function hText(a) { return a ? a[2] + ' ' + HM[a[1] - 1] + ' ' + a[0] + 'هـ' : ''; }
  function weekday(a) { return WD[new Date(Date.UTC(a[0], a[1] - 1, a[2])).getUTCDay()]; }
  function parseISO(s) { var p = s.split('-'); return [+p[0], +p[1], +p[2]]; }
  function todayRiyadh() { var t = new Date(Date.now() + RIYADH); return [t.getUTCFullYear(), t.getUTCMonth() + 1, t.getUTCDate()]; }
  function daysWord(n) {
    if (n === 1) return 'يوم';
    if (n === 2) return 'يومان';
    if (n >= 3 && n <= 10) return 'أيام';
    return 'يومًا';
  }
  function money(x) {
    if (!isFinite(x)) return '—';
    return x.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  window.Mawed = {
    toHijri: toHijri, fromHijri: fromHijri, hMonthLen: hMonthLen, mjd: mjd, fromMjd: fromMjd,
    gText: gText, hText: hText, weekday: weekday, todayRiyadh: todayRiyadh, daysWord: daysWord,
    money: money, GM: GM, HM: HM, WD: WD
  };

  /* ---------- countdown pages ---------- */
  function readData(id) {
    var el = document.getElementById(id || 'mawed-data');
    if (!el) return null;
    try { return JSON.parse(el.textContent); } catch (e) { return null; }
  }

  function nextOf(dates, today) {
    var t = mjd(today[0], today[1], today[2]);
    for (var i = 0; i < dates.length; i++) {
      var a = parseISO(dates[i].date);
      if (mjd(a[0], a[1], a[2]) >= t) return { i: i, a: a, left: mjd(a[0], a[1], a[2]) - t };
    }
    return null;
  }

  function renderCountdown() {
    var data = readData();
    if (!data || !data.dates) return;
    var today = todayRiyadh();
    var n = nextOf(data.dates, today);
    var leaf = document.querySelector('[data-leaf]');
    if (!n || !leaf) return;
    var item = data.dates[n.i];
    var set = function (sel, v) { var el = leaf.querySelector(sel); if (el) el.textContent = v; };
    var h = toHijri(n.a[0], n.a[1], n.a[2]);
    set('[data-l-month]', GM[n.a[1] - 1] + ' ' + n.a[0]);
    set('[data-l-hmonth]', h ? HM[h[1] - 1] + ' ' + h[0] : '');
    if (n.left === 0) {
      leaf.classList.add('is-today');
      set('[data-l-kicker]', data.todayKicker || 'اليوم');
      set('[data-l-num]', '0');
      set('[data-l-unit]', data.todayUnit || 'موعده اليوم');
    } else {
      set('[data-l-kicker]', data.kicker || 'باقي');
      set('[data-l-num]', String(n.left));
      set('[data-l-unit]', daysWord(n.left));
    }
    set('[data-l-g]', weekday(n.a) + ' ' + gText(n.a));
    set('[data-l-h]', hText(h));
    document.querySelectorAll('[data-answer]').forEach(function (el) {
      var tpl = el.getAttribute('data-answer');
      el.textContent = tpl
        .replace('{label}', item.label || '')
        .replace('{weekday}', weekday(n.a))
        .replace('{date}', gText(n.a))
        .replace('{hijri}', hText(h))
        .replace('{left}', n.left === 0 ? 'اليوم' : 'باقي ' + n.left + ' ' + daysWord(n.left));
    });
    if (data.title_tpl) document.title = data.title_tpl.replace('{label}', item.label || '');
    // table rows
    document.querySelectorAll('tr[data-date]').forEach(function (tr) {
      var a = parseISO(tr.getAttribute('data-date'));
      var d = mjd(a[0], a[1], a[2]) - mjd(today[0], today[1], today[2]);
      tr.classList.toggle('is-past', d < 0);
      tr.classList.toggle('is-next', tr.getAttribute('data-date') === item.date);
    });
    // live timer to 00:00 Riyadh time of the target day
    var timer = document.querySelector('[data-timer]');
    if (timer && n.left > 0) {
      var target = Date.UTC(n.a[0], n.a[1] - 1, n.a[2]) - RIYADH;
      var tick = function () {
        var ms = Math.max(0, target - Date.now());
        var hh = Math.floor(ms / 3600e3) % 24, mm = Math.floor(ms / 60e3) % 60, ss = Math.floor(ms / 1e3) % 60;
        var dd = Math.floor(ms / DAY);
        timer.querySelector('[data-t-d]').textContent = dd;
        timer.querySelector('[data-t-h]').textContent = hh;
        timer.querySelector('[data-t-m]').textContent = mm;
        timer.querySelector('[data-t-s]').textContent = ss;
      };
      tick();
      timer.hidden = false;
      setInterval(tick, 1000);
    }
    leaf.classList.add('tear');
  }

  function renderUpcoming() {
    var data = readData('mawed-upcoming');
    var list = document.querySelector('[data-upcoming]');
    if (!data || !list) return;
    var today = todayRiyadh(), t = mjd(today[0], today[1], today[2]);
    var rows = [];
    data.items.forEach(function (it) {
      var n = nextOf(it.dates, today);
      if (n) rows.push({ it: it, n: n });
    });
    rows.sort(function (a, b) { return a.n.left - b.n.left; });
    list.innerHTML = '';
    rows.forEach(function (r) {
      var a = r.n.a, h = toHijri(a[0], a[1], a[2]);
      var li = document.createElement('li');
      var link = document.createElement('a');
      link.href = r.it.href;
      link.innerHTML =
        '<span class="mini" aria-hidden="true"><span class="m"></span><span class="d"></span></span>' +
        '<span><span class="u-name"></span><span class="u-when"></span></span>' +
        '<span class="u-left"><b></b><span></span></span>';
      link.querySelector('.m').textContent = GM[a[1] - 1];
      link.querySelector('.d').textContent = a[2];
      link.querySelector('.u-name').textContent = r.it.name;
      link.querySelector('.u-when').textContent = weekday(a) + ' ' + gText(a) + (h ? ' · ' + hText(h) : '');
      if (r.n.left === 0) {
        link.querySelector('.u-left b').textContent = 'اليوم';
        link.querySelector('.u-left span').textContent = '';
      } else {
        link.querySelector('.u-left b').textContent = r.n.left;
        link.querySelector('.u-left span').textContent = daysWord(r.n.left);
      }
      li.appendChild(link);
      list.appendChild(li);
    });
    // Hero leaf = the nearest item
    var leaf = document.querySelector('[data-leaf]');
    if (leaf && rows[0]) {
      var first = rows[0], a0 = first.n.a, h0 = toHijri(a0[0], a0[1], a0[2]);
      var set = function (sel, v) { var el = leaf.querySelector(sel); if (el) el.textContent = v; };
      set('[data-l-month]', GM[a0[1] - 1] + ' ' + a0[0]);
      set('[data-l-hmonth]', h0 ? HM[h0[1] - 1] + ' ' + h0[0] : '');
      set('[data-l-kicker]', first.it.name + (first.n.left === 0 ? '' : ' بعد'));
      set('[data-l-num]', first.n.left === 0 ? 'اليوم' : String(first.n.left));
      set('[data-l-unit]', first.n.left === 0 ? '' : daysWord(first.n.left));
      set('[data-l-g]', weekday(a0) + ' ' + gText(a0));
      set('[data-l-h]', hText(h0));
      var link0 = leaf.closest('a') || document.querySelector('[data-leaf-link]');
      if (link0) link0.href = first.it.href;
      leaf.classList.add('tear');
    }
  }

  function renderTodayLine() {
    var el = document.querySelector('[data-today]');
    if (!el) return;
    var t = todayRiyadh(), h = toHijri(t[0], t[1], t[2]);
    el.textContent = 'اليوم ' + weekday(t) + ' ' + gText(t) + ' · ' + hText(h);
  }

  window.Mawed.readData = readData;
  window.Mawed.nextOf = nextOf;
  window.Mawed.parseISO = parseISO;

  document.addEventListener('DOMContentLoaded', function () {
    renderTodayLine();
    renderCountdown();
    renderUpcoming();
    if (typeof window.MawedPage === 'function') window.MawedPage(window.Mawed);
  });
})();
