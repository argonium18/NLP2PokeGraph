from typing import List
from app.domain.value.smogon_section import SmogonSection
from app.infrastructure.client.smogon_client import SmogonClient
from app.infrastructure.parser.smogon_analysis_parser import (
    SmogonAnalysisParser,
)


class SmogonRepository:
    def __init__(
        self,
        client: SmogonClient,
        parser: SmogonAnalysisParser,
    ):
        self.client = client
        self.parser = parser

    def find_by_pokemon(
        self,
        json_url: str,
        pokemon_name: str,
    ) -> List[SmogonSection]:

        raw_data = self.client.fetch_analysis(json_url)
        return self.parser.parse(raw_data, pokemon_name)
