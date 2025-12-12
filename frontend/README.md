# Frontend (Vue 3 + TypeScript)

## Запуск
1. Установить зависимости: `npm install`
2. Запустить dev-сервер: `npm run dev`

Vite настроен на проксирование запросов `/api/*` на `http://127.0.0.1:8000`, поэтому CORS не требуется.

## Страницы
- `Продукция` — список продукции (`/products`) и форма добавления/редактирования (`/products/new`, `/products/:id`)
- `Цеха производства` — список цехов для выбранного продукта и расчет сырья (`/products/:id/workshops`)
- `Партнеры` — CRUD партнеров (`/partners`, `/partners/new`, `/partners/:id`)
- `Склад и материалы` — CRUD поставщиков и материалов (`/warehouse`, формы `.../suppliers/*`, `.../materials/*`)
- `Производство` — CRUD цехов (`/production`, формы `.../workshops/*`)
- `Сотрудники` — CRUD сотрудников (`/staff`, `/staff/new`, `/staff/:id`)
