from securitycore import (
    input_sanitizer,
    sanitize_xss,
    sanitize_sql_input,
    ensure_safe_path,
    ensure_safe_filename,
    generate_token,
    verify_token,
    audit,
)

# === Санитизация входных данных ===

def sanitize_payload(payload: dict) -> dict:
    """
    Применяет input_sanitizer ко всем значениям словаря.
    Используется для входящих JSON‑данных.
    """
    return {
        key: input_sanitizer(value)
        for key, value in payload.items()
    }


# === Безопасные пути и имена файлов ===

def safe_filename(filename: str) -> str:
    """
    Проверяет и нормализует имя файла.
    """
    return ensure_safe_filename(filename)


def safe_path(path: str) -> str:
    """
    Проверяет, что путь не содержит path traversal.
    """
    return ensure_safe_path(path)


# === Защита от XSS и SQL‑инъекций ===

def protect_xss(text: str) -> str:
    return sanitize_xss(text)


def protect_sql(text: str) -> str:
    return sanitize_sql_input(text)


# === Токены ===

def create_access_token(data: dict, expires_in: int = 3600) -> str:
    """
    Генерирует токен с данными и временем жизни.
    """
    return generate_token(data, expires_in=expires_in)


def verify_access_token(token: str) -> dict:
    """
    Проверяет токен и возвращает payload.
    """
    return verify_token(token)


# === Аудит ===

def log_event(event: str, context: dict = None):
    """
    Логирует событие через SecurityCore.audit.
    """
    audit(event, context or {})