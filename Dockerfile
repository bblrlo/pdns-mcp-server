FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src/ src/

ENV PYTHONPATH=/app/src
EXPOSE 8000

CMD ["uv", "run", "--no-sync", "python", "-m", "pdns_mcp_server.main"]