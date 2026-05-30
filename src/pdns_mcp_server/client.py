from __future__ import annotations

from typing import Any

import httpx

from pdns_mcp_server.config import PdnsConfig


class PdnsClient:
    def __init__(self, config: PdnsConfig) -> None:
        self._config = config
        self._client = httpx.AsyncClient(
            base_url=config.pdns_admin_url.rstrip("/"),
            headers={"X-API-Key": config.pdns_api_key},
            timeout=30,
        )

    @property
    def _server_base(self) -> str:
        return f"/api/v1/servers/{self._config.pdns_server_id}"

    async def list_zones(self) -> list[dict[str, Any]]:
        resp = await self._client.get(f"{self._server_base}/zones")
        resp.raise_for_status()
        return resp.json()

    async def get_zone(self, zone_id: str) -> dict[str, Any]:
        zone_id = zone_id.rstrip(".") + "."
        resp = await self._client.get(
            f"{self._server_base}/zones/{zone_id}",
            params={"rrsets": "true"},
        )
        resp.raise_for_status()
        return resp.json()

    async def patch_zone(
        self, zone_id: str, rrsets: list[dict[str, Any]]
    ) -> None:
        zone_id = zone_id.rstrip(".") + "."
        resp = await self._client.patch(
            f"{self._server_base}/zones/{zone_id}",
            json={"rrsets": rrsets},
        )
        resp.raise_for_status()

    async def close(self) -> None:
        await self._client.aclose()