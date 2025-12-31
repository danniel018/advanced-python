from fastapi import FastAPI
from .api.v1 import users

app = FastAPI(title="Capstone Project API", version="1.0.0")
app.include_router(users.router, prefix="/api/v1")
