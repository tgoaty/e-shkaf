from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.types import Message
from create_bot import db, bitrix, bot
from keyboards import main_menu, help_menu

auth_router = Router()


@auth_router.message(F.contact)
async def handle_contact(message: Message):
    """
    Обработка контакта, отправленного пользователем.
    """
    contact = message.contact
    user_phone_number = contact.phone_number
    chat_id = message.chat.id

    await bot.send_chat_action(chat_id, ChatAction.TYPING)

    try:
        company_id = await bitrix.get_company_by_phone(user_phone_number)

        if company_id:
            await message.answer("Вы успешно вошли в Личный кабинет!", reply_markup=main_menu())
            async with db:
                await db.add_contact(chat_id, user_phone_number, company_id)
        else:
            await message.answer(
                "Не удалось найти компанию, привязанную к вашему номеру. Обратитесь в нашу поддержку.",
                reply_markup=help_menu()
            )
    except Exception:
        await message.answer(
            "Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже.",
            reply_markup=help_menu()
        )
