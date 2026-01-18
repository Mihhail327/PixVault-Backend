from flask import Blueprint, request, jsonify
from core.file_service import save_image
from core.logging import log_request, log_error
from core.security import sanitize_payload

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["POST"])
def upload_image():
    # Логируем входящий запрос
    log_request(request)

    # Проверяем, что файл передан
    if "file" not in request.files:
        log_error("No file in request")
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    # Санитизация дополнительных данных (если есть)
    payload = sanitize_payload(request.form.to_dict())

    # В реальном проекте user_id берётся из токена
    user_id = payload.get("user_id", 0)

    try:
        # Сохранение изображения
        filename = save_image(file, user_id)

        return jsonify({
            "status": "ok",
            "file_id": filename
        }), 200

    except Exception as exc:
        log_error("Upload failed", error=str(exc))
        return jsonify({"error": str(exc)}), 400