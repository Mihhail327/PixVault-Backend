# --- Этап 1: Сборка зависимостей (остается без изменений) ---
FROM python:3.13-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# --- Этап 2: Финальный образ ---
FROM python:3.13-slim

WORKDIR /app

# Добавляем postgresql-client-15 (или подходящей версии) для работы pg_dump
RUN apt-get update && apt-get install -y \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости из билдера
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Копируем всё остальное
COPY . .

# Создаем папки и настраиваем переменные окружения
RUN mkdir -p uploads backups
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Используем семантическое версионирование при сборке образа:
# docker build -t pixvault-backend:1.0.0 .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "pixvault_backend.app:create_app()"]