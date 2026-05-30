from __future__ import annotations

import uvicorn

from pdns_mcp_server.config import PdnsConfig
from pdns_mcp_server.tools import create_app


def main() -> None:
    config = PdnsConfig.from_env()
    mcp = create_app(config=config)
    app = mcp.streamable_http_app()
    uvicorn.run(app, host="0.0.0.0", port=config.port)


if __name__ == "__main__":
    main()