/* Старый адрес на GitHub Pages: переводим посетителя на meduprava.ru (тот же путь). */
(function(){var h=location.hostname;if(!/github\.io$/.test(h))return;var p=location.pathname;
if(p.indexOf('/shtin/')===0||p==='/shtin'){location.replace('https://antonshtin.ru/'+p.replace(/^\/shtin\/?/,'')+location.search+location.hash);return;}
location.replace('https://meduprava.ru'+p+location.search+location.hash);})();
