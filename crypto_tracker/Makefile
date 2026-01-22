# Makefile для CryptoTracker

# Переменные
DOCKER_COMPOSE = docker-compose -f backend/docker-compose.yml
PROJECT_NAME = cryptotracker
BACKEND_DIR = backend
FRONTEND_DIR = frontend

.PHONY: help build up down restart logs clean test init

# Помощь по командам
help:
	@echo "Доступные команды:"
	@echo "  make build     - Собрать все сервисы"
	@echo "  make up        - Запустить все сервисы в фоне"
	@echo "  make up-dev    - Запустить в режиме разработки (с логами)"
	@echo "  make down      - Остановить все сервисы"
	@echo "  make restart   - Перезапустить сервисы"
	@echo "  make logs      - Показать логи"
	@echo "  make logs-api  - Показать логи API"
	@echo "  make logs-db   - Показать логи базы данных"
	@echo "  make clean     - Остановить и удалить контейнеры, volumes"
	@echo "  make test      - Запустить тесты"
	@echo "  make init      - Инициализация проекта (первый запуск)"
	@echo "  make status    - Показать статус сервисов"

# Сборка всех сервисов
build:
	@echo "Сборка всех сервисов..."
	$(DOCKER_COMPOSE) build

# Запуск в фоне
up: build
	@echo "Запуск сервисов в фоне..."
	$(DOCKER_COMPOSE) up -d

# Запуск в режиме разработки (с логами)
up-dev: build
	@echo "Запуск сервисов в режиме разработки..."
	$(DOCKER_COMPOSE) up

# Остановка сервисов
down:
	@echo "Остановка сервисов..."
	$(DOCKER_COMPOSE) down

# Перезапуск
restart: down up
	@echo "Сервисы перезапущены"

# Логи всех сервисов
logs:
	$(DOCKER_COMPOSE) logs -f

# Логи API
logs-api:
	$(DOCKER_COMPOSE) logs -f api

# Логи базы данных
logs-db:
	$(DOCKER_COMPOSE) logs -f postgres

# Логи Redis
logs-redis:
	$(DOCKER_COMPOSE) logs -f redis

# Логи worker
logs-worker:
	$(DOCKER_COMPOSE) logs -f worker

# Логи фронтенда
logs-frontend:
	$(DOCKER_COMPOSE) logs -f frontend

# Очистка (контейнеры, volumes)
clean:
	@echo "Остановка и очистка..."
	$(DOCKER_COMPOSE) down -v --remove-orphans
	@echo "Удаление ненужных docker образов..."
	docker system prune -f

# Запуск тестов
test:
	@echo "Запуск тестов..."
	# docker exec -it $(PROJECT_NAME)-api pytest tests/

# Инициализация проекта (первый запуск)
init: up
	@echo "Инициализация проекта..."
	@echo "Ожидание запуска базы данных..."
	sleep 10
	@echo "Проект готов!"
	@echo "Фронтенд: http://localhost:8080"
	@echo "API:      http://localhost:8005"
	@echo "Документация API: http://localhost:8005/docs"

# Статус сервисов
status:
	$(DOCKER_COMPOSE) ps

# Bash в контейнер API
bash-api:
	docker exec -it $$(docker ps -q --filter "name=api") bash

# Bash в контейнер базы данных
bash-db:
	docker exec -it $$(docker ps -q --filter "name=postgres") bash

# Просмотр логов в реальном времени с таймстампами
logs-tail:
	$(DOCKER_COMPOSE) logs -f --tail=100 --timestamps

# Проверка здоровья сервисов
health:
	@echo "Проверка здоровья сервисов..."
	@echo "API:"
	curl -f http://localhost:8005/health || echo "API не доступен"
	@echo ""
	@echo "Фронтенд:"
	curl -f http://localhost:8080 || echo "Фронтенд не доступен"
	@echo ""
	@echo "База данных:"
	docker exec -it $$(docker ps -q --filter "name=postgres") pg_isready -U crypto_user

# Резервное копирование базы данных
backup:
	@echo "Создание резервной копии базы данных..."
	mkdir -p backups
	docker exec -it $$(docker ps -q --filter "name=postgres") pg_dump -U crypto_user crypto_db > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Резервная копия создана в папке backups/"

# Восстановление базы данных из backup
restore:
	@echo "Восстановление базы данных из последнего backup..."
	@ls -t backups/*.sql | head -1 | xargs -I {} docker exec -i $$(docker ps -q --filter "name=postgres") psql -U crypto_user -d crypto_db < {}
	@echo "База данных восстановлена"

# Мониторинг ресурсов
monitor:
	@echo "Мониторинг ресурсов Docker..."
	docker stats

# Остановка всех контейнеров Docker (осторожно!)
stop-all:
	@echo "Остановка ВСЕХ контейнеров Docker..."
	docker stop $$(docker ps -aq)
