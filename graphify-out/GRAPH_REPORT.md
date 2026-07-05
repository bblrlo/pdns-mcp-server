# Graph Report - .  (2026-07-05)

## Corpus Check
- Corpus is ~1,942 words - fits in a single context window. You may not need a graph.

## Summary
- 97 nodes · 179 edges · 18 communities (11 shown, 7 thin omitted)
- Extraction: 63% EXTRACTED · 37% INFERRED · 0% AMBIGUOUS · INFERRED: 67 edges (avg confidence: 0.79)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Project Conventions & Config|Project Conventions & Config]]
- [[_COMMUNITY_Core App & Tool Registration|Core App & Tool Registration]]
- [[_COMMUNITY_DNS Record CRUD|DNS Record CRUD]]
- [[_COMMUNITY_Client & Config Setup|Client & Config Setup]]
- [[_COMMUNITY_Config Validation Tests|Config Validation Tests]]
- [[_COMMUNITY_MCP Tool Descriptions|MCP Tool Descriptions]]
- [[_COMMUNITY_PowerDNS Admin API|PowerDNS Admin API]]
- [[_COMMUNITY_Auth & Docker Deployment|Auth & Docker Deployment]]
- [[_COMMUNITY_PdnsClient Zone API|PdnsClient Zone API]]
- [[_COMMUNITY_ListZones Tool & Tests|ListZones Tool & Tests]]
- [[_COMMUNITY_GetZone Tests|GetZone Tests]]
- [[_COMMUNITY_ListZones Error Tests|ListZones Error Tests]]
- [[_COMMUNITY_DeleteRecord Tool & Tests|DeleteRecord Tool & Tests]]
- [[_COMMUNITY_PatchZone Tests|PatchZone Tests]]
- [[_COMMUNITY_Package Init|Package Init]]

## God Nodes (most connected - your core abstractions)
1. `PdnsClient` - 41 edges
2. `pdns-mcp-server` - 29 edges
3. `PdnsConfig` - 18 edges
4. `create_app()` - 8 edges
5. `create_app()` - 7 edges
6. `TestListZones` - 6 edges
7. `TestGetZone` - 6 edges
8. `TestPatchZone` - 5 edges
9. `TestListZones` - 5 edges
10. `_list_zones()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `pdns-mcp-server` --references--> `PdnsConfig`  [INFERRED]
  README.md → AGENTS.md
- `pdns-mcp-server` --references--> `list_zones`  [INFERRED]
  README.md → AGENTS.md
- `pdns-mcp-server` --references--> `get_zone`  [INFERRED]
  README.md → AGENTS.md
- `pdns-mcp-server` --references--> `create_record`  [INFERRED]
  README.md → AGENTS.md
- `pdns-mcp-server` --references--> `update_record`  [INFERRED]
  README.md → AGENTS.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **MCP DNS Record Management Tools** — agents_list_zones, agents_get_zone, agents_create_record, agents_update_record, agents_delete_record [EXTRACTED 1.00]
- **Environment Configuration Variables** — readme_pdns_admin_url, readme_pdns_api_key, readme_pdns_server_id, readme_pdns_port [EXTRACTED 1.00]
- **Core Application Modules** — agents_pdnsconfig, agents_pdnsclient, agents_create_app, agents_main [EXTRACTED 1.00]

## Communities (18 total, 7 thin omitted)

### Community 0 - "Project Conventions & Config"
Cohesion: 0.13
Nodes (15): FastMCP, Formatted text output, httpx, main.py, pytest, Python 3.12+, respx, Update docs on API change (+7 more)

### Community 1 - "Core App & Tool Registration"
Cohesion: 0.23
Nodes (7): FastMCP, main(), create_app(), _update_record(), test_app_has_all_tools(), test_main_creates_app(), TestUpdateRecord

### Community 2 - "DNS Record CRUD"
Cohesion: 0.33
Nodes (5): PdnsClient, _create_record(), _get_zone(), TestCreateRecord, TestGetZone

### Community 3 - "Client & Config Setup"
Cohesion: 0.25
Nodes (6): PdnsConfig, client(), config(), mock_client(), client(), config()

### Community 4 - "Config Validation Tests"
Cohesion: 0.39
Nodes (5): test_custom_port(), test_custom_server_id(), test_defaults(), test_missing_api_key(), test_missing_url()

### Community 5 - "MCP Tool Descriptions"
Cohesion: 0.33
Nodes (6): create_app(), create_record, delete_record, get_zone, list_zones, update_record

### Community 6 - "PowerDNS Admin API"
Cohesion: 0.50
Nodes (4): PdnsClient, PdnsConfig, PDNS_ADMIN_URL, PowerDNS-Admin API

### Community 7 - "Auth & Docker Deployment"
Cohesion: 0.50
Nodes (3): X-API-Key authentication, pdns-mcp-server Docker service, PDNS_API_KEY

## Knowledge Gaps
- **14 isolated node(s):** `pdns-mcp-server`, `Python 3.12+`, `uv`, `FastMCP`, `httpx` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PdnsClient` connect `DNS Record CRUD` to `Core App & Tool Registration`, `Client & Config Setup`, `PdnsClient Zone API`, `ListZones Tool & Tests`, `GetZone Tests`, `ListZones Error Tests`, `DeleteRecord Tool & Tests`, `PatchZone Tests`?**
  _High betweenness centrality (0.243) - this node is a cross-community bridge._
- **Why does `pdns-mcp-server` connect `Project Conventions & Config` to `PowerDNS Admin API`, `MCP Tool Descriptions`, `Documentation Hub`, `Auth & Docker Deployment`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Why does `PdnsConfig` connect `Client & Config Setup` to `Core App & Tool Registration`, `DNS Record CRUD`, `Config Validation Tests`, `ListZones Tool & Tests`, `GetZone Tests`, `ListZones Error Tests`, `DeleteRecord Tool & Tests`, `PatchZone Tests`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `PdnsClient` (e.g. with `PdnsConfig` and `TestGetZone`) actually correct?**
  _`PdnsClient` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `pdns-mcp-server` (e.g. with `pdns-mcp-server Docker service` and `create_app()`) actually correct?**
  _`pdns-mcp-server` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `PdnsConfig` (e.g. with `PdnsClient` and `TestGetZone`) actually correct?**
  _`PdnsConfig` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `create_app()` (e.g. with `main()` and `test_app_has_all_tools()`) actually correct?**
  _`create_app()` has 3 INFERRED edges - model-reasoned connections that need verification._