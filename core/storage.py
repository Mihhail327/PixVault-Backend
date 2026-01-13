import os
from config import IMAGES_DIR
from core.logging import logger

# Создание директории хранения
os.makedirs(IMAGES_DIR, exist_ok=True)

def safe_join(base: str, *path: str) -> str:
    """
    Безопасное объединение путей.
    Защищает от path traversal атак:
        ../../../etc/passwd
    """
    final_path = os.path.abspath(os.path.join(base, *path))
    base_path = os.path.abspath(base)

    if not final_path.startswith(base_path):
        raise ValueError("Попытка выхода за пределы директории хранения")
    return final_path

def save_file(filename: str, data: bytes) -> str:
    """
    Сохраняет файл в директорию IMAGES_DIR.
    Возвращает полный путь к файлу
    """
    filepath = safe_join(IMAGES_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(data)

    logger.info(f"Файл сохранён: {filepath}")
    return filepath

def delete_file(filename: str) -> bool:
    """
    Удаляет файл по имению
    Возвращает True, если файл удалён.
    """
    filepath = safe_join(IMAGES_DIR, filename)

    if os.path.exists(filename):
        os.remove(filepath)
        logger.info(f"Файл удалён: {filepath}")
    return True

def file_exists(filename: str) -> bool:
    """
    Проверяем существование файла.
    """
    filepath = safe_join(IMAGES_DIR, filename)
    return os.path.exists(filepath)

def get_file_path(filename: str) -> str:
    """
    Возвращает абсолютный путь к файлу.
    Используется для отдачи файла по ID.
    """
    return safe_join(IMAGES_DIR, filename)