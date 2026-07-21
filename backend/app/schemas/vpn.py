from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ServerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    address: str = Field(min_length=3, max_length=255)
    protocol: str = Field(default="wireguard", pattern="^(wireguard|amneziawg|xray)$")


class ServerResponse(ServerCreate):
    id: UUID
    is_active: bool
    model_config = {"from_attributes": True}


class ClientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    server_id: UUID
    expires_at: datetime | None = None


class ClientResponse(ClientCreate):
    id: UUID
    disabled_at: datetime | None
    model_config = {"from_attributes": True}
