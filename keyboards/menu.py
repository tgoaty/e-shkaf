from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Список заказов")],
        [KeyboardButton("Связаться с менеджером")],
        [KeyboardButton("Профиль")]
    ],
    resize_keyboard=True
)
