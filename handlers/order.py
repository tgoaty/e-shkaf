from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import cache_manager

order_router = Router()


def format_date(date_str):
    if not date_str:
        return "Не указана"

    try:
        date_part = date_str.split('T')[0]
        year, month, day = date_part.split('-')
        return '.'.join([day, month, year])
    except (ValueError, AttributeError):
        # Логгируем некорректное значение для анализа
        print(f"Некорректный формат даты: {date_str}")
        return "Некорректный формат"


def format_percent(percent):
    if percent == '165':
        return 'Оплачено 100%'
    if percent == '166':
        return 'Сделка оплачена не полностью'
    if percent == '167':
        return 'Сделка не оплачена'
    return 'Не указан'


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
        f"Дата отгрузки по договору: {format_date(details['shipping_date'])}\n"
        f"Процент оплаты: {format_percent(details['payment_percent'])}\n"
    )

    back_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти к папке заказа", callback_data=f"generate_link_{order_id}")],
        [InlineKeyboardButton(text="Связаться с менеджером",
                              callback_data=f"manager_{details['responsible_id']}_{details['id']}")],
        [InlineKeyboardButton(text="Вернуться к списку заказов", callback_data="back_to_orders")]
    ])

    await callback_query.message.edit_text(description, reply_markup=back_button, parse_mode="Markdown")
    await callback_query.answer()
