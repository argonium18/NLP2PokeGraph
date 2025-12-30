from dataclasses import dataclass
from typing import List
from app.domain.value.smogon_section import SmogonSection


@dataclass
class Article:

    source: str              # "smogon", "victoryroad" など
    title: str               # "Abomasnow"
    sections: List[SmogonSection]
