FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src/ src/

ENV PYTHONPATH=/app/src
EXPOSE 8000

CMD ["uv", "run", "python", "-m", "pdns_mcp_server.main"]