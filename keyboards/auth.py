from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def auth_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Поделиться номером", request_contact=True)],

        ],
        resize_keyboard=True
    )