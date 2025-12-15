# Advanced Python Mastery

> **Goal:** Build a production-grade **Real-Time Chat + Task Queue System** while mastering modern Python ecology, architectural patterns, and deep concurrency concepts.

---

## 📋 Project Overview

This repository is structured as a **progressive learning path** that culminates in a capstone project. Each phase builds upon the previous one, ensuring you understand not just *what* to code, but *why* and *how*.

### What You'll Build

A **Real-Time Chat Application** with:
- WebSocket-based instant messaging
- Distributed message broadcasting using Redis Pub/Sub
- Background task processing for file uploads (images, documents)
- JWT-based authentication
- PostgreSQL for persistent storage
- Horizontal scalability (multiple FastAPI instances)

---

## 🗂️ Repository Structure

```
advanced-python/
├── README.md                 # This file - Your roadmap and progress tracker
├── guideline.md              # Detailed study plan and execution guide
├── .gitignore                # Ignore venv, __pycache__, .env, etc.
├── pyproject.toml            # Global config (Ruff/Mypy settings)
│
├── 01_modern_setup/          # Phase 1: Modern Python Tooling
│   ├── playground_typing.py  # Experiments with Generic/Protocol
│   └── ruff_demo.py          # Code to test linting rules
│
├── 02_oop_patterns/          # Phase 2: Design Patterns Applied
│   ├── repository_pattern.py # Decoupling data access
│   ├── factory_method.py     # Standardizing object creation
│   └── solid_principles/     # S.O.L.I.D principle demonstrations
│
├── 03_concurrency/           # Phase 3: AsyncIO Deep Dive
│   ├── async_locks.py        # asyncio.Lock usage
│   ├── redis_pubsub.py       # Redis connectivity testing
│   └── worker_prototype.py   # Producer-consumer pattern
│
├── 04_fastapi_labs/          # Phase 4: FastAPI Features
│   ├── dependency_injection.py
│   └── middleware_demo.py
│
└── capstone_project/         # THE MAIN APPLICATION
    ├── .env                  # Environment variables
    ├── alembic.ini           # Database migrations
    ├── docker-compose.yml    # Redis + Postgres services
    ├── pyproject.toml        # App-specific dependencies
    ├── src/
    │   ├── main.py           # Application entrypoint
    │   ├── core/             # Config, Security, Exceptions
    │   ├── db/               # Database connection & models
    │   ├── services/         # Business Logic (UserSvc, ChatSvc)
    │   ├── api/              # REST & WebSocket endpoints
    │   └── repositories/     # Data Access Layer
    └── tests/                # Unit and integration tests
```

---

## 🎯 Learning Phases

### **Phase 1: Modern Python Ecology & Setup**
**Goal:** Create a professional development environment that prevents "spaghetti code" before writing a single line of logic.

**Key Topics:**
- Dependency Management (`uv` or `Poetry`)
- Configuration Management (Pydantic Settings + 12-Factor App)
- Type Checking (Mypy strict mode)
- Linting & Formatting (Ruff)

**Deliverable:** A configured repository with `pyproject.toml` and a strictly typed `config.py` that loads environment variables.

---

### **Phase 2: Architectural Patterns (OOP & SOLID)**
**Goal:** Define *how* data moves before defining *how* it travels over the network.

**Key Patterns:**
1. **Repository Pattern** - Decoupling database layer from business logic
2. **Factory Pattern** - Standardizing object creation (TextMessage, ImageMessage, SystemEvent)
3. **Observer Pattern** - WebSocket Manager broadcasts to all connected clients
4. **Command Pattern** - Task Queue encapsulates requests as serializable objects

**Deliverable:** Standalone pattern implementations that will be integrated into the capstone project.

---

### **Phase 3: Deep Concurrency (`asyncio` & Redis)**
**Goal:** Handle "Real-Time" and "Background" workloads without blocking the CPU.

**Key Topics:**
- Event Loop & Connection Pooling (`asyncpg`, `redis-py`)
- AsyncIO Synchronization (`asyncio.Lock`, `asyncio.Event`)
- Redis Pub/Sub for distributed messaging

**Challenge:** When User A on Instance 1 sends a message, User B on Instance 2 must receive it immediately via Redis.

**Deliverable:** Working producer-consumer prototype with Redis.

---

### **Phase 4: FastAPI Implementation**
**Goal:** Expose your architecture to the world via HTTP and WebSocket APIs.

**Key Topics:**
- WebSocket handling & authentication
- Dependency Injection (injecting current user, repositories)
- Background Tasks (simple vs. complex workers)

**Deliverable:** Isolated FastAPI experiments that demonstrate each feature.

---

## 🏗️ Architecture Overview

```
┌──────────┐
│  Client  │
└────┬─────┘
     │ WebSocket
     ▼
┌─────────────┐        ┌──────────┐
│   FastAPI   │◄──────►│  Redis   │ (Pub/Sub + Queue)
└─────┬───────┘        └────┬─────┘
      │                     │
      │ Repository          │ Pop Tasks
      ▼                     ▼
┌──────────┐        ┌──────────┐
│ Postgres │        │  Worker  │ (Background Processor)
└──────────┘        └──────────┘
```

**Flow:**
1. Client connects via WebSocket → FastAPI
2. FastAPI authenticates via JWT
3. FastAPI adds connection to Observer list (Connection Manager)
4. Client sends a message
5. FastAPI uses Repository to save to Postgres
6. FastAPI publishes event to Redis
7. All subscribed instances receive the event and broadcast to their connected clients
8. If file upload, Worker picks up Command from Redis to process the file

---

## 📅 4-Week Development Schedule

### **Week 1: Core & Data Layer**
- **Setup:** Poetry/UV, Ruff, Pytest
- **Topic:** Pydantic V2 & SQLAlchemy Async
- **Task:** Define `User` and `Message` tables, create Repository Protocol, implement JWT auth
- **Outcome:** REST API for register, login, and profile fetch

### **Week 2: Real-Time Engine**
- **Topic:** WebSockets & Redis Pub/Sub
- **Task:** Implement `ConnectionManager` (Observer pattern), integrate Redis
- **Challenge:** Handle disconnect events gracefully
- **Outcome:** Two users exchange messages in real-time

### **Week 3: Task Queue**
- **Topic:** `asyncio` producers/consumers
- **Task:** Build lightweight queue system with Redis Lists
- **Challenge:** `/upload` endpoint returns "Processing", status updates to "Done" after worker completes
- **Outcome:** Background file processing

### **Week 4: Production Polish**
- **Topic:** Rate Limiting, Docker, OpenAPI docs
- **Task:** Dockerize app, worker, Redis, and Postgres
- **Outcome:** Deployable artifact with `docker-compose`

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd advanced-python
   ```

2. **Install dependencies:**
   ```bash
   # Using Poetry
   poetry install
   
   # Or using uv
   uv sync
   ```

3. **Set up environment variables:**
   ```bash
   cd capstone_project
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start services:**
   ```bash
   docker-compose up -d
   ```

5. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start the application:**
   ```bash
   uvicorn src.main:app --reload
   ```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_repository.py
```

---

## 📚 Key Technologies

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Async web framework |
| **SQLAlchemy** | ORM with async support |
| **Pydantic** | Data validation & settings management |
| **Redis** | Pub/Sub messaging & task queue |
| **PostgreSQL** | Relational database |
| **asyncpg** | Async PostgreSQL driver |
| **Uvicorn** | ASGI server |
| **Ruff** | Linting & formatting |
| **Mypy** | Static type checking |
| **Pytest** | Testing framework |

---

## 📖 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/)
- [Redis Pub/Sub Guide](https://redis.io/docs/manual/pubsub/)
- [12-Factor App Methodology](https://12factor.net/)
- [Python AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html)

---

## 🎯 Progress Tracker

- [ ] **Phase 1:** Modern Python Setup
  - [ ] Configure dependency management
  - [ ] Set up Ruff & Mypy
  - [ ] Implement Pydantic Settings
- [ ] **Phase 2:** Architectural Patterns
  - [ ] Repository Pattern
  - [ ] Factory Pattern
  - [ ] Observer Pattern
  - [ ] Command Pattern
- [ ] **Phase 3:** Deep Concurrency
  - [ ] AsyncIO Lock experiments
  - [ ] Redis Pub/Sub prototype
  - [ ] Worker producer-consumer
- [ ] **Phase 4:** FastAPI Implementation
  - [ ] Dependency Injection
  - [ ] WebSocket handling
  - [ ] Background tasks
- [ ] **Capstone Project**
  - [ ] Week 1: Core & Data Layer
  - [ ] Week 2: Real-Time Engine
  - [ ] Week 3: Task Queue
  - [ ] Week 4: Production Polish

---

## 🤝 Contributing

This is a personal learning project, but suggestions and improvements are welcome! Feel free to open an issue or submit a pull request.

---

## 📝 License

This project is for educational purposes.

---

## 🔥 Next Steps

1. Review the [guideline.md](guideline.md) for detailed phase-by-phase instructions
2. Start with Phase 1 in the `01_modern_setup/` directory
3. Work through each phase systematically
4. Apply learned patterns in the `capstone_project/`

**Happy Coding! 🚀**
