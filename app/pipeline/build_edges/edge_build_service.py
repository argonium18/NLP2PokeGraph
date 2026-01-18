from app.infrastructure.client.neo4j_client import Neo4jClient
from app.pipeline.ingest.api_ingest_pipeline import ArticleLoaderService

def build_sets_graph(loader_service: ArticleLoaderService, neo4j_client: Neo4jClient, pokemon_name: str):
    # 攻略セット取得
    sets = loader_service.load_smogon_sets(pokemon_name)

    if not sets:
        print(f"{pokemon_name} のセットは見つかりませんでした。")
        return

    # Neo4j に格納
    neo4j_client.save_pokemon_sets(sets)
    print(f"{pokemon_name} のセットを Neo4j に格納しました。")
