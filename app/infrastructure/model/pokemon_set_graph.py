# infrastructure/model/pokemon_set_graph.py
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass(frozen=True)
class MoveGraph:
    name: str
    slot: int
    candidate: bool

@dataclass(frozen=True)
class PokemonSetGraph:
    set_id: str
    pokemon_name: str
    set_name: str
    nature: Optional[str]
    role: Optional[str]

    hp: Optional[int]
    atk: Optional[int]
    def_: Optional[int]
    spa: Optional[int]
    spd: Optional[int]
    spe: Optional[int]

    moves: List[MoveGraph]
    items: List[str]
    abilities: List[str]
