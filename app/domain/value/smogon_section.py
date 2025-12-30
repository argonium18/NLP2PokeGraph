from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class SmogonSection:
    kind: str              # overview / comments / set
    tier: str              # monotype / ou / etc
    set_name: Optional[str]
    html: str              # raw HTML
