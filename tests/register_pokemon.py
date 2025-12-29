# application/add_pokemon_nodes.py
from app.ingest.infrastructure.client.neo4j_client import Neo4jClient
from app.shared.logging.logger import logger
from app.shared.config.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


def main():

    # 登録したいポケモンのリスト
    pokemon_list = [
        "Pikachu",
        "Bulbasaur",
        "Charmander",
        "Squirtle",
        "Jigglypuff"
    ]

    # Neo4jClient初期化
    neo4j_client = Neo4jClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    # リストの各ポケモンを登録
    for pokemon_name in pokemon_list:
        neo4j_client.create_pokemon_node(pokemon_name)
        print(f"Created node for {pokemon_name}")

    neo4j_client.close()
    logger.info(f"Loaded {len(pokemon_list)} entities from Neo4j")


if __name__ == "__main__":
    main()
