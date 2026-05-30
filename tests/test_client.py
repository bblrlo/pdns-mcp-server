from __future__ import annotations

import httpx
import pytest
import respx

from pdns_mcp_server.client import PdnsClient
from pdns_mcp_server.config import PdnsConfig


@pytest.fixture
def config() -> PdnsConfig:
    return PdnsConfig(
        pdns_admin_url="http://pdns.example.com:9191",
        pdns_api_key="test-key",
        pdns_server_id="localhost",
    )


@pytest.fixture
def client(config: PdnsConfig) -> PdnsClient:
    return PdnsClient(config)


@pytest.fixture(autouse=True)
def mock_httpx():
    with respx.mock:
        yield


class TestListZones:
    async def test_success(self, client: PdnsClient) -> None:
        route = respx.get(
            "http://pdns.example.com:9191/api/v1/servers/localhost/zones"
        ).mock(
            return_value=httpx.Response(
                200,
                json=[
                    {"id": "example.com.", "name": "example.com.", "kind": "Native"},
                    {"id": "test.org.", "name": "test.org.", "kind": "Master"},
                ],
            )
        )

        zones = await client.list_zones()
        assert route.called
        assert len(zones) == 2
        assert zones[0]["name"] == "example.com."

    async def test_auth_error(self, client: PdnsClient) -> None:
        respx.get(
            "http://pdns.example.com:9191/api/v1/servers/localhost/zones"
        ).mock(return_value=httpx.Response(401, text="Unauthorized"))

        with pytest.raises(httpx.HTTPStatusError):
            await client.list_zones()

    async def test_server_error(self, client: PdnsClient) -> None:
        respx.get(
            "http://pdns.example.com:9191/api/v1/servers/localhost/zones"
        ).mock(return_value=httpx.Response(500, text="Internal Server Error"))

        with pytest.raises(httpx.HTTPStatusError):
            await client.list_zones()


class TestGetZone:
    async def test_success(self, client: PdnsClient) -> None:
        zone_data = {
            "id": "example.com.",
            "name": "example.com.",
            "kind": "Native",
            "rrsets": [
                {
                    "name": "example.com.",
                    "type": "A",
                    "ttl": 3600,
                    "records": [{"content": "192.0.2.1", "disabled": False}],
                }
            ],
        }
        route = respx.get(
            "http://pdns.example.com:9191/api/v1/servers/localhost/zones/example.com.",
            params={"rrsets": "true"},
        ).mock(return_value=httpx.Response(200, json=zone_data))

        zone = await client.get_zone("example.com.")
        assert route.called
        assert zone["name"] == "example.com."
        assert len(zone["rrsets"]) == 1

    async def test_zone_not_found(self, client: PdnsClient) -> None:
        respx.get(
            "http://pdns.example.com:9191/api/v1/servers/localhost/zones/nonexistent.com.",
            params={"rrsets": "true"},
        ).mock(return_value=httpx.Response(404, text="Not Found"))

        with pytest.raises(httpx.HTTPStatusError):
            await client.get_zone("nonexistent.com.")

    async def test_normalizes_trailing_dot(self, client: PdnsClient) -> None:
        route = respx.get(
            "http://pdns.example.com:9191/api/v1/servers/localhost/zones/example.com.",
            params={"rrsets": "true"},
        ).mock(return_value=httpx.Response(200, json={"name": "example.com."}))

        await client.get_zone("example.com")
        assert route.called


class TestPatchZone:
    async def test_success(self, client: PdnsClient) -> None:
        rrsets = [
            {
                "name": "www.example.com.",
                "type": "A",
                "ttl": 3600,
                "changetype": "REPLACE",
                "records": [{"content": "192.0.2.10", "disabled": False}],
            }
        ]
        route = respx.patch(
            "http://pdns.example.com:9191/api/v1/servers/localhost/zones/example.com."
        ).mock(return_value=httpx.Response(204))

        await client.patch_zone("example.com", rrsets)
        assert route.called
        import json
        body = json.loads(route.calls[0].request.content)
        assert body == {"rrsets": rrsets}

    async def test_bad_request(self, client: PdnsClient) -> None:
        respx.patch(
            "http://pdns.example.com:9191/api/v1/servers/localhost/zones/example.com."
        ).mock(return_value=httpx.Response(422, text="Unprocessable"))

        with pytest.raises(httpx.HTTPStatusError):
            await client.patch_zone("example.com", [])