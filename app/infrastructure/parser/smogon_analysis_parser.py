from typing import List, Dict
from app.domain.value.smogon_section import SmogonSection


class SmogonAnalysisParser:
    """
    Smogon JSON（単一ポケモン用）を SmogonSection に変換するパーサー
    """

    def parse(self, data: Dict) -> List[SmogonSection]:
        sections: List[SmogonSection] = []

        # 1. overview / comments をトップレベルから追加
        for field in ("overview", "comments"):
            html = data.get(field)
            if html:
                sections.append(
                    SmogonSection(
                        kind=field,
                        tier=None,       # overview はセットではないので None
                        set_name=None,
                        html=html,
                    )
                )

        # 2. sets を処理
        sets_data = data.get("sets", {})
        for set_name, set_info in sets_data.items():
            html = set_info.get("description")
            if html:
                sections.append(
                    SmogonSection(
                        kind="set",
                        tier=None,      # tier 情報があればここに入れる
                        set_name=set_name,
                        html=html,
                    )
                )

        return sections


# Smogon JSONのフォーマット
# {
#     "overview": "...",
#     "comments": "...",
#     "sets": {
#         "Utility": {"description": "..."},
#         "Calm Mind": {"description": "..."},
#         ...
#     },
#     "credits": {...}
# }
