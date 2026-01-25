import os
import uuid
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from sqlalchemy import select
from pixvault_backend.app import db
from pixvault_backend.models import Image

images_bp = Blueprint("images", __name__)


def allowed_file(filename: str) -> bool:
    """Проверка расширения файла через конфиг."""
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[-1].upper()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


@images_bp.route("/upload", methods=["POST"])
def upload_image():
    """Загрузка изображения."""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    original_name = file.filename

    if not original_name or not allowed_file(original_name):
        return jsonify({"error": "Invalid or unsupported file type"}), 400

    ext = original_name.rsplit(".", 1)[-1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    safe_name = secure_filename(unique_filename)

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    save_path = os.path.join(upload_folder, safe_name)

    try:
        file.save(save_path)

        image = Image(
            filename=safe_name,
            original_name=original_name
        )

        db.session.add(image)
        db.session.commit()

        return jsonify({
            "message": "Image uploaded successfully",
            "filename": safe_name,
            "id": image.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@images_bp.route("/images/<filename>", methods=["GET"])
def get_image(filename):
    """Раздача изображения."""
    filename = secure_filename(filename)
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=False
    )


@images_bp.route("/delete/<int:image_id>", methods=["DELETE"])
def delete_image(image_id):
    """Удаление изображения по ID (файл + БД)."""

    # 1. Ищем запись по первичному ключу ID
    # Используем db.session.get для SQLAlchemy >= 3.0 или query.get для старых версий
    image = db.session.get(Image, image_id)

    if not image:
        return jsonify({"error": f"Image #{image_id} not found"}), 404

    # 2. Формируем путь к файлу
    file_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        image.filename
    )

    try:
        # 3. Удаляем физический файл с диска
        if os.path.exists(file_path):
            os.remove(file_path)

        # 4. Удаляем запись из базы данных
        db.session.delete(image)
        db.session.commit()

        return jsonify({"message": f"Image #{image_id} deleted"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Delete failed: {str(e)}"}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Delete failed: {str(e)}"}), 500


@images_bp.route("/list", methods=["GET"])
def list_images():
    """Список изображений с пагинацией."""
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config["ITEMS_PER_PAGE"]

    stmt = select(Image).order_by(Image.created_at.desc())
    pagination = db.paginate(
        stmt,
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "items": [
            {
                "id": img.id,
                "filename": img.filename,
                "original_name": img.original_name,
                "created_at": img.created_at.isoformat()
            }
            for img in pagination.items
        ],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    })
