from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from shared.constants.callback_register import (
    CALLBACK_MENU_MAIN,
    CALLBACK_PAYMENT_INTENSIVE,
    CALLBACK_PROMOCODE,
    BUTTON_TEXT_BACK,
    BUTTON_TEXT_PAY,
    BUTTON_TEXT_PROMOCODE
)

def get_intensive_keyboard():
    """Create keyboard for intensive page with Pay, Promocode and Back buttons"""
    keyboard = [
        [InlineKeyboardButton(BUTTON_TEXT_PAY, callback_data=CALLBACK_PAYMENT_INTENSIVE)],
        [InlineKeyboardButton(BUTTON_TEXT_PROMOCODE, callback_data=CALLBACK_PROMOCODE)],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)

