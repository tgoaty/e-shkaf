from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from os import getenv
from dotenv import load_dotenv
from bitrix_api.bitrix import BitrixAPI
from cash_memory.cash_manager import GlobalCacheManager
from db_handler import db_class
from logger_config import get_logger

load_dotenv()

logger = get_logger(__name__)

TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    logger.error("Не удалось получить TELEGRAM_TOKEN из переменных окружения.")
    raise ValueError("TELEGRAM_TOKEN не найден в переменных окружения")

bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher(storage=MemoryStorage())

try:
    db = db_class.Database()
except Exception as e:
    logger.error(f"Ошибка при инициализации базы данных: {e}")
    raise

try:
    bitrix = BitrixAPI()
except Exception as e:
    logger.error(f"Ошибка при инициализации Bitrix API: {e}")
    raise

cache_manager = GlobalCacheManager(db, bitrix)

logger.info("Все компоненты успешно инициализированы.")
