import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from os import getenv

from bitrix_api.bitrix import BitrixAPI
from cash_memory.cash_manager import GlobalCacheManager
from db_handler import db_class
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()


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

# Инициализируем объект Битрикс API
bitrix = BitrixAPI()

# Инициализируем объект с Кеш Хранилищем
cache_manager = GlobalCacheManager(db, bitrix)