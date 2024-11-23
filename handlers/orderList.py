from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Union
from create_bot import bot, cache_manager
from keyboards import main_menu, manager_menu

orderList_router = Router()


def create_orders_keyboard(orders, refresh: bool) -> InlineKeyboardMarkup:
    """
    Создание inline_keyboard с списком заказов.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"{order['title']} - {order['status']}",
            callback_data=f"order_{order['id']}_{int(refresh)}"
        )] for order in orders
    ])


@orderList_router.message(F.text == "Список заказов")
@orderList_router.callback_query(F.data == "back_to_orders")
async def show_orders(event: Union[Message, CallbackQuery]) -> None:
    """
    Отрисовка списка заказов.
    """
    chat_id = event.from_user.id
    refresh = isinstance(event, Message)

    if refresh:
        await bot.send_chat_action(chat_id, ChatAction.TYPING)
        await event.answer("Поиск активных заказов 🔍", reply_markup=manager_menu())

    company_id = await cache_manager.get_company_id(chat_id)
    orders = await cache_manager.get_orders(company_id, refresh=refresh)

    if not orders:
        no_orders_text = "Заказы не найдены."
        if isinstance(event, Message):
            await event.answer(no_orders_text, reply_markup=main_menu())
        else:  # CallbackQuery
            await event.message.edit_text(no_orders_text, reply_markup=main_menu())
        return

    orders_text = "Список активных заказов:" if isinstance(event, CallbackQuery) else "Выберите заказ из списка ниже:"
    reply_markup = create_orders_keyboard(orders, refresh=refresh)

    if isinstance(event, Message):
        await bot.send_message(chat_id, orders_text, reply_markup=reply_markup)
    else:  # CallbackQuery
        await event.message.edit_text(orders_text, reply_markup=reply_markup)
        await event.answer()
