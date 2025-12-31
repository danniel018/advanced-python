# Capstone Project Setup Guide

This guide explains how to set up the development environment for the capstone project with all the tooling and infrastructure.

## Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose (for PostgreSQL)
- Git

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd advanced-python
   ```

2. **Install dependencies**:
   ```bash
   pip install -e ".[dev,test]"
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```

## Database Setup

### Option 1: PostgreSQL with Docker (Recommended for Development)

1. **Start PostgreSQL**:
   ```bash
   docker-compose up -d
   ```

2. **Update `.env` file**:
   ```env
   DATABASE_URL=postgresql+asyncpg://capstone:capstone_password@localhost:5432/capstone_db
   ```

3. **Run migrations**:
   ```bash
   cd capstone_project
   alembic upgrade head
   ```

### Option 2: SQLite (Quick Testing)

1. **Use default `.env` settings**:
   ```env
   DATABASE_URL=sqlite+aiosqlite:///./test.db
   ```

2. **Run migrations**:
   ```bash
   cd capstone_project
   alembic upgrade head
   ```

## Development

### Running the Application

```bash
cd capstone_project
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`. You can access the interactive API documentation at `http://localhost:8000/docs`.

### Running Tests

```bash
# Run all tests
pytest capstone_project/tests/

# Run with coverage
pytest capstone_project/tests/ --cov=capstone_project

# Run specific test file
pytest capstone_project/tests/test_user_service.py -v
```

### Code Quality

#### Linting

```bash
# Check code
ruff check capstone_project/

# Auto-fix issues
ruff check --fix capstone_project/
```

#### Formatting

```bash
# Format code
ruff format capstone_project/
```

#### Type Checking

```bash
# Check types
mypy capstone_project/src/
```

### Pre-commit Hooks (Optional)

To automatically run linting and formatting on every commit:

```bash
# Install pre-commit hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

## Database Migrations

### Creating a New Migration

```bash
cd capstone_project
alembic revision --autogenerate -m "Description of changes"
```

### Applying Migrations

```bash
cd capstone_project
alembic upgrade head
```

### Rolling Back Migrations

```bash
cd capstone_project
# Roll back one migration
alembic downgrade -1

# Roll back to a specific revision
alembic downgrade <revision_id>

# Roll back all migrations
alembic downgrade base
```

## Project Structure

```
capstone_project/
├── src/
│   ├── api/              # API endpoints
│   │   ├── v1/           # API version 1
│   │   └── dependencies.py
│   ├── core/             # Core application components
│   │   ├── config.py     # Configuration management
│   │   └── models.py     # Domain models
│   ├── db/               # Database components
│   │   ├── models.py     # SQLAlchemy ORM models
│   │   └── session.py    # Database session management
│   ├── repositories/     # Data access layer
│   ├── services/         # Business logic layer
│   └── main.py           # Application entry point
├── tests/                # Test suite
│   ├── conftest.py       # Test fixtures
│   ├── test_user_service.py
│   └── test_users_api.py
├── alembic/              # Database migrations
│   └── versions/         # Migration files
└── alembic.ini           # Alembic configuration
```

## Configuration

All configuration is managed through environment variables loaded from `.env` file:

- `DATABASE_URL`: Database connection string
- `DEBUG`: Enable debug mode (True/False)
- `DB_ECHO`: Echo SQL queries (True/False)
- `DB_POOL_SIZE`: Database connection pool size
- `DB_MAX_OVERFLOW`: Maximum overflow connections

See `.env.example` for all available options.

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL is running: `docker-compose ps`
- Check database logs: `docker-compose logs postgres`
- Verify connection string in `.env` file

### Migration Issues

- Ensure you're in the `capstone_project` directory when running Alembic commands
- Check that all models are imported in `src/db/models.py`
- Verify database is accessible and migrations table exists

### Test Failures

- Ensure all dependencies are installed: `pip install -e ".[dev,test]"`
- Check that test database can be created (SQLite permissions or PostgreSQL connection)
- Run tests with verbose output: `pytest -vv`

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `pytest capstone_project/tests/`
4. Run linting: `ruff check capstone_project/`
5. Run type checking: `mypy capstone_project/src/`
6. Commit your changes
7. Create a pull request
