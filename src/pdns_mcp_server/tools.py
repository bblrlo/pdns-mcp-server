from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from pdns_mcp_server.client import PdnsClient
from pdns_mcp_server.config import PdnsConfig
from pdns_mcp_server.rrset import RRset


async def _list_zones(client: PdnsClient) -> str:
    zones = await client.list_zones()
    lines = [f"- {z['name']} (kind={z.get('kind', '?')})" for z in zones]
    return "\n".join(lines) if lines else "No zones found."


async def _get_zone(client: PdnsClient, zone_id: str) -> str:
    zone = await client.get_zone(zone_id)
    lines = [
        f"Zone: {zone['name']}",
        f"Kind: {zone.get('kind', '?')}",
        f"Serial: {zone.get('serial', '?')}",
    ]
    rrsets = zone.get("rrsets", [])
    if rrsets:
        lines.append("")
        lines.append("Records:")
        for rr in rrsets:
            for rec in rr.get("records", []):
                disabled = " (disabled)" if rec.get("disabled") else ""
                lines.append(
                    f"  {rr['name']} {rr['ttl']} {rr['type']} {rec['content']}{disabled}"
                )
    else:
        lines.append("\nNo records found.")
    return "\n".join(lines)


async def _create_record(
    client: PdnsClient, zone_id: str, name: str, type: str, content: str, ttl: int = 3600
) -> str:
    rrset = RRset(name=name, type=type, ttl=ttl, content=content, changetype="REPLACE")
    await client.patch_zone(zone_id, [rrset.to_dict()])
    return f"Record created: {name} {ttl} {type.upper()} {content}"


async def _update_record(
    client: PdnsClient, zone_id: str, name: str, type: str, content: str, ttl: int = 3600
) -> str:
    rrset = RRset(name=name, type=type, ttl=ttl, content=content, changetype="REPLACE")
    await client.patch_zone(zone_id, [rrset.to_dict()])
    return f"Record updated: {name} {ttl} {type.upper()} {content}"


async def _delete_record(
    client: PdnsClient, zone_id: str, name: str, type: str
) -> str:
    rrset = RRset(name=name, type=type, changetype="DELETE")
    await client.patch_zone(zone_id, [rrset.to_dict()])
    return f"Record deleted: {name} {type.upper()}"


def create_app(config: PdnsConfig | None = None, client: PdnsClient | None = None) -> FastMCP:
    if client is None:
        if config is None:
            config = PdnsConfig.from_env()
        client = PdnsClient(config)

    mcp = FastMCP(
        "pdns-mcp-server",
        json_response=True,
        stateless_http=True,
    )

    @mcp.tool()
    async def list_zones() -> str:
        """List all DNS zones."""
        return await _list_zones(client)

    @mcp.tool()
    async def get_zone(zone_id: str) -> str:
        """Get full zone details including all resource records."""
        return await _get_zone(client, zone_id)

    @mcp.tool()
    async def create_record(
        zone_id: str, name: str, type: str, content: str, ttl: int = 3600
    ) -> str:
        """Create or replace a DNS record in a zone."""
        return await _create_record(client, zone_id, name, type, content, ttl)

    @mcp.tool()
    async def update_record(
        zone_id: str, name: str, type: str, content: str, ttl: int = 3600
    ) -> str:
        """Update an existing DNS record in a zone."""
        return await _update_record(client, zone_id, name, type, content, ttl)

    @mcp.tool()
    async def delete_record(zone_id: str, name: str, type: str) -> str:
        """Delete all DNS records with the given name and type from a zone."""
        return await _delete_record(client, zone_id, name, type)

    return mcp