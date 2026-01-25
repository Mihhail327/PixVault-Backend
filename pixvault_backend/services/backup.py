import os
import shutil
import subprocess
import tarfile
from datetime import datetime, timezone
from flask import current_app
from loguru import logger


def create_backup() -> str:
    """
    Создаёт полный архив данных приложения (uploads + DB).
    Версия приложения и дата включаются в название файла.
    """
    # Семантическая версия (можно вынести в конфиг)
    app_version = "1.0.0"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    # Имя папки и итогового архива
    backup_name = f"pixvault_v{app_version}_{timestamp}"
    backup_root = os.path.join("backups", backup_name)
    os.makedirs(backup_root, exist_ok=True)

    try:
        # 1. Бэкап директории uploads
        uploads = current_app.config["UPLOAD_FOLDER"]
        if os.path.exists(uploads):
            shutil.copytree(uploads, os.path.join(backup_root, "uploads"), dirs_exist_ok=True)
            logger.info("Uploads directory copied to backup")

        # 2. Бэкап Базы Данных
        db_uri = current_app.config["SQLALCHEMY_DATABASE_URI"]

        if db_uri.startswith("sqlite:///"):
            db_path = db_uri.replace("sqlite:///", "")
            if os.path.exists(db_path):
                shutil.copy2(db_path, os.path.join(backup_root, "database.sqlite"))
                logger.info("SQLite database copied")

        elif "postgresql" in db_uri:
            dump_path = os.path.join(backup_root, "database.sql")
            # Используем env для передачи пароля, если он есть в URI
            subprocess.run(
                ["pg_dump", db_uri, "-f", dump_path],
                check=True,
                capture_output=True
            )
            logger.info("PostgreSQL dump created via pg_dump")

        # 3. Создание финального сжатого архива .tar.gz
        archive_path = f"{backup_root}.tar.gz"
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(backup_root, arcname=backup_name)

        # Удаляем временную папку, оставляем только архив
        shutil.rmtree(backup_root)

        logger.success(f"Backup complete: {archive_path}")
        return archive_path

    except subprocess.CalledProcessError as e:
        logger.error(f"Postgres dump error: {e.stderr.decode()}")
        raise Exception("Database dump failed. Make sure postgres-client is installed.")
    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")
        raise e