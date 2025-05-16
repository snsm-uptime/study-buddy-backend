from typing import Dict

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db_session

router = APIRouter()


@router.get("/health-db")
async def health_check(db: AsyncSession = Depends(get_db_session)) -> Dict[str, str]:
    await db.execute(text("SELECT 1"))
    return {"status": "connected"}
