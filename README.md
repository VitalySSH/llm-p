# llm-p — Защищённый API для работы с LLM

Серверное приложение на FastAPI, предоставляющее защищённый API
для взаимодействия с большой языковой моделью (LLM) через
сервис OpenRouter.

## Возможности

- Регистрация и аутентификация пользователей (JWT)
- Взаимодействие с LLM через OpenRouter
- Сохранение истории диалога в SQLite
- Swagger UI с кнопкой Authorize

## Структура проекта

```
llm_p/
├── pyproject.toml
├── README.md
├── .env.example
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── errors.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   │   └── models.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── chat.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── chat_messages.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── openrouter_client.py
│   │
│   ├── usecases/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── chat.py
│   │
│   └── api/
│       ├── __init__.py
│       ├── deps.py
│       ├── routes_auth.py
│       └── routes_chat.py
│
└── app.db
```

## Установка и запуск

### 1. Установить uv

```bash
pip install uv
```

### 2. Инициализировать проект и создать виртуальное окружение

```bash
uv venv
source .venv/bin/activate  # MacOS/Linux
# .venv\Scripts\activate.bat  # Windows
```

### 3. Установить зависимости

```bash
uv pip install -r <(uv pip compile pyproject.toml)
```

### 4. Настроить переменные окружения

Скопировать `.env.example` в `.env` и вставить свой
API-ключ OpenRouter:

```bash
cp .env.example .env
```

Отредактировать `.env`, указав ключ в поле
`OPENROUTER_API_KEY=`.

### 5. Проверить качество кода

```bash
ruff check
```

### 6. Запустить приложение

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

После запуска Swagger UI доступен по адресу:
http://0.0.0.0:8000/docs

## Демонстрация работы

### Регистрация пользователя (POST /auth/register)

Email для регистрации: `student_sharonov@email.com`

![Регистрация](https://github.com/VitalySSH/llm-p/blob/main/app/screenshots/01_register.png)

### Логин и получение JWT (POST /auth/login)

![Логин](https://github.com/VitalySSH/llm-p/blob/main/app/screenshots/02_login.png)

### Авторизация через Swagger (кнопка Authorize)

![Authorize](https://github.com/VitalySSH/llm-p/blob/main/app/screenshots/03_authorize.png)

### Профиль пользователя (GET /auth/me)

![Профиль](https://github.com/VitalySSH/llm-p/blob/main/app/screenshots/04_me.png)

### Запрос к LLM (POST /chat)

![Чат](https://github.com/VitalySSH/llm-p/blob/main/app/screenshots/05_chat.png)

### История диалога (GET /chat/history)

![История](https://github.com/VitalySSH/llm-p/blob/main/app/screenshots/06_history.png)

### Удаление истории (DELETE /chat/history)

![Удаление](https://github.com/VitalySSH/llm-p/blob/main/app/screenshots/07_delete_history.png)
