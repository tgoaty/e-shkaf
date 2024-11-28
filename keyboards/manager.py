from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def manager_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Список заказов")],
            [KeyboardButton(text="Профиль")],
            [KeyboardButton(text="Связаться с поддержкой")]
        ],
        resize_keyboard=True
    )
