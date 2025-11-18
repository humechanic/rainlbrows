from telegram import Update
from telegram.ext import ContextTypes
from modules.main_menu.index import get_main_menu_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    text = "Привет, меня зовут Аня и здесь ты узнаешь про продажи бьюти мастера"
    await update.message.reply_text(text, reply_markup=get_main_menu_keyboard())