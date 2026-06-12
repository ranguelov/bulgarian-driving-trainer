# Контекст проекта: ПДД Тренажор (Болгария)

## Что это
Веб-приложение для подготовки к болгарскому экзамену по ПДД. Single-page app на vanilla HTML/CSS/JS, задеплоенное на Cloudflare Workers.

## URL и репозиторий
- **Прод**: https://bulgarian-driving-trainer.gurd-6ab.workers.dev
- **GitHub**: https://github.com/ranguelov/bulgarian-driving-trainer.git
- **Локальный путь**: `/Users/veterduetnam/Documents/Claude/Projects/PDD Tickets/bulgarian-driving-trainer/`

## Стек
- **Cloudflare Workers** + **KV** (ADMIN_KV) + **R2** (MEDIA_BUCKET)
- Деплой: `npx wrangler deploy` (из папки проекта)
- Все ассеты — статические файлы в папке проекта

## Ключевые файлы
- `index.html` — весь фронтенд (один файл, ~2100 строк)
- `worker.js` — Cloudflare Worker (роутинг, API, отдача ассетов)
- `questions.js` — база вопросов (1514 вопросов, 19 тем)
- `admin-review.html` — панель редактирования вопросов
- `images/` — картинки вопросов (SVG для T4, PNG для остальных)
- `images/hero-car2.mp4` — анимация на главной (машина вращается)

## Текущее состояние UI

### Главная страница (#s-home)
- Фон: `#E1DCE7` (лавандовый)
- Хедер: шестерёнка (открывает шторку настроек) + title + BG/RU переключатель
- Hero: видео `hero-car2.mp4` с `mix-blend-mode: multiply` + заголовок
- Кнопка "Започни изпит" → экзамен
- Блок "Обучение": карточки "Трениране по теми" и "Работа върху грешките"
- **Шторка настроек** (bottom sheet): открывается по шестерёнке, содержит:
  - "База знания" → переход в `/admin-review.html`
  - Toggle "Случаен ред в отговорите"

### Экран вопросов (#s-quiz)
- Фон: `linear-gradient(to bottom, #ffffff 0%, #ebeeee 100%)`
- Навигация по вопросам (пагинация сверху)
- Изображения вопросов из `images/questions/`
- theme-color меняется динамически: главная=#E1DCE7, квиз=#ffffff

## Важные технические детали
- `questions.js` содержит массив объектов с полями: `topic`, `question`, `answers`, `correct`, `images`
- T4 изображения сохранены как `.svg` (не `.png`!)
- `quiz-engine.js` — логика квиза (weakSpots, randomMode, applyTextOverrides)
- Языки: BG (болгарский) и RU (русский), словари внутри `index.html`
- Git часто имеет `.git/index.lock` — нужно удалять вручную: `rm ".git/index.lock"`

## Последние изменения (июнь 2026)
1. Заменили иконку шестерёнки на bottom sheet с настройками
2. Добавили видео-анимацию машины на главной (с seamless loop и crop)
3. Изменили фон главной на `#E1DCE7`, квиза — на белый градиент
4. Переключатель случайного порядка перенесён в шторку
5. Убраны blob-анимации фона
6. theme-color meta тег обновляется динамически при навигации
