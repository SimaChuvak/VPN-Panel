from fastapi import Header, HTTPException, status

from app.config import settings


async def require_backend(x_hostagent_token: str | None = Header(default=None)) -> None:
    if x_hostagent_token != settings.hostagent_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid HostAgent token")
