from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Список заказов")],
            [KeyboardButton(text="Профиль")]
        ],
        resize_keyboard=True
    )
