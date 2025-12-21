# JobQueue-based Reminder System

## Описание

Модуль `job_queue_reminders.py` реализует систему напоминаний, которая **не зависит от базы данных**. Напоминания планируются напрямую через JobQueue после целевых действий и могут быть отменены при выполнении целевого действия-2.

## Как это работает

1. **Целевое действие-1**: Пользователь кликает "Забрать урок" (`CALLBACK_GET_LESSON`)

   - Автоматически планируются 3 напоминания через `schedule_lead_reminders()`
   - Напоминания используют таймауты из конфигурации (минуты для тестирования, часы для продакшена)

2. **Целевое действие-2**: Пользователь выполняет оплату или переходит на страницу интенсива
   - Все запланированные напоминания отменяются через `cancel_lead_reminders()`

## Преимущества

✅ **Независимость от БД**: Работает даже если база данных недоступна  
✅ **Надежность**: Напоминания хранятся в памяти JobQueue  
✅ **Автоматическая отмена**: Напоминания отменяются при выполнении целевого действия  
✅ **Гибкость**: Можно использовать минуты для тестирования или часы для продакшена

## Использование

### Планирование напоминаний

```python
from scheduler.job_queue_reminders import schedule_lead_reminders

# После клика на "Забрать урок"
schedule_lead_reminders(context, user_id, use_minutes=True)  # True для тестирования
```

### Отмена напоминаний

```python
from scheduler.job_queue_reminders import cancel_lead_reminders

# После успешной оплаты
cancel_lead_reminders(context, user_id)
```

## Конфигурация

Интервалы напоминаний настраиваются в `modules/lead_magnet/config.py`:

- `FIRST_REMINDER_MINUTES` / `FIRST_REMINDER_HOURS` - первое напоминание
- `SECOND_REMINDER_MINUTES` / `SECOND_REMINDER_HOURS` - второе напоминание
- `THIRD_REMINDER_AFTER_SECOND_MINUTES` / `THIRD_REMINDER_AFTER_SECOND_HOURS` - третье напоминание

## Интеграция

Модуль уже интегрирован в:

- `modules/lead_magnet/index.py` - планирование после клика на урок
- `modules/payment/index.py` - отмена после успешной оплаты
- `modules/intensive/index.py` - опциональная отмена при переходе на страницу интенсива

## Технические детали

- Использует `JobQueue.run_once()` для одноразовых задач
- Имена задач: `first_reminder_{user_id}`, `second_reminder_{user_id}`, `third_reminder_{user_id}`
- Отмена через APScheduler API (`job.remove()` или `job.schedule_removal()`)
