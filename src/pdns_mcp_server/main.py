from __future__ import annotations

from pdns_mcp_server.config import PdnsConfig
from pdns_mcp_server.tools import create_app


def main() -> None:
    config = PdnsConfig.from_env()
    mcp = create_app(config=config)
    mcp.run(transport="streamable-http", host="0.0.0.0", port=config.port)


if __name__ == "__main__":
    main()