import logging
import os
from config import LOGS_DIR, DEBUG

# Создание директории логов
os.makedirs(LOGS_DIR, exist_ok=True)


# Настройка стандартного логгера
LOG_FILE = os.path.join(LOGS_DIR, "backend.log")

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler() if DEBUG else logging.NullHandler()
    ]
)

logger = logging.getLogger("pixvault")