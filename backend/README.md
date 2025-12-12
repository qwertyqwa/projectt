# Django backend для «Комфорт»

## Запуск
### Рекомендуемое окружение
Создайте виртуальное окружение (venv), чтобы зависимости не ставились в систему:
- Windows (PowerShell): `python -m venv .venv` и затем `.\.venv\Scripts\Activate.ps1`
- Windows (cmd): `python -m venv .venv` и затем `.venv\Scripts\activate.bat`
- Linux/Mac: `python3 -m venv .venv` и затем `source .venv/bin/activate`

### Быстрый старт (с нуля из Excel)
1. Установить зависимости: `pip install -r backend/requirements.txt`
2. Создать и заполнить базу из файлов `*_import.xlsx`: `python import.py`
3. Применить миграции Django (создание таблиц для CRUD): `python backend/manage.py migrate`
4. Запуск сервера: `python backend/manage.py runserver 8000`
5. Проверка: `GET http://127.0.0.1:8000/api/health`

### Где лежит база данных
По умолчанию используется `furniture.db` в корне проекта.

Если нужно использовать другой файл БД (например, чтобы не портить оригинал), задайте переменную окружения `DJANGO_DB_PATH` и используйте её во всех командах:
- Windows (PowerShell): `$env:DJANGO_DB_PATH="furniture_app.db"`
- Windows (cmd): `set DJANGO_DB_PATH=furniture_app.db`
- Linux/Mac: `export DJANGO_DB_PATH=furniture_app.db`

Затем:
- `python import.py`
- `python backend/manage.py migrate`
- `python backend/manage.py runserver 8000`

Если видите ошибку `no such table: partner` (или другие таблицы CRUD) — значит не выполнены миграции: запустите `python backend/manage.py migrate`.

## REST API
- `GET /api/products` — список продукции с подсчитанным временем изготовления.
- `GET /api/products/<id>` — карточка продукции с детализацией по цехам.
- `POST /api/products` — добавить продукцию (поля: `article`, `name`, `min_partner_price`, `product_type_id`, `material_type_id`).
- `PUT /api/products/<id>` — редактировать продукцию (те же поля).
- `DELETE /api/products/<id>` — удалить продукцию.
- `GET /api/product-types` — список типов продукции для выпадающего списка.
- `GET /api/material-types` — список типов материалов для выпадающего списка.
- `GET /api/products/<id>/workshops` — список цехов для производства продукции.
- `POST /api/raw-material/calculate` — расчет количества сырья (возвращает `raw_material_amount`, при ошибке `-1`).
- `GET/POST /api/partners`, `GET/PUT/DELETE /api/partners/<id>` — CRUD партнеров.
- `GET/POST /api/suppliers`, `GET/PUT/DELETE /api/suppliers/<id>` — CRUD поставщиков.
- `GET/POST /api/materials`, `GET/PUT/DELETE /api/materials/<id>` — CRUD материалов.
- `GET/POST /api/employees`, `GET/PUT/DELETE /api/employees/<id>` — CRUD сотрудников.
- `GET/POST /api/workshops`, `GET/PUT/DELETE /api/workshops/<id>` — CRUD цехов.

## Расчет времени изготовления
1. Для продукции суммируются значения `manufacture_hours` из таблицы `product_workshop`.
2. Пропуски учитываются как 0.
3. Результат округляется вверх до целого неотрицательного числа часов.
