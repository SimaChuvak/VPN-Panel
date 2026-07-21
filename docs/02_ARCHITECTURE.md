# Архитектура VPN Panel

## Назначение

Документ описывает архитектуру проекта VPN Panel.

Все изменения архитектуры должны сначала отражаться в данном документе, а затем реализовываться в коде.

---

# Общая схема

                   Internet
                        │
                        │
                 HTTPS / TLS
                        │
                 Reverse Proxy
                    (Nginx)
                        │
          ┌─────────────┴─────────────┐
          │                           │
      React Frontend           FastAPI Backend
                                      │
                  ┌───────────────────┴──────────────────┐
                  │                                      │
             PostgreSQL                           HostAgent
                                                         │
                       ┌─────────────────────────────────┴─────────────┐
                       │                                               │
                WireGuard / AmneziaWG                           Docker
                       │
                 VPN Infrastructure

---

# Компоненты системы

## Frontend

Frontend отвечает исключительно за отображение информации.

### Обязанности

- авторизация пользователя;
- отображение данных;
- работа через REST API;
- формы;
- таблицы;
- графики;
- уведомления.

Frontend не содержит бизнес-логики.

---

## Backend

Backend является центральным компонентом системы.

Через него проходят абсолютно все запросы.

### Backend отвечает за

- аутентификацию;
- авторизацию;
- бизнес-логику;
- работу с БД;
- аудит;
- управление пользователями;
- управление VPN;
- взаимодействие с HostAgent.

Backend не выполняет системные команды напрямую.

---

## HostAgent

HostAgent устанавливается на VPN-сервер.

Он предоставляет Backend безопасный API.

### HostAgent отвечает за

- WireGuard;
- AmneziaWG;
- Xray;
- Docker;
- systemd;
- получение статистики;
- выполнение разрешённых команд;
- чтение конфигураций.

HostAgent не хранит пользователей панели.

---

## PostgreSQL

Единая база данных проекта.

Backend является единственным сервисом, имеющим доступ к БД.

---

# Backend Architecture

Backend разделяется на несколько уровней.

```
API

↓

Services

↓

Repositories

↓

Database
```

## API Layer

Принимает HTTP-запросы.

Не содержит бизнес-логики.

---

## Service Layer

Содержит бизнес-логику.

Именно здесь принимаются все решения.

---

## Repository Layer

Работает исключительно с базой данных.

Без бизнес-логики.

---

## Database Layer

SQLAlchemy.

PostgreSQL.

---

# Frontend Architecture

Frontend разделяется на:

```
Pages

↓

Layouts

↓

Features

↓

Widgets

↓

Components

↓

Shared
```

Каждый уровень имеет собственную область ответственности.

---

# Взаимодействие сервисов

Browser

↓

Frontend

↓

REST API

↓

Backend

↓

HostAgent

↓

VPN

---

# Авторизация

Все запросы проходят через Backend.

Frontend никогда не обращается напрямую к HostAgent.

HostAgent принимает запросы только от Backend.

---

# Масштабирование

Архитектура допускает:

- несколько Backend;
- несколько HostAgent;
- несколько VPN-серверов;
- несколько Frontend.

---

# Безопасность

Backend изолирует внутреннюю инфраструктуру.

HostAgent никогда не публикуется в Интернет.

Внешний доступ осуществляется только через Backend.

---

# Основные архитектурные принципы

- Single Responsibility
- Dependency Injection
- Repository Pattern
- Service Layer
- REST API
- Stateless
- Async
- Modular Architecture
- API First
- Separation of Concerns

---

# Запрещается

Без отдельного архитектурного решения запрещается:

- нарушать разделение слоёв;
- обращаться к БД минуя Repository;
- выполнять системные команды из Backend;
- обращаться к HostAgent напрямую из Frontend;
- добавлять бизнес-логику в API-контроллеры.
