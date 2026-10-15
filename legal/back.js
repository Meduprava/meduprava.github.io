/* Возврат на ту страницу направления, с которой пришел посетитель.
   Ссылки с финансовой страницы ведут сюда с параметром ?from=finance. */
(function () {
  'use strict';
  var from = new URLSearchParams(location.search).get('from');
  if (from !== 'finance') return;
  var back = document.querySelector('.back');
  if (back) {
    back.href = '../finance.html';
    back.textContent = '← К финансовому направлению';
  }
  // Сохраняем признак при переходах между юридическими страницами.
  document.querySelectorAll('a[href]').forEach(function (a) {
    var h = a.getAttribute('href');
    if (/^(privacy|cookies|obezlichivanie|consent)\.html(#.*)?$/.test(h)) {
      var parts = h.split('#');
      a.setAttribute('href', parts[0] + '?from=finance' + (parts[1] ? '#' + parts[1] : ''));
    }
  });
})();
