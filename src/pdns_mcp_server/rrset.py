from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RRset:
    name: str
    type: str
    changetype: str
    ttl: int | None = None
    content: str | None = None

    def __post_init__(self) -> None:
        self.name = self.name if self.name.endswith(".") else f"{self.name}."
        self.type = self.type.upper()

    def to_dict(self) -> dict:
        d: dict = {
            "name": self.name,
            "type": self.type,
            "changetype": self.changetype,
        }
        if self.changetype == "REPLACE":
            d["ttl"] = self.ttl if self.ttl is not None else 3600
            d["records"] = [{"content": self.content, "disabled": False}]
        return d
