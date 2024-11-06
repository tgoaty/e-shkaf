from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def orderList_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Главное меню")]
        ],
        resize_keyboard=True
    )
