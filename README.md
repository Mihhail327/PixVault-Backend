
---

# 📘 PixVault — Secure Image Upload Backend

PixVault — это модульный, безопасный и тестируемый backend‑сервис для загрузки изображений.  
Он построен на Flask, использует библиотеку **SecurityCore** и оформлен с Docker‑структурой, тестами и Makefile.

## 🚀 Возможности

- Загрузка изображений через REST API (`POST /upload`)
- Проверка расширений, размера и имени файла
- Генерация безопасных имён (UUID)
- Хранение файлов в `images/`
- Аудит и логирование в `logs/`
- Полное покрытие тестами (pytest)
- Контейнеризация через Docker и Compose

## 🧱 Структура проекта

```
pixvault-backend/
├── app.py                  # Точка входа: Flask-приложение и регистрация маршрутов
├── config.py               # Конфигурация, env, константы
│
├── core/                   # Ядро логики (артефакты)
│   ├── security.py         # Интеграция SecurityCore (санитизация, безопасные имена)
│   ├── storage.py          # Работа с файлами (сохранение, удаление, путь)
│   ├── validation.py       # Проверка расширений, размера, имени
│   ├── logging.py          # Логи + аудит
│   └── utils.py            # Вспомогательные функции
│
├── routes/                 # Маршруты (как мини-контроллеры)
│   ├── upload.py           # POST /upload
│   ├── index.py            # GET /
│   └── errors.py           # Обработка ошибок
│
├── tests/                  # Pytest тесты
│   ├── test_upload.py
│   ├── test_validation.py
│   ├── test_security.py
│   └── test_storage.py
│
├── Dockerfile          # Бэкенд
│
├── images/                 # Volume: загруженные изображения
├── logs/                   # Volume: логи и аудит
├── requirements.txt        # Зависимости Python
├── Makefile                # Удобные команды (run, test, build)
└── README.md               # Документация проекта
```

## 🔐 SecurityCore

PixVault использует библиотеку **SecurityCore** — независимый модуль безопасности, отвечающий за:

- Проверку расширений  
- Проверку размера  
- Генерацию безопасных имён  
- Санитизацию и аудит  
- Минимальный API, не зависящий от Flask

SecurityCore подключается через `core/security.py` и используется во всех слоях PixVault.

## 📡 API

### `POST /upload`

Загрузка изображения.

**Параметры:**

- `file` — файл изображения (multipart/form-data)

**Ответ (успех):**

```json
{
  "status": "success",
  "id": "generated_filename.png"
}
```

**Ответ (ошибка):**

```json
{
  "error": "Invalid file extension"
}
```

## 🧪 Тестирование

Проект покрыт тестами:

```
make test
```

Покрыты модули:

- storage  
- validation  
- security  
- upload endpoint  

## ⚙️ Конфигурация

Все параметры задаются через `config.py` или переменные окружения:

- `IMAGES_DIR` — директория хранения  
- `LOGS_DIR` — директория логов  
- `MAX_FILE_SIZE` — максимальный размер файла  
- `ALLOWED_EXTENSIONS` — разрешённые расширения  
- `DEBUG` — режим отладки  

## 🐳 Docker

PixVault полностью контейнеризован:

- `docker/Dockerfile` — backend  



## 🛠 Makefile

Упрощённые команды:

```
make run           # Запуск сервера
make test          # Прогон тестов
make lint          # flake8
make format        # black
make docker-build  # Сборка образа
make docker-run    # Запуск контейнера
make clean         # Очистка __pycache__
```

## 📄 Лицензия

MIT License.

---
