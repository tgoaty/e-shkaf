import asyncpg
import os
import logging
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()

# Настройка логгера
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self._pool = None
        self._db_url = os.getenv("PG_LINK")
        logger.info("Создан экземпляр Database с URL: %s", self._db_url)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def connect(self):
        try:
            self._pool = await asyncpg.create_pool(dsn=self._db_url)
            logger.info("Подключение к базе данных установлено")
            await self.create_table()
        except Exception as e:
            logger.error("Ошибка подключения к базе данных: %s", e)
            raise

    async def disconnect(self):
        if self._pool:
            await self._pool.close()
            logger.info("Соединение с базой данных закрыто")

    async def execute(self, query: str, *args):
        """Выполняем запрос без возврата данных (например, INSERT, UPDATE)"""
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.execute(query, *args)
        return result

    async def fetch(self, query: str, *args):
        """Выполняем запрос с возвратом данных (например, SELECT)"""
        async with self._pool.acquire() as connection:
            result = await connection.fetch(query, *args)
        return result

    async def fetchrow(self, query: str, *args):
        """Выполняем запрос, возвращающий одну строку"""
        async with self._pool.acquire() as connection:
            result = await connection.fetchrow(query, *args)
        return result

    async def fetchval(self, query: str, *args):
        """Выполняем запрос, возвращающий одно значение"""
        async with self._pool.acquire() as connection:
            result = await connection.fetchval(query, *args)
        return result

    async def create_table(self):
        """Создаёт таблицу user_contacts, если её нет, и добавляет столбец company_id_by_contact, если он отсутствует."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_contact_company (
            chat_id BIGINT PRIMARY KEY,
            phone_number TEXT NOT NULL,
            company_id_by_contact BIGINT  -- добавляем новый столбец
        );
        """
        await self.execute(create_table_query)
        logger.info("Таблица user_contacts создана или уже существует.")

    async def add_contact(self, chat_id: int, phone_number: str, company_id_by_contact: int):
        """Добавляет контакт в таблицу user_contacts с учетом company_id_by_contact"""
        insert_query = """
        INSERT INTO user_contact_company (chat_id, phone_number, company_id_by_contact)
        VALUES ($1, $2, $3)
        ON CONFLICT (chat_id) DO UPDATE SET phone_number = $2, company_id_by_contact = $3;
        """
        await self.execute(insert_query, chat_id, phone_number, company_id_by_contact)
        logger.info(
            f"Контакт с chat_id={chat_id}, номером телефона={phone_number} и company_id={company_id_by_contact} добавлен в базу данных.")
