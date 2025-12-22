from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from shared.constants.callback_register import (
    CALLBACK_MENU_MAIN,
    CALLBACK_PROMOCODE,
    BUTTON_TEXT_BACK,
    BUTTON_TEXT_PAY,
    BUTTON_TEXT_PROMOCODE
)
from modules.lead_magnet.config import get_lead_magnet_config
import env


def get_watch_lesson_keyboard():
    """Keyboard for watch lesson reminder with payment and promocode buttons"""
    config = get_lead_magnet_config()
    youtube_url = config["youtube_url"]
    
    keyboard = [
        [InlineKeyboardButton("Смотреть урок", url=youtube_url)],
        [InlineKeyboardButton(BUTTON_TEXT_PAY, url=env.BEPAID_PAYMENT_URL_WITHOUT_PROMO)],
        [InlineKeyboardButton(BUTTON_TEXT_PROMOCODE, callback_data=CALLBACK_PROMOCODE)],
        [InlineKeyboardButton("Перейти на сайт интенсива", url="https://rainlbrows.online/beauty-sellers")],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_second_reminder_keyboard():
    """Keyboard for second reminder with payment and promocode buttons"""
    config = get_lead_magnet_config()
    youtube_url = config["youtube_url"]
    
    keyboard = [
        [InlineKeyboardButton("Смотреть урок", url=youtube_url)],
        [InlineKeyboardButton(BUTTON_TEXT_PAY, url=env.BEPAID_PAYMENT_URL_WITHOUT_PROMO)],
        [InlineKeyboardButton(BUTTON_TEXT_PROMOCODE, callback_data=CALLBACK_PROMOCODE)],
        [InlineKeyboardButton("Перейти на сайт интенсива", url="https://rainlbrows.online/beauty-sellers")],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_third_reminder_keyboard():
    """Keyboard for final push reminder"""
    return get_second_reminder_keyboard()


def get_last_call_reminder_keyboard():
    """Keyboard for last call reminder with payment and promocode buttons"""
    keyboard = [
        [InlineKeyboardButton(BUTTON_TEXT_PAY, url=env.BEPAID_PAYMENT_URL_WITHOUT_PROMO)],
        [InlineKeyboardButton(BUTTON_TEXT_PROMOCODE, callback_data=CALLBACK_PROMOCODE)],
        [InlineKeyboardButton("Перейти на сайт интенсива", url="https://rainlbrows.online/beauty-sellers")],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_special_offer_keyboard():
    """Keyboard for special offer reminder with payment and promocode buttons"""
    keyboard = [
        [InlineKeyboardButton(BUTTON_TEXT_PAY, url=env.BEPAID_PAYMENT_URL_WITH_PROMO)],
        [InlineKeyboardButton(BUTTON_TEXT_PROMOCODE, callback_data=CALLBACK_PROMOCODE)],
        [InlineKeyboardButton("Перейти на сайт интенсива", url="https://rainlbrows.online/beauty-sellers")],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    return InlineKeyboardMarkup(keyboard)

