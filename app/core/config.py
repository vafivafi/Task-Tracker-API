from app.database import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase


class Config:
    self.async_engine = create_async_engine(settings.DATABASE_URL, echo=True)

    self.async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass
