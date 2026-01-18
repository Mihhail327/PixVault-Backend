import os
import tarfile
from datetime import datetime
from config import Config


def create_backup():
    """
    Создаёт архив с изображениями и логами PixVault.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}.tar.gz"
    backup_path = os.path.join("backups", backup_name)

    os.makedirs("backups", exist_ok=True)

    with tarfile.open(backup_path, "w:gz") as tar:
        tar.add(Config.STORAGE_DIR, arcname="images")
        tar.add(Config.LOG_DIR, arcname="logs")

    print(f"✅ Backup created: {backup_path}")
    return backup_path