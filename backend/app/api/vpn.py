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
from app.services.hostagent_client import HostAgentClient

router = APIRouter(prefix="/vpn", tags=["vpn"])
operator = Depends(require_roles("administrator", "operator"))
hostagent = HostAgentClient()


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


# HostAgent monitoring endpoints
@router.get("/monitoring/resources")
async def get_resources(_: User = operator) -> dict:
    """Получение системных метрик (CPU, RAM, Disk, Swap, uptime)"""
    try:
        return await hostagent.get_resources()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.get("/monitoring/vpn-clients")
async def get_vpn_clients_real(_: User = operator) -> dict:
    """Получение списка VPN клиентов из HostAgent"""
    try:
        return await hostagent.get_vpn_clients()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.get("/monitoring/vpn-traffic")
async def get_vpn_traffic_real(_: User = operator) -> dict:
    """Получение статистики трафика из HostAgent"""
    try:
        return await hostagent.get_vpn_traffic()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.get("/monitoring/vpn-stats")
async def get_vpn_stats_real(_: User = operator) -> str:
    """Получение статистики VPN (raw text) из HostAgent"""
    try:
        return await hostagent.get_vpn_stats()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.get("/monitoring/docker-containers")
async def get_docker_containers(_: User = operator) -> list[dict]:
    """Получение списка Docker контейнеров из HostAgent"""
    try:
        return await hostagent.get_docker_containers()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.post("/vpn/block-ip")
async def block_ip_endpoint(ip: str, user: User = operator) -> dict:
    """Блокировка IP адреса через HostAgent"""
    try:
        result = await hostagent.block_ip(ip)
        await record_audit(None, actor_id=user.id, action="vpn.block_ip", subject=ip)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.post("/vpn/unblock-ip")
async def unblock_ip_endpoint(ip: str, user: User = operator) -> dict:
    """Разблокировка IP адреса через HostAgent"""
    try:
        result = await hostagent.unblock_ip(ip)
        await record_audit(None, actor_id=user.id, action="vpn.unblock_ip", subject=ip)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.get("/vpn/blocked-ips")
async def get_blocked_ips(_: User = operator) -> dict:
    """Получение списка заблокированных IP из HostAgent"""
    try:
        return await hostagent.get_vpn_blocked()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.post("/docker/restart-container")
async def restart_docker_container(container_name: str, user: User = operator) -> dict:
    """Перезапуск Docker контейнера через HostAgent"""
    try:
        result = await hostagent.restart_docker_container(container_name)
        await record_audit(None, actor_id=user.id, action="docker.restart", subject=container_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
