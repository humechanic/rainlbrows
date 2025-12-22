"""
Keyboard for payment with promocode applied.

This keyboard is shown after user successfully enters a valid promocode.
It provides a button to proceed to payment with discount.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from shared.constants.callback_register import (
    CALLBACK_MENU_MAIN,
    BUTTON_TEXT_BACK
)
import env


def get_promocode_keyboard():
    """
    Create keyboard for payment with promocode applied.
    
    Shows button to proceed to BePaid payment page with discount.
    This keyboard is displayed after user successfully enters a valid promocode.
    
    Returns:
        InlineKeyboardMarkup with payment button (with promocode) and back button
    """
    keyboard = [
        [InlineKeyboardButton(
            "Забрать место на интенсиве и оплатить со скидкой",
            url=env.BEPAID_PAYMENT_URL_WITH_PROMO
        )],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)

