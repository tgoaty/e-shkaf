## Телеграм бот для информировния клиентов

#### Как запустить проект?

1. Установить Python 3.12
2. Склонировать репозиторий ```git clone https://github.com/tgoaty/e-shkaf```
3. Установить все зависимости ```pip install -r requirements.txt```
4. Развернуть PostgresSQL Базу данных
5. Получить PG_LINK для работы с базой данных:
   - В случае работы с online сервисами для хостинга БД, при создании PG_LINK сразу дают
   - В случае локального разворачивания БД:
     1. Установите PostgreSQL:  
        - Windows/Linux: Скачайте с [postgresql.org](https://www.postgresql.org/download/).  
     2. Создайте базу данных и пользователя:  
        ```bash
        psql -U postgres
        ```
        ```sql
        CREATE DATABASE mydb;
        CREATE USER myuser WITH PASSWORD 'mypassword';
        GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
        ```
     3. Сформируйте строку подключения:  
        ```
        postgres://<username>:<password>@<host>:<port>/<database>?sslmode=disable
        postgres://myuser:mypassword@localhost:5432/mydb?sslmode=disable
        ```
     4. Добавьте эту строку в файл `.env` как значение переменной `PG_LINK`.
6. Получить Домен и Токен Авторизации из битрикс:
 - Разработчикам -> Интеграции -> Выбираем нужную интеграцию -> Редактировать
 - Смотрим на поле Вебхук для вызова rest api
 - Пример: https://b24.el.ru/rest/2/asdfasdfasdf/
 - Такен авторизации - набор цифр и буков в концу (в примере asdfasdfasdf)
 - Домен остальная часть ссылки (в примере https://b24.el.ru/rest/2/)
8. Создать в корне проекта и заполнить файл .env по образцу:
    ```
    TELEGRAM_TOKEN=<ТОКЕН БОТА>
   
    HELPER_USERNAME=tgoaty (телеграм username человека из техподдержки)

    BITRIX_BASE_URL=<ДОМЕН БИТРИКСА>
    BITRIX_ACCESS_TOKEN=<ТОКЕН АВТОРИЗАЦИИ>

    PG_LINK=<ССЫЛКА ДЛЯ РАБОТЫ С БАЗОЙ ДАННЫХ>
   ```
9. Запустить бота ```python aiogram_run.py```

