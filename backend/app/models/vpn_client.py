from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import IdentifiedTimestamped


class VpnClient(IdentifiedTimestamped, Base):
    __tablename__ = "vpn_clients"

    name: Mapped[str] = mapped_column(String(128), index=True)
    server_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("vpn_servers.id"))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    disabled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
