# Получаем версию из pyproject.toml
VERSION := $(shell poetry version -s)
IMAGE_NAME := pixvault-backend
# Полное имя образа с тегом
IMAGE := $(IMAGE_NAME):$(VERSION)
# Имя для latest (удобно для локальных тестов)
IMAGE_LATEST := $(IMAGE_NAME):latest

# Папка для загрузок на хосте и в контейнере
UPLOAD_DIR_HOST := $(PWD)/uploads
UPLOAD_DIR_CONTAINER := /app/uploads

# --- Docker ---

# Сборка Docker-образа с семантической версией
build:
	@echo "Building version: $(VERSION)"
	docker build -t $(IMAGE) .
	docker tag $(IMAGE) $(IMAGE_LATEST)

# Запуск контейнера с пробросом папки загрузок
run:
	docker run -p 8000:8000 \
		--name pixvault_server \
		--env-file .env \
		-v $(UPLOAD_DIR_HOST):$(UPLOAD_DIR_CONTAINER) \
		$(IMAGE_LATEST)

# Пересборка
rebuild:
	docker build --no-cache -t $(IMAGE) .
	docker tag $(IMAGE) $(IMAGE_LATEST)

# Интерактивный режим
shell:
	docker run -it --entrypoint /bin/bash $(IMAGE_LATEST)

# Очистка (удаляем и версию, и latest)
clean:
	docker rmi $(IMAGE) $(IMAGE_LATEST)

# --- Database & App ---

db-init:
	poetry run flask --app pixvault_backend.app:create_app db init

db-migrate:
	poetry run flask --app pixvault_backend.app:create_app db migrate -m "auto"

# Исправлена опечатка (creat_app -> create_app) и имя цели (db_upgrade -> db-upgrade)
db-upgrade:
	poetry run flask --app pixvault_backend.app:create_app db upgrade

dev:
	poetry run flask --app pixvault_backend.app:create_app run --host=0.0.0.0 --port=8000