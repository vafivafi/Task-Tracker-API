from app.core.config import Config
from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

class Dependencies:
    @staticmethod
    async def get_session():
        async with Config.async_session_factory() as session:
            yield session

SessionDep = Annotated[AsyncSession, Depends(Dependencies.get_session)]

    