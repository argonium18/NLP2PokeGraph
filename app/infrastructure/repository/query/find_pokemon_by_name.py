FIND_POKEMON_BY_NAME = """
    MATCH (p:Pokemon {name: $name})
    OPTIONAL MATCH (p)-[:OF_POKEMON]-(s)
    RETURN
    p.name AS pokemon,
    collect(s) AS sets
    """