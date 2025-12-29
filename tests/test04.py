from app.ingest.infrastructure.client.smogon_client import SmogonClient
from app.ingest.infrastructure.parser.smogon_analysis_parser import (
    SmogonAnalysisParser,
)
from app.ingest.infrastructure.repository.smogon_repository import SmogonRepository
from app.ingest.application.article_loader_service import ArticleLoaderService


def main():
    client = SmogonClient()
    parser = SmogonAnalysisParser()
    repository = SmogonRepository(client, parser)
    service = ArticleLoaderService(repository)

    # ポケモンによっては記事が記載されていないものもある

    article = service.load_smogon_article(
        json_url="https://pkmn.github.io/smogon/data/analyses/gen9.json",
        pokemon_name="Skeledirge",
    )

    print(f"Source: {article.source}")
    print(f"Title : {article.title}")
    print("-" * 50)

    for section in article.sections:
        print(
            f"[{section.kind}] tier={section.tier} "
            f"set={section.set_name}"
        )
        print(section.html[:200], "...\n")


if __name__ == "__main__":
    main()
