from typing import List
from app.domain.model.entity import Entity
from neo4j import GraphDatabase

class Neo4jEntityRepository:
    """
    Neo4j からポケモン/技/アイテムのエンティティを取得するリポジトリ
    """

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_all_entities(self) -> List[Entity]:
        """
        Neo4j に登録されている全エンティティを取得
        """
        with self.driver.session() as session:
            return session.read_transaction(self._fetch_entities)

    @staticmethod
    def _fetch_entities(tx):
        query = "MATCH (e) RETURN e.name AS name, labels(e) AS type"
        result = tx.run(query)
        entities = []
        for record in result:
            entities.append(Entity(name=record["name"], type=record["type"][0]))
        return entities

    def find_candidates_in_text(self, text: str) -> List[Entity]:
        """
        文中に出現するNeo4jエンティティを列挙
        """
        all_entities = self.get_all_entities()
        candidates = [e for e in all_entities if e.name in text]
        return candidates
    

