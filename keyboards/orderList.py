from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

order_list_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Главное меню")]
    ],
    resize_keyboard=True
)
