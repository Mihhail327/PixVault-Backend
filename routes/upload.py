from flask import request, jsonify
from core.file_service import save_uploaded_file

def handle_upload():
    """
    Post /upload
    Ожидает multipart/from-data с полем 'file'
    """
    if "file" not in request.files:
        return jsonify({"error": "Поле 'file' отсутствует"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Файл не выбран"}), 400

    try:
        file_id = save_uploaded_file(file.filename, file.read())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Ошибка сервера при загрузке файла"}), 500

    return jsonify({
        "status": "success",
        "id":file_id
    })