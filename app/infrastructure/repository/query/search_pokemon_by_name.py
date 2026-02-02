from app.infrastructure.client.neo4j_client import Neo4jClient
from typing import List, Dict, Any

def search_pokemon_by_name(
    client: Neo4jClient,
    name: str
) -> List[Dict[str, Any]]:
    cypher = """
    MATCH (p:Pokemon {name: $name})
    OPTIONAL MATCH (p)-[:OF_POKEMON]-(s)
    RETURN
    p.name AS pokemon,
    collect(s) AS sets
    """
    result = client.read(cypher, {"name": name})


    return result
