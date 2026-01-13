import mimetypes
from core.storage import save_file, delete_file, file_exists, get_file_path
from core.security import generate_secure_filename, sanitize_filename, audit
from core.validation import is_allowed_extension, validate_size
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE


# -----------------------------
# Временная база данных (in-memory)
# Позже заменим на SQLite/Postgres
# -----------------------------
FILES_DB = {}
NEXT_ID = 1


def create_file_record(original_name: str, stored_name: str, size: int, mime: str) -> int:
    """
    Создаёт запись о файле и возвращает ID.
    """
    global NEXT_ID

    file_id = NEXT_ID
    NEXT_ID += 1

    FILES_DB[file_id] = {
        "id": file_id,
        "original_name": original_name,
        "stored_name": stored_name,
        "size": size,
        "mime": mime
    }

    return file_id


def save_uploaded_file(original_name: str, data: bytes) -> int:
    """
    Полный цикл сохранения файла:
    - санитизация имени
    - проверка расширения
    - проверка размера
    - генерация безопасного имени
    - сохранение файла
    - запись в базу
    - аудит
    """

    # Санитизация
    safe_name = sanitize_filename(original_name)

    # Проверка расширения
    if not is_allowed_extension(safe_name, ALLOWED_EXTENSIONS):
        audit("upload_error", {"reason": "bad_extension", "name": safe_name})
        raise ValueError("Неподдерживаемый формат файла")

    # Проверка размера
    if not validate_size(len(data), MAX_FILE_SIZE):
        audit("upload_error", {"reason": "file_too_large", "size": len(data)})
        raise ValueError("Файл слишком большой")

    # Генерация безопасного имени
    ext = "." + safe_name.split(".")[-1]
    stored_name = generate_secure_filename(ext)

    # Сохранение файла
    save_file(stored_name, data)

    # MIME
    mime = mimetypes.guess_type(safe_name)[0] or "application/octet-stream"

    # Создание записи
    file_id = create_file_record(
        original_name=safe_name,
        stored_name=stored_name,
        size=len(data),
        mime=mime
    )

    audit("upload_success", {"id": file_id, "stored_name": stored_name})
    return file_id


def get_file_info(file_id: int) -> dict | None:
    """
    Возвращает запись о файле по ID.
    """
    return FILES_DB.get(file_id)


def get_file_bytes(file_id: int) -> tuple[bytes, str]:
    """
    Возвращает (байты файла, MIME) по ID.
    """
    record = get_file_info(file_id)
    if not record:
        raise FileNotFoundError("Файл не найден")

    path = get_file_path(record["stored_name"])

    with open(path, "rb") as f:
        data = f.read()

    return data, record["mime"]


def delete_file_by_id(file_id: int) -> bool:
    """
    Удаляет файл по ID:
    - удаляет физический файл
    - удаляет запись из базы
    """
    record = get_file_info(file_id)
    if not record:
        return False

    delete_file(record["stored_name"])
    del FILES_DB[file_id]

    audit("delete_success", {"id": file_id})
    return True