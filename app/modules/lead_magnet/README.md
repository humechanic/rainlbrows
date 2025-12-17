# Модуль урока

Этот модуль отправляет видео урок пользователям. Поддерживается три способа отправки видео:

## Вариант 1: YouTube ссылка (рекомендуется)

Самый простой способ - просто указать ссылку на YouTube видео.

1. Откройте `app/modules/lesson/config.py`
2. Укажите ссылку в `LESSON_YOUTUBE_URL`:
```python
LESSON_YOUTUBE_URL = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
# Или короткая ссылка:
LESSON_YOUTUBE_URL = "https://youtu.be/YOUR_VIDEO_ID"
```

## Вариант 2: Telegram video по file_id

Если видео уже загружено в Telegram, можно использовать `file_id` для отправки без повторной загрузки.

### Как получить file_id:

**Способ 1: Через бота**
1. Отправьте видео вашему боту (в личные сообщения боту)
2. Добавьте временный обработчик в `main.py`:
```python
async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.video:
        file_id = update.message.video.file_id
        print(f"Video file_id: {file_id}")
        await update.message.reply_text(f"File ID: {file_id}")
```

3. Запустите бота и отправьте видео
4. Скопируйте `file_id` из ответа бота
5. Вставьте в `config.py`:
```python
LESSON_TELEGRAM_VIDEO_FILE_ID = "BAACAgIAAxkBAAIBY2..."
```

**Способ 2: Через @userinfobot или @getidsbot**
- Отправьте видео этим ботам, они покажут file_id

**Способ 3: Через API**
- Используйте `getUpdates` API для получения file_id из сообщения

### Использование file_id:

В `config.py`:
```python
LESSON_TELEGRAM_VIDEO_FILE_ID = "BAACAgIAAxkBAAIBY2..."
```

**Преимущества file_id:**
- Быстрая отправка (не нужно загружать файл)
- Не занимает место на сервере
- Работает мгновенно

**Недостатки:**
- file_id может стать недействительным, если файл удален из Telegram
- Нужно сначала загрузить видео в Telegram

## Вариант 3: Локальный файл (загрузка с диска)

Если у вас есть видео файл на сервере, можно загрузить его напрямую.

1. Поместите видео файл в проект (например, `app/lessons/lesson_video.mp4`)
2. В `config.py` укажите путь:
```python
LESSON_VIDEO_FILE_PATH = "app/lessons/lesson_video.mp4"
# Или абсолютный путь:
LESSON_VIDEO_FILE_PATH = "/path/to/your/video.mp4"
```

**Ограничения Telegram:**
- Максимальный размер видео: 50 MB (для обычных ботов)
- Для ботов с повышенными лимитами: до 2 GB
- Поддерживаемые форматы: MP4, MOV, AVI и др.

## Приоритет отправки

Обработчик проверяет варианты в следующем порядке:
1. YouTube ссылка (если указана и не равна дефолтной)
2. Telegram file_id (если указан)
3. Локальный файл (если путь указан и файл существует)
4. Fallback сообщение (если ничего не настроено)

## Примеры конфигурации

### Только YouTube:
```python
LESSON_YOUTUBE_URL = "https://youtu.be/dQw4w9WgXcQ"
LESSON_TELEGRAM_VIDEO_FILE_ID = None
LESSON_VIDEO_FILE_PATH = None
```

### Только Telegram file_id:
```python
LESSON_YOUTUBE_URL = None
LESSON_TELEGRAM_VIDEO_FILE_ID = "BAACAgIAAxkBAAIBY2..."
LESSON_VIDEO_FILE_PATH = None
```

### Только локальный файл:
```python
LESSON_YOUTUBE_URL = None
LESSON_TELEGRAM_VIDEO_FILE_ID = None
LESSON_VIDEO_FILE_PATH = "lessons/my_lesson.mp4"
```

## Рекомендации

- **Для начала**: используйте YouTube ссылку - это самый простой способ
- **Для продакшена**: если видео приватное, используйте Telegram file_id или локальный файл
- **Для больших файлов**: используйте YouTube или загрузите в Telegram и используйте file_id

