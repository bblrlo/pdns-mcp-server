from __future__ import annotations

import pytest

from pdns_mcp_server.client import PdnsClient
from pdns_mcp_server.config import PdnsConfig
from pdns_mcp_server.tools import create_app


@pytest.fixture
def mock_client() -> PdnsClient:
    return PdnsClient(
        PdnsConfig(
            pdns_admin_url="http://pdns.example.com:9191",
            pdns_api_key="test-key",
        )
    )


def test_main_creates_app(mock_client: PdnsClient):
    mcp = create_app(client=mock_client)
    assert mcp.name == "pdns-mcp-server"


@pytest.mark.asyncio
async def test_app_has_all_tools(mock_client: PdnsClient):
    mcp = create_app(client=mock_client)
    tools = {t.name for t in await mcp.list_tools()}
    expected = {
        "list_zones",
        "get_zone",
        "create_record",
        "update_record",
        "delete_record",
    }
    assert tools == expected