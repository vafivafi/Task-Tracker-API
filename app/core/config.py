from app.settings import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase



class Config:
    async_engine = create_async_engine(settings.DATABASE_URL, echo=True)

    async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
    
    @classmethod
    async def create_tables(cls):
        async with cls.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    @classmethod
    async def disconnect(cls):
        await cls.async_engine.dispose()

class Base(DeclarativeBase):
    pass


