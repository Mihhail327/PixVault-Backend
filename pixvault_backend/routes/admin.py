from flask import Blueprint, jsonify, request, current_app
from pixvault_backend.services.backup import create_backup
from loguru import logger

# Административный Blueprint — отдельный модуль для служебных операций
admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/backup", methods=["POST"])
def backup():
    """
    Эндпоинт для создания резервной копии.

    Безопасность:
    1. Ограничение по IP (локальный доступ).
    2. Логирование действий админа через Loguru.
    """

    # ВАЖНО: Если приложение за Nginx, нужно использовать
    # Werkzeug ProxyFix, иначе remote_addr всегда будет 127.0.0.1
    client_ip = request.remote_addr

    # Проверка на локальный адрес
    if client_ip not in ("127.0.0.1", "::1"):
        logger.warning(f"Unauthorized backup attempt from IP: {client_ip}")
        return jsonify({"error": "Access denied: Localhost only"}), 403

    try:
        logger.info("Starting manual backup via admin endpoint...")

        # Вызываем логику бэкапа
        # Путь сохраняем в переменную для ответа
        backup_path = create_backup()

        logger.success(f"Backup successfully created at: {backup_path}")

        return jsonify({
            "status": "success",
            "message": "Backup created successfully",
            "path": backup_path
        }), 200

    except Exception as e:
        # Логируем ошибку, чтобы не гадать, почему не создался файл
        logger.error(f"Backup failed: {str(e)}")
        return jsonify({"error": "Internal server error during backup"}), 500