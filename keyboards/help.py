from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def help_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Связаться с поддержкой")],
            [KeyboardButton(text="Попробовать снова")]
        ],
        resize_keyboard=True
    )