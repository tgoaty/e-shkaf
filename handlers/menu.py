from aiogram import Router, F
from aiogram.types import Message
from keyboards import main_menu

menu_router = Router()


@menu_router.message(F.text == 'Главное меню')
async def cmd_start_3(message: Message):
    await message.answer('Главное меню', reply_markup=main_menu())
