import asyncpg
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self._pool = None
        self._db_url = os.getenv("PG_LINK")

        logger.info("Создан экземпляр Database с URL: %s", self._db_url)



    async def connect(self):
        """Подключаемся к базе данных и создаем пул соединений"""
        try:
            self._pool = await asyncpg.create_pool(dsn=self._db_url)
            logger.info("Подключение к базе данных установлено")
        except Exception as e:
            logger.error("Ошибка подключения к базе данных: %s", e)
            raise

    async def disconnect(self):
        """Закрываем соединение с базой данных"""
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
