from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from app.core.config import Config
from app.loger.log import logger
from app.models.user import UsersOrm
from app.models.task import TasksOrm
from app.api.v1.auth import auth_router
from app.api.v1.tasks import task_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:    
        await Config.create_tables()
        logger.info("Таблицы успешно созданы")

        yield

        await Config.disconnect()
        logger.info("База данных успешно отключена")
    except Exception as e:
        logger.info(f"Ошибка базы данных {e}")
        
        
app = FastAPI(lifespan=lifespan, title="Task Tracker API")

app.include_router(auth_router)
app.include_router(task_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)



