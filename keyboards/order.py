from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def order_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Вернуться к списку")],
            [KeyboardButton(text="Главное меню")]
        ],
        resize_keyboard=True
    )
