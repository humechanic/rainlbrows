from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from shared.constants.callback_register import (
    CALLBACK_MENU_MAIN,
    CALLBACK_PROMOCODE,
    BUTTON_TEXT_BACK,
    BUTTON_TEXT_PROMOCODE,
    BUTTON_TEXT_PAY
)
import env

def get_intensive_keyboard():
    """Create keyboard for intensive page with two payment buttons (with and without promocode), Promocode and Back buttons"""
    keyboard = [
        [InlineKeyboardButton(BUTTON_TEXT_PAY, url=env.BEPAID_PAYMENT_URL_WITHOUT_PROMO)],
        [InlineKeyboardButton(BUTTON_TEXT_PROMOCODE, callback_data=CALLBACK_PROMOCODE)],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)

