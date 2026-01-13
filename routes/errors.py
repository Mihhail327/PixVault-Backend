from core.utils import error_response

def handle_not_found(handler):
    """
    Обработчик 404 ошибки.
    """
    return error_response(handler, "Маршрут не найден", status=404)

def handle_method_not_allowed(handler):
    """
    Обработчик 405 ошибки
    """
    return error_response(handler, "Метод не поддерживается", status=405)