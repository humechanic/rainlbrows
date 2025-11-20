from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from shared.constants.callback_register import (
    CALLBACK_MENU_DETAILS,
    CALLBACK_MENU_BLOG,
    CALLBACK_MENU_INTENSIVE,
    BUTTON_TEXT_DETAILS,
    BUTTON_TEXT_BLOG,
    BUTTON_TEXT_INTENSIVE
)

def get_main_menu_keyboard():
    """Create main menu keyboard with INTENSIVE in first row, DETAILS and BLOG in second row"""
    keyboard = [
        [InlineKeyboardButton(BUTTON_TEXT_INTENSIVE, callback_data=CALLBACK_MENU_INTENSIVE)],
        [
            InlineKeyboardButton(BUTTON_TEXT_DETAILS, callback_data=CALLBACK_MENU_DETAILS),
            InlineKeyboardButton(BUTTON_TEXT_BLOG, callback_data=CALLBACK_MENU_BLOG)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
