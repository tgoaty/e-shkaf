from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

profile_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Главное меню")],
        [KeyboardButton("Список заказов")]
    ],
    resize_keyboard=True
)
