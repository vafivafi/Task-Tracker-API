from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.core.config import config
from app.loger.log import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:    
        await config.create_tables
        logger.info("Таблицы успешно созданы")

        yield

        await config.disconnect
        logger.info("База данных успешно отключена")
    except Exception as e:
        logger.info(f"Ошибка базы данных {e}")
        
        
app = FastAPI(lifespan=lifespan)


