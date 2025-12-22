from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from shared.constants.callback_register import CALLBACK_MENU_MAIN

async def handle_intensive_materials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle intensive materials callback - send Telegram channel link"""
    query = update.callback_query
    if query:
        await query.answer()
        message = query.message
    else:
        message = update.message
    
    # Send message with Telegram channel link
    telegram_channel_url = "https://t.me/+rmIBxami96IzMDBi"
    text = (
        "📚 Материалы интенсива\n\n"
        "Присоединяйтесь к нашему Telegram каналу, где вы найдете все материалы интенсива:\n\n"
        f"👉 {telegram_channel_url}"
    )
    
    keyboard = [
        [InlineKeyboardButton("Перейти в канал", url=telegram_channel_url)],
        [InlineKeyboardButton("Назад", callback_data=CALLBACK_MENU_MAIN)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.reply_text(text, reply_markup=reply_markup)

