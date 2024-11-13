from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Union
from aiogram.fsm.context import FSMContext
from create_bot import bot, cache_manager, logger

orderList_router = Router()

hello_message = (
    """
Список активных заказов.

В активные заказы попадают те сделки, которые были полностью оплачены или оплачены частично по договоренности.
    """
)


def orders_keyboard(orders):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{order['title']} - {order['status']}", callback_data=f"order_{order['id']}")]
        for order in orders
    ])


@orderList_router.message(F.text == 'Список заказов')
@orderList_router.callback_query(F.data == 'back_to_orders')
async def show_orders(union: Union[Message, CallbackQuery], state: FSMContext):
    chat_id = union.from_user.id
    await bot.send_chat_action(chat_id, ChatAction.TYPING)

    refresh = isinstance(union, Message)

    company_id = await cache_manager.get_company_id(chat_id)
    orders = await cache_manager.get_orders(company_id, refresh=refresh)

    if isinstance(union, Message):
        await union.answer(
            hello_message,
            reply_markup=orders_keyboard(orders) if orders else "Заказы не найдены."
        )
    elif isinstance(union, CallbackQuery):
        await union.message.edit_text(
            hello_message,
            reply_markup=orders_keyboard(orders) if orders else "Заказы не найдены."
        )
        await union.answer()
