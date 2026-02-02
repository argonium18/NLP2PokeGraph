# application/di/container.py
from app.infrastructure.client.neo4j_client import Neo4jClient
from app.infrastructure.repository.pokemon_graph_repository import PokemonGraphRepository
from app.application.usecase.search_pokemon_graph_usecase import SearchPokemonGraphUseCase
from app.shared.config.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

# Neo4j クライアントを作成
neo4j_client = Neo4jClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

# Repository のインスタンスを作成
pokemon_graph_repo = PokemonGraphRepository(neo4j_client)

# UseCase に Repository を渡す
search_pokemon_usecase = SearchPokemonGraphUseCase(pokemon_graph_repo)

# これを Controller で import して使用
