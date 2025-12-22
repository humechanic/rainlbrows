from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from shared.constants.callback_register import CALLBACK_MENU_MAIN, BUTTON_TEXT_BACK

# Support contact URL
SUPPORT_TELEGRAM_URL = "https://t.me/anna_rainl"

def get_back_keyboard():
    """Create keyboard with back button and support contact button"""
    keyboard = [
        [InlineKeyboardButton("Возникли проблемы? Задайте вопрос", url=SUPPORT_TELEGRAM_URL)],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)