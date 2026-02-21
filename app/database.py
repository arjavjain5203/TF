from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

settings = get_settings()

def build_engine_url(raw_url: str):
    """
    Transforms the DATABASE_URL for asyncpg compatibility:
    - Replaces postgres:// with postgresql+asyncpg://
    - Strips ?sslmode=require from query params and passes it as connect_args instead
    """
    if raw_url.startswith("postgres://"):
        raw_url = raw_url.replace("postgres://", "postgresql+asyncpg://", 1)

    connect_args = {}
    if "?sslmode=require" in raw_url:
        raw_url = raw_url.replace("?sslmode=require", "")
        connect_args["ssl"] = "require"
    elif "&sslmode=require" in raw_url:
        raw_url = raw_url.replace("&sslmode=require", "")
        connect_args["ssl"] = "require"

    return raw_url, connect_args

database_url, connect_args = build_engine_url(settings.DATABASE_URL)

engine = create_async_engine(database_url, echo=False, connect_args=connect_args)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
