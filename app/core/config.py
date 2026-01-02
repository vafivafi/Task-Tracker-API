from app.database import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import sqlite3
import aiosqlite


class Config:
    def __init__(self):
    
        self.async_engine = create_async_engine(settings.DATABASE_URL, echo=True)

        self.async_session_factory = async_sessionmaker(self.async_engine, expire_on_commit=False, class_=AsyncSession)
    
    @property
    async def create_tables(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    @property
    async def disconnect(self):
        await self.async_engine.dispose()

class Base(DeclarativeBase):
    pass


config = Config()
