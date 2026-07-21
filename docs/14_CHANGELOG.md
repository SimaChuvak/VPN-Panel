# Changelog

Все значимые изменения проекта VPN Panel фиксируются в данном документе.

Формат журнала основан на принципах Keep a Changelog.

Также используется семантическое версионирование (Semantic Versioning).

---

# [Unreleased]

## Added

- Подготовка архитектурной документации.
- Подготовка структуры проекта.
- Определение технологического стека.
- Проектирование Backend.
- Проектирование Frontend.
- Проектирование HostAgent.
- Проектирование инфраструктуры.
- Подготовка стандартов разработки.
- Подготовка стандартов API.
- Подготовка стандартов базы данных.
- Подготовка правил безопасности.
- Подготовка правил UI/UX.
- Подготовка Deployment-документации.
- Подготовка Roadmap.
- Подготовка журнала архитектурных решений.

---

# [0.1.0] - Проектирование

## Added

### Документация

- README
- PROJECT_OVERVIEW
- CONTEXT
- ARCHITECTURE
- PROJECT_STRUCTURE
- TECH_STACK
- DEVELOPMENT_RULES
- CODING_STANDARDS
- DATABASE
- API
- UI_UX
- SECURITY
- DEPLOYMENT
- ROADMAP
- DECISIONS
- CHANGELOG

### Архитектура

Определены:

- Backend
- Frontend
- HostAgent
- PostgreSQL
- Docker
- Nginx

### Backend

Выбран стек:

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- AsyncIO

### Frontend

Выбран стек:

- React
- TypeScript
- Vite
- TailwindCSS
- shadcn/ui

### Infrastructure

Подготовлена структура:

- Docker
- Docker Compose
- Nginx
- PostgreSQL

### Security

Определены:

- JWT
- RBAC
- HTTPS
- CORS
- Audit
- Logging

### Development

Подготовлены стандарты:

- Git Workflow
- Code Style
- Testing
- Documentation First
- ADR

---

# Формат будущих записей

Каждая версия оформляется следующим образом.

```
# [1.0.0] - YYYY-MM-DD

## Added

-

## Changed

-

## Fixed

-

## Removed

-

## Deprecated

-

## Security

-
```

---

# Типы изменений

## Added

Новая функциональность.

---

## Changed

Изменения существующей функциональности.

---

## Deprecated

Функциональность помечена устаревшей.

---

## Removed

Удалённая функциональность.

---

## Fixed

Исправленные ошибки.

---

## Security

Изменения, связанные с безопасностью.

---

# Правила ведения журнала

Каждое изменение должно быть отражено в журнале.

Записи должны быть понятными и краткими.

История изменений не должна переписываться задним числом.

При выпуске новой версии необходимо:

- создать новую секцию;
- перенести соответствующие записи из раздела Unreleased;
- указать дату выпуска.

---

# Версионирование

Используется Semantic Versioning.

Формат версии:

MAJOR.MINOR.PATCH

Пример:

1.0.0

1.2.0

1.2.5

2.0.0

---

# Заключение

Changelog является официальной историей развития проекта.

Все изменения должны фиксироваться своевременно и сопровождать соответствующие изменения в коде и документации.
