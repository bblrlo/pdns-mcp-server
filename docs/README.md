# pdns-mcp-server

MCP-сервер для управления DNS записями PowerDNS через API PowerDNS-Admin.

## Архитектура

```
src/pdns_mcp_server/
  __init__.py
  config.py    — PdnsConfig: чтение конфигурации из переменных окружения
  client.py    — PdnsClient: async HTTP-клиент для PowerDNS-Admin API
  tools.py     — create_app(): регистрация MCP инструментов
  main.py      — точка входа, запуск streamable-http сервера
tests/
  __init__.py
  test_config.py   — 5 тестов конфигурации
  test_client.py   — 8 тестов API-клиента (respx моки)
  test_tools.py    — 6 тестов инструментов
  test_main.py     — 2 теста точки входа
```

## Конфигурация

Переменные окружения:

| Переменная | Обязательно | По умолчанию | Описание |
|---|---|---|---|
| `PDNS_ADMIN_URL` | Да | — | URL PowerDNS-Admin (например `http://pda.example.com:9191`) |
| `PDNS_API_KEY` | Да | — | API-ключ для X-API-Key аутентификации |
| `PDNS_SERVER_ID` | Нет | `localhost` | ID сервера PowerDNS |
| `PDNS_PORT` | Нет | `8000` | Порт MCP сервера |

## Инструменты MCP

### list_zones
Список всех DNS зон. Без аргументов.

### get_zone
Полная информация о зоне с ресурсными записями.

| Параметр | Тип | Описание |
|---|---|---|
| `zone_id` | `str` | Имя зоны (e.g. `example.com` или `example.com.`) |

### create_record
Создание или замена DNS записи в зоне.

| Параметр | Тип | По умолч. | Описание |
|---|---|---|---|
| `zone_id` | `str` | — | Имя зоны |
| `name` | `str` | — | Полное имя записи (e.g. `www.example.com`) |
| `type` | `str` | — | Тип записи: `A`, `AAAA`, `CNAME`, `MX`, `TXT`, etc. |
| `content` | `str` | — | Содержимое записи |
| `ttl` | `int` | `3600` | TTL в секундах |

### update_record
Обновление существующей записи. Параметры идентичны `create_record`.

### delete_record
Удаление всех записей с указанным именем и типом.

| Параметр | Тип | Описание |
|---|---|---|
| `zone_id` | `str` | Имя зоны |
| `name` | `str` | Полное имя записи для удаления |
| `type` | `str` | Тип записи |

## Запуск

```bash
# Установить переменные окружения
export PDNS_ADMIN_URL=http://pda.example.com:9191
export PDNS_API_KEY=your-api-key-here

# Запуск сервера
uv run pdns-mcp-server
```

Сервер будет доступен на `http://0.0.0.0:8000` с транспортом `streamable-http`.

## Тестирование

```bash
uv run pytest -v
```

Все тесты используют `respx` для мокирования HTTP-вызовов — не требуют реального PowerDNS.