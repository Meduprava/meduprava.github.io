"""Сборка страниц-хаба Медуправы: index.html, pravo.html, servis.html, llms.txt, robots.txt, sitemap.xml.
Остальные страницы (finance.html, ekspertiza-oms.html, kalkulyator-oms.html, legal/) правятся вручную.
Запуск из корня репозитория: python3 tools/build_hub.py"""
import json, re, html, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://meduprava.github.io'
CSSV = datetime.datetime.now().strftime('%Y%m%d%H%M')
TODAY = datetime.date.today().isoformat()
EMAIL = 'meduprava@mail.ru'
VK, VK_H = 'https://vk.ru/meduprava', 'vk.ru/meduprava'
TG, TG_H = 'https://t.me/AresID13', '@AresID13'
PHONE, PHONE_H = '+79832816353', '+7 983 281-63-53'
OGRNIP = '320246800028048'

NAV = [('pravo.html', 'Право'), ('finance.html', 'Финансы'), ('servis.html', 'Операционное управление и сервис'), ('ekspertiza-oms.html', 'Экспертиза ОМС')]
AREA = [{'@type': 'City', 'name': 'Москва'}, {'@type': 'AdministrativeArea', 'name': 'Московская область'}, {'@type': 'Country', 'name': 'Россия'}]
ORG = {'@type': 'ProfessionalService', '@id': BASE + '/#org', 'name': 'Медуправа', 'alternateName': 'МЕДУПРАВА',
       'description': 'Юридическое, финансовое и операционное сопровождение частных медицинских клиник: диагностика проблемных мест, экспертиза актов страховых компаний по ОМС, финансовый директор на аутсорсе, операционное управление и развитие, служба сервиса и заботы о пациентах.',
       'url': BASE + '/', 'logo': BASE + '/assets/meduprava-logo.svg', 'image': BASE + '/assets/og-hub-v2.png', 'email': EMAIL, 'telephone': PHONE_H,
       'areaServed': AREA, 'knowsLanguage': 'ru', 'sameAs': [VK],
       'founder': [{'@type': 'Person', 'name': 'Антон Штин', 'jobTitle': 'Юрист, руководитель юридического направления', 'image': BASE + '/assets/team/anton-shtin-v2.jpg', 'url': BASE + '/shtin/'},
                   {'@type': 'Person', 'name': 'Елена Штин', 'jobTitle': 'Финансовый директор'},
                   {'@type': 'Person', 'name': 'Дарья Гаврилова', 'jobTitle': 'Операционное управление и развитие, служба сервиса и заботы'}],
       'parentOrganization': {'@type': 'Organization', 'name': 'ИП Штин Антон Владимирович', 'identifier': {'@type': 'PropertyValue', 'propertyID': 'ОГРНИП', 'value': OGRNIP}}}

def esc(t): return html.escape(t, quote=True)
def strip(s): return re.sub(r'<[^>]+>', '', s)
def ld(*o): return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': list(o)}, ensure_ascii=False) + '</script>'
def faq_ld(items, url): return {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': strip(a)}} for q, a in items]}
def faq_html(items): return '<div class="faq">' + ''.join(f'<details><summary>{esc(q)}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in items) + '</div>'
def crumbs_ld(items): return {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': BASE + '/' + u} for i, (u, n) in enumerate(items)]}

def page(fname, title, desc, body, schema, current=None):
    url = BASE + '/' + ('' if fname == 'index.html' else fname)
    AC = ' aria-current="page"'
    nav = ''.join(f'<a href="{u}"{AC if u == current else ""}>{n}</a>' for u, n in NAV)
    menu = ''.join(f'<a href="{u}">{n}</a>' for u, n in NAV)
    doc = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="Медуправа">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/og-hub-v2.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F3F1EA">
<link rel="icon" href="assets/meduprava-znak.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/fonts.css">
<link rel="stylesheet" href="assets/hub.css?v={CSSV}">
{ld(*schema)}
</head>
<body>
<a class="skip" href="#main">К содержанию</a>
<header class="top">
  <div class="wrap top__in">
    <a class="brand" href="index.html" aria-label="Медуправа, на главную"><img src="assets/meduprava-logo.svg" alt="Медуправа" width="271" height="64"></a>
    <nav class="nav" aria-label="Разделы">{nav}</nav>
    <a class="btn" href="index.html#contacts">Связаться</a>
    <details class="menu"><summary>Меню</summary><div class="menu__list">{menu}<a href="mailto:{EMAIL}">{EMAIL}</a></div></details>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap foot__grid">
    <div>
      <b>Медуправа</b>
      <p>Право, финансы и операционное управление частных медицинских клиник. Москва, Московская область, дистанционно по всей России.</p>
      <p>Исполнитель: ИП Штин Антон Владимирович, ОГРНИП {OGRNIP}. Информация на сайте не является публичной офертой. Прямой результат по спорам и проверкам не гарантируется.</p>
      <p><a href="legal/privacy.html">Политика обработки персональных данных</a> · <a href="legal/cookies.html">Cookie</a></p>
    </div>
    <div><b>Направления</b><ul>
      <li><a href="pravo.html">Юридическое</a></li>
      <li><a href="finance.html">Финансовое</a></li>
      <li><a href="servis.html">Операционное управление и сервис</a></li>
      <li><a href="ekspertiza-oms.html">Экспертиза актов по ОМС</a></li>
      <li><a href="kalkulyator-oms.html">Калькулятор потерь по ОМС</a></li></ul></div>
    <div><b>Связаться</b><ul>
      <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><a href="tel:{PHONE}">{PHONE_H}</a></li>
      <li><a href="{VK}" rel="noopener">ВКонтакте {VK_H}</a></li></ul></div>
  </div>
</footer>
<a class="btn btn--brass float" href="mailto:{EMAIL}">Написать в Медуправу</a>
</body>
</html>
'''
    (ROOT / fname).write_text(doc)

def cta(h='Расскажите о клинике', t='Опишите задачу в письме или сообщении. Ответим, с какого направления начать и какие документы понадобятся. Сведения о пациентах присылать не нужно.'):
    return f'''<section class="sec sec--ink" id="contacts"><div class="wrap cols" style="align-items:center">
  <div><p class="over">Первый шаг</p><h2>{h}</h2><p class="lead" style="color:var(--on-ink)">{t}</p></div>
  <div class="hero__cta" style="margin:0;flex-direction:column;align-items:flex-start">
    <a class="btn btn--brass" href="mailto:{EMAIL}">Написать на {EMAIL}</a>
    <a class="btn btn--line" style="color:var(--on-ink);border-color:var(--on-ink-2)" href="tel:{PHONE}">Позвонить {PHONE_H}</a>
    <a class="btn btn--line" style="color:var(--on-ink);border-color:var(--on-ink-2)" href="{VK}" rel="noopener">Сообщество ВКонтакте</a>
  </div>
</div></section>'''

# ---------------- Главная ----------------
HOME_FAQ = [
 ('Чем занимается Медуправа?', 'Мы сопровождаем частные медицинские клиники по трём направлениям: право, финансы, операционное управление и сервис. Выявляем проблемные места клиники, помогаем найти возможности и настраиваем бизнес-процессы так, чтобы клиника не теряла деньги на претензиях, проверках и ошибках в учёте.'),
 ('С каким регионом вы работаете?', 'Основной регион - Москва и Московская область. Большую часть работы выполняем дистанционно, поэтому работаем с клиниками по всей России; выезд в клинику - по договорённости.'),
 ('Нужно ли передавать вам сведения о пациентах?', 'Нет. Документы клиника готовит в нашей программе на своём компьютере: она закрывает ФИО, полис, СНИЛС, дату рождения, адрес и диагноз, в том числе на сканах, и собирает зашифрованный пакет. Если обезличить нельзя, заключаем соглашение об обработке персональных данных по 152-ФЗ.'),
 ('Можно ли подключить только одно направление?', 'Да. Каждое направление работает самостоятельно: можно заказать только экспертизу актов по ОМС, только финансового директора или только настройку службы сервиса. Комплексная диагностика полезна, когда непонятно, где клиника теряет больше.'),
 ('Сколько стоят услуги?', 'Стоимость зависит от объёма задачи и размера клиники. Есть разовые услуги и абонентские пакеты. Стоимость финансового направления указана на его странице, по остальным - называем после знакомства с задачей и до начала работы.'),
]

def home():
    url = BASE + '/'
    dirs = [('pravo.html', 'Юридическое', 'Претензии пациентов, экспертизы страховых по ОМС, договоры, лицензия, персональные данные и врачебная тайна.', 'Антон Штин, юрист'),
            ('finance.html', 'Финансовое', 'Управленческий учёт, деньги к сроку платежей, KPI персонала и финансовая модель клиники.', 'Елена Штин, финансовый директор'),
            ('servis.html', 'Операционное', 'Операционное управление и развитие клиники, служба сервиса и заботы о пациентах.', 'Дарья Гаврилова')]
    dcards = ''.join(f'<a class="card" href="{u}"><span class="tag" style="align-self:flex-start">{t}</span><h3>{t} направление</h3><p>{d}</p><p class="muted" style="margin:0">{w}</p><span class="card__more">Подробнее →</span></a>' for u, t, d, w in dirs)
    body = f'''<section class="hero"><div class="wrap hero__grid">
  <div>
    <p class="over">Москва · Московская область · дистанционно</p>
    <h1>Право, финансы и операционное управление частных медицинских клиник</h1>
    <p class="lead">Находим, где клиника теряет деньги: на претензиях пациентов, снятиях по ОМС, ошибках в учёте и рекламе. И настраиваем процессы так, чтобы потери не повторялись.</p>
    <div class="hero__cta"><a class="btn" href="#contacts">Обсудить задачу клиники</a><a class="btn btn--line" href="kalkulyator-oms.html">Посчитать потери по ОМС</a></div>
  </div>
  <div class="facts" aria-label="Команда">
    <div class="fact"><b>3 направления</b><span>право, финансы, операции и сервис - одна команда</span></div>
    <div class="fact"><b>20+ лет</b><span>в финансах - финансовый директор</span></div>
    <div class="fact"><b>Сервис</b><span>забота о пациентах как процесс, а не настроение</span></div>
    <div class="fact"><b>с 2020</b><span>юридическая практика руководителя направления</span></div>
  </div>
</div></section>
<section class="sec sec--white"><div class="wrap"><div class="brief"><p class="over">Кратко</p>
  <p><b>Медуправа</b> - команда юриста, финансового директора и руководителя операционного направления, которая сопровождает частные медицинские клиники в Москве, Московской области и дистанционно по всей России. Юридическое направление: претензии пациентов, экспертиза актов страховых компаний в рамках ОМС, договоры платных медицинских услуг, лицензия, персональные данные. Финансовое: управленческий учёт, финансовый директор на аутсорсе, финансовая модель. Операционное: управление и развитие клиники, служба сервиса и заботы о пациентах.</p></div></div></section>
<section class="sec"><div class="wrap">
  <div class="sec__head"><p class="over">Направления</p><h2>Три взгляда на одну клинику</h2><p class="lead">Юрист видит риск, финансист - его цену, операционное направление - как процесс устроен для пациента и команды. Каждое направление можно подключить отдельно.</p></div>
  <div class="grid grid--3">{dcards}</div>
</div></section>
<section class="sec sec--white"><div class="wrap cols">
  <div><p class="over">Диагностика клиники</p><h2>С чего начинается работа</h2>
    <p class="lead">Диагностика показывает проблемные места клиники в формате «проблема - риск - норма - решение». Отчёт остаётся у клиники, даже если дальше вы работаете сами.</p>
    <ul class="list" style="margin-top:20px">
      <li>Сведения о пациентах не покидают клинику: мы получаем только обезличенные документы.</li>
      <li>Документы сверяем с действующими редакциями нормативных актов, в том числе программными средствами.</li>
      <li>Нормативную базу проверяем еженедельно: 323-ФЗ, 326-ФЗ, 152-ФЗ, приказы Минздрава и ФФОМС.</li>
    </ul></div>
  <div><p class="over">Порядок</p><h2>Четыре шага</h2><div class="steps">
    <div class="step"><div><h3>Знакомство</h3><p>Обсуждаем задачу и определяем, какое направление нужно первым.</p></div></div>
    <div class="step"><div><h3>Пакет документов</h3><p>Клиника собирает обезличенный пакет по нашему перечню.</p></div></div>
    <div class="step"><div><h3>Анализ</h3><p>Юрист, финансист или руководитель операционного направления разбирают документы в своей части.</p></div></div>
    <div class="step"><div><h3>Отчёт и план</h3><p>Показываем проблемы, их цену и порядок исправления.</p></div></div>
  </div></div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec__head"><p class="over">Команда</p><h2>Кто работает с клиникой</h2></div>
  <div class="team">
    <div class="person"><div class="person__ph"><img src="assets/team/anton-shtin-v2.jpg" alt="Антон Штин, юрист" loading="lazy" width="900" height="1100"></div><div class="person__b"><span class="person__role">Право</span><h3>Антон Штин</h3><p>Юрист, руководитель юридического направления. Управленческий стаж с 2007 года, с 2020 года - частная юридическая практика, пять лет сопровождения медицинской клиники.</p></div></div>
    <div class="person"><div class="person__ph"><img src="assets/finance/elena-shtin-financial-director.jpg" alt="Елена Штин, финансовый директор" loading="lazy" width="900" height="1100"></div><div class="person__b"><span class="person__role">Финансы</span><h3>Елена Штин</h3><p>Финансовый директор. Более 20 лет в финансовой сфере: управленческий учёт, контроль денежных потоков, финансовые модели.</p></div></div>
    <div class="person"><div class="person__ph"><img src="assets/team/daria-gavrilova.jpg" alt="Дарья Гаврилова" loading="lazy" width="900" height="1100"></div><div class="person__b"><span class="person__role">Операционное управление и сервис</span><h3>Дарья Гаврилова</h3><p>Операционное управление и развитие, служба сервиса и заботы. Выстраивает путь пациента и работу команды клиники.</p></div></div>
  </div>
</div></section>
<section class="sec sec--white"><div class="wrap cols" style="align-items:center">
  <div><p class="over">Дела недели</p><h2>Разбираем ситуации клиник с трёх сторон</h2>
  <p class="lead">Каждую неделю в сообществе ВКонтакте - одно дело: юрист показывает риск, финансист считает цену, операционное направление показывает, как ситуацию видит пациент. Без имён, с нормами и цифрами.</p></div>
  <div class="hero__cta" style="margin:0"><a class="btn" href="{VK}" rel="noopener">Читать дела во ВКонтакте</a></div>
</div></section>
<section class="sec" id="faq"><div class="wrap"><div class="sec__head"><p class="over">Вопросы</p><h2>Частые вопросы</h2></div>{faq_html(HOME_FAQ)}</div></section>
{cta()}'''
    site = {'@type': 'WebSite', '@id': url + '#website', 'url': url, 'name': 'Медуправа', 'inLanguage': 'ru', 'publisher': {'@id': BASE + '/#org'}}
    page('index.html', 'Медуправа - юридическое, финансовое и операционное сопровождение медицинских клиник в Москве и МО',
         'Сопровождение частных медицинских клиник в Москве и Московской области: юрист, финансовый директор и операционное направление. Претензии пациентов, экспертиза актов по ОМС, управленческий учёт, служба сервиса и заботы о пациентах.',
         body, [site, ORG, faq_ld(HOME_FAQ, url)])

# ---------------- Право ----------------
PRAVO_FAQ = [
 ('Какой срок на обжалование акта экспертизы страховой компании?', 'Протокол разногласий направляется в страховую медицинскую организацию в течение 10 рабочих дней со дня получения заключения (п. 71.1 Порядка контроля, утв. приказом Минздрава России от 19.03.2021 № 231н). Претензию в территориальный фонд ОМС по результатам медико-экономической экспертизы и экспертизы качества можно направить в течение 15 рабочих дней (ч. 1 ст. 42 Федерального закона от 29.11.2010 № 326-ФЗ).'),
 ('Что грозит клинике, если претензию пациента оставить без ответа?', 'Если пациент - потребитель и его обоснованное требование не удовлетворено добровольно, суд взыщет с клиники штраф 50% от присуждённой суммы (п. 6 ст. 13 Закона РФ «О защите прав потребителей»), кроме случаев, прямо названных в законе. Письменный ответ в срок и зафиксированные предложения пациенту - основа защиты клиники.'),
 ('Кто подаёт протокол разногласий и претензию - клиника или вы?', 'Клиника, от своего имени. Мы готовим юридические документы - протокол разногласий, претензию, ответ пациенту, а клиника подписывает их и комплектует приложения. Так сведения о пациентах остаются в клинике.'),
 ('Можете ли вы оценить, правильно ли врач лечил пациента?', 'Нет. Мы не оцениваем качество лечения и не спорим с медицинскими решениями. Наша часть - процедура контроля, соответствие кода дефекта фактам и документам, сроки, договоры и согласия.'),
]

def pravo():
    url = BASE + '/pravo.html'
    items = [('Экспертиза актов страховых компаний в рамках ОМС', 'Разбор актов медико-экономической экспертизы и экспертизы качества, протокол разногласий в страховую и претензия в территориальный фонд.', 'ekspertiza-oms.html'),
             ('Претензии пациентов', 'Ответ на претензию в срок и по существу, переговоры, позиция для суда. Регламент работы с обращениями, чтобы жалоба не становилась спором.', None),
             ('Договор платных медицинских услуг', 'Договор и сопутствующие документы по Правилам, утв. постановлением Правительства РФ от 11.05.2023 № 736.', None),
             ('Информированное добровольное согласие', 'Согласия на вмешательство с перечнем типичных рисков по видам лечения (ст. 20 Федерального закона № 323-ФЗ), памятки после лечения.', None),
             ('Лицензия на медицинскую деятельность', 'Переоформление лицензии, исключение неиспользуемых работ и услуг, подготовка к проверкам.', None),
             ('Персональные данные и врачебная тайна', 'Политики и согласия по 152-ФЗ, правила ответов на отзывы без раскрытия врачебной тайны (ст. 13 323-ФЗ).', None),
             ('Договоры с подрядчиками', 'IT, маркетинг, продвижение на агрегаторах: риски по пунктам, протокол разногласий, права на результаты.', None),
             ('Трудовые вопросы персонала', 'Положение об оплате труда, премии с критериями, индексация, подготовка к проверкам трудовой инспекции.', None)]
    cards = ''.join(f'<{"a" if l else "div"} class="card"{f" href={chr(34)}{l}{chr(34)}" if l else ""}><h3>{t}</h3><p>{d}</p>{"<span class=card__more>Подробнее →</span>" if l else ""}</{"a" if l else "div"}>' for t, d, l in items)
    body = f'''<section class="page-hero"><div class="wrap media-hero"><div><nav class="crumbs" aria-label="Навигация"><a href="index.html">Главная</a> / Юридическое направление</nav>
<p class="over">Юридическое направление</p><h1>Юрист для медицинской клиники в Москве и Московской области</h1>
<p class="lead">Защищаем деньги и лицензию клиники: претензии пациентов, экспертизы страховых по ОМС, договоры и согласия. Начинаем с документов, которые уже есть, и показываем, где клиника уязвима.</p>
<div class="hero__cta"><a class="btn" href="#contacts">Обсудить задачу</a><a class="btn btn--line" href="ekspertiza-oms.html">Экспертиза актов по ОМС</a></div></div>
<img class="media-img" src="assets/pravo/rabota-s-dokumentami.jpg" alt="Юрист работает с документами клиники" width="900" height="1350" fetchpriority="high"></div></section>
<section class="sec"><div class="wrap"><div class="brief"><p class="over">Кратко</p><p>Юридическое направление Медуправы ведёт юрист Антон Штин. Услуги для частных медицинских клиник: экспертиза актов страховых компаний в рамках ОМС, ответы на претензии пациентов, договоры платных медицинских услуг, информированное добровольное согласие, лицензия на медицинскую деятельность, персональные данные и врачебная тайна, договоры с подрядчиками, трудовые вопросы персонала. Москва, Московская область, дистанционно по всей России.</p></div></div></section>
<section class="sec sec--white"><div class="wrap"><div class="sec__head"><p class="over">Услуги</p><h2>С чем приходят клиники</h2></div><div class="grid grid--2">{cards}</div></div></section>
<section class="sec"><div class="wrap cols">
  <div><img class="media-img media-img--wide" src="assets/pravo/yurist-za-rabotoy.jpg" alt="Антон Штин за работой" width="900" height="1350" loading="lazy" style="margin-bottom:28px">
  <p class="over">Кто ведёт направление</p><h2>Антон Штин, юрист</h2>
  <p>Управленческий стаж с 2007 года, с 2020 года - частная юридическая практика в сопровождении бизнеса. Пять лет юридически сопровождает медицинскую клинику: лицензирование, договоры, персональные данные и врачебная тайна, споры со страховой организацией по результатам экспертиз.</p>
  <p><a href="https://vk.ru/aresid" rel="noopener">Страница во ВКонтакте</a></p></div>
  <div><p class="over">Принцип</p><h2>Процедура, а не лечение</h2><p class="lead">Мы не оцениваем качество лечения и не спорим с медицинскими решениями. Наша часть - процедура контроля, соответствие кода дефекта фактам, сроки, договоры и согласия.</p></div>
</div></section>
<section class="sec sec--white" id="faq"><div class="wrap"><div class="sec__head"><p class="over">Вопросы</p><h2>Юрист для клиники: частые вопросы</h2></div>{faq_html(PRAVO_FAQ)}</div></section>
{cta('Пришлите вопрос юристу', 'Опишите ситуацию без сведений о пациентах. Ответим, какие документы нужны и какой срок у клиники на ответ.')}'''
    srv = {'@type': 'Service', '@id': url + '#service', 'name': 'Юридическое сопровождение медицинских клиник', 'serviceType': 'Медицинское право', 'provider': {'@id': BASE + '/#org'}, 'areaServed': AREA, 'url': url,
           'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Услуги юридического направления', 'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': t, 'description': d}} for t, d, _ in items]}}
    page('pravo.html', 'Юрист для медицинской клиники в Москве и МО - юридическое направление Медуправы',
         'Юрист для частной клиники: экспертиза актов страховых по ОМС, претензии пациентов, договор платных медицинских услуг, ИДС, лицензия, персональные данные и врачебная тайна. Москва, Московская область.',
         body, [ORG, srv, faq_ld(PRAVO_FAQ, url), crumbs_ld([('', 'Главная'), ('pravo.html', 'Юридическое направление')])], 'pravo.html')

# ---------------- Маркетинг ----------------
SERV_FAQ = [
 ('Что такое служба сервиса и заботы в клинике?', 'Это не отдельный сотрудник, а порядок: кто и в какой срок отвечает пациенту на каждом этапе - от записи до повторного визита, как фиксируются обращения и жалобы и кто получает их в тот же день. Чем раньше клиника услышит недовольство, тем дешевле его решить.'),
 ('Можно ли отвечать на негативный отзыв подробностями лечения?', 'Нет. Даже сам факт обращения за медицинской помощью составляет врачебную тайну (ст. 13 Федерального закона от 21.11.2011 № 323-ФЗ). Отвечать стоит коротко: выразить сожаление, предложить разобраться и дать контакт ответственного лица.'),
 ('Как операционное направление связано с юридическим?', 'Регламенты работы с обращениями, ответы на отзывы и стандарты информирования пациентов согласуются с юристом Медуправы: так сервис снижает число претензий и не создаёт новых рисков.'),
]

def servis():
    url = BASE + '/servis.html'
    items = [('Операционное управление', 'Регламенты работы администраторов и регистратуры, распределение задач, загрузка врачей и кабинетов, контроль исполнения.'),
             ('Развитие клиники', 'Запуск новых услуг и направлений, порядок изменений, чтобы рост не ломал текущую работу.'),
             ('Служба сервиса и заботы', 'Путь пациента от записи до повторного визита: напоминания, связь после приёма, ответственные на каждом этапе.'),
             ('Обращения и отзывы', 'Порядок приёма жалоб, сроки ответа, правила ответов на отзывы без раскрытия врачебной тайны.')]
    cards = ''.join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in items)
    body = f'''<section class="page-hero"><div class="wrap"><nav class="crumbs" aria-label="Навигация"><a href="index.html">Главная</a> / Операционное управление и сервис</nav>
<p class="over">Операционное направление</p><h1>Операционное управление клиникой и служба заботы о пациентах</h1>
<p class="lead">Многие претензии начинаются не с лечения, а с процесса: звонок не записали, ответ не дали, пациента не предупредили. Выстраиваем работу команды и путь пациента так, чтобы клиника росла без потерь на сервисе.</p>
<div class="hero__cta"><a class="btn" href="#contacts">Обсудить работу клиники</a></div></div></section>
<section class="sec"><div class="wrap"><div class="brief"><p class="over">Кратко</p><p>Операционное направление Медуправы ведёт Дарья Гаврилова: операционное управление и развитие частных клиник, служба сервиса и заботы о пациентах. Регламенты работы администраторов и регистратуры, путь пациента от записи до повторного визита, порядок работы с обращениями и отзывами. Работает в связке с юристом и финансовым директором Медуправы.</p></div></div></section>
<section class="sec sec--white"><div class="wrap"><div class="sec__head"><p class="over">Что делаем</p><h2>Процессы, которые пациент чувствует сразу</h2></div><div class="grid grid--2">{cards}</div></div></section>
<section class="sec"><div class="wrap cols" style="align-items:center">
  <div class="person" style="max-width:420px"><div class="person__ph"><img src="assets/team/daria-gavrilova.jpg" alt="Дарья Гаврилова" loading="lazy" width="900" height="1100"></div><div class="person__b"><span class="person__role">Операционное управление и сервис</span><h3>Дарья Гаврилова</h3><p>Операционное управление и развитие, служба сервиса и заботы.</p></div></div>
  <div><p class="over">Подход</p><h2>Сервис - это порядок, а не настроение</h2><p class="lead">У каждого этапа пути пациента есть ответственный и срок. Тогда забота не зависит от того, кто сегодня на смене.</p></div>
</div></section>
<section class="sec sec--white" id="faq"><div class="wrap"><div class="sec__head"><p class="over">Вопросы</p><h2>Операции и сервис: частые вопросы</h2></div>{faq_html(SERV_FAQ)}</div></section>
{cta('Расскажите, как устроена работа клиники', 'Опишите, где сейчас теряется время или недовольны пациенты. Ответим, с чего начать.')}'''
    srv = {'@type': 'Service', '@id': url + '#service', 'name': 'Операционное управление и служба сервиса медицинской клиники', 'serviceType': 'Операционное управление', 'provider': {'@id': BASE + '/#org'}, 'areaServed': AREA, 'url': url}
    page('servis.html', 'Операционное управление клиникой и служба заботы о пациентах - Медуправа',
         'Операционное управление и развитие частной клиники, служба сервиса и заботы о пациентах: регламенты администраторов, путь пациента, работа с обращениями и отзывами. Москва, Московская область.',
         body, [ORG, srv, faq_ld(SERV_FAQ, url), crumbs_ld([('', 'Главная'), ('servis.html', 'Операционное управление и сервис')])], 'servis.html')

def extras():
    pages = [('', '1.0'), ('pravo.html', '0.9'), ('finance.html', '0.9'), ('servis.html', '0.8'), ('ekspertiza-oms.html', '0.9'), ('kalkulyator-oms.html', '0.6'),
             ('legal/privacy.html', '0.2'), ('legal/consent.html', '0.2'), ('legal/privacy-finance.html', '0.2'), ('legal/consent-finance.html', '0.2'), ('legal/cookies.html', '0.2'), ('legal/obezlichivanie.html', '0.2')] + [('shtin/' + x, '0.7') for x in ['', 'uslugi.html', 'grazhdanskie-spory.html', 'trudovye-spory.html', 'medicinskoe-pravo.html', 'soprovozhdenie-biznesa.html', 'yurist-po-dtp.html', 'praktika.html', 'razbory.html', 'razbor-beremennye-rabotnicy.html', 'razbor-rabotniki-s-detmi.html', 'razbor-predpensionery-i-pensionery.html', 'razbor-sokrashchenie-shtata.html', 'razbor-soglashenie-storon.html', 'razbor-pravilo-uvolneniya.html', 'razbor-udalenka-vmesto-filiala.html', 'razbor-klishe-podpisi.html', 'razbor-nedovolnyy-klient.html', 'o-yuriste.html', 'voprosy.html', 'kontakty.html']]
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        ''.join(f'  <url><loc>{BASE}/{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n' for p, pr in pages) + '</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\n# Поисковые и ИИ-ассистенты: доступ открыт\nUser-agent: YandexBot\nAllow: /\nUser-agent: GPTBot\nAllow: /\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n')
    (ROOT / 'llms.txt').write_text(f'''# Медуправа - право, финансы и операционное управление частных медицинских клиник

> Медуправа - команда юриста, финансового директора и руководителя операционного направления, которая сопровождает частные медицинские клиники в Москве, Московской области и дистанционно по всей России. Исполнитель: ИП Штин Антон Владимирович (ОГРНИП {OGRNIP}). Контакты: {EMAIL}, {PHONE_H}, ВКонтакте {VK_H}.

## Команда
- Антон Штин - юрист, руководитель юридического направления; частная юридическая практика с 2020 года, пять лет сопровождения медицинской клиники.
- Елена Штин - финансовый директор; более 20 лет в финансовой сфере.
- Дарья Гаврилова - операционное управление и развитие, служба сервиса и заботы.

## Страницы
- [Юридическое направление]({BASE}/pravo.html): экспертиза актов страховых компаний в рамках ОМС, претензии пациентов, договор платных медицинских услуг, информированное добровольное согласие, лицензия, персональные данные и врачебная тайна.
- [Экспертиза актов страховых компаний в рамках ОМС]({BASE}/ekspertiza-oms.html): протокол разногласий (10 рабочих дней, п. 71.1 Порядка контроля, приказ Минздрава России № 231н) и претензия в ТФОМС (15 рабочих дней, ст. 42 326-ФЗ).
- [Финансовый директор для клиник]({BASE}/finance.html): управленческий учёт, денежные потоки, KPI персонала, финансовая модель; стоимость услуг указана на странице.
- [Операционное управление и сервис]({BASE}/servis.html): операционное управление и развитие клиники, служба сервиса и заботы о пациентах, регламент работы с обращениями и отзывами.
- [Калькулятор потерь по ОМС]({BASE}/kalkulyator-oms.html)

## Принципы
- Сведения о пациентах не передаются: клиника обезличивает документы в программе на своём компьютере.
- Качество лечения не оценивается; предмет работы - процедура контроля, документы, сроки, деньги клиники.

## Связанные сайты
- [Антон Штин, юрист (Красногорск)]({BASE}/shtin/): личная страница руководителя юридического направления - гражданские и трудовые споры, медицинское право, сопровождение бизнеса; подробности - {BASE}/shtin/llms.txt
''')

home(); pravo(); servis(); extras()
print('ok')
