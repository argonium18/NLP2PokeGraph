# smogon_repository.py
from typing import List, Dict, Any
from app.domain.value.smogon_section import SmogonSection
from app.infrastructure.client.smogon_client import SmogonClient
from app.infrastructure.parser.smogon_analysis_parser import SmogonAnalysisParser

class SmogonRepository:
    DEFAULT_FORMAT_ID = "gen9ou"

    def __init__(self, client: SmogonClient, parser: SmogonAnalysisParser):
        self.client = client
        self.parser = parser

    # 既存: 記事取得
    def find_by_pokemon(self, pokemon_name: str) -> List[SmogonSection]:
        raw_data = self.client.fetch_analyses(self.DEFAULT_FORMAT_ID)
        pokemon_data = self._find_species(raw_data, pokemon_name)
        if not pokemon_data:
            return []
        return self.parser.parse(pokemon_data)

    # 新規追加: 攻略セット取得
    def find_sets_by_pokemon(self, pokemon_name: str) -> Dict[str, Any]:
        raw_sets = self.client.fetch_sets(self.DEFAULT_FORMAT_ID)
        pokemon_sets = self._find_species(raw_sets, pokemon_name)
        if not pokemon_sets:
            return {}
        return pokemon_sets  # あとで domain/PokemonSet に変換しても良い

    def _find_species(self, raw_data: dict, species: str) -> Any:
        """
        species 名で検索（正規化対応）
        """
        if species in raw_data:
            return raw_data[species]

        norm = self._normalize_name(species)
        for key in raw_data.keys():
            if self._normalize_name(key) == norm:
                return raw_data[key]
        return None

    @staticmethod
    def _normalize_name(name: str) -> str:
        n = name.strip().lower()
        n = n.replace(" ", "").replace(".", "").replace(":", "").replace("’", "'")
        return n
