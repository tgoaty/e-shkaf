import time
from aiogram.fsm.storage.memory import MemoryStorage

global_storage = MemoryStorage()


class GlobalCacheManager:
    def __init__(self, db, bitrix, time_to_update: int = 600):
        self.storage = global_storage
        self.db = db
        self.bitrix = bitrix
        self.time_to_update = time_to_update

    async def _is_data_stale(self, data: dict, key: str) -> bool:
        """
        Проверяет, устарели ли данные в кэше.
        """
        current_time = time.time()
        return key not in data or current_time - data.get(f"{key}_timestamp", 0) > self.time_to_update

    async def _update_cache(self, key: int | str, cache_key: str, fetch_func, refresh=False, *args, **kwargs) -> any:
        """
        Универсальный метод для обновления данных в кэше.
        """
        data = await self.storage.get_data(key=key)
        if await self._is_data_stale(data, cache_key) or refresh:
            data[cache_key] = await fetch_func(*args, **kwargs)
            data[f"{cache_key}_timestamp"] = time.time()
            await self.storage.set_data(key=key, data=data)
        return data[cache_key]

    async def get_company_id(self, chat_id: int) -> int:
        """
        Получает или кэширует `company_id` для пользователя.
        """

        async def fetch_company_id():
            async with self.db:
                return await self.db.get_company_id_by_chat_id(chat_id)

        return await self._update_cache(chat_id, "company_id", fetch_company_id)

    async def get_orders(self, company_id: int, refresh: bool = False) -> list:
        """
        Получает или кэширует список заказов компании.
        """

        async def fetch_orders():
            return await self.bitrix.get_orders_by_company_id(company_id)

        return await self._update_cache(company_id, "orders", fetch_orders, refresh)

    async def order_details(self, order_id: str, refresh: bool = False) -> dict:
        """
        Получает или кэширует детали заказа.
        """

        async def fetch_order_details():
            return await self.bitrix.get_order_details(order_id)

        return await self._update_cache(order_id, "details", fetch_order_details, refresh)
