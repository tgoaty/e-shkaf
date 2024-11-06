from aiogram import Router, F
from aiogram.types import Message

order_list_router = Router()


@order_list_router.message(F.text == 'Список заказов')
async def cmd_start_3(message: Message):
    await message.answer('Список заказов')
