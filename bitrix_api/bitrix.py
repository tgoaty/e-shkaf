import aiohttp
import os
import logging

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class BitrixAPI:
    def __init__(self):
        self.base_url = os.getenv("BITRIX_BASE_URL")
        self.access_token = os.getenv("BITRIX_ACCESS_TOKEN")

        if not self.base_url or not self.access_token:
            logger.error("BASE_URL или ACCESS_TOKEN не найдены в переменных окружения.")

    async def _request(self, method, params):
        """
        Выполняет запрос к API Bitrix24.

        :param method: Метод API, например 'crm.company.list'
        :param params: Параметры запроса
        :return: Ответ JSON от API или None, если произошла ошибка
        """
        url = f"{self.base_url}{self.access_token}/{method}.json"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    logger.info(f"Запрос к {method} выполнен успешно.")
                    return await response.json()
            except aiohttp.ClientError as e:
                logger.error(f"Ошибка при выполнении запроса к {method}: {e}")
                return None

    async def get_company_by_phone(self, phone_number):
        """
        Находит компанию по номеру телефона.

        :param phone_number: Номер телефона для поиска
        :return: Список компаний с указанным номером телефона или None
        """
        method = 'crm.duplicate.findbycomm'
        params = {
            'type': 'PHONE',
            'values[]': phone_number
        }
        result = await self._request(method, params)

        if result.get("result"):
            company_id = result["result"]["COMPANY"][0]
            logger.info(f"Найдена компания ID={company_id} с номером телефона {phone_number}.")
            return company_id
        else:
            logger.info(f"Компании с номером телефона {phone_number} не найдены.")
            return None

    async def get_orders_by_company_id(self, company_id):
        """
        Получает заказы компании по её ID с полями: наименование, статус, ID и процент оплаты.

        :param company_id: ID компании
        :return: Список заказов или None, если произошла ошибка
        """
        method = 'crm.deal.list'
        params = {
            'filter[COMPANY_ID]': company_id,
            'select[]': ['TITLE', 'STAGE_ID', 'ID', 'OPPORTUNITY']
        }

        result = await self._request(method, params)

        if result and result.get("result"):
            orders = [
                {
                    "id": order["ID"],
                    "title": order["TITLE"],
                    "status": order["STAGE_ID"],
                    "amount": order.get("OPPORTUNITY", 0)
                }
                for order in result["result"]
            ]
            logger.info(f"Найдено {len(orders)} заказов для компании с ID={company_id}.")
            return orders
        else:
            logger.info(f"Заказы для компании с ID={company_id} не найдены.")
            return None

    async def get_order_details(self, order_id):
        method = 'crm.deal.get'
        params = {
            'id': order_id,
            'select[]': ['TITLE', 'OPPORTUNITY', 'CLOSEDATE', 'STAGE_ID', 'COMMENTS']
        }
        result = await self._request(method, params)

        if result and result.get("result"):
            order = result["result"]

            products = await self._get_order_products(order_id)

            order_details = {
                "id": order["ID"],
                "title": order["TITLE"],
                "amount": order.get("OPPORTUNITY", 0),
                "close_date": order.get("CLOSEDATE", "Не указана"),
                "status": order.get("STAGE_ID"),
                "products": products,
                "description": order.get("COMMENTS", "Описание отсутствует")
            }
            logger.info(f"Получены детали для заказа с ID={order_id}.")
            return order_details
        else:
            logger.info(f"Детали для заказа с ID={order_id} не найдены.")
            return None

    async def _get_order_products(self, order_id):
        method = 'crm.deal.productrows.get'
        params = {'id': order_id}
        result = await self._request(method, params)

        if result and result.get("result"):
            products = [
                f"{product['PRODUCT_NAME']} - {product['PRICE']} x {product['QUANTITY']}"
                for product in result["result"]
            ]
            logger.info(f"Найдено {len(products)} продуктов для заказа с ID={order_id}.")
            return "\n".join(products) if products else "Состав сделки не указан."
        else:
            logger.info(f"Продукты для заказа с ID={order_id} не найдены.")
            return "Состав сделки не указан."
