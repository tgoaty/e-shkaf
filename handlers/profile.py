from aiogram import Router, F
from aiogram.types import Message
from keyboards import profile_menu
from create_bot import bitrix, cache_manager

profile_router = Router()


@profile_router.message(F.text == "Профиль")
async def show_profile(message: Message) -> None:
    """
    Вывод общей информации о клиенте.
    """
    chat_id = message.from_user.id

    company_id = await cache_manager.get_company_id(chat_id)
    orders = await cache_manager.get_orders(company_id)
    contact_id = await bitrix.get_contact_id_by_company_id(company_id)
    if contact_id:
        full_name = await bitrix.get_full_name_by_contact_id(contact_id)
    else:
        full_name = ''
    manager_id = await bitrix.get_assigned_by_id(company_id)
    if manager_id:
        manager_name = await bitrix.get_responsible_name(manager_id)
    else:
        manager_name = ''
    company_title = await bitrix.get_company_title_by_id(company_id)

    orders = orders or []
    total_orders_amount = sum(float(order.get("amount", 0)) for order in orders)
    default_discount = 0

    profile_text = (
        f"{full_name}\n"
        f"Менеджер: {manager_name}\n"
        f"Организация: {company_title}\n"
        f"Заказы в работе: {len(orders)}\n"
        f"Сумма заказов: {total_orders_amount}\n"
        f"Ваша скидка: {default_discount}%"
    )

    await message.answer(profile_text, reply_markup=profile_menu())
