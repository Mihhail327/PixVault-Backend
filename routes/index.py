from flask import Blueprint, jsonify, request
from core.logging import log_request

# Blueprint для корневого маршрута
index_bp = Blueprint("index", __name__)


@index_bp.route("/", methods=["GET"])
def index():
    """
    Корневой маршрут PixVault Backend.
    Возвращает базовую информацию о состоянии сервиса.
    Используется для health-check, мониторинга и тестирования доступности API.
    """

    # Логируем входящий запрос (метод, путь, IP)
    log_request(request)

    # Возвращаем JSON-ответ с информацией о сервисе
    return jsonify({
        "service": "PixVault Backend",
        "status": "running"
    })