import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from loguru import logger
from werkzeug.exceptions import RequestEntityTooLarge

from pixvault_backend.config import Config

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()

def ensure_upload_folder(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)

    # =========================
    # ОБРАБОТКА ОШИБОК (Внутри фабрики)
    # =========================
    @app.errorhandler(413)
    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(e):
        # Возвращаем JSON, чтобы JS на фронте не упал с SyntaxError
        return jsonify({
            "error": "You are trying to upload an image larger than 5 MB"
        }), 413

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from pixvault_backend.routes.images import images_bp
    from pixvault_backend.routes.admin import admin_bp

    app.register_blueprint(images_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    ensure_upload_folder(app.config["UPLOAD_FOLDER"])

    if app.config["SECRET_KEY"] == "dev-secret":
        logger.warning("Using insecure SECRET_KEY — set SECRET_KEY in .env")

    logger.info("PixVault backend initialized")

    return app