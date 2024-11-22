from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def help_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Связаться с поддержкой")],
        ],
        resize_keyboard=True
    )