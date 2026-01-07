# Async Integration Testing Guide

## Overview

This document explains how the integration tests are configured to work with FastAPI's async framework, SQLAlchemy async sessions, and pytest-asyncio. The testing infrastructure ensures proper isolation, async context management, and dependency injection overrides.

---

## Architecture Components

### 1. Test Configuration (pytest.ini)

```ini
[pytest]
pythonpath = .
asyncio_mode = auto
```

**Key Settings:**
- **`pythonpath = .`**: Sets the project root as the base path for imports
- **`asyncio_mode = auto`**: Automatically detects and handles async test functions without requiring `@pytest.mark.asyncio` decorator on every test (though we still use it for clarity)

---

## 2. Test Fixtures (tests/conftest.py)

The `tests/conftest.py` file provides shared fixtures that establish the async testing infrastructure:

### 2.1 Async Database Engine

```python
@pytest_asyncio.fixture
async def async_engine():
    """Create a test database engine using in-memory SQLite"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()
```

**Purpose:**
- Creates an in-memory SQLite database for each test session
- Uses `aiosqlite` async driver for SQLite
- Automatically creates all tables from SQLAlchemy models
- Cleans up resources after tests complete

**Key Points:**
- ✅ Isolated database per test run
- ✅ Fast (in-memory)
- ✅ Proper async lifecycle management

### 2.2 Async Session

```python
@pytest_asyncio.fixture
async def async_session(async_engine):
    """Create a test database session"""
    async_session_local = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_local() as session:
        yield session
```

**Purpose:**
- Creates a database session tied to the test engine
- Provides transaction context for database operations
- `expire_on_commit=False` keeps objects accessible after commit (useful for testing)

### 2.3 Dependency Override

```python
@pytest.fixture
def override_get_session(async_session):
    """Override FastAPI dependency injection for testing"""
    from src.main import app

    async def get_test_session():
        yield async_session

    app.dependency_overrides[get_session_db] = get_test_session
    yield
    app.dependency_overrides.clear()
```

**Purpose:**
- Replaces the production database dependency (`get_session_db`) with test session
- Ensures all API endpoints use the test database
- Automatically clears overrides after tests to prevent pollution

**Flow:**
```
Production: get_session_db() → Production DB
Testing:    get_session_db() → Test DB (in-memory)
```

---

## 3. Integration Tests (tests/integration/test_user_endpoints.py)

### 3.1 Async Client Fixture

```python
@pytest.fixture(scope="function")
async def async_client(override_get_session):
    """Create an async test client"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
```

**Purpose:**
- Creates an `httpx.AsyncClient` for making HTTP requests to the FastAPI app
- Uses `ASGITransport` to mount the FastAPI application
- `scope="function"` ensures a fresh client for each test
- Depends on `override_get_session` to activate dependency injection override

**Important:**
- The client doesn't make real network requests—it directly invokes the ASGI app
- All requests are async and properly await responses

### 3.2 Test Structure

```python
class TestUserEndpoints:
    """Test suite for user API endpoints"""

    @pytest.mark.asyncio
    async def test_get_users_empty_list(self, async_client):
        """Test GET /users endpoint returns empty list initially"""
        response = await async_client.get("/api/v1/users/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 0
```

**Key Elements:**
- **`@pytest.mark.asyncio`**: Marks test as async (explicit marker for clarity)
- **`async def test_*`**: Async test function
- **`await async_client.get()`**: Async HTTP call
- **Assertions**: Standard synchronous assertions on the response

---

## How It All Works Together

### Request Flow in Tests

```
1. Test starts
   ↓
2. override_get_session fixture activates
   → Replaces app.dependency_overrides[get_session_db]
   ↓
3. async_client fixture creates httpx.AsyncClient
   ↓
4. Test makes async HTTP request: await async_client.get("/api/v1/users/")
   ↓
5. FastAPI router receives request
   ↓
6. Dependency injection resolves:
   get_user_service() → needs get_session_db()
   ↓
7. Override kicks in: returns test async_session (in-memory DB)
   ↓
8. UserService executes with test database
   ↓
9. Response returns to test
   ↓
10. Assertions verify behavior
    ↓
11. Cleanup: client closes, overrides clear, engine disposes
```

### Async Context Management

Every async resource properly manages its lifecycle:

```python
# Engine lifecycle
async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
# → Automatic transaction handling

# Session lifecycle
async with async_session_local() as session:
    yield session
# → Automatic session cleanup

# Client lifecycle
async with AsyncClient(...) as client:
    yield client
# → Automatic connection cleanup
```

---

## Benefits of This Approach

### ✅ **Isolation**
- Each test gets a fresh in-memory database
- No test data pollution between tests
- Dependency overrides are cleared after each test

### ✅ **Speed**
- In-memory SQLite is extremely fast
- No network overhead (direct ASGI app invocation)
- Parallel test execution possible

### ✅ **Realism**
- Tests the actual FastAPI application
- Real dependency injection flow
- Real async database operations

### ✅ **Maintainability**
- Fixtures are reusable across all integration tests
- Centralized configuration in `tests/conftest.py`
- Clear separation of concerns

---

## Adding More Integration Tests

To add new integration tests:

1. **Use the `async_client` fixture:**
   ```python
   @pytest.mark.asyncio
   async def test_create_user(self, async_client):
       response = await async_client.post("/api/v1/users/", json={...})
       assert response.status_code == 201
   ```

2. **Access the test session directly if needed:**
   ```python
   @pytest.mark.asyncio
   async def test_with_db_setup(self, async_client, async_session):
       # Pre-populate test data
       async_session.add(User(name="Test"))
       await async_session.commit()
       
       # Make API request
       response = await async_client.get("/api/v1/users/")
       assert len(response.json()) == 1
   ```

3. **Test error conditions:**
   ```python
   @pytest.mark.asyncio
   async def test_user_not_found(self, async_client):
       response = await async_client.get("/api/v1/users/999")
       assert response.status_code == 404
   ```

---

## Common Patterns

### Testing POST Endpoints
```python
@pytest.mark.asyncio
async def test_create_user(self, async_client):
    payload = {"email": "test@example.com", "name": "Test User"}
    response = await async_client.post("/api/v1/users/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data
```

### Testing with Database State
```python
@pytest.mark.asyncio
async def test_update_existing_user(self, async_client, async_session):
    # Setup: Create user in DB
    user = User(email="old@example.com", name="Old Name")
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    
    # Test: Update user
    response = await async_client.patch(
        f"/api/v1/users/{user.id}",
        json={"name": "New Name"}
    )
    
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"
```

### Testing Validation Errors
```python
@pytest.mark.asyncio
async def test_create_user_invalid_email(self, async_client):
    payload = {"email": "not-an-email", "name": "Test"}
    response = await async_client.post("/api/v1/users/", json=payload)
    
    assert response.status_code == 422
    assert "detail" in response.json()
```

---

## Troubleshooting

### Issue: `RuntimeError: Event loop is closed`
**Solution:** Ensure all fixtures use `@pytest_asyncio.fixture` and `asyncio_mode = auto` is set in pytest.ini.

### Issue: Tests modify production database
**Solution:** Verify `override_get_session` fixture is being used and dependency overrides are active. Check that the test is importing the correct app instance.

### Issue: `AsyncClient` connection errors
**Solution:** Use `ASGITransport(app=app)` instead of a real URL. The client should invoke the app directly, not make network requests.

### Issue: Database state persists between tests
**Solution:** Use in-memory database (`:memory:`) and ensure `scope="function"` for session fixtures to get test isolation.

### Issue: Import errors or module not found
**Solution:** Verify `pythonpath = .` is set in pytest.ini and you're running pytest from the project root directory.

---

## Dependencies Required

```txt
pytest>=7.0.0
pytest-asyncio>=0.21.0
httpx>=0.24.0
sqlalchemy[asyncio]>=2.0.0
aiosqlite>=0.19.0
fastapi>=0.100.0
```

Install with:
```bash
pip install pytest pytest-asyncio httpx sqlalchemy[asyncio] aiosqlite fastapi
```

---

## Running the Tests

### Run all integration tests:
```bash
pytest tests/integration/
```

### Run specific test file:
```bash
pytest tests/integration/test_user_endpoints.py
```

### Run specific test:
```bash
pytest tests/integration/test_user_endpoints.py::TestUserEndpoints::test_get_users_empty_list
```

### Run with verbose output:
```bash
pytest tests/integration/ -v
```

### Run with coverage:
```bash
pytest tests/integration/ --cov=src --cov-report=html
```

---

## Summary

This async integration testing setup provides:
- **Full async/await support** throughout the testing stack
- **Isolated test databases** for each test run
- **FastAPI dependency injection override** for controlled testing
- **Realistic HTTP testing** without network overhead
- **Clean resource management** with proper async context managers

The architecture follows best practices for async Python testing and scales well as the application grows. Each component is designed to be reusable, maintainable, and easy to extend as you add more endpoints and features to your FastAPI application.
