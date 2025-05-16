from typing import Dict

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes import health, user
from app.config import get_settings
from app.dependencies.database import get_db_session

app = FastAPI()
settings = get_settings()


@app.get("/ping")
def ping() -> Dict[str, str]:
    return {"status": "ok", "env": settings.env}


app.include_router(health.router)
app.include_router(user.router, prefix="/users", tags=["Users"])
