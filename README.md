## Телеграм бот для информировния клиентов

#### Как запустить проект?

1. Установить Python 3.12
2. Склонировать репозиторий ```git clone https://github.com/tgoaty/e-shkaf```
3. Установить все зависимости ```pip install -r requirements.txt```
4. Развернуть PostgresSQL Базу данных
5. Создать в корне проекта и заполнить файл .env по образцу:
    ```
    TELEGRAM_TOKEN=<ТОКЕН БОТА>

    BITRIX_BASE_URL=https://b24.electroshkaf.su/rest/1/
    BITRIX_ACCESS_TOKEN=<ТОКЕН АВТОРИЗАЦИИ>

    PG_LINK=<ССЫЛКА ДЛЯ РАБОТЫ С БАЗОЙ ДАННЫХ>
   ```
6. В фале handlers/help.py указать username специалиста техподдержки
7. Запустить бота ```python aiogram_run.py```

