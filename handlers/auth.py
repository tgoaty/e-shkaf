from aiogram import Router, F
from aiogram.types import Message
from create_bot import db, bitrix
from keyboards import main_menu, help_menu

auth_router = Router()

@auth_router.message(F.contact)
async def handle_contact(message: Message):
    contact = message.contact
    user_phone_number = contact.phone_number
    chat_id = message.chat.id

    # TODO сделать другую анимацию
    search_message = await message.answer('Поиск компании...')

    company_id_by_contact = await bitrix.get_company_by_phone(user_phone_number)
    if company_id_by_contact:
        async with db:
            await db.add_contact(chat_id, user_phone_number, company_id_by_contact)
        await search_message.delete()
        await message.answer('Вы успешно вошли в Личный кабинет', reply_markup=main_menu())
    else:
        await search_message.delete()
        await message.answer('Не удалось найти компанию привязанную к вашему номеру. Обратитесь в нашу поддержку.', reply_markup=help_menu())
