from core.utils import json_response

def handle_index(handler):
    """
    Корневой маршрут.
    Возвращает базовую информацию о PixVault
    """
    return json_response(handler, {
        "service": "PixVault Backend",
        "status": "running"
    })