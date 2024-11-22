from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def profile_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Список заказов")],
            [KeyboardButton(text="Связаться с менеджером")]

        ],
        resize_keyboard=True
    )
