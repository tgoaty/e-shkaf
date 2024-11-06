from aiogram import Router, F
from aiogram.types import Message

from keyboards import orderList_menu

orderList_router = Router()


@orderList_router.message(F.text == 'Список заказов')
async def cmd_start_3(message: Message):
    await message.answer('Список заказов', reply_markup=orderList_menu())
