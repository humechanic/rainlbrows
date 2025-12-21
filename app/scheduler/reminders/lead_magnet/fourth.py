"""
Fourth lead magnet reminder.

Final push reminder sent 3 hours after third reminder.
Can be scheduled via JobQueue or called directly.
"""
from db.repository import update_reminder_sent
from shared.utils.get_lead_reminder_keyboards import get_third_reminder_keyboard
from shared.utils.telegram_error_handler import send_message_with_error_handling
from db.session import get_db_session
from db.models import Offer
import logging

logger = logging.getLogger(__name__)

# Job name for fourth reminder
JOB_NAME_FOURTH_REMINDER = "fourth_lead_reminder_{user_id}"


async def send_fourth_reminder_callback(context):
    """Callback for fourth reminder scheduled after third reminder"""
    user_id = context.job.data.get('user_id')
    offer_id = context.job.data.get('offer_id')
    
    if not user_id or not offer_id:
        logger.error("Fourth reminder callback: user_id or offer_id not found in job data")
        return
    
    try:
        db = get_db_session()
        try:
            # Get offer and user from database
            offer = db.query(Offer).filter(Offer.id == offer_id).first()
            
            if not offer or not offer.user:
                logger.warning(f"Offer {offer_id} or user not found for fourth reminder")
                return
            
            user = offer.user
            if not user.telegram_id:
                logger.warning(f"User {user.id} has no telegram_id for fourth reminder")
                return
            
            # Send fourth reminder
            await send_fourth_lead_reminder(context.bot, db, offer, user)
            logger.info(f"Sent fourth reminder to user_id={user_id} via JobQueue")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error in fourth reminder callback for user_id={user_id}: {e}", exc_info=True)


async def send_fourth_lead_reminder(bot, db, offer, user):
    """Send final push special offer reminder (3 hours after third reminder)"""
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
    success = await send_message_with_error_handling(
        bot.send_message,
        user.telegram_id,
        "fourth lead reminder",
        message_text=text,
        chat_id=user.telegram_id,
        text=text,
        parse_mode='HTML',
        reply_markup=keyboard
    )
    
    if success:
        update_reminder_sent(db, offer.id, reminder_type="fourth_lead")
    
    return success

