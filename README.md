# VPN Panel

Современная веб-панель управления VPN-сервисом с разделением на Backend, Frontend и HostAgent.

## Цель проекта

Создать безопасную, масштабируемую и удобную систему управления VPN-инфраструктурой.

Основные требования:

- современный веб-интерфейс;
- полностью асинхронный Backend;
- REST API;
- безопасная авторизация;
- управление VPN-серверами и клиентами;
- мониторинг состояния системы;
- возможность горизонтального масштабирования.

---

# Архитектура проекта

Проект разделён на несколько независимых компонентов.

```
backend/
frontend/
hostagent/
infrastructure/
docs/
scripts/
.github/
```

## Backend

Отвечает за:

- REST API
- авторизацию
- бизнес-логику
- работу с БД
- управление пользователями
- управление VPN

---

## Frontend

SPA-приложение.

Отвечает за:

- интерфейс администратора;
- визуализацию данных;
- работу через REST API.

---

## HostAgent

Отдельный сервис.

Запускается непосредственно на VPN-сервере.

Отвечает за:

- взаимодействие с WireGuard/AmneziaWG/Xray;
- управление сервисами;
- получение статистики;
- выполнение команд Backend.

Backend никогда не управляет VPN напрямую.

---

## Документация

Вся документация располагается в каталоге

docs/

Каждый новый участник проекта обязан ознакомиться с документацией перед началом разработки.

---

## Принципы разработки

- небольшие изменения;
- один логический этап = один коммит;
- сначала проектирование, затем код;
- никакого изменения архитектуры без согласования;
- документация обновляется одновременно с кодом.

---

## Технологический стек

Backend

- Python 3.13
- FastAPI
- SQLAlchemy 2
- Alembic
- PostgreSQL 17
- Pydantic v2

Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui

Инфраструктура

- Docker
- Docker Compose
- Nginx

---

## Текущий статус

Проект находится на этапе Этап 1 — Базовая инфраструктура.

Базовая структура проекта создана, документация подготовлена. Следующий шаг — проверка готовности к запуску сервисов.

---

## Быстрый старт

### Вариант 1: Docker (рекомендуется для production)

```bash
# Клонирование репозитория
git clone <repository-url>
cd VPN-Panel

# Настройка переменных окружения
cp .env.example .env
# Отредактировать .env

# Запуск всех сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps
```

### Вариант 2: Локальная разработка (без Docker)

Подробная инструкция в [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md)

```bash
# Установка зависимостей Backend
cd backend
pip install -e .

# Установка зависимостей Frontend
cd ../frontend
npm install

# Настройка .env файла (см. .env.example)

# Запуск PostgreSQL (локально или через Docker)

# Применение миграций
cd backend
alembic upgrade head

# Запуск Backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Запуск Frontend (в другом терминале)
cd frontend
npm run dev
```

---

## Документация

Подробная документация доступна в каталоге `docs/`:

- [LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) — Локальная разработка без Docker
- [00_PROJECT_OVERVIEW.md](docs/00_PROJECT_OVERVIEW.md) — Обзор проекта
- [01_CONTEXT.md](docs/01_CONTEXT.md) — Контекст и цели
- [02_ARCHITECTURE.md](docs/02_ARCHITECTURE.md) — Архитектура системы
- [03_PROJECT_STRUCTURE.md](docs/03_PROJECT_STRUCTURE.md) — Структура проекта
- [04_TECH_STACK.md](docs/04_TECH_STACK.md) — Технологический стек
- [05_DEVELOPMENT_RULES.md](docs/05_DEVELOPMENT_RULES.md) — Правила разработки
- [06_CODING_STANDARDS.md](docs/06_CODING_STANDARDS.md) — Стандарты кодирования
- [07_DATABASE.md](docs/07_DATABASE.md) — База данных
- [08_API.md](docs/08_API.md) — API стандарты
- [09_UI_UX.md](docs/09_UI_UX.md) — UI/UX guidelines
- [10_SECURITY.md](docs/10_SECURITY.md) — Безопасность
- [11_DEPLOYMENT.md](docs/11_DEPLOYMENT.md) — Развёртывание
- [12_ROADMAP.md](docs/12_ROADMAP.md) — План развития
- [13_DECISIONS.md](docs/13_DECISIONS.md) — Архитектурные решения
- [14_CHANGELOG.md](docs/14_CHANGELOG.md) — Журнал изменений

---

## Лицензия

[Указать лицензию]

---

## Контакты

[Указать контакты]
