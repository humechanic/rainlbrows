from telegram import Update
from telegram.ext import ContextTypes
from shared.utils.get_intensive_keyboard import get_intensive_keyboard
import logging

logger = logging.getLogger(__name__)

async def handle_intensive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'Хочу на интенсив' callback"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    # Cancel scheduled reminders if user visits intensive page (target action-2)
    # This is optional - you may want to cancel only on payment
    # Uncomment if you want to cancel on page visit:
    # try:
    #     from scheduler.job_queue_reminders import cancel_lead_reminders
    #     cancel_lead_reminders(context, user_id)
    #     logger.info(f"Cancelled lead reminders for user_id={user_id} after intensive page visit")
    # except Exception as cancel_error:
    #     logger.warning(f"Error cancelling reminders for user_id={user_id}: {cancel_error}")
    
    text = "Записывайся на интенсив по продажам для бьюти-мастера: rainlbrows.online/beauty-sellers"
    await query.message.reply_text(text, reply_markup=get_intensive_keyboard())

