import os

"""Основные настройки сервера"""

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

"""
Настройка загрузки файлов
Максимальный размер файла (по умолчанию 5 МБ)
"""
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 5 * 1024 *1024))
# Разрешённые расширения
ALLOWED_EXTENSIONS = os.getenv(
    "ALLOWED_EXTENSIONS",
    ".jpg, .jpeg, .png, .gif"
).split(",")

# Путь хранения
IMAGES_DIR = os.getenv("IMAGES_DIR", "images")
LOGS_DIR = os.getenv("LOGS_DIR", "logs")

# Режим отладки
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

