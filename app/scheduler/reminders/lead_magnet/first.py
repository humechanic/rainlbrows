"""
First lead magnet reminder.

Sent 1 hour after lesson click to remind user to watch the lesson.
After sending, schedules:
- Special offer reminder for 1 hour later
- Second reminder for 4 hours later
"""
from db.repository import mark_first_reminder_sent
from modules.lead_magnet.config import get_lead_magnet_config
from shared.utils.get_lead_reminder_keyboards import get_watch_lesson_keyboard
from shared.utils.telegram_error_handler import send_message_with_error_handling
from scheduler.reminders.lead_magnet.special_offer import send_special_offer_reminder
from scheduler.reminders.lead_magnet.second import send_second_reminder_callback, JOB_NAME_SECOND_REMINDER
from db.session import get_db_session
import logging

logger = logging.getLogger(__name__)

# Job names for scheduled reminders
JOB_NAME_SPECIAL_OFFER = "special_offer_reminder_{user_id}"


async def send_special_offer_callback(context):
    """Callback for special offer reminder scheduled after first reminder"""
    from telegram.ext import ContextTypes
    from db.models import Offer
    
    user_id = context.job.data.get('user_id')
    offer_id = context.job.data.get('offer_id')
    
    if not user_id or not offer_id:
        logger.error("Special offer callback: user_id or offer_id not found in job data")
        return
    
    try:
        db = get_db_session()
        try:
            # Get offer and user from database
            offer = db.query(Offer).filter(Offer.id == offer_id).first()
            
            if not offer or not offer.user:
                logger.warning(f"Offer {offer_id} or user not found for special offer reminder")
                return
            
            user = offer.user
            if not user.telegram_id:
                logger.warning(f"User {user.id} has no telegram_id for special offer reminder")
                return
            
            # Send special offer reminder
            await send_special_offer_reminder(context.bot, db, offer, user)
            logger.info(f"Sent special offer reminder to user_id={user_id} via JobQueue")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error in special offer callback for user_id={user_id}: {e}", exc_info=True)


async def send_first_lead_reminder(bot, db, offer, user, context=None):
    """
    Send watch lesson reminder (1 hour after lesson click).
    After successful send, schedules:
    - Special offer reminder for 1 hour later
    - Second reminder for 4 hours later
    
    Args:
        bot: Telegram bot instance
        db: Database session
        offer: Offer object
        user: User object
        context: Optional context with job_queue (if available)
    """
    text = (
        "Коллеги, не забывайте посмотреть урок \"ТОП 3 ошибки в продажах бьюти мастера\"\n\n"
        "Что разобрали?\n\n"
        "▪️ почему клиенты не записываются? ТОП ошибок, о которых никто не говорит\n\n"
        "▪️ реальные примеры из практики для любой бьюти-ниши\n\n"
        "▪️ как привести к покупке через 5 минут после подписки\n\n"
        "🔥рекомендации, которые можно внедрить сразу в ваш инстаграм\n\n"
        "А также рассказала про свой интенсив \"Продажи бьюти-мастера\" и бонусы для участников интенсива❤️\n\n"
        "Жми, чтобы посмотреть запись⤵️\n\n"
        f"Ссылка на урок: {get_lead_magnet_config()['youtube_url']}"
    )
    
    keyboard = get_watch_lesson_keyboard()
    success = await send_message_with_error_handling(
        bot.send_message,
        user.telegram_id,
        "first lead reminder",
        message_text=text,
        chat_id=user.telegram_id,
        text=text,
        reply_markup=keyboard
    )
    
    if success:
        mark_first_reminder_sent(db, offer.id)
        
        # Schedule special offer reminder for 1 hour later using JobQueue
        job_queue = None
        
        # Try to get job_queue from context if provided
        if context and hasattr(context, 'job_queue'):
            job_queue = context.job_queue
        # Try to get job_queue from bot.application
        elif hasattr(bot, 'application') and hasattr(bot.application, 'job_queue'):
            job_queue = bot.application.job_queue
        
        if job_queue:
            try:
                job_data = {
                    'user_id': user.telegram_id,
                    'offer_id': offer.id
                }
                
                # Schedule special offer reminder for 1 hour (3600 seconds) later
                special_offer_job_name = JOB_NAME_SPECIAL_OFFER.format(user_id=user.telegram_id)
                job_queue.run_once(
                    callback=send_special_offer_callback,
                    when=3600,  # 1 hour in seconds
                    data=job_data,
                    name=special_offer_job_name,
                    chat_id=user.telegram_id
                )
                logger.info(f"Scheduled special offer reminder for user_id={user.telegram_id} in 1 hour via JobQueue")
                
                # Schedule second reminder for 4 hours (14400 seconds) later
                second_job_name = JOB_NAME_SECOND_REMINDER.format(user_id=user.telegram_id)
                job_queue.run_once(
                    callback=send_second_reminder_callback,
                    when=14400,  # 4 hours in seconds
                    data=job_data,
                    name=second_job_name,
                    chat_id=user.telegram_id
                )
                logger.info(f"Scheduled second reminder for user_id={user.telegram_id} in 4 hours via JobQueue")
            except Exception as e:
                logger.error(f"Failed to schedule reminders for user_id={user.telegram_id}: {e}", exc_info=True)
        else:
            logger.warning(f"JobQueue not available. Cannot schedule reminders for user_id={user.telegram_id}")
    
    return success

