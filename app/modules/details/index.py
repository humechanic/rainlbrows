from telegram import Update
from telegram.ext import ContextTypes
from shared.utils.get_back import get_back_keyboard

async def handle_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'Узнать подробнее' callback"""
    query = update.callback_query
    await query.answer()
    
    text = "Интересный факт: Бьюти-мастера, которые используют правильные техники продаж, увеличивают свой доход в среднем на 40% за первые 3 месяца работы. Хочешь узнать больше? Записывайся на интенсив!"
    await query.edit_message_text(text, reply_markup=get_back_keyboard())

