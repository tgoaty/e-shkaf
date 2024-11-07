from aiogram import Router, F
from aiogram.types import Message
from keyboards import auth

start_router = Router()


@start_router.message(F.text == '/start')
async def cmd_start_3(message: Message):
    await message.answer('Старт', reply_markup=auth())

