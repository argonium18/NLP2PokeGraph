# app/domain/model/article.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Article:
    source: str            # "smogon" / "victoryroad"
    url: str
    raw_html: str
    title: Optional[str] = None
