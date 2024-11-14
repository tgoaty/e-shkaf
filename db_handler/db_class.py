import asyncpg
import os
from logger_config import get_logger
from dotenv import load_dotenv
import asyncio

load_dotenv()

logger = get_logger(__name__)

class Database:
    def __init__(self):
        self._pool = None
        self._db_url = os.getenv("PG_LINK")
        self._reconnect_delay = 1

        logger.info("Создан экземпляр Database с URL: %s", self._db_url)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def connect(self):
        """Подключаемся к базе данных и создаем пул соединений"""
        try:
            self._pool = await asyncpg.create_pool(dsn=self._db_url)
            logger.info("Подключение к базе данных установлено")
            await self.create_table()
        except Exception as e:
            logger.error("Ошибка подключения к базе данных: %s", e)
            raise

    async def disconnect(self):
        """Закрываем соединение с базой данных"""
        if self._pool:
            await self._pool.close()
            logger.info("Соединение с базой данных закрыто")

    async def _ensure_pool(self):
        """Проверяет состояние пула и ожидает его восстановления при закрытии"""
        while not self._pool:
            try:
                await self.connect()
            except Exception as e:
                logger.error(f"Не удалось подключиться к базе данных: {e}. Повтор через {self._reconnect_delay} сек.")
                await asyncio.sleep(self._reconnect_delay)  # Ожидание перед повтором

    async def execute(self, query: str, *args):
        """Выполняем запрос без возврата данных (например, INSERT, UPDATE)"""
        await self._ensure_pool()
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.execute(query, *args)
        return result

    async def fetch(self, query: str, *args):
        """Выполняем запрос с возвратом данных (например, SELECT)"""
        await self._ensure_pool()
        async with self._pool.acquire() as connection:
            result = await connection.fetch(query, *args)
        return result

    async def fetchrow(self, query: str, *args):
        """Выполняем запрос, возвращающий одну строку"""
        await self._ensure_pool()
        async with self._pool.acquire() as connection:
            result = await connection.fetchrow(query, *args)
        return result

    async def fetchval(self, query: str, *args):
        """Выполняем запрос, возвращающий одно значение"""
        await self._ensure_pool()
        async with self._pool.acquire() as connection:
            result = await connection.fetchval(query, *args)
        return result

    async def create_table(self):
        """Создаёт таблицу user_contacts, если её нет."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_contact_company (
            chat_id BIGINT PRIMARY KEY,
            phone_number TEXT NOT NULL,
            company_id BIGINT
        );
        """
        await self.execute(create_table_query)
        logger.info("Таблица user_contacts создана или уже существует.")

    async def add_contact(self, chat_id: int, phone_number: str, company_id: int):
        """Добавляет контакт в таблицу user_contacts с учетом company_id_by_contact"""
        insert_query = """
        INSERT INTO user_contact_company (chat_id, phone_number, company_id)
        VALUES ($1, $2, $3)
        ON CONFLICT (chat_id) DO UPDATE SET phone_number = $2, company_id = $3;
        """
        await self.execute(insert_query, chat_id, phone_number, company_id)
        logger.info(
            f"Контакт с chat_id={chat_id}, номером телефона={phone_number} и company_id={company_id} добавлен в базу данных.")

    async def get_company_id_by_chat_id(self, chat_id: int):
        query = """
           SELECT company_id
           FROM user_contact_company
           WHERE chat_id = $1;
           """
        company_id = await self.fetchval(query, chat_id)
        if company_id is not None:
            logger.info(f"Найден company_id={company_id} для chat_id={chat_id}.")
        else:
            logger.info(f"Компания для chat_id={chat_id} не найдена.")
        return company_id
