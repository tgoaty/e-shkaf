from aiogram import Router, F
from aiogram.types import Message
from keyboards import profile_menu

profile_router = Router()


@profile_router.message(F.text == 'Профиль')
async def cmd_start_3(message: Message):
    await message.answer('профиль', reply_markup=profile_menu())
