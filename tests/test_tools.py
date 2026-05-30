from __future__ import annotations

import httpx
import pytest
import respx

from pdns_mcp_server.client import PdnsClient
from pdns_mcp_server.config import PdnsConfig
from pdns_mcp_server.tools import (
    _create_record,
    _delete_record,
    _get_zone,
    _list_zones,
    _update_record,
)


@pytest.fixture
def config() -> PdnsConfig:
    return PdnsConfig(
        pdns_admin_url="http://pdns.example.com:9191",
        pdns_api_key="test-key",
    )


@pytest.fixture
def client(config: PdnsConfig) -> PdnsClient:
    return PdnsClient(config)


@pytest.fixture(autouse=True)
def mock_httpx():
    with respx.mock:
        yield


class TestListZones:
    async def test_returns_formatted_list(self, client: PdnsClient) -> None:
        respx.get(
            "http://pdns.example.com:9191/api/v1/servers/localhost/zones"
        ).mock(
            return_value=httpx.Response(
                200,
                json=[
                    {"name": "example.com.", "kind": "Native"},
                    {"name": "test.org.", "kind": "Master"},
                ],
            )
        )

        result = await _list_zones(client)
        assert "- example.com. (kind=Native)" in result
        assert "- test.org. (kind=Master)" in result

    async def test_no_zones(self, client: PdnsClient) -> None:
        respx.get(
            "http://pdns.example.com:9191/api/v1/servers/localhost/zones"
        ).mock(return_value=httpx.Response(200, json=[]))

        result = await _list_zones(client)
        assert result == "No zones found."


class TestGetZone:
    async def test_returns_formatted_zone(self, client: PdnsClient) -> None:
        respx.get(
            "http://pdns.example.com:9191/api/v1/servers/localhost/zones/example.com.",
            params={"rrsets": "true"},
        ).mock(
            return_value=httpx.Response(
                200,
                json={
                    "name": "example.com.",
                    "kind": "Native",
                    "serial": 2024010100,
                    "rrsets": [
                        {
                            "name": "www.example.com.",
                            "type": "A",
                            "ttl": 3600,
                            "records": [{"content": "192.0.2.1", "disabled": False}],
                        }
                    ],
                },
            )
        )

        result = await _get_zone(client, "example.com")
        assert "Zone: example.com." in result
        assert "www.example.com. 3600 A 192.0.2.1" in result


class TestCreateRecord:
    async def test_creates_and_returns_message(self, client: PdnsClient) -> None:
        route = respx.patch(
            "http://pdns.example.com:9191/api/v1/servers/localhost/zones/example.com."
        ).mock(return_value=httpx.Response(204))

        result = await _create_record(
            client, "example.com", "www.example.com", "A", "192.0.2.10", 7200
        )
        assert result == "Record created: www.example.com 7200 A 192.0.2.10"
        body = route.calls[0].request.content
        import json

        payload = json.loads(body)
        assert payload["rrsets"][0]["name"] == "www.example.com."
        assert payload["rrsets"][0]["type"] == "A"


class TestUpdateRecord:
    async def test_updates_and_returns_message(self, client: PdnsClient) -> None:
        route = respx.patch(
            "http://pdns.example.com:9191/api/v1/servers/localhost/zones/example.com."
        ).mock(return_value=httpx.Response(204))

        result = await _update_record(
            client, "example.com", "www.example.com", "A", "192.0.2.20"
        )
        assert result == "Record updated: www.example.com 3600 A 192.0.2.20"
        import json

        payload = json.loads(route.calls[0].request.content)
        assert payload["rrsets"][0]["changetype"] == "REPLACE"


class TestDeleteRecord:
    async def test_deletes_and_returns_message(self, client: PdnsClient) -> None:
        route = respx.patch(
            "http://pdns.example.com:9191/api/v1/servers/localhost/zones/example.com."
        ).mock(return_value=httpx.Response(204))

        result = await _delete_record(client, "example.com", "www.example.com", "A")
        assert result == "Record deleted: www.example.com A"
        import json

        payload = json.loads(route.calls[0].request.content)
        assert payload["rrsets"][0]["changetype"] == "DELETE"