from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import bitrix, cache_manager

order_router = Router()


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
        f"**Наименование сделки:** {details['title']}\n"
        f"**Статус сделки:** {details['status']}\n"
        f"**Ответственный:** {details['responsible_name']}\n"
        f"**ID:** {details['id']}\n"
        f"**Сумма сделки:** {details['amount']}\n"
        f"**Ответственный РП** {details['responsible_rp']}\n"
        f"**Дата отгрузки:** {details['shipping_date']}\n"
        f"**Дата передачи в ОТК:** {details['otk_transfer_date']}\n"
        f"**Дата поставки материалов:** {details['materials_delivery_date']}\n"
        f"**Процент оплаты сделки:** {details['payment_percent']}%\n"
    )

    back_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти к папке заказа", callback_data=f"generate_link_{order_id}")],
        [InlineKeyboardButton(text="Связаться с менеджером",
                              callback_data=f"manager_{details['responsible_id']}_{details['id']}")],
        [InlineKeyboardButton(text="Вернуться к списку заказов", callback_data="back_to_orders")]
    ])

    await callback_query.message.edit_text(description, reply_markup=back_button, parse_mode="Markdown")
    await callback_query.answer()


@order_router.callback_query(F.data.startswith("generate_link_"))
async def generate_public_link(callback_query: CallbackQuery) -> None:
    """
    Генерация публичной ссылки на папку с файлами о заказе.
    """
    order_id = callback_query.data.split("_")[2]
    public_link = await bitrix.get_public_link(order_id)

    if not public_link:
        await callback_query.answer("Не удалось сгенерировать ссылку. Повторите позже.", show_alert=True)
        return

    back_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти к папке заказа", url=public_link)],
        [InlineKeyboardButton(text="Вернуться к списку заказов", callback_data="back_to_orders")]
    ])

    try:
        await callback_query.message.edit_reply_markup(reply_markup=back_button)
        await callback_query.answer("Публичная ссылка сгенерирована!")
    except Exception as e:
        await callback_query.answer(f"Ошибка: {e}", show_alert=True)
