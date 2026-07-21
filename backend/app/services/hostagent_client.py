import httpx

from app.core.config import settings


class HostAgentClient:
    def __init__(self):
        self.base_url = settings.hostagent_url
        self.api_key = settings.hostagent_token

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        """Выполняет запрос к HostAgent с аутентификацией"""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30.0) as client:
            response = await client.request(
                method,
                path,
                headers={"X-API-Key": self.api_key},
                **kwargs
            )
            response.raise_for_status()
            return response.json()

    async def ping(self) -> str:
        """Проверка доступности HostAgent"""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=5.0) as client:
            response = await client.get("/ping")
            return response.text

    async def get_resources(self) -> dict:
        """Получение системных метрик (CPU, RAM, Disk, Swap, uptime)"""
        return await self._request("GET", "/resources")

    async def get_vpn_clients(self) -> dict:
        """Получение списка VPN клиентов"""
        return await self._request("GET", "/vpn/clients")

    async def get_vpn_stats(self) -> str:
        """Получение статистики VPN (raw text)"""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30.0) as client:
            response = await client.get(
                "/vpn/stats",
                headers={"X-API-Key": self.api_key}
            )
            response.raise_for_status()
            return response.text

    async def get_vpn_traffic(self) -> dict:
        """Получение статистики трафика"""
        return await self._request("GET", "/vpn/traffic")

    async def get_vpn_config(self) -> str:
        """Получение конфигурации VPN"""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30.0) as client:
            response = await client.get(
                "/vpn/config",
                headers={"X-API-Key": self.api_key}
            )
            response.raise_for_status()
            return response.text

    async def block_ip(self, ip: str) -> dict:
        """Блокировка IP адреса"""
        return await self._request("POST", "/vpn/block", json={"ip": ip})

    async def unblock_ip(self, ip: str) -> dict:
        """Разблокировка IP адреса"""
        return await self._request("POST", "/vpn/unblock", json={"ip": ip})

    async def get_vpn_blocked(self) -> dict:
        """Получение списка заблокированных IP"""
        return await self._request("GET", "/vpn/blocked")

    async def get_docker_containers(self) -> list[dict]:
        """Получение списка Docker контейнеров"""
        return await self._request("GET", "/docker/containers")

    async def restart_docker_container(self, container_name: str) -> dict:
        """Перезапуск Docker контейнера"""
        return await self._request("POST", "/docker/restart", json={"container": container_name})

    async def get_fail2ban_status(self) -> dict:
        """Получение статуса Fail2Ban"""
        return await self._request("GET", "/fail2ban")

    async def get_fail2ban_bans(self) -> dict:
        """Получение списка заблокированных IP в Fail2Ban"""
        return await self._request("GET", "/fail2ban/bans")

    async def restart_fail2ban(self) -> dict:
        """Перезапуск Fail2Ban"""
        return await self._request("POST", "/fail2ban/restart")
