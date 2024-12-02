from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import cache_manager

order_router = Router()


def format_date(date_str):
    year, month, day = date_str.split('T')[0].split('-')
    return '.'.join([day, month, year])


@order_router.callback_query(F.data.startswith("order_"))
async def show_order_details(callback_query: CallbackQuery) -> None:
    """
    Вывод подробной информации о заказе.
    """
    _, order_id, refresh = callback_query.data.split("_")
    refresh = bool(int(refresh))

    details = await cache_manager.order_details(order_id, refresh=refresh)

    if not details:
        await callback_query.answer("Не удалось найти информацию по заказу.", show_alert=True)
        return

    description = (
        f"Наименование сделки: {details['title']}\n"
        f"Статус сделки: {details['status']}\n"
        f"Ответственный: {details['responsible_name']}\n"
        f"ID: {details['id']}\n"
        f"Сумма сделки: {details['amount']}\n"
        f"Ответственный РП {details['responsible_rp']}\n"
        f"Дата отгрузки: {format_date(details['shipping_date'])}\n"
        f"Дата передачи в ОТК: {format_date(details['otk_transfer_date'])}\n"
        f"Дата поставки материалов: {format_date(details['materials_delivery_date'])}\n"
        f"Процент оплаты сделки: {details['payment_percent']}%\n"
    )

    back_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти к папке заказа", callback_data=f"generate_link_{order_id}")],
        [InlineKeyboardButton(text="Связаться с менеджером",
                              callback_data=f"manager_{details['responsible_id']}_{details['id']}")],
        [InlineKeyboardButton(text="Вернуться к списку заказов", callback_data="back_to_orders")]
    ])

    await callback_query.message.edit_text(description, reply_markup=back_button, parse_mode="Markdown")
    await callback_query.answer()
