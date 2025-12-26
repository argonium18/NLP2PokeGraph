from app.ingest.infrastructure.client.smogon_client import SmogonClient
from app.ingest.infrastructure.repository.smogon_repository import SmogonRepository
from app.ingest.infrastructure.translator.smogon_section_assembler import (
    SmogonSectionAssembler,
)
from app.ingest.application.article_loader_service import ArticleLoaderService


def main():
    client = SmogonClient()
    repository = SmogonRepository(client)
    assembler = SmogonSectionAssembler()

    service = ArticleLoaderService(
        repository=repository,
        assembler=assembler,
    )

    article = service.load_smogon_article(
        json_url="https://pkmn.github.io/smogon/data/analyses/gen9.json",
        pokemon_name="Abomasnow",
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
