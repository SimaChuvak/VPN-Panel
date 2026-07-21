from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.user import User
from app.services.auth_service import password_hash


async def create_initial_admin(session: AsyncSession) -> None:
    if not settings.admin_username or not settings.admin_password:
        return
    existing = await session.scalar(select(User.id).limit(1))
    if existing is not None:
        return
    session.add(
        User(
            username=settings.admin_username,
            password_hash=password_hash.hash(settings.admin_password),
            role="administrator",
        )
    )
    await session.commit()
