"""
FastAPI Dependency Injection Examples
Demonstrates various dependency patterns and use cases
"""

from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="FastAPI Dependency Injection Examples")


# ============================================================================
# EXAMPLE 1: Simple Function Dependencies
# ============================================================================


def get_query_params(skip: int = 0, limit: int = 10):
    """Simple dependency that extracts common query parameters"""
    return {"skip": skip, "limit": limit}


@app.get("/items/")
def read_items(params: dict = Depends(get_query_params)):
    """
    Route handler with dependency injection.
    The get_query_params function is automatically called with request parameters.
    """
    return {"message": "Items endpoint", "pagination": params}


# ============================================================================
# EXAMPLE 2: Class-based Dependencies
# ============================================================================


class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True


class PaginationParams:
    """Class-based dependency for pagination"""

    def __init__(self, skip: int = 0, limit: int = 10, sort_by: str = "id"):
        self.skip = skip
        self.limit = limit
        self.sort_by = sort_by


@app.get("/users/", response_model=dict)
def list_users(params: PaginationParams = Depends()):
    """
    Using a class as a dependency.
    FastAPI automatically instantiates it with request parameters.
    """
    return {
        "message": "Users list",
        "skip": params.skip,
        "limit": params.limit,
        "sort_by": params.sort_by,
    }


# ============================================================================
# EXAMPLE 3: Sub-dependencies (Dependency Tree)
# ============================================================================

# Simulated database
fake_db = {
    "users": {
        1: {"id": 1, "name": "Alice", "email": "alice@example.com", "is_active": True},
        2: {"id": 2, "name": "Bob", "email": "bob@example.com", "is_active": True},
    }
}


def verify_token(token: str = Header(...)) -> int:
    """
    First-level dependency: Extract and validate token.
    Returns the user_id from the token.
    """
    # Simple token validation (in reality, use JWT)
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid token")

    user_id = int(token.split()[-1])  # Simplified: token = "Bearer 1"
    if user_id not in fake_db["users"]:
        raise HTTPException(status_code=404, detail="User not found")

    return user_id


def get_current_user(user_id: int = Depends(verify_token)) -> User:
    """
    Second-level dependency: Depends on verify_token.
    Retrieves the complete User object.
    """
    user_data = fake_db["users"][user_id]
    return User(**user_data)


@app.get("/auth/me", response_model=User)
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Route handler with nested dependencies.
    Dependency chain: verify_token -> get_current_user -> read_current_user
    """
    return current_user


@app.get("/auth/user-data")
def get_user_data(current_user: User = Depends(get_current_user)):
    """Another endpoint using the same dependency chain"""
    return {"user": current_user, "timestamp": datetime.now().isoformat()}


# ============================================================================
# EXAMPLE 4: Optional Dependencies
# ============================================================================


def get_optional_token(token: Optional[str] = Header(None)) -> Optional[str]:
    """Dependency that returns None if token is not provided"""
    return token


@app.get("/public/items")
def read_public_items(token: Optional[str] = Depends(get_optional_token)):
    """
    Endpoint that works with or without authentication.
    If token is provided, return personalized response.
    """
    if token:
        return {"message": "Public items (authenticated)", "token": token}
    else:
        return {"message": "Public items (anonymous)"}


# ============================================================================
# EXAMPLE 5: Dependency with Side Effects (Database Connection)
# ============================================================================


class Database:
    """Simulated database connection"""

    def __init__(self):
        self.connected = True
        print("Database connected")

    def close(self):
        self.connected = False
        print("Database closed")

    def query(self, sql: str) -> List[dict]:
        if not self.connected:
            raise RuntimeError("Database connection is closed")
        return [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]


def get_db():
    """
    Generator-based dependency for resource management.
    Yields the resource and cleans up after use.
    """
    db = Database()
    try:
        yield db
    finally:
        db.close()


@app.get("/database/items")
def get_items_from_db(db: Database = Depends(get_db)):
    """
    Endpoint that uses database dependency.
    FastAPI handles the context manager lifecycle.
    """
    items = db.query("SELECT * FROM items")
    return {"items": items}


# ============================================================================
# EXAMPLE 6: Multiple Dependencies in One Handler
# ============================================================================


def get_user_agent(user_agent: str = Header(None)) -> str:
    """Extract user agent from headers"""
    return user_agent or "Unknown"


@app.get("/complex")
def complex_endpoint(
    pagination: PaginationParams = Depends(),
    user_agent: str = Depends(get_user_agent),
    token: Optional[str] = Depends(get_optional_token),
    db: Database = Depends(get_db),
):
    """
    Endpoint with multiple dependencies.
    Each dependency is resolved independently.
    Dependencies can depend on other dependencies.
    """
    return {
        "pagination": {"skip": pagination.skip, "limit": pagination.limit},
        "user_agent": user_agent,
        "authenticated": token is not None,
        "db_status": "connected" if db.connected else "disconnected",
    }


# ============================================================================
# EXAMPLE 7: Dependency Caching
# ============================================================================

call_count = 0


def count_calls(times: int = 1) -> int:
    """Dependency that increments a counter"""
    global call_count
    call_count += 1
    print(f"count_calls called - Total calls: {call_count}")
    return call_count


@app.get("/cache-demo")
def cache_demo(
    count1: int = Depends(count_calls),
    count2: int = Depends(count_calls),  # Uses cached value by default
    count3: int = Depends(count_calls, use_cache=False),  # Fresh call
):
    """
    Demonstrates dependency caching within a request.
    count1 and count2 will have the same value (cached).
    count3 will have a different value (use_cache=False).
    """
    return {
        "count1": count1,
        "count2": count2,
        "count3": count3,
        "cached": count1 == count2,
        "not_cached": count1 != count3,
    }


# ============================================================================
# EXAMPLE 8: Dependency for Validation
# ============================================================================


def validate_limit(limit: int = 10) -> int:
    """Dependency that validates and constrains limit parameter"""
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit cannot exceed 100")
    if limit < 1:
        raise HTTPException(status_code=400, detail="Limit must be at least 1")
    return limit


@app.get("/validated-items")
def get_validated_items(limit: int = Depends(validate_limit)):
    """
    Endpoint with validation dependency.
    Invalid limit values are rejected automatically.
    """
    return {"limit": limit, "items": list(range(1, limit + 1))}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
