from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from shared.constants.callback_register import CALLBACK_MENU_MAIN, BUTTON_TEXT_BACK

def get_back_keyboard():
    keyboard = [
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)