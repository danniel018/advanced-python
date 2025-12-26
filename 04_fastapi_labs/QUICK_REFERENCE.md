# FastAPI Dependency Injection - Quick Reference

## Table of Contents
1. [Basic Syntax](#basic-syntax)
2. [Dependency Types](#dependency-types)
3. [Dependency Patterns](#dependency-patterns)
4. [Best Practices](#best-practices)
5. [Common Use Cases](#common-use-cases)
6. [Testing](#testing)

---

## Basic Syntax

### Declaring a Dependency
```python
from fastapi import Depends

def my_dependency():
    return "value"

@app.get("/")
def my_endpoint(value: str = Depends(my_dependency)):
    return {"value": value}
```

### Dependency with Parameters
```python
def pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/items")
def get_items(params: dict = Depends(pagination)):
    return params
```

---

## Dependency Types

### Function Dependencies
```python
def get_db():
    # Initialize resource
    yield db
    # Cleanup resource
```

### Class Dependencies
```python
class CommonParams:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/items")
def get_items(params: CommonParams = Depends()):
    return params.skip
```

### Generator Dependencies (Context Managers)
```python
from contextlib import contextmanager

@contextmanager
def get_resource():
    resource = Resource()
    try:
        yield resource
    finally:
        resource.cleanup()

@app.get("/")
def endpoint(resource = Depends(get_resource)):
    return resource.use()
```

---

## Dependency Patterns

### Sub-dependencies (Dependency Tree)
```
Endpoint
  └─ Depends(get_current_user)
      └─ Depends(verify_token)
          └─ Depends(extract_token)
```

```python
def extract_token(authorization: str = Header(...)) -> str:
    return authorization.split(" ")[1]

def verify_token(token: str = Depends(extract_token)) -> int:
    return decode_token(token)

def get_current_user(user_id: int = Depends(verify_token)):
    return db.get_user(user_id)

@app.get("/me")
def current_user(user: User = Depends(get_current_user)):
    return user
```

### Caching Dependencies
```python
# Within a single request, dependencies are cached by default
@app.get("/")
def endpoint(
    dep1 = Depends(my_dependency),     # Called once
    dep2 = Depends(my_dependency)      # Returns cached value
):
    pass

# Force fresh instance
@app.get("/")
def endpoint(
    dep1 = Depends(my_dependency),                    # Called
    dep2 = Depends(my_dependency, use_cache=False)   # Fresh call
):
    pass
```

### Optional Dependencies
```python
from typing import Optional

def optional_token(token: Optional[str] = Header(None)) -> Optional[str]:
    return token

@app.get("/")
def endpoint(token: Optional[str] = Depends(optional_token)):
    return {"has_token": token is not None}
```

### Multiple Dependencies
```python
@app.get("/")
def endpoint(
    user: User = Depends(get_current_user),
    db: Database = Depends(get_db),
    logger: Logger = Depends(get_logger),
    config: Config = Depends(get_config)
):
    pass
```

---

## Best Practices

### ✅ DO

1. **Use dependencies for cross-cutting concerns**
   ```python
   def verify_auth(token: str = Header(...)):
       # Shared authentication logic
       return decode_token(token)
   ```

2. **Create reusable dependency chains**
   ```python
   def get_current_user(token: str = Depends(verify_auth)):
       return fetch_user(token)
   
   # Reuse across multiple endpoints
   @app.get("/me")
   def profile(user: User = Depends(get_current_user)):
       pass
   ```

3. **Use class-based dependencies for complex logic**
   ```python
   class Pagination:
       def __init__(self, skip: int = 0, limit: int = 10):
           self.skip = skip
           self.limit = limit
       
       def get_range(self):
           return (self.skip, self.skip + self.limit)
   
   @app.get("/items")
   def items(paging: Pagination = Depends()):
       return list(items[paging.skip:paging.skip + paging.limit])
   ```

4. **Separate concerns into different layers**
   ```python
   # Authentication layer
   def authenticate(token: str = Header(...)):
       return verify_token(token)
   
   # Authorization layer
   def require_admin(user_id: int = Depends(authenticate)):
       user = db.get_user(user_id)
       if not user.is_admin:
           raise HTTPException(403, "Admin required")
       return user
   ```

### ❌ DON'T

1. **Don't put business logic in dependencies**
   ```python
   # ❌ Bad
   def dependency():
       # Heavy computation
       result = expensive_operation()
       return result
   
   # ✅ Good
   def dependency(service: MyService = Depends(get_service)):
       return service
   
   @app.get("/")
   def endpoint(service: MyService = Depends(dependency)):
       result = service.expensive_operation()
       return result
   ```

2. **Don't create new connections for every request**
   ```python
   # ❌ Bad
   def get_db():
       return Database("connection_string")
   
   # ✅ Good
   _db = Database("connection_string")
   
   def get_db():
       return _db
   ```

3. **Don't neglect cleanup of resources**
   ```python
   # ❌ Bad
   def get_db():
       return Database()  # Connection never closed
   
   # ✅ Good
   def get_db():
       db = Database()
       try:
           yield db
       finally:
           db.close()
   ```

---

## Common Use Cases

### Authentication & Authorization
```python
def get_current_user(token: str = Header(...)):
    user_id = verify_jwt(token)
    return db.get_user(user_id)

def require_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(403)
    return user

@app.post("/admin/settings")
def update_settings(settings: Settings, admin: User = Depends(require_admin)):
    pass
```

### Database Connections
```python
def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
def get_items(db: Database = Depends(get_db)):
    return db.query("SELECT * FROM items")
```

### Logging
```python
def get_logger():
    return logging.getLogger(__name__)

@app.get("/")
def endpoint(logger = Depends(get_logger)):
    logger.info("Request received")
    return {"status": "ok"}
```

### Configuration
```python
def get_config():
    return Config.from_env()

@app.on_event("startup")
async def startup(config: Config = Depends(get_config)):
    await initialize_services(config)
```

### Request Validation
```python
def validate_id(item_id: int = Path(..., gt=0)):
    return item_id

@app.get("/items/{item_id}")
def get_item(item_id: int = Depends(validate_id)):
    return db.get_item(item_id)
```

---

## Testing

### Mocking Dependencies
```python
from fastapi.testclient import TestClient

def mock_database():
    return {"items": []}

app.dependency_overrides[get_db] = mock_database

client = TestClient(app)
response = client.get("/items")

# Clean up
app.dependency_overrides.clear()
```

### Test with Different User Contexts
```python
def mock_admin():
    return User(id=1, is_admin=True)

def mock_user():
    return User(id=2, is_admin=False)

app.dependency_overrides[get_current_user] = mock_admin
client = TestClient(app)
assert client.get("/admin").status_code == 200

app.dependency_overrides[get_current_user] = mock_user
client = TestClient(app)
assert client.get("/admin").status_code == 403
```

---

## Common Patterns Summary

| Pattern | Use Case | Example |
|---------|----------|---------|
| Function | Simple dependencies | `def get_config()` |
| Class | Complex with state | `class Pagination` |
| Generator | Resource cleanup | `yield db; cleanup()` |
| Sub-dependencies | Dependency chains | Auth → User → Profile |
| Optional | Conditional deps | Bearer token (optional) |
| Caching | Performance | Reuse within request |
| Override | Testing | Mock in tests |

---

## Quick Start Example

```python
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

# 1. Define a service
class UserService:
    def get_user(self, user_id: int):
        return {"id": user_id, "name": "John"}

# 2. Create a dependency for the service
def get_user_service():
    return UserService()

# 3. Create a dependency for authentication
def get_current_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404)
    return user

# 4. Use in endpoint
@app.get("/users/me")
def profile(user = Depends(get_current_user)):
    return user
```

This provides automatic:
- ✅ Dependency injection
- ✅ Request validation
- ✅ Error handling
- ✅ Automatic API documentation
- ✅ Testability
