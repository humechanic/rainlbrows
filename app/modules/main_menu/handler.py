from telegram import Update
from telegram.ext import ContextTypes
from shared.utils.welcome_text import get_welcome_text
from shared.utils.get_welcome_keyboard import get_welcome_keyboard
import logging

logger = logging.getLogger(__name__)

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle main menu callback - return to welcome message"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    text = get_welcome_text()
    await query.message.reply_text(text, reply_markup=get_welcome_keyboard(user_id=user_id))

