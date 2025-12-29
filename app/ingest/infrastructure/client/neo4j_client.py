# infrastructure/client/neo4j_client.py
from neo4j import GraphDatabase
from app.domain.model.entity import Entity

class Neo4jClient:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # -----------------------
    # 既存: 読み取り用
    # -----------------------
    def get_all_entities(self) -> list[Entity]:
        with self.driver.session() as session:
            result = session.execute_read(self._fetch_entities)
            return result

    @staticmethod
    def _fetch_entities(tx):
        query = "MATCH (e) RETURN e.name AS name, labels(e) AS type"
        result = tx.run(query)
        entities = []
        for record in result:
            # type はラベルの最初のものを使用
            entities.append(Entity(name=record["name"], type=record["type"][0]))
        return entities

    # -----------------------
    # 追加: 書き込み用
    # -----------------------
    def create_pokemon_node(self, name: str):
        query = """
        CREATE (p:Pokemon {name: $name})
        """
        with self.driver.session() as session:
            session.run(query, name=name)

    def create_move_node(self, name: str, power: int = None, type_: str = None):
        query = """
        CREATE (m:Move {name: $name, power: $power, type: $type})
        """
        with self.driver.session() as session:
            session.run(query, name=name, power=power, type=type_)

    def create_ability_node(self, name: str):
        query = """
        CREATE (a:Ability {name: $name})
        """
        with self.driver.session() as session:
            session.run(query, name=name)

    def create_relationship(self, from_name: str, rel_type: str, to_name: str, from_label="Pokemon", to_label="Move"):
        query = f"""
        MATCH (a:{from_label} {{name: $from_name}})
        MATCH (b:{to_label} {{name: $to_name}})
        CREATE (a)-[r:{rel_type}]->(b)
        """
        with self.driver.session() as session:
            session.run(query, from_name=from_name, to_name=to_name)
