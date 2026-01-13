import os

def is_allowed_extension(filename: str, allowed_exts: list[str]) -> bool:
    """
    Проверяет, что файл имеет допустимое расширение.
    """
    ext = os.path.splitext(filename)[1].lower()
    return ext in [e.lower() for e in allowed_exts]

def validate_size(size: int, max_size: int) -> bool:
    """
    Проверяет, что размер файла не превышает max_size
    """
    return size <= max_size

def extract_extension(filename: str) -> str:
    """
    Возвращает расширение файла в нижнем регистре.
    Например: "cat.JPG" -> ".jpg"
    """
    return os.path.splitext(filename)[1].lower()

def is_filename_safe(filename: str) -> bool:
    """
    Проверяет, что имя файла не содержит опасных символов.
    Это дополнительная защита, хотя sanitize_filename уже чистит строку.
    """
    forbidden = ['..', '/', '\\', '\0']

    return not any(bad in filename for bad in forbidden)