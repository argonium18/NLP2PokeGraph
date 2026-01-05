# api_ingest_pipeline.py
from typing import Dict, Any
from app.domain.model.article import Article
from app.domain.model.pokemon_set import PokemonSet
from app.infrastructure.repository.smogon_repository import SmogonRepository
from app.infrastructure.repository.pokemon_master_repository import PokemonMasterRepository
from app.pipeline.ingest.smogon_normalize_service import SmogonNormalizeService

class ArticleLoaderService:
    def __init__(
        self,
        smogon_repository: SmogonRepository,
        pokemon_master_repository: PokemonMasterRepository,
        smogon_normalize_service: SmogonNormalizeService,
    ):
        self.smogon_repository = smogon_repository
        self.pokemon_master_repository = pokemon_master_repository
        self.smogon_normalize_service = smogon_normalize_service

    # 記事情報取得（既存）
    def load_smogon_article(self, pokemon_name: str) -> Article:


        raw_smogon = self.smogon_repository.find_by_pokemon(pokemon_name)
        # normalized = self.smogon_normalize_service.normalize(raw_smogon, master, pokemon_name)

        return Article(
            source="smogon",
            title=pokemon_name,
            sections=raw_smogon,
        )

    # 新規追加: 攻略セット情報取得
    def load_smogon_sets(self, pokemon_name: str) -> dict[str, PokemonSet]:
        master = self.pokemon_master_repository.load_all()

        sets_data = self.smogon_repository.find_sets_by_pokemon(pokemon_name)
        if not sets_data:
            return {}

        # PokemonSet に変換
        raw_sets: dict[str, PokemonSet] = {}
        for set_name, data in sets_data.items():
            raw_sets[set_name] = PokemonSet(
                pokemon_name=pokemon_name,
                set_name=set_name,
                moves=data.get("moves") or [],
                nature=data.get("nature"),
                ability=data.get("ability"),
                item=data.get("item"),
                evs=data.get("evs"),
                role=data.get("role"),
                raw=data,
            )

        # 正規化
        normalized = self.smogon_normalize_service.normalize_sets(raw_sets, master)
        return normalized
