from aiogram import Router, F
from aiogram.types import Message
from os import getenv
from dotenv import load_dotenv

load_dotenv()

help_router = Router()


@help_router.message(F.text == 'Связаться с поддержкой')
async def general_manager(message: Message):
    """
    Переводим в чат поддержки при технической ошибке.
    """


    username = getenv("HELPER_USERNAME")  # Username работника поддержки

    help_message = ""
    await message.answer(
        text=(
            f"Здравствуйте! Если у вас возникли трудности, вы можете обратиться за помощью в этот "
            f"[чат](https://t.me/{username}?text={help_message})."
        ),
        parse_mode="Markdown",
    )
