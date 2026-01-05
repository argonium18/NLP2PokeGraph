# run_smogon_sets.py
from app.infrastructure.client.smogon_client import SmogonClient
from app.infrastructure.parser.smogon_analysis_parser import SmogonAnalysisParser
from app.infrastructure.repository.smogon_repository import SmogonRepository
from app.infrastructure.repository.pokemon_master_repository import PokemonMasterRepository
from app.pipeline.ingest.api_ingest_pipeline import ArticleLoaderService
from app.pipeline.ingest.api_ingest_pipeline import SmogonNormalizeService

def main():
    # 1. Client / Parser / Repository を初期化
    smogon_client = SmogonClient()
    smogon_parser = SmogonAnalysisParser()  # 解析記事用ですが Repository に必要
    smogon_repo = SmogonRepository(client=smogon_client, parser=smogon_parser)
    pokemon_master_repo = PokemonMasterRepository()  # ダミーでも OK
    smogon_normalize_service = SmogonNormalizeService()
    loader_service = ArticleLoaderService(
        smogon_repository=smogon_repo,
        pokemon_master_repository=pokemon_master_repo,
        smogon_normalize_service=smogon_normalize_service  # 今回はセット取得のみなので None でも OK
    )

    # 2. ポケモン名を指定
    pokemon_name = "Great Tusk"

    # 3. 攻略セットを取得
    sets = loader_service.load_smogon_sets(pokemon_name)

    # 4. 結果表示
    if not sets:
        print(f"{pokemon_name} の攻略セットは見つかりませんでした。")
        return

    print(f"{pokemon_name} の攻略セット一覧:")
    for set_name, pokemon_set in sets.items():
        print(f"\n=== セット名: {set_name} ===")
        print("Moves:", pokemon_set.moves)
        print("Nature:", pokemon_set.nature)
        print("Ability:", pokemon_set.ability)
        print("Item:", pokemon_set.item)
        print("EVs:", pokemon_set.evs)
        print("Role:", pokemon_set.role)

if __name__ == "__main__":
    main()
