import os
from typing import Optional, BinaryIO

from core.logging import log_info, log_error
from core.security import safe_filename, safe_path


STORAGE_DIR = "images"


# === Инициализация хранилища ===

def init_storage():
    """
    Создаёт директорию для хранения файлов, если её нет.
    """
    os.makedirs(STORAGE_DIR, exist_ok=True)
    log_info("Storage initialized", directory=STORAGE_DIR)


# === Путь к файлу ===

def get_path(filename: str) -> str:
    """
    Возвращает безопасный путь к файлу в хранилище.
    """
    filename = safe_filename(filename)
    return safe_path(os.path.join(STORAGE_DIR, filename))


# === Проверка существования ===

def exists(filename: str) -> bool:
    """
    Проверяет, существует ли файл.
    """
    path = get_path(filename)
    return os.path.exists(path)


# === Сохранение файла ===

def save(filename: str, data: BinaryIO) -> str:
    """
    Сохраняет бинарные данные в файл.
    data — это BytesIO или любой поток с .read().
    """
    path = get_path(filename)

    with open(path, "wb") as f:
        f.write(data.read())

    log_info("File saved", filename=filename, path=path)
    return filename


# === Чтение файла ===

def load(filename: str) -> Optional[bytes]:
    """
    Загружает файл и возвращает его содержимое.
    """
    path = get_path(filename)

    if not os.path.exists(path):
        log_error("Attempt to load non-existing file", filename=filename)
        return None

    with open(path, "rb") as f:
        return f.read()


# === Удаление файла ===

def delete(filename: str) -> bool:
    """
    Удаляет файл. Возвращает True, если файл был удалён.
    """
    path = get_path(filename)

    if not os.path.exists(path):
        log_error("Attempt to delete non-existing file", filename=filename)
        return False

    os.remove(path)
    log_info("File deleted", filename=filename)
    return True


# === Список файлов ===

def list_files() -> list[str]:
    """
    Возвращает список всех файлов в хранилище.
    """
    return [
        f for f in os.listdir(STORAGE_DIR)
        if os.path.isfile(os.path.join(STORAGE_DIR, f))
    ]