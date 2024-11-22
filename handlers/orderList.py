from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Union
from create_bot import bot, cache_manager
from keyboards import main_menu

orderList_router = Router()


def orders_keyboard(orders, refresh):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{order['title']} - {order['status']}", callback_data=f"order_{order['id']}_{int(refresh)}")]
        for order in orders
    ])


@orderList_router.message(F.text == 'Список заказов')
@orderList_router.callback_query(F.data == 'back_to_orders')
async def show_orders(union: Union[Message, CallbackQuery]):
    chat_id = union.from_user.id
    if isinstance(union, Message):
        await bot.send_chat_action(chat_id, ChatAction.TYPING)

    refresh = isinstance(union, Message)

    company_id = await cache_manager.get_company_id(chat_id)
    orders = await cache_manager.get_orders(company_id, refresh=refresh)

    if isinstance(union, Message):
        if orders:
            await union.answer(
                "Список активных заказов:",
                reply_markup=orders_keyboard(orders, refresh=refresh)
            )
        else:
            await union.answer("Заказы не найдены.", reply_markup=main_menu())
    elif isinstance(union, CallbackQuery):
        if orders:
            await union.message.edit_text(
                "Список активных заказов:",
                reply_markup=orders_keyboard(orders, refresh=refresh)
            )
        else:
            await union.message.edit_text("Заказы не найдены.", reply_markup=main_menu())
        await union.answer()
