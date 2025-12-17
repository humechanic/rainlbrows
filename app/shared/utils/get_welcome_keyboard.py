from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from shared.constants.callback_register import (
    CALLBACK_GET_LESSON,
    BUTTON_TEXT_GET_LESSON,
    ADMIN_USER_IDS,
    CALLBACK_ADMIN_EXPORT_USERS,
    CALLBACK_ADMIN_EXPORT_OFFERS,
    BUTTON_TEXT_ADMIN_EXPORT_USERS,
    BUTTON_TEXT_ADMIN_EXPORT_OFFERS
)


def get_welcome_keyboard(user_id: int = None):
    """Create keyboard for welcome message with 'забрать урок' button
    If user is admin, also add admin menu buttons
    """
    keyboard = [
        [InlineKeyboardButton(BUTTON_TEXT_GET_LESSON, callback_data=CALLBACK_GET_LESSON)]
    ]
    
    # Add admin menu if user is admin
    if user_id and user_id in ADMIN_USER_IDS:
        keyboard.append([
            InlineKeyboardButton(BUTTON_TEXT_ADMIN_EXPORT_USERS, callback_data=CALLBACK_ADMIN_EXPORT_USERS),
            InlineKeyboardButton(BUTTON_TEXT_ADMIN_EXPORT_OFFERS, callback_data=CALLBACK_ADMIN_EXPORT_OFFERS)
        ])
    
    return InlineKeyboardMarkup(keyboard)

