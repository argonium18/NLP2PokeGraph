from app.domain.model.article import Article
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

    def load_smogon_article(
        self,
        pokemon_name: str,
    ) -> Article:
        # ① マスタ取得
        master = self.pokemon_master_repository.load_all()

        # ② Smogon生データ取得
        raw_smogon = self.smogon_repository.find_by_pokemon(
            pokemon_name=pokemon_name
        )


        # ④ Article に詰める
        return Article(
            source="smogon",
            title=pokemon_name,
            sections=raw_smogon,
        )

