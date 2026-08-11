import httpx

from src.config import settings


class ServiceNowClient:
    def __init__(self) -> None:
        self._base_url = settings.servicenow.instance_url
        self._auth = (settings.servicenow.username, settings.servicenow.password)
        self._client = httpx.AsyncClient(base_url=self._base_url, auth=self._auth)

    async def get_ticket(self, sys_id: str) -> dict:
        response = await self._client.get(f"/api/now/table/incident/{sys_id}")
        response.raise_for_status()
        return response.json()["result"]

    async def update_ticket(self, sys_id: str, fields: dict) -> dict:
        response = await self._client.patch(
            f"/api/now/table/incident/{sys_id}",
            json=fields,
        )
        response.raise_for_status()
        return response.json()["result"]

    async def close(self) -> None:
        await self._client.aclose()


_servicenow_client: ServiceNowClient | None = None


def get_servicenow_client() -> ServiceNowClient:
    global _servicenow_client
    if _servicenow_client is None:
        _servicenow_client = ServiceNowClient()
    return _servicenow_client