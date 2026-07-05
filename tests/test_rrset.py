from __future__ import annotations

from pdns_mcp_server.rrset import RRset


class TestRRset:
    def test_replace_to_dict(self) -> None:
        rrset = RRset(name="www.example.com", type="A", ttl=7200, content="192.0.2.1", changetype="REPLACE")
        d = rrset.to_dict()
        assert d == {
            "name": "www.example.com.",
            "type": "A",
            "ttl": 7200,
            "changetype": "REPLACE",
            "records": [{"content": "192.0.2.1", "disabled": False}],
        }

    def test_delete_to_dict(self) -> None:
        rrset = RRset(name="www.example.com.", type="a", changetype="DELETE")
        d = rrset.to_dict()
        assert d == {
            "name": "www.example.com.",
            "type": "A",
            "changetype": "DELETE",
        }

    def test_normalises_name_trailing_dot(self) -> None:
        rrset = RRset(name="www.example.com", type="A", changetype="DELETE")
        assert rrset.name == "www.example.com."

    def test_preserves_existing_trailing_dot(self) -> None:
        rrset = RRset(name="www.example.com.", type="A", changetype="DELETE")
        assert rrset.name == "www.example.com."

    def test_uppercases_type(self) -> None:
        rrset = RRset(name="www.example.com", type="aaaa", changetype="DELETE")
        assert rrset.type == "AAAA"

    def test_default_ttl_is_3600_for_replace(self) -> None:
        rrset = RRset(name="x.com", type="A", content="1.2.3.4", changetype="REPLACE")
        assert rrset.to_dict()["ttl"] == 3600

    def test_no_ttl_no_records_for_delete(self) -> None:
        rrset = RRset(name="x.com", type="A", changetype="DELETE")
        d = rrset.to_dict()
        assert "ttl" not in d
        assert "records" not in d
