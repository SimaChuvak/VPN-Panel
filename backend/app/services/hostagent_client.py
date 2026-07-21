import httpx

from app.core.config import settings


class HostAgentClient:
    async def get_status(self) -> dict[str, object]:
        async with httpx.AsyncClient(base_url=settings.hostagent_url, timeout=5.0) as client:
            response = await client.get(
                "/internal/v1/status",
                headers={"X-Hostagent-Token": settings.hostagent_token},
            )
            response.raise_for_status()
            return response.json()
