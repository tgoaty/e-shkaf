from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

order_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Вернуться к списку")],
        [KeyboardButton("Главное меню")]
    ],
    resize_keyboard=True
)
