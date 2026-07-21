from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.api import auth, users, vpn

router = APIRouter()
router.include_router(auth.router)
router.include_router(users.router)
router.include_router(vpn.router)


@router.get("/health", tags=["system"])
async def health(db: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    await db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok"}
