import re
from app.domain.value.smogon_section import SmogonSection


def normalize_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


class SmogonNormalizeService:
    def normalize(
        self,
        sections: list[SmogonSection],
        masters: dict,
        pokemon_name: str,   # <- 追加
    ) -> list[dict]:

        pokedex = masters["pokedex"]
        moves_master = masters["moves"]
        abilities_master = masters["abilities"]
        items_master = masters["items"]

        normalized: list[dict] = []

        for section in sections:
            normalized_section = self._normalize_section(
                section,
                pokemon_name,          # <- 追加
                pokedex,
                moves_master,
                abilities_master,
                items_master,
            )
            if normalized_section:
                normalized.append(normalized_section)

        return normalized

    # -------------------------
    # section 単位の正規化
    # -------------------------
    def _normalize_section(
        self,
        pokemon_name: str,      # <- 追加
        section: SmogonSection,
        pokedex: dict,
        moves_master: dict,
        abilities_master: dict,
        items_master: dict,
    ) -> dict | None:

        dex_key = normalize_key(pokemon_name)
        dex_entry = pokedex.get(dex_key)
        if not dex_entry:
            return None

        return {
            "pokemon_id": dex_entry["num"],
            "name": dex_entry["name"],
            "types": dex_entry["types"],

            "tier": section.tier,
            "kind": section.kind,
            "set_name": section.set_name,

            # html はこの段階ではそのまま
            "html": section.html,
        }

    # --------------- 旧API（将来用） ---------------
    def _normalize_list(self, names: list[str], master: dict) -> list[str]:
        result = []
        for name in names:
            key = normalize_key(name)
            if key in master:
                result.append(master[key]["name"])
        return result

    def _normalize_single(self, name: str | None, master: dict) -> str | None:
        if not name:
            return None
        key = normalize_key(name)
        return master.get(key, {}).get("name")
