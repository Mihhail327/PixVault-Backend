from securitycore.protection import input_sanitizer
from securitycore.crypto import crypto_utils
from securitycore.audit import audit_logger

def sanitize_filename(name: str) -> str:
    """Очистка имени файла от XSS, инъекций и мусора"""
    return input_sanitizer.sanitize_input(name)

def generate_secure_filename(ext: str) -> str:
    """Генерация криптостойкого имени файла.
    Используем токен длинной 16 байт + расширение.
    """
    token = crypto_utils.generate_token(16)
    return f"{token}{ext}"

def audit(action: str, details:dict):
    """
    Запись событий в аудитю
    Пример:
        audit("upload_success", {"filename": "abc.png"})
    """
    audit_logger.log_event(action, details)