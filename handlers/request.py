from aiogram import Router, F
from aiogram.types import Message


request_router = Router()


@request_router.message(F.text == 'Создать заявку на расчет')
async def cmd_start_3(message: Message):
    await message.answer('Создать заявку')
