from typing import Dict

from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import FileRouter, HealthRouter, UserRouter
from app.config import get_settings, setup_logging, logger
from app.dependencies.database import get_db_session

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("[bold green]this is a test[/bold green] without color")
    yield
    logger.info("Stopping application")


app = FastAPI(lifespan=lifespan)


@app.get("/ping")
def ping() -> Dict[str, str]:
    return {"status": "ok", "env": settings.env}


app.include_router(HealthRouter, prefix="/health", tags=["Health"])
app.include_router(UserRouter, prefix="/users", tags=["Users"])
app.include_router(FileRouter, prefix="/files", tags=["Files"])
