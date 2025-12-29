from dataclasses import dataclass

@dataclass
class Entity:
    name: str
    type: str  # "Pokemon" / "Move" / "Item"
