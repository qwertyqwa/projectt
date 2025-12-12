# Django backend для «Комфорт»

## Запуск
1. Установить зависимости: `pip install --user --break-system-packages -r backend/requirements.txt` (или в виртуальное окружение).
2. Запуск сервера: `python3 backend/manage.py runserver 8000`.
3. Проверка: `GET http://127.0.0.1:8000/api/health`.

База `furniture.db` подключена напрямую; её путь задан относительно корня проекта.

## REST API
- `GET /api/products` — список продукции с подсчитанным временем изготовления.
- `GET /api/products/<id>` — карточка продукции с детализацией по цехам.
- `POST /api/products` — добавить продукцию (поля: `article`, `name`, `min_partner_price`, `product_type_id`, `material_type_id`).
- `PUT /api/products/<id>` — редактировать продукцию (те же поля).
- `GET /api/product-types` — список типов продукции для выпадающего списка.
- `GET /api/material-types` — список типов материалов для выпадающего списка.

## Расчет времени изготовления
1. Для продукции суммируются значения `manufacture_hours` из таблицы `product_workshop`.
2. Пропуски учитываются как 0.
3. Результат округляется вверх до целого неотрицательного числа часов.
