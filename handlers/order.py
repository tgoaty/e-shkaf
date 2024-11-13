from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from create_bot import bitrix
from keyboards import order_menu

order_router = Router()


@order_router.callback_query(F.data.startswith('order_'))
async def show_order_details(callback_query: CallbackQuery, state: FSMContext):
    order_id = callback_query.data.split('_')[1]
    details = await bitrix.get_order_details(order_id)
    back_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться к списку заказов", callback_data="back_to_orders")]
    ])
    description = (
        f"ID: {details['id']}\nНазвание: {details['title']}\nСтоимость: {details['amount']}\n"
        f"Дата производства: {details['close_date']}\nСтадия: {details['status']}\nСостав сделки:\n{details['products']}"
    )
    await callback_query.message.edit_text(description, reply_markup=back_button)
    await callback_query.answer()