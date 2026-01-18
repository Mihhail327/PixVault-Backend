import logging
import json
import os
from datetime import datetime
from securitycore import audit_json
from config import Config


# === Пути к логам ===

LOG_DIR = Config.LOG_DIR
APP_LOG = os.path.join(LOG_DIR, "app.log")
AUDIT_LOG = os.path.join(LOG_DIR, "audit.log")


def init_logging():
    """
    Инициализирует систему логирования PixVault Backend.
    Создаёт директорию логов и настраивает логгер.
    """

    # Создаём директорию для логов
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("pixvault")

    # Чтобы не добавлять хендлеры повторно при hot-reload
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # === File handler ===
    file_handler = logging.FileHandler(APP_LOG, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    ))

    # === Stream handler (для Docker) ===
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    ))

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.info("Logging initialized")

    return logger


# Получаем логгер после инициализации
logger = logging.getLogger("pixvault")


# === Структурированное логирование ===

def log_info(message: str, **context):
    """
    Логирует информационное сообщение.
    """
    if context:
        message = f"{message} | {json.dumps(context, ensure_ascii=False)}"
    logger.info(message)


def log_error(message: str, **context):
    """
    Логирует ошибку.
    """
    if context:
        message = f"{message} | {json.dumps(context, ensure_ascii=False)}"
    logger.error(message)


# === Аудит действий (через SecurityCore) ===

def audit_event(event: str, **context):
    """
    Записывает событие аудита в отдельный файл.
    Использует SecurityCore.audit_json для структурированного формата.
    """
    entry = audit_json(event, context)

    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


# === Удобные фасады ===

def log_request(request):
    """
    Логирует входящий HTTP‑запрос.
    """
    log_info(
        "Incoming request",
        method=request.method,
        path=request.path,
        ip=request.remote_addr,
    )


def log_upload(filename: str, user_id: int):
    """
    Логирует успешную загрузку файла.
    """
    audit_event(
        "image_uploaded",
        filename=filename,
        user_id=user_id,
        timestamp=datetime.utcnow().isoformat()
    )


def log_exception(exc: Exception):
    """
    Логирует исключение.
    """
    log_error(
        "Exception occurred",
        error=str(exc),
        type=exc.__class__.__name__
    )