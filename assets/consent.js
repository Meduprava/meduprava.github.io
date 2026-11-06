/* Баннер файлов cookie и Яндекс Метрика по согласию посетителя.
   Подключение: <script src="assets/consent.js" data-metrika="ID" data-notice="legal/cookies.html" defer></script>
   - Метрика грузится только после нажатия «Принять» и только на рабочем домене (data-host).
   - «Только необходимые» - аналитика не подключается.
   - Ссылка или кнопка с атрибутом data-cookie-settings снова открывает баннер, выбор можно изменить или отозвать.
   - При отзыве согласия удаляются файлы _ym* и страница перезагружается. */
(function () {
  'use strict';
  var me = document.currentScript;
  var ID = me && me.getAttribute('data-metrika');
  var NOTICE = (me && me.getAttribute('data-notice')) || 'legal/cookies.html';
  var HOST = (me && me.getAttribute('data-host')) || '';
  var KEY = (me && me.getAttribute('data-key')) || 'cookie.choice';
  var THEME = (me && me.getAttribute('data-theme')) || 'meduprava';

  function read() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function save(v) { try { localStorage.setItem(KEY, v); } catch (e) { /* приватный режим */ } }
  function onHost() { return !HOST || location.hostname === HOST || location.hostname === 'www.' + HOST; }

  function loadMetrika() {
    if (!ID || !onHost() || window.__ymLoaded) return;
    window.__ymLoaded = true;
    window.ym = window.ym || function () { (window.ym.a = window.ym.a || []).push(arguments); };
    window.ym.l = +new Date();
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://mc.yandex.ru/metrika/tag.js';
    document.head.appendChild(s);
    window.ym(Number(ID), 'init', { clickmap: true, trackLinks: true, accurateTrackBounce: true, webvisor: false });
  }

  function clearYm() {
    var host = location.hostname;
    document.cookie.split(';').forEach(function (c) {
      var name = c.split('=')[0].trim();
      if (name.indexOf('_ym') !== 0) return;
      var exp = '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
      document.cookie = name + exp;
      document.cookie = name + exp + '; domain=' + host;
      document.cookie = name + exp + '; domain=.' + host;
    });
  }

  var C = THEME === 'shtin'
    ? { bg: '#FFFFFF', ink: '#1B2638', line: '#D9D3C7', acc: '#1B2638', accInk: '#FFFFFF', alt: '#F6F4EF', link: '#1B2638', r: '2px', font: 'Manrope, system-ui, sans-serif' }
    : { bg: '#FBFAF6', ink: '#23332C', line: '#D9D3C3', acc: '#23332C', accInk: '#F3F1EA', alt: '#DCE5D6', link: '#B5552F', r: '18px', font: '"Golos Text", system-ui, sans-serif' };

  var css = '.ck{position:fixed;left:16px;right:16px;bottom:calc(env(safe-area-inset-bottom,0px) + 16px);max-width:640px;margin:0 auto;'
    + 'background:' + C.bg + ';color:' + C.ink + ';border:1px solid ' + C.line + ';border-radius:' + C.r + ';padding:16px 20px;display:flex;flex-wrap:wrap;gap:12px;align-items:center;'
    + 'box-shadow:0 10px 30px rgba(20,24,28,.16);z-index:9999;font:400 14px/1.45 ' + C.font + '}'
    + '.ck[hidden]{display:none!important}.ck p{margin:0;flex:1 1 260px}.ck a{color:' + C.link + ';text-decoration:underline}'
    + '.ck__b{display:flex;flex-wrap:wrap;gap:8px}.ck button{font:600 13px/1 ' + C.font + ';min-height:40px;padding:10px 16px;border-radius:' + C.r + ';cursor:pointer;border:1px solid ' + C.acc + '}'
    + '.ck .ck__y{background:' + C.acc + ';color:' + C.accInk + '}.ck .ck__n{background:' + C.alt + ';color:' + C.ink + ';border-color:' + C.line + '}'
    + '.ck button:focus-visible{outline:2px solid ' + C.acc + ';outline-offset:2px}';
  var st = document.createElement('style');
  st.textContent = css;
  document.head.appendChild(st);

  var box = document.createElement('div');
  box.className = 'ck';
  box.hidden = true;
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-label', 'Настройки файлов cookie');
  box.innerHTML = '<p>Сайт запоминает ваш выбор в браузере. Яндекс Метрика (статистика посещений) подключается только с вашего согласия. '
    + 'Подробнее - в <a href="' + NOTICE + '">уведомлении о файлах cookie</a>.</p>'
    + '<div class="ck__b"><button type="button" class="ck__y" data-ck="accept">Принять</button>'
    + '<button type="button" class="ck__n" data-ck="decline">Только необходимые</button></div>';

  function mount() {
    document.body.appendChild(box);
    var choice = read();
    if (choice === 'accept') loadMetrika();
    else if (!choice) box.hidden = false;

    box.addEventListener('click', function (e) {
      var b = e.target.closest('[data-ck]');
      if (!b) return;
      var v = b.getAttribute('data-ck');
      var prev = read();
      save(v);
      box.hidden = true;
      if (v === 'accept') loadMetrika();
      else if (prev === 'accept') { clearYm(); location.reload(); }
    });
    document.addEventListener('click', function (e) {
      var s = e.target.closest('[data-cookie-settings]');
      if (!s) return;
      e.preventDefault();
      box.hidden = false;
      var f = box.querySelector('button');
      if (f) f.focus();
    });
  }
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount);
})();
