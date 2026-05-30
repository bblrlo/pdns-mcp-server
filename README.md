# pdns-mcp-server

MCP-сервер для управления DNS записями PowerDNS через API PowerDNS-Admin.

## Архитектура

```
src/pdns_mcp_server/
  config.py    — PdnsConfig: чтение конфигурации из переменных окружения
  client.py    — PdnsClient: async HTTP-клиент для PowerDNS-Admin API
  tools.py     — create_app(): регистрация MCP инструментов
  main.py      — точка входа, запуск streamable-http сервера
tests/
  test_config.py   — тесты конфигурации
  test_client.py   — тесты API-клиента (respx моки)
  test_tools.py    — тесты MCP инструментов
  test_main.py     — тесты точки входа
```

## Конфигурация

| Переменная | Обязательно | По умолчанию | Описание |
|---|---|---|---|
| `PDNS_ADMIN_URL` | Да | — | URL PowerDNS-Admin (например `http://pda.example.com:9191`) |
| `PDNS_API_KEY` | Да | — | API-ключ для X-API-Key аутентификации |
| `PDNS_SERVER_ID` | Нет | `localhost` | ID сервера PowerDNS |
| `PDNS_PORT` | Нет | `8000` | Порт MCP сервера |

## Инструменты MCP

| Инструмент | Описание |
|---|---|
| `list_zones` | Список всех DNS зон |
| `get_zone` | Детали зоны с записями |
| `create_record` | Создать/заменить RRset в зоне |
| `update_record` | Обновить содержимое записи |
| `delete_record` | Удалить RRset |

Подробные параметры и примеры — в [docs/usage.md](docs/usage.md).

## Запуск

```bash
export PDNS_ADMIN_URL=http://pda.example.com:9191
export PDNS_API_KEY=your-api-key-here
uv run pdns-mcp-server
```

Сервер будет доступен на `http://0.0.0.0:8000` (streamable-http транспорт).

### Docker

```bash
export PDNS_ADMIN_URL=http://pda.example.com:9191
export PDNS_API_KEY=your-api-key-here
docker compose up
```

## Тестирование

```bash
uv run pytest -v
```

Все тесты используют `respx` для мокирования HTTP-вызовов — не требуют реального PowerDNS.