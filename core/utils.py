import os
import mimetypes
import secrets
from datetime import datetime
from io import BytesIO


# === Время ===

def now_iso() -> str:
    """
    Возвращает текущее время в ISO‑формате.
    """
    return datetime.utcnow().isoformat()


# === Строки ===

def normalize_str(value: str) -> str:
    """
    Убирает пробелы по краям и нормализует строку.
    """
    return value.strip() if isinstance(value, str) else value


# === Расширения файлов ===

def get_extension(filename: str) -> str:
    """
    Возвращает расширение файла в нижнем регистре.
    """
    if "." not in filename:
        return ""
    return filename.rsplit(".", 1)[-1].lower()


# === MIME‑тип ===

def guess_mime(filename: str) -> str:
    """
    Определяет MIME‑тип по имени файла.
    """
    mime, _ = mimetypes.guess_type(filename)
    return mime or "application/octet-stream"


# === BytesIO ===

def to_bytesio(data: bytes) -> BytesIO:
    """
    Превращает bytes в BytesIO.
    """
    buffer = BytesIO()
    buffer.write(data)
    buffer.seek(0)
    return buffer


# === Генерация коротких ID ===

def short_id(length: int = 12) -> str:
    """
    Генерирует короткий криптостойкий ID.
    Пример: 'a9f3b1c8d4e2'
    """
    return secrets.token_hex(length // 2)