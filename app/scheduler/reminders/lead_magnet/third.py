"""
Third lead magnet reminder.

Sent after second reminder with FAQ about intensive.
After sending, schedules fourth reminder for 3 hours later.
Can be scheduled via JobQueue or called directly.
"""
from db.repository import update_reminder_sent
from modules.lead_magnet.config import get_lead_magnet_config
from shared.utils.get_lead_reminder_keyboards import get_second_reminder_keyboard
from shared.utils.telegram_error_handler import send_message_with_error_handling
from scheduler.reminders.lead_magnet.fourth import send_fourth_reminder_callback, JOB_NAME_FOURTH_REMINDER
from db.session import get_db_session
from db.models import Offer
import logging

logger = logging.getLogger(__name__)

# Job name for third reminder
JOB_NAME_THIRD_REMINDER = "third_lead_reminder_{user_id}"


async def send_third_reminder_callback(context):
    """Callback for third reminder scheduled after second reminder"""
    user_id = context.job.data.get('user_id')
    offer_id = context.job.data.get('offer_id')
    
    if not user_id or not offer_id:
        logger.error("Third reminder callback: user_id or offer_id not found in job data")
        return
    
    try:
        db = get_db_session()
        try:
            # Get offer and user from database
            offer = db.query(Offer).filter(Offer.id == offer_id).first()
            
            if not offer or not offer.user:
                logger.warning(f"Offer {offer_id} or user not found for third reminder")
                return
            
            user = offer.user
            if not user.telegram_id:
                logger.warning(f"User {user.id} has no telegram_id for third reminder")
                return
            
            # Send third reminder (pass context to enable scheduling of fourth reminder)
            await send_third_lead_reminder(context.bot, db, offer, user, context=context)
            logger.info(f"Sent third reminder to user_id={user_id} via JobQueue")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error in third reminder callback for user_id={user_id}: {e}", exc_info=True)


async def send_third_lead_reminder(bot, db, offer, user, context=None):
    """
    Send special price reminder (FAQ about intensive).
    After successful send, schedules fourth reminder for 3 hours later.
    
    Args:
        bot: Telegram bot instance
        db: Database session
        offer: Offer object
        user: User object
        context: Optional context with job_queue (if available)
    """
    text = (
        "❓ <b>ТОП-4 вопроса об интенсиве \"Продажи бьюти-мастера\"</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        
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
        
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💫 <i>Почему бы не начать Новый год по новому? Особенно с поддержкой и рекомендациями от эксперта.</i>\n\n"
        f"🔥 <b>Смотри урок {get_lead_magnet_config()['youtube_url']}, там есть промокод на участие</b>"
    )
    
    keyboard = get_second_reminder_keyboard()
    success = await send_message_with_error_handling(
        bot.send_message,
        user.telegram_id,
        "third lead reminder",
        message_text=text,
        chat_id=user.telegram_id,
        text=text,
        parse_mode='HTML',
        reply_markup=keyboard
    )
    
    if success:
        update_reminder_sent(db, offer.id, reminder_type="third_lead")
        
        # Schedule fourth reminder for 3 hours later using JobQueue
        job_queue = None
        
        # Try to get job_queue from context if provided
        if context and hasattr(context, 'job_queue'):
            job_queue = context.job_queue
        # Try to get job_queue from bot.application
        elif hasattr(bot, 'application') and hasattr(bot.application, 'job_queue'):
            job_queue = bot.application.job_queue
        
        if job_queue:
            try:
                # Schedule fourth reminder for 3 hours (10800 seconds) later
                job_name = JOB_NAME_FOURTH_REMINDER.format(user_id=user.telegram_id)
                job_data = {
                    'user_id': user.telegram_id,
                    'offer_id': offer.id
                }
                
                job_queue.run_once(
                    callback=send_fourth_reminder_callback,
                    when=10800,  # 3 hours in seconds
                    data=job_data,
                    name=job_name,
                    chat_id=user.telegram_id
                )
                logger.info(f"Scheduled fourth reminder for user_id={user.telegram_id} in 3 hours via JobQueue")
            except Exception as e:
                logger.error(f"Failed to schedule fourth reminder for user_id={user.telegram_id}: {e}", exc_info=True)
        else:
            logger.warning(f"JobQueue not available. Cannot schedule fourth reminder for user_id={user.telegram_id}")
    
    return success

