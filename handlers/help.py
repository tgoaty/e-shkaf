from aiogram import Router, F
from aiogram.types import Message

help_router = Router()


@help_router.message(F.text == 'Связаться с поддержкой')
async def general_manager(message: Message):
    """
    Переводим в чат поддержки при технической ошибке.
    """
    username = "tgoaty"  # Username работника поддержки
    help_message = "Здравствуйте. Не получается зайти в бота."
    await message.answer(
        text=(
            f"Здравствуйте! Если у вас возникли трудности, вы можете обратиться за помощью в этот "
            f"[чат](https://t.me/{username}?text={help_message})."
        ),
        parse_mode="Markdown",
    )
