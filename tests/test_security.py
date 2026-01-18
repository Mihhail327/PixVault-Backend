import re
from core import sanitize_filename, generate_secure_filename, audit

def test_sanitize_filename_basic():
    """
    Проверяем, что функция корректно обрабатывает обычные названия
    изображений и заменяет пробелы на прочерки.
    """
    assert sanitize_filename("cat.png") == "cat.png"
    assert sanitize_filename("my photo.jpg") == "my_photo.jpg"
    assert sanitize_filename("cool-image.jpeg") == "cool-image.jpeg"
    assert sanitize_filename("funny meme.gif") == "funny_meme.gif"

def tes_sanitize_filename_remove_dangerous_parts():
    """
    Проверяем защиту от path traversal и опасных символов.
    sanitize_filename должен:
    - удалять ../ и ..\
    - заменять / и \ на безопасные симфолы
    """
    assert sanitize_filename("../cat.jpg") == "__cat.jpg"
    assert sanitize_filename("..\\dog.png") == "__dog.png"
    assert sanitize_filename("evil/path.jpeg") == "evil_path.jpeg"
    assert sanitize_filename("bad\\path.gif") == "bad_path.gif"


def test_generate_secure_filename_for_images():
    """
    Проверяем, что функция генерирует уникальные криптостойкие имена
    и сохраняет расширения файла
    """
    name1 = generate_secure_filename(".jpg")
    name2 = generate_secure_filename(".jpg")

    assert name1 != name2 # имена должны быть разные
    assert name1.endswith(".jpg") # расширение сохраняется
    assert name2.endswith(".jpg")

def test_generate_secure_filename_format():
    """
    Проверяем формат имени:
    - 32 hex-символа (UUID без дефисов)
    - корректное расширение
    """
    name = generate_secure_filename(".png")
    assert re.match(r"^[a-f0-9]{32}\.png$", name)


def test_audit_does_not_crash():
    """
    Аудит не должен выбрасывать исключений.
    Мы не проверяем вывод, только стабильность работы
    """
    audit("upload_test", {"file": "cat.jpg"})