"""
JobQueue-based reminder system that doesn't depend on database.

This module schedules reminders directly using JobQueue after target actions.
Reminders can be cancelled if target action-2 is performed.
"""
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError, NetworkError, TimedOut, RetryAfter, BadRequest
from modules.lead_magnet.config import get_lead_magnet_config
from shared.utils.get_lead_reminder_keyboards import (
    get_watch_lesson_keyboard,
    get_second_reminder_keyboard,
    get_third_reminder_keyboard
)
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

# Job names for identification and cancellation
JOB_NAME_FIRST_REMINDER = "first_reminder_{user_id}"
JOB_NAME_SECOND_REMINDER = "second_reminder_{user_id}"
JOB_NAME_THIRD_REMINDER = "third_reminder_{user_id}"


async def send_first_reminder_callback(context: ContextTypes.DEFAULT_TYPE):
    """Callback for first reminder - send watch lesson reminder"""
    user_id = context.job.data.get('user_id')
    if not user_id:
        logger.error("First reminder callback: user_id not found in job data")
        return
    
    try:
        config = get_lead_magnet_config()
        text = (
            "Коллеги, не забывайте посмотреть урок \"ТОП 3 ошибки в продажах бьюти мастера\"\n\n"
            "Что разобрали?\n\n"
            "▪️ почему клиенты не записываются? ТОП ошибок, о которых никто не говорит\n\n"
            "▪️ реальные примеры из практики для любой бьюти-ниши\n\n"
            "▪️ как привести к покупке через 5 минут после подписки\n\n"
            "🔥рекомендации, которые можно внедрить сразу в ваш инстаграм\n\n"
            "А также рассказала про свой интенсив \"Продажи бьюти-мастера\" и бонусы для участников интенсива❤️\n\n"
            f"Ссылка на урок: {config['youtube_url']}"
        )
        
        keyboard = get_watch_lesson_keyboard()
        await context.bot.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=keyboard
        )
        logger.info(f"Sent first lead reminder to user_id={user_id}")
    except (NetworkError, TimedOut) as e:
        logger.warning(f"Network error sending first reminder to user_id={user_id}: {e}")
    except RetryAfter as e:
        logger.warning(f"Rate limit sending first reminder to user_id={user_id}: {e}")
    except BadRequest as e:
        logger.error(f"Bad request sending first reminder to user_id={user_id}: {e}")
    except TelegramError as e:
        logger.error(f"Failed to send first reminder to user_id={user_id}: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Unexpected error sending first reminder to user_id={user_id}: {e}", exc_info=True)


async def send_second_reminder_callback(context: ContextTypes.DEFAULT_TYPE):
    """Callback for second reminder - send special price reminder"""
    user_id = context.job.data.get('user_id')
    if not user_id:
        logger.error("Second reminder callback: user_id not found in job data")
        return
    
    try:
        text = (
            "❓ <b>ТОП-4 вопроса об интенсиве \"Продажи бьюти-мастера\"</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            "🔹 <b>Для какой бьюти ниши подойдет интенсив?</b>\n"
            "   Интенсив подходит для любой ниши: брови, перманент, массаж, ламинирование ресниц, "
            "косметология, подология, маникюр, кератин - примеры и инструменты в уроках можно "
            "адаптировать под любую нишу.\n\n"
            
            "🔹 <b>Смогу ли я проходить интенсив, если у меня плотный график?</b>\n"
            "   Да, уроки интенсива в записи, можно просматривать их и выполнять рекомендации в "
            "любое удобное для вас время.\n\n"
            
            "🔹 <b>Хочу начать обучать, поможет ли мне интенсив?</b>\n"
            "   Да, уроки в интенсиве построены на базовых знаниях маркетинга и продаж, поэтому "
            "вы с легкостью сможете их адаптировать для вашего будущего курса.\n\n"
            
            "🔹 <b>Смогу ли я задать вопросы по своему инстаграм автору интенсива?</b>\n"
            "   Да, после просмотра интенсива вы сможете задать вопросы в отдельный чат, Анна "
            "дает обратную связь в чате и также проводит прямые эфиры с разбором популярных вопросов.\n\n"
            
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "💫 <i>Почему бы не начать Новый год по новому? Еще и с поддержкой и рекомендациями от меня.</i>\n\n"
            "🔥 <b>Смотри урок, там есть промокод на участие</b>"
        )
        
        keyboard = get_second_reminder_keyboard()
        await context.bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode='HTML',
            reply_markup=keyboard
        )
        logger.info(f"Sent second lead reminder to user_id={user_id}")
    except (NetworkError, TimedOut) as e:
        logger.warning(f"Network error sending second reminder to user_id={user_id}: {e}")
    except RetryAfter as e:
        logger.warning(f"Rate limit sending second reminder to user_id={user_id}: {e}")
    except BadRequest as e:
        logger.error(f"Bad request sending second reminder to user_id={user_id}: {e}")
    except TelegramError as e:
        logger.error(f"Failed to send second reminder to user_id={user_id}: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Unexpected error sending second reminder to user_id={user_id}: {e}", exc_info=True)


async def send_third_reminder_callback(context: ContextTypes.DEFAULT_TYPE):
    """Callback for third reminder - send final push reminder"""
    user_id = context.job.data.get('user_id')
    if not user_id:
        logger.error("Third reminder callback: user_id not found in job data")
        return
    
    try:
        text = (
            "🔔 <b>Важно!</b>\n"
            "Скоро спецпредложение пропадет\n\n"
            
            "Успей:\n\n"
            
            "▪️ Забрать место на курсе с выгодой (без промокода цена будет выше)\n\n"
            
            "▪️ Получить бонусы:\n\n"
            
            "- урок «Нейросети для бьюти мастера» - как создать контент без моделей, с 0 и оживить фото "
            "(практический урок от приглашенного эксперта Александры Легович)\n\n"
            
            "- готовый контент-план с идеями, который можно адаптировать под любой месяц и нишу\n\n"
        )
        
        keyboard = get_third_reminder_keyboard()
        await context.bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode='HTML',
            reply_markup=keyboard
        )
        logger.info(f"Sent third lead reminder to user_id={user_id}")
    except (NetworkError, TimedOut) as e:
        logger.warning(f"Network error sending third reminder to user_id={user_id}: {e}")
    except RetryAfter as e:
        logger.warning(f"Rate limit sending third reminder to user_id={user_id}: {e}")
    except BadRequest as e:
        logger.error(f"Bad request sending third reminder to user_id={user_id}: {e}")
    except TelegramError as e:
        logger.error(f"Failed to send third reminder to user_id={user_id}: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Unexpected error sending third reminder to user_id={user_id}: {e}", exc_info=True)


def schedule_lead_reminders(context: ContextTypes.DEFAULT_TYPE, user_id: int, use_minutes: bool = False):
    """
    Schedule all lead magnet reminders after lesson click.
    
    Args:
        context: Application context with job_queue
        user_id: Telegram user ID
        use_minutes: If True, use minutes for testing. If False, use hours from config.
    
    Returns:
        List of scheduled job names
    """
    # Get job_queue from context
    try:
        job_queue = context.job_queue
    except AttributeError:
        logger.warning("JobQueue is not available. Install python-telegram-bot[job-queue] to use this feature.")
        return []
    
    if not job_queue:
        logger.warning("JobQueue is not available. Cannot schedule reminders. Install python-telegram-bot[job-queue] to use this feature.")
        return []
    
    config = get_lead_magnet_config()
    job_names = []
    
    try:
        # Get intervals from config
        if use_minutes:
            first_interval = config.get("first_reminder_minutes", 1) * 60  # Convert to seconds
            second_interval = config.get("second_reminder_minutes", 2) * 60
            third_interval = config.get("third_reminder_after_second_minutes", 1) * 60
        else:
            first_interval = config.get("first_reminder_hours", 1) * 3600  # Convert to seconds
            second_interval = config.get("second_reminder_hours", 2) * 3600
            third_interval = config.get("third_reminder_after_second_hours", 3) * 3600
        
        # Job data
        job_data = {'user_id': user_id}
        
        # Schedule first reminder
        first_job_name = JOB_NAME_FIRST_REMINDER.format(user_id=user_id)
        first_job = job_queue.run_once(
            callback=send_first_reminder_callback,
            when=first_interval,
            data=job_data,
            name=first_job_name,
            chat_id=user_id
        )
        job_names.append(first_job_name)
        logger.info(f"Scheduled first reminder for user_id={user_id} in {first_interval}s")
        
        # Schedule second reminder (after first interval + second interval)
        second_job_name = JOB_NAME_SECOND_REMINDER.format(user_id=user_id)
        second_job = job_queue.run_once(
            callback=send_second_reminder_callback,
            when=first_interval + second_interval,
            data=job_data,
            name=second_job_name,
            chat_id=user_id
        )
        job_names.append(second_job_name)
        logger.info(f"Scheduled second reminder for user_id={user_id} in {first_interval + second_interval}s")
        
        # Schedule third reminder (after second reminder + third interval)
        third_job_name = JOB_NAME_THIRD_REMINDER.format(user_id=user_id)
        third_job = job_queue.run_once(
            callback=send_third_reminder_callback,
            when=first_interval + second_interval + third_interval,
            data=job_data,
            name=third_job_name,
            chat_id=user_id
        )
        job_names.append(third_job_name)
        logger.info(f"Scheduled third reminder for user_id={user_id} in {first_interval + second_interval + third_interval}s")
        
        return job_names
        
    except Exception as e:
        logger.error(f"Error scheduling reminders for user_id={user_id}: {e}", exc_info=True)
        return job_names


def cancel_lead_reminders(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """
    Cancel all scheduled lead reminders for a user.
    This should be called when target action-2 is performed (e.g., payment or intensive page visit).
    
    Args:
        context: Application context with job_queue
        user_id: Telegram user ID
    """
    # Get job_queue from context
    try:
        job_queue = context.job_queue
    except AttributeError:
        logger.warning("JobQueue is not available. Install python-telegram-bot[job-queue] to use this feature.")
        return
    
    if not job_queue:
        logger.warning("JobQueue is not available. Cannot cancel reminders. Install python-telegram-bot[job-queue] to use this feature.")
        return
    
    cancelled_count = 0
    
    try:
        # Get all jobs for this user
        job_names = [
            JOB_NAME_FIRST_REMINDER.format(user_id=user_id),
            JOB_NAME_SECOND_REMINDER.format(user_id=user_id),
            JOB_NAME_THIRD_REMINDER.format(user_id=user_id)
        ]
        
        # Cancel each job by iterating through all jobs
        # JobQueue uses APScheduler internally, jobs are stored in scheduler
        for job_name in job_names:
            try:
                # Try to get jobs by name if method exists
                jobs_to_cancel = []
                if hasattr(job_queue, 'get_jobs_by_name'):
                    jobs_to_cancel = job_queue.get_jobs_by_name(job_name)
                else:
                    # Fallback: iterate through scheduler jobs
                    # APScheduler stores jobs in scheduler._jobs dict
                    scheduler = getattr(job_queue, '_scheduler', None)
                    if scheduler and hasattr(scheduler, 'get_jobs'):
                        all_jobs = scheduler.get_jobs()
                        for job in all_jobs:
                            if hasattr(job, 'id') and job.id == job_name:
                                jobs_to_cancel.append(job)
                    elif hasattr(job_queue, 'scheduler') and hasattr(job_queue.scheduler, 'get_jobs'):
                        all_jobs = job_queue.scheduler.get_jobs()
                        for job in all_jobs:
                            if hasattr(job, 'id') and job.id == job_name:
                                jobs_to_cancel.append(job)
                
                # Cancel found jobs
                for job in jobs_to_cancel:
                    if hasattr(job, 'remove'):
                        job.remove()
                        cancelled_count += 1
                        logger.info(f"Cancelled reminder job: {job_name}")
                    elif hasattr(job, 'schedule_removal'):
                        job.schedule_removal()
                        cancelled_count += 1
                        logger.info(f"Cancelled reminder job: {job_name}")
            except Exception as e:
                logger.warning(f"Error cancelling job {job_name}: {e}")
        
        if cancelled_count > 0:
            logger.info(f"Cancelled {cancelled_count} reminder(s) for user_id={user_id}")
        else:
            logger.debug(f"No reminder jobs found to cancel for user_id={user_id}")
            
    except Exception as e:
        logger.error(f"Error cancelling reminders for user_id={user_id}: {e}", exc_info=True)

