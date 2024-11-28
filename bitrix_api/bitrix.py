import os
import aiohttp
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

    async def _request(self, method: str, params: dict) -> dict | None:
        """
        Выполняет запрос к API Bitrix24.
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

    @staticmethod
    def _check_response(result: dict, key: str) -> bool:
        """
        Проверяет, содержит ли результат необходимый ключ.
        """
        return result is not None and key in result and result[key]

    async def get_company_by_phone(self, phone_number: str) -> int | None:
        """
        Находит компанию по номеру телефона.
        """
        method = 'crm.duplicate.findbycomm'
        params = {
            'type': 'PHONE',
            'values[]': [phone_number],
            'entity_type': 'COMPANY'
        }
        result = await self._request(method, params)

        if self._check_response(result, "result") and "COMPANY" in result["result"]:
            companies = result["result"]["COMPANY"]
            if companies:
                company_id = companies[0]
                logger.info(f"Найдена компания ID={company_id} с номером телефона {phone_number}.")
                return company_id
        logger.info(f"Компании с номером телефона {phone_number} не найдены.")
        return None

    async def get_orders_by_company_id(self, company_id: int) -> list | None:
        """
        Получает заказы компании по её ID.
        """
        method = 'crm.deal.list'
        params = {
            'filter[COMPANY_ID]': company_id,
            'filter[TYPE_ID]': 'SALE',
            'select[]': ['TITLE', 'STAGE_ID', 'ID', 'OPPORTUNITY']
        }

        result = await self._request(method, params)

        if self._check_response(result, "result"):
            orders = [
                {
                    "id": order["ID"],
                    "title": order["TITLE"],
                    "status": await get_normal_status_name(order["STAGE_ID"]),
                    "amount": order.get("OPPORTUNITY", 0)
                }
                for order in result["result"]
            ]
            # убираем не нужные стадии
            orders = [order for order in orders if order["status"] not in ['Собрать информацию для ТКП']]
            logger.info(f"Найдено {len(orders)} заказов для компании с ID={company_id}.")
            if len(orders) > 0:
                return orders
            else:
                return None
        logger.info(f"Заказы для компании с ID={company_id} не найдены.")
        return None

    async def get_user_field(self, user_id: int, field: str) -> str | None:
        """
        Получает указанное поле пользователя по его ID.
        """
        method = 'user.get'
        params = {'ID': user_id}

        result = await self._request(method, params)
        if self._check_response(result, "result"):
            user_data = result["result"][0]
            return user_data.get(field, None)
        logger.warning(f"Пользователь с ID={user_id} не найден или поле {field} отсутствует.")
        return None

    async def get_responsible_name(self, responsible_id: int) -> str:
        """
        Получить имя ответственного пользователя по его ID.
        """
        if not responsible_id:
            return "Не указан"
        name = await self.get_user_field(responsible_id, 'NAME')
        last_name = await self.get_user_field(responsible_id, 'LAST_NAME')
        return f"{name or ''} {last_name or ''}".strip()

    async def get_site_by_assigned_id(self, assigned_by_id: int | None) -> str:
        """
        Получает телеграмм username из поля сайт (PERSONAL_WWW) ответственного менеджера по его ID (ASSIGNED_BY_ID).
        """
        if not assigned_by_id:
            logger.warning("Не указан ASSIGNED_BY_ID.")
            return "Не указан ASSIGNED_BY_ID"

        method = 'user.get'
        params = {'ID': assigned_by_id}

        result = await self._request(method, params)

        if self._check_response(result, "result"):
            user_data = result["result"][0]
            user_site = user_data.get('PERSONAL_WWW')
            if user_site:
                logger.info(f"Username для пользователя с ID={assigned_by_id}: {user_site}")
                return user_site
            logger.warning(f"Username для пользователя с ID={assigned_by_id} отсутствует.")
            return " Username не указан"
        logger.error(f"Ошибка получения данных пользователя с ID={assigned_by_id}.")
        return "Ошибка получения данных пользователя"

    async def get_order_details(self, order_id: int) -> dict | None:
        """
        Получает детализированную информацию о заказе.
        """
        method = 'crm.deal.get'
        params = {'id': order_id}

        result = await self._request(method, params)

        if not self._check_response(result, "result"):
            logger.info(f"Детали для заказа с ID={order_id} не найдены.")
            return None

        order = result["result"]
        responsible_id = order.get('ASSIGNED_BY_ID')
        responsible_name = await self.get_responsible_name(responsible_id)

        def get_field_value(field: str, default: str = "Не указана") -> str:
            return order.get(field, default)

        order_details = {
            "title": order["TITLE"],
            "status": await get_normal_status_name(order["STAGE_ID"]),
            "responsible_name": responsible_name,
            "id": order["ID"],
            "amount": order.get("OPPORTUNITY", 0),
            "responsible_rp": order.get("UF_CRM_1591784142", "Не указан"),  # Ответственный РП
            "shipping_date": get_field_value('UF_CRM_1593059797889', "Не указан"),  # Дата отгрузки
            "otk_transfer_date": get_field_value('UF_CRM_1593059727643', "Не указан"),  # Дата передачи в ОТК
            "materials_delivery_date": get_field_value('UF_CRM_1593016707093', "Не указан"),  # Дата поставки материалов

            "payment_percent": get_field_value('UF_CRM_1682643592', "Не указан"),  # Процент оплаты сделки

            "responsible_id": responsible_id,

        }

        logger.info(f"Получены детали для заказа с ID={order_id}.")
        return order_details

    async def _get_order_products(self, order_id: int) -> str:
        """
        Получает список продуктов, связанных с заказом.
        """
        method = 'crm.deal.productrows.get'
        params = {'id': order_id}

        result = await self._request(method, params)

        if self._check_response(result, "result"):
            products = [
                f"{product['PRODUCT_NAME']} - {product['PRICE']} x {product['QUANTITY']}"
                for product in result["result"]
            ]
            if products:
                logger.info(f"Найдено {len(products)} продуктов для заказа с ID={order_id}.")
                return "\n".join(products)
        logger.info(f"Продукты для заказа с ID={order_id} не найдены.")
        return "Состав сделки не указан."

    async def find_folder_by_order_id(self, order_id: int, company_title: str, parent_id: str = "18818") -> str | None:
        """
        Рекурсивный метод поиска папки по ID заказа с учетом сортировки, фильтрации и пагинации.

        Как работает:

        В пределах папки "заявки" проверяет каждую папку на наличие папки с id заказа в названии

        Если в папке "заявки" есть папка, с названием, совпадающим с названием компании,
        то в первую очередь поиск папки осуществляется там.
        """
        method = 'disk.folder.getChildren'
        start = 0
        found_folders = []

        while True:
            params = {
                'id': parent_id,
                'filter[TYPE]': 'folder',
                'start': start
            }

            result = await self._request(method, params)

            if not self._check_response(result, "result"):
                break

            folders = result.get("result", [])
            found_folders.extend(folders)

            if not folders:
                break

            start += len(folders)

        folders = sorted(
            found_folders,
            key=lambda folder: folder.get("UPDATE_TIME", ""),
            reverse=True
        )

        for folder in folders:
            folder_name = folder.get("NAME", "")
            folder_id = folder.get("ID", "")

            if folder_name.lower() == company_title.lower():
                logger.info(f"Найдена папка компании '{company_title}' (ID={folder_id}).")

                subfolder_link = await self.find_folder_by_order_id(order_id, company_title, parent_id=folder_id)
                if subfolder_link:
                    return subfolder_link

        for folder in folders:
            folder_name = folder.get("NAME", "")
            folder_id = folder.get("ID", "")

            if any(
                    part.isdigit() and len(part) >= 4 and part != str(order_id)
                    for part in folder_name.split()
            ):
                continue

            if str(order_id) in folder_name:
                public_link = await self.get_public_link(folder_id)
                if public_link:
                    logger.info(f"Найдена папка для заказа ID={order_id}, публичная ссылка: {public_link}")
                    return public_link
                logger.error(f"Не удалось получить публичную ссылку для папки ID={folder_id}.")

            subfolder_link = await self.find_folder_by_order_id(order_id, company_title, parent_id=folder_id)
            if subfolder_link:
                return subfolder_link

        return None

    async def get_public_link(self, folder_id: int) -> str | None:
        """
        Получить публичную ссылку на папку.
        """
        method = 'disk.folder.getExternalLink'
        params = {'id': str(folder_id)}
        result = await self._request(method, params)

        if self._check_response(result, "result"):
            public_link = result["result"]
            logger.info(f"Публичная ссылка для папки ID={folder_id}: {public_link}")
            return public_link
        logger.error(f"Публичная ссылка для папки ID={folder_id} отсутствует или произошла ошибка.")
        return None

    async def get_assigned_by_id(self, company_id: int) -> int | None:
        """
        Получает ID ответственного пользователя (ASSIGNED_BY_ID) для указанной компании.
        """
        method = 'crm.company.get'
        params = {'id': company_id}

        result = await self._request(method, params)

        if self._check_response(result, "result"):
            assigned_by_id = result["result"].get("ASSIGNED_BY_ID")
            logger.info(f"ID ответственного пользователя для компании с ID={company_id}: {assigned_by_id}.")
            return assigned_by_id

        logger.warning(f"Не удалось получить ID ответственного пользователя для компании с ID={company_id}.")
        return None

    async def get_full_name_by_contact_id(self, contact_id: int) -> str:
        """
        Получает данные контакта по ID и возвращает его полное имя.
        """
        method = 'crm.contact.get'
        params = {'id': contact_id}

        result = await self._request(method, params)

        if self._check_response(result, "result"):
            contact_data = result["result"]
            name = contact_data.get('NAME', '')
            second_name = contact_data.get('SECOND_NAME', '')
            last_name = contact_data.get('LAST_NAME', '')

            full_name = f"{name} {second_name} {last_name} ".replace('None ', '').strip()
            logger.info(f"Извлечённое полное имя контакта с ID={contact_id}: {full_name}")
            return full_name or "Имя контакта отсутствует"

        logger.error(f"Ошибка получения данных контакта с ID={contact_id}.")
        return "Ошибка получения данных контакта"

    async def get_contact_id_by_company_id(self, company_id: int) -> int | None:
        """
        Получает идентификатор контакта по идентификатору компании.
        """
        method = 'crm.company.contact.items.get'
        params = {'id': company_id}

        result = await self._request(method, params)

        if self._check_response(result, "result"):
            contact_items = result["result"]
            if contact_items:
                contact_id = contact_items[0]['CONTACT_ID']
                logger.info(f"Найден контакт с ID={contact_id} для компании с ID={company_id}.")
                return contact_id

            logger.info(f"Для компании с ID={company_id} контакты не найдены.")
            return None

        logger.error(f"Ошибка получения контактов для компании с ID={company_id}.")
        return None

    async def get_company_title_and_inn_by_id(self, company_id: int) -> dict:
        """
        Получает название компании по её ID и ИНН из поля UF_CRM_6658A426B3467.
        """
        method = 'crm.company.get'
        params = {'id': company_id}

        result = await self._request(method, params)

        if self._check_response(result, "result"):
            company_data = result["result"]
            company_title = company_data.get("TITLE", "")
            inn = company_data.get("UF_CRM_6658A426B3467", "")

            logger.info(f"Название компании с ID={company_id}: {company_title}, ИНН: {inn}")

            return {
                "company_title": company_title if company_title else "Название компании отсутствует",
                "inn": inn if inn else "ИНН отсутствует"
            }
        else:
            logger.warning(f"Компания с ID={company_id} не найдена.")
            return {"company_title": "Название компании отсутствует", "inn": "ИНН отсутствует"}

    async def get_all_deal_categories_and_stages(self):
        """
        Получает все воронки и их этапы.
        """

        method = 'crm.dealcategory.list'
        result = await self._request(method, {})

        if not self._check_response(result, "result"):
            return None

        categories = result.get("result", [])
        all_stages = {}
        categories.append({'ID': '0'})
        for category in categories:
            category_id = category.get('ID')
            if not category_id:
                continue

            method = 'crm.dealcategory.stage.list'
            params = {'id': category_id}
            stages_result = await self._request(method, params)

            if not self._check_response(stages_result, "result"):
                continue

            stages = stages_result.get("result", [])
            for stage in stages:

                status_id = stage.get('STATUS_ID')
                if status_id:
                    all_stages[status_id] = [stage.get("NAME", ""), stage.get("SORT", 0)]
        return all_stages if all_stages else None
