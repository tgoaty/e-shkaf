from aiogram.fsm.storage.memory import MemoryStorage

global_storage = MemoryStorage()

class GlobalCacheManager:
    def __init__(self, db, bitrix):
        self.storage = global_storage
        self.db = db
        self.bitrix = bitrix

    async def get_company_id(self, chat_id: int):
        """Получает или кэширует company_id для всех пользователей."""
        data = await self.storage.get_data(key=chat_id)
        if "company_id" not in data:
            async with self.db:
                data["company_id"] = await self.db.get_company_id_by_chat_id(chat_id)
            await self.storage.set_data(key=chat_id, data=data)
        return data["company_id"]

    async def get_orders(self, company_id: int, refresh: bool = False):
        """Получает или кэширует список заказов для всех пользователей."""
        data = await self.storage.get_data(key=company_id)
        if refresh or "orders" not in data:
            orders = await self.bitrix.get_orders_by_company_id(company_id)
            data["orders"] = orders
            await self.storage.set_data(key=company_id, data=data)
        return data["orders"]