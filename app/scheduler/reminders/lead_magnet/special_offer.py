"""
Special offer reminder.

Sent 1 hour after first reminder with special pricing offer.
"""
from db.repository import update_reminder_sent
from shared.utils.get_lead_reminder_keyboards import get_special_offer_keyboard
from shared.utils.telegram_error_handler import send_message_with_error_handling
import logging

logger = logging.getLogger(__name__)


async def send_special_offer_reminder(bot, db, offer, user):
    """Send special offer reminder (1 hour after first reminder)"""
    text = (
        "<b>ТОЛЬКО 24 ЧАСА</b>\n\n"
        "Можно зайти в интенсив по приятной цене\n\n"
        
        "<b>290 вместо 350 рублей</b>\n"
        "промокод <b>УРОК</b>\n\n"
        "Забирай свое место⬇️"
    )
    
    keyboard = get_special_offer_keyboard()
    success = await send_message_with_error_handling(
        bot.send_message,
        user.telegram_id,
        "special offer reminder",
        message_text=text,
        chat_id=user.telegram_id,
        text=text,
        parse_mode='HTML',
        reply_markup=keyboard
    )
    
    if success:
        update_reminder_sent(db, offer.id, reminder_type="special_offer")
    
    return success

