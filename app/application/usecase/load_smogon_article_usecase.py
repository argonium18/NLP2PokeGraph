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

        # CLI表示用の文字列を作成
        lines = [
            "=== Article ===",
            f"source: {article.source}",
            f"title: {article.title}",
            "sections:",
        ]
        for section in article.sections:
            lines.append(str(section))

        # 標準出力
        print("\n".join(lines))

        # 文字列として返す
        return "\n".join(lines)
