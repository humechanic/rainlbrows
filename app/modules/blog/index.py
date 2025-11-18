from telegram import Update
from telegram.ext import ContextTypes
from shared.utils.get_back import get_back_keyboard

async def handle_blog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'Блог' callback"""
    query = update.callback_query
    await query.answer()
    
    text = "Читай полезные статьи в моем блоге: https://rainlbrows.online/posts"
    await query.edit_message_text(text, reply_markup=get_back_keyboard())

