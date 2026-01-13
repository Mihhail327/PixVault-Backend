from flask import Flask
from routes.upload import handle_upload
from routes.index import handle_index
from routes.errors import handle_not_found
from config import HOST, PORT

app = Flask(__name__)

# Маршруты
app.add_url_rule("/", "index", handle_index, methods=["GET"])
app.add_url_rule("/upload", "upload", handle_upload, methods=["POST"])


# Обработка 404
@app.errorhandler(404)
def not_found(e):
    return handle_not_found(None)

# Запуск сервера
if __name__ == "__main__":
    print(f"PixVault backend running on http://{HOST}:{PORT}")
    app.run(host=HOST, port=PORT)