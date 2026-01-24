
---

# **PixVault Backend**

PixVault Backend — это модульная, безопасная и контейнеризованная серверная часть для PixVault: сервиса хранения и управления изображениями.  
Проект построен на Flask, SQLAlchemy, PostgreSQL и полностью готов к работе в Docker‑окружении.

---

## 🚀 **Функциональность**

- Загрузка изображений  
- Хранение файлов на сервере  
- Метаданные в PostgreSQL  
- Получение списка изображений  
- Доступ к файлам по URL  
- Миграции через Flask‑Migrate  
- CORS для фронтенда  
- Чистая архитектура: `routes/`, `services/`, `models/`, `config/`

---

## 🧱 **Технологии**

| Компонент | Используется |
|----------|--------------|
| Backend Framework | Flask |
| ORM | SQLAlchemy |
| Миграции | Flask‑Migrate |
| База данных | PostgreSQL |
| Контейнеризация | Docker |
| Управление зависимостями | Poetry |
| Оркестрация | Makefile |

---

## 📦 **Установка и запуск (локально)**

### 1. Установка зависимостей
```
poetry install
```

### 2. Настройка окружения  
Создай `.env`:

```
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/pixvault
UPLOAD_FOLDER=uploads
```

### 3. Миграции
```
poetry run flask --app pixvault_backend.app:create_app db upgrade
```

### 4. Запуск сервера
```
make dev
```

Сервер будет доступен на:

```
http://localhost:8000
```

---

## 🐳 **Запуск через Docker**

### 1. Собрать образ
```
make build
```

### 2. Запустить контейнер
```
make run
```

---

## 🗄️ **Миграции (через Makefile)**

```
make db-init
make db-migrate
make db-upgrade
```

---

## 📁 **Структура проекта**

```
PixVaultBackend/
│
├── pixvault_backend/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── routes/
│   ├── services/
│   └── utils/
│
├── migrations/
├── requirements.txt
├── Dockerfile
├── Makefile
├── pyproject.toml
└── README.md
```

---

## 🔐 **Безопасность**

- SQL‑инъекции исключены благодаря SQLAlchemy ORM  
- Файлы сохраняются только в разрешённую директорию  
- CORS ограничен  
- Конфигурация вынесена в `.env`

---

## 🧭 **Философия проекта** 

PixVault Backend создан как инженерный артефакт:
- минимализм в архитектуре
- чистые слои ответственности
- предсказуемость и расширяемость
- готовность к продакшен‑инфраструктуре


