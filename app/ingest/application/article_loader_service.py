from app.ingest.domain.model.article import Article
from app.ingest.infrastructure.repository.smogon_repository import SmogonRepository


class ArticleLoaderService:
    def __init__(self, repository: SmogonRepository):
        self.repository = repository

    def load_smogon_article(
        self,
        json_url: str,
        pokemon_name: str,
    ) -> Article:

        sections = self.repository.find_by_pokemon(
            json_url=json_url,
            pokemon_name=pokemon_name,
        )

        return Article(
            source="smogon",
            title=pokemon_name,
            sections=sections,
        )
