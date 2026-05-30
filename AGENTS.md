# AGENTS.md — pdns-mcp-server

MCP-сервер для управления DNS записями PowerDNS через API PowerDNS-Admin.

## Стек

- **Python 3.12+**
- **uv** — менеджер проектов и зависимостей
- **mcp (FastMCP)** — SDK для создания MCP сервера
- **httpx** — асинхронный HTTP-клиент
- **pytest + pytest-asyncio + respx** — тестирование

## Структура

```
src/pdns_mcp_server/
  config.py    — PdnsConfig (dataclass, from_env фабрика)
  client.py    — PdnsClient (async HTTP-клиент к PowerDNS-Admin API)
  tools.py     — create_app(): регистрация MCP инструментов
  main.py      — точка входа: FastMCP + streamable-http
tests/
  test_config.py   — тесты конфигурации
  test_client.py   — тесты API-клиента (respx моки)
  test_tools.py    — тесты MCP инструментов
  test_main.py     — тесты точки входа
docs/
  README.md    — обзор, конфигурация, инструменты, запуск
  usage.md     — примеры вызова каждого инструмента
```

## Запуск

```bash
uv run pdns-mcp-server
# требуется PDNS_ADMIN_URL и PDNS_API_KEY в окружении
```

## Тестирование

```bash
uv run pytest -v              # все тесты
uv run pytest tests/test_X.py # конкретный файл
```

## Инструменты MCP

| Инструмент | Назначение |
|---|---|
| `list_zones` | Список всех DNS зон |
| `get_zone` | Детали зоны с записями |
| `create_record` | Создать/заменить RRset в зоне |
| `update_record` | Обновить содержимое записи |
| `delete_record` | Удалить RRset |

## Конвенции

- Все запросы к PowerDNS через X-API-Key аутентификацию
- zone_id нормализуется (добавляется точка в конце)
- Инструменты возвращают форматированный текст (строки)
- При изменении API-клиента или инструментов — обновлять docs/
- Перед commit: `uv run pytest -v` — все тесты должны проходить