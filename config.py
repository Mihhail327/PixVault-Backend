import os


# === Основные настройки приложения ===

class Config:
    """
    Базовая конфигурация PixVault Backend.
    Все параметры читаются из переменных окружения,
    чтобы не хранить секреты в коде и легко менять настройки
    между dev/stage/prod окружениями.
    """

    # Режим работы приложения (влияет на логи и поведение Flask)
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Директория для хранения изображений
    STORAGE_DIR: str = os.getenv("STORAGE_DIR", "images")

    # Директория для логов
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")

    # Максимальный размер загружаемого файла (в мегабайтах)
    MAX_FILE_MB: int = int(os.getenv("MAX_FILE_MB", "10"))

    # Разрешённые расширения изображений
    ALLOWED_EXTENSIONS: set[str] = {
        ext.strip().lower()
        for ext in os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,webp").split(",")
    }

    # Секретный ключ (например, для токенов или подписи данных)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")

    # URL базы данных (если появится)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Максимальное разрешение изображений (для ресайза или защиты)
    MAX_RESOLUTION: int = int(os.getenv("MAX_RESOLUTION", "2048"))