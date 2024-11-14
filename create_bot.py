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

# admins = [int(admin_id) for admin_id in getenv('ADMINS').split(',')]

bot = Bot(token=getenv('TELEGRAM_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher(storage=MemoryStorage())

db = db_class.Database()

bitrix = BitrixAPI()

cache_manager = GlobalCacheManager(db, bitrix)
