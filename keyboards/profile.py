from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def profile_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Главное меню")],
            [KeyboardButton(text="Список заказов")]
        ],
        resize_keyboard=True
    )
