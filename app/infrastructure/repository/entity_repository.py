# infrastructure/repository/entity_repository.py
from typing import List
from app.domain.model.entity import Entity
from app.infrastructure.client.neo4j_client import Neo4jClient


class EntityRepository:
    """
    Neo4j に存在するエンティティの参照専用 Repository
    （NLP / 正規化用途）
    """

    def __init__(self, client: Neo4jClient):
        self.client = client

    def list_all(self) -> List[Entity]:
        rows = self.client.read(
            "MATCH (e) RETURN e.name AS name, labels(e) AS labels"
        )
        return [
            Entity(name=row["name"], type=row["labels"][0])
            for row in rows
        ]

    def find_in_text(self, text: str) -> List[Entity]:
        entities = self.list_all()
        return [e for e in entities if e.name in text]
