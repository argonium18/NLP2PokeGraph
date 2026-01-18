# domain/model/pokemon_set.py
from dataclasses import dataclass
from typing import List, Optional, Any
from app.domain.value.evs import Evs
from dataclasses import field

@dataclass(frozen=True)
class PokemonSet:
    pokemon_name: str
    set_name: str
    moves: list[Any]                 # str | list[str]
    nature: Optional[str] = None
    ability: list[str] = field(default_factory=list)
    item: list[str] = field(default_factory=list)
    evs: Optional[Evs] = None
    role: Optional[str] = None
