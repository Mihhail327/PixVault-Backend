# --- Этап 1: Сборка зависимостей ---
FROM python:3.13-slim AS builder

WORKDIR /app

# Системные зависимости для сборки
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы проекта
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости в системную папку билдера
# (флаг --no-root важен, так как само приложение мы скопируем позже)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main --no-root

# --- Этап 2: Финальный образ ---
FROM python:3.13-slim

WORKDIR /app

# Библиотеки для работы и бэкапов
RUN apt-get update && apt-get install -y \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копируем установленные пакеты из билдера в финальный образ
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Копируем исходный код
COPY . .

# Создаем нужные папки
RUN mkdir -p uploads backups

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Запуск
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "pixvault_backend.app:create_app()"]