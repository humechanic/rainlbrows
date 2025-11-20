from telegram import Update
from telegram.ext import ContextTypes
from shared.utils.get_intensive_keyboard import get_intensive_keyboard

async def handle_intensive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'Хочу на интенсив' callback"""
    query = update.callback_query
    await query.answer()
    
    text = "Записывайся на интенсив по продажам для бьюти-мастера: rainlbrows.online/beauty-sellers"
    await query.message.reply_text(text, reply_markup=get_intensive_keyboard())

