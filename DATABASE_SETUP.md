# Инструкция по настройке базы данных

## Быстрый старт

1. **Установите PostgreSQL** (если еще не установлен):
```bash
brew install postgresql@14
```

2. **Запустите PostgreSQL**:
```bash
brew services start postgresql@14
```

3. **Создайте базу данных** (автоматически):
```bash
source venv/bin/activate
cd app
python db/create_database.py
```

4. **Таблицы создадутся автоматически** при первом запуске бота, или вручную:
```bash
python db/init_tables.py
```

## Подробная инструкция

### 1. Проверка установки PostgreSQL

```bash
# Проверить, установлен ли PostgreSQL
which psql

# Проверить версию
psql --version
```

Если PostgreSQL не установлен:
```bash
brew install postgresql@14
```

### 2. Запуск PostgreSQL

```bash
# Запустить службу PostgreSQL
brew services start postgresql@14

# Проверить статус
brew services list | grep postgres

# Остановить (если нужно)
brew services stop postgresql@14
```

### 3. Настройка пользователя и пароля

По умолчанию PostgreSQL создает пользователя с именем вашего macOS пользователя. 

**Вариант 1: Использовать текущего пользователя**

Измените `DATABASE_URL` в `app/env.py`:
```python
DATABASE_URL = 'postgresql+psycopg://YOUR_USERNAME@localhost:5432/rainlbrows'
```

**Вариант 2: Создать пользователя postgres**

```bash
# Создать пользователя postgres (если не существует)
createuser -s postgres

# Установить пароль
psql -U YOUR_USERNAME -d postgres
ALTER USER postgres WITH PASSWORD 'postgres';
\q
```

### 4. Создание базы данных

**Автоматический способ (рекомендуется):**

```bash
source venv/bin/activate
cd app
python db/create_database.py
```

**Ручной способ:**

```bash
# Подключиться к PostgreSQL
psql -U postgres -d postgres

# Создать базу данных
CREATE DATABASE rainlbrows;

# Выйти
\q
```

Или одной командой:
```bash
psql -U postgres -d postgres -c "CREATE DATABASE rainlbrows;"
```

### 5. Создание таблиц

**Автоматически при запуске бота:**

Таблицы создадутся автоматически при первом запуске бота (`python main.py`).

**Вручную:**

```bash
source venv/bin/activate
cd app
python db/init_tables.py
```

### 6. Проверка

```bash
# Подключиться к базе данных
psql -U postgres -d rainlbrows

# Показать все таблицы
\dt

# Показать структуру таблицы users
\d users

# Показать структуру таблицы offers
\d offers

# Выйти
\q
```

## Решение проблем

### Ошибка: "connection refused"

**Проблема:** PostgreSQL не запущен

**Решение:**
```bash
brew services start postgresql@14
```

### Ошибка: "password authentication failed"

**Проблема:** Неправильный пароль или пользователь

**Решение:**
1. Проверьте `DATABASE_URL` в `app/env.py`
2. Убедитесь, что пользователь существует:
```bash
psql -U YOUR_USERNAME -d postgres -c "\du"
```

### Ошибка: "database does not exist"

**Проблема:** База данных не создана

**Решение:**
```bash
cd app
python db/create_database.py
```

### Ошибка: "permission denied"

**Проблема:** Пользователь не имеет прав на создание базы данных

**Решение:**
```bash
# Создать суперпользователя
createuser -s postgres

# Или использовать текущего пользователя (он уже суперпользователь)
```

## Настройка для продакшена

Для продакшена рекомендуется:

1. **Использовать отдельного пользователя** (не postgres):
```sql
CREATE USER rainlbrows_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE rainlbrows TO rainlbrows_user;
```

2. **Использовать переменные окружения** вместо хардкода в `env.py`:
```python
import os
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg://...')
```

3. **Настроить бэкапы** базы данных

4. **Использовать миграции Alembic** для управления схемой БД

