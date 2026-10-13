/* Логика лендинга: калькулятор срока, форма заявки, cookie-баннер, аналитика по согласию. */
(function () {
  'use strict';
  var CFG = window.MEDUPRAVA || {};
  var LS_COOKIE = 'meduprava.cookie';

  /* ---------- Реквизиты в подвале ---------- */
  Object.keys(CFG.REQUISITES || {}).forEach(function (k) {
    var el = document.querySelector('[data-field="' + k + '"]');
    if (el && CFG.REQUISITES[k]) el.textContent = CFG.REQUISITES[k];
  });

  /* ---------- Калькулятор сроков обжалования ---------- */
  // Протокол разногласий - 10 рабочих дней (п. 71.1 Порядка контроля, приказ Минздрава России № 231н),
  // претензия в фонд - 15 рабочих дней, только по МЭЭ и ЭКМП (ч. 1 ст. 42 Федерального закона № 326-ФЗ).
  // Нерабочие будни 2026 г. - ст. 112 ТК РФ и постановление Правительства РФ от 24.09.2025 № 1466.
  var HOLIDAYS = ['2026-01-01','2026-01-02','2026-01-05','2026-01-06','2026-01-07','2026-01-08','2026-01-09',
    '2026-02-23','2026-03-09','2026-05-01','2026-05-11','2026-06-12','2026-11-04','2026-12-31'];
  function iso(d) {
    var m = d.getMonth() + 1, day = d.getDate();
    return d.getFullYear() + '-' + (m < 10 ? '0' : '') + m + '-' + (day < 10 ? '0' : '') + day;
  }
  function isWork(d) {
    var wd = d.getDay();
    return wd !== 0 && wd !== 6 && HOLIDAYS.indexOf(iso(d)) === -1;
  }
  function addWorkingDays(date, days) {
    var d = new Date(date.getTime());
    var left = days;
    while (left > 0) {
      d.setDate(d.getDate() + 1);
      if (isWork(d)) left--;
    }
    return d;
  }
  function fmt(d) {
    return d.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' });
  }
  function workingDaysBetween(from, to) {
    var d = new Date(from.getTime()), n = 0;
    while (d < to) {
      d.setDate(d.getDate() + 1);
      if (isWork(d)) n++;
    }
    return n;
  }
  function describe(due, today) {
    if (due < today) return fmt(due) + ' - срок истек';
    return fmt(due) + ' - осталось рабочих дней: ' + workingDaysBetween(today, due);
  }
  var calcInput = document.getElementById('calc-date');
  var calcOut = document.getElementById('calc-out');
  if (calcInput && calcOut) {
    calcInput.addEventListener('change', function () {
      var v = calcInput.value;
      if (!v) { calcOut.textContent = 'Укажите дату, посчитаем крайние дни подачи протокола и претензии.'; calcOut.classList.remove('is-soon'); return; }
      var start = new Date(v + 'T00:00:00');
      if (isNaN(start.getTime())) return;
      var today = new Date(); today.setHours(0, 0, 0, 0);
      var proto = addWorkingDays(start, 10);
      var claim = addWorkingDays(start, 15);
      var text = 'Протокол разногласий: ' + describe(proto, today) + '. ' +
        'Претензия в фонд (по МЭЭ и ЭКМП): ' + describe(claim, today) + '. ';
      if (claim < today) text += 'Оба срока прошли, но документы стоит посмотреть: остается суд. ';
      var soonProto = proto >= today && workingDaysBetween(today, proto) <= 5;
      var soonClaim = claim >= today && workingDaysBetween(today, claim) <= 5;
      if (soonProto || soonClaim) text += 'Стоит не тянуть. ';
      text += 'Праздники учтены по производственному календарю 2026 года, для других лет расчет ориентировочный.';
      calcOut.textContent = text;
      calcOut.classList.toggle('is-soon', soonProto || soonClaim);
    });
  }

  /* ---------- Форма заявки ---------- */
  var form = document.getElementById('lead-form');
  var status = document.getElementById('form-status');
  function setStatus(msg, isError) {
    if (!status) return;
    status.textContent = msg;
    status.classList.toggle('is-error', !!isError);
  }
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fields = ['org', 'name', 'contact'];
      var bad = null;
      fields.forEach(function (id) {
        var el = document.getElementById(id);
        var ok = el && el.value.trim().length > 1;
        if (el) el.setAttribute('aria-invalid', ok ? 'false' : 'true');
        if (!ok && !bad) bad = el;
      });
      var consent = document.getElementById('consent');
      if (!consent || !consent.checked) {
        setStatus('Отметьте согласие на обработку персональных данных.', true);
        if (consent) consent.focus();
        return;
      }
      if (bad) { setStatus('Заполните обязательные поля.', true); bad.focus(); return; }

      var payload = {
        org: document.getElementById('org').value.trim(),
        name: document.getElementById('name').value.trim(),
        contact: document.getElementById('contact').value.trim(),
        email: (document.getElementById('email') || {}).value || '',
        consent_at: new Date().toISOString(),
        page: location.pathname,
        source: new URLSearchParams(location.search).get('utm_source') || ''
      };

      if (!CFG.FORM_ENDPOINT) {
        setStatus('Прием заявок на сайте еще не подключен. Напишите нам на ' + (CFG.FALLBACK_EMAIL || '') + ' - ответим так же быстро.', true);
        return;
      }
      var btn = form.querySelector('button[type="submit"]');
      if (btn) btn.disabled = true;
      setStatus('Отправляем...');
      fetch(CFG.FORM_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function (r) {
        if (!r.ok) throw new Error('bad status');
        form.reset();
        setStatus('Заявка отправлена. Ответим в рабочее время и скажем, какие документы нужны.');
      }).catch(function () {
        setStatus('Не удалось отправить. Напишите на ' + (CFG.FALLBACK_EMAIL || '') + ', пожалуйста.', true);
      }).then(function () {
        if (btn) btn.disabled = false;
      });
    });
  }

  /* ---------- Cookie и аналитика ---------- */
  function readChoice() {
    try { return localStorage.getItem(LS_COOKIE); } catch (e) { return null; }
  }
  function saveChoice(v) {
    try { localStorage.setItem(LS_COOKIE, v); } catch (e) { /* приватный режим */ }
  }
  function loadMetrika(id) {
    if (!id) return;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://mc.yandex.ru/metrika/tag.js';
    s.onload = function () {
      if (typeof window.ym === 'function') {
        window.ym(id, 'init', { clickmap: true, trackLinks: true, accurateTrackBounce: true });
      }
    };
    document.head.appendChild(s);
    window.ym = window.ym || function () { (window.ym.a = window.ym.a || []).push(arguments); };
    window.ym.l = +new Date();
  }
  var banner = document.getElementById('cookie');
  var choice = readChoice();
  if (choice === 'accept') {
    loadMetrika(CFG.ANALYTICS && CFG.ANALYTICS.YANDEX_METRIKA_ID);
  } else if (!choice && banner) {
    banner.hidden = false;
  }
  if (banner) {
    banner.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cookie]');
      if (!b) return;
      var v = b.getAttribute('data-cookie');
      saveChoice(v);
      banner.hidden = true;
      if (v === 'accept') loadMetrika(CFG.ANALYTICS && CFG.ANALYTICS.YANDEX_METRIKA_ID);
    });
  }
})();
