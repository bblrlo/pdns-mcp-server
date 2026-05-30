# Использование pdns-mcp-server

## Примеры вызова инструментов

### list_zones

```json
{
  "name": "list_zones",
  "arguments": {}
}
```

Ответ:
```
- example.com. (kind=Native)
- test.org. (kind=Master)
```

### get_zone

```json
{
  "name": "get_zone",
  "arguments": {
    "zone_id": "example.com"
  }
}
```

Ответ:
```
Zone: example.com.
Kind: Native
Serial: 2024050100

Records:
  example.com. 3600 SOA ns1.example.com. admin.example.com. 2024050100 3600 900 604800 86400
  example.com. 3600 NS ns1.example.com.
  www.example.com. 3600 A 192.0.2.1
  mail.example.com. 3600 MX 10 mail.example.com.
```

### create_record

```json
{
  "name": "create_record",
  "arguments": {
    "zone_id": "example.com",
    "name": "www.example.com",
    "type": "A",
    "content": "192.0.2.10",
    "ttl": 7200
  }
}
```

Ответ:
```
Record created: www.example.com 7200 A 192.0.2.10
```

### update_record

```json
{
  "name": "update_record",
  "arguments": {
    "zone_id": "example.com",
    "name": "www.example.com",
    "type": "A",
    "content": "192.0.2.20",
    "ttl": 3600
  }
}
```

Ответ:
```
Record updated: www.example.com 3600 A 192.0.2.20
```

### delete_record

```json
{
  "name": "delete_record",
  "arguments": {
    "zone_id": "example.com",
    "name": "www.example.com",
    "type": "A"
  }
}
```

Ответ:
```
Record deleted: www.example.com A
```

## Запуск с .env файлом

Создайте `.env` в корне проекта:

```
PDNS_ADMIN_URL=http://pda.example.com:9191
PDNS_API_KEY=your-api-key-here
PDNS_SERVER_ID=localhost
PDNS_PORT=8000
```

Затем просто:

```bash
uv run pdns-mcp-server
```

## Интеграция с MCP-клиентом

Для подключения к серверу через streamable-http, клиент должен отправлять POST-запросы на эндпоинт `/mcp`:

```
POST http://localhost:8000/mcp
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "list_zones",
    "arguments": {}
  }
}
```

## Обработка ошибок

При отсутствии обязательных переменных окружения сервер завершится с сообщением:

```
ValueError: PDNS_ADMIN_URL is required
```

При ошибках API PowerDNS (401 Unauthorized, 404 Not Found и т.д.) инструмент вернёт HTTPError с описанием.