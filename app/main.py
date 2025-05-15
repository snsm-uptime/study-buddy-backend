from typing import Dict

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import health
from app.config import get_settings
from app.db.deps import get_db

app = FastAPI()
settings = get_settings()


@app.get("/ping")
def ping() -> Dict[str, str]:
    return {"status": "ok", "env": settings.env}


app.include_router(health.router)
