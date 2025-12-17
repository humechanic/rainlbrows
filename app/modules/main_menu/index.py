from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from shared.constants.callback_register import (
    CALLBACK_MENU_DETAILS,
    CALLBACK_MENU_BLOG,
    CALLBACK_MENU_INTENSIVE,
    CALLBACK_MATERIALS_INTENSIVE,
    CALLBACK_ADMIN_EXPORT_USERS,
    CALLBACK_ADMIN_EXPORT_OFFERS,
    ADMIN_USER_IDS,
    BUTTON_TEXT_DETAILS,
    BUTTON_TEXT_BLOG,
    BUTTON_TEXT_INTENSIVE,
    BUTTON_TEXT_MATERIALS,
    BUTTON_TEXT_ADMIN_EXPORT_USERS,
    BUTTON_TEXT_ADMIN_EXPORT_OFFERS
)

def get_main_menu_keyboard(has_paid: bool = False, user_id: int = None):
    """Create main menu keyboard with INTENSIVE in first row, DETAILS and BLOG in second row
    If user has paid, add MATERIALS button in third row
    If user is admin, add admin menu in separate row
    """
    keyboard = [
        [InlineKeyboardButton(BUTTON_TEXT_INTENSIVE, callback_data=CALLBACK_MENU_INTENSIVE)],
        [
            InlineKeyboardButton(BUTTON_TEXT_DETAILS, callback_data=CALLBACK_MENU_DETAILS),
            InlineKeyboardButton(BUTTON_TEXT_BLOG, callback_data=CALLBACK_MENU_BLOG)
        ]
    ]
    
    # Add materials button if user has paid
    if has_paid:
        keyboard.append([InlineKeyboardButton(BUTTON_TEXT_MATERIALS, callback_data=CALLBACK_MATERIALS_INTENSIVE)])
    
    # Add admin menu if user is admin
    if user_id and user_id in ADMIN_USER_IDS:
        keyboard.append([
            InlineKeyboardButton(BUTTON_TEXT_ADMIN_EXPORT_USERS, callback_data=CALLBACK_ADMIN_EXPORT_USERS),
            InlineKeyboardButton(BUTTON_TEXT_ADMIN_EXPORT_OFFERS, callback_data=CALLBACK_ADMIN_EXPORT_OFFERS)
        ])
    
    return InlineKeyboardMarkup(keyboard)
