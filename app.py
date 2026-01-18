from flask import Flask
from config import Config
from core.storage import init_storage
from routes.errors import register_error_handlers
from core.logging import init_logging

# Blueprints
from routes.index import index_bp
from routes.upload import upload_bp


def create_app():
    """
    Создаёт и настраивает Flask-приложение.
    Вся инициализация вынесена сюда, чтобы код был чистым и тестируемым.
    """
    app = Flask(__name__)
    app.config["DEBUG"] = Config.DEBUG
    app.config["SECRET_KEY"] = Config.SECRET_KEY

    # Инициализация подсистем
    init_storage()       # создаёт директорию для изображений
    init_logging()       # создаёт директорию для логов и файл app.log
    register_error_handlers(app)  # глобальные обработчики ошибок

    # Регистрация маршрутов
    app.register_blueprint(index_bp)
    app.register_blueprint(upload_bp)

    return app


# Экземпляр приложения (используется index.py)
app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)