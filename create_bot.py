import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from os import getenv

from dotenv import load_dotenv

load_dotenv()

# на будущее
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# scheduler = AsyncIOScheduler(timezone='Asia/Barnaul')

# извлечение админов из .env
admins = [int(admin_id) for admin_id in getenv('ADMINS').split(',')]

# создание логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=getenv('TELEGRAM_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# храним данные бота в RAM
dp = Dispatcher(storage=MemoryStorage())