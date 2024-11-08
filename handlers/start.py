from aiogram import Router, F
from aiogram.types import Message
from keyboards import auth_menu

start_router = Router()


@start_router.message(F.text == '/start')
async def cmd_start_3(message: Message):
    await message.answer('Для начала работы поделитесь своим номером.', reply_markup=auth_menu())

@start_router.message(F.contact)
async def handle_contact(message: Message):
    contact = message.contact
    user_phone_number = contact.phone_number
    await message.answer(user_phone_number)