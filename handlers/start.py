from aiogram import Router, F
from aiogram.types import Message
from keyboards import auth_menu

start_router = Router()


@start_router.message(F.text == "/start")
async def cmd_start(message: Message) -> None:
    """
    Начало работы с ботом. Запуск бота.
    """
    await message.answer("Для начала работы поделитесь своим номером.", reply_markup=auth_menu())