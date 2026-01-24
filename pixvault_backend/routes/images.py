import os
import uuid
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from sqlalchemy import select
from pixvault_backend.app import db
from pixvault_backend.models import Image

# Изолируем логику работы с изображениями
images_bp = Blueprint("images", __name__)


def allowed_file(filename: str) -> bool:
    """Проверка расширения файла через конфиг."""
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[-1].upper()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


@images_bp.route("/upload", methods=["POST"])
def upload_image():
    """
    Загрузка изображения:
    1. Валидация наличия и типа файла.
    2. Генерация безопасного UUID-имени.
    3. Сохранение на диск и запись метаданных в БД.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    original_name = file.filename

    if original_name == "" or not allowed_file(original_name):
        return jsonify({"error": "Invalid or unsupported file type"}), 400

    # Генерируем уникальное имя, сохраняя оригинальное расширение
    ext = original_name.rsplit(".", 1)[-1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"

    # Дополнительная очистка (на случай странных символов в расширении)
    safe_name = secure_filename(unique_filename)
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], safe_name)

    try:
        file.save(save_path)

        # Создаем запись в БД (SQLAlchemy 2.0 style)
        new_image = Image(
            filename=safe_name,
            original_name=original_name  # Полезно для скачивания
        )
        db.session.add(new_image)
        db.session.commit()

        return jsonify({
            "message": "Image uploaded successfully",
            "filename": safe_name,
            "id": new_image.id
        }), 201

    except Exception as e:
        db.session.rollback()  # Откатываем транзакцию при ошибке записи
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@images_bp.route("/images/<filename>")
def get_image(filename):
    """Раздача файлов из папки загрузок."""
    # Flask сам проверит наличие файла и вернет 404, если его нет
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=False  # Браузер будет пытаться отобразить, а не скачать
    )


@images_bp.route("/list")
def list_images():
    """Список изображений с пагинацией (современный синтаксис)."""
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config["ITEMS_PER_PAGE"]

    # Используем select() вместо legacy Query
    stmt = select(Image).order_by(Image.created_at.desc())
    pagination = db.paginate(stmt, page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": [
            {
                "id": img.id,
                "filename": img.filename,
                "original_name": img.original_name,
                "created_at": img.created_at.isoformat()
            } for img in pagination.items
        ],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    })