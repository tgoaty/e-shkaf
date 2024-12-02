from aiogram import Router, F
from aiogram.types import CallbackQuery
from create_bot import bitrix, cache_manager

public_link_router = Router()


@public_link_router.callback_query(F.data.startswith("generate_link_"))
async def generate_public_link(callback_query: CallbackQuery) -> None:
    """
    Генерация публичной ссылки на папку с файлами о заказе.
    """
    order_id = callback_query.data.split("_")[2]
    public_link = None

    await callback_query.message.answer("Ищем папку заказа...")

    try:
        company_id = await cache_manager.get_company_id(callback_query.message.chat.id)
        company_data = await bitrix.get_company_title_and_inn_by_id(company_id)
        company_title = company_data['company_title']
    except Exception as e:
        await callback_query.answer(f"Ошибка при получении данных компании: {e}", show_alert=True)
        return

    try:
        folder_id = await cache_manager.folder_id(order_id, company_title)
        if folder_id:

            public_link = await bitrix.get_public_link(folder_id)
        else:
            await callback_query.answer("Папка для заказа не найдена.", show_alert=True)
    except Exception as e:
        await callback_query.answer(f"Ошибка при генерации ссылки: {e}", show_alert=True)

    if not public_link:
        await callback_query.message.answer(f"Не удалось найти папку заказа {order_id}. Повторите попытку позже.")
        return

    await callback_query.message.answer(
        text=f"Вот ссылка на папку заказа {order_id}:\n[Перейти к папке]({public_link})",
        disable_web_page_preview=True,
        parse_mode="Markdown"
    )
