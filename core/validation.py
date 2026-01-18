from PIL import Image
from werkzeug.datastructures import FileStorage

from core.utils import get_extension
from core.logging import log_error


ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_FILE_MB = 10


def validate_extension(filename: str):
    ext = get_extension(filename)
    if ext not in ALLOWED_EXTENSIONS:
        log_error("Invalid file extension", filename=filename, ext=ext)
        raise ValueError(f"Extension '{ext}' is not allowed")


def validate_size(file_storage: FileStorage, max_mb: int = MAX_FILE_MB):
    file_storage.seek(0, 2)
    size = file_storage.tell()
    file_storage.seek(0)

    max_bytes = max_mb * 1024 * 1024

    if size > max_bytes:
        log_error("File too large", size=size, max_bytes=max_bytes)
        raise ValueError(f"File exceeds {max_mb} MB limit")


def validate_mime(file_storage: FileStorage):
    """
    Проверяет реальный формат изображения через Pillow.
    """
    try:
        img = Image.open(file_storage)
        img.verify()
    except Exception:
        log_error("Invalid or corrupted image")
        raise ValueError("Invalid or corrupted image")
    finally:
        file_storage.seek(0)


def validate_image(file_storage: FileStorage):
    filename = file_storage.filename

    validate_extension(filename)
    validate_size(file_storage)
    validate_mime(file_storage)