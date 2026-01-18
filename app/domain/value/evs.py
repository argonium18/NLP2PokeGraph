# domain/model/evs.py
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Evs:
    hp: Optional[int] = None
    atk: Optional[int] = None
    def_: Optional[int] = None
    spa: Optional[int] = None
    spd: Optional[int] = None
    spe: Optional[int] = None
