from app.pipeline.ingest.api_ingest_pipeline import ArticleLoaderService


class LoadAndRenderSmogonArticleUseCase:
    def __init__(self, article_loader_service: ArticleLoaderService):
        self.article_loader_service = article_loader_service

    def execute(
        self,
        pokemon_name: str,
    ) -> str:
        """
        Smogon 記事を取得し、CLI表示用の文字列を生成する
        """
        article = self.article_loader_service.load_smogon_article(
            pokemon_name=pokemon_name,
        )

        lines: list[str] = []

        lines.append(f"Source: {article.source}")
        lines.append(f"Title : {article.title}")
        lines.append("-" * 50)

        for section in article.sections:
            lines.append(
                f"[{section.kind}] tier={section.tier} "
                f"set={section.set_name}"
            )
            lines.append(section.html[:200] + "...\n")

        return "\n".join(lines)
