import os
from dataclasses import dataclass


@dataclass(frozen=True)
class PdnsConfig:
    pdns_admin_url: str
    pdns_api_key: str
    pdns_server_id: str = "localhost"
    port: int = 8000

    @classmethod
    def from_env(cls) -> "PdnsConfig":
        pdns_admin_url = os.environ.get("PDNS_ADMIN_URL")
        pdns_api_key = os.environ.get("PDNS_API_KEY")
        pdns_server_id = os.environ.get("PDNS_SERVER_ID", "localhost")
        port_str = os.environ.get("PDNS_PORT", "8000")

        if not pdns_admin_url:
            raise ValueError("PDNS_ADMIN_URL is required")
        if not pdns_api_key:
            raise ValueError("PDNS_API_KEY is required")

        return cls(
            pdns_admin_url=pdns_admin_url,
            pdns_api_key=pdns_api_key,
            pdns_server_id=pdns_server_id,
            port=int(port_str),
        )