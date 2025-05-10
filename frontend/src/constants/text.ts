export const HOME_PAGE_MESSAGE =
  "Заполните форму данными, на основе которых вы хотите проанализировать сайт:";

export const SEO_PARAMS = [
  {
    key: "favicon",
    title: "Favicon",
    description:
      "Маленькая иконка сайта, отображающаяся в браузере рядом с заголовком вкладки. Улучшает узнаваемость бренда и повышает доверие пользователей.",
    positiveResultText: "Сайт использует иконку",
    negativeResultText: "Отсутствует файл favicon",
  },
  {
    key: "robots",
    title: "Robots.txt",
    description:
      "Файл, указывающий поисковым роботам, какие страницы сканировать, а какие — игнорировать. Помогает управлять индексацией и защитить внутренние или дублирующиеся страницы.",
    positiveResultText: "Сайт использует файл robots.txt",
    negativeResultText: "Отсутствует файл robots.txt",
  },
  {
    key: "sitemap",
    title: "Sitemap.xml",
    description:
      "Карта сайта, содержащая список всех важных страниц. Облегчает поисковым системам сканирование и индексацию содержимого.",
    positiveResultText: "Сайт имеет файл sitemap.xml",
    negativeResultText: "Отсутствует файл sitemap.xml",
  },
  {
    key: "title",
    title: "Название",
    description:
      "Тег <title> отображается в результатах поиска и на вкладке браузера. Влияет на кликабельность (CTR) и помогает поисковикам понять тему страницы.",
    positiveResultText: "Сайт использует тег <title/>",
    negativeResultText: "Отсутствует тег <title/>",
  },
  {
    key: "description",
    title: "Описание",
    description:
      'Мета-тег <meta name="description"> показывает краткое описание страницы в поисковой выдаче. Может повлиять на кликабельность и привлечение трафика.',
    positiveResultText: "Сайт использует тег <meta description/>",
    negativeResultText: "Отсутствует тег <meta description/>",
  },
  {
    key: "socials",
    title: "Социальные сети",
    description:
      "OpenGraph и другие теги (например, Twitter Cards) обеспечивают корректное отображение страницы при её расшаривании в соцсетях. Это улучшает внешний вид публикаций и может повысить трафик.",
    positiveResultText: "Сайт использует теги для социальных сетей",
    negativeResultText:
      "Сайт не использует все необходимые теги для социальных сетей",
  },
  {
    key: "imageSeo",
    title: "Image SEO",
    description:
      "Атрибут alt у изображений помогает поисковым системам понимать содержание изображений и делает сайт доступным для пользователей с нарушениями зрения.",
    positiveResultText: "Атрибут Alt присутсвует у всех изображений",
    negativeResultText: "Атрибут Alt присутсвует не у всех изображений",
  },
  {
    key: "inlineCode",
    title: "Inline code",
    description:
      "Встроенные стили и скрипты затрудняют кэширование и повторное использование кода, а также могут ухудшать производительность и структуру страницы для поисковиков.",
    positiveResultText: "Отсутствует встроенный в html код или стили",
    negativeResultText: "Присутствует встроенный в html код или стили",
  },
  {
    key: "h1Missing",
    title: "Заголовок H1",
    description:
      "Тег <h1> обозначает основной заголовок страницы. Он помогает поисковым системам понять основную тему страницы и должен быть уникальным на каждой странице.",
    positiveResultText: "Все страницы имеют тег <h1/>",
    negativeResultText: "Не все страницы имеют тег <h1/>",
  },
  {
    key: "brokenLinks",
    title: "Сломанные ссылки",
    description:
      "Неработающие (битые) ссылки негативно влияют на пользовательский опыт и могут снизить доверие поисковых систем к сайту.",
    positiveResultText: "Нет сломанных ссылок",
    negativeResultText: "Присутствуют сломанные ссылки",
  },
  {
    key: "canonicalUrl",
    title: "Канонический URL",
    description:
      'Канонический тег <link rel="canonical"> сообщает поисковым системам, какая версия страницы является основной, предотвращая дублирование контента.',
    positiveResultText: "На странице указан канонический URL",
    negativeResultText: "Канонический URL отсутствует",
  },
  {
    key: "structuredData",
    title: "Структурированные данные",
    description:
      "Структурированные данные (schema.org, JSON-LD) помогают поисковым системам лучше понимать содержание страницы и позволяют отображать расширенные сниппеты в выдаче.",
    positiveResultText: "На странице присутствуют структурированные данные",
    negativeResultText: "Отсутствуют структурированные данные",
  },
  {
    key: "charset",
    title: "Кодировка страницы",
    description:
      "Указание кодировки (например, UTF-8) в мета-теге предотвращает проблемы с отображением текста и влияет на корректную индексацию.",
    positiveResultText: "Указана кодировка UTF-8",
    negativeResultText: "Кодировка не указана или указана некорректно",
  },
  {
    key: "doctype",
    title: "Doctype",
    description:
      "Тег <!DOCTYPE> сообщает браузеру, в каком стандарте написан HTML-код. Отсутствие этого тега может вызвать проблемы с отображением страницы.",
    positiveResultText: "Указан doctype",
    negativeResultText: "Doctype отсутствует",
  },
  {
    key: "noindex",
    title: "Мета-тег noindex",
    description:
      "Мета-тег noindex предотвращает индексацию страницы поисковыми системами. Полезен для страниц, не предназначенных для публичного поиска.",
    positiveResultText: "На неиндексируемых страницах установлен тег noindex",
    negativeResultText:
      "Отсутствует тег noindex на страницах, которые не должны индексироваться",
  },
  {
    key: "flashContent",
    title: "Flash-контент",
    description:
      "Использование Flash устарело и не поддерживается большинством современных браузеров. Его наличие негативно влияет на пользовательский опыт и SEO.",
    positiveResultText: "Flash-контент не используется",
    negativeResultText: "На сайте используется устаревший Flash-контент",
  },
  {
    key: "framesetUsed",
    title: "Использование <frameset>",
    description:
      "Элемент <frameset> является устаревшим и мешает корректной индексации сайта. Его использование не рекомендуется.",
    positiveResultText: "Элемент <frameset> не используется",
    negativeResultText: "На сайте используется элемент <frameset>",
  },
];

export const PERFORMANCE_PARAMS = [
  {
    key: "domSize",
    title: "Размер DOM",
    description:
      "Количество элементов в DOM влияет на производительность страницы. Слишком большой DOM может замедлить загрузку и рендеринг.",
    positiveResultText: "Размер DOM находится в пределах нормы",
    negativeResultText: "DOM содержит слишком много элементов",
  },
  {
    key: "htmlSize",
    title: "Размер HTML-страницы",
    description:
      "Чем меньше размер HTML-файла, тем быстрее он загружается. Большой размер может повлиять на время отклика и индексируемость.",
    positiveResultText: "Размер HTML-файла оптимален",
    negativeResultText: "HTML-файл слишком большой",
  },
  {
    key: "htmlCompression",
    title: "Сжатие HTML",
    description:
      "Сжатие HTML (например, через GZIP) позволяет уменьшить объем передаваемых данных и ускорить загрузку страницы.",
    positiveResultText: "HTML-файл сжимается на сервере",
    negativeResultText: "Сжатие HTML-файла отсутствует",
  },
  {
    key: "uncachedJs",
    title: "Кэширование JS-файлов",
    description:
      "Настроенное кэширование JavaScript-файлов уменьшает количество загрузок и ускоряет работу сайта при повторных посещениях.",
    positiveResultText: "Кэширование JavaScript-файлов настроено",
    negativeResultText: "Отсутствует кэширование JavaScript-файлов",
  },
  {
    key: "uncachedCss",
    title: "Кэширование CSS-файлов",
    description:
      "Кэширование CSS-файлов позволяет повторно использовать стили без повторной загрузки, что улучшает производительность.",
    positiveResultText: "Кэширование CSS-файлов настроено",
    negativeResultText: "Отсутствует кэширование CSS-файлов",
  },
  {
    key: "unminifiedCss",
    title: "Минификация CSS",
    description:
      "Минификация CSS удаляет лишние пробелы и комментарии, уменьшая объем файлов и ускоряя загрузку.",
    positiveResultText: "CSS-файлы минифицированы",
    negativeResultText: "CSS-файлы не минифицированы",
  },
  {
    key: "unminifiedJs",
    title: "Минификация JS",
    description:
      "Минификация JavaScript уменьшает размер файлов и повышает производительность сайта.",
    positiveResultText: "JavaScript-файлы минифицированы",
    negativeResultText: "JavaScript-файлы не минифицированы",
  },
  {
    key: "uncachedImages",
    title: "Кэширование изображений",
    description:
      "Кэширование изображений снижает нагрузку на сервер и ускоряет повторную загрузку страниц пользователями.",
    positiveResultText: "Изображения кэшируются корректно",
    negativeResultText: "Некоторые изображения не кэшируются",
  },
  {
    key: "oversizedImages",
    title: "Размер изображений",
    description:
      "Слишком большие изображения замедляют загрузку страниц и потребляют трафик. Их следует оптимизировать.",
    positiveResultText: "Размер изображений в пределах нормы",
    negativeResultText: "Некоторые изображения слишком большие",
  },
];

export const SECURITY_AND_SERVER_PARAMS = [
  {
    key: "unsafeLinks",
    title: "Небезопасные ссылки",
    description:
      'Ссылки на внешние ресурсы без параметра rel="noopener noreferrer" могут представлять угрозу безопасности, особенно при использовании target="_blank".',
    positiveResultText: "Все внешние ссылки безопасны",
    negativeResultText: "На сайте есть небезопасные внешние ссылки",
  },
  {
    key: "spfRecord",
    title: "SPF-запись",
    description:
      "SPF (Sender Policy Framework) — это запись в DNS, которая указывает, какие серверы могут отправлять электронную почту от имени домена. Это важно для защиты от подделки отправителя (spoofing).",
    positiveResultText: "SPF-запись настроена правильно",
    negativeResultText: "Отсутствует SPF-запись или она настроена некорректно",
  },
  {
    key: "http2Support",
    title: "Поддержка HTTP/2",
    description:
      "HTTP/2 — это современная версия протокола HTTP, который улучшает производительность за счет множества оптимизаций, таких как мультиплексирование запросов, сжатие заголовков и более эффективное использование соединений. Поддержка HTTP/2 может существенно ускорить загрузку веб-страниц, уменьшив время отклика и нагрузку на сервер.",
    positiveResultText: "Сервер поддерживает протокол",
    negativeResultText: "Сервер не поддерживает протокол",
  },
];
