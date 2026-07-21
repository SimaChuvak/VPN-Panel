# Структура проекта VPN Panel

## Назначение

Документ определяет официальную структуру репозитория.

Любые изменения структуры каталогов должны сначала отражаться в этом документе.

---

# Корень репозитория

```
VPN-Panel/

├── backend/
├── frontend/
├── hostagent/
├── infrastructure/
├── docs/
├── scripts/
├── .github/

├── docker-compose.yml
├── .env.example
├── README.md
├── LICENSE
└── .gitignore
```

---

# backend/

Backend представляет собой FastAPI-приложение.

```
backend/

├── app/

│   ├── api/
│   │
│   ├── core/
│   │
│   ├── db/
│   │
│   ├── dependencies/
│   │
│   ├── middleware/
│   │
│   ├── models/
│   │
│   ├── repositories/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   ├── utils/
│   │
│   └── main.py

├── tests/

├── migrations/

├── pyproject.toml

└── Dockerfile
```

---

## Назначение каталогов Backend

### api/

REST API.

Только маршруты.

Без бизнес-логики.

---

### services/

Вся бизнес-логика проекта.

---

### repositories/

Работа исключительно с PostgreSQL.

---

### models/

SQLAlchemy модели.

---

### schemas/

Pydantic модели.

---

### db/

Подключение к БД.

Session.

Engine.

Alembic.

---

### dependencies/

FastAPI Depends.

---

### middleware/

JWT.

Logging.

Request ID.

Rate Limit.

---

### utils/

Вспомогательные функции.

---

# frontend/

```
frontend/

├── src/

│   ├── app/
│   │
│   ├── pages/
│   │
│   ├── widgets/
│   │
│   ├── features/
│   │
│   ├── entities/
│   │
│   ├── shared/
│   │
│   ├── assets/
│   │
│   └── main.tsx

├── public/

├── package.json

└── Dockerfile
```

---

## Frontend

Используется Feature-Sliced Design.

### app/

Инициализация приложения.

---

### pages/

Страницы.

---

### widgets/

Крупные UI-блоки.

---

### features/

Функциональные возможности.

---

### entities/

Доменные сущности.

---

### shared/

Общие компоненты.

---

# hostagent/

```
hostagent/

├── api/
├── services/
├── system/
├── vpn/
├── docker/
├── config/
├── utils/

├── main.py

└── Dockerfile
```

HostAgent полностью независим от Backend.

---

# infrastructure/

```
infrastructure/

├── nginx/

├── docker/

├── monitoring/

└── production/
```

---

# docs/

```
docs/

00_PROJECT_OVERVIEW.md

01_CONTEXT.md

02_ARCHITECTURE.md

03_PROJECT_STRUCTURE.md

04_TECH_STACK.md

05_DEVELOPMENT_RULES.md

06_CODING_STANDARDS.md

07_DATABASE.md

08_API.md

09_UI_UX.md

10_SECURITY.md

11_DEPLOYMENT.md

12_ROADMAP.md

13_DECISIONS.md

14_CHANGELOG.md
```

---

# scripts/

```
scripts/

dev.sh

build.sh

deploy.sh

backup.sh

restore.sh
```

---

# .github/

```
.github/

workflows/

ISSUE_TEMPLATE/

PULL_REQUEST_TEMPLATE.md
```

---

# Правила

Каждый каталог имеет собственную ответственность.

Запрещается:

- смешивать Backend и Frontend;
- размещать бизнес-логику вне `services/`;
- обращаться к БД вне `repositories/`;
- размещать SQLAlchemy-модели вне `models/`;
- создавать новые верхнеуровневые каталоги без обновления документации.
