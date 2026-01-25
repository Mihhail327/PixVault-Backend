import os
from dotenv import load_dotenv

# Загружаем .env только вне продакшена
if os.getenv("FLASK_ENV") != "production":
    load_dotenv()


class Config:
    """
    Центральная конфигурация приложения.
    Все настройки вынесены сюда, чтобы не размазывать их по коду.
    """

    # Строка подключения к базе данных
    _db_url = os.getenv("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = (os.getenv("DATABASE_URL") or "sqlite:///pixvault.db").replace("postgres://", "postgresql://")

    # Отключаем устаревший механизм отслеживания изменений
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Секретный ключ для сессий и безопасности
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # Папка, куда сохраняются изображения (нормализуем путь)
    UPLOAD_FOLDER = os.path.abspath(os.getenv("UPLOAD_FOLDER", "uploads"))

    # Максимальный размер загружаемого файла (5 MB)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    # Разрешённые форматы изображений (в верхнем регистре)
    ALLOWED_EXTENSIONS = {"PNG", "JPG", "JPEG", "GIF", "WEBP"}

    # Количество элементов на странице (для пагинации)
    ITEMS_PER_PAGE = 25