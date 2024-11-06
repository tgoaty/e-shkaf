from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Создать заявку на расчет")],
            [KeyboardButton(text="Список заказов")],
            [KeyboardButton(text="Связаться с менеджером")],
            [KeyboardButton(text="Профиль")]
        ],
        resize_keyboard=True
    )
