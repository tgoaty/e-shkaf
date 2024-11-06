from aiogram import Router, F
from aiogram.types import Message

from keyboards import order_menu

order_router = Router()


@order_router.message(F.text == '/start')
async def cmd_start_3(message: Message):
    await message.answer('Запуск сообщения по команде /start_3 используя магический фильтр F.text!',
                         reply_markup=order_menu())
