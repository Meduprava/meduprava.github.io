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

  /* ---------- Калькулятор 15 рабочих дней ---------- */
  // Считаем только выходные. Праздники закон о переносах меняет каждый год,
  // поэтому результат показываем как ориентир, а не как юридический расчет.
  function addWorkingDays(date, days) {
    var d = new Date(date.getTime());
    var left = days;
    while (left > 0) {
      d.setDate(d.getDate() + 1);
      var wd = d.getDay();
      if (wd !== 0 && wd !== 6) left--;
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
      var wd = d.getDay();
      if (wd !== 0 && wd !== 6) n++;
    }
    return n;
  }
  var calcInput = document.getElementById('calc-date');
  var calcOut = document.getElementById('calc-out');
  if (calcInput && calcOut) {
    calcInput.addEventListener('change', function () {
      var v = calcInput.value;
      if (!v) { calcOut.textContent = 'Укажите дату, посчитаем крайний день подачи претензии.'; calcOut.classList.remove('is-soon'); return; }
      var start = new Date(v + 'T00:00:00');
      if (isNaN(start.getTime())) return;
      var due = addWorkingDays(start, 15);
      var today = new Date(); today.setHours(0, 0, 0, 0);
      var left = workingDaysBetween(today, due);
      var text = 'Крайний день подачи претензии в территориальный фонд: ' + fmt(due) + '. ';
      if (due < today) { text += 'Срок истек, но посмотреть документы все равно имеет смысл.'; }
      else if (left <= 5) { text += 'Осталось рабочих дней: ' + left + '. Стоит не тянуть.'; }
      else { text += 'Осталось рабочих дней: ' + left + '.'; }
      text += ' Расчет учитывает выходные, но не переносы праздничных дней, поэтому это ориентир.';
      calcOut.textContent = text;
      calcOut.classList.toggle('is-soon', left <= 5);
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
