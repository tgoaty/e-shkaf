from aiogram import Router, F
from aiogram.types import Message
from create_bot import db

auth_router = Router()

@auth_router.message(F.contact)
async def handle_contact(message: Message):
    contact = message.contact
    user_phone_number = contact.phone_number
    chat_id = message.chat.id

    async with db:
        await db.add_contact(chat_id, user_phone_number)

    await message.answer("Номер добавлен")