from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards import manager_menu
from create_bot import bitrix, cache_manager

manager_router = Router()

managers = {
    '1': ['Николай', 'tgoaty']
    # здесь список всех менеджеров, в формате
    # 'id менеджера в crm': ['имя менеджера', 'юзернейм в телеграмме без "@"']
}


@manager_router.callback_query(F.data.startswith('manager_'))
async def order_manager(callback_query: CallbackQuery):
    _, manager_id, order_id = callback_query.data.split('_')
    name = managers[manager_id][0]
    username = managers[manager_id][1]
    message_to_manager = f'Здравствуйте {name} хотелось бы уточнить информацию по поводу заказа номер {order_id}.'
    await callback_query.message.answer(
        text=f'Здравствуйте, вы можете обратиться к нашему менеджеру в этом чате [Перейти в чат](https://t.me/{username}?text={message_to_manager})',
        reply_markup=manager_menu(),
        parse_mode="Markdown"
    )


@manager_router.message(F.text == 'Связаться с менеджером')
async def general_manager(message: Message):
    company_id = await cache_manager.get_company_id(message.chat.id)
    manager_id = await bitrix.get_assigned_by_id(company_id)
    name = managers[manager_id][0]
    username = managers[manager_id][1]
    message_to_manager = f'Здравствуйте {name}, хотелось бы уточнить иноформацию по компании номер {company_id}.'
    await message.answer(
        text=f'Здравствуйте, вы можете обратиться к нашему менеджеру в этом чате [Перейти в чат](https://t.me/{username}?text={message_to_manager})',
        reply_markup=manager_menu(),
        parse_mode="Markdown"
    )
