import uuid
from io import BytesIO
from PIL import Image

from core.storage import save as storage_save
from core.storage import delete as storage_delete
from core.storage import get_path as storage_get_path
from core.validation import validate_extension, validate_size
from core.logging import log_upload, log_error


# === Генерация безопасного имени файла ===

def generate_filename(ext: str) -> str:
    """
    Генерирует безопасное случайное имя файла.
    Пример: 4f8c2a9e3d124e8c9b7f2a3c4d5e6f7a.webp
    """
    return f"{uuid.uuid4().hex}.{ext.lower()}"


# === Обработка изображения ===

def process_image(file_storage) -> BytesIO:
    """
    Приводит изображение к безопасному формату:
    - конвертация в RGB
    - ресайз до 2048x2048
    - сохранение в WebP
    """
    img = Image.open(file_storage)
    img = img.convert("RGB")
    img.thumbnail((2048, 2048))

    buffer = BytesIO()
    img.save(buffer, format="WEBP", quality=90)
    buffer.seek(0)

    return buffer


# === Основная функция сохранения ===

def save_image(file_storage, user_id: int) -> str:
    """
    Принимает файл из Flask (werkzeug FileStorage),
    валидирует, обрабатывает и сохраняет его.
    Возвращает итоговое имя файла.
    """

    original_name = file_storage.filename

    # 1. Проверка расширения
    validate_extension(original_name)

    # 2. Проверка размера (например, 10 MB)
    validate_size(file_storage, max_mb=10)

    # 3. Генерация безопасного имени
    ext = original_name.rsplit(".", 1)[-1]
    filename = generate_filename(ext)

    # 4. Обработка изображения
    processed = process_image(file_storage)

    # 5. Сохранение в хранилище
    storage_save(filename, processed)

    # 6. Логирование
    log_upload(filename, user_id)

    return filename


# === Удаление изображения ===

def delete_image(filename: str) -> bool:
    """
    Удаляет изображение по имени файла.
    """
    try:
        return storage_delete(filename)
    except Exception as exc:
        log_error("Failed to delete image", filename=filename, error=str(exc))
        return False


# === Получение пути ===

def get_image_path(filename: str) -> str:
    """
    Возвращает безопасный путь к изображению.
    """
    return storage_get_path(filename)