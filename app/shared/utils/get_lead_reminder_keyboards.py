from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from shared.constants.callback_register import (
    CALLBACK_MENU_MAIN,
    BUTTON_TEXT_BACK
)
from modules.lead_magnet.config import get_lead_magnet_config


def get_watch_lesson_keyboard():
    """Keyboard for watch lesson reminder with website link"""
    config = get_lead_magnet_config()
    youtube_url = config["youtube_url"]
    
    keyboard = [
        [InlineKeyboardButton("Смотреть урок", url=youtube_url)],
        [InlineKeyboardButton("Перейти на сайт интенсива", url="https://rainlbrows.online/beauty-sellers")],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_second_reminder_keyboard():
    """Keyboard for second reminder with website link"""
    config = get_lead_magnet_config()
    youtube_url = config["youtube_url"]
    
    keyboard = [
        [InlineKeyboardButton("Смотреть урок", url=youtube_url)],
        [InlineKeyboardButton("Перейти на сайт интенсива", url="https://rainlbrows.online/beauty-sellers")],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_third_reminder_keyboard():
    """Keyboard for final push reminder"""
    return get_second_reminder_keyboard()


def get_last_call_reminder_keyboard():
    """Keyboard for last call reminder with website link"""
    keyboard = [
        [InlineKeyboardButton("Перейти на сайт интенсива", url="https://rainlbrows.online/beauty-sellers")],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_special_offer_keyboard():
    """Keyboard for special offer reminder with website link"""
    keyboard = [
        [InlineKeyboardButton("Перейти на сайт интенсива", url="https://rainlbrows.online/beauty-sellers")],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)

