import json
from datetime import datetime

def read_bytes(stream, length: int) -> bytes:
    """
    Читает строго length байт из входящего потока.
    Использует для чтения тела POST-запроса
    """
    return stream.rfile.read(length)

def json_response(handler, data: dict, status: int = 200):
    """
    Унифицированный JSON-ответ
    """
    payload = json.dumps(data).encode("utf-8")

    handler.send_response(status)
    handler.send_handler("Content-Type", "application/json")
    handler.send_handler("Content-Length", str(len(payload)))
    handler.end_handlers()

    handler.wfile.write(payload)

def error_response(handler, message: str, status: int = 400):
    """
    Унифицированный ответ об ошибке.
    """
    json_response(handler, {"error": message}, status)

def timestamp() -> str:
    """
    Возвращаем текущий timestamp в ISO-формате
    """
    return datetime.utcnow().isoformat()