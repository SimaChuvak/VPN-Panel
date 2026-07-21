from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog


async def record_audit(
    session: AsyncSession, *, actor_id: UUID, action: str, subject: str, details: str | None = None
) -> None:
    session.add(AuditLog(actor_id=actor_id, action=action, subject=subject, details=details))
