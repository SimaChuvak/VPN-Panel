from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.dependencies.permissions import require_roles
from app.models.user import User
from app.models.vpn_client import VpnClient
from app.models.vpn_server import VpnServer
from app.schemas.vpn import ClientCreate, ClientResponse, ServerCreate, ServerResponse
from app.services.audit_service import record_audit

router = APIRouter(prefix="/vpn", tags=["vpn"])
operator = Depends(require_roles("administrator", "operator"))


@router.get("/servers", response_model=list[ServerResponse])
async def list_servers(_: User = operator, session: AsyncSession = Depends(get_db_session)) -> list[VpnServer]:
    return list((await session.scalars(select(VpnServer).order_by(VpnServer.name))).all())


@router.post("/servers", response_model=ServerResponse, status_code=status.HTTP_201_CREATED)
async def create_server(payload: ServerCreate, user: User = operator, session: AsyncSession = Depends(get_db_session)) -> VpnServer:
    server = VpnServer(**payload.model_dump())
    session.add(server)
    await record_audit(session, actor_id=user.id, action="vpn_server.create", subject=payload.name)
    await session.commit()
    await session.refresh(server)
    return server


@router.get("/clients", response_model=list[ClientResponse])
async def list_clients(_: User = operator, session: AsyncSession = Depends(get_db_session)) -> list[VpnClient]:
    return list((await session.scalars(select(VpnClient).order_by(VpnClient.name))).all())


@router.post("/clients", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(payload: ClientCreate, user: User = operator, session: AsyncSession = Depends(get_db_session)) -> VpnClient:
    if await session.get(VpnServer, payload.server_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="VPN server not found")
    client = VpnClient(**payload.model_dump())
    session.add(client)
    await record_audit(session, actor_id=user.id, action="vpn_client.create", subject=payload.name)
    await session.commit()
    await session.refresh(client)
    return client


@router.post("/clients/{client_id}/disable", response_model=ClientResponse)
async def disable_client(client_id: UUID, user: User = operator, session: AsyncSession = Depends(get_db_session)) -> VpnClient:
    client = await session.get(VpnClient, client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="VPN client not found")
    client.disabled_at = datetime.now(UTC)
    await record_audit(session, actor_id=user.id, action="vpn_client.disable", subject=str(client.id))
    await session.commit()
    await session.refresh(client)
    return client
