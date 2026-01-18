# Имя проекта
PROJECT = pixvault

# Основные команды Docker Compose
DC = docker compose

# === Запуск приложения ===

run:
	$(DC) up --build

up:
	$(DC) up -d

down:
	$(DC) down

restart:
	$(DC) down
	$(DC) up -d

# === Логи ===

logs:
	$(DC) logs -f

# === Пересборка ===

build:
	$(DC) build

rebuild:
	$(DC) down
	$(DC) build --no-cache
	$(DC) up -d

# === Очистка ===

clean:
	$(DC) down --volumes --remove-orphans

prune:
	docker system prune -af

# === Тесты ===

test:
	$(DC) exec app pytest -q

# === Утилиты ===

shell:
	$(DC) exec app sh

bash:
	$(DC) exec app bash