# application/usecase/search_pokemon_graph_usecase.py
from app.infrastructure.repository.pokemon_graph_repository import PokemonGraphRepository

class SearchPokemonGraphUseCase:
    def __init__(self, repository:PokemonGraphRepository):
        self.repository = repository

    def execute(self, name: str):
        pokemon = self.repository.search_by_name(name)
        return pokemon