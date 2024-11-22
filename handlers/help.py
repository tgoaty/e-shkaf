from aiogram import Router, F
from aiogram.types import Message

help_router = Router()

@help_router.message(F.text == 'Связаться с поддержкой')
async def general_manager(message: Message):
    username = 'tgoaty' # юзернейм человека из техподдержки
    message_to_helper = f'Здравствуйте. Не получается зайти в бота.'
    await message.answer(
        text=f'Здравствуйте, вы можете обратиться за помощью в этот чат [Перейти в чат](https://t.me/{username}?text={message_to_helper})',
        parse_mode="Markdown"
    )
