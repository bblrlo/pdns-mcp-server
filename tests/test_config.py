import os

import pytest

from pdns_mcp_server.config import PdnsConfig


@pytest.fixture(autouse=True)
def clear_env():
    keys = [k for k in os.environ if k.startswith("PDNS_")]
    for k in keys:
        del os.environ[k]
    yield
    keys = [k for k in os.environ if k.startswith("PDNS_")]
    for k in keys:
        del os.environ[k]


def test_defaults():
    os.environ["PDNS_ADMIN_URL"] = "http://pdns.example.com:9191"
    os.environ["PDNS_API_KEY"] = "test-api-key-123"
    config = PdnsConfig.from_env()
    assert config.pdns_admin_url == "http://pdns.example.com:9191"
    assert config.pdns_api_key == "test-api-key-123"
    assert config.pdns_server_id == "localhost"
    assert config.port == 8000


def test_custom_server_id():
    os.environ["PDNS_ADMIN_URL"] = "http://pdns.example.com:9191"
    os.environ["PDNS_API_KEY"] = "test-api-key-123"
    os.environ["PDNS_SERVER_ID"] = "myserver"
    config = PdnsConfig.from_env()
    assert config.pdns_server_id == "myserver"


def test_custom_port():
    os.environ["PDNS_ADMIN_URL"] = "http://pdns.example.com:9191"
    os.environ["PDNS_API_KEY"] = "test-api-key-123"
    os.environ["PDNS_PORT"] = "9090"
    config = PdnsConfig.from_env()
    assert config.port == 9090


def test_missing_url():
    os.environ["PDNS_API_KEY"] = "test-api-key-123"
    with pytest.raises(ValueError, match="PDNS_ADMIN_URL is required"):
        PdnsConfig.from_env()


def test_missing_api_key():
    os.environ["PDNS_ADMIN_URL"] = "http://pdns.example.com:9191"
    with pytest.raises(ValueError, match="PDNS_API_KEY is required"):
        PdnsConfig.from_env()