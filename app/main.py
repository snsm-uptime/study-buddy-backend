from typing import Dict

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import FileRouter, HealthRouter, UserRouter
from app.config import get_settings
from app.dependencies.database import get_db_session

app = FastAPI()
settings = get_settings()


@app.get("/ping")
def ping() -> Dict[str, str]:
    return {"status": "ok", "env": settings.env}


app.include_router(HealthRouter, prefix="/health", tags=["Health"])
app.include_router(UserRouter, prefix="/users", tags=["Users"])
app.include_router(FileRouter, prefix="/files", tags=["Files"])
