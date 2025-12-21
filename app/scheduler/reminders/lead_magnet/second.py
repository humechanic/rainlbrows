"""
Second lead magnet reminder.

Sent after first reminder with urgency message about special offer.
After sending, schedules third reminder for 3 hours later.
Can be scheduled via JobQueue or called directly.
"""
from db.repository import mark_second_reminder_sent
from shared.utils.get_lead_reminder_keyboards import get_second_reminder_keyboard
from shared.utils.telegram_error_handler import send_message_with_error_handling
from scheduler.reminders.lead_magnet.third import send_third_reminder_callback, JOB_NAME_THIRD_REMINDER
from db.session import get_db_session
from db.models import Offer
import logging

logger = logging.getLogger(__name__)

# Job name for second reminder
JOB_NAME_SECOND_REMINDER = "second_lead_reminder_{user_id}"


async def send_second_reminder_callback(context):
    """Callback for second reminder scheduled after first reminder"""
    user_id = context.job.data.get('user_id')
    offer_id = context.job.data.get('offer_id')
    
    if not user_id or not offer_id:
        logger.error("Second reminder callback: user_id or offer_id not found in job data")
        return
    
    try:
        db = get_db_session()
        try:
            # Get offer and user from database
            offer = db.query(Offer).filter(Offer.id == offer_id).first()
            
            if not offer or not offer.user:
                logger.warning(f"Offer {offer_id} or user not found for second reminder")
                return
            
            user = offer.user
            if not user.telegram_id:
                logger.warning(f"User {user.id} has no telegram_id for second reminder")
                return
            
            # Send second reminder (pass context to enable scheduling of third reminder)
            await send_second_lead_reminder(context.bot, db, offer, user, context=context)
            logger.info(f"Sent second reminder to user_id={user_id} via JobQueue")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error in second reminder callback for user_id={user_id}: {e}", exc_info=True)


async def send_second_lead_reminder(bot, db, offer, user, context=None):
    """
    Send second lead reminder with urgency message.
    After successful send, schedules third reminder for 3 hours later.
    
    Args:
        bot: Telegram bot instance
        db: Database session
        offer: Offer object
        user: User object
        context: Optional context with job_queue (if available)
    """
    text = (
        "Спецпредложение скоро исчезнет!\n\n"
        
        "Каждая ошибка в бьюти-нише - это деньги, которые прямо сейчас утекают к другим.\n\n"
        
        "В уроке ты сможешь:\n\n"
        
        "👉🏼 Понять, что именно тормозит твои продажи\n"
        "👉🏼 Взять готовые идеи контента\n"
        "👉🏼 Внедрить конкретные рекомендации и увеличить записи в 2-5 раз\n\n"
        
        "Смотри сейчас, чтобы уже завтра сделать новые рекорды ⤵️"
    )
    
    keyboard = get_second_reminder_keyboard()
    success = await send_message_with_error_handling(
        bot.send_message,
        user.telegram_id,
        "second lead reminder",
        message_text=text,
        chat_id=user.telegram_id,
        text=text,
        reply_markup=keyboard
    )
    
    if success:
        mark_second_reminder_sent(db, offer.id)
        
        # Schedule third reminder for 3 hours later using JobQueue
        job_queue = None
        
        # Try to get job_queue from context if provided
        if context and hasattr(context, 'job_queue'):
            job_queue = context.job_queue
        # Try to get job_queue from bot.application
        elif hasattr(bot, 'application') and hasattr(bot.application, 'job_queue'):
            job_queue = bot.application.job_queue
        
        if job_queue:
            try:
                # Schedule third reminder for 3 hours (10800 seconds) later
                job_name = JOB_NAME_THIRD_REMINDER.format(user_id=user.telegram_id)
                job_data = {
                    'user_id': user.telegram_id,
                    'offer_id': offer.id
                }
                
                job_queue.run_once(
                    callback=send_third_reminder_callback,
                    when=10800,  # 3 hours in seconds
                    data=job_data,
                    name=job_name,
                    chat_id=user.telegram_id
                )
                logger.info(f"Scheduled third reminder for user_id={user.telegram_id} in 3 hours via JobQueue")
            except Exception as e:
                logger.error(f"Failed to schedule third reminder for user_id={user.telegram_id}: {e}", exc_info=True)
        else:
            logger.warning(f"JobQueue not available. Cannot schedule third reminder for user_id={user.telegram_id}")
    
    return success

