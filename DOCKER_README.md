# Docker Deployment Guide

Это руководство описывает развертывание Telegram-бота с использованием Docker для локальной разработки и продакшена.

## Оглавление

- [Требования](#требования)
- [Локальная разработка](#локальная-разработка)
- [Продакшен](#продакшен)
- [Управление контейнерами](#управление-контейнерами)
- [Troubleshooting](#troubleshooting)

---

## Требования

- Docker Engine 20.10+
- Docker Compose 2.0+
- Для продакшена: внешняя PostgreSQL база данных

---

## Локальная разработка

### Шаг 1: Настройка переменных окружения

Создайте файл `.env` в корне проекта на основе `env.example`:

```bash
cp env.example .env
```

Отредактируйте `.env` и укажите ваши токены:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
PAYMENT_PROVIDER_TOKEN=your_payment_token
```

> **Примечание**: DATABASE_URL для локальной разработки настроен автоматически в `docker-compose.dev.yml`

### Шаг 2: Запуск контейнеров

```bash
docker-compose -f docker-compose.dev.yml up -d
```

Эта команда запустит:
- **PostgreSQL** (порт 5432) - база данных
- **Telegram Bot** - ваше приложение
- **pgAdmin** (порт 5050) - веб-интерфейс для управления БД

### Шаг 3: Проверка логов

```bash
# Логи приложения
docker-compose -f docker-compose.dev.yml logs -f app

# Логи PostgreSQL
docker-compose -f docker-compose.dev.yml logs -f postgres
```

### Шаг 4: Доступ к pgAdmin (опционально)

Откройте браузер: http://localhost:5050

- Email: `admin@admin.com`
- Password: `admin`

Подключение к БД:
- Host: `postgres`
- Port: `5432`
- Database: `rainlbrows`
- Username: `postgres`
- Password: `postgres`

### Остановка контейнеров

```bash
docker-compose -f docker-compose.dev.yml down
```

Для удаления данных БД:

```bash
docker-compose -f docker-compose.dev.yml down -v
```

---

## Продакшен

### Шаг 1: Подготовка внешней базы данных

Убедитесь, что у вас есть доступ к PostgreSQL базе данных с параметрами:
- Хост и порт (например, `db.example.com:5432`)
- Имя базы данных (например, `rainlbrows`)
- Пользователь и пароль

### Шаг 2: Настройка переменных окружения

Создайте файл `.env` на сервере:

```bash
nano .env
```

Укажите следующие параметры:

```env
# Telegram Bot
TELEGRAM_TOKEN=your_production_telegram_bot_token
PAYMENT_PROVIDER_TOKEN=your_production_payment_token

# External PostgreSQL Database
DATABASE_URL=postgresql+psycopg://dbuser:dbpassword@db.example.com:5432/rainlbrows
```

> **Важно**: Замените `dbuser`, `dbpassword`, `db.example.com` и `rainlbrows` на ваши реальные данные.

### Шаг 3: Сборка и запуск

```bash
# Сборка образа
docker-compose -f docker-compose.prod.yml build

# Запуск контейнера
docker-compose -f docker-compose.prod.yml up -d
```

### Шаг 4: Проверка работы

```bash
# Статус контейнера
docker-compose -f docker-compose.prod.yml ps

# Логи приложения
docker-compose -f docker-compose.prod.yml logs -f app

# Проверка healthcheck
docker inspect rainlbrows_app_prod | grep -A 10 Health
```

### Шаг 5: Автозапуск (systemd)

Создайте systemd service для автоматического запуска:

```bash
sudo nano /etc/systemd/system/rainlbrows-bot.service
```

Содержимое файла:

```ini
[Unit]
Description=Rainlbrows Telegram Bot
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/rainlbrows
ExecStart=/usr/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.prod.yml down
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Активируйте service:

```bash
sudo systemctl enable rainlbrows-bot
sudo systemctl start rainlbrows-bot
sudo systemctl status rainlbrows-bot
```

---

## Управление контейнерами

### Перезапуск

```bash
# Development
docker-compose -f docker-compose.dev.yml restart

# Production
docker-compose -f docker-compose.prod.yml restart app
```

### Обновление кода

```bash
# Development (код монтируется автоматически, просто перезапустите)
docker-compose -f docker-compose.dev.yml restart app

# Production
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

### Просмотр логов

```bash
# Последние 100 строк
docker-compose -f docker-compose.prod.yml logs --tail=100 app

# Следить за логами в реальном времени
docker-compose -f docker-compose.prod.yml logs -f app
```

### Вход в контейнер

```bash
# Development
docker-compose -f docker-compose.dev.yml exec app bash

# Production
docker-compose -f docker-compose.prod.yml exec app bash
```

### Проверка использования ресурсов

```bash
docker stats rainlbrows_app_prod
```

---

## Troubleshooting

### Проблема: Контейнер не запускается

**Решение:**
1. Проверьте логи:
   ```bash
   docker-compose -f docker-compose.prod.yml logs app
   ```
2. Проверьте переменные окружения в `.env`
3. Убедитесь, что база данных доступна

### Проблема: Не могу подключиться к базе данных

**Решение:**
1. Проверьте `DATABASE_URL` в `.env`
2. Проверьте доступность БД с сервера:
   ```bash
   docker-compose -f docker-compose.prod.yml exec app psql $DATABASE_URL
   ```
3. Проверьте firewall правила на сервере БД

### Проблема: База данных не инициализируется

**Решение:**
1. Проверьте права пользователя БД на создание таблиц
2. Вручную запустите инициализацию:
   ```bash
   docker-compose -f docker-compose.prod.yml exec app python -c "from app.db.init_db import init_db; init_db()"
   ```

### Проблема: Контейнер постоянно перезапускается

**Решение:**
1. Проверьте логи на наличие ошибок
2. Отключите healthcheck временно (закомментируйте в docker-compose.prod.yml)
3. Проверьте доступность Telegram API

### Проблема: Out of memory

**Решение:**
1. Увеличьте лимиты в `docker-compose.prod.yml`:
   ```yaml
   deploy:
     resources:
       limits:
         memory: 1024M  # Увеличьте это значение
   ```
2. Проверьте утечки памяти в логах

---

## Дополнительные команды

### Резервное копирование данных (Development)

```bash
# Backup PostgreSQL
docker-compose -f docker-compose.dev.yml exec postgres pg_dump -U postgres rainlbrows > backup.sql

# Restore
docker-compose -f docker-compose.dev.yml exec -T postgres psql -U postgres rainlbrows < backup.sql
```

### Очистка Docker

```bash
# Удалить неиспользуемые образы
docker image prune -a

# Удалить неиспользуемые volumes
docker volume prune

# Полная очистка системы Docker
docker system prune -a --volumes
```

---

## Мониторинг

### Prometheus + Grafana (опционально)

Для продакшена рекомендуется настроить мониторинг:
- Использование CPU/Memory
- Логи ошибок
- Время отклика бота
- Количество активных пользователей

### Простой мониторинг

```bash
# Запустите в отдельном терминале
watch -n 5 'docker stats rainlbrows_app_prod --no-stream'
```

---

## Безопасность

1. **Никогда не коммитьте `.env` файл в Git**
2. **Используйте сильные пароли для БД**
3. **Регулярно обновляйте Docker образы**:
   ```bash
   docker-compose -f docker-compose.prod.yml pull
   docker-compose -f docker-compose.prod.yml up -d
   ```
4. **Используйте Docker secrets для чувствительных данных** (для Docker Swarm)

---

## Контакты и поддержка

При возникновении проблем проверьте:
- Логи контейнера
- Переменные окружения
- Доступность внешних сервисов (БД, Telegram API)

Для получения помощи обратитесь к документации:
- [Docker Documentation](https://docs.docker.com/)
- [Python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

