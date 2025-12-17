from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from shared.constants.callback_register import (
    CALLBACK_MENU_MAIN,
    CALLBACK_MENU_INTENSIVE,
    CALLBACK_PAYMENT_INTENSIVE,
    CALLBACK_PROMOCODE,
    BUTTON_TEXT_BACK,
    BUTTON_TEXT_PAY,
    BUTTON_TEXT_PROMOCODE,
    BUTTON_TEXT_INTENSIVE
)
from modules.lead_magnet.config import get_lead_magnet_config


def get_watch_lesson_keyboard():
    """Keyboard for watch lesson reminder with intensive and promocode buttons"""
    config = get_lead_magnet_config()
    youtube_url = config["youtube_url"]
    
    keyboard = [
        [InlineKeyboardButton("Смотреть урок", url=youtube_url)],
        [
            InlineKeyboardButton(BUTTON_TEXT_INTENSIVE, callback_data=CALLBACK_MENU_INTENSIVE),
            InlineKeyboardButton("Ввести промокод", callback_data=CALLBACK_PROMOCODE)
        ],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_second_reminder_keyboard():
    """Keyboard for special offer reminders"""
    keyboard = [
        [InlineKeyboardButton(BUTTON_TEXT_INTENSIVE, callback_data=CALLBACK_PAYMENT_INTENSIVE)],
        [InlineKeyboardButton(BUTTON_TEXT_PROMOCODE, callback_data=CALLBACK_PROMOCODE)],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_third_reminder_keyboard():
    """Keyboard for final push reminder"""
    return get_second_reminder_keyboard()


def get_last_call_reminder_keyboard():
    """Keyboard for last call reminder with intensive and promocode buttons"""
    keyboard = [
        [InlineKeyboardButton("Забрать интенсив", callback_data=CALLBACK_PAYMENT_INTENSIVE)],
        [InlineKeyboardButton("Применить промокод", callback_data=CALLBACK_PROMOCODE)],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)

