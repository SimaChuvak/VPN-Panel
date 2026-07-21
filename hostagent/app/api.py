from fastapi import APIRouter, Depends

from app.security import require_backend

router = APIRouter(dependencies=[Depends(require_backend)])


@router.get("/status")
async def status() -> dict[str, object]:
    """Expose only the minimum infrastructure status required by Backend."""
    return {"status": "ok", "vpn_services": []}
