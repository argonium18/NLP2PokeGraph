from typing import List
from app.domain.value.smogon_section import SmogonSection


class SmogonAnalysisParser:
    def parse(
        self,
        data: dict,
        pokemon_name: str
    ) -> List[SmogonSection]:

        if pokemon_name not in data:
            raise KeyError(f"{pokemon_name} not found")

        sections: List[SmogonSection] = []
        mon_data = data[pokemon_name]

        for tier, tier_data in mon_data.items():
            sections.extend(self._parse_overview(tier, tier_data))
            sections.extend(self._parse_sets(tier, tier_data))

        return sections

    def _parse_overview(self, tier: str, tier_data: dict):
        result = []
        for field in ("overview", "comments"):
            html = tier_data.get(field)
            if html:
                result.append(
                    SmogonSection(
                        kind=field,
                        tier=tier,
                        set_name=None,
                        html=html,
                    )
                )
        return result

    def _parse_sets(self, tier: str, tier_data: dict):
        result = []
        for set_name, set_data in tier_data.get("sets", {}).items():
            html = set_data.get("description")
            if html:
                result.append(
                    SmogonSection(
                        kind="set",
                        tier=tier,
                        set_name=set_name,
                        html=html,
                    )
                )
        return result
