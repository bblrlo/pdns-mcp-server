# pdns-mcp-server

MCP server for PowerDNS DNS record management via PowerDNS-Admin API.

## Структура проекта

```
src/pdns_mcp_server/
  __init__.py
  config.py      — Конфигурация (pydantic-settings)
  client.py      — HTTP-клиент для PowerDNS-Admin API
  tools.py       — MCP инструменты для управления DNS записями
  main.py        — Точка входа FastMCP сервера
tests/
  __init__.py
  test_config.py — Тесты конфигурации
  test_client.py — Тесты API-клиента (respx моки)
  test_tools.py  — Тесты MCP инструментов
  test_main.py   — Тесты точки входа
docs/
  README.md      — Этот файл
  usage.md       — Примеры запуска и использования
```

## Конфигурация

Переменные окружения (префикс `PDNS_`):

| Переменная | По умолчанию | Описание |
|---|---|---|
| `PDNS_ADMIN_URL` | — | URL PowerDNS-Admin (обязательно) |
| `PDNS_API_KEY` | — | API-ключ для X-API-Key аутентификации (обязательно) |
| `PDNS_SERVER_ID` | `localhost` | ID сервера PowerDNS |
| `PDNS_PORT` | `8000` | Порт MCP сервера |

## Инструменты MCP

- `list_zones` — список всех DNS зон
- `get_zone(zone_id)` — информация о зоне с записями
- `create_record(zone_id, name, type, content, ttl)` — создать/заменить RRset
- `update_record(zone_id, name, type, content, ttl)` — обновить запись
- `delete_record(zone_id, name, type)` — удалить RRset