import io
import pytest
from app import app



@pytest.fixture
def client():
    """
    Создаёт тестовый клиент Flask.
    Позволяет отправлять запросы к API без запуска сервера.
    """
    app.config["TESTING"] = True
    return app.test_client()



def test_upload_success(client):
    """
    Проверяем успешную загрузку корректного изображения.
    """
    data = {
        "file": (io.BytesIO(b"fake image data"), "cat.jpg")
    }

    response = client.post("/upload", data=data, content_type="multipart/form-data")

    assert response.status_code == 200
    json = response.get_json()

    assert json["status"] == "success"
    assert "id" in json



def test_upload_missing_file_field(client):
    """
    Если поле 'file' отсутствует — API должно вернуть 400.
    """
    response = client.post("/upload", data={}, content_type="multipart/form-data")

    assert response.status_code == 400
    assert "error" in response.get_json()



def test_upload_empty_filename(client):
    """
    Если имя файла пустое — API должно вернуть 400.
    """
    data = {
        "file": (io.BytesIO(b"data"), "")
    }

    response = client.post("/upload", data=data, content_type="multipart/form-data")

    assert response.status_code == 400
    assert "error" in response.get_json()



def test_upload_bad_extension(client):
    """
    Если расширение не входит в ALLOWED_EXTENSIONS — API должно вернуть 400.
    """
    data = {
        "file": (io.BytesIO(b"data"), "virus.exe")
    }

    response = client.post("/upload", data=data, content_type="multipart/form-data")

    assert response.status_code == 400
    assert "error" in response.get_json()



def test_upload_too_large(client, monkeypatch):
    """
    Подменяем MAX_FILE_SIZE, чтобы проверить ошибку превышения размера.
    """
    monkeypatch.setattr("core.file_service.MAX_FILE_SIZE", 1)  # 1 байт

    data = {
        "file": (io.BytesIO(b"123456"), "big.jpg")
    }

    response = client.post("/upload", data=data, content_type="multipart/form-data")

    assert response.status_code == 400
    assert "error" in response.get_json()