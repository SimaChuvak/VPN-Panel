# Локальная разработка без Docker

## Требования

Для локальной разработки необходимы:

- Python 3.13+
- Node.js 22+
- npm 10+
- PostgreSQL 17 (можно установить локально или использовать Docker только для БД)

---

## Установка зависимостей

### Backend

```bash
cd backend
pip install -e .
```

### Frontend

```bash
cd frontend
npm install
```

### HostAgent

```bash
cd hostagent
pip install -e .
```

---

## Настройка PostgreSQL

### Вариант 1: Локальная установка PostgreSQL

1. Установить PostgreSQL 17 с [postgresql.org](https://www.postgresql.org/download/)
2. Создать базу данных:
```sql
CREATE DATABASE vpn_panel;
CREATE USER vpn_panel WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE vpn_panel TO vpn_panel;
```

### Вариант 2: Docker только для PostgreSQL

```bash
docker run -d \
  --name vpn-panel-postgres \
  -e POSTGRES_DB=vpn_panel \
  -e POSTGRES_USER=vpn_panel \
  -e POSTGRES_PASSWORD=your-password \
  -p 5432:5432 \
  postgres:17-alpine
```

---

## Настройка переменных окружения

Создать файл `.env` в корне проекта:

```env
POSTGRES_DB=vpn_panel
POSTGRES_USER=vpn_panel
POSTGRES_PASSWORD=your-password
DATABASE_URL=postgresql+asyncpg://vpn_panel:your-password@localhost:5432/vpn_panel
JWT_SECRET=replace-with-a-long-random-secret
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-this-before-first-start
HOSTAGENT_URL=http://localhost:8001
HOSTAGENT_TOKEN=replace-with-a-long-random-token
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

---

## Запуск Backend

```bash
cd backend

# Применение миграций
alembic upgrade head

# Запуск сервера
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend будет доступен на http://localhost:8000

API документация: http://localhost:8000/docs

---

## Запуск Frontend

```bash
cd frontend

# Запуск dev сервера
npm run dev
```

Frontend будет доступен на http://localhost:5173

---

## Запуск HostAgent

```bash
cd hostagent

# Запуск сервера
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

HostAgent будет доступен на http://localhost:8001

---

## VS Code настройка

Рекомендуемые расширения:

- Python (Microsoft)
- Pylance (Microsoft)
- ESLint (Microsoft)
- Prettier (Prettier)
- Tailwind CSS IntelliSense (Tailwind Labs)

---

## Полный процесс разработки

1. Запустить PostgreSQL (если используется Docker для БД)
2. Настроить `.env` файл
3. Применить миграции: `cd backend && alembic upgrade head`
4. Запустить Backend: `cd backend && uvicorn app.main:app --reload`
5. Запустить HostAgent: `cd hostagent && uvicorn app.main:app --reload`
6. Запустить Frontend: `cd frontend && npm run dev`
7. Открыть http://localhost:5173 в браузере

---

## Полезные команды

### Backend

```bash
# Проверка кода
ruff check .

# Форматирование
ruff format .

# Создание новой миграции
alembic revision --autogenerate -m "description"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

### Frontend

```bash
# Сборка для production
npm run build

# Предпросмотр production сборки
npm run preview

# Проверка типов
tsc --noEmit
```

---

## Решение проблем

### Backend не запускается

- Проверить, что PostgreSQL запущен
- Проверить настройки в `.env`
- Убедиться, что миграции применены

### Frontend не подключается к Backend

- Проверить `VITE_API_BASE_URL` в `.env`
- Убедиться, что Backend запущен на порту 8000
- Проверить CORS настройки в Backend

### Ошибки импорта Python

- Убедиться, что зависимости установлены: `pip install -e .`
- Проверить, что используется Python 3.13+
