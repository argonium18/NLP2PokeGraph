from app.infrastructure.client.smogon_client import SmogonClient
from app.infrastructure.parser.smogon_analysis_parser import SmogonAnalysisParser
from app.infrastructure.repository.smogon_repository import SmogonRepository

from app.infrastructure.repository.pokemon_master_repository import PokemonMasterRepository
from app.pipeline.ingest.smogon_normalize_service import SmogonNormalizeService
from app.pipeline.ingest.api_ingest_pipeline import ArticleLoaderService


def main():
    # ① Repository / Service を手で生成
    smogon_client = SmogonClient()
    smogon_parser = SmogonAnalysisParser()

    smogon_repository = SmogonRepository(
        client=smogon_client,
        parser=smogon_parser,
    )
    pokemon_master_repository = PokemonMasterRepository()
    smogon_normalize_service = SmogonNormalizeService()

    # ② ArticleLoaderService をインスタンス化
    article_loader = ArticleLoaderService(
        smogon_repository=smogon_repository,
        pokemon_master_repository=pokemon_master_repository,
        smogon_normalize_service=smogon_normalize_service,
    )

    # ③ 入力パラメータ
    # json_url = "https://pkmn.github.io/smogon/data/analyses/gen9ou.json"
    pokemon_name = "Clefable"

    # ④ 実行
    article = article_loader.load_smogon_article(
        pokemon_name=pokemon_name,
    )

    # ⑤ 結果確認
    print("=== Article ===")
    print(f"source: {article.source}")
    print(f"title: {article.title}")
    print("sections:")
    for section in article.sections:
        print(section)


if __name__ == "__main__":
    main()
