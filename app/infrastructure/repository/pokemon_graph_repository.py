from app.infrastructure.client.neo4j_client import Neo4jClient
from app.infrastructure.repository.query.search_pokemon_by_name import search_pokemon_by_name
from app.infrastructure.repository.query.find_pokemon_by_name import FIND_POKEMON_BY_NAME
from app.infrastructure.repository.query.find_all_pokemons import FIND_ALL_POKEMONS

class PokemonGraphRepository:
    def __init__(self, neo4j_client : Neo4jClient):
        self.client = neo4j_client

    # ポケモン名で検索（0件以上返る）
    def search_by_name(self, name: str) -> list[dict]:
        rows = self.client.read(
            FIND_POKEMON_BY_NAME,
            {"name": name},
        )
        return rows

    # ポケモン全件取得
    def find_all(self) -> list[dict]:
        rows = self.client.read(FIND_ALL_POKEMONS)
        return [row["p"] for row in rows]