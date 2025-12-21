"""
Offer expiration reminder functions.

This module contains functions for sending reminders about offer expiration
(last call and regular reminders).
"""
from db.repository import update_reminder_sent
from shared.utils.get_lead_reminder_keyboards import get_last_call_reminder_keyboard
from shared.utils.telegram_error_handler import send_message_with_error_handling
import logging

logger = logging.getLogger(__name__)


async def send_last_call_reminder(bot, db, offer, user):
    """Send 'last call' reminder message"""
    expiration_date = offer.offer_expiration_date.strftime("%d.%m.%Y в %H:%M")
    text = (
        f"⚠️ Внимание! Ваше специальное предложение истекает завтра в {expiration_date}!\n\n"
        f"Не упустите возможность воспользоваться выгодным предложением!"
    )
    
    keyboard = get_last_call_reminder_keyboard()
    success = await send_message_with_error_handling(
        bot.send_message,
        user.telegram_id,
        "last call reminder",
        message_text=text,
        chat_id=user.telegram_id,
        text=text,
        reply_markup=keyboard
    )
    
    if success:
        update_reminder_sent(db, offer.id, reminder_type='last_call')
    
    return success


async def send_regular_reminder(bot, db, offer, user):
    """Send regular reminder message"""
    expiration_date = offer.offer_expiration_date.strftime("%d.%m.%Y в %H:%M")
    text = (
        f"💡 Не забудьте! Ваше специальное предложение все еще ждет вас.\n\n"
        f"⏰ Действует до: {expiration_date}\n\n"
        f"Воспользуйтесь выгодным предложением пока оно активно!"
    )
    
    success = await send_message_with_error_handling(
        bot.send_message,
        user.telegram_id,
        "regular reminder",
        message_text=text,
        chat_id=user.telegram_id,
        text=text
    )
    
    if success:
        update_reminder_sent(db, offer.id, reminder_type=None)
    
    return success

