# application/usecase/build_graph_from_api_usecase.py

from app.pipeline.ingest.api_ingest_pipeline import ArticleLoaderService
from app.infrastructure.repository.pokemon_set_repository import PokemonSetRepository


class BuildGraphFromApiUsecase:
    def __init__(
        self,
        loader_service: ArticleLoaderService,
        pokemon_set_repository: PokemonSetRepository,
    ):
        self.loader_service = loader_service
        self.pokemon_set_repository = pokemon_set_repository

    def execute(self, pokemon_name: str) -> None:
        sets = self.loader_service.load_smogon_sets(pokemon_name)

        if not sets:
            return

        self.pokemon_set_repository.save_sets(
            pokemon_name,
            sets
        )
