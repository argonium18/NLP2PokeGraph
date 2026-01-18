from dataclasses import dataclass
from typing import Mapping, Any

@dataclass
class SmogonSetDTO:
    raw: Mapping[str, Any]

