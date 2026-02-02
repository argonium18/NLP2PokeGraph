from app.infrastructure.client.neo4j_client import Neo4jClient
from app.infrastructure.repository.pokemon_graph_repository import PokemonGraphRepository
from app.infrastructure.repository.pokemon_master_repository import PokemonMasterRepository

from app.infrastructure.client.smogon_client import SmogonClient
from app.infrastructure.parser.smogon_analysis_parser import SmogonAnalysisParser
from app.infrastructure.repository.smogon_repository import SmogonRepository

from app.pipeline.ingest.smogon_normalize_service import SmogonNormalizeService
from app.pipeline.ingest.smogon_translate_service import SmogonTranslateService

from app.pipeline.ingest.api_ingest_pipeline import ArticleLoaderService

from app.application.usecase.search_pokemon_graph_usecase import SearchPokemonGraphUseCase
from app.application.usecase.load_smogon_article_usecase import LoadAndRenderSmogonArticleUseCase

from app.shared.config.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


# =========================
# Neo4j 系
# =========================
neo4j_client = Neo4jClient(
    NEO4J_URI,
    NEO4J_USER,
    NEO4J_PASSWORD,
)

pokemon_graph_repo = PokemonGraphRepository(neo4j_client)
pokemon_master_repo = PokemonMasterRepository()

search_pokemon_usecase = SearchPokemonGraphUseCase(
    pokemon_graph_repo
)

# =========================
# Smogon 系
# =========================
smogon_client = SmogonClient()
smogon_parser = SmogonAnalysisParser()

smogon_repository = SmogonRepository(
    smogon_client,
    smogon_parser,
)

smogon_normalize_service = SmogonNormalizeService()
smogon_translate_service = SmogonTranslateService()

article_loader_service = ArticleLoaderService(
    smogon_repository=smogon_repository,
    pokemon_master_repository=pokemon_master_repo,
    smogon_normalize_service=smogon_normalize_service,
    smogon_translate_service=smogon_translate_service,
)

load_and_render_smogon_article_usecase = (
    LoadAndRenderSmogonArticleUseCase(
        article_loader_service
    )
)
