from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from .api import health
from .config import get_settings
from .db.deps import get_db

app = FastAPI()
settings = get_settings()


@app.get("/ping")
def ping():
    return {"status": "ok", "env": settings.env}


app.include_router(health.router)
