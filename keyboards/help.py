from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def help_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Поддержка")],

        ],
        resize_keyboard=True
    )