from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import IdentifiedTimestamped


class VpnServer(IdentifiedTimestamped, Base):
    __tablename__ = "vpn_servers"

    name: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    address: Mapped[str] = mapped_column(String(255), unique=True)
    protocol: Mapped[str] = mapped_column(String(32), default="wireguard")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
