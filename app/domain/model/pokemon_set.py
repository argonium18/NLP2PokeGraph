# domain/model/pokemon_set.py
from typing import List, Optional

class PokemonSet:
    def __init__(
        self,
        name: str,
        moves: List[str],
        nature: Optional[str] = None,
        ability: Optional[str] = None,
        item: Optional[str] = None,
        evs: Optional[dict] = None,
        role: Optional[str] = None,
        raw: Optional[dict] = None,
    ):
        self.name = name
        self.moves = moves
        self.nature = nature
        self.ability = ability
        self.item = item
        self.evs = evs
        self.role = role
        self.raw = raw
