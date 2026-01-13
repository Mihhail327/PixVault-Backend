import os
import tempfile
import config
from core.storage import save_file, delete_file, file_exists, get_file_path



def setup_module(module):
    """
    Перед запуском тестов создаём временную директорию
    и подменяем config.IMAGES_DIR на неё.
    Это гарантирует:
    - полную изоляцию тестов
    - отсутствие побочных эффектов
    - безопасность реальной директории images/
    """
    module.temp_dir = tempfile.mkdtemp()
    config.IMAGES_DIR = module.temp_dir



def test_save_file_creates_file():
    """
    save_file должен:
    - создать файл в IMAGES_DIR
    - корректно записать переданные байты
    """
    filename = "test_image.png"
    data = b"123456789"

    save_file(filename, data)

    path = get_file_path(filename)
    assert os.path.exists(path)
    assert open(path, "rb").read() == data



def test_file_exists_true():
    """
    file_exists должен вернуть True,
    если файл реально существует в IMAGES_DIR.
    """
    filename = "exists.jpg"
    save_file(filename, b"data")

    assert file_exists(filename) is True


def test_file_exists_false():
    """
    file_exists должен вернуть False,
    если файла нет.
    """
    assert file_exists("no_such_file.png") is False



def test_delete_file_removes_file():
    """
    delete_file должен:
    - удалить существующий файл
    - вернуть True
    - после удаления file_exists должен вернуть False
    """
    filename = "delete_me.gif"
    save_file(filename, b"xxx")

    assert file_exists(filename) is True
    assert delete_file(filename) is True
    assert file_exists(filename) is False


def test_delete_file_nonexistent():
    """
    Если файла нет — delete_file должен вернуть False.
    Это важно для корректной логики API.
    """
    assert delete_file("ghost.jpeg") is False



def test_get_file_path_returns_correct_path():
    """
    get_file_path должен формировать путь строго внутри IMAGES_DIR.
    Это защищает от path traversal и ошибок конфигурации.
    """
    filename = "photo.jpg"
    path = get_file_path(filename)

    assert path.endswith(os.path.join(config.IMAGES_DIR, filename))