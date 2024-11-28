import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import bitrix, cache_manager

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


@order_router.callback_query(F.data.startswith("generate_link_"))
async def generate_public_link(callback_query: CallbackQuery) -> None:
    """
    Генерация публичной ссылки на папку с файлами о заказе.
    """
    order_id = callback_query.data.split("_")[2]

    # Уведомление пользователя, что идет процесс поиска папки
    await callback_query.message.answer("Ищем папку заказа...")

    # Получение ID компании и названия компании
    try:
        company_id = await cache_manager.get_company_id(callback_query.message.chat.id)
        company_data = await bitrix.get_company_title_and_inn_by_id(company_id)
        company_title = company_data[('company_title'
                                      '')]
    except Exception as e:
        await callback_query.answer(f"Ошибка при получении данных компании: {e}", show_alert=True)
        return

    # Попытка получить публичную ссылку
    try:
        public_link = await bitrix.find_folder_by_order_id(order_id, company_title)
    except Exception as e:
        await callback_query.answer(f"Ошибка при генерации ссылки: {e}", show_alert=True)
        return

    if not public_link:
        await callback_query.message.answer("Не удалось найти папку заказа. Повторите попытку позже.")
        return

    # Отправка сообщения с публичной ссылкой
    await callback_query.message.answer(
        text=f"Вот ссылка на папку заказа:\n[Перейти к папке]({public_link})",
        disable_web_page_preview=True,
        parse_mode="Markdown"
    )

