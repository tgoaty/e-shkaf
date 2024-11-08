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
            'type': 'PHONE',  # Поиск по типу "PHONE"
            'values[]': phone_number
        }
        result = await self._request(method, params)

        if result["result"]:
            company_id = result["result"]["COMPANY"][0]
            logger.info(f"Найдена компания ID={company_id} с номером телефона {phone_number}.")
            return company_id
        else:
            logger.info(f"Компании с номером телефона {phone_number} не найдены.")
            return None
