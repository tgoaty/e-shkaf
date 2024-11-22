from aiogram import Router, F
from aiogram.types import Message
from keyboards import profile_menu
from create_bot import bitrix, cache_manager

profile_router = Router()


@profile_router.message(F.text == 'Профиль')
async def cmd_start_3(message: Message):
    chat_id = message.from_user.id

    company_id = await cache_manager.get_company_id(chat_id)
    orders = await cache_manager.get_orders(company_id)
    contact_id = await bitrix.get_contact_id_by_company_id(company_id)

    full_name = await bitrix.get_full_name_by_contact_id(contact_id)
    manager = await bitrix.get_assigned_by_id(company_id)
    company_title = await bitrix.get_company_title_by_id(company_id)

    default_discount = None

    if not orders:
        orders = []

    await message.answer(
        f'''{full_name}
Менеджер: {manager}
Организация: {company_title}
Заказы в работе: {len(orders)}
Сумма заказов: {sum([float(order["amount"]) for order in orders])}
Ваша скидка: {default_discount}%''',
        reply_markup=profile_menu()
    )
