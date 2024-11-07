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
        """Создаёт таблицу user_contacts, если её нет"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_contacts (
            chat_id BIGINT PRIMARY KEY,
            phone_number TEXT NOT NULL
        );
        """
        await self.execute(create_table_query)
        logger.info("Таблица user_contacts создана или уже существует.")

    async def add_contact(self, chat_id: int, phone_number: str):
        """Добавляет контакт в таблицу user_contacts"""
        insert_query = """
        INSERT INTO user_contacts (chat_id, phone_number)
        VALUES ($1, $2)
        ON CONFLICT (chat_id) DO UPDATE SET phone_number = $2;
        """
        await self.execute(insert_query, chat_id, phone_number)
        logger.info(f"Контакт с chat_id={chat_id} и номером телефона={phone_number} добавлен в базу данных.")
