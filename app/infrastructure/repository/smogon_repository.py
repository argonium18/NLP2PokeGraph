from typing import List
from app.domain.value.smogon_section import SmogonSection
from app.infrastructure.client.smogon_client import SmogonClient
from app.infrastructure.parser.smogon_analysis_parser import SmogonAnalysisParser


class SmogonRepository:

    # 世代ID
    DEFAULT_FORMAT_ID = "gen9ou" 

    def __init__(
        self,
        client: SmogonClient,
        parser: SmogonAnalysisParser,
    ):
        self.client = client
        self.parser = parser

    def find_by_pokemon(
        self,
        pokemon_name: str,
    ) -> List[SmogonSection]:
        """
        指定フォーマットのポケモンに関する Smogon の分析記事を取得して
        SmogonSection のリストで返す
        """
        # Client 側で format_id だけで analyses JSON を取得
        raw_data = self.client.fetch_analyses(self.DEFAULT_FORMAT_ID)

        # species単位に切り出して parser に渡す
        pokemon_data = raw_data.get(pokemon_name)
        if not pokemon_data:
            # 正規化して検索（JSONキーの揺れに対応）
            norm_name = self._normalize_name(pokemon_name)
            for key in raw_data.keys():
                if self._normalize_name(key) == norm_name:
                    pokemon_data = raw_data[key]
                    break

        if not pokemon_data:
            return []

        # print(pokemon_data)
        # print(pokemon_name)
        return self.parser.parse(pokemon_data)

    @staticmethod
    def _normalize_name(name: str) -> str:
        """
        Smogon JSON のキーに合わせた正規化
        """
        n = name.strip().lower()
        n = n.replace(" ", "").replace(".", "").replace(":", "").replace("’", "'")
        return n
