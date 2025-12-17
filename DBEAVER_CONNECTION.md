# Инструкция по подключению к базе данных через DBeaver

## Параметры подключения

Из файла `app/env.py`:
- **Host:** `localhost`
- **Port:** `5432`
- **Database:** `rainlbrows`
- **Username:** `postgres`
- **Password:** `postgres`

## Шаги подключения в DBeaver

1. **Откройте DBeaver**

2. **Создайте новое подключение:**
   - Нажмите на иконку "New Database Connection" (или `Cmd+Shift+N` на Mac)
   - Выберите **PostgreSQL**

3. **Заполните параметры подключения:**
   - **Host:** `localhost`
   - **Port:** `5432`
   - **Database:** `rainlbrows`
   - **Username:** `postgres`
   - **Password:** `postgres`
   - **Show all databases:** оставьте выключенным

4. **Нажмите "Test Connection"**
   - Если появится ошибка о драйвере, DBeaver предложит скачать его автоматически
   - Нажмите "Download" и дождитесь установки

5. **Сохраните подключение:**
   - Нажмите "Finish"
   - Подключение появится в списке слева

## Проверка подключения

После подключения вы должны увидеть:
- База данных `rainlbrows`
- Таблицы:
  - `users` - пользователи Telegram
  - `offers` - предложения и напоминания

## Возможные проблемы

### Ошибка: "Connection refused"

**Причина:** PostgreSQL не запущен

**Решение:**
```bash
brew services start postgresql@14
```

### Ошибка: "password authentication failed"

**Причина:** Неправильный пароль

**Решение:**
1. Проверьте пароль в `app/env.py`
2. Или сбросьте пароль:
```bash
psql -U postgres -d postgres
ALTER USER postgres WITH PASSWORD 'postgres';
\q
```

### Ошибка: "database does not exist"

**Причина:** База данных не создана

**Решение:**
```bash
cd app
source ../venv/bin/activate
python db/create_database.py
```

### Ошибка: "FATAL: password authentication failed for user"

**Причина:** Пользователь `postgres` не существует или имеет другой пароль

**Решение:**
1. Проверьте, какой пользователь используется в вашей системе:
```bash
psql -U $(whoami) -d postgres
```

2. Если нужно создать пользователя postgres:
```bash
createuser -s postgres
psql -U postgres -d postgres
ALTER USER postgres WITH PASSWORD 'postgres';
\q
```

3. Или измените `DATABASE_URL` в `app/env.py` на вашего пользователя:
```python
DATABASE_URL = 'postgresql+psycopg://YOUR_USERNAME@localhost:5432/rainlbrows'
```

## Полезные SQL запросы

После подключения вы можете выполнять SQL запросы:

```sql
-- Показать всех пользователей
SELECT * FROM users;

-- Показать все предложения
SELECT * FROM offers;

-- Показать активные предложения с информацией о пользователях
SELECT 
    u.telegram_id,
    u.first_name,
    u.nickname,
    o.offer_expiration_date,
    o.lesson_clicked_at,
    o.first_reminder_sent,
    o.second_reminder_sent,
    o.is_active
FROM offers o
JOIN users u ON o.user_id = u.id
WHERE o.is_active = true;

-- Показать пользователей, которые кликнули урок, но еще не получили первое напоминание
SELECT 
    u.telegram_id,
    u.first_name,
    o.lesson_clicked_at,
    o.first_reminder_sent
FROM offers o
JOIN users u ON o.user_id = u.id
WHERE o.lesson_clicked_at IS NOT NULL
  AND o.first_reminder_sent IS NULL
  AND o.is_active = true;
```

