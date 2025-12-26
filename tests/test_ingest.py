# scripts/test_ingest.py
from app.ingest.application.article_loader_service import ArticleLoaderService
from app.ingest.infrastructure.client.smogon_client import SmogonClient
from app.ingest.infrastructure.parser.html_text_parser import HtmlTextParser
from app.ingest.infrastructure.repository.smogon_repository import SmogonRepository

URL = "https://www.smogon.com/dex/sv/pokemon/abomasnow/"

def main():
    client = SmogonClient()
    parser = HtmlTextParser()
    repo = SmogonRepository(client, parser)
    loader = ArticleLoaderService(repo)

    article = loader.load(URL)

    print("SOURCE:", article.source)
    print("TITLE :", article.title)
    print("HTML   :", article.raw_html[:500], "...")

if __name__ == "__main__":
    main()
