# scripts/run_build_sets_graph.py

from app.infrastructure.client.neo4j_client import Neo4jClient
from app.infrastructure.client.smogon_client import SmogonClient
from app.infrastructure.parser.smogon_analysis_parser import SmogonAnalysisParser
from app.infrastructure.repository.smogon_repository import SmogonRepository
from app.infrastructure.repository.pokemon_master_repository import PokemonMasterRepository
from app.infrastructure.repository.pokemon_set_repository import PokemonSetRepository
from app.application.usecase.port.pokemon_set_repository import PokemonSetRepository as PokemonSetRepositoryPort
from app.pipeline.ingest.api_ingest_pipeline import ArticleLoaderService
from app.pipeline.ingest.smogon_normalize_service import SmogonNormalizeService
from app.pipeline.ingest.smogon_translate_service import SmogonTranslateService
from app.application.usecase.build_graph_from_api_usecase import BuildGraphFromApiUsecase
from app.shared.config.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


def main() -> None:
    # ----------------------
    # クライアント / Repository 準備
    # ----------------------
    neo4j_client = Neo4jClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    smogon_client = SmogonClient()
    smogon_parser = SmogonAnalysisParser()
    smogon_repo = SmogonRepository(smogon_client, smogon_parser)
    pokemon_master_repo = PokemonMasterRepository()

    normalize_service = SmogonNormalizeService()
    smogon_translate_service = SmogonTranslateService()

    loader_service = ArticleLoaderService(
        smogon_repository=smogon_repo,
        pokemon_master_repository=pokemon_master_repo,
        smogon_normalize_service=normalize_service,
        smogon_translate_service=smogon_translate_service
    )

    # ----------------------
    # PokemonSetRepository (Port 実装)
    # ----------------------
    # 型チェック用に Port で型注釈
    pokemon_set_repo: PokemonSetRepositoryPort = PokemonSetRepository(neo4j_client)

    # ----------------------
    # Usecase 実行
    # ----------------------
    usecase = BuildGraphFromApiUsecase(
        loader_service=loader_service,
        pokemon_set_repository=pokemon_set_repo
    )

    # 例: Great Tusk のセットを取得して Neo4j に格納
    usecase.execute("Great Tusk")

    # ----------------------
    # 後片付け
    # ----------------------
    neo4j_client.close()
    print("完了！")


if __name__ == "__main__":
    main()
