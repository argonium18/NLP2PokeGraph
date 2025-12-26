from dataclasses import dataclass
from typing import Optional

@dataclass
class SmogonSection:
    kind: str              # overview / comments / set
    tier: str
    set_name: Optional[str]
    html: str
