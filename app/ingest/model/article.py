from dataclasses import dataclass
from typing import List
from app.ingest.model.smogon_section import SmogonSection


@dataclass
class Article:
    """
    ingest が返す「1記事」単位のデータ
    """
    source: str              # "smogon", "victoryroad" など
    title: str               # "Abomasnow"
    sections: List[SmogonSection]
