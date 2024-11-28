from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards import manager_menu
from create_bot import bitrix, cache_manager

manager_router = Router()


@manager_router.callback_query(F.data.startswith("manager_"))
async def order_manager(callback_query: CallbackQuery):
    """
    Связь с менеджером по конкретному заказу.
    """
    _, manager_id, order_id = callback_query.data.split("_")
    name = await bitrix.get_responsible_name(manager_id)
    username = await bitrix.get_site_by_assigned_id(manager_id)
    if username:
        message_to_manager = (
            f"Здравствуйте {name.split()[0]}, хотелось бы уточнить информацию по поводу заказа номер {order_id}."
        )
        text = (
            f"Здравствуйте, вы можете обратиться к нашему менеджеру в этом "
            f"[чате](https://t.me/{username}?text={message_to_manager})"
        )
    else:
        text = "Контакт вашего менеджера не найдет, обратитесь в нашу поддержку"
    await callback_query.message.answer(
        text=text,
        reply_markup=manager_menu(),
        parse_mode="Markdown",
    )


@manager_router.message(F.text == "Связаться с менеджером")
async def general_manager(message: Message):
    """
    Связь с менеджером по компании.
    """
    company_id = await cache_manager.get_company_id(message.chat.id)
    company_data = await bitrix.get_company_title_and_inn_by_id(company_id)
    manager_id = await bitrix.get_assigned_by_id(company_id)
    name = await bitrix.get_responsible_name(manager_id)
    username = await bitrix.get_site_by_assigned_id(manager_id)

    if username:
        message_to_manager = (
            f"Здравствуйте {name.split()[0]}, хотелось бы уточнить информацию по компании {company_data['title']} ({company_id})."
        )
        text = (
            f"Здравствуйте, вы можете обратиться к нашему менеджеру в этом "
            f"[чате](https://t.me/{username}?text={message_to_manager})"
        )
    else:
        text = "Контакт вашего менеджера не найдет, обратитесь в нашу поддержку"
    await message.answer(
        text=text,
        reply_markup=manager_menu(),
        parse_mode="Markdown",
    )
