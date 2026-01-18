# infrastructure/client/neo4j_client.py
from neo4j import GraphDatabase
from typing_extensions import LiteralString
from typing import Any, cast


class Neo4jClient:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def read(self, cypher: str, params: dict | None = None) -> list[dict[str, Any]]:
        with self.driver.session() as session:
            result = session.execute_read(
                lambda tx: [record.data() for record in tx.run(cast(LiteralString, cypher), params or {})]
            )
            return result

    def write(self, cypher: str, params: dict | None = None) -> None:
        with self.driver.session() as session:
            session.execute_write(
                lambda tx: tx.run(cast(LiteralString, cypher), params or {})
            )
