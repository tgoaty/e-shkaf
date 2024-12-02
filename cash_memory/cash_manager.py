import time
from aiogram.fsm.storage.memory import MemoryStorage

global_storage = MemoryStorage()

class GlobalCacheManager:
    def __init__(self, db, bitrix):
        self.storage = global_storage
        self.db = db
        self.bitrix = bitrix
        self.time_to_update = 600

    async def get_company_id(self, chat_id: int):
        """
        Получает или кэширует company_id для всех пользователей.
        """
        data = await self.storage.get_data(key=chat_id)
        if "company_id" not in data:
            async with self.db:
                data["company_id"] = await self.db.get_company_id_by_chat_id(chat_id)
            await self.storage.set_data(key=chat_id, data=data)
        return data["company_id"]

    async def get_orders(self, company_id: int, refresh: bool = False):
        """
        Получает или кэширует список заказов для всех пользователей.
        """
        data = await self.storage.get_data(key=company_id)
        current_time = time.time()

        if refresh or "orders" not in data or current_time - data.get("orders_timestamp", 0) > self.time_to_update:
            orders = await self.bitrix.get_orders_by_company_id(company_id)
            data["orders"] = orders
            data["orders_timestamp"] = current_time
            await self.storage.set_data(key=company_id, data=data)
        return data["orders"]

    async def order_details(self, order_id: str, refresh: bool = False):
        """
        Получает или кэширует детали заказа.
        """
        data = await self.storage.get_data(key=order_id)
        current_time = time.time()

        if refresh or "details" not in data or current_time - data.get("details_timestamp", 0) > self.time_to_update:
            details = await self.bitrix.get_order_details(order_id)
            data["details"] = details
            data["details_timestamp"] = current_time
            await self.storage.set_data(key=order_id, data=data)
        return data["details"]

    async def get_deal_categories(self) -> list:
        """
        Получает или кэширует список категорий сделок.
        """
        data = await self.storage.get_data(key="stages")

        if "stages" not in data:
            stages = await self.bitrix.get_all_deal_categories_and_stages()
            data["stages"] = stages
            await self.storage.set_data(key="stages", data=data)
        return data["stages"]

    async def folder_id(self, order_id: str, company_title: str):
        data = await self.storage.get_data(key=order_id + 'f')

        if "folder_id" not in data:
            folder_id = await self.bitrix.get_folder_id_by_order_id(order_id, company_title)
            data["folder_id"] = folder_id
            await self.storage.set_data(key=order_id + 'f', data=data)
        return data["folder_id"]
