FROM python:3.13-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY docker .

# Backend слушает порт 8000
EXPOSE 8000

# Запуск приложения
CMD ["python", "app.py"]