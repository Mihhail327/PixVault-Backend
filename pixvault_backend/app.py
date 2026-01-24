import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from loguru import logger

from pixvault_backend.config import Config


# Инициализация расширений (создаются один раз)
db = SQLAlchemy()
migrate = Migrate()


def ensure_upload_folder(path: str) -> None:
    """
    Гарантирует, что папка для загрузок существует.
    Вынесено в отдельную функцию для чистоты фабрики.
    """
    os.makedirs(path, exist_ok=True)


def create_app():
    """
    Фабрика приложения.
    Создаёт и настраивает Flask-приложение.
    Такой подход упрощает тестирование, конфигурацию и масштабирование.
    """
    app = Flask(__name__)

    # Загружаем конфигурацию
    app.config.from_object(Config)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    # CORS (исправлено: resources вместо resource)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Импорт блюпринтов после инициализации расширений
    from pixvault_backend.routes.images import images_bp
    from pixvault_backend.routes.admin import admin_bp

    # Регистрация блюпринтов
    app.register_blueprint(images_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    # Создание папки для загрузок
    ensure_upload_folder(app.config["UPLOAD_FOLDER"])

    # Предупреждение о небезопасном ключе
    if app.config["SECRET_KEY"] == "dev-secret":
        logger.warning("Using insecure SECRET_KEY — set SECRET_KEY in .env")

    logger.info("PixVault backend initialized")

    return app