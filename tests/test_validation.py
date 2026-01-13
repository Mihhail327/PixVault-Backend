import config
from core.validation import is_allowed_extension, validate_size



def test_allowed_extensions_valid():
    """
    Проверяем, что изображения с разрешёнными расширениями
    корректно проходят валидацию.
    """
    assert is_allowed_extension("cat.jpg", config.ALLOWED_EXTENSIONS)
    assert is_allowed_extension("dog.jpeg", config.ALLOWED_EXTENSIONS)
    assert is_allowed_extension("photo.png", config.ALLOWED_EXTENSIONS)
    assert is_allowed_extension("meme.gif", config.ALLOWED_EXTENSIONS)


def test_allowed_extensions_case_insensitive():
    """
    Валидация должна быть нечувствительной к регистру.
    """
    assert is_allowed_extension("CAT.JPG", config.ALLOWED_EXTENSIONS)
    assert is_allowed_extension("dog.JPEG", config.ALLOWED_EXTENSIONS)


def test_allowed_extensions_invalid():
    """
    Файлы с запрещёнными расширениями должны отклоняться.
    """
    assert not is_allowed_extension("virus.exe", config.ALLOWED_EXTENSIONS)
    assert not is_allowed_extension("archive.zip", config.ALLOWED_EXTENSIONS)
    assert not is_allowed_extension("script.py", config.ALLOWED_EXTENSIONS)
    assert not is_allowed_extension("readme.txt", config.ALLOWED_EXTENSIONS)


def test_allowed_extensions_missing_dot():
    """
    Проверяем защиту от файлов без расширения.
    """
    assert not is_allowed_extension("file", config.ALLOWED_EXTENSIONS)
    assert not is_allowed_extension("image", config.ALLOWED_EXTENSIONS)



def test_validate_size_valid():
    """
    Файл меньшего размера должен проходить валидацию.
    """
    assert validate_size(1024, config.MAX_FILE_SIZE)  # 1 KB
    assert validate_size(4 * 1024 * 1024, config.MAX_FILE_SIZE)  # 4 MB


def test_validate_size_exact_limit():
    """
    Файл, равный лимиту, должен быть допустим.
    """
    assert validate_size(config.MAX_FILE_SIZE, config.MAX_FILE_SIZE)


def test_validate_size_too_large():
    """
    Файл, превышающий лимит, должен отклоняться.
    """
    assert not validate_size(config.MAX_FILE_SIZE + 1, config.MAX_FILE_SIZE)