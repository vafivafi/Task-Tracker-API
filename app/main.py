from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.core.config import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    await config.create_tables
    
    yield

    await config.disconnect
    
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def get_data():
    return {"message": "привет"}
