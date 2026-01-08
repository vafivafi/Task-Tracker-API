Task Tracker API 📝
Production-ready REST API для управления задачами на FastAPI + PostgreSQL с JWT аутентификацией


```bash
# 1. Запусти PostgreSQL
docker run -d --name postgres-task-tracker \
  -e POSTGRES_USER=tracker \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=task_tracker \
  -p 5432:5432 postgres:16
```
```
# 2. Установи зависимости
pip install -r requirements.txt
```
```
# 3. Запусти API
uvicorn app.main:app --reload
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
```
📋 API Эндпоинты
Аутентификация
```text
POST /api/v1/auth/register    # Регистрация
POST /api/v1/auth/login       # Логин → JWT токен
```
Задачи
```
GET    /api/v1/tasks/          # Список (все задачи)
POST   /api/v1/tasks/          # Создать задачу
GET    /api/v1/tasks/{id}      # Получить задачу
PUT    /api/v1/tasks/{id}      # Обновить
DELETE /api/v1/tasks/{id}      # Удалить
```
🏗️ Чистая архитектура
```
app/
├── api/
│   ├── v1/
│   │   ├── auth.py
│   │   └── tasks.py
│   └── deps.py
├── core/
│   ├── config.py
│   └── security.py
├── crud/
│   ├── task.py
│   └── user.py
├── loger/
│   └── log.py
├── models/
│   ├── task.py
│   └── user.py
├── schemas/
│   ├── task.py
│   └── user.py
├── main.py
└── settings.py

```
🛠 Технологии
FastAPI — высокопроизводительный API

PostgreSQL — надежная реляционная БД

SQLAlchemy 2.0 — ORM с типизацией

Pydantic v2 — валидация данных

JWT + secure-python-utils(argon2) — безопасная аутентификация
