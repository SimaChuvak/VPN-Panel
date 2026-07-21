from uuid import UUID

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import IdentifiedTimestamped


class AuditLog(IdentifiedTimestamped, Base):
    __tablename__ = "audit_logs"

    actor_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(128), index=True)
    subject: Mapped[str] = mapped_column(String(128))
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
