# AGENTS.md — pdns-mcp-server

MCP-сервер для управления DNS записями PowerDNS через API PowerDNS-Admin.

## Стек

- **Python 3.12+**
- **uv** — пакетный менеджер (uv.lock закоммичен)
- **mcp (FastMCP)** — MCP SDK, транспорт `streamable-http` (JSON-RPC POST на `/mcp`)
- **httpx** — async HTTP-клиент (таймаут 30 с)
- **pytest** (`asyncio_mode=auto` в pyproject.toml) + **respx** — моки HTTP

## Запуск

```bash
uv run pdns-mcp-server          # entrypoint из [project.scripts]
# требует PDNS_ADMIN_URL + PDNS_API_KEY в окружении
```

Docker: `docker compose up` (CMD внутри — `uv run --no-sync python -m pdns_mcp_server.main`).

## Тестирование

```bash
uv run pytest -v                     # все тесты (не требуют реального PowerDNS)
uv run pytest tests/test_X.py -v     # один файл
uv run pytest tests/ -k "test_name"  # один тест по имени
```

Тесты HTTP мокаются через `respx.mock` (autouse fixture во всех test_*.py).
`test_config.py` чистит `PDNS_*` переменные через autouse fixture — изолированно.

## Архитектура

```
src/pdns_mcp_server/
  config.py    — PdnsConfig (dataclass frozen, from_env читает os.environ)
  client.py    — PdnsClient (httpx.AsyncClient, X-API-Key в заголовке)
  tools.py     — create_app(): DI-фабрика, регистрирует @mcp.tool()
  main.py      — main(): config → create_app() → uvicorn
tests/
  test_config.py — 5 тестов (значения по умолч., кастом, ошибки)
  test_client.py — 8 тестов (respx на client.list_zones/get_zone/patch_zone)
  test_tools.py  — 6 тестов (вызывают _list_zones, _get_zone и т.д. напрямую)
  test_main.py   — 2 теста (create_app, список инструментов)
```

## Инструменты MCP

`list_zones` | `get_zone(zone_id)` | `create_record(zone_id, name, type, content, ttl=3600)` | `update_record(zone_id, name, type, content, ttl=3600)` | `delete_record(zone_id, name, type)`

Все возвращают форматированную строку (не JSON). `FastMCP(json_response=True, stateless_http=True)`.

## Конвенции

- `create_app(config=None, client=None)` — опциональные params для тестовой подмены DI
- `zone_id` нормализуется: `rstrip(".") + "."` в `client.py:29,40`
- Все HTTP-запросы через X-API-Key (заголовок, не Bearer)
- Перед commit: `uv run pytest -v` — все тесты зелёные
- При изменении API или инструментов — обновлять `docs/`
- `graphify-out/` — сгенерированный граф, не трогать вручную