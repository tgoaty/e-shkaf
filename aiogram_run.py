import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from os import getenv

from sqlalchemy.util import await_fallback
from db_handler import db_class  # Импортируем наш класс базы данных
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Загружаем переменные окружения из .env
load_dotenv()

# Планировщик задач
scheduler = AsyncIOScheduler(timezone='Asia/Barnaul')

# Извлечение списка администраторов из .env
admins = [int(admin_id) for admin_id in getenv('ADMINS').split(',')]

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=getenv('TELEGRAM_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Хранение данных бота в памяти
dp = Dispatcher(storage=MemoryStorage())

# Инициализируем объект базы данных
db = db_class.Database()


# Логгирование подключения к бд
# TODO причесать файл
async def on_startup():
    try:
        await db.connect()
        logger.info("Бот успешно подключен к базе данных.")
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        await bot.close()
        raise e

    await db.disconnect()

async def main():
    await on_startup()

if __name__ == "__main__":
    asyncio.run(main())
