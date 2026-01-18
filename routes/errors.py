from flask import jsonify, request
from core import log_error, log_request


class PixVaultError(Exception):
    """
    Базовое кастомное исключение PixVault.
    Используется для контролируемых ошибок (валидация, логика).
    """
    def __init__(self, message, status=400):
        super().__init__(message)
        self.message = message
        self.status = status


def register_error_handlers(app):
    """
    Регистрирует глобальные обработчики ошибок Flask.
    """

    @app.errorhandler(PixVaultError)
    def handle_pixvault_error(exc: PixVaultError):
        """
        Обработка контролируемых ошибок.
        Например: неправильный формат файла, превышение размера, неверные параметры.
        """
        log_error("PixVaultError", error=exc.message, status=exc.status)
        return jsonify({"error": exc.message}), exc.status

    @app.errorhandler(404)
    def handle_404(_):
        """
        Обработка отсутствующих маршрутов.
        """
        log_request(request)
        log_error("Route not found", path=request.path)
        return jsonify({"error": "Route not found"}), 404

    @app.errorhandler(500)
    def handle_500(exc):
        """
        Обработка непредвиденных ошибок.
        Скрывает детали от клиента, но логирует всё.
        """
        log_error("Internal server error", error=str(exc))
        return jsonify({"error": "Internal server error"}), 500