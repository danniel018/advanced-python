# Capstone Project: Real-Time Chat + Task Queue System

## 📋 Project Overview

This capstone project is a **production-grade Real-Time Chat Application** that integrates all concepts learned throughout the Advanced Python course. It demonstrates mastery of modern Python ecosystem, architectural patterns, and deep concurrency concepts.

### Core Features

- **WebSocket-based instant messaging** - Real-time bidirectional communication
- **Distributed message broadcasting** - Using Redis Pub/Sub for horizontal scalability
- **Background task processing** - Async workers for file uploads (images, documents)
- **JWT-based authentication** - Secure stateless authentication
- **PostgreSQL persistence** - Relational data storage with async support
- **Horizontal scalability** - Architecture supports multiple instances via Redis Pub/Sub

---

## 🏗️ Architectural Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                              CLIENTS                                 │
│         (Web Browsers, Mobile Apps, Desktop Applications)            │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          │ WebSocket / HTTP
                          ▼
                   ┌──────────────┐
                   │   FastAPI    │
                   │   Instance   │
                   └──────┬───────┘
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
┌───────────────┐               ┌───────────────┐
│    Redis      │               │  PostgreSQL   │
│  (Pub/Sub +   │               │  (Persistent  │
│   Queue)      │               │   Storage)    │
└───────┬───────┘               └───────────────┘
        │
        │ Pop Tasks
        ▼
┌───────────────┐
│   Worker(s)   │
│  (Background  │
│  Processors)  │
└───────────────┘
```

### Layered Architecture

The application follows a **Clean Architecture** approach with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                        │
│                           (src/api/)                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐   │
│  │  REST Endpoints │  │ WebSocket       │  │  Middleware    │   │
│  │  (routes/)      │  │ Handlers        │  │  (auth, cors)  │   │
│  └─────────────────┘  └─────────────────┘  └────────────────┘   │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                        SERVICE LAYER                             │
│                         (src/services/)                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐   │
│  │  UserService    │  │  ChatService    │  │  FileService   │   │
│  │                 │  │                 │  │                │   │
│  └─────────────────┘  └─────────────────┘  └────────────────┘   │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                       REPOSITORY LAYER                           │
│                       (src/repositories/)                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐   │
│  │ UserRepository  │  │ MessageRepo     │  │  FileRepo      │   │
│  │                 │  │                 │  │                │   │
│  └─────────────────┘  └─────────────────┘  └────────────────┘   │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE LAYER                        │
│                           (src/db/)                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐   │
│  │ Database Models │  │ Session Manager │                      │
│  │ (SQLAlchemy)    │  │ (async)         │                      │
│  └─────────────────┘  └─────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
capstone_project/
├── .env                          # Environment variables (secrets, config)
├── .env.example                  # Template for environment setup
├── docker-compose.yml            # Docker services orchestration
├── Dockerfile                    # Application container definition
├── pyproject.toml                # Dependencies & tool configuration
├── README.md                     # Project-specific documentation
│
├── src/
│   ├── __init__.py
│   ├── main.py                   # Application entrypoint (FastAPI app)
│   │
│   ├── core/                     # Cross-cutting concerns
│   │   ├── __init__.py
│   │   ├── config.py             # Pydantic Settings (env loading)
│   │   ├── security.py           # JWT utilities, password hashing
│   │   ├── exceptions.py         # Custom exception classes
│   │   └── dependencies.py       # FastAPI dependency injection
│   │
│   ├── db/                       # Database layer
│   │   ├── __init__.py
│   │   ├── session.py            # Async session factory
│   │   ├── base.py               # SQLAlchemy Base class
│   │   └── models/               # ORM models
│   │       ├── __init__.py
│   │       ├── user.py
│   │       ├── message.py
│   │       ├── room.py
│   │       └── file.py
│   │
│   ├── repositories/             # Data Access Layer (Repository Pattern)
│   │   ├── __init__.py
│   │   ├── base.py               # Abstract Repository Protocol
│   │   ├── user_repository.py
│   │   ├── message_repository.py
│   │   └── room_repository.py
│   │
│   ├── services/                 # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── user_service.py       # User registration, auth logic
│   │   ├── chat_service.py       # Message handling, room management
│   │   ├── connection_manager.py # WebSocket Observer pattern
│   │   └── task_queue.py         # Background task management
│   │
│   └── api/                      # Presentation Layer
│       ├── __init__.py
│       ├── deps.py               # Route-level dependencies
│       ├── v1/                   # API version 1
│       │   ├── __init__.py
│       │   ├── router.py         # Aggregates all v1 routes
│       │   ├── auth.py           # /auth endpoints
│       │   ├── users.py          # /users endpoints
│       │   ├── rooms.py          # /rooms endpoints
│       │   ├── messages.py       # /messages endpoints
│       │   └── websocket.py      # WebSocket handlers
│       └── schemas/              # Pydantic request/response models
│           ├── __init__.py
│           ├── user.py
│           ├── message.py
│           ├── room.py
│           └── token.py
│
├── workers/                      # Background processors
│   ├── __init__.py
│   ├── base_worker.py            # Abstract worker class
│   ├── file_processor.py         # Image/document processing
│   └── notification_worker.py    # Push notification handling
│
└── tests/                        # Test suite
    ├── __init__.py
    ├── conftest.py               # Pytest fixtures
    ├── unit/                     # Unit tests
    │   ├── test_services/
    │   └── test_repositories/
    └── integration/              # Integration tests
        ├── test_api/
        └── test_websocket/
```

---

## 🎨 Design Patterns Applied

### 1. Repository Pattern
**Location:** `src/repositories/`

Decouples data access from business logic, enabling:
- Easy database swapping (PostgreSQL → MongoDB)
- Simplified testing with mock repositories
- Clear separation of concerns

```python
# Protocol definition
class UserRepository(Protocol):
    async def get_by_id(self, user_id: UUID) -> User | None: ...
    async def get_by_email(self, email: str) -> User | None: ...
    async def create(self, user: UserCreate) -> User: ...
    async def update(self, user_id: UUID, data: UserUpdate) -> User: ...
```

### 2. Factory Pattern
**Location:** `src/services/chat_service.py`

Creates different message types (Text, Image, System, File) with a unified interface:

```python
class MessageFactory:
    @staticmethod
    def create(msg_type: MessageType, **kwargs) -> BaseMessage:
        factories = {
            MessageType.TEXT: TextMessage,
            MessageType.IMAGE: ImageMessage,
            MessageType.SYSTEM: SystemMessage,
            MessageType.FILE: FileMessage,
        }
        return factories[msg_type](**kwargs)
```

### 3. Observer Pattern
**Location:** `src/services/connection_manager.py`

Manages WebSocket connections and broadcasts messages to subscribed clients:

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
    
    async def connect(self, room_id: str, websocket: WebSocket): ...
    async def disconnect(self, room_id: str, websocket: WebSocket): ...
    async def broadcast(self, room_id: str, message: dict): ...
```

### 4. Command Pattern
**Location:** `src/services/task_queue.py`

Encapsulates background tasks as serializable objects:

```python
@dataclass
class ProcessImageCommand:
    file_id: UUID
    user_id: UUID
    operations: list[str]  # ["resize", "compress", "thumbnail"]
    
    def to_json(self) -> str: ...
    
    @classmethod
    def from_json(cls, data: str) -> "ProcessImageCommand": ...
```

### 5. Dependency Injection
**Location:** `src/core/dependencies.py`, `src/api/deps.py`

Leverages FastAPI's dependency injection for clean, testable code:

```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
) -> User:
    ...

async def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository)
```

---

## 🔄 Data Flow Diagrams

### Authentication Flow

```
┌────────┐     POST /auth/login      ┌─────────┐
│ Client │ ──────────────────────────► FastAPI │
└────────┘   {email, password}       └────┬────┘
                                          │
                                          ▼
                                    ┌───────────┐
                                    │ UserSvc   │
                                    │ verify()  │
                                    └─────┬─────┘
                                          │
                                          ▼
                                    ┌───────────┐
                                    │ UserRepo  │
                                    │ get_by_   │
                                    │ email()   │
                                    └─────┬─────┘
                                          │
                                          ▼
                                    ┌───────────┐
                                    │PostgreSQL │
                                    └─────┬─────┘
                                          │
                                          ▼
┌────────┐     {access_token, ...}   ┌─────────┐
│ Client │ ◄──────────────────────── │ FastAPI │
└────────┘                           └─────────┘
```

### Real-Time Message Flow

```
┌──────────┐  WS Message   ┌───────────┐
│ Client A │ ─────────────► │ FastAPI  │
│(Instance1)│               │ #1       │
└──────────┘               └─────┬─────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
              ┌──────────┐ ┌──────────┐ ┌──────────┐
              │ Save to  │ │ Publish  │ │ Broadcast│
              │ Postgres │ │ to Redis │ │ Local    │
              └──────────┘ └────┬─────┘ │ Clients  │
                                │       └──────────┘
                                │
                    Redis Pub/Sub Channel
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
        ┌───────────┐    ┌───────────┐    ┌───────────┐
        │ FastAPI   │    │ FastAPI   │    │ FastAPI   │
        │ #1        │    │ #2        │    │ #N        │
        └─────┬─────┘    └─────┬─────┘    └─────┬─────┘
              │                │                │
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │Broadcast │    │Broadcast │    │Broadcast │
        │to Local  │    │to Local  │    │to Local  │
        │Clients   │    │Clients   │    │Clients   │
        └──────────┘    └──────────┘    └──────────┘
```

### Background Task Flow

```
┌────────┐  POST /upload     ┌─────────┐
│ Client │ ──────────────────► FastAPI │
└────────┘  {file}           └────┬────┘
                                  │
      ┌───────────────────────────┼───────────────────────┐
      ▼                           ▼                       ▼
┌───────────┐           ┌─────────────────┐       ┌─────────────┐
│Save Meta  │           │Push Command to  │       │Return 202   │
│to Postgres│           │Redis Queue      │       │{task_id,    │
│           │           │(LPUSH)          │       │status:      │
└───────────┘           └────────┬────────┘       │"processing"}│
                                 │                └─────────────┘
                                 ▼
                        ┌─────────────────┐
                        │    Redis List   │
                        │  (Task Queue)   │
                        └────────┬────────┘
                                 │
                                 │ BRPOP (blocking)
                                 ▼
                        ┌─────────────────┐
                        │     Worker      │
                        │ (File Processor)│
                        └────────┬────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
              ┌──────────┐ ┌──────────┐ ┌──────────┐
              │ Process  │ │ Upload   │ │ Update   │
              │ Image    │ │ to S3    │ │ Status   │
              └──────────┘ └──────────┘ └──────────┘
```

---

## 🗄️ Database Schema

### Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                            USERS                                 │
├─────────────────────────────────────────────────────────────────┤
│ id: UUID (PK)                                                   │
│ email: VARCHAR(255) UNIQUE NOT NULL                             │
│ hashed_password: VARCHAR(255) NOT NULL                          │
│ username: VARCHAR(50) UNIQUE NOT NULL                           │
│ avatar_url: VARCHAR(500) NULL                                   │
│ is_active: BOOLEAN DEFAULT TRUE                                 │
│ is_verified: BOOLEAN DEFAULT FALSE                              │
│ created_at: TIMESTAMP DEFAULT NOW()                             │
│ updated_at: TIMESTAMP DEFAULT NOW()                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ 1:N
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                           MESSAGES                               │
├─────────────────────────────────────────────────────────────────┤
│ id: UUID (PK)                                                   │
│ content: TEXT NOT NULL                                          │
│ message_type: ENUM('text','image','file','system')              │
│ sender_id: UUID (FK → users.id)                                 │
│ room_id: UUID (FK → rooms.id)                                   │
│ file_id: UUID (FK → files.id) NULL                              │
│ is_edited: BOOLEAN DEFAULT FALSE                                │
│ created_at: TIMESTAMP DEFAULT NOW()                             │
│ updated_at: TIMESTAMP DEFAULT NOW()                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                            ROOMS                                 │
├─────────────────────────────────────────────────────────────────┤
│ id: UUID (PK)                                                   │
│ name: VARCHAR(100) NOT NULL                                     │
│ description: TEXT NULL                                          │
│ is_private: BOOLEAN DEFAULT FALSE                               │
│ owner_id: UUID (FK → users.id)                                  │
│ created_at: TIMESTAMP DEFAULT NOW()                             │
│ updated_at: TIMESTAMP DEFAULT NOW()                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ N:M
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        ROOM_MEMBERS                              │
├─────────────────────────────────────────────────────────────────┤
│ room_id: UUID (FK → rooms.id) (PK)                              │
│ user_id: UUID (FK → users.id) (PK)                              │
│ role: ENUM('owner','admin','member') DEFAULT 'member'           │
│ joined_at: TIMESTAMP DEFAULT NOW()                              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                            FILES                                 │
├─────────────────────────────────────────────────────────────────┤
│ id: UUID (PK)                                                   │
│ filename: VARCHAR(255) NOT NULL                                 │
│ original_name: VARCHAR(255) NOT NULL                            │
│ mime_type: VARCHAR(100) NOT NULL                                │
│ size_bytes: BIGINT NOT NULL                                     │
│ storage_path: VARCHAR(500) NOT NULL                             │
│ status: ENUM('pending','processing','completed','failed')       │
│ uploader_id: UUID (FK → users.id)                               │
│ created_at: TIMESTAMP DEFAULT NOW()                             │
│ processed_at: TIMESTAMP NULL                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔐 Security Considerations

### Authentication & Authorization

1. **JWT Tokens** - Short-lived access tokens (15 min) + refresh tokens (7 days)
2. **Password Hashing** - bcrypt with salt rounds
3. **Rate Limiting** - Per-IP and per-user limits on sensitive endpoints
4. **CORS** - Strict origin validation in production

### Data Protection

1. **Input Validation** - Pydantic models for all request data
2. **SQL Injection Prevention** - Parameterized queries via SQLAlchemy
3. **XSS Prevention** - Sanitized message content before storage
4. **File Upload Security** - Type validation, size limits, virus scanning

---

## 🚀 Deployment Architecture

### Docker Compose (Development)

```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    depends_on: [db, redis]
    
  worker:
    build: .
    command: python -m workers.file_processor
    depends_on: [redis]
    
  db:
    image: postgres:15-alpine
    volumes: [postgres_data:/var/lib/postgresql/data]
    
  redis:
    image: redis:7-alpine
    volumes: [redis_data:/data]
```

### Production Considerations

- **Kubernetes** for container orchestration
- **AWS RDS** for managed PostgreSQL
- **AWS ElastiCache** for managed Redis
- **S3** for file storage
- **CloudFront** for CDN

---

## 📊 API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | User registration |
| POST | `/api/v1/auth/login` | User login (returns JWT) |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/users/me` | Get current user profile |
| PUT | `/api/v1/users/me` | Update current user |
| GET | `/api/v1/rooms` | List available rooms |
| POST | `/api/v1/rooms` | Create new room |
| GET | `/api/v1/rooms/{id}` | Get room details |
| GET | `/api/v1/rooms/{id}/messages` | Get room message history |
| POST | `/api/v1/files/upload` | Upload file (returns task ID) |
| GET | `/api/v1/files/{id}/status` | Check upload status |
| WS | `/api/v1/ws/{room_id}` | WebSocket connection |

---

## ✅ SOLID Principles Applied

| Principle | Application |
|-----------|-------------|
| **S**ingle Responsibility | Each service handles one domain (UserService, ChatService) |
| **O**pen/Closed | Message types extensible via Factory without modifying existing code |
| **L**iskov Substitution | Repository implementations interchangeable via Protocol |
| **I**nterface Segregation | Small, focused protocols (Repository, MessageHandler) |
| **D**ependency Inversion | High-level services depend on abstractions (Repository Protocol) |

---

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Redis Pub/Sub](https://redis.io/docs/manual/pubsub/)
- [12-Factor App](https://12factor.net/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
