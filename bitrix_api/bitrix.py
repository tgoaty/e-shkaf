import aiohttp
import os
from logger_config import get_logger

from dotenv import load_dotenv

from utils.status_normalization import get_normal_status_name

load_dotenv()

logger = get_logger(__name__)


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

        # Check if the result is not None and contains the expected keys
        if result is not None and "result" in result and "COMPANY" in result["result"]:
            # Ensure that "COMPANY" is a list and has at least one element
            if isinstance(result["result"]["COMPANY"], list) and result["result"]["COMPANY"]:
                company_id = result["result"]["COMPANY"][0]
                logger.info(f"Найдена компания ID={company_id} с номером телефона {phone_number}.")
                return company_id
            else:
                logger.info(f"Компании с номером телефона {phone_number} не найдены.")
                return None
        else:
            logger.warning(f"Unexpected result format or no company found for phone number {phone_number}: {result}")
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
            # TODO изменить под bitrix компании
             #'filter[STAGE_ID][]': ['C1:PREPARATION', 'C1:PREPAYMENT_INVOICE', 'C1:EXECUTING', 'C1:FINAL_INVOIC',
             #                      'C1:WON',
             #                     'C1:LOSE', 'C1:APOLOGY'],
            'filter[TYPE_ID]': 'SALE',
            'select[]': ['TITLE', 'STAGE_ID', 'ID', 'OPPORTUNITY']
        }

        result = await self._request(method, params)

        if result and result.get("result"):
            orders = [
                {
                    "id": order["ID"],
                    "title": order["TITLE"],
                    #"status": get_normal_status_name(order["STAGE_ID"]),
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

    async def get_responsible_name(self, responsible_id):
        """Получить имя ответственного пользователя по его ID."""
        if not responsible_id:
            return "Не указан"

        user_method = 'user.get'
        user_params = {
            'ID': responsible_id
        }
        user_result = await self._request(user_method, user_params)

        if user_result and user_result.get('result'):
            responsible_user = user_result['result'][0]
            responsible_name = f"{responsible_user.get('NAME', '')} {responsible_user.get('LAST_NAME', '')}"
            return responsible_name
        else:
            return "Не указан"

    async def get_order_details(self, order_id):
        method = 'crm.deal.get'
        params = {
            'id': order_id,
            'select[]': [
                'TITLE', 'OPPORTUNITY', 'CLOSEDATE', 'STAGE_ID', 'COMMENTS',
                'ASSIGNED_BY_ID', 'UF_CRM_1682643499', 'UF_CRM_1682643527', 'UF_CRM_1682643555', 'UF_CRM_1682643581'
            ]
        }
        result = await self._request(method, params)

        if result and result.get("result"):
            order = result["result"]

            responsible_id = order.get('ASSIGNED_BY_ID', None)
            responsible_name = await self.get_responsible_name(responsible_id)

            shipping_date = order.get('UF_CRM_1682643527', 'Не указана')  # Дата отгрузки
            otk_transfer_date = order.get('UF_CRM_1682643555', 'Не указана')  # Дата передачи в ОТК
            materials_delivery_date = order.get('UF_CRM_1682643581', 'Не указана')  # Дата поставки материалов
            payment_percent = order.get('UF_CRM_1682643592', 'Не указан')  # Процент оплаты сделки

            order_details = {
                "id": order["ID"],
                "title": order["TITLE"],
                "amount": order.get("OPPORTUNITY", 0),
                "close_date": order.get("CLOSEDATE", "Не указана"),
                #"status": get_normal_status_name(order["STAGE_ID"]),
                "status": order.get("STAGE_ID", "Не указана"),
                "responsible_name": responsible_name,
                "responsible_id": responsible_id,
                "shipping_date": shipping_date,
                "otk_transfer_date": otk_transfer_date,
                "materials_delivery_date": materials_delivery_date,
                "payment_percent": payment_percent,
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

    async def find_folder_by_order_id(self, order_id):
        method = 'disk.folder.search'
        params = {
            'filter[NAME]': f'{order_id}',
            'filter[TYPE]': 'folder'
        }

        result = await self._request(method, params)

        if result and result.get("result"):
            for folder in result["result"]:
                folder_name = folder.get("NAME", "")
                if result.search(f"\\b{order_id}\\b", folder_name):
                    public_link = await self.get_public_link(folder["ID"])
                    if public_link:
                        logger.info(f"Найдена папка для заказа ID={order_id}, публичная ссылка: {public_link}")
                        return public_link
            logger.info(f"Папка с ID заказа {order_id} не найдена.")
        return None

    async def get_public_link(self, folder_id):

        method = 'disk.folder.getexternallink'
        params = {
            'id': folder_id
        }

        result = await self._request(method, params)
        logger.info(f"Ответ от Bitrix для папки {folder_id}: {result}")

        if result is not None and "result" in result:
            public_link = result["result"]
            if public_link:
                logger.info(f"Публичная ссылка для папки ID={folder_id} получена: {public_link}")
                return public_link
            else:
                logger.error(f"Публичная ссылка для папки ID={folder_id} не найдена в ответе.")
        else:
            logger.error(f"Некорректный ответ от Bitrix для папки ID={folder_id}: {result}")

        return None

    async def get_assigned_by_id(self, company_id):
        """
        Получает ID ответственного пользователя (ASSIGNED_BY_ID) для указанной компании.
        """
        method = 'crm.company.get'
        params = {
            'id': company_id,
            'select': ['ASSIGNED_BY_ID']
        }

        result = await self._request(method, params)

        if result and result.get("result"):
            assigned_by_id = result["result"].get("ASSIGNED_BY_ID")
            logger.info(f"ID ответственного пользователя для компании с ID={company_id}: {assigned_by_id}.")
            return assigned_by_id
        else:
            logger.warning(f"Не удалось получить ID ответственного пользователя для компании с ID={company_id}.")
            return None

    async def get_full_name_by_contact_id(self, contact_id: int) -> str:
        """Получает данные контакта по ID и возвращает его полное имя."""
        method = 'crm.contact.get'
        params = {
            'id': contact_id
        }

        try:
            result = await self._request(method, params)
            if result and 'result' in result:
                contact_data = result['result']

                name = contact_data.get('NAME', '')
                second_name = contact_data.get('SECOND_NAME', '')
                last_name = contact_data.get('LAST_NAME', '')

                full_name = f"{name} {second_name} {last_name}".strip().replace('None', '')
                logger.info(f"Извлечённое полное имя: {full_name}")
                return full_name
            else:
                logger.error(f"Ошибка запроса: {result}")
                return "Ошибка получения данных контакта"
        except Exception as e:
            logger.error(f"Ошибка при запросе данных контакта: {e}")
            return "Ошибка при запросе данных контакта"

    async def get_contact_id_by_company_id(self, company_id: int) -> int:
        """Получает идентификатор контакта по идентификатору компании."""
        method = 'crm.company.contact.items.get'
        params = {
            'id': company_id
        }
        result = await self._request(method, params)
        if result and 'result' in result:
            contact_items = result['result']
            if contact_items:
                contact_id = contact_items[0]['CONTACT_ID']
                logger.info(f"Найден контакт с ID={contact_id} для компании с ID={company_id}.")
                return contact_id
            else:
                logger.info(f"Для компании с ID={company_id} контакты не найдены.")
        else:
            logger.error(f"Ошибка получения контактов для компании с ID={company_id}.")
        return None

    async def get_company_title_by_id(self, company_id: int) -> str:
        """ Получает название компании по её ID."""
        method = 'crm.company.get'
        params = {
            'id': company_id
        }
        try:
            result = await self._request(method, params)
            if result and 'result' in result:
                company_data = result['result']
                company_title = company_data.get('TITLE', '')

                if company_title:
                    logger.info(f"Название компании: {company_title}")
                    return company_title
                else:
                    logger.warning(f"Название компании отсутствует для company_id={company_id}")
                    return "Название компании отсутствует"
            else:
                logger.error(f"Ошибка получения данных компании: {result}")
                return "Ошибка получения данных компании"
        except Exception as e:
            logger.error(f"Ошибка при запросе данных компании: {e}")
            return "Ошибка при запросе данных компании"
