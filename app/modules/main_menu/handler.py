from telegram import Update
from telegram.ext import ContextTypes
from modules.main_menu.index import get_main_menu_keyboard

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle main menu callback - return to main menu"""
    query = update.callback_query
    await query.answer()
    
    text = "Привет, меня зовут Аня и здесь ты узнаешь про продажи бьюти мастера"
    await query.edit_message_text(text, reply_markup=get_main_menu_keyboard())

