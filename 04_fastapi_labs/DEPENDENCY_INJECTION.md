# FastAPI Dependency Injection System

## Overview

FastAPI's dependency injection (DI) system is a powerful feature that enables:
- **Automatic dependency resolution**: Inject dependencies into route handlers automatically
- **Code reusability**: Share common logic across multiple endpoints
- **Testability**: Easy to mock dependencies for testing
- **Decoupling**: Separate concerns between route handlers and business logic

## Core Concepts

### 1. **Dependency Function**
A callable (function) that returns a value to be used in other functions.

```python
def get_db() -> Database:
    """Dependency that provides database connection"""
    db = Database()
    yield db
    db.close()
```

### 2. **Dependency Declaration**
Dependencies are declared using the `Depends()` class in function parameters.

```python
from fastapi import Depends

@app.get("/items/")
def read_items(db: Database = Depends(get_db)):
    return db.query("SELECT * FROM items")
```

### 3. **Sub-dependencies**
Dependencies can depend on other dependencies, creating a dependency tree.

```python
def get_user_id(token: str = Header(...)) -> int:
    return decode_token(token)

def get_current_user(user_id: int = Depends(get_user_id)) -> User:
    return db.get_user(user_id)

@app.get("/users/me")
def read_current_user(user: User = Depends(get_current_user)):
    return user
```

## Key Features

### Dependency Types

#### 1. **Function Dependencies**
```python
def common_parameters(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/items/")
def read_items(params: dict = Depends(common_parameters)):
    return params
```

#### 2. **Class Dependencies**
```python
class CommonQueryParams:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/items/")
def read_items(params: CommonQueryParams = Depends()):
    return {"skip": params.skip, "limit": params.limit}
```

#### 3. **Context Managers** (Resource Cleanup)
```python
from contextlib import contextmanager

@contextmanager
def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
def read_items(db = Depends(get_db)):
    return db.query("SELECT * FROM items")
```

### Caching & Performance

FastAPI caches dependencies within a single request by default:
- Multiple uses of the same dependency in a request reuse the same instance
- Use `use_cache=False` if you need a fresh instance each time

```python
def get_query_params(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/items/")
def read_items(
    params1: dict = Depends(get_query_params),
    params2: dict = Depends(get_query_params, use_cache=False)
):
    # params1 and params2 reference the same instance
    # Unless use_cache=False is specified
    return {"params1": params1, "params2": params2}
```

## Benefits

| Benefit | Description |
|---------|-------------|
| **Modularity** | Separate business logic from route handlers |
| **Reusability** | Share dependencies across multiple routes |
| **Testability** | Mock dependencies easily in unit tests |
| **Automatic Validation** | Dependencies are validated automatically |
| **Self-documenting** | Type hints make dependencies explicit |
| **Error Handling** | FastAPI handles dependency errors gracefully |

## Common Use Cases

1. **Database connections** - Share a single connection pool
2. **Authentication** - Validate tokens and extract user info
3. **Authorization** - Check permissions before executing handlers
4. **Logging** - Inject logger instances
5. **External API clients** - Share API client instances
6. **Configuration** - Inject app configuration
7. **Business Logic** - Share service/repository classes

