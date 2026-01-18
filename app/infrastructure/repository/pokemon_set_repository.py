from app.infrastructure.client.neo4j_client import Neo4jClient
from app.infrastructure.model.pokemon_set_graph import PokemonSetGraph
from app.domain.model.pokemon_set import PokemonSet  # 追加
from app.infrastructure.model.pokemon_set_graph import MoveGraph

class PokemonSetRepository:

    def __init__(self, client: Neo4jClient):
        self.client = client

    def save_sets(self, pokemon_name: str, sets: dict[str, PokemonSet]) -> None:
        """複数の PokemonSet または PokemonSetGraph をまとめて保存"""
        for s in sets.values():
            # PokemonSetGraph に変換
            s = self._to_graph(s)
            self.save_set(s)
        print(f"{pokemon_name} の {len(sets)} セットを Neo4j に保存しました。")

    def _to_graph(self, s: PokemonSet) -> PokemonSetGraph:
        # moves の変換
        moves = []
        for i, m in enumerate(s.moves or []):
            if isinstance(m, list):
                for j, mm in enumerate(m):
                    moves.append(MoveGraph(name=mm, slot=j+1, candidate=True))
            else:
                moves.append(MoveGraph(name=m, slot=i+1, candidate=True))

        return PokemonSetGraph(
            set_id=f"{s.pokemon_name}_{s.set_name}",
            pokemon_name=s.pokemon_name,
            set_name=s.set_name,
            moves=moves,
            items=s.item or [],
            abilities=s.ability or [],
            nature=s.nature,
            role=s.role,
            hp=s.evs.hp if s.evs and s.evs.hp is not None else 0,
            atk=s.evs.atk if s.evs and s.evs.atk is not None else 0,
            def_=s.evs.def_ if s.evs and s.evs.def_ is not None else 0,
            spa=s.evs.spa if s.evs and s.evs.spa is not None else 0,
            spd=s.evs.spd if s.evs and s.evs.spd is not None else 0,
            spe=s.evs.spe if s.evs and s.evs.spe is not None else 0,
        )



    def save_set(self, s: PokemonSetGraph) -> None:
        """PokemonSetGraph を Neo4j に保存"""
        self._save_set_node(s)
        self._connect_pokemon(s)
        self._connect_items(s)
        self._connect_abilities(s)
        self._connect_moves(s)

    # ----------------
    # Private helpers
    # ----------------
    def _save_set_node(self, s: PokemonSetGraph):
        self.client.write(
            """
            MERGE (set:Set {id:$id})
            SET set.pokemon_name=$pokemon,
                set.set_name=$name,
                set.nature=$nature,
                set.role=$role,
                set.hp=$hp,
                set.atk=$atk,
                set.def_=$def_,
                set.spa=$spa,
                set.spd=$spd,
                set.spe=$spe
            """,
            {
                "id": s.set_id,
                "pokemon": s.pokemon_name,
                "name": s.set_name,
                "nature": s.nature,
                "role": s.role,
                "hp": s.hp,
                "atk": s.atk,
                "def_": s.def_,
                "spa": s.spa,
                "spd": s.spd,
                "spe": s.spe,
            },
        )

    def _connect_pokemon(self, s: PokemonSetGraph):
        self.client.write(
            """
            MERGE (p:Pokemon {name:$pokemon})
            MERGE (set:Set {id:$id})-[:OF_POKEMON]->(p)
            """,
            {"id": s.set_id, "pokemon": s.pokemon_name},
        )

    def _connect_items(self, s: PokemonSetGraph):
        for item in s.items:
            self.client.write(
                """
                MERGE (i:Item {name:$item})
                MERGE (set:Set {id:$id})-[:HOLDS]->(i)
                """,
                {"id": s.set_id, "item": item},
            )

    def _connect_abilities(self, s: PokemonSetGraph):
        for ability in s.abilities:
            self.client.write(
                """
                MERGE (a:Ability {name:$ability})
                MERGE (set:Set {id:$id})-[:HAS_ABILITY]->(a)
                """,
                {"id": s.set_id, "ability": ability},
            )

    def _connect_moves(self, s: PokemonSetGraph):
        for move in s.moves:
            self.client.write(
                """
                MERGE (m:Move {name:$name})
                MERGE (set:Set {id:$id})-[:HAS_MOVE {slot:$slot, candidate:$candidate}]->(m)
                """,
                {"id": s.set_id, "name": move.name, "slot": move.slot, "candidate": move.candidate},
            )
