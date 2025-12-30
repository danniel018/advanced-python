from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)


async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False
)

async def get_session_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
        
