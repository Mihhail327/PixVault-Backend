from datetime import datetime, timezone
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from pixvault_backend.app import db

class Image(db.Model):
    """
    Модель для хранения метаданных загруженных изображений.
    Сами файлы хранятся в файловой системе, а здесь мы держим только ссылки и инфо.
    """
    __tablename__ = "images"

    # Первичный ключ (автоматически инкрементируется)
    id: Mapped[int] = mapped_column(primary_key=True)

    # Уникальное имя файла в системе (например, UUID + расширение).
    # Используем String(255) — этого достаточно для большинства путей.
    # unique=True защищает от коллизий имен.
    filename: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    # Храним оригинальное имя (например, 'мое_фото.jpg'),
    # чтобы пользователю было приятнее скачивать файл обратно.
    original_name: Mapped[str] = mapped_column(String(255), nullable=True)

    # Дата и время добавления записи.
    # DateTime(timezone=True) — "золотой стандарт", чтобы время не "поплыло" при переносе сервера.
    # index=True ускоряет сортировку (например, "показать последние загруженные").
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
        nullable=False
    )

    def __repr__(self) -> str:
        """Понятное текстовое представление объекта в логах и консоли."""
        return f"<Image(id={self.id}, filename='{self.filename}')>"